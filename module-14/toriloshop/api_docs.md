# Torilo Shop REST API Documentation

## Overview

This document describes all REST API endpoints available in Torilo Shop. The API uses JWT (JSON Web Token) authentication for protected endpoints.

**Note**: The web interface at `/products/` now includes the same pagination, filtering, and search capabilities as the API endpoints described below.

---

## Authentication

### Get JWT Token

**Endpoint:** `POST /api/token/`

**Description:** Obtain a JWT access token and refresh token using username and password.

**Request Body:**
```json
{
  "username": "workspace1",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODc2NjUwMiwiaWF0IjoxNzc4NjgwMTAyLCJqdGkiOiJmMDExZjI4MDhmNDQ0MGMzYjA0ZTQ2Y2I2ZTY4YTQ4YyIsInVzZXJfaWQiOiIzIn0.7UFmZKKFNQkxtQ-CcWRv4oD0FSwiLzaFluMRn4SvQxg",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4NjgwNDAyLCJpYXQiOjE3Nzg2ODAxMDMsImp0aSI6IjViOTc1ODU0ZjkzNTQ2ZTFiODAwMjViNjkxMGFlZTg4IiwidXNlcl9pZCI6IjMifQ.KZCDE7NtZ2SlzzBREbiIbqpAmaXGRe7eYcgw0foZt9Q"
}
```

**Usage in Postman:**
1. Send POST request with credentials
2. Copy the `access` token
3. For authenticated requests, add header: `Authorization: Bearer <access_token>`

---

### Refresh JWT Token

**Endpoint:** `POST /api/token/refresh/`

**Description:** Get a new access token using a refresh token.

**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Response (200 OK):**
```json
{
  "access": "new_access_token"
}
```

---

## Products API

### List All Products (Paginated)

**Endpoint:** `GET /api/products/`

**Method:** GET

**Authentication:** Not required (read-only)

**Query Parameters:**
- `page` (int) — page number (default: 1)
- `category` (int) — filter by category ID
- `is_available` (bool) — filter by availability (true/false)
- `search` (string) — search by product name
- `ordering` (string) — order by field (price, created_at, -price, -created_at)

**Example URLs:**
- `GET /api/products/` — all products, page 1
- `GET /api/products/?page=2` — page 2
- `GET /api/products/?category=1` — only category 1
- `GET /api/products/?is_available=true` — only available products
- `GET /api/products/?search=laptop` — search for "laptop"
- `GET /api/products/?ordering=price` — order by price ascending
- `GET /api/products/?ordering=-price` — order by price descending

**Response (200 OK):**
```json
{
  "count": 8,
  "next": "http://127.0.0.1:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Laptop",
      "price": "89999.99",
      "stock": 15,
      "image": "http://127.0.0.1:8000/media/products/laptop.jpg",
      "category": {
        "id": 1,
        "name": "Electronics",
        "slug": "electronics",
        "description": "Electronic devices",
        "product_count": 3
      },
      "is_available": true,
      "created_at": "2026-04-18T18:59:04.408184Z",
      "created_by": {
        "id": 1,
        "username": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com"
      }
    }
  ]
}
```

---

### Create a Product

**Endpoint:** `POST /api/products/`

**Method:** POST

**Authentication:** Required (JWT token)

**Headers:**
- `Authorization: Bearer <access_token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "name": "New Laptop",
  "price": "1299.99",
  "stock": 10,
  "category_id": 1,
  "is_available": true,
  "image": null
}
```

**Response (201 Created):**
```json
{
  "id": 9,
  "name": "New Laptop",
  "price": "1299.99",
  "stock": 10,
  "image": null,
  "category": {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics",
    "description": "Electronic devices",
    "product_count": 4
  },
  "is_available": true,
  "created_at": "2026-05-13T10:30:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "name": ["This field may not be blank."],
  "category_id": ["This field is required."]
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### Retrieve a Single Product

**Endpoint:** `GET /api/products/<id>/`

**Method:** GET

**Authentication:** Not required

**URL Parameters:**
- `id` (int) — product ID (required)

**Example:** `GET /api/products/1/`

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Laptop",
  "price": "89999.99",
  "stock": 15,
  "image": "http://127.0.0.1:8000/media/products/laptop.jpg",
  "category": {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics",
    "description": "Electronic devices",
    "product_count": 3
  },
  "is_available": true,
  "created_at": "2026-04-18T18:59:04.408184Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com"
  }
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### Update a Product

**Endpoint:** `PUT /api/products/<id>/`

**Method:** PUT

**Authentication:** Required (JWT token; only creator or staff can edit)

**Headers:**
- `Authorization: Bearer <access_token>`
- `Content-Type: application/json`

**URL Parameters:**
- `id` (int) — product ID (required)

**Example:** `PUT /api/products/1/`

**Request Body:**
```json
{
  "name": "Updated Laptop",
  "price": "99999.99",
  "stock": 20,
  "category_id": 1,
  "is_available": true
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Laptop",
  "price": "99999.99",
  "stock": 20,
  "image": "http://127.0.0.1:8000/media/products/laptop.jpg",
  "category": {...},
  "is_available": true,
  "created_at": "2026-04-18T18:59:04.408184Z",
  "created_by": {...}
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "You can only edit your own products."
}
```

---

### Delete a Product

**Endpoint:** `DELETE /api/products/<id>/`

**Method:** DELETE

**Authentication:** Required (JWT token; only creator or staff can delete)

**Headers:**
- `Authorization: Bearer <access_token>`

**URL Parameters:**
- `id` (int) — product ID (required)

**Example:** `DELETE /api/products/1/`

**Response (204 No Content):**
- No response body; HTTP status 204 indicates successful deletion.

**Response (403 Forbidden):**
```json
{
  "detail": "You can only delete your own products."
}
```

---

## Categories API

### List All Categories

**Endpoint:** `GET /api/categories/`

**Method:** GET

**Authentication:** Not required

**Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Electronics",
      "slug": "electronics",
      "description": "Electronic devices and gadgets",
      "product_count": 3
    },
    {
      "id": 2,
      "name": "Accessories",
      "slug": "accessories",
      "description": "Mobile and tech accessories",
      "product_count": 2
    },
    {
      "id": 3,
      "name": "Audio",
      "slug": "audio",
      "description": "Audio equipment and headphones",
      "product_count": 2
    }
  ]
}
```

