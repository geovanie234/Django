from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Category, Product, Transaction
from django.utils.html import format_html


# ------------ 1. EXPORT CSV ACTION ------------
def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{modeladmin.model.__name__}.csv"'

    writer = csv.writer(response)
    fields = [field.name for field in modeladmin.model._meta.fields]

    writer.writerow(fields)

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])

    return response

export_to_csv.short_description = "Export Selected to CSV"


# ------------ 2. CATEGORY ADMIN ------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    actions = [export_to_csv]


# ------------ 3. PRODUCT ADMIN ------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "price", "stock_value")
    list_filter = ("category",)
    search_fields = ("name",)
    actions = [export_to_csv]

    # Stock Value Column
    def stock_value(self, obj):
        value = obj.quantity * obj.price
        return f"${value:.2f}"

    stock_value.short_description = "Stock Value"


# ------------ 4. TRANSACTION ADMIN (+ colored badges) ------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("product", "colored_type", "quantity", "date")
    list_filter = ("transaction_type", "date")
    actions = [export_to_csv]

    # Colored Badge
    def colored_type(self, obj):
        color = "green" if obj.transaction_type == "IN" else "red"
        return format_html(f"<strong><span style='color:{color};'>{obj.transaction_type}</span></strong>")

    colored_type.short_description = "Type"


# ------------ 5. CUSTOM ADMIN DASHBOARD ------------
from django.contrib.admin import AdminSite

class InventoryAdminSite(AdminSite):
    site_header = "Inventory Management Admin"
    site_title = "Inventory Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_stock_value = sum([p.quantity * p.price for p in Product.objects.all()])
        recent = Transaction.objects.order_by('-date')[:5]

        extra_context = extra_context or {}
        extra_context.update({
            "total_products": total_products,
            "total_categories": total_categories,
            "total_stock_value": total_stock_value,
            "recent": recent,
        })
        return super().index(request, extra_context)

# Replace default admin
custom_admin_site = InventoryAdminSite(name="custom_admin")

custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Product, ProductAdmin)
custom_admin_site.register(Transaction, TransactionAdmin)


# Register your models here.
