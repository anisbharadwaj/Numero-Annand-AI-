# =========================================================
# COMMUNITY & SOCIAL FEATURES
# =========================================================

from datetime import datetime
from models import db, ContactMessage, User

# =========================================================
# COMMUNITY LINKS
# =========================================================

COMMUNITY_LINKS = {
    'whatsapp_support': {
        'url': 'https://wa.me/917099805039',
        'title': 'WhatsApp Support',
        'description': 'Chat directly with our numerology expert',
        'icon': 'whatsapp'
    },
    'whatsapp_community': {
        'url': 'https://chat.whatsapp.com/G23u7Yf3PuIC6Gw7GCJIMJ',
        'title': 'WhatsApp Community',
        'description': 'Join our active community group',
        'icon': 'whatsapp'
    }
}

# =========================================================
# DAILY TIPS & CONTENT
# =========================================================

DAILY_TIPS = {
    'en': [
        'Lucky numbers bring positive vibrations when aligned with your birth date. Embrace them!',
        'Your destiny number reveals your life purpose. Meditate on this powerful number.',
        'Master numbers (11, 22, 33) carry elevated spiritual energy. Respect their power.',
        'Balance your missing numbers through conscious practice and spiritual growth.',
        'Your numerology chart is your personal roadmap to success and fulfillment.',
        'Angel numbers appear when you need guidance. Pay attention to repeating sequences.',
        'Your life path number guides your journey. Trust the universe\'s plan for you.'
    ],
    'hi': [
        'भाग्यशाली संख्याएं सकारात्मक कंपन लाती हैं। उन्हें स्वीकार करें!',
        'आपका भाग्य अंक जीवन का उद्देश्य बताता है।',
        'मास्टर नंबर (11, 22, 33) आध्यात्मिक ऊर्जा रखते हैं।',
        'अंकशास्त्र चार्ट सफलता का नक्शा है।',
        'देवदूत संख्याएं मार्गदर्शन के लिए प्रकट होती हैं।'
    ],
    'as': [
        'ভাগ্যশালী সংখ্যাগুলি ইতিবাচক কম্পন নিয়ে আসে।',
        'আপনার ভাগ্য সংখ্যা জীবনের উদ্দেশ্য প্রকাশ করে।',
        'মাস্টার সংখ্যাগুলি আধ্যাত্মিক শক্তি বহন করে।',
        'সংখ্যা বিজ্ঞান চার্ট সাফল্যের রোডম্যাপ।',
        'দেবদূত সংখ্যাগুলি দিকনির্দেশনা প্রদান করে।'
    ]
}

# =========================================================
# LUCKY NUMBERS & COLORS
# =========================================================

LUCKY_ELEMENTS = {
    1: {
        'lucky_color': 'Red',
        'lucky_days': ['Sunday'],
        'lucky_stone': 'Ruby',
        'lucky_direction': 'East'
    },
    2: {
        'lucky_color': 'White',
        'lucky_days': ['Monday'],
        'lucky_stone': 'Pearl',
        'lucky_direction': 'West'
    },
    3: {
        'lucky_color': 'Yellow',
        'lucky_days': ['Thursday'],
        'lucky_stone': 'Topaz',
        'lucky_direction': 'North'
    },
    4: {
        'lucky_color': 'Blue',
        'lucky_days': ['Wednesday'],
        'lucky_stone': 'Sapphire',
        'lucky_direction': 'South'
    },
    5: {
        'lucky_color': 'Green',
        'lucky_days': ['Friday'],
        'lucky_stone': 'Emerald',
        'lucky_direction': 'Northeast'
    },
    6: {
        'lucky_color': 'Pink',
        'lucky_days': ['Saturday'],
        'lucky_stone': 'Diamond',
        'lucky_direction': 'Southwest'
    },
    7: {
        'lucky_color': 'Purple',
        'lucky_days': ['Monday'],
        'lucky_stone': 'Amethyst',
        'lucky_direction': 'Northwest'
    },
    8: {
        'lucky_color': 'Gold',
        'lucky_days': ['Tuesday'],
        'lucky_stone': 'Blue Sapphire',
        'lucky_direction': 'South'
    },
    9: {
        'lucky_color': 'Maroon',
        'lucky_days': ['Friday'],
        'lucky_stone': 'Red Coral',
        'lucky_direction': 'South'
    }
}

# =========================================================
# TESTIMONIALS & SUCCESS STORIES
# =========================================================

TESTIMONIALS = {
    'en': [
        {
            'name': 'Rajesh Kumar',
            'location': 'Bangalore',
            'story': 'After getting my numerology reading, I changed my business name and saw 300% growth!',
            'rating': 5
        },
        {
            'name': 'Priya Sharma',
            'location': 'Delhi',
            'story': 'The numerology insights helped me understand my true potential. Life has never been better!',
            'rating': 5
        },
        {
            'name': 'Amit Singh',
            'location': 'Mumbai',
            'story': 'Accurate and detailed report. Highly recommended for anyone seeking spiritual guidance.',
            'rating': 5
        }
    ],
    'hi': [
        {
            'name': 'राज कुमार',
            'location': 'बेंगलुरु',
            'story': 'अंकशास्त्र रीडिंग के बाद मेरे व्यवसाय की वृद्धि 300% हुई!',
            'rating': 5
        }
    ]
}

# =========================================================
# CONTACT & MESSAGE HANDLING
# =========================================================

