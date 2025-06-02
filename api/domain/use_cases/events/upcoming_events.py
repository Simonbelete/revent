from dataclasses import dataclass
from datetime import timezone
from rest_framework.response import Response

from infrastructure.repositories import EventRepository

@dataclass
class UpcomingEventsUseCase():
    """Return upcoming events ordered by start_datetime
    """
    repository: EventRepository = EventRepository()
   
    def execute(self):
        events = self.repository.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)