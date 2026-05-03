import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ----------------------------------------------
# إعداد الصفحة
# ----------------------------------------------
st.set_page_config(page_title="⚖️ الميزان", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# ----------------------------------------------
# قاعدة بيانات الحروف الـ 28
# ----------------------------------------------
MIZAN_LETTERS = {
    "light": {
        "أ": {"v": 1,   "l": "الوحدانية", "a": "إِيَّاكَ نَعْبُدُ"},
        "ل": {"v": 30,  "l": "المُلك",     "a": "إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ"},
        "م": {"v": 40,  "l": "الجمع",      "a": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ"},
        "ر": {"v": 200, "l": "اليقظة",     "a": "فَإِذَا فَرَغْتَ فَانصَبْ"},
        "ك": {"v": 20,  "l": "الأمر",      "a": "كُن فَيَكُونُ"},
        "هـ": {"v": 5,   "l": "الهوية",     "a": "وَاجْتَنِبُوا الطَّاغُوتَ"},
        "ي": {"v": 10,  "l": "الاستجابة",  "a": "اسْتَجِيبُوا لِلَّهِ وَلِلرَّسُولِ"},
        "ع": {"v": 70,  "l": "الإدراك",    "a": "وَقُل رَّبِّ زِدْنِي عِلْمًا"},
        "ص": {"v": 90,  "l": "الصمد",      "a": "اللَّهُ الصَّمَدُ"},
        "ق": {"v": 100, "l": "الميزان",    "a": "وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ"},
        "ن": {"v": 50,  "l": "النور",      "a": "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ"},
        "س": {"v": 60,  "l": "السمع",      "a": "سَمِعْنَا وَأَطَعْنَا"},
        "ح": {"v": 8,   "l": "الحياة",     "a": "فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً"},
        "ط": {"v": 9,   "l": "الطهارة",    "a": "إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ"},
    },
    "neutral": {
        "ف": {"v": 80,  "l": "فاء السببية",   "r": "=",  "a": "فَمَن يَكْفُرْ بِالطَّاغُوتِ..."},
        "و": {"v": 6,   "l": "واو العطف",     "r": "×/+","a": "وَيُؤْمِن بِاللَّهِ"},
        "ب": {"v": 2,   "l": "باء الاستعانة", "r": "بـ", "a": "بِسْمِ اللَّهِ الرَّحْمَٰنِ"},
        "ل": {"v": 30,  "l": "لام التعليل",   "r": "→",  "a": "لِيَعْبُدُونِ"},
        "ت": {"v": 400, "l": "تاء الفاعل",    "r": "ف",  "a": "قَالَتِ امْرَأَتُ فِرْعَوْنَ"},
        "ث": {"v": 500, "l": "ثم العطف",      "r": "ت",  "a": "ثُمَّ خَلَقْنَا النُّطْفَةَ"},
    },
    "dark": {
        "ظ": {"v": 900, "l": "الظلم",   "a": "إِنَّ الظَّالِمِينَ لَهُمْ عَذَابٌ أَلِيمٌ"},
        "ض": {"v": 800, "l": "الضلال",  "a": "وَمَن يُضْلِلِ اللَّهُ فَمَا لَهُ مِنْ هَادٍ"},
        "غ": {"v": 1000,"l": "الغش",    "a": "مَنْ غَشَّنَا فَلَيْسَ مِنَّا"},
        "ذ": {"v": 700, "l": "الذل",    "a": "أَذِلَّةٍ عَلَى الْمُؤْمِنِينَ"},
        "خ": {"v": 600, "l": "الخيانة", "a": "لَا تَخُونُوا اللَّهَ وَالرَّسُولَ"},
        "ش": {"v": 300, "l": "الشهوة",  "a": "وَلَا تَتَّبِعِ الْهَوَىٰ"},
        "ز": {"v": 7,   "l": "الزور",   "a": "وَاجْتَنِبُوا قَوْلَ الزُّورِ"},
        "ج": {"v": 3,   "l": "الجهل",   "a": "بَلْ أَكْثَرُهُمْ يَجْهَلُونَ"},
    }
}

# ----------------------------------------------
# النصوص الأساسية (واجهة غنية)
# ----------------------------------------------
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #000000 100%); 
padding: 30px; border-radius: 20px; border: 2px solid #FFD700; margin-bottom: 30px;
box-shadow: 0 0 50px rgba(255, 215, 0, 0.4);">
    <span style="font-size: 70px; display: block;">⚖️</span>
    <h1 style="color: #FFD700; font-size: 55px; margin: 10px 0; text-shadow: 0 0 20px gold; font-weight: 900;">
        الميزان
    </h1>
    <p style="color: #CCCCCC; font-size: 22px; letter-spacing: 2px; margin: 5px 0;">
        S = W × B | قانون التوازن الكوني
    </p>
    <hr style="border-color: #FFD700; width: 50%; opacity: 0.5;">
    <p style="color: #FFFFFF; font-size: 20px; font-style: italic;">
        "هل يوجد قانون واحد يحكم الذرة والحضارة؟ هذا هو نموذج الميزان الذي يثبت أن S = W × B"
    </p>
    <p style="color: #AAAAAA; font-size: 16px; margin-top: 20px;">
        "أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان. استقراركم ليس صدفة. انهياركم ليس حظاً سيئاً. إنها معادلة. إنها S = W × B."
    </p>
    <hr style="border-color: #FFD700; width: 50%; opacity: 0.5;">
    <p style="color: #FFD700; font-size: 18px; font-weight: bold;">علي عادل العاطفي</p>
    <p style="color: #FFD700; font-size: 14px; opacity: 0.8;">Ali Adel Alatifi | 2026</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------
# الشريط الجانبي (المختبر)
# ----------------------------------------------
with st.sidebar:
    st.image("https://i.imgur.com/5XMQooo.png", width=80) # أيقونة افتراضية
    st.markdown("## ⚖️ لوحة التحكم")
    st.markdown("---")
    
    st.subheader("🕌 أركان الإسلام")
    prayer = st.slider("🟣 الصلاة", 0.0, 1.0, 0.8, 0.01)
    zakat = st.slider("🟡 الزكاة", 0.0, 1.0, 0.6, 0.01)
    fasting = st.slider("🟠 الصوم", 0.0, 1.0, 0.7, 0.01)
    hajj = st.slider("🔵 الحج", 0.0, 1.0, 0.5, 0.01)

    st.subheader("🏛️ أسس الحكم")
    amr = st.slider("📢 الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01)
    nahy = st.slider("🚫 النهي عن المنكر", 0.0, 1.0, 0.5, 0.01)
    adl = st.slider("⚖️ العدل", 0.0, 1.0, 0.6, 0.01)
    shura = st.slider("🤝 الشورى", 0.0, 1.0, 0.5, 0.01)

    st.header("🔤 الحروف العربية الـ 28")
    with st.expander("🔆 النورانية (14)", expanded=False):
        light_vals = {}
        for letter, data in MIZAN_LETTERS["light"].items():
            light_vals[letter] = st.slider(f"{letter} ({data['l']})", 0.0, 1.0, 0.7, 0.01, help=data['a'])
    with st.expander("⚙️ المحايدة (6)", expanded=False):
        neutral_vals = {}
        for letter, data in MIZAN_LETTERS["neutral"].items():
            neutral_vals[letter] = st.slider(f"{letter} ({data['l']})", 0.0, 1.0, 0.5, 0.01, help=data['a'])
    with st.expander("🌑 الظلامية (8)", expanded=False):
        dark_vals = {}
        for letter, data in MIZAN_LETTERS["dark"].items():
            dark_vals[letter] = st.slider(f"{letter} ({data['l']})", 0.0, 1.0, 0.2, 0.01, help=data['a'])

    st.subheader("⚙️ معاملات المحاكاة")
    W_init = st.slider("W (الولاء) الابتدائي", 0.0, 1.0, 0.55, 0.01)
    B_init = st.slider("B (البراءة) الابتدائية", 0.0, 1.0, 0.52, 0.01)
    N_STARS = st.slider("عدد النجوم", 100, 600, 300, 50)
    cycle_speed = st.slider("سرعة الدورة الحضارية", 0.001, 0.05, 0.008, 0.001)
    delay_frames = st.slider("تأخير التمكين (الاستدراج)", 5, 50, 22, 1)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ تشغيل", use_container_width=True):
            st.session_state.run = True
    with col2:
        if st.button("⏹️ إيقاف", use_container_width=True):
            st.session_state.run = False
    with col3:
        if st.button("🔄 إعادة ضبط", use_container_width=True):
            for k in list(st.session_state.keys()):
                if k not in ("lang",): del st.session_state[k]
            st.rerun()

# ----------------------------------------------
# دوال مساعدة
# ----------------------------------------------
def get_color(w, b):
    try:
        w, b = float(w), float(b)
        if w >= 0.7 and b >= 0.7: return '#FFD700'
        if w >= 0.55 and b < 0.45: return '#E0E0E0'
        if w < 0.45 and b >= 0.55: return '#FF5252'
        if w < 0.45 and b < 0.45: return '#FF8A80'
        return '#FFF9C4' if w > b else '#FFCCBC'
    except: return '#888888'

def calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, light_vals, dark_vals):
    ق, ن = light_vals.get('ق',0.7)*100, light_vals.get('ن',0.7)*50
    ص, ط = light_vals.get('ص',0.7)*90, light_vals.get('ط',0.7)*9
    ح, أ = light_vals.get('ح',0.7)*8, light_vals.get('أ',0.7)*1
    ل, م = light_vals.get('ل',0.7)*30, light_vals.get('م',0.7)*40
    ر, ي = light_vals.get('ر',0.7)*200, light_vals.get('ي',0.7)*10
    ع, س = light_vals.get('ع',0.7)*70, light_vals.get('س',0.7)*60
    هـ = light_vals.get('هـ',0.7)*5
    ظ, ض = dark_vals.get('ظ',0.2)*900, dark_vals.get('ض',0.2)*800
    ش, ج = dark_vals.get('ش',0.2)*300, dark_vals.get('ج',0.2)*3
    غ, ذ = dark_vals.get('غ',0.2)*1000, dark_vals.get('ذ',0.2)*700
    خ = dark_vals.get('خ',0.2)*600

    Sb = W * B
    pb = (prayer*(.5+.5*min(1,ن/50))+zakat*(.5+.5*min(1,ص/90))+fasting*(.5+.5*min(1,ط/9))+hajj*(.5+.5*min(1,ح/8)))/4
    Sb *= (.5+.5*pb)
    pr = (amr*W*(.5+.5*min(1,ل/30))+nahy*B*(.5+.5*min(1,ق/100)))/2
    Sb *= (.8+.4*pr) * (.9+.2*adl*(.5+.5*min(1,ل/30))) * (.85+.3*shura*(.5+.5*min(1,م/40)))
    Sb *= (1+.05*min(1,أ/1))*(1+.02*min(1,ر/200))*(1+.03*min(1,ي/10))*(1+.04*min(1,ع/70))*(1+.01*min(1,س/60))*(1+.01*min(1,هـ/5))
    df = max(0.1, 1.0 - .05*min(1,ظ/900) - .03*min(1,ض/800) - .04*min(1,ش/300) - .02*min(1,ج/3))
    Sb *= df
    if E > Sb: Sb -= .3*(1+.5*min(1,غ/1000))*(E-Sb)
    Ww, Bw = W*(1-.15*min(1,خ/600)), B*(1-.15*min(1,ذ/700))
    Sf = Ww * Bw
    Sf *= (.5+.5*pb)*(.8+.4*pr)*(.9+.2*adl*(.5+.5*min(1,ل/30)))*(.85+.3*shura*(.5+.5*min(1,م/40)))*df
    return np.clip(Sf, 0.001, 1.0)

def check_warnings(W, B, S, E, ph):
    w = []
    if E > S*1.5: w.append("⚠️ فجوة استدراج خطيرة")
    elif E > S*1.2: w.append("⚡ بداية استدراج")
    if abs(W-B) > 0.3: w.append("⚖️ اختلال كبير")
    elif abs(W-B) > 0.2: w.append("📊 ميلان")
    if S < 0.2: w.append("🔴 خطر الانهيار")
    elif S < 0.3: w.append("🟠 حالة حرجة")
    if 'ISTIDRAJ' in ph: w.append("💀 استدراج نشط")
    elif 'RECOVERY' in ph: w.append("🌱 مرحلة تعافي")
    return w

def create_heatmap(sw, sb):
    fig, ax = plt.subplots(figsize=(5, 4), facecolor='#000010')
    wr, br = np.linspace(0,1,30), np.linspace(0,1,30)
    Wg, Bg = np.meshgrid(wr, br)
    ax.pcolormesh(Wg, Bg, Wg*Bg, cmap='RdYlGn', shading='auto', vmin=0, vmax=1)
    ax.scatter(sw, sb, c='white', s=5, alpha=0.7)
    ax.set_xlabel('W (الولاء)', color='white', fontsize=10)
    ax.set_ylabel('B (البراءة)', color='white', fontsize=10)
    ax.set_title('S = W × B', color='white', fontsize=12, fontweight='bold')
    ax.tick_params(colors='white', labelsize=8)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    plt.tight_layout(pad=0.5)
    return fig

# ----------------------------------------------
# التهيئة
# ----------------------------------------------
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False

if not st.session_state.init:
    try:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        st.session_state.cx, st.session_state.cy = cx, cy
        st.session_state.sx = np.random.uniform(cx-13, cx+13, N_STARS)
        st.session_state.sy = np.random.uniform(cy-9, cy+9, N_STARS)
        st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.W, st.session_state.B = W_init, B_init
        st.session_state.E, st.session_state.S = 0.3, W_init*B_init
        st.session_state.ph, st.session_state.ca = "Balance", 0.0
        st.session_state.aW, st.session_state.aB, st.session_state.aa = 0.0, np.pi*0.5, 0.0
        st.session_state.eb = deque([W_init*B_init]*30, maxlen=30)
        st.session_state.pS = deque(maxlen=400)
        st.session_state.pE = deque(maxlen=400)
        st.session_state.px = deque(maxlen=400)
        st.session_state.pc = 0
        st.session_state.init = True
    except Exception as e:
        st.error(f"خطأ في التهيئة: {str(e)}")
        st.session_state.init = False

# ----------------------------------------------
# قسم العدادات (مكبر)
# ----------------------------------------------
if st.session_state.init:
    st.markdown("<br>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 28px; margin: 0;'>{st.session_state.S:.3f}</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white; margin: 0;'>⚖️ استقرار (S)</p>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<p style='text-align: center; color: #FFFFFF; font-size: 28px; margin: 0;'>{st.session_state.W:.3f}</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white; margin: 0;'>🤍 ولاء (W)</p>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<p style='text-align: center; color: #FF3333; font-size: 28px; margin: 0;'>{st.session_state.B:.3f}</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white; margin: 0;'>❤️ براءة (B)</p>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<p style='text-align: center; color: #00FFFF; font-size: 28px; margin: 0;'>{st.session_state.E:.3f}</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white; margin: 0;'>💫 تمكين (E)</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    warns = check_warnings(st.session_state.W, st.session_state.B, st.session_state.S, st.session_state.E, st.session_state.ph)
    if warns: st.error(" | ".join(warns))
    else: st.success("✅ النظام في حالة توازن تام")

# ----------------------------------------------
# المحاكاة الحية
# ----------------------------------------------
if st.session_state.get("run", False):
    placeholder = st.empty()
    
    while st.session_state.get("run", False):
        try:
            W, B, E = st.session_state.W, st.session_state.B, st.session_state.E
            S, ph, ca = st.session_state.S, st.session_state.ph, st.session_state.ca
            aW, aB, aa = st.session_state.aW, st.session_state.aB, st.session_state.aa
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx, cy = st.session_state.cx, st.session_state.cy
            eb = st.session_state.eb
            pS = st.session_state.pS.copy(); pE = st.session_state.pE.copy()
            px = st.session_state.px.copy(); pc = st.session_state.pc

            ca += cycle_speed
            sv = np.sin(ca)
            if sv > 0.5: ph = 'استقرار تام'
            elif sv > 0: ph = 'صعود'
            elif sv > -0.5: ph = 'انهيار'
            else: ph = 'قاع'
            if 0.3 < sv < 0.35: ph = '>> استدراج <<'
            if -0.35 < sv < -0.3: ph = '>> تعافي <<'
            target_S = 0.5 + 0.45*sv

            n_stars = len(sw)
            for i in range(n_stars):
                wb = prayer*0.01*(0.5+0.5*light_vals.get('ن',0.7))
                bb = fasting*0.01*(0.5+0.5*light_vals.get('ط',0.7))
                dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
                close = (dist < 2.0) & (np.arange(n_stars) != i)
                sw[i] += amr*0.015; sb[i] += nahy*0.015
                sw[i] += (target_S-sw[i])*0.02 + np.random.uniform(-0.02,0.02) + wb
                sb[i] += (target_S-sb[i])*0.02 + np.random.uniform(-0.02,0.02) + bb
                if np.any(close):
                    sw[i] += (np.mean(sw[close])-sw[i])*0.03*(0.5+0.5*shura)
                    sb[i] += (np.mean(sb[close])-sb[i])*0.03*(0.5+0.5*shura)
                sw[i] *= (1-dark_vals.get('خ',0.2)*0.02); sb[i] *= (1-dark_vals.get('ذ',0.2)*0.02)
                sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

            shock_p = 0.005*(1-adl*0.8)*(1-light_vals.get('ر',0.7)*0.5)
            if random.random() < shock_p:
                aff = np.random.choice(n_stars, size=int(n_stars*0.3), replace=False)
                sw[aff] *= np.random.uniform(0.5,0.8); sb[aff] *= np.random.uniform(0.5,0.8)
            if random.random() < shock_p:
                aff = np.random.choice(n_stars, size=int(n_stars*0.2), replace=False)
                sw[aff] = np.minimum(1.0, sw[aff]*1.3); sb[aff] = np.minimum(1.0, sb[aff]*1.2)

            avgW, avgB = np.mean(sw), np.mean(sb)
            W += (avgW-W)*0.04; B += (avgB-B)*0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = calc_S(W,B,E,prayer,zakat,fasting,hajj,amr,nahy,adl,shura,light_vals,dark_vals)
            eb.append(S)
            eff_delay = int(delay_frames*(1+dark_vals.get('غ',0.2)*0.5))
            eb_list = list(eb)
            E_target = eb_list[-min(eff_delay, len(eb_list))] if len(eb_list) >= eff_delay else S
            E += 0.03*(E_target-E)
            zf = 1+0.1*dark_vals.get('ظ',0.2)
            W = W - 0.015*E*zf + 0.03/(S+0.1) - 0.007*(1-B)
            B = B - 0.012*E*zf + 0.006*(1-B)*W*(1-W)
            W, B = np.clip(W,0.01,1.0), np.clip(B,0.01,1.0)
            S = calc_S(W,B,E,prayer,zakat,fasting,hajj,amr,nahy,adl,shura,light_vals,dark_vals)
            pc += 1
            if pc%2 == 0: pS.append(S); pE.append(E); px.append(len(px))
            aW += 0.02+random.uniform(-0.025,0.025)*(1-W)**2
            aB += 0.02+random.uniform(-0.025,0.025)*(1-B)**2
            wx = cx+(7-2.5*W)*np.cos(aW); wy = cy+(7-2.5*W)*np.sin(aW)*0.7
            bx = cx+(5-1.5*B)*np.cos(aB); by = cy+(5-1.5*B)*np.sin(aB)*0.7
            ins = 1-np.mean(sw*sb)
            sx += np.random.uniform(-0.07,0.07,n_stars)*ins
            sy += np.random.uniform(-0.07,0.07,n_stars)*ins
            sx, sy = np.clip(sx,cx-13,cx+13), np.clip(sy,cy-9,cy+9)

            st.session_state.W, st.session_state.B = W, B
            st.session_state.E, st.session_state.S = E, S
            st.session_state.ph, st.session_state.ca = ph, ca
            st.session_state.aW, st.session_state.aB, st.session_state.aa = aW, aB, aa+0.12
            st.session_state.eb = eb
            st.session_state.sx, st.session_state.sy = sx, sy
            st.session_state.sw, st.session_state.sb = sw, sb
            st.session_state.pS, st.session_state.pE, st.session_state.px, st.session_state.pc = pS, pE, px, pc

            # ----------------------------------------------
            # الرسم البياني العملاق
            # ----------------------------------------------
            fig, ax = plt.subplots(figsize=(20, 15), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')

            for r, a, c in [(0.5,0.98,'#FFF'), (1,0.65,'#FFD700'), (1.7,0.3,'#FFD700'), (2.6,0.12,'#FFA500'), (3.8,0.05,'#FF6347'), (5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=20, ha='center', va='center', fontweight='bold')
            ax.text(cx, cy-2.5, f'S={S:.2f}', color='#FFD700', fontsize=14, ha='center')

            ax.add_patch(Circle((cx,cy), 0.5+16*E, color='#00FFFF', alpha=0.25*(1-min(E,1))+0.04, zorder=7))
            ax.add_patch(Circle((cx,cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=3, zorder=2))
            for r in [10.0, 11.5, 13.0]:
                ax.add_patch(Circle((cx,cy), r, color='#FFD700', alpha=0.03, fill=False, lw=0.8, ls=':'))

            for i in range(6):
                an = -np.pi/4 + i*(np.pi/2)/5
                ax.add_patch(Circle((cx+8.5*np.cos(an), cy+8.5*np.sin(an)), 0.5, color='#FFF', alpha=0.3+0.5*avgW, zorder=8))
            for i in range(6):
                an = np.pi - np.pi/4 + i*(np.pi/2)/5
                ax.add_patch(Circle((cx+8.5*np.cos(an), cy+8.5*np.sin(an)), 0.5, color='#F33', alpha=0.25+0.35*avgB, zorder=8))

            ax.add_patch(Circle((wx,wy), 0.2+0.6*W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx,by), 0.2+0.6*B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy+0.8, 'W', color='#FFF', fontsize=14, ha='center')
            ax.text(bx, by+0.8, 'B', color='#F33', fontsize=14, ha='center')

            colors = [get_color(sw[i], sb[i]) for i in range(n_stars)]
            ax.scatter(sx, sy, s=45, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)

            aa += 0.12; er = 0.5+0.4*S
            ax.add_patch(Circle((3.5, 4.0), 0.15+0.25*S, color='#4488FF', alpha=0.8, zorder=7))
            ax.add_patch(Circle((3.5+er*np.cos(aa), 4.0+er*np.sin(aa)), 0.04, color='white', alpha=0.95, zorder=8))
            ax.text(3.5, 2.7, '⚛️ ذرة', color='#4488FF', fontsize=8, ha='center')

            chem_x, chem_y = 9.5, 4.0
            ax.add_patch(RegularPolygon((chem_x, chem_y), numVertices=6, radius=0.35+0.25*S, orientation=np.pi/6, facecolor='#FFA500', alpha=0.7, zorder=7))
            ax.text(chem_x, chem_y-0.9, '🧪 جزيء', color='#FFA500', fontsize=8, ha='center')

            ax.add_patch(Circle((24.5, 4.0), 0.35+0.45*S, color='#00FF88', alpha=0.35, zorder=7, ec='#00FF88', lw=1.5))
            ax.add_patch(Circle((24.5, 4.0), 0.1+0.15*S, color='white', alpha=0.8, zorder=8))
            ax.text(24.5, 2.7, '🧫 خلية', color='#00FF88', fontsize=8, ha='center')

            # مقياس الميزان
            mx, my, bw, bh = 0.5, 16.5, 4.0, 0.6
            ax.add_patch(FancyBboxPatch((mx,my), bw, bh, boxstyle="round,pad=0.2", facecolor='#1a1a2e', alpha=0.9, zorder=20))
            if W > 0: ax.add_patch(FancyBboxPatch((mx,my), W*bw/2, bh, boxstyle="round,pad=0.1", facecolor='#FFF', alpha=0.9, zorder=21))
            if B > 0: ax.add_patch(FancyBboxPatch((mx+bw/2,my), B*bw/2, bh, boxstyle="round,pad=0.1", facecolor='#F33', alpha=0.9, zorder=21))
            if W+B > 0: ax.plot(mx+(W/(W+B))*bw, my+bh/2, 'v', color='#FFD700', markersize=15, markeredgecolor='white', zorder=22)
            ax.text(mx, my-0.8, f'W={W:.2f}', color='white', fontsize=10, ha='center')
            ax.text(mx+bw, my-0.8, f'B={B:.2f}', color='#F33', fontsize=10, ha='center')
            ax.text(mx+bw/2, my+bh+0.8, '⚖️ الميزان', color='#FFD700', fontsize=12, ha='center', fontweight='bold')

            # لوحة الإثبات (مكبرة)
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            if pSl:
                pax = ax.inset_axes([0.45, 0.02, 0.50, 0.14])
                pax.set_xlim(0, max(400, len(pxl))); pax.set_ylim(0, 1.05)
                pax.set_title('📈 لوحة الإثبات: S يقود E (الاستدراج)', color='white', fontsize=10, fontweight='bold')
                pax.tick_params(colors='white', labelsize=7); pax.grid(True, alpha=0.3)
                pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S (الاستقرار)')
                pax.plot(pxl, pEl, color='#00FFFF', lw=2, alpha=0.9, label='E (التمكين)')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=8)

            # خريطة الحرارة (مكبرة)
            hfig = create_heatmap(sw, sb)
            hbuf = BytesIO(); hfig.savefig(hbuf, format='png', dpi=100, facecolor='#000010'); hbuf.seek(0)
            heat_ax = ax.inset_axes([0.02, 0.02, 0.25, 0.22])
            heat_ax.imshow(plt.imread(hbuf)); heat_ax.axis('off'); plt.close(hfig)

            ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=16, ha='center', fontweight='bold')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)

            buf = BytesIO(); fig.savefig(buf, format='png', dpi=120, facecolor='#000010'); buf.seek(0)
            st.session_state.latest_image = buf; plt.close(fig)

            time.sleep(0.1)

        except Exception as e:
            st.error(f"خطأ: {str(e)}")
            st.session_state.run = False
            break
    st.success("⏸️ تم إيقاف المحاكاة")

elif st.session_state.init and 'latest_image' in st.session_state:
    st.image(st.session_state.latest_image, caption="آخر حالة للمحاكاة", use_column_width=True)

# ----------------------------------------------
# تحميل الصورة والتذييل
# ----------------------------------------------
if 'latest_image' in st.session_state:
    st.sidebar.download_button("📥 تحميل صورة المشهد", st.session_state.latest_image, "mizan_scene.png", "image/png")

st.markdown("---")
st.markdown("<p style='text-align:center; color: gray;'>© 2026 علي عادل العاطفي | v6.0 القانون الأعظم</p>", unsafe_allow_html=True)
