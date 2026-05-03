import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random, time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# ⚖️ الدِّينُ الْقَيِّم – للجوال
# =============================================

st.set_page_config(
    page_title="الدين القيم",
    page_icon="⚖️",
    layout="centered", # الأفضل للجوال
    initial_sidebar_state="collapsed"
)

# =============================================
# 🎨 CSS قوي لتحسين عرض الجوال
# =============================================
st.markdown("""
<style>
    /* خلفية داكنة */
    .stApp {
        background: #0a0a1a;
    }
    /* عنوان رئيسي */
    .main-title {
        font-size: 1.8em;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        margin: 5px 0 0 0;
        text-shadow: 0 0 10px rgba(255,215,0,0.6);
    }
    .sub-title {
        font-size: 0.9em;
        color: #CCCCCC;
        text-align: center;
        margin: 0 0 15px 0;
    }
    /* أزرار التحكم */
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        height: 3.2em;
        width: 100%;
        font-size: 1.1em;
        background-color: #1a1a2e;
        color: white;
        border: 2px solid #FFD700;
        transition: all 0.3s;
    }
    .stButton>button:active {
        background-color: #FFD700;
        color: black;
        transform: scale(0.95);
    }
    /* أشرطة التمرير */
    .stSlider>div>div>div>div {
        background: #FFD700;
    }
    /* بطاقات المؤشرات */
    .metric-card {
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 12px 5px;
        text-align: center;
        border: 1px solid rgba(255,215,0,0.2);
        margin: 3px 0;
    }
    .metric-value {
        font-size: 1.6em;
        font-weight: bold;
        margin: 0;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.65em;
        color: #aaa;
        margin: 0;
    }
    /* إخفاء عناصر Streamlit الافتراضية */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding: 10px 5px 10px 5px;
    }
    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.8em;
        padding: 8px 10px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ عنوان التطبيق
# =============================================
st.markdown('<p class="main-title">⚖️ الدِّينُ الْقَيِّم ⚖️</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">S = W × B | قانون التوازن الكوني</p>', unsafe_allow_html=True)

# =============================================
# 🎮 أزرار التحكم – في الأعلى دائماً
# =============================================
# نستخدم st.columns لوضع الأزرار جنباً إلى جنب
col1, col2, col3 = st.columns(3)

with col1:
    play_btn = st.button("▶️ تشغيل", key="play", use_container_width=True)
with col2:
    pause_btn = st.button("⏹️ إيقاف", key="pause", use_container_width=True)
with col3:
    reset_btn = st.button("🔄 إعادة", key="reset", use_container_width=True)

# معالجة ضغطات الأزرار
if play_btn:
    st.session_state.run = True
    st.rerun()
if pause_btn:
    st.session_state.run = False
    st.rerun()
if reset_btn:
    st.session_state.init = False
    st.session_state.run = False
    st.rerun()

# =============================================
# 📊 مؤشرات S, W, B, E (مصغرة وجميلة)
# =============================================
if 'init' not in st.session_state: st.session_state.init = False
if 'run' not in st.session_state: st.session_state.run = False

if st.session_state.init:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FFD700;">{st.session_state.S:.2f}</p><p class="metric-label">⚖️ S</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FFF;">{st.session_state.W:.2f}</p><p class="metric-label">🤍 W</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FF5252;">{st.session_state.B:.2f}</p><p class="metric-label">❤️ B</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#00FFFF;">{st.session_state.E:.2f}</p><p class="metric-label">💫 E</p></div>', unsafe_allow_html=True)

# =============================================
# 📑 تبويبات: الإعدادات + الكون
# =============================================
tab1, tab2 = st.tabs(["⚖️ الكون", "🎛️ الإعدادات"])

with tab2:
    st.markdown("**🕌 الأركان**")
    col_a, col_b = st.columns(2)
    with col_a:
        prayer = st.slider("الصلاة", 0.0, 1.0, 0.8, 0.05, key="p")
        zakat = st.slider("الزكاة", 0.0, 1.0, 0.6, 0.05, key="z")
    with col_b:
        fasting = st.slider("الصوم", 0.0, 1.0, 0.7, 0.05, key="f")
        hajj = st.slider("الحج", 0.0, 1.0, 0.5, 0.05, key="h")

    st.markdown("**🏛️ الحكم**")
    col_c, col_d = st.columns(2)
    with col_c:
        amr = st.slider("الأمر بالمعروف", 0.0, 1.0, 0.5, 0.05, key="amr")
        nahy = st.slider("النهي عن المنكر", 0.0, 1.0, 0.5, 0.05, key="nahy")
    with col_d:
        adl = st.slider("العدل", 0.0, 1.0, 0.6, 0.05, key="adl")
        shura = st.slider("الشورى", 0.0, 1.0, 0.5, 0.05, key="shura")

    st.markdown("**🦠 الأمراض**")
    col_e, col_f = st.columns(2)
    with col_e:
        riba = st.slider("الربا", 0.0, 1.0, 0.2, 0.05, key="riba")
        ghish = st.slider("الغش", 0.0, 1.0, 0.2, 0.05, key="ghish")
    with col_f:
        kadhib = st.slider("الكذب", 0.0, 1.0, 0.2, 0.05, key="kadhib")

    st.markdown("**⚡ المحاكاة**")
    cycle_speed = st.slider("سرعة الدورة (ث)", 0.02, 0.3, 0.12, 0.01, key="spd")
    delay_frames = st.slider("تأخير التمكين", 5, 40, 22, 1, key="dly")

with tab1:
    plot_placeholder = st.empty()

# =============================================
# دوال مساعدة
# =============================================
def get_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#FFFFFF'
    elif w < 0.45 and b >= 0.55: return '#FF3333'
    return '#FFF8DC'

def calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib):
    S_base = W * B
    pillars = (prayer + zakat + fasting + hajj) / 4
    S_base *= (0.5 + 0.5 * pillars)
    protection = (amr * W + nahy * B) / 2
    S_base *= (0.8 + 0.4 * protection) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    if E > S_base: S_base -= riba * (E - S_base) * 0.3
    return np.clip(S_base, 0.001, 1.0)

# =============================================
# تهيئة الحالة
# =============================================
if not st.session_state.init:
    np.random.seed(42); random.seed(42)
    N_STARS = 70
    st.session_state.cx, st.session_state.cy = 5, 5
    st.session_state.sx = np.random.uniform(0, 10, N_STARS)
    st.session_state.sy = np.random.uniform(0, 10, N_STARS)
    st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.W = 0.55
    st.session_state.B = 0.52
    st.session_state.E = 0.3
    st.session_state.S = 0.55 * 0.52
    st.session_state.ph = "استقرار"
    st.session_state.ca = 0.0
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.pS = deque(maxlen=200)
    st.session_state.pE = deque(maxlen=200)
    st.session_state.px = deque(maxlen=200)
    st.session_state.init = True

# =============================================
# 🚨 تحذيرات الحالة
# =============================================
if st.session_state.init:
    S, E = st.session_state.S, st.session_state.E
    if E > S * 1.5:
        st.error("⚠️ فجوة استدراج خطيرة!")
    elif E > S * 1.2:
        st.warning("⚡ بداية استدراج")
    elif S < 0.2:
        st.error("🔴 خطر الانهيار")

# =============================================
# ⚡ المحاكاة الحية
# =============================================
if st.session_state.get("run", False):
    while st.session_state.get("run", False):
        try:
            W, B = st.session_state.W, st.session_state.B
            E, S = st.session_state.E, st.session_state.S
            ph, ca = st.session_state.ph, st.session_state.ca
            sx = st.session_state.sx.copy()
            sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy()
            sb = st.session_state.sb.copy()
            eb = st.session_state.eb
            pS, pE, px = st.session_state.pS, st.session_state.pE, st.session_state.px

            ca += 0.1; sv = np.sin(ca)
            target_S = 0.5 + 0.45 * sv
            
            if sv > 0.5: ph = 'استقرار تام'
            elif sv > 0: ph = 'صعود'
            elif sv > -0.5: ph = 'انهيار'
            else: ph = 'قاع'
            if 0.3 < sv < 0.35: ph = '⚠️ استدراج'
            if -0.35 < sv < -0.3: ph = '🌱 تعافي'

            n = len(sw)
            for i in range(n):
                sw[i] += prayer*0.005 + hajj*0.003
                sb[i] += fasting*0.005 + zakat*0.003
                sw[i] += amr*0.008
                sb[i] += nahy*0.008
                
                sw[i] += (target_S - sw[i])*0.02 + np.random.uniform(-0.02,0.02)
                sb[i] += (target_S - sb[i])*0.02 + np.random.uniform(-0.02,0.02)
                
                dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
                close = (dist < 1.5) & (np.arange(n) != i)
                if np.any(close):
                    sw[i] += (np.mean(sw[close]) - sw[i])*shura*0.03
                    sb[i] += (np.mean(sb[close]) - sb[i])*shura*0.03
                
                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)

            # صدمات
            if random.random() < 0.005*(1-adl*0.8):
                aff = np.random.choice(n, size=int(n*0.2), replace=False)
                sw[aff] *= np.random.uniform(0.6,0.9)
                sb[aff] *= np.random.uniform(0.6,0.9)

            avgW, avgB = np.mean(sw), np.mean(sb)
            W += (avgW-W)*0.04; B += (avgB-B)*0.04
            W, B = np.clip(W,0.01,1.0), np.clip(B,0.01,1.0)
            
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            eb.append(S)
            
            Et = list(eb)[-delay_frames] if len(eb) > delay_frames else S
            E += 0.03*(Et - E)
            
            W = W - 0.01*E + 0.02/(S+0.1)
            B = B - 0.008*E + 0.005*(1-B)*W*(1-W)
            W, B = np.clip(W,0.01,1.0), np.clip(B,0.01,1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            
            pS.append(S); pE.append(E); px.append(len(px))
            
            # حركة النجوم
            sx += np.random.uniform(-0.04,0.04,n)
            sy += np.random.uniform(-0.04,0.04,n)
            sx, sy = np.clip(sx,0,10), np.clip(sy,0,10)

            # حفظ
            st.session_state.W, st.session_state.B = W, B
            st.session_state.E, st.session_state.S = E, S
            st.session_state.ph, st.session_state.ca = ph, ca
            st.session_state.sx, st.session_state.sy = sx, sy
            st.session_state.sw, st.session_state.sb = sw, sb
            st.session_state.pS, st.session_state.pE, st.session_state.px = pS, pE, px

            # الرسم – بحجم مثالي للجوال
            fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0a0a1a')
            ax.set_facecolor('#0a0a1a')
            
            colors = [get_color(sw[i], sb[i]) for i in range(n)]
            ax.scatter(sx, sy, c=colors, s=60, alpha=0.9, edgecolors='white', linewidth=0.4)
            ax.add_patch(Circle((5,5), 2*S, color='#FFD700', alpha=0.25))
            ax.add_patch(Circle((5,5), 1.5*E, color='#00FFFF', alpha=0.15))
            ax.text(5, 5, '⚖️', fontsize=24, ha='center', va='center', color='#FFD700')
            ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
            ax.set_title(f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, fontweight='bold')
            
            # لوحة الإثبات في الأسفل
            ax2 = ax.inset_axes([0.1, -0.25, 0.8, 0.25])
            ax2.set_facecolor('#111122')
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            ax2.plot(pxl, pSl, color='#FFD700', lw=2, label='S')
            ax2.plot(pxl, pEl, color='#00FFFF', lw=2, label='E')
            ax2.legend(loc='upper right', fontsize=6, facecolor='#111122', edgecolor='white', labelcolor='white')
            ax2.set_ylim(0,1.05); ax2.tick_params(colors='white', labelsize=6)
            ax2.grid(True, alpha=0.15)
            
            plt.tight_layout(pad=1.5)
            plot_placeholder.pyplot(fig)
            plt.close(fig)
            
            time.sleep(max(0.08, cycle_speed))
            
        except Exception as e:
            st.error(f"خطأ: {str(e)}")
            st.session_state.run = False
            break
    st.success("⏸️ تم إيقاف المحاكاة")
elif st.session_state.init:
    with tab1:
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#0a0a1a')
        ax.set_facecolor('#0a0a1a')
        colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx, st.session_state.sy, c=colors, s=60, alpha=0.9, edgecolors='white', linewidth=0.4)
        ax.add_patch(Circle((5,5), 2*st.session_state.S, color='#FFD700', alpha=0.25))
        ax.text(5, 5, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
        ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
        ax.set_title('اضغط ▶️ تشغيل للبدء', color='white', fontsize=16)
        plot_placeholder.pyplot(fig)
        plt.close(fig)

# تذييل
st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;font-size:0.7em;'>© 2026 علي عادل العاطفي | v14 – للجوال</p>", unsafe_allow_html=True)
