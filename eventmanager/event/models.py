from users.models import Organizer

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Type(models.Model):
    name = models.CharField(
        verbose_name = _("name"), 
        max_length=50
    )

    description - models.TextField(
        verbose_name = _("description"), 
        null = True,
    )


class Event(models.Model):

    types = models.ManyToManyField(
        Type,
        verbose_name = _("categories"),
        through = "Membership",
        through_fields = ('type', 'event',),
        related_name='events',
        related_query_name='event',
        null = True,
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

    created_on = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()

class EventType(models.Model):
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
        related_name='eventtype',
    )


