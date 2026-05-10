import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import random
import time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# إعداد الصفحة
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="مختبر الميزان – القانون الواحد",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
# اللغة
# ═══════════════════════════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(ar, en):
    return ar if LANG == "ar" else en

# ═══════════════════════════════════════════════════════════════
# تنسيق CSS – روح المشروع
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Cairo&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at center, #0a0a2e 0%, #050510 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Amiri', 'Cairo', serif;
        color: #FFD700;
    }
    
    .main-title {
        font-size: 4em;
        font-weight: 900;
        background: linear-gradient(180deg, #FFE55C 0%, #FFD700 40%, #B8960F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.3);
    }
    
    .sub-title {
        font-size: 1.4em;
        color: #B0B0B0;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Cairo', sans-serif;
    }
    
    .stButton > button {
        background: rgba(20, 20, 60, 0.8);
        border: 1px solid #FFD700;
        color: #FFD700;
        border-radius: 8px;
        padding: 10px 20px;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #FFD700;
        color: #0a0a2e;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(20, 20, 60, 0.6);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 10px 10px 0 0;
        color: #B0B0B0;
        font-family: 'Cairo', sans-serif;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 215, 0, 0.15) !important;
        border-bottom: 2px solid #FFD700 !important;
        color: #FFD700 !important;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# دوال الحساب
# ═══════════════════════════════════════════════════════════════
def get_star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    else: return '#888888'

def classify_quadrant(W, B):
    if W >= 0.5 and B >= 0.5: return "مؤمن", '#FFD700'
    elif W < 0.5 and B >= 0.5: return "كافر", '#FF5252'
    elif W < 0.5 and B < 0.5: return "منافق", '#FFB6C1'
    else: return "مشرك", '#FFA500'

def compute_curvature(W_hist, B_hist):
    if len(W_hist) < 3: return 0.0
    dW = np.gradient(W_hist)
    dB = np.gradient(B_hist)
    ddW = np.gradient(dW)
    ddB = np.gradient(dB)
    num = abs(dW[-1] * ddB[-1] - dB[-1] * ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**(1.5)
    return num / denom

def calc_S(W, B, E, q=1.0):
    return np.clip(W * B * (1 + q * 0.5), 0.001, 1.0)


# ═══════════════════════════════════════════════════════════════
# العنوان الجليل
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="text-align: center; padding: 40px 0 0 0;">
    <h1 class="main-title">⚖️ مختبر الميزان</h1>
    <p style="color: #FFD700; font-size: 1.6em; font-family: 'Cairo'; font-weight: bold;">
        {t('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}
    </p>
    <p style="color: #888; font-size: 1.1em; direction: rtl;">
        {t('﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾', 
           '﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾')}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# لوحة القيادة (الشريط الجانبي)
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🕋 لوحة القيادة")
    
    lang_choice = st.radio("اللغة", ["العربية", "English"], index=0 if LANG == "ar" else 1)
    if (lang_choice == "English" and LANG == "ar") or (lang_choice == "العربية" and LANG == "en"):
        st.session_state.lang = "en" if lang_choice == "English" else "ar"
        st.rerun()
        
    st.markdown("---")
    st.markdown("#### ⚙️ إعدادات المحاكاة")
    W_init = st.slider("W (الولاء)", 0.0, 1.0, 0.55, 0.01)
    B_init = st.slider("B (البراءة)", 0.0, 1.0, 0.52, 0.01)
    lag_frames = st.slider("فجوة الاستدراج", 5, 50, 22, 1)
    N_STARS = st.slider("عدد النجوم", 100, 600, 300, 50)
    q_intensity = st.slider("⚖️ ق (الميزان)", 0.0, 1.0, 1.0, 0.01)
    
    st.markdown("---")
    if st.button("▶️ تشغيل المشهد الكوني", use_container_width=True):
        st.session_state.run = True
    if st.button("⏹️ إيقاف", use_container_width=True):
        st.session_state.run = False

# ═══════════════════════════════════════════════════════════════
# التبويبات
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌌 المشهد الكوني",
    "🌍 مختبر الأمم",
    "🧭 ميزانك الشخصي",
    "📐 هندسة الصراط",
    "📜 رسالة إلى البشرية"
])

# ═══════════════════════════════════════════════════════════════
# تبويب ١: المشهد الكوني
# ═══════════════════════════════════════════════════════════════
with tab1:
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init_cosmic' not in st.session_state: st.session_state.init_cosmic = False

    if not st.session_state.init_cosmic:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        sx = np.random.uniform(cx-13, cx+13, N_STARS)
        sy = np.random.uniform(cy-9, cy+9, N_STARS)
        sw = np.random.uniform(0.1, 1.0, N_STARS)
        sb = np.random.uniform(0.1, 1.0, N_STARS)
        star_W_hist = [deque([sw[i]], maxlen=50) for i in range(N_STARS)]
        star_B_hist = [deque([sb[i]], maxlen=50) for i in range(N_STARS)]
        W, B, E = W_init, B_init, 0.3
        S = calc_S(W, B, E, q_intensity)
        planet_W_hist = deque([W], maxlen=50); planet_B_hist = deque([B], maxlen=50)
        phase = "توازن"
        cycle_angle, angle_W, angle_B = 0.0, 0.0, np.pi*0.5
        eb = deque([S]*30, maxlen=30)
        pS, pE, px = deque(maxlen=400), deque(maxlen=400), deque(maxlen=400)
        frame_count, good_deeds, bad_deeds = 0, 10.0, 5.0
        st.session_state.update({
            'cx':cx,'cy':cy,'sx':sx,'sy':sy,'sw':sw,'sb':sb,
            'star_W_hist':star_W_hist,'star_B_hist':star_B_hist,
            'W':W,'B':B,'E':E,'S':S,'phase':phase,'cycle_angle':cycle_angle,
            'angle_W':angle_W,'angle_B':angle_B,'empowerment_buffer':eb,
            'history_S':pS,'history_E':pE,'history_x':px,'frame_count':frame_count,
            'planet_W_hist':planet_W_hist,'planet_B_hist':planet_B_hist,
            'good_deeds':good_deeds,'bad_deeds':bad_deeds,'init_cosmic':True
        })

    if st.session_state.get("run", False):
        placeholder = st.empty()
        while st.session_state.get("run", False):
            W=st.session_state.W; B=st.session_state.B; E=st.session_state.E; S=st.session_state.S
            phase=st.session_state.phase; cycle_angle=st.session_state.cycle_angle
            angle_W=st.session_state.angle_W; angle_B=st.session_state.angle_B
            sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
            sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
            star_W_hist=st.session_state.star_W_hist; star_B_hist=st.session_state.star_B_hist
            cx=st.session_state.cx; cy=st.session_state.cy; eb=st.session_state.empowerment_buffer
            pS=st.session_state.history_S; pE=st.session_state.history_E; px=st.session_state.history_x
            frame_count=st.session_state.frame_count
            planet_W_hist=st.session_state.planet_W_hist; planet_B_hist=st.session_state.planet_B_hist
            good_deeds=st.session_state.good_deeds; bad_deeds=st.session_state.bad_deeds

            cycle_angle += 0.008; sv = np.sin(cycle_angle)
            if sv>0.5: phase='ذروة'
            elif sv>0: phase='صعود'
            elif sv>-0.5: phase='انهيار'
            else: phase='قاع'
            if 0.3<sv<0.35: phase='>> استدراج <<'
            target_S = 0.5+0.45*sv

            for i in range(N_STARS):
                dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
                close = np.where((dist < 2.0) & (np.arange(N_STARS) != i))[0]
                sw[i] += (target_S - sw[i])*0.02 + np.random.uniform(-0.02,0.02)
                sb[i] += (target_S - sb[i])*0.02 + np.random.uniform(-0.02,0.02)
                if len(close) > 0:
                    sw[i] += (np.mean(sw[close])-sw[i])*0.03
                    sb[i] += (np.mean(sb[close])-sb[i])*0.03
                sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)
                star_W_hist[i].append(sw[i]); star_B_hist[i].append(sb[i])

            if random.random()<0.005:
                aff = np.random.choice(N_STARS, size=int(N_STARS*0.2), replace=False)
                sw[aff]*=np.random.uniform(0.5,0.8); sb[aff]*=np.random.uniform(0.5,0.8)

            avgW=np.mean(sw); avgB=np.mean(sb)
            W+=(avgW-W)*0.04; B+=(avgB-B)*0.04
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

            S = calc_S(W,B,E,q_intensity)
            eb.append(S)
            E_target = list(eb)[-lag_frames] if len(eb)>=lag_frames else S
            E += 0.03*(E_target-E)

            W = W - 0.015*E + 0.03/(S+0.1) - 0.007*(1-B)
            B = B - 0.012*E + 0.006*(1-B)*W*(1-W)
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
            S = calc_S(W,B,E,q_intensity)

            planet_W_hist.append(W); planet_B_hist.append(B)
            frame_count+=1
            if frame_count%2==0: pS.append(S); pE.append(E); px.append(len(px))

            angle_W+=0.02+random.uniform(-0.025,0.025)*(1-W)**2
            angle_B+=0.02+random.uniform(-0.025,0.025)*(1-B)**2
            wx=cx+(7-2.5*W)*np.cos(angle_W); wy=cy+(7-2.5*W)*np.sin(angle_W)*0.7
            bx=cx+(5-1.5*B)*np.cos(angle_B); by=cy+(5-1.5*B)*np.sin(angle_B)*0.7

            instability = 1-np.mean(sw*sb)
            sx+=np.random.uniform(-0.07,0.07,N_STARS)*instability
            sy+=np.random.uniform(-0.07,0.07,N_STARS)*instability
            sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)

            good_deeds += W*0.1; bad_deeds += (1-B)*0.1

            st.session_state.update({
                'W':W,'B':B,'E':E,'S':S,'phase':phase,'cycle_angle':cycle_angle,
                'angle_W':angle_W,'angle_B':angle_B,'empowerment_buffer':eb,
                'sx':sx,'sy':sy,'sw':sw,'sb':sb,
                'star_W_hist':star_W_hist,'star_B_hist':star_B_hist,
                'planet_W_hist':planet_W_hist,'planet_B_hist':planet_B_hist,
                'history_S':pS,'history_E':pE,'history_x':px,'frame_count':frame_count,
                'good_deeds':good_deeds,'bad_deeds':bad_deeds
            })

            fig, ax = plt.subplots(figsize=(14,10),facecolor='#000010')
            ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
            for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                          (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy),r*(0.5+2.8*S),color=c,alpha=a,zorder=15))
            ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
            halo_alpha = 0.25 * (1 - min(E, 1)) + 0.04
            ax.add_patch(Circle((cx,cy), 0.5+17*E, color='#00FFFF', alpha=halo_alpha, zorder=7))
            ax.add_patch(Circle((cx,cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2.5, zorder=2))
            ax.add_patch(Circle((wx,wy), 0.2+0.6*W, color='#FFFFFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx,by), 0.2+0.6*B, color='#FF3333', alpha=0.8, zorder=13))
            ax.text(wx, wy+0.8, 'W', color='#FFF', fontsize=10, ha='center')
            ax.text(bx, by+0.8, 'B', color='#F33', fontsize=10, ha='center')
            colors = [get_star_color(sw[i],sb[i]) for i in range(N_STARS)]
            ax.scatter(sx, sy, s=30, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)

            # الميزان الأخروي
            akh_x, akh_y, ms = 26.5, 18, 1.5
            ax.plot([akh_x, akh_x], [akh_y-3, akh_y+1.5], color='#FFD700', lw=1, alpha=0.4)
            ly = akh_y-1.5 + ms*min(good_deeds/50, 1.5)
            ry = akh_y-1.5 - ms*min(bad_deeds/50, 1.5)
            ax.add_patch(Circle((akh_x-1, ly), 0.6, color='#FFD700', alpha=0.3, zorder=20))
            ax.text(akh_x-1, ly-1, f'حسنات', color='#FFD700', fontsize=6, ha='center')
            ax.add_patch(Circle((akh_x+1, ry), 0.6, color='#FF4444', alpha=0.3, zorder=20))
            ax.text(akh_x+1, ry-1, f'سيئات', color='#FF4444', fontsize=6, ha='center')
            diff = (bad_deeds - good_deeds)/50*ms
            ax.plot([akh_x-1, akh_x+1], [akh_y-diff, akh_y+diff], color='#FFD700', lw=1.5, alpha=0.6)

            pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
            pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
            pax.set_title('S (الذهب) يقود E (السماوي) — الاستدراج', color='white', fontsize=7)
            pax.tick_params(colors='white', labelsize=4); pax.grid(True, alpha=0.12)
            if pS: 
                pax.plot(list(px), list(pS), color='#FFD700', lw=2)
                pax.plot(list(px), list(pE), color='#00FFFF', lw=1.5)

            ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f}', color='white', fontsize=11, ha='center')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.08)
        st.success("✅ توقفت المحاكاة")
    else:
        st.info("اضغط ▶️ تشغيل المشهد الكوني في لوحة القيادة")

# ═══════════════════════════════════════════════════════════════
# تبويب ٢: مختبر الأمم والحضارات
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.header("🌍 مختبر الأمم والحضارات")
    st.markdown("اضبط مولدات الطاقة وحدود البراءة، وشاهد كيف تنهض الحضارة أو تنهار عبر 300 عام.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🕌 مولدات الطاقة")
        civ_prayer = st.slider("الصلاة (تقوي W)", 0.0, 1.0, 0.7, 0.01, key="civ_prayer")
        civ_fasting = st.slider("الصوم (يقوي B)", 0.0, 1.0, 0.6, 0.01, key="civ_fasting")
        civ_zakat = st.slider("الزكاة (تقوي B)", 0.0, 1.0, 0.5, 0.01, key="civ_zakat")
        civ_hajj = st.slider("الحج (يقوي W)", 0.0, 1.0, 0.4, 0.01, key="civ_hajj")
    with col2:
        st.markdown("### 🛡️ حدود البراءة")
        civ_jihad_self = st.slider("جهاد النفس (يقوي B)", 0.0, 1.0, 0.8, 0.01, key="civ_jihad_self")
        civ_disavowal = st.slider("البراءة من الطاغوت (تقوي B)", 0.0, 1.0, 0.9, 0.01, key="civ_disavowal")
        civ_alliance = st.slider("موالاة المؤمنين (تقوي W)", 0.0, 1.0, 0.8, 0.01, key="civ_alliance")
        civ_sharia = st.slider("تحكيم الشرع (يقوي W و B)", 0.0, 1.0, 0.5, 0.01, key="civ_sharia")
    with col3:
        st.markdown("### ⚖️ أسس الحكم")
        civ_justice = st.slider("العدل", 0.0, 1.0, 0.6, 0.01, key="civ_justice")
        civ_shura = st.slider("الشورى", 0.0, 1.0, 0.5, 0.01, key="civ_shura")

    st.markdown("---")
    st.markdown("### 📜 سيناريوهات تاريخية")
    pcol = st.columns(4)
    if pcol[0].button("🏴 الخلافة الراشدة", use_container_width=True):
        civ_prayer=0.9; civ_fasting=0.8; civ_zakat=0.9; civ_hajj=0.7
        civ_jihad_self=0.9; civ_disavowal=0.9; civ_alliance=0.9; civ_sharia=0.9
        civ_justice=0.9; civ_shura=0.8
        st.rerun()
    if pcol[1].button("🏳️ العثمانيون 1800", use_container_width=True):
        civ_prayer=0.5; civ_fasting=0.4; civ_zakat=0.3; civ_hajj=0.3
        civ_jihad_self=0.4; civ_disavowal=0.3; civ_alliance=0.5; civ_sharia=0.4
        civ_justice=0.4; civ_shura=0.3
        st.rerun()
    if pcol[2].button("🔻 الاتحاد السوفيتي", use_container_width=True):
        civ_prayer=0.0; civ_fasting=0.0; civ_zakat=0.0; civ_hajj=0.0
        civ_jihad_self=0.0; civ_disavowal=0.0; civ_alliance=0.0; civ_sharia=0.0
        civ_justice=0.0; civ_shura=0.0
        st.rerun()
    if pcol[3].button("🕌 الأندلس قبل السقوط", use_container_width=True):
        civ_prayer=0.4; civ_fasting=0.3; civ_zakat=0.2; civ_hajj=0.2
        civ_jihad_self=0.2; civ_disavowal=0.2; civ_alliance=0.3; civ_sharia=0.3
        civ_justice=0.3; civ_shura=0.2
        st.rerun()

    st.markdown("---")
    if st.button("🚀 أطلق محاكاة الحضارة", use_container_width=True, type="primary"):
        W_civ = (civ_prayer + civ_hajj + civ_alliance + civ_sharia + civ_justice*0.5) / 4.5
        B_civ = (civ_fasting + civ_zakat + civ_jihad_self + civ_disavowal + civ_justice*0.5) / 4.5
        W_civ = np.clip(W_civ, 0.01, 1.0)
        B_civ = np.clip(B_civ, 0.01, 1.0)

        years = 300
        W_hist = np.zeros(years)
        B_hist = np.zeros(years)
        S_hist = np.zeros(years)
        E_hist = np.zeros(years)

        W_hist[0] = W_civ
        B_hist[0] = B_civ
        S_hist[0] = W_civ * B_civ
        E_hist[0] = 0.1

        for t in range(1, years):
            W_hist[t] = W_hist[t-1] - 0.01 * E_hist[t-1] + 0.01 * civ_prayer * civ_alliance
            B_hist[t] = B_hist[t-1] - 0.008 * E_hist[t-1] + 0.01 * civ_disavowal * civ_jihad_self
            W_hist[t] += 0.005 * civ_sharia
            B_hist[t] += 0.005 * civ_sharia
            W_hist[t] = np.clip(W_hist[t], 0.01, 1.0)
            B_hist[t] = np.clip(B_hist[t], 0.01, 1.0)
            S_hist[t] = W_hist[t] * B_hist[t]

            E_target = S_hist[max(0, t - lag_frames)]
            E_hist[t] = E_hist[t-1] + 0.03 * (E_target - E_hist[t-1])
            E_hist[t] = np.clip(E_hist[t], 0.01, 1.0)

        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#000010')
        
        ax1 = axes[0]
        ax1.set_facecolor('#0a0a2e')
        ax1.plot(S_hist, 'g-', lw=2.5, label='S (الثبات)')
        ax1.plot(E_hist, 'b--', lw=2.0, label='E (التمكين)')
        ax1.plot(W_hist, color='gold', lw=1.5, alpha=0.7, label='W (الولاء)')
        ax1.plot(B_hist, color='#FF5252', lw=1.5, alpha=0.7, label='B (البراءة)')
        idx_S_max = np.argmax(S_hist)
        idx_E_max = np.argmax(E_hist)
        if idx_S_max < idx_E_max:
            ax1.axvspan(idx_S_max, idx_E_max, alpha=0.2, color='red', label='فجوة الاستدراج')
        ax1.set_title('دورة الحضارة عبر ٣٠٠ عام', color='white', fontsize=14, fontweight='bold')
        ax1.set_xlabel('السنوات', color='white')
        ax1.set_ylabel('القيمة', color='white')
        ax1.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=9)
        ax1.grid(True, alpha=0.2)
        ax1.tick_params(colors='white')
        ax1.set_ylim(0, 1.05)

        ax2 = axes[1]
        ax2.set_facecolor('#0a0a2e')
        ax2.plot(B_hist, W_hist, 'w-', alpha=0.4, lw=0.8)
        ax2.scatter(B_hist[0], W_hist[0], s=150, c='green', edgecolors='white', linewidth=2, zorder=10, label='البداية')
        ax2.scatter(B_hist[-1], W_hist[-1], s=150, c='red', edgecolors='white', linewidth=2, zorder=10, label='النهاية')
        ax2.axhline(0.5, color='grey', ls=':', lw=1)
        ax2.axvline(0.5, color='grey', ls=':', lw=1)
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.set_xlabel('B (البراءة)', color='white')
        ax2.set_ylabel('W (الولاء)', color='white')
        ax2.set_title('مسار الحضارة في فضاء (W, B)', color='white', fontsize=14, fontweight='bold')
        ax2.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green')
        ax2.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='orange')
        ax2.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='blue')
        ax2.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='red')
        ax2.text(0.75, 0.75, 'مؤمن', color='green', fontsize=10, ha='center')
        ax2.text(0.25, 0.75, 'كافر', color='orange', fontsize=10, ha='center')
        ax2.text(0.25, 0.25, 'منافق', color='red', fontsize=10, ha='center')
        ax2.text(0.75, 0.25, 'مشرك', color='blue', fontsize=10, ha='center')
        ax2.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=9)
        ax2.grid(True, alpha=0.2)
        ax2.tick_params(colors='white')

        plt.tight_layout()
        st.pyplot(fig)

        st.divider()
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("W النهائي", f"{W_hist[-1]:.3f}")
        c2.metric("B النهائي", f"{B_hist[-1]:.3f}")
        c3.metric("S النهائي", f"{S_hist[-1]:.3f}")
        collapse_year = np.argmin(S_hist)
        status = "مستقر" if S_hist[collapse_year] >= 0.2 else f"عام {collapse_year}"
        c4.metric("عام الانهيار", status)
        istidraj_gap = max(0, np.argmax(E_hist) - np.argmax(S_hist))
        c5.metric("فجوة الاستدراج", f"{istidraj_gap} عام")

