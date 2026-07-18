# =========================================================
# ANNAND AI ASSISTANT ENGINE
# =========================================================

import random
import json
from datetime import datetime
from models import db, AIChat, AIMessageCounter, User

# =========================================================
# AI KNOWLEDGE BASE
# =========================================================

AI_KNOWLEDGE_BASE = {
    'numerology': {
        'about': 'Numerology is the study of numbers and their mystical meanings. It reveals your personality, destiny, and life path.',
        'systems': [
            'Lo Shu Grid - Ancient Chinese numerology system',
            'Vedic Numerology - Indian numerological traditions',
            'Pythagorean - Western numerology system',
            'Chaldean - Babylonian numerology system'
        ]
    },
    'services': {
        'digital_report': {
            'name': 'Digital Numerology Report',
            'price': '₹201',
            'description': 'Instant digital PDF report with complete numerology analysis'
        },
        'printed_report': {
            'name': 'Premium Printed Report',
            'price': '₹501',
            'description': 'Premium printed report delivered to your address'
        },
        'consultation': {
            'name': 'Personal Consultation',
            'price': '₹500/month (Premium Members)',
            'description': 'Direct consultation with numerology experts'
        },
        'premium': {
            'name': 'Premium Membership',
            'price': 'From ₹500/month',
            'description': 'Unlimited reports, consultations, and premium features'
        }
    },
    'numbers': {
        '1': 'Leadership, Independence, Innovation',
        '2': 'Balance, Harmony, Cooperation',
        '3': 'Creativity, Communication, Expression',
        '4': 'Stability, Foundation, Hard Work',
        '5': 'Freedom, Adventure, Change',
        '6': 'Responsibility, Harmony, Healing',
        '7': 'Spirituality, Wisdom, Intuition',
        '8': 'Power, Success, Material Abundance',
        '9': 'Compassion, Completion, Humanitarianism'
    },
    'faq': {
        'how_it_works': 'Numerology analyzes your name and birth date to reveal your personality, destiny number, and life path. Different systems provide unique insights.',
        'accuracy': 'Numerology is a spiritual practice. Its accuracy depends on your openness to the insights and how you apply the guidance.',
        'payment': 'We accept payments via UPI (PhonePe, Google Pay, Paytm, BHIM, Amazon Pay). Scan the QR code and enter your UTR for verification.',
        'reports': 'Digital reports are instant. Premium printed reports take 5-7 business days for delivery.',
        'membership': 'Premium membership includes unlimited reports, consultations, and exclusive features. Plans start at ₹500/month.'
    },
    'contact': {
        'founder': 'Annand Sarma',
        'mobile': '+91 7099805039',
        'email': 'support@numeroannand.com',
        'whatsapp': 'https://wa.me/917099805039',
        'community': 'https://chat.whatsapp.com/G23u7Yf3PuIC6Gw7GCJIMJ'
    }
}

# =========================================================
# TRANSLATIONS
# =========================================================

AI_TRANSLATIONS = {
    'en': {
        'greeting': 'Hello! I am Annand AI, your personal numerology assistant. How can I help you today?',
        'help': 'I can help you with:\n• Numerology information\n• Service details\n• Number meanings\n• Payment guidance\n• Account support',
        'typing': 'Annand is typing...',
        'thinking': 'Let me think about that...',
        'farewell': 'Thank you for chatting! Visit our website to learn more about numerology.'
    },
    'hi': {
        'greeting': 'नमस्ते! मैं Annand AI हूं, आपका व्यक्तिगत अंकशास्त्र सहायक। मैं आपकी कैसे मदद कर सकता हूं?',
        'help': 'मैं आपकी मदद कर सकता हूं:\n• अंकशास्त्र की जानकारी\n• सेवा विवरण\n• संख्या के अर्थ\n• भुगतान मार्गदर्शन\n• खाता समर्थन',
        'typing': 'Annand टाइप कर रहे हैं...',
        'thinking': 'मुझे इसके बारे में सोचने दें...',
        'farewell': 'चैट करने के लिए धन्यवाद! अंकशास्त्र के बारे में अधिक जानने के लिए हमारी वेबसाइट पर जाएं।'
    },
    'as': {
        'greeting': 'নমস্কাৰ! মই Annand AI, আপোনাৰ ব্যক্তিগত সংখ্যা বিজ্ঞান সহায়ক। মই আপোনাক কেনেকৈ সহায়তা কৰিব পাৰোঁ?',
        'help': 'মই আপোনাক সহায়তা কৰিব পাৰোঁ:\n• সংখ্যা বিজ্ঞান তথ্য\n• সেৱা বিৱৰণ\n• সংখ্যা অৰ্থ\n• পেমেন্ট নিৰ্দেশনা\n• অ্যাকাউন্ট সমৰ্থন',
        'typing': 'Annand টাইপ কৰিছে...',
        'thinking': 'মোক এই বিষয়ে চিন্তা কৰিবলৈ দিয়ক...',
        'farewell': 'চ্যাট কৰাৰ বাবে ধন্যবাদ! সংখ্যা বিজ্ঞান সম্পৰ্কে আৰও জানিবলৈ আমাদের ওয়েবসাইট ভিজিট কৰক।'
    }
}

# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

SUGGESTED_QUESTIONS = {
    'en': [
        'What is numerology?',
        'How do I get a report?',
        'What are lucky numbers?',
        'Tell me about services',
        'How does payment work?',
        'What is my destiny number?'
    ],
    'hi': [
        'अंकशास्त्र क्या है?',
        'मुझे रिपोर्ट कैसे मिलेगी?',
        'भाग्यशाली संख्याएं क्या हैं?',
        'सेवाओं के बारे में बताएं',
        'भुगतान कैसे काम करता है?',
        'मेरा भाग्य अंक क्या है?'
    ],
    'as': [
        'সংখ্যা বিজ্ঞান কি?',
        'মই প্রতিবেদন কেনেকৈ পাব?',
        'ভাগ্যৱান সংখ্যা কি?',
        'সেৱা সম্পর্কে বলক',
        'পেমেন্ট কেনেকৈ কাম কৰে?',
        'মোৰ ভাগ্য সংখ্যা কি?'
    ]
}

# =========================================================
# AI RESPONSE ENGINE
# =========================================================

class AnnandAI:
    
    def __init__(self, language='en'):
        self.language = language if language in AI_TRANSLATIONS else 'en'
    
    def get_greeting(self):
        """Get greeting message"""
        return AI_TRANSLATIONS[self.language]['greeting']
    
    def get_help_text(self):
        """Get help/menu text"""
        return AI_TRANSLATIONS[self.language]['help']
    
    def get_suggested_questions(self):
        """Get suggested questions"""
        return SUGGESTED_QUESTIONS.get(self.language, SUGGESTED_QUESTIONS['en'])
    
    def process_message(self, user_message):
        """Process user message and generate response"""
        
        message_lower = user_message.lower().strip()
        
        # Check for service inquiries
        if any(word in message_lower for word in ['report', 'package', 'service', 'price']):
            return self._respond_about_services()
        
        # Check for numerology info
        if any(word in message_lower for word in ['numerology', 'number', 'meaning', 'lucky']):
            return self._respond_about_numerology(message_lower)
        
        # Check for payment info
        if any(word in message_lower for word in ['payment', 'pay', 'utr', 'upi', 'price']):
            return self._respond_about_payment()
        
        # Check for contact info
        if any(word in message_lower for word in ['contact', 'support', 'help', 'phone', 'whatsapp']):
            return self._respond_contact_info()
        
        # Check for membership info
        if any(word in message_lower for word in ['premium', 'membership', 'subscribe']):
            return self._respond_about_membership()
        
        # Default response
        return self._respond_default(user_message)
    
    def _respond_about_services(self):
        """Generate response about services"""
        response = "Here are our services:\n\n"
        
        for service_id, service in AI_KNOWLEDGE_BASE['services'].items():
            response += f"🔮 {service['name']}\n"
            response += f"Price: {service['price']}\n"
            response += f"{service['description']}\n\n"
        
        return response
    
    def _respond_about_numerology(self, message):
        """Generate response about numerology"""
        
        # Check if asking about specific number
        for num in range(1, 10):
            if str(num) in message:
                return f"Number {num}: {AI_KNOWLEDGE_BASE['numbers'][str(num)]}\n\nEach number carries unique vibrations and meanings in numerology. Want to know more about other numbers?"
        
        # General numerology response
        response = "Numerology is a spiritual science that studies the vibrations of numbers.\n\n"
        response += "We support multiple systems:\n"
        for system in AI_KNOWLEDGE_BASE['numerology']['systems']:
            response += f"• {system}\n"
        response += "\nEach system provides unique insights into your personality and destiny."
        
        return response
    
    def _respond_about_payment(self):
        """Generate response about payment"""
        response = "Payment Process:\n\n"
        response += "1. Select your report or membership\n"
        response += "2. Click 'Pay Now' to generate QR code\n"
        response += "3. Scan with PhonePe, Google Pay, Paytm, or any UPI app\n"
        response += "4. Enter UTR after successful payment\n"
        response += "5. We verify and send your report\n\n"
        response += "Accepted: PhonePe, Google Pay, Paytm, BHIM, Amazon Pay, All Banking Apps"
        return response
    
    def _respond_contact_info(self):
        """Generate contact information response"""
        response = "Get in Touch:\n\n"
        contact = AI_KNOWLEDGE_BASE['contact']
        response += f"Founder: {contact['founder']}\n"
        response += f"Mobile: {contact['mobile']}\n"
        response += f"Email: {contact['email']}\n\n"
        response += f"Chat on WhatsApp: {contact['whatsapp']}\n"
        response += f"Join Community: {contact['community']}"
        return response
    
    def _respond_about_membership(self):
        """Generate response about membership"""
        response = "Premium Membership Benefits:\n\n"
        response += "✓ Unlimited AI Messages\n"
        response += "✓ Free Reports\n"
        response += "✓ Priority Support\n"
        response += "✓ Monthly Consultations\n"
        response += "✓ Exclusive Tips & Insights\n"
        response += "✓ Early Access to Features\n\n"
        response += "Plans starting from ₹500/month"
        return response
    
    def _respond_default(self, message):
        """Generate default response"""
        responses = [
            "That's an interesting question! I'm learning more about it. What would you like to know more about?",
            "I'm always happy to help! Try asking me about our services, numerology, or payment information.",
            "Let me help you better - could you ask me about numerology, services, or payments?",
            "I'm here to assist! Ask me anything about our numerology services."
        ]
        return random.choice(responses)

