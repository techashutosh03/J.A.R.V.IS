#!/usr/bin/env python3

import streamlit as st
import subprocess
import webbrowser
import datetime
import random
import time
import os
import json
import psutil
from pathlib import Path

# ===== PAGE CONFIG (MUST BE FIRST) =====
st.set_page_config(
    page_title="JARVIS — Ultimate AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

home = str(Path.home())

# ===== INJECT FULL JARVIS CSS =====
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>

/* ===== GLOBAL RESET ===== */
:root {
    --cyan: #00d4ff;
    --cyan-dim: rgba(0,212,255,0.12);
    --cyan-glow: rgba(0,212,255,0.4);
    --orange: #ff6a00;
    --orange-dim: rgba(255,106,0,0.12);
    --bg: #020810;
    --panel: rgba(0,20,40,0.9);
    --grid: rgba(0,212,255,0.04);
    --text: #a8d8ea;
    --text-dim: rgba(168,216,234,0.5);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Animated grid background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridMove 20s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes gridMove {
    0% { background-position: 0 0; }
    100% { background-position: 60px 60px; }
}

/* Scanlines */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* Hide streamlit branding */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], .stDeployButton { display: none !important; }

/* Main content area */
[data-testid="stMain"] > div {
    padding: 1rem 1.5rem !important;
}

section[data-testid="stSidebar"] { display: none; }

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4 {
    font-family: 'Orbitron', monospace !important;
    color: var(--cyan) !important;
    letter-spacing: 4px !important;
    text-transform: uppercase;
}

p, span, div, label {
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--text) !important;
}

/* ===== JARVIS HEADER ===== */
.jarvis-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(0,212,255,0.25);
    padding-bottom: 14px;
    margin-bottom: 18px;
}

.jarvis-logo {
    font-family: 'Orbitron', monospace;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 10px;
    color: var(--cyan);
    text-shadow: 0 0 20px var(--cyan-glow), 0 0 50px rgba(0,212,255,0.2);
    animation: logoPulse 3s ease-in-out infinite;
    line-height: 1;
}

@keyframes logoPulse {
    0%,100% { text-shadow: 0 0 20px var(--cyan-glow), 0 0 50px rgba(0,212,255,0.2); }
    50% { text-shadow: 0 0 35px var(--cyan), 0 0 80px var(--cyan-glow); }
}

.jarvis-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 4px;
    color: var(--text-dim);
    margin-top: 4px;
}

.status-row {
    display: flex;
    gap: 28px;
    align-items: center;
}

.status-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
}

.status-val {
    font-family: 'Orbitron', monospace;
    font-size: 16px;
    color: var(--cyan);
}

.status-lbl {
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--text-dim);
}

.online-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    letter-spacing: 2px;
    color: #00ff88;
}

.pulse-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 8px #00ff88;
    animation: pulseDot 2s ease-in-out infinite;
    display: inline-block;
}

@keyframes pulseDot { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

/* ===== PANELS ===== */
.j-panel {
    background: var(--panel);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 2px;
    padding: 18px;
    position: relative;
    backdrop-filter: blur(12px);
    margin-bottom: 14px;
}

.j-panel::before {
    content: '';
    position: absolute;
    top: -1px; left: 20px;
    width: 44px; height: 2px;
    background: var(--cyan);
    box-shadow: 0 0 8px var(--cyan);
}

.panel-title {
    font-family: 'Orbitron', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--cyan);
    margin-bottom: 16px;
    text-transform: uppercase;
    opacity: 0.9;
}

/* ===== ARC REACTOR ===== */
.arc-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px 0 20px;
}

.arc-reactor {
    position: relative;
    width: 180px; height: 180px;
    margin-bottom: 20px;
}

.arc-ring {
    position: absolute;
    border-radius: 50%;
    border-style: solid;
    border-color: transparent;
}

.ring1 {
    inset: 0; border-width: 2px;
    border-top-color: var(--cyan);
    border-right-color: var(--cyan);
    animation: spinR 3s linear infinite;
    box-shadow: 0 0 12px var(--cyan-glow);
}

.ring2 {
    inset: 16px; border-width: 1px;
    border-bottom-color: rgba(0,212,255,0.5);
    border-left-color: rgba(0,212,255,0.5);
    animation: spinR 5s linear infinite reverse;
}

