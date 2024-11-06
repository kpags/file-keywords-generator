from django.urls import include, path
from .views import (
    FileAPIView
)

app_name="generator"

urlpatterns = [
    path('file-upload/', FileAPIView.as_view(), name='file-upload'),
]