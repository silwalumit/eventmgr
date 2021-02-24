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

from django.views.generic import TemplateView

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
import json, code

User = get_user_model()

class Login(AjaxTemplateMixin, LoginView):
    success_url= reverse_lazy("all-events")
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


        if self.request.is_ajax():
            data = {
                'data': render_to_string(
                    "header.html", 
                    {}, 
                    request = self.request
                )};
            return self.render_to_json(data)
        else:
            return response

    def render_to_json(self, data):
        return HttpResponse(
            json.dumps(data, ensure_ascii = False),
            content_type = self.request.is_ajax() and "application/json" or "text/html"
        )



class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("home")
    
class VolunteerSignUp(AjaxableResponseMixin, MultiFormsView):
    extra_content = {
        "title":"Volunteer's Sign Up"
    }
    template_name = "volunteer/signup.html"
    ajax_template_name = "header.html"

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
    def form_valid(self, forms):
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

        return super().form_valid(forms)

class OrganizerSignUp(AjaxableResponseMixin, MultiFormsView):
    """Sign up view for organizations"""
    extra_content = {
        "title":"Organizer's Sign Up"
    }

    template_name = "organizer/signup.html"
    ajax_template_name = "header.html"

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
    def form_valid(self, forms):
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
        
        return super().form_valid(forms)

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

class ChangePassword(LoginRequiredMixin, AjaxableResponseMixin,PasswordChangeView):
  
  success_url = reverse_lazy("user:dashboard")
  form_class = CustomPasswordChangeForm
  ajax_template_name = "header.html"
  template_name = "registration/change_password.html"

  def form_valid(self, form):
    
    messages.success(
        self.request, 
        "You have successfully changed your password"
    )
    
    return super().form_valid(form)

from locations.forms import LocationForm
class EditProfile(LoginRequiredMixin, MultiFormsView):

    form_classes = {
        'user': UserProfile,
        'location': LocationForm
    }
    prefix = {
        'user':'user',
        'location':'location',
    }
    success_url = reverse_lazy("user:settings")

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        
        self.extra_context = {
            'profile':request.user
        }

        if self.user.is_volunteer:
            self.form_classes['volunteer'] = VolunteerProfileForm
            self.prefix['volunteer'] = 'volunteer'
            self.template_name = "volunteer/profile.html"
        else:
            self.form_classes.update({
                'organizer': OrganizerCreationForm,
                'contact': ContactsForm
            })

            self.prefix.update({
                'organizer':'organizer',
                'contact':'contact'
            })
            self.template_name = "organizer/profile.html"

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, form_name):
        kwargs = super().get_form_kwargs(form_name)
        if form_name == 'user':
            kwargs.update({'instance':self.user})
        elif form_name == "location":
            if self.user.location:
                kwargs.update({'instance':self.user.location})
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
    def form_valid(self, forms):
        self.object = forms['user'].save(commit = False)
        location = forms['location'].save()
        self.object.location = location
        self.object.save(update_fields = ('avatar','location',))

        if self.object.is_volunteer:
            volunteer = forms['volunteer'].save()
        else:
            organizer = forms['organizer'].save()
            contact = forms['contact'].save()

        messages.success(self.request, "Profile successfully updated.")
        return super().form_valid(forms)


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

class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('home') 
    template_name = "registration/password_rst_confirm.html"
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your password has been reset. You may go ahead and login now"
        )
        return super().form_valid(form)

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_rst_done.html'

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "registration/password_rst_complete.html"

class Dashboard(LoginRequiredMixin,TemplateView):
    template_name = "volunteer/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_volunteer:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("user:settings"))

from django.views.generic import ListView
class OrganizerList(ListView):
    model = Organizer
    template_name = "organizer/list.html"
    context_object_name = "organizers"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET
        qs = super().get_queryset()
        if query:
            return self.filter(qs, query)
        else:
            return qs 

    def filter(self, qs ,query):
        q = {}

        location = query.get('location')
        address = query.get('address')

        if location:
            q["user__location__name"] = location

        if address:
            q["user__location__address"] = address

        return qs.filter(**q) if q else qs

class VolunteerList(LoginRequiredMixin, ListView):
    model = Volunteer
    template_name = "volunteer/list.html"
    context_object_name = "volunteers_list"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_volunteer:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def get_queryset(self):
        query = self.request.GET
        qs = super().get_queryset()
        if query:
            return self.filter(qs, query)
        else:
            return qs 

    def filter(self, qs ,query):
        q = {}

        location = query.get('location')
        address = query.get('address')

        if location:
            q["user__location__name"] = location

        if address:
            q["user__location__address"] = address

        return qs.filter(**q) if q else qs

class MyVolunteers(LoginRequiredMixin, ListView):
    model = Volunteer
    template_name = "volunteer/list.html"
    context_object_name = "volunteers_list"
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_volunteer:
            return HttpResponseRedirect("home")
        else:
            self.organizer = self.request.user.organizer
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET
        qs = super().get_queryset().filter(
            subscription__organizer = self.organizer
        )
        if query:
            return self.filter(qs, query)
        else:
            return qs 

    def filter(self, qs ,query):
        q = {}

        location = query.get('location')
        address = query.get('address')

        if location:
            q["user__location__name"] = location

        if address:
            q["user__location__address"] = address

        return qs.filter(**q) if q else qs

from django.views.generic import View
class SubscribeOrganizer(LoginRequiredMixin, View):

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            organizer = Organizer.objects.filter(id = pk)
        else:
            organizer = None

        if request.user.is_volunteer and organizer.exists():
            obj, created = Subscription.objects.get_or_create(
                organizer = organizer.get(),
                volunteer = request.user.volunteer
            )

            request.user.volunteer.organizers.add(organizer.get())
            request.user.volunteer.save()
            return HttpResponseRedirect(reverse("user:dashboard"))
        else:
            return HttpResponseRedirect(reverse("organizers"))

from django.views.generic import DeleteView
class DeleteSubscription(LoginRequiredMixin, DeleteView):
    model = Subscription
    success_url = reverse_lazy("user:dashboard")

class SubscribedOrganization(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = "volunteer/subscriptions.html"
    context_object_name = "subscriptions"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_volunteer:
            self.volunteer = request.user.volunteer
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def get_queryset(self):
        return super().get_queryset().filter(volunteer = self.volunteer)
