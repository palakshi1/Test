"""
🌿 Leafy — Premium Plant E-Commerce (Ugaoo-inspired)
Single-file Streamlit app with full cart + floating AI chatbot.
Run: streamlit run app.py
"""

import streamlit as st
import random

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Leafy 🌿 | Bring Nature Home",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────
# GLOBAL CSS  –  Premium white + sage green + blush pink palette
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Jost:wght@300;400;500;600&display=swap');

:root {
  --white:#ffffff; --off:#f8f6f2; --cream:#f2ede6;
  --green:#3a6b47; --sage:#6b9e78; --light-g:#d6e8db;
  --pink:#e8a0a0; --blush:#fce8e8; --bark:#4a3728;
  --text:#1e1e1e; --muted:#6b6b6b; --border:#e8e0d8;
  --shadow:0 4px 24px rgba(0,0,0,0.08);
  --shadow-h:0 8px 36px rgba(0,0,0,0.14);
}

html, body, [class*="css"], .stApp {
  font-family: 'Jost', sans-serif;
  background: var(--off) !important;
  color: var(--text);
}
h1,h2,h3,h4 { font-family: 'Cormorant Garamond', serif; }

#MainMenu, footer, header, .stDeployButton { visibility:hidden !important; display:none !important; }
[data-testid="stSidebar"] { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }
section.main > div { padding:0 !important; }

/* Nav */
.nav-bar {
  background:var(--white); border-bottom:1px solid var(--border);
  padding:0 3rem; display:flex; align-items:center;
  justify-content:space-between; height:64px;
  position:sticky; top:0; z-index:999;
  box-shadow:0 1px 12px rgba(0,0,0,0.06);
}
.nav-logo { font-family:'Cormorant Garamond',serif; font-size:1.75rem; font-weight:700; color:var(--green); letter-spacing:-0.02em; }
.nav-logo span { color:var(--pink); }
.nav-cart { background:var(--green); color:white; padding:8px 18px; border-radius:30px; font-size:0.82rem; font-weight:600; }

