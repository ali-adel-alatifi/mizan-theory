# mizan/app.py
"""
المدخل الرئيسي لتطبيق مختبر الميزان
يدعم الترجمة الكاملة باستخدام st.query_params لتجنب أخطاء الاتصال
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
    initial_sidebar_state="expanded"
)

# =============================================
# تحديد اللغة من query_params (حل مشكلة الاتصال)
# =============================================
if "lang" in st.query_params:
    st.session_state.lang = st.query_params["lang"]

if "lang" not in st.session_state:
    st.session_state.lang = "ar"

# =============================================
# تنسيق CSS بسيط
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
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:15px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:15px;margin-bottom:20px;border:2px solid #FFD700;'>
        <p style='font-size:2.5em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:5px 0;font-size:1.3em;'>{TXT('مختبر الميزان', 'The Mizan Lab')}</h2>
        <p style='color:#e0e0e0;font-size:0.7em;margin:2px 0;'>{TXT('محطة الأرصاد الحضارية', 'Global Observatory')}</p>
        <p style='color:#FFD700;font-size:1em;margin:5px 0;font-weight:bold;'>S = W x B</p>
    </div>
    """, unsafe_allow_html=True)
    
    # زر اللغة باستخدام query_params (لا يسبب أخطاء اتصال)
    if st.button(TXT("🇬🇧 English", "🇸🇦 العربية"), use_container_width=True, key="btn_lang_sidebar"):
        new_lang = "en" if st.session_state.lang == "ar" else "ar"
        st.query_params["lang"] = new_lang
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"### 🧭 {TXT('روابط سريعة', 'Quick Links')}")
    
    tabs_info = [
        ("🧍", TXT("البوصلة", "Compass"), TXT("تحديد موقعك", "Find your position")),
        ("🏛️", TXT("مختبر الأمة", "Nation Lab"), TXT("تحليل الدول", "Analyze nations")),
        ("🌌", TXT("المشهد الكوني", "Cosmic Scene"), TXT("محاكاة حية", "Live simulation")),
        ("📖", TXT("المعجم", "Lexicon"), TXT("أسرار الحروف", "Letter secrets")),
        ("📜", TXT("الشواهد", "Evidence"), TXT("مقارنة التاريخ", "Compare history")),
        ("📐", TXT("الصراط", "Path"), TXT("مسارك", "Your path")),
        ("🌍", TXT("المرصد", "Observatory"), TXT("خريطة العالم", "World map")),
        ("🩺", TXT("طبيب القلوب", "Healer"), TXT("روشتة علاجية", "Prescription")),
        ("🤝", TXT("شبكة الناجين", "Network"), TXT("تواصل", "Connect")),
        ("🎓", TXT("الجامعة", "Academy"), TXT("دورات", "Courses")),
        ("🏴", TXT("آل البيت", "Ahlul Bayt"), TXT("نماذج", "Models")),
        ("📚", TXT("الملاحق", "Appendices"), TXT("مراجع", "References")),
        ("⚛️", TXT("القانون الواحد", "The One Law"), TXT("تجليات", "Manifestations")),
    ]
    
    for icon, name, desc in tabs_info:
        st.markdown(f"{icon} **{name}** — *{desc}*")
    
    st.markdown("---")
    if st.button(TXT("🔄 إعادة ضبط كل شيء", "🔄 Full Reset"), key="btn_reset_all", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",):
                del st.session_state[k]
        st.query_params.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption(TXT("© 2026 علي عادل العاطفي\nمختبر الميزان v2.0", "© 2026 Ali Adel Alatifi\nMizan Lab v2.0"))

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
        new_lang = "en" if st.session_state.lang == "ar" else "ar"
        st.query_params["lang"] = new_lang
        st.rerun()

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

with tab1:
    render_compass()

with tab2:
    render_nation_lab()

with tab3:
    render_cosmic_scene()

with tab4:
    render_new_lexicon()

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

with tab12:
    render_new_appendices()

with tab13:
    render_new_the_one_law()

with tab14:
    render_new_spiritual_energy()

with tab15:
    render_new_civilization_cycle()

with tab16:
    render_social_fabric()

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