# =========================================================
# MESSAGE PERSISTENCE
# =========================================================

def save_ai_chat(user_id, message, response, language='en'):
    """Save AI chat to database"""
    
    chat = AIChat(
        user_id=user_id,
        message=message,
        response=response,
        language=language
    )
    
    db.session.add(chat)
    db.session.commit()
    
    return chat

def get_chat_history(user_id, limit=20):
    """Get user chat history"""
    
    chats = AIChat.query.filter_by(user_id=user_id).order_by(
        AIChat.created_at.desc()
    ).limit(limit).all()
    
    history = []
    for chat in reversed(chats):
        history.append({
            'id': chat.id,
            'message': chat.message,
            'response': chat.response,
            'created_at': chat.created_at.isoformat()
        })
    
    return history

def clear_chat_history(user_id):
    """Clear user chat history"""
    
    AIChat.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    return True

# =========================================================
# MESSAGE COUNTER MANAGEMENT
# =========================================================

def get_or_create_counter(user_id):
    """Get or create message counter for user"""
    
    counter = AIMessageCounter.query.filter_by(user_id=user_id).first()
    
    if not counter:
        counter = AIMessageCounter(user_id=user_id)
        db.session.add(counter)
        db.session.commit()
    
    return counter

def get_remaining_messages(user_id):
    """Get remaining messages for user"""
    
    user = User.query.get(user_id)
    counter = get_or_create_counter(user_id)
    
    counter.reset_if_needed()
    
    if user.role == 'admin' or (user.role == 'premium' or user.is_premium()):
        return -1  # Unlimited
    elif user.role == 'basic':
        remaining = 1 - counter.message_count
        return max(0, remaining)
    else:  # guest
        remaining = 1 - counter.message_count
        return max(0, remaining)

def can_send_message(user_id):
    """Check if user can send message"""
    
    user = User.query.get(user_id)
    counter = get_or_create_counter(user_id)
    
    return counter.can_send_message(user)

def log_message_sent(user_id):
    """Log message sent for user"""
    
    counter = get_or_create_counter(user_id)
    counter.increment_message()
    db.session.commit()
