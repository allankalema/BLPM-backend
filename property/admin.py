from django.contrib import admin
from .models import Property, LandLocation

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('land_title', 'title_number', 'owner', 'total_area', 'date_surveyed')
    search_fields = ('land_title', 'title_number', 'owner__email', 'owner__username')
    list_filter = ('date_surveyed',)
    ordering = ('-date_surveyed',)

    fieldsets = (
        ("Property Details", {
            "fields": ("land_title", "title_number", "title_document", "owner"),
        }),
        ("Land Info", {
            "fields": ("total_area", "reference_point", "date_surveyed"),
        }),
    )

    def get_queryset(self, request):
        """Optimize query by selecting related fields"""
        return super().get_queryset(request).select_related('owner')

@admin.register(LandLocation)
class LandLocationAdmin(admin.ModelAdmin):
    list_display = ('property', 'latitude', 'longitude', 'altitude')
    search_fields = ('property__land_title', 'property__title_number')
    list_filter = ('property',)
    ordering = ('property__land_title',)

    fieldsets = (
        ("Location Details", {
            "fields": ("property", "latitude", "longitude", "altitude"),
        }),
    )

    def get_queryset(self, request):
        """Optimize query for the LandLocation model"""
        return super().get_queryset(request).select_related('property')
