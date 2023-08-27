from django.contrib.auth.models import User
from django.db import models, transaction


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{str(self.user)}-{str(self.position)}"


class LeaveRequest(models.Model):
    leave_types = (
        ("vacation", "Vacation"),
        ("sick", "Sick Leave"),
        # Add more leave types as needed
    )
    status = (("Accepted", "Accepted"), ("Pending", "Pending"))

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(choices=leave_types, max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=status, default="Pending")
    comments = models.TextField()

    @transaction.atomic
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.status == "Accepted":
            leave_balance = LeaveBalance.objects.filter(
                employee__id=self.employee.id
            ).first()
            if leave_balance:
                leave_balance.leave_type = self.leave_type
                leave_balance.available_balance -= 1
                leave_balance.save()
        super().save()

    def __str__(self):
        return f"{str(self.employee)}"


class LeaveBalance(models.Model):
    leave_types = (
        ("vacation", "Vacation"),
        ("sick", "Sick Leave"),
        # Add more leave types as needed
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(choices=leave_types, max_length=20)
    available_balance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{str(self.employee)}-{str(self.available_balance)}"
