"""
Advanced Auto QR Generation System
Automatic QR code generation with caching, optimization, and creative enhancements
"""

import qrcode
import io
import base64
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

class AutoQRGenerator:
    """Advanced QR Code generator with creative enhancements"""
    
    def __init__(self):
        self.cache_dir = Path('qr_cache')
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_expiry = 24 * 60 * 60  # 24 hours
        
    def _get_cache_key(self, data):
        """Generate cache key for QR data"""
        return hashlib.md5(str(data).encode()).hexdigest()
    
    def _is_cache_valid(self, cache_file):
        """Check if cache file is still valid"""
        if not cache_file.exists():
            return False
        
        file_age = datetime.now().timestamp() - cache_file.stat().st_mtime
        return file_age < self.cache_expiry
    
    def generate_basic_qr(self, data, version=None, box_size=10, border=4):
        """Generate basic QR code"""
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    
    def generate_branded_qr(self, data, brand_text="Numero Annand AI", logo=None):
        """Generate QR code with branding"""
        
        # Generate base QR
        qr_img = self.generate_basic_qr(data, box_size=8)
        
        # Add border and brand text
        qr_width = qr_img.size[0]
        new_size = qr_width + 200
        
        branded = Image.new('RGB', (new_size, new_size), 'white')
        branded.paste(qr_img, (100, 50))
        
        # Add brand text
        try:
            draw = ImageDraw.Draw(branded)
            # Use default font if custom font not available
            draw.text((new_size//2, new_size - 40), brand_text, 
                     fill='black', anchor='mm')
        except:
            pass
        
        return branded
    
    def generate_gradient_qr(self, data, primary_color=(102, 126, 234), 
                            secondary_color=(118, 75, 162)):
        """Generate QR code with gradient effect"""
        
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image with gradient
        size = qr.modules_count
        img = Image.new('RGB', (size * 10, size * 10), 'white')
        pixels = img.load()
        
        # Fill with QR pattern using gradient colors
        for i in range(size):
            for j in range(size):
                if qr.modules[i][j]:
                    # Create gradient effect
                    ratio = i / size
                    r = int(primary_color[0] * (1-ratio) + secondary_color[0] * ratio)
                    g = int(primary_color[1] * (1-ratio) + secondary_color[1] * ratio)
                    b = int(primary_color[2] * (1-ratio) + secondary_color[2] * ratio)
                    
                    for x in range(10):
                        for y in range(10):
                            pixels[i*10+x, j*10+y] = (r, g, b)
        
        return img
    
    def generate_styled_qr(self, data, style='professional', size=300):
        """Generate styled QR code for different use cases"""
        
        styles = {
            'professional': {
                'border': 80,
                'colors': {'dark': '#1F2937', 'light': '#FFFFFF'},
                'corner_radius': 0
            },
            'vibrant': {
                'border': 60,
                'colors': {'dark': '#667EEA', 'light': '#F3F4F6'},
                'corner_radius': 15
            },
            'minimal': {
                'border': 40,
                'colors': {'dark': '#000000', 'light': '#FFFFFF'},
                'corner_radius': 0
            },
            'spiritual': {
                'border': 100,
                'colors': {'dark': '#764BA2', 'light': '#F9F5F0'},
                'corner_radius': 5
            }
        }
        
        config = styles.get(style, styles['professional'])
        
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(
            fill_color=config['colors']['dark'],
            back_color=config['colors']['light']
        )
        
        return qr_img
    
    def generate_cached_qr(self, data, format='base64', style='professional'):
        """Generate QR with caching"""
        
        cache_key = self._get_cache_key(f"{data}_{style}")
        cache_file = self.cache_dir / f"{cache_key}.png"
        
        # Check cache
        if self._is_cache_valid(cache_file):
            with open(cache_file, 'rb') as f:
                if format == 'base64':
                    return base64.b64encode(f.read()).decode()
                else:
                    return f.read()
        
        # Generate new QR
        qr_img = self.generate_styled_qr(data, style)
        
        # Cache it
        qr_img.save(cache_file)
        
        # Return in requested format
        if format == 'base64':
            buffer = io.BytesIO()
            qr_img.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode()
        else:
            return qr_img
    
    def generate_qr_with_metadata(self, data, metadata=None):
        """Generate QR with associated metadata"""
        
        qr_data = {
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {},
            'qr_code': None
        }
        
        # Generate QR
        qr_img = self.generate_styled_qr(data, 'professional')
        
        # Convert to base64
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_data['qr_code'] = base64.b64encode(buffer.getvalue()).decode()
        
        return qr_data
    
    def bulk_generate_qrs(self, data_list, style='professional'):
        """Generate multiple QR codes efficiently"""
        
        qr_codes = []
        for i, data in enumerate(data_list):
            try:
                qr_base64 = self.generate_cached_qr(data, style=style)
                qr_codes.append({
                    'index': i,
                    'data': data,
                    'qr_code': qr_base64,
                    'status': 'success'
                })
            except Exception as e:
                qr_codes.append({
                    'index': i,
                    'data': data,
                    'error': str(e),
                    'status': 'failed'
                })
        
        return qr_codes
    
    def generate_dynamic_qr(self, base_url, params=None):
        """Generate QR for dynamic URLs with parameters"""
        
        url = base_url
        if params:
            param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            url = f"{base_url}?{param_string}"
        
        return self.generate_styled_qr(url, 'professional')
    
    def get_qr_stats(self):
        """Get statistics about cached QR codes"""
        
        cache_files = list(self.cache_dir.glob('*.png'))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_cached': len(cache_files),
            'cache_size_mb': round(total_size / (1024*1024), 2),
            'cache_directory': str(self.cache_dir),
            'expiry_hours': self.cache_expiry // 3600
        }
    
    def clear_expired_cache(self):
        """Clean up expired cache files"""
        
        current_time = datetime.now().timestamp()
        expired_count = 0
        
        for cache_file in self.cache_dir.glob('*.png'):
            file_age = current_time - cache_file.stat().st_mtime
            if file_age > self.cache_expiry:
                cache_file.unlink()
                expired_count += 1
        
        return {
            'expired_removed': expired_count,
            'timestamp': datetime.now().isoformat()
        }


