from user_mgmt.models import *
from common.roles import roles

class ScopeOfEmployee:
    '''
        A service class that returns the scope of employees 
        for currently authenticated user.
    '''
    def get_employee_scope(self,request):
        role = request.user.role.name
        if role.name == roles['employee']:
            return request.user
        if role.name == roles['reporting manager']:
            return Employee.objects.filter(reporting_manager = request.user)
        if role.name == roles['manager']:
            return Employee.objects.filter(department = request.user.department)
        if role.name == roles['hr']:
            hr_department = Department.objects.filter(hr = request.user) #finding department for which he/she is HR
            return Employee.objects.filter(department = hr_department)
        