from dataclasses import dataclass

from base import BaseEntity

@dataclass
class CalendarEntity(BaseEntity):
    name: str = None
    