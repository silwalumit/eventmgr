from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from users.models import Organizer, Volunteer
def upload_location(instance, filename):
    return "event/organizer/{0}/{1}".format(instance.organizer.id, filename)

class Type(models.Model):
    name = models.CharField(
        verbose_name = _("name"), 
        max_length=50,
        unique = True,
    )

    description = models.TextField(
        verbose_name = _("description"), 
        null = True,
    )

    def __str__(self):
        return self.name

class EventManager(models.Manager):
    
    def for_organizer(self, organizer):
        return super().filter(user__organizer = organizer)

class Event(models.Model):

    id = models.BigAutoField(
        primary_key=True,
        verbose_name = _("ID")
    )

    types = models.ManyToManyField(
        Type,
        verbose_name = _("categories"),
        through = "EventType",
        through_fields = ('event', 'type',),
        related_name='events',
        related_query_name='event',
    )

    banner_image = models.ImageField(
        upload_to = upload_location,
        null= True,
        blank= True
    )

    organizer = models.ForeignKey(
        Organizer,
        verbose_name = _("organizer"),
        on_delete = models.CASCADE,
        related_name = "events",
        related_query_name = "event",
    )

    title = models.CharField(
        verbose_name = _("title"),
        max_length = 100
    )
    
    description = models.TextField(
        verbose_name = _("description"), 
        null = True
    )

    location = models.OneToOneField(
        "locations.Location",
        on_delete = models.PROTECT,
        null = True
    )
    
    updated_on = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    class Meta:
        ordering = ['-timestamp', '-updated_on']


class EventType(models.Model):
    
    id = models.BigAutoField(
        primary_key=True,
        verbose_name = _("ID")
    )

    type = models.ForeignKey(
        Type,
        on_delete = models.CASCADE,
        related_name='eventtypes',
        related_query_name='eventtype',
    )

    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
        related_name='eventtypes',
        related_query_name='eventtype',
    )

class SavedEvent(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        verbose_name = _("ID")
    )
    
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete = models.CASCADE,
        related_name = "saved_events",
        related_query_name = "saved_event",
    )

    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
        related_name = "saved_events",
        related_query_name = "saved_event"
    )

    class Meta:
        ordering = ["-id"]
