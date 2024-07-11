from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views

uelpatterns = urlpatterns = [
    path('', views.main_page),
]