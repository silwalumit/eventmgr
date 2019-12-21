from django.shortcuts import render
from django.db import transaction
from django.urls import reverse_lazy, reverse

from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .forms import *
from core.views import MultiFormsView, AjaxResponseMixin

class Login(AjaxResponseMixin, LoginView):
    success_url= reverse_lazy("home")
    ajax_template_name = "registration/login.html"
    form_class = userLoginForm
    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)

class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("home")
    
class VolunteerSignUp(AjaxResponseMixin, MultiFormsView):
    extra_content = {
        "title":"Volunteer's Sign Up"
    }
    template_name = "volunteer/signup.html"
    ajax_template_name = "volunteer/signup.html"

    form_classes = {
        "user":UserCreationForm,
        "volunteer": VolunteerCreationForm
    }

    prefix = {
        "user":"user",
        "volunteer":"volunteer"
    }
    success_url = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def forms_valid(self, forms):
        user = forms['user'].save()
        volunteer = forms['volunteer'].save(commit = False)
        volunteer.user = user
        volunteer.save()
        return super().forms_valid(forms)

class OrganizerSignUp(AjaxResponseMixin,MultiFormsView):
    """Sign up view for organizations"""
    extra_content = {
        "title":"Organizer's Sign Up"
    }

    template_name = "organizer/signup.html"
    ajax_template_name = "organizer/signup.html"

    form_classes = {
        "user":UserCreationForm,
        "organizer": OrganizerCreationForm,
        "contact": ContactsForm,
    }

    prefix = {
        "user":"user",
        "organizer":"organizer",
        "contact":"contact-detail"
    }
    success_url = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def forms_valid(self, forms):
        user = forms['user'].save(commit = False)
        user.is_volunteer = False
        user.save()

        organizer = forms['organizer'].save(commit = False)
        organizer.user = user
        organizer.save()

        contact = forms['contact'].save(commit = False)
        contact.organizer = organizer
        contact.save()
        return super().forms_valid(forms)

# class EditOrganizationProfile(LoginRequiredMixin, MultiFormsView):


