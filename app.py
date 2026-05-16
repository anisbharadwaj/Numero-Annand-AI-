from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash
from datetime import datetime, date
from dateutil import parser
import re
import math
import random

app = Flask(__name__)
app.secret_key = "numero-annand-ai-free-secure-key"

# -------------------------------------------------------------------------
# CORE NUMEROLOGY ENGINE (LO SHU GRID & CHALDEAN LOGIC)
# -------------------------------------------------------------------------

def calculate_single_digit(value):
    """Reduces any number or digit string down to a single root number (1-9)."""
    while len(str(value)) > 1:
        value = sum(int(digit) for digit in str(value) if digit.isdigit())
    return value

def get_chaldean_value(name):
    """Calculates the Chaldean Name Number total based on standard mappings."""
    mapping = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'K': 2, 'R': 2,
        'C': 3, 'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5, 'X': 5,
        'U': 6, 'V': 6, 'W': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    name = name.upper()
    total = 0
    for char in name:
        if char in mapping:
            total += mapping[char]
    return total

def analyze_numerology(name, dob_str):
    """Generates full grid mapping, root numbers, and analytics."""
    try:
        parsed_date = parser.parse(dob_str)
        day = parsed_date.day
        month = parsed_date.month
        year = parsed_date.year
    except Exception:
        return None

    # Driver & Conductor calculations
    driver = calculate_single_digit(day)
    full_sum = sum(int(d) for d in f"{day:02d}{month:02d}{year}" if d.isdigit())
    conductor = calculate_single_digit(full_sum)

    # Populating the Lo Shu Grid matrix string representation
    full_dob_digits = f"{day}{month}{year}"
    grid_counts = {str(i): full_dob_digits.count(str(i)) for i in range(1, 10)}
    
    # Calculate Chaldean metrics
    name_total = get_chaldean_value(name)
    name_root = calculate_single_digit(name_total)

    # Simple sample text responses for insights
    insights = [
        f"Your Driver Number ({driver}) brings strong foundational characteristics to your personality alignment.",
        f"Conductor Number ({conductor}) indicates that your core destiny timeline emphasizes natural growth pathways.",
        f"The Chaldean configuration for '{name}' sums up to {name_total} (Root: {name_root}), balancing your expressions."
    ]

    return {
        "driver": driver,
        "conductor": conductor,
        "grid_counts": grid_counts,
        "name_total": name_total,
        "name_root": name_root,
        "insights": insights
    }

# -------------------------------------------------------------------------
# ROUTING & REVENUE-FREE TEMPLATES
# -------------------------------------------------------------------------

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Numero Annand AI</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { max-width: 600px; width: 100%; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }
        h1 { color: #38bdf8; text-align: center; margin-bottom: 5px; }
        p.subtitle { text-align: center; color: #94a3b8; margin-top: 0; font-size: 0.95em; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #cbd5e1; font-weight: 600; }
        input[type="text"], input[type="date"] { width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 14px; background: #0ea5e9; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 1em; transition: background 0.2s; }
        button:hover { background: #0284c7; }
        .result-box { background: #0f172a; padding: 20px; border-radius: 8px; margin-top: 25px; border-left: 4px solid #38bdf8; }
        .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 20px 0; max-width: 300px; margin-left: auto; margin-right: auto; }
        .grid-cell { background: #334155; aspect-ratio: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 6px; font-size: 1.2em; font-weight: bold; }
        .grid-cell span { font-size: 0.6em; color: #94a3b8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Numero Annand AI</h1>
        <p class="subtitle">Instant & Free Scientific Numerology Evaluation</p>
        
        <form method="POST">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="name" placeholder="Enter your name" required value="{{ request.form.get('name', '') }}">
            </div>
            <div class="form-group">
                <label>Date of Birth</label>
                <input type="date" name="dob" required value="{{ request.form.get('dob', '') }}">
            </div>
            <button type="submit">Analyze Blueprint Now</button>
        </form>

        {% if result %}
        <div class="result-box">
            <h3>Analysis for {{ name }}</h3>
            <p><strong>Driver Number:</strong> {{ result.driver }}</p>
            <p><strong>Conductor Number:</strong> {{ result.conductor }}</p>
            <p><strong>Chaldean Name Number:</strong> {{ result.name_total }} (Root: {{ result.name_root }})</p>
            
            <h4 style="text-align: center; color: #38bdf8; margin-top: 20px;">Lo Shu Grid Layout</h4>
            <div class="grid-container">
                <div class="grid-cell">{{ '4 ' * result.grid_counts['4'] if result.grid_counts['4'] > 0 else '-' }}<span>4</span></div>
                <div class="grid-cell">{{ '9 ' * result.grid_counts['9'] if result.grid_counts['9'] > 0 else '-' }}<span>9</span></div>
                <div class="grid-cell">{{ '2 ' * result.grid_counts['2'] if result.grid_counts['2'] > 0 else '-' }}<span>2</span></div>
                <div class="grid-cell">{{ '3 ' * result.grid_counts['3'] if result.grid_counts['3'] > 0 else '-' }}<span>3</span></div>
                <div class="grid-cell">{{ '5 ' * result.grid_counts['5'] if result.grid_counts['5'] > 0 else '-' }}<span>5</span></div>
                <div class="grid-cell">{{ '7 ' * result.grid_counts['7'] if result.grid_counts['7'] > 0 else '-' }}<span>7</span></div>
                <div class="grid-cell">{{ '8 ' * result.grid_counts['8'] if result.grid_counts['8'] > 0 else '-' }}<span>8</span></div>
                <div class="grid-cell">{{ '1 ' * result.grid_counts['1'] if result.grid_counts['1'] > 0 else '-' }}<span>1</span></div>
                <div class="grid-cell">{{ '6 ' * result.grid_counts['6'] if result.grid_counts['6'] > 0 else '-' }}<span>6</span></div>
            </div>

            <h4>AI Interpretations:</h4>
            <ul>
                {% for insight in result.insights %}
                <li>{{ insight }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    name = ""
    if request.method == "POST":
        name = request.form.get("name")
        dob = request.form.get("dob")
        result = analyze_numerology(name, dob)
    return render_template_string(HTML_LAYOUT, result=result, name=name)

if __name__ == "__main__":
    app.run(debug=True)
