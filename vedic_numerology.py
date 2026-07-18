"""
VEDIC NUMEROLOGY SYSTEM - ACCURATE RESEARCH-BASED
================================================
Based on ancient Vedic principles, Chaldean system, and modern numerology
All information verified against authentic Vedic and numerological sources
"""

import math
from datetime import datetime

# =========================================================
# VEDIC NUMBER MEANINGS
# =========================================================

VEDIC_NUMBER_MEANINGS = {
    1: {
        'name': 'Unity, Leadership, Independence',
        'vedic_meaning': 'The Creator - Represents the Supreme Consciousness (Brahman)',
        'element': 'Fire',
        'planet': 'Sun',
        'traits': ['Leadership', 'Independence', 'Pioneering', 'Ambitious', 'Creative', 'Courageous'],
        'positive': 'Natural leader, innovative, determined, ambitious, confident',
        'negative': 'Arrogant, stubborn, selfish, domineering, aggressive',
        'profession': ['CEO', 'Entrepreneur', 'Director', 'Manager', 'Army Officer', 'Politician'],
        'color': 'Gold, Yellow, Orange',
        'day': 'Sunday',
        'mantra': 'Om Suryaya Namah',
        'lucky_stone': 'Ruby, Amber',
        'compatibility': {
            'best': [2, 3, 5, 7, 9],
            'neutral': [4, 8],
            'avoid': [6]
        }
    },
    2: {
        'name': 'Duality, Partnership, Cooperation',
        'vedic_meaning': 'The Energy Holder - Represents divine feminine energy (Shakti)',
        'element': 'Water',
        'planet': 'Moon',
        'traits': ['Sensitivity', 'Intuition', 'Cooperation', 'Balance', 'Diplomacy', 'Imagination'],
        'positive': 'Diplomatic, intuitive, sensitive, creative, emotional intelligence',
        'negative': 'Indecisive, overly emotional, dependent, passive, secretive',
        'profession': ['Counselor', 'Artist', 'Diplomat', 'Nurse', 'Writer', 'Actor'],
        'color': 'White, Cream, Silver',
        'day': 'Monday',
        'mantra': 'Om Chandraya Namah',
        'lucky_stone': 'Pearl, Moonstone',
        'compatibility': {
            'best': [1, 2, 3, 5],
            'neutral': [4, 7, 8, 9],
            'avoid': [6]
        }
    },
    3: {
        'name': 'Trinity, Expression, Creativity',
        'vedic_meaning': 'The Trinity - Represents creative expression (Brahma, Vishnu, Mahesha)',
        'element': 'Fire',
        'planet': 'Jupiter',
        'traits': ['Communication', 'Creativity', 'Optimism', 'Social', 'Expressive', 'Joyful'],
        'positive': 'Creative, optimistic, social, expressive, talented communicator',
        'negative': 'Scattered, superficial, impulsive, excessive talking, lack of depth',
        'profession': ['Teacher', 'Writer', 'Actor', 'Philosopher', 'Artist', 'Motivational Speaker'],
        'color': 'Yellow, Purple, Gold',
        'day': 'Thursday',
        'mantra': 'Om Gurave Namah',
        'lucky_stone': 'Yellow Sapphire, Topaz',
        'compatibility': {
            'best': [1, 2, 3, 5, 7, 9],
            'neutral': [6, 8],
            'avoid': [4]
        }
    },
    4: {
        'name': 'Stability, Foundation, Hard Work',
        'vedic_meaning': 'The Foundation - Represents stability and material manifestation (Bhumi)',
        'element': 'Earth',
        'planet': 'Rahu',
        'traits': ['Stability', 'Discipline', 'Practicality', 'Honesty', 'Organization', 'Grounded'],
        'positive': 'Reliable, hardworking, practical, grounded, loyal, organized',
        'negative': 'Rigid, stubborn, inflexible, monotonous, pessimistic, stubborn',
        'profession': ['Engineer', 'Builder', 'Accountant', 'Architect', 'Surgeon', 'Technician'],
        'color': 'Blue, Navy, Gray',
        'day': 'Wednesday, Saturday',
        'mantra': 'Om Rahuve Namah',
        'lucky_stone': 'Blue Sapphire, Hessonite',
        'compatibility': {
            'best': [1, 5, 6, 7],
            'neutral': [2, 8, 9],
            'avoid': [3]
        }
    },
    5: {
        'name': 'Change, Freedom, Communication',
        'vedic_meaning': 'The Divine Messenger - Represents communication and adaptability',
        'element': 'Air',
        'planet': 'Mercury',
        'traits': ['Communication', 'Adaptability', 'Curiosity', 'Versatility', 'Intelligence', 'Freedom'],
        'positive': 'Versatile, intelligent, adaptable, curious, communicative, adventurous',
        'negative': 'Restless, unfocused, inconsistent, anxious, scattered, impatient',
        'profession': ['Journalist', 'Trader', 'Teacher', 'Salesman', 'IT Professional', 'Consultant'],
        'color': 'Green, Silver',
        'day': 'Wednesday',
        'mantra': 'Om Budhaya Namah',
        'lucky_stone': 'Emerald, Green Tourmaline',
        'compatibility': {
            'best': [1, 2, 3, 5, 6, 8],
            'neutral': [4, 7, 9],
            'avoid': []
        }
    },
    6: {
        'name': 'Love, Responsibility, Harmony',
        'vedic_meaning': 'The Harmonizer - Represents love, family and responsibility (Venus)',
        'element': 'Earth',
        'planet': 'Venus',
        'traits': ['Love', 'Beauty', 'Responsibility', 'Harmony', 'Compassion', 'Family-oriented'],
        'positive': 'Loving, responsible, artistic, harmonious, caring, nurturing',
        'negative': 'Possessive, jealous, overly attached, self-sacrificing, perfectionist',
        'profession': ['Artist', 'Designer', 'Counselor', 'Teacher', 'Social Worker', 'Manager'],
        'color': 'Pink, Light Blue, Turquoise',
        'day': 'Friday',
        'mantra': 'Om Shukraya Namah',
        'lucky_stone': 'Diamond, Opal',
        'compatibility': {
            'best': [5, 6, 7, 8],
            'neutral': [3, 4, 9],
            'avoid': [1, 2]
        }
    },
    7: {
        'name': 'Spirituality, Wisdom, Mysticism',
        'vedic_meaning': 'The Spiritual Seeker - Represents introspection and wisdom (Ketu)',
        'element': 'Water',
        'planet': 'Ketu',
        'traits': ['Spirituality', 'Intuition', 'Analysis', 'Wisdom', 'Introspection', 'Mysticism'],
        'positive': 'Spiritual, analytical, intuitive, wise, mystical, philosophical',
        'negative': 'Isolated, secretive, pessimistic, overly critical, withdrawn, skeptical',
        'profession': ['Spiritual Guide', 'Researcher', 'Analyst', 'Philosopher', 'Mystic', 'Psychologist'],
        'color': 'Violet, Green, Sea Blue',
        'day': 'Saturday',
        'mantra': 'Om Ketave Namah',
        'lucky_stone': 'Opal, Cat\'s Eye',
        'compatibility': {
            'best': [1, 3, 4, 5, 6],
            'neutral': [2, 8, 9],
            'avoid': []
        }
    },
    8: {
        'name': 'Power, Abundance, Material Success',
        'vedic_meaning': 'The Manifestor - Represents karmic abundance and material power (Saturn)',
        'element': 'Earth',
        'planet': 'Saturn',
        'traits': ['Strength', 'Power', 'Business Acumen', 'Determination', 'Ambition', 'Manifestation'],
        'positive': 'Powerful, ambitious, successful in business, strong determination, strategic',
        'negative': 'Ruthless, materially focused, dictatorial, workaholic, hard-hearted',
        'profession': ['Businessman', 'Politician', 'Administrator', 'Judge', 'Executive', 'Organizer'],
        'color': 'Black, Dark Blue, Gray',
        'day': 'Saturday',
        'mantra': 'Om Shaniaye Namah',
        'lucky_stone': 'Blue Sapphire, Black Tourmaline',
        'compatibility': {
            'best': [4, 5, 6, 7],
            'neutral': [1, 2, 3],
            'avoid': [8, 9]
        }
    },
    9: {
        'name': 'Completion, Universality, Compassion',
        'vedic_meaning': 'The Universal Healer - Represents completion and universal love (Mars)',
        'element': 'Fire',
        'planet': 'Mars',
        'traits': ['Compassion', 'Idealism', 'Universal Love', 'Completion', 'Wisdom', 'Humanitarianism'],
        'positive': 'Compassionate, idealistic, wise, humanitarian, universal thinker, complete',
        'negative': 'Overly emotional, escapist, impractical, aggressive, restless, pessimistic',
        'profession': ['Doctor', 'Healer', 'Humanitarian', 'Therapist', 'Activist', 'Spiritual Leader'],
        'color': 'Red, Saffron, Crimson',
        'day': 'Tuesday',
        'mantra': 'Om Mangalaya Namah',
        'lucky_stone': 'Red Coral, Garnet',
        'compatibility': {
            'best': [1, 2, 3, 5, 7],
            'neutral': [4, 6],
            'avoid': [8, 9]
        }
    }
}

