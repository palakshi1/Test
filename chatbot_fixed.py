
def render_chatbot():
    """
    Renders the chatbot floating panel.
    - FAB is a pure HTML/JS button injected via st.components → no inline Streamlit widget
    - Sidebar is CSS-repositioned to bottom-right floating panel
    - Toggle state is managed via st.query_params so JS can flip it
    """
    import streamlit.components.v1 as components

    # ── Read toggle signal from query params ─────────────────────────────────
    qp = st.query_params
    if qp.get("cb_toggle") == "1":
        st.session_state.chatbot_open = not st.session_state.chatbot_open
        if st.session_state.chatbot_open:
            st.session_state.chatbot_mode     = None
            st.session_state.chatbot_messages = []
            st.session_state.diagnosis_result = None
            st.session_state[SUGGESTION_RESULTS_KEY] = None
        # Clear the param so it doesn't re-fire on next render
        st.query_params.clear()
        st.rerun()

    # ── Inject global CSS ────────────────────────────────────────────────────
    st.markdown(CHATBOT_CSS, unsafe_allow_html=True)

    # ── Show/hide sidebar via CSS ────────────────────────────────────────────
    if st.session_state.chatbot_open:
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            opacity: 1 !important; pointer-events: all !important;
            transform: translateY(0) scale(1) !important;
            visibility: visible !important;
        }
        </style>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            opacity: 0 !important; pointer-events: none !important;
            transform: translateY(16px) scale(0.97) !important;
            visibility: hidden !important;
        }
        </style>""", unsafe_allow_html=True)

    # ── TRUE FIXED FAB — injected as a real HTML component ───────────────────
    # This lives completely outside Streamlit's render tree so it never creates
    # whitespace or inline elements on the main page.
    is_open   = st.session_state.chatbot_open
    fab_label = "✕  Close Chat" if is_open else "🌿  PlantBot"
    fab_bg    = "linear-gradient(135deg,#AD1457,#880E4F)" if is_open else "linear-gradient(135deg,#E91E8C,#AD1457)"

    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin:0; padding:0; background:transparent; overflow:hidden; }}
        #fab {{
            position: fixed;
            bottom: 24px;
            right: 20px;
            background: {fab_bg};
            color: white;
            padding: 14px 22px;
            border-radius: 50px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: 'DM Sans', 'Segoe UI', sans-serif;
            font-weight: 700;
            font-size: 14px;
            box-shadow: 0 8px 28px rgba(233,30,140,0.55);
            border: 3px solid rgba(255,255,255,0.4);
            cursor: pointer;
            user-select: none;
            z-index: 999999;
            animation: fabGlow 2.6s infinite;
            white-space: nowrap;
        }}
        #fab:hover {{
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 12px 36px rgba(233,30,140,0.70);
        }}
        @keyframes fabGlow {{
            0%,100% {{ box-shadow: 0 8px 28px rgba(233,30,140,0.55); }}
            50%      {{ box-shadow: 0 14px 42px rgba(233,30,140,0.80), 0 0 0 10px rgba(233,30,140,0.08); }}
        }}
        .dot {{
            width: 9px; height: 9px;
            background: #69F0AE;
            border-radius: 50%;
            animation: blink 1.4s infinite;
            flex-shrink: 0;
        }}
        @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}
    </style>
    </head>
    <body>
    <div id="fab" onclick="toggleChat()">
        <span style="font-size:18px;">{"✕" if is_open else "🌿"}</span>
        {fab_label}
        <div class="dot"></div>
    </div>
    <script>
    function toggleChat() {{
        // Navigate the parent Streamlit window to add ?cb_toggle=1
        // Streamlit will catch this on next rerun via st.query_params
        var url = new URL(window.parent.location.href);
        url.searchParams.set('cb_toggle', '1');
        window.parent.location.href = url.toString();
    }}
    </script>
    </body>
    </html>
    """, height=0, scrolling=False)
    # height=0 means the component takes zero vertical space — no whitespace

    # ── Sidebar panel content ────────────────────────────────────────────────
    with st.sidebar:
        _render_chatbot_panel()


