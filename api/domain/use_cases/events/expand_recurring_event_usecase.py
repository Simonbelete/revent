import calendar
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
from rest_framework.response import Response

from infrastructure.repositories import EventRepository
from domain.entities import EventEntity

@dataclass
class ExpandRecurringEventUseCase():
    """Return upcoming events ordered by start_datetime
    """
    event: EventEntity = None
    repository: EventRepository = EventRepository()
    
    def execute(self, event: EventEntity, range_start = timezone.now(), range_end = timezone.now() + relativedelta(months=6)):
        """
        Generate recurring instances of an event between range_start and range_end.
        Supports daily, weekly, and monthly relative recurrences.

        Args:
            event: Dict with recurrence info
            range_start: datetime
            range_end: datetime
            
        Returns:
            List of event instances (start, end)
        """
        self.event = event
        
        instances = []
        base_start = self._parse_datetime(event['start_datetime'])
        base_end = self._parse_datetime(event['end_datetime'])

        # base_start = datetime.fromisoformat(event['start_datetime'])
        # base_end = datetime.fromisoformat(event['end_datetime'])

        freq = event.get('freq')
        interval = event.get('interval', 1)
        weekdays = event.get('weekdays') or []
        recurrence_end_date = datetime.strptime(event['recurrence_end_date'], "%Y-%m-%d") if event.get('recurrence_end_date') else range_end

        current_start = base_start
        current_end = base_end
 
        if(not event['recurrence']):
            return self._expand_single_occurrence(event)

        while current_start <= range_end and current_start <= recurrence_end_date:
            if current_start >= range_start:
                if freq == 'daily':
                    instances.append(self._build_instance(current_start, current_end))
                elif freq == 'weekly':
                    if current_start.weekday() in weekdays:
                        instances.append(self._build_instance(current_start, current_end))
                elif freq == 'monthly':
                    # Monthly by relative pattern
                    week_number = event.get('relative_week_number')
                    weekday = event.get('relative_weekday')
                    year, month = current_start.year, current_start.month
                    dates = [day for day in calendar.Calendar().itermonthdates(year, month)
                            if day.weekday() == weekday and day.month == month]
                    if 0 <= week_number - 1 < len(dates):
                        date = dates[week_number - 1]
                        start = datetime.combine(date, base_start.time())
                        # make it aware in the current timezone
                        start = timezone.make_aware(start, timezone.get_current_timezone())
                        end = datetime.combine(date, base_end.time())
                        if range_start <= start <= range_end and start <= recurrence_end_date:
                            instances.append(self._build_instance(start, end))
                elif freq == 'yearly':
                    start = current_start
                    end = current_end
                    if start >= range_start and start <= range_end and start <= recurrence_end_date:
                        instances.append(self._build_instance(start, end))
            # Move to next period
            if freq == 'daily':
                current_start += timedelta(days=interval)
                current_end += timedelta(days=interval)
            elif freq == 'weekly':
                current_start += timedelta(days=1)
                current_end += timedelta(days=1)
            elif freq == 'monthly':
                # Add one month with simple logic
                month = current_start.month - 1 + interval
                year = current_start.year + month // 12
                month = month % 12 + 1
                day = min(current_start.day, calendar.monthrange(year, month)[1])
                current_start = current_start.replace(year=year, month=month, day=day)
                current_end = current_start + (base_end - base_start)
            elif freq == 'yearly':
                year = current_start.year + interval
                try:
                    current_start = current_start.replace(year=year)
                except ValueError:
                    # Handle Feb 29 in non-leap years
                    current_start = current_start.replace(month=2, day=28, year=year)
                current_end = current_start + (base_end - base_start)

        return instances
    
    def _build_instance(self, start: datetime, end: datetime):
        return {
            'title': self.event['name'],
            'start': start,
            'end': end,
        }
    
    def _expand_single_occurrence(self, event: EventEntity):
        return [self._build_instance(event['start_datetime'], event['end_datetime'])]
    
    def _parse_datetime(self, value):
        """
        Safely parse a datetime value that may already be a datetime object or a string.

        :param value: str or datetime
        :return: datetime object
        :raises ValueError: if value is neither a string nor a datetime
        """
        if isinstance(value, datetime):
            return value
        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid ISO datetime string: {value}")
        else:
            raise ValueError(f"Expected str or datetime, got {type(value)}")