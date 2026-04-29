from leavemanagement.models import *


class LeaveBalance:
    """
    Service class which returns leave balance for requested user.
    """

    @staticmethod
    def get_balance(user):
        leave_requests = LeaveLog.objects.filter(employee=user)
        leaves_taken = {"paid": 0, "unpaid": 0, "compensation": 0, "incident": 0}
        for leave in leave_requests:
            if leave.status == "apr":
                leaves_taken[leave.leave_type] += 1

        leavepolicies = LeavePolicy.objects.all()
        pendingleaves = {"paid": 0, "unpaid": 0, "compensation": 0, "incident": 0}
        for leavepolicy in leavepolicies:
            pendingleaves[leavepolicy.leave_type] = (
                leavepolicy.given_days - leaves_taken[leavepolicy.leave_type]
            )

        return pendingleaves
