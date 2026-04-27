from django.db import models
from django.core.exceptions import ValidationError

class LeaveTypeEnum(models.TextChoices):
    """
    Centralized enum for leave types
    """

    PAID = "paid"
    UNPAID = "unpaid"
    COMPENSATION = "compensation"  # leaves which you can avail as a bonus for work done
    INCIDENT = "incident"  # leaves in incidents like Maternity Period, etc.


class LeaveLog(models.Model):
    """
    Model to store history of leaves
    """

    status_options = (("pen", "Pending"), ("apr", "Approved"))

    employee = models.ForeignKey(
        "user_mgmt.Employee", on_delete=models.CASCADE, related_name="leaves"
    )
    leave_type = models.CharField(max_length=15, choices=LeaveTypeEnum.choices)
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    status = models.CharField(
        max_length=10,
        choices=status_options,
        default=status_options[0],
        blank=True,
        null=True,
    )
    reason = models.CharField(max_length=250)
    approved_by = models.ForeignKey(
        "user_mgmt.Employee", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Leaves"
        db_table = "leavelog"

    def __str__(self):
        return self.employee + " took leave on: " + self.start_date


class LeavePolicy(models.Model):
    """
    Model to store various leave policies
    """

    name = models.CharField(max_length=30)
    given_days = models.IntegerField()
    leave_type = models.CharField(max_length=15, choices=LeaveTypeEnum.choices, unique=True)

    class Meta:
        verbose_name_plural = "Leave Policies"
        db_table = "leavepolicy"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.given_days < 0:
            raise ValidationError("Leaves cannot be in negative.")