def submit_contact_message(name, email, mobile, message):
    """Submit contact form message"""
    
    if not all([name, email, message]):
        return None, 'Missing required fields'
    
    contact = ContactMessage(
        name=name,
        email=email,
        mobile=mobile,
        message=message,
        status='new'
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return contact, None

def get_public_testimonials(language='en', limit=3):
    """Get public testimonials"""
    
    testimonials = TESTIMONIALS.get(language, TESTIMONIALS['en'])
    return testimonials[:limit]

# =========================================================
# DAILY NUMEROLOGY FEATURES
# =========================================================

def get_daily_tip(language='en'):
    """Get daily numerology tip"""
    
    tips = DAILY_TIPS.get(language, DAILY_TIPS['en'])
    import random
    return random.choice(tips)

def get_lucky_numbers(number):
    """Get lucky elements for a number"""
    
    return LUCKY_ELEMENTS.get(number, {})

# =========================================================
# NEWSLETTER & SUBSCRIPTION
# =========================================================

def subscribe_newsletter(email, name='', language='en'):
    """Subscribe user to newsletter"""
    
    # In production, would integrate with email service
    return True, f'Successfully subscribed {email} to newsletter'

# =========================================================
# FAQ SYSTEM
# =========================================================

FAQ_CONTENT = {
    'en': [
        {
            'question': 'What is numerology?',
            'answer': 'Numerology is the study of numbers and their spiritual significance. It reveals your personality, destiny, and life path through numerical analysis.'
        },
        {
            'question': 'How long does it take to generate a report?',
            'answer': 'Digital reports are generated instantly after payment verification. Premium printed reports take 5-7 business days for delivery.'
        },
        {
            'question': 'What payment methods do you accept?',
            'answer': 'We accept UPI payments (PhonePe, Google Pay, Paytm, BHIM, Amazon Pay, and all banking apps). Complete the payment and provide UTR for verification.'
        },
        {
            'question': 'Is numerology accurate?',
            'answer': 'Numerology is a spiritual science that provides insights into your character and life path. Its effectiveness depends on your openness to the guidance provided.'
        },
        {
            'question': 'Can I change my name according to numerology?',
            'answer': 'Yes, changing your name to align with your destiny number can bring positive changes. However, this should be done with proper guidance.'
        }
    ],
    'hi': [
        {
            'question': 'अंकशास्त्र क्या है?',
            'answer': 'अंकशास्त्र संख्याओं का आध्यात्मिक अध्ययन है। यह आपके व्यक्तित्व, भाग्य और जीवन पथ को प्रकट करता है।'
        }
    ]
}

def get_faq(language='en'):
    """Get FAQ content"""
    
    return FAQ_CONTENT.get(language, FAQ_CONTENT['en'])

# =========================================================
# POLICIES & TERMS
# =========================================================

POLICIES = {
    'privacy': {
        'en': 'Your privacy is important to us. We never share your personal information with third parties.',
        'hi': 'आपकी गोपनीयता हमारे लिए महत्वपूर्ण है। हम आपकी व्यक्तिगत जानकारी कभी तीसरे पक्ष के साथ साझा नहीं करते।'
    },
    'refund': {
        'en': 'Digital reports are non-refundable after delivery. Refunds for printed reports are available within 7 days of delivery if damaged.',
        'hi': 'डिजिटल रिपोर्ट डिलीवरी के बाद वापसी के लिए पात्र नहीं हैं। क्षतिग्रस्त रिपोर्ट के लिए 7 दिन के भीतर वापसी उपलब्ध है।'
    },
    'terms': {
        'en': 'By using our services, you agree to our terms and conditions. All reports are for personal use only.',
        'hi': 'हमारी सेवाओं का उपयोग करके, आप हमारी शर्तों से सहमत हैं। सभी रिपोर्ट केवल व्यक्तिगत उपयोग के लिए हैं।'
    }
}

def get_policy(policy_type='privacy', language='en'):
    """Get policy content"""
    
    policy = POLICIES.get(policy_type, {})
    return policy.get(language, policy.get('en', ''))

# =========================================================
# LANGUAGE SUPPORT
# =========================================================

SUPPORTED_LANGUAGES = {
    'en': {
        'name': 'English',
        'flag': 'us',
        'native': 'English'
    },
    'hi': {
        'name': 'Hindi',
        'flag': 'in',
        'native': 'हिन्दी'
    },
    'as': {
        'name': 'Assamese',
        'flag': 'in',
        'native': 'অসমীয়া'
    }
}

def get_supported_languages():
    """Get list of supported languages"""
    
    return SUPPORTED_LANGUAGES

def set_user_language(user_id, language):
    """Set user preferred language"""
    
    user = User.query.get(user_id)
    if not user:
        return False
    
    if language not in SUPPORTED_LANGUAGES:
        return False
    
    user.language = language
    db.session.commit()
    
    return True

# =========================================================
# BLOG & ARTICLES
# =========================================================

BLOG_ARTICLES = {
    'en': [
        {
            'title': 'Understanding Your Birth Number',
            'slug': 'understanding-birth-number',
            'excerpt': 'Learn how your birth number defines your personality and natural abilities.',
            'content': 'Your birth number is calculated from your date of birth...',
            'author': 'Annand Sarma',
            'published': '2024-01-15'
        },
        {
            'title': 'Life Path Predictions for 2024',
            'slug': 'life-path-2024',
            'excerpt': 'Discover what numerology reveals about your year ahead.',
            'content': 'The year 2024 brings unique numerological energy...',
            'author': 'Annand Sarma',
            'published': '2024-01-10'
        }
    ]
}

def get_blog_articles(language='en', limit=10):
    """Get blog articles"""
    
    articles = BLOG_ARTICLES.get(language, BLOG_ARTICLES['en'])
    return articles[:limit]

def get_blog_article(slug, language='en'):
    """Get specific blog article"""
    
    articles = BLOG_ARTICLES.get(language, BLOG_ARTICLES['en'])
    
    for article in articles:
        if article['slug'] == slug:
            return article
    
    return None
