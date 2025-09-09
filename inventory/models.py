from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    owner = models.ForeignKey(User, related_name='inventory_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dose = models.CharField(max_length=50, blank=True)          # e.g., "500mg"
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.dose})"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    item = models.ForeignKey(InventoryItem, related_name='sales', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, related_name='sales', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    sold_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.item.name} x{self.quantity}"

class InventoryLog(models.Model):
    item = models.ForeignKey(InventoryItem, related_name='logs', on_delete=models.CASCADE)
    change_amount = models.IntegerField()   # positive if restock, negative if sale
    change_type = models.CharField(max_length=20, choices=(('restock','restock'),('sale','sale'),('update','update')))
    timestamp = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.item.name}: {self.change_amount} ({self.change_type})"
