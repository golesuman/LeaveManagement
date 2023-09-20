from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from .forms import LeaveRequestForm, LoginForm
from .leave_services import get_leaves_by_status, get_total_leaves_left_for_user
from .models import Employee, LeaveRequest


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        try:
            leaves_data = LeaveRequest.objects.filter(
                employee__user=request.user
            ).count()
            pending_leaves = get_leaves_by_status(user=request.user, status="Pending")
            accepted_leaves = get_leaves_by_status(user=request.user, status="Accepted")
            remaining_leaves = get_total_leaves_left_for_user(user=request.user)
            all_leaves = LeaveRequest.objects.filter(employee__user=request.user)
            return render(
                request,
                template_name=self.template_name,
                context={
                    "leaves": leaves_data,
                    "accepted_leaves": accepted_leaves,
                    "pending_leaves": pending_leaves,
                    "remaining_leaves": remaining_leaves,
                    "all_leaves": all_leaves,
                },
            )
        except Exception as e:
            return redirect("login")
            # return render(request, template_name="login.html")


class LoginView(View):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Replace 'home' with your desired URL name
            else:
                form.add_error(None, "Invalid username or password.")
        return render(request, self.template_name, {"form": form})


class LeaveRequestCreateView(View):
    template_name = "leave_request_create.html"
    form_class = LeaveRequestForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)

            leave_request.employee = Employee.objects.filter(user=request.user).first()
            leave_request.save()
            return redirect("home")  # Redirect to a success page
        return render(request, self.template_name, {"form": form})
