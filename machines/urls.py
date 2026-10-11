from django.urls import path
from .views import machines_view

app_name = 'machines'
urlpatterns = [

    path('',machines_view,name='machines'),
]