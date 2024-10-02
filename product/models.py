from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from core.storage_backend import MediaStorage, PublicMediaStorage
from django_ckeditor_5.fields import CKEditor5Field

def product_directory_path(instance, filename):
    return f'products/{instance.pid}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(storage=MediaStorage(),default="category.jpg")

    def __str__(self):
        return self.name

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet='abcdefgh12345')
    name = models.CharField(max_length=255)
    detail = models.TextField(null=True)
    description = CKEditor5Field('Text', config_name='extends', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(storage=PublicMediaStorage(), default="product.jpg")
    stock = models.IntegerField()
    discount = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    is_recommended = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    reviews_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def update_review_count(self):
        self.reviews_count = self.ratings.count()
        self.save()

    @property
    def average_rating(self):
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return average if average is not None else 0.0
    
class ProductImages(models.Model):
	images = models.ImageField(upload_to="product-images", default="product.jpg")
	product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Product Images'
          
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='test')
    rating = models.PositiveIntegerField(default=1)  # Rating from 1 to 5 or any scale you prefer
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')  # Prevents duplicate reviews by the same user on a product

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name