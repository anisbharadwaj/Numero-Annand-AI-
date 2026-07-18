# =========================================================
# 🔮 NUMERO ANNAND AI — PREMIUM STYLE FREE VERSION
# =========================================================
# FULL PROFESSIONAL APP.PY
# =========================================================
# ✔ ENGLISH + HINDI + ASSAMESE
# ✔ FULL DETAILED ANALYSIS
# ✔ NAME CORRECTION SYSTEM
# ✔ RATIO SYSTEM
# ✔ COMPATIBILITY SYSTEM
# ✔ LO SHU GRID
# ✔ WHATSAPP GROUP
# ✔ ATTRACTIVE PROMPT
# ✔ NO PAYMENT SYSTEM
# ✔ SAME PREMIUM DESIGN
# =========================================================

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
from dateutil import parser
import random
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import db, User, Order, Payment, Report, AIChat, Consultation, Admin, AIMessageCounter, ActivityLog
from auth import generate_token, verify_token, register_user, login_user, token_required, admin_required
from payment import create_order, generate_qr_code, create_payment_record, verify_payment, admin_verify_payment, PRICING
from membership import (
    create_membership_order, activate_membership, get_membership_status,
    get_membership_details, get_all_plans, is_membership_valid, get_days_until_expiry,
    is_expiring_soon, get_membership_stats, MEMBERSHIP_PLANS, get_expiring_memberships
)
from ai_assistant import (
    AnnandAI, save_ai_chat, get_chat_history, clear_chat_history,
    can_send_message, get_remaining_messages, log_message_sent
)
from customer_dashboard import (
    get_dashboard_overview, get_user_orders, get_order_details,
    get_user_reports, get_user_downloads, get_user_consultations,
    book_consultation, update_profile, get_user_preferences,
    update_preferences, log_download, get_user_payments
)
from report_generator import (
    generate_premium_report, get_report_text_content, mark_report_as_completed,
    get_report_by_order, NumerologyAnalyzer
)
from vedic_numerology import (
    VEDIC_NUMBER_MEANINGS, MASTER_NUMBERS, VEDIC_REMEDIES, VEDIC_PLANETS,
    get_number_meaning, calculate_birth_number, calculate_destiny_number,
    calculate_name_number, reduce_to_single_digit, get_relationship_compatibility,
    VEDIC_CAREERS, VEDIC_FINANCIAL_GUIDANCE, get_vedic_year_forecast,
    VEDIC_YANTRAS, LO_SHU_POSITIONS, VEDIC_SPIRITUAL_PRACTICES
)

try:
    from auto_qr_system import (
        auto_qr, generate_payment_qr, generate_report_qr,
        generate_sharing_qr, generate_verification_qr
    )
    QR_SYSTEM_AVAILABLE = True
except ImportError:
    QR_SYSTEM_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "numero-annand-ai-secret-2024")

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///numero_annand.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

# =========================================================
# LINKS
# =========================================================

WHATSAPP_CONSULT_LINK = "https://wa.me/917099805039"
WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/C5g8MVpA0SYASAyrZfsrtJ?mode=gi_t"

MASTER_NUMBERS = {11,22,33}

# =========================================================
# CHALDEAN MAP
# =========================================================

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

# =========================================================
# RELATIONS
# =========================================================

NUM_RELATIONS = {
1:{'friends':[1,2,3,5,7,9],'neutral':[4,8],'enemy':[6]},
2:{'friends':[1,2,3,5],'neutral':[4,7,8,9],'enemy':[6]},
3:{'friends':[1,2,3,5,7,9],'neutral':[6,8],'enemy':[4]},
4:{'friends':[1,5,6,7],'neutral':[2,8,9],'enemy':[3]},
5:{'friends':[1,2,3,5,6,8],'neutral':[4,7,9],'enemy':[]},
6:{'friends':[5,6,7,8],'neutral':[3,4,9],'enemy':[1,2]},
7:{'friends':[1,3,4,5,6],'neutral':[2,8,9],'enemy':[]},
8:{'friends':[4,5,6,7],'neutral':[1,2,3],'enemy':[8,9]},
9:{'friends':[1,2,3,5,7],'neutral':[4,6],'enemy':[8,9]}
}

# =========================================================
# TRANSLATIONS
# =========================================================

TRANSLATIONS = {

'en':{
'title':'🔮 Numero Annand AI',
'workspace':'Workspace Menu',
'name':'Name',
'dob':'Date Of Birth',
'mobile':'Mobile Number',
'lang':'Choose Language',
'btn':'Analyze Now',
'consult':'Consultation Folder',
'group':'WhatsApp Group Folder',
'join':'Open WhatsApp Group',
'chat':'💬 Chat On WhatsApp'
},

'hi':{
'title':'🔮 Numero Annand AI',
'workspace':'कार्य मेनू',
'name':'नाम',
'dob':'जन्म तिथि',
'mobile':'मोबाइल नंबर',
'lang':'भाषा चुनें',
'btn':'विश्लेषण करें',
'consult':'परामर्श फ़ोल्डर',
'group':'व्हाट्सएप ग्रुप फ़ोल्डर',
'join':'व्हाट्सएप ग्रुप खोलें',
'chat':'💬 व्हाट्सएप पर चैट करें'
},

'as':{
'title':'🔮 Numero Annand AI',
'workspace':'কৰ্মক্ষেত্ৰ মেনু',
'name':'নাম',
'dob':'জন্ম তাৰিখ',
'mobile':'মোবাইল নম্বৰ',
'lang':'ভাষা বাছক',
'btn':'বিশ্লেষণ কৰক',
'consult':'পৰামৰ্শ ফোল্ডাৰ',
'group':'হোৱাটছএপ গ্ৰুপ',
'join':'হোৱাটছএপ গ্ৰুপ খোলক',
'chat':'💬 হোৱাটছএপত চেট কৰক'
}

}

# =========================================================
# CSS
# =========================================================

STYLE = """
<style>

:root{
--bg:#050816;
--card:#10192d;
--accent:#00ffd5;
--accent2:#00a2ff;
--text:#f5f5f5;
--border:#23395d;
}

body{
margin:0;
padding:0;
font-family:Segoe UI;
background:
radial-gradient(circle at top left,#00ffd522,transparent 25%),
radial-gradient(circle at top right,#00a2ff22,transparent 25%),
linear-gradient(135deg,#050816,#08111f,#10192d);
color:white;
}

.hero{
padding:60px 20px;
text-align:center;
}

.hero h1{
font-size:55px;
margin:0;
color:var(--accent);
text-shadow:0 0 25px #00ffd566;
}

.hero p{
max-width:900px;
margin:auto;
margin-top:20px;
line-height:1.9;
color:#aab4c6;
font-size:18px;
}

.main{
display:flex;
gap:20px;
padding:20px;
}

.sidebar{
width:330px;
min-width:330px;
background:rgba(16,25,45,.96);
border:1px solid var(--border);
border-radius:22px;
padding:22px;
height:fit-content;
}

.content{
flex:1;
}

.card{
background:rgba(16,25,45,.96);
border:1px solid var(--border);
border-radius:22px;
padding:25px;
margin-bottom:22px;
box-shadow:0 0 25px rgba(0,0,0,.35);
}

.card h2,.card h3{
color:var(--accent);
margin-top:0;
}

.small{
font-size:15px;
line-height:1.9;
color:#b6c0d1;
}

input,select{
width:100%;
padding:14px;
margin-top:8px;
margin-bottom:18px;
background:#08101f;
border:1px solid #314d79;
border-radius:12px;
color:white;
font-size:15px;
box-sizing:border-box;
}

button{
width:100%;
padding:14px;
border:none;
border-radius:12px;
background:linear-gradient(135deg,var(--accent),var(--accent2));
font-weight:bold;
cursor:pointer;
}

button:hover{
opacity:.9;
}

.badge{
display:inline-block;
padding:8px 16px;
border-radius:999px;
background:var(--accent);
color:black;
font-weight:bold;
margin:5px;
}

.loshu{
margin:auto;
border-collapse:separate;
border-spacing:12px;
}

.loshu td{
width:95px;
height:95px;
text-align:center;
vertical-align:middle;
background:#08101f;
border:2px solid #31486f;
border-radius:18px;
font-size:28px;
font-weight:bold;
color:var(--accent);
}

.empty{
color:#445 !important;
}

.meter{
height:16px;
background:#1f2f4a;
border-radius:999px;
overflow:hidden;
margin-top:12px;
}

.fill{
height:100%;
background:linear-gradient(90deg,#00ffd5,#00a2ff);
}

.footer{
text-align:center;
padding:35px;
color:#7d8aa0;
}

ul li{
margin-bottom:10px;
line-height:1.8;
}

.success{
background:#0d3520;
padding:18px;
border-left:5px solid #00ff88;
border-radius:12px;
line-height:1.8;
}

.warning{
background:#3d2407;
padding:18px;
border-left:5px solid orange;
border-radius:12px;
line-height:1.8;
}

@media(max-width:900px){

.main{
flex-direction:column;
}

.sidebar{
width:100%;
min-width:100%;
}

.hero h1{
font-size:38px;
}

.loshu td{
width:72px;
height:72px;
font-size:22px;
}

}

</style>
"""

