from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("add_blog", views.add_blog, name="add_blog"),
    path("blogs", views.blogs, name="blogs"),
    path("blog_details/<slug:slug>", views.blog_details, name="blog_details"),
    path("edit_blog/<slug:slug>", views.edit_blog, name="edit_blog"),
]
