# =============================================
# ⚖️ AL-DEEN AL-QAYYIM – THE COSMIC BALANCE LAW
# S = W × B | W = الولاء | B = البراءة
# © 2026 Ali Adel Alatifi | All rights reserved.
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

st.set_page_config(page_title="الدين القيم", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# --- CSS ---
st.markdown("<style> .stApp { background: #000010; } .gold { color: #FFD700; text-align: center; } .stButton>button { border: 1px solid #FFD700; color: #FFD700; background: #111; } </style>", unsafe_allow_html=True)

st.markdown("<h1 class='gold'>⚖️ الدِّينُ الْقَيِّم ⚖️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ccc;'>S = W × B | قانون التوازن الكوني</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#FFD700;'>© 2026 Ali Adel Alatifi</p>", unsafe_allow_html=True)

with st.expander("📜 رسالة الترحيب", expanded=False):
    st.markdown("> \"هل يوجد قانون واحد يحكم الذرة والحضارة؟ S = W × B\"")
    st.markdown("الدين القيم = قانون السببية الكوني. © Ali Adel Alatifi")

# --- Sidebar ---
with st.sidebar:
    st.header("🎛️ لوحة التحكم")
    prayer = st.slider("الصلاة 🟣", 0.0, 1.0, 0.8, 0.01)
    zakat = st.slider("الزكاة 🟡", 0.0, 1.0, 0.6, 0.01)
    fasting = st.slider("الصوم 🟠", 0.0, 1.0, 0.7, 0.01)
    hajj = st.slider("الحج 🔵", 0.0, 1.0, 0.5, 0.01)
    amr = st.slider("الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01)
    nahy = st.slider("النهي عن المنكر", 0.0, 1.0, 0.5, 0.01)
    adl = st.slider("العدل ⚖️", 0.0, 1.0, 0.6, 0.01)
    shura = st.slider("الشورى 🤝", 0.0, 1.0, 0.5, 0.01)
    taawun_birr = st.slider("التعاون على البر", 0.0, 1.0, 0.5, 0.01)
    taawun_taqwa = st.slider("التعاون على التقوى", 0.0, 1.0, 0.5, 0.01)
    tawasi_haqq = st.slider("التواصي بالحق", 0.0, 1.0, 0.5, 0.01)
    tawasi_sabr = st.slider("التواصي بالصبر", 0.0, 1.0, 0.5, 0.01)
    nahy_marouf_e = st.slider("النهي عن المعروف (إفساد)", 0.0, 1.0, 0.2, 0.01)
    amr_munkar_e = st.slider("الأمر بالمنكر (إفساد)", 0.0, 1.0, 0.2, 0.01)
    taawun_ithm = st.slider("التعاون على الإثم", 0.0, 1.0, 0.2, 0.01)
    taawun_udwan = st.slider("التعاون على العدوان", 0.0, 1.0, 0.2, 0.01)
    tawasi_batil = st.slider("التواصي بالباطل", 0.0, 1.0, 0.2, 0.01)
    adam_sabr = st.slider("عدم الصبر", 0.0, 1.0, 0.2, 0.01)
    riba = st.slider("الربا 💸", 0.0, 1.0, 0.2, 0.01)
    ghish = st.slider("الغش 🎭", 0.0, 1.0, 0.2, 0.01)
    kadhib = st.slider("الكذب 🤥", 0.0, 1.0, 0.2, 0.01)
    cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.01, 0.001)
    delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1)
    N_STARS = st.slider("عدد النجوم", 100, 600, 300, 50)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("▶️ تشغيل"): st.session_state.run = True
    if c2.button("⏹️ إيقاف"): st.session_state.run = False
    if c3.button("🔄 إعادة"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- Helper Functions ---
def get_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#FFFFFF'
    elif w < 0.45 and b >= 0.55: return '#FF3333'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    return '#FFF8DC' if w > b else '#FFA07A'

def calc_S(W, B, E, p, z, f, h, amr, nahy, adl, shura, riba, ghish, kadhib):
    Sb = W * B
    pillars = (p + z + f + h) / 4
    Sb *= (0.5 + 0.5 * pillars)
    prot = (amr * W + nahy * B) / 2
    Sb *= (0.8 + 0.4 * prot) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    if E > Sb: Sb -= riba * (E - Sb) * 0.3
    return np.clip(Sb, 0.001, 1.0)

# --- Init ---
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False

if not st.session_state.init:
    np.random.seed(42); random.seed(42)
    cx, cy = 14, 10.0
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-13, cx+13, N_STARS)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, N_STARS)
    st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.W = 0.55; st.session_state.B = 0.52
    st.session_state.E = 0.3; st.session_state.S = 0.286
    st.session_state.ph = "Balance"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5
    st.session_state.eb = [0.286]*30
    st.session_state.pS = []; st.session_state.pE = []; st.session_state.px = []
    st.session_state.pc = 0
    st.session_state.init = True

plot_placeholder = st.empty()

# --- Simulation ---
if st.session_state.get("run", False):
    while st.session_state.run:
        W = st.session_state.W; B = st.session_state.B; E = st.session_state.E; S = st.session_state.S
        ph = st.session_state.ph; ca = st.session_state.ca
        aW = st.session_state.aW; aB = st.session_state.aB
        sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
        sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
        cx, cy = st.session_state.cx, st.session_state.cy
        eb = st.session_state.eb; pS = st.session_state.pS; pE = st.session_state.pE; px = st.session_state.px

        ca += cycle_speed; sv = np.sin(ca)
        target_S = 0.5 + 0.45 * sv
        if sv > 0.5: ph = 'استقرار تام'
        elif sv > 0: ph = 'صعود'
        elif sv > -0.5: ph = 'انهيار'
        else: ph = 'قاع'
        if 0.3 < sv < 0.35: ph = '>> استدراج <<'

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
            sw[aff] *= random.uniform(0.5, 0.8); sb[aff] *= random.uniform(0.5, 0.8)

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
        if len(px) > 400: pS.pop(0); pE.pop(0); px.pop(0)

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
        st.session_state.aW, st.session_state.aB = aW, aB
        st.session_state.sx, st.session_state.sy = sx, sy
        st.session_state.sw, st.session_state.sb = sw, sb
        st.session_state.pS, st.session_state.pE, st.session_state.px = pS, pE, px

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
        pSl, pEl, pxl = list(pS), list(pE), list(px)
        if pSl:
            pax = ax.inset_axes([0.4, 0.02, 0.55, 0.12])
            pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
            pax.plot(pxl, pSl, color='#FFD700', lw=2); pax.plot(pxl, pEl, color='#00FFFF', lw=1.5)
        ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, ha='center')
        plt.tight_layout(pad=0)
        plot_placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.08)
    st.success("⏸️ تم الإيقاف")
elif st.session_state.init:
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#000010')
    ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
    colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
    ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9)
    ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
    plot_placeholder.pyplot(fig)
    plt.close(fig)

st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;'>© 2026 Ali Adel Alatifi | Al-Deen Al-Qayyim</p>", unsafe_allow_html=True)
