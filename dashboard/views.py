from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect

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
