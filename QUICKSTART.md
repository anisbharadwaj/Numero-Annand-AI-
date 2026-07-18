# Numero Annand AI - Quick Start Guide

## 30 Second Setup

### 1. Install & Initialize
```bash
pip install -r requirements.txt
python init_db.py
```

### 2. Start Server
```bash
python app.py
```

Server running at: `http://localhost:5000`

---

## Default Credentials

**Admin Account:**
- Email: `admin@numeroannand.com`
- Password: `ChangeMe@2024`

**IMPORTANT:** Change password immediately on first login!

---

## Test the Platform

### 1. Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Password123",
    "name": "Test User"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Password123"
  }'
```

Save the returned `token` for next requests.

### 3. Create Order
```bash
curl -X POST http://localhost:5000/api/orders/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"report_type": "digital"}'
```

You'll get a QR code for UPI payment.

### 4. Test AI Assistant
```bash
curl -X POST http://localhost:5000/api/ai/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is numerology?",
    "language": "en"
  }'
```

### 5. Check Membership Plans
```bash
curl http://localhost:5000/api/membership/plans
```

---

## Platform Features Overview

| Feature | Endpoint | Authentication |
|---------|----------|-----------------|
| User Auth | `/api/auth/*` | Optional |
| Membership | `/api/membership/*` | User |
| Orders & Payments | `/api/orders/*` | User |
| Dashboard | `/api/dashboard/*` | User |
| Reports | `/api/reports/*` | User |
| AI Assistant | `/api/ai/*` | Optional |
| Admin | `/api/admin/*` | Admin |
| Community | `/api/community/*` | Optional |

---

## File Organization

```
Core Files:
├── app.py              - Main application with all routes
├── models.py           - Database models
├── auth.py             - Authentication system
├── payment.py          - Payment/QR system

Feature Modules:
├── membership.py       - Premium membership
├── customer_dashboard.py - User dashboard
├── admin_utils.py      - Admin functions
├── ai_assistant.py     - AI engine
├── report_generator.py - Report system
└── community.py        - Community features
```

---

## Next Steps

1. **Update Admin Password**
   ```bash
   # Use admin login endpoint with new credentials
   ```

2. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Update UPI_ID, PAYEE_NAME, etc.

3. **Test Payment Flow**
   - Create order
   - Generate QR code
   - Verify with UTR

4. **Customize Content**
   - Update community links
   - Add testimonials
   - Customize FAQ

5. **Deploy**
   - Vercel: `vercel deploy`
   - Railway: Connect PostgreSQL
   - Render: Update DATABASE_URL

---

## Common Issues

**Port 5000 already in use:**
```bash
python app.py --port 8000
```

**Database error:**
```bash
rm numero_annand.db
python init_db.py
```

**Import errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

---

## API Response Format

All responses follow this format:

**Success (200-201):**
```json
{
  "success": true,
  "data": {},
  "message": "Optional message"
}
```

**Error (400-500):**
```json
{
  "error": "Error message",
  "status": 400
}
```

---

## Pricing Quick Reference

- Digital Report: ₹201
- Printed Report: ₹501
- 1-Month Premium: ₹500
- 3-Month Premium: ₹1200
- 6-Month Premium: ₹2200
- 12-Month Premium: ₹4000

---

## Contact & Support

- **Mobile:** +91 7099805039
- **WhatsApp:** https://wa.me/917099805039
- **Community:** https://chat.whatsapp.com/G23u7Yf3PuIC6Gw7GCJIMJ

---

**Happy Numerology! ✨**
