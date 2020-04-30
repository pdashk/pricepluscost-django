from django.contrib import admin
from django.conf import settings
from .models import State

from eia.utils.update import update_state_data

class StateAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'series_id',
        'iso3166',
        'rolling_average',
        'average_start_date',
        'average_end_date',
        'source_update_date',
        'last_updated',
    ]

    readonly_fields = ['last_updated']

    actions = ['refresh_state_data']

    def refresh_state_data(self, request, queryset):
        
        updates = []

        for obj in queryset:
            update = update_state_data(settings.EIA_API_KEY, obj)
            updates.append(update)
        
        self.message_user(request, f"Successfully refreshed {sum(updates)}/{len(updates)} selected states")

admin.site.register(State, StateAdmin)