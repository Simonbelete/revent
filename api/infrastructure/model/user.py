from django.db import models

from .base import BaseModel

class User(BaseModel):
    name = models.CharField(max_length=100)