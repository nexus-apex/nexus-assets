from django.contrib import admin
from .models import Asset, AssetAssignment, MaintenanceLog

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ["name", "asset_tag", "category", "purchase_date", "purchase_cost", "created_at"]
    list_filter = ["category", "status"]
    search_fields = ["name", "asset_tag", "assigned_to"]

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ["asset_name", "assigned_to", "department", "assigned_date", "returned_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["asset_name", "assigned_to", "department"]

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ["asset_name", "maintenance_type", "date", "cost", "vendor", "created_at"]
    list_filter = ["maintenance_type", "status"]
    search_fields = ["asset_name", "vendor"]
