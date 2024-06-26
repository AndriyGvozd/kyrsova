from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .enviroment import REGIONS
from .forms import NewItemForm, EditItemForm, ComplaintForm
from .models import Category, Item, Complaint, Region
from django.db.models.functions import Lower
from dashboard.models import History, Wishlist

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category')
    if category_id:
        category_id = int(category_id)
    else:
        category_id = 0
    region_id = request.GET.get('region')
    if region_id:
        region_id = int(region_id)
    else:
        region_id = 0
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', float('inf'))

    categories = Category.objects.all()
    regions = Region.objects.all()
    all_items = Item.objects.filter(is_sold=False).order_by('-created_at')

    if category_id is not "0" and category_id:
        all_items = all_items.filter(category_id=int(category_id))
    
    if query:
        all_items = all_items.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(name__icontains=query[1:]) | Q(description__icontains=query[1:])
    )
        
    if region_id is not "0" and region_id:
        all_items = all_items.filter(region_id=int(region_id))

    if min_price and max_price:
        min_price, max_price = float(min_price), float(max_price)
        if max_price > 0 and min_price > max_price:
            min_price, max_price = max_price, min_price
        all_items = all_items.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        all_items = all_items.filter(price__gte=min_price)

    paginator = Paginator(all_items, 9)
    
    page = request.GET.get('page', 1)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'region_id': int(region_id),
        'regions': regions, 
        'min_price': min_price,
        'max_price': max_price,
    })
    
    

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    in_wishlist = False
    if request.user.is_authenticated:
        history_record = History.objects.filter(user=request.user, item=item).first()
        
        if history_record:
            history_record.delete()
        History.objects.create(user=request.user, item=item)
        in_wishlist = Wishlist.objects.filter(user=request.user, item=item).exists()

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'in_wishlist': in_wishlist
    })

@login_required    
def complaint(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)

        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.author = request.user
            complaint.post = item
            complaint.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = ComplaintForm()

    return render(request, 'item/form.html', {'item': item, 'form': form})

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Створення оголошення',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Редагування',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    complaints = Complaint.objects.filter(post=pk)
    complaints.delete()
    item.delete()
    return redirect('dashboard:index')

def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'item/complaint.html', {'complaints': complaints})

