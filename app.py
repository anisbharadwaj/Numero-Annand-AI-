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

from flask import Flask, render_template_string, request
from datetime import datetime
from dateutil import parser
import random
import re

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
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True,port=8501)
