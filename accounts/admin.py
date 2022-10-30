from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

# Register your models here.

class CustomAccountAdmin(UserAdmin):
    readonly_fields = (
        'is_active',
        'is_superuser',
        'date_joined'
    )
    
    fieldsets = (
        (
            None,
            {
                "fields": ('username', 'first_name', 'last_name', 'is_seller', 'date_joined', 'is_active', 'is_superuser'),
            },
        ),
    )


admin.site.register(Account, CustomAccountAdmin)
