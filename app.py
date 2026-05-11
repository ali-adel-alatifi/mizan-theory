import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# إعداد الصفحة
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="مختبر الميزان", page_icon="⚖️", layout="wide")

if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

# ═══════════════════════════════════════════════════════════════
# التنسيق
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri+Quran&display=swap');
.stApp { background: linear-gradient(180deg, #0a0f1e 0%, #0d1528 30%, #0f1a2e 100%); }
h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #FFD700; }
p, label, div { font-family: 'Cairo', sans-serif; color: #E0E0E0; }
.golden-title { font-size: 3.5em; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; }
.verse-text { text-align: center; color: #FFD700; font-family: 'Amiri Quran', 'Cairo', serif; font-size: 1.3em; margin: 15px 0; line-height: 2; }
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; font-size: 1em; width: 100%; transition: all 0.3s ease; font-family: 'Cairo', sans-serif; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; box-shadow: 0 0 25px rgba(255,215,0,0.5); transform: scale(1.02); }
.stTabs [data-baseweb="tab-list"] { gap: 5px; background: rgba(13,21,40,0.8); border-radius: 15px; padding: 5px; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; font-family: 'Cairo', sans-serif; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# دوال أساسية
# ═══════════════════════════════════════════════════════════════
def star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    return '#888888'

def classify(W, B):
    if W >= 0.5 and B >= 0.5: return (T("مؤمن","Believer"), '#FFD700')
    elif W < 0.5 and B >= 0.5: return (T("كافر","Disbeliever"), '#FF5252')
    elif W < 0.5 and B < 0.5: return (T("منافق","Hypocrite"), '#FFB6C1')
    return (T("مشرك","Polytheist"), '#FFA500')

def curvature(W, B):
    if len(W) < 3: return 0
    dW = np.gradient(list(W)); dB = np.gradient(list(B))
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return num / denom

def calc_S(W, B, E, q=1.0):
    return np.clip(W * B * (1 + q * 0.5), 0.001, 1.0)

# ═══════════════════════════════════════════════════════════════
# القاموس الشامل للقيم الإسلامية المؤثرة على W و B
# ═══════════════════════════════════════════════════════════════
ISLAMIC_VALUES = {
    "W_generators": {
        "prayer": {"label": T("الصلاة", "Prayer"), "weight": 0.15, "aya": "﴿إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ﴾"},
        "fasting": {"label": T("الصوم", "Fasting"), "weight": 0.10, "aya": "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ﴾"},
        "hajj": {"label": T("الحج", "Hajj"), "weight": 0.08, "aya": "﴿وَلِلَّهِ عَلَى النَّاسِ حِجُّ الْبَيْتِ﴾"},
        "charity": {"label": T("الصدقة", "Charity"), "weight": 0.07, "aya": "﴿مَّثَلُ الَّذِينَ يُنفِقُونَ أَمْوَالَهُمْ فِي سَبِيلِ اللَّهِ﴾"},
        "remembrance": {"label": T("ذكر الله", "Dhikr"), "weight": 0.12, "aya": "﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾"},
        "trust": {"label": T("التوكل على الله", "Tawakkul"), "weight": 0.10, "aya": "﴿وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ﴾"},
        "quran": {"label": T("تلاوة القرآن", "Reciting Quran"), "weight": 0.10, "aya": "﴿الَّذِينَ آتَيْنَاهُمُ الْكِتَابَ يَتْلُونَهُ حَقَّ تِلَاوَتِهِ﴾"},
        "love_allah": {"label": T("حب الله ورسوله", "Love of Allah & Messenger"), "weight": 0.15, "aya": "﴿وَالَّذِينَ آمَنُوا أَشَدُّ حُبًّا لِّلَّهِ﴾"},
        "alliance_believers": {"label": T("موالاة المؤمنين", "Alliance with Believers"), "weight": 0.12, "aya": "﴿إِنَّمَا وَلِيُّكُمُ اللَّهُ وَرَسُولُهُ وَالَّذِينَ آمَنُوا﴾"},
        "support_oppressed": {"label": T("نصرة المظلومين", "Supporting Oppressed"), "weight": 0.10, "aya": "﴿وَمَا لَكُمْ لَا تُقَاتِلُونَ فِي سَبِيلِ اللَّهِ وَالْمُسْتَضْعَفِينَ﴾"},
        "truthfulness": {"label": T("الصدق", "Truthfulness"), "weight": 0.10, "aya": "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ وَكُونُوا مَعَ الصَّادِقِينَ﴾"},
        "keeping_promises": {"label": T("الوفاء بالعهد", "Keeping Promises"), "weight": 0.08, "aya": "﴿وَأَوْفُوا بِالْعَهْدِ إِنَّ الْعَهْدَ كَانَ مَسْئُولًا﴾"},
        "gratitude": {"label": T("الشكر", "Gratitude"), "weight": 0.10, "aya": "﴿لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ﴾"},
        "patience": {"label": T("الصبر", "Patience"), "weight": 0.12, "aya": "﴿إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾"},
        "repentance": {"label": T("التوبة", "Repentance"), "weight": 0.15, "aya": "﴿إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ﴾"},
        "knowledge": {"label": T("طلب العلم", "Seeking Knowledge"), "weight": 0.08, "aya": "﴿وَقُل رَّبِّ زِدْنِي عِلْمًا﴾"},
        "kindness_parents": {"label": T("بر الوالدين", "Kindness to Parents"), "weight": 0.12, "aya": "﴿وَبِالْوَالِدَيْنِ إِحْسَانًا﴾"},
        "family_ties": {"label": T("صلة الرحم", "Family Ties"), "weight": 0.10, "aya": "﴿وَاتَّقُوا اللَّهَ الَّذِي تَسَاءَلُونَ بِهِ وَالْأَرْحَامَ﴾"},
        "humility": {"label": T("التواضع", "Humility"), "weight": 0.08, "aya": "﴿وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا﴾"},
        "mercy": {"label": T("الرحمة", "Mercy"), "weight": 0.10, "aya": "﴿وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ﴾"},
    },
    "B_generators": {
        "disavowal_taghut": {"label": T("البراءة من الطاغوت", "Disavowal of Taghut"), "weight": 0.20, "aya": "﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ﴾"},
        "enjoining_good": {"label": T("الأمر بالمعروف", "Enjoining Good"), "weight": 0.15, "aya": "﴿وَلْتَكُن مِّنكُمْ أُمَّةٌ يَدْعُونَ إِلَى الْخَيْرِ﴾"},
        "forbidding_evil": {"label": T("النهي عن المنكر", "Forbidding Evil"), "weight": 0.18, "aya": "﴿وَيَنْهَوْنَ عَنِ الْمُنكَرِ﴾"},
        "jihad_self": {"label": T("جهاد النفس", "Jihad of Self"), "weight": 0.15, "aya": "﴿وَجَاهِدُوا فِي اللَّهِ حَقَّ جِهَادِهِ﴾"},
        "jihad_wealth": {"label": T("الجهاد بالمال", "Jihad with Wealth"), "weight": 0.12, "aya": "﴿وَجَاهِدُوا بِأَمْوَالِكُمْ وَأَنفُسِكُمْ﴾"},
        "chastity": {"label": T("العفة", "Chastity"), "weight": 0.12, "aya": "﴿وَلْيَسْتَعْفِفِ الَّذِينَ لَا يَجِدُونَ نِكَاحًا﴾"},
        "hatred_sins": {"label": T("بغض المعاصي", "Hatred of Sins"), "weight": 0.10, "aya": "﴿وَكَرَّهَ إِلَيْكُمُ الْكُفْرَ وَالْفُسُوقَ وَالْعِصْيَانَ﴾"},
        "reject_injustice": {"label": T("رفض الظلم", "Rejecting Injustice"), "weight": 0.15, "aya": "﴿وَلَا تَرْكَنُوا إِلَى الَّذِينَ ظَلَمُوا﴾"},
        "avoid_usury": {"label": T("اجتناب الربا", "Avoiding Usury"), "weight": 0.10, "aya": "﴿وَذَرُوا مَا بَقِيَ مِنَ الرِّبَا﴾"},
        "lowering_gaze": {"label": T("غض البصر", "Lowering Gaze"), "weight": 0.08, "aya": "﴿قُل لِّلْمُؤْمِنِينَ يَغُضُّوا مِنْ أَبْصَارِهِمْ﴾"},
        "honest_testimony": {"label": T("الشهادة بالحق", "Truthful Testimony"), "weight": 0.10, "aya": "﴿وَلَا تَكْتُمُوا الشَّهَادَةَ﴾"},
        "avoid_backbiting": {"label": T("ترك الغيبة", "Avoiding Backbiting"), "weight": 0.10, "aya": "﴿وَلَا يَغْتَب بَّعْضُكُم بَعْضًا﴾"},
        "avoid_lies": {"label": T("ترك الكذب", "Avoiding Lies"), "weight": 0.12, "aya": "﴿وَاجْتَنِبُوا قَوْلَ الزُّورِ﴾"},
        "apply_sharia": {"label": T("تحكيم شرع الله", "Applying Sharia"), "weight": 0.18, "aya": "﴿وَمَن لَّمْ يَحْكُم بِمَا أَنزَلَ اللَّهُ﴾"},
        "justice": {"label": T("العدل", "Justice"), "weight": 0.15, "aya": "﴿إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالْإِحْسَانِ﴾"},
        "consultation": {"label": T("الشورى", "Consultation"), "weight": 0.10, "aya": "﴿وَأَمْرُهُمْ شُورَىٰ بَيْنَهُمْ﴾"},
        "guard_chastity": {"label": T("حفظ الفرج", "Guarding Chastity"), "weight": 0.12, "aya": "﴿وَالَّذِينَ هُمْ لِفُرُوجِهِمْ حَافِظُونَ﴾"},
        "avoid_fraud": {"label": T("ترك الغش", "Avoiding Fraud"), "weight": 0.10, "aya": "﴿مَنْ غَشَّنَا فَلَيْسَ مِنَّا﴾"},
        "love_hate_allah": {"label": T("الحب والبغض في الله", "Love & Hate for Allah"), "weight": 0.15, "aya": "﴿أَشِدَّاءُ عَلَى الْكُفَّارِ رُحَمَاءُ بَيْنَهُمْ﴾"},
    }
}

# ═══════════════════════════════════════════════════════════════
# مصفوفة الترابط بين القيم (الديناميكية الحية للإسلام الحنيف)
# ═══════════════════════════════════════════════════════════════
VALUE_LINKS = {
    "prayer": ["truthfulness", "chastity", "humility", "patience", "remembrance"],
    "fasting": ["chastity", "patience", "humility", "hatred_sins", "jihad_self"],
    "charity": ["gratitude", "humility", "mercy", "support_oppressed"],
    "hajj": ["love_allah", "repentance", "alliance_believers", "humility"],
    "remembrance": ["love_allah", "trust", "patience", "gratitude"],
    "quran": ["knowledge", "truthfulness", "love_allah", "remembrance"],
    "knowledge": ["truthfulness", "enjoining_good", "forbidding_evil", "apply_sharia"],
    "repentance": ["prayer", "charity", "humility", "love_allah"],
    "truthfulness": ["trust", "keeping_promises", "honest_testimony", "alliance_believers"],
    "patience": ["gratitude", "trust", "jihad_self", "humility"],
    "gratitude": ["prayer", "charity", "remembrance", "love_allah"],
    "love_allah": ["prayer", "remembrance", "jihad_self", "repentance"],
    "alliance_believers": ["support_oppressed", "enjoining_good", "jihad_wealth", "apply_sharia"],
    "enjoining_good": ["forbidding_evil", "apply_sharia", "jihad_self", "honest_testimony"],
    "forbidding_evil": ["disavowal_taghut", "jihad_self", "reject_injustice", "hatred_sins"],
    "disavowal_taghut": ["jihad_self", "jihad_wealth", "love_hate_allah", "forbidding_evil"],
    "jihad_self": ["chastity", "patience", "avoid_lies", "lowering_gaze"],
    "jihad_wealth": ["charity", "support_oppressed", "apply_sharia"],
    "apply_sharia": ["justice", "consultation", "reject_injustice", "avoid_usury"],
    "justice": ["reject_injustice", "support_oppressed", "honest_testimony", "alliance_believers"],
    "humility": ["mercy", "patience", "gratitude", "kindness_parents"],
    "mercy": ["charity", "support_oppressed", "kindness_parents", "family_ties"],
}

# ═══════════════════════════════════════════════════════════════
# دالة حساب W و B من القيم المترابطة (الضرب لا الجمع)
# ═══════════════════════════════════════════════════════════════
def compute_WB_interlinked(input_values, base_W=0.05, base_B=0.05, iterations=3):
    enhanced = input_values.copy()
    for _ in range(iterations):
        new_enhanced = enhanced.copy()
        for key in enhanced:
            if key in VALUE_LINKS:
                linked_sum = 0
                for linked_key in VALUE_LINKS[key]:
                    linked_sum += enhanced.get(linked_key, 0.5)
                if len(VALUE_LINKS[key]) > 0:
                    avg_linked = linked_sum / len(VALUE_LINKS[key])
                    new_enhanced[key] = enhanced[key] * 0.7 + avg_linked * 0.3
        enhanced = new_enhanced
    
    W_total = base_W
    for key in ISLAMIC_VALUES["W_generators"]:
        if key in enhanced:
            W_total += enhanced[key] * ISLAMIC_VALUES["W_generators"][key]["weight"]
    
    B_total = base_B
    for key in ISLAMIC_VALUES["B_generators"]:
        if key in enhanced:
            B_total += enhanced[key] * ISLAMIC_VALUES["B_generators"][key]["weight"]
    
    return np.clip(W_total, 0.01, 1.0), np.clip(B_total, 0.01, 1.0)

# ═══════════════════════════════════════════════════════════════
# دالة حساب W و B البسيطة (بدون ترابط)
# ═══════════════════════════════════════════════════════════════
def compute_WB_simple(input_values, base_W=0.1, base_B=0.1):
    W_total = base_W
    B_total = base_B
    for key, val in input_values.items():
        if key in ISLAMIC_VALUES["W_generators"]:
            W_total += val * ISLAMIC_VALUES["W_generators"][key]["weight"]
        elif key in ISLAMIC_VALUES["B_generators"]:
            B_total += val * ISLAMIC_VALUES["B_generators"][key]["weight"]
    return np.clip(W_total, 0.01, 1.0), np.clip(B_total, 0.01, 1.0)

# ═══════════════════════════════════════════════════════════════
# دالة إنشاء منزلقات القيم
# ═══════════════════════════════════════════════════════════════
def create_value_sliders(prefix, W_defaults=None, B_defaults=None):
    if W_defaults is None: W_defaults = {k: 0.5 for k in ISLAMIC_VALUES["W_generators"]}
    if B_defaults is None: B_defaults = {k: 0.5 for k in ISLAMIC_VALUES["B_generators"]}
    values = {}
    col_w, col_b = st.columns(2)
    with col_w:
        st.markdown(f"### 🤍 {T('مولدات الولاء (W)', 'Loyalty Generators (W)')}")
        for key, data in ISLAMIC_VALUES["W_generators"].items():
            values[key] = st.slider(data["label"], 0.0, 1.0, W_defaults.get(key, 0.5), 0.05, key=f"{prefix}_W_{key}", help=data["aya"])
    with col_b:
        st.markdown(f"### ❤️ {T('مولدات البراءة (B)', 'Disavowal Generators (B)')}")
        for key, data in ISLAMIC_VALUES["B_generators"].items():
            values[key] = st.slider(data["label"], 0.0, 1.0, B_defaults.get(key, 0.5), 0.05, key=f"{prefix}_B_{key}", help=data["aya"])
    return values

# ═══════════════════════════════════════════════════════════════
# دالة عرض مصفوفة الترابط
# ═══════════════════════════════════════════════════════════════
def show_value_links(values_dict):
    with st.expander(T("🔗 مصفوفة الترابط بين القيم", "🔗 Value Interconnection Matrix"), expanded=False):
        st.markdown(T(
            "هذه المصفوفة تُظهر كيف تترابط القيم الإسلامية. كل قيمة تؤثر في غيرها. "
            "العلاقة **ضرب لا جمع**: انهيار قيمة واحدة يُضعف المنظومة كلها.",
            "This matrix shows how Islamic values interconnect. Each value affects others. "
            "The relationship is **multiplication, not addition**."
        ))
        W_simple, B_simple = compute_WB_simple(values_dict)
        W_enhanced, B_enhanced = compute_WB_interlinked(values_dict)
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(T("W (بسيط)", "W (Simple)"), f"{W_simple:.3f}")
        with col2: st.metric(T("W (مترابط)", "W (Interlinked)"), f"{W_enhanced:.3f}")
        with col3: st.metric(T("الفرق", "Delta"), f"{W_enhanced - W_simple:+.3f}")
        st.markdown(T("#### 🔗 الروابط النشطة:", "#### 🔗 Active Links:"))
        for key, links in VALUE_LINKS.items():
            if key in values_dict and values_dict[key] > 0.5:
                linked_names = []
                for l in links:
                    if l in ISLAMIC_VALUES["W_generators"]:
                        linked_names.append(ISLAMIC_VALUES["W_generators"][l]["label"])
                    elif l in ISLAMIC_VALUES["B_generators"]:
                        linked_names.append(ISLAMIC_VALUES["B_generators"][l]["label"])
                label = ""
                if key in ISLAMIC_VALUES["W_generators"]: label = ISLAMIC_VALUES["W_generators"][key]["label"]
                elif key in ISLAMIC_VALUES["B_generators"]: label = ISLAMIC_VALUES["B_generators"][key]["label"]
                st.markdown(f"- **{label}** ← " + ", ".join(linked_names))

print("✅ المرحلة الأولى مكتملة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثانية: الجلسة والعنوان وأزرار التحكم والتبويبات
# ═══════════════════════════════════════════════════════════════

# --- الجلسة العامة ---
if 'init' not in st.session_state:
    np.random.seed(42); random.seed(42)
    cx, cy = 14, 10.0; N = 150
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-13, cx+13, N)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, N)
    st.session_state.sw = np.random.uniform(0.1, 1, N)
    st.session_state.sb = np.random.uniform(0.1, 1, N)
    st.session_state.N = N
    st.session_state.W = 0.55; st.session_state.B = 0.52; st.session_state.E = 0.3
    st.session_state.S = 0.55 * 0.52
    st.session_state.pW = deque([0.55], maxlen=50)
    st.session_state.pB = deque([0.52], maxlen=50)
    st.session_state.hS = deque(maxlen=300)
    st.session_state.hE = deque(maxlen=300)
    st.session_state.hx = deque(maxlen=300)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0
    st.session_state.frame = 0
    st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
    st.session_state.kappa_vals = [0.0]
    st.session_state.run = False
    st.session_state.init = True

# --- العنوان الرئيسي ---
col_icon1, col_title, col_icon2 = st.columns([1, 6, 1])
with col_icon1:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{T('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
with col_icon2:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='verse-text'>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    <br><span style='font-size:0.8em;'>S = W × B | ق = ١٠٠ = الحق = الميزان</span>
</div>
""", unsafe_allow_html=True)

# --- أزرار التحكم ---
c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
with c1:
    if st.button("▶️ تشغيل", key="btn_run", use_container_width=True):
        st.session_state.run = True
with c2:
    if st.button("⏹️ إيقاف", key="btn_stop", use_container_width=True):
        st.session_state.run = False
with c3:
    if st.button("English" if L == "ar" else "العربية", key="btn_lang", use_container_width=True):
        st.session_state.lang = "en" if L == "ar" else "ar"
        st.rerun()
with c4:
    lag = st.select_slider(
        T("فجوة الاستدراج", "Istidraj Gap"),
        options=[5, 10, 15, 22, 30, 40, 50],
        value=22, key="lag"
    )
with c5:
    if st.button("🔄 إعادة", key="btn_reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

st.markdown("---")

# --- التبويبات ---
tab_labels = [
    T("🌌 الكون", "🌌 Cosmos"),
    T("🧍 الفرد", "🧍 Individual"),
    T("👥 المجتمع", "👥 Society"),
    T("🏛️ الدولة", "🏛️ State"),
    T("🌍 الأمة", "🌍 Nation"),
    T("🏰 الحضارة", "🏰 Civilization"),
    T("📜 الآخرة", "📜 Hereafter"),
    T("📐 الصراط", "📐 Path"),
]

tabs = st.tabs(tab_labels)

print("✅ المرحلة الثانية مكتملة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثالثة: الكون، الفرد، المجتمع
# ═══════════════════════════════════════════════════════════════

# --- تبويب ١: الكون ---
with tabs[0]:
    st.header(T("🌌 المشهد الكوني", "🌌 The Cosmic Scene"))
    
    with st.expander(T("⚙️ مولدات الطاقة", "⚙️ Energy Generators"), expanded=False):
        cosmic_values = create_value_sliders("cosmic")
        show_value_links(cosmic_values)
    
    placeholder = st.empty()
    
    if st.session_state.get("run", False):
        W, B = compute_WB_interlinked(cosmic_values)
        st.session_state.W = W; st.session_state.B = B
        
        while st.session_state.run:
            W = st.session_state.W; B = st.session_state.B; E = st.session_state.E
            S = st.session_state.S; phase = st.session_state.phase; ca = st.session_state.ca
            aW = st.session_state.aW; aB = st.session_state.aB
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx = st.session_state.cx; cy = st.session_state.cy; eb = st.session_state.eb
            hS = st.session_state.hS; hE = st.session_state.hE; hx = st.session_state.hx
            good = st.session_state.good; bad = st.session_state.bad
            pW = st.session_state.pW; pB = st.session_state.pB; frame = st.session_state.frame
            N = st.session_state.N

            ca += 0.008; sv = np.sin(ca)
            if sv > 0.5: phase = T('ذروة', 'Peak')
            elif sv > 0: phase = T('صعود', 'Rising')
            elif sv > -0.5: phase = T('انهيار', 'Collapse')
            else: phase = T('قاع', 'Bottom')
            if 0.3 < sv < 0.35: phase = T('>> استدراج <<', '>> Istidraj <<')
            target = 0.5 + 0.45 * sv

            for i in range(N):
                dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                nbr = np.where((dist < 2.0) & (np.arange(N) != i))[0]
                sw[i] += (target - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (target - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                if len(nbr) > 0:
                    sw[i] += (np.mean(sw[nbr]) - sw[i]) * 0.03
                    sb[i] += (np.mean(sb[nbr]) - sb[i]) * 0.03
                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)

            if random.random() < 0.005:
                aff = np.random.choice(N, size=int(N * 0.2), replace=False)
                sw[aff] *= random.uniform(0.5, 0.8)
                sb[aff] *= random.uniform(0.5, 0.8)

            W += (np.mean(sw) - W) * 0.04
            B += (np.mean(sb) - B) * 0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            eb.append(S)
            past = list(eb)[-lag] if len(eb) >= lag else S
            E += 0.03 * (past - E)
            W = W - 0.015 * E + 0.03 / (S + 0.1) - 0.007 * (1 - B)
            B = B - 0.012 * E + 0.006 * (1 - B) * W * (1 - W)
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            pW.append(W); pB.append(B)
            frame += 1
            if frame % 2 == 0:
                hS.append(S); hE.append(E); hx.append(len(hx))

            aW += 0.02 + random.uniform(-0.02, 0.02) * (1 - W)**2
            aB += 0.02 + random.uniform(-0.02, 0.02) * (1 - B)**2
            wx = cx + (7 - 2.5 * W) * np.cos(aW)
            wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB)
            by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7

            instability = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.07, 0.07, N) * instability
            sy += np.random.uniform(-0.07, 0.07, N) * instability
            sx = np.clip(sx, cx - 13, cx + 13)
            sy = np.clip(sy, cy - 9, cy + 9)

            good += W * 0.1; bad += (1 - B) * 0.1

            st.session_state.W = W; st.session_state.B = B; st.session_state.E = E; st.session_state.S = S
            st.session_state.phase = phase; st.session_state.ca = ca
            st.session_state.aW = aW; st.session_state.aB = aB; st.session_state.eb = eb
            st.session_state.sx = sx; st.session_state.sy = sy; st.session_state.sw = sw; st.session_state.sb = sb
            st.session_state.pW = pW; st.session_state.pB = pB
            st.session_state.hS = hS; st.session_state.hE = hE; st.session_state.hx = hx; st.session_state.frame = frame
            st.session_state.good = good; st.session_state.bad = bad

            fig, ax = plt.subplots(figsize=(16, 10), facecolor='#0a0f1e')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.6, '#FFD700'), (1.8, 0.3, '#FFD700'), (2.8, 0.1, '#FFA500'), (4, 0.03, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 3 * S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#000', fontsize=14, ha='center', va='center', fontweight='bold')
            ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#0FF', alpha=0.15, zorder=7))
            ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy + 0.8, 'W', color='#FFF', fontsize=10, ha='center')
            ax.text(bx, by + 0.8, 'B', color='#F33', fontsize=10, ha='center')
            colors = [star_color(sw[i], sb[i]) for i in range(N)]
            ax.scatter(sx, sy, s=20, c=colors, alpha=0.9, edgecolors='white', linewidths=0.2, zorder=5)

            # الميزان الأخروي
            akh_x, akh_y, ms = 26.5, 18, 1.5
            ax.plot([akh_x, akh_x], [akh_y - 3, akh_y + 1.5], color='#FFD700', lw=1, alpha=0.4)
            ly = akh_y - 1.5 + ms * min(good / 50, 1.5)
            ry = akh_y - 1.5 - ms * min(bad / 50, 1.5)
            ax.add_patch(Circle((akh_x - 1, ly), 0.6, color='#FFD700', alpha=0.3, zorder=20))
            ax.text(akh_x - 1, ly - 1, T('حسنات', 'Good'), color='#FFD700', fontsize=5, ha='center')
            ax.add_patch(Circle((akh_x + 1, ry), 0.6, color='#FF4444', alpha=0.3, zorder=20))
            ax.text(akh_x + 1, ry - 1, T('سيئات', 'Bad'), color='#FF4444', fontsize=5, ha='center')
            diff = (bad - good) / 50 * ms
            ax.plot([akh_x - 1, akh_x + 1], [akh_y - diff, akh_y + diff], color='#FFD700', lw=1.5, alpha=0.6)

            # منحنى الاستدراج
            pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
            pax.set_xlim(0, 350); pax.set_ylim(0, 1.05)
            pax.set_title(T("S يقود E — الاستدراج", "S leads E — Istidraj"), color='white', fontsize=7)
            pax.tick_params(colors='white', labelsize=5); pax.grid(True, alpha=0.12)
            if hS: pax.plot(list(hx), list(hS), color='#FFD700', lw=2); pax.plot(list(hx), list(hE), color='#0FF', lw=1.5)

            ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f} | κ={curvature(pW, pB):.3f}',
                   color='#CCC', fontsize=9, ha='center')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.06)
    else:
        st.info(T("اضغط ▶️ تشغيل لرؤية المشهد الحي", "Press ▶️ Run to see the live scene"))

    # زر تحميل البيانات
    if not st.session_state.get("run", False) and len(st.session_state.hS) > 0:
        csv_data = "Time,S,E\n" + "\n".join([f"{i},{s:.4f},{e:.4f}" for i, (s, e) in enumerate(zip(st.session_state.hS, st.session_state.hE))])
        st.download_button(
            T("📥 تحميل بيانات المحاكاة", "📥 Download Simulation Data"),
            data=csv_data, file_name="mizan_cosmic.csv", mime="text/csv", key="dl_cosmic"
        )

# --- تبويب ٢: الفرد ---
with tabs[1]:
    st.header(T("🧍 مختبر الفرد", "🧍 Individual Lab"))
    
    indiv_values = create_value_sliders("indiv")
    show_value_links(indiv_values)
    
    if st.button(T("🔍 احسب موقعي", "🔍 Calculate My Position"), key="btn_indiv", use_container_width=True):
        W, B = compute_WB_interlinked(indiv_values)
        S_val = W * B
        name, color = classify(W, B)
        
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric(T("W (الولاء)", "W (Loyalty)"), f"{W:.3f}")
        col_r2.metric(T("B (البراءة)", "B (Disavowal)"), f"{B:.3f}")
        col_r3.metric(T("S (الثبات)", "S (Stability)"), f"{S_val:.3f}")
        
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;border:2px solid {color};text-align:center;margin:15px 0;'>
            <h2 style='color:{color};'>{name}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.15))
        ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF5252', alpha=0.15))
        ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.15))
        ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA500', alpha=0.15))
        ax.text(0.5, 0.5, T("مؤمن", "Believer"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, 0.5, T("كافر", "Disbeliever"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, -0.5, T("منافق", "Hypocrite"), ha='center', color='white', alpha=0.6)
        ax.text(0.5, -0.5, T("مشرك", "Polytheist"), ha='center', color='white', alpha=0.6)
        ax.scatter(B * 2 - 1, W * 2 - 1, s=200, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
        ax.set_xlabel(T("B (البراءة)", "B (Disavowal)"), color='white')
        ax.set_ylabel(T("W (الولاء)", "W (Loyalty)"), color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)

# --- تبويب ٣: المجتمع ---
with tabs[2]:
    st.header(T("👥 مختبر المجتمع", "👥 Society Lab"))
    
    soc_values = create_value_sliders("soc")
    show_value_links(soc_values)
    
    pop = st.slider(T("عدد الأفراد", "Population"), 50, 300, 150, 25, key="pop_soc")
    years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 10, 200, 80, 10, key="yrs_soc")
    
    if st.button(T("🚀 شغّل محاكاة المجتمع", "🚀 Run Society Simulation"), key="btn_soc", use_container_width=True):
        W_base, B_base = compute_WB_interlinked(soc_values)
        pW = np.random.uniform(0.2, 0.9, pop); pB = np.random.uniform(0.2, 0.9, pop)
        px = np.random.uniform(0, 30, pop); py = np.random.uniform(0, 30, pop)
        
        hist_W, hist_B, hist_S = [], [], []
        
        for _ in range(years):
            nW = pW.copy(); nB = pB.copy()
            for i in range(pop):
                d = np.sqrt((px - px[i])**2 + (py - py[i])**2)
                nbr = np.where((d < 2.5) & (np.arange(pop) != i))[0]
                if len(nbr) > 0:
                    nW[i] += 0.03 * (np.mean(pW[nbr]) - pW[i])
                    nB[i] += 0.03 * (np.mean(pB[nbr]) - pB[i])
                nW[i] += 0.02 * (W_base - pW[i]) + 0.01 * (np.random.rand() - 0.5)
                nB[i] += 0.02 * (B_base - pB[i]) + 0.01 * (np.random.rand() - 0.5)
                nW[i] = np.clip(nW[i], 0.01, 1.0); nB[i] = np.clip(nB[i], 0.01, 1.0)
            pW = nW; pB = nB
            px += np.random.randint(-1, 2, pop); py += np.random.randint(-1, 2, pop)
            px = np.clip(px, 0, 29); py = np.clip(py, 0, 29)
            hist_W.append(np.mean(pW)); hist_B.append(np.mean(pB)); hist_S.append(np.mean(pW * pB))
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
        ax1 = axes[0]; ax1.set_facecolor('#0a0f1e')
        colors = [star_color(pW[i], pB[i]) for i in range(pop)]
        ax1.scatter(px, py, c=colors, s=30, alpha=0.8, edgecolors='white', linewidths=0.2)
        ax1.set_xlim(0, 30); ax1.set_ylim(0, 30)
        ax1.set_title(T("خريطة المجتمع", "Society Map"), color='white', fontsize=13)
        ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
        
        ax2 = axes[1]; ax2.set_facecolor('#0a0f1e')
        ax2.plot(hist_W, color='gold', lw=2, label='W')
        ax2.plot(hist_B, color='#FF5252', lw=2, label='B')
        ax2.plot(hist_S, color='#0F8', lw=2, label='S')
        ax2.set_title(T("تطور المجتمع عبر الزمن", "Society Evolution"), color='white', fontsize=13)
        ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white'); ax2.set_ylim(0, 1.05)
        plt.tight_layout(); st.pyplot(fig)
        
        st.metric(T("متوسط S النهائي", "Final Average S"), f"{hist_S[-1]:.3f}")

print("✅ المرحلة الثالثة مكتملة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الرابعة: الدولة، الأمة، الحضارة
# ═══════════════════════════════════════════════════════════════

# --- تبويب ٤: الدولة ---
with tabs[3]:
    st.header(T("🏛️ مختبر الدولة", "🏛️ State Lab"))
    
    state_values = create_value_sliders("state")
    show_value_links(state_values)
    
    state_years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 50, 300, 120, 10, key="yrs_state")
    
    if st.button(T("🚀 شغّل محاكاة الدولة", "🚀 Run State Simulation"), key="btn_state", use_container_width=True):
        W_base, B_base = compute_WB_interlinked(state_values)
        Y = state_years
        
        Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
        Wh[0] = W_base * 0.8; Bh[0] = B_base * 0.8
        Sh[0] = Wh[0] * Bh[0]; Eh[0] = 0.1
        
        for t in range(1, Y):
            Wh[t] = np.clip(Wh[t-1] + 0.03 * (W_base - Wh[t-1]) - 0.01 * Eh[t-1], 0.01, 1.0)
            Bh[t] = np.clip(Bh[t-1] + 0.03 * (B_base - Bh[t-1]) - 0.008 * Eh[t-1], 0.01, 1.0)
            Sh[t] = Wh[t] * Bh[t]
            past = Sh[max(0, t - 15)]
            Eh[t] = np.clip(Eh[t-1] + 0.04 * (past - Eh[t-1]), 0.01, 1.0)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(Sh, 'g-', lw=2, label='S (الثبات)')
        ax.plot(Eh, 'b--', lw=2, label='E (التمكين)')
        ax.plot(Wh, color='gold', lw=1, alpha=0.6, label='W')
        ax.plot(Bh, '#FF5252', lw=1, alpha=0.6, label='B')
        ax.set_title(T("دورة الدولة عبر الزمن", "State Cycle Over Time"), color='white', fontsize=13)
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
        st.pyplot(fig)
        
        idxS = np.argmax(Sh); idxE = np.argmax(Eh)
        c1, c2, c3 = st.columns(3)
        c1.metric(T("S النهائي", "Final S"), f"{Sh[-1]:.3f}")
        c2.metric(T("أقصى S", "Max S"), f"{np.max(Sh):.3f}")
        c3.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, idxE - idxS)} {T('عام', 'yrs')}")

# --- تبويب ٥: الأمة ---
with tabs[4]:
    st.header(T("🌍 مختبر الأمة", "🌍 Nation Lab"))
    
    nation_values = create_value_sliders("nation")
    show_value_links(nation_values)
    
    nation_years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 100, 500, 250, 25, key="yrs_nation")
    
    if st.button(T("🚀 شغّل محاكاة الأمة", "🚀 Run Nation Simulation"), key="btn_nation", use_container_width=True):
        W_base, B_base = compute_WB_interlinked(nation_values)
        Y = nation_years
        
        Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
        Wh[0] = W_base * 0.7; Bh[0] = B_base * 0.7
        Sh[0] = Wh[0] * Bh[0]; Eh[0] = 0.1
        
        for t in range(1, Y):
            Wh[t] = np.clip(Wh[t-1] + 0.02 * (W_base - Wh[t-1]) - 0.008 * Eh[t-1], 0.01, 1.0)
            Bh[t] = np.clip(Bh[t-1] + 0.02 * (B_base - Bh[t-1]) - 0.006 * Eh[t-1], 0.01, 1.0)
            Sh[t] = Wh[t] * Bh[t]
            past = Sh[max(0, t - lag)]
            Eh[t] = np.clip(Eh[t-1] + 0.03 * (past - Eh[t-1]), 0.01, 1.0)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(Sh, 'g-', lw=2, label='S')
        ax.plot(Eh, 'b--', lw=2, label='E')
        ax.plot(Wh, color='gold', lw=1, alpha=0.6, label='W')
        ax.plot(Bh, '#FF5252', lw=1, alpha=0.6, label='B')
        ax.set_title(T("دورة الأمة عبر الزمن", "Nation Cycle Over Time"), color='white', fontsize=13)
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
        st.pyplot(fig)
        
        idxS = np.argmax(Sh); idxE = np.argmax(Eh)
        c1, c2, c3 = st.columns(3)
        c1.metric(T("S النهائي", "Final S"), f"{Sh[-1]:.3f}")
        c2.metric(T("أقصى S", "Max S"), f"{np.max(Sh):.3f}")
        c3.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, idxE - idxS)} {T('عام', 'yrs')}")

# --- تبويب ٦: الحضارة ---
with tabs[5]:
    st.header(T("🏰 مختبر الحضارة", "🏰 Civilization Lab"))
    st.markdown(T("قارن بين حضارتين تبدأ كل منهما بقيم مختلفة.", "Compare two civilizations starting with different values."))
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"### 🟡 {T('الحضارة الأولى', 'Civilization A')}")
        civ_a_values = create_value_sliders("civ_a")
        show_value_links(civ_a_values)
    with col_b:
        st.markdown(f"### 🔴 {T('الحضارة الثانية', 'Civilization B')}")
        civ_b_values = create_value_sliders("civ_b",
            W_defaults={k: 0.2 for k in ISLAMIC_VALUES["W_generators"]},
            B_defaults={k: 0.2 for k in ISLAMIC_VALUES["B_generators"]})
        show_value_links(civ_b_values)
    
    if st.button(T("🚀 شغّل مقارنة الحضارات", "🚀 Run Civilization Comparison"), key="btn_civ", use_container_width=True):
        W_a, B_a = compute_WB_interlinked(civ_a_values)
        W_b, B_b = compute_WB_interlinked(civ_b_values)
        
        Y = 200
        Sh_a = np.zeros(Y); Eh_a = np.zeros(Y)
        Sh_b = np.zeros(Y); Eh_b = np.zeros(Y)
        Wh_a = np.zeros(Y); Bh_a = np.zeros(Y)
        Wh_b = np.zeros(Y); Bh_b = np.zeros(Y)
        
        Wh_a[0] = W_a * 0.8; Bh_a[0] = B_a * 0.8; Sh_a[0] = Wh_a[0] * Bh_a[0]; Eh_a[0] = 0.1
        Wh_b[0] = W_b * 0.8; Bh_b[0] = B_b * 0.8; Sh_b[0] = Wh_b[0] * Bh_b[0]; Eh_b[0] = 0.1
        
        for t in range(1, Y):
            # الحضارة أ
            Wh_a[t] = np.clip(Wh_a[t-1] + 0.02 * (W_a - Wh_a[t-1]) - 0.01 * Eh_a[t-1], 0.01, 1.0)
            Bh_a[t] = np.clip(Bh_a[t-1] + 0.02 * (B_a - Bh_a[t-1]) - 0.008 * Eh_a[t-1], 0.01, 1.0)
            Sh_a[t] = Wh_a[t] * Bh_a[t]
            past_a = Sh_a[max(0, t - 20)]
            Eh_a[t] = np.clip(Eh_a[t-1] + 0.04 * (past_a - Eh_a[t-1]), 0.01, 1.0)
            
            # الحضارة ب
            Wh_b[t] = np.clip(Wh_b[t-1] + 0.02 * (W_b - Wh_b[t-1]) - 0.01 * Eh_b[t-1], 0.01, 1.0)
            Bh_b[t] = np.clip(Bh_b[t-1] + 0.02 * (B_b - Bh_b[t-1]) - 0.008 * Eh_b[t-1], 0.01, 1.0)
            Sh_b[t] = Wh_b[t] * Bh_b[t]
            past_b = Sh_b[max(0, t - 20)]
            Eh_b[t] = np.clip(Eh_b[t-1] + 0.04 * (past_b - Eh_b[t-1]), 0.01, 1.0)
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
        
        ax1 = axes[0]; ax1.set_facecolor('#0a0f1e')
        ax1.plot(Sh_a, 'gold', lw=2, label=T('الحضارة أ (S)', 'Civ A (S)'))
        ax1.plot(Eh_a, 'gold', lw=1.5, ls='--', alpha=0.6, label=T('الحضارة أ (E)', 'Civ A (E)'))
        ax1.plot(Sh_b, '#FF5252', lw=2, label=T('الحضارة ب (S)', 'Civ B (S)'))
        ax1.plot(Eh_b, '#FF5252', lw=1.5, ls='--', alpha=0.6, label=T('الحضارة ب (E)', 'Civ B (E)'))
        ax1.set_title(T("مقارنة الحضارتين", "Civilization Comparison"), color='white', fontsize=13)
        ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
        ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white'); ax1.set_ylim(0, 1.05)
        
        ax2 = axes[1]; ax2.set_facecolor('#0a0f1e')
        ax2.plot(Bh_a, Wh_a, 'gold', lw=1.5, alpha=0.7, label=T('حضارة أ', 'Civ A'))
        ax2.plot(Bh_b, Wh_b, '#FF5252', lw=1.5, alpha=0.7, label=T('حضارة ب', 'Civ B'))
        ax2.scatter(Bh_a[0], Wh_a[0], s=80, c='gold', edgecolors='white', linewidth=2, zorder=10)
        ax2.scatter(Bh_b[0], Wh_b[0], s=80, c='#FF5252', edgecolors='white', linewidth=2, zorder=10)
        ax2.axhline(0.5, color='grey', ls=':', lw=1); ax2.axvline(0.5, color='grey', ls=':', lw=1)
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
        ax2.set_xlabel('B', color='white'); ax2.set_ylabel('W', color='white')
        ax2.set_title(T("المسار في فضاء (W,B)", "Path in (W,B) Space"), color='white', fontsize=13)
        ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
        ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
        plt.tight_layout(); st.pyplot(fig)
        
        c1, c2 = st.columns(2)
        c1.metric(T("S النهائي - حضارة أ", "Final S - Civ A"), f"{Sh_a[-1]:.3f}")
        c2.metric(T("S النهائي - حضارة ب", "Final S - Civ B"), f"{Sh_b[-1]:.3f}")

print("✅ المرحلة الرابعة مكتملة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الخامسة: الآخرة، الصراط، التذييل
# ═══════════════════════════════════════════════════════════════

# --- تبويب ٧: الآخرة ---
with tabs[6]:
    st.header(T("📜 ميزان الآخرة", "📜 Hereafter Balance"))
    st.markdown(T(
        "هذا هو الميزان الأخروي. الحسنات تتراكم مع زيادة W (الولاء)، "
        "والسيئات تتراكم مع نقصان B (البراءة). راقب كفتي الميزان وهما تتحركان.",
        
        "This is the Hereafter Balance. Good deeds accumulate with increasing W (Loyalty), "
        "and bad deeds accumulate with decreasing B (Disavowal). Watch the scales move."
    ))
    
    akh_good = st.session_state.good
    akh_bad = st.session_state.bad
    balance = akh_good - akh_bad
    
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    
    # عمود الميزان
    ax.plot([5, 5], [2, 9], color='#FFD700', lw=3, alpha=0.8)
    
    # العارضة
    tilt = np.clip(balance / 100, -1.5, 1.5)
    ax.plot([3, 7], [5.5 - tilt, 5.5 + tilt], color='#FFD700', lw=4, alpha=0.9)
    
    # كفة الحسنات
    gY = 5.5 - tilt - 1.5
    ax.add_patch(Circle((3, gY), 0.8, color='#FFD700', alpha=0.3, ec='#FFD700', lw=2))
    ax.text(3, gY, f'{akh_good:.0f}', color='#FFD700', fontsize=14, ha='center', va='center', fontweight='bold')
    ax.text(3, gY - 1.5, T('حسنات', 'Good Deeds'), color='#FFD700', fontsize=11, ha='center')
    
    # كفة السيئات
    bY = 5.5 + tilt + 1.5
    ax.add_patch(Circle((7, bY), 0.8, color='#FF4444', alpha=0.3, ec='#FF4444', lw=2))
    ax.text(7, bY, f'{akh_bad:.0f}', color='#FF4444', fontsize=14, ha='center', va='center', fontweight='bold')
    ax.text(7, bY - 1.5, T('سيئات', 'Bad Deeds'), color='#FF4444', fontsize=11, ha='center')
    
    # نتيجة الميزان
    if balance > 0:
        result_text = T("راجحة", "Winning")
        result_color = '#FFD700'
    elif balance < 0:
        result_text = T("خاسرة", "Losing")
        result_color = '#FF4444'
    else:
        result_text = T("متوازنة", "Balanced")
        result_color = '#888'
    
    ax.text(5, 1, result_text, color=result_color, fontsize=16, ha='center', fontweight='bold')
    ax.set_title(T("الميزان الأخروي", "The Hereafter Balance"), color='white', fontsize=16, fontweight='bold')
    st.pyplot(fig)
    
    col1, col2, col3 = st.columns(3)
    col1.metric(T("الحسنات", "Good Deeds"), f"{akh_good:.1f}")
    col2.metric(T("السيئات", "Bad Deeds"), f"{akh_bad:.1f}")
    col3.metric(
        T("الميزان", "Balance"), 
        f"{balance:+.1f}",
        delta=T("راجحة", "Winning") if balance > 0 else T("خاسرة", "Losing")
    )

# --- تبويب ٨: الصراط ---
with tabs[7]:
    st.header(T("📐 هندسة الصراط", "📐 Path Geometry"))
    st.markdown(T(
        "هذا المختبر يُريك كيف ينحني مسارك في فضاء (W, B) بالمعصية، "
        "وكيف تعيده التوبة إلى الاستقامة. الخط الذهبي هو الصراط المستقيم (κ = 0)، "
        "وهو مسار إبراهيم عليه السلام.",
        
        "This lab shows how your path curves in (W, B) space with sin, "
        "and how repentance straightens it. The gold line is the Straight Path (κ = 0), "
        "the path of Abraham (AS)."
    ))
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(T("▶️ خطوة", "▶️ Step"), key="btn_step8", use_container_width=True):
            Wc = st.session_state.path_W[-1]; Bc = st.session_state.path_B[-1]
            nW = np.clip(Wc + (1 - Wc) * 0.15 + random.uniform(-0.03, 0.03), 0.01, 1.0)
            nB = np.clip(Bc + (1 - Bc) * 0.15 + random.uniform(-0.03, 0.03), 0.01, 1.0)
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.kappa_vals.append(curvature(st.session_state.path_W, st.session_state.path_B))
            st.rerun()
    with c2:
        sin_str = st.slider(T("شدة المعصية", "Sin Strength"), 0.01, 0.2, 0.05, 0.01, key="sl_sin8")
        if st.button(T("⚠️ معصية", "⚠️ Sin"), key="btn_sin8", use_container_width=True):
            Wc = st.session_state.path_W[-1]; Bc = st.session_state.path_B[-1]
            nW = np.clip(Wc - sin_str * (Wc - 0.1) + random.uniform(-0.05, 0.05), 0.01, 1.0)
            nB = np.clip(Bc - sin_str * (Bc - 0.1) + random.uniform(-0.05, 0.05), 0.01, 1.0)
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.kappa_vals.append(curvature(st.session_state.path_W, st.session_state.path_B))
            st.rerun()
    with c3:
        if st.button(T("🕌 توبة", "🕌 Repent"), key="btn_rep8", use_container_width=True):
            Wc = st.session_state.path_W[-1]; Bc = st.session_state.path_B[-1]
            nW = np.clip(Wc + (1 - Wc) * 0.8, 0.01, 1.0)
            nB = np.clip(Bc + (1 - Bc) * 0.8, 0.01, 1.0)
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.kappa_vals.append(0.0)
            st.rerun()
    
    if st.button(T("🔄 إعادة الرحلة", "🔄 Reset Path"), key="btn_reset8", use_container_width=True):
        st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
        st.session_state.kappa_vals = [0.0]
        st.rerun()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0a0f1e')
    
    # رسم المسار
    ax1 = axes[0]
    ax1.set_facecolor('#0a0f1e')
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_xlabel("B (البراءة)", color='white'); ax1.set_ylabel("W (الولاء)", color='white')
    ax1.set_title(T("مسارك في فضاء (W, B)", "Your Path in (W, B) Space"), color='white', fontsize=13)
    
    # الصراط المستقيم
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=2.5, alpha=0.7,
             label=T("الصراط المستقيم (إبراهيم)", "Straight Path (Abraham)"))
    ax1.scatter([1], [1], s=120, c='#FFD700', edgecolors='white', linewidth=2, zorder=10,
                label=T("الكمال (1,1)", "Perfection (1,1)"))
    
    pW = st.session_state.path_W; pB = st.session_state.path_B
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.kappa_vals[i] if i < len(st.session_state.kappa_vals) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2 if kv < 0.05 else 3)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10,
                    label=T("البداية", "Start"))
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10,
                    label=T("الآن", "Now"))
    
    ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
    
    # منحنى الانحناء
    ax2 = axes[1]
    ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.kappa_vals, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6,
                label=T("حد الخطر (0.05)", "Danger Threshold (0.05)"))
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4,
                label=T("الصراط (0.0)", "Straight Path (0.0)"))
    ax2.set_title(T("منحنى الانحناء عبر الزمن", "Curvature Over Time"), color='white', fontsize=13)
    ax2.set_xlabel(T("الخطوات", "Steps"), color='white')
    ax2.set_ylabel("κ (الانحناء)", color='white')
    ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
    max_kappa = max(st.session_state.kappa_vals) if st.session_state.kappa_vals else 0.1
    ax2.set_ylim(-0.01, max(0.2, max_kappa * 1.2))
    
    plt.tight_layout(); st.pyplot(fig)
    
    # مؤشرات حية
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("W (الولاء)", f"{pW[-1]:.3f}")
    c2.metric("B (البراءة)", f"{pB[-1]:.3f}")
    current_kappa = st.session_state.kappa_vals[-1] if st.session_state.kappa_vals else 0.0
    c3.metric("κ (الانحناء)", f"{current_kappa:.4f}")
    
    on_path = current_kappa < 0.03
    c4.metric(
        T("الصراط؟", "On Path?"),
        T("✅ نعم", "✅ YES") if on_path else T("⚠️ لا", "⚠️ NO")
    )
    
    # المعادلات
    with st.expander(T("📖 معادلات المختبر", "📖 Lab Equations"), expanded=False):
        st.markdown(T("""
        **١. المسار (Path):**
        $$
        \\gamma(t) = (B(t), W(t))
        $$
        حيث $t$ هو الزمن (الخطوات).
        
        **٢. الانحناء (Curvature):**
        $$
        \\kappa(t) = \\frac{|W' B'' - B' W''|}{(W'^2 + B'^2)^{3/2}}
        $$
        - $\\kappa = 0$: الصراط المستقيم (لا معصية).
        - $\\kappa > 0$: انحراف (معصية).
        
        **٣. قوة المعصية:**
        $$
        \\frac{d\\gamma}{dt} = -\\text{قوة المعصية} \\times (\\gamma - \\gamma_{\\text{الهاوية}})
        $$
        
        **٤. قوة التوبة:**
        $$
        \\gamma_{\\text{جديد}} = \\gamma + \\text{صدق التوبة} \\times (\\gamma_{\\text{الكمال}} - \\gamma)
        $$
        
        **٥. المسار الإبراهيمي (الجيوديسي):**
        $$
        \\gamma_{\\text{إبراهيم}}(t): \\kappa(t) = 0, \\|\\dot{\\gamma}\\| = \\text{const}
        $$
        """,
        """
        **1. Path:** $\\gamma(t) = (B(t), W(t))$ where $t$ is time (steps).
        
        **2. Curvature:** $\\kappa(t) = \\frac{|W' B'' - B' W''|}{(W'^2 + B'^2)^{3/2}}$
        - $\\kappa = 0$: Straight Path (no sin).
        - $\\kappa > 0$: Deviation (sin).
        
        **3. Sin Force:** pulls away from the straight path.
        
        **4. Repentance Force:** pulls toward perfection (1,1).
        
        **5. Abrahamic Geodesic:** $\\gamma_{\\text{Ab}}(t): \\kappa = 0, \\|\\dot{\\gamma}\\| = \\text{const}$
        """))

# ═══════════════════════════════════════════════════════════════
# التذييل
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.3em;">⚖️ مختبر الميزان</p>
    <p>{T('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>
    <p>S = W × B | ق = ١٠٠ = الحق = الميزان</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size:0.8em;margin-top:10px;">
        {T(
            'هذا المختبر شهادة رقمية على أن الله حق، وأن وعده حق، وأن لقاءه حق، وأن الجنة حق، وأن النار حق.',
            'This lab is a digital testimony that Allah is Truth, His promise is true, the meeting with Him is true, Paradise is true, and Hell is true.'
        )}
    </p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الخامسة مكتملة.")
print("✅✅✅ تم بناء مختبر الميزان – النسخة النهائية المتكاملة.")
