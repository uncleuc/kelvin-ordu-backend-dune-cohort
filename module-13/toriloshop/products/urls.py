from django.urls import path
from . import views
from .views import ProductListAPIView, ProductDetailAPIView, CategoryListView, CategoryDetailAPIView

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_products, name='category_products'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('about/', views.about, name='about'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api_product_list'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/categories/', views.CategoryListView.as_view(), name='api_category_list'),
    path('api/categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='api_category_detail'),
]
