# mizan/ui_enhancements.py
"""
تحسينات واجهة المستخدم وتجربة الاستخدام
"""

import streamlit as st
from config import TXT

def apply_global_css():
    """تطبيق الأنماط CSS الشاملة على المنصة."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Amiri+Quran&display=swap');
    
    :root {
        --bg-primary: #0a0f1e;
        --bg-secondary: #0d1528;
        --bg-card: rgba(20, 30, 60, 0.7);
        --gold: #FFD700;
        --gold-light: #FFF8DC;
        --gold-dark: #B8860B;
        --text-primary: #E0E0E0;
        --text-secondary: #AAAAAA;
        --red: #FF5252;
        --cyan: #00FFFF;
        --green: #00FF88;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a0f1e 0%, #0d1528 30%, #0f1a2e 100%);
        font-family: 'Cairo', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cairo', sans-serif;
        color: #FFD700;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h1 { font-size: 2.5em; margin-bottom: 10px; }
    h2 { font-size: 1.8em; border-bottom: 2px solid rgba(255, 215, 0, 0.3); padding-bottom: 8px; margin-bottom: 20px; }
    h3 { font-size: 1.4em; margin-bottom: 12px; }
    
    p, label, div, span, li {
        font-family: 'Cairo', sans-serif;
        color: #E0E0E0;
        line-height: 1.8;
    }
    
    .golden-title {
        font-size: 3.2em;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
    }
    
    .verse-text {
        text-align: center;
        color: #FFD700;
        font-size: 1.3em;
        margin: 15px 0;
        line-height: 2.2;
        font-family: 'Amiri Quran', serif;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(20, 30, 60, 0.9), rgba(30, 40, 70, 0.9));
        border: 2px solid #FFD700;
        color: #FFD700;
        border-radius: 12px;
        padding: 12px 25px;
        font-weight: bold;
        font-family: 'Cairo', sans-serif;
        width: 100%;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: #FFD700;
        color: #0a0f1e;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
        transform: translateY(-2px);
    }
    
    .stButton > button:active { transform: translateY(1px); }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background: rgba(13, 21, 40, 0.8);
        border-radius: 15px;
        padding: 5px;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 10px;
        color: #CCC;
        padding: 10px 18px;
        font-family: 'Cairo', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 215, 0, 0.15) !important;
        border: 2px solid #FFD700 !important;
        color: #FFD700 !important;
        font-weight: bold;
    }
    
    .message-box {
        background: rgba(20, 30, 60, 0.7);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255, 215, 0, 0.3);
        line-height: 2.2;
        backdrop-filter: blur(10px);
    }
    
    .card {
        background: rgba(20, 30, 60, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    @keyframes glow { 0%, 100% { box-shadow: 0 0 5px rgba(255, 215, 0, 0.3); } 50% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.7); } }
    
    .pulse { animation: pulse 2s ease-in-out infinite; }
    .glow { animation: glow 3s ease-in-out infinite; }
    
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0a0f1e; }
    ::-webkit-scrollbar-thumb { background: #FFD700; border-radius: 4px; }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(20, 30, 60, 0.8);
        border: 1px solid rgba(255, 215, 0, 0.3);
        color: #E0E0E0;
        border-radius: 8px;
        font-family: 'Cairo', sans-serif;
    }
    
    .stSlider > div > div > div > div { background: #FFD700; }
    
    .stSelectbox > div > div {
        background: rgba(20, 30, 60, 0.8);
        border: 1px solid rgba(255, 215, 0, 0.3);
        color: #E0E0E0;
        border-radius: 8px;
    }
    
    .js-plotly-plot, .plot-container {
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)


def render_enhanced_sidebar():
    """شريط جانبي محسن مع روابط سريعة."""
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:15px;background:linear-gradient(135deg,#1a1a2e,#16213e);
        border-radius:15px;margin-bottom:20px;border:2px solid #FFD700;' class='glow'>
            <p style='font-size:2.5em;margin:0;'>⚖️</p>
            <h2 style='color:#FFD700;margin:5px 0;font-size:1.3em;'>{TXT('مختبر الميزان', 'The Mizan Lab')}</h2>
            <p style='color:#e0e0e0;font-size:0.7em;margin:2px 0;'>{TXT('محطة الأرصاد الحضارية', 'Global Observatory')}</p>
            <p style='color:#FFD700;font-size:1em;margin:5px 0;font-weight:bold;'>S = W x B</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(TXT("🇬🇧 English", "🇸🇦 العربية"), use_container_width=True, key="btn_lang_sidebar"):
            st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
            st.rerun()
        
        st.markdown("---")
        st.markdown(f"### 🧭 {TXT('روابط سريعة', 'Quick Links')}")
        
        tabs_info = [
            ("🧍", TXT("البوصلة", "Compass"), "تحديد موقعك"),
            ("🏛️", TXT("مختبر الأمة", "Nation Lab"), "تحليل الدول"),
            ("🌌", TXT("المشهد الكوني", "Cosmic Scene"), "محاكاة حية"),
            ("🌍", TXT("المرصد العالمي", "Observatory"), "خريطة العالم"),
            ("🩺", TXT("طبيب القلوب", "Healer"), "روشتة علاجية"),
            ("🤝", TXT("شبكة الناجين", "Network"), "تواصل"),
            ("🎓", TXT("جامعة الميزان", "Academy"), "دورات"),
            ("🏴", TXT("مدرسة آل البيت", "Ahlul Bayt"), "نماذج"),
        ]
        
        for icon, name, desc in tabs_info:
            st.markdown(f"{icon} **{name}** — *{desc}*")
        
        st.markdown("---")
        st.markdown(f"### ⚙️ {TXT('إعدادات', 'Settings')}")
        lag = st.select_slider(
            TXT("فجوة الاستدراج", "Istidraj Gap"),
            options=[5, 10, 15, 22, 30, 40, 50],
            value=22, key="lag"
        )
        
        st.markdown("---")
        if st.button(TXT("🔄 إعادة ضبط كل شيء", "🔄 Full Reset"), key="btn_reset_all", use_container_width=True):
            for k in list(st.session_state.keys()):
                if k not in ("lang",):
                    del st.session_state[k]
            st.rerun()
        
        st.markdown("---")
        st.caption(TXT("© 2026 علي عادل العاطفي\nمختبر الميزان v2.0", "© 2026 Ali Adel Alatifi\nMizan Lab v2.0"))


def render_enhanced_header():
    """عنوان رئيسي محسن."""
    col_icon1, col_title, col_icon2 = st.columns([1, 6, 1])
    with col_icon1:
        st.markdown("<p style='text-align:center;font-size:4em;' class='pulse'>⚖️</p>", unsafe_allow_html=True)
    with col_title:
        st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{TXT('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
    with col_icon2:
        st.markdown("<p style='text-align:center;font-size:4em;' class='pulse'>⚖️</p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='verse-text glow'>
        ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
        <br><span style='font-size:0.8em;'>S = W x B | ق = ١٠٠ = الحق = الميزان</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button(TXT("English", "العربية"), key="btn_lang_main", use_container_width=True):
            st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
            st.rerun()


def render_enhanced_footer():
    """تذييل محسن."""
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;padding:20px;">
        <p style="color:#FFD700;font-size:1.5em;">⚖️ مختبر الميزان</p>
        <p style="font-size:1.1em;">{TXT('محطة الأرصاد الحضارية العالمية', 'Global Civilization Observatory')}</p>
        <p style="color:#FFD700;font-size:1.3em;">S = W x B</p>
        <p>ق = ١٠٠ = الحق = الميزان</p>
        <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
        <p style="font-size:0.8em;margin-top:15px;color:#AAA;">
            {TXT(
                'هذا المختبر ليس إلا محاولة متواضعة لفهم سنة من سنن الله في خلقه. '
                'إن أصبنا فمن الله، وإن أخطأنا فمن أنفسنا. '
                'والحمد لله الذي هدانا لهذا وما كنا لنهتدي لولا أن هدانا الله.',
                'This lab is but a humble attempt to understand one of Allah\'s laws in His creation.'
            )}
        </p>
        <p style="color:#FFD700;font-size:1.2em;margin-top:15px;">﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
    </div>
    """, unsafe_allow_html=True)
