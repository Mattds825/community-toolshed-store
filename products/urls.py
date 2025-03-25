from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('management/', views.management, name='management'),
    path('add_tool/', views.add_tool, name='add_tool'),
    path('add_party_item/', views.add_party_item, name='add_party_item'),
    path('edit_tool/<int:item_id>/', views.edit_tool, name='edit_tool'),
    path('edit_party_item/<int:item_id>/', views.edit_party_item, name='edit_party_item'),
]