.ring3 {
    inset: 30px; border-width: 2px;
    border-top-color: var(--orange);
    border-left-color: var(--orange);
    animation: spinR 2s linear infinite;
    box-shadow: 0 0 8px rgba(255,106,0,0.4);
}

.ring4 {
    inset: 46px; border-width: 1px;
    border-right-color: rgba(0,212,255,0.3);
    border-bottom-color: rgba(0,212,255,0.3);
    animation: spinR 7s linear infinite;
}

@keyframes spinR { from{transform:rotate(0deg);} to{transform:rotate(360deg);} }

.arc-core {
    position: absolute;
    inset: 60px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,255,0.9) 0%, rgba(0,212,255,0.3) 40%, rgba(0,30,60,0.9) 100%);
    box-shadow: 0 0 30px var(--cyan), 0 0 60px rgba(0,212,255,0.3), inset 0 0 20px rgba(0,212,255,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: corePulse 2s ease-in-out infinite;
}

@keyframes corePulse {
    0%,100%{ box-shadow:0 0 30px var(--cyan),0 0 60px rgba(0,212,255,0.3); }
    50%{ box-shadow:0 0 50px var(--cyan),0 0 100px rgba(0,212,255,0.5); }
}

.core-text {
    font-family: 'Orbitron', monospace;
    font-size: 10px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 1px;
    text-shadow: 0 0 10px #fff;
}

/* ===== WAVEFORM ===== */
.waveform {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3px;
    height: 40px;
    margin: 8px 0 16px;
}

.wbar {
    width: 3px;
    border-radius: 2px;
    background: var(--cyan);
    opacity: 0.7;
    animation: waveAnim var(--d) ease-in-out infinite;
    animation-delay: var(--dl);
}

@keyframes waveAnim {
    0%,100%{ height:3px; opacity:0.2; }
    50%{ height:var(--h); opacity:1; }
}

/* ===== OUTPUT BOX ===== */
.output-box {
    background: rgba(0,212,255,0.05);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 2px;
    padding: 14px 16px;
    font-size: 13px;
    color: var(--cyan);
    letter-spacing: 0.5px;
    line-height: 1.7;
    min-height: 60px;
    position: relative;
    margin: 10px 0;
    font-family: 'Share Tech Mono', monospace;
}

.output-label {
    font-family: 'Orbitron', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--cyan);
    opacity: 0.6;
    margin-bottom: 6px;
}

.output-text {
    color: #7fffd4 !important;
    font-size: 13px !important;
}

/* ===== STAT BARS ===== */
.stat-wrap { margin-bottom: 12px; }

.stat-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.stat-name {
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--text-dim);
    text-transform: uppercase;
}

.stat-num {
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    color: var(--cyan);
}

.stat-track {
    width: 100%; height: 4px;
    background: rgba(0,212,255,0.08);
    border-radius: 2px;
    overflow: hidden;
}

.stat-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.8s ease;
}

.fill-cyan { background: linear-gradient(90deg, rgba(0,212,255,0.4), var(--cyan)); box-shadow: 0 0 6px var(--cyan-glow); }
.fill-orange { background: linear-gradient(90deg, rgba(255,106,0,0.4), var(--orange)); box-shadow: 0 0 6px rgba(255,106,0,0.4); }
.fill-green { background: linear-gradient(90deg, rgba(0,255,136,0.4), #00ff88); box-shadow: 0 0 6px rgba(0,255,136,0.4); }

/* ===== CAPABILITY LIST ===== */
.cap-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(0,212,255,0.06);
    font-size: 11px;
    letter-spacing: 0.5px;
    color: var(--text-dim);
}

.cap-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
}

.cap-active { background: #00ff88; box-shadow: 0 0 5px #00ff88; }
.cap-armed { background: var(--orange); box-shadow: 0 0 5px var(--orange); }

.cap-status {
    margin-left: auto;
    font-size: 9px;
    letter-spacing: 1px;
}

.cap-status-active { color: rgba(0,255,136,0.8); }
.cap-status-armed { color: rgba(255,106,0,0.8); }

/* ===== MODE PILLS ===== */
.modes-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}

.mode-pill {
    font-family: 'Orbitron', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    padding: 4px 10px;
    border-radius: 1px;
    border: 1px solid rgba(0,212,255,0.25);
    color: rgba(0,212,255,0.5);
    text-transform: uppercase;
    display: inline-block;
}

.mode-pill-active {
    border-color: var(--cyan);
    color: var(--cyan);
    background: var(--cyan-dim);
    box-shadow: 0 0 8px rgba(0,212,255,0.15);
}

