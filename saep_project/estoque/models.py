from django.db import models
from django.contrib.auth import get_user_model

# Usando o modelo de usuário padrão do Django
User = get_user_model()

class Product(models.Model):
    name = models.CharField("Nome", max_length=200)
    description = models.TextField("Descrição", blank=True)
    stock = models.IntegerField("Estoque atual", default=0)
    min_stock = models.IntegerField("Estoque mínimo", default=0)
    # Informação extra do produto (ex: armazenamento dos celulares)
    storage = models.CharField("Armazenamento", max_length=100, blank=True)

    class Meta:
        # Ordenação alfabética dos produtos
        ordering = ['name']

    def __str__(self):
        return self.name


class StockMovement(models.Model):
    # Tipos de movimentação
    ENTRY = 'E'
    EXIT = 'S'
    TYPE_CHOICES = [
        (ENTRY, 'Entrada'),
        (EXIT, 'Saída'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField("Tipo", max_length=1, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField("Quantidade")
    # Usuário que realizou a operação
    performed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    # Salva a data automaticamente
    date = models.DateTimeField("Data", auto_now_add=True)
    notes = models.TextField("Observações", blank=True)

    class Meta:
        # Mostra movimentações mais recentes primeiro
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity} - {self.product.name}"
