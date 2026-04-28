from rest_framework import generics, viewsets
from user_mgmt.models import Employee
from leavemanagement.models import LeaveLog
from leavemanagement.serializers import LeaveLogSerializer
from common.permissions import *
from common.scopeservice import *


class LeaveViewSet(viewsets.ModelViewSet):
    """
    Default pagination and filtering applied.
    """

    serializer_class = LeaveLogSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        leaves = LeaveLog.objects.filter(employee=self.request.user)
        return leaves

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)


class PendingLeavesView(generics.ListAPIView):
    """
    Pending leaves class.
    """

    serializer_class = LeaveLogSerializer
    permission_classes = [IsReportingManagerOrManagerOrHR]

    def get_queryset(self):
        employees = ScopeOfEmployee.get_employee_scope(request=self.request)
        leaves = LeaveLog.objects.filter(employee__in = employees)
        return leaves

