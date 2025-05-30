from django.db.models import manager

from infrastructure import model
from .base_repository import BaseRepository

# class CalendarRepository(manager.BaseManager[model.Calendar]):
#     """Adapter: ORM -> Entity

#     Args:
#     """
#     def __init__(self):
#         super().__init__(model.Calendar)


class CalendarRepository(BaseRepository[model.Calendar]):
    def __init__(self):
        super().__init__(model.Calendar)