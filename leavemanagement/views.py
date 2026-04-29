from rest_framework import generics, viewsets, views
from leavemanagement.models import *
from leavemanagement.serializers import LeaveLogSerializer
from common.permissions import *
from common.scopeservice import *
from rest_framework.status import *
from rest_framework.response import Response
from leavemanagement.services.leavebalanceservice import *
from leavemanagement.tasks import *


class LeaveViewSet(viewsets.ModelViewSet):
    """
    Default pagination and filtering applied.
    """

    serializer_class = LeaveLogSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        leaves = LeaveLog.objects.filter(employee=self.request.user)
        return leaves

    def is_overlapping(self, new_start_date, new_end_date, existing_leaves):
        """
        Check for overlapping leaves
        """
        if existing_leaves.filter(
            start_date__lte=new_end_date, start_date__gte=new_start_date
        ).exists():
            return True
        elif existing_leaves.filter(
            start_date__lte=new_start_date, end_date__gte=new_end_date
        ).exists():
            return True
        elif existing_leaves.filter(
            end_date__gte=new_start_date, end_date__lte=new_end_date
        ).exists():
            return True
        return False

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # overlapping leaves logic
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        same_user_leaves = LeaveLog.objects.filter(employee=request.user)
        if same_user_leaves.exists():
            try:
                start_date_same_leave = same_user_leaves.get(start_date=start_date)
                return Response(
                    f"You already have a leave on given start date until {start_date_same_leave.end_date}.",
                    status=HTTP_400_BAD_REQUEST,
                )
            except:
                pass

            if self.is_overlapping(start_date, end_date, same_user_leaves):
                return Response(
                    "You are trying to create an overlapping leave which is not allowed.",
                    status=HTTP_400_BAD_REQUEST,
                )

        # leave span request logic
        leave_type = data.get("leave_type")
        leavepolicy = LeavePolicy.objects.get(leave_type=leave_type)
        if (end_date - start_date).days > leavepolicy.given_days:
            return Response(
                f"You can have only {leavepolicy.given_days} days for {leave_type} leave. Please change duration.",
                status=HTTP_400_BAD_REQUEST,
            )

        # weekdays validation
        if start_date.weekday() == 6:
            return Response(
                "Your start date is set to Sunday. Please change.",
                status=HTTP_400_BAD_REQUEST,
            )
        if end_date.weekday() == 6:
            return Response(
                "Your end date is set to Sunday. Please change.",
                status=HTTP_400_BAD_REQUEST,
            )

        # leave balance logic
        pendingleaves = LeaveBalance.get_balance(request.user)
        if pendingleaves[leave_type] < ((end_date - start_date).days + 1):
            return Response(
                f"You only have {pendingleaves[leave_type]} {leave_type} leaves remaining.",
                HTTP_400_BAD_REQUEST,
            )

        serializer.save(employee=request.user)
        reason = data.get("reason")
        try:
            send_leave_request_mail.delay(request.user.id, reason, start_date, end_date)
        except:
            pass
        finally:
            return Response(serializer.data, status=HTTP_200_OK)


class PendingLeavesView(generics.ListAPIView):
    """
    Pending leaves class.
    """

    serializer_class = LeaveLogSerializer
    permission_classes = [IsReportingManagerOrManagerOrHR]

    def get_queryset(self):
        employees = ScopeOfEmployee.get_employee_scope(request=self.request)
        leaves = LeaveLog.objects.filter(employee__in=employees).filter(status="pen")
        return leaves


class ApproveOrRejectLeaveView(generics.UpdateAPIView):
    """
    Approve leaves class.
    """

    serializer_class = LeaveLogSerializer
    permission_classes = [IsReportingManagerOrManagerOrHR]

    def get_queryset(self):
        employees = ScopeOfEmployee.get_employee_scope(request=self.request)
        leaves = LeaveLog.objects.filter(employee__in=employees)
        return leaves

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if instance.status != "pen":
            return Response(
                {"detail": "Leave request already acknowledged"},
                status=HTTP_400_BAD_REQUEST,
            )

        if instance.employee == request.user:
            return Response(
                {"detail": "Cannot approve your own leave request."},
                status=HTTP_400_BAD_REQUEST,
            )

        new_status = data.get("status")
        rejection_reason = data.get("rejection_reason")

        if new_status == "rej" and not rejection_reason:
            return Response(
                {"detail": "Provide a rejection reason."}, status=HTTP_400_BAD_REQUEST
            )

        serializer.save(actioned_by=request.user)
        try:
            approve_reject_mail.delay(instance.id, new_status, rejection_reason, request.user.id)
        except Exception as e:
            print(e)
        finally:
            return Response(serializer.data, status=HTTP_200_OK)


class GetLeaveBalance(views.APIView):
    """
    Get remaining leave balance for user.
    """

    permission_classes = [IsEmployee]

    def get(self, request, format=None):
        pendingleaves = LeaveBalance.get_balance(request.user)

        return Response({"leave balance": pendingleaves}, status=HTTP_200_OK)
