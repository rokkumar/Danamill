from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Events
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),

    # Items
    path('<int:event_id>/item/add/', views.item_create, name='item_create'),
    path('item/<int:item_id>/edit/', views.item_edit, name='item_edit'),
    path('item/<int:item_id>/delete/', views.item_delete, name='item_delete'),
]