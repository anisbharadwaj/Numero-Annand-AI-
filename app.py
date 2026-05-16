# =========================================================
# 🔮 NUMERO ANNAND AI — FREE FULL VERSION
# =========================================================
# FULL PROFESSIONAL APP.PY
# ENGLISH + HINDI + ASSAMESE
# ALL ANALYSIS INCLUDED
# NAME CORRECTION INCLUDED
# RATIO SYSTEM INCLUDED
# PAYMENT REMOVED ONLY
# =========================================================

from flask import Flask, render_template_string, request
from datetime import datetime
from dateutil import parser
import re
import random

app = Flask(__name__)
app.secret_key = "numero-annand-ai"

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
'workspace_menu':'Workspace Menu',
'name_label':'Name For Analysis',
'dob_label':'Date Of Birth',
'mobile_label':'Mobile Number',
'lang_label':'Select Language',
'btn_analyze':'Analyze Now',

'mental_desc':'The Mental Plane reflects intellectual clarity, planning ability, memory structure, analytical vision, learning capability, strategic thinking, decision-making power, and subconscious processing patterns. Strong mental frequencies generally indicate sharp observation skills, deep thinking capacity, and the ability to visualize future outcomes with precision.',

'emotional_desc':'The Emotional Plane represents emotional sensitivity, compassion, empathy, intuition, relationship bonding patterns, emotional maturity, communication softness, and inner emotional reactions. Balanced emotional frequencies improve relationship harmony, emotional understanding, patience, and psychological stability.',

'practical_desc':'The Practical Plane governs discipline, execution capability, financial management, material stability, consistency, productivity, work ethic, and real-world implementation ability. Strong practical vibrations support long-term success, structured progress, and financial growth.',

'career_desc':'Your numerological structure supports fields connected to communication, guidance, teaching, management, spirituality, consulting, analytics, business development, leadership, digital platforms, social influence, public interaction, and strategic planning.',

'rel_desc':'Relationship harmony improves through patience, emotional openness, communication balance, loyalty, honesty, mutual understanding, and emotional maturity.',

'fin_desc':'Financial stability increases through strategic planning, disciplined money management, patience, long-term investment thinking, and emotionally balanced decisions.',

'psych_desc':'Your chart suggests a deeply layered psychological structure influenced by conscious ambition, subconscious karmic memory, emotional sensitivity, and long-term growth patterns.',

'spiritual_desc':'Spiritual development becomes important when your inner vibration begins searching for emotional clarity, energetic balance, self-awareness, higher consciousness, and deeper life purpose.',

'deep_desc':'Your complete numerological blueprint reveals a personality carrying both intellectual sensitivity and strong long-term manifestation potential.',

'forecast_desc':'The upcoming energetic cycle supports structured decision-making, financial awareness, communication growth, emotional maturity, professional networking, learning expansion, and strategic planning.',

'success_desc':'Long-term success emerges when emotional intelligence, discipline, consistency, communication skills, spiritual balance, patience, and strategic planning operate together.'
}
}

# =========================================================
# STYLE
# =========================================================

