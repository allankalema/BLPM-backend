from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('land_title', 'title_number', 'owner', 'location', 'total_area', 'date_surveyed')
    search_fields = ('land_title', 'title_number', 'owner__email', 'owner__username', 'location__name')
    list_filter = ('location', 'date_surveyed')
    ordering = ('-date_surveyed',)

    fieldsets = (
        ("Property Details", {
            "fields": ("land_title", "title_number", "title_document", "owner", "location"),
        }),
        ("Coordinates & Survey Info", {
            "fields": ("latitude", "longitude", "altitude", "total_area", "reference_point", "date_surveyed"),
        }),
    )

    def get_queryset(self, request):
        """Optimize query by selecting related fields"""
        return super().get_queryset(request).select_related('owner', 'location')
