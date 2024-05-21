from django.contrib.auth.models import User
from item.models import Item
from django.db import models

class History(models.Model):
    user = models.ForeignKey(User, related_name='history_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='history_items', on_delete=models.CASCADE)
