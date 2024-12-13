from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    content=HTMLField(null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title
    
class Comment(models.Model):
    content=models.TextField(null=False, blank=False)
    author=models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)