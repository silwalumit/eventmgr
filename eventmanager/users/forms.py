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
            'placeholder':"email address",
        })
        self.fields["password"].widget.attrs.update({
            'placeholder':"password",
        })



class VolunteerCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control-sm'})
    
    class Meta:
        model = Volunteer
        fields = ('first_name','last_name',)

class UserCreationForm(AuthUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control-sm'})
    
    class Meta:
        model = User
        fields = ("email", )

class OrganizerCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control-sm'})
    
    class Meta:
        model = Organizer
        exclude = ('user', )

class ContactsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control-sm'})

    class Meta:
        model = OrganizationContact
        exclude = ('organizer',)
