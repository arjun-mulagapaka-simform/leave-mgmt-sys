from rest_framework import generics
from user_mgmt.models import Employee
from leavemanagement.serializers import LeaveLogSerializer

class LeaveListCreateView(generics.ListCreateAPIView):
    '''
        GET all and POST method views for LeaveLog model
    '''
    serializer_class = LeaveLogSerializer
    
    def get_queryset(self):
        return Employee.objects.filter(id=self.request.user.id)

class LeaveRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    '''
        GET one and PUT, PATCH method views for LeaveLog model
    '''
    serializer_class = LeaveLogSerializer
    
    def get_queryset(self):
        return Employee.objects.filter(id=self.request.user.id)
