import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import time
from collections import deque

st.set_page_config(page_title="المشهد الكوني", page_icon="⚖️", layout="wide")

# --- التصميم ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at center, #0a0a2e 0%, #000010 100%); }
    .golden-title {
        font-size: 2.5em; font-weight: 900; text-align: center; margin: 10px 0 0 0;
        background: linear-gradient(180deg, #FFE566 0%, #FFD700 40%, #DAA520 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stButton > button {
        border-radius: 10px; font-weight: bold; height: 2.6em;
        background: #1a1a3e; color: #FFD700; border: 1.5px solid #DAA520;
    }
    .metric-card {
        background: rgba(10,10,46,0.8); border-radius: 12px; padding: 10px 5px;
        text-align: center; border: 1px solid rgba(218,165,32,0.3);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="golden-title">⚖️ الدِّينُ الْقَيِّم ⚖️</p>', unsafe_allow_html=True)
st.caption("S = W × B | قانون التوازن الكوني")

# --- تهيئة الحالة الافتراضية ---
defaults = {
    'prayer': 0.8, 'zakat': 0.6, 'fasting': 0.7, 'hajj': 0.5,
    'amr': 0.5, 'nahy': 0.5, 'adl': 0.6, 'shura': 0.5,
    'taawun_birr': 0.5, 'taawun_taqwa': 0.5, 'tawasi_haqq': 0.5, 'tawasi_sabr': 0.5,
    'nahy_marouf_e': 0.2, 'amr_munkar_e': 0.2, 'taawun_ithm': 0.2, 'taawun_udwan': 0.2,
    'tawasi_batil': 0.2, 'adam_sabr': 0.2, 'riba': 0.2, 'ghish': 0.2, 'kadhib': 0.2,
    'cycle_speed': 0.008, 'delay_frames': 22, 'N_STARS': 150
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False

# --- أزرار ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("▶️ تشغيل", use_container_width=True): st.session_state.run = True
with c2:
    if st.button("⏹️ إيقاف", use_container_width=True): st.session_state.run = False
with c3:
    if st.button("🔄 إعادة", use_container_width=True):
        st.session_state.init = False
        st.session_state.run = False
        st.rerun()

# --- دوال ---
def get_color(w, b):
    if w >= 0.7 and b >= 0.7: return '#FFD700'
    if w >= 0.55 and b < 0.45: return '#E0E0E0'
    if w < 0.45 and b >= 0.55: return '#FF5252'
    if w < 0.45 and b < 0.45: return '#FF8A80'
    return '#FFF9C4' if w > b else '#FFCCBC'

def calc_S(W, B, E, p, z, f, h, amr, nahy, adl, shura, riba, ghish, kadhib):
    Sb = W * B
    pb = (p + z + f + h) / 4
    Sb *= (0.5 + 0.5 * pb)
    pr = (amr * W + nahy * B) / 2
    Sb *= (0.8 + 0.4 * pr) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    if E > Sb: Sb -= riba * (E - Sb) * 0.3
    return np.clip(Sb, 0.001, 1.0)

# --- تهيئة المحاكاة ---
if not st.session_state.init:
    np.random.seed(42)
    n = st.session_state.N_STARS
    cx, cy = 14, 10
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

# --- مؤشرات ---
if st.session_state.init:
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><h2 style="color:#FFD700;">{st.session_state.S:.3f}</h2><small>⚖️ S</small></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><h2 style="color:#FFF;">{st.session_state.W:.3f}</h2><small>🤍 W</small></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><h2 style="color:#FF5252;">{st.session_state.B:.3f}</h2><small>❤️ B</small></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><h2 style="color:#00FFFF;">{st.session_state.E:.3f}</h2><small>💫 E</small></div>', unsafe_allow_html=True)

plot_placeholder = st.empty()

# --- المحاكاة ---
if st.session_state.run:
    while st.session_state.run:
        params = {k: st.session_state[k] for k in defaults}
        W, B, E = st.session_state.W, st.session_state.B, st.session_state.E
        S, ph, ca = st.session_state.S, st.session_state.ph, st.session_state.ca
        aW, aB, aa = st.session_state.aW, st.session_state.aB, st.session_state.aa
        sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
        sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
        cx, cy = st.session_state.cx, st.session_state.cy
        eb = st.session_state.eb
        pS, pE, px, pc = st.session_state.pS, st.session_state.pE, st.session_state.px, st.session_state.pc

        ca += params['cycle_speed']; sv = np.sin(ca)
        target_S = 0.5 + 0.45 * sv
        if sv > 0.5: ph = 'استقرار تام'
        elif sv > 0: ph = 'صعود'
        elif sv > -0.5: ph = 'انهيار'
        else: ph = 'قاع'
        if 0.3 < sv < 0.35: ph = '>> استدراج <<'
        if -0.35 < sv < -0.3: ph = '>> تعافي <<'

        n = len(sw)
        for i in range(n):
            wb = params['prayer'] * 0.01; bb = params['fasting'] * 0.01
            dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
            close = (dist < 2.0) & (np.arange(n) != i)
            sw[i] += params['amr'] * 0.015; sb[i] += params['nahy'] * 0.015
            sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + wb
            sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + bb
            if np.any(close):
                sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03 * (0.5 + 0.5 * params['shura'])
                sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03 * (0.5 + 0.5 * params['shura'])
            sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

        shock_p = 0.005 * (1 - params['adl'] * 0.8)
        if np.random.random() < shock_p:
            aff = np.random.choice(n, size=int(n * 0.3), replace=False)
            sw[aff] *= np.random.uniform(0.5, 0.8); sb[aff] *= np.random.uniform(0.5, 0.8)

        avgW = np.mean(sw); avgB = np.mean(sb)
        W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
        W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
        S = calc_S(W, B, E, params['prayer'], params['zakat'], params['fasting'], params['hajj'],
                   params['amr'], params['nahy'], params['adl'], params['shura'],
                   params['riba'], params['ghish'], params['kadhib'])
        eb.append(S)
        eff = int(params['delay_frames'] * (1 + params['ghish'] * 0.5))
        Et = list(eb)[-min(eff, len(eb))] if len(eb) >= eff else S
        E += 0.03 * (Et - E)
        W = W - 0.01 * E + 0.02 / (S + 0.1)
        B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
        W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
        S = calc_S(W, B, E, params['prayer'], params['zakat'], params['fasting'], params['hajj'],
                   params['amr'], params['nahy'], params['adl'], params['shura'],
                   params['riba'], params['ghish'], params['kadhib'])
        pc += 1
        if pc % 2 == 0:
            pS.append(S); pE.append(E); px.append(len(px))

        aW += 0.02 + np.random.uniform(-0.025, 0.025) * (1 - W)**2
        aB += 0.02 + np.random.uniform(-0.025, 0.025) * (1 - B)**2
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

        fig, ax = plt.subplots(figsize=(10, 7), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        for r, a, c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),(2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
            ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
        ax.text(cx, cy, 'S', color='#1a1000', fontsize=22, ha='center', va='center', fontweight='bold')
        ax.add_patch(Circle((cx,cy), 0.5+13*E, color='#00FFFF', alpha=0.15, zorder=7))
        ax.add_patch(Circle((cx,cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2, zorder=2))
        colors = [get_color(sw[i], sb[i]) for i in range(n)]
        ax.scatter(sx, sy, s=45, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)
        pSl, pEl, pxl = list(pS), list(pE), list(px)
        if pSl:
            pax = ax.inset_axes([0.4, 0.02, 0.55, 0.15])
            pax.set_xlim(0, max(400, len(pxl))); pax.set_ylim(0, 1.05)
            pax.set_title('S يقود E', color='white', fontsize=8)
            pax.plot(pxl, pSl, color='#FFD700', lw=2, label='S')
            pax.plot(pxl, pEl, color='#00FFFF', lw=1.5, label='E')
            pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=6)
        ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, ha='center')
        plt.tight_layout(pad=0)
        plot_placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.08)
    st.success("⏸️ تم الإيقاف")
else:
    if st.session_state.init:
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9)
        ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
        st.pyplot(fig)
