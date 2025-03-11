from django.db import models

# Create your models here.

ITEM_TYPE = (
    (0, 'Tool'),
    (1, 'Party Item'),    
)


TOOL_CONDITION = (
    (0, 'New'),
    (1, 'Fair'),
    (2, 'Poor'),
)
# this is the category model
# it has a name, friendly name and a slug
# the friendly name is used to display the name in a more readable format
class Category(models.Model):
    name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255, null=True, blank=True)    

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name
    
# this is the item model
# it has a name and a type
# the type is an integer field with choices of ITEM_TYPE
# this is used to determine if the item is a tool or a party item
class Item(models.Model):    
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=ITEM_TYPE, default=0)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='items')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True) # separated by commas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
# this is the tool model
# it extends the item model
# the type is set to 0 by default
# this means that the item is a tool
class Tool(Item):
    # image_url = models.URLField(max_length=1024, null=True, blank=True)    
    serial_number = models.CharField(max_length=255)
    care_instructions = models.TextField(null=True, blank=True)
    is_written_off = models.BooleanField(default=False)
    needs_repair = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    condition = models.IntegerField(choices=TOOL_CONDITION, default=0)
    
    class Meta:
        verbose_name_plural = 'Tools'
    
    def __str__(self):
        # return name from Item class
        return self.name
    
# this is the party item model
# it extends the item model
# the type is set to 1 by default
# this means that the item is a party item
class PartyItem(Item):    
    stock_amount = models.IntegerField()
    available_amount = models.IntegerField()
    broken_amount = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Party Items'
    
    def __str__(self):
        # return name from Item class
        return self.name
