from django.contrib import admin
from .models import Category, Item, Tool, PartyItem

# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Tool)
admin.site.register(PartyItem)
