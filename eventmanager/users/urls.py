from django.urls import path, re_path
from .views import *
from django.views.generic import TemplateView
from django.contrib.auth.views import(
    PasswordResetView,
    PasswordResetDoneView, 
    PasswordResetConfirmView
)

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
    ),

    path('settings/', EditProfile.as_view(), name = "settings"),
    path('settings/changepassword/', ChangePassword.as_view(), name = "changepassword"),
    
     path('password/reset/', PasswordResetView.as_view(template_name = 'registration/password_reset.html'), name = 'password_reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html') ,name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html'), name = "password_reset_confirm"), 
    path('reset/done/', PasswordResetDoneView.as_view(template_name = 'registration/password_reset_complete.html'), name = 'password_reset_complete'),
]