from django.contrib import admin
from .models import InventoryItem, Category, Customer, Sale, InventoryLog
admin.site.register([InventoryItem, Category, Customer, Sale, InventoryLog])
