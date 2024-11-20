from rest_framework import serializers
from django.db.models import Avg
from .models import Product, Category, Review, ProductImages, Contact

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['product', 'title', 'user', 'rating', 'comment', 'created_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['images']  

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    reviews_count = serializers.SerializerMethodField()  # Added reviews_count

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'description',
            'price',
            'image',
            'stock',
            'discount',
            'is_recommended',
            'is_trending',
            'reviews_count',  # Include reviews_count
            'average_rating'
        ]
        
    def get_reviews_count(self, obj):
        # Returns the count of reviews related to the product
        return obj.reviews.count()
    

class ProductDetailSerializer(serializers.ModelSerializer):
    additionalImages = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image','additionalImages', 'stock', 'discount', 'is_recommended', 'is_trending','reviews_count','average_rating', 'reviews']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']