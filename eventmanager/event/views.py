from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from django.views.generic.detail import SingleObjectMixin

from django.views.generic import(
    ListView,
    DetailView,
)

from django.views.generic import (
    CreateView,
    UpdateView,
    FormView,
)

from core.views import MultiFormsView

from .forms import *
from locations.forms import *

import code 
class CreateEvent(MultiFormsView):
    template_name = "event/add.html"
    
    form_classes = {
        "event":EventCreationForm,
        "location": LocationForm,
        "type":TypeCreationFormset
    }

    prefixes = {
        "event":"event",
        "location":"location",
        "type":"type"
    }

    extra_context = {
        "title": "Create Event"
    }

    def get_success_url(self):
        return reverse("event:my-events", args=[self.organizer.user.slug])

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_volunteer:
            self.organizer = request.user.organizer
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))
    
    def get_form_kwargs(self, form_name):
        kwargs = super().get_form_kwargs(form_name)
        if form_name == "type":
            kwargs['queryset'] = Type.objects.none()
        return kwargs

    @transaction.atomic
    def form_valid(self, forms):
        location = forms['location'].save()
        event_type = forms['type'].save()
        event = forms['event'].save(commit = False)
        event.organizer = self.organizer
        event.location = location
        
        event.types.add(**event_type)
        event.save()
        
        return HttpResponseRedirect(self.get_success_url())

class UpdateEvent(CreateEvent):
    model = Event
    event = None
    extra_context = {
        "title": "Update Event"
    }

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get("id")
        
        if id:
            self.event = self.model.objects.get(id = id)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, form_name):
        kwargs = super().get_form_kwargs(form_name)
        
        if form_name == "event":
            kwargs.update({"instance":self.event})

        if form_name == "location" and self.event :
            kwargs.update({"instance":self.event.location})

        return kwargs

    @transaction.atomic
    def form_valid(self, forms):
        event_type = forms['type'].save()
        self.event = forms['event'].save()
        self.event.types.add(*event_type)
        # code.interact(local = dict(globals(), **locals()))
        self.event.save()
        forms['location'].save()
        return HttpResponseRedirect(self.get_success_url())


class AllEvents(ListView):
    model = Event
    template_name = "event/list.html"
    context_object_name = "events_list"
    paginate_by = 10

class MyEvents(AllEvents):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            return qs.filter(organizer__user__slug = slug)
        else:
            return qs

class EventDetailView(DetailView):
    model = Event
    template_name = "event/detail.html"
    context_object_name = "event"

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return self.model.objects.get(id = pk)

class SavedEventsView(ListView):
    model = SavedEvent
    template_name = "event/saved_events.html"
    context_object_name = "events_list"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_volunteer:
            self.volunteer = request.user.volunteer
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def get_queryset(self):
        return super().get_queryset().filter(volunteer = self.volunteer)