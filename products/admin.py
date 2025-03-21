from django.contrib import admin
from .models import Category, Item, Tool, PartyItem
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):    
    list_display = (
        'name',
        'friendly_name',
    )
    list_filter = ('name','friendly_name')
    search_fields = ('name','friendly_name')


# admin.site.register(Item)

@admin.register(Item)
class ItemAdmin(SummernoteModelAdmin):    
    list_display = (
        'name',
        'type',
        'category',        
        'price',
        'rating',     
    )
    list_filter = ('name','type','category','price','rating')
    search_fields = ('name','type','category')


# Custom admin action to duplicate a Tool instance
def duplicate_tool(modeladmin, request, queryset):
    for tool in queryset:
        print(tool.pk)
        
        # create a new instance of the Tool model
        new_tool = Tool.objects.create(
            name=tool.name,
            category=tool.category,
            description=tool.description,
            price=tool.price,
            rating=tool.rating,
            image=tool.image,
            keywords=tool.keywords,
            serial_number=f"{tool.serial_number}_copy",
            sku=tool.sku,
            care_instructions=tool.care_instructions,
        )
       
        new_tool.save() 
        
        # tool_copy.save()

duplicate_tool.short_description = "Duplicate selected tools"

@admin.register(Tool)
class ToolAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = (
        'name',
        'category',        
        'price',
        'rating',        
        'serial_number',        
        'is_written_off',
        'needs_repair',
        'is_available',
        'created_at',
        'updated_at',
    )
    list_filter = ('name','category','price','rating','is_written_off','needs_repair','is_available','created_at','updated_at')
    search_fields = ('name','category','serial_number')
    actions = [duplicate_tool]

# admin.site.register(PartyItem)

@admin.register(PartyItem)
class PartyItemAdmin(SummernoteModelAdmin):    
    list_display = (
        'name',
        'category',        
        'price',
        'rating',                        
        'stock_amount',
        'broken_amount',
        'available_amount',        
        'created_at',
        'updated_at',
    )
    list_filter = ('name','category','price','rating','stock_amount','broken_amount','available_amount','created_at','updated_at')
    search_fields = ('name','category')
