from django.urls import path
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login" ),
    path("logout", views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('profile/change/email', views.change_email, name="change_email"),
    path('profile/change/password', views.change_password, name="change_password"),

    path("posts/save/<post_id>", views.toggle_save_post, name="toggle_save_post"),

    
    path("activate/<token>/<uid>", views.activate, name="activate_email"),

    path('password/reset', views.reset_password, name="reset_password"),
    path("password/reset/<token>/<uid>", views.reset_password_confirm, name="reset_password_confirm"),
    ]