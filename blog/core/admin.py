from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'created_at')
    list_filter=('author', 'created_at')
    search_fields=('author', 'title')

# Register your models here.
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)