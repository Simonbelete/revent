from django.db import models

from .timestamped import TimestampedModel

class BaseModel(TimestampedModel):
    class Meta:
        abstract = True
        ordering = ['-created_at']