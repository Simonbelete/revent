from django.urls import path, include
from rest_framework import routers

from presentation import views

router = routers.DefaultRouter()

router.register(
    r'',
    viewset=views.CalendarViewSet,
    )

urlpatterns = [
    path('calendars', include(router.urls)),
]