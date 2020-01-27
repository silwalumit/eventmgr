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

urlpatterns = [
    path('', RedirectView.as_view(url = 'events/', permanent = True), name = "home"),
    path('accounts/', include('users.urls', namespace = "user")),
    
    path("events/", AllEvents.as_view(), name = "all-events" ),
    path("events/<int:pk>/save/", SaveEvent.as_view(), name = "save-event"),
    path('evennts/saved/<int:pk>/delete/', DeleteSavedEvent.as_view(), name= "delete-saved-event"),
    path('<slug:slug>/events/', include('event.urls', namespace = "event")),
    
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)