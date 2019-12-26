from .models import *
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as AuthUserCreationForm,
    AuthenticationForm
)
from django.contrib.auth import get_user_model

user = get_user_model

class userLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        initial= False,
        label = 'Remember me',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = ''
        self.fields["password"].label = ''    
        self.fields["username"].widget.attrs.update({
            'placeholder':"Email Address",
        })
        self.fields["password"].widget.attrs.update({
            'placeholder':"Password",
        })



class VolunteerCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({'placeholder':'First Name'})
        self.fields["last_name"].widget.attrs.update({'placeholder':'Last Name'})
        for field in self.fields:
            self.fields[field].label=''
            
    
    class Meta:
        model = Volunteer
        fields = ('first_name','last_name',)

class UserCreationForm(AuthUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholder = "Email Address"
        
        for field in self.fields:
            self.fields[field].label = ''
            if field == 'password1':
                placeholder = "Password"
            elif field == 'password2':
                placeholder = "Confirm password"
            self.fields[field].widget.attrs.update({'placeholder':placeholder,'class':'form-control'})
    
    class Meta:
        model = User
        fields = ("email", )

class OrganizerCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'placeholder':'Name of your organization'})
        self.fields['description'].widget.attrs.update({
            "placeholder":"Describe what your organization do",
            "rows":5
        })
        for field in self.fields:
            self.fields[field].label = ''
    
    class Meta:
        model = Organizer
        exclude = ('user', )

class ContactsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label=''

        placeholders = {
            'primary_no':'Primary Number',
            'secondary_no':'Secondary Number',
            'website':'Website(e.g website.org)',
            'facebook':'Facebook Page (e.g facebook.com/yourpage)',
            'twitter':'Twitter Page (e.g twitter.com/yourprofile)',
            'instagram':'instagram (e.g instagram.com/yourprofile)'
        }

        for k, v in placeholders.items():
            self.fields[k].widget.attrs.update({'placeholder':v})
    
    class Meta:
        model = OrganizationContact
        exclude = ('organizer',)
