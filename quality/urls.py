from django.urls import path
from .views import quality_view

app_name = 'quality'

urlpatterns = [
    path('', quality_view, name='quality-app'),
]