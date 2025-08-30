from django.urls import path

from .views import indexPrompt 

urlpatterns = [
    path("", indexPrompt.as_view(), name="index"),
    path("prompt", indexPrompt.as_view(), name="prompt"),
]

