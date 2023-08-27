from .models import LeaveRequest, LeaveBalance


def get_leaves_by_status(user, status):
    return LeaveRequest.objects.filter(employee__user=user, status=status).count()


def get_total_leaves_left_for_user(user):
    leaves_balance = LeaveBalance.objects.filter(employee__user=user).first()
    return leaves_balance.available_balance