# Initialize global instance
auto_qr = AutoQRGenerator()


def generate_payment_qr(amount, order_id, upi_id="anand@okhdfcbank"):
    """Auto-generate payment QR for orders"""
    
    upi_string = f"upi://pay?pa={upi_id}&pn=NumeroAnnand&am={amount}&tn=Order%20{order_id}&tr={order_id}"
    
    qr_data = auto_qr.generate_qr_with_metadata(
        upi_string,
        metadata={
            'type': 'payment',
            'amount': amount,
            'order_id': order_id,
            'timestamp': datetime.now().isoformat()
        }
    )
    
    return qr_data


def generate_report_qr(report_id, user_email):
    """Auto-generate QR for report downloads"""
    
    download_url = f"https://numero-annand.ai/download-report/{report_id}"
    
    qr_data = auto_qr.generate_qr_with_metadata(
        download_url,
        metadata={
            'type': 'report',
            'report_id': report_id,
            'user_email': user_email,
            'timestamp': datetime.now().isoformat()
        }
    )
    
    return qr_data


def generate_sharing_qr(content_id, content_type='analysis'):
    """Auto-generate QR for social sharing"""
    
    share_url = f"https://numero-annand.ai/share/{content_type}/{content_id}"
    
    qr_data = auto_qr.generate_qr_with_metadata(
        share_url,
        metadata={
            'type': 'sharing',
            'content_id': content_id,
            'content_type': content_type,
            'timestamp': datetime.now().isoformat()
        }
    )
    
    return qr_data


def generate_verification_qr(verification_token):
    """Auto-generate QR for email/account verification"""
    
    verify_url = f"https://numero-annand.ai/verify/{verification_token}"
    
    qr_data = auto_qr.generate_qr_with_metadata(
        verify_url,
        metadata={
            'type': 'verification',
            'token': verification_token,
            'timestamp': datetime.now().isoformat()
        }
    )
    
    return qr_data
