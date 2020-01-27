from django import forms
from django.forms import modelformset_factory
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

class EventCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field in ("start_time", "end_time",):
                self.fields[field].widget.attrs.update({'class':'form-control-sm timepicker'})
            elif field in ("start_date", "end_date",):
                self.fields[field].widget.attrs.update({'class':'form-control-sm datepicker'})
            elif field == "types":
                self.fields[field].widget.attrs.update({'class':'select2'})
            else:
                self.fields[field].widget.attrs.update({'class':'form-control-sm'})
                
            self.fields[field].label=''
    
    class Meta:
        model = Event
        fields = (
            "title", 
            "description", 
            "start_date",
            "end_date",
            "is_published",
            "types",
            "banner_image"
        )

class TypeCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label=''
        self.fields['name'].widget.attrs.update({'class':'form-control-sm'})

    class Meta:
        model = Type
        fields = ("name",)

TypeCreationFormset = modelformset_factory(
    Type, 
    form = TypeCreationForm,
    fields = ('name',),
    extra = 0
)