/* Hero */
.hero {
  background:linear-gradient(120deg,#e8f0ea 0%,#f7ece9 50%,#edf4ee 100%);
  padding:5rem 4rem 4rem; display:flex; align-items:center;
  gap:3rem; min-height:460px; position:relative; overflow:hidden;
}
.hero::before {
  content:''; position:absolute; right:-60px; top:-60px;
  width:500px; height:500px;
  background:radial-gradient(circle,rgba(107,158,120,0.12) 0%,transparent 70%);
  border-radius:50%;
}
.hero-badge {
  display:inline-block; background:var(--blush); color:var(--pink);
  border:1px solid #f0c0c0; padding:5px 16px; border-radius:30px;
  font-size:0.76rem; font-weight:600; letter-spacing:0.08em;
  text-transform:uppercase; margin-bottom:1.2rem;
}
.hero-title { font-family:'Cormorant Garamond',serif; font-size:clamp(2.8rem,5vw,4.2rem); font-weight:700; color:var(--bark); line-height:1.12; margin:0 0 1rem; }
.hero-title em { color:var(--green); font-style:italic; }
.hero-sub { font-size:1.05rem; color:var(--muted); font-weight:300; line-height:1.7; max-width:480px; margin-bottom:2rem; }
.hero-pill { display:inline-block; background:white; border:1px solid var(--border); border-radius:30px; padding:8px 18px; font-size:0.8rem; color:var(--muted); margin:0.3rem; box-shadow:0 2px 8px rgba(0,0,0,0.05); }
.hero-img-card { border-radius:20px; overflow:hidden; box-shadow:var(--shadow-h); }
.hero-img-card img { width:200px; height:260px; object-fit:cover; display:block; }
.hero-img-card.tall img { height:320px; }
.hero-stat { background:white; border-radius:16px; padding:16px 20px; text-align:center; box-shadow:var(--shadow); min-width:100px; }
.hero-stat-num { font-family:'Cormorant Garamond',serif; font-size:1.8rem; font-weight:700; color:var(--green); }
.hero-stat-lbl { font-size:0.72rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.06em; }

/* Trust */
.trust-strip { background:var(--green); color:white; padding:14px 3rem; display:flex; justify-content:center; gap:3rem; flex-wrap:wrap; }
.trust-item { font-size:0.82rem; font-weight:500; letter-spacing:0.04em; opacity:0.92; }
.trust-item span { opacity:0.65; margin:0 0.5rem; }

/* Section */
.section-wrap { padding:3.5rem 3rem; background:var(--white); }
.section-wrap.alt { background:var(--off); }
.section-title { font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:700; color:var(--bark); line-height:1.1; margin:0 0 4px; }
.section-title em { color:var(--green); font-style:italic; }
.section-sub { font-size:0.85rem; color:var(--muted); margin-bottom:2rem; }

/* Product Card */
.pcard { background:var(--white); border-radius:18px; overflow:hidden; box-shadow:0 2px 16px rgba(0,0,0,0.06); transition:transform 0.25s,box-shadow 0.25s; position:relative; height:100%; }
.pcard:hover { transform:translateY(-5px); box-shadow:var(--shadow-h); }
.pcard-img { width:100%; aspect-ratio:4/3; object-fit:cover; display:block; }
.pcard-badge { position:absolute; top:12px; left:12px; background:var(--blush); color:var(--pink); font-size:0.68rem; font-weight:700; padding:3px 10px; border-radius:20px; letter-spacing:0.06em; text-transform:uppercase; }
.pcard-badge.green { background:var(--light-g); color:var(--green); }
.pcard-body { padding:1rem 1.1rem 1.2rem; }
.pcard-name { font-family:'Cormorant Garamond',serif; font-size:1.15rem; font-weight:700; color:var(--bark); margin:0 0 4px; line-height:1.3; }
.pcard-desc { font-size:0.78rem; color:var(--muted); line-height:1.5; margin:0 0 10px; }
.pcard-price { font-size:1.1rem; font-weight:700; color:var(--green); }
.pcard-mrp { font-size:0.78rem; color:#bbb; text-decoration:line-through; margin-left:6px; }
.pcard-off { font-size:0.72rem; color:var(--pink); font-weight:700; margin-left:4px; }

/* Tags */
.tag { display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.7rem; font-weight:600; letter-spacing:0.05em; text-transform:uppercase; margin:2px; }
.tag-new { background:var(--blush); color:var(--pink); }
.tag-eco { background:var(--light-g); color:var(--green); }
.tag-sale { background:#fff3e0; color:#e65100; }
.tag-rare { background:#f3e5f5; color:#7b1fa2; }

/* Cart */
.cart-item-name { font-family:'Cormorant Garamond',serif; font-size:1.05rem; font-weight:700; color:var(--bark); }
.cart-item-price { font-size:0.9rem; color:var(--green); font-weight:600; margin-top:2px; }
.cart-summary { background:linear-gradient(135deg,#e8f0ea,#f7ece9); border-radius:16px; padding:1.5rem; box-shadow:var(--shadow); }
.cart-total { font-family:'Cormorant Garamond',serif; font-size:1.6rem; font-weight:700; color:var(--bark); }

/* Promo */
.promo-banner { background:linear-gradient(135deg,#fce8e8 0%,#f5f0e8 50%,#e8f0ea 100%); border-radius:20px; padding:2.5rem 3rem; display:flex; align-items:center; justify-content:space-between; margin:1rem 0; overflow:hidden; position:relative; }
.promo-banner::after { content:'🌸'; position:absolute; right:120px; top:50%; transform:translateY(-50%); font-size:5rem; opacity:0.15; }
.promo-text { font-family:'Cormorant Garamond',serif; font-size:1.6rem; font-weight:700; color:var(--bark); }
.promo-sub { font-size:0.88rem; color:var(--muted); margin-top:4px; }
.promo-code { background:white; border:2px dashed var(--pink); border-radius:10px; padding:10px 20px; font-weight:700; font-size:1.1rem; color:var(--pink); letter-spacing:0.1em; }

/* Empty cart */
.empty-cart { text-align:center; padding:4rem 2rem; color:var(--muted); }
.empty-cart-icon { font-size:4rem; margin-bottom:1rem; }
.empty-cart-msg { font-family:'Cormorant Garamond',serif; font-size:1.5rem; color:var(--bark); }

/* Chatbot FAB */
.chat-fab-wrap { position:fixed; bottom:28px; left:28px; z-index:10001; }

/* Chat panel */
.chat-panel {
  position:fixed; bottom:90px; left:28px; width:368px;
  background:white; border-radius:20px;
  box-shadow:0 16px 60px rgba(0,0,0,0.18);
  z-index:9999; border:1px solid var(--border);
  animation:slideUp 0.3s cubic-bezier(0.34,1.2,0.64,1);
  overflow:hidden;
}
@keyframes slideUp { from{transform:translateY(30px);opacity:0} to{transform:translateY(0);opacity:1} }

.chat-header {
  background:linear-gradient(135deg,var(--green) 0%,#5a8f63 100%);
  padding:14px 18px; display:flex; align-items:center; gap:10px;
}
.chat-avatar { width:36px; height:36px; background:rgba(255,255,255,0.25); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.1rem; }
.chat-title { color:white; font-weight:600; font-size:0.9rem; }
.chat-status { color:rgba(255,255,255,0.75); font-size:0.72rem; }

.chat-messages { max-height:280px; overflow-y:auto; padding:14px; display:flex; flex-direction:column; gap:10px; background:#f9f9f7; }
.chat-messages::-webkit-scrollbar { width:4px; }
.chat-messages::-webkit-scrollbar-thumb { background:var(--border); border-radius:4px; }

.msg-bot { background:white; border:1px solid var(--border); border-radius:16px 16px 16px 4px; padding:10px 14px; font-size:0.84rem; color:var(--text); line-height:1.55; max-width:85%; box-shadow:0 1px 6px rgba(0,0,0,0.05); }
.msg-user { background:var(--green); color:white; border-radius:16px 16px 4px 16px; padding:10px 14px; font-size:0.84rem; line-height:1.55; max-width:85%; align-self:flex-end; box-shadow:0 2px 10px rgba(58,107,71,0.25); }

.chat-opt-btn { width:100%; background:white; border:1.5px solid var(--light-g); color:var(--green); border-radius:30px; padding:8px 16px; font-size:0.8rem; font-weight:600; cursor:pointer; transition:all 0.2s; letter-spacing:0.02em; margin-bottom:6px; }
.chat-opt-btn:hover { background:var(--green); color:white; border-color:var(--green); }

.chat-prod-mini { background:white; border:1px solid var(--border); border-radius:12px; padding:9px 10px; display:flex; gap:9px; align-items:center; box-shadow:0 1px 5px rgba(0,0,0,0.05); margin-bottom:6px; }
.chat-prod-img { width:48px; height:48px; object-fit:cover; border-radius:8px; flex-shrink:0; }
.chat-prod-name { font-family:'Cormorant Garamond',serif; font-size:0.92rem; font-weight:700; color:var(--bark); line-height:1.2; }
.chat-prod-price { font-size:0.76rem; color:var(--green); font-weight:600; }

.diagnose-box { background:linear-gradient(135deg,#e8f0ea,#f7ece9); border-radius:12px; padding:11px 13px; font-size:0.82rem; color:var(--bark); line-height:1.6; border:1px solid #dde8dd; margin-bottom:4px; }

.chat-input-row { padding:10px 12px; border-top:1px solid var(--border); display:flex; gap:8px; background:white; align-items:center; }
.chat-input { flex:1; border:1.5px solid var(--border); border-radius:30px; padding:8px 14px; font-size:0.82rem; outline:none; color:var(--text); transition:border-color 0.2s; }
.chat-input:focus { border-color:var(--sage); }

/* Footer */
.footer { background:var(--bark); color:rgba(255,255,255,0.7); padding:3rem; text-align:center; font-size:0.82rem; line-height:2; }
.footer-logo { font-family:'Cormorant Garamond',serif; font-size:2rem; color:white; margin-bottom:0.5rem; }

/* Streamlit overrides */
.stButton > button { font-family:'Jost',sans-serif !important; border-radius:10px !important; font-weight:600 !important; }
.stTextInput > div > input { border-radius:10px !important; font-family:'Jost',sans-serif !important; border:1.5px solid var(--border) !important; }
.stTextArea > div > textarea { border-radius:10px !important; font-family:'Jost',sans-serif !important; }
.stSelectbox > div > div { border-radius:10px !important; }
div[data-testid="stExpander"] { border:1px solid var(--border) !important; border-radius:14px !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# DATA CATALOG
# ──────────────────────────────────────────────────────────────

PLANTS = [
    {"id":"PL01","name":"Monstera Deliciosa","price":549,"mrp":799,"desc":"The iconic Swiss cheese plant. Perfect for bright, indirect light.","img":"https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400&q=80","badge":"Bestseller","tag":"eco"},
    {"id":"PL02","name":"Peace Lily","price":349,"mrp":499,"desc":"Elegant white blooms, purifies air and thrives in low light.","img":"https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400&q=80","badge":"Low Light","tag":"new"},
    {"id":"PL03","name":"Snake Plant","price":299,"mrp":449,"desc":"Nearly indestructible. Removes toxins and looks stunning.","img":"https://images.unsplash.com/photo-1616961808965-7d8d7c9a1e30?w=400&q=80","badge":"Easy Care","tag":"eco"},
    {"id":"PL04","name":"Fiddle Leaf Fig","price":899,"mrp":1299,"desc":"Architectural beauty with large, waxy leaves. A designer's favourite.","img":"https://images.unsplash.com/photo-1520412099551-62b6bafeb5bb?w=400&q=80","badge":"Trending","tag":"rare"},
    {"id":"PL05","name":"Pothos Golden","price":199,"mrp":299,"desc":"Fast-growing trailing vine. Ideal for shelves and hanging baskets.","img":"https://images.unsplash.com/photo-1622398925373-3f91b1e275f5?w=400&q=80","badge":"Budget Pick","tag":"eco"},
    {"id":"PL06","name":"ZZ Plant","price":449,"mrp":649,"desc":"Glossy, waxy leaves that tolerate neglect. Zero drama, all style.","img":"https://images.unsplash.com/photo-1632207691143-643e2a9a9361?w=400&q=80","badge":"Drought Tolerant","tag":"eco"},
    {"id":"PL07","name":"Bird of Paradise","price":1199,"mrp":1699,"desc":"Tropical showstopper with banana-like foliage.","img":"https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=400&q=80","badge":"Statement","tag":"rare"},
    {"id":"PL08","name":"Rubber Plant","price":499,"mrp":749,"desc":"Deep burgundy leaves add drama to any corner.","img":"https://images.unsplash.com/photo-1631125915902-d5e28543d7b1?w=400&q=80","badge":"Air Purifier","tag":"new"},
    {"id":"PL09","name":"Aloe Vera","price":179,"mrp":249,"desc":"Medicinal succulent. Keep on your windowsill for instant skincare.","img":"https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&q=80","badge":"Medicinal","tag":"eco"},
    {"id":"PL10","name":"Chinese Money Plant","price":399,"mrp":549,"desc":"Round pancake leaves on red stems. Brings good luck.","img":"https://images.unsplash.com/photo-1615233500064-bf92e853e847?w=400&q=80","badge":"Lucky Plant","tag":"new"},
    {"id":"PL11","name":"Philodendron Brasil","price":329,"mrp":499,"desc":"Heart-shaped leaves with neon-green streaks. Effortlessly chic.","img":"https://images.unsplash.com/photo-1597055181300-1f18e27f55f6?w=400&q=80","badge":"Variegated","tag":"new"},
    {"id":"PL12","name":"Oxalis Triangularis","price":249,"mrp":349,"desc":"Purple butterfly leaves that fold at night. A magical living decor.","img":"https://images.unsplash.com/photo-1520302630591-fd1f1b95b4b7?w=400&q=80","badge":"Exotic","tag":"rare"},
]

PLANT_CARE = [
    {"id":"PC01","name":"NPK Organic Fertilizer","price":249,"mrp":349,"desc":"Balanced 10-10-10 formula for all indoor plants. 500g bag.","img":"https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80","badge":"Bestseller","tag":"eco"},
    {"id":"PC02","name":"Neem Oil Spray 250ml","price":179,"mrp":249,"desc":"Cold-pressed neem. Controls aphids, mites and fungal issues.","img":"https://images.unsplash.com/photo-1585435557343-3b092031a831?w=400&q=80","badge":"Organic","tag":"eco"},
    {"id":"PC03","name":"Moisture Retention Granules","price":199,"mrp":279,"desc":"Hydrogel granules for pots — reduces watering by 50%.","img":"https://images.unsplash.com/photo-1447708440306-ec9a5d88d310?w=400&q=80","badge":"Water Saver","tag":"new"},
    {"id":"PC04","name":"Liquid Seaweed Extract","price":299,"mrp":399,"desc":"Micronutrient booster. Spray on leaves for rapid green-up.","img":"https://images.unsplash.com/photo-1599598425947-5202edd56fdb?w=400&q=80","badge":"Micronutrient","tag":"eco"},
    {"id":"PC05","name":"Vermicompost 1kg","price":149,"mrp":199,"desc":"Premium worm castings. Improves soil structure & microbiome.","img":"https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=400&q=80","badge":"Premium Compost","tag":"eco"},
    {"id":"PC06","name":"Systemic Fungicide 100g","price":219,"mrp":299,"desc":"Controls powdery mildew, root rot and blight effectively.","img":"https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=400&q=80","badge":"Plant Saver","tag":"sale"},
    {"id":"PC07","name":"Pruning Shears Pro","price":649,"mrp":899,"desc":"Stainless SK5 blades, ergonomic grip. Clean precision cuts.","img":"https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80","badge":"Pro Tool","tag":"new"},
    {"id":"PC08","name":"Soil pH & Moisture Meter","price":499,"mrp":699,"desc":"3-in-1 digital tester: pH, moisture, light intensity.","img":"https://images.unsplash.com/photo-1585435557343-3b092031a831?w=400&q=80","badge":"Smart Garden","tag":"new"},
]

POTS = [
    {"id":"PT01","name":"Terracotta Pot Set (3)","price":449,"mrp":649,"desc":"Hand-thrown terracotta with drainage holes. Set of 3 sizes.","img":"https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&q=80","badge":"Classic","tag":"eco"},
    {"id":"PT02","name":"Ceramic Glazed Planter","price":699,"mrp":999,"desc":"Sage-green glaze, drainage tray included. 8 inch diameter.","img":"https://images.unsplash.com/photo-1509423350716-97f9360b4e09?w=400&q=80","badge":"Premium","tag":"new"},
    {"id":"PT03","name":"Hanging Macramé Planter","price":349,"mrp":499,"desc":"Handwoven cotton macramé. Holds 6-inch pot perfectly.","img":"https://images.unsplash.com/photo-1463699527455-ddf00a24d09e?w=400&q=80","badge":"Boho","tag":"new"},
    {"id":"PT04","name":"Self-Watering Smart Pot","price":799,"mrp":1099,"desc":"Built-in reservoir with water level indicator. Never over-water.","img":"https://images.unsplash.com/photo-1459156212016-c812468e2115?w=400&q=80","badge":"Smart","tag":"new"},
    {"id":"PT05","name":"Cement Minimalist Planter","price":549,"mrp":799,"desc":"Raw cast cement with matte finish. Industrial chic aesthetic.","img":"https://images.unsplash.com/photo-1444930694458-01babf71870c?w=400&q=80","badge":"Minimalist","tag":"eco"},
    {"id":"PT06","name":"Wicker Basket Planter","price":399,"mrp":549,"desc":"Natural rattan weave with plastic liner. Earthy and warm.","img":"https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&q=80","badge":"Natural","tag":"eco"},
]

SEEDS = [
    {"id":"SD01","name":"Cherry Tomato Seeds","price":79,"mrp":119,"desc":"Prolific indeterminate variety. Harvest in 65 days. 30 seeds.","img":"https://images.unsplash.com/photo-1592921870789-04563d55041c?w=400&q=80","badge":"Grow Your Food","tag":"eco"},
    {"id":"SD02","name":"Basil Herb Mix","price":59,"mrp":89,"desc":"5 basil varieties: Genovese, Thai, Purple, Lemon, Greek.","img":"https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=400&q=80","badge":"Herb Garden","tag":"new"},
    {"id":"SD03","name":"Sunflower Mammoth","price":89,"mrp":129,"desc":"Giant heads up to 30cm! Makes an incredible summer display.","img":"https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=400&q=80","badge":"Kids Love It","tag":"new"},
    {"id":"SD04","name":"Wildflower Meadow Mix","price":149,"mrp":199,"desc":"50 native species. Scatter & watch pollinators arrive.","img":"https://images.unsplash.com/photo-1490750967868-88df5691cc56?w=400&q=80","badge":"Eco Friendly","tag":"eco"},
    {"id":"SD05","name":"Spinach & Lettuce Mix","price":69,"mrp":99,"desc":"Cut-and-come-again salad leaves ready in 4 weeks.","img":"https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&q=80","badge":"Quick Harvest","tag":"sale"},
    {"id":"SD06","name":"Coriander & Mint Combo","price":59,"mrp":89,"desc":"Essential kitchen herbs. Endless fresh supply on your windowsill.","img":"https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&q=80","badge":"Kitchen Herb","tag":"eco"},
]

ALL_PRODUCTS = PLANTS + PLANT_CARE + POTS + SEEDS

# ──────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────
if "cart"         not in st.session_state: st.session_state.cart = []
if "active_tab"   not in st.session_state: st.session_state.active_tab = "plants"
if "chat_open"    not in st.session_state: st.session_state.chat_open = False
if "chat_step"    not in st.session_state: st.session_state.chat_step = "init"
if "chat_msgs"    not in st.session_state: st.session_state.chat_msgs = []
if "notif"        not in st.session_state: st.session_state.notif = None
if "order_placed" not in st.session_state: st.session_state.order_placed = False

# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────

def get_product(pid):
    return next((p for p in ALL_PRODUCTS if p["id"] == pid), None)

def add_to_cart(pid):
    p = get_product(pid)
    if p:
        st.session_state.cart.append(p)
        st.session_state.notif = f"✅ {p['name']} added to cart!"

def cart_count():
    return len(st.session_state.cart)

def cart_total():
    return sum(p["price"] for p in st.session_state.cart)

# Toast notification
if st.session_state.notif:
    st.toast(st.session_state.notif, icon="🌿")
    st.session_state.notif = None

# ──────────────────────────────────────────────────────────────
# TOP NAV
# ──────────────────────────────────────────────────────────────
cart_n = cart_count()
st.markdown(f"""
<div class="nav-bar">
  <div class="nav-logo">Leafy<span>.</span></div>
  <div style="display:flex;gap:2rem;">
    <span style="font-size:0.88rem;font-weight:500;color:{'#3a6b47' if st.session_state.active_tab=='plants' else '#6b6b6b'};letter-spacing:0.06em;">🌿 PLANTS</span>
    <span style="font-size:0.88rem;font-weight:500;color:{'#3a6b47' if st.session_state.active_tab=='care' else '#6b6b6b'};letter-spacing:0.06em;">🧪 PLANT CARE</span>
    <span style="font-size:0.88rem;font-weight:500;color:{'#3a6b47' if st.session_state.active_tab=='pots' else '#6b6b6b'};letter-spacing:0.06em;">🪴 POTS</span>
    <span style="font-size:0.88rem;font-weight:500;color:{'#3a6b47' if st.session_state.active_tab=='seeds' else '#6b6b6b'};letter-spacing:0.06em;">🌾 SEEDS</span>
  </div>
  <div class="nav-cart">🛒 Cart ({cart_n})</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# TAB BAR
# ──────────────────────────────────────────────────────────────
tabs_def = [
    ("plants", "🌿 Plants"),
    ("care",   "🧪 Plant Care"),
    ("pots",   "🪴 Pots"),
    ("seeds",  "🌾 Seeds"),
    ("cart",   f"🛒 Cart ({cart_n})"),
]
tab_cols = st.columns(len(tabs_def))
for col, (key, label) in zip(tab_cols, tabs_def):
    with col:
        active_tab = st.session_state.active_tab == key
        if st.button(label, key=f"tab_{key}", use_container_width=True,
                     type="primary" if active_tab else "secondary"):
            st.session_state.active_tab = key
            st.rerun()

st.divider()

active = st.session_state.active_tab

# ──────────────────────────────────────────────────────────────
# HERO BANNER  (non-cart pages)
# ──────────────────────────────────────────────────────────────
if active != "cart":
    st.markdown("""
    <div class="hero">
      <div style="flex:1.2;min-width:320px;">
        <div class="hero-badge">🌱 Free delivery on orders above ₹599</div>
        <h1 class="hero-title">Bring <em>Nature</em><br>Into Your Home</h1>
        <p class="hero-sub">Handpicked plants, organic care products, and artisan pots — curated for plant lovers who believe every space deserves a touch of green.</p>
        <div>
          <span class="hero-pill">🌿 1,200+ Varieties</span>
          <span class="hero-pill">🚚 Pan-India Delivery</span>
          <span class="hero-pill">⭐ 4.8 Rated</span>
        </div>
      </div>
      <div style="flex:1;display:flex;align-items:flex-end;justify-content:center;gap:1rem;flex-wrap:wrap;">
        <div class="hero-img-card tall">
          <img src="https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=300&q=80" alt="plant"/>
        </div>
        <div style="display:flex;flex-direction:column;gap:1rem;">
          <div class="hero-img-card">
            <img src="https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=300&q=80" alt="plant" style="height:185px;"/>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-num">50k+</div>
            <div class="hero-stat-lbl">Happy Gardeners</div>
          </div>
        </div>
      </div>
    </div>
    <div class="trust-strip">
      <span class="trust-item">🚚 Free Delivery above ₹599<span>|</span></span>
      <span class="trust-item">🌿 100% Healthy Plants<span>|</span></span>
      <span class="trust-item">↩️ 30-Day Returns<span>|</span></span>
      <span class="trust-item">🌱 Eco-Friendly Packaging</span>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# PRODUCT GRID HELPER
# ──────────────────────────────────────────────────────────────
TAG_LABELS = {"new":"🆕 New","eco":"🌱 Eco","sale":"🔥 Sale","rare":"💎 Rare"}
TAG_CLASS  = {"new":"tag-new","eco":"tag-eco","sale":"tag-sale","rare":"tag-rare"}

def render_grid(products, cols=4):
    rows = [products[i:i+cols] for i in range(0, len(products), cols)]
    for row in rows:
        grid = st.columns(cols)
        for col, prod in zip(grid, row):
            with col:
                t = prod.get("tag","")
                tag_html = f'<span class="tag {TAG_CLASS.get(t,"")}">{TAG_LABELS.get(t,"")}</span>' if t in TAG_LABELS else ""
                disc = round((1 - prod["price"] / prod["mrp"]) * 100)
                badge_cls = "green" if any(w in prod.get("badge","") for w in ["Easy","Organic","Eco","Natural","Low"]) else ""
                st.markdown(f"""
                <div class="pcard">
                  <div style="position:relative;">
                    <img src="{prod['img']}" class="pcard-img" onerror="this.style.display='none'"/>
                    <div class="pcard-badge {badge_cls}">{prod.get('badge','')}</div>
                  </div>
                  <div class="pcard-body">
                    <div style="margin-bottom:5px;">{tag_html}</div>
                    <div class="pcard-name">{prod['name']}</div>
                    <div class="pcard-desc">{prod['desc']}</div>
                    <div>
                      <span class="pcard-price">₹{prod['price']}</span>
                      <span class="pcard-mrp">₹{prod['mrp']}</span>
                      <span class="pcard-off">{disc}% off</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🛒 Add to Cart", key=f"add_{prod['id']}", use_container_width=True):
                    add_to_cart(prod["id"])
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# PAGES
# ──────────────────────────────────────────────────────────────

if active == "plants":
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Our <em>Plants</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Curated for every space — sunny balcony to dimly-lit studio.</div>', unsafe_allow_html=True)
    render_grid(PLANTS, cols=4)
    st.markdown("""
    <div class="promo-banner">
      <div>
        <div class="promo-text">First Order? Get 15% Off 🎉</div>
        <div class="promo-sub">Use code at checkout. Valid on all plants.</div>
      </div>
      <div class="promo-code">LEAFY15</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif active == "care":
    st.markdown('<div class="section-wrap alt">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Plant <em>Care</em> Essentials</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Fertilizers, pesticides, tools & soil amendments for thriving plants.</div>', unsafe_allow_html=True)
    render_grid(PLANT_CARE, cols=4)
    st.markdown('</div>', unsafe_allow_html=True)

elif active == "pots":
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Artisan <em>Pots</em> & Planters</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">From terracotta classics to modern self-watering smartpots.</div>', unsafe_allow_html=True)
    render_grid(POTS, cols=3)
    st.markdown('</div>', unsafe_allow_html=True)

elif active == "seeds":
    st.markdown('<div class="section-wrap alt">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Seeds & <em>Grow Kits</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Start from scratch — vegetables, herbs, wildflowers and more.</div>', unsafe_allow_html=True)
    render_grid(SEEDS, cols=3)
    st.markdown('</div>', unsafe_allow_html=True)

elif active == "cart":
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="margin-bottom:1.5rem;">Your <em>Cart</em></div>', unsafe_allow_html=True)

    if st.session_state.order_placed:
        st.success("🎉 **Order Placed Successfully!** You'll receive a confirmation shortly. Happy growing! 🌿")
        st.balloons()
        if st.button("Continue Shopping 🌿"):
            st.session_state.order_placed = False
            st.session_state.active_tab = "plants"
            st.rerun()

    elif not st.session_state.cart:
        st.markdown("""
        <div class="empty-cart">
          <div class="empty-cart-icon">🛒</div>
          <div class="empty-cart-msg">Your cart is empty</div>
          <div style="font-size:0.88rem;color:var(--muted);margin-top:0.5rem;">Explore our collection and add something beautiful!</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Browse Plants 🌿"):
            st.session_state.active_tab = "plants"
            st.rerun()

    else:
        left_col, right_col = st.columns([1.6, 1], gap="large")

        with left_col:
            st.markdown(f"**{len(st.session_state.cart)} item(s) in cart**")
            st.markdown("<br>", unsafe_allow_html=True)
            for idx, item in enumerate(st.session_state.cart):
                c1, c2, c3 = st.columns([1, 4, 1])
                with c1:
                    st.image(item["img"], width=70)
                with c2:
                    st.markdown(f"""
                    <div class="cart-item-name">{item['name']}</div>
                    <div class="cart-item-price">₹{item['price']}</div>
                    <div style="font-size:0.75rem;color:var(--muted);">{item['desc'][:60]}…</div>""",
                    unsafe_allow_html=True)
                with c3:
                    if st.button("🗑", key=f"del_{idx}", help="Remove"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                st.divider()

            if st.button("🗑️ Clear Cart", type="secondary"):
                st.session_state.cart = []
                st.rerun()

        with right_col:
            subtotal = cart_total()
            delivery = 0 if subtotal >= 599 else 79
            discount = round(subtotal * 0.05)
            final    = subtotal + delivery - discount
            free_del = subtotal >= 599

            st.markdown(f"""
            <div class="cart-summary">
              <div style="font-size:0.82rem;color:var(--muted);margin-bottom:1rem;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;">Order Summary</div>
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:0.9rem;"><span>Subtotal ({len(st.session_state.cart)} items)</span><span>₹{subtotal}</span></div>
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:0.9rem;"><span>Delivery</span><span style="color:var(--green);">{'FREE' if free_del else f'₹{delivery}'}</span></div>
              <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:0.9rem;color:var(--pink);"><span>Member Discount (5%)</span><span>- ₹{discount}</span></div>
              <hr style="border:none;border-top:1px solid var(--border);margin:8px 0;"/>
              <div style="display:flex;justify-content:space-between;"><span class="cart-total">Total</span><span class="cart-total">₹{final}</span></div>
              <div style="font-size:0.75rem;color:{'var(--green)' if free_del else 'var(--muted)'};margin-top:6px;">
                {'🎉 You qualify for free delivery!' if free_del else f'Add ₹{599-subtotal} more for free delivery'}
              </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Delivery Details**")
            name    = st.text_input("Full Name",  placeholder="Priya Sharma")
            address = st.text_area ("Address",    placeholder="123, Green Street, Mumbai – 400001", height=75)
            phone   = st.text_input("Phone",      placeholder="+91 98765 43210")
            pay     = st.selectbox ("Payment",    ["💳 Credit/Debit Card","📱 UPI","💰 Cash on Delivery","🏦 Net Banking"])

            if st.button("🌿 Place Order", use_container_width=True, type="primary"):
                if not name.strip() or not address.strip() or not phone.strip():
                    st.warning("Please fill in all delivery details.")
                else:
                    st.session_state.cart = []
                    st.session_state.order_placed = True
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────
if active != "cart":
    st.markdown("""
    <div class="footer">
      <div class="footer-logo">Leafy.</div>
      <div>Bringing nature closer to you, one plant at a time. 🌿</div>
      <div style="margin-top:0.5rem;opacity:0.5;">🌿 Plants &nbsp;|&nbsp; 🧪 Care &nbsp;|&nbsp; 🪴 Pots &nbsp;|&nbsp; 🌾 Seeds &nbsp;|&nbsp; 🤖 PlantBot</div>
      <div style="margin-top:1rem;font-size:0.72rem;opacity:0.4;">© 2025 Leafy. Made with 💚 for plant lovers.</div>
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# FLOATING CHATBOT
# ──────────────────────────────────────────────────────────────

# ── FAB button ─────────────────────────────────────────────────
# Inject a wrapper that positions it fixed bottom-left
st.markdown("""
<style>
/* Target the FAB button specifically */
div[data-testid="stButton"]:has(button[kind="secondary"][data-testid="baseButton-secondary"]:first-of-type) { }
.fab-container { position:fixed; bottom:28px; left:28px; z-index:10001; }
</style>
""", unsafe_allow_html=True)

# We use a container trick: render an expander-free zone, then the button
fab_placeholder = st.empty()
with fab_placeholder.container():
    st.markdown('<div class="fab-container">', unsafe_allow_html=True)
    fab_label = "✕ Close Chat" if st.session_state.chat_open else "💬 PlantBot"
    if st.button(fab_label, key="fab_btn"):
        st.session_state.chat_open = not st.session_state.chat_open
        if st.session_state.chat_open and not st.session_state.chat_msgs:
            st.session_state.chat_msgs = [
                {"role":"bot","type":"text","content":"👋 Hi! I'm **PlantBot** — your personal plant expert.\n\nHow may I help you today?"},
                {"role":"bot","type":"options","options":["🌿 Buy Plants","🧪 Plant Care Help"]},
            ]
            st.session_state.chat_step = "main_menu"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Inject CSS to push that button to fixed position
st.markdown("""
<style>
/* Make the fab button look right and stay fixed */
div[data-testid="stButton"] button[kind="secondary"] {
}
</style>
<script>
// Move the FAB button to fixed position after render
(function() {
  const observer = new MutationObserver(() => {
    const btns = document.querySelectorAll('button');
    btns.forEach(btn => {
      if(btn.textContent.includes('PlantBot') || btn.textContent.includes('Close Chat')) {
        const parent = btn.closest('[data-testid="stButton"]');
        if(parent && !parent.dataset.fabFixed) {
          parent.dataset.fabFixed = '1';
          parent.style.cssText = 'position:fixed!important;bottom:28px!important;left:28px!important;z-index:10001!important;width:auto!important;';
          btn.style.cssText = 'background:#3a6b47!important;color:white!important;border:none!important;border-radius:50px!important;padding:12px 22px!important;font-size:0.88rem!important;font-weight:600!important;cursor:pointer!important;box-shadow:0 6px 28px rgba(58,107,71,0.45)!important;letter-spacing:0.03em!important;';
        }
      }
    });
  });
  observer.observe(document.body, {childList:true, subtree:true});
})();
</script>
""", unsafe_allow_html=True)

# ── Chat panel (rendered when open) ────────────────────────────
if st.session_state.chat_open:

    # Build message HTML
    msgs_html = ""
    for msg in st.session_state.chat_msgs:
        if msg["role"] == "user":
            msgs_html += f'<div class="msg-user">{msg["content"].replace(chr(10),"<br>")}</div>'
        else:
            mtype = msg.get("type","text")
            if mtype == "text":
                msgs_html += f'<div class="msg-bot">{msg["content"].replace(chr(10),"<br>")}</div>'
            elif mtype == "diagnose":
                msgs_html += f'''<div class="diagnose-box">
                  <div style="font-size:1.5rem;margin-bottom:5px;">{msg.get("icon","🔬")}</div>
                  <strong>{msg.get("title","Diagnosis")}</strong><br>{msg.get("content","")}
                </div>'''
            elif mtype == "products":
                for p in msg.get("products",[]):
                    disc = round((1-p["price"]/p["mrp"])*100)
                    msgs_html += f'''<div class="chat-prod-mini">
                      <img src="{p['img']}" class="chat-prod-img" onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=100'"/>
                      <div style="flex:1;">
                        <div class="chat-prod-name">{p['name']}</div>
                        <div class="chat-prod-price">₹{p['price']} <span style="text-decoration:line-through;color:#bbb;font-size:0.7rem;">₹{p['mrp']}</span> <span style="color:#e8a0a0;font-size:0.68rem;">{disc}%off</span></div>
                      </div>
                    </div>'''

    # Render the chat panel HTML
    st.markdown(f"""
    <div class="chat-panel">
      <div class="chat-header">
        <div class="chat-avatar">🌿</div>
        <div>
          <div class="chat-title">PlantBot</div>
          <div class="chat-status">● Online — Plant Expert AI</div>
        </div>
        <div style="margin-left:auto;color:rgba(255,255,255,0.7);font-size:0.8rem;">AI powered</div>
      </div>
      <div class="chat-messages" id="chat-scroll">
        {msgs_html}
      </div>
    </div>
    <script>
      setTimeout(()=>{{
        const el = document.getElementById('chat-scroll');
        if(el) el.scrollTop = el.scrollHeight;
      }}, 100);
    </script>
    """, unsafe_allow_html=True)

    # ── Option buttons (shown if last message has options) ──
    last_msg = st.session_state.chat_msgs[-1] if st.session_state.chat_msgs else None
    if last_msg and last_msg.get("type") == "options":
        opts = last_msg["options"]
        st.markdown("""<div style="position:fixed;bottom:148px;left:28px;width:368px;
            z-index:9999;padding:8px 12px;background:#f9f9f7;
            border-left:1px solid #e8e0d8;border-right:1px solid #e8e0d8;">""",
            unsafe_allow_html=True)

        opt_cols = st.columns(min(len(opts), 2))
        for i, opt in enumerate(opts):
            col = opt_cols[i % len(opt_cols)]
            with col:
                if st.button(opt, key=f"opt_{opt[:20]}_{i}", use_container_width=True):
                    # Convert last option message to plain text
                    st.session_state.chat_msgs[-1] = {
                        "role":"bot","type":"text",
                        "content":st.session_state.chat_msgs[-1].get("content","")
                    }
                    # Add user selection
                    st.session_state.chat_msgs.append({"role":"user","type":"text","content":opt})

                    # ── Route the option ──
                    if "Buy Plants" in opt:
                        st.session_state.chat_msgs += [
                            {"role":"bot","type":"text","content":"Great! 🌿 What are you looking for?"},
                            {"role":"bot","type":"options","options":["🎁 Birthday Gift","🏠 Low Maintenance","🌙 Indoor Plants","💸 Budget Picks"]},
                        ]
                    elif "Plant Care" in opt:
                        st.session_state.chat_msgs.append({"role":"bot","type":"text","content":"Sure! Upload a photo of your plant below and I'll diagnose it. 🔬\n\nOr ask me a specific question like:\n• 'Best fertilizer for indoor plants'\n• 'What pot for snake plant?'"})
                        st.session_state.chat_step = "plant_care"

                    elif "Birthday Gift" in opt:
                        recs = random.sample(PLANTS[:8], 3)
                        st.session_state.chat_msgs += [
                            {"role":"bot","type":"text","content":"🎁 Perfect birthday gifts — beautiful plants that keep giving joy:"},
                            {"role":"bot","type":"products","products":recs},
                            {"role":"bot","type":"options","options":["🔙 Main Menu","🛒 Go to Cart"]},
                        ]
                    elif "Low Maintenance" in opt:
                        recs = [p for p in PLANTS if any(w in p.get("badge","") for w in ["Easy","Drought","Low"])]
                        if not recs: recs = random.sample(PLANTS, 3)
                        st.session_state.chat_msgs += [
                            {"role":"bot","type":"text","content":"😌 These plants basically look after themselves:"},
                            {"role":"bot","type":"products","products":recs[:3]},
                            {"role":"bot","type":"options","options":["🔙 Main Menu","🛒 Go to Cart"]},
                        ]
                    elif "Indoor" in opt:
                        recs = random.sample(PLANTS[:8], 3)
                        st.session_state.chat_msgs += [
                            {"role":"bot","type":"text","content":"🏠 Top indoor plants our customers love:"},
                            {"role":"bot","type":"products","products":recs},
                            {"role":"bot","type":"options","options":["🔙 Main Menu","🛒 Go to Cart"]},
                        ]
                    elif "Budget" in opt:
                        recs = sorted(PLANTS, key=lambda x: x["price"])[:3]
                        st.session_state.chat_msgs += [
                            {"role":"bot","type":"text","content":"💰 Best value plants right now:"},
                            {"role":"bot","type":"products","products":recs},
                            {"role":"bot","type":"options","options":["🔙 Main Menu","🛒 Go to Cart"]},
                        ]
                    elif "Main Menu" in opt:
                        st.session_state.chat_msgs += [
                            {"role":"bot","type":"text","content":"What else can I help with? 🌿"},
                            {"role":"bot","type":"options","options":["🌿 Buy Plants","🧪 Plant Care Help"]},
                        ]
                    elif "Go to Cart" in opt or "Cart" in opt:
                        st.session_state.active_tab = "cart"
                        st.session_state.chat_open = False

                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Image upload for plant care ──
    if st.session_state.chat_step == "plant_care":
        st.markdown("""<div style="position:fixed;bottom:148px;left:28px;width:368px;
            z-index:9998;padding:8px 12px;background:#f9f9f7;
            border-left:1px solid #e8e0d8;border-right:1px solid #e8e0d8;">""",
            unsafe_allow_html=True)

        uploaded = st.file_uploader("Upload plant photo 📷", type=["jpg","jpeg","png","webp"],
                                     key="plant_img", label_visibility="visible")
        if uploaded:
            from PIL import Image as PILImage
            img = PILImage.open(uploaded)
            st.image(img, width=160, caption="Your plant")

            # Simulate diagnosis with simple pixel stats
            img_sm = img.convert("RGB").resize((50,50))
            pixels = list(img_sm.getdata())
            r_avg = sum(p[0] for p in pixels)/len(pixels)
            g_avg = sum(p[1] for p in pixels)/len(pixels)
            b_avg = sum(p[2] for p in pixels)/len(pixels)
            brightness = (r_avg+g_avg+b_avg)/3

            diagnoses = [
                ("🏜️","Dry & Thirsty!","Your plant shows signs of drought stress — wilting and dry leaf edges. It urgently needs water and moisture retention treatment.",["PC01","PC03"]),
                ("🦟","Pest Attack Detected","I can see signs of aphid/mite damage on the foliage. Small brown spots and webbing are visible.",["PC02","PC06"]),
                ("💛","Nutrient Deficiency","Yellowing leaves indicate nitrogen or iron deficiency. Time to feed your plant!",["PC01","PC04"]),
                ("💧","Overwatered","Drooping despite wet soil — classic overwatering. Roots need oxygen, not more water.",["PC03","PC08"]),
                ("🍄","Fungal Infection","White powdery coating and brown spots suggest fungal growth spreading through the plant.",["PC05","PC06"]),
            ]

            if g_avg > r_avg * 1.25 and brightness > 100:
                chosen = diagnoses[0]
            elif r_avg > g_avg * 1.15:
                chosen = diagnoses[1]
            elif brightness < 80:
                chosen = diagnoses[3]
            else:
                chosen = random.choice(diagnoses)

            icon, title, desc, pids = chosen
            recs = [p for p in PLANT_CARE if p["id"] in pids]

            st.session_state.chat_msgs.append({"role":"bot","type":"text","content":"🔬 Analysing your plant image…"})
            st.session_state.chat_msgs.append({"role":"bot","type":"diagnose","icon":icon,"title":title,"content":desc + "<br><br>Here are my recommended treatments:"})
            st.session_state.chat_msgs.append({"role":"bot","type":"products","products":recs})
            st.session_state.chat_msgs.append({"role":"bot","type":"options","options":["🔙 Main Menu","🛒 Go to Cart"]})
            st.session_state.chat_step = "done"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Text input row ──
    st.markdown("""<div style="position:fixed;bottom:90px;left:28px;width:368px;
        z-index:9999;padding:10px 12px;background:white;
        border:1px solid #e8e0d8;border-radius:0 0 20px 20px;
        display:flex;gap:8px;align-items:center;">""", unsafe_allow_html=True)

    inp_c, btn_c = st.columns([5,1])
    with inp_c:
        user_txt = st.text_input("Ask PlantBot…", key="chat_txt",
                                  placeholder="e.g. Best pot for snake plant?",
                                  label_visibility="collapsed")
    with btn_c:
        send_btn = st.button("➤", key="chat_send")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Handle text input ──
    if send_btn and user_txt.strip():
        q = user_txt.lower().strip()
        st.session_state.chat_msgs.append({"role":"user","type":"text","content":user_txt})

        if any(w in q for w in ["snake","sansevieria"]):
            recs = [p for p in POTS if any(k in p["name"] for k in ["Terracotta","Cement"])][:2]
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"🐍 Snake plants love well-draining terracotta or cement pots:"},
                {"role":"bot","type":"products","products":recs},
            ]
        elif any(w in q for w in ["fertilizer","feed","npk","nutrient"]):
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"🌱 Best fertilizers for indoor plants:"},
                {"role":"bot","type":"products","products":PLANT_CARE[:3]},
            ]
        elif any(w in q for w in ["pest","bug","aphid","mite","insect"]):
            recs = [p for p in PLANT_CARE if p["id"] in ["PC02","PC06"]]
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"🛡️ For pest control, these work best:"},
                {"role":"bot","type":"products","products":recs},
            ]
        elif any(w in q for w in ["yellow","pale","chloro"]):
            recs = [p for p in PLANT_CARE if p["id"] in ["PC01","PC04","PC05"]]
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"💛 Yellowing is usually nutrient deficiency. Try these:"},
                {"role":"bot","type":"products","products":recs},
            ]
        elif any(w in q for w in ["gift","birthday","present"]):
            recs = random.sample(PLANTS[:6], 3)
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"🎁 Plants make the most thoughtful gifts! Top picks:"},
                {"role":"bot","type":"products","products":recs},
            ]
        elif any(w in q for w in ["pot","planter","container"]):
            recs = random.sample(POTS, 3)
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"🪴 Our most popular planters:"},
                {"role":"bot","type":"products","products":recs},
            ]
        elif any(w in q for w in ["seed","vegetable","herb","grow"]):
            recs = random.sample(SEEDS, 3)
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"🌱 Perfect for growing from scratch:"},
                {"role":"bot","type":"products","products":recs},
            ]
        elif any(w in q for w in ["water","how often","watering"]):
            st.session_state.chat_msgs.append({"role":"bot","type":"text",
                "content":"💧 **Watering Guide:**\n\n• Tropical plants: every 2–3 days\n• Succulents/Cacti: every 10–14 days\n• Ferns: keep consistently moist\n• Pothos/ZZ: let top 2cm dry out\n\nOur **SoilSense Meter** takes all the guesswork out!"})
            recs = [p for p in PLANT_CARE if p["id"]=="PC08"]
            if recs: st.session_state.chat_msgs.append({"role":"bot","type":"products","products":recs})
        elif any(w in q for w in ["cheap","budget","affordable"]):
            recs = sorted(ALL_PRODUCTS, key=lambda x: x["price"])[:3]
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"💰 Best value products:"},
                {"role":"bot","type":"products","products":recs},
            ]
        elif any(w in q for w in ["hi","hello","hey","namaste"]):
            st.session_state.chat_msgs += [
                {"role":"bot","type":"text","content":"👋 Hello! How can I help you today?"},
                {"role":"bot","type":"options","options":["🌿 Buy Plants","🧪 Plant Care Help"]},
            ]
        else:
            # Fuzzy match on plant names
            matched = [p for p in PLANTS if any(word in p["name"].lower() for word in q.split() if len(word)>3)]
            if matched:
                st.session_state.chat_msgs += [
                    {"role":"bot","type":"text","content":"🌿 Here's what we have:"},
                    {"role":"bot","type":"products","products":matched[:3]},
                ]
            else:
                recs = random.sample(PLANTS[:6], 2)
                st.session_state.chat_msgs += [
                    {"role":"bot","type":"text",
                     "content":"I can help with that! 🌿\n\nTry asking me:\n• *'Best fertilizer for indoor plants'*\n• *'What pot for snake plant?'*\n• *'Birthday gift plants'*\n• *'How often to water?'*"},
                    {"role":"bot","type":"text","content":"Meanwhile, here are some plants you might love:"},
                    {"role":"bot","type":"products","products":recs},
                ]

        st.session_state.chat_msgs.append({"role":"bot","type":"options","options":["🌿 Browse More","🧪 Plant Care Help","🛒 Go to Cart"]})
        st.rerun()

    # ── Quick product add from chat ──
    # Find products recommended in chat and add cart buttons
    for msg in st.session_state.chat_msgs:
        if msg.get("type") == "products":
            for p in msg.get("products", []):
                btn_key = f"chat_cart_{p['id']}_{abs(hash(str(msg)))}"
                if f"__rendered_{btn_key}" not in st.session_state:
                    st.session_state[f"__rendered_{btn_key}"] = False
