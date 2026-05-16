# =========================================================
# 🔮 NUMERO ANNAND AI — COMPLETE FREE MULTI-LANGUAGE EDITION
# =========================================================
# ENGLISH + HINDI + ASSAMESE
# ALL ANALYSIS INCLUDED
# NO PAYMENT SYSTEM
# CONSULT LINK + WHATSAPP GROUP INCLUDED
# =========================================================

from flask import Flask, render_template_string, request
from datetime import datetime
from dateutil import parser
import re
import random

app = Flask(__name__)
app.secret_key = "numero-annand-ai-free"

# =========================================================
# LINKS
# =========================================================

WHATSAPP_CONSULT_LINK = "https://wa.me/917099805039"
WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/C5g8MVpA0SYASAyrZfsrtJ?mode=gi_t"

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
# TRANSLATIONS
# =========================================================

TRANSLATIONS = {

'en':{
'title':'Numero Annand AI Free Edition',
'name':'Full Name',
'dob':'Date Of Birth',
'lang':'Select Language',
'btn':'Analyze Complete Report',
'consult':'Consult with Annand Sarma',
'group':'Join WhatsApp Group',
'analysis':'Available Analysis',
'welcome':'Welcome To Numero Annand AI',
'p1':'PAGE 1 — CORE NUMEROLOGY PROFILE',
'p2':'PAGE 2 — FULL LO SHU GRID ANALYSIS',
'p3':'PAGE 3 — ADVANCED PSYCHOLOGICAL & SPIRITUAL ANALYSIS',
'p4':'PAGE 4 — NAME CORRECTION & LIFE GUIDANCE',
'p5':'PAGE 5 — DEEP AI PROFESSIONAL REPORT'
},

'hi':{
'title':'न्यूमेरो आनंद एआई फ्री संस्करण',
'name':'पूरा नाम',
'dob':'जन्म तिथि',
'lang':'भाषा चुनें',
'btn':'पूर्ण रिपोर्ट देखें',
'consult':'आनंद शर्मा से संपर्क करें',
'group':'व्हाट्सएप ग्रुप जॉइन करें',
'analysis':'उपलब्ध विश्लेषण',
'welcome':'न्यूमेरो आनंद एआई में आपका स्वागत है',
'p1':'पेज 1 — मुख्य अंकज्योतिष प्रोफाइल',
'p2':'पेज 2 — पूर्ण लो शू ग्रिड विश्लेषण',
'p3':'पेज 3 — मनोवैज्ञानिक और आध्यात्मिक विश्लेषण',
'p4':'पेज 4 — नाम सुधार और जीवन मार्गदर्शन',
'p5':'पेज 5 — गहन एआई रिपोर्ट'
},

'as':{
'title':'নিউমেৰো আনন্দ এআই ফ্ৰী সংস্কৰণ',
'name':'সম্পূৰ্ণ নাম',
'dob':'জন্ম তাৰিখ',
'lang':'ভাষা বাছনি কৰক',
'btn':'সম্পূৰ্ণ ৰিপৰ্ট চাওক',
'consult':'আনন্দ শৰ্মাৰ সৈতে যোগাযোগ কৰক',
'group':'হোৱাটছএপ গ্ৰুপ যোগদান কৰক',
'analysis':'উপলব্ধ বিশ্লেষণ',
'welcome':'নিউমেৰো আনন্দ এআইলৈ স্বাগতম',
'p1':'পৃষ্ঠা ১ — মূল সংখ্যাতত্ত্ব প্ৰফাইল',
'p2':'পৃষ্ঠা ২ — সম্পূৰ্ণ লো শ্বু গ্ৰীড বিশ্লেষণ',
'p3':'পৃষ্ঠা ৩ — মানসিক আৰু আধ্যাত্মিক বিশ্লেষণ',
'p4':'পৃষ্ঠা ৪ — নাম সংশোধন আৰু জীৱন নিৰ্দেশনা',
'p5':'পৃষ্ঠা ৫ — গভীৰ এআই ৰিপৰ্ট'
}

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
}

.hero p{
max-width:900px;
margin:auto;
margin-top:20px;
line-height:1.9;
font-size:18px;
color:var(--muted);
}

.main{
display:flex;
gap:20px;
padding:20px;
}

.sidebar{
width:340px;
background:#10192d;
border:1px solid var(--border);
border-radius:22px;
padding:24px;
height:fit-content;
}

.content{
flex:1;
}

.card{
background:#10192d;
border:1px solid var(--border);
border-radius:22px;
padding:25px;
margin-bottom:22px;
}

.card h2,.card h3{
color:var(--accent);
margin-top:0;
}

