# mizan/app.py
"""
المدخل الرئيسي لتطبيق مختبر الميزان
يدعم الترجمة الكاملة واتجاه RTL/LTR
"""

import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from config import TXT, INDICATORS_META, N_IND
from components import (render_compass, render_nation_lab,
                        render_cosmic_scene, render_evidence,
                        render_path_geometry, render_new_observatory,
                        render_new_healer, render_new_network,
                        render_new_academy, render_new_ahlulbayt,
                        render_new_the_one_law, render_new_social_fabric)
from welcome import render_welcome
from reference import render_reference
from ui_enhancements import apply_global_css, render_enhanced_sidebar, render_enhanced_header, render_enhanced_footer

# =============================================
# دوال مساعدة للترجمة والاتجاه
# =============================================
def set_rtl():
    st.markdown("""
    <style>
    html, body, .stApp { direction: rtl; text-align: right; }
    .stMarkdown, .stText, .stInfo, .stSuccess, .stWarning, .stError { text-align: right; }
    [data-testid="stSidebar"] {
        left: auto !important;
        right: 0 !important;
    }
    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        margin-right: 300px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def set_ltr():
    st.markdown("""
    <style>
    html, body, .stApp { direction: ltr; text-align: left; }
    .stMarkdown, .stText, .stInfo, .stSuccess, .stWarning, .stError { text-align: left; }
    [data-testid="stSidebar"] {
        left: 0 !important;
        right: auto !important;
    }
    [data-testid="stAppViewContainer"] {
        margin-left: 300px !important;
        margin-right: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================
# إعدادات الصفحة
# =============================================
st.set_page_config(
    page_title=TXT("⚖️ مختبر الميزان", "⚖️ The Mizan Lab"),
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# الأنماط CSS
# =============================================
apply_global_css()

# =============================================
# تهيئة متغيرات الجلسة
# =============================================
if 'init' not in st.session_state:
    st.session_state.lang = "ar"
    st.session_state.slider_values = {f"V{i}": 0.0 for i in range(N_IND)}
    st.session_state.slider_values["W_pure"] = True
    st.session_state.slider_values["E_val"] = 0.5
    st.session_state.compass_answers = {}
    st.session_state.live_run = False
    st.session_state.live_init = False
    st.session_state.path_W = [0.5]
    st.session_state.path_B = [0.5]
    st.session_state.path_kappa = [0.0]
    st.session_state.spiritual_nudge = None
    st.session_state.init = True

# =============================================
# ضبط اتجاه الصفحة حسب اللغة
# =============================================
if st.session_state.lang == "ar":
    set_rtl()
else:
    set_ltr()

# =============================================
# الشريط الجانبي
# =============================================
render_enhanced_sidebar()

# =============================================
# العنوان الرئيسي والآية
# =============================================
render_enhanced_header()

st.markdown("---")

# =============================================
# التبويبات الـ 13
# =============================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs([
    TXT("🏠 البداية", "🏠 Home"),
    TXT("🧍 البوصلة", "🧍 Compass"),
    TXT("🏛️ مختبر الأمة", "🏛️ Nation Lab"),
    TXT("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    TXT("🧬 محاكي المجتمع", "🧬 Social Fabric"),
    TXT("📜 الشواهد", "📜 Evidence"),
    TXT("📐 هندسة الصراط", "📐 Path Geometry"),
    TXT("🌍 المرصد", "🌍 Observatory"),
    TXT("🩺 طبيب القلوب", "🩺 Healer"),
    TXT("🤝 شبكة الناجين", "🤝 Network"),
    TXT("🎓 الجامعة", "🎓 Academy"),
    TXT("🏴 آل البيت", "🏴 Ahlul Bayt"),
    TXT("📚 الدليل المرجعي", "📚 Reference")
])

with tab1:
    render_welcome()

with tab2:
    render_compass()

with tab3:
    render_nation_lab()

with tab4:
    render_cosmic_scene()

with tab5:
    render_new_social_fabric()

with tab6:
    render_evidence()

with tab7:
    render_path_geometry()

with tab8:
    render_new_observatory()

with tab9:
    render_new_healer()

with tab10:
    render_new_network()

with tab11:
    render_new_academy()

with tab12:
    render_new_ahlulbayt()

with tab13:
    render_reference()

# =============================================
# التذييل
# =============================================
render_enhanced_footer()
