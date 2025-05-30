from abc import ABC, abstractmethod
from django.db.models.query import QuerySet

class AbstractRepository(QuerySet, ABC):
    pass