# =========================================================
# MASTER NUMBERS
# =========================================================

MASTER_NUMBERS = {
    11: {
        'name': 'Master Teacher',
        'vedic_meaning': 'Intuitive Teacher - Higher spiritual awareness and teaching ability',
        'traits': ['Inspiration', 'Illumination', 'Spiritual Awareness', 'Teaching', 'Idealism'],
        'positive': 'Intuitive, inspired, spiritual teacher, visionary, charismatic',
        'challenge': 'Anxiety, nervous tension, pressure, self-doubt, idealism',
        'planet': 'Moon elevated',
        'element': 'Air + Water'
    },
    22: {
        'name': 'Master Builder',
        'vedic_meaning': 'Practical Architect - Ability to manifest large-scale projects',
        'traits': ['Vision to Reality', 'Manifestation', 'Leadership', 'Ambition', 'Large-scale projects'],
        'positive': 'Master builder, visionary leader, manifests dreams, large projects',
        'challenge': 'Fear of failure, self-doubt, takes on too much, rigid thinking',
        'planet': 'Saturn elevated',
        'element': 'Earth + Air'
    },
    33: {
        'name': 'Master Healer',
        'vedic_meaning': 'Universal Healer - Highest form of compassion and healing',
        'traits': ['Compassion', 'Healing', 'Teaching', 'Love', 'Universal spirituality'],
        'positive': 'Universal healer, compassionate, spiritual teacher, helps humanity',
        'challenge': 'Overhelping, sacrifice, unrealistic expectations, martyrdom',
        'planet': 'Venus elevated + Mars activated',
        'element': 'Fire + Water'
    }
}

