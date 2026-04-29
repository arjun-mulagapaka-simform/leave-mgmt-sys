from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from common.roles import roles


class EmployeeManager(BaseUserManager):
    """
    Custom manager for Employee
    """

    def create_user(
        self,
        email,
        first_name,
        last_name,
        department_id,
        role_id,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            department_id=department_id,
            role_id=role_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password,
        department_id,
        role_id,
        first_name=None,
        last_name=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)  # necessary for access to admin site
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        extra_fields.setdefault(
            "is_superuser", True
        )  # provides all permissions to the user
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            department_id=department_id,
            role_id=role_id,
            **extra_fields
        )


class Employee(AbstractBaseUser, PermissionsMixin):
    """
    Class for storing employee details
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    department = models.ForeignKey("Department", on_delete=models.PROTECT)
    reporting_manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    role = models.ForeignKey("Role", on_delete=models.PROTECT)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["department_id", "role_id", "first_name", "last_name"]

    objects = EmployeeManager()

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "employee"
        verbose_name_plural = "Employees"
        ordering = ["id"]

    def __str__(self):
        return self.first_name + " " + self.last_name

    def clean(self):
        """
        Validating the incoming employee data
        """
        super().clean()
        # checking if dept provided exists
        dept_data = self.department
        dept = Department.objects.get(pk=dept_data.id)
        if dept is None:
            raise ValidationError({"department": "No department with specified id."})

        # checking if reporting manager exists if provided
        reporting_mngr = self.reporting_manager
        if reporting_mngr is not None:
            mngr = Employee.objects.get(pk=reporting_mngr.id)
            if mngr is None:
                raise ValidationError(
                    {"reporting_manager": "Reporting manager details are incorrect."}
                )
            if mngr.id == self.id:
                raise ValidationError(
                    {"reporting_manager": "Cannot be your own reporting manager."}
                )
            if mngr.department_id != dept_data.id:
                raise ValidationError(
                    {
                        "reporting_manager": "Reporting manager should belong to same department."
                    }
                )
            if mngr.role.name != roles["reporting manager"]:
                raise ValidationError(
                    {
                        "reporting_manager": "Assigned employee is not a reporting manager."
                    }
                )


class Department(models.Model):
    """
    Class for storing department details
    """

    name = models.CharField(max_length=50, unique=True)
    manager = models.OneToOneField(
        "Employee",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="manager",
    )
    hr = models.OneToOneField(
        "Employee", on_delete=models.SET_NULL, blank=True, null=True, related_name="hr"
    )

    class Meta:
        db_table = "department"
        verbose_name_plural = "Departments"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        """
        Validating incoming department data
        """
        super().clean()
        # checking if reporting manager exists if provided
        mngr = self.manager
        if mngr is not None:
            mngrobj = Employee.objects.get(pk=mngr.id)
            if mngrobj is None:
                raise ValidationError({"manager": "Manager details are incorrect."})
            if mngrobj.role.name != roles["manager"]:
                raise ValidationError(
                    {"manager": "Assigned employee is not a manager."}
                )

        # checking if hr exists if provided
        hr = self.hr
        if hr is not None:
            hrobj = Employee.objects.get(pk=hr.id)
            if hrobj is None:
                raise ValidationError({"hr": "HR details are incorrect."})
            if hrobj.role.name != roles["hr"]:
                raise ValidationError({"hr": "Assigned employee is not an HR."})


class Role(models.Model):
    """
    Class to store various roles
    """

    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "role"
        verbose_name_plural = "Roles"
        ordering = ["name"]

    def __str__(self):
        return self.name
