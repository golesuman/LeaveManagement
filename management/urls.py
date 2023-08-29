from django.urls import path

from .views import LeaveRequestCreateView, LoginView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("create/", LeaveRequestCreateView.as_view(), name="create_leave"),
    path("login/", LoginView.as_view(), name="login"),
]
