from django import forms
from .models import Product, StockMovement

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','stock','min_stock','storage']

    def clean_stock(self):
        s = self.cleaned_data.get('stock')
        if s < 0:
            raise forms.ValidationError("Estoque não pode ser negativo.")
        return s

    def clean_min_stock(self):
        m = self.cleaned_data.get('min_stock')
        if m < 0:
            raise forms.ValidationError("Estoque mínimo não pode ser negativo.")
        return m


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product','movement_type','quantity','notes']

    def clean_quantity(self):
        q = self.cleaned_data.get('quantity')
        if q <= 0:
            raise forms.ValidationError("Quantidade deve ser maior que zero.")
        return q
