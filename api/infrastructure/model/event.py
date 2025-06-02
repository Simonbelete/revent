from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from infrastructure.constants import FREQ_CHOICES, WEEKDAYS
from infrastructure import model

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    calendar = models.ForeignKey(model.Calendar, on_delete=models.CASCADE, related_name='events')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    # Used for single start end date event
    end_datetime = models.DateTimeField()
    # Recurrence fields
    recurrence = models.BooleanField(default=False)
    
    # US-02 & Us-03
    freq = models.CharField(max_length=10, choices=FREQ_CHOICES, blank=True, null=True)
    interval = models.PositiveIntegerField(default=1)  # every n-th day/week/month

    # For weekly recurrence: selected weekdays, US-04
    weekdays = models.JSONField(blank=True, null=True)  # list of ints 0-6 representing days

    # For monthly relative date pattern: e.g. 2nd Friday
    # Store week number and weekday for relative monthly pattern, US-05
    relative_week_number = models.IntegerField(blank=True, null=True)  # e.g., 2 for second
    # US-04
    relative_weekday = models.IntegerField(choices=WEEKDAYS, blank=True, null=True)

    # End recurrence on date (optional), Single Occurrence 
    recurrence_end_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.recurrence:
            if self.freq not in dict(FREQ_CHOICES):
                raise ValidationError('Frequency must be daily, weekly or monthly if recurring.')
            if self.freq == 'weekly' and (not self.weekdays or len(self.weekdays) == 0):
                raise ValidationError('Weekdays must be selected for weekly recurrence.')
            if self.freq == 'monthly' and (self.relative_week_number is None or self.relative_weekday is None):
                raise ValidationError('Relative week number and weekday must be set for monthly relative recurrence.')
        else:
            if not self.start_datetime or not self.end_datetime:
                raise ValidationError('Start and end can not be null')
        super().clean()

    def __str__(self):
        return f"{self.name} ({self.start_datetime})"