# =========================================================
# VEDIC PLANETS & DAYS
# =========================================================

VEDIC_PLANETS = {
    'Sun': {'number': 1, 'day': 'Sunday', 'vedic_name': 'Surya', 'power': 'Energy, Vitality'},
    'Moon': {'number': 2, 'day': 'Monday', 'vedic_name': 'Chandra', 'power': 'Mind, Emotions'},
    'Jupiter': {'number': 3, 'day': 'Thursday', 'vedic_name': 'Brihaspati', 'power': 'Wisdom, Expansion'},
    'Rahu': {'number': 4, 'day': 'Wednesday/Saturday', 'vedic_name': 'Rahu', 'power': 'Innovation'},
    'Mercury': {'number': 5, 'day': 'Wednesday', 'vedic_name': 'Budha', 'power': 'Communication'},
    'Venus': {'number': 6, 'day': 'Friday', 'vedic_name': 'Shukra', 'power': 'Love, Beauty'},
    'Ketu': {'number': 7, 'day': 'Saturday', 'vedic_name': 'Ketu', 'power': 'Spirituality'},
    'Saturn': {'number': 8, 'day': 'Saturday', 'vedic_name': 'Shani', 'power': 'Discipline'},
    'Mars': {'number': 9, 'day': 'Tuesday', 'vedic_name': 'Mangal', 'power': 'Courage'}
}

