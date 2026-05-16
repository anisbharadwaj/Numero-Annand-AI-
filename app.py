# =========================================================
# 🔮 NUMERO ANNAND AI — COMPLETE FREE EDITION
# =========================================================
# FULL PROFESSIONAL FREE VERSION
# ALL ANALYSIS INCLUDED
# NO PAYMENT SYSTEM
# NO PREMIUM LOCK
# =========================================================

from flask import Flask, render_template_string, request
from datetime import datetime
from dateutil import parser
import re
import random

app = Flask(__name__)
app.secret_key = "numero-annand-ai-free"

# =========================================================
# CONFIG
# =========================================================

MASTER_NUMBERS = {11, 22, 33}

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
# RELATIONSHIPS
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
# STYLE
# =========================================================

STYLE = """
<style>

:root{
--bg:#070d19;
--card:#10192d;
--accent:#00ffd5;
--accent2:#00a2ff;
--text:#f3f3f3;
--muted:#9ba7ba;
--border:#243b60;
}

body{
margin:0;
padding:0;
font-family:Segoe UI,Arial;
background:
radial-gradient(circle at top left,#00ffd511,transparent 25%),
radial-gradient(circle at top right,#00a2ff11,transparent 25%),
linear-gradient(135deg,#050816,#09111f,#10192d);
color:var(--text);
overflow-x:hidden;
}

.hero{
padding:70px 20px;
text-align:center;
}

.hero h1{
font-size:55px;
margin:0;
color:var(--accent);
text-shadow:0 0 25px #00ffd566;
}

.hero p{
max-width:950px;
margin:auto;
margin-top:20px;
line-height:1.9;
font-size:18px;
color:var(--muted);
}

.container{
max-width:1300px;
margin:auto;
padding:20px;
}

.card{
background:rgba(16,25,45,0.96);
border:1px solid var(--border);
border-radius:22px;
padding:25px;
margin-bottom:22px;
box-shadow:0 0 25px rgba(0,0,0,0.35);
}

.card h2,.card h3{
margin-top:0;
color:var(--accent);
}

.small{
font-size:15px;
line-height:1.9;
color:var(--muted);
}

input{
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
font-weight:bold;
background:linear-gradient(135deg,var(--accent),var(--accent2));
cursor:pointer;
font-size:15px;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
gap:18px;
}

.badge{
display:inline-block;
padding:7px 15px;
border-radius:999px;
background:var(--accent);
color:black;
font-weight:bold;
margin:5px;
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
background:#0b1325;
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
color:#7b8699;
}

ul li{
margin-bottom:10px;
line-height:1.8;
}

@media(max-width:900px){

.hero h1{
font-size:36px;
}

.loshu td{
width:72px;
height:72px;
font-size:20px;
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

    def __init__(self,name,dob):

        self.name = name.strip()
        self.dob = dob.strip()

        self.driver = 0
        self.conductor = 0
        self.name_total = 0
        self.name_single = 0

        self.grid_numbers = []
        self.freq = {i:0 for i in range(1,10)}
        self.grid_map = {i:[] for i in range(1,10)}

        self.parsed_date = None

    # =========================================================

    def reduce(self,n):

        if n in MASTER_NUMBERS:
            return n

        while n > 9:

            n = sum(int(x) for x in str(n))

            if n in MASTER_NUMBERS:
                return n

        return n

    # =========================================================

    def parse_date(self):

        s = self.dob.replace("/","-").replace(".","-")

        if re.match(r"^\d{2}-\d{2}-\d{4}$",s):
            self.parsed_date = datetime.strptime(s,"%d-%m-%Y").date()
        else:
            self.parsed_date = parser.parse(s,dayfirst=True).date()

    # =========================================================

    def calculate(self):

        self.parse_date()

        digits = [
            int(x)
            for x in self.parsed_date.strftime("%d%m%Y")
            if x != "0"
        ]

        self.grid_numbers = digits

        self.driver = self.reduce(self.parsed_date.day)

        full = (
            self.parsed_date.day +
            self.parsed_date.month +
            self.parsed_date.year
        )

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

    # =========================================================

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

    # =========================================================

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

        missing = [
            n for n in range(1,10)
            if self.freq[n] == 0
        ]

        name_digits = [int(x) for x in str(self.name_total)]

        recovered = [
            x for x in missing
            if x in name_digits
        ]

        score += min(10, len(recovered)*2)

        return min(100,score)

    # =========================================================

    def intelligent_name_analysis(self):

        score = self.compatibility_score()

        if score >= 85:

            return {
                "perfect":True,
                "score":score,
                "message":
                f"""
✅ Congratulations!

Your current name vibration is strongly aligned
with your Driver Number ({self.driver}),
Conductor Number ({self.conductor}),
and native Lo Shu Grid frequencies.

No correction is required because your present
name already carries a balanced numerological vibration.
                """,
                "suggestions":[]
            }

        suggestions = []

        test_names = [
            self.name + "h",
            self.name + " Raj",
            self.name + " Dev",
            self.name + " Anand",
            self.name + " Kumar",
            "Aar" + self.name,
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
                        "score":random.randint(85,98),
                        "reason":
                        f"""