.small{
line-height:1.9;
color:var(--muted);
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
font-weight:bold;
background:linear-gradient(135deg,var(--accent),var(--accent2));
cursor:pointer;
font-size:15px;
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

.footer{
text-align:center;
padding:35px;
color:#7b8699;
}

a{
text-decoration:none;
}

@media(max-width:900px){

.main{
flex-direction:column;
}

.sidebar{
width:100%;
}

.hero h1{
font-size:36px;
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

        self.freq = {i:0 for i in range(1,10)}
        self.grid_map = {i:[] for i in range(1,10)}

    def reduce(self,n):

        if n in MASTER_NUMBERS:
            return n

        while n > 9:

            n = sum(int(x) for x in str(n))

            if n in MASTER_NUMBERS:
                return n

        return n

    def parse_date(self):

        s = self.dob.replace("/","-").replace(".","-")
        return parser.parse(s,dayfirst=True).date()

    def calculate(self):

        d = self.parse_date()

        digits = [
            int(x)
            for x in d.strftime("%d%m%Y")
            if x != "0"
        ]

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
# PAGE TEMPLATE
# =========================================================

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>{{t.title}}</title>
<meta name='viewport' content='width=device-width,initial-scale=1'>
""" + STYLE + """
</head>

<body>

<div class='hero'>

<h1>🔮 Numero Annand AI</h1>

<p>
Advanced Professional Lo Shu Grid Numerology Platform
with Deep AI Analysis,
Personality Blueprint,
Name Correction,
Career Guidance,
Relationship Insights,
Spiritual Analysis
and Future Prediction System.
</p>

</div>

<div class='main'>

<div class='sidebar'>

<div class='card'>

<h2>{{t.welcome}}</h2>

<form method='POST' action='/analyze'>

<label>{{t.name}}</label>
<input type='text' name='name' required>

<label>{{t.dob}}</label>
<input type='text' name='dob' placeholder='DD-MM-YYYY' required>

<label>{{t.lang}}</label>

<select name='lang'>

<option value='en'>English</option>
<option value='hi'>Hindi</option>
<option value='as'>Assamese</option>

</select>

<button type='submit'>{{t.btn}}</button>

</form>

</div>

<div class='card'>

<h3>📞 {{t.consult}}</h3>

<a href='""" + WHATSAPP_CONSULT_LINK + """' target='_blank'>
<button>+91 7099805039</button>
</a>

</div>

<div class='card'>

<h3>👥 {{t.group}}</h3>

<a href='""" + WHATSAPP_GROUP_LINK + """' target='_blank'>
<button>Open WhatsApp Group</button>
</a>

</div>

<div class='card'>

<h3>📋 {{t.analysis}}</h3>

<ul class='small'>

<li>Lo Shu Grid Analysis</li>
<li>Name Correction</li>
<li>Compatibility Analysis</li>
<li>Career Guidance</li>
<li>Relationship Guidance</li>
<li>Financial Guidance</li>
<li>Spiritual Analysis</li>
<li>Psychological Analysis</li>
<li>Lucky Number Analysis</li>
<li>Future Forecast</li>

</ul>

</div>

</div>

<div class='content'>
{{content|safe}}
</div>

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

    t = TRANSLATIONS['en']

    return render_template_string(
        PAGE,
        content="",
        t=t
    )

# =========================================================
# ANALYZE
# =========================================================

@app.route('/analyze',methods=['POST'])
def analyze():

    try:

        name = request.form.get('name')
        dob = request.form.get('dob')
        lang = request.form.get('lang','en')

        t = TRANSLATIONS.get(lang,TRANSLATIONS['en'])

        engine = NumerologyEngine(name,dob)
        engine.calculate()

        result = f"""

<div class='card'>

<h2>{t['p1']}</h2>

<p><b>Name:</b> {name}</p>

<p><b>DOB:</b> {dob}</p>

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

<h2>{t['p2']}</h2>

{engine.loshu_html()}

<p class='small'>
Detailed Lo Shu Grid analysis based on energetic frequencies,
mental plane,
emotional plane,
practical plane,
repeated numbers
and missing numbers.
</p>

</div>

<div class='card'>

<h2>{t['p3']}</h2>

<p class='small'>

Your chart reflects psychological depth,
spiritual learning,
emotional sensitivity,
leadership potential,
intuition
and karmic growth cycles.

</p>

</div>

<div class='card'>

<h2>{t['p4']}</h2>

<p class='small'>

Your name vibration shows compatibility
with Driver and Destiny numbers.

Improved spellings may increase energetic balance.

</p>

</div>

<div class='card'>

<h2>{t['p5']}</h2>

<p class='small'>

Your advanced numerology structure indicates
long-term growth potential,
career progress,
relationship maturity,
financial development
and spiritual evolution.

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
            content=f"<div class='card'><div class='warning'>{str(e)}</div></div>",
            t=TRANSLATIONS['en']
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True,port=8501)
