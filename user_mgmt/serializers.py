from rest_framework import serializers
from user_mgmt.models import *
from common.roles import roles


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer class for Employee model
    """

    class Meta:
        model = Employee
        fields = ["email","first_name","last_name","department","reporting_manager","role"]

    def validate(self, attrs):
        """
        Validating the incoming employee data
        """
        employee = self.instance
        
        # checking if dept provided exists
        dept_data = attrs.get("department")
        if dept_data is not None:
            dept = Department.objects.get(pk=dept_data.id)
            if dept is None:
                raise serializers.ValidationError(
                    {"department": "No department with specified id."}
                )

        # checking if reporting manager exists if provided
        reporting_mngr = attrs.get("reporting_manager")
        if reporting_mngr is not None:
            rmngr = Employee.objects.get(pk=reporting_mngr.id)
            if rmngr is None:
                raise serializers.ValidationError(
                    {"reporting_manager": "Reporting manager details are incorrect."}
                )
            if rmngr.id == employee.id:
                raise serializers.ValidationError(
                    {"reporting_manager": "Cannot be your own reporting manager."}
                )
            if rmngr.department != employee.department:
                raise serializers.ValidationError(
                    {
                        "reporting_manager": "Reporting manager should belong to same department."
                    }
                )
            if rmngr.role.name != roles["reporting manager"]:
                raise serializers.ValidationError(
                    {
                        "reporting_manager": "Assigned employee is not a reporting manager."
                    }
                )

        return attrs
