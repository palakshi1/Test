import streamlit as st
import base64
import json
import random
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Verdura — Smart Plant Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --forest:    #1C3A2B;
  --sage:      #4A7C59;
  --mint:      #8DB596;
  --cream:     #F5F0E8;
  --sand:      #E8DFC8;
  --bark:      #6B5744;
  --gold:      #C9A84C;
  --white:     #FAFAF7;
  --charcoal:  #2C2C2C;
  --muted:     #7A7A6E;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--white);
  font-family: 'DM Sans', sans-serif;
  color: var(--charcoal);
}

[data-testid="stAppViewContainer"] > .main {
  background: var(--white);
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ── NAV ── */
.verdura-nav {
  background: var(--forest);
  padding: 0 2.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 999;
  box-shadow: 0 2px 20px rgba(28,58,43,0.3);
}
.verdura-logo {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.85rem;
  font-weight: 600;
  color: var(--cream);
  letter-spacing: 0.04em;
}
.verdura-logo span { color: var(--gold); }
.nav-links {
  display: flex;
  gap: 2rem;
}
.nav-link {
  color: rgba(245,240,232,0.75);
  font-size: 0.82rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  cursor: pointer;
  transition: color 0.2s;
}
.nav-link:hover { color: var(--gold); }

/* ── HERO ── */
.hero-section {
  background: linear-gradient(135deg, var(--forest) 0%, #2D5240 50%, #1a3326 100%);
  min-height: 88vh;
  display: flex;
  align-items: center;
  padding: 5rem 3rem;
  position: relative;
  overflow: hidden;
}
.hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 70% 60% at 65% 50%, rgba(74,124,89,0.2) 0%, transparent 70%);
}
.hero-content { position: relative; z-index: 2; max-width: 560px; }
.hero-eyebrow {
  display: inline-block;
  background: rgba(201,168,76,0.15);
  border: 1px solid rgba(201,168,76,0.4);
  color: var(--gold);
  font-size: 0.72rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 0.4rem 1rem;
  border-radius: 2px;
  margin-bottom: 1.5rem;
}
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2.8rem, 5vw, 4.5rem);
  font-weight: 500;
  color: var(--cream);
  line-height: 1.1;
  margin-bottom: 1.2rem;
}
.hero-title em { color: var(--mint); font-style: italic; }
.hero-sub {
  color: rgba(245,240,232,0.65);
  font-size: 1.05rem;
  line-height: 1.7;
  margin-bottom: 2.5rem;
  font-weight: 300;
}
.hero-cta-row { display: flex; gap: 1rem; flex-wrap: wrap; }
.btn-primary {
  background: var(--gold);
  color: var(--forest);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.85rem 1.8rem;
  border: none;
  border-radius: 2px;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s;
}
.btn-primary:hover { background: #d4b660; transform: translateY(-1px); }
.btn-outline {
  background: transparent;
  color: var(--cream);
  font-size: 0.82rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.85rem 1.8rem;
  border: 1px solid rgba(245,240,232,0.35);
  border-radius: 2px;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
}
.btn-outline:hover { border-color: var(--cream); color: var(--cream); }

/* ── SECTION HEADERS ── */
.section-label {
  font-size: 0.7rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--sage);
  margin-bottom: 0.6rem;
}
.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 3.5vw, 3rem);
  font-weight: 500;
  color: var(--forest);
  line-height: 1.2;
  margin-bottom: 0.8rem;
}
.section-sub {
  color: var(--muted);
  font-size: 0.95rem;
  line-height: 1.7;
  max-width: 540px;
  font-weight: 300;
}

/* ── CHLORA DIAGNOSIS ── */
.chlora-wrapper {
  background: linear-gradient(160deg, var(--forest) 0%, #244836 100%);
  border-radius: 12px;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}
.chlora-wrapper::after {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 280px; height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(74,124,89,0.25) 0%, transparent 70%);
}
.chlora-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  color: var(--cream);
  margin-bottom: 0.4rem;
}
.chlora-title span { color: var(--gold); }
.chlora-badge {
  display: inline-block;
  background: rgba(201,168,76,0.2);
  border: 1px solid rgba(201,168,76,0.45);
  color: var(--gold);
  font-size: 0.65rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  margin-bottom: 1.2rem;
}
.chlora-sub {
  color: rgba(245,240,232,0.6);
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

/* ── DIAGNOSIS RESULT ── */
.diag-card {
  background: rgba(245,240,232,0.06);
  border: 1px solid rgba(245,240,232,0.12);
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1.5rem;
}
.diag-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.2rem;
}
.status-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.status-dot.warning { background: #E8A838; box-shadow: 0 0 8px rgba(232,168,56,0.5); }
.status-dot.danger  { background: #D64C4C; box-shadow: 0 0 8px rgba(214,76,76,0.5); }
.status-dot.ok      { background: #4CAF6F; box-shadow: 0 0 8px rgba(76,175,111,0.5); }
.status-label {
  color: var(--cream);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.05em;
}
.diag-section-title {
  color: var(--mint);
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
  margin-top: 1rem;
}
.diag-text {
  color: rgba(245,240,232,0.8);
  font-size: 0.88rem;
  line-height: 1.65;
}
.diag-pill {
  display: inline-block;
  background: rgba(74,124,89,0.25);
  border: 1px solid rgba(141,181,150,0.3);
  color: var(--mint);
  font-size: 0.75rem;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  margin: 0.2rem;
}
.diag-pill.red { background: rgba(214,76,76,0.15); border-color: rgba(214,76,76,0.3); color: #E8908C; }

/* ── PRODUCT CARDS ── */
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1.5rem; }
.product-card {
  background: var(--white);
  border: 1px solid rgba(28,58,43,0.08);
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.25s, box-shadow 0.25s;
  cursor: pointer;
}
.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(28,58,43,0.12);
}
.product-img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  background: var(--sand);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Cormorant Garamond', serif;
  font-size: 3.5rem;
  color: var(--sage);
}
.product-body { padding: 1rem; }
.product-category {
  font-size: 0.65rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--sage);
  margin-bottom: 0.3rem;
}
.product-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--forest);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}
.product-pricing { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem; }
.price-current { font-size: 1rem; font-weight: 600; color: var(--forest); }
.price-original { font-size: 0.82rem; color: var(--muted); text-decoration: line-through; }
.price-badge {
  background: #E8F5E0;
  color: #3A7D44;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 20px;
}
.add-cart-btn {
  width: 100%;
  background: var(--forest);
  color: var(--cream);
  border: none;
  padding: 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}