# ═══════════════════════════════════════════════════════════════
# تبويب ٣: ميزانك الشخصي
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.header("🧭 ميزانك الشخصي")
    st.markdown("أجب عن ١٢ سؤالاً بصدق لتكتشف موقعك في فضاء الولاء والبراءة.")
    
    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    questions = {
        "W": [
            ("حياتي كلها لله، لا أبتغي بها إلا وجهه", "My whole life is for Allah alone"),
            ("أقيم الصلاة بخشوع، أستشعر الوقوف بين يدي الله", "I pray with devotion"),
            ("أحب الله ورسوله أكثر من كل شيء", "I love Allah & Messenger most"),
            ("أتوكل على الله مع الأخذ بالأسباب", "I rely on Allah with means"),
            ("أشكر الله في الرخاء وأصبر في البلاء", "I thank and am patient"),
            ("أحمل هم الإسلام والمسلمين، وأسعى لنصرتهم", "I carry concerns of Islam"),
        ],
        "B": [
            ("آمر بالمعروف بالحكمة والموعظة الحسنة", "I enjoin good wisely"),
            ("أنكر المنكر بلساني أو قلبي", "I forbid evil"),
            ("أتبرأ من الشرك وأهله، وأعلن براءتي منهم", "I disavow polytheism"),
            ("أجاهد نفسي على ترك الكذب والغيبة والظلم", "I struggle against sins"),
            ("أرفض الظلم بكل صوره، ولا أرضاه لأحد", "I reject all injustice"),
            ("أحب في الله وأبغض في الله", "I love & hate for Allah"),
        ]
    }

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🤍 الولاء (W)")
        for i, (q_ar, q_en) in enumerate(questions["W"]):
            q = q_ar if LANG == "ar" else q_en
            ans = st.radio(q, ["نعم (+3)", "أحياناً (+1)", "لا (0)", "العكس (-1)"], key=f"w_{i}")
            if "نعم" in ans: st.session_state.compass_answers[f"W{i}"] = 3
            elif "أحياناً" in ans: st.session_state.compass_answers[f"W{i}"] = 1
            elif "لا" in ans: st.session_state.compass_answers[f"W{i}"] = 0
            else: st.session_state.compass_answers[f"W{i}"] = -1

    with col2:
        st.markdown("### ❤️ البراءة (B)")
        for i, (q_ar, q_en) in enumerate(questions["B"]):
            q = q_ar if LANG == "ar" else q_en
            ans = st.radio(q, ["نعم (+3)", "أحياناً (+1)", "لا (0)", "العكس (-1)"], key=f"b_{i}")
            if "نعم" in ans: st.session_state.compass_answers[f"B{i}"] = 3
            elif "أحياناً" in ans: st.session_state.compass_answers[f"B{i}"] = 1
            elif "لا" in ans: st.session_state.compass_answers[f"B{i}"] = 0
            else: st.session_state.compass_answers[f"B{i}"] = -1

    if len(st.session_state.compass_answers) == 12:
        W_raw = sum(st.session_state.compass_answers[f"W{i}"] for i in range(6))
        B_raw = sum(st.session_state.compass_answers[f"B{i}"] for i in range(6))
        W_val = np.clip(W_raw / 18.0, -1, 1)
        B_val = np.clip(B_raw / 18.0, -1, 1)
        W_norm = (W_val + 1) / 2
        B_norm = (B_val + 1) / 2
        S_val = W_norm * B_norm
        
        name, color = classify_quadrant(W_norm, B_norm)

        st.divider()
        st.header("📊 نتيجتك")
        c1, c2, c3 = st.columns(3)
        c1.metric("W (الولاء)", f"{W_val:.2f}")
        c2.metric("B (البراءة)", f"{B_val:.2f}")
        c3.metric("S (الثبات)", f"{S_val:.2f}")
        st.markdown(f"<h2 style='color:{color}; text-align:center;'>{name}</h2>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5)
        ax.axvline(0, color='grey', lw=0.5)
        ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.1", color='#FFD700', alpha=0.15))
        ax.add_patch(FancyBboxPatch((-1, 0), 1, 1, boxstyle="round,pad=0.1", color='#FF5252', alpha=0.15))
        ax.add_patch(FancyBboxPatch((-1, -1), 1, 1, boxstyle="round,pad=0.1", color='#FFB6C1', alpha=0.15))
        ax.add_patch(FancyBboxPatch((0, -1), 1, 1, boxstyle="round,pad=0.1", color='#FFA500', alpha=0.15))
        ax.text(0.5, 0.5, "مؤمن", ha='center', color='white', alpha=0.6)
        ax.text(-0.5, 0.5, "كافر", ha='center', color='white', alpha=0.6)
        ax.text(-0.5, -0.5, "منافق", ha='center', color='white', alpha=0.6)
        ax.text(0.5, -0.5, "مشرك", ha='center', color='white', alpha=0.6)
        ax.scatter(B_val, W_val, s=250, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
        ax.set_xlabel("B (البراءة)", color='white')
        ax.set_ylabel("W (الولاء)", color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)

        if st.button("🔄 أعد الميزان", use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# تبويب ٤: هندسة الصراط
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.header("📐 مختبر هندسة الصراط")
    st.markdown("المسار يتحرك. الصراط المستقيم (κ=0) هو مسار إبراهيم.")
    
    if 'path_W' not in st.session_state:
        st.session_state.path_W = [0.5]
        st.session_state.path_B = [0.5]
        st.session_state.path_kappa = [0.0]

    c1, c2, c3 = st.columns(3)
    with c1:
        sin_strength = st.slider("⚡ شدة المعصية", 0.0, 0.1, 0.02, 0.005, key="sin_str")
    with c2:
        repentance_sincerity = st.slider("💧 صدق التوبة", 0.0, 1.0, 0.8, 0.05, key="sinc")
    with c3:
        if st.button("🕌 توبة", use_container_width=True):
            cW = st.session_state.path_W[-1]
            cB = st.session_state.path_B[-1]
            st.session_state.path_W.append(np.clip(cW + (1.0-cW)*repentance_sincerity, 0.0, 1.0))
            st.session_state.path_B.append(np.clip(cB + (1.0-cB)*repentance_sincerity, 0.0, 1.0))
            st.session_state.path_kappa.append(0.0)
            st.rerun()

    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("▶️ خطوة", use_container_width=True):
            cW = st.session_state.path_W[-1]
            cB = st.session_state.path_B[-1]
            nW = cW - sin_strength*(cW-0.2) + np.random.uniform(-0.01, 0.01)
            nB = cB - sin_strength*(cB-0.2) + np.random.uniform(-0.01, 0.01)
            st.session_state.path_W.append(np.clip(nW, 0.05, 1.0))
            st.session_state.path_B.append(np.clip(nB, 0.05, 1.0))
            kappa = compute_curvature(st.session_state.path_W, st.session_state.path_B) if len(st.session_state.path_W) >= 3 else 0.0
            st.session_state.path_kappa.append(kappa)
            st.rerun()
    with btn2:
        if st.button("🔄 إعادة", use_container_width=True):
            st.session_state.path_W = [0.5]
            st.session_state.path_B = [0.5]
            st.session_state.path_kappa = [0.0]
            st.rerun()

    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#000010')
    
    ax1 = axes[0]
    ax1.set_facecolor('#0a0a2e')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xlabel("B", color='white')
    ax1.set_ylabel("W", color='white')
    ax1.set_title("مسارك في فضاء (W, B)", color='white', fontsize=13)
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=2.5, alpha=0.7, label="الصراط (إبراهيم عليه السلام)")
    ax1.scatter([1], [1], s=150, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, label="الكمال (1,1)")

    pW = st.session_state.path_W
    pB = st.session_state.path_B
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.path_kappa[i] if i < len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2 if kv < 0.05 else 3)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label="البداية")
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label="الآن")
    
    ax1.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2)
    ax1.tick_params(colors='white')

    ax2 = axes[1]
    ax2.set_facecolor('#0a0a2e')
    ax2.plot(st.session_state.path_kappa, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label="حد الخطر (0.05)")
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label="الصراط (0.0)")
    ax2.set_xlabel("الخطوات", color='white')
    ax2.set_ylabel("κ (الانحناء)", color='white')
    ax2.set_title("منحنى الانحناء", color='white', fontsize=13)
    ax2.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.2)
    ax2.tick_params(colors='white')
    ax2.set_ylim(-0.01, max(0.2, max(st.session_state.path_kappa)*1.2 if st.session_state.path_kappa else 0.1))
    
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("W", f"{pW[-1]:.3f}")
    c2.metric("B", f"{pB[-1]:.3f}")
    c3.metric("κ", f"{st.session_state.path_kappa[-1]:.4f}")
    on_path = st.session_state.path_kappa[-1] < 0.03
    c4.metric("الصراط؟", "✅ نعم" if on_path else "⚠️ لا")

# ═══════════════════════════════════════════════════════════════
# تبويب ٥: رسالة إلى البشرية
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.header("📜 رسالة إلى البشرية")
    st.markdown("""
    <div style="text-align:center;font-size:1.1em;line-height:2.2;color:#CCC;">
    
    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟"
    > <br>
    > هذا هو مختبر الميزان الذي يثبت أن <b style="color:#FFD700;">S = W × B</b>
    
    <br><br>
    
    إنه القانون الواحد الذي فطر الله السماوات والأرض عليه.
    من الذرة إلى المجرة، ومن الفرد إلى الحضارة، ومن الدنيا إلى الآخرة،
    كل شيء يسير بهذا الميزان.
    
    <br><br>
    
    <b style="color:#FFD700;">
    ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾
    <br>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    </b>
    
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# التذييل
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align:center; color: #888; font-size: 0.9em;">
    ⚖️ S = W × B &nbsp;|&nbsp; ق = الحق = الميزان &nbsp;|&nbsp; © 2026 علي عادل العاطفي
</div>
""", unsafe_allow_html=True)
