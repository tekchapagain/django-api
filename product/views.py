from rest_framework import generics, permissions
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import status
from django.db.models import Q
from .models import Product, Category, Review
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer, CategorySerializer,\
ReviewSerializer, ProductDetailSerializer, ContactSerializer
from django.views.decorators.cache import cache_page

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 5 # Set your default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'current_page': self.page.number,
            'first_page_url': self.get_first_page_link(),
            'from': self.page.start_index(),
            'last_page': self.page.paginator.num_pages,
            'last_page_url': self.get_last_page_link(),
            'links': self.get_pagination_links(),
            'next_page_url': self.get_next_link(),
            'path': self.request.build_absolute_uri(self.request.path),
            'per_page': self.get_page_size(self.request),
            'prev_page_url': self.get_previous_link(),
            'to': self.page.end_index(),
            'total': self.page.paginator.count
        })

    def get_pagination_links(self):
        links = []
        
        # Previous page link
        if self.page.has_previous():
            previous_url = self.get_previous_link()
            links.append({'url': previous_url, 'label': '&laquo; Previous', 'active': False})
        else:
            links.append({'url': None, 'label': '&laquo; Previous', 'active': False})
    
        # Add page number links
        for page_num in range(1, self.page.paginator.num_pages + 1):
            # Always append the `?page=` parameter, even for page 1
            url = self.request.build_absolute_uri(self.request.path) + f'?page={page_num}'
            links.append({'url': url, 'label': str(page_num), 'active': page_num == self.page.number})
    
        # Next page link
        if self.page.has_next():
            next_url = self.get_next_link()
            links.append({'url': next_url, 'label': 'Next &raquo;', 'active': False})
        else:
            links.append({'url': None, 'label': 'Next &raquo;', 'active': False})
    
        return links

    def get_first_page_link(self):
        return self.request.build_absolute_uri(self.request.path) + '?page=1'

    def get_last_page_link(self):
        return self.request.build_absolute_uri(self.request.path) + f'?page={self.page.paginator.num_pages}'

@method_decorator(cache_page(900), name='dispatch')
class ProductListAllView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None  # Disable pagination for this view

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get query params
        colors = self.request.query_params.getlist('color[]', [])
        categories = self.request.query_params.getlist('category[]', [])
        price = self.request.query_params.get('price')

        # Apply color filtering
        if colors:
            queryset = queryset.filter(color__in=colors)

        # Apply category filtering
        if categories:
            queryset = queryset.filter(category__id__in=categories)

        # Apply price filtering (assuming less than or equal to)
        if price:
            try:
                price = float(price)
                queryset = queryset.filter(price__lte=price)
            except ValueError:
                pass  # If price is not a valid number, you can log or handle it

        return queryset

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Fallback if pagination isn't applied
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Handle product creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(cache_page(900), name='dispatch')
class NewArrivalsView(generics.ListAPIView):
    queryset = Product.objects.order_by('-id')[:10]  # Adjust as needed
    serializer_class = ProductSerializer

@method_decorator(cache_page(900), name='dispatch')
class RecommendedView(generics.ListAPIView):
    # You can implement your logic for recommended products here
    queryset = Product.objects.filter(is_recommended=True)  # Adjust your condition
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        # Call the default list method to get the serialized data
        response = super().list(request, *args, **kwargs)
        
        # Nest the data under 'data' key
        return Response({'data': response.data})
    
@method_decorator(cache_page(900), name='dispatch')
class TrendingView(generics.ListAPIView):
    # Implement your logic for trending products
    queryset = Product.objects.filter(is_trending=True)  # Adjust your condition
    serializer_class = ProductSerializer
    
    def list(self, request, *args, **kwargs):
        # Call the default list method to get the serialized data
        response = super().list(request, *args, **kwargs)
        
        # Nest the data under 'data' key
        return Response({'data': response.data})

class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        # The serializer will automatically include reviews in the response
        return super().get(request, *args, **kwargs)
    
class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

class ProductsByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')  # Get category_id from the URL
        return Product.objects.filter(category__id=category_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response structure
        return Response({'data': serializer.data})
    
@method_decorator(cache_page(3600), name='dispatch')
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        # Call the default list method to get the serialized data
        response = super().list(request, *args, **kwargs)
        
        # Nest the data under 'data' key
        return Response({'data': response.data})

# Retrieve a category by ID
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id)
        serializer.save(user=self.request.user, product=product)
        if product:
            product.update_review_count() 

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product__id=product_id)
    


class ContactAPIView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Contact form submitted successfully!'}, status=status.HTTP_201_CREATED)