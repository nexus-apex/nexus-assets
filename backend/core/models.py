from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=255)
    asset_tag = models.CharField(max_length=255, blank=True, default="")
    category = models.CharField(max_length=50, choices=[("laptop", "Laptop"), ("desktop", "Desktop"), ("monitor", "Monitor"), ("phone", "Phone"), ("server", "Server"), ("network", "Network")], default="laptop")
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("in_use", "In Use"), ("available", "Available"), ("maintenance", "Maintenance"), ("retired", "Retired")], default="in_use")
    assigned_to = models.CharField(max_length=255, blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class AssetAssignment(models.Model):
    asset_name = models.CharField(max_length=255)
    assigned_to = models.CharField(max_length=255, blank=True, default="")
    department = models.CharField(max_length=255, blank=True, default="")
    assigned_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("returned", "Returned")], default="active")
    condition = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.asset_name

class MaintenanceLog(models.Model):
    asset_name = models.CharField(max_length=255)
    maintenance_type = models.CharField(max_length=50, choices=[("repair", "Repair"), ("upgrade", "Upgrade"), ("inspection", "Inspection"), ("replacement", "Replacement")], default="repair")
    date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vendor = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("scheduled", "Scheduled"), ("in_progress", "In Progress"), ("completed", "Completed")], default="scheduled")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.asset_name