---

## Testing in Postman

### Step 1: Obtain JWT Token

1. **Create a new request:**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/token/`

2. **Headers:**
   - `Content-Type: application/json`

3. **Body (raw JSON):**
   ```json
   {
     "username": "admin",
     "password": "your_password"
   }
   ```

4. **Send** and copy the `access` token.

### Step 2: Create a Product

1. **Create a new request:**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/products/`

2. **Headers:**
   - `Authorization: Bearer <paste_access_token>`
   - `Content-Type: application/json`

3. **Body (raw JSON):**
   ```json
   {
     "name": "Test Product",
     "price": "150.00",
     "stock": 20,
     "category_id": 1,
     "is_available": true
   }
   ```

4. **Send** to create the product.

### Step 3: List Products with Filters

1. **Create a new request:**
   - Method: `GET`
   - URL: `http://127.0.0.1:8000/api/products/?category=1&search=laptop&ordering=price`

2. **Send** to fetch filtered products.

### Step 4: Update a Product

1. **Create a new request:**
   - Method: `PUT`
   - URL: `http://127.0.0.1:8000/api/products/9/` (replace 9 with product ID)

2. **Headers:**
   - `Authorization: Bearer <access_token>`
   - `Content-Type: application/json`

3. **Body (raw JSON):**
   ```json
   {
     "name": "Updated Product",
     "price": "200.00",
     "stock": 15,
     "category_id": 1,
     "is_available": false
   }
   ```

4. **Send** to update.

### Step 5: Delete a Product

1. **Create a new request:**
   - Method: `DELETE`
   - URL: `http://127.0.0.1:8000/api/products/9/` (replace 9 with product ID)

2. **Headers:**
   - `Authorization: Bearer <access_token>`

3. **Send** to delete.

---

## Error Responses

### 400 Bad Request
Returned when request data is invalid.
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
Returned when authentication is required but not provided.
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
Returned when user lacks permission to perform the action.
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
Returned when the requested resource does not exist.
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
Returned when an unexpected server error occurs.
```json
{
  "detail": "Internal server error."
}
```

---

## Pagination

All list endpoints are paginated with 6 items per page.

**Pagination Parameters:**
- `count` (int) — total number of items
- `next` (string) — URL to next page (null if last page)
- `previous` (string) — URL to previous page (null if first page)
- `results` (array) — list of items on current page

**Example:**
```
GET /api/products/?page=2
```

---

## CORS

The API allows requests from all origins via CORS headers.

**Allowed Origins:**
- `http://localhost:3000`
- `http://localhost:8000`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8000`
- All other origins (due to `CORS_ALLOW_ALL_ORIGINS = True`)

---

## Summary Table

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/token/` | No | Obtain JWT token |
| POST | `/api/token/refresh/` | No | Refresh JWT token |
| GET | `/api/products/` | No | List products (paginated) |
| POST | `/api/products/` | Yes | Create product |
| GET | `/api/products/<id>/` | No | Retrieve product |
| PUT | `/api/products/<id>/` | Yes | Update product |
| DELETE | `/api/products/<id>/` | Yes | Delete product |
| GET | `/api/categories/` | No | List categories |

---

## Notes

- JWT tokens expire after a configurable period (default: 5 minutes access, 1 day refresh).
- Use the refresh token to obtain a new access token.
- Only product creators or staff users can edit/delete products.
- Pagination is set to 6 products per page.
- Filtering by `category` and `is_available` is supported.
- Search is available on product `name`.
- Ordering by `price` and `created_at` is supported (use `-` prefix for descending).
