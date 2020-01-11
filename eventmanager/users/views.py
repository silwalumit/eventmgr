from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import (
    urlsafe_base64_encode, 
    urlsafe_base64_decode
)

from django.utils.encoding import force_bytes, force_text

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse

# from django.contrib.auth import login as auth_login
from .forms import *
from core.views import MultiFormsView, AjaxTemplateMixin, AjaxableResponseMixin

from users.tokens import account_activation_token
from django.views.generic import View, FormView

from django.contrib.auth.views import(
    PasswordResetView,
    PasswordResetDoneView,
)

from django.contrib.auth import (
    # authenticate, 
    get_user_model, 
    login, 
    # logout
)
import json

User = get_user_model()

class Login(AjaxTemplateMixin, LoginView):
    success_url= reverse_lazy("home")
    ajax_template_name = "registration/login.html"
    form_class = UserLoginForm
    
    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)

    def form_valid(self,form):
        response = super().form_valid(form)
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(30*24*60)
        else:
            self.request.session.set_expiry(0)

        messages.success(
            self.request, 
            "Successfully logged in. Logged in as <strong>{0}</strong>.".format(self.request.user)
        )

        return response


class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("home")
    
class VolunteerSignUp(AjaxTemplateMixin, MultiFormsView):
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
        
        current_site = get_current_site(self.request)
        subject = "Activate your Come and Volunteer Account"

        message = render_to_string(
            'registration/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )

        user.email_user(subject, message)

        message = "Thank you for registering with us. An activation link is sent to <strong class ='font-weight-bolder'>{0}</strong>. Please confirm you email.".format(user.email)

        messages.success(self.request, message)

        return super().forms_valid(forms)

class OrganizerSignUp(AjaxTemplateMixin,MultiFormsView):
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

        current_site = get_current_site(self.request)
        subject = "Activate your Come and Volunteer Account"

        message = render_to_string(
            'registration/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )

        user.email_user(subject, message)

        message = "Thank you for registering with us. An activation link is sent to {0}. Please confirm you email.".format(user.email)

        messages.success(self.request, message)
        return super().forms_valid(forms)

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Congratulations! Your account have been confirmed.")
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
        
        return HttpResponseRedirect(reverse("home"))

class ChangePassword(LoginRequiredMixin,PasswordChangeView):
  template_name = "registration/change_password.html"
  success_url = reverse_lazy("home")
  form_class = CustomPasswordChangeForm
  ajax_template_name = "header.html"

  def form_valid(self, form):
    messages.success(
        self.request, 
        "You have successfully changed your password"
    )

    return super().form_valid(form)


class EditProfile(LoginRequiredMixin, MultiFormsView):

    form_classes = {
        'user': UserProfile
    }
    success_url = reverse_lazy("user:settings")

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        
        self.extra_context = {
            'profile':request.user
        }

        if self.user.is_volunteer:
            self.form_classes['volunteer'] = VolunteerProfileForm
            self.template_name = "volunteer/profile.html"
        else:
            self.form_classes.update({
                'organizer': OrganizerCreationForm,
                'contact': ContactsForm
            })
            self.template_name = "organizer/profile.html"

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, form_name):
        kwargs = super().get_form_kwargs(form_name)
        if form_name == 'user':
            kwargs.update({'instance':self.user})
        else:
            if self.user.is_volunteer:
                kwargs.update({'instance':self.user.volunteer})
            else:
                if form_name == "contact":
                    kwargs.update({'instance':self.user.organizer.contact})
                else:
                    kwargs.update({'instance':self.user.organizer})

        return kwargs

    @transaction.atomic
    def forms_valid(self, forms):
        self.object = forms['user'].save(commit = False)
        self.object.save(update_fields = ('avatar',))

        if self.object.is_volunteer:
            volunteer = forms['volunteer'].save()
        else:
            organizer = forms['organizer'].save()
            contact = forms['contact'].save()
        messages.success(self.request, "Profile successfully updated.")
        return super().forms_valid(forms)


from django.contrib.auth.views import(
    PasswordResetView,
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('home') 
    template_name = 'registration/password_rst_form.html'
    email_template_name = 'registration/password_rst_email.html'

    def form_valid(self, form):
        message = '''
        <p>
        We've emailed you instructions for setting your password, if an 
        account exists with the email you entered, should receive them shortly.
        </p>
        <p>
        If you don't receive an email, please make sure you've entered the
        address you registered with, check your spam folder.
         </p>
    '''
        messages.success(
            self.request,
            message
        )

        return super().form_valid(form)


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_rst_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('user:password_reset_complete') 
    template_name = "registration/password_rst_confirm.html"

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "registration/password_rst_complete.html"