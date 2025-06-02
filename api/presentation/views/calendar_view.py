from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from domain import use_cases
from infrastructure import repositories, model
from presentation import serializers

class CalendarViewSet(use_cases.CalendarUseCase, viewsets.GenericViewSet):
    queryset = repositories.CalendarRepository().all()
    serializer_class = serializers.CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    expandCalendar = use_cases.ExpandCalendarUseCase()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'], url_path="expand")
    def expand(self, request, pk=None):
        try:
            event = self.get_object()
            data = self.get_serializer(event).data
            instances = self.expandCalendar.execute(calendar=data)
            return Response(instances)
        except model.Calendar.DoesNotExist:
            raise NotFound("Not found")
    
    