.mode-pill-orange {
    border-color: var(--orange);
    color: var(--orange);
    background: var(--orange-dim);
}

/* ===== LOG BOX ===== */
.log-box {
    font-size: 10px;
    color: var(--text-dim);
    line-height: 2;
    font-family: 'Share Tech Mono', monospace;
    max-height: 140px;
    overflow: hidden;
}

.log-line { color: rgba(0,212,255,0.6) !important; }
.log-line-ok { color: rgba(0,255,136,0.6) !important; }
.log-line-warn { color: rgba(255,106,0,0.7) !important; }

/* ===== RADAR ===== */
.radar-container {
    display: flex;
    justify-content: center;
    padding: 10px 0;
}

.radar {
    position: relative;
    width: 110px; height: 110px;
}

.radar-ring {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(0,212,255,0.15);
}

.rr1{inset:0;} .rr2{inset:18px;} .rr3{inset:36px;} .rr4{inset:52px;}

.radar-sweep {
    position: absolute;
    inset: 0; margin: auto;
    width: 1px;
    height: 50%;
    background: linear-gradient(transparent, var(--cyan));
    transform-origin: bottom center;
    bottom: 50%; top: 0;
    left: 50%;
    transform: translateX(-50%);
    animation: radarSpin 3s linear infinite;
}

@keyframes radarSpin {
    from{transform:translateX(-50%) rotate(0deg);}
    to{transform:translateX(-50%) rotate(360deg);}
}

.rdot {
    position: absolute;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 6px var(--cyan);
    animation: rdotFade 3s ease-in-out infinite;
    animation-delay: var(--dl, 0s);
}

@keyframes rdotFade{ 0%,100%{opacity:0.15;} 50%{opacity:1;} }

/* ===== BATTERY ===== */
.batt-visual {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
}

.batt-body {
    width: 54px; height: 90px;
    border: 2px solid rgba(0,212,255,0.4);
    border-radius: 3px;
    position: relative;
    overflow: hidden;
}

.batt-nub {
    width: 20px; height: 7px;
    background: rgba(0,212,255,0.35);
    border-radius: 2px;
    margin: 0 auto;
    position: relative; top: -9px;
}

.batt-fill-vis {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(180deg, rgba(0,212,255,0.3), var(--cyan));
    box-shadow: 0 0 10px var(--cyan-glow);
    animation: battGlow 2s ease-in-out infinite;
}

@keyframes battGlow { 0%,100%{opacity:0.85;} 50%{opacity:1;} }

.batt-pct-text {
    font-family: 'Orbitron', monospace;
    font-size: 20px;
    font-weight: 700;
    color: var(--cyan);
    text-shadow: 0 0 12px var(--cyan-glow);
}

