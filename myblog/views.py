from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . import models
from . import forms
from django.contrib.auth.decorators import login_required

def user_signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}:-> {error}")
    else:
        form = CustomUserCreationForm()
    context = {
            "form": form,
        }
    return render(request, "myblog/user_signup.html", context)


def user_signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "myblog/user_signin.html", context)


def user_signout(request):
    logout(request)
    return redirect("user_signin")


def index(request):
    return render(request, "myblog/index.html")


@login_required(login_url="user_signin")
def home(request):
    username = request.user.username
    blogs = models.Blog.objects.filter(author=request.user)
    context = {
        "username": username,
        "blogs": blogs
    }
    return render(request, "myblog/home.html", context) 


@login_required(login_url="/user_signin")
def add_blog(request):
    if request.method == "POST":
        form = forms.AddBlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("home")
    else:
        form = forms.AddBlogForm()

    context = {
        "form": form,
    }
    return render(request, "myblog/add_blog.html", context)


def blogs(request):
    blogs = models.Blog.objects.all().order_by("-created_at")
    context = {
        "blogs": blogs,
    }
    return render(request, "myblog/blogs.html", context)


def blog_details(request, slug):
    blog = get_object_or_404(models.Blog, slug=slug)
    context = {
        "blog": blog,
    }
    return render(request, "myblog/blog_details.html", context)


def edit_blog(request, slug):
    # blog_to_edit = models.Blog.objects.filter(slug=slug)
    blog_to_edit = get_object_or_404(models.Blog, slug=slug)
    if request.method == "POST":
        form = forms.EditBlogForm(request.POST, instance=blog_to_edit)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
    else:
        form = forms.EditBlogForm(instance=blog_to_edit)
    context = {
        "form": form,
    }
    return render(request, "myblog/edit_blog.html", context)


def delete_blog(request, slug):
    blog = get_object_or_404(models.Blog, slug=slug)
    blog.delete()
    return redirect("home")