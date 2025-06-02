from django.urls import path, include
from rest_framework import routers

from presentation import views

router = routers.DefaultRouter()

router.register(
    r'calendars',
    viewset=views.CalendarViewSet,
    )

urlpatterns = [
    path('', include(router.urls)),
]