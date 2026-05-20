# mizan/app.py
"""
الإصدار البسيط (LTR) - سيعمل كالسابق
"""

import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from config import TXT, INDICATORS_META, N_IND
from components import (render_welcome, render_compass, render_nation_lab,
                        render_cosmic_scene, render_new_lexicon, render_evidence,
                        render_path_geometry, render_new_observatory,
                        render_new_healer, render_new_network,
                        render_new_academy, render_new_ahlulbayt,
                        render_new_appendices, render_new_the_one_law,
                        render_new_spiritual_energy, render_new_civilization_cycle,
                        render_social_fabric)

st.set_page_config(
    page_title=TXT("⚖️ مختبر الميزان", "⚖️ The Mizan Lab"),
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
.stApp { font-family: 'Cairo', sans-serif; }
.golden-title { font-size: 2.8em; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.verse-text { text-align: center; color: #FFD700; font-size: 1.3em; line-height: 2.2; font-family: 'Amiri Quran', serif; }
</style>
""", unsafe_allow_html=True)

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

# عرض الشريط الجانبي والمحتوى بالترتيب العادي (LTR)
with st.sidebar:
    st.markdown("### 🧭 قائمة سريعة")
    # أضف أزرارًا أو روابط سريعة هنا
    if st.button(TXT("🇬🇧 English", "🇸🇦 العربية"), key="btn_lang_sidebar"):
        st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
        st.rerun()

# عرض العنوان
col_icon1, col_title, col_icon2 = st.columns([1, 6, 1])
with col_icon1:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{TXT('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
with col_icon2:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)

# عرض الآية وزر اللغة
st.markdown(f"""
<div class='verse-text'>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    <br><span style='font-size:0.8em;'>S = W x B | ق = ١٠٠ = الحق = الميزان</span>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button(TXT("English", "العربية"), key="btn_lang_main", use_container_width=True):
        st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
        st.rerun()

st.markdown("---")
render_welcome()

# عرض التبويبات
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs([
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
    TXT("🏴 آل البيت", "🏴 Ahlul Bayt"),
    TXT("📚 الملاحق", "📚 Appendices"),
    TXT("⚛️ القانون الواحد", "⚛️ The One Law"),
    TXT("⚡ الطاقة الروحية", "⚡ Spiritual Energy"),
    TXT("🔄 الدورة الحضارية", "🔄 Civilization Cycle"),
    TXT("🧬 النسيج الاجتماعي", "🧬 Social Fabric")
])

with tab1: render_compass()
with tab2: render_nation_lab()
with tab3: render_cosmic_scene()
with tab4: render_new_lexicon()
with tab5: render_evidence()
with tab6: render_path_geometry()
with tab7: render_new_observatory()
with tab8: render_new_healer()
with tab9: render_new_network()
with tab10: render_new_academy()
with tab11: render_new_ahlulbayt()
with tab12: render_new_appendices()
with tab13: render_new_the_one_law()
with tab14: render_new_spiritual_energy()
with tab15: render_new_civilization_cycle()
with tab16: render_social_fabric()

st.markdown("---")
st.markdown(f"<div style='text-align:center;color:#888;'>{TXT('© 2026 علي عادل العاطفي', '© 2026 Ali Adel Alatifi')}</div>", unsafe_allow_html=True)
