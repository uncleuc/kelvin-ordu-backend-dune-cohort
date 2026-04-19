# 🛍️ Torilo Shop - Django E-Commerce Project

## Project Description

**Torilo Shop** is a beginner-friendly Django e-commerce web application built to demonstrate core Django concepts and data modeling. It includes product and category data structures so users can browse items sorted by category.

The project now includes the following models:
- `Category`: stores product categories with `name` and optional `description`
- `Product`: stores products with `name`, `price`, `stock`, `category`, and `created_at`

The project showcases:
- Django project structure and app architecture
- URL routing and view functions
- Database modeling with Django ORM
- Filtering and querying products by category and price
- Admin data management and custom 404 page handling

## Features Implemented

### Models Created
1. **Category**
   - `name` (CharField)
   - `description` (TextField, blank=True)
2. **Product**
   - `name` (CharField)
   - `price` (DecimalField)
   - `stock` (IntegerField)
   - `category` (ForeignKey to Category)
   - `created_at` (DateTimeField, auto_now_add=True)

### ORM Operations Performed
- `Product.objects.all()` — View all products
- `Product.objects.filter(category__name='Electronics')` — Filter products by category name
- `cat = Category.objects.get(name='Electronics')`
  `Product.objects.filter(category=cat)` — Filter by a category object
- `Product.objects.filter(price__gt=5000)` — Products with price greater than 5000

### URL Routes
| URL | View | Purpose |
|-----|------|---------|
| `/` | home() | Home page |
| `/products/` | product_list() | Products listing |
| `/about/` | about() | About page |
| (Any invalid URL) | page_not_found() | 404 error page |

### Apps Registered
- `products` - Main commerce app containing views, models, admin, and URLs
- `users` - User management app (placeholder for future development)

## Setup Instructions

### Step 1: Create Virtual Environment
```bash
# Navigate to the project directory
cd Kelvin_Ordu_Module7/toriloshop

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install django
```

### Step 3: Create and Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser for Admin
```bash
python manage.py createsuperuser
```

### Step 5: Run the Development Server
```bash
python manage.py runserver
```

Open the app at: **http://127.0.0.1:8000/**

### Step 6: Access the Admin Panel
Open: **http://127.0.0.1:8000/admin/**

### To Stop the Server
Press `CTRL + C` in the terminal

## Project Structure

```
Kelvin_Ordu_Module7/
├── toriloshop/                  # Project configuration folder
│   ├── settings.py             # Settings with INSTALLED_APPS
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── products/                    # Products app
│   ├── views.py                # All view functions
│   ├── urls.py                 # URL patterns for products app
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
├── users/                       # Users app (empty)
│   └── ...
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database
├── venv/                        # Virtual environment
├── screenshots/                 # Project screenshots
└── README.md                    # This file
```

## Screenshots

### Admin Category List
![Admin Category List](screenshots/01_admin_category_list.png)

### Admin Product List
![Admin Product List](screenshots/02_admin_product_list.png)

### Django Shell - All Products
![All Products](screenshots/03_shell_all_products.png)

### Django Shell - Filter by Category
![Filter by Category](screenshots/04_shell_filter_by_category.png)

### Django Shell - Filter by Price
![Filter by Price](screenshots/05_shell_filter_by_price.png)

### Migration Success
![Migration Success](screenshots/06_migration_success.png)

## Key Files

### settings.py
- Location: `toriloshop/settings.py`
- Registered apps: `'products'` and `'users'`
- DEBUG mode enabled for development

### products/views.py
Contains four view functions:
- `home()` - Returns welcome page with navigation
- `product_list()` - Returns product catalog
- `about()` - Returns company information
- `page_not_found()` - Custom 404 error handler

### products/urls.py
Maps URLs to views:
```python
path('', views.home, name='home')
path('products/', views.product_list, name='product_list')
path('about/', views.about, name='about')
```

### toriloshop/urls.py
Root URL configuration that includes products app URLs and sets up custom 404 handler

## Technologies Used

- **Python 3.x**
- **Django 6.0.4**
- **SQLite** (default database)

## Learning Topics Covered

✅ Django project structure  
✅ Creating Django apps  
✅ Function-based views  
✅ URL routing with `path()`  
✅ Returning HTTP responses with HTML  
✅ Navigating between pages  
✅ Custom error handling (404)  
✅ Using INSTALLED_APPS configuration  

## Notes

- This is a development server and should NOT be used in production
- The application uses inline HTML in views for simplicity
- No database models are currently used
- No static files (CSS, JS) are configured yet

## Future Enhancements

- Add templates directory for proper HTML organization
- Implement database models for products and users
- Add CSS styling with static files
- Implement user authentication
- Add shopping cart functionality
- Integrate payment processing

## Author

Created as an educational Django learning project for Module 7

---

**Happy Learning!!! 🚀**
