import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="مختبر الميزان – القانون الواحد", page_icon="⚖️", layout="wide")

if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri+Quran&display=swap');
.stApp { background: linear-gradient(180deg, #0a0f1e 0%, #0d1528 30%, #0f1a2e 100%); }
h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #FFD700; }
p, label, div { font-family: 'Cairo', sans-serif; color: #E0E0E0; }
.golden-title { font-size: 3.2em; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; }
.verse-text { text-align: center; color: #FFD700; font-size: 1.3em; margin: 15px 0; line-height: 2; }
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; width: 100%; transition: all 0.3s ease; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; box-shadow: 0 0 25px rgba(255,215,0,0.5); }
.stTabs [data-baseweb="tab-list"] { gap: 5px; background: rgba(13,21,40,0.8); border-radius: 15px; padding: 5px; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: bold; }
.message-box { background: rgba(20,30,60,0.7); border-radius: 15px; padding: 30px; margin: 20px 0; border: 1px solid rgba(255,215,0,0.3); line-height: 2.2; }
</style>
""", unsafe_allow_html=True)

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

# ═══════════════════════════════════════════════════════════════
# النظام النهائي – المنزلقات السبعة مع الحروف المختارة بدقة
# ═══════════════════════════════════════════════════════════════
ISLAMIC_SYSTEM_FINAL = {
    "faith": {
        "label": T("١. الإيمان", "1. Faith"),
        "desc": T("+ إيمان خالص بالله | − إيمان بغير الله", "+ Pure faith in Allah | − Faith in other than Allah"),
        "aya": "﴿آمَنَ الرَّسُولُ﴾",
        "effect_W": 0.30, "effect_B": 0.15,
        "letters": {"ar": "أ", "en": "A"},
    },
    "worship": {
        "label": T("٢. العبادات", "2. Worship"),
        "desc": T("+ إقامة العبادات | − تركها", "+ Performing worship | − Abandoning"),
        "aya": "﴿بُنِيَ الْإِسْلَامُ عَلَىٰ خَمْسٍ﴾",
        "effect_W": 0.20, "effect_B": 0.15,
        "letters": {"ar": "ط", "en": "T"},
    },
    "transactions": {
        "label": T("٣. المعاملات", "3. Transactions"),
        "desc": T("+ تحكيم شرع الله | − الحكم بغيره", "+ Sharia | − Other laws"),
        "aya": "﴿فَاحْكُم بَيْنَهُم بِمَا أَنزَلَ اللَّهُ﴾",
        "effect_W": 0.12, "effect_B": 0.18,
        "letters": {"ar": "س", "en": "S"},
    },
    "morals": {
        "label": T("٤. الأخلاق", "4. Morals"),
        "desc": T("+ موالاة المؤمنين | − موالاة الكفار", "+ Alliance | − Disavowal"),
        "aya": "﴿وَتَعَاوَنُوا عَلَى الْبِرِّ﴾",
        "effect_W": 0.15, "effect_B": 0.10,
        "letters": {"ar": "ي", "en": "Y"},
    },
    "enjoining": {
        "label": T("٥. الأمر والنهي", "5. Enjoining & Forbidding"),
        "desc": T("+ الدعوة للخير | − الأمر بالمنكر", "+ Calling to good | − Calling to evil"),
        "aya": "﴿وَلْتَكُن مِّنكُمْ أُمَّةٌ﴾",
        "effect_W": 0.10, "effect_B": 0.20,
        "letters": {"ar": "ع", "en": "A"},
    },
    "hudud": {
        "label": T("٦. إقامة الحدود", "6. Limits"),
        "desc": T("+ إقامة الحدود | − تعطيلها", "+ Establishing | − Abolishing"),
        "aya": "﴿تِلْكَ حُدُودُ اللَّهِ﴾",
        "effect_W": 0.05, "effect_B": 0.25,
        "letters": {"ar": "ح", "en": "H"},
    },
    "jihad": {
        "label": T("٧. الجهاد", "7. Jihad"),
        "desc": T("+ جهاد في سبيل الله | − قعود", "+ Jihad | − Sitting back"),
        "aya": "﴿وَجَاهِدُوا فِي اللَّهِ﴾",
        "effect_W": 0.15, "effect_B": 0.15,
        "letters": {"ar": "ج", "en": "J"},
    },
}

# ═══════════════════════════════════════════════════════════════
# قاعدة بيانات الشواهد التاريخية (مصححة)
# ═══════════════════════════════════════════════════════════════
HISTORICAL_DATA = {
    T("الخلافة الراشدة (٦٣٢-٦٦١م)", "Rashidun Caliphate (632-661 CE)"): {
        "W": 0.95, "B": 0.95, "E": 0.90,
        "desc": T("أعلى فترات التوازن في التاريخ الإسلامي. الثبات الذاتي.", "Highest balance period. Self-sustained stability.")
    },
    T("الدولة الأموية – أوج التوسع (٧٢٠م)", "Umayyad – Peak Expansion (720 CE)"): {
        "W": 0.50, "B": 0.40, "E": 0.95,
        "desc": T("التمكين هنا امتداد لرصيد الخلافة الراشدة. بداية الاستدراج.", "Empowerment extended from Rashidun reserve. Beginning of Istidraj.")
    },
    T("الدولة الأموية – قبل السقوط (٧٤٠م)", "Umayyad – Before Fall (740 CE)"): {
        "W": 0.25, "B": 0.20, "E": 0.70,
        "desc": T("انهيار W و B مع استمرار التمكين ظاهرياً. استدراج متقدم.", "W and B collapsed while empowerment continued. Advanced Istidraj.")
    },
    T("الدولة العثمانية – أواخر (١٨٠٠م)", "Ottoman Empire – Late (1800 CE)"): {
        "W": 0.35, "B": 0.25, "E": 0.60,
        "desc": T("الرجل المريض: فجوة استدراج طويلة.", "The sick man: Long Istidraj gap.")
    },
    T("الاتحاد السوفيتي (١٩٢٢-١٩٩١م)", "Soviet Union (1922-1991 CE)"): {
        "W": 0.05, "B": 0.10, "E": 0.70,
        "desc": T("W = صفر تقريباً: انهيار مفاجئ.", "W ≈ 0: Sudden collapse.")
    },
}

# ═══════════════════════════════════════════════════════════════
# دالة الحساب
# ═══════════════════════════════════════════════════════════════
def compute_WB_final(values):
    W_total = 0.1; B_total = 0.1
    for key, val in values.items():
        if key in ISLAMIC_SYSTEM_FINAL:
            W_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_W"]
            B_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_B"]
    return np.clip(W_total, 0.01, 1.0), np.clip(B_total, 0.01, 1.0)

# ═══════════════════════════════════════════════════════════════
# أسئلة البوصلة (كل سؤال يؤثر على W و B معًا)
# ═══════════════════════════════════════════════════════════════
COMPASS_QUESTIONS = [
    {"q": T("١. الإيمان بالغيب: أؤمن بالله وملائكته وكتبه ورسله واليوم الآخر والقدر", "1. I believe in Allah, His angels, books, messengers, Last Day, and Decree"), "eff_W": 0.8, "eff_B": 0.2, "key": "Q1"},
    {"q": T("٢. الإيمان بالشهادة: أشهد أن لا إله إلا الله وأن محمداً رسول الله وأعمل بمقتضاهما", "2. I testify there is no god but Allah and Muhammad is His Messenger"), "eff_W": 0.7, "eff_B": 0.3, "key": "Q2"},
    {"q": T("٣. الصلاة: أصلي بخشوع، قلبي حاضر مع الله، وأقيمها في وقتها", "3. I pray with devotion, my heart present, and establish it on time"), "eff_W": 0.7, "eff_B": 0.3, "key": "Q3"},
    {"q": T("٤. الزكاة والصوم: أؤدي الزكاة طيبة بها نفسي وأصوم إيماناً واحتساباً", "4. I pay Zakat willingly and fast with faith and hope"), "eff_W": 0.5, "eff_B": 0.5, "key": "Q4"},
    {"q": T("٥. الحج: في قلبي شوق لبيت الله وأسعى لأداء الحج", "5. I long for the House of Allah and strive to perform Hajj"), "eff_W": 0.6, "eff_B": 0.4, "key": "Q5"},
    {"q": T("٦. المعاملات المالية: أصدق في البيع والشراء، وأرفض الربا، وأجتنب أكل المال بالباطل", "6. I am truthful in trade, reject usury, and avoid unjust wealth"), "eff_W": 0.4, "eff_B": 0.6, "key": "Q6"},
    {"q": T("٧. الحكم والعدل: أحكم شرع الله ولا أحكم بغير ما أنزل الله", "7. I rule by Allah's law and do not rule by other than what He revealed"), "eff_W": 0.4, "eff_B": 0.6, "key": "Q7"},
    {"q": T("٨. موالاة المؤمنين: أوالي المؤمنين بقلبي وأحب لهم ما أحب لنفسي", "8. I ally with believers in my heart and love for them what I love for myself"), "eff_W": 0.7, "eff_B": 0.3, "key": "Q8"},
    {"q": T("٩. الصدق والوفاء: أصدق في أقوالي وأفعالي، وأفي بالعهد، وأؤدي الأمانات", "9. I am truthful in words and deeds, keep promises, and fulfill trusts"), "eff_W": 0.6, "eff_B": 0.4, "key": "Q9"},
    {"q": T("١٠. التعاون على البر: أتعاون مع المؤمنين على البر والتقوى", "10. I cooperate with believers in goodness and piety"), "eff_W": 0.6, "eff_B": 0.4, "key": "Q10"},
    {"q": T("١١. الأمر بالمعروف: آمر بالمعروف بالحكمة والموعظة الحسنة", "11. I enjoin good with wisdom and beautiful preaching"), "eff_W": 0.3, "eff_B": 0.7, "key": "Q11"},
    {"q": T("١٢. النهي عن المنكر: أنهى عن المنكر بيدي ولساني وقلبي حسب استطاعتي", "12. I forbid evil with my hand, tongue, and heart according to my ability"), "eff_W": 0.2, "eff_B": 0.8, "key": "Q12"},
    {"q": T("١٣. البراءة الباطنة: أكفر بالطاغوت بقلبي وأتبرأ من كل ما يعبد من دون الله", "13. I disbelieve in Taghut in my heart and disavow all worshipped besides Allah"), "eff_W": 0.2, "eff_B": 0.8, "key": "Q13"},
    {"q": T("١٤. البراءة الظاهرة: أتبرأ من الشرك وأهله ظاهراً ولا أواليهم", "14. I disavow polytheism and its people openly and do not ally with them"), "eff_W": 0.2, "eff_B": 0.8, "key": "Q14"},
    {"q": T("١٥. بغض الكفر والنفاق: أبغض الكفر والنفاق وأهلهما بقلبي", "15. I hate disbelief, hypocrisy, and their people in my heart"), "eff_W": 0.2, "eff_B": 0.8, "key": "Q15"},
    {"q": T("١٦. إقامة الحدود: أقيم حدود الله ولا أتعداها وأمنع المحرمات", "16. I establish Allah's limits, do not transgress them, and prevent prohibitions"), "eff_W": 0.3, "eff_B": 0.7, "key": "Q16"},
    {"q": T("١٧. الجهاد الباطن: أحمل هم الإسلام والمسلمين في قلبي", "17. I carry the concerns of Islam and Muslims in my heart"), "eff_W": 0.5, "eff_B": 0.5, "key": "Q17"},
    {"q": T("١٨. الجهاد بالمال والنفس: أنصر الحق وأهله والمستضعفين بما أستطيع", "18. I support the truth, its people, and the oppressed as much as I can"), "eff_W": 0.4, "eff_B": 0.6, "key": "Q18"},
    {"q": T("١٩. الولاء والبراءة في الله: أحب في الله وأبغض في الله، أوالي أولياءه وأعادي أعداءه", "19. I love and hate for Allah's sake, ally with His allies and oppose His enemies"), "eff_W": 0.5, "eff_B": 0.5, "key": "Q19"},
]

def compute_WB_from_compass(answers):
    W_total = 0.1; B_total = 0.1
    for q in COMPASS_QUESTIONS:
        score = answers.get(q["key"], 0)
        normalized = score / 3.0
        W_total += normalized * q["eff_W"]
        B_total += normalized * q["eff_B"]
    return np.clip(W_total, 0.01, 1.0), np.clip(B_total, 0.01, 1.0)

# ═══════════════════════════════════════════════════════════════
# دالة رسم شجرة الإيمان
# ═══════════════════════════════════════════════════════════════
def render_faith_tree(values_dict, W_val=None, B_val=None):
    if W_val is None or B_val is None:
        W_val, B_val = compute_WB_final(values_dict)
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    
    faith_y = 9
    ax.text(5, faith_y, f"{ISLAMIC_SYSTEM_FINAL['faith']['label']} [أ]\n{values_dict.get('faith', 0):.2f}",
            ha='center', fontsize=12, color='#FFD700', fontweight='bold',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FFD700', boxstyle='round,pad=0.5'))
    
    worship_y = 7
    ax.text(2.5, worship_y, f"{ISLAMIC_SYSTEM_FINAL['worship']['label']} [ط]\n{values_dict.get('worship', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FFA500', boxstyle='round,pad=0.3'))
    ax.text(7.5, worship_y, f"{ISLAMIC_SYSTEM_FINAL['enjoining']['label']} [ع]\n{values_dict.get('enjoining', 0):.2f}",
            ha='center', fontsize=10, color='#00BFFF',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#00BFFF', boxstyle='round,pad=0.3'))
    
    ax.annotate('', xy=(2.5, worship_y+0.3), xytext=(5, faith_y-0.3), arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1.5))
    ax.annotate('', xy=(7.5, worship_y+0.3), xytext=(5, faith_y-0.3), arrowprops=dict(arrowstyle='->', color='#00BFFF', lw=1.5))
    
    trans_y = 5
    ax.text(5, trans_y, f"{ISLAMIC_SYSTEM_FINAL['transactions']['label']} [س]\n{values_dict.get('transactions', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#00FF88', boxstyle='round,pad=0.3'))
    
    ax.annotate('', xy=(5, trans_y+0.3), xytext=(2.5, worship_y-0.3), arrowprops=dict(arrowstyle='->', color='#FFA500', lw=1.5))
    ax.annotate('', xy=(5, trans_y+0.3), xytext=(7.5, worship_y-0.3), arrowprops=dict(arrowstyle='->', color='#00BFFF', lw=1.5))
    
    morals_y = 3
    ax.text(5, morals_y, f"{ISLAMIC_SYSTEM_FINAL['morals']['label']} [ي]\n{values_dict.get('morals', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FF69B4', boxstyle='round,pad=0.3'))
    
    ax.annotate('', xy=(5, morals_y+0.3), xytext=(5, trans_y-0.3), arrowprops=dict(arrowstyle='->', color='#00FF88', lw=1.5))
    
    bottom_y = 1
    ax.text(2.5, bottom_y, f"{ISLAMIC_SYSTEM_FINAL['hudud']['label']} [ح]\n{values_dict.get('hudud', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FF6347', boxstyle='round,pad=0.3'))
    ax.text(7.5, bottom_y, f"{ISLAMIC_SYSTEM_FINAL['jihad']['label']} [ج]\n{values_dict.get('jihad', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FF4500', boxstyle='round,pad=0.3'))
    
    ax.annotate('', xy=(2.5, bottom_y+0.3), xytext=(5, morals_y-0.3), arrowprops=dict(arrowstyle='->', color='#FF69B4', lw=1.5))
    ax.annotate('', xy=(7.5, bottom_y+0.3), xytext=(5, morals_y-0.3), arrowprops=dict(arrowstyle='->', color='#FF69B4', lw=1.5))
    
    ax.text(5, -0.5, f"S = W × B = {W_val:.2f} × {B_val:.2f} = {W_val*B_val:.3f}",
            ha='center', fontsize=14, color='#FFD700', fontweight='bold')
    ax.set_title(T("🌳 شجرة الإيمان – النظام الهرمي", "🌳 Faith Tree – Hierarchical System"), color='white', fontsize=14, fontweight='bold')
    st.pyplot(fig)

def create_final_sliders(prefix, defaults=None):
    if defaults is None: defaults = {k: 0.0 for k in ISLAMIC_SYSTEM_FINAL}
    values = {}
    for key, data in ISLAMIC_SYSTEM_FINAL.items():
        letters_str = data["letters"][L]
        label_with_letters = f"{data['label']}  [{letters_str}]"
        values[key] = st.slider(
            label_with_letters, -1.0, 1.0, defaults.get(key, 0.0), 0.05,
            key=f"{prefix}_{key}",
            help=f"{data['desc']}\n\n{data['aya']}"
        )
    return values

# ═══════════════════════════════════════════════════════════════
# الجلسة العامة
# ═══════════════════════════════════════════════════════════════
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
    st.session_state.pW = deque([0.55], maxlen=50); st.session_state.pB = deque([0.52], maxlen=50)
    st.session_state.hS = deque(maxlen=300); st.session_state.hE = deque(maxlen=300); st.session_state.hx = deque(maxlen=300)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0; st.session_state.frame = 0
    st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]; st.session_state.path_kappa = [0.0]
    for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
        setattr(st.session_state, f"path_{l}", [0.5])
    st.session_state.compass_answers = {}
    st.session_state.challenge = None
    st.session_state.spiritual_nudge = None
    st.session_state.init = True

print("✅ المرحلة الأولى مكتملة: الأساسات والثوابت والدوال والجلسة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثانية: رسالة الترحيب، دليل المستخدم، الميزان الحي، العنوان، التبويبات
# ═══════════════════════════════════════════════════════════════

# --- رسالة الترحيب – النص الكامل ---
with st.expander(T("📜 رسالة ترحيب", "📜 Welcome Message"), expanded=True):
    st.markdown(f"""
    <div class="message-box">
    <h2 style="text-align:center;color:#FFD700;">⚖️ {T('مختبر الميزان', 'The Mizan Lab')}</h2>
    <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;">
    "{T('هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟', 'Is there a single law governing the atom and civilization?')}"
    </p>
    <p>{T(
    'هذا ليس كتابًا، وليس تطبيقًا. هذا مختبر. مختبرٌ صغير، لعله يفتح لك بابًا كبيرًا. '
    'لا ندّعي الحقيقة المطلقة، بل ندعوك لرؤية شيءٍ قد يكون مرّ على قلبك ولم تلاحظه.',
    'This is not a book, nor an app. This is a lab. A small lab, perhaps it opens a big door for you. '
    'We do not claim absolute truth, but invite you to see something that may have passed your heart unnoticed.'
    )}</p>
    <p>{T(
    'تأمل معي: الذرةُ في داخلها قوتان: جاذبيةٌ تجمع، وتنافرٌ يمنع التصادم. لو اختلت إحداهما، لانهارت الذرة. '
    'والخليةُ في جسدك: جهاز مناعةٍ يحمي، وغذاءٌ يبني. لو نامت المناعة، لالتهم المرضُ الجسد.',
    'Reflect with me: the atom has two forces: attraction that gathers, and repulsion that prevents collision. '
    'If one fails, the atom collapses. And the cell in your body: an immune system that protects, and nutrition that builds. '
    'If immunity sleeps, disease devours the body.'
    )}</p>
    <p>{T(
    'وحتى في عالم الكيمياء، يتجلى القانون نفسه: الذرّات المتآلفة تتحد برابطةٍ قوية (هذا ولاؤها)، '
    'لكنها تحتاج إلى "طاقة تنشيط" لتنفصل عن ذراتٍ أخرى كانت مرتبطة بها (هذه براءتها). '
    'إن لم تملك هذه الطاقة، بقيت أسيرة تفاعلاتها القديمة، لا تتحد بالجديد. '
    'هذه "التوبة" الكيميائية: قوةٌ تدفعها لتكسر حاجزًا، فتنطلق إلى استقرارٍ أعظم. '
    'أليس هذا ما يحدث للمؤمن حين يتوب؟',
    'Even in chemistry, the same law manifests: compatible atoms unite with a strong bond (their loyalty), '
    'but they need "activation energy" to separate from other atoms they were bound to (their disavowal). '
    'Without this energy, they remain captive to old reactions, unable to unite with the new. '
    'This is chemical "repentance": a force that pushes them to break a barrier, launching them to greater stability. '
    'Is this not what happens to the believer when they repent?'
    )}</p>
    <p>{T(
    'والمجتمع: ولاءٌ يجمع أفراده، وبراءةٌ من الفساد تحمي تماسكه. لو غاب أحدهما، تفكك المجتمع.',
    'And society: loyalty that gathers its members, and disavowal of corruption that protects its cohesion. '
    'If either is absent, society disintegrates.'
    )}</p>
    <p style="color:#FFD700;font-weight:bold;">{T(
    'هل هذه مصادفة؟ أم أن هناك "قانونًا واحدًا" ينساب في نسيج الوجود كله، من الذرة إلى الحضارة؟',
    'Is this coincidence? Or is there a "single law" flowing through the fabric of existence, from atom to civilization?'
    )}</p>
    <p>{T(
    'نحن هنا لا نعظ. نحن نعرض. لا نفرض عليك جوابًا، بل نتركك تجرب بيدك. '
    'حرّك المنزلقات. أجب عن الأسئلة. شاهد كيف يتغير الثبات. واسأل نفسك: '
    'لماذا ينهار كل شيء عندما يختل أحد القطبين؟ '
    'لماذا تتكرر هذه الثنائية في كل ما حولنا؟ '
    'هل هناك "حق" و"باطل" موجودان في صلب الوجود، لا في كتب الأخلاق فقط؟',
    'We are not preaching. We are presenting. We do not impose an answer, but let you experiment with your own hands. '
    'Move the sliders. Answer the questions. Watch how stability changes. And ask yourself: '
    'Why does everything collapse when one pole fails? '
    'Why does this duality repeat everywhere around us? '
    'Is there "truth" and "falsehood" embedded in the core of existence, not just in books of ethics?'
    )}</p>
    <p style="text-align:center;color:#FFD700;font-size:1.2em;font-weight:bold;">S = W × B</p>
    <p>{T(
    'W: الولاء لله وأوليائه. B: البراءة من الطاغوت وأوليائه. S: الثبات الوجودي.',
    'W: Loyalty to Allah & His allies. B: Disavowal of Taghut & its allies. S: Existential Stability.'
    )}</p>
    <p>{T(
    'هذه معادلة، لا أكثر. ولكنها قد تكون أعمق مما تظن. إنها ليست اختراعًا، بل استنباطٌ من قوله تعالى: '
    '﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾.',
    'This is an equation, nothing more. But it may be deeper than you think. It is not an invention, '
    'but a derivation from His saying: ﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾.'
    )}</p>
    <p style="color:#FFD700;">{T(
    '"العروة الوثقى" هي الثبات الذي تبحث عنه. والطريق إليها مرسومٌ في هذه المنزلقات السبعة وهذه الأسئلة التسعة عشر.',
    '"The Firm Handhold" is the stability you seek. The path to it is drawn in these seven sliders and nineteen questions.'
    )}</p>
    <p style="text-align:center;font-style:italic;color:#AAA;">{T(
    'جرب. تأمل. واسأل. الباب مفتوح.',
    'Try. Reflect. Ask. The door is open.'
    )}</p>
    </div>
    """, unsafe_allow_html=True)

# --- دليل المستخدم ---
with st.expander(T("📖 دليل المستخدم", "📖 User Guide"), expanded=False):
    st.markdown(T("""
    ### 🎯 كيف تستخدم هذا المختبر؟
    
    **١. المنزلقات السبعة:** كل منزلق يحمل اسمه الشرعي وحرفه من المعجم الهندسي [بين قوسين].
    حركه يمينًا (قيم موجبة) لترى كيف يزيد الثبات، ويسارًا (قيم سالبة) لترى كيف ينهار.
    
    **٢. بوصلة الأسئلة (١٩ سؤالاً):** أجب عن الأسئلة لتعرف موقعك الدقيق.
    كل سؤال يؤثر على القطبين (W و B) معًا، لأن كل حركة في حياة المؤمن تولد طاقة للولاء والبراءة معًا.
    
    **٣. تبويب أصل النظرية:** اقرأ النظرية كاملة: من الفطرة إلى الفاتحة، مع شجرة الإيمان البصرية.
    
    **٤. الشواهد التاريخية:** قارن بين الدول التاريخية لترى كيف تنطبق المعادلة على التاريخ الفعلي.
    
    **٥. تحدي اليوم:** تحدٍ جديد كل يوم لتقوية أحد جوانب ميزانك.
    
    **٦. الميزان الأخروي الحي:** يظهر في الشريط الجانبي، ويسجل حسناتك وسيئاتك في الوقت الحقيقي.
    
    **المعادلة المركزية:** S = W × B (العلاقة ضرب لا جمع).
    """,
    """
    ### 🎯 How to Use This Lab
    
    **1. Seven Sliders:** Each holds its Islamic name and geometric letter [in brackets].
    Move right for positive values, left for negative.
    
    **2. 19-Question Compass:** Each question affects both poles (W and B).
    
    **3. Theory Tab:** Read the complete theory with the visual Faith Tree.
    
    **4. Historical Evidence:** Compare nations to see the equation in action.
    
    **5. Daily Challenge:** A new challenge each day.
    
    **6. Live Scales:** Your deeds tracked in real-time in the sidebar.
    
    **Central Equation:** S = W × B (multiplication, not addition).
    """))

# --- الميزان الأخروي الحي ---
def render_live_scales():
    good = st.session_state.get('good', 0)
    bad = st.session_state.get('bad', 0)
    balance = good - bad
    if balance > 0: status, color = T("⚖️ راجحة", "⚖️ Winning"), '#FFD700'
    elif balance < 0: status, color = T("⚖️ خاسرة", "⚖️ Losing"), '#FF4444'
    else: status, color = T("⚖️ متوازنة", "⚖️ Balanced"), '#888'
    st.sidebar.markdown(f"""
    <div style="text-align:center;padding:10px;background:rgba(10,15,30,0.9);border-radius:10px;border:1px solid #FFD700;margin-top:10px;">
        <p style="color:#FFD700;font-size:0.8em;margin:0;">📜 {T('الميزان الحي', 'Live Scales')}</p>
        <p style="color:#FFD700;font-size:0.7em;margin:2px 0;">{T('حسنات', 'Good')}: {good:.0f} | {T('سيئات', 'Bad')}: {bad:.0f}</p>
        <p style="color:{color};font-size:0.9em;margin:0;font-weight:bold;">{status}</p>
    </div>
    """, unsafe_allow_html=True)

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
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("English" if L == "ar" else "العربية", key="btn_lang", use_container_width=True):
        st.session_state.lang = "en" if L == "ar" else "ar"
        st.rerun()

st.markdown("---")

# --- التبويبات ---
tab_labels = [
    T("📖 أصل النظرية", "📖 Theory"),
    T("🌌 الكون", "🌌 Cosmos"),
    T("🧍 الفرد", "🧍 Individual"),
    T("👥 المجتمع", "👥 Society"),
    T("🏛️ الدولة", "🏛️ State"),
    T("🌍 الأمة", "🌍 Nation"),
    T("🏰 الحضارة", "🏰 Civilization"),
    T("📜 الشواهد", "📜 Evidence"),
    T("📐 الصراط", "📐 Path"),
]

tabs = st.tabs(tab_labels)

# --- شريط جانبي للإعدادات ---
with st.sidebar:
    st.markdown("### ⚙️ إعدادات عامة")
    lag = st.select_slider(
        T("فجوة الاستدراج", "Istidraj Gap"),
        options=[5, 10, 15, 22, 30, 40, 50],
        value=22, key="lag"
    )
    st.markdown("---")
    
    # الميزان الأخروي الحي
    render_live_scales()
    
    st.markdown("---")
    
    # تحدي اليوم
    st.markdown(f"### 🎯 {T('تحدي اليوم', 'Daily Challenge')}")
    if st.session_state.get('challenge') is None:
        challenges = [
            T("اليوم: ارفع منزلق 'الصلاة' إلى +0.8 على الأقل.", "Today: Raise 'Prayer' to at least +0.8."),
            T("اليوم: أجب عن أسئلة البوصلة الـ ١٩.", "Today: Answer the 19 compass questions."),
            T("اليوم: شاهد المشهد الكوني لمدة دقيقتين وتأمل.", "Today: Watch the cosmic scene for 2 minutes and reflect."),
            T("اليوم: قارن بين حضارتين في تبويب 'الحضارة'.", "Today: Compare two civilizations in the 'Civilization' tab."),
        ]
        st.session_state.challenge = random.choice(challenges)
    st.info(st.session_state.challenge)
    
    st.markdown("---")
    if st.button("🔄 إعادة ضبط كل شيء", key="btn_reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

print("✅ المرحلة الثانية مكتملة: رسالة الترحيب، دليل المستخدم، الميزان الحي، العنوان، التبويبات، الشريط الجانبي.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثالثة: أصل النظرية، الكون، الفرد
# ═══════════════════════════════════════════════════════════════

# --- تبويب ١: أصل النظرية ---
with tabs[0]:
    st.header(T("📖 أصل النظرية – نظرية الإسلام المتكاملة", "📖 Theory – The Integrated Islamic Theory"))
    
    st.markdown(T("""
    <div style="text-align:center;color:#AAA;font-size:1.1em;margin-bottom:30px;">
    هذه هي <b style="color:#FFD700;">الأسس القرآنية والنبوية</b> التي تثبت أن المعادلة S = W × B 
    ليست اختراعًا بشريًا، بل هي استنباط من كلام الله وسنة رسوله ﷺ.
    </div>
    """, """
    <div style="text-align:center;color:#AAA;font-size:1.1em;margin-bottom:30px;">
    These are the <b style="color:#FFD700;">Quranic and Prophetic foundations</b>.
    </div>
    """), unsafe_allow_html=True)

    with st.expander(T("🌳 ١. الفطرة – نظام التشغيل الأصلي", "🌳 1. The Fitrah"), expanded=True):
        st.markdown(T("""
        **الفطرة** هي نظام التشغيل الأصلي الذي فطر الله الناس عليه.
        إنها استعداد فطري للإيمان، وتطلع إلى المطلق، وسؤال عن الخالق، وإيمان بوجوده.
        وفيها: حب الخلود، كراهية الفناء، حب الخير، كراهية الشر، والبحث عن معنى الوجود.
        
        > ﴿فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ﴾ — الروم ٣٠
        """, """
        **The Fitrah** is the original operating system upon which Allah created humanity.
        """))

    with st.expander(T("🧬 ٢. الإنسان – فائق القانون", "🧬 2. The Human"), expanded=False):
        st.markdown(T("""
        الإنسان مخلوق فريد: فيه من الجماد، وفيه من الحيوان، وفيه من الملائكة.
        لكن الله زاده: عقلًا وإرادة وحرية. فهو **فوق القانون** (يستطيع أن يعصي)،
        و**تحت القانون** (يجزى على فعله). إنه أكرم المخلوقات إذا أطاع، وأسفلها إذا عصى.
        """, """
        The human is unique: above the law (can disobey), under the law (is recompensed).
        """))

    with st.expander(T("⚖️ ٣. الدين القيم – قانون السببية الرباني", "⚖️ 3. The Divine Law"), expanded=False):
        st.markdown(T("""
        **الدين القيم** هو قانون السببية الرباني الذي يسري على جميع العوالم.
        في الفيزياء: جاذبية وتنافر. في الكيمياء: تفاعل وانفصال. في البيولوجيا: ذاتي ولاذاتي.
        
        > ﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ وَلَهُ أَسْلَمَ مَن فِي السَّمَاوَاتِ وَالْأَرْضِ طَوْعًا وَكَرْهًا﴾ — آل عمران ٨٣
        """, """
        **Al-Deen Al-Qayyim** is the divine law of causality governing all worlds.
        """))

    with st.expander(T("🕌 ٤. الإسلام – التسليم الكوني للقانون", "🕌 4. Al-Islam"), expanded=False):
        st.markdown(T("""
        **الإسلام** هو التسليم والخضوع والانقياد الكوني للقانون، عبر آلية **الولاء والبراءة**:
        - **إسلام قهري**: سائر العوالم (الجماد، النبات، الحيوان، الملائكة).
        - **إسلام طوعي**: المؤمن (الولاء لله وأوليائه، البراءة من أعدائه).
        - **إسلام قهري جزئي**: الكافر (يخضع في جسده وموته، ويعصي في تكليفه).
        """, """
        **Al-Islam** is cosmic submission to the law through loyalty and disavowal.
        """))

    with st.expander(T("📜 ٥. العقيدة والعبادة والشريعة", "📜 5. Creed, Worship & Law"), expanded=False):
        st.markdown(T("""
        - **العقيدة**: الإيمان القلبي بالولاء والبراءة.
        - **العبادة**: التطبيق العملي للولاء والبراءة (الصلاة، الزكاة، الصوم، الحج، الجهاد، الأمر بالمعروف).
        - **الشريعة**: منهج العقيدة ونظام العبادة.
        
        العبادات ليست طقوساً، بل **مدارس تدريبية**:
        - **الصلاة**: المختبر اليومي لتجديد العهد (٨٥ مرة يومياً مع الفاتحة).
        - **الزكاة**: مختبر الولاء الاجتماعي والاقتصادي.
        - **الصوم**: معمل تقوية الإرادة على البراءة.
        - **الحج**: مؤتمر الولاء العالمي السنوي.
        """, """
        **Worship** is not ritual, but training schools for loyalty and disavowal.
        """))

    with st.expander(T("📜 ٦. سنن الله في التاريخ", "📜 6. Divine Laws in History"), expanded=False):
        st.markdown(T("""
        - **سنة التغيير**: ﴿إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ﴾
        - **سنة النصر والتمكين**: ﴿وَلَيَنصُرَنَّ اللَّهُ مَن يَنصُرُهُ﴾
        - **سنة الذل والهلاك**: ﴿ضُرِبَتْ عَلَيْهِمُ الذِّلَّةُ﴾
        - **سنة الاستدراج**: ﴿سَنَسْتَدْرِجُهُم مِّنْ حَيْثُ لَا يَعْلَمُونَ﴾
        
        > ﴿فَلَن تَجِدَ لِسُنَّتِ اللَّهِ تَبْدِيلًا ۖ وَلَن تَجِدَ لِسُنَّتِ اللَّهِ تَحْوِيلًا﴾ — فاطر ٤٣
        """, """
        Divine laws in history are as immutable as physical laws.
        """))

    with st.expander(T("🕋 ٧. الحديثان النبويان", "🕋 7. The Two Prophetic Hadiths"), expanded=False):
        st.markdown(T("""
        **الحديث الأول**: «أَوْثَقُ عُرَى الْإِيمَانِ: الْحُبُّ فِي اللَّهِ، وَالْبُغْضُ فِي اللَّهِ»
        - الحب في الله = W (الولاء). البغض في الله = B (البراءة). أوثق عرى الإيمان = S (الثبات).
        
        **الحديث الثاني**: «مَنْ أَحَبَّ لِلَّهِ، وَأَبْغَضَ لِلَّهِ... فَقَدِ اسْتَكْمَلَ الْإِيمَانَ»
        - استكمل الإيمان = S = 1 (الثبات الكامل).
        
        **الواو هنا واو المعية (×) لا واو الجمع (+)**، لأن أوثق عرى الإيمان لا تتم إلا باجتماعهما معًا.
        """, """
        Two prophetic hadiths that prove S = W × B.
        """))

    with st.expander(T("🌳 ٨. شجرة الإيمان – النظام الهرمي", "🌳 8. Faith Tree – Hierarchical System"), expanded=False):
        st.markdown(T(
            "هذه الشجرة تُظهر كيف تترابط المنزلقات السبعة. كل مستوى يغذي الذي فوقه والذي تحته. "
            "العلاقة **ضرب لا جمع**: انهيار أي مستوى يُسقط المنظومة كلها.",
            "This tree shows how the seven sliders interconnect. Each level feeds the one above and below."
        ))
        # استخدام قيم افتراضية للشجرة (0.0) في هذا السياق النظري
        default_vals = {k: 0.0 for k in ISLAMIC_SYSTEM_FINAL}
        render_faith_tree(default_vals)

    with st.expander(T("📖 ٩. الفاتحة – دستور الانسجام الكوني", "📖 9. Al-Fatihah"), expanded=False):
        st.markdown(T("""
        **سورة الفاتحة** هي "خلاصة الكون" في سبع آيات، تجمع قانون السببية الكوني والشرعي كله:
        
        1. **﴿الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ﴾**: إقرار بأن كل نظام الكون من تنظيمه وحده.
        2. **﴿الرَّحْمَٰنِ الرَّحِيمِ﴾**: الذي خلق الكون برحمة، وأبقى باب التوبة مفتوحًا.
        3. **﴿مَالِكِ يَوْمِ الدِّينِ﴾**: يوم تطبيق قانون السببية الأخلاقي الأكبر.
        4. **﴿إِيَّاكَ نَعْبُدُ﴾**: هذا هو الولاء لله (W).
        5. **﴿وَإِيَّاكَ نَسْتَعِينُ﴾**: لا يمكن الالتزام بالقانون إلا بمعونة واضعه.
        6. **﴿اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ﴾**: الصراط هو النظام الكوني الدقيق (κ = 0).
        7. **﴿صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ...﴾**: المنعم عليهم = الذين والوا الله وتبرأوا من الطاغوت.
        
        **النتيجة**: سورة الفاتحة هي "دستور الانسجام الكوني".
        """, """
        Al-Fatihah is the constitution of cosmic harmony.
        """))

    # خاتمة
    st.markdown("---")
    st.markdown(T("""
    <div style="text-align:center;padding:30px;background:rgba(20,30,60,0.7);border-radius:15px;border:1px solid #FFD700;">
        <h3 style="color:#FFD700;">﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ حَتَّىٰ يَتَبَيَّنَ لَهُمْ أَنَّهُ الْحَقُّ﴾</h3>
        <p style="color:#FFD700;">﴿وَفِي الْأَرْضِ آيَاتٌ لِّلْمُوقِنِينَ • وَفِي أَنفُسِكُمْ ۚ أَفَلَا تُبْصِرُونَ﴾</p>
        <p style="color:#AAA;margin-top:15px;">هذا المختبر هو تحقيق لهذا الوعد الإلهي. 'إراءة' رقمية للآيات في الآفاق والأنفس.</p>
    </div>
    """, """
    <div style="text-align:center;padding:30px;background:rgba(20,30,60,0.7);border-radius:15px;border:1px solid #FFD700;">
        <h3 style="color:#FFD700;">﴿We will show them Our signs...﴾</h3>
        <p style="color:#AAA;margin-top:15px;">This lab is a fulfillment of this divine promise.</p>
    </div>
    """), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# تبويب ٢: الكون
# ═══════════════════════════════════════════════════════════════
with tabs[1]:
    st.header(T("🌌 المشهد الكوني", "🌌 The Cosmic Scene"))
    
    with st.expander(T("⚙️ المنزلقات السبعة", "⚙️ Seven Sliders"), expanded=True):
        cosmic_values = create_final_sliders("cosmic")
    
    # شجرة الإيمان في الكون
    with st.expander(T("🌳 شجرة الإيمان", "🌳 Faith Tree"), expanded=False):
        W_cur, B_cur = compute_WB_final(cosmic_values)
        render_faith_tree(cosmic_values, W_cur, B_cur)
    
    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        if st.button(T("▶️ تشغيل المشهد", "▶️ Run Scene"), key="btn_run_cosmic", use_container_width=True, type="primary"):
            st.session_state.run = True
    with col_btn2:
        if st.button(T("⏹️ إيقاف", "⏹️ Stop"), key="btn_stop_cosmic", use_container_width=True):
            st.session_state.run = False
    
    placeholder = st.empty()
    
    if st.session_state.get("run", False):
        W, B = compute_WB_final(cosmic_values)
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
                sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

            if random.random() < 0.005:
                aff = np.random.choice(N, size=int(N * 0.2), replace=False)
                sw[aff] *= random.uniform(0.5, 0.8); sb[aff] *= random.uniform(0.5, 0.8)

            W += (np.mean(sw) - W) * 0.04; B += (np.mean(sb) - B) * 0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            eb.append(S); past = list(eb)[-lag] if len(eb) >= lag else S
            E += 0.03 * (past - E)
            W = W - 0.015 * E + 0.03 / (S + 0.1) - 0.007 * (1 - B)
            B = B - 0.012 * E + 0.006 * (1 - B) * W * (1 - W)
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            pW.append(W); pB.append(B)
            frame += 1
            if frame % 2 == 0: hS.append(S); hE.append(E); hx.append(len(hx))

            aW += 0.02 + random.uniform(-0.02, 0.02) * (1 - W)**2
            aB += 0.02 + random.uniform(-0.02, 0.02) * (1 - B)**2
            wx = cx + (7 - 2.5 * W) * np.cos(aW); wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB); by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7

            instability = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.07, 0.07, N) * instability
            sy += np.random.uniform(-0.07, 0.07, N) * instability
            sx = np.clip(sx, cx - 13, cx + 13); sy = np.clip(sy, cy - 9, cy + 9)

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

            akh_x, akh_y, ms = 26.5, 18, 1.5
            ax.plot([akh_x, akh_x], [akh_y - 3, akh_y + 1.5], color='#FFD700', lw=1, alpha=0.4)
            ly = akh_y - 1.5 + ms * min(good / 50, 1.5); ry = akh_y - 1.5 - ms * min(bad / 50, 1.5)
            ax.add_patch(Circle((akh_x - 1, ly), 0.6, color='#FFD700', alpha=0.3, zorder=20))
            ax.text(akh_x - 1, ly - 1, T('حسنات', 'Good'), color='#FFD700', fontsize=5, ha='center')
            ax.add_patch(Circle((akh_x + 1, ry), 0.6, color='#FF4444', alpha=0.3, zorder=20))
            ax.text(akh_x + 1, ry - 1, T('سيئات', 'Bad'), color='#FF4444', fontsize=5, ha='center')
            diff = (bad - good) / 50 * ms
            ax.plot([akh_x - 1, akh_x + 1], [akh_y - diff, akh_y + diff], color='#FFD700', lw=1.5, alpha=0.6)

            pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
            pax.set_xlim(0, 350); pax.set_ylim(0, 1.05)
            pax.set_title(T("S يقود E — الاستدراج", "S leads E — Istidraj"), color='white', fontsize=7)
            pax.tick_params(colors='white', labelsize=5); pax.grid(True, alpha=0.12)
            if hS: pax.plot(list(hx), list(hS), color='#FFD700', lw=2); pax.plot(list(hx), list(hE), color='#0FF', lw=1.5)

            ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f} | κ={curvature(pW, pB):.3f}', color='#CCC', fontsize=9, ha='center')
            plt.tight_layout(pad=0); placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.06)
    else:
        st.info(T("اضغط ▶️ تشغيل المشهد لرؤية المحاكاة الحية", "Press ▶️ Run Scene to see the live simulation"))

    # زر تحميل البيانات
    if not st.session_state.get("run", False) and len(st.session_state.hS) > 0:
        csv_data = "Time,S,E\n" + "\n".join([f"{i},{s:.4f},{e:.4f}" for i, (s, e) in enumerate(zip(st.session_state.hS, st.session_state.hE))])
        st.download_button(
            T("📥 تحميل بيانات المحاكاة", "📥 Download Simulation Data"),
            data=csv_data, file_name="mizan_cosmic.csv", mime="text/csv", key="dl_cosmic"
        )

# ═══════════════════════════════════════════════════════════════
# تبويب ٣: الفرد (بوصلة الأسئلة ذات التأثير المزدوج)
# ═══════════════════════════════════════════════════════════════
with tabs[2]:
    st.header(T("🧍 مختبر الفرد – بوصلة الميزان", "🧍 Individual Lab – The Mizan Compass"))
    st.markdown(T(
        "أجب عن ١٩ سؤالاً بصدق. كل سؤال يؤثر على **القطبين معًا** (W و B)، "
        "لأن كل حركة في حياة المؤمن تولد طاقة للولاء والبراءة معًا. "
        "بعد الإجابة، ستحصل على تحليل مفصل مع نصائح قرآنية ونبوية.",
        
        "Answer 19 questions honestly. Each question affects **both poles** (W and B), "
        "because every movement in a believer's life generates energy for both loyalty and disavowal. "
        "After answering, you'll receive a detailed analysis with Quranic and Prophetic advice."
    ))
    
    st.markdown(f"### {T('📝 الأسئلة – ١٩ سؤالاً', '📝 Questions – 19 Questions')}")
    
    # عرض الأسئلة في عمودين لتوفير المساحة
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        for i, q_data in enumerate(COMPASS_QUESTIONS[:10]):
            ans = st.radio(
                q_data["q"],
                [T("+٣ نعم", "+3 Yes"), T("٠ حيادي", "0 Neutral"), T("-٣ لا", "-3 No")],
                key=q_data["key"],
                index=None
            )
            if ans:
                if "+٣" in ans: st.session_state.compass_answers[q_data["key"]] = 3
                elif "٠" in ans: st.session_state.compass_answers[q_data["key"]] = 0
                else: st.session_state.compass_answers[q_data["key"]] = -3
    
    with col_q2:
        for i, q_data in enumerate(COMPASS_QUESTIONS[10:]):
            ans = st.radio(
                q_data["q"],
                [T("+٣ نعم", "+3 Yes"), T("٠ حيادي", "0 Neutral"), T("-٣ لا", "-3 No")],
                key=q_data["key"],
                index=None
            )
            if ans:
                if "+٣" in ans: st.session_state.compass_answers[q_data["key"]] = 3
                elif "٠" in ans: st.session_state.compass_answers[q_data["key"]] = 0
                else: st.session_state.compass_answers[q_data["key"]] = -3
    
    TOTAL_Q = 19
    if len(st.session_state.compass_answers) == TOTAL_Q:
        W_val, B_val = compute_WB_from_compass(st.session_state.compass_answers)
        S_val = W_val * B_val
        q_name, q_color = classify(W_val, B_val)
        
        # حساب أقوى وأضعف المجالات
        scores_by_key = {q["key"]: st.session_state.compass_answers.get(q["key"], 0) for q in COMPASS_QUESTIONS}
        sorted_scores = sorted(scores_by_key.items(), key=lambda x: x[1])
        weakest = sorted_scores[:3]
        strongest = sorted_scores[-3:]
        
        # نصائح قرآنية ونبوية
        quranic_advice = {
            "Q3": T("﴿إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ﴾", "﴿Indeed, prayer prohibits immorality and wrongdoing﴾"),
            "Q6": T("﴿وَأَحَلَّ اللَّهُ الْبَيْعَ وَحَرَّمَ الرِّبَا﴾", "﴿Allah has permitted trade and forbidden usury﴾"),
            "Q11": T("﴿وَلْتَكُن مِّنكُمْ أُمَّةٌ يَدْعُونَ إِلَى الْخَيْرِ﴾", "﴿Let there be a nation inviting to good﴾"),
            "Q13": T("﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ﴾", "﴿Whoever disbelieves in Taghut and believes in Allah﴾"),
            "Q19": T("«أَوْثَقُ عُرَى الْإِيمَانِ: الْحُبُّ فِي اللَّهِ، وَالْبُغْضُ فِي اللَّهِ»", "\"The firmest handhold of faith: love for Allah and hatred for Allah\""),
        }
        
        st.divider()
        st.header(T("📊 نتيجة البوصلة", "📊 Compass Result"))
        
        c1, c2, c3 = st.columns(3)
        c1.metric("W (الولاء)", f"{W_val:.2f}")
        c2.metric("B (البراءة)", f"{B_val:.2f}")
        c3.metric("S (الثبات)", f"{S_val:.3f}")
        
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;border:2px solid {q_color};text-align:center;margin:15px 0;'>
            <h2 style='color:{q_color};'>{q_name}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # المستشار الشامل
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;border:1px solid #FFD700;margin:15px 0;'>
            <h3 style='color:#FFD700;'>🧠 {T('المستشار الشامل', 'The Advisor')}</h3>
        """, unsafe_allow_html=True)
        
        if q_name == "مؤمن":
            st.markdown(T(
                "حافظ على ثباتك. استمر في النمو نحو الكمال (1,1). أكثر من النوافل، واجعل لك وردًا من القرآن.",
                "Maintain your stability. Keep growing toward perfection (1,1). Increase voluntary acts."
            ))
        elif q_name == "كافر":
            st.markdown(T(
                "باب التوبة مفتوح على مصراعيه. ابدأ بالتعرف على الله من خلال أسمائه الحسنى. صلِّ ركعتين وادعُ الله.",
                "The door of repentance is wide open. Learn Allah's names. Pray two rak'ahs and ask for guidance."
            ))
        elif q_name == "منافق":
            st.markdown(T(
                "أنت في منطقة الخطر. لكن الخروج منها ممكن. اصدق مع نفسك. اختر طريقًا واحدًا.",
                "You are in the danger zone. But exit is possible. Be honest with yourself. Choose one path."
            ))
        else:
            st.markdown(T(
                "لديك إيمان ولكنك تخلطه بشرك. تعلم معنى 'لا إله إلا الله' حقًا. تخلص من كل مظاهر الشرك.",
                "You have faith but mix it with polytheism. Learn the true meaning of Tawhid."
            ))
        
        st.markdown(T("**🟢 أقوى المجالات:**", "**🟢 Strongest areas:**"))
        for key, score in strongest:
            q_text = next(q["q"] for q in COMPASS_QUESTIONS if q["key"] == key)
            st.markdown(f"- ✅ {q_text.split(':')[0]}")
        
        st.markdown(T("**🔴 مجالات تحتاج تقوية:**", "**🔴 Areas needing strengthening:**"))
        for key, score in weakest:
            if score <= 0:
                q_text = next(q["q"] for q in COMPASS_QUESTIONS if q["key"] == key)
                advice = quranic_advice.get(key, "")
                st.markdown(f"- ⚠️ {q_text.split(':')[0]}")
                if advice: st.markdown(f"  ↳ {advice}")
        
        st.markdown(f"""
        <p style='color:#FFD700;font-size:1.1em;margin-top:15px;'>
        📏 {T('المسافة إلى مقام إبراهيم (1,1):', 'Distance to Station of Abraham (1,1):')} <b>{np.sqrt((1-W_val)**2 + (1-B_val)**2):.3f}</b>
        </p>
        <p style='color:#AAA;font-size:0.9em;'>
        {T('﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ﴾ [الممتحنة: ٤]', '﴿There has certainly been for you an excellent pattern in Abraham.﴾ [Al-Mumtahanah: 4]')}
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # شجرة الإيمان للمستخدم
        with st.expander(T("🌳 شجرة إيمانك", "🌳 Your Faith Tree"), expanded=False):
            compass_values = {}
            # تحويل الإجابات إلى قيم تقريبية للمنزلقات
            compass_values["faith"] = np.clip((scores_by_key.get("Q1", 0) + scores_by_key.get("Q2", 0)) / 6.0, -1, 1)
            compass_values["worship"] = np.clip((scores_by_key.get("Q3", 0) + scores_by_key.get("Q4", 0) + scores_by_key.get("Q5", 0)) / 9.0, -1, 1)
            compass_values["transactions"] = np.clip((scores_by_key.get("Q6", 0) + scores_by_key.get("Q7", 0)) / 6.0, -1, 1)
            compass_values["morals"] = np.clip((scores_by_key.get("Q8", 0) + scores_by_key.get("Q9", 0) + scores_by_key.get("Q10", 0)) / 9.0, -1, 1)
            compass_values["enjoining"] = np.clip((scores_by_key.get("Q11", 0) + scores_by_key.get("Q12", 0)) / 6.0, -1, 1)
            compass_values["hudud"] = np.clip(scores_by_key.get("Q16", 0) / 3.0, -1, 1)
            compass_values["jihad"] = np.clip((scores_by_key.get("Q17", 0) + scores_by_key.get("Q18", 0)) / 6.0, -1, 1)
            render_faith_tree(compass_values, W_val, B_val)
        
        # رسم الخريطة الرباعية
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.15))
        ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF5252', alpha=0.15))
        ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.15))
        ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA500', alpha=0.15))
        ax.text(0.5, 0.5, T("مؤمن","Believer"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, 0.5, T("كافر","Disbeliever"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, -0.5, T("منافق","Hypocrite"), ha='center', color='white', alpha=0.6)
        ax.text(0.5, -0.5, T("مشرك","Polytheist"), ha='center', color='white', alpha=0.6)
        ax.scatter(B_val * 2 - 1, W_val * 2 - 1, s=250, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
        ax.set_xlabel("B (البراءة)", color='white')
        ax.set_ylabel("W (الولاء)", color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        if st.button(T("🔄 أعد الاختبار", "🔄 Retake Test"), key="btn_reset_compass", use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

print("✅ المرحلة الثالثة مكتملة: أصل النظرية (مع شجرة الإيمان)، الكون، الفرد (بالبوصلة المتكاملة).")

# ═══════════════════════════════════════════════════════════════
# المرحلة الرابعة: المجتمع، الدولة، الأمة، الحضارة، الشواهد
# ═══════════════════════════════════════════════════════════════

# --- تبويب ٤: المجتمع ---
with tabs[3]:
    st.header(T("👥 مختبر المجتمع", "👥 Society Lab"))
    st.markdown(T(
        "شاهد كيف تنتشر قيم الولاء (W) والبراءة (B) في مجتمع حي. "
        "اضبط معاملات الأمر بالمعروف والنهي عن المنكر لترى أثرها على تماسك المجتمع.",
        "Watch how Loyalty (W) and Disavowal (B) values spread in a living society. "
        "Adjust enjoining good and forbidding evil to see their impact on social cohesion."
    ))
    
    soc_values = create_final_sliders("soc")
    
    pop = st.slider(T("عدد الأفراد", "Population"), 50, 300, 150, 25, key="pop_soc")
    years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 10, 200, 80, 10, key="yrs_soc")
    
    if st.button(T("🚀 شغّل محاكاة المجتمع", "🚀 Run Society Simulation"), key="btn_soc", use_container_width=True, type="primary"):
        with st.spinner(T("المحاكاة تعمل...", "Simulation running...")):
            W_base, B_base = compute_WB_final(soc_values)
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
            ax2.set_title(T("تطور المجتمع", "Society Evolution"), color='white', fontsize=13)
            ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
            ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white'); ax2.set_ylim(0, 1.05)
            plt.tight_layout(); st.pyplot(fig)
            st.metric(T("متوسط S النهائي", "Final Average S"), f"{hist_S[-1]:.3f}")

# --- تبويب ٥: الدولة ---
with tabs[4]:
    st.header(T("🏛️ مختبر الدولة", "🏛️ State Lab"))
    st.markdown(T(
        "شاهد كيف تؤثر أسس الحكم (العدل، الشورى، تحكيم الشرع) على استقرار الدولة عبر الزمن.",
        "Watch how governance foundations affect state stability over time."
    ))
    
    state_values = create_final_sliders("state")
    state_years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 50, 300, 120, 10, key="yrs_state")
    
    if st.button(T("🚀 شغّل محاكاة الدولة", "🚀 Run State Simulation"), key="btn_state", use_container_width=True, type="primary"):
        with st.spinner(T("المحاكاة تعمل...", "Simulation running...")):
            W_base, B_base = compute_WB_final(state_values)
            Y = state_years
            Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
            Wh[0] = np.clip(W_base, 0.01, 1.0); Bh[0] = np.clip(B_base, 0.01, 1.0)
            Sh[0] = Wh[0] * Bh[0]; Eh[0] = 0.1
            for t in range(1, Y):
                Wh[t] = np.clip(Wh[t-1] + 0.03 * (W_base - Wh[t-1]) - 0.01 * Eh[t-1], 0.01, 1.0)
                Bh[t] = np.clip(Bh[t-1] + 0.03 * (B_base - Bh[t-1]) - 0.008 * Eh[t-1], 0.01, 1.0)
                Sh[t] = Wh[t] * Bh[t]
                past = Sh[max(0, t - 15)]
                Eh[t] = np.clip(Eh[t-1] + 0.04 * (past - Eh[t-1]), 0.01, 1.0)
            
            fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e'); ax.set_facecolor('#0a0f1e')
            ax.plot(Sh, 'g-', lw=2, label='S'); ax.plot(Eh, 'b--', lw=2, label='E')
            ax.plot(Wh, color='gold', lw=1, alpha=0.6, label='W'); ax.plot(Bh, '#FF5252', lw=1, alpha=0.6, label='B')
            ax.set_title(T("دورة الدولة", "State Cycle"), color='white', fontsize=13)
            ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
            ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
            st.pyplot(fig)
            
            idxS = np.argmax(Sh); idxE = np.argmax(Eh)
            c1, c2, c3 = st.columns(3)
            c1.metric(T("S النهائي", "Final S"), f"{Sh[-1]:.3f}")
            c2.metric(T("أقصى S", "Max S"), f"{np.max(Sh):.3f}")
            c3.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, idxE - idxS)} {T('عام', 'yrs')}")
            
            csv_data = "Year,W,B,S,E\n" + "\n".join([f"{t},{Wh[t]:.4f},{Bh[t]:.4f},{Sh[t]:.4f},{Eh[t]:.4f}" for t in range(Y)])
            st.download_button(T("📥 تحميل بيانات الدولة", "📥 Download State Data"), data=csv_data, file_name="mizan_state.csv", mime="text/csv", key="dl_state")

# --- تبويب ٦: الأمة ---
with tabs[5]:
    st.header(T("🌍 مختبر الأمة", "🌍 Nation Lab"))
    st.markdown(T(
        "هذا هو المختبر الإلهي للأمم. اضبط مولدات الطاقة وحدود البراءة، "
        "وشاهد كيف تنهض الأمة أو تنهار عبر الزمن. المعادلة واحدة: S = W × B.",
        "Adjust energy generators and disavowal boundaries, and watch the nation rise or fall."
    ))
    
    nation_values = create_final_sliders("nation")
    nation_years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 100, 500, 250, 25, key="yrs_nation")
    
    if st.button(T("🚀 شغّل محاكاة الأمة", "🚀 Run Nation Simulation"), key="btn_nation", use_container_width=True, type="primary"):
        with st.spinner(T("المحاكاة تعمل...", "Simulation running...")):
            W_base, B_base = compute_WB_final(nation_values)
            Y = nation_years
            Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
            Wh[0] = np.clip(W_base * 0.7, 0.01, 1.0); Bh[0] = np.clip(B_base * 0.7, 0.01, 1.0)
            Sh[0] = Wh[0] * Bh[0]; Eh[0] = 0.1
            for t in range(1, Y):
                Wh[t] = np.clip(Wh[t-1] + 0.02 * (W_base - Wh[t-1]) - 0.008 * Eh[t-1], 0.01, 1.0)
                Bh[t] = np.clip(Bh[t-1] + 0.02 * (B_base - Bh[t-1]) - 0.006 * Eh[t-1], 0.01, 1.0)
                Sh[t] = Wh[t] * Bh[t]
                past = Sh[max(0, t - lag)]
                Eh[t] = np.clip(Eh[t-1] + 0.03 * (past - Eh[t-1]), 0.01, 1.0)
            
            fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e'); ax.set_facecolor('#0a0f1e')
            ax.plot(Sh, 'g-', lw=2, label='S'); ax.plot(Eh, 'b--', lw=2, label='E')
            ax.plot(Wh, color='gold', lw=1, alpha=0.6, label='W'); ax.plot(Bh, '#FF5252', lw=1, alpha=0.6, label='B')
            ax.set_title(T("دورة الأمة", "Nation Cycle"), color='white', fontsize=13)
            ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
            ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
            st.pyplot(fig)
            
            idxS = np.argmax(Sh); idxE = np.argmax(Eh)
            c1, c2, c3 = st.columns(3)
            c1.metric(T("S النهائي", "Final S"), f"{Sh[-1]:.3f}")
            c2.metric(T("أقصى S", "Max S"), f"{np.max(Sh):.3f}")
            c3.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, idxE - idxS)} {T('عام', 'yrs')}")
            
            csv_data = "Year,W,B,S,E\n" + "\n".join([f"{t},{Wh[t]:.4f},{Bh[t]:.4f},{Sh[t]:.4f},{Eh[t]:.4f}" for t in range(Y)])
            st.download_button(T("📥 تحميل بيانات الأمة", "📥 Download Nation Data"), data=csv_data, file_name="mizan_nation.csv", mime="text/csv", key="dl_nation")

# --- تبويب ٧: الحضارة ---
with tabs[6]:
    st.header(T("🏰 مختبر الحضارة", "🏰 Civilization Lab"))
    st.markdown(T("قارن بين حضارتين تبدأ كل منهما بقيم مختلفة.", "Compare two civilizations starting with different values."))
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"### 🟡 {T('الحضارة الأولى', 'Civilization A')}")
        civ_a_values = create_final_sliders("civ_a")
    with col_b:
        st.markdown(f"### 🔴 {T('الحضارة الثانية', 'Civilization B')}")
        civ_b_values = create_final_sliders("civ_b", defaults={k: -0.5 for k in ISLAMIC_SYSTEM_FINAL})
    
    if st.button(T("🚀 شغّل مقارنة الحضارات", "🚀 Run Comparison"), key="btn_civ", use_container_width=True, type="primary"):
        with st.spinner(T("المحاكاة تعمل...", "Simulation running...")):
            W_a, B_a = compute_WB_final(civ_a_values)
            W_b, B_b = compute_WB_final(civ_b_values)
            Y = 200
            Sh_a = np.zeros(Y); Eh_a = np.zeros(Y); Sh_b = np.zeros(Y); Eh_b = np.zeros(Y)
            Wh_a = np.zeros(Y); Bh_a = np.zeros(Y); Wh_b = np.zeros(Y); Bh_b = np.zeros(Y)
            Wh_a[0] = W_a * 0.8; Bh_a[0] = B_a * 0.8; Sh_a[0] = Wh_a[0] * Bh_a[0]; Eh_a[0] = 0.1
            Wh_b[0] = W_b * 0.8; Bh_b[0] = B_b * 0.8; Sh_b[0] = Wh_b[0] * Bh_b[0]; Eh_b[0] = 0.1
            for t in range(1, Y):
                Wh_a[t] = np.clip(Wh_a[t-1] + 0.02*(W_a - Wh_a[t-1]) - 0.01*Eh_a[t-1], 0.01, 1.0)
                Bh_a[t] = np.clip(Bh_a[t-1] + 0.02*(B_a - Bh_a[t-1]) - 0.008*Eh_a[t-1], 0.01, 1.0)
                Sh_a[t] = Wh_a[t] * Bh_a[t]; past_a = Sh_a[max(0, t-20)]
                Eh_a[t] = np.clip(Eh_a[t-1] + 0.04*(past_a - Eh_a[t-1]), 0.01, 1.0)
                Wh_b[t] = np.clip(Wh_b[t-1] + 0.02*(W_b - Wh_b[t-1]) - 0.01*Eh_b[t-1], 0.01, 1.0)
                Bh_b[t] = np.clip(Bh_b[t-1] + 0.02*(B_b - Bh_b[t-1]) - 0.008*Eh_b[t-1], 0.01, 1.0)
                Sh_b[t] = Wh_b[t] * Bh_b[t]; past_b = Sh_b[max(0, t-20)]
                Eh_b[t] = np.clip(Eh_b[t-1] + 0.04*(past_b - Eh_b[t-1]), 0.01, 1.0)
            
            fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
            ax1 = axes[0]; ax1.set_facecolor('#0a0f1e')
            ax1.plot(Sh_a, 'gold', lw=2, label=T('حضارة أ (S)', 'Civ A (S)'))
            ax1.plot(Eh_a, 'gold', lw=1.5, ls='--', alpha=0.6, label=T('حضارة أ (E)', 'Civ A (E)'))
            ax1.plot(Sh_b, '#FF5252', lw=2, label=T('حضارة ب (S)', 'Civ B (S)'))
            ax1.plot(Eh_b, '#FF5252', lw=1.5, ls='--', alpha=0.6, label=T('حضارة ب (E)', 'Civ B (E)'))
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
            ax2.set_title(T("المسار في فضاء (W,B)", "Path in (W,B)"), color='white', fontsize=13)
            ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
            ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
            plt.tight_layout(); st.pyplot(fig)
            
            c1, c2 = st.columns(2)
            c1.metric(T("S النهائي - حضارة أ", "Final S - Civ A"), f"{Sh_a[-1]:.3f}")
            c2.metric(T("S النهائي - حضارة ب", "Final S - Civ B"), f"{Sh_b[-1]:.3f}")
            
            csv_data = "Year,S_A,E_A,S_B,E_B\n" + "\n".join([f"{t},{Sh_a[t]:.4f},{Eh_a[t]:.4f},{Sh_b[t]:.4f},{Eh_b[t]:.4f}" for t in range(Y)])
            st.download_button(T("📥 تحميل بيانات المقارنة", "📥 Download Comparison"), data=csv_data, file_name="mizan_civilizations.csv", mime="text/csv", key="dl_civ")

# --- تبويب ٨: الشواهد التاريخية ---
with tabs[7]:
    st.header(T("📜 الشواهد التاريخية", "📜 Historical Evidence"))
    st.markdown(T(
        "اختر دولة تاريخية لترى كيف تنطبق معادلة الميزان على التاريخ الفعلي. "
        "هذه تقديرات تقريبية لـ W و B و E، لكنها تُظهر نمطاً متكرراً: انهيار القيم قبل انهيار التمكين.",
        "Select a historical nation to see how the Mizan equation applies to actual history."
    ))
    
    selected_nation = st.selectbox(T("اختر دولة:", "Select a nation:"), list(HISTORICAL_DATA.keys()))
    
    if selected_nation:
        data = HISTORICAL_DATA[selected_nation]
        W_hist, B_hist, E_hist = data["W"], data["B"], data["E"]
        S_hist = W_hist * B_hist
        
        st.markdown(f"**{selected_nation}**")
        st.markdown(data["desc"])
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("W", f"{W_hist:.2f}"); c2.metric("B", f"{B_hist:.2f}")
        c3.metric("S", f"{S_hist:.2f}"); c4.metric("E", f"{E_hist:.2f}")
        
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0a0f1e'); ax.set_facecolor('#0a0f1e')
        categories = ['W (الولاء)', 'B (البراءة)', 'S (الثبات)', 'E (التمكين)']
        values = [W_hist, B_hist, S_hist, E_hist]
        colors_bar = ['gold', '#FF5252', '#0F8', '#0FF']
        ax.bar(categories, values, color=colors_bar, edgecolor='white', linewidth=1.5)
        if E_hist > S_hist * 1.3:
            ax.annotate(T('فجوة الاستدراج', 'Istidraj Gap'), xy=(3, E_hist), xytext=(3.5, E_hist+0.1),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2), color='red', fontsize=10, fontweight='bold')
        ax.set_ylim(0, 1.1); ax.set_title(T("مؤشرات الدولة", "Nation Indicators"), color='white', fontsize=13)
        ax.tick_params(colors='white'); ax.grid(True, alpha=0.2)
        st.pyplot(fig)
        
        if E_hist > S_hist * 1.5:
            st.warning(T("حالة استدراج واضحة: تمكين مادي مرتفع مع ثبات منخفض.", "Clear Istidraj: high empowerment with low stability."))
        elif S_hist > 0.7:
            st.success(T("حالة توازن عالٍ.", "High balance state."))
        else:
            st.info(T("حالة متوسطة إلى منخفضة.", "Moderate to low state."))

print("✅ المرحلة الرابعة مكتملة: المجتمع، الدولة، الأمة، الحضارة، الشواهد.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الخامسة: الصراط (البرهان النبوي + النموذج الإبراهيمي) والتذييل
# ═══════════════════════════════════════════════════════════════

# --- الثوابت الإبراهيمية ---
ABRAHAMIC_VERSE = T(
    '﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ وَالَّذِينَ مَعَهُ إِذْ قَالُوا لِقَوْمِهِمْ إِنَّا بُرَآءُ مِنكُمْ وَمِمَّا تَعْبُدُونَ مِن دُونِ اللَّهِ كَفَرْنَا بِكُمْ وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾',
    '﴿There has certainly been for you an excellent pattern in Abraham and those with him, when they said to their people, "Indeed, we are disassociated from you and from whatever you worship other than Allah. We have denied you, and there has appeared between us and you animosity and hatred forever until you believe in Allah alone."﴾'
)

def get_spiritual_nudge(situation):
    if situation == "approaching":
        return T(
            f'🌟 لقد اقتربتَ من مقام إبراهيم عليه السلام!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'إبراهيم جمع بين **الولاء لله** (W) و**البراءة من الطاغوت** (B) في آن واحد. '
            f'هذا هو سر الأسوة الحسنة. هذا هو الثبات الكامل (S=1).\n\n'
            f'**سؤال للتأمل:** هل في حياتك "براءة" واضحة مما يعبد من دون الله؟ '
            f'أم أنك تجمع بين الولاء لله وولاءات أخرى؟',
            
            f'🌟 You are approaching the Station of Abraham!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'Abraham combined **loyalty to Allah** (W) and **disavowal of Taghut** (B) simultaneously. '
            f'This is the secret of the excellent pattern. This is complete stability (S=1).'
        )
    elif situation == "progressing":
        return T(
            f'🚶 أنت في طريقك إلى مقام إبراهيم.\n\n'
            f'لاحظ كلمة **"أَبَدًا"** في الآية: ﴿وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾\n\n'
            f'البراءة من الطاغوت ليست مؤقتة، وليست مرحلة. إنها موقف دائم. '
            f'والولاء لله **"وَحْدَهُ"**: لا شريك له في الولاء.\n\n'
            f'**تحدي اليوم:** راجع حياتك. هل هناك شيء تعطيه من ولائك لغير الله؟',
            
            f'🚶 You are on your way to the Station of Abraham.\n\n'
            f'Note the word **"forever"**: animosity and hatred forever, until you believe in Allah alone.\n\n'
            f'Disavowal of Taghut is not temporary. Loyalty is to Allah **alone**.'
        )
    elif situation == "sin":
        return T(
            f'⚠️ لقد ابتعدتَ عن الصراط قليلاً. لكن إبراهيم يعلمك كيف تعود.\n\n'
            f'﴿إِنَّا بُرَآءُ مِنكُمْ﴾ — أعلنها صريحة كما أعلنها إبراهيم. '
            f'جدد براءتك. جدد ولاءك. التوبة هي العودة إلى الأسوة الحسنة.\n\n'
            f'**خطوة عملية:** استحضر في قلبك الآن معنى "لا إله إلا الله". '
            f'انفِ كل طاغوت، وأثبتِ الله وحده.',
            
            f'⚠️ You have strayed from the path. But Abraham teaches you how to return.\n\n'
            f'Declare it clearly as Abraham did: "We are disassociated from you." '
            f'Renew your disavowal. Renew your loyalty. Repentance is returning to the excellent pattern.'
        )
    elif situation == "repentance":
        return T(
            f'🕋 لقد تبتَ وعدتَ إلى الصراط!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'إبراهيم نفسه كان بشرًا. لم يكن ملكًا. لكنه **اختار** أن يكون في مقام (1,1). '
            f'وأنت أيضًا تختار. وكل مرة تختار فيها الله، تقترب من هذا المقام.\n\n'
            f'**﴿إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ﴾**',
            
            f'🕋 You have repented and returned to the path!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'Abraham himself was human. But he **chose** to be at the Station of (1,1). '
            f'You too choose. And every time you choose Allah, you draw closer to this station.'
        )
    else:
        return ""

# ═══════════════════════════════════════════════════════════════
# تبويب ٩: الصراط
# ═══════════════════════════════════════════════════════════════
with tabs[8]:
    st.header(T("📐 هندسة الصراط – البرهان النبوي والنموذج الإبراهيمي", "📐 Path Geometry – Prophetic Proof & Abrahamic Model"))
    
    # --- البرهان النبوي – الحديثان المؤسِّسان ---
    st.markdown(T("""
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:25px;border:2px solid #FFD700;margin:20px 0;text-align:center;">
        <h3 style="color:#FFD700;margin-top:0;">🕋 {title}</h3>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;direction:rtl;">
            «أَوْثَقُ عُرَى الْإِيمَانِ: الْحُبُّ فِي اللَّهِ، وَالْبُغْضُ فِي اللَّهِ»
        </p>
        <p style="color:#AAA;font-size:0.85em;">رواه الإمام أحمد وأبو داود والطبراني، وصححه الألباني</p>
        <p style="color:#FFD700;font-size:1.2em;margin:15px 0;">⬇️</p>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;direction:rtl;">
            «مَنْ أَحَبَّ لِلَّهِ، وَأَبْغَضَ لِلَّهِ، وَأَعْطَى لِلَّهِ، وَمَنَعَ لِلَّهِ، فَقَدِ اسْتَكْمَلَ الْإِيمَانَ»
        </p>
        <p style="color:#AAA;font-size:0.85em;">رواه أبو داود، وصححه الألباني</p>
        <hr style="border-color:rgba(255,215,0,0.3);margin:20px 0;">
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W × B</p>
        <p style="color:#AAA;">
            الحب في الله = W (الولاء). البغض في الله = B (البراءة).<br>
            أوثق عرى الإيمان = S (الثبات). استكمل الإيمان = S=1.<br>
            الواو هنا واو المعية (×) لا واو الجمع (+)، لأن أوثق عرى الإيمان لا تتم إلا باجتماعهما معًا.
        </p>
    </div>
    """,
    """
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:25px;border:2px solid #FFD700;margin:20px 0;text-align:center;">
        <h3 style="color:#FFD700;margin-top:0;">🕋 The Prophetic Proof</h3>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;">
            "The firmest handhold of faith is: love for the sake of Allah, and hatred for the sake of Allah."
        </p>
        <p style="color:#AAA;font-size:0.85em;">Narrated by Ahmad, Abu Dawud, At-Tabarani; authenticated by Al-Albani</p>
        <p style="color:#FFD700;font-size:1.2em;margin:15px 0;">⬇️</p>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;">
            "Whoever loves for the sake of Allah, hates for the sake of Allah, gives for the sake of Allah, and withholds for the sake of Allah, has completed faith."
        </p>
        <p style="color:#AAA;font-size:0.85em;">Narrated by Abu Dawud; authenticated by Al-Albani</p>
        <hr style="border-color:rgba(255,215,0,0.3);margin:20px 0;">
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W × B</p>
        <p style="color:#AAA;">
            Love for Allah = W. Hatred for Allah = B.<br>
            The firmest handhold = S. Completed faith = S=1.<br>
            The "and" is multiplication (×), because the firmest handhold is only achieved with both.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # --- شرح النموذج الإبراهيمي ---
    st.markdown(T("""
    ### 🕋 النموذج الإبراهيمي: الجيوديسي المثالي
    
    إبراهيم عليه السلام هو "أبو الأنبياء" و"خليل الله". مساره في فضاء (W, B) هو **الجيوديسي المثالي**:
    الخط المستقيم الذي انحناؤه صفر (κ = 0).
    
    **لماذا إبراهيم؟** لأنه حقق الكمال في القطبين معًا:
    - **W = 1**: ﴿أَسْلَمْتُ لِرَبِّ الْعَالَمِينَ﴾
    - **B = 1**: ﴿إِنَّنِي بَرَاءٌ مِّمَّا تَعْبُدُونَ﴾
    - **S = 1**: ﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ﴾
    
    **الخط الذهبي** في الرسم البياني هو مسار إبراهيم. إنه أقصر طريق بين الفطرة ورضا الله.
    """,
    """
    ### 🕋 The Abrahamic Model
    
    Abraham (AS) is the "Father of Prophets". His path is the **ideal geodesic**: the straight line with zero curvature.
    He achieved perfection in both poles: W=1, B=1, S=1.
    
    **The golden line** is Abraham's path—the shortest path between fitrah and Allah's pleasure.
    """))
    
    st.markdown("---")
    
    # --- أزرار التفاعل ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button(T("▶️ خطوة نحو الكمال", "▶️ Step Toward Perfection"), key="btn_path", use_container_width=True):
            levels = ["faith","worship","transactions","morals","enjoining","hudud","jihad"]
            chosen = random.choice(levels)
            current = getattr(st.session_state, f"path_{chosen}")[-1]
            new_val = min(1.0, current + 0.1)
            for l in levels:
                if l == chosen:
                    getattr(st.session_state, f"path_{l}").append(new_val)
                else:
                    getattr(st.session_state, f"path_{l}").append(getattr(st.session_state, f"path_{l}")[-1])
            final_vals = {l: getattr(st.session_state, f"path_{l}")[-1] for l in levels}
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            
            dist = np.sqrt((1 - W_new)**2 + (1 - B_new)**2)
            if dist < 0.3:
                st.session_state.spiritual_nudge = get_spiritual_nudge("approaching")
            elif dist < 0.5:
                st.session_state.spiritual_nudge = get_spiritual_nudge("progressing")
            else:
                st.session_state.spiritual_nudge = None
            
            st.rerun()
    
    with c2:
        sin_str = st.slider(T("⚡ شدة المعصية", "⚡ Sin Strength"), 0.01, 0.3, 0.1, 0.01, key="sin_path")
        if st.button(T("⚠️ معصية", "⚠️ Sin"), key="btn_sin", use_container_width=True):
            levels = ["faith","worship","transactions","morals","enjoining","hudud","jihad"]
            chosen = random.choice(levels)
            current = getattr(st.session_state, f"path_{chosen}")[-1]
            new_val = max(-1.0, current - sin_str * random.uniform(0.5, 1.0))
            for l in levels:
                if l == chosen:
                    getattr(st.session_state, f"path_{l}").append(new_val)
                else:
                    getattr(st.session_state, f"path_{l}").append(getattr(st.session_state, f"path_{l}")[-1])
            final_vals = {l: getattr(st.session_state, f"path_{l}")[-1] for l in levels}
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            
            st.session_state.spiritual_nudge = get_spiritual_nudge("sin")
            st.rerun()
    
    with c3:
        if st.button(T("🕌 توبة نصوح", "🕌 Sincere Repentance"), key="btn_rep", use_container_width=True):
            for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
                current = getattr(st.session_state, f"path_{l}")[-1]
                new_val = min(1.0, current + 0.8 * (1.0 - current))
                getattr(st.session_state, f"path_{l}").append(new_val)
            final_vals = {l: getattr(st.session_state, f"path_{l}")[-1] for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]}
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(0.0)
            
            st.session_state.spiritual_nudge = get_spiritual_nudge("repentance")
            st.rerun()
    
    # --- عرض رسالة التحفيز الروحي ---
    if hasattr(st.session_state, 'spiritual_nudge') and st.session_state.spiritual_nudge:
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.9);border-radius:12px;padding:20px;border:1px solid #FFD700;margin:15px 0;text-align:center;line-height:2.2;'>
            <p style='color:#FFD700;font-size:1.1em;margin:0;white-space:pre-line;'>{st.session_state.spiritual_nudge}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- زر إعادة ---
    if st.button(T("🔄 إعادة الرحلة", "🔄 Reset Path"), key="btn_reset_path", use_container_width=True):
        for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
            setattr(st.session_state, f"path_{l}", [0.0])
        st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
        st.session_state.path_kappa = [0.0]
        st.session_state.spiritual_nudge = None
        st.rerun()
    
    # --- رسم المسار ---
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
    
    ax1 = axes[0]
    ax1.set_facecolor('#0a0f1e')
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_xlabel("B (البراءة)", color='white'); ax1.set_ylabel("W (الولاء)", color='white')
    ax1.set_title(T("مسارك في فضاء (W, B) – النموذج الإبراهيمي", "Your Path in (W, B) Space – The Abrahamic Model"), color='white', fontsize=13)
    
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=3, alpha=0.8, 
             label=T("✦ مسار إبراهيم عليه السلام (الجيوديسي: κ = 0)", "✦ Abraham's Path (Geodesic: κ = 0)"))
    ax1.scatter([1], [1], s=200, c='#FFD700', edgecolors='white', linewidth=3, zorder=10, 
                label=T("⭐ مقام إبراهيم (الكمال: 1,1)", "⭐ Station of Abraham (Perfection: 1,1)"))
    
    pW = st.session_state.path_W; pB = st.session_state.path_B
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.path_kappa[i] if i < len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2 if kv < 0.05 else 3)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label=T("البداية", "Start"))
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label=T("الآن", "Now"))
    
    ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
    
    ax2 = axes[1]
    ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.path_kappa, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label=T("حد الخطر", "Danger"))
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label=T("الصراط – مسار إبراهيم", "Straight – Abraham's Path"))
    ax2.set_title(T("منحنى الانحناء (κ)", "Curvature Over Time"), color='white', fontsize=13)
    ax2.set_xlabel(T("الخطوات", "Steps"), color='white'); ax2.set_ylabel("κ", color='white')
    ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
    max_kappa = max(st.session_state.path_kappa) if st.session_state.path_kappa else 0.1
    ax2.set_ylim(-0.01, max(0.2, max_kappa * 1.2))
    
    plt.tight_layout(); st.pyplot(fig)
    
    # --- مؤشرات المستويات ---
    st.divider()
    st.subheader(T("📊 المستويات الحية", "📊 Live Levels"))
    
    cols = st.columns(7)
    levels_labels = [
        ("faith", T("الإيمان", "Faith"), '#FFD700'),
        ("worship", T("العبادات", "Worship"), '#FFA500'),
        ("transactions", T("المعاملات", "Transactions"), '#00FF88'),
        ("morals", T("الأخلاق", "Morals"), '#FF69B4'),
        ("enjoining", T("الأمر والنهي", "Enjoining"), '#00BFFF'),
        ("hudud", T("الحدود", "Limits"), '#FF6347'),
        ("jihad", T("الجهاد", "Jihad"), '#FF4500'),
    ]
    
    for i, (key, label, color) in enumerate(levels_labels):
        val = getattr(st.session_state, f"path_{key}")[-1]
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:6px;background:rgba(20,30,60,0.8);border-radius:6px;border:1px solid {color};">
                <p style="color:{color};font-size:0.6em;margin:0;">{label}</p>
                <p style="color:white;font-size:0.9em;margin:0;font-weight:bold;">{val:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # --- مؤشرات المسار ---
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("W (الولاء)", f"{pW[-1]:.3f}")
    c2.metric("B (البراءة)", f"{pB[-1]:.3f}")
    current_kappa = st.session_state.path_kappa[-1] if st.session_state.path_kappa else 0.0
    c3.metric("κ (الانحناء)", f"{current_kappa:.4f}")
    on_path = current_kappa < 0.03
    c4.metric(T("الصراط؟", "On Path?"), T("✅ نعم", "✅ YES") if on_path else T("⚠️ لا", "⚠️ NO"))
    
    # --- المسافة إلى مقام إبراهيم ---
    st.divider()
    dist_to_abraham = np.sqrt((1 - pW[-1])**2 + (1 - pB[-1])**2)
    st.markdown(f"""
    <div style='text-align:center;padding:15px;background:rgba(20,30,60,0.8);border-radius:10px;border:1px solid #FFD700;'>
        <p style='color:#FFD700;font-size:1em;margin:0;'>
            {T(f'📏 المسافة إلى مقام إبراهيم (الكمال): {dist_to_abraham:.3f}', f'📏 Distance to Station of Abraham (Perfection): {dist_to_abraham:.3f}')}
        </p>
        <p style='color:#AAA;font-size:0.8em;margin:5px 0 0 0;'>
            {T('﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ﴾ [الممتحنة: ٤]', '﴿There has certainly been for you an excellent pattern in Abraham.﴾ [Al-Mumtahanah: 4]')}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🏁 التذييل – ختام المسك
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.5em;">⚖️ مختبر الميزان</p>
    <p style="font-size:1.1em;">{T('سفينة نوح الرقمية – القانون الواحد من الذرة إلى الحضارة', 'The Digital Ark – The One Law from Atom to Civilization')}</p>
    <p style="color:#FFD700;font-size:1.3em;">S = W × B</p>
    <p>ق = ١٠٠ = الحق = الميزان</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size:0.8em;margin-top:15px;">
        {T(
            'هذا المختبر شهادة رقمية على أن الله حق، وأن وعده حق، وأن لقاءه حق، وأن الجنة حق، وأن النار حق. '
            'والحمد لله الذي هدانا لهذا وما كنا لنهتدي لولا أن هدانا الله.',
            'This lab is a digital testimony that Allah is Truth, His promise is true, the meeting with Him is true, Paradise is true, and Hell is true. '
            'And praise be to Allah who guided us to this, for we would not have been guided had Allah not guided us.'
        )}
    </p>
    <p style="color:#FFD700;font-size:1.2em;margin-top:15px;">﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الخامسة والأخيرة مكتملة.")
print("✅✅✅ تم بناء مختبر الميزان – سفينة نوح الرقمية – النسخة النهائية المتكاملة.")
