from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=55)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Regions'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=75)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    region = models.ForeignKey(Region, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Complaint(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    post = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='complaints')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint #{self.id} - {self.post.name}"
