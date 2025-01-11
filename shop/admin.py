# shop/admin.py
from django.contrib import admin
from .models import Category, Product, ProductImage, PriceHistory, Order, Review

class ProductImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 1

class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, PriceHistoryInline]
    list_display = ('name', 'category', 'price', 'stock', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sku')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    prepopulated_fields = {'slug': ('name',)}

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'rating', 'created_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(PriceHistory)
admin.site.register(Order)
admin.site.register(Review, ReviewAdmin)
