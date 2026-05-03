"""
🌿 GreenLeaf — Complete Plant E-Commerce + PlantBot
Single-file Streamlit application.
Run with: streamlit run app.py
"""

import streamlit as st
import random
from PIL import Image

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GreenLeaf 🌿",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Nunito:wght@300;400;600;700&display=swap');

:root {
    --cream: #f8f4ee;
    --sage:  #7a9e7e;
    --moss:  #3d6b45;
    --dark:  #243028;
    --bark:  #6b4226;
    --petal: #e8c5a0;
    --dew:   #d4edda;
    --rust:  #c0604a;
    --gold:  #c9952a;
    --white: #ffffff;
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: var(--cream);
    color: var(--dark);
}
h1, h2, h3, h4 { font-family: 'Lora', serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a2e1b 0%, #2b3d2c 100%);
}
[data-testid="stSidebar"] * { color: #e8f5e9 !important; }
[data-testid="stSidebar"] hr { border-color: #3d6b45; }

.stButton > button {
    background: var(--moss);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 0.45rem 1.2rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 600;
    font-size: 0.88rem;
    transition: all 0.2s;
}
.stButton > button:hover { background: var(--bark); transform: translateY(-1px); }

.product-card {
    background: var(--white);
    border: 1px solid #dce8dc;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}
.product-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.10); }
.product-name { font-family: 'Lora', serif; font-size: 1rem; font-weight: 700; color: var(--moss); margin: 6px 0 2px; }
.product-price { font-size: 1.1rem; font-weight: 700; color: var(--bark); }
.product-mrp { font-size: 0.75rem; color: #aaa; text-decoration: line-through; margin-left: 4px; }
.product-desc { font-size: 0.8rem; color: #555; line-height: 1.5; margin: 5px 0; }
.off-badge { display:inline-block; background:#e8f5e9; color:#2e7d32; font-size:0.7rem; font-weight:700; padding:2px 7px; border-radius:20px; margin-left:4px; }
.category-chip { display:inline-block; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.07em; padding:2px 8px; border-radius:20px; margin:2px 0 6px; }
.chip-plant     { background:#e8f5e9; color:#1b5e20; }
.chip-care      { background:#fff3e0; color:#e65100; }
.chip-pot       { background:#ede7f6; color:#4527a0; }
.chip-seed      { background:#e0f7fa; color:#006064; }

.hero-banner {
    background: linear-gradient(135deg, #1a2e1b 0%, #3d6b45 60%, #5a8f63 100%);
    border-radius: 18px;
    padding: 2.2rem 2.8rem;
    color: #e8f5e9;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.hero-banner h1 { color: #e8f5e9 !important; font-size: 2.4rem; margin:0; }
.hero-banner p  { color: #b2dfbc; font-size: 1rem; margin: 0.5rem 0 0; }
.hero-leaf { position:absolute; right:2rem; top:50%; transform:translateY(-50%); font-size:6rem; opacity:0.15; }

.metric-pill { background:var(--white); border:1px solid #dce8dc; border-radius:10px; padding:0.8rem 1rem; text-align:center; }
.metric-value { font-size:1.5rem; font-weight:700; color:var(--moss); }
.metric-label { font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.06em; }

.chat-user {
    background: var(--moss);
    color:#fff;
    border-radius:18px 18px 4px 18px;
    padding:0.6rem 1rem;
    margin:0.4rem 0 0.4rem 18%;
    font-size:0.88rem;
    line-height:1.5;
}
.chat-bot {
    background:var(--white);
    border:1px solid #dce8dc;
    border-radius:18px 18px 18px 4px;
    padding:0.6rem 1rem;
    margin:0.4rem 18% 0.4rem 0;
    font-size:0.88rem;
    line-height:1.6;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);
}
.chat-label { font-size:0.68rem; color:#888; margin:2px 4px; }
.chat-label-right { text-align:right; }

.section-header {
    display:flex; align-items:center; gap:0.5rem;
    border-left:4px solid var(--moss);
    padding-left:0.8rem;
    margin:1rem 0 0.6rem;
}
.section-header h3 { margin:0; color:var(--dark); }

.cart-item {
    background:var(--white);
    border-radius:10px;
    padding:0.75rem 1rem;
    margin-bottom:0.5rem;
    border:1px solid #e0e0e0;
    display:flex;
    align-items:center;
    justify-content:space-between;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display:none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA CATALOG
# ─────────────────────────────────────────────

PLANTS = [
    {"id": "PL01", "name": "Snake Plant", "emoji": "🪴", "price": 249, "mrp": 349,
     "desc": "Virtually indestructible, air-purifying. Perfect for beginners.",
     "images": ["https://images.unsplash.com/photo-1620127252536-03bdfbda8090?w=400", "https://images.unsplash.com/photo-1599598425947-5202edd56fde?w=400"],
     "tags": ["Indoor", "Low Maintenance"], "light": "Low-Medium", "water": "Weekly"},
    {"id": "PL02", "name": "Monstera Deliciosa", "emoji": "🌿", "price": 399, "mrp": 549,
     "desc": "Iconic split leaves. Dramatic tropical statement plant.",
     "images": ["https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=400", "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400"],
     "tags": ["Indoor", "Statement"], "light": "Indirect", "water": "Twice weekly"},
    {"id": "PL03", "name": "Peace Lily", "emoji": "🌸", "price": 199, "mrp": 279,
     "desc": "Elegant white blooms, purifies air of toxins. Low-light champion.",
     "images": ["https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400", "https://images.unsplash.com/photo-1585503419537-9f28cfe10d38?w=400"],
     "tags": ["Flowering", "Air Purifying"], "light": "Low", "water": "Twice weekly"},
    {"id": "PL04", "name": "Pothos", "emoji": "🌱", "price": 149, "mrp": 199,
     "desc": "Trailing vines, tolerates neglect. Ideal for shelves and hangers.",
     "images": ["https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=400", "https://images.unsplash.com/photo-1585400944055-0c0e3be44d24?w=400"],
     "tags": ["Indoor", "Trailing"], "light": "Low-Bright", "water": "Weekly"},
    {"id": "PL05", "name": "Fiddle Leaf Fig", "emoji": "🌳", "price": 599, "mrp": 799,
     "desc": "Designer's favourite with large violin-shaped leaves. Bold statement.",
     "images": ["https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=400", "https://images.unsplash.com/photo-1612539460963-b5cf4fb2e918?w=400"],
     "tags": ["Indoor", "Statement"], "light": "Bright Indirect", "water": "Weekly"},
    {"id": "PL06", "name": "Rubber Plant", "emoji": "🍃", "price": 329, "mrp": 449,
     "desc": "Glossy burgundy leaves, easy care. Grows into a stunning indoor tree.",
     "images": ["https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=400", "https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=400"],
     "tags": ["Indoor", "Easy Care"], "light": "Medium-Bright", "water": "Weekly"},
    {"id": "PL07", "name": "Aloe Vera", "emoji": "🌵", "price": 179, "mrp": 249,
     "desc": "Natural healer. Soothing gel for skin, needs minimal water.",
     "images": ["https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400", "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=400"],
     "tags": ["Succulent", "Medicinal"], "light": "Bright", "water": "Bi-weekly"},
    {"id": "PL08", "name": "Spider Plant", "emoji": "🌾", "price": 129, "mrp": 179,
     "desc": "Variegated foliage with baby plantlets. Great for hanging baskets.",
     "images": ["https://images.unsplash.com/photo-1589393922695-ef4c2f9b4cf6?w=400", "https://images.unsplash.com/photo-1620127252536-03bdfbda8090?w=400"],
     "tags": ["Indoor", "Hanging"], "light": "Indirect", "water": "Twice weekly"},
    {"id": "PL09", "name": "ZZ Plant", "emoji": "🪴", "price": 299, "mrp": 399,
     "desc": "Glossy dark-green leaves, nearly indestructible. Perfect for offices.",
     "images": ["https://images.unsplash.com/photo-1599598425947-5202edd56fde?w=400", "https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400"],
     "tags": ["Indoor", "Low Light"], "light": "Low", "water": "Bi-weekly"},
    {"id": "PL10", "name": "Bird of Paradise", "emoji": "🦜", "price": 799, "mrp": 1099,
     "desc": "Tropical showstopper with dramatic leaves. Grows up to 6 feet indoors.",
     "images": ["https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400", "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=400"],
     "tags": ["Tropical", "Statement"], "light": "Bright", "water": "Twice weekly"},
    {"id": "PL11", "name": "Calathea Orbifolia", "emoji": "🌿", "price": 449, "mrp": 599,
     "desc": "Stunning silver-striped leaves that move with light. Prayer plant.",
     "images": ["https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=400", "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400"],
     "tags": ["Tropical", "Patterned"], "light": "Medium Indirect", "water": "Twice weekly"},
    {"id": "PL12", "name": "String of Pearls", "emoji": "🫧", "price": 219, "mrp": 299,
     "desc": "Trailing succulent with bead-like leaves. Stunning in hanging planters.",
     "images": ["https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400", "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=400"],
     "tags": ["Succulent", "Trailing"], "light": "Bright Indirect", "water": "Bi-weekly"},
    {"id": "PL13", "name": "Dracaena Marginata", "emoji": "🌴", "price": 349, "mrp": 479,
     "desc": "Architectural spiky form with red-edged leaves. Excellent air purifier.",
     "images": ["https://images.unsplash.com/photo-1620127252536-03bdfbda8090?w=400", "https://images.unsplash.com/photo-1589393922695-ef4c2f9b4cf6?w=400"],
     "tags": ["Indoor", "Air Purifying"], "light": "Medium", "water": "Weekly"},
    {"id": "PL14", "name": "Chinese Evergreen", "emoji": "🍀", "price": 199, "mrp": 269,
     "desc": "Colourful patterned foliage. One of the easiest plants to grow.",
     "images": ["https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=400", "https://images.unsplash.com/photo-1599598425947-5202edd56fde?w=400"],
     "tags": ["Indoor", "Beginner"], "light": "Low-Medium", "water": "Weekly"},
    {"id": "PL15", "name": "Jade Plant", "emoji": "💚", "price": 229, "mrp": 319,
     "desc": "Thick glossy leaves, symbol of good luck. Long-lived and sculptural.",
     "images": ["https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400", "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=400"],
     "tags": ["Succulent", "Lucky"], "light": "Bright", "water": "Bi-weekly"},
    {"id": "PL16", "name": "Anthurium", "emoji": "❤️", "price": 349, "mrp": 499,
     "desc": "Waxy heart-shaped blooms in red, pink, or white. Long-lasting flowers.",
     "images": ["https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400", "https://images.unsplash.com/photo-1585503419537-9f28cfe10d38?w=400"],
     "tags": ["Flowering", "Tropical"], "light": "Indirect", "water": "Twice weekly"},
    {"id": "PL17", "name": "Bamboo Palm", "emoji": "🎋", "price": 499, "mrp": 699,
     "desc": "Elegant feathery fronds, thrives in shaded corners. Natural humidifier.",
     "images": ["https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400", "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=400"],
     "tags": ["Palm", "Indoor"], "light": "Low-Medium", "water": "Twice weekly"},
    {"id": "PL18", "name": "Philodendron Heartleaf", "emoji": "💛", "price": 179, "mrp": 249,
     "desc": "Vining philodendron with heart-shaped leaves. Rapidly trailing beauty.",
     "images": ["https://images.unsplash.com/photo-1589393922695-ef4c2f9b4cf6?w=400", "https://images.unsplash.com/photo-1620127252536-03bdfbda8090?w=400"],
     "tags": ["Trailing", "Easy Care"], "light": "Medium Indirect", "water": "Weekly"},
    {"id": "PL19", "name": "Boston Fern", "emoji": "🌿", "price": 259, "mrp": 359,
     "desc": "Lush arching fronds. Loves humidity — perfect for bathrooms.",
     "images": ["https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=400", "https://images.unsplash.com/photo-1589393922695-ef4c2f9b4cf6?w=400"],
     "tags": ["Fern", "Hanging"], "light": "Indirect", "water": "Frequent"},
    {"id": "PL20", "name": "Cactus Mix", "emoji": "🌵", "price": 299, "mrp": 399,
     "desc": "Set of 3 assorted cacti in terracotta. Near-zero maintenance. Desert chic.",
     "images": ["https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400", "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=400"],
     "tags": ["Cactus", "Set"], "light": "Full Sun", "water": "Monthly"},
    {"id": "PL21", "name": "Croton", "emoji": "🎨", "price": 229, "mrp": 319,
     "desc": "Fiery multicolour leaves in reds, oranges, and yellows. Bold accent plant.",
     "images": ["https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=400", "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400"],
     "tags": ["Tropical", "Colorful"], "light": "Bright", "water": "Weekly"},
    {"id": "PL22", "name": "Lucky Bamboo", "emoji": "🀄", "price": 149, "mrp": 199,
     "desc": "Grows in water or soil. Symbol of fortune and positive energy in Feng Shui.",
     "images": ["https://images.unsplash.com/photo-1599598425947-5202edd56fde?w=400", "https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400"],
     "tags": ["Lucky", "Indoor"], "light": "Low-Indirect", "water": "Weekly"},
    {"id": "PL23", "name": "Hoya Carnosa", "emoji": "🌺", "price": 319, "mrp": 449,
     "desc": "Porcelain flower clusters with sweet fragrance. Succulent-like waxy leaves.",
     "images": ["https://images.unsplash.com/photo-1585503419537-9f28cfe10d38?w=400", "https://images.unsplash.com/photo-1585400944055-0c0e3be44d24?w=400"],
     "tags": ["Flowering", "Trailing"], "light": "Bright Indirect", "water": "Bi-weekly"},
    {"id": "PL24", "name": "Money Plant (Scindapsus)", "emoji": "💰", "price": 99, "mrp": 149,
     "desc": "Beloved Indian classic with heart-shaped leaves. Grows anywhere.",
     "images": ["https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=400", "https://images.unsplash.com/photo-1620127252536-03bdfbda8090?w=400"],
     "tags": ["Indoor", "Beginner"], "light": "Any", "water": "Weekly"},
    {"id": "PL25", "name": "Areca Palm", "emoji": "🌴", "price": 549, "mrp": 749,
     "desc": "Feathery fronds bring tropical vibes. Top-rated natural humidifier.",
     "images": ["https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400", "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=400"],
     "tags": ["Palm", "Air Purifying"], "light": "Bright Indirect", "water": "Twice weekly"},
    {"id": "PL26", "name": "Bonsai Ficus", "emoji": "🎍", "price": 899, "mrp": 1199,
     "desc": "Miniature tree, handcrafted into art. Patience rewarded beautifully.",
     "images": ["https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=400", "https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=400"],
     "tags": ["Bonsai", "Gift"], "light": "Bright", "water": "Daily mist"},
    {"id": "PL27", "name": "Tulsi (Holy Basil)", "emoji": "🌿", "price": 79, "mrp": 119,
     "desc": "Sacred Indian herb. Medicinal, aromatic, auspicious. Perfect for balconies.",
     "images": ["https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400", "https://images.unsplash.com/photo-1589393922695-ef4c2f9b4cf6?w=400"],
     "tags": ["Herb", "Medicinal"], "light": "Full Sun", "water": "Daily"},
    {"id": "PL28", "name": "Orchid (Phalaenopsis)", "emoji": "🌸", "price": 649, "mrp": 899,
     "desc": "Elegant moth orchid blooms for months. The ultimate luxury indoor plant.",
     "images": ["https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400", "https://images.unsplash.com/photo-1585503419537-9f28cfe10d38?w=400"],
     "tags": ["Flowering", "Luxury"], "light": "Bright Indirect", "water": "Weekly"},
    {"id": "PL29", "name": "Peperomia Obtusifolia", "emoji": "🫧", "price": 189, "mrp": 259,
     "desc": "Baby rubber plant with thick glossy leaves. Compact and virtually carefree.",
     "images": ["https://images.unsplash.com/photo-1599598425947-5202edd56fde?w=400", "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400"],
     "tags": ["Compact", "Easy Care"], "light": "Medium", "water": "Bi-weekly"},
    {"id": "PL30", "name": "Lavender", "emoji": "💜", "price": 279, "mrp": 379,
     "desc": "Fragrant purple spikes, calming aroma. Perfect for sunny balconies.",
     "images": ["https://images.unsplash.com/photo-1585400944055-0c0e3be44d24?w=400", "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=400"],
     "tags": ["Flowering", "Fragrant"], "light": "Full Sun", "water": "Weekly"},
    {"id": "PL31", "name": "Succulents Gift Pack", "emoji": "🌱", "price": 399, "mrp": 549,
     "desc": "Set of 5 assorted succulents in cute pots. Perfect birthday or housewarming gift.",
     "images": ["https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400", "https://images.unsplash.com/photo-1512428813834-c702c7702b78?w=400"],
     "tags": ["Gift", "Set"], "light": "Bright", "water": "Bi-weekly"},
    {"id": "PL32", "name": "Dieffenbachia", "emoji": "🌿", "price": 239, "mrp": 329,
     "desc": "Bold tropical foliage with cream-and-green patterns. Fast grower indoors.",
     "images": ["https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=400", "https://images.unsplash.com/photo-1589393922695-ef4c2f9b4cf6?w=400"],
     "tags": ["Tropical", "Indoor"], "light": "Medium Indirect", "water": "Weekly"},
]

PLANT_CARE = [
    {"id": "C01", "name": "Organic Growth Booster", "emoji": "🌱", "cat": "Fertilizer",
     "price": 349, "mrp": 499, "desc": "Balanced NPK + humic acid + seaweed extract. Promotes lush vigorous growth for all plants.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C02", "name": "Neem-Guard Pesticide Spray", "emoji": "🛡️", "cat": "Pesticide",
     "price": 279, "mrp": 399, "desc": "Cold-pressed neem oil. Controls aphids, spider mites, whiteflies, and fungal infections naturally.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C03", "name": "AquaSave Moisture Granules", "emoji": "💧", "cat": "Soil",
     "price": 199, "mrp": 299, "desc": "Hydrogel water-retention granules. Keeps roots moist for up to 7 days, reduces watering by 40%.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C04", "name": "RootRevive Rooting Hormone", "emoji": "🌿", "cat": "Fertilizer",
     "price": 189, "mrp": 249, "desc": "IBA formula for strong root development. Ideal for propagation and transplanting stress.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C05", "name": "FungoClear Systemic Fungicide", "emoji": "🍄", "cat": "Pesticide",
     "price": 319, "mrp": 449, "desc": "Broad-spectrum systemic fungicide. Eliminates powdery mildew, black spot, rust, and blight.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C06", "name": "CompoRich Vermicompost", "emoji": "🪱", "cat": "Fertilizer",
     "price": 249, "mrp": 349, "desc": "Premium worm castings with beneficial microbes. Improves soil structure and nutrient availability.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C07", "name": "ErgoGrip Pruning Shears", "emoji": "✂️", "cat": "Tool",
     "price": 599, "mrp": 799, "desc": "Japanese SK5 steel blades, non-slip rubber grip. Makes clean cuts to prevent disease entry.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C08", "name": "SoilSense pH Testing Kit", "emoji": "🧪", "cat": "Tool",
     "price": 449, "mrp": 599, "desc": "Digital 3-in-1 meter: soil pH, moisture, and light intensity. Takes guesswork out of plant care.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C09", "name": "MicroBloom Liquid Foliar Feed", "emoji": "🌸", "cat": "Fertilizer",
     "price": 229, "mrp": 329, "desc": "High-K + P formula for prolific blooming. Chelated iron prevents chlorosis.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C10", "name": "SilverShield Insecticidal Soap", "emoji": "🪲", "cat": "Pesticide",
     "price": 159, "mrp": 219, "desc": "Potassium salt of fatty acids. Targets soft-bodied insects on contact without harming beneficial bugs.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C11", "name": "Coco Peat Block", "emoji": "🟫", "cat": "Soil",
     "price": 149, "mrp": 199, "desc": "Compressed coconut coir block. Expands to 8L of light, airy, pH-neutral growing medium.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "C12", "name": "Drip Irrigation Kit", "emoji": "🚿", "cat": "Tool",
     "price": 849, "mrp": 1199, "desc": "Automated drip system for 10 plants. Timer-controlled, reduces water waste by 60%.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
]

POTS = [
    {"id": "PT01", "name": "Terracotta Classic 6\"", "emoji": "🪴", "price": 129, "mrp": 179,
     "desc": "Traditional unglazed terracotta. Breathable walls prevent root rot. Sizes 4\"–12\".",
     "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400"},
    {"id": "PT02", "name": "Ceramic Nordic White", "emoji": "⬜", "price": 349, "mrp": 499,
     "desc": "Minimalist matte-white ceramic with drainage hole and bamboo tray.",
     "img": "https://images.unsplash.com/photo-1495231916356-a86217efff12?w=400"},
    {"id": "PT03", "name": "Hanging Macramé Planter", "emoji": "🪢", "price": 249, "mrp": 349,
     "desc": "Hand-knotted natural jute rope. Bohemian style, fits pots up to 6\".",
     "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400"},
    {"id": "PT04", "name": "Self-Watering Planter 8\"", "emoji": "💧", "price": 499, "mrp": 699,
     "desc": "Built-in water reservoir with wicking system. Waters itself for up to 2 weeks.",
     "img": "https://images.unsplash.com/photo-1495231916356-a86217efff12?w=400"},
    {"id": "PT05", "name": "Concrete Geometric Pot", "emoji": "⬡", "price": 399, "mrp": 549,
     "desc": "Modern hexagonal concrete pot. Heavy, stable base. Drainage hole included.",
     "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400"},
    {"id": "PT06", "name": "Wicker Basket Planter", "emoji": "🧺", "price": 299, "mrp": 399,
     "desc": "Natural rattan wicker basket with waterproof liner. Earthy rustic look.",
     "img": "https://images.unsplash.com/photo-1495231916356-a86217efff12?w=400"},
    {"id": "PT07", "name": "Coloured Glazed Ceramic Set", "emoji": "🎨", "price": 599, "mrp": 799,
     "desc": "Set of 3 handpainted glazed ceramic pots in cobalt, terracotta, sage.",
     "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400"},
    {"id": "PT08", "name": "Tall Floor Planter 12\"", "emoji": "🏛️", "price": 799, "mrp": 1099,
     "desc": "Statement-sized fibreglass floor planter. Lightweight, weather-resistant.",
     "img": "https://images.unsplash.com/photo-1495231916356-a86217efff12?w=400"},
    {"id": "PT09", "name": "Window Box Planter (60cm)", "emoji": "🪟", "price": 449, "mrp": 599,
     "desc": "Rectangular balcony railing planter with mounting brackets. UV-stable plastic.",
     "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400"},
    {"id": "PT10", "name": "Nursery Grow Bag (5L)", "emoji": "🛍️", "price": 49, "mrp": 79,
     "desc": "Pack of 5 breathable fabric grow bags. Promotes air pruning for strong roots.",
     "img": "https://images.unsplash.com/photo-1495231916356-a86217efff12?w=400"},
]

SEEDS = [
    {"id": "S01", "name": "Cherry Tomato Seeds", "emoji": "🍅", "price": 79, "mrp": 119,
     "desc": "High-yield hybrid variety. Compact plant, perfect for balcony containers.",
     "img": "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=400"},
    {"id": "S02", "name": "Basil (Sweet Genovese)", "emoji": "🌿", "price": 59, "mrp": 89,
     "desc": "Classic Italian basil. Fragrant leaves perfect for cooking. Germinates in 5 days.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "S03", "name": "Marigold Flower Seeds", "emoji": "🌻", "price": 49, "mrp": 79,
     "desc": "Vibrant orange-yellow blooms. Natural pest repellent, easy to grow.",
     "img": "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=400"},
    {"id": "S04", "name": "Spinach (Baby Leaf) Seeds", "emoji": "🥬", "price": 69, "mrp": 99,
     "desc": "Fast-growing baby spinach. Ready to harvest in 25–30 days. Nutrition-packed.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "S05", "name": "Sunflower Dwarf Mix", "emoji": "🌻", "price": 89, "mrp": 129,
     "desc": "Compact 60cm sunflowers in yellow, orange, and red. Great for pots.",
     "img": "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=400"},
    {"id": "S06", "name": "Chilli (Bird's Eye) Seeds", "emoji": "🌶️", "price": 79, "mrp": 119,
     "desc": "Extra-hot bird's eye chillies. Prolific bearer, compact plant for windowsills.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "S07", "name": "Mint (Spearmint) Seeds", "emoji": "🫙", "price": 59, "mrp": 89,
     "desc": "Aromatic spearmint for teas, cocktails, and cooking. Rapid spreader in pots.",
     "img": "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=400"},
    {"id": "S08", "name": "Wildflower Meadow Mix", "emoji": "🌸", "price": 129, "mrp": 179,
     "desc": "20-species blend of native wildflowers. Scatter-and-grow biodiversity garden.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
    {"id": "S09", "name": "Cucumber (Bush) Seeds", "emoji": "🥒", "price": 89, "mrp": 129,
     "desc": "Compact bush cucumber ideal for containers. Crisp, mild-flavoured fruits.",
     "img": "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=400"},
    {"id": "S10", "name": "Pansy Viola Mix", "emoji": "💜", "price": 99, "mrp": 149,
     "desc": "Cold-tolerant pansies in mixed jewel tones. Perfect for winter balconies.",
     "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"},
]

# Chatbot recommendations map
CHAT_INTENTS = {
    "birthday gift": ["PL31", "PL28", "PL22"],
    "indoor plants": ["PL01", "PL09", "PL24"],
    "low maintenance": ["PL01", "PL04", "PL07"],
    "gift": ["PL31", "PL28", "PL26"],
    "beginner": ["PL04", "PL01", "PL24"],
    "flowering": ["PL03", "PL16", "PL30"],
    "best fertilizer": ["C01", "C06", "C09"],
    "snake plant pot": ["PT01", "PT02", "PT04"],
    "pest": ["C02", "C10", "C05"],
    "seeds": ["S01", "S02", "S03"],
}

DIAGNOSES = [
    {"title": "🏜️ Drought / Dry Stress", "desc": "Plant appears dehydrated — wilting, dry soil, curling leaves.", "recs": ["C03", "C01"]},
    {"title": "🐛 Pest Infestation", "desc": "Signs of insect activity — discolouration, sticky residue, or webbing.", "recs": ["C02", "C10"]},
    {"title": "🍄 Fungal Infection", "desc": "White powder, rust spots, or black sooty mould detected.", "recs": ["C05", "C02"]},
    {"title": "🟡 Nutrient Deficiency", "desc": "Interveinal yellowing and pale new growth indicate nutrient deficiency.", "recs": ["C09", "C01"]},
    {"title": "💦 Overwatering", "desc": "Soggy soil, mushy base, drooping despite wet soil — possible root rot.", "recs": ["C04", "C11"]},
]


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "🏠 Home",
        "cart": [],
        "chatbot_open": False,
        "chat_history": [],
        "chat_stage": "welcome",  # welcome | buying | care | done
        "uploaded_image": None,
        "diagnosis": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def add_to_cart(item, item_type):
    entry = {**item, "type": item_type}
    st.session_state.cart.append(entry)
    st.toast(f"✅ {item['name']} added to cart!", icon="🛒")


def get_items_by_ids(ids, catalog):
    return [item for item in catalog for iid in ids if item["id"] == iid]


def get_all_catalog():
    return PLANTS + PLANT_CARE + POTS + SEEDS


def find_item(item_id):
    for item in get_all_catalog():
        if item["id"] == item_id:
            return item
    return None


def render_plant_card(p, key_prefix, show_details=False):
    discount = round((1 - p["price"] / p["mrp"]) * 100)
    tags_html = " ".join(f'<span style="background:#e8f5e9;color:#2e7d32;font-size:0.68rem;padding:2px 7px;border-radius:20px;margin-right:2px;">{t}</span>' for t in p.get("tags", []))
    st.markdown(f"""
    <div class="product-card">
        <img src="{p['images'][0]}" style="width:100%;border-radius:8px;object-fit:cover;height:140px;" onerror="this.style.display='none'"/>
        <div class="product-name">{p['emoji']} {p['name']}</div>
        <div style="margin:3px 0 6px;">{tags_html}</div>
        <div style="font-size:0.78rem;color:#666;margin-bottom:4px;">
            💡 {p.get('light','–')} &nbsp;|&nbsp; 💧 {p.get('water','–')}
        </div>
        <div class="product-desc">{p['desc']}</div>
        <div>
            <span class="product-price">₹{p['price']}</span>
            <span class="product-mrp">₹{p['mrp']}</span>
            <span class="off-badge">{discount}% OFF</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🛒 Add to Cart", key=f"{key_prefix}_{p['id']}", use_container_width=True):
        add_to_cart(p, "plant")


def render_product_card(p, key_prefix, item_type="care"):
    discount = round((1 - p["price"] / p["mrp"]) * 100)
    chip_class = {"Fertilizer": "chip-plant", "Pesticide": "chip-care", "Tool": "chip-pot", "Soil": "chip-seed"}.get(p.get("cat", ""), "chip-plant")
    st.markdown(f"""
    <div class="product-card">
        <div style="font-size:2.5rem;text-align:center;margin:4px 0;">{p['emoji']}</div>
        <div class="product-name">{p['name']}</div>
        <span class="category-chip {chip_class}">{p.get('cat', item_type.title())}</span>
        <div class="product-desc">{p['desc']}</div>
        <div>
            <span class="product-price">₹{p['price']}</span>
            <span class="product-mrp">₹{p['mrp']}</span>
            <span class="off-badge">{discount}% OFF</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🛒 Add to Cart", key=f"{key_prefix}_{p['id']}", use_container_width=True):
        add_to_cart(p, item_type)


def render_chat_bubble(role, content):
    if role == "user":
        st.markdown(f'<div class="chat-label chat-label-right">You</div><div class="chat-user">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-label">🌿 PlantBot</div><div class="chat-bot">{content}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.2rem 0 0.5rem;'>
        <div style='font-size:2.5rem;'>🌿</div>
        <div style='font-family:Lora,serif;font-size:1.5rem;font-weight:700;color:#b2dfbc;'>GreenLeaf</div>
        <div style='font-size:0.7rem;color:#6a9c6e;letter-spacing:0.1em;text-transform:uppercase;'>Your Garden Store</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠 Home", "🪴 Plants", "🌱 Plant Care", "🪴 Pots", "🌾 Seeds", "🛒 Cart", "🤖 PlantBot"],
        index=["🏠 Home", "🪴 Plants", "🌱 Plant Care", "🪴 Pots", "🌾 Seeds", "🛒 Cart", "🤖 PlantBot"].index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = page
    st.divider()

    cart_count = len(st.session_state.cart)
    total = sum(p["price"] for p in st.session_state.cart)
    if cart_count:
        st.markdown(f"🛒 **{cart_count} item(s)** in cart")
        st.markdown(f"💰 Total: **₹{total}**")
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()
    else:
        st.markdown("<div style='font-size:0.8rem;color:#6a9c6e;'>🛒 Your cart is empty</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size:0.7rem;color:#4a6b4d;text-align:center;'>Made with 🌱 for plant lovers<br/>© 2025 GreenLeaf</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
def render_home():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-leaf">🌿</div>
        <h1>Welcome to GreenLeaf</h1>
        <p>30+ plants · Expert care products · Free delivery above ₹499 · Next-day available</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (val, label) in zip([c1, c2, c3, c4], [("30+", "Plants"), ("12", "Care Products"), ("10", "Pot Styles"), ("100%", "Organic Options")]):
        with col:
            st.markdown(f'<div class="metric-pill"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🌿 Shop by Category")
    cats = [
        ("🪴", "Plants", "30+ varieties", "#e8f5e9", "#1b5e20", "🪴 Plants"),
        ("🌱", "Plant Care", "Fertilizers, pesticides & tools", "#fff3e0", "#e65100", "🌱 Plant Care"),
        ("🪴", "Pots & Planters", "Terracotta to self-watering", "#ede7f6", "#4527a0", "🪴 Pots"),
        ("🌾", "Seeds", "Flowers, herbs & veggies", "#e0f7fa", "#006064", "🌾 Seeds"),
    ]
    cols = st.columns(4)
    for col, (icon, name, tag, bg, fg, nav) in zip(cols, cats):
        with col:
            st.markdown(f"""
            <div style="background:{bg};border-radius:12px;padding:1.2rem;text-align:center;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-weight:700;color:{fg};font-size:0.95rem;">{name}</div>
                <div style="font-size:0.75rem;color:#777;margin-top:3px;">{tag}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Browse {name}", key=f"home_nav_{name}", use_container_width=True):
                st.session_state.page = nav
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎁 Great for Gifting")
    gift_ids = ["PL31", "PL28", "PL26", "PL22"]
    gcols = st.columns(4)
    for col, pid in zip(gcols, gift_ids):
        with col:
            p = find_item(pid)
            if p:
                st.markdown(f"""
                <div class="product-card" style="text-align:center;">
                    <img src="{p['images'][0]}" style="width:100%;border-radius:8px;height:100px;object-fit:cover;" onerror="this.style.display='none'"/>
                    <div class="product-name" style="font-size:0.88rem;">{p['emoji']} {p['name']}</div>
                    <span class="product-price" style="font-size:0.95rem;">₹{p['price']}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🛒 Add", key=f"home_gift_{pid}", use_container_width=True):
                    add_to_cart(p, "plant")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🪴 Browse All Plants", use_container_width=True):
            st.session_state.page = "🪴 Plants"
            st.rerun()
    with col_b:
        if st.button("🤖 Chat with PlantBot", use_container_width=True):
            st.session_state.page = "🤖 PlantBot"
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: PLANTS
# ─────────────────────────────────────────────
def render_plants():
    st.markdown("## 🪴 Plants Store")
    st.caption(f"{len(PLANTS)} plants available · Free delivery above ₹499")
    st.divider()

    all_tags = sorted({t for p in PLANTS for t in p.get("tags", [])})
    f1, f2, f3 = st.columns([2, 2, 3])
    with f1:
        tag_filter = st.selectbox("Filter by type", ["All"] + all_tags)
    with f2:
        sort_by = st.selectbox("Sort by", ["Default", "Price: Low → High", "Price: High → Low"])
    with f3:
        search = st.text_input("🔍 Search plants", placeholder="e.g. monstera, succulent...")

    display = PLANTS
    if tag_filter != "All":
        display = [p for p in display if tag_filter in p.get("tags", [])]
    if search:
        s = search.lower()
        display = [p for p in display if s in p["name"].lower() or s in p["desc"].lower()]
    if sort_by == "Price: Low → High":
        display = sorted(display, key=lambda x: x["price"])
    elif sort_by == "Price: High → Low":
        display = sorted(display, key=lambda x: x["price"], reverse=True)

    st.caption(f"Showing {len(display)} plant(s)")

    for i in range(0, len(display), 4):
        cols = st.columns(4)
        for col, p in zip(cols, display[i:i+4]):
            with col:
                render_plant_card(p, "plants_page")


# ─────────────────────────────────────────────
# PAGE: PLANT CARE
# ─────────────────────────────────────────────
def render_plant_care():
    st.markdown("## 🌱 Plant Care")
    st.caption("Fertilizers · Pesticides · Tools · Soil — everything your plants need")
    st.divider()

    cats = ["All", "Fertilizer", "Pesticide", "Tool", "Soil"]
    f1, f2 = st.columns([2, 5])
    with f1:
        cat_filter = st.selectbox("Category", cats)

    display = PLANT_CARE if cat_filter == "All" else [p for p in PLANT_CARE if p.get("cat") == cat_filter]
    st.caption(f"Showing {len(display)} product(s)")

    for i in range(0, len(display), 3):
        cols = st.columns(3)
        for col, p in zip(cols, display[i:i+3]):
            with col:
                render_product_card(p, "care_page", "care")


# ─────────────────────────────────────────────
# PAGE: POTS
# ─────────────────────────────────────────────
def render_pots():
    st.markdown("## 🪴 Pots & Planters")
    st.caption("Terracotta, ceramic, self-watering, hanging and more")
    st.divider()

    f1, f2 = st.columns([2, 5])
    with f1:
        sort_by = st.selectbox("Sort by", ["Default", "Price: Low → High", "Price: High → Low"])

    display = POTS
    if sort_by == "Price: Low → High":
        display = sorted(display, key=lambda x: x["price"])
    elif sort_by == "Price: High → Low":
        display = sorted(display, key=lambda x: x["price"], reverse=True)

    for i in range(0, len(display), 4):
        cols = st.columns(4)
        for col, p in zip(cols, display[i:i+4]):
            with col:
                discount = round((1 - p["price"] / p["mrp"]) * 100)
                st.markdown(f"""
                <div class="product-card">
                    <img src="{p['img']}" style="width:100%;border-radius:8px;height:130px;object-fit:cover;" onerror="this.style.display='none'"/>
                    <div class="product-name">{p['emoji']} {p['name']}</div>
                    <div class="product-desc">{p['desc']}</div>
                    <span class="product-price">₹{p['price']}</span>
                    <span class="product-mrp">₹{p['mrp']}</span>
                    <span class="off-badge">{discount}% OFF</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🛒 Add to Cart", key=f"pot_{p['id']}", use_container_width=True):
                    add_to_cart(p, "pot")


# ─────────────────────────────────────────────
# PAGE: SEEDS
# ─────────────────────────────────────────────
def render_seeds():
    st.markdown("## 🌾 Seeds")
    st.caption("Vegetables · Herbs · Flowers — grow your own garden from scratch")
    st.divider()

    search = st.text_input("🔍 Search seeds", placeholder="e.g. tomato, basil...")
    display = SEEDS
    if search:
        s = search.lower()
        display = [p for p in display if s in p["name"].lower() or s in p["desc"].lower()]

    st.caption(f"Showing {len(display)} seed packet(s)")

    for i in range(0, len(display), 4):
        cols = st.columns(4)
        for col, p in zip(cols, display[i:i+4]):
            with col:
                discount = round((1 - p["price"] / p["mrp"]) * 100)
                st.markdown(f"""
                <div class="product-card" style="text-align:center;">
                    <div style="font-size:2.8rem;">{p['emoji']}</div>
                    <div class="product-name">{p['name']}</div>
                    <div class="product-desc">{p['desc']}</div>
                    <span class="product-price">₹{p['price']}</span>
                    <span class="product-mrp">₹{p['mrp']}</span>
                    <span class="off-badge">{discount}% OFF</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🛒 Add to Cart", key=f"seed_{p['id']}", use_container_width=True):
                    add_to_cart(p, "seed")


# ─────────────────────────────────────────────
# PAGE: CART
# ─────────────────────────────────────────────
def render_cart():
    st.markdown("## 🛒 Your Cart")
    st.divider()

    if not st.session_state.cart:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#aaa;">
            <div style="font-size:4rem;">🛒</div>
            <div style="font-size:1.1rem;margin-top:0.5rem;color:#888;">Your cart is empty</div>
            <div style="font-size:0.85rem;color:#bbb;margin-top:0.3rem;">Add plants, care products, pots, or seeds to get started.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🪴 Start Shopping", use_container_width=True):
            st.session_state.page = "🏠 Home"
            st.rerun()
        return

    left, right = st.columns([2, 1], gap="large")

    with left:
        st.markdown(f"### {len(st.session_state.cart)} item(s)")
        for idx, item in enumerate(st.session_state.cart):
            type_label = {"plant": "🪴 Plant", "care": "🌱 Care", "pot": "🪴 Pot", "seed": "🌾 Seed"}.get(item.get("type", ""), "")
            st.markdown(f"""
            <div class="cart-item">
                <div>
                    <div style="font-weight:700;font-family:Lora,serif;color:#3d6b45;">{item.get('emoji','')} {item['name']}</div>
                    <div style="font-size:0.75rem;color:#888;">{type_label}</div>
                </div>
                <div style="font-weight:700;font-size:1.05rem;color:#6b4226;">₹{item['price']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Remove", key=f"remove_{idx}", help="Remove this item"):
                st.session_state.cart.pop(idx)
                st.rerun()

    with right:
        total = sum(p["price"] for p in st.session_state.cart)
        mrp_total = sum(p["mrp"] for p in st.session_state.cart)
        savings = mrp_total - total
        st.markdown("""
        <div style="background:#fff;border:1px solid #dce8dc;border-radius:14px;padding:1.5rem;">
        """, unsafe_allow_html=True)
        st.markdown("### 🧾 Order Summary")
        st.markdown(f"**Items ({len(st.session_state.cart)}):** ₹{mrp_total}")
        st.markdown(f"**Discount:** -₹{savings} 🎉")
        if total >= 499:
            st.markdown("**Delivery:** FREE ✅")
        else:
            st.markdown(f"**Delivery:** ₹49 (add ₹{499-total} more for free delivery)")
        st.divider()
        final = total if total >= 499 else total + 49
        st.markdown(f"## ₹{final}")
        st.markdown(f"<div style='color:#2e7d32;font-size:0.85rem;'>You save ₹{savings} on this order!</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Place Order", use_container_width=True):
            st.session_state.cart = []
            st.success("🎉 Order placed successfully! Your plants are on their way!")
            st.balloons()
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: PLANTBOT CHATBOT
# ─────────────────────────────────────────────
def handle_chat_text(user_text):
    lower = user_text.lower()

    # Match intents
    matched_ids = []
    matched_key = None
    for key, ids in CHAT_INTENTS.items():
        if any(word in lower for word in key.split()):
            matched_ids = ids
            matched_key = key
            break

    if matched_ids:
        items = []
        for iid in matched_ids:
            item = find_item(iid)
            if item:
                items.append(item)
        names = ", ".join(f"**{i.get('emoji','')} {i['name']}** (₹{i['price']})" for i in items)
        response = f"Great choice! Based on '{matched_key}', I recommend:\n\n{names}\n\nClick **Add to Cart** below each product to get them!"
        return response, items
    elif any(w in lower for w in ["water", "how often", "irrigation"]):
        return ("💧 **Watering Guide:**\n\n• Tropical plants: every 2–3 days in summer\n• Succulents & cacti: every 10–14 days\n• Ferns: keep soil consistently moist\n\nOur **AquaSave Moisture Granules** reduces watering needs by 40%!", [find_item("C03")])
    elif any(w in lower for w in ["yellow", "yellowing", "pale"]):
        return ("🟡 **Yellowing leaves** are usually caused by nutrient deficiency or overwatering.\n\nRecommended: **MicroBloom Foliar Feed** and **CompoRich Vermicompost**.", [find_item("C09"), find_item("C06")])
    elif any(w in lower for w in ["hello", "hi", "hey", "namaste"]):
        return ("👋 Hello! I'm PlantBot. Ask me anything about plants, care tips, or product recommendations. You can also upload a plant photo for a diagnosis!", [])
    else:
        return ("🌿 I can help you with plant recommendations, care tips, and product advice! Try asking:\n• 'Best indoor plants'\n• 'Fertilizer for indoor plants'\n• 'Birthday gift plant'\n• Or upload a plant photo for diagnosis.", [])


def render_plantbot():
    st.markdown("## 🤖 PlantBot")
    st.caption("Your AI plant assistant — get recommendations, diagnose plants, and find products.")
    st.divider()

    left, right = st.columns([1, 1.6], gap="large")

    with left:
        st.markdown("### 🌿 What can I help you with?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🪴 Buying Plants", use_container_width=True):
                st.session_state.chat_stage = "buying"
                st.session_state.chat_history.append({"role": "user", "content": "🪴 Buying Plants"})
                st.session_state.chat_history.append({"role": "bot", "content": "Great! What kind of plant are you looking for? Choose below or type your question.", "items": []})
                st.rerun()
        with col2:
            if st.button("🧪 Plant Care Help", use_container_width=True):
                st.session_state.chat_stage = "care"
                st.session_state.chat_history.append({"role": "user", "content": "🧪 Plant Care Help"})
                st.session_state.chat_history.append({"role": "bot", "content": "Upload a photo of your plant for diagnosis, or ask me a care question!", "items": []})
                st.rerun()

        # Quick option buttons based on stage
        if st.session_state.chat_stage == "buying":
            st.markdown("**Quick Options:**")
            quick_opts = ["🎂 Birthday gift?", "🏠 Best indoor plants", "😴 Low maintenance plants", "🌸 Flowering plants"]
            for opt in quick_opts:
                if st.button(opt, use_container_width=True, key=f"qopt_{opt}"):
                    resp, items = handle_chat_text(opt)
                    st.session_state.chat_history.append({"role": "user", "content": opt})
                    st.session_state.chat_history.append({"role": "bot", "content": resp, "items": items or []})
                    st.rerun()

        elif st.session_state.chat_stage == "care":
            st.markdown("**Upload a plant photo for diagnosis:**")
            uploaded = st.file_uploader("Plant image", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
            if uploaded:
                img = Image.open(uploaded)
                st.session_state.uploaded_image = img
                st.image(img, use_container_width=True, caption="Your plant")

            if st.session_state.uploaded_image and st.button("🔬 Diagnose My Plant", use_container_width=True):
                diagnosis = random.choice(DIAGNOSES)
                st.session_state.diagnosis = diagnosis
                rec_items = [find_item(iid) for iid in diagnosis["recs"] if find_item(iid)]
                rec_names = ", ".join(f"{i['emoji']} {i['name']}" for i in rec_items)
                response = f"**{diagnosis['title']}**\n\n{diagnosis['desc']}\n\n**Recommended products:** {rec_names}"
                st.session_state.chat_history.append({"role": "user", "content": "📷 [Plant photo uploaded] — Please diagnose my plant."})
                st.session_state.chat_history.append({"role": "bot", "content": response, "items": rec_items})
                st.rerun()

        # Care quick options
        if st.session_state.chat_stage == "care":
            st.markdown("**Or ask a question:**")
            care_opts = ["💧 How often to water?", "🐛 Pest control help", "🌿 Best fertilizer", "🪴 Snake plant pot?"]
            for opt in care_opts:
                if st.button(opt, use_container_width=True, key=f"copt_{opt}"):
                    resp, items = handle_chat_text(opt)
                    st.session_state.chat_history.append({"role": "user", "content": opt})
                    st.session_state.chat_history.append({"role": "bot", "content": resp, "items": items or []})
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💡 Tips for best photo results"):
            st.markdown("• Take photos in natural light\n• Capture leaves and soil\n• Include affected areas closely\n• Keep the image in focus")

    with right:
        st.markdown("### 💬 Chat")

        chat_container = st.container(height=420, border=True)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style='text-align:center;padding:3rem 1rem;color:#aaa;'>
                    <div style='font-size:3rem;'>🌿</div>
                    <div style='margin-top:0.5rem;font-size:0.9rem;'>Choose an option or type a question to get started!</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    render_chat_bubble(msg["role"] if msg["role"] != "bot" else "bot", msg["content"])

                    # Show product cards for bot messages with items
                    if msg.get("role") == "bot" and msg.get("items"):
                        items = [i for i in msg["items"] if i]
                        if items:
                            item_cols = st.columns(min(len(items), 3))
                            for ic, item in zip(item_cols, items[:3]):
                                with ic:
                                    discount = round((1 - item["price"] / item["mrp"]) * 100)
                                    st.markdown(f"""
                                    <div style="background:#f8f4ee;border:1px solid #dce8dc;border-radius:10px;padding:0.7rem;text-align:center;font-size:0.8rem;">
                                        <div style="font-size:1.8rem;">{item.get('emoji','🌿')}</div>
                                        <div style="font-weight:700;color:#3d6b45;font-size:0.82rem;">{item['name']}</div>
                                        <div style="color:#6b4226;font-weight:700;">₹{item['price']}</div>
                                        <div style="color:#aaa;font-size:0.7rem;text-decoration:line-through;">₹{item['mrp']}</div>
                                        <div style="color:#2e7d32;font-size:0.7rem;">{discount}% OFF</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    if st.button("🛒 Add", key=f"bot_add_{item['id']}_{id(msg)}", use_container_width=True):
                                        add_to_cart(item, "plant" if item["id"].startswith("PL") else "care")

        # Text input
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        inp_col, btn_col = st.columns([5, 1])
        with inp_col:
            user_text = st.text_input("Ask anything", placeholder="e.g. Best plant for dark room?", label_visibility="collapsed", key="chat_input_text")
        with btn_col:
            send = st.button("Send", use_container_width=True)

        if send and user_text.strip():
            resp, items = handle_chat_text(user_text)
            st.session_state.chat_history.append({"role": "user", "content": user_text})
            st.session_state.chat_history.append({"role": "bot", "content": resp, "items": [i for i in (items or []) if i]})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.chat_stage = "welcome"
                st.session_state.diagnosis = None
                st.session_state.uploaded_image = None
                st.rerun()


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
page = st.session_state.page
if page == "🏠 Home":
    render_home()
elif page == "🪴 Plants":
    render_plants()
elif page == "🌱 Plant Care":
    render_plant_care()
elif page == "🪴 Pots":
    render_pots()
elif page == "🌾 Seeds":
    render_seeds()
elif page == "🛒 Cart":
    render_cart()
elif page == "🤖 PlantBot":
    render_plantbot()