/* ===== STREAMLIT OVERRIDES ===== */
.stTextInput > div > div {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    border-radius: 2px !important;
    color: var(--cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.stTextInput > div > div:focus-within {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.2) !important;
}

.stTextInput input {
    color: var(--cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 1px !important;
    font-size: 13px !important;
}

.stTextInput input::placeholder { color: var(--text-dim) !important; }

.stTextInput label {
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    color: var(--cyan) !important;
    opacity: 0.8;
}

/* Buttons */
.stButton > button {
    background: rgba(0,212,255,0.06) !important;
    border: 1px solid rgba(0,212,255,0.25) !important;
    color: rgba(168,216,234,0.7) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    border-radius: 2px !important;
    padding: 8px 12px !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: rgba(0,212,255,0.15) !important;
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.2) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    color: var(--cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 2px !important;
}

.stSelectbox label {
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    color: var(--cyan) !important;
}

/* Columns */
[data-testid="column"] { padding: 0 6px !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(0,20,40,0.7) !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 2px !important;
    padding: 10px 14px !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 9px !important;
    letter-spacing: 2px !important;
    color: var(--text-dim) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    color: var(--cyan) !important;
    font-size: 20px !important;
}

/* Divider */
hr { border-color: rgba(0,212,255,0.15) !important; }

/* Success/error/info messages */
.stSuccess, .stInfo {
    background: rgba(0,212,255,0.08) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    color: var(--cyan) !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
}

.stError {
    background: rgba(255,106,0,0.08) !important;
    border: 1px solid rgba(255,106,0,0.3) !important;
    color: var(--orange) !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.stWarning {
    background: rgba(255,200,0,0.08) !important;
    border: 1px solid rgba(255,200,0,0.3) !important;
    color: #ffc800 !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(0,212,255,0.2) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    color: var(--text-dim) !important;
    background: transparent !important;
    border: none !important;
    padding: 8px 20px !important;
}

.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important;
}

/* Corner decorations */
.corner-dec {
    position: fixed;
    width: 36px; height: 36px;
    pointer-events: none;
    z-index: 9998;
}

.corner-dec::before, .corner-dec::after {
    content: '';
    position: absolute;
    background: rgba(0,212,255,0.5);
}

.corner-dec::before { width: 2px; height: 100%; }
.corner-dec::after { width: 100%; height: 2px; }

.c-tl { top: 6px; left: 6px; }
.c-tr { top: 6px; right: 6px; transform: scaleX(-1); }
.c-bl { bottom: 6px; left: 6px; transform: scaleY(-1); }
.c-br { bottom: 6px; right: 6px; transform: scale(-1,-1); }

/* Progress bar override */
.stProgress > div > div {
    background: var(--cyan) !important;
    box-shadow: 0 0 6px var(--cyan-glow) !important;
}

.stProgress > div {
    background: rgba(0,212,255,0.08) !important;
}
</style>

<div class="corner-dec c-tl"></div>
<div class="corner-dec c-tr"></div>
<div class="corner-dec c-bl"></div>
<div class="corner-dec c-br"></div>
""", unsafe_allow_html=True)


# ===== UTILITY FUNCTIONS (from original jarvis.py) =====

def speak(text):
    """Speak using macOS say command"""
    try:
        subprocess.run(["say", "-v", "Samantha", text], check=False)
    except:
        pass

def calculate(command):
    try:
        expr = command.lower()
        expr = expr.replace("plus", "+").replace("minus", "-")
        expr = expr.replace("times", "*").replace("multiply", "*")
        expr = expr.replace("divided by", "/")
        # Safe eval — only allow numbers and operators
        allowed = set("0123456789+-*/.() ")
        if all(c in allowed for c in expr):
            return eval(expr)
        return None
    except:
        return None

def get_weather():
    return "Weather is clear and temperature is around 25°C. Humidity 58%. Wind 12 km/h NW."

def battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            pct = round(battery.percent)
            plugged = battery.power_plugged
            status = "charging" if plugged else "on battery"
            return f"Battery is at {pct}% and {status}.", pct
        return "Battery info unavailable.", 0
    except:
        return "Battery info unavailable.", 0

def get_system_stats():
    cpu = round(psutil.cpu_percent(interval=0.3))
    ram = round(psutil.virtual_memory().percent)
    disk = round(psutil.disk_usage('/').percent)
    try:
        batt = round(psutil.sensors_battery().percent)
    except:
        batt = 85
    return cpu, ram, disk, batt

def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{home}/Desktop/screenshot_{timestamp}.png"
    result = subprocess.run(["screencapture", filename], capture_output=True)
    return filename

def create_note(text):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{home}/Desktop/note_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(text)
    return filename

def volume_up():
    subprocess.run(["osascript", "-e",
        "set volume output volume (output volume of (get volume settings) + 10)"])

def volume_down():
    subprocess.run(["osascript", "-e",
        "set volume output volume (output volume of (get volume settings) - 10)"])

def emergency_mode():
    contacts = [
        "+919926941000", "+919244588090",
        "+919238603585", "+917303756755", "+918989446655"
    ]
    for number in contacts:
        try:
            subprocess.run(["open", f"https://wa.me/{number}"])
            time.sleep(1)
        except:
            pass
    return contacts

def process_command(cmd):
    """Core command processor — same logic as original jarvis.py"""
    cmd = cmd.lower().strip()
    original_cmd = cmd

    # Strip wake word
    if cmd.startswith("jarvis"):
        cmd = cmd.replace("jarvis", "", 1).strip()

    # TIME
    if "time" in cmd and len(cmd) < 20:
        now = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The time is {now}, sir."
        speak(response)
        return "⏱ TIME", response, "info"

    # DATE
    elif "date" in cmd or "day" in cmd:
        today = datetime.datetime.now().strftime("%A, %B %d %Y")
        response = f"Today is {today}."
        speak(response)
        return "📅 DATE", response, "info"

    # WEATHER
    elif "weather" in cmd:
        response = get_weather()
        speak(response)
        return "🌤 WEATHER", response, "info"

    # BATTERY
    elif "battery" in cmd:
        response, _ = battery_info()
        speak(response)
        return "🔋 BATTERY", response, "info"

    # CALCULATOR
    elif any(w in cmd for w in ["plus", "minus", "times", "multiply", "divided", "calculate"]):
        result = calculate(cmd)
        if result is not None:
            response = f"The answer is {result}."
            speak(response)
            return "🧮 CALCULATOR", response, "success"
        return "🧮 CALCULATOR", "Calculation failed. Try: 'jarvis 5 plus 3'", "error"

    # SCREENSHOT
    elif "screenshot" in cmd:
        path = take_screenshot()
        response = f"Screenshot saved to Desktop: {os.path.basename(path)}"
        speak("Screenshot saved.")
        return "📸 SCREENSHOT", response, "success"

    # NOTES
    elif "note" in cmd:
        text = cmd.replace("note", "").strip()
        if text:
            path = create_note(text)
            response = f"Note saved: {os.path.basename(path)}"
            speak("Note created.")
            return "📝 NOTE", response, "success"
        return "📝 NOTE", "Please add text. Try: 'jarvis note buy groceries'", "warning"

    # OPEN APP
    elif "open" in cmd:
        app = cmd.replace("open", "").strip()
        try:
            subprocess.run(["open", "-a", app], check=True)
            response = f"Opening {app.title()}..."
            speak(response)
            return "🚀 APP LAUNCH", response, "success"
        except:
            return "🚀 APP LAUNCH", f"Could not find app: {app}", "error"

    # GOOGLE
    elif "google" in cmd or "search" in cmd:
        query = cmd.replace("google", "").replace("search", "").replace("for", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            response = f"Searching Google for: '{query}'"
            speak(response)
            return "🔍 GOOGLE", response, "success"

    # YOUTUBE
    elif "youtube" in cmd:
        query = cmd.replace("youtube", "").strip()
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            response = f"Launching YouTube: '{query}'"
            speak(response)
            return "▶ YOUTUBE", response, "success"
        webbrowser.open("https://youtube.com")
        return "▶ YOUTUBE", "Opening YouTube...", "success"

    # VOLUME
    elif "volume up" in cmd:
        volume_up()
        speak("Volume increased.")
        return "🔊 VOLUME", "Volume increased by 10%.", "success"

    elif "volume down" in cmd:
        volume_down()
        speak("Volume decreased.")
        return "🔉 VOLUME", "Volume decreased by 10%.", "success"

    # JOKE
    elif "joke" in cmd:
        jokes = [
            "Why do programmers hate nature? Too many bugs.",
            "I am not lazy. I am on energy saving mode.",
            "Why did the AI go to therapy? Too much processing.",
            "I told my AI to act human. It started procrastinating.",
            "Error 404: Joke not found. Just kidding — here it is.",
        ]
        j = random.choice(jokes)
        speak(j)
        return "😂 JOKE", j, "info"

    # MOTIVATE
    elif "motivate" in cmd or "motivation" in cmd:
        quotes = [
            "The only way to do great work is to love what you do.",
            "In the middle of every difficulty lies opportunity.",
            "It does not matter how slowly you go as long as you do not stop.",
            "Success is not final, failure is not fatal — it is the courage to continue that counts.",
        ]
        q = random.choice(quotes)
        speak(q)
        return "💡 MOTIVATION", q, "info"

    # EMERGENCY
    elif any(x in cmd for x in ["help", "emergency", "save me", "danger", "sos"]):
        contacts = emergency_mode()
        response = f"🚨 EMERGENCY ACTIVATED. Alerts sent to {len(contacts)} contacts via WhatsApp."
        speak("Emergency mode activated. Sending alerts.")
        return "🚨 EMERGENCY", response, "error"

    # EXIT
    elif any(x in cmd for x in ["bye", "exit", "shutdown", "quit", "goodbye"]):
        speak("Goodbye sir. Shutting down.")
        return "👋 GOODBYE", "Shutting down JARVIS. Goodbye, sir.", "warning"

    # STATUS
    elif "status" in cmd or "diagnostic" in cmd:
        cpu, ram, disk, batt = get_system_stats()
        response = f"Diagnostic complete. CPU: {cpu}% | RAM: {ram}% | Disk: {disk}% | Battery: {batt}%. All systems nominal."
        speak(response)
        return "⚡ DIAGNOSTIC", response, "success"

    # UNKNOWN
    else:
        speak("Command not recognized.")
        return "❓ UNKNOWN", f"Command not recognized: '{original_cmd}'. Say 'jarvis help' for commands.", "warning"


# ===== SESSION STATE =====
if "response_history" not in st.session_state:
    st.session_state.response_history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = "All systems nominal. Ready for your command, sir."
if "last_category" not in st.session_state:
    st.session_state.last_category = "STANDBY"
if "active_modes" not in st.session_state:
    st.session_state.active_modes = {"Focus": True, "Combat": False, "Ghost": False, "Override": True, "Neural": False}


# ===== HEADER =====
st.markdown(f"""
<div class="jarvis-header">
    <div>
        <div class="jarvis-logo">JARVIS</div>
        <div class="jarvis-sub">JUST A RATHER VERY INTELLIGENT SYSTEM — v3.0</div>
    </div>
    <div class="status-row">
        <div class="status-item">
            <span class="status-val" id="clockval">{datetime.datetime.now().strftime("%H:%M:%S")}</span>
            <span class="status-lbl">TIME</span>
        </div>
        <div class="status-item">
            <span class="status-val">{datetime.datetime.now().strftime("%d %b")}</span>
            <span class="status-lbl">DATE</span>
        </div>
        <div class="online-badge">
            <span class="pulse-dot"></span>
            ONLINE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===== MAIN LAYOUT =====
left_col, center_col, right_col = st.columns([1.1, 1.6, 1.1])


# ===== LEFT COLUMN — SYSTEM STATS =====
with left_col:
    cpu, ram, disk, batt = get_system_stats()

    st.markdown(f"""
    <div class="j-panel">
        <div class="panel-title">System Monitor</div>

        <div class="stat-wrap">
            <div class="stat-header">
                <span class="stat-name">CPU Usage</span>
                <span class="stat-num">{cpu}%</span>
            </div>
            <div class="stat-track"><div class="stat-fill fill-cyan" style="width:{cpu}%"></div></div>
        </div>

        <div class="stat-wrap">
            <div class="stat-header">
                <span class="stat-name">Memory</span>
                <span class="stat-num">{ram}%</span>
            </div>
            <div class="stat-track"><div class="stat-fill fill-orange" style="width:{ram}%"></div></div>
        </div>

        <div class="stat-wrap">
            <div class="stat-header">
                <span class="stat-name">Battery</span>
                <span class="stat-num">{batt}%</span>
            </div>
            <div class="stat-track"><div class="stat-fill fill-green" style="width:{batt}%"></div></div>
        </div>

        <div class="stat-wrap">
            <div class="stat-header">
                <span class="stat-name">Disk Usage</span>
                <span class="stat-num">{disk}%</span>
            </div>
            <div class="stat-track"><div class="stat-fill fill-cyan" style="width:{disk}%"></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active Modes
    modes_html = '<div class="j-panel"><div class="panel-title">Active Modes</div><div class="modes-row">'
    for mode, active in st.session_state.active_modes.items():
        cls = "mode-pill-active" if active else ""
        modes_html += f'<span class="mode-pill {cls}">{mode}</span>'
    modes_html += '</div></div>'
    st.markdown(modes_html, unsafe_allow_html=True)

    # Quick Buttons
    st.markdown('<div class="j-panel"><div class="panel-title">Quick Commands</div>', unsafe_allow_html=True)
    qcmds = [
        ("⏱ Time", "jarvis time"),
        ("📅 Date", "jarvis date"),
        ("🔋 Battery", "jarvis battery"),
        ("🌤 Weather", "jarvis weather"),
        ("📸 Screenshot", "jarvis screenshot"),
        ("⚡ Diagnostic", "jarvis status"),
        ("😂 Joke", "jarvis tell me a joke"),
        ("💡 Motivate", "jarvis motivate me"),
    ]
    cols_q = st.columns(2)
    for i, (label, cmd) in enumerate(qcmds):
        with cols_q[i % 2]:
            if st.button(label, key=f"qbtn_{i}"):
                cat, resp, typ = process_command(cmd)
                st.session_state.last_response = resp
                st.session_state.last_category = cat
                st.session_state.response_history.insert(0, {
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "cmd": cmd, "response": resp, "type": typ
                })
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ===== CENTER COLUMN =====
with center_col:

    # Arc Reactor
    st.markdown("""
    <div class="j-panel">
        <div class="panel-title" style="text-align:center;">Core Interface</div>
        <div class="arc-container">
            <div class="arc-reactor">
                <div class="arc-ring ring1"></div>
                <div class="arc-ring ring2"></div>
                <div class="arc-ring ring3"></div>
                <div class="arc-ring ring4"></div>
                <div class="arc-core"><span class="core-text">ONLINE</span></div>
            </div>
            <div class="waveform">
                <div class="wbar" style="--d:0.8s;--dl:0s;--h:5px;"></div>
                <div class="wbar" style="--d:1.1s;--dl:0.1s;--h:10px;"></div>
                <div class="wbar" style="--d:0.9s;--dl:0.2s;--h:18px;"></div>
                <div class="wbar" style="--d:1.3s;--dl:0.05s;--h:28px;"></div>
                <div class="wbar" style="--d:0.7s;--dl:0.3s;--h:36px;"></div>
                <div class="wbar" style="--d:1.0s;--dl:0.15s;--h:40px;"></div>
                <div class="wbar" style="--d:0.85s;--dl:0.25s;--h:36px;"></div>
                <div class="wbar" style="--d:1.2s;--dl:0.1s;--h:28px;"></div>
                <div class="wbar" style="--d:0.95s;--dl:0.35s;--h:18px;"></div>
                <div class="wbar" style="--d:1.1s;--dl:0.2s;--h:10px;"></div>
                <div class="wbar" style="--d:0.8s;--dl:0s;--h:5px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Command Input
    st.markdown('<div class="j-panel"><div class="panel-title">Command Input</div>', unsafe_allow_html=True)

    with st.form("cmd_form", clear_on_submit=True):
        user_input = st.text_input(
            "VOICE COMMAND",
            placeholder="jarvis open spotify  |  jarvis 5 plus 3  |  jarvis time",
            label_visibility="visible"
        )
        submitted = st.form_submit_button("▶  EXECUTE COMMAND")

    if submitted and user_input.strip():
        cat, resp, typ = process_command(user_input.strip())
        st.session_state.last_response = resp
        st.session_state.last_category = cat
        st.session_state.response_history.insert(0, {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "cmd": user_input.strip(),
            "response": resp,
            "type": typ
        })
        st.rerun()

    # Response Output
    resp_color = {
        "success": "#7fffd4",
        "error": "#ff6a00",
        "warning": "#ffc800",
        "info": "#00d4ff"
    }.get(
        st.session_state.response_history[0]["type"]
        if st.session_state.response_history else "info",
        "#00d4ff"
    )

    st.markdown(f"""
    <div class="output-box">
        <div class="output-label">{st.session_state.last_category} — RESPONSE</div>
        <div style="color:{resp_color}; font-family:'Share Tech Mono',monospace; font-size:13px; line-height:1.7; margin-top:8px;">
            {st.session_state.last_response}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # App Launcher Tabs
    st.markdown('<div class="j-panel"><div class="panel-title">App Launcher</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["APPS", "WEB", "MODES"])

    with tab1:
        apps = [("Spotify","Spotify"),("VS Code","Visual Studio Code"),
                ("Chrome","Google Chrome"),("Terminal","Terminal"),
                ("Finder","Finder"),("Notes","Notes")]
        cols_a = st.columns(3)
        for i, (label, app) in enumerate(apps):
            with cols_a[i % 3]:
                if st.button(label, key=f"app_{i}"):
                    cat, resp, typ = process_command(f"jarvis open {app}")
                    st.session_state.last_response = resp
                    st.session_state.last_category = cat
                    st.rerun()

    with tab2:
        sites = [("Google","https://google.com"),("YouTube","https://youtube.com"),
                 ("GitHub","https://github.com"),("Gmail","https://mail.google.com")]
        cols_w = st.columns(2)
        for i, (label, url) in enumerate(sites):
            with cols_w[i % 2]:
                if st.button(label, key=f"web_{i}"):
                    webbrowser.open(url)
                    st.session_state.last_response = f"Opening {label}..."
                    st.session_state.last_category = "🌐 WEB"
                    st.rerun()

    with tab3:
        mode_list = list(st.session_state.active_modes.keys())
        cols_m = st.columns(3)
        for i, mode in enumerate(mode_list):
            with cols_m[i % 3]:
                active = st.session_state.active_modes[mode]
                label = f"✓ {mode}" if active else mode
                if st.button(label, key=f"mode_{i}"):
                    st.session_state.active_modes[mode] = not active
                    status = "activated" if not active else "deactivated"
                    st.session_state.last_response = f"{mode} mode {status}."
                    st.session_state.last_category = "⚡ MODE"
                    speak(f"{mode} mode {status}.")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ===== RIGHT COLUMN =====
with right_col:

    # Capabilities
    caps = [
        ("Voice recognition", "ACTIVE"),
        ("Time & date", "ACTIVE"),
        ("Battery monitor", "ACTIVE"),
        ("App launcher", "ACTIVE"),
        ("Google search", "ACTIVE"),
        ("YouTube search", "ACTIVE"),
        ("Screenshot", "ACTIVE"),
        ("Note creation", "ACTIVE"),
        ("Volume control", "ACTIVE"),
        ("Emergency SOS", "ARMED"),
        ("Calculator", "ACTIVE"),
        ("Weather fetch", "ACTIVE"),
    ]

    caps_html = '<div class="j-panel"><div class="panel-title">Capability Matrix</div>'
    for name, status in caps:
        dot_cls = "cap-active" if status == "ACTIVE" else "cap-armed"
        stat_cls = "cap-status-active" if status == "ACTIVE" else "cap-status-armed"
        caps_html += f"""
        <div class="cap-item">
            <span class="cap-dot {dot_cls}"></span>
            <span style="font-size:11px;">{name}</span>
            <span class="cap-status {stat_cls}">{status}</span>
        </div>"""
    caps_html += '</div>'
    st.markdown(caps_html, unsafe_allow_html=True)

    # Radar
    st.markdown("""
    <div class="j-panel">
        <div class="panel-title">Network Scan</div>
        <div class="radar-container">
            <div class="radar">
                <div class="radar-ring rr1"></div>
                <div class="radar-ring rr2"></div>
                <div class="radar-ring rr3"></div>
                <div class="radar-ring rr4"></div>
                <div class="radar-sweep"></div>
                <div class="rdot" style="top:20%;left:60%;--dl:0.5s;"></div>
                <div class="rdot" style="top:65%;left:30%;--dl:1.2s;"></div>
                <div class="rdot" style="top:70%;left:72%;--dl:2.0s;"></div>
                <div class="rdot" style="top:35%;left:78%;--dl:0.8s;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Battery visual
    batt_height = batt
    batt_color = "#00ff88" if batt > 50 else ("#ffc800" if batt > 20 else "#ff4444")
    st.markdown(f"""
    <div class="j-panel">
        <div class="panel-title">Power Status</div>
        <div class="batt-visual">
            <div>
                <div class="batt-nub"></div>
                <div class="batt-body">
                    <div class="batt-fill-vis" style="height:{batt_height}%;background:linear-gradient(180deg,rgba(0,212,255,0.3),{batt_color});"></div>
                </div>
            </div>
            <div class="batt-pct-text" style="color:{batt_color};text-shadow:0 0 12px {batt_color}66;">{batt}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Command History
    if st.session_state.response_history:
        hist_html = '<div class="j-panel"><div class="panel-title">Command Log</div><div class="log-box">'
        for entry in st.session_state.response_history[:6]:
            color_map = {"success":"rgba(0,255,136,0.6)","error":"rgba(255,106,0,0.7)","warning":"rgba(255,200,0,0.6)","info":"rgba(0,212,255,0.6)"}
            c = color_map.get(entry["type"], "rgba(0,212,255,0.6)")
            hist_html += f'<div style="color:{c};font-size:10px;line-height:1.9;border-bottom:1px solid rgba(0,212,255,0.06);padding:2px 0;">'
            hist_html += f'<span style="color:rgba(168,216,234,0.35);font-size:9px;">[{entry["time"]}]</span> {entry["cmd"]}</div>'
        hist_html += '</div></div>'
        st.markdown(hist_html, unsafe_allow_html=True)


# ===== FOOTER =====
st.markdown("""
<div style="
    border-top: 1px solid rgba(0,212,255,0.15);
    margin-top: 16px;
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    letter-spacing: 2px;
    color: rgba(168,216,234,0.3);
    font-family: 'Share Tech Mono', monospace;
">
    <span>STARK INDUSTRIES — CONFIDENTIAL</span>
    <span>JARVIS v3.0 — PYTHON EDITION</span>
    <span>ALL SYSTEMS NOMINAL</span>
</div>
""", unsafe_allow_html=True)