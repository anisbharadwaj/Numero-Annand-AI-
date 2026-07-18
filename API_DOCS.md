# Numero Annand AI - API Documentation

## Authentication Endpoints

### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "User Name",
  "mobile": "+91 XXXXXXXXXX",
  "language": "en"  // en, hi, as
}

Response: 201 Created
{
  "success": true,
  "user": {...},
  "token": "jwt_token_here"
}
```

### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response: 200 OK
{
  "success": true,
  "user": {...},
  "token": "jwt_token_here"
}
```

### Get Current User
```
GET /api/auth/me
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "user": {...}
}
```

## Payment Endpoints

### Create Order
```
POST /api/orders/create
Authorization: Bearer <token>
Content-Type: application/json

{
  "report_type": "digital"  // digital or printed
}

Response: 201 Created
{
  "success": true,
  "order": {...},
  "payment": {
    "qr_image": "data:image/png;base64,...",
    "upi_id": "7099805039-2@axl",
    "payee_name": "Ananda Sarmah",
    "amount": 201,
    "currency": "INR",
    "reference": "NUM123ABC456"
  }
}
```

### Get Order Details
```
GET /api/orders/<order_id>
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "order": {...}
}
```

### Verify Payment (Submit UTR)
```
POST /api/orders/verify
Authorization: Bearer <token>
Content-Type: application/json

{
  "order_id": 1,
  "utr": "123456789012"
}

Response: 200 OK
{
  "success": true,
  "message": "UTR recorded, awaiting admin verification"
}
```

## Admin Endpoints

### Admin Login
```
POST /api/admin/login
Content-Type: application/json

{
  "email": "admin@numeroannand.com",
  "password": "admin_password"
}
```

### Verify Payment (Admin)
```
POST /api/admin/verify-payment
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "order_id": 1,
  "verified": true
}
```

### Get Dashboard Analytics
```
GET /api/admin/analytics
Authorization: Bearer <admin_token>

Returns revenue, order stats, customer stats, etc.
```

## Pricing

- Digital Report: ₹201
- Printed Report: ₹501
- Premium Membership (1 month): ₹500
- Premium Membership (3 months): ₹1200
- Premium Membership (6 months): ₹2200
- Premium Membership (12 months): ₹4000

## UPI Payment Details

- UPI ID: 7099805039-2@axl
- Payee Name: Ananda Sarmah
- Supported Apps: PhonePe, Google Pay, Paytm, BHIM, Amazon Pay, All Banking Apps

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

Tokens expire after 30 days by default.

## Error Responses

```json
{
  "error": "Error message here",
  "status": 400
}
```

Common status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 500: Server Error
