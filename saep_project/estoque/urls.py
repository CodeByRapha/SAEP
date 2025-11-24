from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # LOGIN / LOGOUT PERSONALIZADOS
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # PRODUTOS
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # MOVIMENTAÇÃO DE ESTOQUE
    path('movement/add/', views.StockMovementCreateView.as_view(), name='movement_add'),
]
