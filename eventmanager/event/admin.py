from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Type)
admin.site.register(SavedEvent)