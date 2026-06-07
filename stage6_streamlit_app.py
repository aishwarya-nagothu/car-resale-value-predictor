"""
Stage 6 — AutoValuate Dashboard
Streamlit frontend that calls the Stage 5 Flask/ngrok API.

Run:
    pip install streamlit requests
    streamlit run stage6_streamlit_app.py
"""

import streamlit as st
import requests
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoValuate · Used Car Price Estimator",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .main-title {
        font-size: 2.2rem; font-weight: 600;
        letter-spacing: -0.5px; margin-bottom: 0;
    }
    .sub-title {
        font-size: 0.95rem; color: #6b7280; margin-top: 4px;
    }
    .price-card {
        background: #f0f9ff;
        border: 1.5px solid #bae6fd;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    .price-value {
        font-size: 3rem; font-weight: 600;
        color: #0c4a6e; letter-spacing: -1px;
    }
    .price-lakh {
        font-size: 1.1rem; color: #0369a1; margin-top: 4px;
    }
    .range-box {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 1rem;
        text-align: center;
    }
    .range-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .06em; }
    .range-val { font-size: 1.2rem; font-weight: 600; color: #1e293b; }
    .factor-chip {
        display: inline-block;
        background: #f1f5f9; border: 1px solid #e2e8f0;
        border-radius: 100px; padding: 4px 12px;
        font-size: 0.8rem; color: #475569; margin: 3px;
    }
    .insight-box {
        background: #eff6ff; border-left: 3px solid #3b82f6;
        border-radius: 0 8px 8px 0; padding: 12px 16px;
        font-size: 0.9rem; color: #1d4ed8;
        margin-top: 1rem;
    }
    .stButton>button {
        width: 100%; background: #0c4a6e; color: white;
        border: none; border-radius: 10px; padding: 0.7rem 1.5rem;
        font-size: 1rem; font-weight: 500; font-family: 'DM Sans', sans-serif;
        transition: .15s;
    }
    .stButton>button:hover { background: #0369a1; }
    .section-head {
        font-size: 0.7rem; font-weight: 600; color: #94a3b8;
        text-transform: uppercase; letter-spacing: .1em;
        margin: 1.2rem 0 0.5rem;
    }
    div[data-testid="stMetricValue"] { font-size: 1.4rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sidebar — API config ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ API connection")
    api_url = st.text_input(
        "Flask/ngrok base URL",
        value="http://127.0.0.1:5000",
        help="Paste your ngrok public URL from Stage 5, e.g. https://xxxx.ngrok.io"
    )
    if st.button("Check health"):
        try:
            r = requests.get(f"{api_url}/health", timeout=5)
            d = r.json()
            st.success(f"✅ Connected — {d.get('model','?')} · {d.get('n_features','?')} features")
        except Exception as e:
            st.error(f"❌ Could not reach API\n{e}")

    st.divider()
    st.markdown("**Endpoints**")
    st.code(f"GET  {api_url}/health\nPOST {api_url}/predict\nPOST {api_url}/predict-batch")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🚗 AutoValuate</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Used car price estimator · Indian market · Stage 6 dashboard</div>', unsafe_allow_html=True)
st.divider()

# ── Two-column layout ─────────────────────────────────────────────────────────
col_form, col_result = st.columns([1.1, 1], gap="large")

with col_form:
    st.markdown('<div class="section-head">Vehicle identity</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        brand = st.selectbox("Brand", [
            "Tata","Hyundai","Kia","Maruti Suzuki","Mahindra",
            "Honda","Toyota","Ford","Volkswagen","Skoda",
            "Renault","MG","Jeep","BMW","Mercedes-Benz","Audi"
        ])
    with c2:
        model_name = st.selectbox("Model", [
            "Nexon","Creta","Seltos","Brezza","XUV300","City",
            "Innova","EcoSport","Polo","Octavia","Duster","Hector","Compass"
        ])

    c3, c4 = st.columns(2)
    with c3:
        make_year = st.selectbox("Make year", list(range(2024, 2009, -1)), index=4)
    with c4:
        km_driven = st.number_input("Kilometres driven", min_value=0, max_value=500000,
                                    value=52000, step=1000)

    car_age = 2025 - make_year

    st.markdown('<div class="section-head">Specs</div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        fuel_type    = st.selectbox("Fuel type", ["Petrol","Diesel","CNG","Electric"])
        bs_norm      = st.selectbox("BS norm", ["BSVI","BSIV","Unknown"])
        owners       = st.selectbox("Previous owners", ["1st Owner","2nd Owner","3rd Owner"])
    with c6:
        transmission = st.radio("Transmission", ["Manual","Automatic"], horizontal=True)
        insurance    = st.radio("Insurance", ["Comprehensive","Third Party"], horizontal=True)
        depreciation = st.selectbox("Depreciation", ["Low","Medium","High","Very High"], index=1)

    trans_sub = "Regular"
    if transmission == "Automatic":
        trans_sub = st.selectbox("Transmission subtype", ["DCT","CVT","Torque Converter","AMT"])

    st.markdown('<div class="section-head">Quality scores (1–10)</div>', unsafe_allow_html=True)
    s_overall  = st.slider("Overall quality", 1.0, 10.0, 8.5, 0.1)
    s_engine   = st.slider("Engine",          1.0, 10.0, 9.0, 0.1)
    s_systems  = st.slider("Systems",         1.0, 10.0, 8.8, 0.1)
    s_interior = st.slider("Interior",        1.0, 10.0, 8.2, 0.1)
    s_exterior = st.slider("Exterior",        1.0, 10.0, 8.5, 0.1)
    s_wear     = st.slider("Wear",            1.0, 10.0, 8.3, 0.1)
    s_value    = st.slider("Value perception",1.0, 10.0, 7.2, 0.1)

    composite = round((s_overall+s_engine+s_systems+s_interior+s_exterior+s_wear)/6, 3)
    st.info(f"Composite score: **{composite}**")

    st.markdown('<div class="section-head">Risk flags</div>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        meter_tampered = st.radio("Meter tampered?", ["No","Yes"], horizontal=True)
    with c8:
        flooded        = st.radio("Flood damaged?", ["No","Yes"], horizontal=True)

    if meter_tampered == "Yes" or flooded == "Yes":
        st.warning("⚠️ Risk flags active — price will be penalised.")

    st.divider()
    predict_clicked = st.button("🔍  Estimate price", use_container_width=True)

# ── Prediction logic ──────────────────────────────────────────────────────────
if predict_clicked:
    payload = {
        "brand": brand, "model": model_name,
        "make_year": make_year, "car_age": car_age,
        "km_driven": km_driven,
        "fuel_type": fuel_type, "transmission": transmission,
        "trans_sub": trans_sub, "bs_norm": bs_norm,
        "owners": owners, "insurance": insurance,
        "overall_quality": s_overall, "engine_score": s_engine,
        "systems_score": s_systems, "interior_score": s_interior,
        "exterior_score": s_exterior, "wear_score": s_wear,
        "value_score": s_value, "depreciation": depreciation,
        "meter_tampered": meter_tampered, "flooded": flooded,
    }
    with col_result:
        with st.spinner("Running model..."):
            try:
                resp = requests.post(f"{api_url}/predict", json=payload, timeout=10)
                data = resp.json()
                if "error" in data:
                    st.error(f"API error: {data['error']}")
                else:
                    st.session_state.result = {**data, **payload}
                    st.session_state.history.append({
                        "car": f"{brand} {model_name} ({make_year})",
                        "price_lakh": data["predicted_price_lakh"],
                        "km": km_driven,
                    })
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach the API. Make sure Flask is running and the URL is correct.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# ── Result panel ──────────────────────────────────────────────────────────────
with col_result:
    if st.session_state.result:
        r = st.session_state.result
        price     = r["predicted_price_inr"]
        lakh      = r["predicted_price_lakh"]
        low_lakh  = round(lakh * 0.92, 2)
        high_lakh = round(lakh * 1.08, 2)

        st.markdown(f"""
        <div class="price-card">
            <div style="font-size:.9rem;color:#0369a1;margin-bottom:.5rem">
                {r['brand']} {r['model']} · {r['make_year']} · {r['km_driven']:,} km
            </div>
            <div class="price-value">₹{price:,}</div>
            <div class="price-lakh">{lakh} Lakhs</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            st.markdown(f'<div class="range-box"><div class="range-label">Low estimate</div><div class="range-val">₹{low_lakh}L</div></div>', unsafe_allow_html=True)
        with rc2:
            st.metric("Model used", r.get("model_used", "—"))
        with rc3:
            st.markdown(f'<div class="range-box"><div class="range-label">High estimate</div><div class="range-val">₹{high_lakh}L</div></div>', unsafe_allow_html=True)

        # Derived factors
        factors = []
        if car_age <= 3: factors.append("Near-new premium")
        elif car_age >= 7: factors.append("High age discount")
        if km_driven < 30000: factors.append("Low km advantage")
        elif km_driven > 100000: factors.append("High km penalty")
        if transmission == "Automatic": factors.append("Automatic premium")
        if fuel_type == "Diesel": factors.append("Diesel demand")
        if bs_norm == "BSVI": factors.append("BSVI compliance")
        if owners == "1st Owner": factors.append("Single owner")
        if composite >= 8.5: factors.append("Excellent condition")
        if meter_tampered == "Yes": factors.append("Meter tamper penalty")
        if flooded == "Yes": factors.append("Flood damage penalty")
        if insurance == "Comprehensive": factors.append("Comprehensive insurance")

        if factors:
            st.markdown("**Key pricing factors**")
            chips = " ".join([f'<span class="factor-chip">{f}</span>' for f in factors[:6]])
            st.markdown(chips, unsafe_allow_html=True)

        insight = f"{brand} {model_name} with {owners.lower()} owner and {car_age}-year age places this competitively in the {fuel_type.lower()} segment."
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;color:#94a3b8">
            <div style="font-size:3rem">🚗</div>
            <div style="font-size:1rem;margin-top:.5rem">Fill in the form and hit <strong>Estimate price</strong></div>
        </div>
        """, unsafe_allow_html=True)

# ── History table ─────────────────────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    st.markdown("#### Prediction history this session")
    import pandas as pd
    df = pd.DataFrame(st.session_state.history)
    df.columns = ["Car", "Price (Lakhs)", "Km driven"]
    df.index += 1
    st.dataframe(df, use_container_width=True)
    if st.button("Clear history"):
        st.session_state.history = []
        st.session_state.result  = None
        st.rerun()

# ── Batch predict tab ─────────────────────────────────────────────────────────
st.divider()
with st.expander("📦 Batch predict — test all 5 sample SUVs"):
    if st.button("Run batch prediction"):
        batch = [
            {"brand":"Tata","model":"Nexon","make_year":2021,"car_age":4,"km_driven":50000,"fuel_type":"Petrol","transmission":"Manual","trans_sub":"Regular","bs_norm":"BSVI","owners":"1st Owner","insurance":"Comprehensive","overall_quality":8.5,"engine_score":9.0,"systems_score":8.8,"interior_score":8.2,"exterior_score":8.5,"wear_score":8.3,"value_score":7.2,"depreciation":"High","meter_tampered":"No","flooded":"No"},
            {"brand":"Hyundai","model":"Creta","make_year":2020,"car_age":5,"km_driven":72000,"fuel_type":"Diesel","transmission":"Manual","trans_sub":"Regular","bs_norm":"BSVI","owners":"1st Owner","insurance":"Comprehensive","overall_quality":8.2,"engine_score":8.8,"systems_score":8.5,"interior_score":7.9,"exterior_score":8.0,"wear_score":7.8,"value_score":6.9,"depreciation":"High","meter_tampered":"No","flooded":"No"},
            {"brand":"Kia","model":"Seltos","make_year":2022,"car_age":3,"km_driven":35000,"fuel_type":"Petrol","transmission":"Automatic","trans_sub":"DCT","bs_norm":"BSVI","owners":"1st Owner","insurance":"Comprehensive","overall_quality":9.0,"engine_score":9.2,"systems_score":9.0,"interior_score":8.8,"exterior_score":8.9,"wear_score":9.1,"value_score":7.8,"depreciation":"Medium","meter_tampered":"No","flooded":"No"},
            {"brand":"Maruti Suzuki","model":"Brezza","make_year":2019,"car_age":6,"km_driven":85000,"fuel_type":"Petrol","transmission":"Manual","trans_sub":"Regular","bs_norm":"BSIV","owners":"2nd Owner","insurance":"Third Party","overall_quality":7.5,"engine_score":7.8,"systems_score":7.6,"interior_score":7.0,"exterior_score":7.2,"wear_score":7.0,"value_score":6.2,"depreciation":"Very High","meter_tampered":"No","flooded":"No"},
            {"brand":"Mahindra","model":"XUV300","make_year":2018,"car_age":7,"km_driven":110000,"fuel_type":"Diesel","transmission":"Manual","trans_sub":"Regular","bs_norm":"BSIV","owners":"2nd Owner","insurance":"Third Party","overall_quality":7.0,"engine_score":7.5,"systems_score":7.2,"interior_score":6.8,"exterior_score":6.9,"wear_score":6.5,"value_score":5.8,"depreciation":"Very High","meter_tampered":"No","flooded":"No"},
        ]
        labels = ["Tata Nexon (2021)","Hyundai Creta (2020)","Kia Seltos (2022)","Maruti Brezza (2019)","Mahindra XUV (2018)"]
        try:
            resp = requests.post(f"{api_url}/predict-batch", json=batch, timeout=15)
            data = resp.json()
            import pandas as pd
            rows = [{"Car": labels[p["index"]], "Predicted Price": p["formatted"]} for p in data["predictions"]]
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        except Exception as e:
            st.error(f"Batch prediction failed: {e}")