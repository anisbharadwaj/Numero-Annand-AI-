# Numero Annand AI - Premium Numerology Platform

## Project Overview

Numero Annand AI is a comprehensive, enterprise-grade premium numerology platform built with Python Flask and SQLAlchemy. It provides a complete SaaS solution for numerology analysis, premium reports, membership management, and AI-assisted customer support.

**Founder:** Annand Sarma  
**Location:** Assam, India  
**Contact:** +91 7099805039  
**Platform:** Production-Ready Flask Backend

---

## Key Features

### 1. Database & Authentication
- SQLite/PostgreSQL with SQLAlchemy ORM
- JWT-based authentication with role-based access control
- Secure password hashing with bcrypt
- User roles: Guest, Basic, Premium, Admin

### 2. Premium Membership System
- Multiple membership plans (1, 3, 6, 12 months)
- Automatic expiry management
- Premium benefits tracking
- Revenue analytics

### 3. Advanced Payment System
- Dynamic QR code generation for UPI payments
- Support for all UPI apps (PhonePe, Google Pay, Paytm, BHIM, Amazon Pay)
- UTR verification system
- Admin payment verification dashboard
- Order tracking and status management

### 4. Annand AI Assistant
- Floating sidebar with glassmorphism design
- Multi-language support (English, Hindi, Assamese)
- Message limits (Guest: 1, Basic: 1/day, Premium: Unlimited)
- Session memory and chat history
- Smart response engine based on knowledge base

### 5. Customer Dashboard
- Profile management
- Order history and tracking
- Report downloads
- Payment history
- Consultation booking
- Preferences management

### 6. Admin Dashboard
- Revenue analytics and charts
- Payment verification system
- User management
- Report management
- Contact message handling
- Activity logging
- CSV export capabilities

### 7. Premium Report Generation
- Comprehensive numerology analysis
- Birth number calculation
- Destiny number analysis
- Name number vibration
- Lo Shu Grid analysis
- Missing numbers identification
- Repeated numbers analysis
- PDF watermarking with digital signature
- QR code verification

### 8. Multi-Language Support
- English, Hindi, Assamese
- Instant language switching
- Language preference persistence
- All UI translations included

### 9. Community Features
- WhatsApp support integration
- WhatsApp community group
- Daily numerology tips
- Public testimonials
- FAQ system
- Blog articles
- Contact form system
- Newsletter subscription ready

---

## Project Structure

```
/vercel/share/v0-project/
├── app.py                    # Main Flask application with all API routes
├── models.py                 # Database models (SQLAlchemy)
├── auth.py                   # Authentication system
├── payment.py                # Payment and QR code system
├── membership.py             # Premium membership management
├── customer_dashboard.py      # Customer dashboard utilities
├── admin_utils.py            # Admin utilities and analytics
├── ai_assistant.py           # Annand AI assistant engine
├── report_generator.py        # Premium report generation
├── community.py              # Community and social features
├── init_db.py                # Database initialization script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── vercel.json               # Vercel deployment config
├── API_DOCS.md               # Complete API documentation
└── README.md                 # This file
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip or poetry
- SQLite3 (included with Python)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd /vercel/share/v0-project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 4: Initialize Database
```bash
python init_db.py
```

This creates:
- All database tables
- Default admin user (admin@numeroannand.com / ChangeMe@2024)
- Default settings

### Step 5: Run Application
```bash
python app.py
```

Server will start at `http://localhost:5000`

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Membership
- `GET /api/membership/plans` - Get all membership plans
- `GET /api/membership/status` - Check membership status
- `POST /api/membership/subscribe` - Subscribe to plan
- `POST /api/membership/verify` - Verify payment

### Orders & Payments
- `POST /api/orders/create` - Create new order
- `GET /api/orders/<id>` - Get order details
- `POST /api/orders/verify` - Verify payment

### Customer Dashboard
- `GET /api/dashboard/overview` - Dashboard overview
- `GET /api/dashboard/orders` - User orders
- `GET /api/dashboard/reports` - User reports
- `GET /api/dashboard/consultations` - User consultations
- `POST /api/dashboard/consultations/book` - Book consultation
- `PUT /api/dashboard/profile` - Update profile

### Reports
- `POST /api/reports/generate` - Generate premium report
- `GET /api/reports/<id>` - Get report details
- `POST /api/numerology/analyze` - Quick analysis