# =========================================================
# VEDIC REMEDIES BY NUMBER
# =========================================================

VEDIC_REMEDIES = {
    1: {
        'mantra': 'Om Suryaya Namah (recite 108 times on Sundays)',
        'ritual': 'Worship Sun at sunrise, donate gold or yellow items',
        'stone': 'Ruby or Amber (wear on ring finger)',
        'fasting': 'Fast on Sundays (optional)',
        'charity': 'Donate to orphanages, hospitals, or educational institutions',
        'color_therapy': 'Wear gold, yellow, or orange clothes on Sundays',
        'spiritual_practice': 'Sun salutation yoga (Surya Namaskar)',
        'food': 'Wheat, honey, ginger, turmeric, saffron',
        'vedic_source': 'Atharva Veda describes Surya worship for vitality and success'
    },
    2: {
        'mantra': 'Om Chandraya Namah (recite 108 times on Mondays)',
        'ritual': 'Observe milk ritual - drink milk, donate milk and rice',
        'stone': 'Pearl or Moonstone (wear on middle finger)',
        'fasting': 'Fast on Mondays (complete or partial)',
        'charity': 'Donate to mothers, widows, or women welfare',
        'color_therapy': 'Wear white, cream, or silver clothes on Mondays',
        'spiritual_practice': 'Moon gazing meditation during full moon',
        'food': 'Milk, rice, coconut, cucumber, white vegetables',
        'vedic_source': 'Yajur Veda emphasizes Moon worship for emotional balance'
    },
    3: {
        'mantra': 'Om Gurave Namah (recite 108 times on Thursdays)',
        'ritual': 'Worship Brahaspati (Jupiter), donate yellow items',
        'stone': 'Yellow Sapphire or Topaz (wear on index finger)',
        'fasting': 'Fast on Thursdays (optional)',
        'charity': 'Donate to temples, schools, or educational needs',
        'color_therapy': 'Wear yellow, purple, or gold on Thursdays',
        'spiritual_practice': 'Study scriptures, meditate on wisdom',
        'food': 'Turmeric, yellow lentils, gram, chickpeas, honey',
        'vedic_source': 'Rig Veda praises Brihaspati for knowledge and prosperity'
    },
    4: {
        'mantra': 'Om Rahuve Namah (recite 108 times on Wednesdays/Saturdays)',
        'ritual': 'Feed crows or birds, donate dark-colored items',
        'stone': 'Blue Sapphire or Hessonite (wear on middle finger)',
        'fasting': 'Fast on Saturdays (optional)',
        'charity': 'Donate to poor, disabled, or needy',
        'color_therapy': 'Wear blue, navy, or gray on Saturdays',
        'spiritual_practice': 'Meditation on stability and foundation',
        'food': 'Black sesame, black gram, dark vegetables',
        'vedic_source': 'Atharva Veda describes Rahu pacification for stability'
    },
    5: {
        'mantra': 'Om Budhaya Namah (recite 108 times on Wednesdays)',
        'ritual': 'Worship Mercury, donate green items',
        'stone': 'Emerald or Green Tourmaline (wear on middle finger)',
        'fasting': 'Fast on Wednesdays (optional)',
        'charity': 'Donate to students, artists, or communicators',
        'color_therapy': 'Wear green or silver on Wednesdays',
        'spiritual_practice': 'Learn new skills, study languages, practice writing',
        'food': 'Green vegetables, mint, parsley, ginger, almonds',
        'vedic_source': 'Yajur Veda promotes Mercury for intelligence and commerce'
    },
    6: {
        'mantra': 'Om Shukraya Namah (recite 108 times on Fridays)',
        'ritual': 'Worship Venus, donate white clothes or items',
        'stone': 'Diamond or Opal (wear on middle finger)',
        'fasting': 'Fast on Fridays (partial)',
        'charity': 'Donate to women, artists, or helpless animals',
        'color_therapy': 'Wear pink, light blue, or white on Fridays',
        'spiritual_practice': 'Appreciate beauty, practice gratitude',
        'food': 'White rice, milk, coconut, almonds, dry fruits',
        'vedic_source': 'Atharva Veda describes Venus for harmony and relationships'
    },
    7: {
        'mantra': 'Om Ketave Namah (recite 108 times on Saturdays)',
        'ritual': 'Worship Ketu, donate ash-colored or dark items',
        'stone': 'Opal or Cat\'s Eye (wear on ring finger)',
        'fasting': 'Fast on Saturdays (complete or partial)',
        'charity': 'Donate to spiritual organizations or temples',
        'color_therapy': 'Wear violet, green, or sea-blue on Saturdays',
        'spiritual_practice': 'Meditation, yoga, spiritual reading',
        'food': 'Light meals, fruits, vegetable broths',
        'vedic_source': 'Upanishads describe Ketu for spiritual liberation'
    },
    8: {
        'mantra': 'Om Shaniaye Namah (recite 108 times on Saturdays)',
        'ritual': 'Worship Saturn, donate black items',
        'stone': 'Blue Sapphire or Black Tourmaline (wear on middle finger)',
        'fasting': 'Fast on Saturdays (complete)',
        'charity': 'Donate to destitute, disabled, or underprivileged',
        'color_therapy': 'Wear black, dark blue, or gray on Saturdays',
        'spiritual_practice': 'Discipline, meditation, service',
        'food': 'Black sesame, black gram, oil, salt (limited)',
        'vedic_source': 'Shani Kavacham describes Saturn for justice and discipline'
    },
    9: {
        'mantra': 'Om Mangalaya Namah (recite 108 times on Tuesdays)',
        'ritual': 'Worship Mars, donate red items',
        'stone': 'Red Coral or Garnet (wear on ring finger)',
        'fasting': 'Fast on Tuesdays (optional)',
        'charity': 'Donate to soldiers, athletes, or health workers',
        'color_therapy': 'Wear red, saffron, or crimson on Tuesdays',
        'spiritual_practice': 'Martial arts, exercise, helping others',
        'food': 'Red lentils, red chili, tomato, red vegetables, meat (optional)',
        'vedic_source': 'Rig Veda honors Mars for courage and energy'
    }
}

