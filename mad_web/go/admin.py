from django.contrib import admin

from .models import Go

@admin.register(Go)
class GoAdmin(admin.ModelAdmin):
    list_display = ('id', 'url')
