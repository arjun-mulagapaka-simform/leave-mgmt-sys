from rest_framework import serializers
from user_mgmt.models import *

class EmployeeSerializer(serializers.ModelSerializer):
    '''
        Serializer class for Employee model
    '''
    class Meta:
        model = Employee
        fields = '__all__'
    
    def validate(self, attrs):
        '''
            Validating the incoming employee data
        '''
        #checking if dept provided exists
        dept_data = attrs.get('department')
        dept = Department.objects.get(pk=dept_data.id)
        if dept is None:
            raise serializers.ValidationError({'department':"No department with specified id."})
        
        #checking if reporting manager exists if provided
        reporting_mngr = attrs.get('reporting_manager')
        if reporting_mngr is not None:
            mngr = Employee.objects.get(pk=reporting_mngr.id)
            if mngr is None:
                raise serializers.ValidationError({'reporting_manager':"Reporting manager details are incorrect."})
            if mngr.id == attrs.get('id'):
                raise serializers.ValidationError({'reporting_manager':"Cannot be your own reporting manager."})
            if mngr.department_id != dept_data.id:
                raise serializers.ValidationError({'reporting_manager':"Reporting manager should belong to same department."})
            if mngr.role.name != 'Reporting Manager':
                raise serializers.ValidationError({'reporting_manager':"Assigned employee is not a reporting manager."})
        
        return attrs
    
class DepartmentSerializer(serializers.ModelSerializer):
    '''
        Serializer class for Department model
    '''
    class Meta:
        model = Department
        fields = "__all__"
    
    def validate(self, attrs):
        '''
            Validating incoming department data
        '''
        #checking if reporting manager exists if provided
        mngr = attrs.get('manager')
        if mngr is not None:
            mngrobj = Employee.objects.get(pk=mngr.id)
            if mngrobj is None:
                raise serializers.ValidationError({'manager':"Manager details are incorrect."})
            if mngrobj.role.name != 'Manager':
                raise serializers.ValidationError({'reporting_manager':"Assigned employee is not a reporting manager."})
            
        #checking if hr exists if provided
        hr = attrs.get('hr')
        if hr is not None:
            hrobj = Employee.objects.get(pk=hr.id)
            if hrobj is None:
                raise serializers.ValidationError({'hr':"HR details are incorrect."})
            if hrobj.role.name != 'HR':
                raise serializers.ValidationError({'reporting_manager':"Assigned employee is not a reporting manager."})
        
        return attrs