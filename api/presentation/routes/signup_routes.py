from django.urls import path

from presentation.views import SignupViewSet

urlpatterns = [
    path('signup/', SignupViewSet.as_view(), name='signup'),
]