from django.urls import path
from .views import *
urlpatterns = [
    path("login/", Login.as_view(), name = "login"),
    path('volunteer/signup/', VolunteerSignUp.as_view(), name = "signup_volunteer"),
    path('org/signup/', OrganizationSignUp.as_view(), name = "signup_org"),
]