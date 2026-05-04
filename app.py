# =============================================
# ⚖️ AL-DEEN AL-QAYYIM – THE COSMIC BALANCE LAW
# S = W × B | W = الولاء (Allegiance) | B = البراءة (Disavowal)
# =============================================
# Book: "The Mizan Theory – from cosmic duality to S = W × B"
# Author: Ali Adel Alatifi | © 2026 | All rights reserved.
# Licensed under GNU GPL v3.0
# =============================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# 🌐 DATA: Multilingual texts
# =============================================
TEXT = {
    "ar": {
        "page_title": "الدين القيم – قانون التوازن الكوني",
        "main_heading": "⚖️ الدِّينُ الْقَيِّم ⚖️",
        "sub_heading": "قَانُونُ التَّوَازُنِ الْكَوْنِيّ",
        "formula_caption": "S = W × B | نظرية الميزان",
        "author": "© 2026 علي عادل العاطفي | Ali Adel Alatifi",
        "welcome_title": "📜 رسالة الترحيب",
        "theory_tab": "📖 النظرية",
        "guide_tab": "❓ كيف تقرأ المشهد",
        "theory_content": """
        > "هل يوجد قانون واحد يحكم الذرة والحضارة؟"
        **S = W × B**
        **الدين القيم** = قانون السببية الكوني.
        إنه "الميزان" الذي قامت به السماوات والأرض.
        """,
        "guide_content": """
        **الألوان:**
        - ذهبي = توازن
        - أبيض = ولاء
        - أحمر = براءة
        - وردي = خطر
        **العناصر:**
        - الدائرة الذهبية = الاستقرار S
        - القرص السماوي = التمكين E
        - لوحة الإثبات = S يقود E
        """,
        "book_title": "📖 كتاب الميزان",
        "book_intro": "نظرية الميزان – من الثنائية الكونية إلى معادلة الوجود S = W × B",
        "control_panel": "🎛️ لوحة التحكم",
        "run_btn": "▶️ تشغيل",
        "stop_btn": "⏹️ إيقاف",
        "reset_btn": "🔄 إعادة ضبط",
        "cache_btn": "🧹 مسح المؤقت",
        "pillars": "🕌 أركان الإسلام",
        "governance": "🏛️ أسس الحكم",
        "reform": "🛡️ آليات الإصلاح",
        "corruption": "💀 آليات الإفساد",
        "diseases": "⚠️ الأمراض الأخلاقية",
        "settings": "⚙️ إعدادات المحاكاة",
        "sliders": {
            "prayer": "الصلاة", "zakat": "الزكاة", "fasting": "الصوم", "hajj": "الحج",
            "amr": "الأمر بالمعروف", "nahy": "النهي عن المنكر", "adl": "العدل", "shura": "الشورى",
            "tb": "التعاون على البر", "th": "التواصي بالحق", "tt": "التعاون على التقوى", "ts": "التواصي بالصبر",
            "nm": "النهي عن المعروف (إفساد)", "amr_e": "الأمر بالمنكر (إفساد)", "ti": "التعاون على الإثم",
            "tu": "التعاون على العدوان", "tbat": "التواصي بالباطل", "as": "عدم الصبر",
            "riba": "الربا", "ghish": "الغش", "kadhib": "الكذب",
            "cycle": "سرعة الدورة", "delay": "تأخير التمكين", "stars": "عدد النجوم"
        },
        "download_btn": "📥 تحميل صورة المشهد",
        "footer": "© 2026 علي عادل العاطفي | Al-Deen Al-Qayyim – قانون التوازن الكوني"
    },
    "en": {
        "page_title": "Al-Deen Al-Qayyim – The Cosmic Balance Law",
        "main_heading": "⚖️ Al-Deen Al-Qayyim ⚖️",
        "sub_heading": "The Cosmic Balance Law",
        "formula_caption": "S = W × B | The Mizan Theory",
        "author": "© 2026 Ali Adel Alatifi | علي عادل العاطفي",
        "welcome_title": "📜 Welcome Message",
        "theory_tab": "📖 The Theory",
        "guide_tab": "❓ How to Read the Scene",
        "theory_content": """
        > "Is there one law governing the atom and civilization?"
        **S = W × B**
        **Al-Deen Al-Qayyim** = The cosmic law of causality.
        It is "The Balance" upon which the heavens and earth were established.
        """,
        "guide_content": """
        **Colors:**
        - Gold = Balance
        - White = Allegiance (W)
        - Red = Disavowal (B)
        - Pink = Danger
        **Elements:**
        - Golden circle = Stability (S)
        - Cyan disc = Empowerment (E)
        - Evidence panel = S leads E
        """,
        "book_title": "📖 The Mizan Book",
        "book_intro": "The Mizan Theory – From Cosmic Duality to the Equation of Existence S = W × B",
        "control_panel": "🎛️ Control Panel",
        "run_btn": "▶️ Run",
        "stop_btn": "⏹️ Stop",
        "reset_btn": "🔄 Reset",
        "cache_btn": "🧹 Clear Cache",
        "pillars": "🕌 Pillars of Islam",
        "governance": "🏛️ Governance Principles",
        "reform": "🛡️ Reform Mechanisms",
        "corruption": "💀 Corruption Mechanisms",
        "diseases": "⚠️ Moral Diseases",
        "settings": "⚙️ Simulation Settings",
        "sliders": {
            "prayer": "Prayer", "zakat": "Zakat", "fasting": "Fasting", "hajj": "Hajj",
            "amr": "Enjoining Good", "nahy": "Forbidding Evil", "adl": "Justice", "shura": "Consultation",
            "tb": "Cooperating in Righteousness", "th": "Enjoining Truth", "tt": "Cooperating in Piety", "ts": "Enjoining Patience",
            "nm": "Forbidding Good (Corruption)", "amr_e": "Enjoining Evil (Corruption)", "ti": "Cooperating in Sin",
            "tu": "Cooperating in Aggression", "tbat": "Enjoining Falsehood", "as": "Impatience",
            "riba": "Usury (Riba)", "ghish": "Deception", "kadhib": "Lying",
            "cycle": "Cycle Speed", "delay": "Empowerment Delay", "stars": "Number of Stars"
        },
        "download_btn": "📥 Download Scene Image",
        "footer": "© 2026 Ali Adel Alatifi | Al-Deen Al-Qayyim – The Cosmic Balance Law"
    }
}

