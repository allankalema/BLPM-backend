from django.contrib import admin
from .models import Account, Location

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'nin', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'nin')
    list_filter = ('is_active', 'is_staff', 'land_owner', 'surveyor', 'govt_official', 'law_enforcement')
    ordering = ('username',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('account', 'village', 'parish', 'subcounty', 'county', 'district', 'country')
    search_fields = ('village', 'parish', 'subcounty', 'county', 'district', 'country')
    list_filter = ('district', 'county', 'country')
    ordering = ('district', 'county', 'village')

# Register the models with the admin site
admin.site.register(Account, AccountAdmin)
admin.site.register(Location, LocationAdmin)
