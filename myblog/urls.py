from django.urls import path
from . import views

urlpatterns = [
    
    path("home", views.home, name="home"),
    path("add_blog", views.add_blog, name="add_blog"),
    path("blogs", views.blogs, name="blogs"),
    path("blog_details/<slug:slug>", views.blog_details, name="blog_details"),
    path("blog_details/<slug:slug>/add_comment", views.add_comment, name="add_comment"),
    path("edit_blog/<slug:slug>", views.edit_blog, name="edit_blog"),
    path("delete_blog/<slug:slug>", views.delete_blog, name="delete_blog"),
    # path("<slug:slug>/add_comment/", views.add_comment, name="add_comment")
]
