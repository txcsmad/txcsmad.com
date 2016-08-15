from django.contrib import admin

from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'creator', 'start_time', 'end_time')
    list_filter = ('creator',)
    ordering = ('-start_time',)
