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
from .models import Product, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

def home(request):
    return render(request, 'products/home.html')

def product_list(request):
    q = request.GET.get('q', '').strip()
    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q)
    context = {'products': products, 'q': q}
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

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

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