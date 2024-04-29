from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("add_blog", views.add_blog, name="add_blog"),
    path("blogs", views.blogs, name="blogs"),
]