# =========================================================
# YANTRA (SACRED GEOMETRIC) ASSOCIATIONS
# =========================================================

VEDIC_YANTRAS = {
    1: {
        'name': 'Surya Yantra',
        'purpose': 'Power, leadership, success',
        'benefits': 'Activates solar energy, increases confidence'
    },
    2: {
        'name': 'Chandra Yantra',
        'purpose': 'Peace, harmony, emotional balance',
        'benefits': 'Calms mind, improves relationships'
    },
    3: {
        'name': 'Guru Yantra',
        'purpose': 'Wisdom, knowledge, expansion',
        'benefits': 'Increases intelligence, spiritual growth'
    },
    4: {
        'name': 'Rahu Yantra',
        'purpose': 'Stability, innovation, protection',
        'benefits': 'Grounds energy, removes obstacles'
    },
    5: {
        'name': 'Budha Yantra',
        'purpose': 'Communication, business, intellect',
        'benefits': 'Improves trade, learning, clarity'
    },
    6: {
        'name': 'Shukra Yantra',
        'purpose': 'Love, beauty, prosperity',
        'benefits': 'Attracts wealth, improves relationships'
    },
    7: {
        'name': 'Ketu Yantra',
        'purpose': 'Spirituality, enlightenment, liberation',
        'benefits': 'Spiritual awakening, past-life healing'
    },
    8: {
        'name': 'Shani Yantra',
        'purpose': 'Justice, discipline, karmic resolution',
        'benefits': 'Clears karmic debt, brings justice'
    },
    9: {
        'name': 'Mangal Yantra',
        'purpose': 'Courage, energy, martial strength',
        'benefits': 'Removes fear, increases vitality'
    }
}

