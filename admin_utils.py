# =========================================================
# ADMIN UTILITIES
# =========================================================

from datetime import datetime, timedelta
from models import db, User, Order, Payment, Report, OrderStatus, AIChat, ActivityLog, ContactMessage
from payment import admin_verify_payment

# =========================================================
# PAYMENT MANAGEMENT
# =========================================================

def get_pending_payments():
    """Get all pending payments awaiting verification"""
    
    orders = Order.query.filter_by(status=OrderStatus.PENDING.value).all()
    
    pending = []
    for order in orders:
        pending.append({
            'id': order.id,
            'order_id': order.order_id,
            'user_email': order.user.email,
            'user_name': order.user.name,
            'amount': order.amount,
            'report_type': order.report_type,
            'utr': order.payment_utr,
            'created_at': order.created_at.isoformat(),
            'verified': order.verified
        })
    
    return pending

def get_verified_payments():
    """Get all verified/paid payments"""
    
    orders = Order.query.filter_by(status=OrderStatus.PAID.value).all()
    
    verified = []
    for order in orders:
        verified.append({
            'id': order.id,
            'order_id': order.order_id,
            'user_email': order.user.email,
            'amount': order.amount,
            'report_type': order.report_type,
            'created_at': order.created_at.isoformat()
        })
    
    return verified

def verify_payment_admin(order_id, verified=True):
    """Admin verify/reject payment"""
    
    order = Order.query.get(order_id)
    if not order:
        return False, 'Order not found'
    
    success, message = admin_verify_payment(order_id, verified)
    
    # Log activity
    action = 'Payment Verified' if verified else 'Payment Rejected'
    log_activity(None, action, f"Order {order.order_id}: {message}")
    
    return success, message

# =========================================================
# USER MANAGEMENT
# =========================================================

def get_all_users(page=1, limit=50):
    """Get paginated user list"""
    
    pagination = User.query.paginate(page=page, per_page=limit, error_out=False)
    
    users = []
    for user in pagination.items:
        users.append({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'mobile': user.mobile,
            'role': user.role,
            'is_premium': user.is_premium(),
            'premium_until': user.premium_until.isoformat() if user.premium_until else None,
            'created_at': user.created_at.isoformat(),
            'orders_count': len(user.orders)
        })
    
    return {
        'users': users,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }

def search_users(query):
    """Search users by email or name"""
    
    results = User.query.filter(
        (User.email.ilike(f'%{query}%')) | 
        (User.name.ilike(f'%{query}%'))
    ).all()
    
    users = []
    for user in results:
        users.append({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'is_premium': user.is_premium()
        })
    
    return users

def get_user_details(user_id):
    """Get comprehensive user information"""
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'mobile': user.mobile,
        'role': user.role,
        'language': user.language,
        'is_premium': user.is_premium(),
        'premium_until': user.premium_until.isoformat() if user.premium_until else None,
        'created_at': user.created_at.isoformat(),
        'orders': [order.to_dict() for order in user.orders],
        'ai_messages_count': len(user.ai_chats),
        'consultations_count': len(user.consultations),
        'downloads_count': len(user.downloads)
    }

# =========================================================
# ANALYTICS
# =========================================================

def get_dashboard_analytics():
    """Get overall dashboard analytics"""
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    this_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Revenue metrics
    today_revenue = db.session.query(db.func.sum(Order.amount)).filter(
        Order.status == OrderStatus.PAID.value,
        Order.created_at >= today
    ).scalar() or 0
    
    month_revenue = db.session.query(db.func.sum(Order.amount)).filter(
        Order.status == OrderStatus.PAID.value,
        Order.created_at >= this_month
    ).scalar() or 0
    
    total_revenue = db.session.query(db.func.sum(Order.amount)).filter(
        Order.status == OrderStatus.PAID.value
    ).scalar() or 0
    
    # User metrics
    total_users = User.query.count()
    today_users = User.query.filter(User.created_at >= today).count()
    premium_users = User.query.filter(User.premium_until > datetime.utcnow()).count()
    
    # Order metrics
    total_orders = Order.query.count()
    paid_orders = Order.query.filter_by(status=OrderStatus.PAID.value).count()
    pending_orders = Order.query.filter_by(status=OrderStatus.PENDING.value).count()
    
    return {
        'revenue': {
            'today': today_revenue,
            'this_month': month_revenue,
            'total': total_revenue
        },
        'users': {
            'total': total_users,
            'today': today_users,
            'premium': premium_users,
            'basic': total_users - premium_users
        },
        'orders': {
            'total': total_orders,
            'paid': paid_orders,
            'pending': pending_orders,
            'success_rate': round((paid_orders / total_orders * 100) if total_orders > 0 else 0, 2)
        },
        'reports': {
            'digital': Order.query.filter_by(report_type='digital').count(),
            'printed': Order.query.filter_by(report_type='printed').count(),
            'membership': Order.query.filter_by(report_type='membership').count()
        }
    }

def get_revenue_by_date(days=30):
    """Get revenue breakdown by date"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    orders = Order.query.filter(
        Order.status == OrderStatus.PAID.value,
        Order.created_at >= start_date
    ).all()
    
    daily_revenue = {}
    for order in orders:
        date_key = order.created_at.strftime('%Y-%m-%d')
        daily_revenue[date_key] = daily_revenue.get(date_key, 0) + order.amount
    
    return daily_revenue

# =========================================================
# REPORT MANAGEMENT
# =========================================================

def get_all_reports(page=1, limit=50):
    """Get paginated report list"""
    
    pagination = Report.query.paginate(page=page, per_page=limit, error_out=False)
    
    reports = []
    for report in pagination.items:
        reports.append({
            'id': report.id,
            'user_name': report.user_name,
            'order_id': report.order_id,
            'pdf_path': report.pdf_path,
            'created_at': report.created_at.isoformat(),
            'downloads': len(report.downloads)
        })
    
    return {
        'reports': reports,
        'total': pagination.total,
        'pages': pagination.pages
    }

# =========================================================
# ACTIVITY LOGGING
# =========================================================

def log_activity(user_id, action, details=None, ip_address=None):
    """Log admin activity"""
    
    log = ActivityLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address
    )
    
    db.session.add(log)
    db.session.commit()
    
    return log

def get_activity_logs(limit=100):
    """Get recent activity logs"""
    
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    
    activity = []
    for log in logs:
        activity.append({
            'id': log.id,
            'user_id': log.user_id,
            'action': log.action,
            'details': log.details,
            'created_at': log.created_at.isoformat()
        })
    
    return activity

# =========================================================
# CONTACT MESSAGES
# =========================================================

def get_contact_messages(status='new'):
    """Get contact messages by status"""
    
    messages = ContactMessage.query.filter_by(status=status).all()
    
    result = []
    for msg in messages:
        result.append({
            'id': msg.id,
            'name': msg.name,
            'email': msg.email,
            'mobile': msg.mobile,
            'message': msg.message,
            'created_at': msg.created_at.isoformat()
        })
    
    return result

def mark_message_as_replied(message_id):
    """Mark contact message as replied"""
    
    message = ContactMessage.query.get(message_id)
    if not message:
        return False
    
    message.status = 'replied'
    db.session.commit()
    
    return True
