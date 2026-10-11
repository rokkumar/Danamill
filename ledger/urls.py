from django.urls import path
from . import views

app_name = 'ledger'

urlpatterns = [
    # Landing page — lists all clients
    path('', views.client_list, name='client_list'),

    # Add new client
    path('client/add/', views.add_client, name='add_client'),

    # Single client ledger
    path('client/<int:client_id>/', views.client_ledger, name='client_ledger'),

    # Add entry for a specific client
    path('client/<int:client_id>/add-entry/', views.add_entry, name='add_entry'),

    # NEW: Edit and delete entries
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
]