### Admin
- `POST /api/admin/login` - Admin login
- `GET /api/admin/analytics` - Dashboard analytics
- `GET /api/admin/pending-payments` - Pending payments
- `POST /api/admin/verify-payment/<id>` - Verify payment
- `GET /api/admin/users` - List all users

### AI Assistant
- `GET /api/ai/greeting` - Get greeting
- `POST /api/ai/message` - Send message
- `GET /api/ai/history` - Chat history
- `GET /api/ai/limits` - Message limits

### Community
- `GET /api/community/links` - Community links
- `GET /api/community/testimonials` - Testimonials
- `GET /api/community/daily-tip` - Daily tip
- `GET /api/community/faq` - FAQ
- `POST /api/community/contact` - Contact form
- `GET /api/community/blog` - Blog articles

See [API_DOCS.md](./API_DOCS.md) for complete API documentation.

---

## Database Schema

### Core Tables
- **users** - User accounts with roles and membership
- **orders** - Order tracking and status
- **payments** - Payment records with QR codes
- **reports** - Generated numerology reports
- **downloads** - Download history
- **ai_chats** - AI assistant conversations
- **consultations** - Consultation bookings
- **admins** - Admin accounts
- **activity_logs** - System activity logging

---

## Configuration

### Environment Variables
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///numero_annand.db
JWT_SECRET=your-jwt-secret
UPI_ID=7099805039-2@axl
PAYEE_NAME=Ananda Sarmah
```

### Pricing Configuration
```python
PRICING = {
    'digital_report': 201,      # ₹201
    'printed_report': 501,      # ₹501
    'premium_membership_1month': 500,
    'premium_membership_3month': 1200,
    'premium_membership_6month': 2200,
    'premium_membership_12month': 4000
}
```

---

## Deployment

### Local Deployment
```bash
python app.py
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Vercel Deployment
Already configured in `vercel.json`. Deploy with:
```bash
vercel deploy
```

### Railway/Render Deployment
Use PostgreSQL and update DATABASE_URL:
```
DATABASE_URL=postgresql://user:password@host/numero_annand
```

---

## Security Features

- JWT token-based authentication
- CSRF protection ready
- XSS protection via jsonify
- SQL injection prevention with ORM
- Rate limiting support
- Secure password hashing (bcrypt)
- Role-based access control
- Admin-only endpoints protected
- User data isolation

---

## Performance Optimization

- Database indexing on frequently queried fields
- Lazy loading for relationships
- Pagination support (20-50 items per page)
- Query optimization with SQLAlchemy
- Efficient JSON serialization
- Caching-ready architecture

---

## Development Workflow

### Adding New Features
1. Add database models in `models.py`
2. Create utility functions in appropriate module
3. Add API routes in `app.py`
4. Update API documentation in `API_DOCS.md`
5. Test with sample requests

### Database Migrations
For changes to models:
1. Update model in `models.py`
2. Run `python init_db.py` (development only)
3. For production, use proper migration tools

---

## Testing

Sample API requests:

```bash
# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123","name":"User"}'

# Create order
curl -X POST http://localhost:5000/api/orders/create \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"report_type":"digital"}'

# Get AI greeting
curl http://localhost:5000/api/ai/greeting?language=en
```

---

## Troubleshooting

### Database Issues
```bash
# Reset database
rm numero_annand.db
python init_db.py
```

### Port Already in Use
```bash
# Use different port
python app.py --port 8000
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Future Enhancements

- Email notification system
- SMS payment reminders
- Advanced analytics dashboard
- Machine learning predictions
- Video consultation support
- Mobile app integration
- Blockchain verification
- Multi-currency support

---

## Support & Contact

- **Founder:** Annand Sarma
- **Mobile:** +91 7099805039
- **WhatsApp:** https://wa.me/917099805039
- **Community:** https://chat.whatsapp.com/G23u7Yf3PuIC6Gw7GCJIMJ
- **Email:** support@numeroannand.com

---

## License & Terms

All rights reserved. Numero Annand AI is a proprietary platform by Annand Sarma.

For more information, visit the official platform or contact support.

---

## Changelog

### v1.0.0 (Current)
- Complete enterprise platform launch
- All 7 major features implemented
- Multi-language support (3 languages)
- Production-ready deployment

---

## Contributing

This is a proprietary project. For contributions or feature requests, contact the founder directly.

---

**Last Updated:** July 2024  
**Status:** Production Ready  
**Maintenance:** Active Development
