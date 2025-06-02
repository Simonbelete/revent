from datetime import datetime, timedelta
import calendar

def expand_recurring_event(event, range_start, range_end):
    """
    Generate recurring instances of an event between range_start and range_end.
    Supports daily, weekly, and monthly relative recurrences.

    :param event: Dict with recurrence info
    :param range_start: datetime
    :param range_end: datetime
    :return: List of event instances (start, end)
    """
    instances = []
    base_start = datetime.fromisoformat(event['start_datetime'])
    base_end = datetime.fromisoformat(event['end_datetime'])

    freq = event.get('freq')
    interval = event.get('interval', 1)
    weekdays = event.get('weekdays') or []
    recurrence_end = datetime.strptime(event['recurrence_end_date'], "%Y-%m-%d") if event.get('recurrence_end_date') else range_end

    current_start = base_start
    current_end = base_end

    while current_start <= range_end and current_start <= recurrence_end:
        if current_start >= range_start:
            if freq == 'daily':
                instances.append((current_start, current_end))
            elif freq == 'weekly':
                if current_start.weekday() in weekdays:
                    instances.append((current_start, current_end))
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
                    end = datetime.combine(date, base_end.time())
                    if range_start <= start <= range_end and start <= recurrence_end:
                        instances.append((start, end))
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

    return instances
