from django import forms

from .models import LeaveRequest


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        LEAVE_CHOICES = (
            ("Vacation", "Vacation"),
            ("Sick", "Sick"),
        )
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "comments"]
        widgets = {
            "leave_type": forms.Select(
                choices=LEAVE_CHOICES, attrs={"class": "form-control"}
            ),
            "start_date": forms.TextInput(attrs={"class": "form-control "}),
            "end_date": forms.TextInput(attrs={"class": "form-control"}),
            "comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "columns": 20}
            ),
        }
