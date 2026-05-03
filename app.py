import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="الدين القيم – قانون التوازن الكوني", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# ====================== عنوان الصفحة ======================
st.markdown("""
<div style="text-align: center; padding: 25px 0 15px 0;">
    <span style="font-size: 60px;">⚖️</span>
    <h1 style="color: #FFD700; font-size: 2.5em; margin: 10px 0; font-weight: 900; letter-spacing: 3px; text-shadow: 0 0 15px rgba(255,215,0,0.5);">الدِّينُ الْقَيِّم</h1>
    <span style="font-size: 60px;">⚖️</span>
    <h2 style="color: #FFD700; font-size: 1.3em; margin-top: 0;">قَانُونُ التَّوَازُنِ الْكَوْنِيّ</h2>
    <p style="color: #CCCCCC; font-size: 18px; margin: 10px 0 0 0; letter-spacing: 2px;">S = W × B | نظرية الميزان</p>
    <p style="color: #FFD700; font-size: 20px; font-weight: bold; margin: 15px 0 0 0;">علي عادل العاطفي</p>
    <p style="color: #FFD700; font-size: 13px; margin: 0; font-style: italic; opacity: 0.8;">Ali Adel Alatifi | 2026</p>
</div>
""", unsafe_allow_html=True)

# ====================== رسالة الترحيب ======================
with st.expander("📜 رسالة الترحيب – افتح للقراءة", expanded=False):
    st.markdown("""
    <div style="text-align: center; font-size: 1.05em; line-height: 2.2; color: #CCCCCC;">

    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
    > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"

    ---

    <b>الدين القيم</b> = قانون السببية الكوني، وهو الحق لأن واضعه الحق،
    وهو القيم لأنه من القيوم نفسه. هو القانون الأعظم، إنه "الدين القيم"
    الذي هو أصل الوجود وغايته. إنه القانون الذي أزال الله به العدم،
    وأوجد به الخلق، وأجرى به السنن، وسيكون به الجزاء.

    إنه <b>"الميزان"</b> الذي قامت به السماوات والأرض،
    والذي يدور حوله كل شيء، من الأزل إلى الخلود.

    ---

    <div style="font-size: 1.1em; color: #FFD700; line-height: 2.5; text-align: center;">
    <b>
    ﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ وَلَهُ أَسْلَمَ مَن فِي السَّمَاوَاتِ وَالْأَرْضِ طَوْعًا وَكَرْهًا وَإِلَيْهِ يُرْجَعُونَ﴾
    <br>— آل عمران 83
    </b>
    </div>

    ---

    > "أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.<br>
    > استقراركم ليس صدفة. انهياركم ليس حظاً سيئاً.<br>
    > إنها معادلة. إنها <b style="color: #FFD700;">S = W × B</b>."

    ---

    المشهد المتكامل الذي يجمع كل شيء في آن واحد:
    من الذرة إلى المجرة، ومن الفيزياء إلى الأخلاق،
    ومن الفرد إلى الحضارة – كله يسير بقانون واحد هو
    <b style="color: #FFD700;">S = W × B</b>. 🌌

    ---

    <b>الدين القيم</b> = القانون الإلهي الذي يسري على كل شيء من الأزل إلى الخلود.<br>
    <b>الإسلام</b> = الاستجابة المثلى للقانون الإلهي من خلال توازن الولاء والبراءة،
    كل مخلوق بما يناسب فطرته = الثبات والاستقرار في كل شيء.

    ---

    <div style="font-size: 1.1em; color: #FFD700; line-height: 2.5; text-align: center;">
    <b>
    ﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ
    لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ وَلَٰكِنَّ أَكْثَرَ النَّاسِ لَا يَعْلَمُونَ﴾
    <br>— الروم 30
    </b>
    </div>

    ---

    <div style="text-align: center; font-size: 1.15em; color: #FFD700; line-height: 2.8;">
        ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ — الرحمن 7<br>
        ﴿وَأَنزَلْنَا مَعَهُمُ الْكِتَابَ وَالْمِيزَانَ﴾ — الحديد 25<br>
        ﴿اللَّهُ الَّذِي أَنزَلَ الْكِتَابَ بِالْحَقِّ وَالْمِيزَانَ﴾ — الشورى 17
    </div>

    </div>
    """, unsafe_allow_html=True)

