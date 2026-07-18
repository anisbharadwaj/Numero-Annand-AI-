# =========================================================
# CUSTOMER DASHBOARD UTILITIES
# =========================================================

from datetime import datetime, timedelta
from models import db, User, Order, Report, Download, Consultation, AIChat

# =========================================================
# DASHBOARD OVERVIEW
# =========================================================

def get_dashboard_overview(user_id):
    """Get customer dashboard overview"""
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    total_orders = Order.query.filter_by(user_id=user_id).count()
    total_spent = db.session.query(db.func.sum(Order.amount)).filter(
        Order.user_id == user_id,
        Order.status == 'paid'
    ).scalar() or 0
    
    return {
        'name': user.name,
        'email': user.email,
        'mobile': user.mobile,
        'role': user.role,
        'is_premium': user.is_premium(),
        'language': user.language,
        'joined_date': user.created_at.isoformat(),
        'stats': {
            'total_orders': total_orders,
            'total_spent': total_spent,
            'reports_generated': Report.query.filter_by(user_id=user_id).count(),
            'total_downloads': Download.query.filter_by(user_id=user_id).count(),
            'consultations': Consultation.query.filter_by(user_id=user_id).count(),
            'ai_chats': AIChat.query.filter_by(user_id=user_id).count()
        }
    }

# =========================================================
# ORDERS MANAGEMENT
# =========================================================

def get_user_orders(user_id, page=1, limit=10):
    """Get user's orders with pagination"""
    
    pagination = Order.query.filter_by(user_id=user_id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=limit, error_out=False)
    
    orders = []
    for order in pagination.items:
        orders.append({
            'id': order.id,
            'order_id': order.order_id,
            'report_type': order.report_type,
            'amount': order.amount,
            'status': order.status,
            'verified': order.verified,
            'created_at': order.created_at.isoformat(),
            'payment_utr': order.payment_utr,
            'has_report': order.report is not None
        })
    
    return {
        'orders': orders,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }

def get_order_details(order_id, user_id):
    """Get detailed order information"""
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return None
    
    details = {
        'id': order.id,
        'order_id': order.order_id,
        'report_type': order.report_type,
        'amount': order.amount,
        'status': order.status,
        'verified': order.verified,
        'created_at': order.created_at.isoformat(),
        'updated_at': order.updated_at.isoformat(),
        'payment_utr': order.payment_utr,
        'report': order.report.to_dict() if order.report else None
    }
    
    return details

# =========================================================
# REPORTS MANAGEMENT
# =========================================================

def get_user_reports(user_id, page=1, limit=10):
    """Get user's reports with pagination"""
    
    # Join with order to get user_id
    pagination = db.session.query(Report).join(Order).filter(
        Order.user_id == user_id
    ).order_by(Report.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)
    
    reports = []
    for report in pagination.items:
        reports.append({
            'id': report.id,
            'user_name': report.user_name,
            'pdf_path': report.pdf_path,
            'created_at': report.created_at.isoformat(),
            'downloads': len(report.downloads),
            'order_id': report.order_id
        })
    
    return {
        'reports': reports,
        'total': pagination.total,
        'pages': pagination.pages
    }

def get_report_details(report_id, user_id):
    """Get detailed report information"""
    
    report = db.session.query(Report).join(Order).filter(
        Report.id == report_id,
        Order.user_id == user_id
    ).first()
    
    if not report:
        return None
    
    details = {
        'id': report.id,
        'user_name': report.user_name,
        'dob': report.dob,
        'mobile': report.mobile,
        'pdf_path': report.pdf_path,
        'watermarked': report.watermarked,
        'created_at': report.created_at.isoformat(),
        'downloads': len(report.downloads),
        'order_id': report.order_id
    }
    
    return details

# =========================================================
# DOWNLOADS MANAGEMENT
# =========================================================

def get_user_downloads(user_id, page=1, limit=20):
    """Get user's download history"""
    
    pagination = Download.query.filter_by(user_id=user_id).order_by(
        Download.downloaded_at.desc()
    ).paginate(page=page, per_page=limit, error_out=False)
    
    downloads = []
    for download in pagination.items:
        downloads.append({
            'id': download.id,
            'report_id': download.report_id,
            'user_name': download.report.user_name,
            'downloaded_at': download.downloaded_at.isoformat()
        })
    
    return {
        'downloads': downloads,
        'total': pagination.total,
        'pages': pagination.pages
    }

def log_download(user_id, report_id, ip_address=None):
    """Log report download"""
    
    report = Report.query.get(report_id)
    if not report:
        return False
    
    download = Download(
        user_id=user_id,
        report_id=report_id,
        ip_address=ip_address
    )
    
    db.session.add(download)
    db.session.commit()
    
    return True

