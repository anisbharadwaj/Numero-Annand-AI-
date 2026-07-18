# =========================================================
# AUTHENTICATION SYSTEM
# =========================================================

import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from models import User, Admin, db

# =========================================================
# JWT CONFIGURATION
# =========================================================

JWT_SECRET = os.getenv('JWT_SECRET', 'numero-annand-ai-secret-key-2024')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRY_DAYS = 30

# =========================================================
# TOKEN GENERATION
# =========================================================

def generate_token(user_id, role='user', expires_in_days=JWT_EXPIRY_DAYS):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'role': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=expires_in_days)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# =========================================================
# DECORATORS
# =========================================================

def token_required(f):
    """Decorator to check if valid token is provided"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.user_id = payload.get('user_id')
        request.user_role = payload.get('role')
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        if payload.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        request.user_id = payload.get('user_id')
        request.user_role = payload.get('role')
        return f(*args, **kwargs)
    
    return decorated

def premium_required(f):
    """Decorator to check if user is premium"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.query.get(payload.get('user_id'))
        if not user or (not user.is_premium() and user.role != 'admin'):
            return jsonify({'error': 'Premium membership required'}), 403
        
        request.user_id = payload.get('user_id')
        request.user_role = payload.get('role')
        return f(*args, **kwargs)
    
    return decorated

# =========================================================
# AUTHENTICATION FUNCTIONS
# =========================================================

def register_user(email, password, name, mobile='', language='en'):
    """Register new user"""
    if User.query.filter_by(email=email).first():
        return None, 'Email already registered'
    
    user = User(
        email=email,
        name=name,
        mobile=mobile,
        language=language,
        role='basic'
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return user, None

def login_user(email, password):
    """Authenticate user login"""
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return None, None, 'Invalid email or password'
    
    token = generate_token(user.id, user.role)
    return user, token, None

def change_password(user_id, old_password, new_password):
    """Change user password"""
    user = User.query.get(user_id)
    
    if not user:
        return False, 'User not found'
    
    if not user.check_password(old_password):
        return False, 'Current password is incorrect'
    
    user.set_password(new_password)
    db.session.commit()
    
    return True, 'Password changed successfully'

def reset_password(email, new_password):
    """Reset user password (admin function)"""
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return False, 'User not found'
    
    user.set_password(new_password)
    db.session.commit()
    
    return True, 'Password reset successfully'

# =========================================================
# SESSION MANAGEMENT
# =========================================================

def create_session(user_id, token):
    """Create user session"""
    session_data = {
        'user_id': user_id,
        'token': token,
        'created_at': datetime.utcnow().isoformat()
    }
    return session_data

def verify_session(token):
    """Verify user session"""
    payload = verify_token(token)
    if payload:
        user = User.query.get(payload.get('user_id'))
        if user:
            return user
    return None
