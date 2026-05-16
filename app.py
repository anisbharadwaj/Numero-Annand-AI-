# =========================================================
# 🔮 NUMERO ANNAND AI — FREE EDITION
# =========================================================
# FULL FREE VERSION — NO PAYMENT / NO PREMIUM LOCK
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

body{
margin:0;
padding:0;
font-family:Segoe UI;
background:#07111f;
color:white;
}

.hero{
padding:50px 20px;
text-align:center;
background:linear-gradient(135deg,#07111f,#0f1f35);
}

.hero h1{
font-size:48px;
color:#00ffd5;
margin:0;
}

.hero p{
max-width:900px;
margin:auto;
margin-top:15px;
line-height:1.8;
color:#c5d0dd;
}

.container{
max-width:1200px;
margin:auto;
padding:20px;
}

.card{
background:#10192d;
border:1px solid #243b60;
border-radius:20px;
padding:25px;
margin-bottom:25px;
}

.card h2,.card h3{
color:#00ffd5;
margin-top:0;
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
box-sizing:border-box;
}

button{
width:100%;
padding:14px;
border:none;
border-radius:12px;
background:linear-gradient(135deg,#00ffd5,#00a2ff);
font-weight:bold;
cursor:pointer;
font-size:16px;
}

.small{
line-height:1.8;
color:#c7d3df;
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

.loshu{
margin:auto;
border-collapse:separate;
border-spacing:12px;
}

.loshu td{
width:90px;
height:90px;
background:#08101f;
border:2px solid #31486f;
border-radius:18px;
text-align:center;
font-size:28px;
font-weight:bold;
color:#00ffd5;
}

.empty{
color:#445 !important;
}

.footer{
text-align:center;
padding:30px;
color:#7b8699;
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
        self.name = name
        self.dob = dob

        self.driver = 0
        self.conductor = 0
        self.name_total = 0
        self.name_single = 0

        self.freq = {i:0 for i in range(1,10)}
        self.grid_map = {i:[] for i in range(1,10)}

    def reduce(self,n):
        while n > 9 and n not in MASTER_NUMBERS:
            n = sum(int(x) for x in str(n))
        return n

    def parse_date(self):
        s = self.dob.replace("/","-").replace(".","-")
        return parser.parse(s,dayfirst=True).date()

    def calculate(self):

        d = self.parse_date()

        digits = [int(x) for x in d.strftime("%d%m%Y") if x != "0"]

        self.driver = self.reduce(d.day)

        full = d.day + d.month + d.year
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

# =========================================================
# PAGE
# =========================================================

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Numero Annand AI Free</title>
<meta name='viewport' content='width=device-width,initial-scale=1'>
""" + STYLE + """
</head>

<body>

<div class='hero'>
<h1>🔮 Numero Annand AI — FREE EDITION</h1>
<p>
Complete Free Numerology Analysis Platform with Lo Shu Grid,
Personality Blueprint, Career Guidance, Spiritual Analysis,
Relationship Insights and Future Forecast System.
</p>
</div>

<div class='container'>

<div class='card'>
<h2>🔍 Start Free Analysis</h2>

<form method='POST' action='/analyze'>

<label>Full Name</label>
<input type='text' name='name' required>

<label>Date Of Birth</label>
<input type='text' name='dob' placeholder='DD-MM-YYYY' required>

<button type='submit'>Analyze Now — 100% Free</button>

</form>
</div>

{{content|safe}}

</div>

<div class='footer'>
Numero Annand AI Free Edition
</div>

</body>
</html>
"""

# =========================================================
# HOME
# =========================================================

@app.route('/')
def home():

    return render_template_string(
        PAGE,
        content=""
    )

# =========================================================
# ANALYZE
# =========================================================

@app.route('/analyze', methods=['POST'])
def analyze():

    try:

        name = request.form.get('name')
        dob = request.form.get('dob')

        engine = NumerologyEngine(name,dob)
        engine.calculate()

        missing = [n for n in range(1,10) if engine.freq[n] == 0]
        repeated = [n for n,c in engine.freq.items() if c >= 2]

        energy = random.randint(80,99)

        result = f"""

<div class='card'>

<h2>📘 CORE NUMEROLOGY PROFILE</h2>

<p><b>Name:</b> {name}</p>
<p><b>Date Of Birth:</b> {dob}</p>

<p><b>Driver Number:</b> <span class='badge'>{engine.driver}</span></p>

<p><b>Conductor Number:</b> <span class='badge'>{engine.conductor}</span></p>

<p><b>Name Number:</b> <span class='badge'>{engine.name_single}</span></p>

<p><b>Compound Name Value:</b> <span class='badge'>{engine.name_total}</span></p>

<h3>⚡ Energy Score: {energy}%</h3>

<p class='small'>
Your chart shows strong energetic patterns connected with personality,
thinking style, emotions, destiny path and karmic learning.
</p>

</div>

<div class='card'>

<h2>📗 FULL LO SHU GRID</h2>

{engine.loshu_html()}

<h3>🔍 Missing Numbers</h3>

<p class='small'>
{missing if missing else "No missing numbers found."}
</p>

<h3>🔥 Repeated Numbers</h3>

<p class='small'>
{repeated if repeated else "No repeated numbers found."}
</p>

</div>

<div class='card'>

<h2>🧠 PERSONALITY ANALYSIS</h2>

<p class='small'>
Your numerology profile indicates a personality influenced by emotional
sensitivity, practical thinking and long-term growth potential.
You naturally seek stability, recognition and meaningful progress.
</p>

<h3>💼 Career Guidance</h3>

<p class='small'>
Suitable fields include communication, management, business,
guidance, teaching, spirituality, consulting and leadership roles.
</p>

<h3>❤️ Relationship Guidance</h3>

<p class='small'>
Relationship harmony improves through emotional openness,
balanced communication and patience.
</p>

<h3>💰 Financial Guidance</h3>

<p class='small'>
Financial stability grows through discipline,
strategic planning and consistency.
</p>

</div>

<div class='card'>

<h2>🪷 Spiritual & Future Analysis</h2>

<h3>📈 Future Forecast</h3>

<p class='small'>
Upcoming cycles indicate opportunities for self-growth,
career improvements and emotional maturity.
</p>

<h3>🧿 Remedies</h3>

<ul class='small'>
<li>Practice meditation daily.</li>
<li>Maintain disciplined routine.</li>
<li>Avoid negative environments.</li>
<li>Use positive affirmations consistently.</li>
</ul>

<h3>🍀 Lucky Indicators</h3>

<ul class='small'>
<li>Lucky Numbers: {engine.driver}, {engine.conductor}, {engine.name_single}</li>
<li>Lucky Days: Sunday, Wednesday, Friday</li>
<li>Lucky Colors: Aqua Blue, White, Emerald Green</li>
</ul>

</div>

"""

        return render_template_string(
            PAGE,
            content=result
        )

    except Exception as e:

        return render_template_string(
            PAGE,
            content=f"<div class='card'><h3>Error:</h3><p>{str(e)}</p></div>"
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, port=8501)
