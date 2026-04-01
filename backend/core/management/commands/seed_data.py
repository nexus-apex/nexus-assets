from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Asset, AssetAssignment, MaintenanceLog
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusAssets with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusassets.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Asset.objects.count() == 0:
            for i in range(10):
                Asset.objects.create(
                    name=f"Sample Asset {i+1}",
                    asset_tag=f"Sample {i+1}",
                    category=random.choice(["laptop", "desktop", "monitor", "phone", "server", "network"]),
                    purchase_date=date.today() - timedelta(days=random.randint(0, 90)),
                    purchase_cost=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["in_use", "available", "maintenance", "retired"]),
                    assigned_to=f"Sample {i+1}",
                    location=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Asset records created'))

        if AssetAssignment.objects.count() == 0:
            for i in range(10):
                AssetAssignment.objects.create(
                    asset_name=f"Sample AssetAssignment {i+1}",
                    assigned_to=f"Sample {i+1}",
                    department=f"Sample {i+1}",
                    assigned_date=date.today() - timedelta(days=random.randint(0, 90)),
                    returned_date=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["active", "returned"]),
                    condition=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 AssetAssignment records created'))

        if MaintenanceLog.objects.count() == 0:
            for i in range(10):
                MaintenanceLog.objects.create(
                    asset_name=f"Sample MaintenanceLog {i+1}",
                    maintenance_type=random.choice(["repair", "upgrade", "inspection", "replacement"]),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    cost=round(random.uniform(1000, 50000), 2),
                    vendor=["TechVision Pvt Ltd","Global Solutions","Pinnacle Systems","Nova Enterprises","CloudNine Solutions","MetaForge Inc","DataPulse Analytics","QuantumLeap Tech","SkyBridge Corp","Zenith Innovations"][i],
                    status=random.choice(["scheduled", "in_progress", "completed"]),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 MaintenanceLog records created'))
