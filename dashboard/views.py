from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404, render, redirect
from dashboard.models import History, Wishlist
from item.models import Item
from django.contrib.auth.models import User
from django.contrib import messages


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

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).order_by('id').reverse()

    return render(request, 'dashboard/wishlist.html', {
        'items': items,
    })

@login_required
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    Wishlist.objects.get_or_create(user=request.user, item=item)
    return redirect('item:detail', pk=item_id)

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    Wishlist.objects.filter(user=request.user, item=item).delete()
    return redirect('item:detail', pk=item_id)

@login_required
def remove_from_wishlist2(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    Wishlist.objects.filter(user=request.user, item=item).delete()
    items = Wishlist.objects.filter(user=request.user).order_by('id').reverse()

    return render(request, 'dashboard/wishlist.html', {
        'items': items,
    })

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    items = Item.objects.filter(created_by=user).order_by('-created_at')

    return render(request, 'dashboard/user_profile.html', {
        'user_profile': user,
        'items': items,
    })

@login_required
def change_user_data(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Перевірка, чи імейл або нікнейм вже використовується
        if User.objects.exclude(id=request.user.id).filter(email=email).exists() or User.objects.exclude(id=request.user.id).filter(username=username).exists():
            error_message = 'Цей email або нікнейм вже використовується.'
            return render(request, 'dashboard/change_user_data.html', {'error_message': error_message})

        # Оновлення даних користувача
        user = request.user
        user.username = username
        user.email = email
        user.save()

        messages.success(request, 'Особисті дані оновлені')
        return redirect('dashboard:index')

    return render(request, 'dashboard/change_user_data.html')
