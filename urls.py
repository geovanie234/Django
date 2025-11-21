from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Category Management
path('categories/', views.category_list, name='category_list'),
path('categories/add/', views.category_add, name='category_add'),
path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

# Stock Management
path('stock/', views.stock_manage, name='stock_manage'),
path('stock/history/', views.stock_history, name='stock_history'),

# dashboard




]
