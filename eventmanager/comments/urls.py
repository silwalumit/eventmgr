from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:id>/', views.comment_thread, name = 'thread'), # comments/3/
    path('<int:id>/delete/', views.comment_delete, name = 'delete'),
    #path('<str:slug>/delete/', views.delete_post, name = 'delete'), # posts/3/delete/
]