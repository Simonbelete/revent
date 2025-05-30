from rest_framework import mixins

class CrudUseCase(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    """Generic abstractor for DRF CRUD actions
    """
    pass