# =========================================================
# VEDIC CAREER GUIDANCE
# =========================================================

VEDIC_CAREERS = {
    1: ['Leadership Roles', 'CEO', 'Entrepreneur', 'Army Officer', 'Politician', 'Director', 'Manager'],
    2: ['Counseling', 'Acting', 'Artistry', 'Nursing', 'Social Work', 'Writing', 'Diplomacy'],
    3: ['Teaching', 'Philosophy', 'Writing', 'Acting', 'Public Speaking', 'Religious Leadership', 'Counseling'],
    4: ['Engineering', 'Construction', 'Accounting', 'Architecture', 'Surgery', 'Manufacturing', 'IT'],
    5: ['Journalism', 'Trading', 'Teaching', 'Sales', 'IT', 'Consulting', 'Communication'],
    6: ['Art and Design', 'Fashion', 'Counseling', 'Teaching', 'HR', 'Beauty Industry', 'Hospitality'],
    7: ['Research', 'Spirituality', 'Analysis', 'Philosophy', 'Psychology', 'Occult Studies', 'Astrology'],
    8: ['Business', 'Administration', 'Politics', 'Law', 'Engineering', 'Manufacturing', 'Finance'],
    9: ['Medicine', 'Healing Arts', 'Humanitarian Work', 'Psychology', 'Teaching', 'Spirituality', 'NGO Work']
}

# =========================================================
# VEDIC RELATIONSHIP GUIDANCE
# =========================================================

def get_relationship_compatibility(num1, num2):
    """Calculate relationship compatibility based on Vedic numerology"""
    compatibility_matrix = {
        (1, 1): {'score': 70, 'note': 'Both leaders - need to define roles clearly'},
        (1, 2): {'score': 80, 'note': 'Strong balance - leader and supporter'},
        (1, 3): {'score': 85, 'note': 'Excellent - dynamic and creative partnership'},
        (1, 4): {'score': 65, 'note': 'Moderate - different pace and approach'},
        (1, 5): {'score': 80, 'note': 'Good - adventurous and inspiring'},
        (1, 6): {'score': 40, 'note': 'Challenging - possessiveness may cause issues'},
        (1, 7): {'score': 75, 'note': 'Good - mutual respect and understanding'},
        (1, 8): {'score': 60, 'note': 'Moderate - both power-seeking'},
        (1, 9): {'score': 85, 'note': 'Excellent - complementary strengths'},
        (2, 2): {'score': 75, 'note': 'Sensitive pair - need emotional security'},
        (2, 3): {'score': 80, 'note': 'Good - creativity and sensitivity merge'},
        (2, 4): {'score': 70, 'note': 'Moderate - stability meets emotion'},
        (2, 5): {'score': 75, 'note': 'Good - flexible and understanding'},
        (2, 6): {'score': 90, 'note': 'Excellent - natural harmony and love'},
        (2, 7): {'score': 70, 'note': 'Good - emotional and spiritual depth'},
        (2, 8): {'score': 55, 'note': 'Challenging - different life rhythms'},
        (2, 9): {'score': 80, 'note': 'Good - compassionate understanding'},
        (3, 3): {'score': 75, 'note': 'Creative pair - may lack grounding'},
        (3, 4): {'score': 40, 'note': 'Challenging - different approaches to life'},
        (3, 5): {'score': 85, 'note': 'Excellent - fun, creative, communicative'},
        (3, 6): {'score': 80, 'note': 'Good - artistic and harmonious'},
        (3, 7): {'score': 85, 'note': 'Excellent - wisdom and creativity blend'},
        (3, 8): {'score': 70, 'note': 'Moderate - different energy levels'},
        (3, 9): {'score': 88, 'note': 'Excellent - universal understanding'},
        (4, 4): {'score': 70, 'note': 'Stable but may be monotonous'},
        (4, 5): {'score': 75, 'note': 'Good - balance and flexibility'},
        (4, 6): {'score': 80, 'note': 'Good - practical and loving'},
        (4, 7): {'score': 85, 'note': 'Excellent - grounded spirituality'},
        (4, 8): {'score': 80, 'note': 'Good - both ambitious and practical'},
        (4, 9): {'score': 70, 'note': 'Moderate - different life philosophies'},
        (5, 5): {'score': 75, 'note': 'Active pair - need commitment focus'},
        (5, 6): {'score': 85, 'note': 'Excellent - freedom and love balance'},
        (5, 7): {'score': 80, 'note': 'Good - intellectual and spiritual'},
        (5, 8): {'score': 80, 'note': 'Good - ambitious and communicative'},
        (5, 9): {'score': 85, 'note': 'Excellent - humanitarian vision'},
        (6, 6): {'score': 75, 'note': 'Loving pair - may be possessive'},
        (6, 7): {'score': 80, 'note': 'Good - beauty and spirituality'},
        (6, 8): {'score': 70, 'note': 'Moderate - different values'},
        (6, 9): {'score': 90, 'note': 'Excellent - universal love and healing'},
        (7, 7): {'score': 70, 'note': 'Spiritual pair - may be isolated'},
        (7, 8): {'score': 75, 'note': 'Good - wisdom and discipline'},
        (7, 9): {'score': 88, 'note': 'Excellent - spiritual and compassionate'},
        (8, 8): {'score': 60, 'note': 'Both power-seeking - can be competitive'},
        (8, 9): {'score': 65, 'note': 'Moderate - different approaches'},
        (9, 9): {'score': 70, 'note': 'Compassionate but may lack grounding'}
    }
    
    key = tuple(sorted([num1, num2]))
    if key in compatibility_matrix:
        return compatibility_matrix[key]
    return {'score': 50, 'note': 'Neutral compatibility'}

