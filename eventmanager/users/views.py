from .forms import *
from django.shortcuts import render
from django.db import transaction
from django.urls import reverse_lazy
from core.views import MultiFormsView
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.

class Login(LoginView):
    success_url= reverse_lazy("home")

    def get_success_url(self):
        return self.success_url
         
class Logout(LogoutView):
    next_page = reverse_lazy("home")
    
class VolunteerSignUp(MultiFormsView):
    extra_content = {
        "title":"Volunteer's Sign Up"
    }
    template_name = "volunteer/signup.html"
    form_classes = {
        "user_form":UserCreationForm,
        "volunteer_form": VolunteerCreationForm
    }

    prefix = {
        "user_form":"user",
        "volunteer_form":"volunteer"
    }
    success_url = reverse_lazy("home")

    @transaction.atomic
    def forms_valid(self, forms):
        user = forms['user_form'].save()
        volunteer = forms['volunteer_form'].save(commit = False)
        volunteer.user = user
        volunteer.save()
        return super().forms_valid(forms)

class OrganizationSignUp(MultiFormsView):
    """Sign up view for organizations"""
    extra_content = {
        "title":"Organization's Sign Up"
    }
    template_name = "organization/signup.html"
    form_classes = {
        "user_form":UserCreationForm,
        "organization_form": OrganizationCreationForm
    }

    prefix = {
        "user_form":"user",
        "organization_form":"organization"
    }
    success_url = reverse_lazy("home")

    @transaction.atomic
    def forms_valid(self, forms):
        user = forms['user_form'].save()
        volunteer = forms['organization_form'].save(commit = False)
        volunteer.user = user
        volunteer.save()
        return super().forms_valid(forms)

