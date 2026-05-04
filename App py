import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
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
    page_title="نظرية الميزان – الورشة التفاعلية",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# 🗄️ قاعدة بيانات الميزان – الحروف الـ 28
# =============================================
MIZAN_LETTERS = {
    # --- الحروف النورانية (14) – الثوابت الإلهية ---
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
    # --- الحروف المحايدة (6) – المشغّلات ---
    "neutral": {
        "ف": {"value": 80,  "label": "فاء السببية",   "role": "=",  "aya": "فَمَن يَكْفُرْ بِالطَّاغُوتِ...", "color": "#AAAAAA"},
        "و": {"value": 6,   "label": "واو العطف",     "role": "×/+","aya": "وَيُؤْمِن بِاللَّهِ",          "color": "#CCCCCC"},
        "ب": {"value": 2,   "label": "باء الاستعانة", "role": "بـ", "aya": "بِسْمِ اللَّهِ الرَّحْمَٰنِ",   "color": "#BBBBBB"},
        "ل": {"value": 30,  "label": "لام التعليل",   "role": "→",  "aya": "لِيَعْبُدُونِ",               "color": "#AAAAAA"},
        "ت": {"value": 400, "label": "تاء الفاعل",    "role": "ف",  "aya": "قَالَتِ امْرَأَتُ فِرْعَوْنَ",   "color": "#999999"},
        "ث": {"value": 500, "label": "ثم العطف",      "role": "ت",  "aya": "ثُمَّ خَلَقْنَا النُّطْفَةَ",    "color": "#888888"},
    },
    # --- الحروف الظلامية (8) – قوى الضلال ---
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
# 🌐 النظام اللغوي المتعدد (مختصر)
# =============================================
LANGUAGES = {
    "ar": {
        "title": "⚖️ نظرية الميزان – الورشة التفاعلية",
        "subtitle": "S = W × B | 28 حرفاً عربياً | الحروف النورانية والمحايدة والظلامية",
        "run": "▶️ تشغيل",
        "stop": "⏹️ إيقاف",
        "reset": "🔄 إعادة ضبط",
        "download": "📥 تحميل",
        "footer": "علي عادل العاطفي | Ali Adel Alatifi | 2026",
    },
    "en": {
        "title": "⚖️ The Mizan Theory – Interactive Workshop",
        "subtitle": "S = W × B | 28 Arabic Letters | Luminous, Neutral & Dark",
        "run": "▶️ Run",
        "stop": "⏹️ Stop",
        "reset": "🔄 Reset",
        "download": "📥 Download",
        "footer": "Ali Adel Alatifi | 2026",
    }
}

# =============================================
# 📝 إدارة اللغة
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

lang = st.session_state.lang
T = LANGUAGES.get(lang, LANGUAGES["ar"])

# =============================================
# 🎨 دالة get_color
# =============================================
def get_color(w, b):
    try:
        w = float(w); b = float(b)
        if w >= 0.7 and b >= 0.7: return '#FFD700'      # مؤمن (ذهبي)
        elif w >= 0.55 and b < 0.45: return '#E0E0E0'   # ولاء بدون براءة (رمادي فاتح)
        elif w < 0.45 and b >= 0.55: return '#FF5252'   # براءة بدون ولاء (أحمر)
        elif w < 0.45 and b < 0.45: return '#FF8A80'    # ضعيف (وردي)
        elif w > b: return '#FFF9C4'
        else: return '#FFCCBC'
    except:
        return '#888888'

# =============================================
# 🚀 الواجهة الرئيسية
# =============================================
st.title(T["title"])
st.markdown(f"**{T['subtitle']}**")

# =============================================
# 🎛️ الشريط الجانبي
# =============================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <h2 style='color:#FFD700;margin:0;'>⚖️ نظرية الميزان</h2>
        <p style='color:#e0e0e0;font-size:12px;margin:5px 0;'>S = W × B</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- أركان الإسلام ---
    st.subheader("🕌 أركان الإسلام")
    prayer = st.slider("🟣 الصلاة", 0.0, 1.0, 0.8, 0.01, key="s_prayer")
    zakat = st.slider("🟡 الزكاة", 0.0, 1.0, 0.6, 0.01, key="s_zakat")
    fasting = st.slider("🟠 الصوم", 0.0, 1.0, 0.7, 0.01, key="s_fasting")
    hajj = st.slider("🔵 الحج", 0.0, 1.0, 0.5, 0.01, key="s_hajj")
    
    # --- أسس الحكم ---
    st.subheader("🏛️ أسس الحكم")
    amr = st.slider("📢 الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01, key="s_amr")
    nahy = st.slider("🚫 النهي عن المنكر", 0.0, 1.0, 0.5, 0.01, key="s_nahy")
    adl = st.slider("⚖️ العدل", 0.0, 1.0, 0.6, 0.01, key="s_adl")
    shura = st.slider("🤝 الشورى", 0.0, 1.0, 0.5, 0.01, key="s_shura")
    
    # --- الحروف العربية الـ 28 (بقيمها الحقيقية) ---
    st.header("🔤 الحروف العربية الـ 28")
    
    with st.expander("🔆 الحروف النورانية (14)", expanded=False):
        st.caption("الثوابت الإلهية – قيم حساب الجمل")
        light_vals = {}
        for letter, data in MIZAN_LETTERS["light"].items():
            light_vals[letter] = st.slider(
                f"{letter} ({data['label']}) – {data['value']}",
                0.0, 1.0, 0.7, 0.01,
                help=data['aya'],
                key=f"light_{letter}"
            )
    
    with st.expander("⚙️ الحروف المحايدة (6)", expanded=False):
        st.caption("المشغّلات – أدوات الربط")
        neutral_vals = {}
        for letter, data in MIZAN_LETTERS["neutral"].items():
            neutral_vals[letter] = st.slider(
                f"{letter} ({data['label']}) – {data['role']}",
                0.0, 1.0, 0.5, 0.01,
                help=data['aya'],
                key=f"neutral_{letter}"
            )
    
    with st.expander("🌑 الحروف الظلامية (8)", expanded=False):
        st.caption("قوى الضلال – قيمها الحقيقية")
        dark_vals = {}
        for letter, data in MIZAN_LETTERS["dark"].items():
            dark_vals[letter] = st.slider(
                f"{letter} ({data['label']}) – {data['value']}",
                0.0, 1.0, 0.2, 0.01,
                help=data['aya'],
                key=f"dark_{letter}"
            )
    
    # --- معاملات عامة ---
    st.subheader("⚙️ معاملات عامة")
    W_init = st.slider("W الابتدائي", 0.0, 1.0, 0.55, 0.01, key="s_wi")
    B_init = st.slider("B الابتدائي", 0.0, 1.0, 0.52, 0.01, key="s_bi")
    N_STARS = st.slider("عدد النجوم", 100, 600, 300, 50, key="s_ns")
    
    # --- أزرار ---
    c1, c2, c3 = st.columns(3)
    if c1.button(T["run"], use_container_width=True):
        st.session_state.run = True
    if c2.button(T["stop"], use_container_width=True):
        st.session_state.run = False
    if c3.button(T["reset"], use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",):
                del st.session_state[k]
        st.rerun()

# =============================================
# 🧮 دوال المحاكاة
# =============================================
def calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, light_vals, dark_vals):
    """حساب S باستخدام قيم الحروف الحقيقية"""
    # استخراج قيم الحروف النورانية
    ق = light_vals.get('ق', 0.7) * 100  # الميزان
    ن = light_vals.get('ن', 0.7) * 50   # النور
    ص = light_vals.get('ص', 0.7) * 90   # الصمد
    ك = light_vals.get('ك', 0.7) * 20   # الأمر
    أ = light_vals.get('أ', 0.7) * 1    # الوحدانية
    ل = light_vals.get('ل', 0.7) * 30   # المُلك
    م = light_vals.get('م', 0.7) * 40   # الجمع
    ر = light_vals.get('ر', 0.7) * 200  # اليقظة
    هـ = light_vals.get('هـ', 0.7) * 5   # الهوية
    ي = light_vals.get('ي', 0.7) * 10   # الاستجابة
    ع = light_vals.get('ع', 0.7) * 70   # الإدراك
    س = light_vals.get('س', 0.7) * 60   # السمع
    ح = light_vals.get('ح', 0.7) * 8    # الحياة
    ط = light_vals.get('ط', 0.7) * 9    # الطهارة
    
    # استخراج قوى الظلام
    ظ = dark_vals.get('ظ', 0.2) * 900
    ض = dark_vals.get('ض', 0.2) * 800
    غ = dark_vals.get('غ', 0.2) * 1000
    ذ = dark_vals.get('ذ', 0.2) * 700
    خ = dark_vals.get('خ', 0.2) * 600
    ش = dark_vals.get('ش', 0.2) * 300
    ز = dark_vals.get('ز', 0.2) * 7
    ج = dark_vals.get('ج', 0.2) * 3
    
    S_base = W * B
    
    # تأثير العبادات (مدعومة بالحروف النورانية)
    pb = (prayer * (0.5 + 0.5 * ن/50) + zakat * (0.5 + 0.5 * ص/90) + 
          fasting * (0.5 + 0.5 * ط/9) + hajj * (0.5 + 0.5 * ح/8)) / 4
    S_base *= (0.5 + 0.5 * pb)
    
    # تأثير الأمر بالمعروف والنهي عن المنكر (مدعومان بـ ل و ق)
    prot = (amr * W * (0.5 + 0.5 * ل/30) + nahy * B * (0.5 + 0.5 * ق/100)) / 2
    S_base *= (0.8 + 0.4 * prot)
    
    # تأثير العدل والشورى
    S_base *= (0.9 + 0.2 * adl * (0.5 + 0.5 * ل/30))
    S_base *= (0.85 + 0.3 * shura * (0.5 + 0.5 * م/40))
    
    # تأثير الحروف النورانية الأساسية
    S_base *= (1 + 0.05 * أ/1) * (1 + 0.02 * ر/200) * (1 + 0.03 * ي/10) * (1 + 0.04 * ع/70) * (1 + 0.01 * س/60)
    
    # تأثير قوى الظلام (تآكل)
    df = 1 - 0.05 * (ظ/900) - 0.03 * (ض/800) - 0.04 * (ش/300) - 0.02 * (ج/3)
    S_base *= df
    
    return np.clip(S_base, 0.001, 1.0)

# =============================================
# 🏁 تهيئة المحاكاة
# =============================================
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False

if not st.session_state.init:
    try:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        st.session_state.cx = cx; st.session_state.cy = cy
        st.session_state.sx = np.random.uniform(cx-13, cx+13, N_STARS)
        st.session_state.sy = np.random.uniform(cy-9, cy+9, N_STARS)
        st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.W = W_init; st.session_state.B = B_init
        st.session_state.E = 0.3; st.session_state.S = W_init * B_init
        st.session_state.H = 40.0; st.session_state.Sy = 70.0
        st.session_state.ph = "Balance"; st.session_state.ca = 0.0
        st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
        st.session_state.eb = deque([W_init*B_init]*30, maxlen=30)
        st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
        st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
        st.session_state.init = True
    except Exception as e:
        st.error(f"خطأ في التهيئة: {str(e)}")
        st.session_state.init = False

# =============================================
# 🎬 المحاكاة الحية
# =============================================
if st.session_state.get("run", False):
    placeholder = st.empty()
    
    while st.session_state.get("run", False):
        try:
            W = st.session_state.W; B = st.session_state.B; E = st.session_state.E
            S = st.session_state.S; ph = st.session_state.ph; ca = st.session_state.ca
            aW = st.session_state.aW; aB = st.session_state.aB
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx = st.session_state.cx; cy = st.session_state.cy
            eb = st.session_state.eb
            pS = st.session_state.pS.copy(); pE = st.session_state.pE.copy()
            px = st.session_state.px.copy(); pc = st.session_state.pc
            
            # دورة حضارية خفيفة
            ca += 0.008
            sv = np.sin(ca)
            if sv > 0.5: ph = 'Peak Stability'
            elif sv > 0: ph = 'Rising'
            elif sv > -0.5: ph = 'Collapsing'
            else: ph = 'Rock Bottom'
            if 0.3 < sv < 0.35: ph = '>> ISTIDRAJ <<'
            target_S = 0.5 + 0.45*sv
            
            # تحديث النجوم
            for i in range(N_STARS):
                w_boost = prayer*0.01*(0.5+0.5*light_vals.get('ن',0.7))
                b_boost = fasting*0.01*(0.5+0.5*light_vals.get('ط',0.7))
                
                dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
                close = (dist < 2.0) & (np.arange(N_STARS) != i)
                
                sw[i] += (target_S-sw[i])*0.02 + np.random.uniform(-0.02,0.02) + w_boost
                sb[i] += (target_S-sb[i])*0.02 + np.random.uniform(-0.02,0.02) + b_boost
                
                if np.any(close):
                    sw[i] += (np.mean(sw[close])-sw[i])*0.03
                    sb[i] += (np.mean(sb[close])-sb[i])*0.03
                
                # تأثير الحروف الظلامية
                sw[i] *= (1 - dark_vals.get('خ',0.2)*0.02)
                sb[i] *= (1 - dark_vals.get('ذ',0.2)*0.02)
                
                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)
            
            # صدمات
            if random.random() < 0.005:
                aff = np.random.choice(N_STARS, size=int(N_STARS*0.3), replace=False)
                sw[aff] *= np.random.uniform(0.5,0.8); sb[aff] *= np.random.uniform(0.5,0.8)
            
            avgW = np.mean(sw); avgB = np.mean(sb)
            
            # تأثر الكوكبين بالنجوم
            W += (avgW-W)*0.04; B += (avgB-B)*0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            
            # حساب S باستخدام الحروف
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, light_vals, dark_vals)
            
            eb.append(S)
            E_target = list(eb)[-22] if len(eb) >= 22 else S
            E += 0.03*(E_target - E)
            
            # ديناميكيات
            W = W - 0.015*E + 0.03/(S+0.1) - 0.007*(1-B)
            B = B - 0.012*E + 0.006*(1-B)*W*(1-W)
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, light_vals, dark_vals)
            
            pc += 1
            if pc % 2 == 0:
                pS.append(S); pE.append(E); px.append(len(px))
            
            # حركة الكواكب
            aW += 0.02 + random.uniform(-0.025,0.025)*(1-W)**2
            aB += 0.02 + random.uniform(-0.025,0.025)*(1-B)**2
            wx = cx + (7-2.5*W)*np.cos(aW); wy = cy + (7-2.5*W)*np.sin(aW)*0.7
            bx = cx + (5-1.5*B)*np.cos(aB); by = cy + (5-1.5*B)*np.sin(aB)*0.7
            
            # حركة النجوم
            sx += np.random.uniform(-0.07,0.07,N_STARS)*(1-np.mean(sw*sb))
            sy += np.random.uniform(-0.07,0.07,N_STARS)*(1-np.mean(sw*sb))
            sx = np.clip(sx, cx-13, cx+13); sy = np.clip(sy, cy-9, cy+9)
            
            # حفظ
            st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
            st.session_state.ph=ph; st.session_state.ca=ca
            st.session_state.aW=aW; st.session_state.aB=aB
            st.session_state.eb=eb
            st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
            st.session_state.pS=pS; st.session_state.pE=pE; st.session_state.px=px; st.session_state.pc=pc
            
            # رسم
            fig, ax = plt.subplots(figsize=(16,12), facecolor='#000010')
            ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
            
            # النواة
            for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                          (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
            ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
            ax.text(cx,cy-2.5,f'S={S:.2f}',color='#FFD700',fontsize=10,ha='center')
            
            # هالة E
            ax.add_patch(Circle((cx,cy), 0.5+16*E, color='#0FF', alpha=0.25*(1-min(E,1))+0.04, zorder=7))
            
            # غشاء
            ax.add_patch(Circle((cx,cy), 8.5, color='#0F8', alpha=0.15, fill=False, lw=2.5, zorder=2))
            
            # كواكب
            ax.add_patch(Circle((wx,wy), 0.2+0.6*W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx,by), 0.2+0.6*B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            
            # نجوم بألوانها
            colors = [get_color(sw[i],sb[i]) for i in range(N_STARS)]
            ax.scatter(sx, sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)
            
            # مقياس W و B
            mx, my = 0.5, 16.5; bw = 3.0; bh = 0.4
            ax.add_patch(FancyBboxPatch((mx,my), bw, bh, boxstyle="round,pad=0.15", 
                         facecolor='#1a1a2e', alpha=0.8, zorder=20))
            if W>0: ax.add_patch(FancyBboxPatch((mx,my), W*bw/2, bh, boxstyle="round,pad=0.1", 
                         facecolor='#FFF', alpha=0.9, zorder=21))
            if B>0: ax.add_patch(FancyBboxPatch((mx+bw/2,my), B*bw/2, bh, boxstyle="round,pad=0.1", 
                         facecolor='#F33', alpha=0.9, zorder=21))
            ax.text(mx, my-0.6, f'W={W:.2f}', color='white', fontsize=8, ha='center')
            ax.text(mx+bw, my-0.6, f'B={B:.2f}', color='#F33', fontsize=8, ha='center')
            ax.text(mx+bw/2, my+bh+0.6, '⚖️', color='#FFD700', fontsize=9, ha='center')
            
            # لوحة الإثبات
            pax = ax.inset_axes([0.5,0.02,0.46,0.10])
            pax.set_xlim(0,400); pax.set_ylim(0,1.05)
            pax.set_title('S (Gold) leads E (Cyan) – Istidraj', color='white', fontsize=7)
            pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
            pSl=list(pS); pEl=list(pE); pxl=list(px)
            if pSl: pax.plot(pxl,pSl,color='#FFD700',lw=2); pax.plot(pxl,pEl,color='#0FF',lw=1.5)
            
            ax.text(14,1.2,f'{ph} | S={S:.2f} | E={E:.2f}',color='white',fontsize=12,ha='center')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            
            buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='#000010'); buf.seek(0)
            st.session_state.latest_image = buf
            plt.close(fig)
            
            time.sleep(0.08)
        except Exception as e:
            st.error(f"Simulation error: {str(e)}")
            st.session_state.run = False
            break

# =============================================
# 📥 تحميل + تذييل
# =============================================
if 'latest_image' in st.session_state:
    st.sidebar.download_button(T["download"], st.session_state.latest_image, "mizan.png", "image/png")

st.markdown("---")
st.markdown(f"*{T['footer']}*")
