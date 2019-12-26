from django.urls import path, re_path
from .views import *
from django.views.generic import TemplateView

app_name = "user"

urlpatterns = [
    path("login/", Login.as_view(), name = "login"),
    path("logout/", Logout.as_view(), name = "logout"),
    path("signup/", TemplateView.as_view(template_name = "registration/signup.html"), name = "signup"),
    path('signup/volunteer/', VolunteerSignUp.as_view(), name = "signup_volunteer"),
    path('signup/org/', OrganizerSignUp.as_view(), name = "signup_org"),

    re_path(
        'activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ActivateAccount.as_view(), 
        name = "activate"
    )
]