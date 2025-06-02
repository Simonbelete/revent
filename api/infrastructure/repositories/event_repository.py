from django.db.models import manager

from infrastructure import model
from .base_repository import BaseRepository

class EventRepository(BaseRepository[model.Event]):
    def __init__(self):
        super().__init__(model.Event)