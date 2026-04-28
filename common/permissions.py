from rest_framework import permissions
from user_mgmt.models import *
from common.roles import roles

class IsEmployee(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is an employee
    '''
    def has_permission(self, request, view):
        if request.user.role.name in roles.values():
            return True
        return False
    
class IsReportingManager(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is a reporting manager
    '''
    def has_permission(self, request, view):
        if request.user.role.name == roles['reporting manager']:
            return True
        return False
    
class IsManager(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is a manager
    '''
    def has_permission(self, request, view):
        if request.user.role.name == roles['manager']:
            return True
        return False
    
class IsHR(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is an HR
    '''
    def has_permission(self, request, view):
        if request.user.role.name == roles['hr']:
            return True
        return False

class IsHrOfDepartment(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is HR for given department
    '''
    def has_object_permission(self, request, view, obj):
        if request.user.role.name == roles['hr']:
            if request.user.id == obj.id:
                return True
        return False
    
class IsManagerOfDepartment(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is Manager for given department
    '''
    def has_object_permission(self, request, view, obj):
        if request.user.role.name == roles['manager']:
            if request.user.id == obj.id:
                return True
        return False

class IsReportingManagerOfEmployee(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is Reporting Manager of given employee
    '''
    def has_object_permission(self, request, view, obj):
        if request.user.role.name == roles['reporting manager']:
            if request.user.id == obj.reporting_manager.id:
                return True
        return False

class IsSelfOrApprover(permissions.IsAuthenticated):
    '''
        Authenticate whether requested user is the owner or approver of requested leave object
    '''
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.employee.id:
            return True
        return False