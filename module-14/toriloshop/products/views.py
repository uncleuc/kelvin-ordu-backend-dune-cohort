from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.exceptions import FieldDoesNotExist
from django.contrib import messages
from .models import Product, Category
from django.db.models import Count
from .forms import ProductForm, CategoryForm
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category

def home(request):
    return render(request, 'products/home.html')

def product_list(request):
    # Get query parameters
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    availability = request.GET.get('availability', '')
    ordering = request.GET.get('ordering', '-created_at')
    page_number = request.GET.get('page', 1)

    # Base queryset
    products = Product.objects.select_related('category', 'created_by')

    # Apply filters
    if q:
        products = products.filter(name__icontains=q)

    if category_id:
        products = products.filter(category_id=category_id)

    if availability:
        if availability == 'available':
            products = products.filter(is_available=True)
        elif availability == 'unavailable':
            products = products.filter(is_available=False)

    # Apply ordering
    if ordering in ['price', '-price', 'created_at', '-created_at', 'name', '-name']:
        products = products.order_by(ordering)

    # Pagination
    paginator = Paginator(products, 6)  # 6 products per page
    page_obj = paginator.get_page(page_number)

    # Get categories for filter dropdown
    categories = Category.objects.all()

    context = {
        'products': page_obj,
        'q': q,
        'category_id': category_id,
        'availability': availability,
        'ordering': ordering,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    context = {'categories': categories}
    return render(request, 'products/category_list.html', context)

def category_products(request, slug):
    try:
        Category._meta.get_field('slug')
        has_slug = True
    except FieldDoesNotExist:
        has_slug = False

    if has_slug:
        category = get_object_or_404(Category, slug=slug)
    else:
        if slug.isdigit():
            category = get_object_or_404(Category, pk=int(slug))
        else:
            raise Http404("Category lookup failed: no slug field and non-numeric identifier")

    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'products/category_products.html', context)


@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Add'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Edit', 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete products.')
        return redirect('product_detail', pk=product.pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Add'})


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Edit', 'category': category})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})

def about(request):
    return render(request, 'products/about.html')
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Page Not Found</title>
        
    </head>
    <body>
        <div class="container">
            <h1>404</h1>
            <h2>Page Not Found</h2>
            <div class="error-message">
                <p>Sorry! The page you're looking for doesn't exist or has been moved.</p>
            </div>
            <p>The requested URL was not found on this server.</p>
            <p>Let's get you back on track:</p>
            <p>
                <a href="/">← Home</a> | 
                <a href="/products/">Products</a> | 
                <a href="/about/">About Us</a>
            </p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, status=404)

def product_list_json(request):
    products = Product.objects.all()
    data = [{'id': product.id, 'name': product.name, 'price': str(product.price), 'stock': product.stock} 
            for product in products]
    return JsonResponse(data, safe=False)

def product_detail_json(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        data = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'stock': product.stock
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionError("You can only edit your own products.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionError("You can only delete your own products.")
        instance.delete()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)