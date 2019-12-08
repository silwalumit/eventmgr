from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name = "user"

urlpatterns = [
    path("login/", Login.as_view(), name = "login"),
    path("logout/", Logout.as_view(), name = "logout"),
    path("signup/", TemplateView.as_view(template_name = "registration/signup.html"), name = "signup"),
    path('signup/volunteer/', VolunteerSignUp.as_view(), name = "signup_volunteer"),
    path('signup/org/', OrganizationSignUp.as_view(), name = "signup_org"),
]