from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from dashboard.models import History
from item.models import Item

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)

    if request.method == 'POST':
        auth_logout(request)
        return redirect('core:index')  

    return render(request, 'dashboard/index.html', {
        'items': items,
    })

@login_required
def history(request):
    items = History.objects.filter(user=request.user).order_by('id').reverse()

    return render(request, 'dashboard/history.html', {
        'items': items,
    })