from dataclasses import dataclass, field
from django.forms.models import model_to_dict
from rest_framework.response import Response

from domain import entities
from infrastructure.repositories import EventRepository
from ..events import ExpandRecurringEventUseCase

@dataclass
class ExpandCalendarUseCase:
    """Expand all events found under the give calendar
    """
    repository: EventRepository = EventRepository()
    expandRecurringEventUseCase: ExpandRecurringEventUseCase = field(default_factory=ExpandRecurringEventUseCase)
   
    def execute(self, calendar: entities.CalendarEntity):
        """Expand all events

        Args:
            calendar : Dict of calendar

        Returns:
            _type_: _description_
        """
        events = self.repository.all().filter(calendar=calendar['id']).order_by('start_datetime')
        
        instances = []
                
        for event in events:
            print(model_to_dict(event))
            instances.extend(self.expandRecurringEventUseCase.execute(event=model_to_dict(event)))
        
        print('**********')
        print(instances)
        
        return instances