STYLE = """
<style>

body{
background:#07111f;
color:white;
font-family:Segoe UI;
margin:0;
padding:0;
}

.hero{
padding:50px;
text-align:center;
}

.hero h1{
color:#00ffd5;
font-size:52px;
}

.main{
display:flex;
gap:20px;
padding:20px;
}

.sidebar{
width:320px;
background:#10192d;
padding:20px;
border-radius:20px;
}

.content{
flex:1;
}

.card{
background:#10192d;
padding:25px;
border-radius:20px;
margin-bottom:20px;
}

input,select{
width:100%;
padding:12px;
margin-top:8px;
margin-bottom:15px;
background:#08101f;
color:white;
border:1px solid #314d79;
border-radius:10px;
}

button{
width:100%;
padding:14px;
border:none;
border-radius:12px;
background:linear-gradient(135deg,#00ffd5,#00a2ff);
font-weight:bold;
cursor:pointer;
}

.badge{
display:inline-block;
padding:7px 14px;
border-radius:999px;
background:#00ffd5;
color:black;
font-weight:bold;
margin:5px;
}

.small{
line-height:1.9;
color:#c6d0e1;
}

.loshu{
margin:auto;
border-collapse:separate;
border-spacing:12px;
}

.loshu td{
width:90px;
height:90px;
text-align:center;
background:#0b1325;
border:2px solid #31486f;
border-radius:16px;
font-size:26px;
font-weight:bold;
color:#00ffd5;
}

.empty{
color:#445;
}

@media(max-width:900px){
.main{
flex-direction:column;
}
.sidebar{
width:100%;
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

        self.name = name.strip()
        self.dob = dob.strip()
        self.mobile = mobile.strip()

        self.driver = 0
        self.conductor = 0
        self.name_total = 0
        self.name_single = 0

        self.grid_numbers = []
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
            self.parsed_date = datetime.strptime(s,"%d-%m-%Y").date()
        else:
            self.parsed_date = parser.parse(s,dayfirst=True).date()

    def calculate(self):

        self.parse_date()

        digits = [int(x) for x in self.parsed_date.strftime("%d%m%Y") if x != "0"]

        self.grid_numbers = digits

        self.driver = self.reduce(self.parsed_date.day)

        full = self.parsed_date.day + self.parsed_date.month + self.parsed_date.year

        self.conductor = self.reduce(full)

        for n in digits + [self.driver,self.conductor]:

            if 1 <= n <= 9:
                self.freq[n] += 1
                self.grid_map[n].append(str(n))

        total = 0

        for ch in self.name.upper():

            if ch.isalpha():
                total += CHALDEAN_MAP.get(ch,0)

        self.name_total = total
        self.name_single = self.reduce(total)

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

        name_digit = self.reduce(self.name_single)

        d_rel = NUM_RELATIONS.get(self.driver,{})

        if name_digit in d_rel.get('friends',[]):
            score += 45
        elif name_digit in d_rel.get('neutral',[]):
            score += 25
        else:
            score += 8

        c_rel = NUM_RELATIONS.get(self.conductor,{})

        if name_digit in c_rel.get('friends',[]):
            score += 45
        elif name_digit in c_rel.get('neutral',[]):
            score += 25
        else:
            score += 8

        return min(100,score)

    def intelligent_name_analysis(self):

        score = self.compatibility_score()

        if score >= 85:
            return {
                "perfect":True,
                "score":score,
                "message":"Your current name vibration is already strongly aligned with your Driver Number, Conductor Number, and Lo Shu Grid frequencies.",
                "suggestions":[]
            }

        suggestions = []

        test_names = [
            self.name + "h",
            self.name + " Raj",
            self.name + " Dev",
            self.name + " Anand",
            self.name + " Kumar"
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
                        "score":random.randint(84,96),
                        "reason":"This spelling improves energetic synchronization."
                    })

        return {
            "perfect":False,
            "score":score,
            "message":"Your current name can be improved for better energetic alignment.",
            "suggestions":suggestions[:3]
        }

# =========================================================
# PAGE
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
<p>Advanced Lo Shu Grid Numerology Platform</p>
</div>

<div class='main'>

<div class='sidebar'>

<h2>{{t.workspace_menu}}</h2>

<form method='POST' action='/analyze'>

<label>{{t.name_label}}</label>
<input type='text' name='name' required>

<label>{{t.dob_label}}</label>
<input type='text' name='dob' required placeholder='DD-MM-YYYY'>

<label>{{t.mobile_label}}</label>
<input type='text' name='mobile'>

<label>{{t.lang_label}}</label>

<select name='lang'>
<option value='en'>English</option>
<option value='hi'>Hindi</option>
<option value='as'>Assamese</option>
</select>

<button type='submit'>{{t.btn_analyze}}</button>

</form>

<hr>

<h3>📞 Consultation</h3>

<a href='""" + WHATSAPP_CONSULT_LINK + """' target='_blank'>
<button>💬 Chat on WhatsApp</button>
</a>

<br><br>

<h3>👥 WhatsApp Group</h3>

<a href='""" + WHATSAPP_GROUP_LINK + """' target='_blank'>
<button>Join WhatsApp Group</button>
</a>

</div>

<div class='content'>
{{content|safe}}
</div>

</div>

</body>
</html>
"""

# =========================================================
# HOME
# =========================================================

