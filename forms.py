from django import forms
from .models import Product, Category, Transaction

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price', 'description']


class StockForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'transaction_type', 'quantity']

        # transactions
        from .models import Transaction
from django import forms

class StockForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'transaction_type', 'quantity']

