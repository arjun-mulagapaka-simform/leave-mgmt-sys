from rest_framework import serializers
from leavemanagement.models import *
from user_mgmt.models import *
from datetime import date


class EmployeeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name"]


class LeaveLogSerializer(serializers.ModelSerializer):
    """
    Serializer class for the model LeaveLog
    """

    actioned_by = EmployeeMiniSerializer(read_only=True)

    class Meta:
        model = LeaveLog
        fields = "__all__"
        read_only_fields = ["employee"]

    def validate(self, attrs):
        """
        Validating incoming Leave data
        """
        # checking if employee provided exists
        emp_data = attrs.get("employee")
        if emp_data is not None:
            emp = Employee.objects.get(pk=emp_data.id)
            if emp is None:
                raise serializers.ValidationError(
                    {"employee": "Employee does not exist."}
                )

        # checking if approved_by employee exists
        approver_data = attrs.get("approved_by")
        if approver_data is not None:
            approver = Employee.objects.get(pk=approver_data.id)
            if approver is None:
                raise serializers.ValidationError(
                    {"approved_by": "Approver employee does not exist."}
                )

        # checking if start date is invalid
        start_date = attrs.get("start_date")
        if start_date is not None:
            if (start_date - date.today()).days > 45:
                raise serializers.ValidationError(
                    {
                        "start_date": "Start date cannot be more than 45 days ahead of today."
                    }
                )
            if start_date < date.today():
                raise serializers.ValidationError(
                    {"start_date": "Start date cannot be in the past."}
                )

        # checking if end date is invalid
        end_date = attrs.get("end_date")
        if end_date is not None:
            if (end_date - start_date).days < 0:
                raise serializers.ValidationError(
                    {"end_date": "End date cannot be before start date."}
                )

        return attrs
