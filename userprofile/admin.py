from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'role']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'dob', 'img', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    readonly_fields = ['date_joined', 'last_login']

admin.site.register(UserProfile, CustomUserAdmin)
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'seller', 'address', 'date_created')
admin.site.register(AddressD)
