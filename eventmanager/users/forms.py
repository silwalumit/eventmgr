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
        self.fields["first_name"].widget.attrs.update({'placeholder':'first name'})
        self.fields["last_name"].widget.attrs.update({'placeholder':'last name'})
        for field in self.fields:
            self.fields[field].label=''
            
    
    class Meta:
        model = Volunteer
        fields = ('first_name','last_name',)

class UserCreationForm(AuthUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholder = "email"
        
        for field in self.fields:
            self.fields[field].label = ''
            if field == 'password1':
                placeholder = "password"
            elif field == 'password2':
                placeholder = "confirm password"
            self.fields[field].widget.attrs.update({'placeholder':placeholder})
    
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
