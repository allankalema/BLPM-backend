from django.contrib import admin
from .models import Transfer

class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'land_title', 'status', 'transfer_date')
    list_filter = ('status', 'transfer_date')
    search_fields = ('from_user__username', 'to_user__username', 'land_title__land_title')
    ordering = ('-transfer_date',)

admin.site.register(Transfer, TransferAdmin)
