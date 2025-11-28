from django import forms
from .models import Product, StockMovement

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Campos exibidos no formulário
        fields = ['name','description','stock','min_stock','storage']

    def clean_stock(self):
        # Validação para impedir estoque negativo
        s = self.cleaned_data.get('stock')
        if s < 0:
            raise forms.ValidationError("Estoque não pode ser negativo.")
        return s

    def clean_min_stock(self):
        # validação do estoque mínimo
        m = self.cleaned_data.get('min_stock')
        if m < 0:
            raise forms.ValidationError("Estoque mínimo não pode ser negativo.")
        return m


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        # Campos exibidos no formulário de movimentação
        fields = ['product','movement_type','quantity','notes']

    def clean_quantity(self):
        # impede quantidade zero ou negativa
        q = self.cleaned_data.get('quantity')
        if q <= 0:
            raise forms.ValidationError("Quantidade deve ser maior que zero.")
        return q
