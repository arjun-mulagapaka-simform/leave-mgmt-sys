from rest_framework import permissions
from user_mgmt.models import *

class IsEmployee(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is an employee
    '''
    def has_permission(self, request, view):
        user = Employee.objects.get(pk=request.user.id)
        if user.role.name in ['employee','reporting manager','manager','hr']:
            return True
        return False
    
class IsReportingManager(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is a reporting manager
    '''
    def has_permission(self, request, view):
        user = Employee.objects.get(pk=request.user.id)
        if user.role.name == 'reporting manager':
            return True
        return False
    
class IsManager(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is a manager
    '''
    def has_permission(self, request, view):
        user = Employee.objects.get(pk=request.user.id)
        if user.role.name == 'manager':
            return True
        return False
    
class IsHR(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is an HR
    '''
    def has_permission(self, request, view):
        user = Employee.objects.get(pk=request.user.id)
        if user.role.name == 'hr':
            return True
        return False

class IsHrOfDepartment(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is HR for given department
    '''
    def has_permission(self, request, view):
        user = Employee.objects.get(pk=request.user.id)
        if user.role.name == 'hr':
            if user.department.id == request.department.id:
                return True
        return False
    
class IsManagerOfDepartment(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is Manager for given department
    '''
    def has_permission(self, request, view):
        user = Employee.objects.get(pk=request.user.id)
        if user.role.name == 'manager':
            if user.department.id == request.department.id:
                return True
        return False

class IsReportingManagerOfEmployee(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is Reporting Manager of given employee
    '''
    def has_permission(self, request, view):
        user = Employee.objects.get(pk=request.user.id)
        if user.role.name == 'reporting manager':
            if request.employee.reporting_manager.id == user.id:
                return True
        return False

class IsSelfOrApprover(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is the owner or approver of requested leave object
    '''
    def has_permission(self, request, view):
        if request.user.id == request.leave.employee.id:
            return True
        return False