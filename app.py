# =============================================
# ⚖️ المختبر القرآني – النسخة الذهبية
# Al-Deen Al-Qayyim – The Cosmic Balance Law
# S = W × B | W = الولاء | B = البراءة
# المؤلف: علي عادل العاطفي | Ali Adel Alatifi
# © 2026 جميع الحقوق محفوظة
# =============================================
# يجمع هذا الكود أفضل الميزات من النسخ الثلاثة:
# - قاعدة بيانات الحروف الـ 28 (من الكود الأول)
# - نظام المتغيرات الكامل + دالة apply_ethics (من الكود الثاني)
# - المشهد الكوني + الميزان الأخروي + الجزيئات (من الكود الثالث)
# =============================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import random
import time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# ⚙️ إعداد الصفحة
# =============================================
st.set_page_config(
    page_title="المختبر القرآني – النسخة الذهبية",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# 🗄️ قاعدة بيانات الحروف الـ 28 (من الكود الأول)
# =============================================
MIZAN_LETTERS = {
    "light": {
        "أ": {"value": 1,   "label": "الوحدانية",   "aya": "إِيَّاكَ نَعْبُدُ",         "color": "#004d00"},
        "ل": {"value": 30,  "label": "المُلك",       "aya": "إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ", "color": "#8B4513"},
        "م": {"value": 40,  "label": "الجمع",        "aya": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ", "color": "#FFD700"},
        "ر": {"value": 200, "label": "اليقظة",       "aya": "فَإِذَا فَرَغْتَ فَانصَبْ",   "color": "#FF6347"},
        "ك": {"value": 20,  "label": "الأمر",        "aya": "كُن فَيَكُونُ",             "color": "#00BFFF"},
        "هـ": {"value": 5,   "label": "الهوية",       "aya": "وَاجْتَنِبُوا الطَّاغُوتَ",   "color": "#000080"},
        "ي": {"value": 10,  "label": "الاستجابة",    "aya": "اسْتَجِيبُوا لِلَّهِ وَلِلرَّسُولِ", "color": "#00CED1"},
        "ع": {"value": 70,  "label": "الإدراك",      "aya": "وَقُل رَّبِّ زِدْنِي عِلْمًا", "color": "#800080"},
        "ص": {"value": 90,  "label": "الصمد",        "aya": "اللَّهُ الصَّمَدُ",         "color": "#228B22"},
        "ق": {"value": 100, "label": "الميزان",      "aya": "وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ", "color": "#000000"},
        "ن": {"value": 50,  "label": "النور",        "aya": "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ", "color": "#FFA500"},
        "س": {"value": 60,  "label": "السمع",        "aya": "سَمِعْنَا وَأَطَعْنَا",       "color": "#87CEEB"},
        "ح": {"value": 8,   "label": "الحياة",       "aya": "فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً", "color": "#32CD32"},
        "ط": {"value": 9,   "label": "الطهارة",      "aya": "إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ", "color": "#F5F5DC"},
    },
    "neutral": {
        "ف": {"value": 80,  "label": "فاء السببية",   "role": "=",  "aya": "فَمَن يَكْفُرْ بِالطَّاغُوتِ...", "color": "#AAAAAA"},
        "و": {"value": 6,   "label": "واو العطف",     "role": "×/+","aya": "وَيُؤْمِن بِاللَّهِ",          "color": "#CCCCCC"},
        "ب": {"value": 2,   "label": "باء الاستعانة", "role": "بـ", "aya": "بِسْمِ اللَّهِ الرَّحْمَٰنِ",   "color": "#BBBBBB"},
        "ل": {"value": 30,  "label": "لام التعليل",   "role": "→",  "aya": "لِيَعْبُدُونِ",               "color": "#AAAAAA"},
        "ت": {"value": 400, "label": "تاء الفاعل",    "role": "ف",  "aya": "قَالَتِ امْرَأَتُ فِرْعَوْنَ",   "color": "#999999"},
        "ث": {"value": 500, "label": "ثم العطف",      "role": "ت",  "aya": "ثُمَّ خَلَقْنَا النُّطْفَةَ",    "color": "#888888"},
    },
    "dark": {
        "ظ": {"value": 900, "label": "الظلم",   "aya": "إِنَّ الظَّالِمِينَ لَهُمْ عَذَابٌ أَلِيمٌ", "color": "#B22222"},
        "ض": {"value": 800, "label": "الضلال",  "aya": "وَمَن يُضْلِلِ اللَّهُ فَمَا لَهُ مِنْ هَادٍ", "color": "#4B0082"},
        "غ": {"value": 1000,"label": "الغش",    "aya": "مَنْ غَشَّنَا فَلَيْسَ مِنَّا",           "color": "#556B2F"},
        "ذ": {"value": 700, "label": "الذل",    "aya": "أَذِلَّةٍ عَلَى الْمُؤْمِنِينَ",          "color": "#696969"},
        "خ": {"value": 600, "label": "الخيانة", "aya": "لَا تَخُونُوا اللَّهَ وَالرَّسُولَ",       "color": "#800000"},
        "ش": {"value": 300, "label": "الشهوة",  "aya": "وَلَا تَتَّبِعِ الْهَوَىٰ",               "color": "#FF1493"},
        "ز": {"value": 7,   "label": "الزور",   "aya": "وَاجْتَنِبُوا قَوْلَ الزُّورِ",           "color": "#8B008B"},
        "ج": {"value": 3,   "label": "الجهل",   "aya": "بَلْ أَكْثَرُهُمْ يَجْهَلُونَ",           "color": "#3E2723"},
    }
}

# =============================================
# 🌐 قاموس اللغات
# =============================================
LANG = {
    "ar": {
        "title": "⚖️ المختبر القرآني – النسخة الذهبية",
        "subtitle": "قانون التوازن الكوني | S = W × B",
        "author": "© 2026 علي عادل العاطفي | Ali Adel Alatifi",
        "lang_btn": "English",
        "tab_macro": "🏛️ المختبر الجماعي",
        "tab_micro": "🧍 المختبر الفردي",
        "tab_book": "📖 كتاب الميزان",
        "tab_lexicon": "🔤 المعجم الهندسي",
        "tab_welcome": "📜 رسالة الترحيب",
        "tab_reference": "📋 الدليل المرجعي",
        "metrics": {
            "S": "⚖️ الثبات (S)",
            "W": "🤍 الولاء (W)",
            "B": "❤️ البراءة (B)",
            "E": "💫 التمكين (E)",
            "akhira": "📜 الميزان الأخروي",
            "gold": "🟡 مؤمن",
            "white": "⚪ راهب",
            "red": "🔴 كافر",
            "pink": "🩷 منافق",
        },
    },
    "en": {
        "title": "⚖️ The Quranic Lab – Golden Edition",
        "subtitle": "The Cosmic Balance Law | S = W × B",
        "author": "© 2026 Ali Adel Alatifi | علي عادل العاطفي",
        "lang_btn": "العربية",
        "tab_macro": "🏛️ The Collective Lab",
        "tab_micro": "🧍 The Individual Lab",
        "tab_book": "📖 The Book of Mizan",
        "tab_lexicon": "🔤 The Geometric Lexicon",
        "tab_welcome": "📜 Welcome Message",
        "tab_reference": "📋 Reference Guide",
        "metrics": {
            "S": "⚖️ Stability (S)",
            "W": "🤍 Allegiance (W)",
            "B": "❤️ Disavowal (B)",
            "E": "💫 Empowerment (E)",
            "akhira": "📜 Hereafter Balance",
            "gold": "🟡 Believer",
            "white": "⚪ Monk",
            "red": "🔴 Disbeliever",
            "pink": "🩷 Hypocrite",
        },
    }
}

# تهيئة اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = "ar"

T = LANG[st.session_state.lang]

# زر تبديل اللغة
col_title, col_lang = st.columns([5, 1])
with col_lang:
    if st.button(T["lang_btn"]):
        st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
        st.rerun()

# =============================================
# 🎨 التنسيق الفاخر
# =============================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a2e 0%, #0d0d28 50%, #0f0f1a 100%);
        color: #E8E8E8;
    }
    .golden-title {
        font-size: 3em; font-weight: 900; color: #FFD700;
        text-align: center; margin: 20px 0 0 0;
        text-shadow: 0 0 30px rgba(255,215,0,0.6);
        letter-spacing: 5px;
    }
    .golden-subtitle {
        font-size: 1.3em; color: #CCCCCC; text-align: center; margin: 0 0 10px 0;
    }
    .golden-author {
        font-size: 1em; color: #AAA; text-align: center; margin: 0 0 30px 0;
    }
    .stButton > button {
        border: 2px solid #FFD700; color: #FFD700; background: rgba(10,10,46,0.9);
        border-radius: 10px; height: 2.5em; font-weight: bold; font-size: 1em;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: #FFD700; color: black; transform: scale(1.02);
    }
    .metric-card {
        background: rgba(10,10,46,0.95); border-radius: 15px; padding: 12px 4px;
        text-align: center; border: 2px solid rgba(218,165,32,0.6);
        margin: 3px 0; box-shadow: 0 0 20px rgba(218,165,32,0.15);
    }
    .metric-value { font-size: 2em; font-weight: bold; margin: 0; }
    .metric-label { font-size: 0.8em; color: #CCC; margin: 5px 0 0 0; }
    [data-testid="stExpander"] details {
        background: rgba(10,10,40,0.85); border: 1px solid rgba(218,165,32,0.5);
        border-radius: 10px; margin-bottom: 10px;
    }
    [data-testid="stExpander"] summary {
        color: #FFD700; font-weight: bold; font-size: 1.1em; padding: 10px;
    }
    .stMarkdown p, .stMarkdown li { color: #E8E8E8; line-height: 2.2; font-size: 1.05em; }
    h1, h2, h3 { color: #FFD700; }
    h3 { font-size: 1.3em; margin-top: 15px; }
    hr { border-color: rgba(218,165,32,0.4); }
    .stSlider > div > div > div > div { background: #FFD700; }
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ العنوان الجليل
# =============================================
st.markdown(f'<p class="golden-title">{T["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="golden-subtitle">{T["subtitle"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="golden-author">{T["author"]}</p>', unsafe_allow_html=True)

# =============================================
# 📑 ألسنة التبويب
# =============================================
tabs = st.tabs([
    T["tab_macro"],
    T["tab_micro"],
    T["tab_book"],
    T["tab_lexicon"],
    T["tab_welcome"],
    T["tab_reference"]
])

# =============================================
# 🎨 نظام الألوان الموحد
# =============================================
COLORS = {
    "مؤمن": "#FFD700",
    "كافر": "#FF3333",
    "منافق": "#FFB6C1",
    "مشرك": "#FFA500"
}

def get_star_color(w, b):
    """تُرجع لون النجمة بناءً على معادلة الميزان S = W × B."""
    if w >= 0.6 and b >= 0.6: return COLORS["مؤمن"]
    elif w >= 0.6 and b < 0.4: return COLORS["مشرك"]
    elif w < 0.4 and b >= 0.6: return COLORS["كافر"]
    elif w < 0.4 and b < 0.4: return COLORS["منافق"]
    else:
        if w > b: return '#FFF8DC'
        elif b > w: return '#FFA07A'
        else: return '#FFBF00'

def get_quadrant_name(L_map, D_map):
    """تُرجع اسم الربع بناءً على إحداثيات (L, D)."""
    lang = st.session_state.lang
    if L_map > 0 and D_map > 0:
        return "المؤمن (الربع الأول)" if lang == "ar" else "The Believer (Q1)"
    elif L_map < 0 and D_map > 0:
        return "الكافر (الربع الثاني)" if lang == "ar" else "The Disbeliever (Q2)"
    elif L_map < 0 and D_map < 0:
        return "المنافق (الربع الثالث)" if lang == "ar" else "The Hypocrite (Q3)"
    elif L_map > 0 and D_map < 0:
        return "المشرك (الربع الرابع)" if lang == "ar" else "The Polytheist (Q4)"
    else:
        return "منطقة محايدة" if lang == "ar" else "Neutral Zone"

def get_quadrant_color(L_map, D_map):
    """تُرجع لون الربع بناءً على إحداثيات (L, D)."""
    if L_map > 0 and D_map > 0: return COLORS["مؤمن"]
    elif L_map < 0 and D_map > 0: return COLORS["كافر"]
    elif L_map < 0 and D_map < 0: return COLORS["منافق"]
    elif L_map > 0 and D_map < 0: return COLORS["مشرك"]
    else: return "#888888"

# =============================================
# 🧮 دالة التفاعل الأخلاقي (من الكود الثاني)
# =============================================
def apply_ethics(sw, sb, neighbors_W, neighbors_B,
                 amr, nahy, taawun_birr, taawun_taqwa, tawasi_haqq, tawasi_sabr,
                 nahy_marouf_e, amr_munkar_e, taawun_ithm, taawun_udwan, tawasi_batil, adam_sabr):
    """تحاكي التفاعل الأخلاقي بين النجوم وتأثير البيئة على الفرد."""
    w_boost = 0.0; b_boost = 0.0
    resistance_w = 0.0; resistance_b = 0.0

    # تأثير الأمر بالمعروف والنهي عن المنكر
    w_boost += amr * 0.015; b_boost += nahy * 0.015
    
    # تأثير التعاون على البر والتقوى
    if neighbors_W > 0.5: w_boost += taawun_birr * 0.02
    if neighbors_B > 0.5: b_boost += taawun_taqwa * 0.02
    
    # مقاومة الصدمات
    resistance_w += tawasi_haqq * 0.1; resistance_b += tawasi_sabr * 0.1

    # تأثير الإفساد
    w_boost -= nahy_marouf_e * 0.015; b_boost -= amr_munkar_e * 0.015
    if neighbors_W < 0.5: w_boost -= taawun_ithm * 0.02
    if neighbors_B < 0.5: b_boost -= taawun_udwan * 0.02
    resistance_w -= tawasi_batil * 0.1; resistance_b -= adam_sabr * 0.1

    resistance_w = max(0, resistance_w); resistance_b = max(0, resistance_b)
    sw += w_boost; sb += b_boost
    return sw, sb, resistance_w, resistance_b
                     # =============================================
# 🏛️ المختبر الجماعي (Macro Lab) – النسخة الذهبية
# =============================================
with tabs[0]:
    lang = st.session_state.lang

    TXT_MACRO = {
        "ar": {
            "control_title": "⚙️ مؤثرات الثبات الجماعي – مولدات ومثبطات",
            "play": "▶️ تشغيل",
            "stop": "⏹️ إيقاف",
            "reset": "🔄 إعادة",
            "clear": "🧹 تنظيف",
            "download": "📥 تحميل صورة المشهد",
            "phase_peak": "استقرار تام",
            "phase_rise": "صعود",
            "phase_fall": "انهيار",
            "phase_bottom": "قاع",
            "phase_istidraj": ">> استدراج <<",
            "phase_recovery": ">> تعافي <<",
            "evidence_title": "📈 لوحة الإثبات: S (الذهب) يقود E (السماوي) — الاستدراج",
            "initial_title": "اضغط ▶️ تشغيل لرؤية المختبر الحي",
            "sim_stopped": "⏸️ تم إيقاف المحاكاة",
            "settings": "⚙️ إعدادات المحاكاة",
            "speed": "سرعة الدورة",
            "delay": "تأخير التمكين",
            "stars": "عدد النجوم",
        },
        "en": {
            "control_title": "⚙️ Collective Stability Factors",
            "play": "▶️ Run",
            "stop": "⏹️ Stop",
            "reset": "🔄 Reset",
            "clear": "🧹 Clear",
            "download": "📥 Download Scene Image",
            "phase_peak": "Peak Stability",
            "phase_rise": "Rising",
            "phase_fall": "Collapsing",
            "phase_bottom": "Rock Bottom",
            "phase_istidraj": ">> Istidraj <<",
            "phase_recovery": ">> Recovery <<",
            "evidence_title": "📈 Evidence Panel: S leads E — Istidraj",
            "initial_title": "Press ▶️ Run to see the Collective Lab",
            "sim_stopped": "⏸️ Simulation Stopped",
            "settings": "⚙️ Simulation Settings",
            "speed": "Cycle Speed",
            "delay": "Empowerment Delay",
            "stars": "Number of Stars",
        }
    }
    T_M = TXT_MACRO[lang]

    # دالة حساب الثبات (مُطوَّرة من الكود الثالث)
    def calc_stability_golden(W, B, E, vals, light_vals, dark_vals):
        S = W * B
        
        # تأثير المولدات الجماعية
        loyalty_keys = [
            'إقام_الصلاة', 'إيتاء_الزكاة', 'صوم_رمضان', 'حج_البيت',
            'تحكيم_الشريعة_في_الحكم', 'تحريم_الربا', 'إقامة_الحدود',
            'العلم', 'الإعلام_الصادق', 'الاقتصاد_الإسلامي',
            'تولية_أولياء_الله', 'العدل_في_الحكم', 'الشورى',
            'الأمر_بالمعروف', 'النهي_عن_المنكر',
            'التعاون_على_البر_والتقوى', 'التواصي_بالحق', 'التواصي_بالصبر',
            'الإنفاق_في_سبيل_الله', 'الجهاد_بالنفس_والمال',
            'تولي_المؤمنين_وحمل_همهم', 'اليقين_بحتمية_الجزاء',
            'الصدق', 'الأمانة', 'الوفاء_بالعهد',
            'العفة', 'الشهادة_بالحق',
            'بر_الوالدين', 'صلة_الرحم', 'حسن_الجوار', 'الرحمة_بين_المؤمنين'
        ]
        corruption_keys = [
            'ترك_الصلاة', 'منع_الزكاة', 'إفطار_رمضان_عمدا', 'ترك_الحج',
            'الحكم_بغير_ما_أنزل_الله', 'استباحة_الربا', 'تعطيل_الحدود',
            'الجهل', 'الإعلام_الفاسد', 'الاقتصاد_الربوي',
            'تولية_الفجار', 'الظلم_في_الحكم', 'الاستبداد',
            'الأمر_بالمنكر', 'النهي_عن_المعروف',
            'التعاون_على_الإثم_والعدوان', 'التواصي_بالباطل', 'التخاذل',
            'البخل', 'القعود_عن_الجهاد',
            'الكذب', 'الخيانة', 'الغدر',
            'الفواحش', 'الفسوق', 'الفجور', 'إشاعة_الفاحشة',
            'كتمان_الشهادة',
            'عقوق_الوالدين', 'قطيعة_الرحم', 'أذى_الجار', 'التقاطع_والتدابر'
        ]
        
        loyalty_boost = sum(vals.get(k, 0.5) for k in loyalty_keys) / len(loyalty_keys)
        corruption = sum(vals.get(k, 0.1) for k in corruption_keys) / len(corruption_keys)
        
        S *= (0.4 + 0.6 * loyalty_boost)
        S *= (1.0 - 0.6 * corruption)
        
        # تأثير الحروف النورانية والظلامية (من الكود الأول والثالث)
        if light_vals and dark_vals:
            light_factor = sum(
                MIZAN_LETTERS["light"][k]["value"] * light_vals.get(k, 0.7)
                for k in MIZAN_LETTERS["light"]
            ) / 14.0
            dark_factor = sum(
                MIZAN_LETTERS["dark"][k]["value"] * dark_vals.get(k, 0.2)
                for k in MIZAN_LETTERS["dark"]
            ) / 8.0
            
            S *= (0.8 + 0.4 * light_factor / 100)
            S *= (1.0 - 0.3 * dark_factor / 1000)
        
        return np.clip(S, 0.001, 1.0)

    # التهيئة
    if 'macro_run' not in st.session_state: st.session_state.macro_run = False
    if 'macro_init' not in st.session_state: st.session_state.macro_init = False
    if not st.session_state.macro_init:
        np.random.seed(42); random.seed(42)
        N = 180
        st.session_state.cx, st.session_state.cy = 14, 10.0
        st.session_state.star_x = np.random.uniform(0, 28, N)
        st.session_state.star_y = np.random.uniform(0, 20, N)
        st.session_state.star_w = np.random.uniform(0.1, 1.0, N)
        st.session_state.star_b = np.random.uniform(0.1, 1.0, N)
        st.session_state.res_w = np.zeros(N)
        st.session_state.res_b = np.zeros(N)
        st.session_state.W = 0.55
        st.session_state.B = 0.52
        st.session_state.E = 0.3
        st.session_state.S = 0.286
        st.session_state.phase = T_M["phase_peak"]
        st.session_state.cycle = 0.0
        st.session_state.aW = 0.0
        st.session_state.aB = np.pi * 0.5
        st.session_state.aa = 0.0
        st.session_state.history_S = deque(maxlen=500)
        st.session_state.history_E = deque(maxlen=500)
        st.session_state.history_x = deque(maxlen=500)
        st.session_state.good_deeds = 10.0
        st.session_state.bad_deeds = 5.0
        st.session_state.eb = deque([0.286]*35, maxlen=35)
        # الجزيئات الكيميائية (من الكود الثالث)
        N_CHEM = 50
        st.session_state.chem_x = np.random.uniform(6, 22, N_CHEM)
        st.session_state.chem_y = np.random.uniform(5, 15, N_CHEM)
        st.session_state.chem_w = np.random.uniform(0.2, 0.9, N_CHEM)
        st.session_state.chem_b = np.random.uniform(0.2, 0.9, N_CHEM)
        st.session_state.macro_init = True

    # مؤشرات الميزان (مع العدادت الحية من الكود الثالث)
    if st.session_state.macro_init:
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FFD700;">{st.session_state.S:.3f}</p><p class="metric-label">{T["metrics"]["S"]}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FFFFFF;">{st.session_state.W:.3f}</p><p class="metric-label">{T["metrics"]["W"]}</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FF5252;">{st.session_state.B:.3f}</p><p class="metric-label">{T["metrics"]["B"]}</p></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#00FFFF;">{st.session_state.E:.3f}</p><p class="metric-label">{T["metrics"]["E"]}</p></div>', unsafe_allow_html=True)
        with col5:
            balance = st.session_state.good_deeds - st.session_state.bad_deeds
            clr = "#FFD700" if balance >= 0 else "#FF3333"
            st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{clr};">{balance:.2f}</p><p class="metric-label">{T["metrics"]["akhira"]}</p></div>', unsafe_allow_html=True)
        with col6:
            n_gold = np.sum((st.session_state.star_w >= 0.6) & (st.session_state.star_b >= 0.6))
            st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FFD700;">{n_gold}</p><p class="metric-label">{T["metrics"]["gold"]}</p></div>', unsafe_allow_html=True)
        with col7:
            n_red = np.sum((st.session_state.star_w < 0.4) & (st.session_state.star_b >= 0.6))
            st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FF3333;">{n_red}</p><p class="metric-label">{T["metrics"]["red"]}</p></div>', unsafe_allow_html=True)

    plot_spot = st.empty()

    # المحاكاة الحية
    if st.session_state.macro_run:
        try:
            W, B = st.session_state.W, st.session_state.B
            E, S = st.session_state.E, st.session_state.S
            phase, cycle = st.session_state.phase, st.session_state.cycle
            aW, aB, aa = st.session_state.aW, st.session_state.aB, st.session_state.aa
            sx = st.session_state.star_x.copy(); sy = st.session_state.star_y.copy()
            sw = st.session_state.star_w.copy(); sb = st.session_state.star_b.copy()
            res_w = st.session_state.res_w.copy(); res_b = st.session_state.res_b.copy()
            cx, cy = st.session_state.cx, st.session_state.cy
            eb = st.session_state.eb
            pS, pE, px = st.session_state.history_S, st.session_state.history_E, st.session_state.history_x
            # الجزيئات
            chem_x = st.session_state.chem_x.copy(); chem_y = st.session_state.chem_y.copy()
            chem_w = st.session_state.chem_w.copy(); chem_b = st.session_state.chem_b.copy()

            cycle += cycle_speed; sv = np.sin(cycle)
            target_S = 0.5 + 0.45 * sv
            if sv > 0.5: phase = T_M["phase_peak"]
            elif sv > 0: phase = T_M["phase_rise"]
            elif sv > -0.5: phase = T_M["phase_fall"]
            else: phase = T_M["phase_bottom"]
            if 0.3 < sv < 0.35: phase = T_M["phase_istidraj"]
            if -0.35 < sv < -0.3: phase = T_M["phase_recovery"]

            n = len(sw)
            # استخدام دالة apply_ethics (من الكود الثاني)
            for i in range(n):
                dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                close = (dist < 2.5) & (np.arange(n) != i)
                neighbors_W = np.mean(sw[close]) if np.any(close) else 0.5
                neighbors_B = np.mean(sb[close]) if np.any(close) else 0.5

                sw[i], sb[i], new_res_w, new_res_b = apply_ethics(
                    sw[i], sb[i], neighbors_W, neighbors_B,
                    vals.get('الأمر_بالمعروف', 0.7), vals.get('النهي_عن_المنكر', 0.7),
                    vals.get('التعاون_على_البر_والتقوى', 0.6), vals.get('التعاون_على_البر_والتقوى', 0.6),
                    vals.get('التواصي_بالحق', 0.6), vals.get('التواصي_بالصبر', 0.6),
                    vals.get('الأمر_بالمنكر', 0.1), vals.get('النهي_عن_المعروف', 0.1),
                    vals.get('التعاون_على_الإثم_والعدوان', 0.1), vals.get('التعاون_على_الإثم_والعدوان', 0.1),
                    vals.get('التواصي_بالباطل', 0.1), vals.get('التخاذل', 0.1)
                )
                res_w[i] = new_res_w; res_b[i] = new_res_b

                # تأثير المولدات والمثبطات
                loyalty_keys = [
                    'إقام_الصلاة', 'إيتاء_الزكاة', 'صوم_رمضان', 'حج_البيت',
                    'تحكيم_الشريعة_في_الحكم', 'تحريم_الربا', 'إقامة_الحدود',
                    'العلم', 'الإعلام_الصادق', 'الاقتصاد_الإسلامي',
                    'تولية_أولياء_الله', 'العدل_في_الحكم', 'الشورى',
                    'الأمر_بالمعروف', 'النهي_عن_المنكر',
                    'التعاون_على_البر_والتقوى', 'التواصي_بالحق', 'التواصي_بالصبر',
                    'الإنفاق_في_سبيل_الله', 'الجهاد_بالنفس_والمال',
                    'تولي_المؤمنين_وحمل_همهم', 'اليقين_بحتمية_الجزاء',
                    'الصدق', 'الأمانة', 'الوفاء_بالعهد',
                    'العفة', 'الشهادة_بالحق',
                    'بر_الوالدين', 'صلة_الرحم', 'حسن_الجوار', 'الرحمة_بين_المؤمنين'
                ]
                corruption_keys = [
                    'ترك_الصلاة', 'منع_الزكاة', 'إفطار_رمضان_عمدا', 'ترك_الحج',
                    'الحكم_بغير_ما_أنزل_الله', 'استباحة_الربا', 'تعطيل_الحدود',
                    'الجهل', 'الإعلام_الفاسد', 'الاقتصاد_الربوي',
                    'تولية_الفجار', 'الظلم_في_الحكم', 'الاستبداد',
                    'الأمر_بالمنكر', 'النهي_عن_المعروف',
                    'التعاون_على_الإثم_والعدوان', 'التواصي_بالباطل', 'التخاذل',
                    'البخل', 'القعود_عن_الجهاد',
                    'الكذب', 'الخيانة', 'الغدر',
                    'الفواحش', 'الفسوق', 'الفجور', 'إشاعة_الفاحشة',
                    'كتمان_الشهادة',
                    'عقوق_الوالدين', 'قطيعة_الرحم', 'أذى_الجار', 'التقاطع_والتدابر'
                ]
                
                w_boost = sum(vals.get(k, 0.5) for k in loyalty_keys) / len(loyalty_keys) * 0.025
                dark_effect = sum(vals.get(k, 0.1) for k in corruption_keys) / len(corruption_keys) * 0.025

                sw[i] += w_boost
                sb[i] += w_boost * 0.6
                sw[i] -= dark_effect
                sb[i] -= dark_effect

                sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)

                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)

            # صدمات مع مقاومة (من الكود الثاني)
            shock_p = 0.006 * (1 - vals.get('العدل_في_الحكم', 0.5) * 0.9)
            if random.random() < shock_p:
                aff = np.random.choice(n, size=int(n * 0.25), replace=False)
                for idx in aff:
                    effective_shock = 1 - (1 - random.uniform(0.4, 0.8)) * (1 - res_w[idx])
                    sw[idx] *= effective_shock
                    sb[idx] *= effective_shock * random.uniform(0.5, 0.8)

            avgW, avgB = np.mean(sw), np.mean(sb)
            W += (avgW - W) * 0.05; B += (avgB - B) * 0.05
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            
            # حساب S باستخدام الدالة الذهبية
            light_vals = {k: vals.get(f"light_{k}", 0.7) for k in MIZAN_LETTERS["light"]}
            dark_vals = {k: vals.get(f"dark_{k}", 0.2) for k in MIZAN_LETTERS["dark"]}
            S = calc_stability_golden(W, B, E, vals, light_vals, dark_vals)
            
            eb.append(S)
            if len(eb) > 35: eb.popleft()
            E_target = eb[-delay_frames] if len(eb) >= delay_frames else S
            E += 0.025 * (E_target - E)
            W = W - 0.012 * E + 0.025 / (S + 0.1)
            B = B - 0.01 * E + 0.006 * (1 - B) * W * (1 - W)
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_stability_golden(W, B, E, vals, light_vals, dark_vals)
            
            pS.append(S); pE.append(E); px.append(len(px))
            if len(px) > 500: pS.popleft(); pE.popleft(); px.popleft()

            st.session_state.good_deeds += np.mean(sw) * 0.12
            st.session_state.bad_deeds += (1 - np.mean(sb)) * 0.12

            # حركة الكواكب
            aW += 0.018 + random.uniform(-0.02, 0.03) * (1 - W)**2
            aB += 0.018 + random.uniform(-0.02, 0.03) * (1 - B)**2
            wx = cx + (7 - 2.5 * W) * np.cos(aW); wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB); by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7
            
            # حركة النجوم والجزيئات
            ins = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.08, 0.08, n) * ins; sy += np.random.uniform(-0.08, 0.08, n) * ins
            sx, sy = np.clip(sx, cx-14, cx+14), np.clip(sy, cy-10, cy+10)
            
            # تحديث الجزيئات
            for i in range(len(chem_w)):
                chem_w[i] += (avgW - chem_w[i]) * 0.02 + np.random.uniform(-0.01, 0.01)
                chem_b[i] += (avgB - chem_b[i]) * 0.02 + np.random.uniform(-0.01, 0.01)
                chem_w[i] = np.clip(chem_w[i], 0.01, 1.0); chem_b[i] = np.clip(chem_b[i], 0.01, 1.0)
            chem_x += np.random.uniform(-0.05, 0.05, len(chem_x)) * ins
            chem_y += np.random.uniform(-0.05, 0.05, len(chem_y)) * ins
            chem_x = np.clip(chem_x, cx-8, cx+8); chem_y = np.clip(chem_y, cy-6, cy+6)

            st.session_state.W, st.session_state.B = W, B
            st.session_state.E, st.session_state.S = E, S
            st.session_state.phase, st.session_state.cycle = phase, cycle
            st.session_state.aW, st.session_state.aB, st.session_state.aa = aW, aB, aa + 0.15
            st.session_state.eb = eb
            st.session_state.star_x, st.session_state.star_y = sx, sy
            st.session_state.star_w, st.session_state.star_b = sw, sb
            st.session_state.res_w, st.session_state.res_b = res_w, res_b
            st.session_state.chem_x, st.session_state.chem_y = chem_x, chem_y
            st.session_state.chem_w, st.session_state.chem_b = chem_w, chem_b
            st.session_state.history_S, st.session_state.history_E, st.session_state.history_x = pS, pE, px

            # المشهد الكوني (مع الجزيئات والميزان الأخروي)
            fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            
            # النواة الذهبية
            for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                            (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=20, ha='center', va='center', fontweight='bold')
            
            # هالة التمكين
            ax.add_patch(Circle((cx, cy), 0.5 + 15 * E, color='#00FFFF', alpha=0.12, zorder=7))
            ax.add_patch(Circle((cx, cy), 9.0, color='#00FF88', alpha=0.12, fill=False, lw=2.5, zorder=2))
            
            # النجوم
            colors = [get_star_color(sw[i], sb[i]) for i in range(n)]
            ax.scatter(sx, sy, s=45, c=colors, alpha=0.85, edgecolors='white', linewidths=0.3, zorder=5)
            
            # الكوكبان
            ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#F33', alpha=0.85, zorder=13))
            ax.text(wx, wy - 1.3, 'W', color='#FFF', fontsize=13, ha='center', fontweight='bold')
            ax.text(bx, by - 1.3, 'B', color='#F33', fontsize=13, ha='center', fontweight='bold')
            
            # الجزيئات الكيميائية (من الكود الثالث)
            chem_colors = [get_star_color(chem_w[i], chem_b[i]) for i in range(len(chem_w))]
            ax.scatter(chem_x, chem_y, s=20, c=chem_colors, alpha=0.7, edgecolors='white', linewidths=0.2, zorder=6)
            
            # الميزان الأخروي المرئي (من الكود الثالث)
            akh_x, akh_y, akh_scale = 14, 10.0, 8.0
            حسنات = st.session_state.good_deeds * 20
            سيئات = st.session_state.bad_deeds * 20
            akh_balance = (حسنات - سيئات) / max(حسنات + سيئات, 1)
            
            # عمود الميزان
            ax.plot([akh_x, akh_x], [1, 18], color='#FFD700', lw=0.5, alpha=0.3, zorder=1)
            # العارضة
            ax.plot([akh_x - akh_scale, akh_x + akh_scale], [17.5 - akh_balance * 3, 17.5 + akh_balance * 3], 
                   color='#FFD700', lw=1, alpha=0.4, zorder=1)
            # كفتا الميزان
            lpy = 7 - akh_balance * 3; rpy = 7 + akh_balance * 3
            ax.add_patch(Circle((akh_x - akh_scale, lpy), 2.0, color='#FFD700', alpha=0.15, fill=False, lw=0.5, zorder=1))
            ax.add_patch(Circle((akh_x + akh_scale, rpy), 2.0, color='#FFD700', alpha=0.15, fill=False, lw=0.5, zorder=1))
            ax.text(akh_x - akh_scale, lpy - 2.5, f'{حسنات:.0f}', color='white', fontsize=6, ha='center', alpha=0.5)
            ax.text(akh_x + akh_scale, rpy - 2.5, f'{سيئات:.0f}', color='#FF3333', fontsize=6, ha='center', alpha=0.5)
            
            # لوحة الإثبات
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            if pSl:
                pax = ax.inset_axes([0.15, 0.02, 0.78, 0.2])
                pax.set_xlim(0, 500); pax.set_ylim(0, 1.05)
                pax.set_title(T_M["evidence_title"], color='white', fontsize=11, fontweight='bold')
                pax.tick_params(colors='white', labelsize=8); pax.grid(True, alpha=0.3)
                pax.plot(pxl, pSl, color='#FFD700', lw=3, label='S (الثبات)' if lang == "ar" else 'S')
                pax.plot(pxl, pEl, color='#00FFFF', lw=2.5, label='E (التمكين)' if lang == "ar" else 'E')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=9)
            
            ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f}', color='white', fontsize=15, ha='center', fontweight='bold')
            plt.tight_layout(pad=0)
            plot_spot.pyplot(fig)
            buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='#000010'); buf.seek(0)
            st.session_state.latest_image = buf; plt.close(fig)
            time.sleep(0.07)
        except Exception as e:
            st.error(str(e)); st.session_state.macro_run = False
        st.success(T_M["sim_stopped"])
    else:
        if st.session_state.macro_init:
            fig, ax = plt.subplots(figsize=(8, 5), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            colors = [get_star_color(st.session_state.star_w[i], st.session_state.star_b[i])
                     for i in range(len(st.session_state.star_w))]
            ax.scatter(st.session_state.star_x, st.session_state.star_y, s=30, c=colors, alpha=0.8, edgecolors='white', linewidths=0.2)
            ax.text(14, 10, '⚖️', fontsize=45, ha='center', va='center', color='#FFD700')
            ax.set_title(T_M["initial_title"], color='white', fontsize=15)
            plot_spot.pyplot(fig); plt.close(fig)

    if 'latest_image' in st.session_state:
        st.download_button(T_M["download"], st.session_state.latest_image, "الميزان_الكوني.png", "image/png")

    # لوحة التحكم الجماعية (أسفل المشهد)
    st.markdown("---")
    with st.expander(T_M["control_title"], expanded=False):
        vals = {}

        # ========== ١. شعائر الله (العبادات) ==========
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🕌 شعائر الله (العبادات)")
            vals['إقام_الصلاة'] = st.slider("إقام الصلاة", 0.0, 1.0, 0.9, 0.01, help="﴿إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَّوْقُوتًا﴾")
            vals['إيتاء_الزكاة'] = st.slider("إيتاء الزكاة", 0.0, 1.0, 0.7, 0.01, help="﴿وَأَقِيمُوا الصَّلَاةَ وَآتُوا الزَّكَاةَ﴾")
            vals['صوم_رمضان'] = st.slider("صوم رمضان", 0.0, 1.0, 0.8, 0.01, help="﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ﴾")
            vals['حج_البيت'] = st.slider("حج البيت", 0.0, 1.0, 0.6, 0.01, help="﴿وَلِلَّهِ عَلَى النَّاسِ حِجُّ الْبَيْتِ﴾")
        with col2:
            st.markdown("### 💔 نواقض شعائر الله")
            vals['ترك_الصلاة'] = st.slider("ترك الصلاة", 0.0, 1.0, 0.1, 0.01, help="﴿فَخَلَفَ مِن بَعْدِهِمْ خَلْفٌ أَضَاعُوا الصَّلَاةَ﴾")
            vals['منع_الزكاة'] = st.slider("منع الزكاة", 0.0, 1.0, 0.1, 0.01, help="﴿وَلَا يُنفِقُونَهَا فِي سَبِيلِ اللَّهِ﴾")
            vals['إفطار_رمضان_عمدا'] = st.slider("إفطار رمضان عمداً", 0.0, 1.0, 0.1, 0.01, help="المخالفة بغير عذر")
            vals['ترك_الحج'] = st.slider("ترك الحج مع الاستطاعة", 0.0, 1.0, 0.1, 0.01, help="ترك الفريضة")

        st.divider()

        # ========== ٢. أسس الحكم الرشيد ==========
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("### ⚖️ أسس الحكم الرشيد (مولدات)")
            vals['تحكيم_الشريعة_في_الحكم'] = st.slider("تحكيم الشريعة في الحكم", 0.0, 1.0, 0.8, 0.01)
            vals['تحريم_الربا'] = st.slider("تحريم الربا", 0.0, 1.0, 0.9, 0.01)
            vals['إقامة_الحدود'] = st.slider("إقامة الحدود", 0.0, 1.0, 0.7, 0.01)
            vals['العلم'] = st.slider("العلم", 0.0, 1.0, 0.7, 0.01)
            vals['الإعلام_الصادق'] = st.slider("الإعلام الصادق", 0.0, 1.0, 0.7, 0.01)
            vals['الاقتصاد_الإسلامي'] = st.slider("الاقتصاد الإسلامي", 0.0, 1.0, 0.7, 0.01)
            vals['تولية_أولياء_الله'] = st.slider("تولية أولياء الله", 0.0, 1.0, 0.7, 0.01)
            vals['العدل_في_الحكم'] = st.slider("العدل في الحكم", 0.0, 1.0, 0.8, 0.01)
            vals['الشورى'] = st.slider("الشورى", 0.0, 1.0, 0.6, 0.01)
        with col4:
            st.markdown("### 🏴 نواقض الحكم الرشيد (مثبطات)")
            vals['الحكم_بغير_ما_أنزل_الله'] = st.slider("الحكم بغير ما أنزل الله", 0.0, 1.0, 0.1, 0.01)
            vals['استباحة_الربا'] = st.slider("استباحة الربا", 0.0, 1.0, 0.1, 0.01)
            vals['تعطيل_الحدود'] = st.slider("تعطيل الحدود", 0.0, 1.0, 0.1, 0.01)
            vals['الجهل'] = st.slider("الجهل", 0.0, 1.0, 0.1, 0.01)
            vals['الإعلام_الفاسد'] = st.slider("الإعلام الفاسد", 0.0, 1.0, 0.1, 0.01)
            vals['الاقتصاد_الربوي'] = st.slider("الاقتصاد الربوي", 0.0, 1.0, 0.1, 0.01)
            vals['تولية_الفجار'] = st.slider("تولية الفجار", 0.0, 1.0, 0.1, 0.01)
            vals['الظلم_في_الحكم'] = st.slider("الظلم في الحكم", 0.0, 1.0, 0.1, 0.01)
            vals['الاستبداد'] = st.slider("الاستبداد", 0.0, 1.0, 0.1, 0.01)

        st.divider()

        # ========== ٣. الإصلاح الجماعي ==========
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("### 🛡️ آليات الإصلاح الجماعي (مولدات)")
            vals['الأمر_بالمعروف'] = st.slider("الأمر بالمعروف", 0.0, 1.0, 0.7, 0.01)
            vals['النهي_عن_المنكر'] = st.slider("النهي عن المنكر", 0.0, 1.0, 0.7, 0.01)
            vals['التعاون_على_البر_والتقوى'] = st.slider("التعاون على البر والتقوى", 0.0, 1.0, 0.6, 0.01)
            vals['التواصي_بالحق'] = st.slider("التواصي بالحق", 0.0, 1.0, 0.6, 0.01)
            vals['التواصي_بالصبر'] = st.slider("التواصي بالصبر", 0.0, 1.0, 0.6, 0.01)
            vals['الإنفاق_في_سبيل_الله'] = st.slider("الإنفاق في سبيل الله", 0.0, 1.0, 0.5, 0.01)
            vals['الجهاد_بالنفس_والمال'] = st.slider("الجهاد بالنفس والمال", 0.0, 1.0, 0.5, 0.01)
        with col6:
            st.markdown("### 💀 نواقض الإصلاح الجماعي (مثبطات)")
            vals['الأمر_بالمنكر'] = st.slider("الأمر بالمنكر", 0.0, 1.0, 0.1, 0.01)
            vals['النهي_عن_المعروف'] = st.slider("النهي عن المعروف", 0.0, 1.0, 0.1, 0.01)
            vals['التعاون_على_الإثم_والعدوان'] = st.slider("التعاون على الإثم والعدوان", 0.0, 1.0, 0.1, 0.01)
            vals['التواصي_بالباطل'] = st.slider("التواصي بالباطل", 0.0, 1.0, 0.1, 0.01)
            vals['التخاذل'] = st.slider("التخاذل", 0.0, 1.0, 0.1, 0.01)
            vals['البخل'] = st.slider("البخل", 0.0, 1.0, 0.1, 0.01)
            vals['القعود_عن_الجهاد'] = st.slider("القعود عن الجهاد", 0.0, 1.0, 0.2, 0.01)

        st.divider()

        # ========== ٤. الأخلاق والمعاملات ==========
        col7, col8 = st.columns(2)
        with col7:
            st.markdown("### 🌸 مولدات الولاء والبراءة (أخلاق ومعاملات)")
            vals['تولي_المؤمنين_وحمل_همهم'] = st.slider("تولي المؤمنين وحمل همهم", 0.0, 1.0, 0.8, 0.01)
            vals['اليقين_بحتمية_الجزاء'] = st.slider("اليقين بحتمية الجزاء وعدالة القانون", 0.0, 1.0, 0.9, 0.01)
            vals['الصدق'] = st.slider("الصدق", 0.0, 1.0, 0.7, 0.01)
            vals['الأمانة'] = st.slider("الأمانة", 0.0, 1.0, 0.7, 0.01)
            vals['الوفاء_بالعهد'] = st.slider("الوفاء بالعهد", 0.0, 1.0, 0.7, 0.01)
            vals['العفة'] = st.slider("العفة", 0.0, 1.0, 0.7, 0.01)
            vals['الشهادة_بالحق'] = st.slider("الشهادة بالحق", 0.0, 1.0, 0.6, 0.01)
            vals['بر_الوالدين'] = st.slider("بر الوالدين", 0.0, 1.0, 0.8, 0.01)
            vals['صلة_الرحم'] = st.slider("صلة الرحم", 0.0, 1.0, 0.7, 0.01)
            vals['حسن_الجوار'] = st.slider("حسن الجوار", 0.0, 1.0, 0.6, 0.01)
            vals['الرحمة_بين_المؤمنين'] = st.slider("الرحمة بين المؤمنين", 0.0, 1.0, 0.7, 0.01)
        with col8:
            st.markdown("### 🥀 مثبطات الولاء والبراءة (فواحش ومنكرات)")
            vals['الكذب'] = st.slider("الكذب", 0.0, 1.0, 0.1, 0.01)
            vals['الخيانة'] = st.slider("الخيانة", 0.0, 1.0, 0.1, 0.01)
            vals['الغدر'] = st.slider("الغدر ونقض العهود", 0.0, 1.0, 0.1, 0.01)
            vals['الفواحش'] = st.slider("الفواحش", 0.0, 1.0, 0.1, 0.01)
            vals['الفسوق'] = st.slider("الفسوق", 0.0, 1.0, 0.1, 0.01)
            vals['الفجور'] = st.slider("الفجور", 0.0, 1.0, 0.1, 0.01)
            vals['إشاعة_الفاحشة'] = st.slider("إشاعة الفاحشة", 0.0, 1.0, 0.1, 0.01)
            vals['كتمان_الشهادة'] = st.slider("كتمان الشهادة", 0.0, 1.0, 0.1, 0.01)
            vals['عقوق_الوالدين'] = st.slider("عقوق الوالدين", 0.0, 1.0, 0.1, 0.01)
            vals['قطيعة_الرحم'] = st.slider("قطيعة الرحم", 0.0, 1.0, 0.1, 0.01)
            vals['أذى_الجار'] = st.slider("أذى الجار", 0.0, 1.0, 0.1, 0.01)
            vals['التقاطع_والتدابر'] = st.slider("التقاطع والتدابر", 0.0, 1.0, 0.1, 0.01)

        st.divider()

        # ========== الإعدادات ==========
        st.markdown(f"**{T_M['settings']}**")
        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            cycle_speed = st.slider(T_M["speed"], 0.001, 0.05, 0.008, 0.001)
        with cols2:
            delay_frames = st.slider(T_M["delay"], 5, 50, 22, 1)
        with cols3:
            N_STARS = st.slider(T_M["stars"], 50, 300, 150, 10)

    # أزرار التحكم
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button(T_M["play"], use_container_width=True): st.session_state.macro_run = True
    with c2:
        if st.button(T_M["stop"], use_container_width=True): st.session_state.macro_run = False
    with c3:
        if st.button(T_M["reset"], use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
    with c4:
        if st.button(T_M["clear"], use_container_width=True):
            st.cache_data.clear(); st.cache_resource.clear()
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
            # =============================================
# 🧍 المختبر الفردي (Micro Lab) – النسخة الذهبية
# =============================================
with tabs[1]:
    lang = st.session_state.lang

    TXT_MICRO = {
        "ar": {
            "compass_title": "🧭 البوصلة الكونية",
            "compass_subtitle": "اكتشف موقعك في فضاء الولاء والبراءة – 28 سؤالاً",
            "compass_caption": "14 سؤالاً للولاء + 14 سؤالاً للبراءة | S = L × D",
            "loyalty_header": "🤍 أسئلة الولاء (L)",
            "disavowal_header": "❤️ أسئلة البراءة (D)",
            "choose": "اختر إجابتك:",
            "result_header": "📊 نتيجة البوصلة الكونية",
            "quadrant_advice": {
                "مؤمن (الربع الأول)": "حافظ على ثباتك واستمر في النمو نحو (1,1).",
                "كافر (الربع الثاني)": "أنت بحاجة إلى توبة جذرية وتحويل بوصلتك نحو الخالق.",
                "منافق (الربع الثالث)": "أنت بحاجة إلى الصدق مع نفسك واتخاذ قرار حاسم.",
                "مشرك (الربع الرابع)": "لديك إيمان لكن براءتك منهارة. قوِّ مناعتك الإيمانية.",
            },
            "S_label": "⚖️ ثباتك الوجودي: S = L × D",
            "raw_score": "الدرجة الخام",
            "reset_btn": "🔄 إعادة الاختبار",
            "sim_title": "🧬 محاكاة الثبات الفردي",
            "sim_play": "▶️ شغّل محاكاتك الشخصية",
            "sim_stop": "⏹️ إيقاف",
            "sim_advice": "اضبط أشرطة التمرير ثم اضغط تشغيل لترى كيف يتغير ثباتك الشخصي.",
        },
        "en": {
            "compass_title": "🧭 The Cosmic Compass",
            "compass_subtitle": "Discover your position – 28 Questions",
            "compass_caption": "14 Allegiance + 14 Disavowal | S = L × D",
            "loyalty_header": "🤍 Allegiance Questions (L)",
            "disavowal_header": "❤️ Disavowal Questions (D)",
            "choose": "Choose:",
            "result_header": "📊 Compass Result",
            "quadrant_advice": {
                "The Believer (Q1)": "Stay steadfast and keep growing.",
                "The Disbeliever (Q2)": "You need sincere repentance.",
                "The Hypocrite (Q3)": "Be honest with yourself.",
                "The Polytheist (Q4)": "Strengthen your immunity.",
            },
            "S_label": "⚖️ Your Stability: S = L × D",
            "raw_score": "Raw Score",
            "reset_btn": "🔄 Retake Test",
            "sim_title": "🧬 Personal Stability Simulation",
            "sim_play": "▶️ Run Your Simulation",
            "sim_stop": "⏹️ Stop",
            "sim_advice": "Adjust the sliders then press Run.",
        }
    }
    T_I = TXT_MICRO[lang]

    st.header(T_I["compass_title"])
    st.subheader(T_I["compass_subtitle"])
    st.caption(T_I["compass_caption"])

    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    questions = {
        "L": [
            ("إخلاص القلب لله: هل تعيش حياتك لله وحده، لا تبتغي بذلك إلا وجهه؟",
             [("نعم، حياتي كلها لله (10)", 10), ("أحاول جاهداً لكن الدنيا تشغلني أحياناً (7)", 7),
              ("أرجو ذلك لكني لا أجتهد كفاية (4)", 4), ("حياتي لنفسي ودُنياي، والعبادة واجب ثقيل (0)", 0)]),
            ("الصلاة: هل تقيم الصلاة كما أمر الله، خاشعاً، تستشعر الوقوف بين يديه؟",
             [("أقيمها خاشعاً في وقتها، هي راحتي (10)", 10), ("أصلي الفروض، وأجاهد نفسي على الخشوع (7)", 7),
              ("أصلي بعض الفروض وأقطع بعضها (4)", 4), ("لا أصلي إلا نادراً أو لا أصلي (0)", 0)]),
            ("الزكاة والصدقة: هل تؤدي زكاة مالك طيبة بها نفسك، وتتصدق ابتغاء وجه الله؟",
             [("أؤدي الزكاة كاملة، وأتصدق بانتظام (10)", 10), ("أؤدي الزكاة، وقليلاً ما أتصدق (7)", 7),
              ("أخرج المال لكن بغير حساب (4)", 4), ("لا أخرج زكاة ولا صدقة (0)", 0)]),
            ("الصيام: هل تصوم رمضان إيماناً واحتساباً، وتصوم تطوعاً؟",
             [("أصوم رمضان وأزيده من النوافل (10)", 10), ("أصوم الفرض كاملاً (7)", 7),
              ("أصوم معظم الفرض (4)", 4), ("لا أصوم إلا قليلاً أو لا أصوم (0)", 0)]),
            ("الشوق إلى بيت الله: هل في قلبك شوق لزيارة بيت الله، وهل سعيت أو تخطط للسعي لأداء الحج؟",
             [("أديته، أو لي خطة واضحة لأدائه (10)", 10), ("لدي نية صادقة وأدخر لأجله (7)", 7),
              ("أتمنى ذلك فقط دون تخطيط (4)", 4), ("لا أشعر بالشوق، ولا أخطط له (0)", 0)]),
            ("حب رسول الله ﷺ: هل تقتدي بهدي النبي ﷺ في أخلاقك ومعاملاتك، وتقدم محبته على محبة الناس؟",
             [("أحبه أكثر من نفسي، وأقتدي به في كل شيء (10)", 10), ("أحبه، وأحاول الاقتداء به (7)", 7),
              ("أحبه لكني لا أقرأ سيرته ولا أهتدي بهديه (4)", 4), ("لا أشعر بمحبة خاصة له (0)", 0)]),
            ("الصدق: هل أنت صادق مع الله، ومع نفسك، ومع الناس؟",
             [("أصدق في كل أحوالي (10)", 10), ("أصدق غالباً (7)", 7),
              ("أصدق أحياناً (4)", 4), ("الكذب جزء من حياتي (0)", 0)]),
            ("الأمانة: هل تؤدي الأمانات إلى أهلها، وتحفظ السر، وتفي بالوعد؟",
             [("أؤدي الأمانة كاملة (10)", 10), ("أؤدي الأمانة غالباً (7)", 7),
              ("أؤديها أحياناً (4)", 4), ("لا أؤدي الأمانة (0)", 0)]),
            ("التوكل على الله: هل تتوكل على الله حق توكله، مع الأخذ بالأسباب؟",
             [("أتوكل على الله في كل أمري، وأعمل بالأسباب (10)", 10), ("أتوكل غالباً، لكن القلق يغلبني أحياناً (7)", 7),
              ("أتوكل قليلاً، وأعتمد على نفسي أكثر (4)", 4), ("لا أفكر في التوكل (0)", 0)]),
            ("الشكر والصبر: هل تشكر الله في الرخاء، وتصبر وتحتسب في البلاء؟",
             [("أشكر وأصبر، وأرى الخير في كل حال (10)", 10), ("أشكر غالباً، وأصبر بصعوبة (7)", 7),
              ("أنسى الشكر، وأتذمر من البلاء (4)", 4), ("لا أشكر ولا أصبر (0)", 0)]),
            ("حمل هم الأمة: هل تحمل هم الإسلام والمسلمين، وتسعى لنصرتهم بما تستطيع؟",
             [("نعم، أحمل هم الأمة وأعمل لنصرتها (10)", 10), ("أهتم، لكني لا أعمل شيئاً (7)", 7),
              ("أحزن للأحداث، ولا أفعل شيئاً (4)", 4), ("لا شأن لي بالمسلمين (0)", 0)]),
            ("الوفاء بالعهد: إذا عاهدت الله أو الناس، هل تفي بعهدك؟",
             [("أفي بعهدي دائماً (10)", 10), ("أفي بعهدي غالباً (7)", 7),
              ("أفي بعهدي أحياناً (4)", 4), ("لا أفي بعهدي (0)", 0)]),
            ("القناعة والرضا: هل أنت راضٍ بما قسم الله لك من رزق وقدر؟",
             [("أنا في غاية الرضا والقناعة (10)", 10), ("أرضى لكني أطمح للمزيد (7)", 7),
              ("لا أرضى كثيراً، وأشكو حالي (4)", 4), ("لا أرضى أبداً (0)", 0)]),
            ("نصرة المؤمنين: إذا رأيت مؤمناً يُظلم، هل تنصره وتدافع عنه؟",
             [("أنصره بكل ما أستطيع (10)", 10), ("أنصره إن لم يضرني ذلك (7)", 7),
              ("أكتفي بالدعاء له (4)", 4), ("لا أنصره (0)", 0)]),
        ],
        "D": [
            ("الأمر بالمعروف: هل تدعو إلى الخير، وتأمر بالمعروف بالحكمة والموعظة الحسنة؟",
             [("نعم، آمر بالمعروف وأدعو إليه (10)", 10), ("آمر بالمعروف أحياناً (7)", 7),
              ("أفعله في نفسي، ولا آمر غيري (4)", 4), ("لا آمر بالمعروف (0)", 0)]),
            ("النهي عن المنكر: هل تنكر المنكر بلسانك أو بيدك أو بقلبك؟",
             [("نعم، أنكر المنكر بكل وسيلة مشروعة (10)", 10), ("أنكره بلساني أو بقلبي (7)", 7),
              ("أكتفي بإنكار القلب (4)", 4), ("لا أنكر المنكر (0)", 0)]),
            ("بذل النفس والمال في سبيل الله: هل أنت مستعد لبذل نفسك ومالك لإعلاء كلمة الله؟",
             [("نعم، نفسي ومالي لله، وأتمنى الشهادة (10)", 10), ("أتمنى ذلك، لكني أخشى على نفسي (7)", 7),
              ("لا أرغب في بذل النفس، لكن قد أبذل المال (4)", 4), ("لا أبذل نفساً ولا مالاً (0)", 0)]),
            ("البراءة من الشرك وأهله: هل تتبرأ من كل ما يُعبد من دون الله، ومن كل مظهر من مظاهر الشرك؟",
             [("نعم، أتبرأ من الشرك وأهله تماماً (10)", 10), ("أرفض الشرك، لكني لا أجاهر بالبراءة (7)", 7),
              ("لا أهتم كثيراً بموضوع الشرك (4)", 4), ("أشارك في بعض مظاهر الشرك مجاملة (0)", 0)]),
            ("البراءة من الكفر والإلحاد: هل ترفض الكفر والإلحاد بقلبك ولسانك، وتحذر منهما؟",
             [("أرفضهما وأحذر منهما (10)", 10), ("أرفضهما في قلبي فقط (7)", 7),
              ("لا أهتم بهما (4)", 4), ("أرى فيهما فكراً متحضراً (0)", 0)]),
            ("البراءة من النفاق: هل تكره النفاق والتلون، وتجاهد نفسك على الإخلاص والصدق؟",
             [("أمقت النفاق وأجاهد نفسي على الإخلاص (10)", 10), ("أكره النفاق، لكني أتلون أحياناً (7)", 7),
              ("لا أهتم كثيراً بموضوع النفاق (4)", 4), ("أرى النفاق ضرورة في الحياة (0)", 0)]),
            ("مجاهدة الكذب: هل تجاهد نفسك على ترك الكذب في الجد والهزل؟",
             [("لا أكذب أبداً (10)", 10), ("نادراً ما أكذب (7)", 7),
              ("أكذب أحياناً (4)", 4), ("الكذب جزء من حياتي (0)", 0)]),
            ("مجاهدة الغش: هل تتجنب الغش في كل معاملاتك، وتتبرأ منه؟",
             [("لا أغش أبداً (10)", 10), ("نادراً ما أغش (7)", 7),
              ("أغش أحياناً (4)", 4), ("الغش أسلوب حياة (0)", 0)]),
            ("مجاهدة الخيانة: هل تفي بعهودك، ولا تخون من ائتمنك؟",
             [("لا أخون أبداً (10)", 10), ("نادراً ما أخون (7)", 7),
              ("أخون أحياناً إذا اضطررت (4)", 4), ("الخيانة أمر عادي (0)", 0)]),
            ("مجاهدة الظلم: هل ترفض الظلم بكل صوره، ولا ترضاه لأحد؟",
             [("لا أظلم أحداً أبداً (10)", 10), ("نادراً ما أظلم (7)", 7),
              ("أظلم أحياناً (4)", 4), ("لا أرى مشكلة في الظلم (0)", 0)]),
            ("مجاهدة الفواحش: هل تجاهد نفسك على ترك الفواحش، وتغض بصرك، وتحفظ فرجك؟",
             [("نعم، أحفظ نفسي ولا أقرب الفواحش (10)", 10), ("أجاهد نفسي، وأقع أحياناً (7)", 7),
              ("لا أجاهد نفسي كثيراً (4)", 4), ("لا أرى بأساً في الفواحش (0)", 0)]),
            ("مجاهدة الرياء: هل تخلص عملك لله، وتجاهد نفسك على ترك الرياء وحب الظهور؟",
             [("عملي كله لله، وأحاسب نفسي على الرياء (10)", 10), ("أحاول الإخلاص، لكن الرياء يغلبني أحياناً (7)", 7),
              ("لا أهتم بموضوع الرياء (4)", 4), ("لا أرى مشكلة في الرياء (0)", 0)]),
            ("مجاهدة الحسد: هل تسلم لله في قسمته، ولا تحسد أحداً على ما آتاه الله؟",
             [("لا أحسد أحداً أبداً (10)", 10), ("نادراً ما أحسد (7)", 7),
              ("أحسد أحياناً (4)", 4), ("كثيراً ما أحسد (0)", 0)]),
            ("الولاء للمؤمنين والبراءة من أعدائهم: هل تحب في الله، وتبغض في الله، وتكون مع المؤمنين ضد أعدائهم؟",
             [("نعم، أحب في الله وأبغض في الله (10)", 10), ("أحب المؤمنين، لكني لا أبغض أعداءهم (7)", 7),
              ("لا أحب ولا أبغض في الله (4)", 4), ("أبغض المؤمنين، وأحب أعداءهم (0)", 0)]),
        ]
    }

    st.markdown("### 📝 أجب بصدق (كل سؤال في موسع مستقل)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {T_I['loyalty_header']}")
        for i, q in enumerate(questions["L"]):
            with st.expander(q[0], expanded=False):
                ans = st.radio(T_I["choose"], [a[0] for a in q[1]], key=f"L{i}", index=None)
                if ans:
                    for a in q[1]:
                        if a[0] == ans: st.session_state.compass_answers[f"L{i}"] = a[1]
    with col2:
        st.markdown(f"#### {T_I['disavowal_header']}")
        for i, q in enumerate(questions["D"]):
            with st.expander(q[0], expanded=False):
                ans = st.radio(T_I["choose"], [a[0] for a in q[1]], key=f"D{i}", index=None)
                if ans:
                    for a in q[1]:
                        if a[0] == ans: st.session_state.compass_answers[f"D{i}"] = a[1]

    TOTAL_Q = 28
    if len(st.session_state.compass_answers) == TOTAL_Q:
        L_score = sum(st.session_state.compass_answers[f"L{i}"] for i in range(14))
        D_score = sum(st.session_state.compass_answers[f"D{i}"] for i in range(14))
        L = L_score / 140.0; D = D_score / 140.0
        L_map = L * 2 - 1; D_map = D * 2 - 1
        S_val = L * D
        q_name = get_quadrant_name(L_map, D_map)
        q_color = get_quadrant_color(L_map, D_map)
        advice = T_I["quadrant_advice"].get(q_name, "")

        st.divider(); st.header(T_I["result_header"])
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f"""
            <div style="background: rgba(10,10,46,0.95); border-radius: 15px; padding: 25px; border: 3px solid {q_color}; text-align: center;">
                <p style="font-size: 2.5em; font-weight: bold; color: {q_color};">{q_name}</p>
                <p>L = {L_map:.2f} | D = {D_map:.2f}</p>
                <p style="color:#FFD700; font-size: 1.3em;">{T_I['S_label']} = {S_val:.2f}</p>
                <p style="color:#aaa; font-size: 0.9em;">({L_score}/140 | {D_score}/140)</p>
                <p>{advice}</p>
            </div>
            """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e'); ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.set_xlabel("البراءة (D)", color='white'); ax.set_ylabel("الولاء (L)", color='white')
        ax.add_patch(Rectangle((0, 0), 1, 1, color=COLORS["مؤمن"], alpha=0.2))
        ax.add_patch(Rectangle((-1, 0), 1, 1, color=COLORS["كافر"], alpha=0.2))
        ax.add_patch(Rectangle((-1, -1), 1, 1, color=COLORS["منافق"], alpha=0.2))
        ax.add_patch(Rectangle((0, -1), 1, 1, color=COLORS["مشرك"], alpha=0.3))
        ax.text(0.5, 0.5, "مؤمن", ha='center', alpha=0.8); ax.text(-0.5, 0.5, "كافر", ha='center', alpha=0.8)
        ax.text(-0.5, -0.5, "منافق", ha='center', alpha=0.8); ax.text(0.5, -0.5, "مشرك", ha='center', alpha=0.8)
        ax.scatter(D_map, L_map, c='#00FFFF', s=250, edgecolors='white', linewidth=3, zorder=10)
        ax.tick_params(colors='white')
        st.pyplot(fig)

        if st.button(T_I["reset_btn"]): st.session_state.compass_answers = {}; st.rerun()
            # =============================================
# 📖 كتاب المختبر القرآني – النسخة الذهبية
# =============================================
with tabs[2]:
    st.header("📖 كتاب المختبر القرآني")
    st.subheader("من الثنائية الكونية إلى معادلة الوجود – نظرية الميزان")
    st.caption("تأليف: علي عادل العاطفي | © 2026")
    st.divider()

    with st.expander("📜 الإهداء والمقدمة", expanded=False):
        st.markdown("""
        ### الإهداء

        إلى كل باحث عن الحقيقة، يبحث عن الخيط الناظم الذي يربط شتات هذا الوجود.
        إلى كل قلب حائر، يبحث عن الطمأنينة في زمن القلق.
        وإلى كل عقل متعطش، يريد أن يرى كيف يلتقي الوحي بالعلم.

        هذا الكتاب هو محاولة متواضعة لإعادة الأمور إلى نصابها، ولإثبات أن "الدين" ليس مجرد طقوس،
        بل هو "نظام التشغيل" الذي صممه الخالق لهذا الكون. إنه "الميزان" الذي وضعه الله،
        والذي يجب أن نتعلم كيف نقرأه في كتابه المسطور (القرآن) وكتابه المنظور (الكون).

        ### مقدمة المؤلف

        الحمد لله الذي رفع السماء ووضع الميزان، وجعل في كل شيء آية تدل على أنه الواحد الديان.
        والصلاة والسلام على النبي الأمي الذي أرسله الله بالدين القيم والإسلام الحنيف،
        رحمة للعالمين، وقدوة للسالكين.

        أما بعد، فهذا كتاب "المختبر القرآني". وهو ليس كتاباً كغيره من الكتب. إنه محاولة متواضعة،
        ولكنها جادة، لإعادة بناء "نظرية كل شيء" على أسس الوحي، بدلاً من أسس الفلسفة البشرية القاصرة.
        إنه يقدم "الدين القيم" (قانون السببية الأعظم) و"الإسلام الحنيف" (الاستجابة المثلى لهذا القانون)
        كمنظومة متكاملة تفسر الوجود من الذرة إلى الحضارة، ومن الأزل إلى الخلود.

        لقد حاولتُ أن أتتبع هذه المنظومة في كتاب الله المسطور (القرآن)، وفي كتابه المنظور (الآفاق والأنفس)،
        وأن أثبت أنهما يلتقيان على "ميزان" واحد دقيق، هو المعادلة:

        **S = W × B**

        حيث S هو الثبات الوجودي (Stability)، وW هو الولاء لله (Wala')، وB هي البراءة من الطاغوت (Bara'a).
        هذه المعادلة البسيطة في لفظها، العميقة في معناها، هي المفتاح الذي يفتح مغاليق كثيرة،
        ويجيب عن أسئلة حائرة.

        هذا الكتاب هو ثمرة تدبر وبحث. وهو ليس "علماً" يضاف إلى العلوم، بل هو "أم العلم"
        التي تنتظم تحتها كل العلوم. والله أسأل أن يجعله خالصاً لوجهه، وأن ينفع به كاتبه وقارئه.
        """)

    with st.expander("🔍 تمهيد: البحث عن نظرية كل شيء", expanded=False):
        st.markdown("""
        منذ فجر الوعي، والبشرية تبحث عن إجابة لسؤال واحد:
        ما هو القانون الذي يحكم هذا الوجود؟
        لماذا تسقط ورقة الشجر بهذه الطريقة؟ ولماذا تسقط الحضارات العظيمة بعد أن تبلغ ذروتها؟
        هل هناك نظام واحد يفسر حركة الذرة والمجرة، ونبض الخلية وفناء الأمم؟

        في الفيزياء، قضى أينشتاين عقوده الأخيرة باحثاً عن "نظرية المجال الموحد"
        التي تجمع قوى الكون في معادلة واحدة. وفي الفلسفة، حاول الفلاسفة منذ أفلاطون وهيغل
        صياغة "نظرية كل شيء" تشرح المعنى الكلي للحياة. كان هذا هو "الكأس المقدسة" للعلم والفلسفة.
        لكنهم لم يصلوا.

        هذا الكتاب يقدم الإجابة التي بحثوا عنها. إجابة ليست من عند فيزيائي، ولا من عند فيلسوف،
        بل من عند خالق الكون نفسه. الإجابة كانت هنا دائماً، في كتابه المسطور (القرآن)،
        وفي كتابه المنظور (الكون). إنها نظرية "الدين القيم"، أو ما نسميه "الميزان".
        إنها تثبت أن هناك قانوناً واحداً فقط، هو "قانون السببية"، يحكم كل شيء:
        الذرة، الخلية، النفس، الأسرة، المجتمع، الأمة، الحضارة، والتاريخ.

        وهذا القانون يجد تعبيره الأكمل في معادلة الثبات الوجودي: **S = W × B**.

        هذه المعادلة ليست اختراعاً بشرياً، بل هي ترجمة رياضية لقوله تعالى:
        ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256].

        في زمن طغت فيه المادة على الروح، يأتي هذا الكتاب ليعيد للروح مكانتها،
        وليثبت أن "الغيب" هو أصل "الشهادة"، وأن "الوحي" هو مرشد "العقل"،
        وأن "الإيمان" هو "طاقة روحية" يمكن قياسها ومحاكاتها.
        """)

    with st.expander("الباب الأول: الأصول – من أين بدأنا؟", expanded=False):
        st.markdown("""
        ### الفصل الأول: ﴿اقْرَأْ بِاسْمِ رَبِّكَ﴾ – المنهج الإلهي لاكتشاف النظام

        في لحظة فارقة من تاريخ البشرية، تنزلت أول كلمة من السماء إلى الأرض.
        لم تكن أمراً عسكرياً، ولا قانوناً اجتماعياً، بل كانت أمراً معرفياً: ﴿اقْرَأْ﴾.
        إنه الإعلان عن مولد "منهج" جديد في النظر إلى الوجود.

        "اقرأ" لم تقتصر على تلاوة الحروف المكتوبة في المصحف، بل شملت قراءة "الكتاب المنظور"
        (الكون والأنفس) وقراءة "الكتاب المسطور" (الوحي). إنها دعوة مزدوجة للجمع بين العلم والإيمان،
        بين الفيزياء والميتافيزيقا، بين الخلق والأمر.

        والأمر لم يكن مطلقاً، بل كان مقيداً بقيد هو "المفتاح" لهذا المنهج: ﴿بِاسْمِ رَبِّكَ﴾.
        هذه هي "عدسة الدين القيم". إنها التي تحول القراءة المادية المحايدة إلى قراءة إيمانية غائية.
        أن تقرأ "باسم ربك" يعني أن تسأل عن "لماذا" و"من" وراء كل ظاهرة، لا أن تكتفي بـ "كيف" حدثت.
        هذا القيد هو "الولاء" (W) الذي يوجه العقل نحو اكتشاف "القانون".

        ### الفصل الثاني: ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ – الإعلان عن القانون الأعظم

        بعد الأمر بالقراءة، يأتي الإعلان عن "القانون" نفسه. يقول الله تعالى:
        ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ﴾ [الرحمن: 7-8].

        هذا هو "الدين القيم". إنه ليس مجرد قوانين فيزيائية تحكم الكون، بل هو أيضاً
        ناموس أخلاقي واجتماعي يحكم حياة الإنسان. إنه القانون الذي يجعل من الذرة مستقرة،
        ومن الخلية حية، ومن الحضارة صامدة.

        لماذا "الميزان"؟ لأن الميزان له كفتان. الكفة الأولى هي "الولاء لله" (W).
        والكفة الثانية هي "البراءة من الطاغوت" (B). والثبات (S) لا يتحقق إلا إذا توازنت الكفتان.

        ### الفصل الثالث: ﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ﴾ – المنهج التجريبي القرآني

        وهذه الآية هي "خريطة الطريق" لمشروعنا:
        ﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ حَتَّىٰ يَتَبَيَّنَ لَهُمْ أَنَّهُ الْحَقُّ﴾ [فصلت: 53].

        إنها دعوة إلهية للبحث العلمي، وللنمذجة والمحاكاة. نحن مدعوون للنظر في "الآفاق"
        (الكون والفيزياء والتاريخ) وفي "الأنفس" (البيولوجيا والنفس والمجتمع)
        لنكتشف "الميزان" الذي يحكم كل شيء.
        """)

    with st.expander("الباب الثاني: التعريفات المركزية – أركان النظرية", expanded=False):
        st.markdown("""
        ### أولاً: الدين القيم – قانون السببية الكوني الثابت

        الدين القيم هو: قانون السببية الأعظم، الثابت في أصله، والمتجدد في تطبيقاته (الحنيفية).
        إنه "الميزان" الذي فطر الله السماوات والأرض عليه، وأرسل به الرسل، وأنزل به الكتب،
        وخلق عليه الإنسان، وعليه الحساب، ومنه الجزاء.

        خصائصه: الربانية (مصدره الله وحده)، الثبات (أصله لا يتغير)، الشمول (يسري على كل العوالم)،
        الحتمية (النتيجة مرتبطة بالسبب)، الديناميكية (يتجدد في تطبيقاته مع ثبات أصله).

        ### ثانياً: الإسلام الحنيف – الاستجابة الكونية الديناميكية

        الإسلام الحنيف هو: الاستجابة الكونية الديناميكية للدين القيم، من خلال آلية
        "الولاء لله" (W) و"البراءة من الطاغوت" (B)، كل عالم بما يناسب فطرته.

        - إسلام الجماد: الجاذبية (W) والتنافر (B). ثباته S = W × B.
        - إسلام النبات والحيوان: النمو (W) والمناعة (B).
        - إسلام الملائكة: التسبيح والعبادة.
        - إسلام الإنسان: الولاء والبراءة طوعاً. S = W × B.

        ### ثالثاً: العقيدة – الإيمان القلبي بعدالة القانون
        العقيدة هي الإيمان القلبي بوحدانية خالق القانون، وعدالة هذا القانون، وحتمية نتائجه.
        وهي تشمل أركان الإيمان الستة. إنها "الطاقة الروحية" التي تولد W في القلب.

        ### رابعاً: العبادة – محطات شحن الميزان
        العبادات ليست طقوساً، بل هي "محطات شحن" للميزان:
        الصلاة تشحن W يومياً. الزكاة تمنع طغيان التمكين E على المناعة B.
        الصيام يدرب B على مقاومة الهوى. الحج محاكاة سنوية كاملة للمعادلة.

        ### خامساً: الشريعة – المنهج والنظام
        الشريعة هي المنهج التفصيلي للعقيدة، والنظام المتكامل للعبادة.
        إنها "دليل المستخدم" الذي يضمن صحة الإيمان وصحة العمل.
        """)

    with st.expander("الباب الثالث: الثنائية الكونية – الولاء والبراء في مرآة الوجود", expanded=False):
        st.markdown("""
        ### الكون يتكلم بلغة الثنائيات
        النور والظلام، الليل والنهار، الذكر والأنثى، الموجب والسالب، الجذب والتنافر.
        هذه الثنائيات ليست عشوائية، بل هي تعبير عن قانون واحد هو "الميزان".
        الولاء والبراء ليسا مفهومين أخلاقيين فقط، بل هما الثنائية الكونية الأساسية.

        ### التطابق مع قوانين الفيزياء
        الجاذبية (W) والتنافر (B) في الذرة. الديناميكا الحرارية: الولاء يقلل الفوضى والبراءة تمنعها.
        التشابك الكمومي: ترابط المؤمنين بالولاء. النفق الكمومي: التوبة تخترق حاجز المعصية.

        ### التطابق مع البيولوجيا
        جهاز المناعة: تمييز الذات (W) من اللاذات (B). السرطان: استدراج بيولوجي (W شاذ، B=0).

        ### الدليل من الحروف المقطعة والأنظمة العددية
        أربعة عشر حرفاً نورانياً (الثوابت) وأربعة عشر حرفاً (المتغيرات).
        النظام السداسي (أيام الخلق وسور الم). النظام الخماسي (الحواس وسور الر).
        النظام السباعي (السماوات وسور حم).
        """)

    with st.expander("الباب الرابع: وحدة الخلق والأمر – الدليل الكوني", expanded=False):
        st.markdown("""
        ### ﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ﴾ – وحدة المصدر
        الخالق والشارع واحد. القانون الذي يحكم الذرة (الخلق) هو نفسه الذي شرعه الله للإنسان (الأمر).
        لا يوجد تناقض بين "العلم" و"الدين". لا يوجد انفصام بين "الفيزياء" و"الشريعة".

        ### الميزان في الآفاق – فيزياء الميزان
        الجاذبية (W) والتنافر (B) في الذرة. استقرار الذرة S = W × B.
        اختبرنا هذا في مختبرنا الرقمي: نسبة W إلى B تقارب الواحد الصحيح في ذرة الهيدروجين.

        ### الميزان في الكيمياء
        الاتحاد (W) والتفكك (B) في التفاعلات. طاقة التنشيط = التوبة.
        العامل المساعد = الأنبياء والقرآن. الاتزان الكيميائي = الثبات الديناميكي.

        ### الميزان في الأنفس – بيولوجيا الميزان
        جهاز المناعة: ذات (W) ولاذات (B). أمراض المناعة الذاتية: خلل في W.
        السرطان = استدراج بيولوجي: نمو متسارع (W شاذ) ومناعة منهارة (B=0).

        ### الميزان في التاريخ – سنة الله في الأمم
        الدولة الأموية: انهارت بفساد المناعة B. الاتحاد السوفيتي: انهار بانهيار الإيمان W.
        الدولة العثمانية: استدراج طويل (تمكين E مرتفع وثبات S منهار).
        """)

    with st.expander("الباب الخامس: المختبر – تشغيل المحاكاة ورؤية الاستدراج", expanded=False):
        st.markdown("""
        ### لماذا النمذجة الحاسوبية؟
        لترجمة الوحي إلى لغة العصر. لإثبات أن السنن الإلهية قوانين قابلة للبرمجة والمحاكاة.

        ### الحالات الأربع للكائن البشري (ألوان النجوم)
        - **الذهبي**: المؤمن (W عالية، B عالية). الثبات الكامل.
        - **البرتقالي**: المشرك (W عالية، B منهارة). ولاء بلا مناعة.
        - **الأحمر**: الكافر (W منهارة، B عالية). براءة بلا ولاء.
        - **الوردي**: المنافق (W منهارة، B منهارة). تيه وضياع.

        ### سرعة الضوء الأخلاقية – إثبات الاستدراج
        في لوحة الإثبات، المنحنى الذهبي S يسبق دائماً المنحنى السماوي E.
        هذه هي فجوة الاستدراج: التمكين يتأخر عن الثبات.
        تنهار S أولاً، ثم يلحقها E بفارق زمني. هذا يفسر لماذا يزدهر الظالمون قبل سقوطهم.
        """)

    with st.expander("الباب السادس: نحو الأمة الذهبية – من المختبر إلى الواقع", expanded=False):
        st.markdown("""
        ### إعادة تعريف الذات
        أين أنت على خريطة الميزان؟ ما هو لون نجمتك؟
        التشخيص الذاتي هو أول خطوة في رحلة التحول.

        ### ورشة البناء – كيف نصنع إنساناً ذهبياً؟
        **توليد W (محطات الشحن):** الصلاة، القرآن، الذكر، الدعاء.
        **بناء B (تقوية المناعة):** مخالفة الهوى، الأمر بالمعروف، النهي عن المنكر، دراسة سيرة الأنبياء.
        **التوازن بين W و B:** فقه الأولويات. لا تقدم B على W قبل أوانها.

        ### هندسة المجتمع الذهبي
        **خلايا النحل:** بناء الجماعة التي تشحن W و B.
        **صناعة القدوة:** إنتاج ذهبيين في كل مجال (طب، هندسة، تجارة، فن).
        **بناء المؤسسات:** تحويل المبادئ إلى أنظمة تحفظ المسيرة عبر الأجيال.
        """)

    with st.expander("الباب السابع: الفطرة – نظام التشغيل الأصلي", expanded=False):
        st.markdown("""
        ### الميثاق الغليظ – يوم قالوا بلى
        ﴿أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾ [الأعراف: 172].
        هذه "البلى" الأزلية هي بذرة W المزروعة في أعماق كل نفس بشرية.
        كل طفل يولد على الفطرة. إنه "المسلم" بالفطرة.

        ### بنية الفطرة (نظام التشغيل)
        تتكون من أربع دوائر متداخلة:
        1. التطلع إلى المطلق (منبع W).
        2. حب الخلود وكراهية الفناء (منبع B).
        3. حب الخير وكراهية الشر (الميزان الداخلي S).
        4. الحاجة إلى المعنى (سؤال "لماذا").

        ### محاولات إسكات الفطرة (ثلاث طرق فاشلة)
        - عبادة العقل المجرد: تنتهي إلى قلق وجودي.
        - عبادة المادة والشهوة: تنتهي إلى فراغ أعمق.
        - عبادة الذات: تنتهي إلى عزلة وجودية.
        الوحي هو الماء الذي يروي ظمأ الفطرة.
        """)

    with st.expander("الباب الثامن: التشخيص – واقع الأمة في ميزان S = W × B", expanded=False):
        st.markdown("""
        ### حال الميزان اليوم
        W (الولاء) ضعيفة ومشتتة. B (البراءة) منهارة تقريباً.
        S (الثبات) في الحضيض. E (التمكين) إما منهار أو متضخم كالورم الخبيث.

        ### الانفصام الخماسي
        - الانفصام العقدي: تحولت "لا إله إلا الله" إلى شعار.
        - الانفصام التشريعي: استبدال شرع الله بقوانين وضعية.
        - الانفصام الأخلاقي: ازدواجية بين المسجد والسوق.
        - الانفصام الاجتماعي: تفكك الأسرة وضعف صلة الرحم.
        - الانفصام السياسي: تمزق الأمة إلى دويلات متناحرة.

        ### الأسباب الجذرية
        - الخلل في فهم "لا إله إلا الله".
        - الانهيار التربوي.
        - الغزو الفكري والثقافي.
        - التبعية الاقتصادية.
        - غياب القدوة الذهبية الجامعة.
        """)

    with st.expander("الباب التاسع: سبل العودة إلى القانون – كيف نعيد ضبط الميزان؟", expanded=False):
        st.markdown("""
        ### الحركة الأولى: الإصلاح الفردي – بناء الإنسان الذهبي
        - العلاج المعرفي: تصحيح فهم التوحيد.
        - العلاج القلبي: تطهير القلب بالذكر والقرآن والدعاء.
        - العلاج السلوكي: تحويل العبادة إلى سلوك.

        ### الحركة الثانية: الإصلاح الأسري – بناء الحصن الاجتماعي
        - التأسيس السليم: اختيار الزوج الصالح.
        - التربية الواعية: غرس حب الله في الأبناء.
        - العلاج الحكيم: حل المشكلات بالحوار.

        ### الحركة الثالثة: الإصلاح المجتمعي – بناء الجماعة المؤمنة
        - إحياء روح الجماعة: الهجرة من الفردانية.
        - بناء المؤسسات الفاعلة.
        - تفعيل الأمر بالمعروف والنهي عن المنكر.

        ### الحركة الرابعة: انتظار سنة التمكين – الصبر الاستراتيجي
        الصبر على فجوة الاستدراج. الثقة بوعد الله. البقاء ذهبياً حتى يأتي النصر.
        """)

    with st.expander("الباب العاشر: اكتمال الدائرة – من الأزل إلى الخلود", expanded=False):
        st.markdown("""
        ### المراحل الخمس للوجود
        **الطور الأول: الأزل – الميثاق الغليظ.**
        غُرس أصل W في الفطرة: ﴿أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾.

        **الطور الثاني: الخلق – كلمة "كُنْ".**
        الكاف (20) + النون (50) = العين (70). الأمر الإلهي + النور = الوجود المُدرَك.

        **الطور الثالث: عالم الشهادة – الاستجابة للقانون.**
        الجماد قسراً، النبات والحيوان غريزةً، الملائكة روحاً، الإنسان اختياراً.

        **الطور الرابع: السنن الإلهية – القوانين الحاكمة.**
        سنة التغيير، سنة التمكين، سنة الاستدراج، سنة التدافع.

        **الطور الخامس: الخلود – الميزان يوم القيامة.**
        ﴿وَنَضَعُ الْمَوَازِينَ الْقِسْطَ لِيَوْمِ الْقِيَامَةِ﴾.
        فمن أقام الميزان في الدنيا، استقر ميزانه في الآخرة.

        ---
        اكتملت الدائرة. من ﴿اقْرَأْ﴾ إلى "الميزان"، من الأزل إلى الخلود.
        لم يعد الوجود فوضى، بل نظام. لم يعد التاريخ عبثاً، بل سنة. لم يعد الموت نهاية، بل عدالة.
        """)
        # =============================================
# 📜 رسالة الترحيب ودليل المستخدم – النسخة الذهبية
# =============================================
with tabs[4]:
    st.header("📜 رسالة الترحيب")
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 1.1em; line-height: 2.5; color: #CCCCCC;">

        > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
        > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"

        ---

        <b>الدين القيم</b> هو قانون السببية الكوني، الحق لأن واضعه الحق،
        والقيم لأنه من القيوم نفسه. هو القانون الأعظم الذي أزال الله به العدم،
        وأوجد به الخلق، وأجرى به السنن، وسيكون به الجزاء.

        إنه <b>"الميزان"</b> الذي قامت به السماوات والأرض،
        والذي يدور حوله كل شيء، من الأزل إلى الخلود.

        ---

        التوازن والانهيار، السقوط والصمود، الثبات والاستقرار:
        في الذرة والمجرة، في المادة والروح، في الفرد والحضارة،
        في الفيزياء والكيمياء والبيولوجيا والأخلاق –
        كله نتيجة حتمية لمدى <b>الإسلام الحنيف</b>،
        وهو الاستجابة الديناميكية المثلى للقانون الإلهي
        من خلال تحقيق التوازن في الولاء والبراءة،
        كلٌّ بما يناسب فطرته.

        ---

        <div style="font-size: 1.2em; color: #FFD700; line-height: 2.5; text-align: center;">
        <b>
        ﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ وَلَهُ أَسْلَمَ مَن فِي السَّمَاوَاتِ وَالْأَرْضِ طَوْعًا وَكَرْهًا وَإِلَيْهِ يُرْجَعُونَ﴾
        <br>— سورة آل عمران، الآية 83
        </b>
        </div>

        ---

        > "أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.<br>
        > استقراركم ليس صدفة. انهياركم ليس حظاً سيئاً.<br>
        > إنها معادلة. إنها <b style="color: #FFD700;">S = W × B</b>."

        ---

        هذا المشهد المتكامل الذي يجمع الذرة والمجرة،
        الفرد والحضارة، المادة والروح،
        إنما يسير بقانون واحد هو <b style="color: #FFD700;">S = W × B</b>.

        ---

        **الدين القيم** = القانون الإلهي الذي يسري على كل شيء من الأزل إلى الخلود.

        **الإسلام الحنيف** = الاستجابة الديناميكية المثلى للقانون الإلهي
        من خلال تحقيق التوازن في الولاء والبراءة.

        ---

        <div style="font-size: 1.2em; color: #FFD700; line-height: 2.5; text-align: center;">
        <b>
        ﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ
        لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ وَلَٰكِنَّ أَكْثَرَ النَّاسِ لَا يَعْلَمُونَ﴾
        <br>— سورة الروم، الآية 30
        </b>
        </div>

        ---

        <b style="color: #FFD700;">© 2026 علي عادل العاطفي | Ali Adel Alatifi</b>

        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # =============================================
    # 📖 دليل المستخدم
    # =============================================
    st.header("📖 دليل المستخدم")
    
    with st.expander("🎯 نظرة عامة على المختبر القرآني", expanded=False):
        st.markdown("""
        مرحباً بك في **"المختبر القرآني – النسخة الذهبية"**، التطبيق التفاعلي 
        الذي يجمع بين الوحي والعلم في محاكاة حية. يعتمد التطبيق على معادلة وحيدة 
        هي `S = W × B`، حيث:
        - **S (الثبات):** هو الاستقرار الناتج عن توازن القطبين.
        - **W (الولاء):** قوة الإيمان والعمل الصالح.
        - **B (البراءة):** قوة المناعة ضد الفساد والطاغوت.
        
        يحتوي التطبيق على **ستة أقسام رئيسية** يمكن التنقل بينها عبر الألسنة في الأعلى.
        """)
    
    with st.expander("🏛️ المختبر الجماعي", expanded=False):
        st.markdown("""
        **هو قلب التطبيق.** يعرض محاكاة بصرية لحركة المجتمع بناءً على المتغيرات 
        التي تتحكم بها. يحتوي على **الميزان الأخروي المرئي** و**الجزيئات الكيميائية** 
        و**العدادات الحية**.
        
        **كيف تستخدمه:**
        1. اذهب إلى قسم **المختبر الجماعي**.
        2. أسفل المشهد، ستجد زر **"⚙️ مؤثرات الثبات الجماعي"**. اضغط عليه لفتح لوحة التحكم.
        3. اضبط المتغيرات (شعائر، حكم، إصلاح، أخلاق) كما تشاء.
        4. اضغط على **▶️ تشغيل** لمشاهدة المحاكاة الحية.
        5. راقب المؤشرات العلوية والميزان الأخروي وهو يتحرك حسب الحسنات والسيئات.
        6. لاحظ **لوحة الإثبات** التي تفضح الاستدراج: الثبات (S) ينهار أولاً ثم يلحقه التمكين (E).
        """)

    with st.expander("🧭 المختبر الفردي (البوصلة الكونية)", expanded=False):
        st.markdown("""
        **اختبار شخصي** مكون من 28 سؤالاً يساعدك على اكتشاف موقعك في فضاء الولاء والبراءة.
        
        **كيف تستخدمه:**
        1. اذهب إلى قسم **المختبر الفردي**.
        2. أجب عن الأسئلة بصدق. كل سؤال في موسع مستقل.
        3. بعد الانتهاء، ستظهر نتيجتك مباشرة: إحداثياتك (L, D)، ثباتك الوجودي (S)، 
           وموقعك على خريطة الأرباع الأربعة (مؤمن، كافر، منافق، مشرك).
        """)

    with st.expander("📖 كتاب المختبر القرآني", expanded=False):
        st.markdown("""
        **يحتوي على النص النظري الكامل** للمشروع. مقسم إلى عشرة أبواب، 
        من الأصول الفلسفية إلى التطبيقات العملية. مناسب للقراءة المتعمقة لفهم أسس المحاكاة.
        
        **كيف تستخدمه:**
        * تصفحه كأي كتاب إلكتروني. المحتوى مقدم في أقسام قابلة للطي لتسهيل القراءة.
        """)

    with st.expander("🔤 المعجم الهندسي", expanded=False):
        st.markdown("""
        **قاموس يحول 45 مشغلاً قرآنياً** (مثل: الفاء، الواو، اللام) إلى رموز رياضية.
        يحتوي أيضاً على **قاعدة بيانات الحروف الـ 28** (نورانية، محايدة، ظلامية) 
        مع قيم حساب الجمل والآيات القرآنية.
        
        **كيف تستخدمه:**
        * مرجع سريع لفهم "لغة" المحاكاة. يمكن للباحثين استخدامه لدراسة البنية 
          الرياضية للنص القرآني.
        """)

    with st.expander("📜 رسالة الترحيب", expanded=False):
        st.markdown("""
        **المدخل الفلسفي** للمشروع. يشرح الفكرة العامة والمعادلة المركزية 
        مع الآيات القرآنية الكريمة.
        """)

    with st.expander("📋 الدليل المرجعي", expanded=False):
        st.markdown("""
        **يحتوي على معلومات** عن المؤلف، حقوق الملكية، والترخيص.
        """)

    st.divider()

    with st.expander("🌟 نصائح للاستخدام", expanded=False):
        st.markdown("""
        1. **ابدأ بالبوصلة:** قبل أن تخوض في المختبر، اختبر نفسك بالبوصلة لترى أين تقف.
        2. **جرب التطرف:** في المختبر الجماعي، ارفع جميع المولدات إلى أقصى قيمة (1.0) 
           وشاهد كيف يصبح المجتمع ذهبياً.
        3. **جرب الانهيار:** ارفع جميع المثبطات إلى أقصى قيمة وشاهد كيف يتحول المجتمع 
           إلى اللون الأحمر والوردي.
        4. **لاحظ الاستدراج:** ارفع "استباحة الربا" واخفض "تحريم الربا" ولاحظ كيف تستمر 
           "الهالة" الزرقاء بالتوسع بينما تنهار "الشمس" الذهبية... ثم فجأة يسقط كل شيء.
        5. **راقب الميزان الأخروي:** أثناء المحاكاة، لاحظ الميزان في وسط المشهد وهو يميل 
           حسب تراكم الحسنات والسيئات. هذا هو "العدل الخفي" الذي لا يراه الناس.
        """)

    with st.expander("🛠️ استكشاف الأخطاء وإصلاحها", expanded=False):
        st.markdown("""
        * **التطبيق لا يستجيب:** اضغط على زر **🧹 تنظيف** ثم أعد تشغيل التطبيق.
        * **لا أستطيع رؤية كل الخيارات:** استخدم شريط التمرير الجانبي للصفحة للتنقل.
        * **الرسوم البيانية لا تظهر:** قد يكون الاتصال بالإنترنت بطيئاً. انتظر قليلاً.
        * **أريد العودة للإعدادات الافتراضية:** اضغط على **🔄 إعادة**.
        """)

    st.divider()
    st.info("""
    ### 💡 تذكير مهم
    
    هذا التطبيق هو **محاكاة تعليمية** تهدف إلى تقريب مفهوم السنن الإلهية بطريقة علمية.
    النتائج التي تظهر هي نتائج تقريبية مبنية على نموذج رياضي، وليس وحيًا أو تنبؤًا.
    الهدف هو التدبر في كتاب الله وسننه في الكون، وليس التكهن بالمستقبل.
    """)
    # =============================================
# 🔤 المعجم الهندسي للقرآن – النسخة الذهبية
# =============================================
with tabs[3]:
    st.header("🔤 المعجم الهندسي للقرآن")
    st.subheader("قاموس المشغلات القرآنية – من الحرف إلى الخوارزمية")
    st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi")
    st.divider()

    st.markdown("""
    ### 📖 مدخل إلى المعجم

    الحروف في القرآن ليست مجرد أدوات لغوية، بل هي **"مشغّلات رياضية" (Operators)**
    في لغة السماء. لكل منها وظيفة رياضية دقيقة. هذا هو جوهر "المعجم الهندسي"
    و"نحو الميزان" الذي يحول النص القرآني إلى معادلات قابلة للبرمجة والمحاكاة.

    ---
    """)

    # =============================================
    # قاعدة بيانات الحروف الـ 28 (من الكود الأول)
    # =============================================
    with st.expander("🗄️ قاعدة بيانات الحروف العربية الـ 28", expanded=False):
        st.markdown("### 🔆 الحروف النورانية (14) – الثوابت الإلهية")
        cols_light = st.columns(7)
        light_keys = list(MIZAN_LETTERS["light"].keys())
        for i, key in enumerate(light_keys):
            data = MIZAN_LETTERS["light"][key]
            with cols_light[i % 7]:
                st.markdown(f"""
                <div style="text-align:center; padding:5px; border:1px solid {data['color']}; border-radius:5px; margin:3px;">
                    <span style="font-size:1.5em; color:{data['color']};">{key}</span><br>
                    <small style="color:#CCC;">{data['label']}</small><br>
                    <small style="color:#FFD700;">{data['value']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### ⚙️ الحروف المحايدة (6) – المشغّلات")
        cols_neutral = st.columns(6)
        neutral_keys = list(MIZAN_LETTERS["neutral"].keys())
        for i, key in enumerate(neutral_keys):
            data = MIZAN_LETTERS["neutral"][key]
            with cols_neutral[i % 6]:
                st.markdown(f"""
                <div style="text-align:center; padding:5px; border:1px solid {data['color']}; border-radius:5px; margin:3px;">
                    <span style="font-size:1.5em; color:{data['color']};">{key}</span><br>
                    <small style="color:#CCC;">{data['label']}</small><br>
                    <small style="color:#FFD700;">{data['role']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### 🌑 الحروف الظلامية (8) – قوى الضلال")
        cols_dark = st.columns(8)
        dark_keys = list(MIZAN_LETTERS["dark"].keys())
        for i, key in enumerate(dark_keys):
            data = MIZAN_LETTERS["dark"][key]
            with cols_dark[i % 8]:
                st.markdown(f"""
                <div style="text-align:center; padding:5px; border:1px solid {data['color']}; border-radius:5px; margin:3px;">
                    <span style="font-size:1.5em; color:{data['color']};">{key}</span><br>
                    <small style="color:#CCC;">{data['label']}</small><br>
                    <small style="color:#FFD700;">{data['value']}</small>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    with st.expander("١. أدوات السببية والنتيجة – المعادلات المباشرة", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **الفاء (فَـ)** | **=** | علامة التساوي (النتيجة الحتمية) | ﴿فَمَن يَكْفُرْ... فَقَدِ اسْتَمْسَكَ﴾ |
        | **الباء (بِـ)** | **بـ** | وسيلة التوصيل (السبب المادي) | ﴿بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ﴾ |
        | **اللام (لِـ)** | **→** | سهم الغاية (اتجاه المقصد) | ﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ﴾ |
        | **حتى** | **...** | استمرار السبب حتى تحقق النتيجة | ﴿حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ﴾ |
        | **كي** | **∴** | بيان السبب الغائي المؤكد | ﴿كَيْ لَا يَكُونَ دُولَةً﴾ |
        | **لعل** | **≈** | توقع النتيجة (احتمال راجح) | ﴿لَعَلَّكُمْ تَتَّقُونَ﴾ |
        """)

    with st.expander("٢. أدوات الشرط والجزاء – المعادلات الشرطية", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **إنْ** | **( )ᵒ** | قوس الشرط الاختياري (حرية الإنسان) | ﴿فَإِن تَابُوا وَأَقَامُوا الصَّلَاةَ﴾ |
        | **إذا** | **( )ᶜ** | قوس الشرط المحقق (حتمية الجزاء) | ﴿إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ﴾ |
        | **لو** | **↯** | افتراض سبب ممتنع لبيان امتناع النتيجة | ﴿وَلَوْ شَاءَ اللَّهُ مَا أَشْرَكُوا﴾ |
        | **لولا** | **⛔** | كشف المانع الذي حال دون تحقق النتيجة | ﴿لَوْلَا أَن رَّأَىٰ بُرْهَانَ رَبِّهِ﴾ |
        | **مَنْ** | **( )ᶜ** | شرط محقق للعاقل | ﴿وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا﴾ |
        """)

    with st.expander("٣. الواو – المشغّل المزدوج", expanded=False):
        st.markdown("""
        | النوع | الرمز | الوظيفة في القانون | مثال قرآني |
        |:------|:------|:--------------------|:-----------|
        | **واو الضرب (العمل)** | **×** | ربط شرطي: لا يتم الأمر إلا باجتماع الطرفين | ﴿يَكْفُرْ بِالطَّاغُوتِ وَ يُؤْمِن بِاللَّهِ﴾ |
        | **واو الجمع (الحساب)** | **+** | جمع تراكمي: القيمتان تتراكمان | ﴿خَيْرًا يَرَهُ وَ شَرًّا يَرَهُ﴾ |

        ### 🧠 شجرة قرارات الواو
        لتحديد نوع الواو في أي آية:
        1. ماذا تربط الواو؟ (أفعالاً مطلوبة؟ → انتقل للسؤال 2) (أعمالاً بشرية؟ → واو الجمع +)
        2. ما هو مقام الآية؟ (مقام عمل أو شرط نجاة؟ → واو الضرب ×) (مقام جزاء أو حساب؟ → واو الجمع +)
        """)

    with st.expander("٤. أدوات النفي – تعطيل المعادلات الفاسدة", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **ما** | **≠** | نفي السببية الفاسدة | ﴿مَا أَمْوَالُكُمْ وَلَا أَوْلَادُكُم﴾ |
        | **لا** | **≠** | نفي العلاقة السببية | ﴿لَا عَاصِمَ الْيَوْمَ مِنْ أَمْرِ اللَّهِ﴾ |
        | **لا النافية للجنس** | **∅** | نفي الجنس كله (المجموعة فارغة) | ﴿لَا إِلَٰهَ إِلَّا اللَّهُ﴾ |
        | **لم** | **⨯** | نفي وقوع السبب في الماضي | ﴿لَمْ يَلِدْ وَلَمْ يُولَدْ﴾ |
        | **لن** | **⨯◄◄** | نفي إمكانية تحقق النتيجة مستقبلاً | ﴿لَن تَرَانِي﴾ |
        """)

    with st.expander("٥. أدوات الحصر والاستثناء – حدود المعادلات", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **إلا** | **{}** | حدود المجموعة: تحدد أهل الولاية والنجاة | ﴿إِلَّا مَن رَّحِمَ﴾ |
        | **إنما** | **{}** | حصر العلاقة في مجموعة محددة | ﴿إِنَّمَا وَلِيُّكُمُ اللَّهُ وَرَسُولُهُ﴾ |
        """)

    with st.expander("٦. أدوات التوكيد – صمامات أمان المعادلات", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **إنَّ** | **!!** | صمام أمان: توكيد حقيقة ثابتة | ﴿إِنَّ اللَّهَ لَا يُخْلِفُ الْمِيعَادَ﴾ |
        | **قد** | **✓** | تأكيد وقوع السبب أو قرب النتيجة | ﴿قَدْ أَفْلَحَ الْمُؤْمِنُونَ﴾ |
        | **لام القسم** | **🖐️** | توكيد بالقسم على حتمية النتيجة | ﴿لَتُبْلَوُنَّ فِي أَمْوَالِكُمْ﴾ |
        """)

    with st.expander("٧. أدوات الزمان والمكان – الإحداثيات", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **إذ** | **⏱️** | تحديد لحظة تحقق السبب في الماضي | ﴿وَاذْكُرُوا إِذْ أَنتُمْ قَلِيلٌ﴾ |
        | **إذا (الظرفية)** | **⏱️** | تحديد لحظة تحقق السبب في المستقبل | ﴿إِذَا جَاءَ نَصْرُ اللَّهِ﴾ |
        | **حيث** | **📍** | تحديد مكان تحقق النتيجة | ﴿حَيْثُ خَرَجْتَ فَوَلِّ وَجْهَكَ﴾ |
        """)

    with st.expander("٨. أدوات الاستفهام والردع والتكليف", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **هل** | **؟!** | تقرير حتمية القانون في ضمير المخاطب | ﴿هَلْ جَزَاءُ الْإِحْسَانِ إِلَّا الْإِحْسَانُ﴾ |
        | **كلا** | **⛔** | قطع المعادلة الفاسدة | ﴿كَلَّا إِنَّ الْإِنسَانَ لَيَطْغَىٰ﴾ |
        | **يا** | **📢** | استدعاء المخاطب للتكليف | ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ﴾ |
        """)

    with st.expander("٩. أدوات الاستقبال والتنبيه – المؤقتات والمؤشرات", expanded=False):
        st.markdown("""
        | المشغّل | الرمز | الوظيفة في القانون | مثال قرآني |
        |:---------|:------|:--------------------|:-----------|
        | **سـ** | **◄** | النتيجة القريبة | ﴿سَيُهْزَمُ الْجَمْعُ﴾ |
        | **سوف** | **◄◄** | النتيجة البعيدة أو المؤكدة | ﴿سَوْفَ يُؤْتِيهِمْ أُجُورَهُمْ﴾ |
        | **ها** | **👉** | الإشارة إلى متغير مهم | ﴿هَـ أَنتُمْ هَٰؤُلَاءِ﴾ |
        | **ذا / ذلك** | **👉** | الإشارة إلى نتيجة أو قانون | ﴿ذَٰلِكَ الدِّينُ الْقَيِّمُ﴾ |
        """)

    st.divider()
    st.info("""
    هذا هو المعجم الهندسي الموجز. المعجم الكامل يحتوي على **45 مشغلاً قرآنياً** مع:
    - قواعدها النحوية.
    - رموزها الهندسية.
    - معانيها الرياضية.
    - وظائفها في قانون السببية الإلهي.
    - أمثلة قرآنية متعددة لكل مشغّل.

    يُعد هذا المعجم "حجر رشيد" بين الوحي والخوارزمية، وهو الأداة الأساسية
    لفهم كيفية تحويل النص القرآني إلى كود برمجي قابل للتنفيذ.
    """)

# =============================================
# 📋 الدليل المرجعي – النسخة الذهبية
# =============================================
with tabs[5]:
    st.header("📋 الدليل المرجعي")
    st.markdown("""
    ---

    ### ⚖️ المختبر القرآني – النسخة الذهبية

    **المشروع:** المختبر القرآني – نظرية الميزان (النسخة الذهبية)
    **المعادلة المركزية:** S = W × B
    **المؤلف:** علي عادل العاطفي (Ali Adel Alatifi)
    **البريد الإلكتروني:** abwahmdalsbyhy925@gmail.com
    **الترخيص:** MIT License – يُسمح بالاستخدام والتعديل والنشر مع ذكر المصدر الأصلي والمؤلف.

    © 2026 علي عادل العاطفي. جميع الحقوق محفوظة.

    ---

    ### 📚 مكونات المشروع

    **١. المختبر الجماعي:** محاكاة تفاعلية لتأثير السياسات الشرعية (أسس الحكم، آليات الإصلاح، 
    الأخلاق) على استقرار المجتمع. يستخدم 36 متغيراً مستمداً من القرآن الكريم، مع ميزان أخروي 
    مرئي وجزيئات كيميائية وعدادات حية.

    **٢. المختبر الفردي (البوصلة الكونية):** اختبار تشخيصي ذاتي مكون من 28 سؤالاً، يحدد موقع 
    الفرد على خريطة الأرباع الوجودية (مؤمن، كافر، منافق، مشرك) ويحسب ثباته الوجودي.

    **٣. كتاب المختبر القرآني:** الأبواب العشرة الكاملة التي تشرح النظرية من جذورها الفلسفية 
    إلى تطبيقاتها العملية.

    **٤. المعجم الهندسي للقرآن:** قاموس يحول 45 مشغلاً قرآنياً إلى رموز رياضية قابلة للبرمجة، 
    مع قاعدة بيانات الحروف الـ 28 (نورانية، محايدة، ظلامية).

    **٥. رسالة الترحيب ودليل المستخدم:** شرح وافٍ لكيفية استخدام التطبيق مع نصائح عملية.

    ---

    ### 🛡️ حقوق الملكية الفكرية

    هذا المشروع هو نتاج بحث وتدبر في كتاب الله المسطور (القرآن) وكتابه المنظور (الكون).
    جميع الحقوق محفوظة للمؤلف. وهو محمي بموجب ترخيص MIT License.
    """)

# =============================================
# 📥 تذييل الصفحة
# =============================================
st.divider()
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi | Al-Deen Al-Qayyim – The Cosmic Balance Law")