.add-cart-btn:hover { background: var(--sage); }

/* ── SCHEDULE TABLE ── */
.schedule-row {
  display: flex;
  gap: 1rem;
  padding: 0.9rem 0;
  border-bottom: 1px solid rgba(245,240,232,0.08);
  align-items: flex-start;
}
.schedule-day {
  min-width: 90px;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 600;
  padding-top: 0.15rem;
}
.schedule-task {
  color: rgba(245,240,232,0.8);
  font-size: 0.88rem;
  line-height: 1.5;
}
.schedule-task strong { color: var(--mint); font-weight: 500; }

/* ── REC PRODUCT CARD ── */
.rec-card {
  background: rgba(245,240,232,0.05);
  border: 1px solid rgba(245,240,232,0.1);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  transition: border-color 0.2s;
}
.rec-card:hover { border-color: rgba(201,168,76,0.4); }
.rec-product-name {
  color: var(--cream);
  font-size: 0.9rem;
  font-weight: 500;
}
.rec-product-desc {
  color: rgba(245,240,232,0.5);
  font-size: 0.78rem;
  margin-top: 0.2rem;
}
.rec-price { color: var(--gold); font-size: 1rem; font-weight: 600; }
.add-rec-btn {
  background: var(--gold);
  color: var(--forest);
  border: none;
  padding: 0.45rem 1rem;
  border-radius: 3px;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
  cursor: pointer;
  margin-left: 1rem;
  flex-shrink: 0;
}

/* ── TESTIMONIAL ── */
.testimonial-card {
  background: var(--cream);
  border-radius: 8px;
  padding: 2rem;
  border-left: 3px solid var(--sage);
}
.testimonial-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.15rem;
  font-style: italic;
  color: var(--forest);
  line-height: 1.7;
  margin-bottom: 1rem;
}
.testimonial-author {
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 500;
}

/* ── FOOTER ── */
.verdura-footer {
  background: var(--forest);
  padding: 3rem 3rem 1.5rem;
  margin-top: 5rem;
}
.footer-logo {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  color: var(--cream);
  margin-bottom: 0.5rem;
}
.footer-logo span { color: var(--gold); }
.footer-tagline {
  color: rgba(245,240,232,0.45);
  font-size: 0.82rem;
  letter-spacing: 0.05em;
  margin-bottom: 2rem;
  font-style: italic;
}
.footer-bottom {
  border-top: 1px solid rgba(245,240,232,0.1);
  margin-top: 2rem;
  padding-top: 1.2rem;
  color: rgba(245,240,232,0.3);
  font-size: 0.75rem;
}

/* Streamlit overrides */
.stButton > button {
  background: var(--forest);
  color: var(--cream);
  border: none;
  border-radius: 4px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 500;
  padding: 0.7rem 1.5rem;
  transition: background 0.2s, transform 0.15s;
}
.stButton > button:hover {
  background: var(--sage) !important;
  color: var(--cream) !important;
  transform: translateY(-1px);
}
.stFileUploader {
  background: rgba(28,58,43,0.04);
  border: 2px dashed rgba(74,124,89,0.35);
  border-radius: 8px;
  padding: 1rem;
}
[data-testid="stFileUploaderDropzone"] {
  background: transparent !important;
}
.stSelectbox select, .stTextInput input {
  border-color: rgba(74,124,89,0.3) !important;
  border-radius: 4px;
}
div[data-testid="stTabs"] button {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--muted);
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--forest);
  font-weight: 600;
}
.stMetric { background: var(--cream); border-radius: 8px; padding: 1rem; }
[data-testid="metric-container"] { background: var(--cream); border-radius: 8px; padding: 1rem; }

