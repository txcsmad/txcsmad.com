from django.contrib import admin

from mad_web.madcon.models import Registration


@admin.register(Registration)
class MADconApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status', 'dietary_restrictions', "first_time", "t_shirt_size")
    ordering = ('-created_at',)
