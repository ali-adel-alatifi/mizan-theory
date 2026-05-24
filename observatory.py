# mizan/observatory.py
"""
الرادار الأخلاقي للعالم الرقمي
يطبق معادلة الميزان على المشاعر والاتجاهات من العالم الرقمي
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from logic import calculate_S
from live_data import fetch_live_indicators, build_world_data
from config import TXT  # ✅ هذا هو السطر المهم

def fix_rtl_display():
    st.markdown("""
    <style>
    div, p, h1, h2, h3, h4, h5, h6, span, strong, em, li, label, .stMarkdown, .stText {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: plaintext !important;
    }
    .stTitle, .stHeader, .stSubheader { direction: rtl !important; text-align: right !important; }
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError { direction: rtl !important; text-align: right !important; }
    .stDataFrame { direction: rtl !important; }
    </style>
    """, unsafe_allow_html=True)

WORLD_DATA_SIMULATED = [
    # ... (نفس البيانات كما هي)
]

def render_observatory():
    fix_rtl_display()
    
    st.header("🌍 الرادار الأخلاقي للعالم الرقمي")
    st.markdown("### 📡 محطة الرصد الأخلاقية – القانون الكوني الحي")
    st.caption(TXT(
        "يقيس هذا الرادار نبض العالم الرقمي في الزمن الحقيقي، ويطبق معادلة الميزان على المشاعر والاتجاهات.",
        "This radar measures the pulse of the digital world in real-time, applying the Mizan equation to sentiment and trends."
    ))
    
    # ─────────────────────────────────────────
    # اختيار وضع التشغيل
    # ─────────────────────────────────────────
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        mode = st.radio(
            TXT("وضع الرادار", "Radar Mode"),
            [TXT("🖐️ يدوي (تحليل ثابت)", "🖐️ Manual (Static)"), TXT("📡 رادار أخلاقي حي", "📡 Live Ethical Radar")],
            key="observatory_mode"
        )
    
    # ─────────────────────────────────────────
    # جلب البيانات حسب الوضع
    # ─────────────────────────────────────────
    if mode == TXT("🖐️ يدوي (تحليل ثابت)", "🖐️ Manual (Static)"):
        st.caption(TXT("استخدم المنزلقات للتحكم في قيم W و B و E يدويًا.", "Use sliders to control W, B, and E manually."))
        col_w, col_b, col_e = st.columns(3)
        with col_w:
            manual_w = st.slider("W (الولاء)", -1.0, 1.0, 0.5, 0.1, key="manual_w")
        with col_b:
            manual_b = st.slider("B (البراءة)", -1.0, 1.0, 0.5, 0.1, key="manual_b")
        with col_e:
            manual_e = st.slider("E (التمكين)", 0.0, 1.0, 0.5, 0.1, key="manual_e")
        
        live_data = fetch_live_indicators(
            mode="manual",
            manual_values={"sentiment": manual_w, "trend": manual_b, "engagement": manual_e * 1000}
        )
    else:
        st.caption(TXT(
            "📡 الرادار الأخلاقي الحي يستخدم الذكاء الاصطناعي لتحليل المشاعر والاتجاهات من المصادر الحية.",
            "📡 Live Ethical Radar uses AI to analyze sentiment and trends from live sources."
        ))
        live_data = fetch_live_indicators(mode="auto")
    
    # ─────────────────────────────────────────
    # عرض بيانات الرادار
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("📊 بيانات الرادار الأخلاقي", "📊 Ethical Radar Data"))
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    col_s1.metric(TXT("متوسط المشاعر", "Avg Sentiment"), f"{live_data.get('sentiment_avg', 0.0):.2f}")
    col_s2.metric(TXT("اتجاه الاتجاه", "Trend Direction"), f"{live_data.get('trend_direction', 0.0):.2f}")
    col_s3.metric(TXT("التفاعلات", "Engagement"), f"{live_data.get('engagement_count', 0)}")
    col_s4.metric(TXT("حالة الرادار", "Radar Status"), 
                 TXT("🟢 حي", "🟢 Live") if live_data.get("status") == "live" else 
                 TXT("🟡 محاكاة", "🟡 Simulated"))
    
    # عرض نبض العالم الرقمي (مؤشر بصري)
    st.markdown("---")
    st.subheader(TXT("📡 نبض العالم الرقمي", "📡 Digital World Pulse"))
    
    pulse_value = (live_data.get('sentiment_avg', 0.0) + 1) / 2 * 100
    st.progress(int(pulse_value), text=TXT(f"نبض العالم الرقمي: {pulse_value:.1f}%", f"Digital World Pulse: {pulse_value:.1f}%"))
    
    if pulse_value > 70:
        st.success(TXT("🟢 العالم الرقمي في حالة ثبات عالٍ.", "🟢 The digital world is in high stability."))
    elif pulse_value > 50:
        st.info(TXT("🟡 العالم الرقمي في حالة متوسطة.", "🟡 The digital world is in moderate stability."))
    elif pulse_value > 30:
        st.warning(TXT("🟠 العالم الرقمي في حالة انحدار.", "🟠 The digital world is declining."))
    else:
        st.error(TXT("🔴 العالم الرقمي في حالة انهيار.", "🔴 The digital world is collapsing."))
    
    # عرض الخريطة والجدول
    world_list = build_world_data(live_data)
    df = pd.DataFrame(world_list)
    
    fig = px.scatter_geo(
        df,
        locations="iso",
        locationmode="ISO-3",
        size="pop",
        color="worship",
        hover_name="country",
        hover_data={"worship": True, "taghut": True},
        color_continuous_scale="RdYlGn",
        projection="natural earth",
        title=TXT("خريطة الميزان العالمية (تحديث حي)", "Global Mizan Map (Live Update)")
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader(TXT("📊 جدول الأمم – الميزان التفصيلي", "📊 Nations Table – Detailed Mizan"))
    display_cols = ["country", "worship", "taghut", "pop", "gdp"]
    st.dataframe(df[display_cols], hide_index=True, use_container_width=True)
