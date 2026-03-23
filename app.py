import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px

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
    /* White page background */
    .stApp {
        background-color: #f0f4f8;
        color: #1a1a2e;
    }

    /* Hide streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Navbar rectangle */
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
    .navbar-logo {
        font-size: 32px;
    }
    .navbar-title {
        font-size: 32px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .navbar-title span {
        color: #60a5fa;
    }
    .navbar-subtitle {
        font-size: 15px;
        color: #93c5fd;
        margin-top: 3px;
        font-weight: 500;
    }

    /* Tabs inside navbar */
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
        padding: 10px 28px !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        letter-spacing: 0.3px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e40af !important;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(30,64,175,0.5) !important;
    }
    /* Pull tabs up into navbar */
    .stTabs [data-baseweb="tab-list"] {
        margin-top: -72px !important;
        margin-bottom: 32px !important;
        float: right !important;
        width: fit-content !important;
    }
    /* Tab content area */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 8px !important;
    }

    /* Cards */
    .card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 28px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* Section headers */
    .section-header {
        color: #1e40af;
        font-size: 14px;
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

    /* Metric styling */
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

    /* Bigger fonts throughout */
    .stRadio label {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    .stSelectbox label {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    .stSlider label {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    .stNumberInput label {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    h2 {
        font-size: 32px !important;
    }
    p {
        font-size: 16px !important;
    }
    .stRadio > div {
        font-size: 16px !important;
    }
    div[data-testid="stSelectbox"] > div {
        font-size: 16px !important;
    }
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
tab1, tab2, tab3 = st.tabs([
    "🔍  Predict",
    "📊  Model Insights",
    "ℹ️   About"
])

with tab1:
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #1e40af; font-size: 28px; font-weight: 800; margin: 0;">
            Transaction Analysis
        </h2>
        <p style="color: #6b7280; font-size: 16px; margin-top: 6px;">
            Fill in the details below to check whether a transaction is fraudulent.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input form ─────────────────────────────────────────
    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">Transaction Details</div>',
                    unsafe_allow_html=True)

        st.markdown("**Transaction Amount ($)**")
        amt_col1, amt_col2 = st.columns(2)
        with amt_col1:
            dollars = st.number_input(
                "Dollars",
                min_value=0, max_value=19999,
                value=150, step=1
            )
        with amt_col2:
            cents = st.number_input(
                "Cents",
                min_value=0, max_value=99,
                value=0, step=1
            )
        amount = dollars + cents / 100
        st.caption(f"Total amount: **${amount:.2f}**")

        col_a, col_b = st.columns(2)
        with col_a:
            hour = st.slider(
                "Hour of Day",
                min_value=0, max_value=23, value=14,
                help="0 = midnight, 23 = 11pm"
            )
            # Convert to readable time
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
                                        'Saturday','Sunday'][x],
                index=0
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
            avg_dollars = st.number_input(
                "Dollars ",
                min_value=0, max_value=9999,
                value=200, step=1
            )
        with avg_col2:
            avg_cents = st.number_input(
                "Cents ",
                min_value=0, max_value=99,
                value=0, step=1
            )
        avg_spend = avg_dollars + avg_cents / 100
        st.caption(f"Monthly average: **${avg_spend:.2f}**")

        st.markdown('<div class="section-header">Transaction Flags</div>',
                    unsafe_allow_html=True)

        col_c, col_d = st.columns(2)
        with col_c:
            is_online = st.radio(
                "Online Transaction?",
                options=[0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                horizontal=True
            )
            is_international = st.radio(
                "International Transaction?",
                options=[0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                horizontal=True
            )
        with col_d:
            card_present = st.radio(
                "Card Physically Present?",
                options=[0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                index=1,
                horizontal=True
            )
            is_round = st.radio(
                "Round Amount?",
                options=[0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                horizontal=True
            )

        merchant = st.selectbox(
            "Merchant Category",
            options=['grocery', 'restaurant', 'gas_station',
                     'online_retail', 'electronics', 'travel',
                     'entertainment', 'pharmacy', 'clothing',
                     'atm_withdrawal', 'other']
        )


        predict_btn = st.button("🔍  Analyse Transaction")

    # ── Results ────────────────────────────────────────────
    with col_right:
        if predict_btn:
            # Build feature vector
            amount_to_avg = round(amount / (avg_spend + 1), 3)

            merchant_cols = {
                f'merchant_{m}': 0 for m in
                ['grocery','restaurant','gas_station','online_retail',
                 'electronics','travel','entertainment','pharmacy',
                 'clothing','atm_withdrawal']
            }
            merchant_cols[f'merchant_{merchant}'] = 1

            input_dict = {
                'amount':                 amount,
                'hour_of_day':            hour,
                'day_of_week':            day,
                'distance_from_home_km':  distance,
                'transactions_last_24h':  velocity,
                'avg_spend_last_30d':     avg_spend,
                'is_online':              is_online,
                'is_international':       is_international,
                'card_present':           card_present,
                'is_round_amount':        is_round,
                'amount_to_avg_ratio':    amount_to_avg,
                **merchant_cols
            }

            input_df = pd.DataFrame([input_dict])[feature_cols]
            input_scaled = scaler.transform(input_df)

            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0][1]
            fraud_pct   = round(probability * 100, 2)

            # Risk level
            if fraud_pct >= 70:
                risk_level  = "HIGH"
                badge_class = "badge-high"
            elif fraud_pct >= 35:
                risk_level  = "MEDIUM"
                badge_class = "badge-medium"
            else:
                risk_level  = "LOW"
                badge_class = "badge-low"

            # Verdict
            if prediction == 1:
                st.markdown(f"""
                <div class="verdict-fraud">
                    <div style="font-size:48px; margin-bottom:8px;">🚨</div>
                    <div style="color:#fca5a5; font-size:13px;
                                font-weight:700; letter-spacing:2px;">
                        VERDICT
                    </div>
                    <div style="color:#ffffff; font-size:32px;
                                font-weight:900; margin:8px 0;">
                        FRAUDULENT
                    </div>
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
                                font-weight:700; letter-spacing:2px;">
                        VERDICT
                    </div>
                    <div style="color:#ffffff; font-size:32px;
                                font-weight:900; margin:8px 0;">
                        LEGITIMATE
                    </div>
                    <div style="color:#6ee7b7; font-size:15px;">
                        This transaction appears to be genuine
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Metrics row
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Fraud Probability", f"{fraud_pct:.2f}%")
            with m2:
                st.markdown(f"""
                <div style="background:#ffffff; border-radius:12px;
                            padding:16px 20px; border:1px solid #e2e8f0;
                            box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                    <div style="font-size:13px; font-weight:700;
                                color:#6b7280; margin-bottom:6px;">
                        RISK LEVEL
                    </div>
                    <span class="{badge_class}">{risk_level}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=fraud_pct,
                number={'suffix': '%', 'font': {'size': 28,
                                                 'color': '#1e40af'}},
                gauge={
                    'axis': {'range': [0, 100],
                             'tickwidth': 1,
                             'tickcolor': '#94a3b8'},
                    'bar': {'color': '#ef4444' if fraud_pct >= 70
                            else '#f59e0b' if fraud_pct >= 35
                            else '#10b981'},
                    'bgcolor': '#f8fafc',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 35],   'color': '#d1fae5'},
                        {'range': [35, 70],  'color': '#fef3c7'},
                        {'range': [70, 100], 'color': '#fee2e2'}
                    ],
                    'threshold': {
                        'line': {'color': '#1e40af', 'width': 3},
                        'thickness': 0.8,
                        'value': fraud_pct
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
            st.plotly_chart(fig, use_container_width=True)

            # Flagged features
            st.markdown('<div class="section-header">Why was this flagged?</div>',
                        unsafe_allow_html=True)

            flags = []
            if is_online == 1:
                flags.append(("🌐", "Online transaction",
                               "Highest fraud risk channel"))
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
                    <div style="display:flex; align-items:center;
                                gap:12px; padding:10px 0;
                                border-bottom:1px solid #f1f5f9;">
                        <div style="font-size:20px;">{icon}</div>
                        <div>
                            <div style="font-weight:700; color:#1e293b;
                                        font-size:14px;">{title}</div>
                            <div style="color:#6b7280;
                                        font-size:12px;">{desc}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="color:#6b7280; font-size:14px;
                            padding:12px 0;">
                    No major risk flags detected for this transaction.
                </div>
                """, unsafe_allow_html=True)


        else:
            # Placeholder before prediction
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
                    Fill in the transaction details and click
                    <strong>Analyse Transaction</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #1e40af; font-size: 32px;
                   font-weight: 800; margin: 0;">
            Model Performance
        </h2>
        <p style="color: #6b7280; font-size: 16px; margin-top: 6px;">
            Comparing all 6 algorithms trained on the same dataset.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Best model highlight ───────────────────────────────
    best  = max(results_summary,
                key=lambda x: results_summary[x]['F1 Score'])
    bm    = results_summary[best]

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0f1b4c, #1a3a6b);
                border-radius: 16px; padding: 28px;
                margin-bottom: 28px; color: white;">
        <div style="font-size: 12px; font-weight: 700;
                    letter-spacing: 2px; color: #93c5fd;
                    margin-bottom: 8px;">
            BEST PERFORMING MODEL
        </div>
        <div style="font-size: 32px; font-weight: 900;
                    margin-bottom: 16px;">
            {best}
        </div>
        <div style="display: flex; gap: 40px; flex-wrap: wrap;">
            <div>
                <div style="color:#93c5fd; font-size:12px;
                            font-weight:700;">ACCURACY</div>
                <div style="font-size:24px; font-weight:800;">
                    {bm['Accuracy']*100:.2f}%
                </div>
            </div>
            <div>
                <div style="color:#93c5fd; font-size:12px;
                            font-weight:700;">F1 SCORE</div>
                <div style="font-size:24px; font-weight:800;">
                    {bm['F1 Score']:.4f}
                </div>
            </div>
            <div>
                <div style="color:#93c5fd; font-size:12px;
                            font-weight:700;">ROC-AUC</div>
                <div style="font-size:24px; font-weight:800;">
                    {bm['ROC-AUC']:.4f}
                </div>
            </div>
            <div>
                <div style="color:#93c5fd; font-size:12px;
                            font-weight:700;">PRECISION</div>
                <div style="font-size:24px; font-weight:800;">
                    {bm['Precision']:.4f}
                </div>
            </div>
            <div>
                <div style="color:#93c5fd; font-size:12px;
                            font-weight:700;">RECALL</div>
                <div style="font-size:24px; font-weight:800;">
                    {bm['Recall']:.4f}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metrics table ──────────────────────────────────────
    st.markdown('<div class="section-header">All Models Comparison</div>',
                unsafe_allow_html=True)

    table_data = []
    for name, metrics in results_summary.items():
        table_data.append({
            'Model':     name,
            'Accuracy':  f"{metrics['Accuracy']*100:.2f}%",
            'Precision': f"{metrics['Precision']:.4f}",
            'Recall':    f"{metrics['Recall']:.4f}",
            'F1 Score':  f"{metrics['F1 Score']:.4f}",
            'ROC-AUC':   f"{metrics['ROC-AUC']:.4f}"
        })

    table_df = pd.DataFrame(table_data)
    table_df = table_df.sort_values('F1 Score', ascending=False)
    st.dataframe(table_df, use_container_width=True, hide_index=True)

    # ── Bar charts ─────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Visual Comparison</div>',
                unsafe_allow_html=True)

    metrics_list  = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC-AUC']
    model_names   = list(results_summary.keys())
    chart_colors  = ['#4C9BE8','#E8944C','#E85D5D',
                     '#5DBE85','#9B5DE8','#E8D45D']

    selected_metric = st.selectbox(
        "Select metric to visualise",
        options=metrics_list,
        index=3
    )

    values = [results_summary[m][selected_metric] for m in model_names]
    best_idx = values.index(max(values))

    bar_colors = [
        '#1e40af' if i == best_idx else chart_colors[i]
        for i in range(len(model_names))
    ]

    fig_bar = go.Figure(go.Bar(
        x=model_names,
        y=values,
        marker_color=bar_colors,
        text=[f'{v:.4f}' for v in values],
        textposition='outside',
        textfont=dict(size=13, color='#1e293b')
    ))

    fig_bar.update_layout(
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#374151', size=13),
        yaxis=dict(
            range=[min(values)*0.97, min(max(values)*1.03, 1.0)],
            gridcolor='#e2e8f0',
            tickformat='.3f'
        ),
        xaxis=dict(gridcolor='#e2e8f0'),
        margin=dict(t=40, b=20, l=20, r=20),
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── ROC curve ─────────────────────────────────────────
    st.markdown('<div class="section-header">ROC-AUC Scores</div>',
                unsafe_allow_html=True)

    fig_roc = go.Figure()
    for i, (name, metrics) in enumerate(results_summary.items()):
        fig_roc.add_trace(go.Bar(
            name=name,
            x=[name],
            y=[metrics['ROC-AUC']],
            marker_color=chart_colors[i],
            text=f"{metrics['ROC-AUC']:.4f}",
            textposition='outside',
            textfont=dict(size=13)
        ))

    fig_roc.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#374151', size=13),
        yaxis=dict(
            range=[0.95, 1.001],
            gridcolor='#e2e8f0',
            tickformat='.3f',
            title='ROC-AUC Score'
        ),
        xaxis=dict(gridcolor='#e2e8f0'),
        margin=dict(t=40, b=20, l=20, r=20),
        showlegend=False
    )
    st.plotly_chart(fig_roc, use_container_width=True)

with tab3:
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="color: #1e40af; font-size: 32px;
                   font-weight: 800; margin: 0;">
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
        <div style="background:#ffffff; border-radius:16px;
                    padding:28px; border:1px solid #e2e8f0;
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
        <div style="background:#ffffff; border-radius:16px;
                    padding:28px; border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);
                    margin-bottom:20px;">
            <div class="section-header">The Approach</div>
            <p style="color:#374151; font-size:15px; line-height:1.8;">
                We trained and compared 6 machine learning algorithms on a
                synthetic dataset of 100,000 transactions with a realistic
                2% fraud rate. SMOTE was used to balance the dataset before
                training — ensuring the model genuinely learns fraud patterns
                rather than taking the easy route of predicting everything
                as normal.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#ffffff; border-radius:16px;
                    padding:28px; border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);
                    margin-bottom:20px;">
            <div class="section-header">The Result</div>
            <p style="color:#374151; font-size:15px; line-height:1.8;">
                XGBoost emerged as the best model with 99.84% accuracy,
                an F1 score of 0.9612 and a near-perfect ROC-AUC of 0.9995.
                It catches 96% of all real fraud while only raising false
                alarms on 0.08% of legitimate transactions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#ffffff; border-radius:16px;
                    padding:28px; border:1px solid #e2e8f0;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);
                    margin-bottom:20px;">
            <div class="section-header">Tech Stack</div>
            <div style="display:flex; flex-wrap:wrap; gap:10px;">
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">Python</span>
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">XGBoost</span>
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">Scikit-learn</span>
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">SMOTE</span>
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">Streamlit</span>
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">Plotly</span>
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">Pandas</span>
                <span style="background:#dbeafe; color:#1e40af;
                             padding:6px 16px; border-radius:20px;
                             font-weight:700; font-size:14px;">NumPy</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Key stats ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Key Stats</div>',
                unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Training Data", "100,000", "transactions")
    with s2:
        st.metric("Fraud Rate", "2.00%", "realistic imbalance")
    with s3:
        st.metric("Models Tested", "6", "algorithms compared")
    with s4:
        st.metric("Best F1 Score", "0.9612", "XGBoost")