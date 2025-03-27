from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.maintenance, name='maintenance'),    
    path('create_ticket/<tool_id>/<order_id>', views.create_ticket, name='create_ticket'),
    path('create_new_ticket/', views.create_new_ticket, name='create_new_ticket'),
    path('edit_ticket/<ticket_id>', views.edit_ticket, name='edit_ticket'),
    path('complete_ticket/<ticket_id>', views.complete_ticket, name='complete_ticket'),
    path('view_ticket/<ticket_id>', views.view_ticket, name='view_ticket'),
]