# =============================================
# ⚖️ AL-DEEN AL-QAYYIM – THE COSMIC BALANCE LAW
# S = W × B | W = الولاء (Allegiance) | B = البراءة (Disavowal)
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

st.set_page_config(page_title="المختبر الحي – الميزان", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

# =============================================
# 🎨 CSS
# =============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); }
    .stButton > button { border: 1px solid #FFD700; color: #FFD700; background: #1a1a3e; border-radius: 8px; height: 2.5em; }
    .metric-box { background: rgba(10,10,46,0.8); border-radius: 10px; padding: 8px 5px; text-align: center; border: 1px solid rgba(218,165,32,0.3); }
    .metric-val { font-size: 1.6em; font-weight: bold; margin: 0; }
    .metric-lbl { font-size: 0.7em; color: #aaa; margin: 0; }
    [data-testid="stExpander"] details { background: rgba(10,10,40,0.5); border: 1px solid rgba(218,165,32,0.3); border-radius: 8px; }
    [data-testid="stExpander"] summary { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ العنوان
# =============================================
st.title("🌌 المختبر الحي")
st.header("المحاكاة التفاعلية لنظرية الميزان")
st.caption("S = W × B | © 2026 Ali Adel Alatifi")

# =============================================
# 🎛️ الشريط الجانبي
# =============================================
with st.sidebar:
    st.header("🎛️ لوحة التحكم")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("▶️", use_container_width=True): st.session_state.run = True
    with c2:
        if st.button("⏹️", use_container_width=True): st.session_state.run = False
    with c3:
        if st.button("🔄", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
    with c4:
        if st.button("🧹", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    st.divider()

    with st.expander("🕌 أركان الإسلام", expanded=False):
        prayer = st.slider("الصلاة", 0.0, 1.0, 0.8, 0.01, key="p")
        zakat = st.slider("الزكاة", 0.0, 1.0, 0.6, 0.01, key="z")
        fasting = st.slider("الصوم", 0.0, 1.0, 0.7, 0.01, key="f")
        hajj = st.slider("الحج", 0.0, 1.0, 0.5, 0.01, key="h")

    with st.expander("🏛️ أسس الحكم", expanded=False):
        amr = st.slider("الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01, key="amr")
        nahy = st.slider("النهي عن المنكر", 0.0, 1.0, 0.5, 0.01, key="nahy")
        adl = st.slider("العدل", 0.0, 1.0, 0.6, 0.01, key="adl")
        shura = st.slider("الشورى", 0.0, 1.0, 0.5, 0.01, key="shura")

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
        riba = st.slider("الربا", 0.0, 1.0, 0.2, 0.01, key="riba")
        ghish = st.slider("الغش", 0.0, 1.0, 0.2, 0.01, key="ghish")
        kadhib = st.slider("الكذب", 0.0, 1.0, 0.2, 0.01, key="kadhib")

    with st.expander("⚙️ إعدادات المحاكاة", expanded=True):
        cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001, key="spd")
        delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1, key="dly")
        N_STARS = st.slider("عدد النجوم", 50, 300, 150, 10, key="nst")

# =============================================
# 🧮 دوال المحاكاة
# =============================================

# --- الدالة الجديدة لألوان النجوم (الحالات الوجودية الأربعة) ---
def get_color(w, b):
    """
    تحدد لون النجمة بناءً على حالتها الوجودية في معادلة الميزان S = W × B:
    - الأبيض: الراهب أو الصوفي (ولاء بلا براءة)
    - الذهبي: المؤمن (ولاء وبراءة)
    - الأحمر: الكافر (براءة بلا ولاء)
    - الوردي: المنافق (لا ولاء ولا براءة)
    """
    if w >= 0.6 and b >= 0.6:
        return '#FFD700'  # ذهبي: مؤمن (W و B عاليتان)
    elif w >= 0.6 and b < 0.4:
        return '#FFFFFF'  # أبيض: راهب أو صوفي (W عالية، B منهارة)
    elif w < 0.4 and b >= 0.6:
        return '#FF3333'  # أحمر: كافر (W منهارة، B عالية)
    elif w < 0.4 and b < 0.4:
        return '#FFB6C1'  # وردي: منافق (W و B منهارتان)
    else:
        # حالات وسطية
        if w > b: return '#FFF8DC'
        elif b > w: return '#FFA07A'
        else: return '#FFBF00'

def calc_S(W, B, E, p, z, f, h, amr, nahy, adl, shura, riba, ghish, kadhib):
    Sb = W * B
    pillars = (p + z + f + h) / 4
    Sb *= (0.5 + 0.5 * pillars)
    prot = (amr * W + nahy * B) / 2
    Sb *= (0.8 + 0.4 * prot) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    if E > Sb: Sb -= riba * (E - Sb) * 0.3
    return np.clip(Sb, 0.001, 1.0)

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
    st.session_state.E = 0.3; st.session_state.S = 0.286
    st.session_state.ph = "استقرار"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5; st.session_state.aa = 0.0
    st.session_state.eb = deque([0.286]*30, maxlen=30)
    st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
    st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
    # عدادات الآخرة (الميزان الخفي)
    st.session_state.hasanat = 0.0
    st.session_state.sayyiat = 0.0
    st.session_state.init = True

# =============================================
# 📊 مؤشرات S, W, B, E + عداد الآخرة
# =============================================
if st.session_state.init:
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFD700;">{st.session_state.S:.3f}</p><p class="metric-lbl">⚖️ S</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFF;">{st.session_state.W:.3f}</p><p class="metric-lbl">🤍 W</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FF5252;">{st.session_state.B:.3f}</p><p class="metric-lbl">❤️ B</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#00FFFF;">{st.session_state.E:.3f}</p><p class="metric-lbl">💫 E</p></div>', unsafe_allow_html=True)
    with m5:
        # عداد الآخرة (الميزان الخفي)
        mizan_akhira = st.session_state.hasanat - st.session_state.sayyiat
        color = "#FFD700" if mizan_akhira >= 0 else "#FF3333"
        st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:{color};">{mizan_akhira:.3f}</p><p class="metric-lbl">📜 الميزان الأخروي</p></div>', unsafe_allow_html=True)

plot_placeholder = st.empty()

# =============================================
# 🎬 المحاكاة الحية
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

            # --- تحديث عداد الآخرة (الميزان الخفي) ---
            st.session_state.hasanat += np.mean(sw) * 0.01  # الحسنات تتراكم مع زيادة W
            st.session_state.sayyiat += (1 - np.mean(sb)) * 0.01  # السيئات تتراكم مع انهيار B

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
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            if pSl:
                pax = ax.inset_axes([0.35, 0.02, 0.60, 0.15])
                pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
                pax.set_title('S leads E — Istidraj', color='white', fontsize=9, fontweight='bold')
                pax.tick_params(colors='white', labelsize=6); pax.grid(True, alpha=0.3)
                pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S')
                pax.plot(pxl, pEl, color='#00FFFF', lw=2, label='E')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=7)
            ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, ha='center', fontweight='bold')
            plt.tight_layout(pad=0)
            plot_placeholder.pyplot(fig)
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
    st.success("⏸️ تم إيقاف المحاكاة")
else:
    if st.session_state.init:
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9)
        ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
        plot_placeholder.pyplot(fig)
        plt.close(fig)

if 'latest_image' in st.session_state:
    st.download_button("📥 تحميل صورة المشهد", st.session_state.latest_image, "mizan_scene.png", "image/png")

st.caption("© 2026 Ali Adel Alatifi | Al-Deen Al-Qayyim")
