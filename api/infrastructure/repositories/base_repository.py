
from typing import Type, TypeVar, Generic
from django.db import models

from domain import abstract

Model = TypeVar("Model", bound=models.Model)

class BaseRepository(Generic[Model], abstract.AbstractRepository):
    """Adapter: ORM -> Entity

    Args:
        Generic (_type_): _description_
    """
    def __init__(self, model: Type[Model]):
        self.model = model
    
    def all(self):  # instance method
        return self.model.objects.all()
    