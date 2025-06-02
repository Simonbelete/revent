from django.urls import path, include

urlpatterns = [
        path('', include('presentation.routes.calendar_routes')),
        path('', include('presentation.routes.event_routes')),
        path('', include('presentation.routes.me_routes')),
        path('', include('presentation.routes.signup_routes')),
]