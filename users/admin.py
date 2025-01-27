from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Location


class AccountAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'land_owner', 'surveyor', 'govt_official', 'law_enforcement')
    list_filter = ('is_staff', 'land_owner', 'surveyor', 'govt_official', 'law_enforcement')

    # Fields to display in the admin detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'middle_name', 'last_name', 'email', 'date_of_birth', 'nin', 'location')}),
        ('Roles', {'fields': ('land_owner', 'surveyor', 'govt_official', 'law_enforcement')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    # Fields to display when creating a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'nin', 'password1', 'password2', 'is_staff'),
        }),
    )

    # Fields to use for searching in the admin
    search_fields = ('username', 'email', 'first_name', 'last_name', 'nin')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')


# Register the Account model
admin.site.register(Account, AccountAdmin)


# Register the Location model
class LocationAdmin(admin.ModelAdmin):
    list_display = ('village', 'parish', 'subcounty', 'county', 'district', 'country')
    search_fields = ('village', 'parish', 'subcounty', 'county', 'district', 'country')
    ordering = ('country', 'district', 'county', 'subcounty', 'parish', 'village')


admin.site.register(Location, LocationAdmin)
