from django.urls import path

from . import views

urlpatterns = [
    path("login", views.handleLogin, name="login"),
    path("signup", views.handleSignup, name="signup"),
    path("logout", views.handleLogout, name="logout")
]
