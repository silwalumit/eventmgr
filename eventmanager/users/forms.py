from .models import *
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as AuthUserCreationForm,
    AuthenticationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        initial= False,
        label = 'Remember me',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.placeholders = {
            'username': 'Email Address',
            'password': 'Password'
        }

        for k,v in self.placeholders.items():
            self.fields[k].label=''
            self.fields[k].widget.attrs.update({'placeholder':v})  



class VolunteerCreationForm(forms.ModelForm):
    placeholders = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.placeholders.update({
            'first_name': 'First Name',
            'last_name': 'last Name'
        })

        for k, v in self.placeholders.items():
            self.fields[k].label=''
            self.fields[k].widget.attrs.update({'placeholder':v})
    
    class Meta:
        model = Volunteer
        fields = ('first_name','last_name',)

class UserCreationForm(AuthUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.placeholders = {
            'email': "Email Address",
            'password1':"Password",
            'password2':"Confirm Password"
        }
        
        for k,v in self.placeholders.items():
            self.fields[k].label = ''
            self.fields[k].widget.attrs.update({'placeholder':v,'class':'form-control'})
    
    class Meta:
        model = User
        fields = ("email", )

class OrganizerCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.placeholders = {
            "name": "Name of your organization",
            "description": "Describe what your organization do ..."
        }

        for k,v in self.placeholders.items():
            self.fields[k].label = ''
            if k == "description":
                self.fields[k].widget.attrs.update({"placeholder":v, "rows":5})
            else:
                self.fields[k].widget.attrs.update({'placeholder':v})
       
    class Meta:
        model = Organizer
        exclude = ('user', )

class ContactsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label=''

        self.placeholders = {
            'primary_no':'Primary Number',
            'secondary_no':'Secondary Number',
            'website':'Website(e.g website.org)',
            'facebook':'Facebook Page (e.g facebook.com/yourpage)',
            'twitter':'Twitter Page (e.g twitter.com/yourprofile)',
            'instagram':'instagram (e.g instagram.com/yourprofile)'
        }

        for k, v in self.placeholders.items():
            self.fields[k].widget.attrs.update({'placeholder':v})
    
    class Meta:
        model = OrganizationContact
        exclude = ('organizer',)

class VolunteerProfileForm(VolunteerCreationForm):

    def __init__(self, *args,**kwargs):
        self.placeholders.update({
            'dob': 'Date of Birth',
            'bio': 'Tell us something about you ...',
            'contact_no':'How can we contact you?'
        })

        super().__init__(*args,**kwargs)

    class Meta:
        model = Volunteer
        exclude = ('user',)

class UserProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ('avatar', )
