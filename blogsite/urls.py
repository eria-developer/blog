from django.contrib import admin
from django.urls import path, include
from myblog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("blog/", include("myblog.urls")),
    path("user_signup", views.user_signup, name="user_signup"),
    path("user_signin", views.user_signin, name="user_signin"),
    path("user_signout", views.user_signout, name="user_signout"),

    # password reset links
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")
]
