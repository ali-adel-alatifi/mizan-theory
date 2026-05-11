import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="S = W × B", page_icon="⚖️", layout="wide")

# اللغة
if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

# نسق الصفحة
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Cairo:wght@400;700;900&display=swap');
    .stApp {{ background: radial-gradient(ellipse at 50% 50%, #0a0a1a 0%, #020108 100%); }}
    .golden-text {{ font-family: 'Amiri Quran', 'Cairo', serif; font-size: 5em; font-weight: 900; text-align: center; 
                    background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 40%, #B8860B 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }}
    .arabic {{ font-family: 'Cairo', sans-serif; direction: rtl; }}
    .stButton > button {{ background: none; border: 2px solid #FFD700; color: #FFD700; border-radius: 50px; 
                        padding: 15px 30px; font-size: 1.2em; font-weight: bold; transition: all 0.5s; }}
    .stButton > button:hover {{ background: #FFD700; color: #000; box-shadow: 0 0 30px gold; }}
</style>
""", unsafe_allow_html=True)

# دوال
def star_color(w, b):
    if w > 0.55 and b > 0.55: return '#FFD700'
    if w < 0.45 and b < 0.45: return '#FF69B4'
    if w < 0.45 and b > 0.55: return '#FF4500'
    if w > 0.55 and b < 0.45: return '#E0E0E0'
    return '#888'

def curve(W, B):
    if len(W) < 3: return 0
    dW = np.gradient(W); dB = np.gradient(B)
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return num / denom

# حالة الجلسة
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state:
    np.random.seed(42); random.seed(42)
    N = 250
    cx, cy = 14, 10.0
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-13, cx+13, N)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, N)
    st.session_state.sw = np.random.uniform(0.1, 1.0, N)
    st.session_state.sb = np.random.uniform(0.1, 1.0, N)
    st.session_state.W = 0.55; st.session_state.B = 0.52; st.session_state.E = 0.3
    st.session_state.S = 0.55 * 0.52
    st.session_state.pW = deque([0.55], maxlen=50); st.session_state.pB = deque([0.52], maxlen=50)
    st.session_state.hS = deque(maxlen=400); st.session_state.hE = deque(maxlen=400); st.session_state.hx = deque(maxlen=400)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0
    st.session_state.frame = 0; st.session_state.init = True

# العنوان
st.markdown('<h1 class="golden-text">⚖️ ميزان</h1>', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; margin-top:-30px; margin-bottom:30px;">
    <p style="color:#AAA; font-family:'Cairo'; font-size:1.3em; direction:rtl;">{T('القانون الواحد من الذرة إلى الحضارة', 'The One Law, from Atom to Civilization')}</p>
    <p style="color:#888; font-size:1em; direction:rtl;">{T('﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾', '﴿Whoever rejects false gods and believes in Allah has grasped the firm handhold﴾')}</p>
</div>
""", unsafe_allow_html=True)

# أزرار التحكم - صف واحد أنيق
c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])
with c1:
    if st.button("▶️ نشاهد", use_container_width=True): st.session_state.run = True
with c2:
    if st.button("⏸️ نتأمل", use_container_width=True): st.session_state.run = False
with c3:
    lag = st.select_slider(T("فجوة الاستدراج", "Istidraj Gap"), options=[5, 10, 15, 22, 30, 40, 50], value=22)
with c4:
    if st.button("🕌 توبة", use_container_width=True):
        Wc = st.session_state.W; Bc = st.session_state.B
        st.session_state.W = min(1.0, Wc + 0.2)
        st.session_state.B = min(1.0, Bc + 0.2)
        st.session_state.good += 5
with c5:
    lang_btn = st.button("En" if L == "ar" else "عربي", use_container_width=True)
    if lang_btn: st.session_state.lang = "en" if L == "ar" else "ar"; st.rerun()

# المشهد الحي
placeholder = st.empty()

if st.session_state.run:
    while st.session_state.run:
        W = st.session_state.W; B = st.session_state.B; E = st.session_state.E; S = st.session_state.S
        phase = st.session_state.phase; ca = st.session_state.ca
        aW = st.session_state.aW; aB = st.session_state.aB
        sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
        sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
        cx = st.session_state.cx; cy = st.session_state.cy
        eb = st.session_state.eb; pW = st.session_state.pW; pB = st.session_state.pB
        hS = st.session_state.hS; hE = st.session_state.hE; hx = st.session_state.hx
        frame = st.session_state.frame
        good = st.session_state.good; bad = st.session_state.bad

        ca += 0.008; sv = np.sin(ca)
        if sv > 0.5: phase = "ذروة"
        elif sv > 0: phase = "صعود"
        elif sv > -0.5: phase = "انهيار"
        else: phase = "قاع"
        if 0.3 < sv < 0.35: phase = "! استدراج"
        target = 0.5 + 0.45 * sv

        N = len(sw)
        for i in range(N):
            dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
            nbr = np.where((dist < 2.0) & (np.arange(N) != i))[0]
            sw[i] += (target - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
            sb[i] += (target - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
            if len(nbr) > 0:
                sw[i] += (np.mean(sw[nbr]) - sw[i]) * 0.03
                sb[i] += (np.mean(sb[nbr]) - sb[i]) * 0.03
            sw[i] = np.clip(sw[i], 0.01, 1.0)
            sb[i] = np.clip(sb[i], 0.01, 1.0)

        if random.random() < 0.005:
            aff = np.random.choice(N, size=int(N*0.2), replace=False)
            sw[aff] *= random.uniform(0.5, 0.8)
            sb[aff] *= random.uniform(0.5, 0.8)

        W += (np.mean(sw) - W) * 0.04
        B += (np.mean(sb) - B) * 0.04
        W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)

        S = np.clip(W * B, 0.001, 1.0)
        eb.append(S)
        past = list(eb)[-lag] if len(eb) >= lag else S
        E += 0.03 * (past - E)

        W = W - 0.015*E + 0.03/(S+0.1) - 0.007*(1-B)
        B = B - 0.012*E + 0.006*(1-B)*W*(1-W)
        W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
        S = np.clip(W * B, 0.001, 1.0)

        pW.append(W); pB.append(B)
        frame += 1
        if frame % 2 == 0:
            hS.append(S); hE.append(E); hx.append(len(hx))

        aW += 0.02 + random.uniform(-0.02, 0.02)*(1-W)**2
        aB += 0.02 + random.uniform(-0.02, 0.02)*(1-B)**2
        wx = cx + (7-2.5*W)*np.cos(aW); wy = cy + (7-2.5*W)*np.sin(aW)*0.7
        bx = cx + (5-1.5*B)*np.cos(aB); by = cy + (5-1.5*B)*np.sin(aB)*0.7

        instability = 1 - np.mean(sw*sb)
        sx += np.random.uniform(-0.07, 0.07, N) * instability
        sy += np.random.uniform(-0.07, 0.07, N) * instability
        sx = np.clip(sx, cx-13, cx+13); sy = np.clip(sy, cy-9, cy+9)

        good += W * 0.1; bad += (1-B) * 0.1

        st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
        st.session_state.phase=phase; st.session_state.ca=ca
        st.session_state.aW=aW; st.session_state.aB=aB; st.session_state.eb=eb
        st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
        st.session_state.pW=pW; st.session_state.pB=pB
        st.session_state.hS=hS; st.session_state.hE=hE; st.session_state.hx=hx; st.session_state.frame=frame
        st.session_state.good=good; st.session_state.bad=bad

        # الرسم
        fig, ax = plt.subplots(figsize=(16, 11), facecolor='#030310')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        
        for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                        (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
            ax.add_patch(plt.Circle((cx, cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
        ax.text(cx, cy, 'ﷲ', color='#1a1000', fontsize=12, ha='center', va='center', fontweight='bold', fontfamily='Amiri Quran')
        ax.add_patch(plt.Circle((cx, cy), 0.5+17*E, color='#00FFFF', alpha=0.2*(1-min(E,1))+0.03, zorder=7))
        ax.add_patch(plt.Circle((cx, cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2.5, zorder=2))
        ax.add_patch(plt.Circle((wx, wy), 0.2+0.6*W, color='#FFF', alpha=1, zorder=13))
        ax.add_patch(plt.Circle((bx, by), 0.2+0.6*B, color='#FF3333', alpha=0.8, zorder=13))
        ax.text(wx, wy+0.8, 'W', color='#FFF', fontsize=10, ha='center')
        ax.text(bx, by+0.8, 'B', color='#F33', fontsize=10, ha='center')
        
        colors = [star_color(sw[i], sb[i]) for i in range(N)]
        ax.scatter(sx, sy, s=30, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)

        # الميزان الأخروي
        ax.plot([26.5, 26.5], [15, 19.5], color='#FFD700', lw=1, alpha=0.4)
        gY = 16 + min(good/50, 2); bY = 16 - min(bad/50, 2)
        ax.add_patch(plt.Circle((25.5, gY), 0.5, color='#FFD700', alpha=0.3, zorder=20))
        ax.text(25.5, gY-1, f'حسنات', color='#FFD700', fontsize=6, ha='center')
        ax.add_patch(plt.Circle((27.5, bY), 0.5, color='#FF4444', alpha=0.3, zorder=20))
        ax.text(27.5, bY-1, f'سيئات', color='#FF4444', fontsize=6, ha='center')
        ax.plot([25.5, 27.5], [gY, bY], color='#FFD700', lw=1.5, alpha=0.6)

        # منحنى الاستدراج
        pax = ax.inset_axes([0.5, 0.01, 0.47, 0.14])
        pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
        pax.set_title(f"S (الذهب) يقود E (السماوي)", color='white', fontsize=7)
        pax.tick_params(colors='white', labelsize=4); pax.grid(True, alpha=0.12)
        if hS: pax.plot(list(hx), list(hS), color='#FFD700', lw=2); pax.plot(list(hx), list(hE), color='#00FFFF', lw=1.5)

        # لوحة المعلومات السفلية
        ax.text(14, 1.5, f'{phase}  |  W={W:.2f}  |  B={B:.2f}  |  S={S:.2f}  |  E={E:.2f}  |  κ={curve(list(pW), list(pB)):.3f}',
                color='white', fontsize=11, ha='center', fontweight='bold',
                bbox=dict(facecolor='#0a0a2e', edgecolor='#FFD700', boxstyle='round,pad=0.5', alpha=0.7))

        plt.tight_layout(pad=0)
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.08)

# عرض آخر إطار عند التوقف
elif st.session_state.init:
    W = st.session_state.W; B = st.session_state.B; E = st.session_state.E; S = st.session_state.S
    N = len(st.session_state.sw)
    fig, ax = plt.subplots(figsize=(16, 11), facecolor='#030310')
    ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
    cx = st.session_state.cx; cy = st.session_state.cy
    for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                    (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
        ax.add_patch(plt.Circle((cx, cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
    ax.text(cx, cy, 'ﷲ', color='#1a1000', fontsize=12, ha='center', va='center', fontweight='bold', fontfamily='Amiri Quran')
    ax.add_patch(plt.Circle((cx, cy), 0.5+17*E, color='#00FFFF', alpha=0.2*(1-min(E,1))+0.03, zorder=7))
    ax.add_patch(plt.Circle((cx, cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2.5, zorder=2))
    colors = [star_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(N)]
    ax.scatter(st.session_state.sx, st.session_state.sy, s=30, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)
    ax.text(14, 1.5, T('انقر "نشاهد" لرؤية القانون الحي', 'Click "Watch" to see the living law'),
            color='white', fontsize=14, ha='center', fontweight='bold')
    plt.tight_layout(pad=0)
    placeholder.pyplot(fig)
    plt.close(fig)

# تذييل
st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#666;'>⚖️ S = W × B | ق = ١٠٠ = الحق = الميزان | علي عادل العاطفي | ٢٠٢٦</p>", unsafe_allow_html=True)
