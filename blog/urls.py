from django.urls import path
from . import views

urlpatterns = [
    path("post_blog/", views.post_blog, name="post_blog"),
    path("blog_details/<slug:slug>/", views.blog_details, name="blog_details"),
    path("reply_comment/", views.reply_comment, name="reply_comment"),
    path("search/", views.search_view, name="search"),
    
    path("blog_details/<slug:slug>/like/", views.like_post, name="like_post"),
]
