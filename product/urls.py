
from django.urls import path
from .views import ProductListView,ProductListAllView, NewArrivalsView, RecommendedView, \
TrendingView, ProductDetailView , ProductsByCategoryView, CategoryListView ,\
CategoryDetailView, ReviewListView, ReviewCreateView, ContactAPIView, ProductSearchView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/all/', ProductListAllView.as_view(), name='product-list-all'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/new-arrivals/', NewArrivalsView.as_view(), name='new-arrivals'),
    path('products/recommended/', RecommendedView.as_view(), name='recommended'),
    path('products/trending/', TrendingView.as_view(), name='trending'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/<int:category_id>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    
    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('products/<int:product_id>/reviews/add/', ReviewCreateView.as_view(), name='review-create'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),

    path('contact/', ContactAPIView.as_view(), name='contact'),
]