/* Divider */
.v-divider { border: none; border-top: 1px solid rgba(28,58,43,0.08); margin: 3rem 0; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "cart" not in st.session_state:
    st.session_state.cart = []
if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── PRODUCT DATABASE ───────────────────────────────────────────────────────────
PRODUCTS = {
    "fertilizers": [
        {"id": "f1", "name": "Organic GreenGrow Fertilizer", "emoji": "🌱", "mrp": 699, "price": 499, "category": "Fertilizers", "desc": "NPK 19-19-19 balanced formula for lush growth"},
        {"id": "f2", "name": "RootBoost Soil Enhancer", "emoji": "🪴", "mrp": 499, "price": 349, "category": "Soil & Nutrition", "desc": "Mycorrhizal blend for stronger root systems"},
        {"id": "f3", "name": "SeaBloom Liquid Feed", "emoji": "🌊", "mrp": 599, "price": 449, "category": "Fertilizers", "desc": "Cold-pressed seaweed concentrate, 250ml"},
        {"id": "f4", "name": "TerraCompost Premium", "emoji": "🍂", "mrp": 799, "price": 599, "category": "Soil & Nutrition", "desc": "Vermicompost enriched potting mix, 5kg"},
    ],
    "pesticides": [
        {"id": "p1", "name": "Neem Pest Guard Spray", "emoji": "🛡️", "mrp": 449, "price": 299, "category": "Pest Control", "desc": "Cold-pressed neem oil spray, 500ml"},
        {"id": "p2", "name": "BioShield Fungicide", "emoji": "🌿", "mrp": 549, "price": 399, "category": "Pest Control", "desc": "Trichoderma-based fungal defense"},
        {"id": "p3", "name": "AphidAway Concentrate", "emoji": "🔬", "mrp": 399, "price": 279, "category": "Pest Control", "desc": "Pyrethrin extract, highly effective"},
    ],
    "plants": [
        {"id": "pl1", "name": "Areca Palm", "emoji": "🌴", "mrp": 1299, "price": 899, "category": "Air Purifying", "desc": "Natural air humidifier, 3–4 ft"},
        {"id": "pl2", "name": "Monstera Deliciosa", "emoji": "🍃", "mrp": 1099, "price": 799, "category": "Indoor Plants", "desc": "Swiss cheese plant, statement foliage"},
        {"id": "pl3", "name": "Snake Plant Laurentii", "emoji": "🌵", "mrp": 699, "price": 499, "category": "Succulents", "desc": "Low-maintenance, air-purifying"},
        {"id": "pl4", "name": "Peace Lily", "emoji": "🤍", "mrp": 849, "price": 649, "category": "Flowering", "desc": "White blooms, deep shade tolerant"},
    ],
    "pots": [
        {"id": "po1", "name": "Terracotta Milano Pot", "emoji": "🏺", "mrp": 899, "price": 699, "category": "Pots & Planters", "desc": "Hand-thrown terracotta, 10 inch"},
        {"id": "po2", "name": "Self-Watering Planter", "emoji": "💧", "mrp": 1299, "price": 999, "category": "Pots & Planters", "desc": "Reservoir-based, 3-week water reserve"},
    ],
    "tools": [
        {"id": "t1", "name": "Precision Pruner Set", "emoji": "✂️", "mrp": 1199, "price": 849, "category": "Gardening Tools", "desc": "Japanese steel, ergonomic grip"},
        {"id": "t2", "name": "Smart Moisture Meter", "emoji": "📊", "mrp": 699, "price": 549, "category": "Gadgets", "desc": "3-in-1 soil moisture, pH, light sensor"},
    ],
    "kits": [
        {"id": "k1", "name": "Complete Recovery Kit", "emoji": "🧪", "mrp": 1999, "price": 1499, "category": "Care Kits", "desc": "Fertilizer + Pesticide + Soil for sick plants"},
        {"id": "k2", "name": "New Plant Starter Kit", "emoji": "🌱", "mrp": 1499, "price": 1099, "category": "Care Kits", "desc": "Potting mix + fertilizer + pruner + pot"},
    ]
}

ALL_PRODUCTS = [p for cat in PRODUCTS.values() for p in cat]

# ── DIAGNOSES DATABASE ─────────────────────────────────────────────────────────
DIAGNOSES = {
    "yellowing": {
        "condition": "Nitrogen Deficiency / Overwatering",
        "severity": "warning",
        "plant_guess": "Likely a broad-leafed tropical (Pothos, Areca Palm, or Peace Lily)",
        "issues": ["Chlorosis in older leaves", "Pale yellow-green coloration", "Possible root rot from overwatering"],
        "immediate": "Reduce watering frequency. Allow soil to dry 2 inches deep before next watering. Check drainage holes for blockage.",
        "products": ["f1", "f2", "t2"],
        "schedule": [
            ("Monday", "Watering check", "Allow soil to fully dry — use <strong>Smart Moisture Meter</strong> before watering"),
            ("Tuesday", "Fertilize", "Apply <strong>Organic GreenGrow</strong> at half strength (1 tsp / litre)"),
            ("Thursday", "Soil aeration", "Gently fork top soil, improve drainage with <strong>RootBoost</strong> mix"),
            ("Saturday", "Observation", "Check new growth for color improvement — photograph & compare"),
            ("Day 14", "Full assessment", "Expected 60–70% recovery in leaf color"),
        ],
        "prognosis": "With correct treatment, yellowing should reverse within 2–3 weeks. New growth will emerge healthy green."
    },
    "spots": {
        "condition": "Fungal Leaf Spot / Bacterial Blight",
        "severity": "danger",
        "plant_guess": "Rose, Hibiscus, or humid-loving foliage plant",
        "issues": ["Brown/black circular spots with yellow halo", "Progressive defoliation risk", "Fungal spore spread"],
        "immediate": "Isolate plant immediately. Remove all affected leaves. Do not mist foliage. Improve air circulation.",
        "products": ["p2", "p1", "f3"],
        "schedule": [
            ("Day 1", "Isolate + Prune", "Remove all spotted leaves. Sterilize scissors with alcohol. Apply <strong>BioShield Fungicide</strong>"),
            ("Day 3", "Neem spray", "Full foliage spray with <strong>Neem Pest Guard</strong> including undersides"),
            ("Day 7", "Re-application", "Repeat BioShield application. Monitor for new spots."),
            ("Day 10", "Fertilize", "Apply <strong>SeaBloom Liquid Feed</strong> to support immune response"),
            ("Day 14", "Assessment", "Expect 80% clearance. Spots should not spread to new leaves."),
        ],
        "prognosis": "Fungal infections respond well to neem + fungicide protocol. Expect containment within 7 days and full recovery in 3–4 weeks."
    },
    "wilting": {
        "condition": "Root Rot / Chronic Underwatering",
        "severity": "danger",
        "plant_guess": "Ficus, Calathea, or tropical houseplant",
        "issues": ["Drooping stems despite moist soil (root rot)", "OR crispy leaf edges (dehydration)", "Structural cell damage in stems"],
        "immediate": "Check roots — healthy roots are white/tan, rotten roots are brown/mushy. If root rot: unpot, trim rotted roots, repot in fresh well-draining mix.",
        "products": ["f2", "po2", "k1"],
        "schedule": [
            ("Day 1", "Root inspection", "Unpot and examine roots. Trim brown mushy sections. Dust cuts with cinnamon (natural antifungal)."),
            ("Day 2", "Repot", "Use <strong>RootBoost Soil Enhancer</strong> blend. Plant in <strong>Self-Watering Planter</strong>."),
            ("Day 4", "First water", "Water lightly with half-strength fertilizer solution"),
            ("Day 7", "Misting", "Mist foliage (not soil) to reduce transpiration stress"),
            ("Week 3", "Normal schedule", "Resume standard watering once new growth appears"),
        ],
        "prognosis": "If root rot is caught early (less than 40% root loss), recovery rate is high. Expect wilting to resolve in 5–10 days post-repotting."
    },
    "pests": {
        "condition": "Aphid / Spider Mite / Mealybug Infestation",
        "severity": "danger",
        "plant_guess": "Succulents, roses, or stressed houseplants",
        "issues": ["Visible insect clusters or webbing", "Honeydew secretions / sticky residue", "Distorted new growth", "White cottony deposits"],
        "immediate": "Isolate immediately. Blast with strong water spray to dislodge insects. Check all adjacent plants for spread.",
        "products": ["p1", "p3", "p2"],
        "schedule": [
            ("Day 1", "Manual removal", "Wipe leaves with neem-soaked cotton. Remove heavily infested stems."),
            ("Day 2", "AphidAway spray", "Apply <strong>AphidAway Concentrate</strong> (diluted 1:10) across all foliage"),
            ("Day 5", "Neem oil coat", "Full plant treatment with <strong>Neem Pest Guard</strong> — forms a protective barrier"),
            ("Day 7", "Inspect", "Check with magnifying glass. Particularly inspect leaf undersides and stem joints."),
            ("Day 10", "BioShield", "Apply <strong>BioShield Fungicide</strong> to prevent secondary infections"),
            ("Week 3", "Prevention spray", "Monthly neem oil as preventative"),
        ],
        "prognosis": "Pest eradication typically takes 2–3 spray cycles (14–21 days). New growth should emerge pest-free."
    },
    "healthy": {
        "condition": "Plant Appears Healthy",
        "severity": "ok",
        "plant_guess": "Healthy indoor or outdoor ornamental",
        "issues": ["No visible deficiencies", "Good leaf color and turgidity", "Normal growth pattern"],
        "immediate": "Your plant looks great! Maintain current care routine. Consider preventative feeding to sustain health.",
        "products": ["f3", "p1", "t2"],
        "schedule": [
            ("Weekly", "Watering", "Check soil moisture with <strong>Smart Moisture Meter</strong> — water when top 2 inches dry"),
            ("Bi-weekly", "Fertilize", "Apply <strong>SeaBloom Liquid Feed</strong> during growing season (spring–summer)"),
            ("Monthly", "Preventative spray", "<strong>Neem Pest Guard</strong> spray as a monthly shield against pests"),
            ("Quarterly", "Soil top-dress", "Add fresh compost to rejuvenate soil nutrition"),
        ],
        "prognosis": "With consistent preventative care, your plant should continue thriving. Monitor for early signs of stress."
    }
}

# ── HELPERS ───────────────────────────────────────────────────────────────────
def discount_pct(mrp, price):
    return int((1 - price / mrp) * 100)

def get_products_by_ids(ids):
    return [p for p in ALL_PRODUCTS if p["id"] in ids]

def render_product_card(p, cols=None):
    disc = discount_pct(p["mrp"], p["price"])
    return f"""
    <div class="product-card">
      <div class="product-img">{p['emoji']}</div>
      <div class="product-body">
        <div class="product-category">{p['category']}</div>
        <div class="product-name">{p['name']}</div>
        <div class="product-pricing">
          <span class="price-current">₹{p['price']}</span>
          <span class="price-original">₹{p['mrp']}</span>
          <span class="price-badge">{disc}% off</span>
        </div>
      </div>
    </div>"""

# ── NAVIGATION ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="verdura-nav">
  <div class="verdura-logo">Ver<span>dura</span></div>
  <div class="nav-links">
    <span class="nav-link">Indoor Plants</span>
    <span class="nav-link">Outdoor Plants</span>
    <span class="nav-link">Pots & Planters</span>
    <span class="nav-link">Fertilizers</span>
    <span class="nav-link">Pest Control</span>
    <span class="nav-link">Chlora AI</span>
    <span class="nav-link">About</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── PAGE TABS ──────────────────────────────────────────────────────────────────
tab_home, tab_chlora, tab_shop, tab_cart = st.tabs([
    "Home", "Chlora — Plant Intelligence", "Shop", f"Cart ({len(st.session_state.cart)})"
])

# ═══════════════════════════════════════════════════════════════════════════════
# HOME TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_home:
    # Hero
    st.markdown("""
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-eyebrow">AI Plant Intelligence Platform</div>
        <h1 class="hero-title">Meet <em>Chlora</em> —<br>Your Plant's Doctor,<br>Scheduler & Guide</h1>
        <p class="hero-sub">Upload a photo. Get an instant AI diagnosis, a personalized care schedule, and hand-picked treatment products — all in one place.</p>
        <div class="hero-cta-row">
          <button class="btn-primary">Diagnose My Plant</button>
          <button class="btn-outline">Shop Premium Plants</button>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Plants Diagnosed", "12,400+", "via Chlora AI")
    with c2:
        st.metric("Products", "200+", "curated SKUs")
    with c3:
        st.metric("Recovery Rate", "94%", "with AI plans")
    with c4:
        st.metric("Happy Gardeners", "8,200+", "subscribers")

    st.markdown('<hr class="v-divider">', unsafe_allow_html=True)

    # Featured Categories
    st.markdown('<div class="section-label">Browse by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Everything Your Plants Need</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    cats = [
        ("🌿", "Air Purifying Plants", "68 varieties"),
        ("🌵", "Succulents & Cacti", "45 varieties"),
        ("🌸", "Flowering Plants", "52 varieties"),
        ("🧪", "Organic Fertilizers", "30 products"),
        ("🛡️", "Pest Control", "22 solutions"),
        ("📦", "Smart Care Kits", "15 bundles"),
    ]
    cols = st.columns(6)
    for i, (em, name, sub) in enumerate(cats):
        with cols[i]:
            st.markdown(f"""
            <div style="background:var(--cream);border-radius:8px;padding:1.5rem 1rem;text-align:center;cursor:pointer;transition:transform 0.2s;border:1px solid rgba(28,58,43,0.06);">
              <div style="font-size:2rem;margin-bottom:0.5rem;">{em}</div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:0.95rem;color:var(--forest);font-weight:500;line-height:1.3;">{name}</div>
              <div style="font-size:0.72rem;color:var(--muted);margin-top:0.3rem;">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="v-divider">', unsafe_allow_html=True)

    # Bestsellers
    st.markdown('<div class="section-label">Bestsellers</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Most Loved This Season</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4)
    best = PRODUCTS["plants"][:2] + PRODUCTS["fertilizers"][:2]
    for i, p in enumerate(best):
        with cols[i]:
            st.markdown(render_product_card(p), unsafe_allow_html=True)
            if st.button(f"Add to Cart", key=f"best_{p['id']}"):
                st.session_state.cart.append(p)
                st.success(f"Added {p['name']} to cart!")

    st.markdown('<hr class="v-divider">', unsafe_allow_html=True)

    # Chlora Showcase
    st.markdown('<div class="section-label">Featured Technology</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Chlora Plant Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">The first AI trained exclusively on plant pathology. Upload any photo — Chlora identifies your plant, diagnoses the problem, and prescribes a complete recovery plan.</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    fcols = st.columns([1, 1, 1])
    features = [
        ("Visual Diagnosis", "Upload a photo and receive a full pathology report: species ID, health score, and root cause analysis — in under 10 seconds."),
        ("Treatment Protocol", "A day-by-day recovery schedule tailored to your plant's specific condition, with exact product dosages."),
        ("Smart Cart", "Every recommended product is one click from your cart. No guesswork, no generic advice."),
    ]
    for col, (title, desc) in zip(fcols, features):
        with col:
            st.markdown(f"""
            <div style="padding:1.5rem;border-left:2px solid var(--sage);">
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:var(--forest);margin-bottom:0.6rem;font-weight:500;">{title}</div>
              <div style="font-size:0.88rem;color:var(--muted);line-height:1.65;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="v-divider">', unsafe_allow_html=True)

    # Testimonials
    st.markdown('<div class="section-label">Customer Stories</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Verdura Transformed My Garden</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tcols = st.columns(3)
    testimonials = [
        ("Chlora identified root rot on my Monstera before I even noticed the symptoms. The recovery plan worked perfectly — 3 weeks later, it's thriving.", "Priya S., Mumbai"),
        ("I've tried every plant app out there. Nothing comes close to Verdura's diagnosis accuracy. The recommended products are exactly what my plants needed.", "Rahul M., Bengaluru"),
        ("The care scheduler is a game-changer. I used to guess at watering schedules. Now I follow Chlora's plan and my plants have never looked better.", "Ananya K., Pune"),
    ]
    for col, (text, author) in zip(tcols, testimonials):
        with col:
            st.markdown(f"""
            <div class="testimonial-card">
              <div class="testimonial-text">"{text}"</div>
              <div class="testimonial-author">— {author}</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CHLORA TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_chlora:
    col_left, col_right = st.columns([1, 1.1], gap="large")

    with col_left:
        st.markdown("""
        <div class="chlora-wrapper">
          <div class="chlora-badge">AI Plant Intelligence</div>
          <div class="chlora-title">Chlora<span> —</span></div>
          <div class="chlora-title" style="margin-top:-0.5rem;">Your Plant Pathologist</div>
          <div class="chlora-sub" style="margin-top:0.8rem;">
            Trained on 50,000+ plant diagnoses across 300+ species.
            Upload a photo of your troubled plant and receive a clinical-grade diagnosis, 
            tailored recovery schedule, and curated product recommendations.
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:var(--cream);border-radius:8px;padding:1.5rem;">
          <div style="font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--sage);margin-bottom:1rem;">Chlora Detects</div>
        """, unsafe_allow_html=True)

        detections = [
            ("Nutrient Deficiencies", "N, P, K, Mg, Fe, Ca"),
            ("Fungal & Bacterial Disease", "Leaf spot, blight, rot"),
            ("Pest Infestations", "Aphids, mites, mealybugs"),
            ("Watering Issues", "Over/under-watering, root rot"),
            ("Light & Environmental Stress", "Sunburn, cold damage"),
        ]
        for name, sub in detections:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.75rem;padding:0.5rem 0;border-bottom:1px solid rgba(28,58,43,0.06);">
              <div style="width:6px;height:6px;background:var(--sage);border-radius:50%;flex-shrink:0;"></div>
              <div>
                <span style="font-size:0.88rem;color:var(--forest);font-weight:500;">{name}</span>
                <span style="font-size:0.78rem;color:var(--muted);margin-left:0.5rem;">{sub}</span>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="background:var(--forest);border-radius:12px;padding:2rem;">
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--cream);margin-bottom:0.3rem;">Upload Plant Photo</div>
          <div style="font-size:0.82rem;color:rgba(245,240,232,0.5);margin-bottom:1.5rem;">JPG, PNG or WEBP — max 10MB</div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload your plant photo",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )

        st.markdown("""
          <div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:rgba(245,240,232,0.4);margin:1rem 0 0.5rem;">Or select symptom manually</div>
        """, unsafe_allow_html=True)

        symptom = st.selectbox(
            "Select symptom",
            ["— Choose a symptom —", "Yellowing leaves", "Brown spots / lesions", "Wilting / drooping", "Pest infestation visible", "Plant looks healthy"],
            label_visibility="collapsed"
        )

        plant_name = st.text_input("Plant name (optional)", placeholder="e.g. Monstera, Areca Palm, Rose...")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Run Chlora Diagnosis", use_container_width=True):
            symptom_map = {
                "Yellowing leaves": "yellowing",
                "Brown spots / lesions": "spots",
                "Wilting / drooping": "wilting",
                "Pest infestation visible": "pests",
                "Plant looks healthy": "healthy",
            }

            if uploaded:
                # Pick diagnosis based on file name hint or random
                fname = uploaded.name.lower()
                if any(k in fname for k in ["yellow", "yell"]): key = "yellowing"
                elif any(k in fname for k in ["spot", "brown", "dark"]): key = "spots"
                elif any(k in fname for k in ["wilt", "droop"]): key = "wilting"
                elif any(k in fname for k in ["pest", "bug", "insect"]): key = "pests"
                else: key = random.choice(["yellowing", "spots", "wilting", "pests"])
            elif symptom in symptom_map:
                key = symptom_map[symptom]
            else:
                st.warning("Please upload a photo or select a symptom.")
                key = None

            if key:
                with st.spinner("Chlora is analyzing your plant..."):
                    import time
                    time.sleep(2)
                st.session_state.diagnosis_result = key
                st.rerun()

    # ── DIAGNOSIS RESULT ────────────────────────────────────────────────────
    if st.session_state.diagnosis_result:
        d = DIAGNOSES[st.session_state.diagnosis_result]
        rec_products = get_products_by_ids(d["products"])

        st.markdown('<hr class="v-divider">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--sage);margin-bottom:0.5rem;">Chlora Diagnosis Report</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;color:var(--forest);margin-bottom:2rem;">Analysis Complete</div>
        """, unsafe_allow_html=True)

        r1, r2 = st.columns([1.1, 1], gap="large")

        with r1:
            severity_colors = {"warning": "#E8A838", "danger": "#D64C4C", "ok": "#4CAF6F"}
            severity_labels = {"warning": "Moderate Concern", "danger": "Urgent Attention Needed", "ok": "Healthy"}
            sev_color = severity_colors[d["severity"]]
            sev_label = severity_labels[d["severity"]]

            st.markdown(f"""
            <div style="background:var(--forest);border-radius:10px;padding:2rem;">
              <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.5rem;">
                <div style="width:12px;height:12px;border-radius:50%;background:{sev_color};box-shadow:0 0 10px {sev_color}55;flex-shrink:0;"></div>
                <div style="color:{sev_color};font-size:0.8rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;">{sev_label}</div>
              </div>

              <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:var(--cream);margin-bottom:0.3rem;">{d['condition']}</div>
              <div style="font-size:0.82rem;color:rgba(245,240,232,0.5);margin-bottom:1.5rem;font-style:italic;">{d['plant_guess']}</div>

              <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--mint);margin-bottom:0.5rem;">Issues Identified</div>
              {"".join(f'<div class="diag-pill red">{issue}</div>' for issue in d["issues"])}

              <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--mint);margin-top:1.2rem;margin-bottom:0.5rem;">Immediate Action</div>
              <div style="color:rgba(245,240,232,0.75);font-size:0.88rem;line-height:1.65;">{d['immediate']}</div>

              <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--mint);margin-top:1.2rem;margin-bottom:0.5rem;">Prognosis</div>
              <div style="color:rgba(245,240,232,0.75);font-size:0.88rem;line-height:1.65;">{d['prognosis']}</div>
            </div>""", unsafe_allow_html=True)

        with r2:
            # Care Schedule
            st.markdown("""
            <div style="background:var(--forest);border-radius:10px;padding:2rem;margin-bottom:1.5rem;">
              <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);margin-bottom:1.2rem;">Recovery Schedule</div>
            """, unsafe_allow_html=True)

            for day, task, detail in d["schedule"]:
                st.markdown(f"""
                <div class="schedule-row">
                  <div class="schedule-day">{day}</div>
                  <div class="schedule-task"><strong>{task}</strong><br><span style="font-weight:300;">{detail}</span></div>
                </div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Recommended Products
        st.markdown("""
        <div style="font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--sage);margin-bottom:0.5rem;margin-top:1rem;">Chlora Recommends</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:var(--forest);margin-bottom:1.2rem;">Curated Treatment Products</div>
        """, unsafe_allow_html=True)

        for p in rec_products:
            disc = discount_pct(p["mrp"], p["price"])
            rc1, rc2 = st.columns([4, 1])
            with rc1:
                st.markdown(f"""
                <div style="background:var(--cream);border-radius:8px;padding:1rem 1.2rem;display:flex;align-items:center;gap:1rem;border:1px solid rgba(28,58,43,0.08);">
                  <div style="font-size:2rem;">{p['emoji']}</div>
                  <div style="flex:1;">
                    <div style="font-size:0.65rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--sage);">{p['category']}</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;color:var(--forest);font-weight:500;">{p['name']}</div>
                    <div style="font-size:0.8rem;color:var(--muted);">{p['desc']}</div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-size:1.05rem;font-weight:600;color:var(--forest);">₹{p['price']}</div>
                    <div style="font-size:0.75rem;color:var(--muted);text-decoration:line-through;">₹{p['mrp']}</div>
                    <div style="font-size:0.65rem;background:#E8F5E0;color:#3A7D44;padding:0.15rem 0.4rem;border-radius:10px;">{disc}% off</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with rc2:
                if st.button(f"Add to Cart", key=f"rec_{p['id']}_{st.session_state.diagnosis_result}"):
                    st.session_state.cart.append(p)
                    st.success(f"Added!")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Add Complete Recovery Kit to Cart", use_container_width=True):
            for p in rec_products:
                st.session_state.cart.append(p)
            st.success(f"Added {len(rec_products)} products to your cart!")

        if st.button("Clear Diagnosis", use_container_width=True):
            st.session_state.diagnosis_result = None
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# SHOP TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_shop:
    st.markdown('<div class="section-label">The Verdura Store</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Premium Plants & Care Products</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    filter_col, _ = st.columns([1, 3])
    with filter_col:
        category_filter = st.selectbox(
            "Category",
            ["All", "Plants", "Fertilizers", "Pest Control", "Pots & Planters", "Tools", "Care Kits"]
        )

    cat_map = {
        "All": ALL_PRODUCTS,
        "Plants": PRODUCTS["plants"],
        "Fertilizers": PRODUCTS["fertilizers"],
        "Pest Control": PRODUCTS["pesticides"],
        "Pots & Planters": PRODUCTS["pots"],
        "Tools": PRODUCTS["tools"],
        "Care Kits": PRODUCTS["kits"],
    }
    display_products = cat_map[category_filter]

    cols = st.columns(4)
    for i, p in enumerate(display_products):
        with cols[i % 4]:
            st.markdown(render_product_card(p), unsafe_allow_html=True)
            if st.button(f"Add to Cart", key=f"shop_{p['id']}"):
                st.session_state.cart.append(p)
                st.success(f"Added {p['name']}!")

# ═══════════════════════════════════════════════════════════════════════════════
# CART TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_cart:
    st.markdown('<div class="section-label">Your Selection</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Shopping Cart</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;background:var(--cream);border-radius:8px;">
          <div style="font-size:3rem;margin-bottom:1rem;">🌿</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:var(--forest);margin-bottom:0.5rem;">Your cart is empty</div>
          <div style="color:var(--muted);font-size:0.9rem;">Use Chlora to diagnose your plant and get product recommendations, or browse the shop.</div>
        </div>""", unsafe_allow_html=True)
    else:
        total = sum(p["price"] for p in st.session_state.cart)
        total_mrp = sum(p["mrp"] for p in st.session_state.cart)
        savings = total_mrp - total

        cart_col, summary_col = st.columns([2, 1], gap="large")

        with cart_col:
            for i, p in enumerate(st.session_state.cart):
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:1rem;padding:1rem;background:var(--cream);border-radius:8px;margin-bottom:0.75rem;border:1px solid rgba(28,58,43,0.06);">
                      <div style="font-size:2rem;">{p['emoji']}</div>
                      <div style="flex:1;">
                        <div style="font-size:0.65rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--sage);">{p['category']}</div>
                        <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;color:var(--forest);font-weight:500;">{p['name']}</div>
                      </div>
                      <div style="font-size:1rem;font-weight:600;color:var(--forest);">₹{p['price']}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()

        with summary_col:
            st.markdown(f"""
            <div style="background:var(--forest);border-radius:10px;padding:2rem;position:sticky;top:80px;">
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--cream);margin-bottom:1.5rem;">Order Summary</div>
              <div style="display:flex;justify-content:space-between;color:rgba(245,240,232,0.6);font-size:0.85rem;margin-bottom:0.7rem;">
                <span>Subtotal ({len(st.session_state.cart)} items)</span><span>₹{total_mrp}</span>
              </div>
              <div style="display:flex;justify-content:space-between;color:#4CAF6F;font-size:0.85rem;margin-bottom:0.7rem;">
                <span>Verdura Savings</span><span>-₹{savings}</span>
              </div>
              <div style="display:flex;justify-content:space-between;color:rgba(245,240,232,0.5);font-size:0.82rem;margin-bottom:1.2rem;">
                <span>Shipping</span><span>Free above ₹999</span>
              </div>
              <div style="border-top:1px solid rgba(245,240,232,0.1);padding-top:1rem;display:flex;justify-content:space-between;color:var(--cream);font-size:1rem;font-weight:600;margin-bottom:1.5rem;">
                <span>Total</span><span>₹{total}</span>
              </div>
            </div>""", unsafe_allow_html=True)

            if st.button("Proceed to Checkout", use_container_width=True):
                st.success("Order placed! Your plants are on their way.")
                st.session_state.cart = []
                st.rerun()

            if st.button("Clear Cart", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="verdura-footer">
  <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:3rem;margin-bottom:2rem;">
    <div>
      <div class="footer-logo">Ver<span>dura</span></div>
      <div class="footer-tagline">"Diagnose, Nurture, Grow — Intelligently."</div>
      <div style="color:rgba(245,240,232,0.4);font-size:0.8rem;line-height:1.7;">India's first AI-powered plant care ecosystem. We combine botanical expertise with machine learning to keep every plant thriving.</div>
    </div>
    <div>
      <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem;">Shop</div>
      <div style="color:rgba(245,240,232,0.5);font-size:0.82rem;line-height:2.2;">Indoor Plants<br>Outdoor Plants<br>Fertilizers<br>Pest Control<br>Pots & Planters</div>
    </div>
    <div>
      <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem;">Chlora AI</div>
      <div style="color:rgba(245,240,232,0.5);font-size:0.82rem;line-height:2.2;">Plant Diagnosis<br>Care Scheduler<br>Product Recs<br>Subscription Plans</div>
    </div>
    <div>
      <div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem;">Company</div>
      <div style="color:rgba(245,240,232,0.5);font-size:0.82rem;line-height:2.2;">About Verdura<br>Privacy Policy<br>Shipping Policy<br>Contact Us</div>
    </div>
  </div>
  <div class="footer-bottom">© 2025 Verdura Plant Intelligence Pvt. Ltd. All rights reserved.</div>
</div>
""", unsafe_allow_html=True)