# ── Panel content (runs inside `with st.sidebar:`) ──────────────────────────
def _render_chatbot_panel():
    """All chatbot UI lives here — header, modes, diagnosis, suggestions."""

    # ── HEADER ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cb-header">
        <div style="display:flex;align-items:center;gap:12px;">
            <div class="cb-avatar">🌿</div>
            <div style="flex:1;">
                <div class="cb-title">PlantBot</div>
                <div class="cb-subtitle">Your AI Plant Expert · Always Online</div>
            </div>
            <div style="display:flex;align-items:center;gap:5px;">
                <div style="width:8px;height:8px;background:#69F0AE;border-radius:50%;
                            animation:dotBlink 1.4s infinite;"></div>
                <span style="font-size:11px;color:rgba(255,255,255,0.7);">Live</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── WELCOME MESSAGE ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:12px 12px 0;">
    <div class="chat-msg-bot">
        <strong>Hi! I'm PlantBot 🌱</strong><br>
        How can I help you today? Choose an option below to get started.
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MODE SELECTOR ────────────────────────────────────────────────────────
    if st.session_state.chatbot_mode is None:
        st.markdown("<div style='padding:0 12px;'>", unsafe_allow_html=True)

        st.markdown("""
        <div class="cb-mode-card">
            <div class="cb-mode-icon">🔬</div>
            <div class="cb-mode-title">🌿 Plant Diagnosis</div>
            <div class="cb-mode-desc">Upload a photo of your plant and describe symptoms.
            Get an AI diagnosis with treatment plan and product recommendations.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Diagnosis →", key="cb_btn_diag", type="primary", use_container_width=True):
            st.session_state.chatbot_mode     = "diagnosis"
            st.session_state.diagnosis_result = None
            st.rerun()

        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="cb-mode-card">
            <div class="cb-mode-icon">🛒</div>
            <div class="cb-mode-title">🛒 Plant Buying Suggestions</div>
            <div class="cb-mode-desc">Answer 4 quick questions about your space & lifestyle.
            I'll suggest perfect plants with prices and cart buttons.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Suggestions →", key="cb_btn_sugg", use_container_width=True):
            st.session_state.chatbot_mode = "suggestions"
            st.session_state[SUGGESTION_RESULTS_KEY] = None
            st.rerun()

        st.markdown("""
        <div style="margin-top:14px;padding:12px;
                    background:linear-gradient(135deg,#FFF0F8,#FCE4EC);
                    border-radius:12px;border-left:3px solid #E91E8C;">
            <div style="font-size:11px;color:#E91E8C;font-weight:700;margin-bottom:4px;">💡 Did you know?</div>
            <div style="font-size:11px;color:#555;line-height:1.6;">
                NASA's Clean Air Study found houseplants can remove up to 87%
                of indoor air toxins in 24 hours.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── BACK BUTTON ─────────────────────────────────────────────────────────
    st.markdown("<div style='padding:8px 12px 0;'>", unsafe_allow_html=True)
    if st.button("← Back to Menu", key="cb_back_top", use_container_width=True):
        st.session_state.chatbot_mode     = None
        st.session_state.diagnosis_result = None
        st.session_state[SUGGESTION_RESULTS_KEY] = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.chatbot_mode == "diagnosis":
        handle_diagnosis()
    elif st.session_state.chatbot_mode == "suggestions":
        handle_recommendations()


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE 1 — PLANT DIAGNOSIS
# ─────────────────────────────────────────────────────────────────────────────
def handle_diagnosis():
    st.markdown("""
    <div style="padding:0 12px;">
    <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                letter-spacing:1.5px;color:#E91E8C;margin:10px 0 8px;">
        🔬 Plant Diagnosis Doctor
    </div>
    <div class="chat-msg-bot">
        Upload a photo of your plant and describe what you're seeing.
        I'll diagnose the issue and suggest a treatment plan.
    </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload plant photo",
        type=["jpg", "jpeg", "png", "webp"],
        key="diag_image_upload",
        label_visibility="collapsed",
    )
    if uploaded:
        st.image(uploaded, use_container_width=True,
                 caption="Your plant photo", output_format="auto")

    st.markdown("**Describe the symptoms:**")
    symptoms = st.text_area(
        "Symptoms",
        placeholder="e.g. Yellow leaves, brown tips, wilting, spots, mushy stems...",
        key="diag_symptoms",
        label_visibility="collapsed",
        height=80,
    )

    st.markdown("<div style='font-size:11px;color:#888;margin-bottom:4px;'>Quick select:</div>",
                unsafe_allow_html=True)
    chip_cols = st.columns(2)
    quick = ["Yellow leaves", "Brown tips", "Wilting", "Spots/fungus",
             "Root rot", "Leggy growth", "Drooping", "Pale color"]
    for i, label in enumerate(quick):
        with chip_cols[i % 2]:
            if st.button(label, key=f"chip_{i}", use_container_width=True):
                st.session_state["diag_symptoms"] = label
                st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    diag_ready = uploaded is not None or (symptoms and len(symptoms.strip()) > 3)
    if st.button("🔬 Diagnose My Plant", key="run_diagnosis_btn",
                 type="primary", use_container_width=True, disabled=not diag_ready):
        if uploaded:
            result = analyze_plant(uploaded)
        else:
            sym_lower = symptoms.lower()
            key_map = {
                "yellow":    "Overwatering",
                "overwater": "Overwatering",
                "droop":     "Overwatering",
                "brown":     "Underwatering",
                "dry":       "Underwatering",
                "wilt":      "Underwatering",
                "spot":      "Fungal Leaf Spot",
                "fungus":    "Fungal Leaf Spot",
                "mold":      "Fungal Leaf Spot",
                "bug":       "Spider Mite Infestation",
                "mite":      "Spider Mite Infestation",
                "insect":    "Spider Mite Infestation",
                "pale":      "Nutrient Deficiency",
                "nutrient":  "Nutrient Deficiency",
                "root":      "Root Rot",
                "rot":       "Root Rot",
                "leggy":     "Insufficient Light",
                "light":     "Insufficient Light",
                "burn":      "Sunburn / Heat Stress",
                "sunburn":   "Sunburn / Heat Stress",
            }
            matched = None
            for kw, dk in key_map.items():
                if kw in sym_lower:
                    matched = dk
                    break
            result = DIAGNOSIS_MAP.get(matched, list(DIAGNOSIS_MAP.values())[0])
        st.session_state.diagnosis_result = result
        st.rerun()

    if st.session_state.diagnosis_result:
        result = st.session_state.diagnosis_result

        st.markdown(f"""
        <div class="chat-msg-bot" style="margin-top:10px;">
            <strong>✅ Diagnosis Complete!</strong><br>
            Here's what I found:
        </div>
        <div class="diag-result-card">
            <div class="diag-result-header"
                 style="background:linear-gradient(135deg,#FFF0F8,#FCE4EC);">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                    <span style="font-size:24px;">{result.get('icon','🌿')}</span>
                    <div>
                        <div style="font-family:'Playfair Display',serif;font-size:15px;
                                    font-weight:700;color:#1A1A1A;">{result['issue']}</div>
                        <div style="margin-top:4px;">{_severity_badge(result['severity'])}</div>
                    </div>
                </div>
                {_confidence_bar(result['confidence'])}
                <div style="font-size:12px;color:#555;margin-top:8px;line-height:1.6;">
                    {result['description']}
                </div>
            </div>
            <div class="diag-result-body">
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                            letter-spacing:1px;color:#E91E8C;margin-bottom:8px;">
                    💊 Treatment Steps
                </div>
        """, unsafe_allow_html=True)

        for i, step in enumerate(result["steps"], 1):
            st.markdown(f"""
            <div class="care-step">
                <div class="step-num">{i}</div>
                <div>{step}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        if result.get("care_schedule"):
            st.markdown("""
            <div style="background:#FFF0F8;border-radius:12px;
                        padding:12px 14px;margin:10px 0;">
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                            letter-spacing:1px;color:#E91E8C;margin-bottom:8px;">
                    📅 Care Schedule
                </div>
            """, unsafe_allow_html=True)
            for day, task in result["care_schedule"].items():
                st.markdown(f"""
                <div style="display:flex;gap:8px;align-items:flex-start;padding:5px 0;
                            border-bottom:1px solid #F8E8F0;font-size:12px;color:#444;">
                    <span style="font-weight:700;color:#E91E8C;min-width:70px;">{day}</span>
                    <span>{task}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        remedy_products = [p for p in PRODUCTS if p["name"] in result.get("remedy_products", [])]
        if remedy_products:
            st.markdown("""
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                        letter-spacing:1px;color:#E91E8C;margin:12px 0 8px;">
                🛍️ Recommended Products
            </div>
            """, unsafe_allow_html=True)
            for prod in remedy_products:
                disc = discount_pct(prod["price"], prod["original_price"])
                st.markdown(f"""
                <div class="remedy-card">
                    <img class="remedy-img" src="{prod['image']}" alt="{prod['name']}"
                         onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=100&h=100&fit=crop'"/>
                    <div style="flex:1;min-width:0;">
                        <div style="font-weight:700;font-size:12px;color:#1A1A1A;
                                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                            {prod['name']}</div>
                        <div style="font-size:11px;color:#777;margin:2px 0;">
                            {prod['category']}</div>
                        <div style="display:flex;align-items:center;gap:6px;">
                            <span style="font-weight:700;font-size:14px;color:#1B5E20;">
                                ₹{prod['price']}</span>
                            {'<span style="font-size:10px;background:#FCE4EC;color:#C62828;padding:1px 6px;border-radius:50px;font-weight:700;">' + str(disc) + '% off</span>' if disc else ''}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🛒 Add to Cart", key=f"diag_atc_{prod['id']}",
                             use_container_width=True, type="primary"):
                    add_to_cart(prod["id"])
                    st.success(f"✅ {prod['name']} added!")
                    st.rerun()

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 New Diagnosis", key="diag_reset", use_container_width=True):
                st.session_state.diagnosis_result = None
                st.rerun()
        with c2:
            if st.button("🏠 Main Menu", key="diag_to_menu", use_container_width=True):
                st.session_state.chatbot_mode     = None
                st.session_state.diagnosis_result = None
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE 2 — PLANT BUYING SUGGESTIONS
# ─────────────────────────────────────────────────────────────────────────────
def handle_recommendations():
    results_ready = bool(st.session_state.get(SUGGESTION_RESULTS_KEY))

    st.markdown("""
    <div style="padding:0 12px 8px;">
    <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                letter-spacing:1.5px;color:#E91E8C;margin-bottom:8px;">
        🛒 Plant Suggestions Expert
    </div>
    """, unsafe_allow_html=True)

    dots_html = '<div class="quiz-dots">'
    for i in range(4):
        cls = "quiz-dot active" if (results_ready or i < 0) else "quiz-dot"
        dots_html += f'<div class="{cls}"></div>'
    dots_html += "</div></div>"
    st.markdown(dots_html, unsafe_allow_html=True)

    if not results_ready:
        st.markdown("""
        <div style="padding:0 12px;">
        <div class="chat-msg-bot">
            Answer 4 quick questions and I'll find your perfect plant match! 🌱
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Q1 — Where will the plant live?**")
        location = st.radio("Location",
            ["🏠 Indoor", "🌳 Outdoor", "🏡 Both"],
            key="q_location", label_visibility="collapsed")

        st.markdown("**Q2 — How much natural light?**")
        light = st.radio("Light",
            ["🌑 Very Low", "🌤 Indirect Bright", "⛅ Partial Sun", "☀️ Full Sun"],
            key="q_light", label_visibility="collapsed")

        st.markdown("**Q3 — Time for plant care?**")
        maintenance = st.radio("Maintenance",
            ["😴 Minimal (once a week)", "🌿 Moderate (2–3×/week)", "🌸 Enthusiast (daily)"],
            key="q_maintenance", label_visibility="collapsed")

        st.markdown("**Q4 — What matters most?**")
        purpose = st.multiselect("Purpose",
            ["Air Purification", "Flowering / Colour", "Gifting",
             "Low Maintenance", "Aesthetic Decor", "Beginner Friendly"],
            key="q_purpose", label_visibility="collapsed",
            placeholder="Select all that apply...")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("🌿 Find My Perfect Plants", key="run_suggestions_btn",
                     type="primary", use_container_width=True):
            pool = list(PRODUCTS)
            if "Indoor" in location:
                pool = [p for p in pool if p["category"] in
                        ["Indoor Plants","Air Purifying Plants","Succulents","Flowering Plants","Bonsai Plants"]]
            elif "Outdoor" in location:
                pool = [p for p in pool if p["category"] in ["Outdoor Plants","Flowering Plants"]]

            if "Very Low" in light:
                pool = [p for p in pool if p.get("sunlight") in ["Low Light","Low to Bright","Indirect",None]]
            elif "Indirect" in light:
                pool = [p for p in pool if p.get("sunlight") in ["Indirect","Bright Indirect","Low to Bright","Low to Medium",None]]
            elif "Full Sun" in light:
                pool = [p for p in pool if p.get("sunlight") in ["Full Sun",None]]

            if "Minimal" in maintenance:
                pool = [p for p in pool if p.get("care_level") in ["Very Easy",None]]
            elif "Moderate" in maintenance:
                pool = [p for p in pool if p.get("care_level") in ["Very Easy","Easy",None]]

            if "Air Purification" in purpose:
                ap = [p for p in pool if p.get("air_purifying")]
                if ap: pool = ap
            if "Flowering / Colour" in purpose:
                fl = [p for p in pool if p["category"] in ["Flowering Plants","Outdoor Plants"]]
                if fl: pool = fl
            if "Low Maintenance" in purpose:
                lm = [p for p in pool if p.get("care_level") in ["Very Easy","Easy"]]
                if lm: pool = lm

            def _score(p):
                s = p["rating"] * 10
                if p.get("badge") in ["Bestseller","Top Rated"]: s += 8
                if "Air Purification" in purpose and p.get("air_purifying"): s += 15
                if "Beginner Friendly" in purpose and p.get("care_level") in ["Very Easy","Easy"]: s += 10
                return s

            pool = sorted(pool, key=_score, reverse=True)
            if not pool:
                pool = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)[:4]
            st.session_state[SUGGESTION_RESULTS_KEY] = pool[:5]
            st.rerun()

    else:
        results = st.session_state[SUGGESTION_RESULTS_KEY]
        st.markdown(f"""
        <div style="padding:0 12px;">
        <div class="chat-msg-bot">
            🎉 Found <strong>{len(results)}</strong> perfect matches!
            Tap <em>Add to Cart</em> to get started.
        </div>
        </div>
        """, unsafe_allow_html=True)

        care_map = {"Very Easy":"🟢 Easy","Easy":"🟡 Some care","Moderate":"🟠 Moderate","Expert":"🔴 Advanced"}
        for rank, prod in enumerate(results):
            match_pct = max(72, 98 - rank * 5)
            disc      = discount_pct(prod["price"], prod["original_price"])
            air_tag   = " · 💨 Air Purifier" if prod.get("air_purifying") else ""

            st.markdown(f"""
            <div class="sugg-plant-card">
                <div style="position:relative;">
                    <img class="sugg-plant-img" src="{prod['image']}" alt="{prod['name']}"
                         onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=110&fit=crop'"/>
                    <div style="position:absolute;top:8px;left:8px;">
                        <span class="sugg-match-badge">{match_pct}% Match</span>
                    </div>
                    {'<div style="position:absolute;top:8px;right:8px;background:#FCE4EC;color:#C62828;padding:2px 7px;border-radius:50px;font-size:10px;font-weight:700;">' + str(disc) + '% off</div>' if disc else ''}
                </div>
                <div class="sugg-plant-body">
                    <div style="font-size:10px;color:#E91E8C;font-weight:700;
                                text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;">
                        {prod['category']}</div>
                    <div style="font-family:'Playfair Display',serif;font-size:14px;
                                font-weight:700;color:#1A1A1A;margin-bottom:3px;">
                        {prod['name']}</div>
                    <div style="font-size:11px;color:#777;margin-bottom:7px;">
                        {care_map.get(prod.get('care_level',''),'🟡 Some care')}{air_tag}</div>
                    <div style="display:flex;align-items:center;justify-content:space-between;">
                        <div>
                            <span style="font-weight:700;font-size:16px;color:#1B5E20;">
                                ₹{prod['price']}</span>
                            <span style="font-size:11px;color:#bbb;text-decoration:line-through;margin-left:4px;">
                                ₹{prod['original_price']}</span>
                        </div>
                        <div style="color:#FFA000;font-size:12px;">
                            {"★" * int(prod['rating'])} {prod['rating']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            sc1, sc2 = st.columns(2)
            with sc1:
                if st.button("🛒 Add to Cart", key=f"sugg_atc_{prod['id']}",
                             use_container_width=True, type="primary"):
                    add_to_cart(prod["id"])
                    st.success(f"✅ {prod['name']} added!")
                    st.rerun()
            with sc2:
                if st.button("👁 View", key=f"sugg_view_{prod['id']}", use_container_width=True):
                    nav_to("product", selected_product=prod["id"])
                    st.session_state.chatbot_open = False
                    st.rerun()

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Retake Quiz", key="retake_quiz", use_container_width=True):
                st.session_state[SUGGESTION_RESULTS_KEY] = None
                st.rerun()
        with c2:
            if st.button("🏠 Main Menu", key="sugg_to_menu", use_container_width=True):
                st.session_state.chatbot_mode = None
                st.session_state[SUGGESTION_RESULTS_KEY] = None
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # ── 1. Chatbot FIRST (mounts sidebar + FAB, reads query_params toggle)
    render_chatbot()

    # ── 2. Navbar
    render_navbar()

    # ── 3. Page content
    page = st.session_state.page
    if page == "home":
        render_home()
    elif page == "category":
        render_category_page()
    elif page == "product":
        render_product_detail()
    elif page == "search":
        render_search()
    elif page == "cart":
        render_cart()
    elif page == "checkout":
        render_checkout()
    elif page == "about":
        render_about()
    elif page == "contact":
        render_contact()
    elif page == "offers":
        render_offers()
    else:
        render_home()


main()
