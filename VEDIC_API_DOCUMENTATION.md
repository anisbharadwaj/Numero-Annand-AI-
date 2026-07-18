# 🔮 VEDIC NUMEROLOGY API DOCUMENTATION
## Numero Annand AI - Complete Research-Based API Reference

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [API Endpoints](#api-endpoints)
4. [Number Meanings](#number-meanings)
5. [Vedic Remedies](#vedic-remedies)
6. [Examples](#examples)
7. [Error Handling](#error-handling)

---

## OVERVIEW

The Vedic Numerology API provides comprehensive, research-based numerological analysis using ancient Vedic principles combined with modern numerological science.

**Base URL:** `http://localhost:8501/api`

**All responses are in JSON format**

---

## CORE CONCEPTS

### VEDIC NUMBER SYSTEM

Numbers 1-9 represent fundamental cosmic energies:

| Number | Name | Vedic Meaning | Planet | Element |
|--------|------|---------------|--------|---------|
| 1 | Unity | The Creator (Brahman) | Sun | Fire |
| 2 | Duality | Divine Feminine Energy (Shakti) | Moon | Water |
| 3 | Trinity | Creative Expression | Jupiter | Fire |
| 4 | Stability | Foundation & Material Manifestation | Rahu | Earth |
| 5 | Change | Divine Messenger | Mercury | Air |
| 6 | Love | Harmonizer (Venus) | Venus | Earth |
| 7 | Spirituality | Spiritual Seeker (Ketu) | Ketu | Water |
| 8 | Power | Manifestor (Saturn) | Saturn | Earth |
| 9 | Completion | Universal Healer (Mars) | Mars | Fire |

### MASTER NUMBERS

Special double-digit numbers with elevated spiritual significance:

- **11** (Master Teacher): Intuitive awareness, spiritual teaching
- **22** (Master Builder): Vision manifesting to reality
- **33** (Master Healer): Universal compassion and healing

### THREE CORE NUMBERS

1. **Birth Number**: Calculated from day of birth (your natural talent)
2. **Destiny Number**: Total of full date (your life purpose)
3. **Name Number**: Letters in your name (your expression)

---

## API ENDPOINTS

### 1. FULL VEDIC ANALYSIS

**Endpoint:** `POST /vedic/full-analysis`

**Description:** Get complete Vedic numerology blueprint including all numbers, meanings, remedies, careers, and spiritual practices.

**Request:**
```json
{
  "name": "Annand Sarma",
  "dob": "1985-03-15",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "name": "Annand Sarma",
    "dob": "1985-03-15",
    "numbers": {
      "birth_number": {
        "number": 6,
        "meaning": { ... },
        "remedies": { ... },
        "careers": [...],
        "finance": { ... },
        "practices": [...]
      },
      "destiny_number": { ... },
      "name_number": { ... }
    },
    "yearly_forecast": { ... },
    "vedic_planets": { ... }
  }
}
```

---

### 2. RELATIONSHIP COMPATIBILITY

**Endpoint:** `POST /vedic/relationship-compatibility`

**Description:** Calculate compatibility between two people using their numerological profiles.

**Request:**
```json
{
  "name1": "Person A",
  "dob1": "1990-01-20",
  "name2": "Person B",
  "dob2": "1992-06-15"
}
```

**Response:**
```json
{
  "success": true,
  "compatibility": {
    "person1": {
      "name": "Person A",
      "birth": 2,
      "destiny": 5,
      "name_num": 3
    },
    "person2": {
      "name": "Person B",
      "birth": 7,
      "destiny": 4,
      "name_num": 8
    },
    "birth_compatibility": {
      "score": 75,
      "note": "Good compatibility note"
    },
    "destiny_compatibility": { ... },
    "name_compatibility": { ... },
    "overall_score": 73,
    "interpretation": "Good match"
  }
}
```

**Compatibility Scores:**
- 80-100: Excellent match
- 60-79: Good match
- 40-59: Moderate match
- Below 40: Challenging match

---

### 3. NUMBER MEANINGS

**Endpoint:** `GET /vedic/number-meanings/<number>`

**Description:** Get detailed Vedic meaning for a specific number (1-9 or master numbers).

**Example:** `/vedic/number-meanings/5`

**Response:**
```json
{
  "success": true,
  "number": 5,
  "meaning": {
    "name": "Change, Freedom, Communication",
    "vedic_meaning": "The Divine Messenger - Represents communication and adaptability",
    "element": "Air",
    "planet": "Mercury",
    "traits": ["Communication", "Adaptability", "Curiosity", ...],
    "positive": "Versatile, intelligent, adaptable, curious, communicative",
    "negative": "Restless, unfocused, inconsistent, anxious",
    "profession": ["Journalist", "Trader", "Teacher", ...],
    "color": "Green, Silver",
    "day": "Wednesday",
    "mantra": "Om Budhaya Namah",
    "lucky_stone": "Emerald, Green Tourmaline",
    "compatibility": { ... }
  },
  "remedies": { ... },
  "careers": [...],
  "yantra": { ... },
  "financial_guidance": { ... },
  "spiritual_practices": [...]
}
```

---

### 4. LUCKY ELEMENTS

**Endpoint:** `GET /vedic/lucky-elements/<number>`

**Description:** Get lucky colors, stones, days, and elements for a number.

**Example:** `/vedic/lucky-elements/3`

**Response:**
```json
{
  "success": true,
  "number": 3,
  "lucky_elements": {
    "color": "Yellow, Purple, Gold",
    "day": "Thursday",
    "stone": "Yellow Sapphire, Topaz",
    "mantra": "Om Gurave Namah",
    "element": "Fire",
    "yantra": {
      "name": "Guru Yantra",
      "purpose": "Wisdom, knowledge, expansion",
      "benefits": "Increases intelligence, spiritual growth"
    },
    "planet_name": "Jupiter",
    "positive_traits": ["Communication", "Creativity", "Optimism", ...],
    "professions": ["Teacher", "Writer", "Actor", ...]
  }
}
```

---

### 5. LIFE PATH & DESTINY

**Endpoint:** `POST /vedic/life-path`

**Description:** Get complete life path guidance based on destiny number.

**Request:**
```json
{
  "name": "Annand Sarma",
  "dob": "1985-03-15"
}
```

**Response:**
```json
{
  "success": true,
  "life_path": {
    "destiny_number": 5,
    "birth_number": 6,
    "name_number": 3,
    "life_purpose": "The Divine Messenger - Represents communication and adaptability",
    "key_traits": ["Communication", "Adaptability", ...],
    "career_path": ["Journalist", "Trader", "Teacher", ...],
    "challenges": "Main challenge is to balance [negatives] and embrace [positives]",
    "life_lessons": "Learn to embody the highest expression of Change, Freedom, Communication",
    "success_factors": [
      "Follow your Change, Freedom, Communication nature",
      "Embrace the energy of Mercury",
      "Practice the mantra: Om Budhaya Namah",
      "Use color therapy with Green, Silver"
    ]
  }
}
```

---

### 6. VEDIC REMEDIES & RITUALS

**Endpoint:** `GET /vedic/remedies/<number>`

**Description:** Get specific Vedic remedies and rituals for a number.

**Example:** `/vedic/remedies/7`

**Response:**
```json
{
  "success": true,
  "number": 7,
  "remedies": {
    "mantra": "Om Ketave Namah (recite 108 times on Saturdays)",
    "ritual": "Worship Ketu, donate ash-colored or dark items",
    "stone": "Opal or Cat's Eye (wear on ring finger)",
    "fasting": "Fast on Saturdays (complete or partial)",
    "charity": "Donate to spiritual organizations or temples",
    "color_therapy": "Wear violet, green, or sea-blue on Saturdays",
    "spiritual_practice": "Meditation, yoga, spiritual reading",
    "food": "Light meals, fruits, vegetable broths",
    "vedic_source": "Upanishads describe Ketu for spiritual liberation"
  },
  "note": "These remedies are based on ancient Vedic principles. Consistency and faith are key to effectiveness."
}
```

---

### 7. SPIRITUAL PRACTICES

**Endpoint:** `GET /vedic/spiritual-practices/<number>`

**Description:** Get spiritual practices recommended for a number.

**Example:** `/vedic/spiritual-practices/9`

**Response:**
```json
{
  "success": true,
  "number": 9,
  "practices": [
    "Medicine",
    "Healing Arts",
    "Humanitarian Work",
    "Psychology",
    "Teaching",
    "Spirituality",
    "NGO Work"
  ],
  "mantra": "Om Mangalaya Namah",
  "description": "Spiritual practices for Completion, Universality, Compassion energy"
}
```

---

## NUMBER MEANINGS (DETAILED)

### NUMBER 1 - Unity, Leadership, Independence
- **Vedic Name:** Surya (Sun)
- **Life Purpose:** Leadership, innovation, pioneering
- **Positive Traits:** Confident, ambitious, creative, determined
- **Challenges:** Arrogant, stubborn, domineering
- **Best Careers:** CEO, Entrepreneur, Director, Army Officer, Politician
- **Lucky Color:** Gold, Yellow, Orange
- **Lucky Stone:** Ruby, Amber
- **Mantra:** Om Suryaya Namah
- **Friendly Numbers:** 2, 3, 5, 7, 9
- **Enemy Numbers:** 6
- **Neutral Numbers:** 4, 8

### NUMBER 2 - Duality, Partnership, Cooperation
- **Vedic Name:** Chandra (Moon)
- **Life Purpose:** Diplomacy, support, balance
- **Positive Traits:** Intuitive, sensitive, diplomatic, cooperative
- **Challenges:** Indecisive, overly emotional, dependent
- **Best Careers:** Counselor, Artist, Diplomat, Nurse, Writer, Actor
- **Lucky Color:** White, Cream, Silver
- **Lucky Stone:** Pearl, Moonstone
- **Mantra:** Om Chandraya Namah
- **Friendly Numbers:** 1, 2, 3, 5
- **Enemy Numbers:** 6
- **Neutral Numbers:** 4, 7, 8, 9

### NUMBER 3 - Trinity, Expression, Creativity
- **Vedic Name:** Brihaspati (Jupiter)
- **Life Purpose:** Creative expression, teaching, communication
- **Positive Traits:** Creative, optimistic, social, expressive
- **Challenges:** Scattered, superficial, impulsive
- **Best Careers:** Teacher, Writer, Actor, Philosopher, Artist
- **Lucky Color:** Yellow, Purple, Gold
- **Lucky Stone:** Yellow Sapphire, Topaz
- **Mantra:** Om Gurave Namah
- **Friendly Numbers:** 1, 2, 3, 5, 7, 9
- **Enemy Numbers:** 4
- **Neutral Numbers:** 6, 8

### NUMBER 4 - Stability, Foundation, Hard Work
- **Vedic Name:** Rahu
- **Life Purpose:** Building foundations, stable progress
- **Positive Traits:** Reliable, hardworking, practical, loyal
- **Challenges:** Rigid, stubborn, inflexible
- **Best Careers:** Engineer, Builder, Accountant, Architect, Technician
- **Lucky Color:** Blue, Navy, Gray
- **Lucky Stone:** Blue Sapphire, Hessonite
- **Mantra:** Om Rahuve Namah
- **Friendly Numbers:** 1, 5, 6, 7
- **Enemy Numbers:** 3
- **Neutral Numbers:** 2, 8, 9

### NUMBER 5 - Change, Freedom, Communication
- **Vedic Name:** Budha (Mercury)
- **Life Purpose:** Communication, versatility, adaptability
- **Positive Traits:** Intelligent, versatile, curious, communicative
- **Challenges:** Restless, unfocused, anxious
- **Best Careers:** Journalist, Trader, Teacher, Salesman, IT Professional
- **Lucky Color:** Green, Silver
- **Lucky Stone:** Emerald, Green Tourmaline
- **Mantra:** Om Budhaya Namah
- **Friendly Numbers:** 1, 2, 3, 5, 6, 8
- **Enemy Numbers:** None
- **Neutral Numbers:** 4, 7, 9

### NUMBER 6 - Love, Responsibility, Harmony
- **Vedic Name:** Shukra (Venus)
- **Life Purpose:** Love, family, harmony, responsibility
- **Positive Traits:** Loving, artistic, caring, nurturing
- **Challenges:** Possessive, jealous, overly attached
- **Best Careers:** Artist, Designer, Counselor, Social Worker, Manager
- **Lucky Color:** Pink, Light Blue, Turquoise
- **Lucky Stone:** Diamond, Opal
- **Mantra:** Om Shukraya Namah
- **Friendly Numbers:** 5, 6, 7, 8
- **Enemy Numbers:** 1, 2
- **Neutral Numbers:** 3, 4, 9

### NUMBER 7 - Spirituality, Wisdom, Mysticism
- **Vedic Name:** Ketu
- **Life Purpose:** Spiritual development, introspection, wisdom
- **Positive Traits:** Spiritual, analytical, intuitive, philosophical
- **Challenges:** Isolated, pessimistic, withdrawn
- **Best Careers:** Spiritual Guide, Researcher, Analyst, Philosopher, Mystic
- **Lucky Color:** Violet, Green, Sea Blue
- **Lucky Stone:** Opal, Cat's Eye
- **Mantra:** Om Ketave Namah
- **Friendly Numbers:** 1, 3, 4, 5, 6
- **Enemy Numbers:** None
- **Neutral Numbers:** 2, 8, 9

### NUMBER 8 - Power, Abundance, Material Success
- **Vedic Name:** Shani (Saturn)
- **Life Purpose:** Manifestation, power, material success
- **Positive Traits:** Powerful, ambitious, strategic, strong determination
- **Challenges:** Ruthless, workaholic, materialistic
- **Best Careers:** Businessman, Politician, Administrator, Judge, Executive
- **Lucky Color:** Black, Dark Blue, Gray
- **Lucky Stone:** Blue Sapphire, Black Tourmaline
- **Mantra:** Om Shaniaye Namah
- **Friendly Numbers:** 4, 5, 6, 7
- **Enemy Numbers:** 8, 9
- **Neutral Numbers:** 1, 2, 3

### NUMBER 9 - Completion, Universality, Compassion
- **Vedic Name:** Mangal (Mars)
- **Life Purpose:** Healing, humanitarian work, completion
- **Positive Traits:** Compassionate, idealistic, wise, humanitarian
- **Challenges:** Overly emotional, escapist, impractical
- **Best Careers:** Doctor, Healer, Humanitarian, Therapist, Spiritual Leader
- **Lucky Color:** Red, Saffron, Crimson
- **Lucky Stone:** Red Coral, Garnet
- **Mantra:** Om Mangalaya Namah
- **Friendly Numbers:** 1, 2, 3, 5, 7
- **Enemy Numbers:** 8, 9
- **Neutral Numbers:** 4, 6

---

## VEDIC REMEDIES

Each number has specific remedies based on Vedic principles:

### Remedy Components:
1. **Mantra:** Sacred words to recite (usually 108 times)
2. **Ritual:** Actions to perform for energy alignment
3. **Stone:** Crystal to wear for energy enhancement
4. **Fasting:** Day to fast for spiritual cleansing
5. **Charity:** Giving to specific categories for karmic balance
6. **Color Therapy:** Wearing specific colors to absorb frequency
7. **Spiritual Practice:** Daily practices for personal evolution
8. **Food:** Recommended dietary items to support the frequency
9. **Vedic Source:** References from ancient Vedic texts

---

## EXAMPLES

### Example 1: Get Full Analysis for Annand Sarma

```bash
curl -X POST http://localhost:8501/api/vedic/full-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Annand Sarma",
    "dob": "1985-03-15",
    "language": "en"
  }'
```

**Result will include:**
- Birth Number: 6 (Love, Responsibility)
- Destiny Number: 5 (Change, Freedom)
- Name Number: 3 (Expression, Creativity)
- All remedies, careers, compatibility info

### Example 2: Check Relationship Compatibility

```bash
curl -X POST http://localhost:8501/api/vedic/relationship-compatibility \
  -H "Content-Type: application/json" \
  -d '{
    "name1": "Person A",
    "dob1": "1990-01-15",
    "name2": "Person B",
    "dob2": "1995-06-20"
  }'
```

### Example 3: Get Number Remedies

```bash
curl http://localhost:8501/api/vedic/remedies/5
```

---

## ERROR HANDLING

### Common Errors:

**400 - Bad Request:**
```json
{
  "error": "Name and date of birth required"
}
```

**404 - Not Found:**
```json
{
  "error": "Number not found"
}
```

**400 - Invalid Format:**
```json
{
  "error": "Analysis failed: Invalid date format"
}
```

### Date Format:
- Always use ISO format: `YYYY-MM-DD`
- Example: `1985-03-15`

---

## IMPORTANT NOTES

1. **All calculations are based on verified Vedic and Chaldean numerology principles**
2. **No false information is provided - all data comes from authentic sources**
3. **Remedies should be practiced consistently for best results**
4. **The API is free to use and open to all**
5. **Results are for guidance and personal development purposes**

---

## SUPPORT & CONTACT

For issues, questions, or integration help:
- Email: support@numeroanandai.com
- WhatsApp: +91 7099805039
- Website: www.numeroanandai.com

---

**Last Updated:** July 2024
**Version:** 2.0
**Status:** Production Ready ✅
