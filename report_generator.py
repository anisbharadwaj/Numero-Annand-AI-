# =========================================================
# PREMIUM REPORT GENERATION SYSTEM
# =========================================================

import json
import os
from datetime import datetime
from models import db, Report, Order, User
from payment import generate_qr_code

# =========================================================
# NUMEROLOGY ENGINE FOR REPORTS
# =========================================================

class NumerologyAnalyzer:
    """Advanced numerology analyzer for premium reports"""
    
    CHALDEAN_MAP = {
        'A':1,'I':1,'J':1,'Q':1,'Y':1,
        'B':2,'K':2,'R':2,
        'C':3,'G':3,'L':3,'S':3,
        'D':4,'M':4,'T':4,
        'E':5,'H':5,'N':5,'X':5,
        'U':6,'V':6,'W':6,
        'O':7,'Z':7,
        'F':8,'P':8
    }
    
    MASTER_NUMBERS = {11, 22, 33}
    
    LOSHU_LAYOUT = [
        [4,9,2],
        [3,5,7],
        [8,1,6]
    ]
    
    def __init__(self, name, dob):
        self.name = name
        self.dob = dob
        self.freq = {i: 0 for i in range(1, 10)}
        self.grid_map = {i: [] for i in range(1, 10)}
    
    def reduce(self, n, master=True):
        """Reduce number to single digit"""
        if master and n in self.MASTER_NUMBERS:
            return n
        
        while n > 9:
            n = sum(int(x) for x in str(n))
            if master and n in self.MASTER_NUMBERS:
                return n
        
        return n
    
    def calculate_birth_number(self, dob_str):
        """Calculate birth number from date of birth"""
        parts = dob_str.replace('/', '-').split('-')
        day = int(parts[0])
        return self.reduce(day)
    
    def calculate_destiny_number(self, dob_str):
        """Calculate destiny number"""
        parts = dob_str.replace('/', '-').split('-')
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
        total = day + month + year
        return self.reduce(total)
    
    def calculate_name_number(self):
        """Calculate name number"""
        total = 0
        for ch in self.name.upper():
            if ch.isalpha():
                total += self.CHALDEAN_MAP.get(ch, 0)
        return self.reduce(total)
    
    def get_loshu_grid(self, dob_str):
        """Generate Lo Shu Grid"""
        grid_data = {}
        
        # Populate grid with numbers
        for row in self.LOSHU_LAYOUT:
            for num in row:
                grid_data[num] = {
                    'value': num,
                    'count': self.freq.get(num, 0)
                }
        
        return grid_data
    
    def get_missing_numbers(self):
        """Get missing numbers in grid"""
        return [n for n in range(1, 10) if self.freq[n] == 0]
    
    def get_repeated_numbers(self):
        """Get repeated numbers in grid"""
        return [n for n, c in self.freq.items() if c >= 2]

# =========================================================
# REPORT GENERATION
# =========================================================

