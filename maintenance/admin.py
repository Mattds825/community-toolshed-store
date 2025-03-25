from django.contrib import admin
from .models import MaintenanceTicket
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(MaintenanceTicket)
class MaintenanceTicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_number',
        'tool',
        'associated_order',
        'issue_description',
        'status',
        'created_date',
        'completion_date',
    )
    list_filter = ('status',)
    search_fields = ('ticket_number', 'tool', 'associated_order', 'issue_description', 'status', 'created_date', 'completion_date')
    ordering = ('-created_date',)