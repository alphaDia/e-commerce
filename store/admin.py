from django.contrib import admin
from .models import Product, Variation
from category.models import Category


class VariationInline(admin.TabularInline):
    model = Product.variations.through

class CategoryInline(admin.TabularInline):
    model = Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category',
                    'modified_at', 'is_available',)
    prepopulated_fields = {'slug': ('name', )}
    inlines = [VariationInline]
    exclude = ('variations',)
    

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('variation_category', 'variation_value', 'is_active',)
    list_filter = ('variation_category', 'variation_value', 'is_active',)
    list_editable = ('is_active',)
    inlines = [VariationInline]
