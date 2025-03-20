from django.contrib import admin
from .models import Order, OrderItem
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

admin.site.register(OrderItem)
class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_total',)
    extra = 0

@admin.register(Order)
class OrderAdmin(SummernoteModelAdmin):    
    inlines = (OrderItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'order_total', 'payment_status', 'start_date', 'end_date', 'original_cart', 'stripe_pid')
    list_display = (
        'order_number',
        'date',
        'start_date',
        'end_date',
        'order_total',
        'payment_status',     
    )
    list_filter = ('order_number','date','start_date','end_date','order_total','payment_status')
    search_fields = ('order_number','date','start_date','end_date')
    ordering = ('-date',)