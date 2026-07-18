# =========================================================
# PREMIUM MEMBERSHIP SYSTEM
# =========================================================

from datetime import datetime, timedelta
from models import db, User, Order, Payment, OrderStatus
from payment import PRICING, UPI_ID, PAYEE_NAME, CURRENCY
import json

# =========================================================
# MEMBERSHIP PLANS
# =========================================================

MEMBERSHIP_PLANS = {
    '1month': {
        'duration': 1,
        'price': 500,
        'duration_days': 30,
        'benefits': [
            'Unlimited AI Assistant Messages',
            '1 Free Report per Month',
            'Priority Support',
            'Exclusive Numerology Tips',
            'Access to Premium Blog'
        ]
    },
    '3months': {
        'duration': 3,
        'price': 1200,
        'duration_days': 90,
        'benefits': [
            'Unlimited AI Assistant Messages',
            '3 Free Reports',
            'Priority Support',
            'Exclusive Numerology Tips',
            'Access to Premium Blog',
            'Monthly Consultation Session'
        ]
    },
    '6months': {
        'duration': 6,
        'price': 2200,
        'duration_days': 180,
        'benefits': [
            'Unlimited AI Assistant Messages',
            '6 Free Reports',
            'Priority Support',
            'Exclusive Numerology Tips',
            'Access to Premium Blog',
            'Monthly Consultation Session',
            'PDF Report Generation',
            'Download History'
        ]
    },
    '12months': {
        'duration': 12,
        'price': 4000,
        'duration_days': 365,
        'benefits': [
            'Unlimited AI Assistant Messages',
            'Unlimited Reports',
            '24/7 Priority Support',
            'Exclusive Numerology Tips',
            'Access to Premium Blog',
            'Monthly Consultation Sessions',
            'PDF Report Generation',
            'Download History',
            'Early Access to New Features',
            'Personal Numerology Coach'
        ]
    }
}

# =========================================================
# MEMBERSHIP MANAGEMENT
# =========================================================

def create_membership_order(user_id, plan_duration):
    """Create premium membership order"""
    
    if plan_duration not in MEMBERSHIP_PLANS:
        return None, 'Invalid membership plan'
    
    plan = MEMBERSHIP_PLANS[plan_duration]
    amount = plan['price']
    
    order = Order(
        order_id=f"MEM{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{plan_duration[-1:]}",
        user_id=user_id,
        report_type='membership',
        amount=amount,
        status=OrderStatus.PENDING.value
    )
    
    db.session.add(order)
    db.session.commit()
    
    return order, None

def activate_membership(user_id, plan_duration):
    """Activate premium membership for user"""
    
    user = User.query.get(user_id)
    if not user:
        return False, 'User not found'
    
    if plan_duration not in MEMBERSHIP_PLANS:
        return False, 'Invalid membership plan'
    
    plan = MEMBERSHIP_PLANS[plan_duration]
    user.upgrade_premium(months=plan['duration'])
    user.role = 'premium'
    
    db.session.commit()
    
    return True, f'Premium membership activated for {plan["duration"]} month(s)'

def get_membership_status(user_id):
    """Get user membership status"""
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    status = {
        'is_premium': user.is_premium(),
        'role': user.role,
        'premium_until': user.premium_until.isoformat() if user.premium_until else None,
        'days_remaining': None,
        'plan': None
    }
    
    if user.is_premium() and user.premium_until:
        days_remaining = (user.premium_until - datetime.utcnow()).days
        status['days_remaining'] = max(0, days_remaining)
        
        # Determine current plan
        if days_remaining > 300:
            status['plan'] = '12months'
        elif days_remaining > 150:
            status['plan'] = '6months'
        elif days_remaining > 60:
            status['plan'] = '3months'
        else:
            status['plan'] = '1month'
    
    return status

def get_membership_details(plan_duration):
    """Get membership plan details"""
    
    if plan_duration not in MEMBERSHIP_PLANS:
        return None
    
    plan = MEMBERSHIP_PLANS[plan_duration].copy()
    plan['duration_name'] = f"{plan['duration']} {'Month' if plan['duration'] == 1 else 'Months'}"
    
    return plan

def renew_membership(user_id, plan_duration):
    """Renew user membership"""
    
    user = User.query.get(user_id)
    if not user:
        return False, 'User not found'
    
    if plan_duration not in MEMBERSHIP_PLANS:
        return False, 'Invalid membership plan'
    
    plan = MEMBERSHIP_PLANS[plan_duration]
    
    # If already premium, add to existing expiry
    if user.is_premium():
        user.premium_until = user.premium_until + timedelta(days=plan['duration_days'])
    else:
        user.premium_until = datetime.utcnow() + timedelta(days=plan['duration_days'])
    
    db.session.commit()
    
    return True, 'Membership renewed successfully'

def cancel_membership(user_id):
    """Cancel user premium membership"""
    
    user = User.query.get(user_id)
    if not user:
        return False, 'User not found'
    
    user.premium_until = None
    user.role = 'basic'
    
    db.session.commit()
    
    return True, 'Premium membership cancelled'

def get_all_plans():
    """Get all membership plans with details"""
    
    plans = []
    for plan_id, plan_data in MEMBERSHIP_PLANS.items():
        plan = plan_data.copy()
        plan['id'] = plan_id
        plan['price_formatted'] = f"₹{plan['price']}"
        plan['price_per_day'] = round(plan['price'] / plan['duration_days'], 2)
        plans.append(plan)
    
    return plans

# =========================================================
# MEMBERSHIP VERIFICATION
# =========================================================

def is_membership_valid(user_id):
    """Check if user has valid premium membership"""
    
    user = User.query.get(user_id)
    if not user:
        return False
    
    return user.is_premium()

def get_days_until_expiry(user_id):
    """Get days remaining in premium membership"""
    
    user = User.query.get(user_id)
    if not user or not user.premium_until:
        return 0
    
    days = (user.premium_until - datetime.utcnow()).days
    return max(0, days)

def is_expiring_soon(user_id, days_threshold=7):
    """Check if membership is expiring soon"""
    
    days_remaining = get_days_until_expiry(user_id)
    return 0 < days_remaining <= days_threshold

# =========================================================
# MEMBERSHIP STATISTICS
# =========================================================

def get_membership_stats():
    """Get overall membership statistics"""
    
    total_users = User.query.count()
    premium_users = User.query.filter(User.premium_until > datetime.utcnow()).count()
    basic_users = User.query.filter_by(role='basic').count()
    
    total_revenue = db.session.query(db.func.sum(Order.amount)).filter(
        Order.status == OrderStatus.PAID.value,
        Order.report_type == 'membership'
    ).scalar() or 0
    
    return {
        'total_users': total_users,
        'premium_users': premium_users,
        'basic_users': basic_users,
        'premium_percentage': round((premium_users / total_users * 100) if total_users > 0 else 0, 2),
        'total_revenue': total_revenue,
        'average_revenue_per_user': round(total_revenue / premium_users if premium_users > 0 else 0, 2)
    }

def get_expiring_memberships(days_threshold=7):
    """Get list of memberships expiring within threshold"""
    
    expiry_date = datetime.utcnow() + timedelta(days=days_threshold)
    
    expiring = User.query.filter(
        User.premium_until.isnot(None),
        User.premium_until <= expiry_date,
        User.premium_until > datetime.utcnow()
    ).all()
    
    return expiring
