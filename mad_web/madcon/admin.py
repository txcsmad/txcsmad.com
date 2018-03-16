from django.contrib import admin

from mad_web.madcon.models import Registration, MADcon


def change_status_to_accepted(modeladmin, request, queryset):
    queryset.update(status='A')
    change_status_to_accepted.short_description = "Mark selected registrations as accepted"


@admin.register(Registration)
class MADconRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'madcon_id', 'created_at', 'status', 'dietary_restrictions', "first_time", "t_shirt_size")
    ordering = ('-created_at',)
    actions = [change_status_to_accepted]


@admin.register(MADcon)
class MADconAdmin(admin.ModelAdmin):
    list_display = ('date', 'registration_open')
    ordering = ('-date',)
