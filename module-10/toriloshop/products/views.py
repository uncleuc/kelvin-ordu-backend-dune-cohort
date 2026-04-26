from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.exceptions import FieldDoesNotExist
from django.contrib import messages
from .models import Product, Category
from django.db.models import Count
from .forms import ProductForm, CategoryForm

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


def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Add'})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Edit', 'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
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
