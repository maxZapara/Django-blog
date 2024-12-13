from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/create", views.create_post, name="create_post"),
    path("posts/<post_id>", views.post_view, name="post_view"),

    path("posts/comments/<comment_id>/delete", views.delete_comment, name="delete_comment"),

    ]