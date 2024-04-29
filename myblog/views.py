from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . import models
from . import forms

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


def home(request):
    username = request.user.username
    context = {
        "username": username,
    }
    return render(request, "myblog/home.html", context) 


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
    blogs = models.Blog.objects.all()
    context = {
        "blogs": blogs,
    }
    return render(request, "myblog/blogs.html", context)