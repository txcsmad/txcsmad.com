from django.contrib import admin

from mad_web.madcon.models import Registration, MADcon


@admin.register(Registration)
class MADconRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status', 'dietary_restrictions', "first_time", "t_shirt_size")
    ordering = ('-created_at',)


@admin.register(MADcon)
class MADconAdmin(admin.ModelAdmin):
    list_display = ('date',)
    ordering = ('-date',)
