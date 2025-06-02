
from django.contrib import admin

from infrastructure import model

@admin.register(model.Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
