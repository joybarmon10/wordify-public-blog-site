from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/author/<str:username>/", views.view_user_profile, name="view_user_profile"),
]