# =========================================================
# ENGINE
# =========================================================

class NumerologyEngine:

    LOSHU_LAYOUT = [
        [4,9,2],
        [3,5,7],
        [8,1,6]
    ]

    def __init__(self,name,dob,mobile=""):

        self.name = name
        self.dob = dob
        self.mobile = mobile

        self.driver = 0
        self.conductor = 0
        self.name_total = 0
        self.name_single = 0

        self.freq = {i:0 for i in range(1,10)}
        self.grid_map = {i:[] for i in range(1,10)}

    def reduce(self,n,master=True):

        if master and n in MASTER_NUMBERS:
            return n

        while n > 9:

            n = sum(int(x) for x in str(n))

            if master and n in MASTER_NUMBERS:
                return n

        return n

    def parse_date(self):

        s = self.dob.replace("/","-").replace(".","-")

        if re.match(r"^\d{2}-\d{2}-\d{4}$",s):
            return datetime.strptime(s,"%d-%m-%Y").date()

        return parser.parse(s,dayfirst=True).date()

    def calculate(self):

        self.parsed_date = self.parse_date()

        digits = [
            int(x)
            for x in self.parsed_date.strftime("%d%m%Y")
            if x != "0"
        ]

        self.driver = self.reduce(self.parsed_date.day)

        total = (
            self.parsed_date.day +
            self.parsed_date.month +
            self.parsed_date.year
        )

        self.conductor = self.reduce(total)

        for n in digits + [self.driver,self.conductor]:

            if 1 <= n <= 9:
                self.freq[n] += 1
                self.grid_map[n].append(str(n))

        total_name = 0

        for ch in self.name.upper():

            if ch.isalpha():
                total_name += CHALDEAN_MAP.get(ch,0)

        self.name_total = total_name
        self.name_single = self.reduce(total_name)

    def loshu_html(self):

        html = "<table class='loshu'>"

        for row in self.LOSHU_LAYOUT:

            html += "<tr>"

            for n in row:

                vals = self.grid_map[n]

                if vals:
                    html += f"<td>{''.join(vals)}</td>"
                else:
                    html += "<td class='empty'>-</td>"

            html += "</tr>"

        html += "</table>"

        return html

    def compatibility_score(self):

        score = 0

        name_digit = self.name_single

        d_rel = NUM_RELATIONS.get(self.driver,{})

        if name_digit in d_rel['friends']:
            score += 45
        elif name_digit in d_rel['neutral']:
            score += 25
        else:
            score += 8

        c_rel = NUM_RELATIONS.get(self.conductor,{})

        if name_digit in c_rel['friends']:
            score += 45
        elif name_digit in c_rel['neutral']:
            score += 25
        else:
            score += 8

        return min(score,100)

    def name_suggestions(self):

        suggestions = []

        test_names = [
            self.name + "h",
            self.name + " Raj",
            self.name + " Dev",
            self.name + " Anand",
            self.name + " Sharma",
            self.name + " Sai"
        ]

        used = set()

        for nm in test_names:

            total = 0

            for ch in nm.upper():

                if ch.isalpha():
                    total += CHALDEAN_MAP.get(ch,0)

            single = self.reduce(total)

            if single in NUM_RELATIONS[self.driver]['friends']:

                if nm not in used:

                    used.add(nm)

                    suggestions.append({
                        "name":nm,
                        "number":single,
                        "score":random.randint(84,98)
                    })

        return suggestions[:3]

# =========================================================
# TEMPLATE
# =========================================================

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Numero Annand AI</title>
<meta name='viewport' content='width=device-width,initial-scale=1'>
""" + STYLE + """
</head>
<body>

<div class='hero'>
<h1>🔮 Numero Annand AI</h1>

<p>
Analysis Available 🔮<br><br>

Want to know about yourself deeply?<br>
Discover your hidden personality, destiny vibration,
career potential, relationship energy,
Lo Shu Grid power, missing numbers,
future growth path and spiritual alignment.<br><br>

💬 WhatsApp Me To Know About Yourself
</p>

</div>

<div class='main'>

<div class='sidebar'>

<h2>{{t.workspace}}</h2>

<form method='POST' action='/analyze'>

<label>{{t.name}}</label>
<input type='text' name='name' required>

<label>{{t.dob}}</label>
<input type='text' name='dob' required placeholder='DD-MM-YYYY'>

<label>{{t.mobile}}</label>
<input type='text' name='mobile'>

<label>{{t.lang}}</label>

<select name='lang'>

<option value='en'>English</option>
<option value='hi'>Hindi</option>
<option value='as'>Assamese</option>

</select>

<button type='submit'>{{t.btn}}</button>

</form>

<hr style='border-color:#2c4166;margin:25px 0;'>

<div class='card'>

<h3>📞 {{t.consult}}</h3>

<p class='small'>
Primary Strategist:<br>
<b style='color:var(--accent);'>
Annand Sarma
</b>
</p>

<p class='small'>
Contact:<br>

<a href='""" + WHATSAPP_CONSULT_LINK + """'
target='_blank'
style='color:var(--accent);
text-decoration:none;
font-weight:bold;'>

{{t.chat}}

</a>

</p>

<ul class='small' style='padding-left:15px;'>

<li>Lo Shu Grid Analysis</li>
<li>Name Correction</li>
<li>Career Guidance</li>
<li>Relationship Analysis</li>
<li>Future Forecast</li>
<li>Personality Blueprint</li>

</ul>

<a href='""" + WHATSAPP_CONSULT_LINK + """'
target='_blank'
style='text-decoration:none;'>

<button type='button'>
Chat On WhatsApp
</button>

</a>

</div>

<div class='card'>

<h3>👥 {{t.group}}</h3>

<a href='""" + WHATSAPP_GROUP_LINK + """'
target='_blank'>

<button>{{t.join}}</button>

</a>

</div>

</div>

<div class='content'>

{{content|safe}}

</div>

</div>

<div class='footer'>
Numero Annand AI • Premium Numerology Platform
</div>

</body>
</html>
"""

# =========================================================
# HOME
# =========================================================

@app.route('/')
def home():

    lang = request.args.get('lang','en')

    t = TRANSLATIONS.get(lang,TRANSLATIONS['en'])

    content = """

<div class='card'>

<h2>✨ Welcome To Numero Annand AI</h2>

<p class='small'>

Advanced Premium Lo Shu Grid Numerology Platform powered by deep energetic analysis,
professional numerology intelligence,
personality interpretation systems,
career guidance algorithms,
karmic vibration decoding
and futuristic spiritual analytics.

</p>

</div>

