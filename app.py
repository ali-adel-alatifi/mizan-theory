# mizan/app.py
"""
المدخل الرئيسي لتطبيق مختبر الميزان
يربط جميع الوحدات ويعرض الواجهة
"""

import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# استيراد الوحدات المحلية
from config import TXT, INDICATORS_META, N_IND
from components import (render_welcome, render_compass, render_nation_lab,
                        render_cosmic_scene, render_lexicon, render_evidence,
                        render_path_geometry, render_new_observatory,
                        render_new_healer, render_new_network,
                        render_new_academy, render_new_ahlulbayt)
from ui_enhancements import apply_global_css, render_enhanced_sidebar, render_enhanced_header, render_enhanced_footer

# =============================================
# إعدادات الصفحة
# =============================================
st.set_page_config(
    page_title="⚖️ مختبر الميزان",
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
# الشريط الجانبي
# =============================================
render_enhanced_sidebar()

# =============================================
# العنوان الرئيسي والآية
# =============================================
render_enhanced_header()

st.markdown("---")

# =============================================
# عرض الترحيب ودليل المستخدم
# =============================================
render_welcome()

# =============================================
# التبويبات الإحدى عشر
# =============================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
    TXT("🧍 البوصلة", "🧍 Compass"),
    TXT("🏛️ مختبر الأمة", "🏛️ Nation Lab"),
    TXT("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    TXT("📖 المعجم", "📖 Lexicon"),
    TXT("📜 الشواهد", "📜 Evidence"),
    TXT("📐 الصراط", "📐 Path"),
    TXT("🌍 المرصد", "🌍 Observatory"),
    TXT("🩺 طبيب القلوب", "🩺 Healer"),
    TXT("🤝 شبكة الناجين", "🤝 Network"),
    TXT("🎓 الجامعة", "🎓 Academy"),
    TXT("🏴 آل البيت", "🏴 Ahlul Bayt")
])

with tab1:
    render_compass()

with tab2:
    render_nation_lab()

with tab3:
    render_cosmic_scene()

with tab4:
    render_lexicon()

with tab5:
    render_evidence()

with tab6:
    render_path_geometry()

with tab7:
    render_new_observatory()

with tab8:
    render_new_healer()

with tab9:
    render_new_network()

with tab10:
    render_new_academy()

with tab11:
    render_new_ahlulbayt()

# =============================================
# التذييل
# =============================================
render_enhanced_footer()
