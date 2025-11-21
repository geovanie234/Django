from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

# List all products
def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})

# Add a new product
def product_add(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "inventory/product_form.html", {"form": form})

# Edit an existing product
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "inventory/product_form.html", {"form": form})

# Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "inventory/product_delete.html", {"product": product})


# category management view

from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm

# List all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, "inventory/category_list.html", {"categories": categories})

# Add a new category
def category_add(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "inventory/category_form.html", {"form": form})

# Edit an existing category
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "inventory/category_form.html", {"form": form})

# Delete a category
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "inventory/category_delete.html", {"category": category})

# VIEWS FOR STOCK MANAGEMENT

from .forms import StockForm
from .models import Product, Transaction

# Stock In / Out
def stock_manage(request):
    form = StockForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        transaction = form.save(commit=False)
        product = transaction.product

        if transaction.transaction_type == "IN":
            product.quantity += transaction.quantity
        elif transaction.transaction_type == "OUT":
            if product.quantity >= transaction.quantity:
                product.quantity -= transaction.quantity
            else:
                return render(request, "stock_form.html", {
                    "form": form,
                    "error": "Not enough stock available!"
                })

        product.save()
        transaction.save()
        return redirect("stock_history")

    return render(request, "inventory/stock_form.html", {"form": form})

# STOCK HISTORY VIEW
def stock_history(request):
    transactions = Transaction.objects.order_by("-date")
    return render(request, "inventory/stock_history.html", {"transactions": transactions})

from django.shortcuts import render
from .models import Product, Category, Transaction

# DASHBOARD
def dashboard(request):
    # Basic stats
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    low_stock = Product.objects.filter(quantity__lt=10).count()
    recent_transactions = Transaction.objects.order_by('-date')[:5]

    # Chart Data: Product Quantity
    products = Product.objects.all()
    product_names = [p.name for p in products]
    product_quantities = [p.quantity for p in products]

    # Chart Data: Category Value
    categories = Category.objects.all()
    category_names = []
    category_values = []

    for cat in categories:
        items = Product.objects.filter(category=cat)
        total_value = sum([item.quantity * item.price for item in items])
        category_names.append(cat.name)
        category_values.append(total_value)

    return render(request, "inventory/dashboard.html", {
        "total_products": total_products,
        "total_categories": total_categories,
        "low_stock": low_stock,
        "recent_transactions": recent_transactions,
        "product_names": product_names,
        "product_quantities": product_quantities,
        "category_names": category_names,
        "category_values": category_values
    })




