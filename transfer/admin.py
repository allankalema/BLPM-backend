from django.contrib import admin
from .models import Transfer
from property.models import Property
from django.contrib.auth import get_user_model

# Define the custom admin class for Transfer
class TransferAdmin(admin.ModelAdmin):
    list_display = ('land_title', 'from_user', 'to_user', 'status', 'transfer_date')
    list_filter = ('status', 'transfer_date')
    search_fields = ('land_title__land_title', 'from_user__username', 'to_user__username')
    ordering = ('-transfer_date',)
    autocomplete_fields = ('from_user', 'to_user', 'land_title')  # Use autocomplete for FK fields
    
    # Make the transfer_date read-only as it is auto-generated
    readonly_fields = ('transfer_date',)

    # You can also customize how the ForeignKey fields are displayed in the form view
    fieldsets = (
        (None, {
            'fields': ('land_title', 'from_user', 'to_user', 'status', 'transfer_date')
        }),
    )

    # Customize the display of the 'from_user' and 'to_user' fields in the list view
    def from_user_username(self, obj):
        return obj.from_user.username
    from_user_username.admin_order_field = 'from_user__username'  # Allow ordering by username
    from_user_username.short_description = 'From User'  # Display name in the admin

    def to_user_username(self, obj):
        return obj.to_user.username
    to_user_username.admin_order_field = 'to_user__username'  # Allow ordering by username
    to_user_username.short_description = 'To User'  # Display name in the admin

# Register the model with the admin site
admin.site.register(Transfer, TransferAdmin)
