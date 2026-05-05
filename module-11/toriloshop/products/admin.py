from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'category__name')
    ordering = ('-created_at',)
    actions = ['mark_out_of_stock']

    def mark_out_of_stock(self, request, queryset):
        updated = queryset.update(stock=0, is_available=False)
        self.message_user(request, f'{updated} products marked as out of stock.')

    mark_out_of_stock.short_description = 'Mark selected products as out of stock'
