from django.urls import path, re_path
from .views import *
from django.views.generic import TemplateView
from event.views import SavedEventsView, DeleteSavedEvent

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
    path('dashboard/', Dashboard.as_view(), name = "dashboard"),
    
    path('dashboard/saved-events/', SavedEventsView.as_view(), name = "saved-events"),
    path('dashboard/subscriptions/', SubscribedOrganization.as_view(), name = "subscriptions"),

    path('settings/', EditProfile.as_view(), name = "settings"),
    path('settings/changepassword/', ChangePassword.as_view(), name = "changepassword"),
    
    path('password_reset/', PasswordReset.as_view(), name = 'password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name = "password_reset_confirm"), 
    path('reset/done/', PasswordResetComplete.as_view(), name = 'password_reset_complete'),
]