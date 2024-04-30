from . import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.CustomUser
        fields = ["username", "email"]


class AddBlogForm(ModelForm):
    class Meta:
        model = models.Blog
        fields = ["title", "description", "photo"]


class EditBlogForm(ModelForm):
    class Meta:
        model = models.Blog
        fields = ["title", "description", "photo"]       