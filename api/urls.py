from django.urls import path, include
from rest_framework import viewsets
from api.views import testView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('test/', testView)
]
