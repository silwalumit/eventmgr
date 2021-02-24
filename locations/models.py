from django.db import models
from django.utils.translation import ugettext_lazy as _

class Location(models.Model):
    id = models.BigAutoField(
        primary_key = True,
        verbose_name = _("ID")
    )
    name = models.CharField(
        verbose_name = _("Name"),
        max_length=50
    )

    address = models.CharField(
        verbose_name = _("Address"),
        max_length=250
    )

    # longitude = models.FloatField()
    # latitude = models.FloatField()
