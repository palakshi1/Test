"""
🌿 Verdana — Premium AI-Powered Plant Care Platform
====================================================
Run: streamlit run verdana_app.py

Requirements:
    pip install streamlit anthropic pillow requests

Set your Anthropic API key:
    export ANTHROPIC_API_KEY="sk-ant-..."
    or add it in the sidebar when the app loads.
"""

import streamlit as st
import anthropic
import base64
import random
import os
from io import BytesIO

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Verdana — Your Smart Plant Care Partner",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --forest:#2d5016; --sage:#5a8a3c; --leaf:#7db05a; --mint:#c8e6c9;
  --cream:#faf7f2; --warm:#f5efe6; --parchment:#ede8df;
  --bark:#3d2b1f; --clay:#8b6347; --terra:#c17f5a; --blush:#f7ede8;
  --white:#ffffff; --text:#1a1a1a; --muted:#7a7060;
  --border:#e5ddd0; --gold:#c9a227;
  --shadow:0 4px 24px rgba(0,0,0,0.08);
  --shadow-h:0 10px 40px rgba(0,0,0,0.14);
}

html, body, [class*="css"], .stApp {
  font-family:'DM Sans',sans-serif !important;
  background:var(--cream) !important;
  color:var(--text) !important;
}
h1,h2,h3,h4 { font-family:'Playfair Display',serif !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"] { visibility:hidden !important; display:none !important; }
[data-testid="stSidebar"] > div:first-child { background:var(--warm) !important; }
.block-container { padding:0 !important; max-width:100% !important; }
section.main > div { padding:0 !important; }

/* ── NAV ── */
.v-nav {
  background:rgba(255,255,255,0.97);
  border-bottom:1px solid var(--border);
  padding:0 2.5rem; display:flex; align-items:center;
  justify-content:space-between; height:68px;
  position:sticky; top:0; z-index:999;
  box-shadow:0 1px 16px rgba(0,0,0,0.06);
  backdrop-filter:blur(10px);
}
.v-logo {
  font-family:'Playfair Display',serif;
  font-size:1.85rem; font-weight:700;
  color:var(--forest); letter-spacing:-0.03em;
}
.v-logo sup {
  font-family:'DM Sans',sans-serif;
  font-size:0.46rem; font-weight:600;
  letter-spacing:0.14em; color:var(--terra);
  text-transform:uppercase; vertical-align:super;
}
.v-nav-links {
  display:flex; gap:0.3rem; list-style:none;
}
.v-nav-link {
  padding:6px 13px; border-radius:8px;
  font-size:0.82rem; font-weight:500;
  color:var(--muted); text-decoration:none;
  cursor:pointer; transition:all 0.18s;
  white-space:nowrap;
}
.v-nav-link:hover { background:var(--warm); color:var(--forest); }
.v-nav-link.active { color:var(--sage); font-weight:600; }
.v-cart-btn {
  background:var(--forest); color:white;
  padding:9px 22px; border-radius:30px;
  font-size:0.82rem; font-weight:600;
  cursor:pointer; border:none;
  transition:all 0.2s; letter-spacing:0.02em;
  font-family:'DM Sans',sans-serif;
}
.v-cart-btn:hover { background:var(--sage); transform:translateY(-1px);
  box-shadow:0 6px 20px rgba(45,80,22,0.3); }

/* ── HERO ── */
.v-hero {
  background:linear-gradient(135deg,#e8f0e2 0%,#f5efe6 45%,#edf4e0 100%);
  padding:5rem 2.5rem 4.5rem; display:flex;
  align-items:center; gap:3rem;
  min-height:500px; position:relative; overflow:hidden;
}
.v-hero::before {
  content:''; position:absolute; right:-80px; top:-80px;
  width:520px; height:520px;
  background:radial-gradient(circle,rgba(125,176,90,0.14) 0%,transparent 70%);
  border-radius:50%; pointer-events:none;
}
.v-hero::after {
  content:''; position:absolute; left:5%; bottom:-60px;
  width:280px; height:280px;
  background:radial-gradient(circle,rgba(193,127,90,0.09) 0%,transparent 70%);
  border-radius:50%; pointer-events:none;
}
.v-eyebrow {
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(255,255,255,0.82); border:1px solid var(--border);
  border-radius:30px; padding:5px 16px;
  font-size:0.74rem; font-weight:600; letter-spacing:0.1em;
  text-transform:uppercase; color:var(--sage); margin-bottom:1.4rem;
}
.v-eyebrow-dot {
  width:6px; height:6px; background:var(--leaf);
  border-radius:50%; display:inline-block;
  animation:dot-pulse 2s infinite;
}
@keyframes dot-pulse {
  0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.8)}
}
.v-hero-title {
  font-family:'Playfair Display',serif;
  font-size:clamp(2.6rem,4.5vw,4rem);
  font-weight:700; color:var(--bark); line-height:1.1; margin:0 0 1.1rem;
}
.v-hero-title em { color:var(--sage); font-style:italic; }
.v-hero-desc {
  font-size:1rem; color:var(--muted);
  font-weight:300; line-height:1.75;
  max-width:500px; margin-bottom:2.2rem;
}
.v-hero-pills { display:flex; gap:0.7rem; flex-wrap:wrap; margin-bottom:2.5rem; }
.v-pill {
  background:rgba(255,255,255,0.85); border:1px solid var(--border);
  border-radius:30px; padding:6px 15px;
  font-size:0.78rem; color:var(--muted);
  box-shadow:0 2px 6px rgba(0,0,0,0.04);
}
.v-hero-stats { display:flex; gap:2rem; flex-wrap:wrap; }
.v-stat { text-align:center; }
.v-stat-num {
  font-family:'Playfair Display',serif;
  font-size:1.5rem; font-weight:700; color:var(--forest);
}
.v-stat-lbl {
  font-size:0.7rem; color:var(--muted);
  letter-spacing:0.07em; text-transform:uppercase;
}
.v-hero-imgs { display:flex; gap:1rem; align-items:flex-end; }
.v-img-card {
  border-radius:20px; overflow:hidden;
  box-shadow:var(--shadow-h); position:relative;
}
.v-img-card img { display:block; object-fit:cover; }
.v-img-card.tall img { width:185px; height:300px; }
.v-img-card.short img { width:160px; height:210px; }
.v-img-overlay {
  position:absolute; bottom:0; left:0; right:0;
  background:linear-gradient(0,rgba(0,0,0,.5),transparent);
  padding:1rem 0.8rem;
}
.v-img-tag {
  background:rgba(255,255,255,.92); border-radius:8px;
  padding:3px 9px; font-size:0.68rem; font-weight:600; color:var(--forest);
}
.v-ai-badge-card {
  background:white; border-radius:16px; padding:16px 18px;
  box-shadow:var(--shadow); text-align:center; min-width:110px;
}
.v-ai-num {
  font-family:'Playfair Display',serif; font-size:1.3rem;
  font-weight:700; color:var(--sage);
}
.v-ai-lbl { font-size:0.68rem; color:var(--muted); letter-spacing:.06em; text-transform:uppercase; margin-top:2px; }
.v-ai-active { font-size:0.66rem; color:#48b048; font-weight:600; margin-top:3px; }

/* ── TRUST STRIP ── */
.v-trust {
  background:var(--forest); color:rgba(255,255,255,.9);
  display:flex; justify-content:center; align-items:center;
  flex-wrap:wrap; padding:13px 2rem; gap:0;
}
.v-trust-item {
  font-size:0.8rem; font-weight:500; letter-spacing:.04em;
  padding:3px 2rem; border-right:1px solid rgba(255,255,255,.2);
}
.v-trust-item:last-child { border-right:none; }

/* ── FEATURES ── */
.v-features {
  background:var(--warm);
  border-top:1px solid var(--border);
  border-bottom:1px solid var(--border);
  padding:2.5rem 2.5rem;
}
.v-features-grid {
  display:grid; grid-template-columns:repeat(5,1fr);
  gap:2rem; max-width:1200px; margin:0 auto;
}
.v-feat { text-align:center; }
.v-feat-icon {
  width:50px; height:50px; border-radius:14px;
  background:white; box-shadow:var(--shadow);
  display:flex; align-items:center; justify-content:center;
  font-size:1.25rem; margin:0 auto 0.75rem;
}
.v-feat-title { font-size:0.86rem; font-weight:600; color:var(--bark); margin-bottom:3px; }
.v-feat-desc { font-size:0.74rem; color:var(--muted); line-height:1.5; }

/* ── SECTION ── */
.v-section { padding:4rem 2.5rem; max-width:1300px; margin:0 auto; }
.v-section-hdr { margin-bottom:2.2rem; }
.v-section-eye {
  font-size:0.73rem; font-weight:700; letter-spacing:.13em;
  text-transform:uppercase; color:var(--terra); margin-bottom:4px;
}
.v-section-title {
  font-family:'Playfair Display',serif;
  font-size:2.1rem; font-weight:700; color:var(--bark); line-height:1.2;
}
.v-section-title em { color:var(--sage); font-style:italic; }
.v-section-sub { font-size:0.85rem; color:var(--muted); margin-top:5px; font-weight:300; }

/* ── PRODUCT CARD ── */
.v-pcard {
  background:white; border-radius:18px;
  overflow:hidden; box-shadow:0 2px 14px rgba(0,0,0,.06);
  transition:all 0.28s cubic-bezier(.25,.46,.45,.94);
  height:100%; position:relative;
}
.v-pcard:hover { transform:translateY(-5px); box-shadow:var(--shadow-h); }
.v-pcard-img { width:100%; aspect-ratio:4/3; object-fit:cover; display:block;
  transition:transform .5s ease; }
.v-pcard:hover .v-pcard-img { transform:scale(1.05); }
.v-badge {
  position:absolute; top:10px; left:10px;
  font-size:0.62rem; font-weight:700; letter-spacing:.06em;
  text-transform:uppercase; padding:3px 9px; border-radius:20px;
}
.v-badge-main { background:rgba(255,255,255,.93); color:var(--forest); }
.v-badge-eco { background:var(--mint); color:var(--forest); }
.v-badge-new { background:var(--blush); color:var(--terra); }
.v-badge-sale { background:#fff0eb; color:#c0450a; }
.v-badge-rare { background:#f3eaff; color:#6b21a8; }
.v-pcard-body { padding:1rem 1.1rem 1.2rem; }
.v-pcard-name {
  font-family:'Playfair Display',serif;
  font-size:1.05rem; font-weight:600; color:var(--bark);
  line-height:1.3; margin-bottom:4px;
}
.v-pcard-desc { font-size:0.76rem; color:var(--muted); line-height:1.5; margin-bottom:9px; }
.v-pcard-price { font-size:1.1rem; font-weight:700; color:var(--forest); }
.v-pcard-mrp { font-size:0.76rem; color:#bbb; text-decoration:line-through; margin-left:6px; }
.v-pcard-disc { font-size:0.7rem; color:#c0450a; font-weight:700; margin-left:4px; }

/* ── PROMO BANNER ── */
.v-promo {
  background:linear-gradient(135deg,#f7ede8,#f0ebe0,#e8f0e2);
  border-radius:20px; padding:2.5rem 3rem;
  display:flex; align-items:center; justify-content:space-between;
  gap:2rem; flex-wrap:wrap; border:1px solid var(--border);
  position:relative; overflow:hidden;
  margin:1rem 2.5rem;
}
.v-promo-title {
  font-family:'Playfair Display',serif;
  font-size:1.6rem; font-weight:700; color:var(--bark);
}
.v-promo-sub { font-size:0.85rem; color:var(--muted); }
.v-promo-code {
  background:white; border:2px dashed var(--terra);
  border-radius:12px; padding:10px 22px;
  font-size:1.1rem; font-weight:700; color:var(--terra);
  letter-spacing:.12em;
}

/* ── AI SHOWCASE ── */
.v-ai-showcase {
  background:linear-gradient(135deg,var(--forest) 0%,#1d3a0a 100%);
  padding:5rem 2.5rem; color:white; position:relative; overflow:hidden;
}
.v-ai-showcase::before {
  content:''; position:absolute; right:-100px; top:-100px;
  width:500px; height:500px;
  background:radial-gradient(circle,rgba(125,176,90,.14) 0%,transparent 65%);
  border-radius:50%; pointer-events:none;
}
.v-ai-badge {
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.2);
  border-radius:30px; padding:5px 16px;
  font-size:0.72rem; font-weight:600; letter-spacing:.1em;
  text-transform:uppercase; color:rgba(255,255,255,.85); margin-bottom:1.2rem;
}
.v-ai-title {
  font-family:'Playfair Display',serif;
  font-size:2.4rem; font-weight:700; line-height:1.2; margin-bottom:1rem;
}
.v-ai-desc {
  font-size:.95rem; color:rgba(255,255,255,.75);
  line-height:1.75; font-weight:300; max-width:440px; margin-bottom:2rem;
}
.v-ai-feature {
  display:flex; align-items:flex-start; gap:12px;
  padding:13px 15px;
  background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.12);
  border-radius:14px; margin-bottom:10px;
}
.v-ai-feat-icon {
  width:36px; height:36px; border-radius:10px;
  background:rgba(255,255,255,.15); flex-shrink:0;
  display:flex; align-items:center; justify-content:center; font-size:1rem;
}
.v-ai-feat-title { font-size:.87rem; font-weight:600; margin-bottom:3px; }
.v-ai-feat-desc { font-size:.76rem; color:rgba(255,255,255,.65); line-height:1.5; }

/* ── PLAN CARDS ── */
.v-plan {
  background:white; border-radius:18px; padding:2rem 1.8rem;
  border:2px solid var(--border); transition:all .25s;
  position:relative; height:100%;
}
.v-plan:hover { border-color:var(--sage); box-shadow:var(--shadow); }
.v-plan.featured { border-color:var(--forest); }
.v-plan-badge {
  position:absolute; top:-12px; left:50%; transform:translateX(-50%);
  background:var(--forest); color:white;
  font-size:.66rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  padding:4px 14px; border-radius:20px;
}
.v-plan-name {
  font-family:'Playfair Display',serif;
  font-size:1.25rem; font-weight:700; color:var(--bark); margin-bottom:4px;
}
.v-plan-price { font-size:2rem; font-weight:700; color:var(--forest); margin:0.5rem 0; }
.v-plan-price span { font-size:.88rem; font-weight:400; color:var(--muted); }
.v-plan-desc { font-size:.82rem; color:var(--muted); margin-bottom:1.2rem; line-height:1.5; }
.v-plan-feat { font-size:.8rem; color:var(--text); padding:5px 0; border-bottom:1px solid var(--border); }
.v-plan-feat:last-of-type { border-bottom:none; }

/* ── TESTIMONIALS ── */
.v-testi {
  background:white; border-radius:18px;
  padding:1.8rem; box-shadow:var(--shadow);
}
.v-testi-stars { color:var(--gold); letter-spacing:2px; margin-bottom:.8rem; }
.v-testi-text {
  font-size:.87rem; color:var(--text); line-height:1.7;
  margin-bottom:1rem; font-style:italic;
  font-family:'Playfair Display',serif;
}
.v-testi-name { font-size:.84rem; font-weight:600; color:var(--bark); }
.v-testi-loc { font-size:.72rem; color:var(--muted); }

/* ── BLOG CARD ── */
.v-blog {
  background:white; border-radius:18px; overflow:hidden;
  box-shadow:var(--shadow); transition:all .25s; cursor:pointer;
}
.v-blog:hover { transform:translateY(-4px); box-shadow:var(--shadow-h); }
.v-blog img { width:100%; height:175px; object-fit:cover; display:block; }
.v-blog-body { padding:1.2rem 1.3rem 1.4rem; }
.v-blog-tag {
  font-size:.67rem; font-weight:700; letter-spacing:.08em;
  text-transform:uppercase; color:var(--terra); margin-bottom:6px;
}
.v-blog-title {
  font-family:'Playfair Display',serif;
  font-size:1rem; font-weight:600; color:var(--bark); line-height:1.4; margin-bottom:7px;
}
.v-blog-meta { font-size:.71rem; color:var(--muted); }

/* ── CHAT PANEL ── */
.v-chat-header {
  background:linear-gradient(135deg,var(--forest),#3d7020);
  padding:14px 18px; border-radius:16px 16px 0 0;
  display:flex; align-items:center; gap:12px;
}
.v-chat-avatar {
  width:38px; height:38px; border-radius:50%;
  background:rgba(255,255,255,.22);
  display:flex; align-items:center; justify-content:center; font-size:1.1rem;
}
.v-chat-name { font-size:.9rem; font-weight:600; color:white; }
.v-chat-status { font-size:.7rem; color:rgba(255,255,255,.75); }
.v-chat-status::before { content:'● '; color:#90ee90; }

/* Chat messages */
.v-msg-bot {
  background:white; border:1px solid var(--border);
  border-radius:14px 14px 14px 3px; padding:10px 13px;
  font-size:.83rem; color:var(--text); line-height:1.55;
  max-width:85%; box-shadow:0 1px 5px rgba(0,0,0,.05);
  margin-bottom:4px;
}
.v-msg-user {
  background:var(--forest); color:white;
  border-radius:14px 14px 3px 14px; padding:10px 13px;
  font-size:.83rem; line-height:1.55;
  max-width:85%; align-self:flex-end;
  box-shadow:0 2px 10px rgba(45,80,22,.2);
  margin-bottom:4px; margin-left:auto;
}
.v-diag-box {
  background:linear-gradient(135deg,#e8f5e8,#f7ece9);
  border:1px solid #cce0cc; border-radius:13px;
  padding:12px 14px; font-size:.82rem;
  color:var(--bark); line-height:1.6; margin-bottom:5px;
}
.v-diag-title { font-weight:700; font-size:.9rem; color:var(--forest); margin-bottom:5px; }
.v-chat-prod {
  background:white; border:1px solid var(--border);
  border-radius:11px; padding:8px 10px;
  display:flex; gap:9px; align-items:center;
  margin-bottom:5px; box-shadow:0 1px 4px rgba(0,0,0,.04);
}
.v-chat-prod-img { width:44px; height:44px; border-radius:7px; object-fit:cover; }
.v-chat-prod-name { font-size:.81rem; font-weight:600; color:var(--bark); }
.v-chat-prod-price { font-size:.72rem; color:var(--sage); font-weight:700; }
.v-sched {
  background:white; border:1px solid var(--border);
  border-radius:12px; padding:12px 14px; font-size:.79rem;
}
.v-sched-day {
  display:flex; gap:8px; align-items:center;
  padding:5px 0; border-bottom:1px solid var(--border);
}
.v-sched-day:last-child { border-bottom:none; }
.v-sched-name { font-weight:600; color:var(--forest); min-width:75px; }

/* ── TYPING INDICATOR ── */
.v-typing {
  display:inline-flex; align-items:center; gap:4px;
  padding:10px 14px; background:white;
  border:1px solid var(--border); border-radius:14px 14px 14px 3px;
}
.v-dot {
  width:6px; height:6px; border-radius:50%; background:var(--muted);
  animation:typeBounce 1.2s ease-in-out infinite;
}
.v-dot:nth-child(2){animation-delay:.2s}
.v-dot:nth-child(3){animation-delay:.4s}
@keyframes typeBounce {
  0%,100%{transform:translateY(0);opacity:.4}
  50%{transform:translateY(-5px);opacity:1}
}

/* ── FOOTER ── */
.v-footer {
  background:var(--bark); color:rgba(255,255,255,.7);
  padding:3.5rem 2.5rem 2rem;
}
.v-footer-logo {
  font-family:'Playfair Display',serif;
  font-size:1.8rem; color:white; margin-bottom:.7rem;
}
.v-footer-desc { font-size:.82rem; line-height:1.75; margin-bottom:1.5rem; }
.v-footer-col-title {
  font-size:.76rem; font-weight:700; letter-spacing:.1em;
  text-transform:uppercase; color:rgba(255,255,255,.9); margin-bottom:.8rem;
}
.v-footer-link {
  font-size:.8rem; color:rgba(255,255,255,.5); display:block;
  margin-bottom:.45rem; text-decoration:none; transition:color .15s;
}
.v-footer-link:hover { color:white; }
.v-footer-bottom {
  padding-top:1.5rem; margin-top:2.5rem;
  border-top:1px solid rgba(255,255,255,.1);
  font-size:.76rem; color:rgba(255,255,255,.35);
  display:flex; justify-content:space-between; flex-wrap:wrap; gap:1rem;
}

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
  font-family:'DM Sans',sans-serif !important;
  border-radius:10px !important;
  font-weight:600 !important;
  transition:all .2s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; }
.stTextInput > div > input,
.stTextArea > div > textarea {
  border-radius:10px !important;
  font-family:'DM Sans',sans-serif !important;
  border:1.5px solid var(--border) !important;
  background:var(--cream) !important;
}
.stTextInput > div > input:focus,
.stTextArea > div > textarea:focus {
  border-color:var(--sage) !important;
  box-shadow:0 0 0 3px rgba(90,138,60,.12) !important;
}
div[data-testid="stExpander"] {
  border:1px solid var(--border) !important;
  border-radius:14px !important;
  background:white !important;
}
.stSelectbox > div > div { border-radius:10px !important; }
.stTab [data-baseweb="tab"] {
  font-family:'DM Sans',sans-serif !important;
  font-weight:600 !important;
}
.stTab [data-baseweb="tab-highlight"] { background:var(--forest) !important; }
div[data-testid="metric-container"] {
  background:white; border-radius:14px;
  border:1px solid var(--border);
  padding:1rem; box-shadow:var(--shadow);
}
[data-testid="stMetricValue"] { color:var(--forest) !important; font-family:'Playfair Display',serif !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# PRODUCT DATABASE
# ──────────────────────────────────────────────────────────────
PLANTS = [
    {"id":"PL01","name":"Monstera Deliciosa","price":549,"mrp":799,
     "desc":"The iconic Swiss cheese plant. Perfect for bright, indirect light.",
     "img":"https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400&q=80",
     "badge":"Bestseller","tag":"eco","cat":"air"},
    {"id":"PL02","name":"Peace Lily","price":349,"mrp":499,
     "desc":"Elegant white blooms, purifies air and thrives in low light.",
     "img":"https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400&q=80",
     "badge":"Low Light Hero","tag":"new","cat":"air"},
    {"id":"PL03","name":"Snake Plant","price":299,"mrp":449,
     "desc":"Nearly indestructible. Removes toxins and looks stunning.",
     "img":"https://images.unsplash.com/photo-1616961808965-7d8d7c9a1e30?w=400&q=80",
     "badge":"Easy Care","tag":"eco","cat":"easy"},
    {"id":"PL04","name":"Fiddle Leaf Fig","price":899,"mrp":1299,
     "desc":"Architectural beauty with large, waxy leaves. A designer's favourite.",
     "img":"https://images.unsplash.com/photo-1520412099551-62b6bafeb5bb?w=400&q=80",
     "badge":"Trending","tag":"rare","cat":"rare"},
    {"id":"PL05","name":"Pothos Golden","price":199,"mrp":299,
     "desc":"Fast-growing trailing vine. Ideal for shelves and hanging baskets.",
     "img":"https://images.unsplash.com/photo-1622398925373-3f91b1e275f5?w=400&q=80",
     "badge":"Budget Pick","tag":"eco","cat":"easy"},
    {"id":"PL06","name":"ZZ Plant","price":449,"mrp":649,
     "desc":"Glossy, waxy leaves that tolerate neglect. Zero drama, all style.",
     "img":"https://images.unsplash.com/photo-1632207691143-643e2a9a9361?w=400&q=80",
     "badge":"Drought Tolerant","tag":"eco","cat":"easy"},
    {"id":"PL07","name":"Bird of Paradise","price":1199,"mrp":1699,
     "desc":"Tropical showstopper with banana-like foliage.",
     "img":"https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=400&q=80",
     "badge":"Statement","tag":"rare","cat":"rare"},
    {"id":"PL08","name":"Aloe Vera","price":179,"mrp":249,
     "desc":"Medicinal succulent. Keep on your windowsill for instant skincare.",
     "img":"https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&q=80",
     "badge":"Medicinal","tag":"eco","cat":"succulent"},
    {"id":"PL09","name":"Anthurium Red","price":649,"mrp":899,
     "desc":"Glossy red spathes that bloom nearly year-round.",
     "img":"https://images.unsplash.com/photo-1520302630591-fd1f1b95b4b7?w=400&q=80",
     "badge":"Flowering","tag":"new","cat":"flowering"},
    {"id":"PL10","name":"Chinese Money Plant","price":399,"mrp":549,
     "desc":"Round pancake leaves on red stems. Brings good luck.",
     "img":"https://images.unsplash.com/photo-1615233500064-bf92e853e847?w=400&q=80",
     "badge":"Lucky Plant","tag":"new","cat":"rare"},
    {"id":"PL11","name":"String of Pearls","price":349,"mrp":499,
     "desc":"Cascading beads of green — one of nature's most dramatic succulents.",
     "img":"https://images.unsplash.com/photo-1597055181300-1f18e27f55f6?w=400&q=80",
     "badge":"Trailing","tag":"rare","cat":"succulent"},
    {"id":"PL12","name":"Rubber Plant","price":499,"mrp":749,
     "desc":"Deep burgundy leaves add drama. Excellent air purifier.",
     "img":"https://images.unsplash.com/photo-1631125915902-d5e28543d7b1?w=400&q=80",
     "badge":"Air Purifier","tag":"new","cat":"air"},
]

PLANT_CARE = [
    {"id":"PC01","name":"NPK Organic Fertilizer 500g","price":249,"mrp":349,
     "desc":"Balanced 10-10-10 formula for all indoor plants. Slow-release granules.",
     "img":"https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80",
     "badge":"Bestseller","tag":"eco"},
    {"id":"PC02","name":"Neem Oil Spray 250ml","price":179,"mrp":249,
     "desc":"Cold-pressed neem. Controls aphids, mites and fungal issues organically.",
     "img":"https://images.unsplash.com/photo-1585435557343-3b092031a831?w=400&q=80",
     "badge":"Organic","tag":"eco"},
    {"id":"PC03","name":"Moisture Retention Granules","price":199,"mrp":279,
     "desc":"Hydrogel granules for pots — reduces watering frequency by 50%.",
     "img":"https://images.unsplash.com/photo-1447708440306-ec9a5d88d310?w=400&q=80",
     "badge":"Water Saver","tag":"new"},
    {"id":"PC04","name":"Liquid Seaweed Extract","price":299,"mrp":399,
     "desc":"Micronutrient booster. Spray on leaves for rapid green-up within days.",
     "img":"https://images.unsplash.com/photo-1599598425947-5202edd56fdb?w=400&q=80",
     "badge":"Micronutrients","tag":"eco"},
    {"id":"PC05","name":"Vermicompost Premium 1kg","price":149,"mrp":199,
     "desc":"Premium worm castings. Improves soil structure and beneficial microbiome.",
     "img":"https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=400&q=80",
     "badge":"Premium Compost","tag":"eco"},
    {"id":"PC06","name":"Systemic Fungicide 100g","price":219,"mrp":299,
     "desc":"Controls powdery mildew, root rot and leaf blight effectively.",
     "img":"https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=400&q=80",
     "badge":"Plant Saver","tag":"sale"},
    {"id":"PC07","name":"Pruning Shears Pro","price":649,"mrp":899,
     "desc":"Stainless SK5 blades, ergonomic grip. Clean precision cuts every time.",
     "img":"https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80",
     "badge":"Pro Tool","tag":"new"},
    {"id":"PC08","name":"Soil pH & Moisture Meter","price":499,"mrp":699,
     "desc":"3-in-1 digital tester: soil pH, moisture level, and light intensity.",
     "img":"https://images.unsplash.com/photo-1585435557343-3b092031a831?w=400&q=80",
     "badge":"Smart Garden","tag":"new"},
]

POTS = [
    {"id":"PT01","name":"Terracotta Pot Set (3)","price":449,"mrp":649,
     "desc":"Hand-thrown terracotta with drainage holes. Set of 3 graduated sizes.",
     "img":"https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&q=80",
     "badge":"Classic","tag":"eco"},
    {"id":"PT02","name":"Ceramic Glazed Planter","price":699,"mrp":999,
     "desc":"Sage-green glaze, drainage tray included. 8 inch diameter.",
     "img":"https://images.unsplash.com/photo-1509423350716-97f9360b4e09?w=400&q=80",
     "badge":"Premium","tag":"new"},
    {"id":"PT03","name":"Hanging Macramé Planter","price":349,"mrp":499,
     "desc":"Handwoven cotton macramé. Holds 6-inch pot beautifully.",
     "img":"https://images.unsplash.com/photo-1463699527455-ddf00a24d09e?w=400&q=80",
     "badge":"Boho","tag":"new"},
    {"id":"PT04","name":"Self-Watering Smart Pot","price":799,"mrp":1099,
     "desc":"Built-in reservoir with water level indicator. Never over-water again.",
     "img":"https://images.unsplash.com/photo-1459156212016-c812468e2115?w=400&q=80",
     "badge":"Smart","tag":"new"},
    {"id":"PT05","name":"Cement Minimalist Planter","price":549,"mrp":799,
     "desc":"Raw cast cement with matte finish. Industrial chic for modern interiors.",
     "img":"https://images.unsplash.com/photo-1444930694458-01babf71870c?w=400&q=80",
     "badge":"Minimalist","tag":"eco"},
    {"id":"PT06","name":"Wicker Basket Planter","price":399,"mrp":549,
     "desc":"Natural rattan weave with plastic liner. Earthy and warm aesthetic.",
     "img":"https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&q=80",
     "badge":"Natural","tag":"eco"},
]

SEEDS = [
    {"id":"SD01","name":"Cherry Tomato Seeds","price":79,"mrp":119,
     "desc":"Prolific indeterminate variety. Harvest in 65 days. 30 seeds included.",
     "img":"https://images.unsplash.com/photo-1592921870789-04563d55041c?w=400&q=80",
     "badge":"Grow Your Food","tag":"eco"},
    {"id":"SD02","name":"Basil Herb Mix","price":59,"mrp":89,
     "desc":"5 basil varieties: Genovese, Thai, Purple, Lemon, Greek. 200 seeds.",
     "img":"https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=400&q=80",
     "badge":"Herb Garden","tag":"new"},
    {"id":"SD03","name":"Lavender Seeds","price":89,"mrp":129,
     "desc":"True English lavender. Fragrant, drought-tolerant perennial. 50 seeds.",
     "img":"https://images.unsplash.com/photo-1566438480900-0609be27a4be?w=400&q=80",
     "badge":"Fragrant","tag":"new"},
    {"id":"SD04","name":"Marigold Mix Seeds","price":49,"mrp":75,
     "desc":"6 varieties. Natural pest deterrent and beautiful border plant.",
     "img":"https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&q=80",
     "badge":"Pest Guard","tag":"eco"},
]

ALL_PRODUCTS = PLANTS + PLANT_CARE + POTS + SEEDS

# ──────────────────────────────────────────────────────────────
# AI SYSTEM PROMPT
# ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Verdana AI, an expert horticulturist and plant care advisor for the Verdana premium plant eCommerce platform. You are friendly, professional, and highly knowledgeable about plant health, nutrition, and care.

PRODUCT INVENTORY (only recommend these exact products with these prices):

PLANTS:
- Monstera Deliciosa ₹549
- Peace Lily ₹349
- Snake Plant ₹299
- Fiddle Leaf Fig ₹899
- Pothos Golden ₹199
- ZZ Plant ₹449
- Bird of Paradise ₹1199
- Aloe Vera ₹179
- Anthurium Red ₹649
- Chinese Money Plant ₹399
- String of Pearls ₹349
- Rubber Plant ₹499

FERTILIZERS & CARE:
- NPK Organic Fertilizer 500g ₹249
- Neem Oil Spray 250ml ₹179
- Moisture Retention Granules ₹199
- Liquid Seaweed Extract ₹299
- Vermicompost Premium 1kg ₹149
- Systemic Fungicide 100g ₹219

TOOLS:
- Pruning Shears Pro ₹649
- Soil pH & Moisture Meter ₹499

POTS:
- Terracotta Pot Set ₹449
- Ceramic Glazed Planter ₹699
- Hanging Macramé Planter ₹349
- Self-Watering Smart Pot ₹799
- Cement Minimalist Planter ₹549
- Wicker Basket Planter ₹399

SEEDS:
- Cherry Tomato Seeds ₹79
- Basil Herb Mix ₹59
- Lavender Seeds ₹89
- Marigold Mix Seeds ₹49

YOUR ROLES:
1. DIAGNOSE plant problems (yellowing, wilting, pests, root rot, overwatering, nutrient deficiency, fungal issues) from descriptions or uploaded images. Be specific about the condition, cause, and severity.
2. RECOMMEND specific products from the inventory above. Always include prices. Suggest 2-4 products per issue.
3. CREATE personalised weekly care schedules with day-by-day plans (watering, fertilising, pruning, pest control).
4. SUGGEST the right plants based on space, light, budget, or purpose (air purifier, beginner-friendly, gifts, etc.).
5. ACT as a sales advisor — guide users to relevant products naturally within expert advice.

RESPONSE FORMAT:
- Be concise but thorough. Use **bold** for key terms and product names.
- For diagnoses: state condition, cause, severity, then treatment with product recommendations.
- For schedules: list day-by-day in a clear format.
- For plant suggestions: describe 2-3 options with care difficulty and price.
- Always end with an actionable recommendation.

Use ₹ symbol for all prices. Be warm, expert, and helpful."""

# ──────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────
defaults = {
    "cart": {},
    "active_tab": "🏠 Home",
    "chat_open": False,
    "chat_messages": [],     # list of {"role": "user"|"assistant", "content": str|list}
    "chat_history_display": [],  # for rendering in UI
    "api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    "wishlist": set(),
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────
def get_product(pid):
    return next((p for p in ALL_PRODUCTS if p["id"] == pid), None)

def add_to_cart(pid):
    p = get_product(pid)
    if not p:
        return
    if pid in st.session_state.cart:
        st.session_state.cart[pid]["qty"] += 1
    else:
        st.session_state.cart[pid] = {"product": p, "qty": 1}
    st.toast(f"✅ {p['name']} added to cart!", icon="🌿")

def cart_count():
    return sum(v["qty"] for v in st.session_state.cart.values())

def cart_total():
    return sum(v["product"]["price"] * v["qty"] for v in st.session_state.cart.values())

TAG_CLASS = {"eco": "v-badge-eco", "new": "v-badge-new", "sale": "v-badge-sale", "rare": "v-badge-rare"}
TAG_LABEL = {"eco": "Eco", "new": "New", "sale": "Sale", "rare": "Rare"}

def product_card_html(p):
    disc = round((1 - p["price"] / p["mrp"]) * 100)
    tag = p.get("tag", "")
    tag_html = (f'<span class="v-badge {TAG_CLASS.get(tag,"")}" '
                f'style="position:absolute;top:10px;right:10px;">'
                f'{TAG_LABEL.get(tag,"")}</span>') if tag in TAG_CLASS else ""
    return f"""
    <div class="v-pcard">
      <div style="position:relative;overflow:hidden;">
        <img src="{p['img']}" class="v-pcard-img" onerror="this.style.background='#e8f0e2'" alt="{p['name']}"/>
        <div class="v-badge v-badge-main" style="position:absolute;top:10px;left:10px;">{p['badge']}</div>
        {tag_html}
      </div>
      <div class="v-pcard-body">
        <div class="v-pcard-name">{p['name']}</div>
        <div class="v-pcard-desc">{p['desc']}</div>
        <div>
          <span class="v-pcard-price">₹{p['price']:,}</span>
          <span class="v-pcard-mrp">₹{p['mrp']:,}</span>
          <span class="v-pcard-disc">{disc}% off</span>
        </div>
      </div>
    </div>"""

def render_product_grid(products, cols=4):
    rows = [products[i:i+cols] for i in range(0, len(products), cols)]
    for row in rows:
        grid_cols = st.columns(len(row))
        for col, prod in zip(grid_cols, row):
            with col:
                st.markdown(product_card_html(prod), unsafe_allow_html=True)
                b1, b2 = st.columns([3, 1])
                with b1:
                    if st.button("Add to Cart", key=f"cart_{prod['id']}", use_container_width=True):
                        add_to_cart(prod["id"])
                        st.rerun()
                with b2:
                    wl = "♥" if prod["id"] in st.session_state.wishlist else "♡"
                    if st.button(wl, key=f"wl_{prod['id']}", use_container_width=True):
                        if prod["id"] in st.session_state.wishlist:
                            st.session_state.wishlist.discard(prod["id"])
                        else:
                            st.session_state.wishlist.add(prod["id"])
                        st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

def call_claude(messages_for_api, image_b64=None, image_type="image/jpeg"):
    """Call Claude API. Returns reply string."""
    if not st.session_state.api_key:
        return "Please enter your Anthropic API key in the sidebar to use AI features."
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=messages_for_api,
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "Invalid API key. Please check your Anthropic API key in the sidebar."
    except anthropic.RateLimitError:
        return "Rate limit reached. Please wait a moment and try again."
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def get_product_suggestions(reply_text):
    """Find products mentioned in AI reply."""
    mentioned = []
    for p in ALL_PRODUCTS:
        # match on name keywords
        name_words = [w for w in p["name"].lower().split() if len(w) > 3]
        if any(w in reply_text.lower() for w in name_words):
            mentioned.append(p)
    # deduplicate
    seen = set()
    unique = []
    for p in mentioned:
        if p["id"] not in seen:
            seen.add(p["id"])
            unique.append(p)
    return unique[:4]

# ──────────────────────────────────────────────────────────────
# TOP NAV
# ──────────────────────────────────────────────────────────────
cart_n = cart_count()
st.markdown(f"""
<div class="v-nav">
  <div class="v-logo">Verdana<sup>®</sup></div>
  <div style="display:flex;gap:0.3rem;flex-wrap:wrap;">
    <span class="v-nav-link">Indoor Plants</span>
    <span class="v-nav-link">Outdoor Plants</span>
    <span class="v-nav-link">Pots & Planters</span>
    <span class="v-nav-link">Fertilizers</span>
    <span class="v-nav-link">AI Plant Doctor</span>
    <span class="v-nav-link">Subscriptions</span>
  </div>
  <button class="v-cart-btn">🛒 Cart ({cart_n})</button>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SIDEBAR — API KEY + CART + WISHLIST
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_input = st.text_input(
        "Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com"
    )
    if api_input != st.session_state.api_key:
        st.session_state.api_key = api_input
    if st.session_state.api_key:
        st.success("API Key set ✓")
    else:
        st.warning("Enter API key to use AI Doctor")

    st.divider()

    # Cart sidebar
    st.markdown("### 🛒 Your Cart")
    if not st.session_state.cart:
        st.caption("Your cart is empty.")
    else:
        total = 0
        for pid, item in list(st.session_state.cart.items()):
            p = item["product"]
            q = item["qty"]
            line = p["price"] * q
            total += line
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.caption(f"**{p['name']}**")
                st.caption(f"₹{p['price']:,} × {q} = ₹{line:,}")
            with c2:
                if st.button("＋", key=f"sideinc_{pid}"):
                    st.session_state.cart[pid]["qty"] += 1
                    st.rerun()
            with c3:
                if st.button("−", key=f"sidedec_{pid}"):
                    st.session_state.cart[pid]["qty"] -= 1
                    if st.session_state.cart[pid]["qty"] <= 0:
                        del st.session_state.cart[pid]
                    st.rerun()

        delivery = 0 if total >= 599 else 79
        st.divider()
        st.markdown(f"**Subtotal:** ₹{total:,}")
        st.markdown(f"**Delivery:** {'FREE' if delivery == 0 else f'₹{delivery}'}")
        st.markdown(f"### Total: ₹{total + delivery:,}")
        if st.button("Proceed to Checkout", use_container_width=True, type="primary"):
            st.success("Order placed! (Demo mode)")
            st.session_state.cart = {}
            st.rerun()
        if st.button("Clear Cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

    st.divider()

    # Wishlist
    st.markdown("### ♥ Wishlist")
    if not st.session_state.wishlist:
        st.caption("No saved items.")
    else:
        for pid in st.session_state.wishlist:
            p = get_product(pid)
            if p:
                wc1, wc2 = st.columns([3, 1])
                with wc1:
                    st.caption(f"**{p['name']}** — ₹{p['price']:,}")
                with wc2:
                    if st.button("Cart", key=f"wladd_{pid}"):
                        add_to_cart(pid)
                        st.rerun()

# ──────────────────────────────────────────────────────────────
# MAIN TABS
# ──────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏠 Home",
    "🌿 Plants",
    "🧪 Plant Care",
    "🪴 Pots",
    "🌾 Seeds",
    "🤖 AI Plant Doctor",
    "📦 Subscriptions",
    "📖 Blog",
    "👤 My Account",
])

# ══════════════════════════════════════════════════════════════
# TAB 0 — HOME
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    # Hero
    st.markdown("""
    <div class="v-hero">
      <div style="flex:1.2;min-width:300px;position:relative;z-index:1;">
        <div class="v-eyebrow">
          <span class="v-eyebrow-dot"></span>
          AI-Powered Plant Care Platform
        </div>
        <h1 class="v-hero-title">
          Diagnose, <em>Nurture</em>,<br>& Let Plants Thrive
        </h1>
        <p class="v-hero-desc">
          Premium plants, expert care products, and an AI Plant Doctor that diagnoses
          your plant's health — prescribing exact treatments from our store.
        </p>
        <div class="v-hero-pills">
          <span class="v-pill">🌿 1,200+ Varieties</span>
          <span class="v-pill">🚚 Pan-India Delivery</span>
          <span class="v-pill">⭐ 4.9 Rated</span>
          <span class="v-pill">🤖 AI Diagnosis</span>
        </div>
        <div class="v-hero-stats">
          <div class="v-stat"><div class="v-stat-num">1,200+</div><div class="v-stat-lbl">Plant Varieties</div></div>
          <div class="v-stat"><div class="v-stat-num">50k+</div><div class="v-stat-lbl">Happy Gardeners</div></div>
          <div class="v-stat"><div class="v-stat-num">4.9★</div><div class="v-stat-lbl">Avg. Rating</div></div>
        </div>
      </div>
      <div class="v-hero-imgs" style="position:relative;z-index:1;">
        <div class="v-img-card tall">
          <img src="https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400&q=85" alt="Monstera"/>
          <div class="v-img-overlay"><span class="v-img-tag">Monstera Deliciosa</span></div>
        </div>
        <div style="display:flex;flex-direction:column;gap:1rem;">
          <div class="v-img-card short">
            <img src="https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=300&q=85" alt="Peace Lily"/>
            <div class="v-img-overlay"><span class="v-img-tag">Peace Lily</span></div>
          </div>
          <div class="v-ai-badge-card">
            <div class="v-ai-num">AI</div>
            <div class="v-ai-lbl">Plant Doctor</div>
            <div class="v-ai-active">● Active Now</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Trust Strip
    st.markdown("""
    <div class="v-trust">
      <div class="v-trust-item">Free Delivery above ₹599</div>
      <div class="v-trust-item">100% Healthy Guarantee</div>
      <div class="v-trust-item">30-Day Return Policy</div>
      <div class="v-trust-item">Expert AI Plant Doctor</div>
      <div class="v-trust-item">Eco-Friendly Packaging</div>
    </div>
    """, unsafe_allow_html=True)

    # Features
    st.markdown("""
    <div class="v-features">
      <div class="v-features-grid">
        <div class="v-feat"><div class="v-feat-icon">🌿</div>
          <div class="v-feat-title">Curated Plants</div>
          <div class="v-feat-desc">Expert-selected, nursery-fresh varieties shipped pan-India</div>
        </div>
        <div class="v-feat"><div class="v-feat-icon">🤖</div>
          <div class="v-feat-title">AI Plant Doctor</div>
          <div class="v-feat-desc">Upload a photo for instant diagnosis and treatment plan</div>
        </div>
        <div class="v-feat"><div class="v-feat-icon">📅</div>
          <div class="v-feat-title">Smart Scheduler</div>
          <div class="v-feat-desc">Personalised watering, feeding and care reminders</div>
        </div>
        <div class="v-feat"><div class="v-feat-icon">📦</div>
          <div class="v-feat-title">Monthly Kits</div>
          <div class="v-feat-desc">Seasonal care subscriptions delivered to your door</div>
        </div>
        <div class="v-feat"><div class="v-feat-icon">🛡️</div>
          <div class="v-feat-title">Secure Checkout</div>
          <div class="v-feat-desc">Trusted by 50,000+ plant lovers across India</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Bestsellers section
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Bestsellers</div>
      <div class="v-section-title">Most <em>Loved</em> Plants</div>
      <div class="v-section-sub">Our top 8 plants that plant parents can't get enough of.</div>
    </div>
    """, unsafe_allow_html=True)
    render_product_grid(PLANTS[:8], cols=4)
    st.markdown('</div>', unsafe_allow_html=True)

    # Promo Banner
    st.markdown("""
    <div class="v-promo">
      <div>
        <div class="v-promo-title">First Order Special</div>
        <div class="v-promo-sub">Get 20% off your first purchase — valid on all categories</div>
      </div>
      <div class="v-promo-code">VERDANA20</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # AI Showcase
    st.markdown("""
    <div class="v-ai-showcase">
      <div style="display:flex;align-items:center;gap:3rem;flex-wrap:wrap;max-width:1200px;margin:0 auto;position:relative;z-index:1;">
        <div style="flex:1;min-width:280px;">
          <div class="v-ai-badge">AI · Powered by Claude</div>
          <h2 class="v-ai-title">Meet Your Personal<br><em style="font-style:italic;color:#a0d070;">Plant Doctor</em></h2>
          <p class="v-ai-desc">
            Upload a photo of your struggling plant and our AI instantly diagnoses the problem —
            nutrient deficiency, pests, overwatering, root rot — and prescribes an exact
            treatment plan with products from our store.
          </p>
          <div class="v-ai-feature">
            <div class="v-ai-feat-icon">📷</div>
            <div>
              <div class="v-ai-feat-title">Photo Diagnosis</div>
              <div class="v-ai-feat-desc">AI analyses leaf colour, texture, and structure to identify 20+ plant conditions</div>
            </div>
          </div>
          <div class="v-ai-feature">
            <div class="v-ai-feat-icon">🧪</div>
            <div>
              <div class="v-ai-feat-title">Smart Recommendations</div>
              <div class="v-ai-feat-desc">Only suggests products available in our store — specific and actionable</div>
            </div>
          </div>
          <div class="v-ai-feature">
            <div class="v-ai-feat-icon">📅</div>
            <div>
              <div class="v-ai-feat-title">Weekly Care Scheduler</div>
              <div class="v-ai-feat-desc">Auto-generates a watering, fertilising, and treatment calendar</div>
            </div>
          </div>
        </div>
        <div style="flex:1;min-width:280px;display:flex;justify-content:center;">
          <div style="background:rgba(255,255,255,.1);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.18);border-radius:24px;padding:1.5rem;width:300px;box-shadow:0 20px 60px rgba(0,0,0,.2);">
            <div style="display:flex;align-items:center;gap:10px;padding-bottom:1rem;border-bottom:1px solid rgba(255,255,255,.15);margin-bottom:1rem;">
              <div style="width:36px;height:36px;background:rgba(255,255,255,.2);border-radius:50%;display:flex;align-items:center;justify-content:center;">🌿</div>
              <div>
                <div style="font-size:.88rem;font-weight:600;color:white;">Verdana AI</div>
                <div style="font-size:.68rem;color:#90ee90;">● Online — Ready to diagnose</div>
              </div>
            </div>
            <div style="background:rgba(255,255,255,.1);border-radius:10px 10px 10px 3px;padding:9px 12px;font-size:.79rem;color:rgba(255,255,255,.9);margin-bottom:8px;line-height:1.5;">
              Upload a photo and I'll diagnose your plant instantly.
            </div>
            <div style="background:#5a8a3c;color:white;border-radius:10px 10px 3px 10px;padding:9px 12px;font-size:.79rem;margin-left:auto;max-width:80%;margin-bottom:8px;line-height:1.5;">
              My Monstera leaves are yellow.
            </div>
            <div style="background:rgba(255,255,255,.1);border-radius:10px 10px 10px 3px;padding:9px 12px;font-size:.79rem;color:rgba(255,255,255,.9);line-height:1.5;">
              Likely <strong>nitrogen deficiency</strong>. Recommend: <strong>NPK Organic Fertilizer ₹249</strong> + <strong>Liquid Seaweed Extract ₹299</strong>.
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Testimonials
    st.markdown('<div class="v-section" style="background:var(--warm);">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Stories</div>
      <div class="v-section-title">What Our Plant Parents <em>Say</em></div>
    </div>
    """, unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""<div class="v-testi">
          <div class="v-testi-stars">★★★★★</div>
          <div class="v-testi-text">"The AI Plant Doctor diagnosed my Fiddle Leaf Fig immediately — nitrogen deficiency. The fertilizer arrived in two days and my plant recovered within a week."</div>
          <div class="v-testi-name">Arjun Mehta</div><div class="v-testi-loc">Mumbai, Maharashtra</div>
        </div>""", unsafe_allow_html=True)
    with t2:
        st.markdown("""<div class="v-testi">
          <div class="v-testi-stars">★★★★★</div>
          <div class="v-testi-text">"The care scheduler is a game changer. I uploaded a photo of my Monstera and got a complete weekly care plan. My plants have never looked better."</div>
          <div class="v-testi-name">Priya Rajan</div><div class="v-testi-loc">Bengaluru, Karnataka</div>
        </div>""", unsafe_allow_html=True)
    with t3:
        st.markdown("""<div class="v-testi">
          <div class="v-testi-stars">★★★★★</div>
          <div class="v-testi-text">"The monthly subscription kit is excellent. High quality organic fertilizers and the AI reminds me exactly when to use each product. Highly recommended."</div>
          <div class="v-testi-name">Vikram Sharma</div><div class="v-testi-loc">Pune, Maharashtra</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="v-footer">
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:3rem;max-width:1200px;margin:0 auto 2.5rem;">
        <div>
          <div class="v-footer-logo">Verdana</div>
          <div class="v-footer-desc">Your smart plant care partner. Combining premium botanicals with AI-powered diagnosis so your plants always thrive.</div>
        </div>
        <div>
          <div class="v-footer-col-title">Shop</div>
          <a class="v-footer-link" href="#">Indoor Plants</a>
          <a class="v-footer-link" href="#">Outdoor Plants</a>
          <a class="v-footer-link" href="#">Pots & Planters</a>
          <a class="v-footer-link" href="#">Fertilizers</a>
          <a class="v-footer-link" href="#">Seeds & Tools</a>
        </div>
        <div>
          <div class="v-footer-col-title">Services</div>
          <a class="v-footer-link" href="#">AI Plant Doctor</a>
          <a class="v-footer-link" href="#">Subscriptions</a>
          <a class="v-footer-link" href="#">Care Scheduler</a>
          <a class="v-footer-link" href="#">Plant Care Blog</a>
          <a class="v-footer-link" href="#">About Us</a>
        </div>
        <div>
          <div class="v-footer-col-title">Support</div>
          <a class="v-footer-link" href="#">Shipping Policy</a>
          <a class="v-footer-link" href="#">Return Policy</a>
          <a class="v-footer-link" href="#">Privacy Policy</a>
          <a class="v-footer-link" href="#">Track Your Order</a>
          <a class="v-footer-link" href="#">FAQ</a>
        </div>
      </div>
      <div class="v-footer-bottom" style="max-width:1200px;margin:0 auto;">
        <span>© 2025 Verdana. All rights reserved.</span>
        <span>"Diagnose, Nurture, Grow."</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 1 — PLANTS
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Bestsellers</div>
      <div class="v-section-title">Indoor <em>Plants</em></div>
      <div class="v-section-sub">Handpicked varieties that thrive indoors — for beginners and seasoned plant parents alike.</div>
    </div>
    """, unsafe_allow_html=True)

    cat_filter = st.selectbox(
        "Filter by category",
        ["All Plants", "Easy Care", "Air Purifying", "Rare & Exotic", "Flowering", "Succulents"],
        key="plant_cat"
    )
    cat_map = {
        "All Plants": None, "Easy Care": "easy", "Air Purifying": "air",
        "Rare & Exotic": "rare", "Flowering": "flowering", "Succulents": "succulent"
    }
    filtered = PLANTS if not cat_map[cat_filter] else [p for p in PLANTS if p.get("cat") == cat_map[cat_filter]]
    st.markdown(f"<div class='v-section-sub'>{len(filtered)} plants found</div><br>", unsafe_allow_html=True)
    render_product_grid(filtered, cols=4)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — PLANT CARE
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Organic Care</div>
      <div class="v-section-title">Fertilizers &amp; <em>Treatments</em></div>
      <div class="v-section-sub">Science-backed, AI-recommended plant care products for every condition.</div>
    </div>
    """, unsafe_allow_html=True)
    render_product_grid(PLANT_CARE, cols=4)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — POTS
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Artisan Collection</div>
      <div class="v-section-title">Pots &amp; <em>Planters</em></div>
      <div class="v-section-sub">Handcrafted pots that complement every aesthetic — from boho to brutalist.</div>
    </div>
    """, unsafe_allow_html=True)
    render_product_grid(POTS, cols=3)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — SEEDS
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Grow From Scratch</div>
      <div class="v-section-title">Seeds &amp; <em>Tools</em></div>
      <div class="v-section-sub">Everything you need to start and maintain your garden from day one.</div>
    </div>
    """, unsafe_allow_html=True)
    render_product_grid(SEEDS + PLANT_CARE[6:], cols=4)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — AI PLANT DOCTOR ⭐ MAIN FEATURE
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Powered by Claude AI</div>
      <div class="v-section-title">AI <em>Plant Doctor</em></div>
      <div class="v-section-sub">Upload a photo or describe your plant's symptoms — get an instant expert diagnosis with product recommendations and a personalised care schedule.</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.warning("Enter your Anthropic API key in the **sidebar** to activate the AI Plant Doctor.")

    # Chat header
    st.markdown("""
    <div class="v-chat-header">
      <div class="v-chat-avatar">🌿</div>
      <div>
        <div class="v-chat-name">Verdana AI Plant Doctor</div>
        <div class="v-chat-status">Expert Horticulturist — Online</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history_display:
            st.markdown("""
            <div class="v-msg-bot" style="margin-top:1rem;">
              Hello! I'm Verdana AI, your personal plant care expert. 🌿<br><br>
              I can help you:<br>
              • <strong>Diagnose</strong> plant problems from photos or descriptions<br>
              • <strong>Recommend</strong> the right fertilizers, pesticides, and care products<br>
              • <strong>Create</strong> a personalised weekly care schedule<br>
              • <strong>Find</strong> the perfect plant for your space<br><br>
              Upload a plant photo or type your question below!
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history_display:
                if msg["role"] == "user":
                    if msg.get("type") == "image":
                        st.image(msg["content"], width=220, caption="Plant photo uploaded")
                    else:
                        st.markdown(f'<div class="v-msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "assistant":
                    if msg.get("type") == "text":
                        st.markdown(f'<div class="v-msg-bot">{msg["content"].replace(chr(10), "<br>")}</div>',
                                    unsafe_allow_html=True)
                    elif msg.get("type") == "products":
                        prods = msg["content"]
                        cols = st.columns(min(len(prods), 3))
                        for col, p in zip(cols, prods):
                            with col:
                                st.markdown(f"""
                                <div class="v-chat-prod">
                                  <img src="{p['img']}" class="v-chat-prod-img" alt="{p['name']}"/>
                                  <div>
                                    <div class="v-chat-prod-name">{p['name']}</div>
                                    <div class="v-chat-prod-price">₹{p['price']:,}</div>
                                  </div>
                                </div>""", unsafe_allow_html=True)
                                if st.button("+ Cart", key=f"aicp_{p['id']}_{random.randint(0,9999)}"):
                                    add_to_cart(p["id"])
                                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick action buttons
    st.markdown("**Quick Actions:**")
    qa_cols = st.columns(4)
    quick_prompts = [
        ("🔬 Diagnose Plant", "I have a plant with yellowing leaves and drooping stems. Please diagnose the problem and recommend treatment."),
        ("🌿 Best Beginners", "Suggest the best plants for a beginner with low light conditions and a ₹500 budget."),
        ("📅 Care Schedule", "Create a detailed weekly care schedule for a Monstera Deliciosa."),
        ("🛡️ Pest Control", "My plant has small white insects and webbing on the leaves. What pest is this and how do I treat it organically?"),
    ]
    for col, (label, prompt) in zip(qa_cols, quick_prompts):
        with col:
            if st.button(label, use_container_width=True, key=f"qa_{label}"):
                if not st.session_state.api_key:
                    st.error("Add your API key in the sidebar.")
                else:
                    st.session_state.chat_history_display.append(
                        {"role": "user", "type": "text", "content": prompt})
                    st.session_state.chat_messages.append({"role": "user", "content": prompt})

                    with st.spinner("Verdana AI is thinking…"):
                        reply = call_claude(st.session_state.chat_messages)

                    st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                    st.session_state.chat_history_display.append(
                        {"role": "assistant", "type": "text", "content": reply})

                    prods = get_product_suggestions(reply)
                    if prods:
                        st.session_state.chat_history_display.append(
                            {"role": "assistant", "type": "products", "content": prods})
                    st.rerun()

    st.markdown("---")

    # Image upload
    st.markdown("**Upload a plant photo for AI diagnosis:**")
    uploaded_img = st.file_uploader(
        "Choose an image", type=["jpg", "jpeg", "png", "webp"],
        key="plant_img_upload", label_visibility="collapsed"
    )
    if uploaded_img:
        img_bytes = uploaded_img.read()
        b64 = base64.standard_b64encode(img_bytes).decode("utf-8")
        media_type = uploaded_img.type or "image/jpeg"

        col_img, col_btn = st.columns([3, 1])
        with col_img:
            st.image(img_bytes, width=280, caption="Plant photo ready for diagnosis")
        with col_btn:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("🔬 Diagnose Now", type="primary", use_container_width=True):
                if not st.session_state.api_key:
                    st.error("Add your API key in the sidebar.")
                else:
                    st.session_state.chat_history_display.append(
                        {"role": "user", "type": "image", "content": img_bytes})

                    msg_content = [
                        {"type": "image",
                         "source": {"type": "base64", "media_type": media_type, "data": b64}},
                        {"type": "text",
                         "text": ("Please diagnose this plant. Identify the plant type, assess its health, "
                                  "detect any issues (nutrient deficiency, pests, overwatering, disease, etc.), "
                                  "and recommend specific products from your inventory with a weekly care schedule.")}
                    ]
                    st.session_state.chat_messages.append({"role": "user", "content": msg_content})

                    with st.spinner("Analysing plant photo…"):
                        reply = call_claude(st.session_state.chat_messages)

                    st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                    st.session_state.chat_history_display.append(
                        {"role": "assistant", "type": "text", "content": reply})

                    prods = get_product_suggestions(reply)
                    if prods:
                        st.session_state.chat_history_display.append(
                            {"role": "assistant", "type": "products", "content": prods})
                    st.rerun()

    # Text chat input
    st.markdown("**Or type your question:**")
    chat_col, btn_col = st.columns([5, 1])
    with chat_col:
        user_input = st.text_area(
            "Chat input",
            placeholder="e.g. My pothos is wilting despite regular watering. What's wrong?",
            label_visibility="collapsed",
            key="chat_input_box",
            height=90,
        )
    with btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        send = st.button("Send", type="primary", use_container_width=True, key="chat_send")
        clear = st.button("Clear", use_container_width=True, key="chat_clear")

    if clear:
        st.session_state.chat_messages = []
        st.session_state.chat_history_display = []
        st.rerun()

    if send and user_input.strip():
        if not st.session_state.api_key:
            st.error("Please add your Anthropic API key in the sidebar to use the AI Doctor.")
        else:
            txt = user_input.strip()
            st.session_state.chat_history_display.append({"role": "user", "type": "text", "content": txt})
            st.session_state.chat_messages.append({"role": "user", "content": txt})

            with st.spinner("Verdana AI is thinking…"):
                reply = call_claude(st.session_state.chat_messages)

            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.session_state.chat_history_display.append(
                {"role": "assistant", "type": "text", "content": reply})

            prods = get_product_suggestions(reply)
            if prods:
                st.session_state.chat_history_display.append(
                    {"role": "assistant", "type": "products", "content": prods})
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 6 — SUBSCRIPTIONS
# ══════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Subscriptions</div>
      <div class="v-section-title">Care Plans for Every <em>Gardener</em></div>
      <div class="v-section-sub">Monthly deliveries of curated plant care products — with AI-powered reminders.</div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        <div class="v-plan">
          <div class="v-plan-name">Seedling</div>
          <div class="v-plan-price">₹299<span>/month</span></div>
          <div class="v-plan-desc">Perfect for beginners with 1–2 plants needing guidance and essentials.</div>
          <div class="v-plan-feat">Monthly fertilizer (500g)</div>
          <div class="v-plan-feat">AI diagnosis — 3 times/month</div>
          <div class="v-plan-feat">Basic care reminders</div>
          <div class="v-plan-feat">Free delivery</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started — ₹299/mo", use_container_width=True, key="plan1"):
            st.toast("Seedling Plan selected!", icon="🌱")
    with p2:
        st.markdown("""
        <div class="v-plan featured">
          <div class="v-plan-badge">Most Popular</div>
          <div class="v-plan-name">Green Thumb</div>
          <div class="v-plan-price">₹599<span>/month</span></div>
          <div class="v-plan-desc">For the growing plant parent with 3–8 plants and serious care ambitions.</div>
          <div class="v-plan-feat">Monthly fertilizer + pest control</div>
          <div class="v-plan-feat">Unlimited AI diagnoses</div>
          <div class="v-plan-feat">Weekly scheduler + reminders</div>
          <div class="v-plan-feat">Seasonal care kit (quarterly)</div>
          <div class="v-plan-feat">Priority support</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Subscribe — ₹599/mo", use_container_width=True, key="plan2", type="primary"):
            st.toast("Green Thumb Plan selected!", icon="🌿")
    with p3:
        st.markdown("""
        <div class="v-plan">
          <div class="v-plan-name">Botanist</div>
          <div class="v-plan-price">₹999<span>/month</span></div>
          <div class="v-plan-desc">For serious collectors and indoor garden curators with 10+ plants.</div>
          <div class="v-plan-feat">Full care kit (8 products)</div>
          <div class="v-plan-feat">Unlimited AI + photo diagnosis</div>
          <div class="v-plan-feat">Custom care plans per plant</div>
          <div class="v-plan-feat">Early access to rare plants</div>
          <div class="v-plan-feat">Dedicated horticulturist chat</div>
          <div class="v-plan-feat">Free same-day delivery (metro)</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started — ₹999/mo", use_container_width=True, key="plan3"):
            st.toast("Botanist Plan selected!", icon="🪴")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 7 — BLOG
# ══════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Plant Care Journal</div>
      <div class="v-section-title">Expert <em>Insights</em></div>
      <div class="v-section-sub">Science-backed plant care advice from our horticulture team.</div>
    </div>
    """, unsafe_allow_html=True)

    blogs = [
        {"tag":"Nutrient Guide","title":"Why Your Indoor Plants Always Look Pale: A Guide to Nitrogen Deficiency",
         "meta":"5 min read · June 2025",
         "img":"https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&q=80",
         "excerpt":"Pale, yellow-green leaves are the most common sign of nitrogen deficiency. Learn how to identify it, correct it quickly, and prevent it from recurring."},
        {"tag":"Pest Control","title":"Spider Mites, Aphids & Fungus Gnats: The Organic Way to Eliminate Them",
         "meta":"7 min read · May 2025",
         "img":"https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=600&q=80",
         "excerpt":"Discover how cold-pressed neem oil and systemic fungicides can eliminate the three most common indoor plant pests without harming your family or pets."},
        {"tag":"Soil Science","title":"The Secret to Thriving Houseplants: Understanding Soil pH and Drainage",
         "meta":"6 min read · May 2025",
         "img":"https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=600&q=80",
         "excerpt":"Most plant problems trace back to soil pH and waterlogging. Here's how to test and correct your potting mix for any plant species."},
        {"tag":"Plant Styling","title":"Designing a Living Wall: The Expert's Guide to Vertical Indoor Gardens",
         "meta":"8 min read · April 2025",
         "img":"https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=600&q=80",
         "excerpt":"Vertical gardens are the ultimate biophilic design statement. Learn which plants work best, how to mount them, and how to maintain them with minimal effort."},
        {"tag":"Rare Plants","title":"How to Care for a Bird of Paradise: The Complete Guide",
         "meta":"6 min read · April 2025",
         "img":"https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=600&q=80",
         "excerpt":"The Bird of Paradise is stunning but demanding. Master its watering, fertilising, and repotting schedule to keep it thriving year-round."},
        {"tag":"Beginners","title":"10 Nearly Indestructible Plants for the Black-Thumbed Gardener",
         "meta":"4 min read · March 2025",
         "img":"https://images.unsplash.com/photo-1632207691143-643e2a9a9361?w=600&q=80",
         "excerpt":"If you've killed every plant you've owned, this list is for you. These 10 varieties tolerate neglect, low light, and irregular watering with grace."},
    ]

    for i in range(0, len(blogs), 3):
        row = blogs[i:i+3]
        cols = st.columns(len(row))
        for col, b in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="v-blog">
                  <img src="{b['img']}" alt="{b['title']}"/>
                  <div class="v-blog-body">
                    <div class="v-blog-tag">{b['tag']}</div>
                    <div class="v-blog-title">{b['title']}</div>
                    <div style="font-size:.78rem;color:#7a7060;margin-bottom:8px;line-height:1.5;">{b['excerpt']}</div>
                    <div class="v-blog-meta">{b['meta']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Read Article", key=f"blog_{i}_{b['tag']}", use_container_width=True):
                    st.toast(f"Opening: {b['title'][:40]}…")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 8 — MY ACCOUNT
# ══════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<div class="v-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="v-section-hdr">
      <div class="v-section-eye">Dashboard</div>
      <div class="v-section-title">My <em>Account</em></div>
      <div class="v-section-sub">Track your orders, care history, saved diagnoses and wishlist.</div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Cart Items", cart_count(), help="Items in your current cart")
    with m2:
        st.metric("Wishlist", len(st.session_state.wishlist), help="Saved products")
    with m3:
        st.metric("AI Diagnoses", len([m for m in st.session_state.chat_history_display if m.get("role") == "user"]), help="Total AI consultations this session")
    with m4:
        st.metric("Cart Value", f"₹{cart_total():,}", help="Current cart total")

    st.markdown("<br>", unsafe_allow_html=True)
    acc1, acc2 = st.columns([1, 2])

    with acc1:
        st.markdown("#### Profile")
        with st.form("profile_form"):
            st.text_input("Full Name", value="Plant Lover", placeholder="Your name")
            st.text_input("Email", value="", placeholder="you@example.com")
            st.text_input("City", value="", placeholder="Mumbai")
            st.selectbox("Preferred Plant Type", ["Indoor", "Outdoor", "Both", "Succulents"])
            if st.form_submit_button("Save Profile", use_container_width=True, type="primary"):
                st.success("Profile saved!")

    with acc2:
        st.markdown("#### Care Reminders")
        st.markdown("Set up your plant care schedule — get notified when to water, fertilise, and treat.")
        with st.form("sched_form"):
            plant_name = st.text_input("Plant Name", placeholder="e.g. Monstera Deliciosa")
            r1, r2 = st.columns(2)
            with r1:
                water_freq = st.selectbox("Watering frequency", ["Every 2 days", "Every 3 days", "Weekly", "Every 10 days", "Every 2 weeks"])
            with r2:
                fert_freq = st.selectbox("Fertilizing frequency", ["Weekly", "Every 2 weeks", "Monthly", "Every 2 months"])
            if st.form_submit_button("Set Reminder", use_container_width=True):
                if plant_name:
                    st.success(f"Reminder set for **{plant_name}** — Water: {water_freq} | Fertilize: {fert_freq}")
                else:
                    st.warning("Please enter a plant name.")

        st.markdown("#### Saved Diagnoses")
        if not st.session_state.chat_history_display:
            st.info("No diagnoses yet. Visit the AI Plant Doctor tab to get started.")
        else:
            ai_replies = [m for m in st.session_state.chat_history_display
                          if m.get("role") == "assistant" and m.get("type") == "text"]
            if ai_replies:
                with st.expander(f"Latest Diagnosis ({len(ai_replies)} total)", expanded=True):
                    st.markdown(ai_replies[-1]["content"].replace("\n", "\n\n"))
            if st.button("Clear Chat History"):
                st.session_state.chat_messages = []
                st.session_state.chat_history_display = []
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
