"""
URL configuration for danamill project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views
from accounts import views as account_views


urlpatterns = [
    # Hidden Django admin (used rarely — custom dashboard is the main UI)
    path(settings.ADMIN_URL, admin.site.urls),

    # ---------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path('logout/', account_views.logout_view, name='logout'),

    # ---------------------------------------------------------
    # Public site
    # ---------------------------------------------------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('infrastructure/', views.infrastructure, name='infrastructure'),
    path('contact/', views.contact, name='contact'),
    path('quality/', views.quality, name='quality'),

    path('', include('Enquiry.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),

    # ---------------------------------------------------------
    # Custom dashboard (ERP)
    # ---------------------------------------------------------
    # Main dashboard (Reports / Analytics)
    path('dashboard/', include('reports.urls')),

    # Sub-modules

    path('dashboard/ledger/', include('ledger.urls')),
    path('dashboard/inventory/', include('inventory.urls')),
    path('dashboard/production/', include('production.urls')),
    path('dashboard/machines/', include('machines.urls')),
    path('dashboard/workforce/', include('workforce.urls')),
    path('dashboard/quality/', include('quality.urls')),
    path('dashboard/finance/', include('finance.urls')),
    path('dashboard/dispatch/', include('dispatch.urls')),
    # path('dashboard/reports/', include('reports.urls')),
    path('dashboard/events/', include('events.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)