def generate_premium_report(user_id, order_id, name, dob, mobile=''):
    """Generate comprehensive premium numerology report"""
    
    try:
        user = User.query.get(user_id)
        order = Order.query.get(order_id)
        
        if not order or not user:
            return None, 'Order or user not found'
        
        # Analyze numerology
        analyzer = NumerologyAnalyzer(name, dob)
        
        birth_number = analyzer.calculate_birth_number(dob)
        destiny_number = analyzer.calculate_destiny_number(dob)
        name_number = analyzer.calculate_name_number()
        
        # Create comprehensive report data
        report_data = {
            'user': {
                'name': name,
                'dob': dob,
                'mobile': mobile,
                'email': user.email
            },
            'numbers': {
                'birth': birth_number,
                'destiny': destiny_number,
                'name': name_number
            },
            'analysis': {
                'birth_number': get_number_meaning(birth_number),
                'destiny_number': get_number_meaning(destiny_number),
                'name_number': get_number_meaning(name_number),
                'missing_numbers': analyzer.get_missing_numbers(),
                'repeated_numbers': analyzer.get_repeated_numbers()
            },
            'generated_at': datetime.utcnow().isoformat(),
            'founder': 'Annand Sarma',
            'platform': 'Numero Annand AI Premium'
        }
        
        # Create report record
        report = Report(
            order_id=order_id,
            user_name=name,
            dob=dob,
            mobile=mobile,
            report_data=json.dumps(report_data),
            watermarked=True,
            digital_signature=f"NUM-{order_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        )
        
        db.session.add(report)
        db.session.commit()
        
        # Generate QR code for PDF verification
        qr_data = generate_qr_code(0, report.id)  # 0 for no payment
        
        return report, None
        
    except Exception as e:
        return None, str(e)

def get_number_meaning(number):
    """Get detailed meaning of numerology number"""
    
    meanings = {
        1: {
            'title': 'The Leader',
            'keywords': ['Independence', 'Innovation', 'Initiative', 'Ambition'],
            'description': 'Number 1 represents leadership, independence, and originality. You are a pioneer who creates new paths.',
            'strengths': ['Ambitious', 'Independent', 'Courageous', 'Innovative'],
            'challenges': ['Domineering', 'Impulsive', 'Stubborn'],
            'lucky_color': 'Red',
            'lucky_day': 'Sunday'
        },
        2: {
            'title': 'The Diplomat',
            'keywords': ['Harmony', 'Cooperation', 'Balance', 'Sensitivity'],
            'description': 'Number 2 represents balance, harmony, and cooperation. You are a peacemaker and mediator.',
            'strengths': ['Diplomatic', 'Friendly', 'Sensitive', 'Cooperative'],
            'challenges': ['Indecisive', 'Overly passive', 'Dependent'],
            'lucky_color': 'White',
            'lucky_day': 'Monday'
        },
        3: {
            'title': 'The Creator',
            'keywords': ['Creativity', 'Communication', 'Expression', 'Inspiration'],
            'description': 'Number 3 represents creativity, communication, and self-expression. You are an artist and communicator.',
            'strengths': ['Creative', 'Communicative', 'Optimistic', 'Sociable'],
            'challenges': ['Scattered', 'Unfocused', 'Superficial'],
            'lucky_color': 'Yellow',
            'lucky_day': 'Thursday'
        },
        4: {
            'title': 'The Builder',
            'keywords': ['Stability', 'Foundation', 'Hard Work', 'Practicality'],
            'description': 'Number 4 represents stability, structure, and hard work. You are a builder and organizer.',
            'strengths': ['Practical', 'Reliable', 'Organized', 'Hardworking'],
            'challenges': ['Rigid', 'Limited', 'Materialistic'],
            'lucky_color': 'Blue',
            'lucky_day': 'Wednesday'
        },
        5: {
            'title': 'The Explorer',
            'keywords': ['Freedom', 'Adventure', 'Change', 'Versatility'],
            'description': 'Number 5 represents freedom, adventure, and change. You are an explorer and adventurer.',
            'strengths': ['Adventurous', 'Versatile', 'Curious', 'Dynamic'],
            'challenges': ['Reckless', 'Inconsistent', 'Scattered'],
            'lucky_color': 'Green',
            'lucky_day': 'Friday'
        },
        6: {
            'title': 'The Healer',
            'keywords': ['Responsibility', 'Harmony', 'Love', 'Service'],
            'description': 'Number 6 represents responsibility, harmony, and service. You are a caregiver and healer.',
            'strengths': ['Caring', 'Responsible', 'Loving', 'Harmonious'],
            'challenges': ['Worrying', 'Controlling', 'Over-responsible'],
            'lucky_color': 'Pink',
            'lucky_day': 'Saturday'
        },
        7: {
            'title': 'The Mystic',
            'keywords': ['Spirituality', 'Wisdom', 'Intuition', 'Analysis'],
            'description': 'Number 7 represents spirituality, wisdom, and intuition. You are a seeker and philosopher.',
            'strengths': ['Intuitive', 'Spiritual', 'Analytical', 'Wise'],
            'challenges': ['Withdrawn', 'Cynical', 'Secretive'],
            'lucky_color': 'Purple',
            'lucky_day': 'Monday'
        },
        8: {
            'title': 'The Power Player',
            'keywords': ['Power', 'Success', 'Abundance', 'Authority'],
            'description': 'Number 8 represents power, success, and material abundance. You are an achiever and leader.',
            'strengths': ['Ambitious', 'Powerful', 'Successful', 'Authoritative'],
            'challenges': ['Materialistic', 'Aggressive', 'Obsessive'],
            'lucky_color': 'Gold',
            'lucky_day': 'Tuesday'
        },
        9: {
            'title': 'The Humanist',
            'keywords': ['Compassion', 'Completion', 'Humanitarianism', 'Wisdom'],
            'description': 'Number 9 represents compassion, wisdom, and completion. You are a healer of humanity.',
            'strengths': ['Compassionate', 'Humanitarian', 'Wise', 'Spiritual'],
            'challenges': ['Overly emotional', 'Scattered', 'Moody'],
            'lucky_color': 'Maroon',
            'lucky_day': 'Friday'
        }
    }
    
    return meanings.get(number, {'title': 'Unknown', 'description': 'Number not found'})

def get_report_text_content(report_id):
    """Get text content of report for display"""
    
    report = Report.query.get(report_id)
    if not report:
        return None
    
    data = json.loads(report.report_data)
    
    content = f"""
NUMERO ANNAND AI - PREMIUM NUMEROLOGY REPORT
==========================================

User: {data['user']['name']}
Date of Birth: {data['user']['dob']}
Mobile: {data['user']['mobile']}
Email: {data['user']['email']}

NUMEROLOGY ANALYSIS
===================

Birth Number: {data['numbers']['birth']}
{data['analysis']['birth_number']['title']}
{data['analysis']['birth_number']['description']}

Destiny Number: {data['numbers']['destiny']}
{data['analysis']['destiny_number']['title']}
{data['analysis']['destiny_number']['description']}

Name Number: {data['numbers']['name']}
{data['analysis']['name_number']['title']}
{data['analysis']['name_number']['description']}

Missing Numbers: {', '.join(map(str, data['analysis']['missing_numbers'])) or 'None'}
Repeated Numbers: {', '.join(map(str, data['analysis']['repeated_numbers'])) or 'None'}

Generated: {data['generated_at']}
Platform: {data['platform']}
Founder: {data['founder']}
Digital Signature: {report.digital_signature}
"""
    
    return content

# =========================================================
# REPORT MANAGEMENT
# =========================================================

def mark_report_as_completed(order_id):
    """Mark order and report as completed"""
    
    order = Order.query.get(order_id)
    if not order:
        return False, 'Order not found'
    
    order.status = 'completed'
    db.session.commit()
    
    return True, 'Order completed'

def get_report_by_order(order_id):
    """Get report associated with order"""
    
    report = Report.query.filter_by(order_id=order_id).first()
    return report

def regenerate_report(order_id):
    """Regenerate report for an order"""
    
    order = Order.query.get(order_id)
    if not order:
        return None, 'Order not found'
    
    # Delete existing report
    Report.query.filter_by(order_id=order_id).delete()
    db.session.commit()
    
    # Generate new report
    # This would require user input again
    return None, 'Please re-submit user data for report generation'
