from django.contrib import admin
from .models import Property

# Define an inline admin descriptor for the Property model
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('land_title', 'title_number', 'owner', 'location', 'latitude', 'longitude', 'altitude', 'total_area', 'reference_point', 'date_surveyed')
    search_fields = ('land_title', 'title_number', 'owner__username', 'location__name')
    list_filter = ('location', 'date_surveyed')
    ordering = ('-date_surveyed',)
    
    # Optionally, add actions
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        # Example action to mark selected properties as verified
        queryset.update(is_verified=True)
    mark_as_verified.short_description = "Mark selected properties as verified"

# Register the Property model with the custom admin
admin.site.register(Property, PropertyAdmin)
