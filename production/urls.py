from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.production_view, name='production'),
    path('batches/', views.batches_view, name='batches'),
    path('analytics/', views.analytics_view, name='analytics'),
]