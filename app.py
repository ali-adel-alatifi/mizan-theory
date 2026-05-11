import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="مختبر الميزان", page_icon="⚖️", layout="wide")

if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri+Quran&display=swap');
.stApp { background: linear-gradient(180deg, #0a0f1e 0%, #0d1528 30%, #0f1a2e 100%); }
h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #FFD700; }
p, label, div { font-family: 'Cairo', sans-serif; color: #E0E0E0; }
.golden-title { font-size: 3em; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; }
.verse-text { text-align: center; color: #FFD700; font-size: 1.3em; margin: 15px 0; line-height: 2; }
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; width: 100%; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; }
.stTabs [data-baseweb="tab-list"] { gap: 5px; background: rgba(13,21,40,0.8); border-radius: 15px; padding: 5px; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    return '#888888'

def classify(W, B):
    if W >= 0.5 and B >= 0.5: return (T("مؤمن","Believer"), '#FFD700')
    elif W < 0.5 and B >= 0.5: return (T("كافر","Disbeliever"), '#FF5252')
    elif W < 0.5 and B < 0.5: return (T("منافق","Hypocrite"), '#FFB6C1')
    return (T("مشرك","Polytheist"), '#FFA500')

def curvature(W, B):
    if len(W) < 3: return 0
    dW = np.gradient(list(W)); dB = np.gradient(list(B))
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return num / denom

def calc_S(W, B, E, q=1.0):
    return np.clip(W * B * (1 + q * 0.5), 0.001, 1.0)

# ═══════════════════════════════════════════════════════════════
# النظام النهائي – المنزلقات السبعة
# ═══════════════════════════════════════════════════════════════
ISLAMIC_SYSTEM_FINAL = {
    "faith": {
        "label": T("١. الإيمان", "1. Faith"),
        "desc": T("الإيمان بالله وملائكته وكتبه ورسله واليوم الآخر والقدر خيره وشره", "Belief in Allah, His angels, books, messengers, Last Day, and Decree"),
        "aya": "﴿آمَنَ الرَّسُولُ بِمَا أُنزِلَ إِلَيْهِ مِن رَّبِّهِ وَالْمُؤْمِنُونَ﴾",
        "effect_W": 0.30, "effect_B": 0.15,
    },
    "worship": {
        "label": T("٢. العبادات", "2. Worship"),
        "desc": T("الشهادتان، الصلاة، الزكاة، الصوم، الحج", "Shahada, Prayer, Zakat, Fasting, Hajj"),
        "aya": "﴿بُنِيَ الْإِسْلَامُ عَلَىٰ خَمْسٍ﴾",
        "effect_W": 0.20, "effect_B": 0.15,
    },
    "transactions": {
        "label": T("٣. المعاملات", "3. Transactions"),
        "desc": T("تحكيم شرع الله، الحكم بالعدل، الأمر بالشورى، الأمانة", "Applying Sharia, Justice, Consultation, Trustworthiness"),
        "aya": "﴿فَاحْكُم بَيْنَهُم بِمَا أَنزَلَ اللَّهُ﴾",
        "effect_W": 0.12, "effect_B": 0.18,
    },
    "morals": {
        "label": T("٤. الأخلاق", "4. Morals"),
        "desc": T("موالاة المؤمنين، التعاون على البر والتقوى، التواصي بالحق والصبر، الصدق، الوفاء", "Alliance, Cooperation, Truth, Patience, Honesty, Promises"),
        "aya": "﴿وَتَعَاوَنُوا عَلَى الْبِرِّ وَالتَّقْوَىٰ﴾",
        "effect_W": 0.15, "effect_B": 0.10,
    },
    "enjoining": {
        "label": T("٥. الأمر بالمعروف والنهي عن المنكر", "5. Enjoining Good & Forbidding Evil"),
        "desc": T("الدعوة إلى الخير، ومحاربة المنكر، والنصيحة للأمة", "Calling to goodness, fighting evil, advising the nation"),
        "aya": "﴿وَلْتَكُن مِّنكُمْ أُمَّةٌ يَدْعُونَ إِلَى الْخَيْرِ﴾",
        "effect_W": 0.10, "effect_B": 0.20,
    },
    "hudud": {
        "label": T("٦. إقامة الحدود", "6. Establishing Limits"),
        "desc": T("إقامة حدود الله، وتحريم الربا، واجتناب الكبائر", "Establishing Allah's limits, prohibiting usury, avoiding major sins"),
        "aya": "﴿تِلْكَ حُدُودُ اللَّهِ فَلَا تَعْتَدُوهَا﴾",
        "effect_W": 0.05, "effect_B": 0.25,
    },
    "jihad": {
        "label": T("٧. الجهاد في سبيل الله ونصرة الحق", "7. Jihad & Supporting Truth"),
        "desc": T("الجهاد بالنفس والمال، ونصرة الحق وأهله، ونصرة المستضعفين", "Jihad with self and wealth, supporting truth and the oppressed"),
        "aya": "﴿وَجَاهِدُوا فِي اللَّهِ حَقَّ جِهَادِهِ﴾",
        "effect_W": 0.15, "effect_B": 0.15,
    },
}

def compute_WB_final(values):
    W_total = 0.1; B_total = 0.1
    for key, val in values.items():
        if key in ISLAMIC_SYSTEM_FINAL:
            W_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_W"]
            B_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_B"]
    return np.clip(W_total, 0.01, 1.0), np.clip(B_total, 0.01, 1.0)

def create_final_sliders(prefix, defaults=None):
    if defaults is None: defaults = {k: 0.7 for k in ISLAMIC_SYSTEM_FINAL}
    values = {}
    for key, data in ISLAMIC_SYSTEM_FINAL.items():
        values[key] = st.slider(
            data["label"], 0.0, 1.0, defaults.get(key, 0.7), 0.05,
            key=f"{prefix}_{key}",
            help=f"{data['desc']}\n\n{data['aya']}\n\nW: {data['effect_W']:.2f} | B: {data['effect_B']:.2f}"
        )
    return values

# ═══════════════════════════════════════════════════════════════
# الجلسة
# ═══════════════════════════════════════════════════════════════
if 'init' not in st.session_state:
    np.random.seed(42); random.seed(42)
    cx, cy = 14, 10.0; N = 150
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-13, cx+13, N)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, N)
    st.session_state.sw = np.random.uniform(0.1, 1, N)
    st.session_state.sb = np.random.uniform(0.1, 1, N)
    st.session_state.N = N
    st.session_state.W = 0.55; st.session_state.B = 0.52; st.session_state.E = 0.3
    st.session_state.S = 0.55 * 0.52
    st.session_state.pW = deque([0.55], maxlen=50); st.session_state.pB = deque([0.52], maxlen=50)
    st.session_state.hS = deque(maxlen=300); st.session_state.hE = deque(maxlen=300); st.session_state.hx = deque(maxlen=300)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0; st.session_state.frame = 0
    st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]; st.session_state.path_kappa = [0.0]
    for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
        setattr(st.session_state, f"path_{l}", [0.5])
    st.session_state.compass_W = 0.5; st.session_state.compass_B = 0.5
    st.session_state.compass_hist_W = [0.5]; st.session_state.compass_hist_B = [0.5]
    st.session_state.run = False
    st.session_state.init = True

print("✅ المرحلة الأولى مكتملة: الأساسات والنظام النهائي والجلسة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثانية: العنوان وأزرار التحكم والتبويبات
# ═══════════════════════════════════════════════════════════════

# --- العنوان الرئيسي ---
col_icon1, col_title, col_icon2 = st.columns([1, 6, 1])
with col_icon1:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{T('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
with col_icon2:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='verse-text'>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    <br><span style='font-size:0.8em;'>S = W × B | ق = ١٠٠ = الحق = الميزان</span>
</div>
""", unsafe_allow_html=True)

# --- أزرار التحكم ---
c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
with c1:
    if st.button("▶️ تشغيل", key="btn_run", use_container_width=True):
        st.session_state.run = True
with c2:
    if st.button("⏹️ إيقاف", key="btn_stop", use_container_width=True):
        st.session_state.run = False
with c3:
    if st.button("English" if L == "ar" else "العربية", key="btn_lang", use_container_width=True):
        st.session_state.lang = "en" if L == "ar" else "ar"
        st.rerun()
with c4:
    lag = st.select_slider(
        T("فجوة الاستدراج", "Istidraj Gap"),
        options=[5, 10, 15, 22, 30, 40, 50],
        value=22, key="lag"
    )
with c5:
    if st.button("🔄 إعادة", key="btn_reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

st.markdown("---")

# --- التبويبات ---
tab_labels = [
    T("🌌 الكون", "🌌 Cosmos"),
    T("🧍 الفرد", "🧍 Individual"),
    T("👥 المجتمع", "👥 Society"),
    T("🏛️ الدولة", "🏛️ State"),
    T("🌍 الأمة", "🌍 Nation"),
    T("🏰 الحضارة", "🏰 Civilization"),
    T("📜 الآخرة", "📜 Hereafter"),
    T("📐 الصراط", "📐 Path"),
]

tabs = st.tabs(tab_labels)

print("✅ المرحلة الثانية مكتملة: العنوان وأزرار التحكم والتبويبات.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثالثة: الكون، الفرد، المجتمع
# ═══════════════════════════════════════════════════════════════

# --- تبويب ١: الكون ---
with tabs[0]:
    st.header(T("🌌 المشهد الكوني", "🌌 The Cosmic Scene"))
    
    with st.expander(T("⚙️ مولدات الطاقة – المنزلقات السبعة", "⚙️ Energy Generators – Seven Sliders"), expanded=False):
        cosmic_values = create_final_sliders("cosmic")
    
    placeholder = st.empty()
    
    if st.session_state.get("run", False):
        W, B = compute_WB_final(cosmic_values)
        st.session_state.W = W; st.session_state.B = B
        
        while st.session_state.run:
            W = st.session_state.W; B = st.session_state.B; E = st.session_state.E
            S = st.session_state.S; phase = st.session_state.phase; ca = st.session_state.ca
            aW = st.session_state.aW; aB = st.session_state.aB
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx = st.session_state.cx; cy = st.session_state.cy; eb = st.session_state.eb
            hS = st.session_state.hS; hE = st.session_state.hE; hx = st.session_state.hx
            good = st.session_state.good; bad = st.session_state.bad
            pW = st.session_state.pW; pB = st.session_state.pB; frame = st.session_state.frame
            N = st.session_state.N

            ca += 0.008; sv = np.sin(ca)
            if sv > 0.5: phase = T('ذروة', 'Peak')
            elif sv > 0: phase = T('صعود', 'Rising')
            elif sv > -0.5: phase = T('انهيار', 'Collapse')
            else: phase = T('قاع', 'Bottom')
            if 0.3 < sv < 0.35: phase = T('>> استدراج <<', '>> Istidraj <<')
            target = 0.5 + 0.45 * sv

            for i in range(N):
                dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                nbr = np.where((dist < 2.0) & (np.arange(N) != i))[0]
                sw[i] += (target - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (target - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                if len(nbr) > 0:
                    sw[i] += (np.mean(sw[nbr]) - sw[i]) * 0.03
                    sb[i] += (np.mean(sb[nbr]) - sb[i]) * 0.03
                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)

            if random.random() < 0.005:
                aff = np.random.choice(N, size=int(N * 0.2), replace=False)
                sw[aff] *= random.uniform(0.5, 0.8)
                sb[aff] *= random.uniform(0.5, 0.8)

            W += (np.mean(sw) - W) * 0.04
            B += (np.mean(sb) - B) * 0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            eb.append(S)
            past = list(eb)[-lag] if len(eb) >= lag else S
            E += 0.03 * (past - E)
            W = W - 0.015 * E + 0.03 / (S + 0.1) - 0.007 * (1 - B)
            B = B - 0.012 * E + 0.006 * (1 - B) * W * (1 - W)
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            pW.append(W); pB.append(B)
            frame += 1
            if frame % 2 == 0:
                hS.append(S); hE.append(E); hx.append(len(hx))

            aW += 0.02 + random.uniform(-0.02, 0.02) * (1 - W)**2
            aB += 0.02 + random.uniform(-0.02, 0.02) * (1 - B)**2
            wx = cx + (7 - 2.5 * W) * np.cos(aW)
            wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB)
            by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7

            instability = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.07, 0.07, N) * instability
            sy += np.random.uniform(-0.07, 0.07, N) * instability
            sx = np.clip(sx, cx - 13, cx + 13)
            sy = np.clip(sy, cy - 9, cy + 9)

            good += W * 0.1; bad += (1 - B) * 0.1

            st.session_state.W = W; st.session_state.B = B; st.session_state.E = E; st.session_state.S = S
            st.session_state.phase = phase; st.session_state.ca = ca
            st.session_state.aW = aW; st.session_state.aB = aB; st.session_state.eb = eb
            st.session_state.sx = sx; st.session_state.sy = sy; st.session_state.sw = sw; st.session_state.sb = sb
            st.session_state.pW = pW; st.session_state.pB = pB
            st.session_state.hS = hS; st.session_state.hE = hE; st.session_state.hx = hx; st.session_state.frame = frame
            st.session_state.good = good; st.session_state.bad = bad

            fig, ax = plt.subplots(figsize=(16, 10), facecolor='#0a0f1e')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.6, '#FFD700'), (1.8, 0.3, '#FFD700'), (2.8, 0.1, '#FFA500'), (4, 0.03, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 3 * S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#000', fontsize=14, ha='center', va='center', fontweight='bold')
            ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#0FF', alpha=0.15, zorder=7))
            ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy + 0.8, 'W', color='#FFF', fontsize=10, ha='center')
            ax.text(bx, by + 0.8, 'B', color='#F33', fontsize=10, ha='center')
            colors = [star_color(sw[i], sb[i]) for i in range(N)]
            ax.scatter(sx, sy, s=20, c=colors, alpha=0.9, edgecolors='white', linewidths=0.2, zorder=5)

            # الميزان الأخروي
            akh_x, akh_y, ms = 26.5, 18, 1.5
            ax.plot([akh_x, akh_x], [akh_y - 3, akh_y + 1.5], color='#FFD700', lw=1, alpha=0.4)
            ly = akh_y - 1.5 + ms * min(good / 50, 1.5)
            ry = akh_y - 1.5 - ms * min(bad / 50, 1.5)
            ax.add_patch(Circle((akh_x - 1, ly), 0.6, color='#FFD700', alpha=0.3, zorder=20))
            ax.text(akh_x - 1, ly - 1, T('حسنات', 'Good'), color='#FFD700', fontsize=5, ha='center')
            ax.add_patch(Circle((akh_x + 1, ry), 0.6, color='#FF4444', alpha=0.3, zorder=20))
            ax.text(akh_x + 1, ry - 1, T('سيئات', 'Bad'), color='#FF4444', fontsize=5, ha='center')
            diff = (bad - good) / 50 * ms
            ax.plot([akh_x - 1, akh_x + 1], [akh_y - diff, akh_y + diff], color='#FFD700', lw=1.5, alpha=0.6)

            # منحنى الاستدراج
            pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
            pax.set_xlim(0, 350); pax.set_ylim(0, 1.05)
            pax.set_title(T("S يقود E — الاستدراج", "S leads E — Istidraj"), color='white', fontsize=7)
            pax.tick_params(colors='white', labelsize=5); pax.grid(True, alpha=0.12)
            if hS: pax.plot(list(hx), list(hS), color='#FFD700', lw=2); pax.plot(list(hx), list(hE), color='#0FF', lw=1.5)

            ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f} | κ={curvature(pW, pB):.3f}',
                   color='#CCC', fontsize=9, ha='center')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.06)
    else:
        st.info(T("اضغط ▶️ تشغيل لرؤية المشهد الحي", "Press ▶️ Run to see the live scene"))

    # زر تحميل البيانات
    if not st.session_state.get("run", False) and len(st.session_state.hS) > 0:
        csv_data = "Time,S,E\n" + "\n".join([f"{i},{s:.4f},{e:.4f}" for i, (s, e) in enumerate(zip(st.session_state.hS, st.session_state.hE))])
        st.download_button(
            T("📥 تحميل بيانات المحاكاة", "📥 Download Simulation Data"),
            data=csv_data, file_name="mizan_cosmic.csv", mime="text/csv", key="dl_cosmic"
        )

# --- تبويب ٢: الفرد (البوصلة التفاعلية) ---
with tabs[1]:
    st.header(T("🧍 مختبر الفرد – بوصلة الحياة", "🧍 Individual Lab – Life Compass"))
    
    st.markdown(T(
        "اختر فعلاً، وستتحرك نقطتك في فضاء (W, B). الهدف: الوصول إلى مربع المؤمن (1,1) والمكوث فيه.",
        "Choose an action, and your point moves in (W, B) space. Goal: reach the Believer's quadrant (1,1)."
    ))
    
    # الموقع الحالي
    q_name, q_color = classify(st.session_state.compass_W, st.session_state.compass_B)
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    col_i1.metric("W", f"{st.session_state.compass_W:.3f}")
    col_i2.metric("B", f"{st.session_state.compass_B:.3f}")
    col_i3.metric("S", f"{st.session_state.compass_W * st.session_state.compass_B:.3f}")
    col_i4.markdown(f"<h3 style='color:{q_color};text-align:center;margin-top:20px;'>{q_name}</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(T("### 🎯 اختر فعلك:", "### 🎯 Choose Your Action:"))
    
    # أعمال تقوي W
    st.markdown(T("#### 🤍 أعمال تقوي الولاء (W)", "#### 🤍 Strengthening Loyalty (W)"))
    cw1, cw2, cw3, cw4, cw5 = st.columns(5)
    with cw1:
        if st.button("🕌 صلاة", key="act_prayer", use_container_width=True):
            st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.15)
            st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.03)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cw2:
        if st.button("📖 قرآن", key="act_quran", use_container_width=True):
            st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.10)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cw3:
        if st.button("🤲 دعاء", key="act_dua", use_container_width=True):
            st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.08)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cw4:
        if st.button("💛 صدقة", key="act_charity", use_container_width=True):
            st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.08)
            st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.08)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cw5:
        if st.button("🤝 صلة رحم", key="act_family", use_container_width=True):
            st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.07)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    
    # أعمال تقوي B
    st.markdown(T("#### ❤️ أعمال تقوي البراءة (B)", "#### ❤️ Strengthening Disavowal (B)"))
    cb1, cb2, cb3, cb4, cb5 = st.columns(5)
    with cb1:
        if st.button("🚫 إنكار منكر", key="act_nahy", use_container_width=True):
            st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.15)
            st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.03)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cb2:
        if st.button("⚔️ جهاد النفس", key="act_jihad_self", use_container_width=True):
            st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.12)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cb3:
        if st.button("🔻 بغض المعاصي", key="act_hate_sins", use_container_width=True):
            st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.10)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cb4:
        if st.button("🛡️ غض البصر", key="act_gaze", use_container_width=True):
            st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.08)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cb5:
        if st.button("⚖️ عدل", key="act_justice", use_container_width=True):
            st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.08)
            st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.08)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    
    # معاصي
    st.markdown(T("#### ⚠️ معاصي تضعف", "#### ⚠️ Sins That Weaken"))
    cs1, cs2, cs3, cs4, cs5 = st.columns(5)
    with cs1:
        if st.button("🤥 كذب", key="sin_lie", use_container_width=True):
            st.session_state.compass_W = max(0.01, st.session_state.compass_W - 0.12)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cs2:
        if st.button("🗣️ غيبة", key="sin_backbite", use_container_width=True):
            st.session_state.compass_W = max(0.01, st.session_state.compass_W - 0.10)
            st.session_state.compass_B = max(0.01, st.session_state.compass_B - 0.08)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cs3:
        if st.button("👊 ظلم", key="sin_injustice", use_container_width=True):
            st.session_state.compass_B = max(0.01, st.session_state.compass_B - 0.18)
            st.session_state.compass_W = max(0.01, st.session_state.compass_W - 0.05)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cs4:
        if st.button("💸 ربا", key="sin_usury", use_container_width=True):
            st.session_state.compass_B = max(0.01, st.session_state.compass_B - 0.15)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    with cs5:
        if st.button("💔 قطيعة رحم", key="sin_cut_family", use_container_width=True):
            st.session_state.compass_W = max(0.01, st.session_state.compass_W - 0.12)
            st.session_state.compass_hist_W.append(st.session_state.compass_W)
            st.session_state.compass_hist_B.append(st.session_state.compass_B)
            st.rerun()
    
    # توبة
    if st.button("🕌 توبة نصوح", key="act_tawbah", use_container_width=True, type="primary"):
        st.session_state.compass_W = min(1.0, st.session_state.compass_W + 0.6 * (1.0 - st.session_state.compass_W))
        st.session_state.compass_B = min(1.0, st.session_state.compass_B + 0.6 * (1.0 - st.session_state.compass_B))
        st.session_state.compass_hist_W.append(st.session_state.compass_W)
        st.session_state.compass_hist_B.append(st.session_state.compass_B)
        st.rerun()
    
    if st.button("🔄 إعادة الرحلة", key="reset_compass", use_container_width=True):
        st.session_state.compass_W = 0.5; st.session_state.compass_B = 0.5
        st.session_state.compass_hist_W = [0.5]; st.session_state.compass_hist_B = [0.5]
        st.rerun()
    
    # رسم الخريطة مع المسار
    st.markdown("---")
    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
    ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.2))
    ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF5252', alpha=0.2))
    ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.2))
    ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA500', alpha=0.2))
    ax.text(0.5, 0.5, "مؤمن", ha='center', color='#FFD700', fontsize=14, fontweight='bold')
    ax.text(-0.5, 0.5, "كافر", ha='center', color='#FF5252', fontsize=14, fontweight='bold')
    ax.text(-0.5, -0.5, "منافق", ha='center', color='#FFB6C1', fontsize=14, fontweight='bold')
    ax.text(0.5, -0.5, "مشرك", ha='center', color='#FFA500', fontsize=14, fontweight='bold')
    
    hist_W = st.session_state.compass_hist_W
    hist_B = st.session_state.compass_hist_B
    if len(hist_W) > 1:
        for i in range(1, len(hist_W)):
            alpha_val = 0.3 + 0.7 * (i / len(hist_W))
            ax.plot([hist_B[i-1]*2-1, hist_B[i]*2-1], [hist_W[i-1]*2-1, hist_W[i]*2-1],
                   color='#00FFFF', lw=2, alpha=alpha_val)
        ax.scatter([hist_B[0]*2-1], [hist_W[0]*2-1], s=80, c='white', edgecolors='#00FFFF', linewidth=2, zorder=10)
    
    current_B = st.session_state.compass_B * 2 - 1
    current_W = st.session_state.compass_W * 2 - 1
    ax.scatter([current_B], [current_W], s=250, c=q_color, edgecolors='white', linewidth=3, zorder=15)
    ax.set_xlabel("B (البراءة)", color='white', fontsize=12)
    ax.set_ylabel("W (الولاء)", color='white', fontsize=12)
    ax.tick_params(colors='white')
    ax.set_title(T("رحلة النقطة في فضاء (W, B)", "Point Journey in (W, B) Space"), color='white', fontsize=14, fontweight='bold')
    st.pyplot(fig)

# --- تبويب ٣: المجتمع ---
with tabs[2]:
    st.header(T("👥 مختبر المجتمع", "👥 Society Lab"))
    
    soc_values = create_final_sliders("soc")
    
    pop = st.slider(T("عدد الأفراد", "Population"), 50, 300, 150, 25, key="pop_soc")
    years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 10, 200, 80, 10, key="yrs_soc")
    
    if st.button(T("🚀 شغّل محاكاة المجتمع", "🚀 Run Society Simulation"), key="btn_soc", use_container_width=True):
        W_base, B_base = compute_WB_final(soc_values)
        pW = np.random.uniform(0.2, 0.9, pop); pB = np.random.uniform(0.2, 0.9, pop)
        px = np.random.uniform(0, 30, pop); py = np.random.uniform(0, 30, pop)
        hist_W, hist_B, hist_S = [], [], []
        for _ in range(years):
            nW = pW.copy(); nB = pB.copy()
            for i in range(pop):
                d = np.sqrt((px - px[i])**2 + (py - py[i])**2)
                nbr = np.where((d < 2.5) & (np.arange(pop) != i))[0]
                if len(nbr) > 0:
                    nW[i] += 0.03 * (np.mean(pW[nbr]) - pW[i])
                    nB[i] += 0.03 * (np.mean(pB[nbr]) - pB[i])
                nW[i] += 0.02 * (W_base - pW[i]) + 0.01 * (np.random.rand() - 0.5)
                nB[i] += 0.02 * (B_base - pB[i]) + 0.01 * (np.random.rand() - 0.5)
                nW[i] = np.clip(nW[i], 0.01, 1.0); nB[i] = np.clip(nB[i], 0.01, 1.0)
            pW = nW; pB = nB
            px += np.random.randint(-1, 2, pop); py += np.random.randint(-1, 2, pop)
            px = np.clip(px, 0, 29); py = np.clip(py, 0, 29)
            hist_W.append(np.mean(pW)); hist_B.append(np.mean(pB)); hist_S.append(np.mean(pW * pB))
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
        ax1 = axes[0]; ax1.set_facecolor('#0a0f1e')
        colors = [star_color(pW[i], pB[i]) for i in range(pop)]
        ax1.scatter(px, py, c=colors, s=30, alpha=0.8, edgecolors='white', linewidths=0.2)
        ax1.set_xlim(0, 30); ax1.set_ylim(0, 30)
        ax1.set_title(T("خريطة المجتمع", "Society Map"), color='white', fontsize=13)
        ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
        ax2 = axes[1]; ax2.set_facecolor('#0a0f1e')
        ax2.plot(hist_W, color='gold', lw=2, label='W')
        ax2.plot(hist_B, color='#FF5252', lw=2, label='B')
        ax2.plot(hist_S, color='#0F8', lw=2, label='S')
        ax2.set_title(T("تطور المجتمع", "Society Evolution"), color='white', fontsize=13)
        ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white'); ax2.set_ylim(0, 1.05)
        plt.tight_layout(); st.pyplot(fig)
        st.metric(T("متوسط S النهائي", "Final Average S"), f"{hist_S[-1]:.3f}")

print("✅ المرحلة الثالثة مكتملة: الكون، الفرد، المجتمع.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الرابعة: الدولة، الأمة، الحضارة
# ═══════════════════════════════════════════════════════════════

# --- تبويب ٤: الدولة ---
with tabs[3]:
    st.header(T("🏛️ مختبر الدولة", "🏛️ State Lab"))
    
    state_values = create_final_sliders("state")
    
    state_years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 50, 300, 120, 10, key="yrs_state")
    
    if st.button(T("🚀 شغّل محاكاة الدولة", "🚀 Run State Simulation"), key="btn_state", use_container_width=True):
        W_base, B_base = compute_WB_final(state_values)
        Y = state_years
        
        Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
        Wh[0] = W_base * 0.8; Bh[0] = B_base * 0.8
        Sh[0] = Wh[0] * Bh[0]; Eh[0] = 0.1
        
        for t in range(1, Y):
            Wh[t] = np.clip(Wh[t-1] + 0.03 * (W_base - Wh[t-1]) - 0.01 * Eh[t-1], 0.01, 1.0)
            Bh[t] = np.clip(Bh[t-1] + 0.03 * (B_base - Bh[t-1]) - 0.008 * Eh[t-1], 0.01, 1.0)
            Sh[t] = Wh[t] * Bh[t]
            past = Sh[max(0, t - 15)]
            Eh[t] = np.clip(Eh[t-1] + 0.04 * (past - Eh[t-1]), 0.01, 1.0)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(Sh, 'g-', lw=2, label='S (الثبات)')
        ax.plot(Eh, 'b--', lw=2, label='E (التمكين)')
        ax.plot(Wh, color='gold', lw=1, alpha=0.6, label='W')
        ax.plot(Bh, '#FF5252', lw=1, alpha=0.6, label='B')
        ax.set_title(T("دورة الدولة عبر الزمن", "State Cycle Over Time"), color='white', fontsize=13)
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
        st.pyplot(fig)
        
        idxS = np.argmax(Sh); idxE = np.argmax(Eh)
        c1, c2, c3 = st.columns(3)
        c1.metric(T("S النهائي", "Final S"), f"{Sh[-1]:.3f}")
        c2.metric(T("أقصى S", "Max S"), f"{np.max(Sh):.3f}")
        c3.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, idxE - idxS)} {T('عام', 'yrs')}")

# --- تبويب ٥: الأمة ---
with tabs[4]:
    st.header(T("🌍 مختبر الأمة", "🌍 Nation Lab"))
    
    nation_values = create_final_sliders("nation")
    
    nation_years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 100, 500, 250, 25, key="yrs_nation")
    
    if st.button(T("🚀 شغّل محاكاة الأمة", "🚀 Run Nation Simulation"), key="btn_nation", use_container_width=True):
        W_base, B_base = compute_WB_final(nation_values)
        Y = nation_years
        
        Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
        Wh[0] = W_base * 0.7; Bh[0] = B_base * 0.7
        Sh[0] = Wh[0] * Bh[0]; Eh[0] = 0.1
        
        for t in range(1, Y):
            Wh[t] = np.clip(Wh[t-1] + 0.02 * (W_base - Wh[t-1]) - 0.008 * Eh[t-1], 0.01, 1.0)
            Bh[t] = np.clip(Bh[t-1] + 0.02 * (B_base - Bh[t-1]) - 0.006 * Eh[t-1], 0.01, 1.0)
            Sh[t] = Wh[t] * Bh[t]
            past = Sh[max(0, t - lag)]
            Eh[t] = np.clip(Eh[t-1] + 0.03 * (past - Eh[t-1]), 0.01, 1.0)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(Sh, 'g-', lw=2, label='S')
        ax.plot(Eh, 'b--', lw=2, label='E')
        ax.plot(Wh, color='gold', lw=1, alpha=0.6, label='W')
        ax.plot(Bh, '#FF5252', lw=1, alpha=0.6, label='B')
        ax.set_title(T("دورة الأمة عبر الزمن", "Nation Cycle Over Time"), color='white', fontsize=13)
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
        st.pyplot(fig)
        
        idxS = np.argmax(Sh); idxE = np.argmax(Eh)
        c1, c2, c3 = st.columns(3)
        c1.metric(T("S النهائي", "Final S"), f"{Sh[-1]:.3f}")
        c2.metric(T("أقصى S", "Max S"), f"{np.max(Sh):.3f}")
        c3.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, idxE - idxS)} {T('عام', 'yrs')}")

# --- تبويب ٦: الحضارة ---
with tabs[5]:
    st.header(T("🏰 مختبر الحضارة", "🏰 Civilization Lab"))
    st.markdown(T("قارن بين حضارتين تبدأ كل منهما بقيم مختلفة.", "Compare two civilizations starting with different values."))
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"### 🟡 {T('الحضارة الأولى', 'Civilization A')}")
        civ_a_values = create_final_sliders("civ_a")
    with col_b:
        st.markdown(f"### 🔴 {T('الحضارة الثانية', 'Civilization B')}")
        civ_b_values = create_final_sliders("civ_b",
            defaults={k: 0.2 for k in ISLAMIC_SYSTEM_FINAL})
    
    if st.button(T("🚀 شغّل مقارنة الحضارات", "🚀 Run Civilization Comparison"), key="btn_civ", use_container_width=True):
        W_a, B_a = compute_WB_final(civ_a_values)
        W_b, B_b = compute_WB_final(civ_b_values)
        
        Y = 200
        Sh_a = np.zeros(Y); Eh_a = np.zeros(Y)
        Sh_b = np.zeros(Y); Eh_b = np.zeros(Y)
        Wh_a = np.zeros(Y); Bh_a = np.zeros(Y)
        Wh_b = np.zeros(Y); Bh_b = np.zeros(Y)
        
        Wh_a[0] = W_a * 0.8; Bh_a[0] = B_a * 0.8; Sh_a[0] = Wh_a[0] * Bh_a[0]; Eh_a[0] = 0.1
        Wh_b[0] = W_b * 0.8; Bh_b[0] = B_b * 0.8; Sh_b[0] = Wh_b[0] * Bh_b[0]; Eh_b[0] = 0.1
        
        for t in range(1, Y):
            # الحضارة أ
            Wh_a[t] = np.clip(Wh_a[t-1] + 0.02 * (W_a - Wh_a[t-1]) - 0.01 * Eh_a[t-1], 0.01, 1.0)
            Bh_a[t] = np.clip(Bh_a[t-1] + 0.02 * (B_a - Bh_a[t-1]) - 0.008 * Eh_a[t-1], 0.01, 1.0)
            Sh_a[t] = Wh_a[t] * Bh_a[t]
            past_a = Sh_a[max(0, t - 20)]
            Eh_a[t] = np.clip(Eh_a[t-1] + 0.04 * (past_a - Eh_a[t-1]), 0.01, 1.0)
            
            # الحضارة ب
            Wh_b[t] = np.clip(Wh_b[t-1] + 0.02 * (W_b - Wh_b[t-1]) - 0.01 * Eh_b[t-1], 0.01, 1.0)
            Bh_b[t] = np.clip(Bh_b[t-1] + 0.02 * (B_b - Bh_b[t-1]) - 0.008 * Eh_b[t-1], 0.01, 1.0)
            Sh_b[t] = Wh_b[t] * Bh_b[t]
            past_b = Sh_b[max(0, t - 20)]
            Eh_b[t] = np.clip(Eh_b[t-1] + 0.04 * (past_b - Eh_b[t-1]), 0.01, 1.0)
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
        
        ax1 = axes[0]; ax1.set_facecolor('#0a0f1e')
        ax1.plot(Sh_a, 'gold', lw=2, label=T('الحضارة أ (S)', 'Civ A (S)'))
        ax1.plot(Eh_a, 'gold', lw=1.5, ls='--', alpha=0.6, label=T('الحضارة أ (E)', 'Civ A (E)'))
        ax1.plot(Sh_b, '#FF5252', lw=2, label=T('الحضارة ب (S)', 'Civ B (S)'))
        ax1.plot(Eh_b, '#FF5252', lw=1.5, ls='--', alpha=0.6, label=T('الحضارة ب (E)', 'Civ B (E)'))
        ax1.set_title(T("مقارنة الحضارتين", "Civilization Comparison"), color='white', fontsize=13)
        ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
        ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white'); ax1.set_ylim(0, 1.05)
        
        ax2 = axes[1]; ax2.set_facecolor('#0a0f1e')
        ax2.plot(Bh_a, Wh_a, 'gold', lw=1.5, alpha=0.7, label=T('حضارة أ', 'Civ A'))
        ax2.plot(Bh_b, Wh_b, '#FF5252', lw=1.5, alpha=0.7, label=T('حضارة ب', 'Civ B'))
        ax2.scatter(Bh_a[0], Wh_a[0], s=80, c='gold', edgecolors='white', linewidth=2, zorder=10)
        ax2.scatter(Bh_b[0], Wh_b[0], s=80, c='#FF5252', edgecolors='white', linewidth=2, zorder=10)
        ax2.axhline(0.5, color='grey', ls=':', lw=1); ax2.axvline(0.5, color='grey', ls=':', lw=1)
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
        ax2.set_xlabel('B', color='white'); ax2.set_ylabel('W', color='white')
        ax2.set_title(T("المسار في فضاء (W,B)", "Path in (W,B) Space"), color='white', fontsize=13)
        ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
        ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
        plt.tight_layout(); st.pyplot(fig)
        
        c1, c2 = st.columns(2)
        c1.metric(T("S النهائي - حضارة أ", "Final S - Civ A"), f"{Sh_a[-1]:.3f}")
        c2.metric(T("S النهائي - حضارة ب", "Final S - Civ B"), f"{Sh_b[-1]:.3f}")

print("✅ المرحلة الرابعة مكتملة: الدولة، الأمة، الحضارة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الخامسة: الآخرة، الصراط، التذييل
# ═══════════════════════════════════════════════════════════════

# --- تبويب ٧: الآخرة ---
with tabs[6]:
    st.header(T("📜 ميزان الآخرة", "📜 Hereafter Balance"))
    st.markdown(T(
        "هذا هو الميزان الأخروي. الحسنات تتراكم مع زيادة W (الولاء)، "
        "والسيئات تتراكم مع نقصان B (البراءة). راقب كفتي الميزان وهما تتحركان.",
        
        "This is the Hereafter Balance. Good deeds accumulate with increasing W (Loyalty), "
        "and bad deeds accumulate with decreasing B (Disavowal). Watch the scales move."
    ))
    
    akh_good = st.session_state.good
    akh_bad = st.session_state.bad
    balance = akh_good - akh_bad
    
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    
    # عمود الميزان
    ax.plot([5, 5], [2, 9], color='#FFD700', lw=3, alpha=0.8)
    
    # العارضة
    tilt = np.clip(balance / 100, -1.5, 1.5)
    ax.plot([3, 7], [5.5 - tilt, 5.5 + tilt], color='#FFD700', lw=4, alpha=0.9)
    
    # كفة الحسنات
    gY = 5.5 - tilt - 1.5
    ax.add_patch(Circle((3, gY), 0.8, color='#FFD700', alpha=0.3, ec='#FFD700', lw=2))
    ax.text(3, gY, f'{akh_good:.0f}', color='#FFD700', fontsize=14, ha='center', va='center', fontweight='bold')
    ax.text(3, gY - 1.5, T('حسنات', 'Good Deeds'), color='#FFD700', fontsize=11, ha='center')
    
    # كفة السيئات
    bY = 5.5 + tilt + 1.5
    ax.add_patch(Circle((7, bY), 0.8, color='#FF4444', alpha=0.3, ec='#FF4444', lw=2))
    ax.text(7, bY, f'{akh_bad:.0f}', color='#FF4444', fontsize=14, ha='center', va='center', fontweight='bold')
    ax.text(7, bY - 1.5, T('سيئات', 'Bad Deeds'), color='#FF4444', fontsize=11, ha='center')
    
    # نتيجة الميزان
    if balance > 0:
        result_text = T("راجحة", "Winning")
        result_color = '#FFD700'
    elif balance < 0:
        result_text = T("خاسرة", "Losing")
        result_color = '#FF4444'
    else:
        result_text = T("متوازنة", "Balanced")
        result_color = '#888'
    
    ax.text(5, 1, result_text, color=result_color, fontsize=16, ha='center', fontweight='bold')
    ax.set_title(T("الميزان الأخروي", "The Hereafter Balance"), color='white', fontsize=16, fontweight='bold')
    st.pyplot(fig)
    
    col1, col2, col3 = st.columns(3)
    col1.metric(T("الحسنات", "Good Deeds"), f"{akh_good:.1f}")
    col2.metric(T("السيئات", "Bad Deeds"), f"{akh_bad:.1f}")
    col3.metric(
        T("الميزان", "Balance"), 
        f"{balance:+.1f}",
        delta=T("راجحة", "Winning") if balance > 0 else T("خاسرة", "Losing")
    )

# --- تبويب ٨: الصراط ---
with tabs[7]:
    st.header(T("📐 هندسة الصراط", "📐 Path Geometry"))
    st.markdown(T(
        "الصراط المستقيم هو المسار الذي تبقى فيه جميع المستويات في أعلى قيمها. "
        "عندما تنهار أي قيمة (بالمعصية)، ينحني المسار. والتوبة تعيده إلى الاستقامة.",
        
        "The Straight Path is where all levels remain at their peak. "
        "When any value collapses (through sin), the path curves. Repentance straightens it."
    ))
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button(T("▶️ خطوة نحو الكمال", "▶️ Step Toward Perfection"), key="btn_path", use_container_width=True):
            levels = ["faith","worship","transactions","morals","enjoining","hudud","jihad"]
            chosen = random.choice(levels)
            current = getattr(st.session_state, f"path_{chosen}")[-1]
            new_val = min(1.0, current + 0.1)
            for l in levels:
                if l == chosen:
                    getattr(st.session_state, f"path_{l}").append(new_val)
                else:
                    getattr(st.session_state, f"path_{l}").append(getattr(st.session_state, f"path_{l}")[-1])
            # حساب W و B
            final_vals = {}
            for l in levels:
                final_vals[l] = getattr(st.session_state, f"path_{l}")[-1]
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            st.rerun()
    
    with c2:
        sin_str = st.slider(T("⚡ شدة المعصية", "⚡ Sin Strength"), 0.01, 0.3, 0.1, 0.01, key="sin_path")
        if st.button(T("⚠️ معصية", "⚠️ Sin"), key="btn_sin", use_container_width=True):
            levels = ["faith","worship","transactions","morals","enjoining","hudud","jihad"]
            chosen = random.choice(levels)
            current = getattr(st.session_state, f"path_{chosen}")[-1]
            new_val = max(0.01, current - sin_str * random.uniform(0.5, 1.0))
            for l in levels:
                if l == chosen:
                    getattr(st.session_state, f"path_{l}").append(new_val)
                else:
                    getattr(st.session_state, f"path_{l}").append(getattr(st.session_state, f"path_{l}")[-1])
            final_vals = {}
            for l in levels:
                final_vals[l] = getattr(st.session_state, f"path_{l}")[-1]
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            st.rerun()
    
    with c3:
        if st.button(T("🕌 توبة نصوح", "🕌 Sincere Repentance"), key="btn_rep", use_container_width=True):
            for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
                current = getattr(st.session_state, f"path_{l}")[-1]
                new_val = min(1.0, current + 0.8 * (1.0 - current))
                getattr(st.session_state, f"path_{l}").append(new_val)
            final_vals = {}
            for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
                final_vals[l] = getattr(st.session_state, f"path_{l}")[-1]
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(0.0)
            st.rerun()
    
    if st.button(T("🔄 إعادة الرحلة", "🔄 Reset Path"), key="btn_reset_path", use_container_width=True):
        for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
            setattr(st.session_state, f"path_{l}", [0.5])
        st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
        st.session_state.path_kappa = [0.0]
        st.rerun()
    
    # رسم المسار
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
    
    ax1 = axes[0]
    ax1.set_facecolor('#0a0f1e')
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_xlabel("B (البراءة)", color='white'); ax1.set_ylabel("W (الولاء)", color='white')
    ax1.set_title(T("مسارك في فضاء (W, B)", "Your Path in (W, B) Space"), color='white', fontsize=13)
    
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=2.5, alpha=0.7, label=T("الصراط المستقيم", "Straight Path"))
    ax1.scatter([1], [1], s=120, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, label=T("الكمال (1,1)", "Perfection (1,1)"))
    
    pW = st.session_state.path_W; pB = st.session_state.path_B
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.path_kappa[i] if i < len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2 if kv < 0.05 else 3)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label=T("البداية", "Start"))
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label=T("الآن", "Now"))
    
    ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
    
    ax2 = axes[1]
    ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.path_kappa, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label=T("حد الخطر", "Danger"))
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label=T("الصراط", "Straight"))
    ax2.set_title(T("منحنى الانحناء (κ)", "Curvature Over Time"), color='white', fontsize=13)
    ax2.set_xlabel(T("الخطوات", "Steps"), color='white'); ax2.set_ylabel("κ", color='white')
    ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
    max_kappa = max(st.session_state.path_kappa) if st.session_state.path_kappa else 0.1
    ax2.set_ylim(-0.01, max(0.2, max_kappa * 1.2))
    
    plt.tight_layout(); st.pyplot(fig)
    
    # مؤشرات المستويات
    st.divider()
    st.subheader(T("📊 المستويات الحية", "📊 Live Levels"))
    
    cols = st.columns(7)
    levels_labels = [
        ("faith", T("الإيمان", "Faith"), '#FFD700'),
        ("worship", T("العبادات", "Worship"), '#FFA500'),
        ("transactions", T("المعاملات", "Transactions"), '#00FF88'),
        ("morals", T("الأخلاق", "Morals"), '#FF69B4'),
        ("enjoining", T("الأمر والنهي", "Enjoining"), '#00BFFF'),
        ("hudud", T("الحدود", "Limits"), '#FF6347'),
        ("jihad", T("الجهاد", "Jihad"), '#FF4500'),
    ]
    
    for i, (key, label, color) in enumerate(levels_labels):
        val = getattr(st.session_state, f"path_{key}")[-1]
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:6px;background:rgba(20,30,60,0.8);border-radius:6px;border:1px solid {color};">
                <p style="color:{color};font-size:0.6em;margin:0;">{label}</p>
                <p style="color:white;font-size:0.9em;margin:0;font-weight:bold;">{val:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # مؤشرات المسار
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("W (الولاء)", f"{pW[-1]:.3f}")
    c2.metric("B (البراءة)", f"{pB[-1]:.3f}")
    current_kappa = st.session_state.path_kappa[-1] if st.session_state.path_kappa else 0.0
    c3.metric("κ (الانحناء)", f"{current_kappa:.4f}")
    on_path = current_kappa < 0.03
    c4.metric(T("الصراط؟", "On Path?"), T("✅ نعم", "✅ YES") if on_path else T("⚠️ لا", "⚠️ NO"))

# ═══════════════════════════════════════════════════════════════
# التذييل
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.3em;">⚖️ مختبر الميزان</p>
    <p>{T('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>
    <p>S = W × B | ق = ١٠٠ = الحق = الميزان</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size:0.8em;margin-top:10px;">
        {T(
            'هذا المختبر شهادة رقمية على أن الله حق، وأن وعده حق، وأن لقاءه حق، وأن الجنة حق، وأن النار حق.',
            'This lab is a digital testimony that Allah is Truth, His promise is true, the meeting with Him is true, Paradise is true, and Hell is true.'
        )}
    </p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الخامسة والأخيرة مكتملة.")
print("✅✅✅ تم بناء مختبر الميزان – النسخة النهائية المتكاملة.")
