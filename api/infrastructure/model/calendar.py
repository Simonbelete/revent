from django.db import models

from .base import BaseModel
from .user import User

class Calendar(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendars')

