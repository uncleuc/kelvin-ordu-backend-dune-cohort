from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name', 'price', 'category', 'stock', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'category__name')
    ordering = ('-created_at',)
    actions = ['mark_out_of_stock']

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px;border-radius:6px;object-fit:cover;" alt="{}"/>',
                obj.image.url,
                obj.name,
            )
        return '-'

    image_tag.short_description = 'Image'

    def mark_out_of_stock(self, request, queryset):
        updated = queryset.update(stock=0, is_available=False)
        self.message_user(request, f'{updated} products marked as out of stock.')

    mark_out_of_stock.short_description = 'Mark selected products as out of stock'
