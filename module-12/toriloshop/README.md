# 🛍️ Torilo Shop — Module 12 (Authentication + Admin & UI Enhancements)

## Project Description

This repository contains Torilo Shop, a Django e-commerce demo. Module 12 expands the project with full authentication and user-flow improvements. Authentication features added:

- Login page (`/accounts/login/`) using Django's `LoginView` with a custom `login.html` template.
- Logout at `/accounts/logout/` with a confirmation prompt and redirect to the home page.
- Registration page (`/accounts/register/`) with a custom registration form capturing name, username, email and password; users are logged in after registering.
- Protected product management routes: `add`, `edit`, and `delete` require login; `delete` is restricted to staff users only.
- Navbar updates showing `Login` / `Register` when logged out and username + `Logout` when logged in.

These changes make the product admin flows more secure and provide a better UX for site managers and customers.

## Features Implemented (Module 12)

- Authentication
  - Login (`/accounts/login/`) using `LoginView` and `templates/accounts/login.html`.
  - Logout (`/accounts/logout/`) via `LogoutView`; client-side confirmation prompt added.
  - Registration (`/accounts/register/`) using a custom `RegisterForm` that stores name and email.
- Protected routes
  - `product_add`, `product_edit`, `product_delete` are protected with `@login_required`.
  - Only staff users (`request.user.is_staff`) can delete products; others are redirected and shown an error message.
- Navbar / UI
  - Navbar shows `Login` and `Register` when not authenticated; shows `Hello, <username>` and a `Logout` link when authenticated.
  - Login and registration pages restyled with `.auth-card` for consistent spacing and field alignment.

## Setup Instructions (run locally)

### 1. Create virtual environment and activate
```bash
# from project root (Assignment/module-12/module-12/toriloshop)
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies (includes Pillow for image support)
```bash
pip install django Pillow
```

### 3. Create and apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 5. (Optional) Collect static files
```bash
python manage.py collectstatic
```

### 6. Run development server
```bash
python manage.py runserver
```

Open the site at: http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin/

## Screenshots

### 1) Login page
![Login page](Assignment/module-12/module-12/toriloshop/screenshots/01_login_page.png)

### 2) Registration page
![Registration page](Assignment/module-12/module-12/toriloshop/screenshots/02_registration_page.png)

### 3) Protected route redirects unauthenticated users (example)
![Protected route redirect](Assignment/module-12/module-12/toriloshop/screenshots/03_protected_route_redirect.png)

### 4) Logged-in navbar (shows username + Logout)
![Logged-in navbar](Assignment/module-12/module-12/toriloshop/screenshots/04_logged_in_navbar.png)

### 5) Logged-out navbar (shows Login / Register)
![Logged-out navbar](Assignment/module-12/module-12/toriloshop/screenshots/05_logged_out_navbar.png)

## Full Project Structure

```
Assignment/
├── module-12/
│   └── module-12/
│       └── toriloshop/
│           ├── manage.py
│           ├── db.sqlite3
│           ├── README.md
│           ├── requirements.txt (optional)
│           ├── media/                        
│           ├── static/                       
│           │   └── css/main.css
│           ├── staticfiles/                   
│           ├── templates/
│           │   ├── accounts/
│           │   │   ├── login.html
│           │   │   └── register.html
│           │   └── products/
│           │       ├── base.html
│           │       ├── product_list.html
│           │       ├── product_detail.html
│           │       └── ...
│           ├── toriloshop/                   
│           │   ├── settings.py
│           │   ├── urls.py
│           │   └── wsgi.py
│           └── products/                      
│               ├── admin.py
│               ├── apps.py
│               ├── forms.py
│               ├── models.py
│               ├── views.py
│               ├── urls.py
│               └── templates/products/
└── ...
```

## Key Files

- `accounts/forms.py` — `RegisterForm` for new user registrations.
- `accounts/views.py` & `accounts/urls.py` — login/logout/register endpoints.
- `products/views.py` — product CRUD views now protected with `@login_required` and staff-only deletes.
- `products/admin.py` — admin customisations (image thumbnail, list_display, bulk action).
- `static/css/main.css` — custom UI & auth form styles.

## Notes

- The login/logout flow uses Django auth. Logout uses a client-side confirmation prompt; the server `LogoutView` handles session termination and redirects to home.
- Ensure `MEDIA_URL`/`MEDIA_ROOT` are configured (they are in `toriloshop/settings.py`) and Pillow is installed for handling `ImageField`.
- For production, configure secure settings, a proper static/media server, and HTTPS.

**This is Module 12 — authentication and admin improvements.**