# =========================================================
# CONSULTATIONS MANAGEMENT
# =========================================================

def get_user_consultations(user_id, page=1, limit=10):
    """Get user's consultations"""
    
    pagination = Consultation.query.filter_by(user_id=user_id).order_by(
        Consultation.scheduled_date.desc()
    ).paginate(page=page, per_page=limit, error_out=False)
    
    consultations = []
    for consultation in pagination.items:
        consultations.append({
            'id': consultation.id,
            'type': consultation.consultation_type,
            'date': consultation.scheduled_date.isoformat(),
            'language': consultation.language,
            'status': consultation.status,
            'notes': consultation.notes,
            'created_at': consultation.created_at.isoformat()
        })
    
    return {
        'consultations': consultations,
        'total': pagination.total,
        'pages': pagination.pages
    }

def book_consultation(user_id, consultation_type, scheduled_date, language='en', notes=''):
    """Book a consultation"""
    
    try:
        consultation = Consultation(
            user_id=user_id,
            consultation_type=consultation_type,
            scheduled_date=datetime.fromisoformat(scheduled_date),
            language=language,
            notes=notes,
            status='scheduled'
        )
        
        db.session.add(consultation)
        db.session.commit()
        
        return consultation, None
    except Exception as e:
        return None, str(e)

def update_consultation(consultation_id, user_id, **kwargs):
    """Update consultation details"""
    
    consultation = Consultation.query.filter_by(
        id=consultation_id,
        user_id=user_id
    ).first()
    
    if not consultation:
        return False, 'Consultation not found'
    
    if 'status' in kwargs:
        consultation.status = kwargs['status']
    if 'notes' in kwargs:
        consultation.notes = kwargs['notes']
    
    db.session.commit()
    
    return True, 'Consultation updated'

# =========================================================
# PAYMENTS MANAGEMENT
# =========================================================

def get_user_payments(user_id, page=1, limit=10):
    """Get user's payment history"""
    
    orders = Order.query.filter_by(user_id=user_id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=limit, error_out=False)
    
    payments = []
    for order in orders.items:
        if order.payment:
            payments.append({
                'id': order.payment.id,
                'order_id': order.order_id,
                'amount': order.payment.amount,
                'currency': order.payment.currency,
                'status': order.status,
                'created_at': order.payment.created_at.isoformat()
            })
    
    return {
        'payments': payments,
        'total': orders.total,
        'pages': orders.pages
    }

# =========================================================
# PROFILE MANAGEMENT
# =========================================================

def update_profile(user_id, **kwargs):
    """Update user profile"""
    
    user = User.query.get(user_id)
    if not user:
        return False, 'User not found'
    
    allowed_fields = ['name', 'mobile', 'language']
    
    for field, value in kwargs.items():
        if field in allowed_fields:
            setattr(user, field, value)
    
    db.session.commit()
    
    return True, 'Profile updated'

def get_user_preferences(user_id):
    """Get user preferences"""
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    return {
        'language': user.language,
        'theme': 'dark',  # Default theme
        'notifications': True
    }

def update_preferences(user_id, preferences):
    """Update user preferences"""
    
    user = User.query.get(user_id)
    if not user:
        return False
    
    if 'language' in preferences:
        user.language = preferences['language']
    
    db.session.commit()
    
    return True

# =========================================================
# NOTIFICATIONS
# =========================================================

def get_user_notifications(user_id, limit=10):
    """Get user notifications"""
    
    notifications = [
        {
            'id': 1,
            'type': 'order',
            'title': 'Order Completed',
            'message': 'Your report is ready for download',
            'created_at': datetime.utcnow().isoformat()
        }
    ]
    
    # In production, these would come from database
    return notifications[:limit]

# =========================================================
# ACTIVITY TRACKING
# =========================================================

def get_recent_activity(user_id, days=7):
    """Get user's recent activity"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    activity = []
    
    # Orders
    orders = Order.query.filter(
        Order.user_id == user_id,
        Order.created_at >= start_date
    ).all()
    
    for order in orders:
        activity.append({
            'type': 'order',
            'description': f'Created order {order.order_id}',
            'timestamp': order.created_at.isoformat()
        })
    
    # Consultations
    consultations = Consultation.query.filter(
        Consultation.user_id == user_id,
        Consultation.created_at >= start_date
    ).all()
    
    for consultation in consultations:
        activity.append({
            'type': 'consultation',
            'description': f'Booked {consultation.consultation_type}',
            'timestamp': consultation.created_at.isoformat()
        })
    
    # Sort by timestamp descending
    activity.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return activity
