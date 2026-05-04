# =============================================
# ⚖️ AL-DEEN AL-QAYYIM – THE COSMIC BALANCE LAW
# S = W × B | W = الولاء (Allegiance) | B = البراءة (Disavowal)
#
# © 2026 Ali Adel Alatifi
# All rights reserved.
# Licensed under GNU GPL v3.0
# =============================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# ⚙️ إعداد الصفحة
# =============================================
st.set_page_config(
    page_title="الدين القيم – قانون التوازن الكوني",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# 🎨 التصميم
# =============================================
st.markdown("""
<style>
    .stApp { background: #000010; }
    .golden-title {
        font-size: 2.5em; font-weight: 900; text-align: center; margin: 10px 0 0 0;
        background: linear-gradient(180deg, #FFE566 0%, #FFD700 40%, #DAA520 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: none; letter-spacing: 3px;
    }
    .sub-title { font-size: 1.2em; color: #FFD700; text-align: center; margin: 5px 0; }
    .author-line { font-size: 0.9em; color: #CCCCCC; text-align: center; margin-bottom: 20px; }
    .stButton > button {
        border-radius: 10px; font-weight: bold; height: 2.6em;
        background: #1a1a3e; color: #FFD700; border: 1.5px solid #DAA520;
    }
    .metric-box {
        background: rgba(255,255,255,0.05); border-radius: 10px; padding: 8px 5px;
        text-align: center; border: 1px solid rgba(255,215,0,0.2);
    }
    .metric-val { font-size: 1.8em; font-weight: bold; margin: 0; }
    .metric-lbl { font-size: 0.8em; color: #aaa; margin: 0; }
    [data-testid="stExpander"] details {
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,215,0,0.3);
        border-radius: 8px; margin-bottom: 5px;
    }
    [data-testid="stExpander"] summary { color: #FFD700; font-weight: bold; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ العنوان والمؤلف
# =============================================
st.markdown('<p class="golden-title">⚖️ الدِّينُ الْقَيِّم ⚖️</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">قَانُونُ التَّوَازُنِ الْكَوْنِيّ | S = W × B</p>', unsafe_allow_html=True)
st.markdown('<p class="author-line">© 2026 Ali Adel Alatifi | علي عادل العاطفي</p>', unsafe_allow_html=True)

# =============================================
# 📜 رسالة الترحيب والتعريفات (قابلة للطي)
# =============================================
with st.expander("📜 رسالة الترحيب – افتح للقراءة", expanded=False):
    tab1, tab2 = st.tabs(["📖 النظرية", "❓ كيف تقرأ المشهد"])
    
    with tab1:
        st.markdown("""
        <div style="text-align: center; font-size: 1em; line-height: 2.2; color: #CCCCCC;">
        > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
        > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"
        
        ---
        
        <b style="color: #FFD700;">الدين القيم</b> = قانون السببية الكوني، وهو الحق لأن واضعه الحق،
        وهو القيم لأنه من القيوم نفسه. هو القانون الأعظم، إنه "الدين القيم"
        الذي هو أصل الوجود وغايته.
        
        إنه <b style="color: #FFD700;">"الميزان"</b> الذي قامت به السماوات والأرض،
        والذي يدور حوله كل شيء، من الأزل إلى الخلود.
        
        ---
        
        <b style="color: #FFD700;">الإسلام</b> = الاستجابة المثلى للقانون الإلهي من خلال توازن الولاء والبراءة،
        كل مخلوق بما يناسب فطرته = الثبات والاستقرار في كل شيء.
        
        ---
        
        ﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا﴾ — الروم 30
        
        ---
        
        <b>© 2026 Ali Adel Alatifi | علي عادل العاطفي</b>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        ### 🔍 دليل قراءة المشهد
        
        - **كل نقطة**: كيان (فرد أو مجتمع).
        - **🟡 ذهبي**: توازن مثالي (W و B مرتفعان).
        - **⚪ أبيض/رمادي**: غلبة الولاء (W) مع ضعف البراءة (B).
        - **🔴 أحمر**: غلبة البراءة (B) مع ضعف الولاء (W).
        - **🩷 وردي/برتقالي**: منطقة الخطر (كلاهما منخفض).
        
        - **الدائرة الذهبية حول المركز**: قوة الاستقرار (S).
        - **القرص السماوي**: التمكين (E). إذا اتسع بينما يضيق الذهبي، فهذا هو **الاستدراج**.
        - **الميزان في الأعلى**: يوضح نسبة W (أبيض) إلى B (أحمر).
        - **لوحة الإثبات أسفل الرسم**: الخط الذهبي S يقود الخط السماوي E.
        """)

# =============================================
# 📊 مؤشرات الميزان
# =============================================
if 'init' in st.session_state and st.session_state.init:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFD700;">{st.session_state.S:.3f}</p><p class="metric-lbl">⚖️ استقرار S</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFF;">{st.session_state.W:.3f}</p><p class="metric-lbl">🤍 ولاء W</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FF5252;">{st.session_state.B:.3f}</p><p class="metric-lbl">❤️ براءة B</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#00FFFF;">{st.session_state.E:.3f}</p><p class="metric-lbl">💫 تمكين E</p></div>', unsafe_allow_html=True)

# =============================================
# 🎛️ الشريط الجانبي – لوحة التحكم الكاملة
# =============================================
with st.sidebar:
    st.header("🎛️ لوحة التحكم")
    
    # أزرار التحكم
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("▶️ تشغيل", use_container_width=True): st.session_state.run = True
    with c2:
        if st.button("⏹️ إيقاف", use_container_width=True): st.session_state.run = False
    with c3:
        if st.button("🔄 إعادة", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
    
    st.markdown("---")
    
    # الخيارات في موسعات (طي الصفحات)
    with st.expander("🕌 أركان الإسلام", expanded=True):
        prayer = st.slider("الصلاة 🟣", 0.0, 1.0, 0.8, 0.01, key="p")
        zakat = st.slider("الزكاة 🟡", 0.0, 1.0, 0.6, 0.01, key="z")
        fasting = st.slider("الصوم 🟠", 0.0, 1.0, 0.7, 0.01, key="f")
        hajj = st.slider("الحج 🔵", 0.0, 1.0, 0.5, 0.01, key="h")
    
    with st.expander("🏛️ أسس الحكم", expanded=False):
        amr = st.slider("الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01, key="amr")
        nahy = st.slider("النهي عن المنكر", 0.0, 1.0, 0.5, 0.01, key="nahy")
        adl = st.slider("العدل ⚖️", 0.0, 1.0, 0.6, 0.01, key="adl")
        shura = st.slider("الشورى 🤝", 0.0, 1.0, 0.5, 0.01, key="shura")
    
    with st.expander("🛡️ آليات الإصلاح", expanded=False):
        taawun_birr = st.slider("التعاون على البر", 0.0, 1.0, 0.5, 0.01, key="tb")
        tawasi_haqq = st.slider("التواصي بالحق", 0.0, 1.0, 0.5, 0.01, key="th")
        taawun_taqwa = st.slider("التعاون على التقوى", 0.0, 1.0, 0.5, 0.01, key="tt")
        tawasi_sabr = st.slider("التواصي بالصبر", 0.0, 1.0, 0.5, 0.01, key="ts")
    
    with st.expander("💀 آليات الإفساد", expanded=False):
        nahy_marouf_e = st.slider("النهي عن المعروف (إفساد)", 0.0, 1.0, 0.2, 0.01, key="nm")
        amr_munkar_e = st.slider("الأمر بالمنكر (إفساد)", 0.0, 1.0, 0.2, 0.01, key="amr_e")
        taawun_ithm = st.slider("التعاون على الإثم", 0.0, 1.0, 0.2, 0.01, key="ti")
        taawun_udwan = st.slider("التعاون على العدوان", 0.0, 1.0, 0.2, 0.01, key="tu")
        tawasi_batil = st.slider("التواصي بالباطل", 0.0, 1.0, 0.2, 0.01, key="tbat")
        adam_sabr = st.slider("عدم الصبر", 0.0, 1.0, 0.2, 0.01, key="as")
    
    with st.expander("⚠️ الأمراض الأخلاقية", expanded=False):
        riba = st.slider("الربا 💸", 0.0, 1.0, 0.2, 0.01, key="riba")
        ghish = st.slider("الغش 🎭", 0.0, 1.0, 0.2, 0.01, key="ghish")
        kadhib = st.slider("الكذب 🤥", 0.0, 1.0, 0.2, 0.01, key="kadhib")
    
    with st.expander("⚙️ إعدادات المحاكاة", expanded=True):
        cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001, key="spd")
        delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1, key="dly")
        N_STARS = st.slider("عدد النجوم", 50, 300, 150, 10, key="nst")

# =============================================
# 🧮 دوال المحاكاة
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
    protection = (amr * W + nahy * B) / 2
    Sb *= (0.8 + 0.4 * protection) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    if E > Sb: Sb -= riba * (E - Sb) * 0.3
    Ww = W * (1 - kadhib * 0.2)
    Sf = Ww * B
    Sf *= (0.5 + 0.5 * pillars) * (0.8 + 0.4 * protection) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    return np.clip(Sf, 0.001, 1.0)

# =============================================
# 🏁 تهيئة المحاكاة
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
    st.session_state.E = 0.3; st.session_state.S = 0.55 * 0.52
    st.session_state.ph = "استقرار"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5; st.session_state.aa = 0.0
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
    st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
    st.session_state.init = True

# =============================================
# 🎬 المحاكاة الحية
# =============================================
plot_placeholder = st.empty()

if st.session_state.get("run", False):
    while st.session_state.run:
        try:
            W = st.session_state.W; B = st.session_state.B; E = st.session_state.E; S = st.session_state.S
            ph = st.session_state.ph; ca = st.session_state.ca
            aW = st.session_state.aW; aB = st.session_state.aB; aa = st.session_state.aa
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx, cy = st.session_state.cx, st.session_state.cy
            eb = st.session_state.eb; pS = st.session_state.pS; pE = st.session_state.pE
            px = st.session_state.px; pc = st.session_state.pc

            ca += cycle_speed; sv = np.sin(ca)
            target_S = 0.5 + 0.45 * sv
            if sv > 0.5: ph = 'استقرار تام'
            elif sv > 0: ph = 'صعود'
            elif sv > -0.5: ph = 'انهيار'
            else: ph = 'قاع'
            if 0.3 < sv < 0.35: ph = '>> استدراج <<'
            if -0.35 < sv < -0.3: ph = '>> تعافي <<'

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
            if random.random() < shock_p:
                aff = np.random.choice(n, size=int(n * 0.2), replace=False)
                sw[aff] = np.minimum(1.0, sw[aff] * 1.3); sb[aff] = np.minimum(1.0, sb[aff] * 1.2)

            avgW = np.mean(sw); avgB = np.mean(sb)
            W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            eb.append(S)
            eff = int(delay_frames * (1 + ghish * 0.5))
            Et = list(eb)[-min(eff, len(eb))] if len(eb) >= eff else S
            E += 0.03 * (Et - E)
            W = W - 0.01 * E + 0.02 / (S + 0.1)
            B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            pc += 1
            if pc % 2 == 0: pS.append(S); pE.append(E); px.append(len(px))
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
            st.session_state.pS, st.session_state.pE, st.session_state.px, st.session_state.pc = pS, pE, px, pc

            # ---------- المشهد الكوني ----------
            fig, ax = plt.subplots(figsize=(12, 9), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            
            # نواة الاستقرار
            for r, a, c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                            (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=20, ha='center', va='center', fontweight='bold')
            
            # هالة التمكين
            ax.add_patch(Circle((cx,cy), 0.5+12*E, color='#00FFFF', alpha=0.2, zorder=7))
            ax.add_patch(Circle((cx,cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2, zorder=2))
            
            # مدارات
            for r in [10.0, 11.5, 13.0]:
                ax.add_patch(Circle((cx,cy), r, color='#FFD700', alpha=0.03, fill=False, lw=0.8, ls=':', zorder=0))
            
            # نقاط W و B
            for i in range(6):
                an = -np.pi/4 + i*(np.pi/2)/5
                ax.add_patch(Circle((cx+8.5*np.cos(an), cy+8.5*np.sin(an)), 0.4,
                                    color='#FFF', alpha=0.3+0.5*avgW, zorder=8))
            for i in range(6):
                an = np.pi - np.pi/4 + i*(np.pi/2)/5
                ax.add_patch(Circle((cx+8.5*np.cos(an), cy+8.5*np.sin(an)), 0.4,
                                    color='#F33', alpha=0.25+0.35*avgB, zorder=8))
            
            # كوكبا W و B
            ax.add_patch(Circle((wx,wy), 0.2+0.5*W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx,by), 0.2+0.5*B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy-1.2, 'W', color='#FFF', fontsize=12, ha='center', fontweight='bold')
            ax.text(bx, by-1.2, 'B', color='#F33', fontsize=12, ha='center', fontweight='bold')
            
            # نجوم
            colors = [get_color(sw[i], sb[i]) for i in range(n)]
            ax.scatter(sx, sy, s=45, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)
            
            # ذرة
            er = 0.5 + 0.4 * S
            ax.add_patch(Circle((3.5, 4.0), 0.15+0.2*S, color='#4488FF', alpha=0.8, zorder=7))
            ax.add_patch(Circle((3.5+er*np.cos(aa), 4.0+er*np.sin(aa)), 0.04, color='white', alpha=0.95, zorder=8))
            ax.text(3.5, 2.7, '⚛️ ذرة', color='#4488FF', fontsize=8, ha='center')
            
            # خلية
            ax.add_patch(Circle((24.5, 4.0), 0.35+0.45*S, color='#00FF88', alpha=0.35, zorder=7))
            ax.add_patch(Circle((24.5, 4.0), 0.1+0.15*S, color='white', alpha=0.8, zorder=8))
            ax.text(24.5, 2.7, '🧫 خلية', color='#00FF88', fontsize=8, ha='center')
            
            # الميزان
            mx, my, bw, bh = 0.5, 17, 4.0, 0.6
            ax.add_patch(FancyBboxPatch((mx,my), bw, bh, boxstyle="round,pad=0.2",
                                        facecolor='#1a1a2e', alpha=0.9, zorder=20))
            if W > 0: ax.add_patch(FancyBboxPatch((mx,my), W*bw/2, bh, boxstyle="round,pad=0.1",
                                                  facecolor='#FFF', alpha=0.9, zorder=21))
            if B > 0: ax.add_patch(FancyBboxPatch((mx+bw/2,my), B*bw/2, bh, boxstyle="round,pad=0.1",
                                                  facecolor='#F33', alpha=0.9, zorder=21))
            if W+B > 0: ax.plot(mx+(W/(W+B))*bw, my+bh/2, 'v', color='#FFD700', markersize=15,
                                markeredgecolor='white', zorder=22)
            ax.text(mx, my-0.8, f'W={W:.2f}', color='white', fontsize=8, ha='center')
            ax.text(mx+bw, my-0.8, f'B={B:.2f}', color='#F33', fontsize=8, ha='center')
            ax.text(mx+bw/2, my+bh+0.8, '⚖️ الميزان', color='#FFD700', fontsize=10, ha='center', fontweight='bold')
            
            # لوحة الإثبات – مكبرة وواضحة
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            if pSl:
                pax = ax.inset_axes([0.35, 0.02, 0.60, 0.16])  # أكبر من السابق
                pax.set_xlim(0, max(400, len(pxl))); pax.set_ylim(0, 1.05)
                pax.set_title('📈 لوحة الإثبات: S (الذهب) يقود E (السماوي) — الاستدراج',
                              color='white', fontsize=9, fontweight='bold')
                pax.tick_params(colors='white', labelsize=6); pax.grid(True, alpha=0.3)
                pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S (الاستقرار)')
                pax.plot(pxl, pEl, color='#00FFFF', lw=2, label='E (التمكين)')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=7)
            
            ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=15,
                    ha='center', fontweight='bold')
            plt.tight_layout(pad=0)
            plot_placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.08)
        except Exception as e:
            st.error(str(e)); st.session_state.run = False; break
    st.success("⏸️ تم إيقاف المحاكاة")
else:
    if st.session_state.init:
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx, st.session_state.sy, s=30, c=colors, alpha=0.9,
                   edgecolors='white', linewidths=0.3)
        ax.text(14, 10, '⚖️', fontsize=35, ha='center', va='center', color='#FFD700')
        ax.set_title('اضغط ▶️ تشغيل لاستكشاف أسرار الميزان', color='white', fontsize=14, fontweight='bold')
        plot_placeholder.pyplot(fig)
        plt.close(fig)

# =============================================
# 📥 تذييل
# =============================================
st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;font-size:0.8em;'>© 2026 Ali Adel Alatifi | Al-Deen Al-Qayyim – The Cosmic Balance Law | V31</p>", unsafe_allow_html=True)
