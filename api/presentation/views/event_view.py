from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from domain import use_cases
from infrastructure import repositories, model
from presentation import serializers

class EventViewSet(use_cases.EventUseCase, viewsets.GenericViewSet):
    queryset = repositories.EventRepository().all()
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Usecases
    upcomingEventsUseCase = use_cases.UpcomingEventsUseCase()
    expandUseCase = use_cases.ExpandRecurringEventUseCase()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'], url_path='/upcoming')
    def upcoming(self, request):
        return self.upcomingEventsUseCase.execute()
    
    @action(detail=True, methods=['get'], url_path='expand')
    def expand(self, request, pk=None):
        try:
            event = self.get_object()
            data = self.get_serializer(event).data
            instances = self.expandUseCase.execute(event=data)
            return Response(instances)
        except model.Calendar.DoesNotExist:
            raise NotFound("Not found")
    
   
        
    # @action(detail=False, methods=['get'])
    # def calendar(self, request):
    #     # Accept start_date and end_date as query params
    #     start_date = request.query_params.get('start_date')
    #     end_date = request.query_params.get('end_date')

    #     if not start_date or not end_date:
    #         return Response({"error": "start_date and end_date query params are required"}, status=400)

    #     # Filter events overlapping with this range
    #     events = self.get_queryset().filter(
    #         Q(start_datetime__lte=end_date),
    #         Q(end_datetime__gte=start_date)
    #     )
    #     serializer = self.get_serializer(events, many=True)
    #     return Response(serializer.data)