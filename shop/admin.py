from django.contrib import admin
from .models import Product, ProductImage, ProductSpecification, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return ""
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price','stock','is_active','created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title','description')
    inlines = [ProductImageInline, ProductSpecificationInline]  # add both inlines

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product','price','quantity')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','email','status','created_at')
    list_filter = ('status','created_at')
    inlines = [OrderItemInline]
    search_fields = ('email','first_name','last_name')
