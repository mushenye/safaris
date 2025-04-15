from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('park_create/', views.Park_create.as_view(), name="create_park"),
]