# =============================================
# ⚙️ Page config
# =============================================
st.set_page_config(
    page_title="Al-Deen Al-Qayyim",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# 🌐 Language selection
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

with st.sidebar:
    lang_choice = st.radio(
        "🌐 اللغة / Language",
        options=["🇸🇦 العربية", "🇬🇧 English"],
        index=0 if st.session_state.lang == "ar" else 1,
        horizontal=True,
        key="lang_radio"
    )
    st.session_state.lang = "ar" if "🇸🇦" in lang_choice else "en"

LANG = st.session_state.lang
T = TEXT[LANG]

# =============================================
# 🎨 CSS (lightweight)
# =============================================
st.markdown("""
<style>
    .stApp { background: #000010; }
    .stButton > button { border: 1px solid #FFD700; color: #FFD700; background: #111; border-radius: 8px; height: 2.5em; }
    .metric-box { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 8px 5px; text-align: center; border: 1px solid #FFD700; }
    .metric-val { font-size: 1.6em; font-weight: bold; margin: 0; }
    .metric-lbl { font-size: 0.7em; color: #aaa; margin: 0; }
    [data-testid="stExpander"] details { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,215,0,0.3); border-radius: 8px; }
    [data-testid="stExpander"] summary { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ Main title
# =============================================
st.title(T["main_heading"])
st.header(T["sub_heading"])
st.caption(f"{T['formula_caption']} | {T['author']}")

# =============================================
# 📜 Welcome message (expandable)
# =============================================
with st.expander(T["welcome_title"], expanded=False):
    tab1, tab2 = st.tabs([T["theory_tab"], T["guide_tab"]])
    with tab1:
        st.markdown(T["theory_content"])
    with tab2:
        st.markdown(T["guide_content"])

st.divider()

# =============================================
# 📖 The Book (embedded)
# =============================================
with st.expander(T["book_title"], expanded=False):
    st.markdown(f"### {T['book_intro']}")
    # We'll embed a condensed version of the book as markdown
    st.markdown("""
    **الباب الأول: الأصول – من أين بدأنا؟**
    ﴿اقْرَأْ بِاسْمِ رَبِّكَ﴾ المنهج الإلهي لاكتشاف النظام.
    **الباب الثاني: التعريفات المركزية**
    الدين القيم، الإسلام الحنيف، العقيدة، العبادة، الشريعة.
    **الباب الثالث: الثنائية الكونية**
    الولاء والبراء في مرآة الوجود – التطابق مع الفيزياء والبيولوجيا.
    **الباب الرابع: وحدة الخلق والأمر**
    ﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ﴾ – الميزان في الآفاق والأنفس.
    **الباب الخامس: الدورة الإلهية المحكمة**
    من الأزل إلى الخلود – مراحل الوجود الخمس.
    **الباب السادس: المختبر – النمذجة الحاسوبية**
    البرهان العملي على S = W × B وطبقة الآخرة.
    **الباب السابع: الفطرة – البوصلة الأصيلة**
    الميل الفطري للإيمان ومحاولات إسكاته.
    **الباب الثامن: سبل العودة إلى القانون**
    الإصلاح الفردي والأسري والمجتمعي.
    **الباب التاسع: التشخيص – واقع الأمة**
    مظاهر الانفصال عن القانون وقراءة الواقع بالميزان.
    **الباب العاشر: الخاتمة – اكتمال الدائرة**
    """)

st.divider()

# =============================================
# 🎛️ Sidebar controls
# =============================================
with st.sidebar:
    st.header(T["control_panel"])

    # --- action buttons ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button(T["run_btn"], use_container_width=True): st.session_state.run = True
    with c2:
        if st.button(T["stop_btn"], use_container_width=True): st.session_state.run = False
    with c3:
        if st.button(T["reset_btn"], use_container_width=True):
            for k in list(st.session_state.keys()):
                if k not in ("lang",): del st.session_state[k]
            st.rerun()
    with c4:
        if st.button(T["cache_btn"], use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            for k in list(st.session_state.keys()):
                if k not in ("lang",): del st.session_state[k]
            st.rerun()

    st.divider()

    # --- expandable groups ---
    with st.expander(T["pillars"], expanded=False):
        prayer = st.slider(T["sliders"]["prayer"], 0.0, 1.0, 0.8, 0.01, key="p")
        zakat = st.slider(T["sliders"]["zakat"], 0.0, 1.0, 0.6, 0.01, key="z")
        fasting = st.slider(T["sliders"]["fasting"], 0.0, 1.0, 0.7, 0.01, key="f")
        hajj = st.slider(T["sliders"]["hajj"], 0.0, 1.0, 0.5, 0.01, key="h")

    with st.expander(T["governance"], expanded=False):
        amr = st.slider(T["sliders"]["amr"], 0.0, 1.0, 0.5, 0.01, key="amr")
        nahy = st.slider(T["sliders"]["nahy"], 0.0, 1.0, 0.5, 0.01, key="nahy")
        adl = st.slider(T["sliders"]["adl"], 0.0, 1.0, 0.6, 0.01, key="adl")
        shura = st.slider(T["sliders"]["shura"], 0.0, 1.0, 0.5, 0.01, key="shura")

    with st.expander(T["reform"], expanded=False):
        taawun_birr = st.slider(T["sliders"]["tb"], 0.0, 1.0, 0.5, 0.01, key="tb")
        tawasi_haqq = st.slider(T["sliders"]["th"], 0.0, 1.0, 0.5, 0.01, key="th")
        taawun_taqwa = st.slider(T["sliders"]["tt"], 0.0, 1.0, 0.5, 0.01, key="tt")
        tawasi_sabr = st.slider(T["sliders"]["ts"], 0.0, 1.0, 0.5, 0.01, key="ts")

    with st.expander(T["corruption"], expanded=False):
        nahy_marouf_e = st.slider(T["sliders"]["nm"], 0.0, 1.0, 0.2, 0.01, key="nm")
        amr_munkar_e = st.slider(T["sliders"]["amr_e"], 0.0, 1.0, 0.2, 0.01, key="amr_e")
        taawun_ithm = st.slider(T["sliders"]["ti"], 0.0, 1.0, 0.2, 0.01, key="ti")
        taawun_udwan = st.slider(T["sliders"]["tu"], 0.0, 1.0, 0.2, 0.01, key="tu")
        tawasi_batil = st.slider(T["sliders"]["tbat"], 0.0, 1.0, 0.2, 0.01, key="tbat")
        adam_sabr = st.slider(T["sliders"]["as"], 0.0, 1.0, 0.2, 0.01, key="as")

    with st.expander(T["diseases"], expanded=False):
        riba = st.slider(T["sliders"]["riba"], 0.0, 1.0, 0.2, 0.01, key="riba")
        ghish = st.slider(T["sliders"]["ghish"], 0.0, 1.0, 0.2, 0.01, key="ghish")
        kadhib = st.slider(T["sliders"]["kadhib"], 0.0, 1.0, 0.2, 0.01, key="kadhib")

    with st.expander(T["settings"], expanded=True):
        cycle_speed = st.slider(T["sliders"]["cycle"], 0.001, 0.05, 0.008, 0.001, key="spd")
        delay_frames = st.slider(T["sliders"]["delay"], 5, 50, 22, 1, key="dly")
        N_STARS = st.slider(T["sliders"]["stars"], 50, 300, 150, 10, key="nst")

# =============================================
# 🧮 Helper functions
# =============================================
def get_color(w, b):
    if w >= 0.7 and b >= 0.7: return '#FFD700'
    if w >= 0.55 and b < 0.45: return '#E0E0E0'
    if w < 0.45 and b >= 0.55: return '#FF5252'
    if w < 0.45 and b < 0.45: return '#FF8A80'
    return '#FFF9C4' if w > b else '#FFCCBC'

def calc_S(W, B, E, p, z, f, h, amr, nahy, adl, shura, riba, ghish, kadhib):
    Sb = W * B
    pillars = (p + z + f + h) / 4
    Sb *= (0.5 + 0.5 * pillars)
    prot = (amr * W + nahy * B) / 2
    Sb *= (0.8 + 0.4 * prot) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    if E > Sb: Sb -= riba * (E - Sb) * 0.3
    return np.clip(Sb, 0.001, 1.0)

# =============================================
# 🏁 Initialization
# =============================================
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False

if not st.session_state.init:
    np.random.seed(42); random.seed(42)
    n = N_STARS if 'N_STARS' in locals() else 150
    cx, cy = 14, 10.0
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-13, cx+13, n)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, n)
    st.session_state.sw = np.random.uniform(0.1, 1.0, n)
    st.session_state.sb = np.random.uniform(0.1, 1.0, n)
    st.session_state.W = 0.55; st.session_state.B = 0.52
    st.session_state.E = 0.3; st.session_state.S = 0.286
    st.session_state.ph = "استقرار"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5; st.session_state.aa = 0.0
    st.session_state.eb = deque([0.286]*30, maxlen=30)
    st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
    st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
    st.session_state.init = True

# =============================================
# 📊 Real-time metrics
# =============================================
if st.session_state.init:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFD700;">{st.session_state.S:.3f}</p><p class="metric-lbl">⚖️ S</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFF;">{st.session_state.W:.3f}</p><p class="metric-lbl">🤍 W</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FF5252;">{st.session_state.B:.3f}</p><p class="metric-lbl">❤️ B</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#00FFFF;">{st.session_state.E:.3f}</p><p class="metric-lbl">💫 E</p></div>', unsafe_allow_html=True)

plot_placeholder = st.empty()

# =============================================
# 🎬 Simulation loop
# =============================================
if st.session_state.get("run", False):
    while st.session_state.run:
        try:
            W = st.session_state.W; B = st.session_state.B; E = st.session_state.E; S = st.session_state.S
            ph = st.session_state.ph; ca = st.session_state.ca
            aW = st.session_state.aW; aB = st.session_state.aB; aa = st.session_state.aa
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx, cy = st.session_state.cx, st.session_state.cy
            eb = st.session_state.eb; pS = st.session_state.pS; pE = st.session_state.pE; px = st.session_state.px

            ca += cycle_speed; sv = np.sin(ca)
            target_S = 0.5 + 0.45 * sv
            if sv > 0.5: ph = 'Peak Stability'
            elif sv > 0: ph = 'Rising'
            elif sv > -0.5: ph = 'Collapsing'
            else: ph = 'Rock Bottom'
            if 0.3 < sv < 0.35: ph = '>> Istidraj <<'
            if -0.35 < sv < -0.3: ph = '>> Recovery <<'

            n = len(sw)
            for i in range(n):
                wb = prayer * 0.01; bb = fasting * 0.01
                dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                close = (dist < 2.0) & (np.arange(n) != i)
                sw[i] += amr * 0.015; sb[i] += nahy * 0.015
                sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + wb
                sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + bb
                if np.any(close):
                    sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03 * (0.5 + 0.5 * shura)
                    sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03 * (0.5 + 0.5 * shura)
                sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

            shock_p = 0.005 * (1 - adl * 0.8)
            if random.random() < shock_p:
                aff = np.random.choice(n, size=int(n * 0.3), replace=False)
                sw[aff] *= np.random.uniform(0.5, 0.8); sb[aff] *= np.random.uniform(0.5, 0.8)

            avgW = np.mean(sw); avgB = np.mean(sb)
            W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            eb.append(S)
            if len(eb) > 30: eb.pop(0)
            E_target = eb[-delay_frames] if len(eb) >= delay_frames else S
            E += 0.03 * (E_target - E)
            W = W - 0.01 * E + 0.02 / (S + 0.1)
            B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            pS.append(S); pE.append(E); px.append(len(px))
            if len(px) > 400: pS.popleft(); pE.popleft(); px.popleft()

            aW += 0.02 + random.uniform(-0.025, 0.025) * (1 - W)**2
            aB += 0.02 + random.uniform(-0.025, 0.025) * (1 - B)**2
            wx = cx + (7 - 2.5 * W) * np.cos(aW); wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB); by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7
            ins = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.07, 0.07, n) * ins; sy += np.random.uniform(-0.07, 0.07, n) * ins
            sx, sy = np.clip(sx, cx-13, cx+13), np.clip(sy, cy-9, cy+9)

            st.session_state.W, st.session_state.B = W, B
            st.session_state.E, st.session_state.S = E, S
            st.session_state.ph, st.session_state.ca = ph, ca
            st.session_state.aW, st.session_state.aB, st.session_state.aa = aW, aB, aa + 0.12
            st.session_state.eb = eb
            st.session_state.sx, st.session_state.sy = sx, sy
            st.session_state.sw, st.session_state.sb = sw, sb
            st.session_state.pS, st.session_state.pE, st.session_state.px = pS, pE, px

            # --- Cosmic scene ---
            fig, ax = plt.subplots(figsize=(12, 9), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),(2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=18, ha='center', va='center', fontweight='bold')
            ax.add_patch(Circle((cx,cy), 0.5+14*E, color='#00FFFF', alpha=0.15, zorder=7))
            ax.add_patch(Circle((cx,cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2, zorder=2))
            colors = [get_color(sw[i], sb[i]) for i in range(n)]
            ax.scatter(sx, sy, s=40, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)
            ax.add_patch(Circle((wx,wy), 0.2+0.5*W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx,by), 0.2+0.5*B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy-1.2, 'W', color='#FFF', fontsize=12, ha='center')
            ax.text(bx, by-1.2, 'B', color='#F33', fontsize=12, ha='center')
            # Evidence panel (larger)
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            if pSl:
                pax = ax.inset_axes([0.35, 0.02, 0.60, 0.15])
                pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
                pax.set_title('📈 Evidence Panel: S leads E (Istidraj)', color='white', fontsize=9, fontweight='bold')
                pax.tick_params(colors='white', labelsize=6); pax.grid(True, alpha=0.3)
                pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S')
                pax.plot(pxl, pEl, color='#00FFFF', lw=2, label='E')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=7)
            ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, ha='center', fontweight='bold')
            plt.tight_layout(pad=0)
            plot_placeholder.pyplot(fig)
            # save image for download
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, facecolor='#000010')
            buf.seek(0)
            st.session_state.latest_image = buf
            plt.close(fig)
            time.sleep(0.08)
        except Exception as e:
            st.error(str(e))
            st.session_state.run = False
            break
    st.success("⏸️ Simulation stopped." if LANG == "en" else "⏸️ تم إيقاف المحاكاة.")
else:
    if st.session_state.init:
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9)
        ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
        plot_placeholder.pyplot(fig)
        plt.close(fig)

# =============================================
# 📥 Download button
# =============================================
if 'latest_image' in st.session_state:
    st.download_button(T["download_btn"], st.session_state.latest_image, "mizan_scene.png", "image/png")

st.caption(T["footer"])
