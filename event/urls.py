from django.urls import path
from .views import *

app_name = "event"

urlpatterns = [
    path('' ,MyEvents.as_view(), name = "my-events"),
    path('create/', CreateEvent.as_view(), name = "add"),
    path('<int:id>/edit/', UpdateEvent.as_view(), name = "update"),
    path('<int:id>/volunteers/', EventSpecifcVolunteers.as_view(), name = "event-volunteers"),
    path('<int:pk>/detail/', EventDetailView.as_view(), name = "detail"),
]

