from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/create/', views.asset_create, name='asset_create'),
    path('assets/<int:pk>/edit/', views.asset_edit, name='asset_edit'),
    path('assets/<int:pk>/delete/', views.asset_delete, name='asset_delete'),
    path('assetassignments/', views.assetassignment_list, name='assetassignment_list'),
    path('assetassignments/create/', views.assetassignment_create, name='assetassignment_create'),
    path('assetassignments/<int:pk>/edit/', views.assetassignment_edit, name='assetassignment_edit'),
    path('assetassignments/<int:pk>/delete/', views.assetassignment_delete, name='assetassignment_delete'),
    path('maintenancelogs/', views.maintenancelog_list, name='maintenancelog_list'),
    path('maintenancelogs/create/', views.maintenancelog_create, name='maintenancelog_create'),
    path('maintenancelogs/<int:pk>/edit/', views.maintenancelog_edit, name='maintenancelog_edit'),
    path('maintenancelogs/<int:pk>/delete/', views.maintenancelog_delete, name='maintenancelog_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
