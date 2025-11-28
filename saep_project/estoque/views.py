from django.shortcuts import get_object_or_404, redirect, render   # <-- adicionei render aqui
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout  # <-- adicionado
from django.db.models.functions import Lower  # <-- necessário para ordenação correta
from .models import Product, StockMovement
from .forms import ProductForm, StockMovementForm


# ============================================================
# LOGIN PERSONALIZADO
# ============================================================
def login_view(request):
    """
    Exibe o formulário de login e autentica o usuário.
    """
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect("estoque:product_list")
        else:
            return render(request, "estoque/login.html", {
                "error": "Usuário ou senha inválidos"
            })

    return render(request, "estoque/login.html")


# ============================================================
# LOGOUT PERSONALIZADO
# ============================================================
def logout_view(request):
    """
    Faz logout via POST e redireciona para a página de login.
    """
    if request.method == "POST":
        logout(request)
        return redirect("estoque:login")
    return redirect("estoque:login")


# ============================================================
# LISTAGEM DE PRODUTOS
# ============================================================
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'estoque/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        # ordenação A-Z ignorando maiúsculas/minúsculas
        qs = super().get_queryset().annotate(
            name_lower=Lower("name")
        ).order_by("name_lower")

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q).annotate(
                name_lower=Lower("name")
            ).order_by("name_lower")

        return qs


# ============================================================
# CRIAÇÃO DE PRODUTO
# ============================================================
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'estoque/product_form.html'
    success_url = reverse_lazy('estoque:product_list')


# ============================================================
# EDIÇÃO DE PRODUTO
# ============================================================
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'estoque/product_form.html'
    success_url = reverse_lazy('estoque:product_list')


# ============================================================
# EXCLUSÃO DE PRODUTO
# ============================================================
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'estoque/product_confirm_delete.html'
    success_url = reverse_lazy('estoque:product_list')


# ============================================================
# MOVIMENTAÇÃO DE ESTOQUE
# ============================================================
class StockMovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'estoque/stockmovement_form.html'
    success_url = reverse_lazy('estoque:product_list')

    def form_valid(self, form):
        # define o usuário que realizou a movimentação
        form.instance.performed_by = self.request.user

        product = form.cleaned_data['product']
        qty = form.cleaned_data['quantity']
        mtype = form.cleaned_data['movement_type']

        # atualiza estoque conforme o tipo de movimento
        if mtype == StockMovement.EXIT:
            product.stock -= qty
        else:
            product.stock += qty

        product.save()

        # verifica alerta de estoque mínimo
        if product.stock < product.min_stock:
            messages.warning(
                self.request,
                f"Atenção: o produto '{product.name}' está abaixo do estoque mínimo ({product.stock} < {product.min_stock})."
            )

        messages.success(self.request, "Movimentação registrada com sucesso.")
        return super().form_valid(form)
