from django.db import models
from django.contrib.auth.models import User
from core.models import Post
from django.contrib import admin

# Create your models here.
class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   image = models.ImageField(upload_to="profiles/", blank=True, null=True)
   saved_posts = models.ManyToManyField(Post, blank=True, null=True)
   activated = models.BooleanField(default=False, null=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)


    