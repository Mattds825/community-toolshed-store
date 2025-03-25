from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.maintenance, name='maintenance'),    
    path('create_ticket/<tool_id>/<order_id>', views.create_ticket, name='create_ticket'),
    path('create_new_ticket/', views.create_new_ticket, name='create_new_ticket'),
]