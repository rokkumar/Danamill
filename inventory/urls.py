from django.urls import path
from .views import inventory_view

app_name = 'inventory'

urlpatterns = [
    path('', inventory_view, name='inventory'),
]