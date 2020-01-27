from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        query_set = super(CommentManager, self).filter(content_type = content_type, object_id = obj_id, parent = None)
        return query_set

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1, on_delete = models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    # post = models.ForeignKey(Post, on_delete = models.CASCADE)
    
    content = models.TextField()
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
   
    parent = models.ForeignKey("self", null = True, blank = True, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    objects = CommentManager() 
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return self.user.username
    
    def children(self):
        return Comment.objects.filter(parent = self)
    
    @property
    def is_parent(self):
        return self.parent is None 
            
    # def get_absolute_url(self):
    #     return reverse("comments:thread", args = [int(self.id)])