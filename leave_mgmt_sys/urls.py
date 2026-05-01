from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user_mgmt.urls')),
    path('leaves/',include('leavemanagement.urls')),
    path('',include('frontend.urls'))
]
