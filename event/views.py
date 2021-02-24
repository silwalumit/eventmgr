from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import(
    ListView,
    DetailView,
)

from django.views.generic.edit import (
    CreateView,
    UpdateView,
    FormView,
    FormMixin,
)

from core.views import MultiFormsView

from .forms import *
from locations.forms import *
import code 
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

class CreateEvent(LoginRequiredMixin, MultiFormsView):
    template_name = "event/add.html"
    
    form_classes = {
        "event":EventCreationForm,
        "location": LocationForm,
        "type":TypeCreationFormset
    }

    prefix = {
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
        event.save()
        forms['event'].save_m2m()
        # code.interact(local = dict(globals(), **locals()))

        if event_type:
            event.types.add(*event_type)
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

    def get_queryset(self):
        qs = super().get_queryset().filter(is_published = True)

        if self.request.GET:
            return self.filter(qs, self.request.GET)
        else:
            return  qs


    def filter(self, qs, query):
        
        q = {}
        if query.get("title"):
            q["title__icontains"] = query["title"]
        if query.get("org"):
            q["organizer__name__iexact"] = query["org"]
        if query.get("tag"):
            q["types__name__iexact"] = query["tag"]
        if query.get("location"):
            q["location__name__icontains"] = query["location"]
        if query.get("id"):
            q["organizer__id"] = query.get("id")
            # q["location__address__icontains"] = query["location"]

       
        queryset = qs.filter(**q).distinct()
        # queryset = qs.filter(
        #     Q(title__icontains = query["title"])|
        #     Q(organizer__name__iexact = query["org"])|
        #     Q(types__name__iexact = query["tag"])|
        #     Q(location__name__icontains = query["location"])|
        #     Q(location__address__icontains = query["location"])
        # ).distinct()
        # code.interact(local = dict(globals(), **locals()))
        return queryset

class MyEvents(LoginRequiredMixin, AllEvents):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = "event/my_events.html"

    def get_queryset(self):
        qs = self.model.objects.all()
        slug = self.kwargs.get(self.slug_url_kwarg)

        if slug is not None:
            qs =  qs.filter(organizer__user__slug = slug)
        else:
            qs =  qs

        if self.request.GET:
            return self.filter(qs, self.request.GET)
        else:
            return qs

from comments.forms import CommentForm

class EventDetailView(FormMixin, DetailView):
    form_class = CommentForm
    model = Event
    template_name = "event/detail.html"
    context_object_name = "event"
    parent_id = None
    parent_obj = None

    def get_form_kwargs(self):
        self.object = self.get_object()
        self.initial = {
            "content_type": self.object.get_content_type,
            "object_id":self.object.id
        }
        return super().get_form_kwargs()
    def get(self, request, *args, **kwargs):
        self.extra_context = {
            "comments":self.get_object().comments
        }
        return super().get(request, *args, **kwargs)
        
    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return self.model.objects.get(id = pk)

    def post(self, request, *args, **kwargs):
        self.parent_id = request.POST.get("parent_id")
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return super().form_valid()

    def form_valid(self, form):
        c_type = form.cleaned_data.get("content_type")
       
        content_type = self.get_object().get_content_type
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get('content')

        if self.parent_id:
            parent_qs = Comment.objects.filter(id = self.parent_id)

            if parent_qs.exists() and parent_qs.count() == 1:
                self.parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = self.request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = self.parent_obj,
        )

        return HttpResponseRedirect(reverse("event:detail" ,args=[self.get_object().organizer.user.slug,self.get_object().id]))

class SavedEventsView(LoginRequiredMixin, ListView):
    model = SavedEvent
    template_name = "volunteer/saved_events.html"
    context_object_name = "saved_events"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_volunteer:
            self.volunteer = request.user.volunteer
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def get_queryset(self):
        return super().get_queryset().filter(volunteer = self.volunteer)

from django.views.generic import View
class SaveEvent(LoginRequiredMixin, View):

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            event = Event.objects.filter(id = pk)
        else:
            event = None

        if request.user.is_volunteer and event.exists():
            obj, created = SavedEvent.objects.get_or_create(
                event = event.get(),
                volunteer = request.user.volunteer
            )

            request.user.volunteer.events.add(event.get())
            request.user.volunteer.save()
            return HttpResponseRedirect(reverse("user:dashboard"))
        else:
            return HttpResponseRedirect(reverse("all-events"))

from django.views.generic import DeleteView
class DeleteSavedEvent(LoginRequiredMixin, DeleteView):
    model = SavedEvent
    success_url = reverse_lazy("user:dashboard")

from users.models import Volunteer
class EventSpecifcVolunteers(LoginRequiredMixin, ListView):
    model = Volunteer
    template_name = "organizer/event_volunteers.html"
    context_object_name = "volunteers_list"
    event = None
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_volunteer:
            return HttpResponseRedirect("home")
        else:
            id = kwargs.get("id")
            self.event = Event.objects.filter(id = id)
            if self.event.exists():
                self.event = self.event.get()
                self.extra_context = {
                    "event": self.event
                }
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse("event:my-events"))

    def get_queryset(self):
        qs = super().get_queryset().filter(
            saved_event__event = self.event
        )
        query = self.request.GET
        
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
        return qs.filter(**q)