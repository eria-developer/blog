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


@login_required(login_url="user_signin")
def user_signout(request):
    logout(request)
    return redirect("user_signin")


def index(request):
    return render(request, "myblog/index.html")


@login_required(login_url="user_signin")
def home(request):
    username = request.user.username
    blogs = models.Blog.objects.filter(author=request.user).order_by("-created_at")
    context = {
        "username": username,
        "blogs": blogs
    }
    return render(request, "myblog/home.html", context) 


@login_required(login_url="user_signin")
def profile(request, id):
    user = get_object_or_404(models.CustomUser, id=id)
    context = {
        "user": user,
    }
    return render(request, "myblog/profile.html", context)


@login_required(login_url="user_signin")
def edit_profile(request, id):
    user = get_object_or_404(models.CustomUser, id=id)
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect("profile", id=id)
    else:
        form = forms.ProfileForm(instance=user)
    context = {
        "form": form,
    } 
    return render(request, "myblog/edit_profile.html", context)


@login_required(login_url="user_signin")
def add_blog(request):
    if request.method == "POST":
        form = forms.AddBlogForm(request.POST, request.FILES)
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
    comments = models.Comment.objects.filter(blog=blog).order_by("-created_at")
    context = {
        "blog": blog,
        "comments": comments
    }
    return render(request, "myblog/blog_details.html", context)


@login_required(login_url="user_signin")
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


@login_required(login_url="user_signin")
def delete_blog(request, slug):
    blog = get_object_or_404(models.Blog, slug=slug)
    blog.delete()
    return redirect("home")


@login_required(login_url="user_signin")
def add_comment(request, slug):
    blog = get_object_or_404(models.Blog, slug=slug)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user
            comment.blog = blog
            comment.save()
            return redirect("blog_details", slug=slug)
    else:
        form = forms.CommentForm()
    context = {
            "form": form,
            "blog": blog,
        }
    return render(request, "myblog/add_comment.html", context)