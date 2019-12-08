from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm
from django.contrib.auth import get_user_model

user = get_user_model

class VolunteerCreationForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        exclude = ('user', 'middle_name', 'gender')

class UserCreationForm(AuthUserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class OrganizationCreationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ('user', )
