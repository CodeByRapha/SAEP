from django.contrib import admin
from .models import Product, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stock', 'min_stock')
    search_fields = ('name', 'description')
    list_filter = ('min_stock',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'movement_type', 'quantity', 'performed_by', 'date')
    list_filter = ('movement_type','date')
    search_fields = ('product__name',)
