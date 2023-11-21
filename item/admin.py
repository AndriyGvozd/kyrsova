from django.contrib import admin

from .models import Category, Item, Complaint, Region

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Complaint)
admin.site.register(Region)