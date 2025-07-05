from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['ip_address', 'created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        # Prevent manual addition of contact messages
        return False
    
    def has_change_permission(self, request, obj=None):
        # Allow editing but not creating
        return True
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion
        return True 