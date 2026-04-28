from common.scopeservice import ScopeOfEmployee
from common.permissions import *
from rest_framework import generics
from user_mgmt.serializers import *


class EmployeeListView(generics.ListAPIView):
    """
    List all the employees based on scope of requested user.
    Paginated by Default Pagination and Filtered by Default
    Filtering.
    """

    serializer_class = EmployeeSerializer
    permission_classes = [IsReportingManagerOrManagerOrHR]
    filterset_fields = ['first_name','last_name','department']

    def get_queryset(self):
        employees = ScopeOfEmployee.get_employee_scope(request=self.request)
        return employees

class EmployeeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve the requested employee based on scope of requested user.
    """

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        employees = ScopeOfEmployee.get_employee_scope(request=self.request)
        return employees
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsReportingManagerOrManagerOrHR()]
        elif self.request.method in ['PUT','PATCH']:
            return [IsManager()]
        return super().get_permissions()