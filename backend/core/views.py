import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Asset, AssetAssignment, MaintenanceLog


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['asset_count'] = Asset.objects.count()
    ctx['asset_laptop'] = Asset.objects.filter(category='laptop').count()
    ctx['asset_desktop'] = Asset.objects.filter(category='desktop').count()
    ctx['asset_monitor'] = Asset.objects.filter(category='monitor').count()
    ctx['asset_total_purchase_cost'] = Asset.objects.aggregate(t=Sum('purchase_cost'))['t'] or 0
    ctx['assetassignment_count'] = AssetAssignment.objects.count()
    ctx['assetassignment_active'] = AssetAssignment.objects.filter(status='active').count()
    ctx['assetassignment_returned'] = AssetAssignment.objects.filter(status='returned').count()
    ctx['maintenancelog_count'] = MaintenanceLog.objects.count()
    ctx['maintenancelog_repair'] = MaintenanceLog.objects.filter(maintenance_type='repair').count()
    ctx['maintenancelog_upgrade'] = MaintenanceLog.objects.filter(maintenance_type='upgrade').count()
    ctx['maintenancelog_inspection'] = MaintenanceLog.objects.filter(maintenance_type='inspection').count()
    ctx['maintenancelog_total_cost'] = MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0
    ctx['recent'] = Asset.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def asset_list(request):
    qs = Asset.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(category=status_filter)
    return render(request, 'asset_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def asset_create(request):
    if request.method == 'POST':
        obj = Asset()
        obj.name = request.POST.get('name', '')
        obj.asset_tag = request.POST.get('asset_tag', '')
        obj.category = request.POST.get('category', '')
        obj.purchase_date = request.POST.get('purchase_date') or None
        obj.purchase_cost = request.POST.get('purchase_cost') or 0
        obj.status = request.POST.get('status', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.location = request.POST.get('location', '')
        obj.save()
        return redirect('/assets/')
    return render(request, 'asset_form.html', {'editing': False})


@login_required
def asset_edit(request, pk):
    obj = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.asset_tag = request.POST.get('asset_tag', '')
        obj.category = request.POST.get('category', '')
        obj.purchase_date = request.POST.get('purchase_date') or None
        obj.purchase_cost = request.POST.get('purchase_cost') or 0
        obj.status = request.POST.get('status', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.location = request.POST.get('location', '')
        obj.save()
        return redirect('/assets/')
    return render(request, 'asset_form.html', {'record': obj, 'editing': True})


@login_required
def asset_delete(request, pk):
    obj = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/assets/')


@login_required
def assetassignment_list(request):
    qs = AssetAssignment.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(asset_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'assetassignment_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def assetassignment_create(request):
    if request.method == 'POST':
        obj = AssetAssignment()
        obj.asset_name = request.POST.get('asset_name', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.department = request.POST.get('department', '')
        obj.assigned_date = request.POST.get('assigned_date') or None
        obj.returned_date = request.POST.get('returned_date') or None
        obj.status = request.POST.get('status', '')
        obj.condition = request.POST.get('condition', '')
        obj.save()
        return redirect('/assetassignments/')
    return render(request, 'assetassignment_form.html', {'editing': False})


@login_required
def assetassignment_edit(request, pk):
    obj = get_object_or_404(AssetAssignment, pk=pk)
    if request.method == 'POST':
        obj.asset_name = request.POST.get('asset_name', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.department = request.POST.get('department', '')
        obj.assigned_date = request.POST.get('assigned_date') or None
        obj.returned_date = request.POST.get('returned_date') or None
        obj.status = request.POST.get('status', '')
        obj.condition = request.POST.get('condition', '')
        obj.save()
        return redirect('/assetassignments/')
    return render(request, 'assetassignment_form.html', {'record': obj, 'editing': True})


@login_required
def assetassignment_delete(request, pk):
    obj = get_object_or_404(AssetAssignment, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/assetassignments/')


@login_required
def maintenancelog_list(request):
    qs = MaintenanceLog.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(asset_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(maintenance_type=status_filter)
    return render(request, 'maintenancelog_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def maintenancelog_create(request):
    if request.method == 'POST':
        obj = MaintenanceLog()
        obj.asset_name = request.POST.get('asset_name', '')
        obj.maintenance_type = request.POST.get('maintenance_type', '')
        obj.date = request.POST.get('date') or None
        obj.cost = request.POST.get('cost') or 0
        obj.vendor = request.POST.get('vendor', '')
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/maintenancelogs/')
    return render(request, 'maintenancelog_form.html', {'editing': False})


@login_required
def maintenancelog_edit(request, pk):
    obj = get_object_or_404(MaintenanceLog, pk=pk)
    if request.method == 'POST':
        obj.asset_name = request.POST.get('asset_name', '')
        obj.maintenance_type = request.POST.get('maintenance_type', '')
        obj.date = request.POST.get('date') or None
        obj.cost = request.POST.get('cost') or 0
        obj.vendor = request.POST.get('vendor', '')
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/maintenancelogs/')
    return render(request, 'maintenancelog_form.html', {'record': obj, 'editing': True})


@login_required
def maintenancelog_delete(request, pk):
    obj = get_object_or_404(MaintenanceLog, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/maintenancelogs/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['asset_count'] = Asset.objects.count()
    data['assetassignment_count'] = AssetAssignment.objects.count()
    data['maintenancelog_count'] = MaintenanceLog.objects.count()
    return JsonResponse(data)
