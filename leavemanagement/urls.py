from leavemanagement.views import *
from django.urls import path,include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"leaves",LeaveViewSet,basename="myleaves")

urlpatterns = [
    path("leaves/pending/",PendingLeavesView.as_view(),name="pending-leaves"),
    path("",include(router.urls))
]
