import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="الدين القيم – قانون التوازن الكوني", page_icon="⚖️", layout="wide")

# ====================== CSS بسيط للجوال ======================
st.markdown("""
<style>
    .stApp { background: #000010; }
    .stButton > button {
        border-radius: 12px; font-weight: bold; height: 3em; width: 100%;
        background: #1a1a2e; color: white; border: 2px solid #FFD700; font-size: 1em;
    }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== عنوان الصفحة الجميل ======================
st.markdown("""
<div style="text-align: center; padding: 15px 0 5px 0;">
    <h1 style="color: #FFD700; font-size: 2.2em; margin: 10px 0; font-weight: 900;">⚖️ الدِّينُ الْقَيِّم</h1>
    <h2 style="color: #FFD700; font-size: 1.2em; margin-top: 0;">قَانُونُ التَّوَازُنِ الْكَوْنِيّ</h2>
</div>
""", unsafe_allow_html=True)

# ====================== أزرار التحكم في الأعلى ======================
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("▶️ تشغيل", use_container_width=True): st.session_state.run = True; st.rerun()
with c2:
    if st.button("⏹️ إيقاف", use_container_width=True): st.session_state.run = False; st.rerun()
with c3:
    if st.button("🔄 إعادة", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# ====================== مؤشرات علوية ======================
if 'init' in st.session_state and st.session_state.init:
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("⚖️ استقرار S", f"{st.session_state.S:.3f}")
    with m2: st.metric("🤍 ولاء W", f"{st.session_state.W:.3f}")
    with m3: st.metric("❤️ براءة B", f"{st.session_state.B:.3f}")
    with m4: st.metric("💫 تمكين E", f"{st.session_state.E:.3f}")

# ============================================================
#  🎛️ الشريط الجانبي – جميع الخيارات (مضمونة الظهور)
# ============================================================
with st.sidebar:
    st.markdown("## 🎛️ جميع الخيارات")
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
    
    st.subheader("🛡️ آليات الإصلاح")
    taawun_birr = st.slider("🤝 التعاون على البر", 0.0, 1.0, 0.5, 0.01)
    taawun_taqwa = st.slider("🤝 التعاون على التقوى", 0.0, 1.0, 0.5, 0.01)
    tawasi_haqq = st.slider("💬 التواصي بالحق", 0.0, 1.0, 0.5, 0.01)
    tawasi_sabr = st.slider("⏳ التواصي بالصبر", 0.0, 1.0, 0.5, 0.01)
    
    st.subheader("💀 آليات الإفساد")
    nahy_marouf_e = st.slider("🔇 النهي عن المعروف", 0.0, 1.0, 0.2, 0.01)
    amr_munkar_e = st.slider("👿 الأمر بالمنكر", 0.0, 1.0, 0.2, 0.01)
    taawun_ithm = st.slider("🤝 التعاون على الإثم", 0.0, 1.0, 0.2, 0.01)
    taawun_udwan = st.slider("🤝 التعاون على العدوان", 0.0, 1.0, 0.2, 0.01)
    tawasi_batil = st.slider("💬 التواصي بالباطل", 0.0, 1.0, 0.2, 0.01)
    adam_sabr = st.slider("😤 عدم الصبر", 0.0, 1.0, 0.2, 0.01)
    
    st.subheader("⚠️ الأمراض الأخلاقية")
    riba = st.slider("💸 الربا", 0.0, 1.0, 0.2, 0.01)
    ghish = st.slider("🎭 الغش", 0.0, 1.0, 0.2, 0.01)
    kadhib = st.slider("🤥 الكذب", 0.0, 1.0, 0.2, 0.01)
    
    st.subheader("⚙️ معاملات")
    cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001)
    delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1)
    N_STARS = st.slider("النجوم", 100, 600, 300, 50)

# ====================== دوال مساعدة ======================
def get_color(w, b):
    try:
        w, b = float(w), float(b)
        if w >= 0.7 and b >= 0.7: return '#FFD700'
        if w >= 0.55 and b < 0.45: return '#E0E0E0'
        if w < 0.45 and b >= 0.55: return '#FF5252'
        if w < 0.45 and b < 0.45: return '#FF8A80'
        return '#FFF9C4' if w > b else '#FFCCBC'
    except: return '#888888'

def calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib):
    Sb = W * B
    pb = (prayer + zakat + fasting + hajj) / 4
    Sb *= (0.5 + 0.5 * pb)
    pr = (amr * W + nahy * B) / 2
    Sb *= (0.8 + 0.4 * pr) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    if E > Sb: Sb -= riba * (E - Sb) * 0.3
    Ww = W * (1 - kadhib * 0.2)
    Sf = Ww * B
    Sf *= (0.5 + 0.5 * pb) * (0.8 + 0.4 * pr) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
    return np.clip(Sf, 0.001, 1.0)

# ====================== التهيئة ======================
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False

if not st.session_state.init:
    np.random.seed(42); random.seed(42)
    cx, cy = 14, 10.0
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx - 13, cx + 13, N_STARS)
    st.session_state.sy = np.random.uniform(cy - 9, cy + 9, N_STARS)
    st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.W = 0.55; st.session_state.B = 0.52
    st.session_state.E = 0.3; st.session_state.S = 0.55 * 0.52
    st.session_state.ph = "Balance"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5; st.session_state.aa = 0.0
    st.session_state.eb = deque([0.55*0.52] * 30, maxlen=30)
    st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
    st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
    st.session_state.init = True

# ====================== المحاكاة الحية ======================
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

            ca += cycle_speed; sv = np.sin(ca)
            if sv > 0.5: ph = 'استقرار تام'
            elif sv > 0: ph = 'صعود'
            elif sv > -0.5: ph = 'انهيار'
            else: ph = 'قاع'
            if 0.3 < sv < 0.35: ph = '>> استدراج <<'
            if -0.35 < sv < -0.3: ph = '>> تعافي <<'
            target_S = 0.5 + 0.45 * sv

            n = len(sw)
            for i in range(n):
                wb = prayer * 0.01; bb = fasting * 0.01
                dist = np.sqrt((sx[i] - sx) ** 2 + (sy[i] - sy) ** 2)
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
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            eb.append(S)
            eff = int(delay_frames * (1 + ghish * 0.5))
            eb_list = list(eb)
            Et = eb_list[-min(eff, len(eb_list))] if len(eb_list) >= eff else S
            E += 0.03 * (Et - E)
            W = W - 0.01 * E + 0.02 / (S + 0.1)
            B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            pc += 1
            if pc % 2 == 0: pS.append(S); pE.append(E); px.append(len(px))
            aW += 0.02 + random.uniform(-0.025, 0.025) * (1 - W) ** 2
            aB += 0.02 + random.uniform(-0.025, 0.025) * (1 - B) ** 2
            wx = cx + (7 - 2.5 * W) * np.cos(aW); wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB); by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7
            ins = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.07, 0.07, n) * ins
            sy += np.random.uniform(-0.07, 0.07, n) * ins
            sx, sy = np.clip(sx, cx - 13, cx + 13), np.clip(sy, cy - 9, cy + 9)

            st.session_state.W, st.session_state.B = W, B
            st.session_state.E, st.session_state.S = E, S
            st.session_state.ph, st.session_state.ca = ph, ca
            st.session_state.aW, st.session_state.aB, st.session_state.aa = aW, aB, aa + 0.12
            st.session_state.eb = eb
            st.session_state.sx, st.session_state.sy = sx, sy
            st.session_state.sw, st.session_state.sb = sw, sb
            st.session_state.pS, st.session_state.pE, st.session_state.px, st.session_state.pc = pS, pE, px, pc

            # ---------- المشهد الكوني الجميل (بحجم مناسب للجوال) ----------
            fig, ax = plt.subplots(figsize=(10, 7), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'), (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=18, ha='center', va='center', fontweight='bold')
            ax.add_patch(Circle((cx, cy), 0.5 + 10 * E, color='#00FFFF', alpha=0.15, zorder=7))
            ax.add_patch(Circle((cx, cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2, zorder=2))
            for i in range(6):
                an = -np.pi / 4 + i * (np.pi / 2) / 5
                ax.add_patch(Circle((cx + 8.5 * np.cos(an), cy + 8.5 * np.sin(an)), 0.4, color='#FFF', alpha=0.3 + 0.5 * avgW, zorder=8))
            for i in range(6):
                an = np.pi - np.pi / 4 + i * (np.pi / 2) / 5
                ax.add_patch(Circle((cx + 8.5 * np.cos(an), cy + 8.5 * np.sin(an)), 0.4, color='#F33', alpha=0.25 + 0.35 * avgB, zorder=8))
            ax.add_patch(Circle((wx, wy), 0.2 + 0.5 * W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx, by), 0.2 + 0.5 * B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy - 1.2, 'W', color='#FFF', fontsize=12, ha='center')
            ax.text(bx, by - 1.2, 'B', color='#F33', fontsize=12, ha='center')
            colors = [get_color(sw[i], sb[i]) for i in range(n)]
            ax.scatter(sx, sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)
            er = 0.5 + 0.4 * S
            ax.add_patch(Circle((3.5, 4.0), 0.15 + 0.2 * S, color='#4488FF', alpha=0.8, zorder=7))
            ax.add_patch(Circle((3.5 + er * np.cos(aa), 4.0 + er * np.sin(aa)), 0.04, color='white', alpha=0.95, zorder=8))
            ax.text(3.5, 2.5, '⚛️ ذرة', color='#4488FF', fontsize=8, ha='center')
            ax.text(24.5, 2.5, '🧫 خلية', color='#00FF88', fontsize=8, ha='center')
            
            # الميزان
            mx, my, bw, bh = 0.5, 17, 3.5, 0.5
            ax.add_patch(FancyBboxPatch((mx, my), bw, bh, boxstyle="round,pad=0.2", facecolor='#1a1a2e', alpha=0.9, zorder=20))
            if W > 0: ax.add_patch(FancyBboxPatch((mx, my), W * bw / 2, bh, boxstyle="round,pad=0.1", facecolor='#FFF', alpha=0.9, zorder=21))
            if B > 0: ax.add_patch(FancyBboxPatch((mx + bw / 2, my), B * bw / 2, bh, boxstyle="round,pad=0.1", facecolor='#F33', alpha=0.9, zorder=21))
            if W + B > 0: ax.plot(mx + (W / (W + B)) * bw, my + bh / 2, 'v', color='#FFD700', markersize=12, markeredgecolor='white', zorder=22)

            # لوحة الإثبات
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            if pSl:
                pax = ax.inset_axes([0.4, 0.02, 0.55, 0.14])
                pax.set_xlim(0, max(400, len(pxl))); pax.set_ylim(0, 1.05)
                pax.set_title('📈 S (ذهب) يقود E (سماوي) – الاستدراج', color='white', fontsize=7)
                pax.tick_params(colors='white', labelsize=5); pax.grid(True, alpha=0.3)
                pax.plot(pxl, pSl, color='#FFD700', lw=2, label='S')
                pax.plot(pxl, pEl, color='#00FFFF', lw=1.5, alpha=0.9, label='E')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=6)

            ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, ha='center', fontweight='bold')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='#000010'); buf.seek(0)
            st.session_state.latest_image = buf; plt.close(fig)
            time.sleep(0.1)
        except Exception as e:
            st.error(f"خطأ: {str(e)}")
            st.session_state.run = False
            break
    st.success("⏸️ تم إيقاف المحاكاة")
elif st.session_state.init and 'latest_image' in st.session_state:
    st.image(st.session_state.latest_image, caption="آخر حالة للمحاكاة", use_column_width=True)
else:
    # رسم أولي صغير
    if st.session_state.init:
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9, edgecolors='white', linewidths=0.2)
        ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
        ax.set_title('اضغط ▶️ تشغيل لرؤية المشهد الكوني', color='white', fontsize=14)
        st.pyplot(fig)

st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;'>© 2026 علي عادل العاطفي | V23 – التصميم الأصلي المستقر</p>", unsafe_allow_html=True)
