from leavemanagement.models import LeaveLog
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from celery import shared_task
from leave_mgmt_sys import settings


@shared_task
def send_leave_request_mail(user_id, reason, start_date, end_date):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    employee = User.objects.get(id=user_id)

    if start_date == end_date:
        msg = f"Hello,\n\t{employee.first_name} {employee.last_name} has requested for a leave on date {start_date}. The reason mentioned is {reason}.\nThank you!"
    else:
        msg = f'Hello,\n\t{employee.first_name} {employee.last_name} has requested for a leave from date {start_date} to {end_date}. The reason mentioned is\n"{reason}"\nThank you!'

    send_mail(
        subject="Leave request",
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["tesov11693@pertok.com"],
    )


@shared_task
def approve_reject_mail(leave_id, status, rejection_reason, actioned_by_id):

    User = get_user_model()

    instance = LeaveLog.objects.get(id=leave_id)
    employee = instance.employee
    actioned_by = User.objects.get(id=actioned_by_id)

    if status == "apr":
        msg = f"Hello {employee.first_name},\nYour leave on {instance.start_date} has been approved by {actioned_by.first_name}."
        subject = f"Leave approved for {instance.start_date}"
    else:
        msg = f'Hello {employee.first_name},\nYour leave on {instance.start_date} has been rejected.\nReason:\n"{rejection_reason}"'
        subject = f"Leave rejected for {instance.start_date}"

    send_mail(subject, msg, settings.EMAIL_HOST_USER, ["tesov11693@pertok.com"])
