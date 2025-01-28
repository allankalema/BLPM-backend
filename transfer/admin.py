from django.contrib import admin
from .models import  Transfer 
from users.models import Location, Account
from property.models import Property

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'location')
    search_fields = ('username', 'first_name', 'last_name', 'email')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('land_title', 'title_number', 'owner', 'location', 'total_area')
    list_filter = ('location', 'owner')

class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'land_title', 'status', 'transfer_date')
    search_fields = ('from_user__username', 'to_user__username', 'land_title__land_title')

admin.site.register(Account, AccountAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(Location)
