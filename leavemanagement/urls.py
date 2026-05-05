from leavemanagement.views import *
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"leaves", LeaveViewSet, basename="myleaves")

urlpatterns = [
    path("pending/", PendingLeavesView.as_view(), name="pending-leaves"),
    path("<int:pk>/approve/", ApproveOrRejectLeaveView.as_view(), name="approve-leave"),
    path("<int:pk>/reject/", ApproveOrRejectLeaveView.as_view(), name="reject-leave"),
    path("balance/", GetLeaveBalance.as_view(), name="leave-balance"),
    path("", include(router.urls)),
]