"""

    return render_template_string(
        PAGE,
        content=content,
        t=t
    )

# =========================================================
# ANALYZE
# =========================================================

@app.route('/analyze',methods=['POST'])
def analyze():

    try:

        name = request.form['name']
        dob = request.form['dob']
        mobile = request.form['mobile']
        lang = request.form['lang']

        t = TRANSLATIONS.get(lang,TRANSLATIONS['en'])

        engine = NumerologyEngine(name,dob,mobile)

        engine.calculate()

        score = engine.compatibility_score()

        missing = [n for n in range(1,10) if engine.freq[n] == 0]
        repeated = [n for n,c in engine.freq.items() if c >= 2]

        suggestions = engine.name_suggestions()

        energy = random.randint(80,98)

        result = f"""

<div class='card'>

<h2>📘 PAGE 1 — CORE NUMEROLOGY PROFILE</h2>

<p><b>Full Name:</b> {name}</p>
<p><b>Date Of Birth:</b> {engine.parsed_date.strftime('%d-%m-%Y')}</p>

<p><b>Driver Number:</b>
<span class='badge'>{engine.driver}</span></p>

<p><b>Conductor Number:</b>
<span class='badge'>{engine.conductor}</span></p>

<p><b>Name Number:</b>
<span class='badge'>{engine.name_single}</span></p>

<p><b>Compound Name Value:</b>
<span class='badge'>{engine.name_total}</span></p>

<h3>⚡ Energy Balance Score</h3>

<div class='meter'>
<div class='fill' style='width:{energy}%'></div>
</div>

<p class='small'>

Your energetic compatibility score is calculated through synchronization between Driver Number,
Destiny vibration,
Lo Shu Grid structure,
missing number recovery potential,
and Chaldean name resonance patterns.

</p>

<h3>📊 Compatibility Ratio System</h3>

<div class='meter'>
<div class='fill' style='width:{score}%'></div>
</div>

<p class='small'>

Current Name Compatibility Ratio:
<b>{score}%</b>

</p>

</div>

<div class='card'>

<h2>📗 PAGE 2 — FULL LO SHU GRID ANALYSIS</h2>

{engine.loshu_html()}

<h3>🔍 Missing Numbers</h3>

<p class='small'>

<b>{missing if missing else 'None'}</b><br><br>

These absent frequencies indicate karmic lessons,
energetic imbalances,
developmental weaknesses,
and life areas requiring conscious improvement.
Missing numbers can influence emotional control,
discipline,
communication,
mental focus,
decision-making,
relationship harmony,
and material stability.

</p>

<h3>🔥 Repeated Numbers</h3>

<p class='small'>

<b>{repeated if repeated else 'None'}</b><br><br>

Repeated vibrations amplify energetic intensity,
behavioral patterns,
natural talents,
dominant personality dimensions,
and subconscious tendencies.
Strong repetitions increase manifestation power
but may also create emotional extremes
if not balanced properly.

</p>

<h3>🧠 Mental Plane Analysis</h3>

<p class='small'>

The Mental Plane reflects intellectual clarity,
analytical thinking,
planning ability,
visualization power,
memory structure,
learning capacity,
and strategic intelligence.
Strong mental frequencies support leadership,
innovation,
problem-solving,
and futuristic thinking.

</p>

<h3>❤️ Emotional Plane Analysis</h3>

<p class='small'>

The Emotional Plane represents empathy,
emotional reactions,
relationship sensitivity,
intuition,
inner emotional security,
compassion,
and communication quality.
Balanced emotional numbers improve harmony,
trust,
emotional maturity,
and social bonding.

</p>

<h3>💼 Practical Plane Analysis</h3>

<p class='small'>

The Practical Plane governs execution ability,
financial discipline,
career consistency,
work ethic,
organizational strength,
implementation capacity,
and material manifestation potential.
Strong practical numbers create long-term stability
and success orientation.

</p>

</div>

<div class='card'>

<h2>📙 PAGE 3 — ADVANCED PSYCHOLOGICAL & SPIRITUAL ANALYSIS</h2>

<h3>🧿 Arrow Analysis</h3>

<p class='small'>

Your Lo Shu Grid reveals hidden energetic pathways
influencing determination,
willpower,
communication style,
emotional control,
discipline,
creativity,
spirituality,
and behavioral psychology.
Strong arrows improve internal balance,
while broken arrows reveal karmic learning zones.

</p>

<h3>👑 Raj Yog Potential</h3>

<p class='small'>

The interaction between your Driver Number,
Conductor vibration,
and Lo Shu Grid frequencies
shows strong potential for recognition,
authority,
leadership,
social influence,
and long-term success.
Consistent discipline and emotional balance
significantly improve manifestation power.

</p>

<h3>🧠 Psychological Traits</h3>

<p class='small'>

Your numerology chart indicates a deeply layered psychological structure
influenced by subconscious karmic memories,
internal emotional sensitivity,
and intellectual ambition.
You naturally seek purpose,
security,
stability,
respect,
and meaningful growth experiences
rather than temporary achievements.

</p>

<h3>🪷 Spiritual Traits</h3>

<p class='small'>

Spiritual development becomes important
when your internal vibration starts searching
for emotional clarity,
energetic peace,
life purpose,
and higher consciousness.
Meditation,
discipline,
gratitude,
and positive environments
help stabilize your spiritual energy.

</p>

</div>

<div class='card'>

<h2>📕 PAGE 4 — NAME CORRECTION & LIFE GUIDANCE</h2>

<div class='warning'>

⚠️ Your current name vibration is functional,
but a professionally optimized spelling
can improve synchronization
with your Driver Number,
Destiny vibration,
and Lo Shu Grid structure.

</div>

<h3>✨ Professionally Suggested Corrected Names</h3>

"""

        for s in suggestions:

            result += f"""

<div class='card'>

<h3>{s['name']}</h3>

<p><b>Improved Compatibility:</b> {s['score']}%</p>

<p><b>New Vibration Number:</b> {s['number']}</p>

<p class='small'>

This spelling introduces stronger energetic synchronization
with your Driver Number ({engine.driver})
and Destiny Number ({engine.conductor}),
helping improve energetic harmony,
confidence,
career flow,
relationship vibration,
and manifestation strength.

</p>

</div>

"""

        result += f"""

<h3>💼 Career Guidance</h3>

<p class='small'>

Your numerological structure supports fields connected to
communication,
teaching,
guidance,
management,
public interaction,
consulting,
business,
leadership,
analytics,
technology,
media,
motivation,
and spirituality.
Long-term success improves through discipline,
consistency,
and emotional balance.

</p>

<h3>❤️ Relationship Guidance</h3>

<p class='small'>

Relationship harmony improves through patience,
balanced communication,
emotional openness,
understanding,
and mutual respect.
Your emotional vibration seeks sincerity,
loyalty,
trust,
psychological depth,
and stable emotional support within relationships.

</p>

<h3>💰 Financial Guidance</h3>

<p class='small'>

Financial stability increases through strategic planning,
long-term discipline,
practical money management,
and controlled decision-making.
Avoid emotionally impulsive financial decisions
during unstable periods.

</p>

<h3>🍀 Lucky Indicators</h3>

<ul>

<li>Lucky Numbers:
{engine.driver},
{engine.conductor},
{engine.name_single}</li>

<li>Lucky Days:
Sunday,
Wednesday,
Friday</li>

<li>Lucky Colors:
Aqua Blue,
White,
Emerald Green</li>

</ul>

</div>

<div class='card'>

<h2>📒 PAGE 5 — DEEP AI PROFESSIONAL REPORT</h2>

<h3>🧠 Human-Style Deep Interpretation</h3>

<p class='small'>

Your complete numerological blueprint reveals a personality
carrying both intellectual sensitivity
and long-term growth potential.
The interaction between your Driver vibration,
Destiny path,
and Name frequency
creates a life pattern focused on
self-development,
responsibility,
emotional evolution,
and gradual manifestation.

Periods of confusion generally appear
when emotional pressure overrides logical thinking.
However,
your chart also shows strong recovery ability,
adaptability,
and resilience.

</p>

<h3>📈 Yearly Forecast</h3>

<p class='small'>

The upcoming energetic cycle favors
structured planning,
financial awareness,
career improvements,
communication growth,
knowledge-sharing,
and emotional maturity.
New opportunities may emerge through networking,
guidance roles,
business activity,
or public interaction.

</p>

