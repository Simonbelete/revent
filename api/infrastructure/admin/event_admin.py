
from django.contrib import admin

from infrastructure import model

@admin.register(model.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