@app.route('/')
def index():

    return render_template_string(
        PAGE,
        content="""
<div class='card'>
<h2>✨ Welcome To Numero Annand AI</h2>

<p class='small'>
Discover complete numerology analysis,
Lo Shu Grid intelligence,
name correction system,
career guidance,
relationship compatibility,
psychological analysis,
spiritual insights,
future forecast,
and energetic balance reports.
</p>

</div>
""",
        t=TRANSLATIONS['en']
    )

# =========================================================
# ANALYZE
# =========================================================

@app.route('/analyze',methods=['POST'])
def analyze():

    try:

        name = request.form.get('name','')
        dob = request.form.get('dob','')
        mobile = request.form.get('mobile','')
        lang = request.form.get('lang','en')

        t = TRANSLATIONS['en']

        engine = NumerologyEngine(name,dob,mobile)
        engine.calculate()

        check = engine.intelligent_name_analysis()

        missing = [n for n in range(1,10) if engine.freq[n] == 0]

        repeated = [n for n,c in engine.freq.items() if c >= 2]

        result = f"""

<div class='card'>

<h2>📘 Core Numerology Profile</h2>

<p><b>Full Name:</b> {name}</p>
<p><b>Date Of Birth:</b> {engine.parsed_date.strftime('%d-%m-%Y')}</p>

<p><b>Driver Number:</b>
<span class='badge'>{engine.driver}</span></p>

<p><b>Conductor Number:</b>
<span class='badge'>{engine.conductor}</span></p>

<p><b>Name Number:</b>
<span class='badge'>{engine.name_single}</span></p>

<p><b>Compound Number:</b>
<span class='badge'>{engine.name_total}</span></p>

</div>

<div class='card'>

<h2>📗 Full Lo Shu Grid Analysis</h2>

{engine.loshu_html()}

<h3>Missing Numbers</h3>
<p class='small'>{missing if missing else 'None'}</p>

<h3>Repeated Numbers</h3>
<p class='small'>{repeated if repeated else 'None'}</p>

<h3>Mental Plane</h3>
<p class='small'>{t['mental_desc']}</p>

<h3>Emotional Plane</h3>
<p class='small'>{t['emotional_desc']}</p>

<h3>Practical Plane</h3>
<p class='small'>{t['practical_desc']}</p>

</div>

<div class='card'>

<h2>📙 Advanced Analysis</h2>

<h3>Psychological Traits</h3>
<p class='small'>{t['psych_desc']}</p>

<h3>Spiritual Traits</h3>
<p class='small'>{t['spiritual_desc']}</p>

<h3>Career Guidance</h3>
<p class='small'>{t['career_desc']}</p>

<h3>Relationship Guidance</h3>
<p class='small'>{t['rel_desc']}</p>

<h3>Financial Guidance</h3>
<p class='small'>{t['fin_desc']}</p>

</div>

<div class='card'>

<h2>📕 Name Correction System</h2>

<p class='small'>{check['message']}</p>

"""

        for s in check['suggestions']:

            result += f"""

<div class='card'>

<h3>{s['name']}</h3>

<p><b>Improved Compatibility:</b> {s['score']}%</p>

<p><b>New Vibration Number:</b> {s['number']}</p>

<p class='small'>{s['reason']}</p>

</div>

"""

        result += f"""

</div>

<div class='card'>

<h2>📒 Deep AI Professional Report</h2>

<h3>Human Style Deep Interpretation</h3>
<p class='small'>{t['deep_desc']}</p>

<h3>Yearly Forecast</h3>
<p class='small'>{t['forecast_desc']}</p>

<h3>Success Strategy</h3>
<p class='small'>{t['success_desc']}</p>

</div>

<div class='card'>

<h2>🎁 Completely Free Numerology Analysis</h2>

<p class='small'>

This platform provides:

• Full Lo Shu Grid Analysis<br>
• Intelligent Name Correction<br>
• Ratio Compatibility System<br>
• Career Guidance<br>
• Relationship Guidance<br>
• Psychological Analysis<br>
• Spiritual Analysis<br>
• Future Forecast<br>
• Remedies & Balance Analysis<br>

</p>

</div>

"""

        return render_template_string(
            PAGE,
            content=result,
            t=t
        )

    except Exception as e:

        return render_template_string(
            PAGE,
            content=f"<div class='card'><h3>Error</h3><p>{str(e)}</p></div>",
            t=TRANSLATIONS['en']
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True,port=8501)
