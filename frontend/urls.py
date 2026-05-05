from django.urls import path
from .views import *

urlpatterns = [
    path("", index_view, name="dashboard"),
    path("login", login_view, name="login-page"),
    path("leaves/request",request_leave_view,name="leave-request"),
    path("leaves/all",leave_history_view,name="leave-history"),
    path("leaves/<int:pk>", leave_view,name="leave-detail"),
    path("leaves/pending", pending_leaves_view,name="pending-leaves"),
]
