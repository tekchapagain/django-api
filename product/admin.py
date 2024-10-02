from django.contrib import admin
from .models import Review
from .models import Product, ProductImages, Contact, Category

class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 1  # Number of empty forms to display

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price','image', 'discount')
    search_fields = ('name',)
    inlines = [ProductImageInline]

    def image_preview(self, obj):
        if obj.images.exists():
            # Assuming you want to show the first image
            return mark_safe(f'<img src="{obj.images.first().image.url}" width="50" height="50" />')
        return "No image"
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at', 'updated_at', 'product')
    search_fields = ('user__username', 'product__name', 'comment')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject')  # Fields to display in the admin list view
    search_fields = ('name', 'email', 'subject')          # Searchable fields
    list_filter = ('email',)  

admin.site.register(Product,ProductAdmin,)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category,CategoryAdmin)