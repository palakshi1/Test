"""
🌿 PlantPal — AI-Powered Plant Care E-Commerce App
Single-file Streamlit application with AI Plant Doctor chatbot.
Run with: streamlit run app.py
"""

import streamlit as st
import random
from PIL import Image
import io
import base64
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PlantPal 🌿",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — organic/botanical aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --cream:   #f7f3ec;
    --sage:    #7a9e7e;
    --moss:    #3d6b45;
    --bark:    #5c3d2e;
    --soil:    #2b1d0e;
    --petal:   #e8c5a0;
    --dew:     #d4edda;
    --rust:    #c0604a;
    --gold:    #c9952a;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--soil);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2b3d2c 0%, #1a2e1b 100%);
    color: #e8f5e9;
}
[data-testid="stSidebar"] * { color: #e8f5e9 !important; }
[data-testid="stSidebar"] .stRadio > label { font-size: 1rem; letter-spacing: 0.03em; }
[data-testid="stSidebar"] hr { border-color: #3d6b45; }

/* Headers */
h1, h2, h3 { font-family: 'Playfair Display', serif; }

/* Buttons */
.stButton > button {
    background: var(--moss);
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.4rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.04em;
    transition: background 0.2s;
}
.stButton > button:hover { background: var(--bark); }

/* Product cards */
.product-card {
    background: #fff;
    border: 1px solid #dce8dc;
    border-radius: 12px;
    padding: 1.25rem;
    height: 100%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}
.product-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}
.product-emoji { font-size: 2.8rem; margin-bottom: 0.4rem; }
.product-name { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: var(--moss); margin: 0; }
.product-category { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--sage); background: var(--dew); display: inline-block; padding: 2px 8px; border-radius: 20px; margin: 4px 0 6px; }
.product-price { font-size: 1.2rem; font-weight: 700; color: var(--bark); }
.product-mrp { font-size: 0.78rem; color: #999; text-decoration: line-through; margin-left: 4px; }
.product-desc { font-size: 0.82rem; color: #555; line-height: 1.5; margin: 6px 0; }
.product-usage { font-size: 0.78rem; color: var(--moss); background: var(--dew); border-left: 3px solid var(--sage); padding: 4px 8px; border-radius: 0 4px 4px 0; margin-top: 8px; }

/* Chat bubbles */
.chat-user {
    background: var(--moss);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.65rem 1rem;
    margin: 0.5rem 0 0.5rem 20%;
    font-size: 0.9rem;
    line-height: 1.5;
}
.chat-bot {
    background: #fff;
    border: 1px solid #dce8dc;
    color: var(--soil);
    border-radius: 18px 18px 18px 4px;
    padding: 0.65rem 1rem;
    margin: 0.5rem 20% 0.5rem 0;
    font-size: 0.9rem;
    line-height: 1.6;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.chat-label { font-size: 0.7rem; color: #888; margin: 2px 4px; }
.chat-label-right { text-align: right; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #2b3d2c 0%, #3d6b45 50%, #5a8f63 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    color: #e8f5e9;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.hero-banner h1 { color: #e8f5e9 !important; font-size: 2.6rem; margin: 0; }
.hero-banner p { color: #b2dfbc; font-size: 1.05rem; margin: 0.5rem 0 0; }
.hero-leaf { position: absolute; right: 2rem; top: 50%; transform: translateY(-50%); font-size: 7rem; opacity: 0.18; }

/* Badge */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-fertilizer { background: #e8f5e9; color: #2e7d32; }
.badge-pesticide   { background: #fff3e0; color: #e65100; }
.badge-tool        { background: #e3f2fd; color: #1565c0; }
.badge-soil        { background: #fce4ec; color: #880e4f; }

/* Diagnosis card */
.diagnosis-card {
    background: linear-gradient(135deg, #f0f8f1, #e8f5e9);
    border: 1px solid #a5d6a7;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin: 1rem 0;
}
.diagnosis-title { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: var(--moss); margin-bottom: 0.5rem; }

/* Schedule table */
.schedule-row { display: flex; gap: 0.5rem; align-items: center; padding: 4px 0; font-size: 0.88rem; }
.schedule-day { font-weight: 600; color: var(--moss); min-width: 90px; }
.schedule-task { color: #444; }

/* Divider with leaf */
.leaf-divider { text-align: center; color: var(--sage); font-size: 1.2rem; margin: 0.5rem 0; opacity: 0.5; }

/* Feature tiles */
.feature-tile {
    background: #fff;
    border-radius: 10px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.feature-icon { font-size: 2.2rem; }
.feature-title { font-family: 'Playfair Display', serif; font-size: 1rem; color: var(--moss); margin-top: 0.4rem; }
.feature-desc { font-size: 0.82rem; color: #666; margin-top: 0.25rem; }

/* Metric pill */
.metric-pill {
    background: var(--dew);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    text-align: center;
}
.metric-value { font-size: 1.6rem; font-weight: 700; color: var(--moss); }
.metric-label { font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.06em; }

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PRODUCT CATALOG  (in-memory)
# ─────────────────────────────────────────────
PRODUCTS = [
    {
        "id": "P001",
        "name": "Organic Growth Booster",
        "category": "Fertilizer",
        "emoji": "🌱",
        "price": 349,
        "mrp": 499,
        "description": "Balanced NPK formula enriched with humic acid and seaweed extract. Promotes lush, vigorous growth.",
        "usage": "Apply 50g per plant every 3–4 days. Mix with soil or dissolve in water.",
        "conditions": ["dry", "weak", "yellow leaves", "slow growth"],
    },
    {
        "id": "P002",
        "name": "Neem-Guard Pesticide Spray",
        "category": "Pesticide",
        "emoji": "🛡️",
        "price": 279,
        "mrp": 399,
        "description": "Cold-pressed neem oil concentrate. Controls aphids, spider mites, whiteflies, and fungal infections naturally.",
        "usage": "Dilute 5ml per litre of water. Spray on leaves every 5 days until pest-free.",
        "conditions": ["pest attack", "fungal infection", "spots on leaves", "insects"],
    },
    {
        "id": "P003",
        "name": "AquaSave Moisture Granules",
        "category": "Soil",
        "emoji": "💧",
        "price": 199,
        "mrp": 299,
        "description": "Hydrogel-based water-retention granules that keep roots moist for up to 7 days.",
        "usage": "Mix 10g into soil before potting. Reduces watering frequency by 40%.",
        "conditions": ["dry", "wilting", "drought stress", "dehydrated"],
    },
    {
        "id": "P004",
        "name": "RootRevive Rooting Hormone",
        "category": "Fertilizer",
        "emoji": "🌿",
        "price": 189,
        "mrp": 249,
        "description": "Indole-3-butyric acid formula for strong root development. Ideal for propagation and transplanting.",
        "usage": "Dip cutting base in powder before planting. Apply diluted solution weekly after repotting.",
        "conditions": ["transplant shock", "root rot", "weak roots", "repotting"],
    },
    {
        "id": "P005",
        "name": "FungoClear Systemic Fungicide",
        "category": "Pesticide",
        "emoji": "🍄",
        "price": 319,
        "mrp": 449,
        "description": "Broad-spectrum systemic fungicide. Eliminates powdery mildew, black spot, rust, and blight.",
        "usage": "Mix 2g per litre. Drench soil and spray leaves every 7 days for 3 weeks.",
        "conditions": ["fungal infection", "white powder on leaves", "blight", "rust spots"],
    },
    {
        "id": "P006",
        "name": "CompoRich Vermicompost",
        "category": "Fertilizer",
        "emoji": "🪱",
        "price": 249,
        "mrp": 349,
        "description": "Premium worm castings packed with beneficial microbes. Improves soil structure and nutrient availability.",
        "usage": "Add 100g to topsoil monthly. Mix thoroughly and water generously.",
        "conditions": ["poor soil", "yellow leaves", "slow growth", "nutrient deficiency"],
    },
    {
        "id": "P007",
        "name": "ErgoGrip Pruning Shears",
        "category": "Tool",
        "emoji": "✂️",
        "price": 599,
        "mrp": 799,
        "description": "Japanese SK5 steel blades, non-slip rubber grip. Makes clean cuts to prevent disease entry.",
        "usage": "Sterilise blades with alcohol before use. Ideal for shaping, deadheading, and removing dead branches.",
        "conditions": ["dead branches", "overgrown", "pruning needed", "shaping"],
    },
    {
        "id": "P008",
        "name": "SoilSense pH Testing Kit",
        "category": "Tool",
        "emoji": "🧪",
        "price": 449,
        "mrp": 599,
        "description": "Digital 3-in-1 meter: soil pH, moisture, and light intensity. Takes guesswork out of plant care.",
        "usage": "Insert probe 5cm into soil. Reads pH 3.5–9, moisture 0–10, and light 0–2000 lux.",
        "conditions": ["yellowing", "nutrient lockout", "overwatering", "general diagnosis"],
    },
    {
        "id": "P009",
        "name": "MicroBloom Liquid Foliar Feed",
        "category": "Fertilizer",
        "emoji": "🌸",
        "price": 229,
        "mrp": 329,
        "description": "High-potassium + phosphorus formula for prolific blooming. Chelated iron prevents chlorosis.",
        "usage": "Dilute 3ml per litre. Spray on leaves and soil weekly during flowering season.",
        "conditions": ["no flowers", "pale leaves", "iron deficiency", "chlorosis"],
    },
    {
        "id": "P010",
        "name": "SilverShield Insecticidal Soap",
        "category": "Pesticide",
        "emoji": "🪲",
        "price": 159,
        "mrp": 219,
        "description": "Potassium salt of fatty acids. Targets soft-bodied insects on contact without harming beneficial bugs.",
        "usage": "Mix 10ml per litre of water. Spray entire plant including undersides of leaves. Repeat every 3 days.",
        "conditions": ["aphids", "pest attack", "mealybugs", "scale insects"],
    },
]

CATEGORY_BADGE = {
    "Fertilizer": "badge-fertilizer",
    "Pesticide":  "badge-pesticide",
    "Tool":       "badge-tool",
    "Soil":       "badge-soil",
}

# ─────────────────────────────────────────────
# AI DIAGNOSIS ENGINE  (rule-based simulation)
# ─────────────────────────────────────────────

CONDITIONS = {
    "dry": {
        "label": "Drought / Dry Stress 🏜️",
        "description": "The plant shows signs of water deficit — wilting, dry soil crust, and curling leaves. Without intervention, cell damage and leaf drop will follow.",
        "product_ids": ["P001", "P003", "P006"],
        "schedule": [
            ("Mon", "Water thoroughly + apply AquaSave Moisture Granules to topsoil"),
            ("Tue", "Mist foliage lightly to reduce transpiration stress"),
            ("Thu", "Apply 50g Organic Growth Booster dissolved in 500ml water"),
            ("Sat", "Check soil moisture with SoilSense kit; add granules if dry again"),
            ("Sun", "Light foliar spray of MicroBloom if leaves remain pale"),
        ],
    },
    "pest": {
        "label": "Pest Infestation 🐛",
        "description": "Visible signs of insect activity — discoloured patches, sticky residue (honeydew), webbing, or tiny moving specks on leaves and stems.",
        "product_ids": ["P002", "P010", "P007"],
        "schedule": [
            ("Mon", "Spray Neem-Guard Pesticide on all leaf surfaces (top + bottom)"),
            ("Wed", "Apply SilverShield Insecticidal Soap — focus on stems and nodes"),
            ("Fri", "Repeat Neem-Guard spray; prune severely infested branches with ErgoGrip Shears"),
            ("Sun", "Inspect carefully; re-treat with Neem-Guard if pests persist"),
        ],
    },
    "fungal": {
        "label": "Fungal / Mould Infection 🍄",
        "description": "White powdery coating, brown rust spots, or black sooty mould detected. Fungal pathogens spread rapidly in humid conditions.",
        "product_ids": ["P005", "P002", "P008"],
        "schedule": [
            ("Mon", "Soil drench + foliar spray with FungoClear Systemic Fungicide"),
            ("Thu", "Follow-up spray of Neem-Guard to suppress spore germination"),
            ("Sat", "Test soil pH with SoilSense — aim for 6.0–6.8 to reduce fungal spread"),
            ("Sun", "Remove and bag all affected leaves to prevent recontamination"),
        ],
    },
    "yellow": {
        "label": "Nutrient Deficiency / Chlorosis 🟡",
        "description": "Interveinal yellowing, pale new growth, and reduced vigour indicate a macro or micro-nutrient deficiency — commonly nitrogen, iron, or magnesium.",
        "product_ids": ["P009", "P001", "P006"],
        "schedule": [
            ("Mon", "Apply MicroBloom Liquid Foliar Feed (3ml/L) directly to leaves"),
            ("Wed", "Top-dress with 100g CompoRich Vermicompost; water in well"),
            ("Fri", "Diluted Organic Growth Booster drench (50g in 1L water per plant)"),
            ("Sun", "Assess leaf colour improvement; repeat foliar feed if no change"),
        ],
    },
    "overwatered": {
        "label": "Overwatering / Root Rot 💦",
        "description": "Soggy soil, mushy stems at the base, and drooping despite wet soil point to root oxygen starvation and potential rot fungi.",
        "product_ids": ["P004", "P005", "P008"],
        "schedule": [
            ("Mon", "Repot into fresh, well-draining soil; apply RootRevive Rooting Hormone to roots"),
            ("Wed", "Light FungoClear drench to prevent rot-associated fungi"),
            ("Fri", "Monitor — water only when top 2cm of soil is dry; test with SoilSense"),
            ("Sun", "Apply diluted RootRevive as soil drench to stimulate root recovery"),
        ],
    },
    "healthy": {
        "label": "Plant Looks Healthy 🌟",
        "description": "No acute stress detected! The plant shows good colour, firm stems, and no visible pest or disease signs. Focus on maintenance nutrition.",
        "product_ids": ["P001", "P006", "P009"],
        "schedule": [
            ("Mon", "Regular watering; apply Organic Growth Booster (50g) every week"),
            ("Thu", "Top-dress with CompoRich Vermicompost for microbe diversity"),
            ("Sat", "Optional foliar feed with MicroBloom for enhanced flowering"),
        ],
    },
}

def detect_condition_from_image(image: Image.Image) -> str:
    """
    Simulate plant condition detection from an uploaded image.
    In a real app, this would call a vision model API (e.g. Claude claude-sonnet-4-20250514 or GPT-4o).
    Here we use image statistics as a lightweight proxy.
    """
    # Convert to RGB to ensure consistent analysis
    img_rgb = image.convert("RGB").resize((100, 100))

    # Sample pixel statistics
    pixels = list(img_rgb.getdata())
    r_avg = sum(p[0] for p in pixels) / len(pixels)
    g_avg = sum(p[1] for p in pixels) / len(pixels)
    b_avg = sum(p[2] for p in pixels) / len(pixels)

    brightness = (r_avg + g_avg + b_avg) / 3

    # Rule-based heuristic mapping colours → conditions
    if g_avg > r_avg * 1.3 and g_avg > b_avg * 1.2 and brightness > 100:
        return "healthy"
    elif r_avg > g_avg * 1.2 and r_avg > b_avg * 1.1:
        return "pest"
    elif b_avg > r_avg * 1.1 and brightness < 90:
        return "overwatered"
    elif r_avg > 160 and g_avg > 130 and g_avg < r_avg:
        return "yellow"
    elif brightness < 75:
        return "fungal"
    elif g_avg < 90 and brightness < 120:
        return "dry"
    else:
        # Weighted random fallback so demo always returns something meaningful
        return random.choice(["dry", "pest", "yellow", "healthy"])


def get_products_by_ids(ids: list) -> list:
    """Return product dicts matching the given IDs."""
    return [p for p in PRODUCTS if p["id"] in ids]


def build_diagnosis_response(condition_key: str) -> str:
    """
    Compose a rich markdown-flavoured plain text response
    for display in the chat interface.
    """
    cond = CONDITIONS[condition_key]
    recs = get_products_by_ids(cond["product_ids"])

    lines = []
    lines.append(f"**🔍 Diagnosis: {cond['label']}**\n")
    lines.append(f"{cond['description']}\n")
    lines.append("---")
    lines.append("**🛍️ Recommended Products from Our Catalog:**\n")
    for prod in recs:
        lines.append(
            f"• **{prod['emoji']} {prod['name']}** — ₹{prod['price']}  \n"
            f"  _{prod['description']}_  \n"
            f"  📋 Usage: {prod['usage']}"
        )
    lines.append("\n---")
    lines.append("**📅 Weekly Care Schedule:**\n")
    for day, task in cond["schedule"]:
        lines.append(f"• **{day}:** {task}")
    lines.append("\n---")
    lines.append("_💬 Ask me anything else about your plant or our products!_")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"


# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:3rem;'>🌿</div>
        <div style='font-family: "Playfair Display", serif; font-size:1.5rem; color:#b2dfbc; font-weight:700;'>PlantPal</div>
        <div style='font-size:0.78rem; color:#6a9c6e; letter-spacing:0.1em; text-transform:uppercase;'>Your Green Companion</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠 Home", "🛍️ Shop Products", "🤖 AI Plant Doctor"],
        index=["🏠 Home", "🛍️ Shop Products", "🤖 AI Plant Doctor"].index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.divider()

    # Mini cart summary
    if st.session_state.cart:
        st.markdown(f"🛒 **Cart:** {len(st.session_state.cart)} item(s)")
        total = sum(p["price"] for p in st.session_state.cart)
        st.markdown(f"💰 **Total:** ₹{total}")
        if st.button("🗑️ Clear Cart"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.markdown("<div style='font-size:0.8rem; color:#6a9c6e;'>🛒 Your cart is empty</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size:0.72rem; color:#4a6b4d; text-align:center;'>Made with 🌱 for plant lovers<br/>© 2025 PlantPal</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
def render_home():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-leaf">🌿</div>
        <h1>Welcome to PlantPal</h1>
        <p>AI-powered plant care, expert products, and a greener home — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    stats = [("10+", "Products"), ("5", "Conditions Diagnosed"), ("100%", "Organic Options"), ("⭐ 4.8", "Avg. Rating")]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-pill">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Why PlantPal?")

    f1, f2, f3 = st.columns(3)
    features = [
        ("🤖", "AI Plant Doctor", "Upload a photo — get an instant diagnosis, product recommendations, and a care schedule."),
        ("🛍️", "Curated Catalog", "Hand-picked fertilizers, pesticides, and tools trusted by expert gardeners."),
        ("📅", "Care Schedules", "Personalised weekly routines so you never miss a treatment."),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3], features):
        with col:
            st.markdown(f"""
            <div class="feature-tile">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Category highlights
    st.markdown("### Shop by Category")
    cats = [
        ("🌱", "Fertilizers", "Nourish & grow", "#e8f5e9", "#2e7d32"),
        ("🛡️", "Pesticides", "Protect naturally", "#fff3e0", "#e65100"),
        ("🔧", "Tools", "Work smarter", "#e3f2fd", "#1565c0"),
        ("🌍", "Soil & Media", "Build from roots", "#fce4ec", "#880e4f"),
    ]
    cols = st.columns(4)
    for col, (icon, name, tag, bg, fg) in zip(cols, cats):
        with col:
            st.markdown(f"""
            <div style="background:{bg}; border-radius:10px; padding:1.1rem; text-align:center; cursor:pointer;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-weight:700; color:{fg}; font-size:0.95rem;">{name}</div>
                <div style="font-size:0.75rem; color:#777; margin-top:2px;">{tag}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🛍️ Browse All Products", use_container_width=True):
            st.session_state.page = "🛍️ Shop Products"
            st.rerun()
    with col_b:
        if st.button("🤖 Diagnose My Plant Now", use_container_width=True):
            st.session_state.page = "🤖 AI Plant Doctor"
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: SHOP
# ─────────────────────────────────────────────
def render_shop():
    st.markdown("## 🛍️ Shop Products")
    st.caption(f"{len(PRODUCTS)} products available — free delivery on orders above ₹999")
    st.divider()

    # Filter bar
    all_cats = ["All"] + sorted({p["category"] for p in PRODUCTS})
    filter_col, sort_col, _ = st.columns([2, 2, 3])
    with filter_col:
        cat_filter = st.selectbox("Category", all_cats)
    with sort_col:
        sort_by = st.selectbox("Sort by", ["Default", "Price: Low → High", "Price: High → Low"])

    # Apply filters
    display = PRODUCTS if cat_filter == "All" else [p for p in PRODUCTS if p["category"] == cat_filter]
    if sort_by == "Price: Low → High":
        display = sorted(display, key=lambda x: x["price"])
    elif sort_by == "Price: High → Low":
        display = sorted(display, key=lambda x: x["price"], reverse=True)

    st.markdown(f"<div style='font-size:0.82rem; color:#888; margin-bottom:0.8rem;'>Showing {len(display)} product(s)</div>", unsafe_allow_html=True)

    # Grid — 3 per row
    cols_per_row = 3
    for row_start in range(0, len(display), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, prod in zip(cols, display[row_start:row_start + cols_per_row]):
            with col:
                badge_class = CATEGORY_BADGE.get(prod["category"], "badge-fertilizer")
                discount = round((1 - prod["price"] / prod["mrp"]) * 100)
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-emoji">{prod['emoji']}</div>
                    <div class="product-name">{prod['name']}</div>
                    <span class="badge {badge_class}">{prod['category']}</span>
                    <div>
                        <span class="product-price">₹{prod['price']}</span>
                        <span class="product-mrp">₹{prod['mrp']}</span>
                        <span style="font-size:0.72rem; color:#c62828; font-weight:600; margin-left:4px;">{discount}% OFF</span>
                    </div>
                    <div class="product-desc">{prod['description']}</div>
                    <div class="product-usage">📋 {prod['usage']}</div>
                </div>
                """, unsafe_allow_html=True)

                # Add to cart button
                if st.button(f"Add to Cart", key=f"cart_{prod['id']}"):
                    st.session_state.cart.append(prod)
                    st.toast(f"✅ {prod['name']} added to cart!", icon="🌿")


# ─────────────────────────────────────────────
# PAGE: AI PLANT DOCTOR
# ─────────────────────────────────────────────
def render_chat_message(role: str, content: str):
    """Render a single chat bubble."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-label chat-label-right">You</div>
        <div class="chat-user">{content}</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-label">🌿 PlantPal AI</div>
        <div class="chat-bot">{content}</div>
        """, unsafe_allow_html=True)


def render_ai_doctor():
    st.markdown("## 🤖 AI Plant Doctor")
    st.caption("Upload a plant photo and chat with our AI for instant diagnosis, product recs, and a care schedule.")
    st.divider()

    left, right = st.columns([1, 1.6], gap="large")

    # ── LEFT: Image upload + controls ──
    with left:
        st.markdown("### 📷 Upload Plant Photo")
        uploaded = st.file_uploader(
            "Upload an image of your plant",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )

        if uploaded:
            img = Image.open(uploaded)
            st.session_state.uploaded_image = img
            st.image(img, use_container_width=True, caption="Your uploaded plant")

        # Analyse button
        if st.session_state.uploaded_image:
            if st.button("🔬 Analyse My Plant", use_container_width=True):
                with st.spinner("Analysing plant health…"):
                    condition_key = detect_condition_from_image(st.session_state.uploaded_image)
                    response = build_diagnosis_response(condition_key)
                    cond = CONDITIONS[condition_key]

                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": "📷 [Plant image uploaded] — Please diagnose my plant and recommend products.",
                    })
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "condition": condition_key,
                        "products": get_products_by_ids(cond["product_ids"]),
                    })
                    st.session_state.analyzed = True
                st.rerun()
        else:
            st.info("Upload a photo above to begin diagnosis.", icon="👆")

        # Tips
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💡 Tips for best results"):
            st.markdown("""
- Take photos in good natural light
- Capture the whole plant + a close-up of affected areas
- Ensure the image is in focus
- Include both leaves and soil if possible
            """)

    # ── RIGHT: Chat interface ──
    with right:
        st.markdown("### 💬 Chat with PlantPal AI")

        # Chat container
        chat_container = st.container(height=480, border=True)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style='text-align:center; padding:3rem 1rem; color:#aaa;'>
                    <div style='font-size:3rem;'>🌿</div>
                    <div style='font-size:0.9rem; margin-top:0.5rem;'>Upload a plant photo and click <strong>Analyse My Plant</strong> to start!</div>
                    <div style='font-size:0.8rem; margin-top:0.3rem; color:#bbb;'>Or type a question below.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    render_chat_message(msg["role"], msg["content"])

        # Text input for follow-up questions
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_text = st.text_input(
                "Ask a question",
                placeholder="e.g. How often should I water? Which fertilizer is best?",
                label_visibility="collapsed",
                key="chat_input",
            )
        with btn_col:
            send = st.button("Send", use_container_width=True)

        if send and user_text.strip():
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_text})

            # Generate contextual response (keyword-based simulation)
            lower = user_text.lower()
            if any(w in lower for w in ["fertiliz", "feed", "nutrient", "npk"]):
                fert = [p for p in PRODUCTS if p["category"] == "Fertilizer"]
                answer = "Here are our top fertilizers:\n\n" + "\n".join(
                    f"• **{p['emoji']} {p['name']}** (₹{p['price']}) — {p['description']}" for p in fert[:3]
                )
            elif any(w in lower for w in ["pest", "insect", "bug", "aphid", "spray"]):
                pests = [p for p in PRODUCTS if p["category"] == "Pesticide"]
                answer = "For pest control we recommend:\n\n" + "\n".join(
                    f"• **{p['emoji']} {p['name']}** (₹{p['price']}) — {p['description']}" for p in pests[:3]
                )
            elif any(w in lower for w in ["water", "how often", "irrigation", "drip"]):
                answer = (
                    "**Watering frequency** depends on the plant type, pot size, and season:\n\n"
                    "• Tropical plants: every 2–3 days in summer, weekly in winter\n"
                    "• Succulents & cacti: every 10–14 days\n"
                    "• Ferns & moisture lovers: keep soil consistently moist\n\n"
                    "💡 Our **AquaSave Moisture Granules** (P003) can reduce watering frequency by up to 40%!"
                )
            elif any(w in lower for w in ["yellow", "yellowing", "pale", "chloro"]):
                answer = (
                    "**Yellowing leaves** are usually caused by nutrient deficiency, overwatering, or poor light.\n\n"
                    "We recommend:\n"
                    "• **🌸 MicroBloom Liquid Foliar Feed** — corrects iron & micro-nutrient deficiency\n"
                    "• **🌱 Organic Growth Booster** — broad NPK support\n"
                    "• **🧪 SoilSense pH Testing Kit** — rule out pH-related nutrient lockout\n\n"
                    "Would you like a detailed care plan? Upload a photo for a personalised diagnosis!"
                )
            elif any(w in lower for w in ["price", "cost", "cheap", "afford", "budget"]):
                cheap = sorted(PRODUCTS, key=lambda x: x["price"])[:3]
                answer = "Our most affordable options:\n\n" + "\n".join(
                    f"• **{p['emoji']} {p['name']}** — ₹{p['price']} _(MRP ₹{p['mrp']})_" for p in cheap
                )
            elif any(w in lower for w in ["hello", "hi", "hey", "namaste"]):
                answer = "👋 Hello! I'm PlantPal AI, your plant health assistant. Upload a photo for a diagnosis, or ask me anything about plant care or our products!"
            elif any(w in lower for w in ["tool", "shear", "prune", "cut"]):
                tools = [p for p in PRODUCTS if p["category"] == "Tool"]
                answer = "Our gardening tools:\n\n" + "\n".join(
                    f"• **{p['emoji']} {p['name']}** (₹{p['price']}) — {p['description']}" for p in tools
                )
            else:
                answer = (
                    "Great question! 🌿 For the most accurate advice, please upload a photo of your plant "
                    "so I can diagnose its specific condition.\n\n"
                    "In the meantime, here are a few general tips:\n"
                    "• Ensure adequate light (most plants need 6h+ indirect sunlight)\n"
                    "• Check soil moisture before watering — don't guess!\n"
                    "• Use balanced fertilizer monthly during the growing season\n\n"
                    "_Is there a specific product or issue I can help you with?_"
                )

            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        # Clear chat
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.analyzed = False
                st.rerun()

    # ── Product quick-add after analysis ──
    if st.session_state.analyzed:
        st.divider()
        st.markdown("### 🛍️ Recommended Products — Quick Add")

        # Get the last analysis products
        last_analysis = next(
            (m for m in reversed(st.session_state.chat_history) if m.get("products")),
            None
        )
        if last_analysis:
            prods = last_analysis["products"]
            cols = st.columns(len(prods))
            for col, prod in zip(cols, prods):
                with col:
                    discount = round((1 - prod["price"] / prod["mrp"]) * 100)
                    st.markdown(f"""
                    <div class="product-card" style="text-align:center;">
                        <div class="product-emoji">{prod['emoji']}</div>
                        <div class="product-name" style="font-size:0.9rem;">{prod['name']}</div>
                        <div style="margin:4px 0;">
                            <span class="product-price" style="font-size:1rem;">₹{prod['price']}</span>
                            <span class="product-mrp">₹{prod['mrp']}</span>
                        </div>
                        <div style="font-size:0.72rem; color:#c62828; font-weight:600;">{discount}% OFF</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🛒 Add", key=f"rec_cart_{prod['id']}", use_container_width=True):
                        st.session_state.cart.append(prod)
                        st.toast(f"✅ {prod['name']} added to cart!", icon="🌿")


# ─────────────────────────────────────────────
# ROUTER — render selected page
# ─────────────────────────────────────────────
if st.session_state.page == "🏠 Home":
    render_home()
elif st.session_state.page == "🛍️ Shop Products":
    render_shop()
elif st.session_state.page == "🤖 AI Plant Doctor":
    render_ai_doctor()
