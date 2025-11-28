from django.contrib import admin
from .models import Product, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Campos exibidos na listagem do admin
    list_display = ('id', 'name', 'stock', 'min_stock')
    # Permite buscar produtos por nome ou descrição
    search_fields = ('name', 'description')
    # Filtros laterais no admin
    list_filter = ('min_stock',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    # Listagem das movimentações no admin
    list_display = ('id', 'product', 'movement_type', 'quantity', 'performed_by', 'date')
    # Filtros úteis para localizar movimentações
    list_filter = ('movement_type','date')
    # Busca por nome do produto relacionado
    search_fields = ('product__name',)
