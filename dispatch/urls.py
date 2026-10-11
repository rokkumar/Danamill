from django.urls import path
from .views import dispatch_view

app_name = 'dispatch'

urlpatterns = [
    path('', dispatch_view, name='dispatch'),
]