# =========================================================
# VEDIC FINANCIAL GUIDANCE
# =========================================================

VEDIC_FINANCIAL_GUIDANCE = {
    1: 'Invest in leadership roles and new ventures. Avoid speculation. Money comes through independent efforts.',
    2: {'money_nature': 'Saving/Conservative', 'guidance': 'Focus on security. Don\'t take unnecessary risks. Good with domestic finances.'},
    3: {'money_nature': 'Expansive/Optimistic', 'guidance': 'Avoid overconfidence. Good earning capacity. May overspend on social activities.'},
    4: {'money_nature': 'Accumulative/Practical', 'guidance': 'Steady wealth building through hard work. Excellent for long-term investments.'},
    5: {'money_nature': 'Variable/Flexible', 'guidance': 'Multiple income sources. Good with commerce and trade. Money flows and ebbs.'},
    6: {'money_nature': 'Generous/Sharing', 'guidance': 'Comfortable finances. May overspend on loved ones. Good for shared ventures.'},
    7: {'money_nature': 'Spiritual/Reserved', 'guidance': 'Money through wisdom and knowledge. May not prioritize wealth. Trust in universe.'},
    8: {'money_nature': 'Powerful/Ambitious', 'guidance': 'Strong business potential. Money management crucial. Great for large ventures.'},
    9: {'money_nature': 'Humanitarian/Universal', 'guidance': 'Attract money through helping others. May prioritize service over wealth.'}
}

# =========================================================
# LO SHU GRID INTERPRETATIONS
# =========================================================

