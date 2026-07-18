# =========================================================
# PAYMENT & QR CODE SYSTEM
# =========================================================

import qrcode
import io
import base64
import secrets
from datetime import datetime
from models import db, Order, Payment, OrderStatus

# =========================================================
# PAYMENT CONFIGURATION
# =========================================================

UPI_ID = "7099805039-2@axl"
PAYEE_NAME = "Ananda Sarmah"
CURRENCY = "INR"

PRICING = {
    'digital_report': 201,
    'printed_report': 501,
    'premium_membership_1month': 500,
    'premium_membership_3month': 1200,
    'premium_membership_6month': 2200,
    'premium_membership_12month': 4000
}

# =========================================================
# QR CODE GENERATION
# =========================================================

def generate_upi_string(amount, order_id, reference=None):
    """
    Generate UPI payment string for QR code
    Format: upi://pay?pa=UPI_ID&pn=PAYEE_NAME&am=AMOUNT&tn=NOTE&tr=REFERENCE
    """
    if not reference:
        reference = f"NUM{order_id}{secrets.token_hex(4).upper()}"
    
    note = f"Numerology Report - Order {order_id}"
    
    upi_string = (
        f"upi://pay?"
        f"pa={UPI_ID}&"
        f"pn={PAYEE_NAME.replace(' ', '%20')}&"
        f"am={amount}&"
        f"tn={note.replace(' ', '%20')}&"
        f"tr={reference}"
    )
    
    return upi_string, reference

def generate_qr_code(amount, order_id):
    """Generate QR code image for payment"""
    upi_string, reference = generate_upi_string(amount, order_id)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(upi_string)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert image to base64
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    return {
        'image': f"data:image/png;base64,{img_base64}",
        'upi_string': upi_string,
        'reference': reference,
        'upi_id': UPI_ID,
        'payee_name': PAYEE_NAME,
        'amount': amount,
        'currency': CURRENCY
    }

# =========================================================
# ORDER MANAGEMENT
# =========================================================

def create_order(user_id, report_type, amount):
    """Create new payment order"""
    order_id = f"ORD{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{secrets.token_hex(3).upper()}"
    
    order = Order(
        order_id=order_id,
        user_id=user_id,
        report_type=report_type,
        amount=amount,
        status=OrderStatus.PENDING.value
    )
    
    db.session.add(order)
    db.session.commit()
    
    return order

def create_payment_record(order_id, amount, qr_data):
    """Create payment record"""
    order = Order.query.get(order_id)
    
    if not order:
        return None, 'Order not found'
    
    payment = Payment(
        order_id=order_id,
        amount=amount,
        upi_id=UPI_ID,
        payee_name=PAYEE_NAME,
        currency=CURRENCY,
        qr_code_data=qr_data
    )
    
    db.session.add(payment)
    db.session.commit()
    
    return payment, None

def verify_payment(order_id, utr):
    """Verify payment via UTR"""
    order = Order.query.get(order_id)
    
    if not order:
        return False, 'Order not found'
    
    if order.status == OrderStatus.PAID.value:
        return True, 'Payment already verified'
    
    # Store UTR and mark as verified (admin will verify in dashboard)
    order.payment_utr = utr
    order.verified = False
    order.status = OrderStatus.PENDING.value
    
    db.session.commit()
    
    return True, 'UTR recorded, awaiting admin verification'

def admin_verify_payment(order_id, verified=True):
    """Admin verify payment"""
    order = Order.query.get(order_id)
    
    if not order:
        return False, 'Order not found'
    
    if verified:
        order.status = OrderStatus.PAID.value
        order.verified = True
    else:
        order.status = OrderStatus.FAILED.value
        order.verified = False
    
    db.session.commit()
    
    return True, 'Payment verification updated'

# =========================================================
# PAYMENT HELPERS
# =========================================================

def get_report_price(report_type):
    """Get price for report type"""
    return PRICING.get(report_type, 0)

def get_membership_price(duration):
    """Get membership price"""
    key = f'premium_membership_{duration}'
    return PRICING.get(key, 500)

def format_amount(amount):
    """Format amount for display"""
    return f"₹{amount}"

def get_payment_status(order):
    """Get readable payment status"""
    status_map = {
        'pending': 'Awaiting Payment',
        'paid': 'Payment Received',
        'completed': 'Completed',
        'failed': 'Payment Failed',
        'refunded': 'Refunded'
    }
    return status_map.get(order.status, order.status)
