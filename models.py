# =========================================================
# DATABASE MODELS
# =========================================================

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from enum import Enum
import bcrypt
import secrets

db = SQLAlchemy()

# =========================================================
# ENUMS
# =========================================================

class UserRole(Enum):
    GUEST = "guest"
    BASIC = "basic"
    PREMIUM = "premium"
    ADMIN = "admin"

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class ReportType(Enum):
    DIGITAL = "digital"
    PRINTED = "printed"

# =========================================================
# USERS TABLE
# =========================================================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(50), default=UserRole.BASIC.value)
    premium_until = db.Column(db.DateTime, nullable=True)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    ai_chats = db.relationship('AIChat', backref='user', lazy=True, cascade='all, delete-orphan')
    consultations = db.relationship('Consultation', backref='user', lazy=True, cascade='all, delete-orphan')
    downloads = db.relationship('Download', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def is_premium(self):
        if self.premium_until is None:
            return False
        return datetime.utcnow() < self.premium_until
    
    def upgrade_premium(self, months=1):
        if self.premium_until and self.premium_until > datetime.utcnow():
            self.premium_until = self.premium_until + timedelta(days=30*months)
        else:
            self.premium_until = datetime.utcnow() + timedelta(days=30*months)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'mobile': self.mobile,
            'role': self.role,
            'is_premium': self.is_premium(),
            'language': self.language,
            'created_at': self.created_at.isoformat()
        }

# =========================================================
# ORDERS TABLE
# =========================================================

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # digital, printed
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default=OrderStatus.PENDING.value)
    payment_utr = db.Column(db.String(100), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    report = db.relationship('Report', backref='order', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'report_type': self.report_type,
            'amount': self.amount,
            'status': self.status,
            'verified': self.verified,
            'created_at': self.created_at.isoformat()
        }

# =========================================================
# PAYMENTS TABLE
# =========================================================

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    upi_id = db.Column(db.String(255), nullable=False)
    payee_name = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(10), default='INR')
    qr_code_data = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'upi_id': self.upi_id,
            'currency': self.currency
        }

# =========================================================
# REPORTS TABLE
# =========================================================

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    report_data = db.Column(db.Text, nullable=False)  # JSON format
    pdf_path = db.Column(db.String(255), nullable=True)
    watermarked = db.Column(db.Boolean, default=True)
    digital_signature = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'pdf_path': self.pdf_path,
            'created_at': self.created_at.isoformat()
        }

# =========================================================
# DOWNLOADS TABLE
# =========================================================

class Download(db.Model):
    __tablename__ = 'downloads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    downloaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50), nullable=True)
    
    report = db.relationship('Report', backref='downloads')

# =========================================================
# AI CHATS TABLE
# =========================================================

class AIChat(db.Model):
    __tablename__ = 'ai_chats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'response': self.response,
            'created_at': self.created_at.isoformat()
        }

# =========================================================
# CONSULTATIONS TABLE
# =========================================================

class Consultation(db.Model):
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    consultation_type = db.Column(db.String(100), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    language = db.Column(db.String(10), default='en')
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='scheduled')  # scheduled, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.consultation_type,
            'date': self.scheduled_date.isoformat(),
            'status': self.status
        }

# =========================================================
# ADMIN TABLE
# =========================================================

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# =========================================================
# AI MESSAGE COUNTER TABLE
# =========================================================

class AIMessageCounter(db.Model):
    __tablename__ = 'ai_message_counters'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    message_count = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)
    
    def should_reset(self):
        return (datetime.utcnow() - self.last_reset).days >= 1
    
    def reset_if_needed(self):
        if self.should_reset():
            self.message_count = 0
            self.last_reset = datetime.utcnow()
    
    def can_send_message(self, user):
        self.reset_if_needed()
        
        if user.role == UserRole.ADMIN.value:
            return True
        if user.role == UserRole.PREMIUM.value or user.is_premium():
            return True
        if user.role == UserRole.BASIC.value:
            return self.message_count < 1  # 1 message per day
        if user.role == UserRole.GUEST.value:
            return self.message_count < 1  # 1 message only
        
        return False
    
    def increment_message(self):
        self.message_count += 1

# =========================================================
# SETTINGS TABLE
# =========================================================

class Settings(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def get(key, default=None):
        setting = Settings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set(key, value):
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

# =========================================================
# CONTACT MESSAGES TABLE
# =========================================================

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='new')  # new, replied, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }

# =========================================================
# ACTIVITY LOGS TABLE
# =========================================================

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
