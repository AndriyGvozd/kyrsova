from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Item(models.Model):
    
    REGION_CHOICES = [
        ("Вінницька область", "Вінницька область"),
        ("Волинська область", "Волинська область"),
        ("Дніпропетровська область", "Дніпропетровська область"),
        ("Донецька область", "Донецька область"),
        ("Житомирська область", "Житомирська область"),
        ("Закарпатська область", "Закарпатська область"),
        ("Запорізька область", "Запорізька область"),
        ("Івано-Франківська область", "Івано-Франківська область"),
        ("Київ", "Київ"),
        ("Київська область", "Київська область"),
        ("Кіровоградська область", "Кіровоградська область"),
        ("Луганська область", "Луганська область"),
        ("Львівська область", "Львівська область"),
        ("Миколаївська область", "Миколаївська область"),
        ("Одеська область", "Одеська область"),
        ("Полтавська область", "Полтавська область"),
        ("Рівненська область", "Рівненська область"),
        ("Сумська область", "Сумська область"),
        ("Тернопільська область", "Тернопільська область"),
        ("Харківська область", "Харківська область"),
        ("Херсонська область", "Херсонська область"),
        ("Хмельницька область", "Хмельницька область"),
        ("Черкаська область", "Черкаська область"),
        ("Чернівецька область", "Чернівецька область"),
        ("Чернігівська область", "Чернігівська область"),
    ]
    
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=75)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    region = models.CharField(max_length=50, null=True, choices=REGION_CHOICES)
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
