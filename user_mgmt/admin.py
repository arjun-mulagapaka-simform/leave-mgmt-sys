from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_mgmt.forms import *
from user_mgmt.models import *


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee

    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("first_name", "last_name")}),
        ("Company", {"fields": ("department", "role", "reporting_manager")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "department",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    ordering = ("email",)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    model = Role

    list_display = ("id", "name")

    ordering = ("id",)


# admin.site.register(Employee)
admin.site.register(Department)