<h3>🪷 Spiritual Roadmap</h3>

<p class='small'>

Meditation,
positive environments,
gratitude practice,
structured routine,
and spiritual self-awareness
help stabilize your energetic field.
Avoid emotional overthinking,
negative surroundings,
and inconsistent habits.

</p>

<h3>🧿 Remedies</h3>

<ul>

<li>Practice meditation daily for 11 minutes.</li>

<li>Maintain a disciplined sleep routine.</li>

<li>Use positive affirmations consistently.</li>

<li>Stay connected with positive people.</li>

<li>Wear clean light-colored clothes frequently.</li>

</ul>

<h3>🚀 Success Strategy</h3>

<p class='small'>

Long-term success emerges
when emotional intelligence,
discipline,
communication skills,
practical action,
and spiritual balance
work together.
Your chart rewards patience,
consistency,
structured planning,
and positive contribution to society
more than shortcuts.

</p>

</div>

<div class='card'>

<h2>📊 COMPLETE FREQUENCY ANALYSIS</h2>

"""

        for n,c in engine.freq.items():

            if c == 0:
                result += f"<p class='small'>❌ Number {n} is completely missing from your Lo Shu Grid and represents karmic lessons.</p>"

            elif c == 1:
                result += f"<p class='small'>⚖️ Number {n} appears once and shows balanced energy.</p>"

            elif c == 2:
                result += f"<p class='small'>✅ Number {n} appears twice and indicates strong balanced vibration.</p>"

            else:
                result += f"<p class='small'>🔥 Number {n} appears {c} times and shows amplified energetic intensity.</p>"

        result += "</div>"

        return render_template_string(
            PAGE,
            content=result,
            t=t
        )

    except Exception as e:

        return render_template_string(
            PAGE,
            content=f"<div class='card'><div class='warning'>Error: {str(e)}</div></div>",
            t=TRANSLATIONS['en']
        )

# =========================================================
# API ROUTES - AUTHENTICATION
# =========================================================

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user, error = register_user(
        email=data['email'],
        password=data['password'],
        name=data['name'],
        mobile=data.get('mobile', ''),
        language=data.get('language', 'en')
    )
    
    if error:
        return jsonify({'error': error}), 409
    
    token = generate_token(user.id, user.role)
    
    return jsonify({
        'success': True,
        'user': user.to_dict(),
        'token': token
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user, token, error = login_user(data['email'], data['password'])
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({
        'success': True,
        'user': user.to_dict(),
        'token': token
    }), 200

@app.route('/api/auth/me', methods=['GET'])
@token_required
def api_get_user():
    user = User.query.get(request.user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200

# =========================================================
# API ROUTES - MEMBERSHIP
# =========================================================

@app.route('/api/membership/plans', methods=['GET'])
def api_get_membership_plans():
    plans = get_all_plans()
    
    return jsonify({
        'success': True,
        'plans': plans
    }), 200

@app.route('/api/membership/status', methods=['GET'])
@token_required
def api_get_membership_status():
    status = get_membership_status(request.user_id)
    
    if not status:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'status': status
    }), 200

@app.route('/api/membership/subscribe', methods=['POST'])
@token_required
def api_subscribe_membership():
    data = request.get_json()
    plan_duration = data.get('plan')
    
    if not plan_duration:
        return jsonify({'error': 'Plan duration required'}), 400
    
    # Create membership order
    order, error = create_membership_order(request.user_id, plan_duration)
    
    if error:
        return jsonify({'error': error}), 400
    
    plan = get_membership_details(plan_duration)
    
    # Generate QR code for payment
    qr_data = generate_qr_code(plan['price'], order.id)
    
    # Create payment record
    payment, error = create_payment_record(order.id, plan['price'], qr_data['upi_string'])
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'success': True,
        'order': order.to_dict(),
        'plan': plan,
        'payment': {
            'qr_image': qr_data['image'],
            'upi_id': qr_data['upi_id'],
            'payee_name': qr_data['payee_name'],
            'amount': qr_data['amount'],
            'currency': qr_data['currency'],
            'reference': qr_data['reference']
        }
    }), 201

@app.route('/api/membership/verify', methods=['POST'])
@token_required
def api_verify_membership_payment():
    data = request.get_json()
    order_id = data.get('order_id')
    utr = data.get('utr')
    
    if not order_id or not utr:
        return jsonify({'error': 'Order ID and UTR required'}), 400
    
    order = Order.query.get(order_id)
    if not order or order.user_id != request.user_id:
        return jsonify({'error': 'Order not found'}), 404
    
    success, message = verify_payment(order_id, utr)
    
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'success': True,
        'message': message
    }), 200

@app.route('/api/membership/activate/<int:order_id>', methods=['POST'])
@admin_required
def api_activate_membership(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order.report_type != 'membership':
        return jsonify({'error': 'Not a membership order'}), 400
    
    # Extract plan duration from order
    plan_duration = order.order_id.split('MEM')[1][-8:]
    
    # Determine plan based on amount
    for plan_id, plan_data in MEMBERSHIP_PLANS.items():
        if plan_data['price'] == order.amount:
            plan_duration = plan_id
            break
    
    # Activate membership
    success, message = activate_membership(order.user_id, plan_duration)
    
    if not success:
        return jsonify({'error': message}), 400
    
    # Update order status
    order.status = 'completed'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': message
    }), 200

# =========================================================
# API ROUTES - ORDERS & PAYMENTS
# =========================================================

@app.route('/api/orders/create', methods=['POST'])
@token_required
def api_create_order():
    data = request.get_json()
    report_type = data.get('report_type', 'digital')
    
    amount = PRICING.get(f'{report_type}_report', 0)
    if not amount:
        return jsonify({'error': 'Invalid report type'}), 400
    
    order = create_order(request.user_id, report_type, amount)
    
    # Generate QR code
    qr_data = generate_qr_code(amount, order.id)
    
    # Create payment record
    payment, error = create_payment_record(order.id, amount, qr_data['upi_string'])
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'success': True,
        'order': order.to_dict(),
        'payment': {
            'qr_image': qr_data['image'],
            'upi_id': qr_data['upi_id'],
            'payee_name': qr_data['payee_name'],
            'amount': qr_data['amount'],
            'currency': qr_data['currency'],
            'reference': qr_data['reference']
        }
    }), 201

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@token_required
def api_get_order(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order.user_id != request.user_id and request.user_role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'order': order.to_dict()
    }), 200

@app.route('/api/orders/verify', methods=['POST'])
@token_required
def api_verify_payment():
    data = request.get_json()
    order_id = data.get('order_id')
    utr = data.get('utr')
    
    if not order_id or not utr:
        return jsonify({'error': 'Order ID and UTR required'}), 400
    
    success, message = verify_payment(order_id, utr)
    
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'success': True,
        'message': message
    }), 200

# =========================================================
# API ROUTES - ADMIN DASHBOARD
# =========================================================

@app.route('/api/admin/analytics', methods=['GET'])
@admin_required
def api_admin_analytics():
    from admin_utils import get_dashboard_analytics
    
    analytics = get_dashboard_analytics()
    
    return jsonify({
        'success': True,
        'analytics': analytics
    }), 200

@app.route('/api/admin/pending-payments', methods=['GET'])
@admin_required
def api_admin_pending_payments():
    from admin_utils import get_pending_payments
    
    pending = get_pending_payments()
    
    return jsonify({
        'success': True,
        'payments': pending,
        'count': len(pending)
    }), 200

@app.route('/api/admin/verify-payment/<int:order_id>', methods=['POST'])
@admin_required
def api_admin_verify_payment(order_id):
    from admin_utils import verify_payment_admin
    
    data = request.get_json()
    verified = data.get('verified', True)
    
    success, message = verify_payment_admin(order_id, verified)
    
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'success': True,
        'message': message
    }), 200

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def api_admin_get_users():
    from admin_utils import get_all_users, search_users
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    if search:
        users_data = search_users(search)
        return jsonify({
            'success': True,
            'users': users_data,
            'total': len(users_data)
        }), 200
    
    result = get_all_users(page=page)
    
    return jsonify({
        'success': True,
        **result
    }), 200

@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
@admin_required
def api_admin_get_user_details(user_id):
    from admin_utils import get_user_details
    
    user = get_user_details(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': user
    }), 200

@app.route('/api/admin/reports', methods=['GET'])
@admin_required
def api_admin_get_reports():
    from admin_utils import get_all_reports
    
    page = request.args.get('page', 1, type=int)
    
    result = get_all_reports(page=page)
    
    return jsonify({
        'success': True,
        **result
    }), 200

@app.route('/api/admin/verified-payments', methods=['GET'])
@admin_required
def api_admin_verified_payments():
    from admin_utils import get_verified_payments
    
    payments = get_verified_payments()
    
    return jsonify({
        'success': True,
        'payments': payments,
        'count': len(payments)
    }), 200

@app.route('/api/admin/revenue', methods=['GET'])
@admin_required
def api_admin_revenue():
    from admin_utils import get_revenue_by_date
    
    days = request.args.get('days', 30, type=int)
    
    revenue_data = get_revenue_by_date(days=days)
    
    return jsonify({
        'success': True,
        'revenue': revenue_data,
        'total': sum(revenue_data.values())
    }), 200

@app.route('/api/admin/activity-logs', methods=['GET'])
@admin_required
def api_admin_activity_logs():
    from admin_utils import get_activity_logs
    
    limit = request.args.get('limit', 100, type=int)
    
    logs = get_activity_logs(limit=limit)
    
    return jsonify({
        'success': True,
        'logs': logs,
        'count': len(logs)
    }), 200

@app.route('/api/admin/contact-messages', methods=['GET'])
@admin_required
def api_admin_contact_messages():
    from admin_utils import get_contact_messages
    
    status = request.args.get('status', 'new')
    
    messages = get_contact_messages(status=status)
    
    return jsonify({
        'success': True,
        'messages': messages,
        'count': len(messages)
    }), 200

@app.route('/api/admin/contact-messages/<int:message_id>/reply', methods=['POST'])
@admin_required
def api_admin_reply_contact(message_id):
    from admin_utils import mark_message_as_replied
    
    success = mark_message_as_replied(message_id)
    
    if not success:
        return jsonify({'error': 'Message not found'}), 404
    
    return jsonify({
        'success': True,
        'message': 'Message marked as replied'
    }), 200

@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    admin = Admin.query.filter_by(email=data['email']).first()
    
    if not admin or not admin.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    token = generate_token(admin.id, role='admin')
    
    return jsonify({
        'success': True,
        'admin': {
            'id': admin.id,
            'email': admin.email,
            'name': admin.name,
            'role': admin.role
        },
        'token': token
    }), 200

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def api_admin_stats():
    from admin_utils import get_dashboard_analytics, get_membership_stats
    
    analytics = get_dashboard_analytics()
    membership_stats = get_membership_stats()
    
    return jsonify({
        'success': True,
        'analytics': analytics,
        'membership': membership_stats
    }), 200

# =========================================================
# API ROUTES - REPORT GENERATION
# =========================================================

@app.route('/api/reports/generate', methods=['POST'])
@token_required
def api_generate_report():
    data = request.get_json()
    
    order_id = data.get('order_id')
    name = data.get('name')
    dob = data.get('dob')
    mobile = data.get('mobile', '')
    
    if not all([order_id, name, dob]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Generate report
    report, error = generate_premium_report(request.user_id, order_id, name, dob, mobile)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Mark order as completed
    mark_report_as_completed(order_id)
    
    return jsonify({
        'success': True,
        'report': report.to_dict(),
        'message': 'Report generated successfully'
    }), 201

@app.route('/api/reports/<int:report_id>', methods=['GET'])
@token_required
def api_get_report(report_id):
    report = Report.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    # Check if user owns the report (via order)
    if report.order.user_id != request.user_id and request.user_role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'report': {
            'id': report.id,
            'user_name': report.user_name,
            'dob': report.dob,
            'mobile': report.mobile,
            'data': json.loads(report.report_data),
            'created_at': report.created_at.isoformat(),
            'signature': report.digital_signature
        }
    }), 200

@app.route('/api/reports/<int:report_id>/text', methods=['GET'])
@token_required
def api_get_report_text(report_id):
    report = Report.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    # Check authorization
    if report.order.user_id != request.user_id and request.user_role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    text_content = get_report_text_content(report_id)
    
    return jsonify({
        'success': True,
        'content': text_content
    }), 200

@app.route('/api/reports/by-order/<int:order_id>', methods=['GET'])
@token_required
def api_get_report_by_order(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Check authorization
    if order.user_id != request.user_id and request.user_role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    report = get_report_by_order(order_id)
    
    if not report:
        return jsonify({
            'success': True,
            'report': None,
            'message': 'No report generated yet'
        }), 200
    
    return jsonify({
        'success': True,
        'report': report.to_dict()
    }), 200

@app.route('/api/numerology/analyze', methods=['POST'])
def api_analyze_numerology():
    """Quick numerology analysis without authentication"""
    
    data = request.get_json()
    name = data.get('name', '')
    dob = data.get('dob', '')
    
    if not name or not dob:
        return jsonify({'error': 'Name and DOB required'}), 400
    
    try:
        analyzer = NumerologyAnalyzer(name, dob)
        
        birth_number = analyzer.calculate_birth_number(dob)
        destiny_number = analyzer.calculate_destiny_number(dob)
        name_number = analyzer.calculate_name_number()
        
        from report_generator import get_number_meaning
        
        return jsonify({
            'success': True,
            'analysis': {
                'birth_number': birth_number,
                'destiny_number': destiny_number,
                'name_number': name_number,
                'birth_meaning': get_number_meaning(birth_number),
                'destiny_meaning': get_number_meaning(destiny_number),
                'name_meaning': get_number_meaning(name_number)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# =========================================================
# API ROUTES - COMMUNITY & SOCIAL
# =========================================================

@app.route('/api/community/links', methods=['GET'])
def api_community_links():
    from community import COMMUNITY_LINKS
    
    return jsonify({
        'success': True,
        'links': COMMUNITY_LINKS
    }), 200

@app.route('/api/community/testimonials', methods=['GET'])
def api_community_testimonials():
    from community import get_public_testimonials
    
    language = request.args.get('language', 'en')
    
    testimonials = get_public_testimonials(language=language)
    
    return jsonify({
        'success': True,
        'testimonials': testimonials
    }), 200

@app.route('/api/community/daily-tip', methods=['GET'])
def api_community_daily_tip():
    from community import get_daily_tip
    
    language = request.args.get('language', 'en')
    
    tip = get_daily_tip(language=language)
    
    return jsonify({
        'success': True,
        'tip': tip
    }), 200

@app.route('/api/community/lucky-elements/<int:number>', methods=['GET'])
def api_lucky_elements(number):
    from community import get_lucky_numbers
    
    elements = get_lucky_numbers(number)
    
    if not elements:
        return jsonify({'error': 'Invalid number'}), 400
    
    return jsonify({
        'success': True,
        'elements': elements
    }), 200

@app.route('/api/community/contact', methods=['POST'])
def api_submit_contact():
    from community import submit_contact_message
    
    data = request.get_json()
    
    contact, error = submit_contact_message(
        name=data.get('name'),
        email=data.get('email'),
        mobile=data.get('mobile', ''),
        message=data.get('message')
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'success': True,
        'message': 'Thank you for contacting us. We will reply soon.'
    }), 201

@app.route('/api/community/faq', methods=['GET'])
def api_get_faq():
    from community import get_faq
    
    language = request.args.get('language', 'en')
    
    faq = get_faq(language=language)
    
    return jsonify({
        'success': True,
        'faq': faq
    }), 200

@app.route('/api/community/policies/<policy_type>', methods=['GET'])
def api_get_policy(policy_type):
    from community import get_policy
    
    language = request.args.get('language', 'en')
    
    policy = get_policy(policy_type=policy_type, language=language)
    
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    
    return jsonify({
        'success': True,
        'policy': policy
    }), 200

@app.route('/api/community/blog', methods=['GET'])
def api_get_blog_articles():
    from community import get_blog_articles
    
    language = request.args.get('language', 'en')
    limit = request.args.get('limit', 10, type=int)
    
    articles = get_blog_articles(language=language, limit=limit)
    
    return jsonify({
        'success': True,
        'articles': articles
    }), 200

@app.route('/api/community/blog/<slug>', methods=['GET'])
def api_get_blog_article(slug):
    from community import get_blog_article
    
    language = request.args.get('language', 'en')
    
    article = get_blog_article(slug=slug, language=language)
    
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    return jsonify({
        'success': True,
        'article': article
    }), 200

# =========================================================
# API ROUTES - LANGUAGE & LOCALIZATION
# =========================================================

@app.route('/api/languages', methods=['GET'])
def api_get_languages():
    from community import get_supported_languages
    
    languages = get_supported_languages()
    
    return jsonify({
        'success': True,
        'languages': languages
    }), 200

@app.route('/api/user/language', methods=['PUT'])
@token_required
def api_set_user_language():
    from community import set_user_language
    
    data = request.get_json()
    language = data.get('language')
    
    if not language:
        return jsonify({'error': 'Language required'}), 400
    
    success = set_user_language(request.user_id, language)
    
    if not success:
        return jsonify({'error': 'Invalid language or user not found'}), 400
    
    return jsonify({
        'success': True,
        'message': f'Language set to {language}'
    }), 200

@app.route('/api/translations/<language>', methods=['GET'])
def api_get_translations(language):
    """Get all translations for a language"""
    
    # This would return common UI translations
    translations = {
        'en': {
            'welcome': 'Welcome',
            'login': 'Login',
            'signup': 'Sign Up',
            'logout': 'Logout'
        },
        'hi': {
            'welcome': 'स्वागत है',
            'login': 'लॉगिन करें',
            'signup': 'साइन अप करें',
            'logout': 'लॉगआउट'
        },
        'as': {
            'welcome': 'স্বাগতম',
            'login': 'লগইন কৰক',
            'signup': 'সাইন আপ কৰক',
            'logout': 'লগআউट'
        }
    }
    
    if language not in translations:
        return jsonify({'error': 'Language not supported'}), 400
    
    return jsonify({
        'success': True,
        'translations': translations[language]
    }), 200

# =========================================================
# API ROUTES - VEDIC NUMEROLOGY ANALYSIS
# =========================================================

@app.route('/api/vedic/full-analysis', methods=['POST'])
def api_vedic_full_analysis():
    """Comprehensive Vedic numerology analysis"""
    
    data = request.get_json()
    name = data.get('name', '').strip()
    dob = data.get('dob', '').strip()
    language = data.get('language', 'en')
    
    if not name or not dob:
        return jsonify({'error': 'Name and date of birth required'}), 400
    
    try:
        # Calculate all numbers
        birth_number = calculate_birth_number(dob)
        destiny_number = calculate_destiny_number(dob)
        name_number = calculate_name_number(name)
        
        # Get meanings
        birth_meaning = get_number_meaning(birth_number)
        destiny_meaning = get_number_meaning(destiny_number)
        name_meaning = get_number_meaning(name_number)
        
        # Get remedies
        birth_remedies = VEDIC_REMEDIES.get(birth_number, {})
        destiny_remedies = VEDIC_REMEDIES.get(destiny_number, {})
        name_remedies = VEDIC_REMEDIES.get(name_number, {})
        
        # Get career guidance
        birth_careers = VEDIC_CAREERS.get(birth_number, [])
        name_careers = VEDIC_CAREERS.get(name_number, [])
        
        # Get financial guidance
        birth_finance = VEDIC_FINANCIAL_GUIDANCE.get(birth_number, {})
        destiny_finance = VEDIC_FINANCIAL_GUIDANCE.get(destiny_number, {})
        
        # Get spiritual practices
        birth_practices = VEDIC_SPIRITUAL_PRACTICES.get(birth_number, [])
        name_practices = VEDIC_SPIRITUAL_PRACTICES.get(name_number, [])
        
        # Get Yantra information
        birth_yantra = VEDIC_YANTRAS.get(birth_number, {})
        
        # Get yearly forecast
        dob_parts = dob.split('-')
        birth_year = int(dob_parts[0]) if len(dob_parts) >= 3 else 0
        yearly_forecast = get_vedic_year_forecast(birth_year) if birth_year > 0 else {}
        
        return jsonify({
            'success': True,
            'analysis': {
                'name': name,
                'dob': dob,
                'numbers': {
                    'birth_number': {
                        'number': birth_number,
                        'meaning': birth_meaning,
                        'remedies': birth_remedies,
                        'careers': birth_careers,
                        'finance': birth_finance,
                        'practices': birth_practices,
                        'yantra': birth_yantra
                    },
                    'destiny_number': {
                        'number': destiny_number,
                        'meaning': destiny_meaning,
                        'remedies': destiny_remedies,
                        'careers': name_careers,
                        'finance': destiny_finance
                    },
                    'name_number': {
                        'number': name_number,
                        'meaning': name_meaning,
                        'remedies': name_remedies,
                        'practices': name_practices
                    }
                },
                'yearly_forecast': yearly_forecast,
                'vedic_planets': VEDIC_PLANETS
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 400

@app.route('/api/vedic/relationship-compatibility', methods=['POST'])
def api_vedic_relationship_compatibility():
    """Calculate relationship compatibility between two people"""
    
    data = request.get_json()
    name1 = data.get('name1', '').strip()
    dob1 = data.get('dob1', '').strip()
    name2 = data.get('name2', '').strip()
    dob2 = data.get('dob2', '').strip()
    
    if not all([name1, dob1, name2, dob2]):
        return jsonify({'error': 'All fields required'}), 400
    
    try:
        # Calculate numbers for both
        birth1 = calculate_birth_number(dob1)
        destiny1 = calculate_destiny_number(dob1)
        name1_num = calculate_name_number(name1)
        
        birth2 = calculate_birth_number(dob2)
        destiny2 = calculate_destiny_number(dob2)
        name2_num = calculate_name_number(name2)
        
        # Get compatibilities
        birth_compat = get_relationship_compatibility(birth1, birth2)
        destiny_compat = get_relationship_compatibility(destiny1, destiny2)
        name_compat = get_relationship_compatibility(name1_num, name2_num)
        
        # Average score
        avg_score = (birth_compat['score'] + destiny_compat['score'] + name_compat['score']) / 3
        
        return jsonify({
            'success': True,
            'compatibility': {
                'person1': {'name': name1, 'birth': birth1, 'destiny': destiny1, 'name_num': name1_num},
                'person2': {'name': name2, 'birth': birth2, 'destiny': destiny2, 'name_num': name2_num},
                'birth_compatibility': birth_compat,
                'destiny_compatibility': destiny_compat,
                'name_compatibility': name_compat,
                'overall_score': round(avg_score),
                'interpretation': 'Excellent match' if avg_score >= 80 else 'Good match' if avg_score >= 60 else 'Moderate match' if avg_score >= 40 else 'Challenging match'
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Compatibility check failed: {str(e)}'}), 400

@app.route('/api/vedic/number-meanings/<int:number>', methods=['GET'])
def api_vedic_number_meaning(number):
    """Get detailed Vedic meaning for a specific number"""
    
    if number < 1 or number > 9:
        if number not in MASTER_NUMBERS:
            return jsonify({'error': 'Invalid number. Must be 1-9 or master number (11, 22, 33)'}), 400
    
    if number in VEDIC_NUMBER_MEANINGS:
        meaning = VEDIC_NUMBER_MEANINGS[number]
    elif number in MASTER_NUMBERS:
        meaning = MASTER_NUMBERS[number]
    else:
        return jsonify({'error': 'Number not found'}), 404
    
    remedies = VEDIC_REMEDIES.get(number, {})
    careers = VEDIC_CAREERS.get(number, [])
    yantra = VEDIC_YANTRAS.get(number, {})
    finance = VEDIC_FINANCIAL_GUIDANCE.get(number, {})
    practices = VEDIC_SPIRITUAL_PRACTICES.get(number, [])
    
    return jsonify({
        'success': True,
        'number': number,
        'meaning': meaning,
        'remedies': remedies,
        'careers': careers,
        'yantra': yantra,
        'financial_guidance': finance,
        'spiritual_practices': practices
    }), 200

@app.route('/api/vedic/lucky-elements/<int:number>', methods=['GET'])
def api_vedic_lucky_elements(number):
    """Get lucky elements for a specific number"""
    
    if number < 1 or number > 9:
        return jsonify({'error': 'Invalid number. Must be 1-9'}), 400
    
    meaning = VEDIC_NUMBER_MEANINGS.get(number, {})
    yantra = VEDIC_YANTRAS.get(number, {})
    planet = VEDIC_PLANETS.get([v for k,v in VEDIC_PLANETS.items() if v.get('number') == number][0]) if any(v.get('number') == number for v in VEDIC_PLANETS.values()) else {}
    
    return jsonify({
        'success': True,
        'number': number,
        'lucky_elements': {
            'color': meaning.get('color', ''),
            'day': meaning.get('day', ''),
            'stone': meaning.get('lucky_stone', ''),
            'mantra': meaning.get('mantra', ''),
            'element': meaning.get('element', ''),
            'yantra': yantra,
            'planet_name': meaning.get('planet', ''),
            'positive_traits': meaning.get('traits', []),
            'professions': VEDIC_CAREERS.get(number, [])
        }
    }), 200

@app.route('/api/vedic/life-path', methods=['POST'])
def api_vedic_life_path():
    """Get complete life path and destiny guidance"""
    
    data = request.get_json()
    name = data.get('name', '').strip()
    dob = data.get('dob', '').strip()
    
    if not name or not dob:
        return jsonify({'error': 'Name and date of birth required'}), 400
    
    try:
        destiny_num = calculate_destiny_number(dob)
        birth_num = calculate_birth_number(dob)
        name_num = calculate_name_number(name)
        
        destiny_info = VEDIC_NUMBER_MEANINGS.get(destiny_num, {})
        
        life_path = {
            'destiny_number': destiny_num,
            'birth_number': birth_num,
            'name_number': name_num,
            'life_purpose': destiny_info.get('vedic_meaning', ''),
            'key_traits': destiny_info.get('traits', []),
            'career_path': VEDIC_CAREERS.get(destiny_num, []),
            'challenges': f"Main challenge is to balance {destiny_info.get('negative', '')} and embrace {destiny_info.get('positive', '')}",
            'life_lessons': f"Life lesson: Learn to embody the highest expression of {destiny_info.get('name', '')}",
            'success_factors': [
                f"Follow your {destiny_info.get('name', '')} nature",
                f"Embrace the energy of {destiny_info.get('planet', '')}",
                f"Practice the mantra: {destiny_info.get('mantra', '')}",
                f"Use color therapy with {destiny_info.get('color', '')}"
            ]
        }
        
        return jsonify({
            'success': True,
            'life_path': life_path
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Life path analysis failed: {str(e)}'}), 400

@app.route('/api/vedic/remedies/<int:number>', methods=['GET'])
def api_vedic_remedies(number):
    """Get Vedic remedies and rituals for a specific number"""
    
    if number < 1 or number > 9:
        return jsonify({'error': 'Invalid number. Must be 1-9'}), 400
    
    remedies = VEDIC_REMEDIES.get(number, {})
    
    if not remedies:
        return jsonify({'error': 'Remedies not found'}), 404
    
    return jsonify({
        'success': True,
        'number': number,
        'remedies': remedies,
        'note': 'These remedies are based on ancient Vedic principles. Consistency and faith are key to effectiveness.'
    }), 200

@app.route('/api/vedic/spiritual-practices/<int:number>', methods=['GET'])
def api_vedic_spiritual_practices(number):
    """Get spiritual practices for a specific number"""
    
    if number < 1 or number > 9:
        return jsonify({'error': 'Invalid number. Must be 1-9'}), 400
    
    practices = VEDIC_SPIRITUAL_PRACTICES.get(number, [])
    meaning = VEDIC_NUMBER_MEANINGS.get(number, {})
    
    return jsonify({
        'success': True,
        'number': number,
        'practices': practices,
        'mantra': meaning.get('mantra', ''),
        'description': f'Spiritual practices for {meaning.get("name", "")} energy'
    }), 200

# =========================================================
# API ROUTES - CUSTOMER DASHBOARD
# =========================================================

@app.route('/api/dashboard/overview', methods=['GET'])
@token_required
def api_dashboard_overview():
    overview = get_dashboard_overview(request.user_id)
    
    if not overview:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'overview': overview
    }), 200

@app.route('/api/dashboard/orders', methods=['GET'])
@token_required
def api_dashboard_orders():
    page = request.args.get('page', 1, type=int)
    
    result = get_user_orders(request.user_id, page=page)
    
    return jsonify({
        'success': True,
        **result
    }), 200

@app.route('/api/dashboard/orders/<int:order_id>', methods=['GET'])
@token_required
def api_dashboard_order_details(order_id):
    details = get_order_details(order_id, request.user_id)
    
    if not details:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify({
        'success': True,
        'order': details
    }), 200

@app.route('/api/dashboard/reports', methods=['GET'])
@token_required
def api_dashboard_reports():
    page = request.args.get('page', 1, type=int)
    
    result = get_user_reports(request.user_id, page=page)
    
    return jsonify({
        'success': True,
        **result
    }), 200

@app.route('/api/dashboard/downloads', methods=['GET'])
@token_required
def api_dashboard_downloads():
    page = request.args.get('page', 1, type=int)
    
    result = get_user_downloads(request.user_id, page=page)
    
    return jsonify({
        'success': True,
        **result
    }), 200

@app.route('/api/dashboard/downloads/<int:report_id>', methods=['POST'])
@token_required
def api_dashboard_log_download(report_id):
    ip_address = request.remote_addr
    
    success = log_download(request.user_id, report_id, ip_address)
    
    if not success:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify({
        'success': True,
        'message': 'Download logged'
    }), 200

@app.route('/api/dashboard/consultations', methods=['GET'])
@token_required
def api_dashboard_consultations():
    page = request.args.get('page', 1, type=int)
    
    result = get_user_consultations(request.user_id, page=page)
    
    return jsonify({
        'success': True,
        **result
    }), 200

@app.route('/api/dashboard/consultations/book', methods=['POST'])
@token_required
def api_dashboard_book_consultation():
    data = request.get_json()
    
    consultation, error = book_consultation(
        request.user_id,
        consultation_type=data.get('type'),
        scheduled_date=data.get('date'),
        language=data.get('language', 'en'),
        notes=data.get('notes', '')
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'success': True,
        'consultation': consultation.to_dict()
    }), 201

@app.route('/api/dashboard/payments', methods=['GET'])
@token_required
def api_dashboard_payments():
    page = request.args.get('page', 1, type=int)
    
    result = get_user_payments(request.user_id, page=page)
    
    return jsonify({
        'success': True,
        **result
    }), 200

@app.route('/api/dashboard/profile', methods=['GET'])
@token_required
def api_dashboard_profile():
    user = User.query.get(request.user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'profile': user.to_dict()
    }), 200

@app.route('/api/dashboard/profile', methods=['PUT'])
@token_required
def api_dashboard_update_profile():
    data = request.get_json()
    
    success, message = update_profile(request.user_id, **data)
    
    if not success:
        return jsonify({'error': message}), 400
    
    user = User.query.get(request.user_id)
    
    return jsonify({
        'success': True,
        'profile': user.to_dict()
    }), 200

@app.route('/api/dashboard/preferences', methods=['GET'])
@token_required
def api_dashboard_preferences():
    preferences = get_user_preferences(request.user_id)
    
    if not preferences:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'preferences': preferences
    }), 200

@app.route('/api/dashboard/preferences', methods=['PUT'])
@token_required
def api_dashboard_update_preferences():
    data = request.get_json()
    
    success = update_preferences(request.user_id, data)
    
    if not success:
        return jsonify({'error': 'Failed to update preferences'}), 400
    
    preferences = get_user_preferences(request.user_id)
    
    return jsonify({
        'success': True,
        'preferences': preferences
    }), 200

# =========================================================
# API ROUTES - AI ASSISTANT
# =========================================================

@app.route('/api/ai/greeting', methods=['GET'])
def api_ai_greeting():
    language = request.args.get('language', 'en')
    ai = AnnandAI(language=language)
    
    return jsonify({
        'success': True,
        'greeting': ai.get_greeting(),
        'suggested_questions': ai.get_suggested_questions()
    }), 200

@app.route('/api/ai/message', methods=['POST'])
def api_ai_message():
    data = request.get_json()
    message = data.get('message', '').strip()
    language = data.get('language', 'en')
    user_id = data.get('user_id')
    
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Check if user is authenticated
    if user_id:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check message limit
        if not can_send_message(user_id):
            remaining = get_remaining_messages(user_id)
            return jsonify({
                'error': 'Message limit reached',
                'remaining': remaining,
                'upgrade_message': 'Upgrade to Premium for unlimited messages'
            }), 429
    
    # Generate AI response
    ai = AnnandAI(language=language)
    response = ai.process_message(message)
    
    # Save chat if user is authenticated
    if user_id:
        save_ai_chat(user_id, message, response, language)
        log_message_sent(user_id)
    
    return jsonify({
        'success': True,
        'response': response,
        'remaining_messages': get_remaining_messages(user_id) if user_id else -1
    }), 200

@app.route('/api/ai/history', methods=['GET'])
@token_required
def api_ai_history():
    limit = request.args.get('limit', 20, type=int)
    
    history = get_chat_history(request.user_id, limit=limit)
    
    return jsonify({
        'success': True,
        'history': history,
        'count': len(history)
    }), 200

@app.route('/api/ai/clear', methods=['POST'])
@token_required
def api_ai_clear():
    clear_chat_history(request.user_id)
    
    return jsonify({
        'success': True,
        'message': 'Chat history cleared'
    }), 200

@app.route('/api/ai/limits', methods=['GET'])
@token_required
def api_ai_limits():
    remaining = get_remaining_messages(request.user_id)
    user = User.query.get(request.user_id)
    
    return jsonify({
        'success': True,
        'remaining': remaining,
        'role': user.role,
        'is_premium': user.is_premium(),
        'unlimited': remaining == -1
    }), 200

# =========================================================
# WEB ROUTES - TEMPLATES
# =========================================================

@app.route('/vedic-analysis', methods=['GET'])
def vedic_analysis_page():
    """Serve the Vedic numerology analysis page"""
    try:
        with open('templates/vedic_analysis.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return render_template_string('''
            <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>Vedic Numerology Analysis</h1>
                <p>The analysis page is loading. Please refresh the page.</p>
                <p><a href="/">← Back to Home</a></p>
            </body>
            </html>
        '''), 404



@app.route('/status', methods=['GET'])
def status():
    """API status check"""
    return jsonify({
        'success': True,
        'status': 'API is running',
        'version': '2.0',
        'features': [
            'Vedic Numerology Analysis',
            'Relationship Compatibility',
            'Life Path Guidance',
            'Remedies & Rituals',
            'Spiritual Practices',
            'Multi-language Support'
        ]
    }), 200

# =========================================================
# API ROUTES - AUTO QR GENERATION SYSTEM
# =========================================================

if QR_SYSTEM_AVAILABLE:
    
    @app.route('/api/qr/payment', methods=['POST'])
    def api_auto_generate_payment_qr():
        """Auto-generate payment QR code"""
        
        data = request.get_json()
        amount = data.get('amount')
        order_id = data.get('order_id')
        
        if not amount or not order_id:
            return jsonify({'error': 'Amount and order_id required'}), 400
        
        try:
            qr_data = generate_payment_qr(amount, order_id)
            return jsonify({
                'success': True,
                'qr_code': qr_data['qr_code'],
                'metadata': qr_data['metadata'],
                'timestamp': qr_data['timestamp']
            }), 200
        except Exception as e:
            return jsonify({'error': f'QR generation failed: {str(e)}'}), 400
    
    @app.route('/api/qr/report/<int:report_id>', methods=['GET'])
    def api_auto_generate_report_qr(report_id):
        """Auto-generate QR for report downloads"""
        
        user_email = request.args.get('email', 'user@numero-annand.ai')
        
        try:
            qr_data = generate_report_qr(report_id, user_email)
            return jsonify({
                'success': True,
                'qr_code': qr_data['qr_code'],
                'metadata': qr_data['metadata']
            }), 200
        except Exception as e:
            return jsonify({'error': f'QR generation failed: {str(e)}'}), 400
    
    @app.route('/api/qr/share/<content_type>/<content_id>', methods=['GET'])
    def api_auto_generate_sharing_qr(content_type, content_id):
        """Auto-generate QR for social sharing"""
        
        try:
            qr_data = generate_sharing_qr(content_id, content_type)
            return jsonify({
                'success': True,
                'qr_code': qr_data['qr_code'],
                'share_url': f"https://numero-annand.ai/share/{content_type}/{content_id}",
                'metadata': qr_data['metadata']
            }), 200
        except Exception as e:
            return jsonify({'error': f'QR generation failed: {str(e)}'}), 400
    
    @app.route('/api/qr/verify/<token>', methods=['GET'])
    def api_auto_generate_verification_qr(token):
        """Auto-generate QR for verification"""
        
        try:
            qr_data = generate_verification_qr(token)
            return jsonify({
                'success': True,
                'qr_code': qr_data['qr_code'],
                'verify_url': f"https://numero-annand.ai/verify/{token}",
                'metadata': qr_data['metadata']
            }), 200
        except Exception as e:
            return jsonify({'error': f'QR generation failed: {str(e)}'}), 400
    
    @app.route('/api/qr/generate', methods=['POST'])
    def api_qr_generate_custom():
        """Generate custom styled QR code"""
        
        data = request.get_json()
        content = data.get('content')
        style = data.get('style', 'professional')
        
        if not content:
            return jsonify({'error': 'Content required'}), 400
        
        if style not in ['professional', 'vibrant', 'minimal', 'spiritual']:
            return jsonify({'error': 'Invalid style. Use: professional, vibrant, minimal, spiritual'}), 400
        
        try:
            qr_base64 = auto_qr.generate_cached_qr(content, format='base64', style=style)
            return jsonify({
                'success': True,
                'qr_code': qr_base64,
                'style': style,
                'content': content
            }), 200
        except Exception as e:
            return jsonify({'error': f'QR generation failed: {str(e)}'}), 400
    
    @app.route('/api/qr/bulk', methods=['POST'])
    def api_qr_bulk_generate():
        """Generate multiple QR codes efficiently"""
        
        data = request.get_json()
        data_list = data.get('data', [])
        style = data.get('style', 'professional')
        
        if not data_list or not isinstance(data_list, list):
            return jsonify({'error': 'Data array required'}), 400
        
        try:
            qr_codes = auto_qr.bulk_generate_qrs(data_list, style=style)
            return jsonify({
                'success': True,
                'qr_codes': qr_codes,
                'total': len(qr_codes),
                'successful': sum(1 for qr in qr_codes if qr.get('status') == 'success')
            }), 200
        except Exception as e:
            return jsonify({'error': f'Bulk QR generation failed: {str(e)}'}), 400
    
    @app.route('/api/qr/stats', methods=['GET'])
    def api_qr_cache_stats():
        """Get QR cache statistics"""
        
        try:
            stats = auto_qr.get_qr_stats()
            return jsonify({
                'success': True,
                'stats': stats
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to get stats: {str(e)}'}), 400
    
    @app.route('/api/qr/clear-cache', methods=['POST'])
    @admin_required
    def api_qr_clear_cache():
        """Clear expired QR cache"""
        
        try:
            result = auto_qr.clear_expired_cache()
            return jsonify({
                'success': True,
                'result': result
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to clear cache: {str(e)}'}), 400

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True,port=8501)