# ====================== الشريط الجانبي ======================
with st.sidebar:
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
    st.subheader("⚠️ الأمراض الأخلاقية")
    riba = st.slider("💸 الربا", 0.0, 1.0, 0.2, 0.01)
    ghish = st.slider("🎭 الغش", 0.0, 1.0, 0.2, 0.01)
    kadhib = st.slider("🤥 الكذب", 0.0, 1.0, 0.2, 0.01)
    st.subheader("⚙️ معاملات")
    W_init = st.slider("W الابتدائي", 0.0, 1.0, 0.55, 0.01)
    B_init = st.slider("B الابتدائي", 0.0, 1.0, 0.52, 0.01)
    N_STARS = st.slider("النجوم", 100, 600, 300, 50)
    cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001,
                            help="يحدد سرعة تحديث المحاكاة (ثواني). كلما قلت القيمة زادت السرعة.")
    delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1,
                             help="عدد الخطوات التي يتأخر فيها التمكين (E) عن الاستقرار (S)، لمحاكاة الاستدراج.")
    c1, c2, c3 = st.columns(3)
    if c1.button("▶️ تشغيل", use_container_width=True): st.session_state.run = True
    if c2.button("⏹️ إيقاف", use_container_width=True): st.session_state.run = False
    if c3.button("🔄 إعادة ضبط", use_container_width=True):
        st.session_state.init = False
        st.rerun()

    # ---- دليل القراءة ----
    with st.expander("❓ كيف تقرأ المشهد؟"):
        st.markdown("""
        - **كل نقطة**: كيان (فرد أو مجتمع صغير).
        - **اللون الذهبي**: توازن عالٍ (W وB مرتفعان).
        - **اللون الأحمر**: انزياح نحو البراءة فقط (B عالٍ، W منخفض).
        - **اللون الرمادي/الأبيض**: انزياح نحو الولاء فقط (W عالٍ، B منخفض).
        - **اللون البرتقالي/الباهت**: منطقة الخطر (كلاهما منخفض).
        - **تجمع النقاط حول المركز**: تماسك وتوازن.
        - **تباعد النقاط**: خلل واضطراب.
        - **الدوائر المتوهجة حول المركز**: قوة الاستقرار S.
        - **القرص السماوي المتسع**: التمكين E.
        - **النص العائم في الخلفية**: تحذير في حالة الاستدراج أو التعافي.
        """)

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

def check_warnings(W, B, S, E, ph):
    w = []
    if E > S * 1.5: w.append("⚠️ فجوة استدراج خطيرة")
    elif E > S * 1.2: w.append("⚡ بداية استدراج")
    if abs(W - B) > 0.3: w.append("⚖️ اختلال كبير")
    elif abs(W - B) > 0.2: w.append("📊 ميلان")
    if S < 0.2: w.append("🔴 خطر الانهيار")
    elif S < 0.3: w.append("🟠 حالة حرجة")
    if 'ISTIDRAJ' in ph: w.append("💀 استدراج نشط")
    elif 'RECOVERY' in ph: w.append("🌱 مرحلة تعافي")
    return w

# ====================== التهيئة ======================
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False
if not st.session_state.init:
    try:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        st.session_state.cx = cx; st.session_state.cy = cy
        st.session_state.sx = np.random.uniform(cx - 13, cx + 13, N_STARS)
        st.session_state.sy = np.random.uniform(cy - 9, cy + 9, N_STARS)
        st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.W = W_init; st.session_state.B = B_init
        st.session_state.E = 0.3; st.session_state.S = W_init * B_init
        st.session_state.ph = "Balance"; st.session_state.ca = 0.0
        st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5; st.session_state.aa = 0.0
        st.session_state.eb = deque([W_init * B_init] * 30, maxlen=30)
        st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
        st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
        st.session_state.init = True
    except Exception as e:
        st.error(f"خطأ: {str(e)}")
        st.session_state.init = False

