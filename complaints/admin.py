from django.contrib import admin
from .models import CustomUser, Complaint

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_superuser']
    list_filter = ['role', 'is_superuser']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'status', 'created_at']
    list_filter = ['priority', 'status']
    search_fields = ['title', 'user__username']