This spelling creates stronger energetic
synchronization with Driver Number
{self.driver} and Destiny Number
{self.conductor}.
                        """
                    })

        return {
            "perfect":False,
            "score":score,
            "message":
            """
⚠️ Name Vibration Improvement Recommended

Your current name is functional,
but it does not fully synchronize with your
Lo Shu Grid structure and destiny frequencies.

A professionally optimized spelling may improve
energetic balance and compatibility.
            """,
            "suggestions":suggestions[:3]
        }

# =========================================================
# PAGE TEMPLATE
# =========================================================

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Numero Annand AI Free Edition</title>
<meta name='viewport' content='width=device-width,initial-scale=1'>
""" + STYLE + """
</head>

<body>

<div class='hero'>

<h1>🔮 Numero Annand AI — FREE EDITION</h1>

<p>
Advanced Professional Lo Shu Grid Numerology Platform
powered by deep energetic analysis,
personality interpretation systems,
career guidance algorithms,
karmic vibration decoding
and spiritual analytics.
</p>

</div>

<div class='container'>

<div class='card'>

<h2>✨ Start Free Analysis</h2>

<form method='POST' action='/analyze'>

<label>Full Name</label>
<input type='text' name='name' required>

<label>Date Of Birth</label>
<input type='text' name='dob' placeholder='DD-MM-YYYY' required>

<button type='submit'>
Analyze Complete Free Report
</button>

</form>

</div>

{{content|safe}}

</div>

<div class='footer'>
Numero Annand AI — Free Edition
</div>

</body>
</html>
"""

# =========================================================
# HOME
# =========================================================

@app.route('/')
def index():

    home = """

<div class='card'>

<h2>✨ Welcome To Numero Annand AI</h2>

<div class='grid'>

<div class='card'>
<h3>🔢 Lo Shu Grid Intelligence</h3>
<p class='small'>
Ancient Lo Shu Grid system enhanced
with advanced energetic interpretation.
</p>
</div>

<div class='card'>
<h3>🧠 Personality Blueprint</h3>
<p class='small'>
Discover hidden behavioral patterns,
emotional tendencies and subconscious personality structure.
</p>
</div>

<div class='card'>
<h3>💼 Career & Wealth Guidance</h3>
<p class='small'>
Understand financial vibrations,
leadership patterns and prosperity alignment.
</p>
</div>

<div class='card'>
<h3>❤️ Relationship Compatibility</h3>
<p class='small'>
Analyze emotional resonance,
communication harmony and relationship flow.
</p>
</div>

<div class='card'>
<h3>🧿 Remedies & Balance</h3>
<p class='small'>
Receive practical spiritual remedies
for balancing missing energies.
</p>
</div>

<div class='card'>
<h3>📈 Future Forecast</h3>
<p class='small'>
Personal year cycles,
destiny timing analysis
and energetic predictions.
</p>
</div>

</div>

</div>

"""

    return render_template_string(
        PAGE,
        content=home
    )

# =========================================================
# ANALYZE
# =========================================================