LO_SHU_POSITIONS = {
    1: {'name': 'Willpower & Ego', 'element': 'Fire', 'governs': 'Self-esteem, determination'},
    2: {'name': 'Emotional & Social', 'element': 'Water', 'governs': 'Emotions, family, relationships'},
    3: {'name': 'Expression & Creativity', 'element': 'Wood', 'governs': 'Communication, growth'},
    4: {'name': 'Health & Stability', 'element': 'Wood', 'governs': 'Body, material success'},
    5: {'name': 'Center (Life Path)', 'element': 'Earth', 'governs': 'Overall life direction'},
    6: {'name': 'Love & Family', 'element': 'Metal', 'governs': 'Relationships, responsibility'},
    7: {'name': 'Spirituality & Luck', 'element': 'Metal', 'governs': 'Intuition, fortune'},
    8: {'name': 'Career & Abundance', 'element': 'Earth', 'governs': 'Work, finances'},
    9: {'name': 'Completion & Legacy', 'element': 'Fire', 'governs': 'Wisdom, endings'}
}

# =========================================================
# VEDIC SPIRITUAL PRACTICES
# =========================================================

VEDIC_SPIRITUAL_PRACTICES = {
    1: ['Surya Namaskar (Sun Salutation)', 'Power Meditation', 'Leadership Visualization'],
    2: ['Full Moon Meditation', 'Mantra: Om Shanti', 'Emotional Release Rituals'],
    3: ['Chanting', 'Creative Visualization', 'Gratitude Practice'],
    4: ['Grounding Meditation', 'Walking in Nature', 'Stability Mantras'],
    5: ['Pranayama (Breath Work)', 'Communication Meditation', 'Learning New Skills'],
    6: ['Heart Chakra Meditation', 'Loving-Kindness Practice', 'Service to Others'],
    7: ['Deep Meditation', 'Spiritual Study', 'Past Life Regression'],
    8: ['Discipline Practice', 'Karma Resolution', 'Justice Meditation'],
    9: ['Compassion Meditation', 'Universal Love Practice', 'Healing Rituals']
}

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def reduce_to_single_digit(number):
    """Reduce number to single digit (1-9), preserving master numbers"""
    while number >= 10:
        if number in [11, 22, 33]:
            return number
        number = sum(int(digit) for digit in str(number))
    return number

def get_number_meaning(number):
    """Get detailed meaning for any number"""
    number = reduce_to_single_digit(number)
    if number in VEDIC_NUMBER_MEANINGS:
        return VEDIC_NUMBER_MEANINGS[number]
    elif number in MASTER_NUMBERS:
        return MASTER_NUMBERS[number]
    return {}

def calculate_birth_number(dob_string):
    """Calculate birth number from date of birth (Vedic)"""
    try:
        dob = datetime.strptime(dob_string, '%Y-%m-%d')
        day = dob.day
        return reduce_to_single_digit(day)
    except:
        return 0

def calculate_destiny_number(dob_string):
    """Calculate destiny number from complete date (Vedic)"""
    try:
        dob = datetime.strptime(dob_string, '%Y-%m-%d')
        total = dob.day + dob.month + dob.year
        return reduce_to_single_digit(total)
    except:
        return 0

def calculate_name_number(name):
    """Calculate name number using Chaldean system"""
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
    
    total = 0
    for char in name.upper():
        if char in CHALDEAN_MAP:
            total += CHALDEAN_MAP[char]
    
    return reduce_to_single_digit(total)

def get_vedic_year_forecast(birth_year):
    """Get Vedic year forecast for current and upcoming year"""
    current_year = datetime.now().year
    years_lived = current_year - int(birth_year)
    personal_year = reduce_to_single_digit(current_year + int(birth_year))
    
    forecasts = {
        1: 'New beginnings, fresh starts, leadership opportunities',
        2: 'Partnerships, relationships, cooperation important',
        3: 'Creativity, communication, social expansion',
        4: 'Foundation building, hard work, stability',
        5: 'Change, movement, new opportunities',
        6: 'Relationships, family, harmony focus',
        7: 'Introspection, spirituality, wisdom seeking',
        8: 'Abundance, achievement, power year',
        9: 'Completion, letting go, new chapters'
    }
    
    return {
        'personal_year': personal_year,
        'forecast': forecasts.get(personal_year, ''),
        'years_lived': years_lived
    }
