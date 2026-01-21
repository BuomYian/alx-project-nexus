# E-Commerce Backend - API Specification

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints (except registration and login) require JWT authentication via the `Authorization` header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register/`

Request:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

### Login User
**POST** `/auth/login/`

Request:
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

Response (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Refresh Token
**POST** `/auth/refresh/`

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Response (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Product Endpoints

### List Products
**GET** `/products/`

Query Parameters:
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20)
- `category` (int): Filter by category ID
- `min_price` (decimal): Minimum price filter
- `max_price` (decimal): Maximum price filter
- `search` (string): Search by name or description
- `ordering` (string): Sort field (e.g., `price`, `-created_at`)

Example:
```
GET /products/?category=5&min_price=100&max_price=500&ordering=-price&page=1
```

Response (200 OK):
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Wireless Headphones",
      "slug": "wireless-headphones",
      "short_description": "High-quality wireless headphones",
      "price": "199.99",
      "discount_price": "149.99",
      "current_price": "149.99",
      "discount_percentage": 25,
      "image": "http://example.com/products/headphones.jpg",
      "category": {
        "id": 5,
        "name": "Electronics",
        "slug": "electronics"
      },
      "average_rating": 4.5,
      "review_count": 150,
      "quantity_in_stock": 45,
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### Get Product Details
**GET** `/products/{id}/`

Example:
```
GET /products/1/
```

Response (200 OK):
```json
{
  "id": 1,
  "name": "Wireless Headphones",
  "slug": "wireless-headphones",
  "description": "Premium wireless headphones with noise cancellation...",
  "short_description": "High-quality wireless headphones",
  "price": "199.99",
  "discount_price": "149.99",
  "current_price": "149.99",
  "discount_percentage": 25,
  "sku": "HEADPHONE-001",
  "category": {
    "id": 5,
    "name": "Electronics",
    "slug": "electronics"
  },
  "quantity_in_stock": 45,
  "image": "http://example.com/products/headphones.jpg",
  "average_rating": 4.5,
  "review_count": 150,
  "sales_count": 1200,
  "attributes": [
    {
      "id": 1,
      "attribute_key": "Color",
      "attribute_value": "Black"
    },
    {
      "id": 2,
      "attribute_key": "Warranty",
      "attribute_value": "2 Years"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "user": "john@example.com",
      "rating": 5,
      "title": "Excellent product",
      "comment": "Great quality and amazing sound...",
      "is_verified_purchase": true,
      "created_at": "2024-01-10T08:20:00Z"
    }
  ],
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:45:00Z"
}
```

---

### Create Product (Admin Only)
**POST** `/products/`

Request:
```json
{
  "name": "Wireless Headphones",
  "description": "Premium wireless headphones with noise cancellation",
  "short_description": "High-quality wireless headphones",
  "category": 5,
  "sku": "HEADPHONE-001",
  "price": "199.99",
  "discount_price": "149.99",
  "quantity_in_stock": 45,
  "image": "<file upload>",
  "is_active": true,
  "attributes": [
    {
      "attribute_key": "Color",
      "attribute_value": "Black"
    }
  ]
}
```

Response (201 Created):
```json
{
  "id": 1,
  "name": "Wireless Headphones",
  "slug": "wireless-headphones",
  ...
}
```

---

### Update Product (Admin Only)
**PUT** `/products/{id}/`

Request:
```json
{
  "name": "Premium Wireless Headphones",
  "price": "229.99",
  "discount_price": "169.99",
  "quantity_in_stock": 50
}
```

Response (200 OK):
```json
{
  "id": 1,
  "name": "Premium Wireless Headphones",
  ...
}
```

---

### Delete Product (Admin Only)
**DELETE** `/products/{id}/`

Response (204 No Content)

---

## Category Endpoints

### List Categories
**GET** `/categories/`

Response (200 OK):
```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Electronics",
      "slug": "electronics",
      "description": "Electronic devices and gadgets"
    },
    {
      "id": 2,
      "name": "Clothing",
      "slug": "clothing",
      "description": "Apparel and fashion items"
    }
  ]
}
```

---

### Get Category Details
**GET** `/categories/{id}/`

Response (200 OK):
```json
{
  "id": 1,
  "name": "Electronics",
  "slug": "electronics",
  "description": "Electronic devices and gadgets"
}
```

---

### Create Category (Admin Only)
**POST** `/categories/`

Request:
```json
{
  "name": "Smart Devices",
  "description": "Smart home and IoT devices",
  "parent_category": 1
}
```

Response (201 Created):
```json
{
  "id": 13,
  "name": "Smart Devices",
  "slug": "smart-devices",
  "description": "Smart home and IoT devices"
}
```

---

## Review Endpoints

### List Product Reviews
**GET** `/products/{product_id}/reviews/`

Response (200 OK):
```json
{
  "count": 150,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": "john@example.com",
      "rating": 5,
      "title": "Excellent product",
      "comment": "Great quality and amazing sound...",
      "is_verified_purchase": true,
      "helpful_count": 45,
      "unhelpful_count": 2,
      "created_at": "2024-01-10T08:20:00Z"
    }
  ]
}
```

---

### Create Review
**POST** `/products/{product_id}/reviews/`

Request:
```json
{
  "rating": 5,
  "title": "Excellent product",
  "comment": "Great quality and amazing sound. Highly recommended!",
  "is_verified_purchase": true
}
```

Response (201 Created):
```json
{
  "id": 1,
  "user": "john@example.com",
  "rating": 5,
  "title": "Excellent product",
  "comment": "Great quality and amazing sound...",
  "is_verified_purchase": true,
  "helpful_count": 0,
  "unhelpful_count": 0,
  "created_at": "2024-01-21T10:30:00Z"
}
```

---

### Update Review
**PUT** `/reviews/{id}/`

Request:
```json
{
  "rating": 4,
  "title": "Good product",
  "comment": "Still good but had some minor issues"
}
```

Response (200 OK):
```json
{
  "id": 1,
  "user": "john@example.com",
  "rating": 4,
  ...
}
```

---

### Delete Review
**DELETE** `/reviews/{id}/`

Response (204 No Content)

---

## User Endpoints

### Get User Profile
**GET** `/users/{id}/`

Response (200 OK):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Update User Profile
**PUT** `/users/{id}/`

Request:
```json
{
  "first_name": "Jonathan",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

Response (200 OK):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "first_name": "Jonathan",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid data provided",
  "errors": {
    "price": ["Ensure this value is greater than or equal to 0."]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Status Codes Reference

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting

Current rate limits:
- **Authenticated users**: 1000 requests per hour
- **Anonymous users**: 100 requests per hour

---

## Pagination

Default pagination: 20 items per page

Available page sizes: 10, 20, 50, 100

---

## Sorting

Available sort fields for products:
- `price` (ascending)
- `-price` (descending)
- `created_at` (ascending)
- `-created_at` (descending)
- `sales_count` (ascending)
- `-sales_count` (descending)
- `average_rating` (ascending)
- `-average_rating` (descending)

---

## Filtering

### Product Filtering
- `category` (int): Category ID
- `min_price` (decimal): Minimum price
- `max_price` (decimal): Maximum price
- `is_active` (boolean): Active status

### Search
- `search` (string): Search in name, description, SKU

---

**Last Updated**: January 2026  
**API Version**: 1.0.0
