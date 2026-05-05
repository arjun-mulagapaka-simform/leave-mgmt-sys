from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from user_mgmt.views import *

app_name = "usermanagement"

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", TokenBlacklistView.as_view(), name="logout"),
    path("api/me",me, name="logged-in-user-detail"),
    # employee manipulation urls
    path("employees/", EmployeeListView.as_view(), name="list-employees"),
    path(
        "employees/<int:pk>/",
        EmployeeRetrieveUpdateView.as_view(),
        name="retrieve-employee",
    )
]
