from django.urls import path
from . import views

app_name = 'workforce'

urlpatterns = [
    path('', views.workforce_view, name='workforce'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('toggle/<int:id>/', views.toggle_attendance, name='toggle_attendance'),
]