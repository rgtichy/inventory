from __future__ import unicode_literals
from django.db import models

def validateItemData(item,description,price):
    error = False
    errors = []
    if len(item) < 1:
        errors.append('Please enter an Item name')
    if len(description) < 1:
        errors.append('Please enter an Item Description.')
    if not price:
        errors.append('Please enter an Item Price.')
    if len(errors) > 0:
        error = True
    return (error,errors)

class ItemManager(models.Manager):

    def newItem(self,data):

        item = data['item'].strip().lower()
        description = data['description'].strip()
        price = data['price'].strip()

        (error,errors) = validateItemData(item,description,price)

        if not error:
            item = Item.objects.create(name=item, description=description, price=price)
            return (True, item)
        else:
            return (False, errors)

    def editItem(self,data,id):
        name = data['item'].strip().lower()
        description = data['description'].strip()
        price = data['price'].strip()

        (error,errors) = validateItemData(name,description,price)

        if not error:
            existing = Item.objects.get(id=id)
            existing.name = name
            existing.price = price
            existing.description = description
            existing.save()
            return (False, existing)
        else:
            return (True, errors)

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length = 45)
    description = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 15, decimal_places = 4)
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    objects = ItemManager()
