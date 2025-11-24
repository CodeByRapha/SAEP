from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField("Nome", max_length=200)
    description = models.TextField("Descrição", blank=True)
    stock = models.IntegerField("Estoque atual", default=0)
    min_stock = models.IntegerField("Estoque mínimo", default=0)
    # campos extras exemplares
    storage = models.CharField("Armazenamento", max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StockMovement(models.Model):
    ENTRY = 'E'
    EXIT = 'S'
    TYPE_CHOICES = [
        (ENTRY, 'Entrada'),
        (EXIT, 'Saída'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField("Tipo", max_length=1, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField("Quantidade")
    performed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField("Data", auto_now_add=True)
    notes = models.TextField("Observações", blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity} - {self.product.name}"
