from dataclasses import dataclass
from datetime import datetime

from .base import BaseEntity

@dataclass
class EventEntity(BaseEntity):
    name: str = None
    start_datetime: datetime = None
    end_datetime: datetime = None
    recurrence: bool = False