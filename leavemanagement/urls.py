from leavemanagement.views import *
from django.urls import path

urlpatterns = [
    path('leaves/',LeaveListCreateView.as_view(),name='viewall-create-leave'),
    path('leaves/<int:pk>/',LeaveRetrieveUpdateView.as_view(),name='viewone-update-leave')
]
