from django.urls import path, include
from rest_framework import routers

from presentation.views import current_user

urlpatterns = [
    path('me/', current_user),
]