# ====================== العدادات ======================
if st.session_state.init:
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"<p style='text-align:center;color:#FFD700;font-size:36px;margin:0;font-weight:bold;'>{st.session_state.S:.3f}</p>", unsafe_allow_html=True)
    m1.markdown("<p style='text-align:center;color:white;font-size:18px;margin:0;'>⚖️ استقرار (S)</p>", unsafe_allow_html=True)
    m2.markdown(f"<p style='text-align:center;color:#FFFFFF;font-size:36px;margin:0;font-weight:bold;'>{st.session_state.W:.3f}</p>", unsafe_allow_html=True)
    m2.markdown("<p style='text-align:center;color:white;font-size:18px;margin:0;'>🤍 ولاء (W)</p>", unsafe_allow_html=True)
    m3.markdown(f"<p style='text-align:center;color:#FF3333;font-size:36px;margin:0;font-weight:bold;'>{st.session_state.B:.3f}</p>", unsafe_allow_html=True)
    m3.markdown("<p style='text-align:center;color:white;font-size:18px;margin:0;'>❤️ براءة (B)</p>", unsafe_allow_html=True)
    m4.markdown(f"<p style='text-align:center;color:#00FFFF;font-size:36px;margin:0;font-weight:bold;'>{st.session_state.E:.3f}</p>", unsafe_allow_html=True)
    m4.markdown("<p style='text-align:center;color:white;font-size:18px;margin:0;'>💫 تمكين (E)</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    warns = check_warnings(st.session_state.W, st.session_state.B, st.session_state.S, st.session_state.E, st.session_state.ph)
    if warns: st.error(" | ".join(warns))
    else: st.success("✅ النظام في حالة توازن تام")

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

            # ---------- المشهد الكوني ----------
            fig, ax = plt.subplots(figsize=(20, 15), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'), (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=22, ha='center', va='center', fontweight='bold')
            ax.text(cx, cy - 2.8, f'S={S:.2f}', color='#FFD700', fontsize=14, ha='center')
            ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#00FFFF', alpha=0.25 * (1 - min(E, 1)) + 0.04, zorder=7))
            ax.add_patch(Circle((cx, cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=3, zorder=2))
            for r in [10.0, 11.5, 13.0]: ax.add_patch(Circle((cx, cy), r, color='#FFD700', alpha=0.03, fill=False, lw=0.8, ls=':'))
            for i in range(6):
                an = -np.pi / 4 + i * (np.pi / 2) / 5
                ax.add_patch(Circle((cx + 8.5 * np.cos(an), cy + 8.5 * np.sin(an)), 0.5, color='#FFF', alpha=0.3 + 0.5 * avgW, zorder=8))
            for i in range(6):
                an = np.pi - np.pi / 4 + i * (np.pi / 2) / 5
                ax.add_patch(Circle((cx + 8.5 * np.cos(an), cy + 8.5 * np.sin(an)), 0.5, color='#F33', alpha=0.25 + 0.35 * avgB, zorder=8))
            ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy + 1.0, 'W', color='#FFF', fontsize=14, ha='center')
            ax.text(bx, by + 1.0, 'B', color='#F33', fontsize=14, ha='center')
            colors = [get_color(sw[i], sb[i]) for i in range(n)]
            ax.scatter(sx, sy, s=50, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)
            aa += 0.12; er = 0.5 + 0.4 * S
            ax.add_patch(Circle((3.5, 4.0), 0.2 + 0.3 * S, color='#4488FF', alpha=0.8, zorder=7))
            ax.add_patch(Circle((3.5 + er * np.cos(aa), 4.0 + er * np.sin(aa)), 0.06, color='white', alpha=0.95, zorder=8))
            ax.text(3.5, 2.5, '⚛️ ذرة', color='#4488FF', fontsize=10, ha='center')
            chem_x, chem_y = 9.5, 4.0
            ax.add_patch(RegularPolygon((chem_x, chem_y), numVertices=6, radius=0.4 + 0.3 * S, orientation=np.pi / 6, facecolor='#FFA500', alpha=0.7, zorder=7))
            ax.text(chem_x, chem_y - 1.2, '🧪 جزيء', color='#FFA500', fontsize=10, ha='center')
            ax.add_patch(Circle((24.5, 4.0), 0.4 + 0.5 * S, color='#00FF88', alpha=0.35, zorder=7, ec='#00FF88', lw=1.5))
            ax.add_patch(Circle((24.5, 4.0), 0.15 + 0.2 * S, color='white', alpha=0.8, zorder=8))
            ax.text(24.5, 2.5, '🧫 خلية', color='#00FF88', fontsize=10, ha='center')
            mx, my, bw, bh = 0.5, 16.5, 4.0, 0.6
            ax.add_patch(FancyBboxPatch((mx, my), bw, bh, boxstyle="round,pad=0.2", facecolor='#1a1a2e', alpha=0.9, zorder=20))
            if W > 0: ax.add_patch(FancyBboxPatch((mx, my), W * bw / 2, bh, boxstyle="round,pad=0.1", facecolor='#FFF', alpha=0.9, zorder=21))
            if B > 0: ax.add_patch(FancyBboxPatch((mx + bw / 2, my), B * bw / 2, bh, boxstyle="round,pad=0.1", facecolor='#F33', alpha=0.9, zorder=21))
            if W + B > 0: ax.plot(mx + (W / (W + B)) * bw, my + bh / 2, 'v', color='#FFD700', markersize=15, markeredgecolor='white', zorder=22)
            # تحسين لون النص مع مربعات دلالة
            ax.text(mx, my - 0.8, f'W={W:.2f}', color='white', fontsize=10, ha='center',
                    bbox=dict(facecolor='black', alpha=0.6, edgecolor='white', boxstyle='round,pad=0.1'))
            ax.text(mx + bw, my - 0.8, f'B={B:.2f}', color='#F33', fontsize=10, ha='center',
                    bbox=dict(facecolor='black', alpha=0.6, edgecolor='#F33', boxstyle='round,pad=0.1'))
            ax.text(mx + bw / 2, my + bh + 0.8, '⚖️ الميزان', color='#FFD700', fontsize=12, ha='center', fontweight='bold')

            # نص تحذيري كبير في الخلفية عند الاستدراج أو التعافي
            if '>> استدراج <<' in ph:
                ax.text(14, 10, '⚠️ استدراج', fontsize=70, color='red', alpha=0.1, ha='center', va='center', fontweight='bold')
            elif '>> تعافي <<' in ph:
                ax.text(14, 10, '🌱 تعافي', fontsize=70, color='green', alpha=0.1, ha='center', va='center', fontweight='bold')

            # لوحة الإثبات (مكبرة قليلاً)
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            if pSl:
                pax = ax.inset_axes([0.45, 0.02, 0.50, 0.18])   # زيادة الارتفاع
                pax.set_xlim(0, max(400, len(pxl))); pax.set_ylim(0, 1.05)
                pax.set_title('📈 لوحة الإثبات: S يقود E (الاستدراج)', color='white', fontsize=10, fontweight='bold')
                pax.tick_params(colors='white', labelsize=7); pax.grid(True, alpha=0.3)
                pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S (الاستقرار)')
                pax.plot(pxl, pEl, color='#00FFFF', lw=2, alpha=0.9, label='E (التمكين)')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=8)

            # خريطة الحرارة بشكل مباشر (بدلاً من الصورة)
            heat_ax = ax.inset_axes([0.02, 0.02, 0.25, 0.22])
            wr, br = np.linspace(0, 1, 30), np.linspace(0, 1, 30)
            Wg, Bg = np.meshgrid(wr, br)
            heat_ax.pcolormesh(Wg, Bg, Wg * Bg, cmap='RdYlGn', shading='auto', vmin=0, vmax=1)
            heat_ax.scatter(sw, sb, c='white', s=1, alpha=0.5)   # نقاط صغيرة لمواقع النجوم
            heat_ax.set_xlabel('W', color='white', fontsize=8); heat_ax.set_ylabel('B', color='white', fontsize=8)
            heat_ax.set_title('S = W × B', color='white', fontsize=9, fontweight='bold')
            heat_ax.tick_params(colors='white', labelsize=6); heat_ax.set_xlim(0, 1); heat_ax.set_ylim(0, 1)

            ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=16, ha='center', fontweight='bold')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            buf = BytesIO(); fig.savefig(buf, format='png', dpi=120, facecolor='#000010'); buf.seek(0)
            st.session_state.latest_image = buf; plt.close(fig)

            # استخدام سرعة الدورة الفعلية
            time.sleep(max(0.01, cycle_speed))
        except Exception as e:
            st.error(f"خطأ: {str(e)}")
            st.session_state.run = False
            break
    st.success("⏸️ تم إيقاف المحاكاة")
elif st.session_state.init and 'latest_image' in st.session_state:
    st.image(st.session_state.latest_image, caption="آخر حالة للمحاكاة", use_column_width=True)

if 'latest_image' in st.session_state:
    st.sidebar.download_button("📥 تحميل صورة المشهد", st.session_state.latest_image, "mizan_scene.png", "image/png")

st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;'>© 2026 علي عادل العاطفي | v11.0 – الدِّينُ الْقَيِّم – قَانُونُ التَّوَازُنِ الْكَوْنِيّ</p>", unsafe_allow_html=True)
