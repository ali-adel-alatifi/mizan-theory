# mizan/app.py
"""
المدخل الرئيسي لتطبيق مختبر الميزان
يدعم الترجمة الكاملة (بدون شريط جانبي - مخصص للهاتف)
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

# =============================================
# إعدادات الصفحة
# =============================================
st.set_page_config(
    page_title=TXT("⚖️ مختبر الميزان", "⚖️ The Mizan Lab"),
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"  # إخفاء الشريط الجانبي تماماً
)

# =============================================
# تنسيق CSS بسيط جداً (لتحسين المظهر فقط)
# =============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
.stApp {
    font-family: 'Cairo', sans-serif;
}
.golden-title {
    font-size: 2.8em !important;
    font-weight: 900 !important;
    text-align: center !important;
    background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 5px 0 !important;
    text-shadow: 0 0 30px rgba(255, 215, 0, 0.3) !important;
    display: block !important;
    width: 100% !important;
}
.verse-text {
    text-align: center !important;
    color: #FFD700 !important;
    font-size: 1.3em !important;
    margin: 15px 0 !important;
    line-height: 2.2 !important;
    font-family: 'Amiri Quran', serif !important;
    word-wrap: break-word !important;
    white-space: normal !important;
    display: block !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

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
# قائمة التنقل (بدلاً من الشريط الجانبي)
# =============================================
selected_tab = st.selectbox(
    TXT("اختر التبويب", "Choose tab"),
    [
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
    ]
)

# =============================================
# عرض المحتوى حسب الاختيار
# =============================================
st.markdown("---")

if selected_tab == TXT("🧍 البوصلة", "🧍 Compass"):
    render_compass()
elif selected_tab == TXT("🏛️ مختبر الأمة", "🏛️ Nation Lab"):
    render_nation_lab()
elif selected_tab == TXT("🌌 المشهد الكوني", "🌌 Cosmic Scene"):
    render_cosmic_scene()
elif selected_tab == TXT("📖 المعجم", "📖 Lexicon"):
    render_new_lexicon()
elif selected_tab == TXT("📜 الشواهد", "📜 Evidence"):
    render_evidence()
elif selected_tab == TXT("📐 الصراط", "📐 Path"):
    render_path_geometry()
elif selected_tab == TXT("🌍 المرصد", "🌍 Observatory"):
    render_new_observatory()
elif selected_tab == TXT("🩺 طبيب القلوب", "🩺 Healer"):
    render_new_healer()
elif selected_tab == TXT("🤝 شبكة الناجين", "🤝 Network"):
    render_new_network()
elif selected_tab == TXT("🎓 الجامعة", "🎓 Academy"):
    render_new_academy()
elif selected_tab == TXT("🏴 آل البيت", "🏴 Ahlul Bayt"):
    render_new_ahlulbayt()
elif selected_tab == TXT("📚 الملاحق", "📚 Appendices"):
    render_new_appendices()
elif selected_tab == TXT("⚛️ القانون الواحد", "⚛️ The One Law"):
    render_new_the_one_law()
elif selected_tab == TXT("⚡ الطاقة الروحية", "⚡ Spiritual Energy"):
    render_new_spiritual_energy()
elif selected_tab == TXT("🔄 الدورة الحضارية", "🔄 Civilization Cycle"):
    render_new_civilization_cycle()
elif selected_tab == TXT("🧬 النسيج الاجتماعي", "🧬 Social Fabric"):
    render_social_fabric()

# =============================================
# العنوان الرئيسي والآية
# =============================================
col_icon1, col_title, col_icon2 = st.columns([1, 6, 1])
with col_icon1:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{TXT('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
with col_icon2:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)

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

# =============================================
# عرض الترحيب ودليل المستخدم
# =============================================
render_welcome()

# =============================================
# التذييل
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;padding:20px;">
    <p style="color:#FFD700;font-size:1.5em;">⚖️ {TXT('مختبر الميزان', 'The Mizan Lab')}</p>
    <p style="font-size:1.1em;">{TXT('محطة الأرصاد الحضارية العالمية', 'Global Civilization Observatory')}</p>
    <p style="color:#FFD700;font-size:1.3em;">S = W x B</p>
    <p>{TXT('ق = ١٠٠ = الحق = الميزان', 'Q = 100 = The Truth = The Balance')}</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size:0.8em;margin-top:15px;color:#AAA;">
        {TXT(
            'هذا المختبر ليس إلا محاولة متواضعة لفهم سنة من سنن الله في خلقه. '
            'إن أصبنا فمن الله، وإن أخطأنا فمن أنفسنا. '
            'والحمد لله الذي هدانا لهذا وما كنا لنهتدي لولا أن هدانا الله.',
            'This lab is but a humble attempt to understand one of Allah\'s laws in His creation. '
            'If we are right, it is from Allah; if we are wrong, it is from ourselves. '
            'And praise be to Allah who guided us to this, for we would not have been guided had Allah not guided us.'
        )}
    </p>
    <p style="color:#FFD700;font-size:1.2em;margin-top:15px;">﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
</div>
""", unsafe_allow_html=True)
