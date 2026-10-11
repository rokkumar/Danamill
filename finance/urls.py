from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('income/', views.income_view, name='income'),
    path('expense/', views.expense_view, name='expense'),
]