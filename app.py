import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="FraudDetect",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #f0f4f8;
        color: #1a1a2e;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Navbar */
    .navbar {
        background: linear-gradient(135deg, #0f1b4c, #1a3a6b);
        border-radius: 0 0 20px 20px;
        padding: 20px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 32px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .navbar-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .navbar-logo { font-size: 32px; }
    .navbar-title {
        font-size: 32px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .navbar-title span { color: #60a5fa; }
    .navbar-subtitle {
        font-size: 13px;
        color: #93c5fd;
        margin-top: 3px;
        font-weight: 500;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 5px !important;
        gap: 4px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #93c5fd !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.3px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e40af !important;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(30,64,175,0.5) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        margin-top: -72px !important;
        margin-bottom: 32px !important;
        float: right !important;
        width: fit-content !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 8px !important;
    }

    /* Section headers */
    .section-header {
        color: #1e40af;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #dbeafe;
    }

    /* Verdict boxes */
    .verdict-fraud {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(239,68,68,0.3);
    }
    .verdict-safe {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(16,185,129,0.3);
    }

    /* Next steps boxes */
    .alert-fraud {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(239,68,68,0.2);
    }
    .alert-safe {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(16,185,129,0.2);
    }
    .alert-waiting {
        background: linear-gradient(135deg, #1e3a5f, #1e40af);
        border: 2px solid #60a5fa;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
    }

    /* Step cards */
    .step-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }

    /* Risk badges */
    .badge-high {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 6px 20px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 15px;
        border: 2px solid #ef4444;
        display: inline-block;
    }
    .badge-medium {
        background-color: #fef3c7;
        color: #92400e;
        padding: 6px 20px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 15px;
        border: 2px solid #f59e0b;
        display: inline-block;
    }
    .badge-low {
        background-color: #d1fae5;
        color: #065f46;
        padding: 6px 20px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 15px;
        border: 2px solid #10b981;
        display: inline-block;
    }

    /* Input styling */
    .stSlider label, .stSelectbox label,
    .stNumberInput label, .stRadio label {
        color: #374151 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    .stRadio > div { font-size: 16px !important; }

    /* Predict button */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af, #1d4ed8);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-size: 19px;
        font-weight: 800;
        width: 100%;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(29,78,216,0.4);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29,78,216,0.5);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #6b7280 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #1e40af !important;
    }

    /* Prevention tip cards */
    .tip-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1e40af;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    /* Risk habit items */
    .habit-safe {
        background: #d1fae5;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
        border-left: 4px solid #10b981;
        color: #065f46;
        font-weight: 600;
        font-size: 14px;
    }
    .habit-risky {
        background: #fee2e2;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
        border-left: 4px solid #ef4444;
        color: #991b1b;
        font-weight: 600;
        font-size: 14px;
    }
    .habit-medium {
        background: #fef3c7;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
        border-left: 4px solid #f59e0b;
        color: #92400e;
        font-weight: 600;
        font-size: 14px;
    }

    h2 { font-size: 32px !important; }
    p  { font-size: 16px !important; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open('best_model.pkl', 'rb') as f:
        bundle = pickle.load(f)
    return bundle

bundle          = load_models()
model           = bundle['model']
scaler          = bundle['scaler']
model_name      = bundle['model_name']
feature_cols    = bundle['feature_cols']
results_summary = bundle['results_summary']

# ── Session state ──────────────────────────────────────────
if 'last_prediction'   not in st.session_state:
    st.session_state.last_prediction   = None
if 'last_fraud_pct'    not in st.session_state:
    st.session_state.last_fraud_pct    = None
if 'last_risk_level'   not in st.session_state:
    st.session_state.last_risk_level   = None
if 'last_inputs'       not in st.session_state:
    st.session_state.last_inputs       = None

# ── Navbar ─────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="navbar-left">
        <div class="navbar-logo">🛡️</div>
        <div>
            <div class="navbar-title">Fraud<span>Detect</span></div>
            <div class="navbar-subtitle">
                Real-time credit card fraud detection
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍  Predict",
    "🛡️  Next Steps",
    "📊  Model Insights",
    "ℹ️   About"
])

# ════════════════════════════════════════════════════════════
# TAB 1 — PREDICT
# ════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #1e40af; font-size: 32px; font-weight: 800; margin: 0;">
            Transaction Analysis
        </h2>
        <p style="color: #6b7280; font-size: 16px; margin-top: 6px;">
            Fill in the details below to check whether a transaction is fraudulent.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">Transaction Details</div>',
                    unsafe_allow_html=True)

        st.markdown("**Transaction Amount ($)**")
        amt_col1, amt_col2 = st.columns(2)
        with amt_col1:
            dollars = st.number_input("Dollars", min_value=0,
                                       max_value=19999, value=150, step=1)
        with amt_col2:
            cents = st.number_input("Cents", min_value=0,
                                     max_value=99, value=0, step=1)
        amount = dollars + cents / 100
        st.caption(f"Total amount: **${amount:.2f}**")

        col_a, col_b = st.columns(2)
        with col_a:
            hour = st.slider("Hour of Day", min_value=0, max_value=23,
                              value=14, help="0 = midnight, 23 = 11pm")
            if hour == 0:
                time_display = "12:00 AM (Midnight)"
            elif hour < 12:
                time_display = f"{hour}:00 AM"
            elif hour == 12:
                time_display = "12:00 PM (Noon)"
            else:
                time_display = f"{hour - 12}:00 PM"
            st.caption(f"Time: **{time_display}**")
        with col_b:
            day = st.selectbox(
                "Day of Week",
                options=[0,1,2,3,4,5,6],
                format_func=lambda x: ['Monday','Tuesday','Wednesday',
                                        'Thursday','Friday',
                                        'Saturday','Sunday'][x]
            )

        distance = st.number_input(
            "Distance from Home (km)",
            min_value=0.0, max_value=800.0,
            value=10.0, step=1.0,
            help="How far is this transaction from the cardholder's home?"
        )

        velocity = st.slider(
            "Transactions in Last 24 Hours",
            min_value=0, max_value=30, value=2,
            help="How many transactions has this card made in the last 24 hours?"
        )

        st.markdown("**Cardholder's Average Monthly Spend ($)**")
        avg_col1, avg_col2 = st.columns(2)
        with avg_col1:
            avg_dollars = st.number_input("Dollars ", min_value=0,
                                           max_value=9999, value=200, step=1)
        with avg_col2:
            avg_cents = st.number_input("Cents ", min_value=0,
                                         max_value=99, value=0, step=1)
        avg_spend = avg_dollars + avg_cents / 100
        st.caption(f"Monthly average: **${avg_spend:.2f}**")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Transaction Flags</div>',
                    unsafe_allow_html=True)

        col_c, col_d = st.columns(2)
        with col_c:
            is_online = st.radio("Online Transaction?", options=[0,1],
                                  format_func=lambda x: "Yes" if x==1 else "No",
                                  horizontal=True)
            is_international = st.radio("International Transaction?",
                                         options=[0,1],
                                         format_func=lambda x: "Yes" if x==1 else "No",
                                         horizontal=True)
        with col_d:
            card_present = st.radio("Card Physically Present?", options=[0,1],
                                     format_func=lambda x: "Yes" if x==1 else "No",
                                     index=1, horizontal=True)
            is_round = st.radio("Round Amount?", options=[0,1],
                                 format_func=lambda x: "Yes" if x==1 else "No",
                                 horizontal=True)

        merchant = st.selectbox(
            "Merchant Category",
            options=['grocery','restaurant','gas_station','online_retail',
                     'electronics','travel','entertainment','pharmacy',
                     'clothing','atm_withdrawal','other']
        )

        predict_btn = st.button("🔍  Analyse Transaction")

    with col_right:
        if predict_btn:
            amount_to_avg = round(amount / (avg_spend + 1), 3)

            merchant_cols = {
                f'merchant_{m}': 0 for m in
                ['grocery','restaurant','gas_station','online_retail',
                 'electronics','travel','entertainment','pharmacy',
                 'clothing','atm_withdrawal']
            }
            if f'merchant_{merchant}' in merchant_cols:
                merchant_cols[f'merchant_{merchant}'] = 1

            input_dict = {
                'amount':                amount,
                'hour_of_day':           hour,
                'day_of_week':           day,
                'distance_from_home_km': distance,
                'transactions_last_24h': velocity,
                'avg_spend_last_30d':    avg_spend,
                'is_online':             is_online,
                'is_international':      is_international,
                'card_present':          card_present,
                'is_round_amount':       is_round,
                'amount_to_avg_ratio':   amount_to_avg,
                **merchant_cols
            }

            input_df     = pd.DataFrame([input_dict])[feature_cols]
            input_scaled = scaler.transform(input_df)

            prediction  = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0][1]
            fraud_pct   = round(probability * 100, 2)

            if fraud_pct >= 70:
                risk_level  = "HIGH"
                badge_class = "badge-high"
            elif fraud_pct >= 35:
                risk_level  = "MEDIUM"
                badge_class = "badge-medium"
            else:
                risk_level  = "LOW"
                badge_class = "badge-low"

            # Save to session state for Next Steps tab
            st.session_state.last_prediction = int(prediction)
            st.session_state.last_fraud_pct  = fraud_pct
            st.session_state.last_risk_level = risk_level
            st.session_state.last_inputs     = {
                'amount':          amount,
                'avg_spend':       avg_spend,
                'is_online':       is_online,
                'is_international':is_international,
                'card_present':    card_present,
                'velocity':        velocity,
                'distance':        distance,
                'is_round':        is_round,
                'hour':            hour,
                'amount_to_avg':   amount_to_avg,
                'merchant':        merchant
            }

            if prediction == 1:
                st.markdown(f"""
                <div class="verdict-fraud">
                    <div style="font-size:48px; margin-bottom:8px;">🚨</div>
                    <div style="color:#fca5a5; font-size:13px;
                                font-weight:700; letter-spacing:2px;">VERDICT</div>
                    <div style="color:#ffffff; font-size:32px;
                                font-weight:900; margin:8px 0;">FRAUDULENT</div>
                    <div style="color:#fca5a5; font-size:15px;">
                        This transaction has been flagged as suspicious
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="verdict-safe">
                    <div style="font-size:48px; margin-bottom:8px;">✅</div>
                    <div style="color:#6ee7b7; font-size:13px;
                                font-weight:700; letter-spacing:2px;">VERDICT</div>
                    <div style="color:#ffffff; font-size:32px;
                                font-weight:900; margin:8px 0;">LEGITIMATE</div>
                    <div style="color:#6ee7b7; font-size:15px;">
                        This transaction appears to be genuine
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            m1, m2 = st.columns(2)
            with m1:
                st.metric("Fraud Probability", f"{fraud_pct:.2f}%")
            with m2:
                st.markdown(f"""
                <div style="background:#ffffff; border-radius:12px;
                            padding:16px 20px; border:1px solid #e2e8f0;
                            box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                    <div style="font-size:13px; font-weight:700;
                                color:#6b7280; margin-bottom:6px;">RISK LEVEL</div>
                    <span class="{badge_class}">{risk_level}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=fraud_pct,
                number={'suffix': '%', 'font': {'size': 28, 'color': '#1e40af'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1,
                             'tickcolor': '#94a3b8'},
                    'bar': {'color': '#ef4444' if fraud_pct >= 70
                            else '#f59e0b' if fraud_pct >= 35
                            else '#10b981'},
                    'bgcolor': '#f8fafc',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0,  35],  'color': '#d1fae5'},
                        {'range': [35, 70],  'color': '#fef3c7'},
                        {'range': [70, 100], 'color': '#fee2e2'}
                    ],
                    'threshold': {
                        'line': {'color': '#1e40af', 'width': 3},
                        'thickness': 0.8, 'value': fraud_pct
                    }
                },
                title={'text': "Fraud Risk Score",
                       'font': {'size': 14, 'color': '#6b7280'}}
            ))
            fig.update_layout(
                height=260,
                margin=dict(t=40, b=0, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#374151'}
            )
            st.plotly_chart(fig, width='stretch')

            # Flagged features
            st.markdown('<div class="section-header">Why was this flagged?</div>',
                        unsafe_allow_html=True)
            flags = []
            if is_online == 1:
                flags.append(("🌐", "Online transaction", "Highest fraud risk channel"))
            if velocity >= 5:
                flags.append(("⚡", f"{velocity} transactions in 24h",
                               "Unusual transaction velocity"))
            if distance >= 50:
                flags.append(("📍", f"{distance}km from home",
                               "Transaction far from home location"))
            if is_round == 1:
                flags.append(("💲", "Round amount",
                               "Suspiciously round transaction value"))
            if is_international == 1:
                flags.append(("✈️", "International transaction",
                               "Cross-border transaction detected"))
            if card_present == 0:
                flags.append(("💳", "Card not present",
                               "Physical card was not used"))
            if amount_to_avg > 5:
                flags.append(("📈", f"{amount_to_avg:.1f}x avg spend",
                               "Amount far exceeds typical spending"))

            if flags:
                for icon, title, desc in flags:
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:12px;
                                padding:10px 0; border-bottom:1px solid #f1f5f9;">
                        <div style="font-size:20px;">{icon}</div>
                        <div>
                            <div style="font-weight:700; color:#1e293b;
                                        font-size:14px;">{title}</div>
                            <div style="color:#6b7280; font-size:12px;">{desc}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="color:#6b7280; font-size:14px; padding:12px 0;">
                    No major risk flags detected for this transaction.
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.info("💡 Head to the **Next Steps** tab for guidance on what to do now.")

        else:
            st.markdown("""
            <div style="display:flex; flex-direction:column;
                        align-items:center; justify-content:center;
                        height:400px; text-align:center;">
                <div style="font-size:64px; margin-bottom:16px;">🛡️</div>
                <div style="color:#1e40af; font-size:22px;
                            font-weight:800; margin-bottom:8px;">
                    Ready to Analyse
                </div>
                <div style="color:#94a3b8; font-size:16px;
                            max-width:300px; line-height:1.6;">
                    Fill in the details and click
                    <strong>Analyse Transaction</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 2 — NEXT STEPS
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #1e40af; font-size: 32px; font-weight: 800; margin: 0;">
            Next Steps
        </h2>
        <p style="color: #6b7280; font-size: 16px; margin-top: 6px;">
            Guidance based on your last prediction — plus fraud prevention tips
            and a personal risk assessment.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Context-aware response ─────────────────────────────
    last = st.session_state.last_prediction

    if last is None:
        st.markdown("""
        <div class="alert-waiting">
            <div style="font-size:40px; margin-bottom:12px;">🔍</div>
            <div style="color:#93c5fd; font-size:13px;
                        font-weight:700; letter-spacing:2px;
                        margin-bottom:8px;">NO PREDICTION YET</div>
            <div style="color:#ffffff; font-size:20px;
                        font-weight:800; margin-bottom:8px;">
                Run a prediction first
            </div>
            <div style="color:#93c5fd; font-size:15px;">
                Head to the Predict tab, enter a transaction and click
                Analyse Transaction. The guidance here will update automatically
                based on your result.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif last == 1:
        fraud_pct  = st.session_state.last_fraud_pct
        risk_level = st.session_state.last_risk_level

        st.markdown(f"""
        <div class="alert-fraud">
            <div style="font-size:40px; margin-bottom:12px;">🚨</div>
            <div style="color:#fca5a5; font-size:13px;
                        font-weight:700; letter-spacing:2px;
                        margin-bottom:8px;">FRAUD DETECTED</div>
            <div style="color:#ffffff; font-size:22px;
                        font-weight:900; margin-bottom:8px;">
                Immediate action required
            </div>
            <div style="color:#fca5a5; font-size:15px;">
                This transaction was flagged as fraudulent with
                <strong style="color:white;">{fraud_pct:.2f}%</strong> confidence.
                Follow the steps below immediately.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_left2, col_right2 = st.columns(2, gap="large")

        with col_left2:
            st.markdown('<div class="section-header">🚨 Immediate Actions</div>',
                        unsafe_allow_html=True)

            steps = [
                ("1", "🔒", "Freeze your card immediately",
                 "Contact your bank or use your banking app to temporarily freeze the card to prevent further fraudulent transactions."),
                ("2", "📞", "Call your bank's fraud helpline",
                 "Report the suspicious transaction to your bank immediately. Most banks have a 24/7 fraud line on the back of your card."),
                ("3", "❌", "Dispute the transaction",
                 "Formally dispute the fraudulent charge through your bank's app or website. Most banks will begin an investigation within 24 hours."),
                ("4", "🔍", "Review recent transactions",
                 "Check all transactions from the past 30 days for any other suspicious activity you may have missed."),
                ("5", "🔐", "Change your passwords",
                 "Update passwords for your banking app, email, and any accounts linked to this card — especially if this was an online transaction."),
                ("6", "📋", "File a police report if needed",
                 "For large amounts, file a report with your local police. The report number may be needed by your bank for the investigation."),
            ]

            for num, icon, title, desc in steps:
                st.markdown(f"""
                <div style="background:#ffffff; border-radius:12px;
                            padding:16px 18px; border:1px solid #fee2e2;
                            border-left:4px solid #ef4444;
                            margin-bottom:10px;
                            box-shadow:0 2px 6px rgba(0,0,0,0.04);">
                    <div style="display:flex; align-items:center;
                                gap:10px; margin-bottom:6px;">
                        <div style="background:#fee2e2; color:#991b1b;
                                    border-radius:50%; width:26px; height:26px;
                                    display:flex; align-items:center;
                                    justify-content:center;
                                    font-weight:800; font-size:12px;
                                    flex-shrink:0;">{num}</div>
                        <div style="font-size:18px;">{icon}</div>
                        <div style="font-weight:700; color:#1e293b;
                                    font-size:15px;">{title}</div>
                    </div>
                    <div style="color:#6b7280; font-size:13px;
                                line-height:1.6; padding-left:36px;">
                        {desc}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_right2:
            st.markdown('<div class="section-header">📋 What to Tell Your Bank</div>',
                        unsafe_allow_html=True)

            inputs = st.session_state.last_inputs
            st.markdown(f"""
            <div style="background:#ffffff; border-radius:12px;
                        padding:20px; border:1px solid #e2e8f0;
                        box-shadow:0 2px 6px rgba(0,0,0,0.05);
                        margin-bottom:16px;">
                <div style="color:#1e40af; font-size:13px; font-weight:800;
                            letter-spacing:1px; margin-bottom:12px;">
                    FLAGGED TRANSACTION DETAILS
                </div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div style="display:flex; justify-content:space-between;
                                padding:8px 0; border-bottom:1px solid #f1f5f9;">
                        <span style="color:#6b7280; font-size:14px;">Amount</span>
                        <span style="color:#1e293b; font-weight:700;
                                     font-size:14px;">${inputs['amount']:.2f}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;
                                padding:8px 0; border-bottom:1px solid #f1f5f9;">
                        <span style="color:#6b7280; font-size:14px;">Transaction type</span>
                        <span style="color:#1e293b; font-weight:700;
                                     font-size:14px;">
                            {'Online' if inputs['is_online'] else 'In-person'}
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between;
                                padding:8px 0; border-bottom:1px solid #f1f5f9;">
                        <span style="color:#6b7280; font-size:14px;">Merchant</span>
                        <span style="color:#1e293b; font-weight:700;
                                     font-size:14px;">
                            {inputs['merchant'].replace('_', ' ').title()}
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between;
                                padding:8px 0; border-bottom:1px solid #f1f5f9;">
                        <span style="color:#6b7280; font-size:14px;">International</span>
                        <span style="color:#1e293b; font-weight:700;
                                     font-size:14px;">
                            {'Yes' if inputs['is_international'] else 'No'}
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between;
                                padding:8px 0;">
                        <span style="color:#6b7280; font-size:14px;">Fraud confidence</span>
                        <span style="color:#ef4444; font-weight:800;
                                     font-size:14px;">{fraud_pct:.2f}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-header">📞 Emergency Contacts</div>',
                        unsafe_allow_html=True)

            contacts = [
                ("🏦", "Your bank's fraud line",
                 "Found on the back of your card or on your bank's website"),
                ("🚔", "Cybercrime helpline",
                 "India: 1930 | Report at cybercrime.gov.in"),
                ("📱", "RBI helpline",
                 "14448 — Reserve Bank of India banking ombudsman"),
                ("🔒", "Card network fraud",
                 "Visa: 1800-419-1717 | Mastercard: 1800-102-6627"),
            ]

            for icon, title, detail in contacts:
                st.markdown(f"""
                <div style="background:#eff6ff; border-radius:10px;
                            padding:14px 16px; margin-bottom:8px;
                            border:1px solid #bfdbfe;">
                    <div style="display:flex; align-items:center;
                                gap:10px; margin-bottom:4px;">
                        <span style="font-size:18px;">{icon}</span>
                        <span style="font-weight:700; color:#1e40af;
                                     font-size:14px;">{title}</span>
                    </div>
                    <div style="color:#6b7280; font-size:12px;
                                padding-left:28px;">{detail}</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        fraud_pct = st.session_state.last_fraud_pct

        st.markdown(f"""
        <div class="alert-safe">
            <div style="font-size:40px; margin-bottom:12px;">✅</div>
            <div style="color:#6ee7b7; font-size:13px;
                        font-weight:700; letter-spacing:2px;
                        margin-bottom:8px;">TRANSACTION CLEARED</div>
            <div style="color:#ffffff; font-size:22px;
                        font-weight:900; margin-bottom:8px;">
                This transaction looks legitimate
            </div>
            <div style="color:#6ee7b7; font-size:15px;">
                Fraud probability was only
                <strong style="color:white;">{fraud_pct:.2f}%</strong>.
                No immediate action needed — but staying vigilant is always smart.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">✅ You\'re Good — Stay Vigilant</div>',
                    unsafe_allow_html=True)

        safe_tips = [
            ("🔔", "Enable transaction alerts",
             "Turn on instant SMS/email alerts for every transaction so you know immediately if something unusual happens."),
            ("👀", "Review your statement monthly",
             "Set a reminder to check your full statement once a month for any transactions you don't recognise."),
            ("🔐", "Use strong unique passwords",
             "Never reuse passwords across banking and other sites. Use a password manager if needed."),
            ("📵", "Never share your OTP",
             "No bank, government agency, or courier will ever ask for your OTP. If someone asks — it's a scam."),
        ]

        col_s1, col_s2 = st.columns(2, gap="large")
        for i, (icon, title, desc) in enumerate(safe_tips):
            col = col_s1 if i % 2 == 0 else col_s2
            with col:
                st.markdown(f"""
                <div style="background:#ffffff; border-radius:12px;
                            padding:16px 18px; border:1px solid #d1fae5;
                            border-left:4px solid #10b981;
                            margin-bottom:10px;
                            box-shadow:0 2px 6px rgba(0,0,0,0.04);">
                    <div style="display:flex; align-items:center;
                                gap:10px; margin-bottom:6px;">
                        <div style="font-size:22px;">{icon}</div>
                        <div style="font-weight:700; color:#1e293b;
                                    font-size:15px;">{title}</div>
                    </div>
                    <div style="color:#6b7280; font-size:13px; line-height:1.6;">
                        {desc}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Fraud Prevention Guide ─────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🛡️ Fraud Prevention Guide</div>',
                unsafe_allow_html=True)

    prev_col1, prev_col2, prev_col3 = st.columns(3, gap="large")

    with prev_col1:
        st.markdown("""
        <div style="background:#ffffff; border-radius:14px; padding:20px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);">
            <div style="font-size:28px; margin-bottom:10px;">💳</div>
            <div style="font-weight:800; color:#1e293b; font-size:15px;
                        margin-bottom:12px;">Card Safety</div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Use virtual cards for online shopping
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Never save card details on unknown websites
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Cover the keypad when entering your PIN
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Check the ATM for skimming devices
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with prev_col2:
        st.markdown("""
        <div style="background:#ffffff; border-radius:14px; padding:20px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);">
            <div style="font-size:28px; margin-bottom:10px;">🌐</div>
            <div style="font-weight:800; color:#1e293b; font-size:15px;
                        margin-bottom:12px;">Online Safety</div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Only shop on HTTPS secured websites
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Avoid public Wi-Fi for banking transactions
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Enable two-factor authentication on all accounts
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Never click links in unsolicited bank emails
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with prev_col3:
        st.markdown("""
        <div style="background:#ffffff; border-radius:14px; padding:20px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);">
            <div style="font-size:28px; margin-bottom:10px;">📱</div>
            <div style="font-weight:800; color:#1e293b; font-size:15px;
                        margin-bottom:12px;">Account Monitoring</div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Set daily transaction limits on your card
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Enable international transactions only when travelling
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Review bank statements every week
                </div>
            </div>
            <div class="tip-card">
                <div style="font-weight:600; color:#1e293b; font-size:14px;">
                    Register for SMS alerts for every transaction
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Personal Risk Calculator ───────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Personal Risk Calculator</div>',
                unsafe_allow_html=True)

    if st.session_state.last_inputs is not None:
        inputs = st.session_state.last_inputs

        habits = []

        # Online
        if inputs['is_online'] == 1:
            habits.append(("risky", "🌐",
                            "Online transaction",
                            "Online transactions carry the highest fraud risk — use virtual cards when possible."))
        else:
            habits.append(("safe", "🌐",
                            "In-person transaction",
                            "In-person transactions are significantly safer than online ones."))

        # International
        if inputs['is_international'] == 1:
            habits.append(("risky", "✈️",
                            "International transaction",
                            "International transactions are 10x more likely to be fraudulent. Enable only when needed."))
        else:
            habits.append(("safe", "✈️",
                            "Domestic transaction",
                            "Staying domestic reduces fraud risk significantly."))

        # Card present
        if inputs['card_present'] == 0:
            habits.append(("risky", "💳",
                            "Card not physically present",
                            "Card-not-present transactions are the primary channel for fraud. Be cautious."))
        else:
            habits.append(("safe", "💳",
                            "Card physically present",
                            "Physical card use is much safer than online or phone transactions."))

        # Velocity
        if inputs['velocity'] >= 7:
            habits.append(("risky", "⚡",
                            f"High velocity — {inputs['velocity']} transactions today",
                            "This many transactions in 24 hours is unusual and raises fraud risk."))
        elif inputs['velocity'] >= 4:
            habits.append(("medium", "⚡",
                            f"Moderate velocity — {inputs['velocity']} transactions today",
                            "Slightly elevated activity. Monitor for any unrecognised charges."))
        else:
            habits.append(("safe", "⚡",
                            f"Normal velocity — {inputs['velocity']} transactions today",
                            "Transaction frequency is within normal range."))

        # Distance
        if inputs['distance'] >= 100:
            habits.append(("risky", "📍",
                            f"Far from home — {inputs['distance']:.0f}km",
                            "Transactions far from home are a strong fraud indicator."))
        elif inputs['distance'] >= 30:
            habits.append(("medium", "📍",
                            f"Moderate distance — {inputs['distance']:.0f}km",
                            "Slightly outside typical range. Keep an eye on your alerts."))
        else:
            habits.append(("safe", "📍",
                            f"Close to home — {inputs['distance']:.0f}km",
                            "Transaction location is within your normal range."))

        # Amount vs avg
        if inputs['amount_to_avg'] > 8:
            habits.append(("risky", "📈",
                            f"Spending {inputs['amount_to_avg']:.1f}x your average",
                            "Spending far above your average is a major fraud trigger."))
        elif inputs['amount_to_avg'] > 3:
            habits.append(("medium", "📈",
                            f"Spending {inputs['amount_to_avg']:.1f}x your average",
                            "Slightly above your normal spending. Not alarming but worth noting."))
        else:
            habits.append(("safe", "📈",
                            f"Spending {inputs['amount_to_avg']:.1f}x your average",
                            "Amount is consistent with your typical spending habits."))

        risky_count  = sum(1 for h in habits if h[0] == "risky")
        medium_count = sum(1 for h in habits if h[0] == "medium")
        safe_count   = sum(1 for h in habits if h[0] == "safe")
        total        = len(habits)
        risk_score   = round((risky_count * 2 + medium_count) / (total * 2) * 100)

        # Overall score
        if risk_score >= 60:
            score_color = "#ef4444"
            score_label = "High Risk Profile"
        elif risk_score >= 30:
            score_color = "#f59e0b"
            score_label = "Moderate Risk Profile"
        else:
            score_color = "#10b981"
            score_label = "Low Risk Profile"

        rc1, rc2, rc3, rc4 = st.columns(4)
        with rc1:
            st.metric("Risk Score", f"{risk_score}/100")
        with rc2:
            st.metric("Risk Factors", f"{risky_count} high")
        with rc3:
            st.metric("Watch Items", f"{medium_count} medium")
        with rc4:
            st.metric("Safe Habits", f"{safe_count} good")

        st.markdown("<br>", unsafe_allow_html=True)

        for level, icon, title, advice in habits:
            css_class = f"habit-{level if level != 'medium' else 'medium'}"
            indicator = "🔴" if level == "risky" else "🟡" if level == "medium" else "🟢"
            st.markdown(f"""
            <div class="{css_class}">
                <div style="display:flex; align-items:center;
                            gap:8px; margin-bottom:4px;">
                    <span>{indicator}</span>
                    <span style="font-size:16px;">{icon}</span>
                    <span>{title}</span>
                </div>
                <div style="font-size:12px; opacity:0.85;
                            padding-left:40px; font-weight:400;">
                    {advice}
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#f8fafc; border-radius:12px; padding:24px;
                    border:1px dashed #cbd5e1; text-align:center;
                    color:#94a3b8; font-size:15px;">
            Run a prediction first to see your personalised risk assessment here.
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 3 — MODEL INSIGHTS (XGBoost only)
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #1e40af; font-size: 32px; font-weight: 800; margin: 0;">
            Model Insights
        </h2>
        <p style="color: #6b7280; font-size: 16px; margin-top: 6px;">
            A deep dive into XGBoost — the model powering FraudDetect.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Why XGBoost banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f1b4c, #1a3a6b);
                border-radius: 16px; padding: 28px; margin-bottom: 28px;
                color: white;">
        <div style="font-size: 12px; font-weight: 700; letter-spacing: 2px;
                    color: #93c5fd; margin-bottom: 8px;">
            WHY XGBOOST?
        </div>
        <div style="font-size: 20px; font-weight: 800; margin-bottom: 12px;">
            6 models were trained and compared — XGBoost won on every key metric.
        </div>
        <div style="color: #93c5fd; font-size: 15px; line-height: 1.7;">
            XGBoost builds decision trees sequentially — each new tree focuses on
            correcting the mistakes of the previous one. This boosting approach
            makes it exceptionally good at finding subtle fraud patterns that
            simpler models miss entirely.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics cards
    st.markdown('<div class="section-header">Performance Metrics</div>',
                unsafe_allow_html=True)

    xgb_metrics = results_summary.get('XGBoost', {})
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Accuracy",
                  f"{xgb_metrics.get('Accuracy', 0)*100:.2f}%")
    with m2:
        st.metric("Precision",
                  f"{xgb_metrics.get('Precision', 0):.4f}")
    with m3:
        st.metric("Recall",
                  f"{xgb_metrics.get('Recall', 0):.4f}")
    with m4:
        st.metric("F1 Score",
                  f"{xgb_metrics.get('F1 Score', 0):.4f}")
    with m5:
        st.metric("ROC-AUC",
                  f"{xgb_metrics.get('ROC-AUC', 0):.4f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # What the metrics mean
    metric_col1, metric_col2 = st.columns(2, gap="large")

    with metric_col1:
        st.markdown("""
        <div style="background:#ffffff; border-radius:14px; padding:22px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);
                    margin-bottom:16px;">
            <div class="section-header">Model Performance</div>
            <div style="display:flex; flex-direction:column; gap:0;">
                <div style="padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <div style="font-weight:700; color:#1e293b;
                                font-size:14px; margin-bottom:4px;">
                        99.84% Accuracy
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        Out of every 10,000 transactions it classifies,
                        9,984 are correct.
                    </div>
                </div>
                <div style="padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <div style="font-weight:700; color:#1e293b;
                                font-size:14px; margin-bottom:4px;">
                        96.24% Precision
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        When it flags a transaction as fraud, it is correct
                        96.24% of the time. Very few false alarms.
                    </div>
                </div>
                <div style="padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <div style="font-weight:700; color:#1e293b;
                                font-size:14px; margin-bottom:4px;">
                        96.00% Recall
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        Out of every 100 real fraud cases, it catches 96.
                        Only 4 slip through undetected.
                    </div>
                </div>
                <div style="padding:12px 0;">
                    <div style="font-weight:700; color:#1e293b;
                                font-size:14px; margin-bottom:4px;">
                        0.9995 ROC-AUC
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        Near-perfect ability to distinguish fraud from
                        legitimate transactions. 1.0 would be perfect.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with metric_col2:
        st.markdown("""
        <div style="background:#ffffff; border-radius:14px; padding:22px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);
                    margin-bottom:16px;">
            <div class="section-header">Test Set Results</div>
            <div style="display:flex; flex-direction:column; gap:0;">
                <div style="padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <div style="font-weight:700; color:#065f46;
                                font-size:14px; margin-bottom:4px;">
                        ✅ 384 / 400 fraud cases caught
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        True Positives — real fraud correctly identified
                        and blocked.
                    </div>
                </div>
                <div style="padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <div style="font-weight:700; color:#065f46;
                                font-size:14px; margin-bottom:4px;">
                        ✅ 19,584 / 19,600 legitimate transactions cleared
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        True Negatives — real transactions correctly
                        allowed through.
                    </div>
                </div>
                <div style="padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <div style="font-weight:700; color:#991b1b;
                                font-size:14px; margin-bottom:4px;">
                        ❌ 16 fraud cases missed
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        False Negatives — real fraud that slipped through.
                        The most dangerous error type.
                    </div>
                </div>
                <div style="padding:12px 0;">
                    <div style="font-weight:700; color:#92400e;
                                font-size:14px; margin-bottom:4px;">
                        ⚠️ 16 legitimate transactions wrongly flagged
                    </div>
                    <div style="color:#6b7280; font-size:13px;">
                        False Positives — real customers incorrectly
                        blocked. 0.08% false alarm rate.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature importance chart
    st.markdown('<div class="section-header">What XGBoost Learned to Look For</div>',
                unsafe_allow_html=True)

    feature_names = feature_cols
    importances   = model.feature_importances_

    feat_df = pd.DataFrame({
        'feature':    feature_names,
        'importance': importances
    }).sort_values('importance', ascending=True).tail(12)

    bar_colors = []
    for val in feat_df['importance']:
        if val >= 0.10:
            bar_colors.append('#ef4444')
        elif val >= 0.05:
            bar_colors.append('#f59e0b')
        else:
            bar_colors.append('#60a5fa')

    fig_imp = go.Figure(go.Bar(
        x=feat_df['importance'],
        y=feat_df['feature'],
        orientation='h',
        marker_color=bar_colors,
        text=[f'{v:.4f}' for v in feat_df['importance']],
        textposition='outside',
        textfont=dict(size=12, color='#1e293b')
    ))
    fig_imp.update_layout(
        height=460,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#374151', size=13),
        xaxis=dict(gridcolor='#e2e8f0', title='Importance Score'),
        yaxis=dict(gridcolor='#e2e8f0'),
        margin=dict(t=20, b=20, l=20, r=60),
        showlegend=False
    )
    st.plotly_chart(fig_imp, width='stretch')

    # Legend
    st.markdown("""
    <div style="display:flex; gap:20px; margin-top:-8px; margin-bottom:16px;">
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#ef4444;
                        border-radius:2px;"></div>
            <span style="color:#6b7280; font-size:13px;">High importance (>10%)</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#f59e0b;
                        border-radius:2px;"></div>
            <span style="color:#6b7280; font-size:13px;">Medium importance (5-10%)</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#60a5fa;
                        border-radius:2px;"></div>
            <span style="color:#6b7280; font-size:13px;">Low importance (<5%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key insight
    st.markdown("""
    <div style="background:#eff6ff; border-radius:12px; padding:20px;
                border-left:4px solid #1e40af; margin-top:8px;">
        <div style="font-weight:800; color:#1e40af; font-size:14px;
                    margin-bottom:6px;">Key insight</div>
        <div style="color:#374151; font-size:14px; line-height:1.7;">
            <strong>is_online (40.2%)</strong> and
            <strong>transactions_last_24h (25.6%)</strong> together account
            for 65% of all decisions. The model independently confirmed
            what our data analysis found — online transactions and high
            velocity are by far the strongest fraud signals.
            Notably, distance_from_home ranked lower than expected because
            that signal is already captured indirectly by is_online and
            is_international.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="color: #1e40af; font-size: 32px; font-weight: 800; margin: 0;">
            About FraudDetect
        </h2>
        <p style="color: #6b7280; font-size: 16px; margin-top: 6px;">
            A machine learning project built to detect credit card fraud in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div style="background:#ffffff; border-radius:16px; padding:28px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);
                    margin-bottom:20px;">
            <div class="section-header">The Problem</div>
            <p style="color:#374151; font-size:15px; line-height:1.8;">
                Credit card fraud costs billions globally every year.
                Traditional rule-based systems miss complex fraud patterns
                and generate too many false alarms — blocking legitimate
                customers and missing real threats.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#ffffff; border-radius:16px; padding:28px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);">
            <div class="section-header">Tech Stack</div>
            <div style="display:flex; flex-wrap:wrap; gap:10px;">
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">Python</span>
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">XGBoost</span>
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">Scikit-learn</span>
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">SMOTE</span>
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">Streamlit</span>
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">Plotly</span>
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">Pandas</span>
                <span style="background:#dbeafe; color:#1e40af; padding:6px 16px;
                             border-radius:20px; font-weight:700;
                             font-size:14px;">NumPy</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#ffffff; border-radius:16px; padding:28px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);
                    margin-bottom:20px;">
            <div class="section-header">The Approach</div>
            <p style="color:#374151; font-size:15px; line-height:1.8;">
                We trained and compared 6 machine learning algorithms on a
                synthetic dataset of 100,000 transactions with a realistic
                2% fraud rate. SMOTE balanced the training set from a 49:1
                ratio to 1:1 — forcing the model to genuinely learn what
                fraud looks like.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#ffffff; border-radius:16px; padding:28px;
                    border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);">
            <div class="section-header">Key Stats</div>
            <div style="display:flex; flex-direction:column; gap:0;">
                <div style="display:flex; justify-content:space-between;
                            padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <span style="color:#6b7280; font-size:14px;">
                        Training data
                    </span>
                    <span style="color:#1e40af; font-weight:800;">
                        100,000 transactions
                    </span>
                </div>
                <div style="display:flex; justify-content:space-between;
                            padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <span style="color:#6b7280; font-size:14px;">
                        Fraud rate
                    </span>
                    <span style="color:#1e40af; font-weight:800;">2%</span>
                </div>
                <div style="display:flex; justify-content:space-between;
                            padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <span style="color:#6b7280; font-size:14px;">
                        Models compared
                    </span>
                    <span style="color:#1e40af; font-weight:800;">6</span>
                </div>
                <div style="display:flex; justify-content:space-between;
                            padding:12px 0; border-bottom:1px solid #f1f5f9;">
                    <span style="color:#6b7280; font-size:14px;">
                        Best model
                    </span>
                    <span style="color:#1e40af; font-weight:800;">XGBoost</span>
                </div>
                <div style="display:flex; justify-content:space-between;
                            padding:12px 0;">
                    <span style="color:#6b7280; font-size:14px;">
                        Fraud caught
                    </span>
                    <span style="color:#1e40af; font-weight:800;">96%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:#9ca3af; font-size:13px;">
        🛡️ Built by Arjuman Sultana &nbsp;·&nbsp;
        AI & Data Science &nbsp;·&nbsp; Machine Learning · Streamlit · Python
    </div>
    """, unsafe_allow_html=True)