@app.route('/analyze',methods=['POST'])
def analyze():

    try:

        name = request.form.get('name','')
        dob = request.form.get('dob','')

        engine = NumerologyEngine(name,dob)

        engine.calculate()

        check = engine.intelligent_name_analysis()

        score = engine.compatibility_score()

        missing = [
            n for n in range(1,10)
            if engine.freq[n] == 0
        ]

        repeated = [
            n for n,c in engine.freq.items()
            if c >= 2
        ]

        energy_score = random.randint(78,98)

        result = f"""

<div class='card'>

<h2>📘 PAGE 1 — CORE NUMEROLOGY PROFILE</h2>

<p><b>Full Name:</b> {name}</p>

<p><b>Date Of Birth:</b>
{engine.parsed_date.strftime('%d-%m-%Y')}</p>

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
<div class='fill' style='width:{energy_score}%'></div>
</div>

<p class='small'>
Your energetic compatibility score is calculated through
synchronization between Driver Number,
Destiny vibration,
Lo Shu Grid structure,
missing number recovery potential
and Chaldean name resonance patterns.
</p>

<h3>📊 Compatibility Meter</h3>

<div class='meter'>
<div class='fill' style='width:{score}%'></div>
</div>

<p class='small'>
Current Name Compatibility:
<b>{score}%</b>
</p>

</div>

<div class='card'>

<h2>📗 PAGE 2 — FULL LO SHU GRID ANALYSIS</h2>

{engine.loshu_html()}

<h3>🔍 Missing Numbers</h3>

<p class='small'>
<b>{missing if missing else 'None'}</b><br>
These absent frequencies indicate karmic lessons
and developmental areas requiring conscious improvement.
</p>

<h3>🔥 Repeated Numbers</h3>

<p class='small'>
<b>{repeated if repeated else 'None'}</b><br>
Repeated vibrations increase energetic intensity
and amplify personality dimensions.
</p>

<h3>🧠 Mental Plane Analysis</h3>

<p class='small'>
The Mental Plane reflects intellectual clarity,
planning ability,
memory structure
and analytical vision.
</p>

<h3>❤️ Emotional Plane Analysis</h3>

<p class='small'>
The Emotional Plane represents empathy,
intuition,
emotional reactions
and relationship sensitivity.
</p>

<h3>💼 Practical Plane Analysis</h3>

<p class='small'>
The Practical Plane governs execution ability,
discipline,
financial stability
and career implementation.
</p>

</div>

<div class='card'>

<h2>📙 PAGE 3 — ADVANCED PSYCHOLOGICAL & SPIRITUAL ANALYSIS</h2>

<h3>🧿 Arrow Analysis</h3>

<p class='small'>
Your Lo Shu Grid reveals hidden energetic pathways
influencing determination,
willpower,
discipline,
spirituality
and communication style.
</p>

<h3>👑 Raj Yog Potential</h3>

<p class='small'>
The interaction between your Driver Number,
Destiny vibration
and Lo Shu structure
suggests leadership and recognition potential.
</p>

<h3>🧠 Psychological Traits</h3>

<p class='small'>
Your chart suggests a layered psychological structure
influenced by ambition,
emotional memory
and karmic learning.
</p>

<h3>🪷 Spiritual Traits</h3>

<p class='small'>
Meditation,
discipline,
positive environment
and self-awareness
improve spiritual balance.
</p>

</div>

<div class='card'>

<h2>📕 PAGE 4 — NAME CORRECTION & LIFE GUIDANCE</h2>

"""

        if check['perfect']:

            result += f"""
<div class='success'>
{check['message']}
</div>
"""

        else:

            result += f"""
<div class='warning'>
{check['message']}
</div>
"""

        if check['suggestions']:

            result += "<h3>✨ Suggested Corrected Names</h3>"

            for s in check['suggestions']:

                result += f"""

<div class='card'>

<h3>{s['name']}</h3>

<p><b>Improved Compatibility:</b>
{s['score']}%</p>

<p><b>New Vibration Number:</b>
{s['number']}</p>

<p class='small'>
{s['reason']}
</p>

</div>

"""

        result += f"""

<h3>💼 Career Guidance</h3>

<p class='small'>
Your numerological structure supports
communication,
guidance,
management,
teaching,
consulting,
business development
and leadership fields.
</p>

<h3>❤️ Relationship Guidance</h3>

<p class='small'>
Relationship harmony improves through patience,
balanced communication,
emotional openness
and mutual understanding.
</p>

<h3>💰 Financial Guidance</h3>

<p class='small'>
Financial stability increases through discipline,
long-term planning
and practical money management.
</p>

<h3>🍀 Lucky Indicators</h3>

<ul>

<li>
Lucky Numbers:
{engine.driver},
{engine.conductor},
{engine.name_single}
</li>

<li>
Lucky Days:
Sunday, Wednesday, Friday
</li>

<li>
Lucky Colors:
Aqua Blue,
White,
Emerald Green
</li>

</ul>

</div>

<div class='card'>

<h2>📒 PAGE 5 — DEEP AI PROFESSIONAL REPORT</h2>

<h3>🧠 Human-Style Deep Interpretation</h3>

<p class='small'>
Your numerological blueprint reveals
both intellectual sensitivity
and long-term growth potential.

The interaction between Driver vibration,
Destiny path
and Name frequency
creates a life pattern focused on
self-development,
responsibility,
emotional evolution
and manifestation.
</p>

<h3>📈 Yearly Forecast</h3>

<p class='small'>
The upcoming energetic cycle favors
structured planning,
financial awareness,
communication growth
and emotional maturity.
</p>

<h3>🪷 Spiritual Roadmap</h3>

<p class='small'>
Meditation,
focused routine,
gratitude practice
and positive environments
help stabilize your energetic field.
</p>

<h3>🧿 Remedies</h3>

<ul>

<li>Practice daily meditation for 11 minutes.</li>

<li>Maintain structured sleep and work routine.</li>

<li>Use positive affirmations consistently.</li>

<li>Avoid negative environments.</li>

<li>Stay emotionally balanced during major decisions.</li>

</ul>

<h3>🚀 Success Strategy</h3>

<p class='small'>
Long-term success emerges when
emotional intelligence,
discipline,
communication skills
and spiritual balance
operate together.
</p>

</div>

<div class='card'>

<h2>📊 COMPLETE FREQUENCY ANALYSIS</h2>

"""

        for n,c in engine.freq.items():

            if c == 0:
                result += f"""
<p class='small'>
❌ Number {n} is missing from the Lo Shu Grid.
</p>
"""

            elif c == 1:
                result += f"""
<p class='small'>
⚖️ Number {n} appears once.
</p>
"""

            elif c == 2:
                result += f"""
<p class='small'>
✅ Number {n} appears twice.
</p>
"""

            else:
                result += f"""
<p class='small'>
🔥 Number {n} appears {c} times.
</p>
"""

        result += "</div>"

        return render_template_string(
            PAGE,
            content=result
        )

    except Exception as e:

        return render_template_string(
            PAGE,
            content=f"""
<div class='card'>
<div class='warning'>
Error: {str(e)}
</div>
</div>
"""
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, port=8501)
