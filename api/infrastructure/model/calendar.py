from django.db import models
from django.contrib.auth.models import User

from .base import BaseModel
class Calendar(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendars')

    def __str__(self):
        return f"{self.name}"