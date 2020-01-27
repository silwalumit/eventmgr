from django import forms
from .models import *

class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].label=''
            self.fields[field].widget.attrs.update({'class':'form-control-sm'})
    
    class Meta:
        model = Location
        fields = "__all__"