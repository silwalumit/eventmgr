"""eventmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from event.views import AllEvents, SaveEvent, DeleteSavedEvent
from users.views import (
    VolunteerList, 
    OrganizerList, 
    SubscribeOrganizer,
    DeleteSubscription
)

urlpatterns = [
    path('', RedirectView.as_view(url = 'events/', permanent = True), name = "home"),
    path('accounts/', include('users.urls', namespace = "user")),
    path('comments', include('comments.urls', namespace = "comments")),
    path("volunteers/", VolunteerList.as_view(), name = "volunteers"),
    path("organizers/", OrganizerList.as_view(), name = "organizers"),
    path("organizers/<int:pk>/subscribe/", SubscribeOrganizer.as_view(), name = "subscribe"),
    path("organizers/subscribed/<int:pk>/delete/", DeleteSubscription.as_view(), name = "delete-subscription"),

    path("events/", AllEvents.as_view(), name = "all-events" ),
    path("events/<int:pk>/save/", SaveEvent.as_view(), name = "save-event"),
    path('events/saved/<int:pk>/delete/', DeleteSavedEvent.as_view(), name= "delete-saved-event"),
    path('<slug:slug>/events/', include('event.urls', namespace = "event")),
    

    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)