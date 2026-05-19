from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_create, name='create_order'),
    path('success/', views.order_success, name='order_success'),
]