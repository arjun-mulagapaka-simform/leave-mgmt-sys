from leavemanagement.views import *
from django.urls import path,include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"leaves",LeaveViewSet,basename="myleaves")

urlpatterns = [
    path("leaves/pending/",PendingLeavesView.as_view(),name="pending-leaves"),
    path("leaves/<int:pk>/approve/",ApproveOrRejectLeaveView.as_view(),name="approve-leave"),
    path("leaves/<int:pk>/reject/",ApproveOrRejectLeaveView.as_view(),name="reject-leave"),
    path("leaves/balance/", GetLeaveBalance.as_view(), name="leave-balance"),
    path("",include(router.urls))
]
