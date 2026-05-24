# mizan/app.py
"""
المدخل الرئيسي لتطبيق مختبر الميزان
يدعم الترجمة الكاملة واتجاه RTL/LTR
التبويبات الـ 16: البوصلة، مختبر الأمة، المشهد الكوني، الصراط، الشواهد، المرصد (الرادار الأخلاقي)، طبيب القلوب، شبكة الناجين، الجامعة، آل البيت، محاكي المجتمع، القانون الواحد، دورة الصلاة، الطاقة الروحية، المعجم الهندسي، الدليل المرجعي.
"""

import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from config import TXT, INDICATORS_META, N_IND
from components import (render_welcome, render_compass, render_nation_lab,
                        render_cosmic_scene, render_evidence, render_path_geometry,
                        render_new_observatory, render_new_healer, render_new_network,
                        render_new_academy, render_new_ahlulbayt, render_social_fabric,
                        render_new_the_one_law, render_new_prayer_cycle,
                        render_new_spiritual_energy, render_new_lexicon)
from ui_enhancements import apply_global_css, render_enhanced_sidebar, render_enhanced_header, render_enhanced_footer

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
# تطبيق الأنماط CSS
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
    st.session_state.spiritual_noor = 0.6
    st.session_state.spiritual_raan = 0.2
    st.session_state.spiritual_conductivity = 0.7
    st.session_state.spiritual_multiplier = 1.0
    st.session_state.prayer_status = 0.5
    st.session_state.patience_tank = 0.5
    st.session_state.maun_today = False
    st.session_state.maun_streak = 0
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
# التبويبات الـ 16
# =============================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs([
    TXT("🧍 البوصلة", "🧍 Compass"),
    TXT("🏛️ مختبر الأمة", "🏛️ Nation Lab"),
    TXT("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    TXT("📐 هندسة الصراط", "📐 Path Geometry"),
    TXT("📜 الشواهد", "📜 Evidence"),
    TXT("🌍 المرصد الأخلاقي", "🌍 Moral Observatory"),
    TXT("🩺 طبيب القلوب", "🩺 Healer"),
    TXT("🤝 شبكة الناجين", "🤝 Network"),
    TXT("🎓 الجامعة", "🎓 Academy"),
    TXT("🏴 آل البيت", "🏴 Ahlul Bayt"),
    TXT("🧬 محاكي المجتمع", "🧬 Social Fabric"),
    TXT("⚛️ القانون الواحد", "⚛️ The One Law"),
    TXT("🔄 دورة الصلاة", "🔄 Prayer Cycle"),
    TXT("⚡ الطاقة الروحية", "⚡ Spiritual Energy"),
    TXT("📖 المعجم الهندسي", "📖 Geometric Lexicon"),
    TXT("📚 الدليل المرجعي", "📚 Reference Guide"),
])

with tab1:
    render_compass()

with tab2:
    render_nation_lab()

with tab3:
    render_cosmic_scene()

with tab4:
    render_path_geometry()

with tab5:
    render_evidence()

with tab6:
    render_new_observatory()

with tab7:
    render_new_healer()

with tab8:
    render_new_network()

with tab9:
    render_new_academy()

with tab10:
    render_new_ahlulbayt()

with tab11:
    render_social_fabric()

with tab12:
    render_new_the_one_law()

with tab13:
    render_new_prayer_cycle()

with tab14:
    render_new_spiritual_energy()

with tab15:
    render_new_lexicon()

# =============================================
# التذييل
# =============================================
render_enhanced_footer()
