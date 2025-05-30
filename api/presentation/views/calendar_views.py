from rest_framework import viewsets

from domain import use_cases
from infrastructure import repositories
from presentation import serializers

class CalendarViewSet(use_cases.CalendarUseCase, viewsets.GenericViewSet):
    queryset = repositories.CalendarRepository().all()
    serializer_class = serializers.CalendarSerializer
    
    
