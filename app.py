import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
import random
import time
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# =============================================
# ⚖️ الدِّينُ الْقَيِّم – قَانُونُ التَّوَازُنِ الْكَوْنِيّ
# S = W × B | W = الولاء | B = البراءة
# Author: Ali Adel Alatifi | علي عادل العاطفي
# =============================================

st.set_page_config(
    page_title="الدين القيم – قانون التوازن الكوني",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# 🏛️ رأس الصفحة – العنوان الجليل
# =============================================
st.markdown("""
<div style="text-align: center; padding: 20px 0 10px 0;">
    <h1 style="color: #FFD700; font-size: 2.5em; margin-bottom: 0;">⚖️ الدِّينُ الْقَيِّم ⚖️</h1>
    <h2 style="color: #FFD700; font-size: 1.3em; margin-top: 0;">قَانُونُ التَّوَازُنِ الْكَوْنِيّ</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =============================================
# 📜 رسالة الترحيب – النص الفلسفي المتكامل
# =============================================
with st.expander("📜 رسالة الترحيب – افتح للقراءة", expanded=True):
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">

        > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
        > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"

        ---

        **الدين القيم** = قانون السببية الكوني، وهو الحق لأن واضعه الحق،
        وهو القيم لأنه من القيوم نفسه. هو القانون الأعظم، إنه "الدين القيم"
        الذي هو أصل الوجود وغايته. إنه القانون الذي أزال الله به العدم،
        وأوجد به الخلق، وأجرى به السنن، وسيكون به الجزاء.

        إنه **"الميزان"** الذي قامت به السماوات والأرض،
        والذي يدور حوله كل شيء، من الأزل إلى الخلود.

        ---

        <div style="font-size: 1.2em; color: #FFD700; line-height: 2.5; text-align: center;">
        <b>
        ﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ وَلَهُ أَسْلَمَ مَن فِي السَّمَاوَاتِ وَالْأَرْضِ طَوْعًا وَكَرْهًا وَإِلَيْهِ يُرْجَعُونَ﴾
        <br>— آل عمران 83
        </b>
        </div>

        ---

        التوازن والانهيار، السقوط والصمود، الثبات والاستقرار:
        في الذرة والمجرة، في المادة والروح، في الفرد والحضارة،
        في الفيزياء والكيمياء والبيولوجيا والأخلاق –
        هو نتيجة حتمية لمدى **الإسلام**،
        أي الاستجابة للقانون الكوني "الدين القيم"،
        من خلال تحقيق توازن الولاء والبراءة،
        كلٌّ بما يناسب فطرته.

        ---

        <div style="font-size: 1.2em; color: #FFD700; line-height: 2.5; text-align: center;">
        <b>
        ﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ
        لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ وَلَٰكِنَّ أَكْثَرَ النَّاسِ لَا يَعْلَمُونَ﴾
        <br>— الروم 30
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
        <b style="color: #FFD700;">S = W × B</b>.

        ---

        **الدين القيم** = القانون الإلهي الذي يسري على كل شيء من الأزل إلى الخلود.

        **الإسلام** = الاستجابة المثلى للقانون الإلهي من خلال توازن الولاء والبراءة،
        كل مخلوق بما يناسب فطرته = الثبات والاستقرار في كل شيء،
        من الذرة إلى المجرة.

        ---

        <b style="color: #FFD700;">Ali Adel Alatifi | علي عادل العاطفي | 2026</b>

        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =============================================
# 📖 الآيات القرآنية – الميزان في الوحي
# =============================================
st.markdown("""
<div style="text-align: center; font-size: 1.2em; color: #FFD700; line-height: 2.5;">
    ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ — الرحمن 7<br>
    ﴿وَأَنزَلْنَا مَعَهُمُ الْكِتَابَ وَالْمِيزَانَ﴾ — الحديد 25<br>
    ﴿اللَّهُ الَّذِي أَنزَلَ الْكِتَابَ بِالْحَقِّ وَالْمِيزَانَ﴾ — الشورى 17
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =============================================
# 🎛️ الشريط الجانبي – كل المتغيرات
# =============================================
st.sidebar.header("🎛️ معاملات المحاكاة")

st.sidebar.subheader("🕌 أركان الإسلام / القوى الأساسية")
prayer_strength = st.sidebar.slider("🟣 الصلاة (النووية القوية)", 0.0, 1.0, 0.8, 0.01)
zakat_strength = st.sidebar.slider("🟡 الزكاة (الكهرومغناطيسية)", 0.0, 1.0, 0.6, 0.01)
fasting_strength = st.sidebar.slider("🟠 الصوم (النووية الضعيفة)", 0.0, 1.0, 0.7, 0.01)
hajj_strength = st.sidebar.slider("🔵 الحج (الجاذبية)", 0.0, 1.0, 0.5, 0.01)

st.sidebar.divider()
st.sidebar.subheader("🏛️ أسس الحكم")
amr_marouf = st.sidebar.slider("📢 الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01)
nahy_munkar = st.sidebar.slider("🚫 النهي عن المنكر", 0.0, 1.0, 0.5, 0.01)
adl_strength = st.sidebar.slider("⚖️ العدل", 0.0, 1.0, 0.6, 0.01)
shura_strength = st.sidebar.slider("🤝 الشورى", 0.0, 1.0, 0.5, 0.01)

st.sidebar.divider()
st.sidebar.subheader("🛡️ آليات الإصلاح")
taawun_birr = st.sidebar.slider("🤝 التعاون على البر", 0.0, 1.0, 0.5, 0.01)
taawun_taqwa = st.sidebar.slider("🤝 التعاون على التقوى", 0.0, 1.0, 0.5, 0.01)
tawasi_haqq = st.sidebar.slider("💬 التواصي بالحق", 0.0, 1.0, 0.5, 0.01)
tawasi_sabr = st.sidebar.slider("⏳ التواصي بالصبر", 0.0, 1.0, 0.5, 0.01)

st.sidebar.divider()
st.sidebar.subheader("💀 آليات الإفساد")
nahy_marouf_e = st.sidebar.slider("🔇 النهي عن المعروف", 0.0, 1.0, 0.2, 0.01)
amr_munkar_e = st.sidebar.slider("👿 الأمر بالمنكر", 0.0, 1.0, 0.2, 0.01)
taawun_ithm = st.sidebar.slider("🤝 التعاون على الإثم", 0.0, 1.0, 0.2, 0.01)
taawun_udwan = st.sidebar.slider("🤝 التعاون على العدوان", 0.0, 1.0, 0.2, 0.01)
tawasi_batil = st.sidebar.slider("💬 التواصي بالباطل", 0.0, 1.0, 0.2, 0.01)
adam_sabr = st.sidebar.slider("😤 عدم الصبر", 0.0, 1.0, 0.2, 0.01)

st.sidebar.divider()
st.sidebar.subheader("⚠️ الأمراض الأخلاقية")
riba_strength = st.sidebar.slider("💸 الربا", 0.0, 1.0, 0.2, 0.01)
ghish_strength = st.sidebar.slider("🎭 الغش", 0.0, 1.0, 0.2, 0.01)
kadhib_strength = st.sidebar.slider("🤥 الكذب", 0.0, 1.0, 0.2, 0.01)

st.sidebar.divider()
st.sidebar.subheader("⚙️ معاملات عامة")
W_init = st.sidebar.slider("W (الولاء) الابتدائي", 0.0, 1.0, 0.55, 0.01)
B_init = st.sidebar.slider("B (البراءة) الابتدائية", 0.0, 1.0, 0.52, 0.01)
cycle_speed = st.sidebar.slider("سرعة الدورة الحضارية", 0.001, 0.05, 0.01, 0.001)
delay_frames = st.sidebar.slider("تأخير التمكين (الاستدراج)", 5, 50, 22, 1)
N_STARS = st.sidebar.slider("عدد النجوم (الأفراد)", 100, 600, 300, 50)
HALO_MAX = st.sidebar.slider("أقصى نصف قطر للهالة E", 8.0, 20.0, 16.0, 0.5)
seed_val = st.sidebar.number_input("بذرة عشوائية (0 = عشوائي)", 0, 9999, 42)

c1, c2, c3 = st.sidebar.columns(3)
if c1.button("▶️ تشغيل"): st.session_state.run = True
if c2.button("⏹️ إيقاف"): st.session_state.run = False
if c3.button("🔄 إعادة ضبط"):
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

download_placeholder = st.sidebar.empty()

# =============================================
# دوال مساعدة
# =============================================
def get_mizan_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#FFFFFF'
    elif w < 0.45 and b >= 0.55: return '#FF3333'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    else:
        if w > b: return '#FFF8DC'
        elif b > w: return '#FFA07A'
        else: return '#FFBF00'

mizan_cmap = LinearSegmentedColormap.from_list('mizan', 
    ['#000000', '#FFB6C1', '#FF4444', '#FFD700', '#FFF8DC', '#FFFFFF'])

def apply_ethics(sw, sb, neighbors_W, neighbors_B,
                 amr_marouf, nahy_munkar, taawun_birr, taawun_taqwa, tawasi_haqq, tawasi_sabr,
                 nahy_marouf_e, amr_munkar_e, taawun_ithm, taawun_udwan, tawasi_batil, adam_sabr):
    w_boost = 0.0; b_boost = 0.0
    resistance_w = 0.0; resistance_b = 0.0

    w_boost += amr_marouf * 0.015; b_boost += nahy_munkar * 0.015
    if neighbors_W > 0.5: w_boost += taawun_birr * 0.02
    if neighbors_B > 0.5: b_boost += taawun_taqwa * 0.02
    resistance_w += tawasi_haqq * 0.1; resistance_b += tawasi_sabr * 0.1

    w_boost -= nahy_marouf_e * 0.015; b_boost -= amr_munkar_e * 0.015
    if neighbors_W < 0.5: w_boost -= taawun_ithm * 0.02
    if neighbors_B < 0.5: b_boost -= taawun_udwan * 0.02
    resistance_w -= tawasi_batil * 0.1; resistance_b -= adam_sabr * 0.1

    resistance_w = max(0, resistance_w); resistance_b = max(0, resistance_b)
    sw += w_boost; sb += b_boost
    return sw, sb, resistance_w, resistance_b

def calculate_S_full(W, B, E, prayer, zakat, fasting, hajj, 
                     amr, nahy, adl, shura, riba, ghish, kadhib):
    S_base = W * B
    pillars_boost = (prayer + zakat + fasting + hajj) / 4
    S_base *= (0.5 + 0.5 * pillars_boost)
    protection = (amr * W + nahy * B) / 2
    S_base *= (0.8 + 0.4 * protection)
    S_base *= (0.9 + 0.2 * adl)
    S_base *= (0.85 + 0.3 * shura)
    if E > S_base:
        riba_effect = riba * (E - S_base) * 0.3
        S_base -= riba_effect
    W_weakened = W * (1 - kadhib * 0.2)
    S_final = W_weakened * B
    S_final *= (0.5 + 0.5 * pillars_boost)
    S_final *= (0.8 + 0.4 * protection)
    S_final *= (0.9 + 0.2 * adl)
    S_final *= (0.85 + 0.3 * shura)
    return np.clip(S_final, 0.001, 1.0)

# =============================================
# تهيئة الحالة
# =============================================
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False

if not st.session_state.run and not st.session_state.init:
    st.info("""
    ### 👋 مرحباً في مختبر الميزان التفاعلي النهائي!
    
    اضبط المعاملات في الشريط الجانبي ثم اضغط **▶️ تشغيل**.
    
    **النجوم** هي المحرك الأول. ألوانها تعكس درجة توازنها:
    - 🟡 **ذهبي** = توازن وثبات (S ≥ 0.55)
    - ⚪ **أبيض** = ولاء دون براءة
    - 🔴 **أحمر** = براءة دون ولاء
    - 🩷 **وردي** = تذبذب (لا ولاء ولا براءة)
    """)

if not st.session_state.init:
    seed = seed_val if seed_val > 0 else random.randint(1, 9999)
    np.random.seed(seed); random.seed(seed)
    
    cx, cy, mr = 14, 10.0, 8.5
    
    st.session_state.cx = cx; st.session_state.cy = cy; st.session_state.mr = mr
    st.session_state.sx = np.random.uniform(cx-13, cx+13, N_STARS)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, N_STARS)
    st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.res_w = np.zeros(N_STARS)
    st.session_state.res_b = np.zeros(N_STARS)
    st.session_state.W = W_init; st.session_state.B = B_init
    st.session_state.E = 0.3; st.session_state.S = W_init * B_init
    st.session_state.K = 0.4; st.session_state.H = 40.0; st.session_state.Sy = 70.0
    st.session_state.ph = "Balance"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5
    st.session_state.aa = 0.0; st.session_state.eb = [W_init * B_init] * 30
    st.session_state.pS = []; st.session_state.pE = []; st.session_state.px = []
    st.session_state.pc = 0; st.session_state.hd = []
    st.session_state.init = True

# =============================================
# المحاكاة الحية
# =============================================
if st.session_state.run:
    placeholder = st.empty()
    progress_text = st.empty()

    while st.session_state.run:
        W = st.session_state.W; B = st.session_state.B
        E = st.session_state.E; S = st.session_state.S
        K = st.session_state.K; H = st.session_state.H
        Sy = st.session_state.Sy; ph = st.session_state.ph
        ca = st.session_state.ca; aW = st.session_state.aW
        aB = st.session_state.aB; aa = st.session_state.aa
        eb = st.session_state.eb
        sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
        sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
        res_w = st.session_state.res_w.copy(); res_b = st.session_state.res_b.copy()
        cx = st.session_state.cx; cy = st.session_state.cy; mr = st.session_state.mr
        pS = st.session_state.pS.copy(); pE = st.session_state.pE.copy()
        px = st.session_state.px.copy(); pc = st.session_state.pc

        ca += cycle_speed
        sin_val = np.sin(ca)
        if sin_val > 0.5: ph = 'Peak Stability'
        elif sin_val > 0: ph = 'Rising'
        elif sin_val > -0.5: ph = 'Collapsing'
        else: ph = 'Rock Bottom'
        if 0.3 < sin_val < 0.35: ph = '>> ISTIDRAJ <<'
        if -0.35 < sin_val < -0.3: ph = '>> RECOVERY <<'

        target_S = 0.5 + 0.45 * sin_val

        for i in range(N_STARS):
            w_boost = prayer_strength * 0.01 + hajj_strength * 0.005
            b_boost = fasting_strength * 0.01 + zakat_strength * 0.005
            
            dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
            close = (dist < 2.0) & (np.arange(N_STARS) != i)
            neighbors_W = np.mean(sw[close]) if np.any(close) else 0.5
            neighbors_B = np.mean(sb[close]) if np.any(close) else 0.5

            sw[i], sb[i], new_res_w, new_res_b = apply_ethics(
                sw[i], sb[i], neighbors_W, neighbors_B,
                amr_marouf, nahy_munkar, taawun_birr, taawun_taqwa, tawasi_haqq, tawasi_sabr,
                nahy_marouf_e, amr_munkar_e, taawun_ithm, taawun_udwan, tawasi_batil, adam_sabr
            )
            res_w[i] = new_res_w; res_b[i] = new_res_b
            
            sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + w_boost
            sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + b_boost
            
            shura_effect = 0.03 + shura_strength * 0.05
            if np.any(close):
                sw[i] += (np.mean(sw[close]) - sw[i]) * shura_effect
                sb[i] += (np.mean(sb[close]) - sb[i]) * shura_effect
            
            sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

        shock_prob = 0.005 * (1 - adl_strength * 0.8)
        if random.random() < shock_prob:
            affected = np.random.choice(N_STARS, size=int(N_STARS*0.3), replace=False)
            shock_w = random.uniform(0.5, 0.8); shock_b = random.uniform(0.5, 0.8)
            for idx in affected:
                effective_shock_w = 1 - (1 - shock_w) * (1 - res_w[idx])
                effective_shock_b = 1 - (1 - shock_b) * (1 - res_b[idx])
                sw[idx] *= effective_shock_w; sb[idx] *= effective_shock_b
        if random.random() < shock_prob:
            affected = np.random.choice(N_STARS, size=int(N_STARS*0.2), replace=False)
            sw[affected] = np.minimum(1.0, sw[affected] * 1.3)
            sb[affected] = np.minimum(1.0, sb[affected] * 1.2)

        avg_W = np.mean(sw); avg_B = np.mean(sb)
        avg_S_stars = np.mean(sw * sb)

        W += (avg_W - W) * 0.04; B += (avg_B - B) * 0.04
        W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
        
        S = calculate_S_full(W, B, E, prayer_strength, zakat_strength, fasting_strength, hajj_strength,
                             amr_marouf, nahy_munkar, adl_strength, shura_strength,
                             riba_strength, ghish_strength, kadhib_strength)

        eb.append(S)
        if len(eb) > 30: eb.pop(0)
        effective_delay = int(delay_frames * (1 + ghish_strength * 0.5))
        E_target = eb[-effective_delay] if len(eb) >= effective_delay else S
        E = E + 0.03 * (E_target - E)

        W = W - 0.01 * E + 0.02 / (S + 0.1)
        B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
        W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
        
        S = calculate_S_full(W, B, E, prayer_strength, zakat_strength, fasting_strength, hajj_strength,
                             amr_marouf, nahy_munkar, adl_strength, shura_strength,
                             riba_strength, ghish_strength, kadhib_strength)
        
        K = np.clip(K + 0.012 * (S - K), 0.01, 2.0)
        H += W * 0.10; Sy += (1 - B) * 0.10

        pc += 1
        if pc % 2 == 0:
            pS.append(S); pE.append(E); px.append(len(px))
            if len(px) > 400: pS.pop(0); pE.pop(0); px.pop(0)

        orbit_W = 7.0 - 2.5 * W; orbit_B = 5.0 - 1.5 * B
        speed = 0.02
        noise_W = random.uniform(-0.025, 0.025) * (1 - W)**2
        noise_B = random.uniform(-0.025, 0.025) * (1 - B)**2
        aW += speed + noise_W; aB += speed + noise_B
        wx = cx + orbit_W * np.cos(aW); wy = cy + orbit_W * np.sin(aW) * 0.7
        bx = cx + orbit_B * np.cos(aB); by = cy + orbit_B * np.sin(aB) * 0.7

        ins = 1 - avg_S_stars
        sx += np.random.uniform(-0.07, 0.07, N_STARS) * ins
        sy += np.random.uniform(-0.07, 0.07, N_STARS) * ins
        sx = np.clip(sx, cx-13, cx+13); sy = np.clip(sy, cy-9, cy+9)

        st.session_state.W = W; st.session_state.B = B
        st.session_state.E = E; st.session_state.S = S
        st.session_state.ph = ph; st.session_state.ca = ca
        st.session_state.aW = aW; st.session_state.aB = aB
        st.session_state.eb = eb
        st.session_state.sx = sx; st.session_state.sy = sy
        st.session_state.sw = sw; st.session_state.sb = sb
        st.session_state.res_w = res_w; st.session_state.res_b = res_b
        st.session_state.pS = pS; st.session_state.pE = pE
        st.session_state.px = px; st.session_state.pc = pc

        fig, ax_cosmic = plt.subplots(figsize=(16, 12), facecolor='#000010')
        ax_cosmic.set_xlim(0, 28); ax_cosmic.set_ylim(0, 20)
        ax_cosmic.axis('off')

        lc = [(0.5,0.98,'#FFFFFF'),(1.0,0.65,'#FFD700'),(1.7,0.30,'#FFD700'),
              (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]
        for r,a,c in lc:
            ax_cosmic.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
        ax_cosmic.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
        ax_cosmic.text(cx,cy-2.5,f'S={S:.2f}',color='#FFD700',fontsize=10,ha='center',fontweight='bold')

        ax_cosmic.add_patch(Circle((cx,cy), 0.5+HALO_MAX*E, color='#00FFFF', 
                                   alpha=0.25*(1-min(E,1))+0.04, zorder=7))
        ax_cosmic.add_patch(Circle((cx,cy), mr, color='#00FF88', alpha=0.15, fill=False, lw=2.5, zorder=2))
        for r in [10.0,11.5,13.0]:
            ax_cosmic.add_patch(Circle((cx,cy), r, color='#FFD700', alpha=0.03, fill=False, lw=0.6, ls=':', zorder=0))

        for i in range(6):
            an = -np.pi/4 + i*(np.pi/2)/5
            ax_cosmic.add_patch(Circle((cx+mr*np.cos(an), cy+mr*np.sin(an)), 0.4, 
                                       color='#FFFFFF', alpha=0.3+0.5*avg_W, zorder=8, ec='#FFD700', lw=1.8))
        for i in range(6):
            an = np.pi - np.pi/4 + i*(np.pi/2)/5
            ax_cosmic.add_patch(Circle((cx+mr*np.cos(an), cy+mr*np.sin(an)), 0.4, 
                                       color='#FF3333', alpha=0.25+0.35*avg_B, zorder=8, ec='#FF6666', lw=1.8))

        ax_cosmic.add_patch(Circle((wx,wy), 0.2+0.6*W, color='#FFFFFF', alpha=1.0, zorder=13, ec='#FFFFFF', lw=1.5))
        ax_cosmic.add_patch(Circle((bx,by), 0.2+0.6*B, color='#FF3333', alpha=0.8, zorder=13, ec='#FF4444', lw=1.5))
        ax_cosmic.text(wx,wy+0.8,'W',color='#FFFFFF',fontsize=10,ha='center',fontweight='bold')
        ax_cosmic.text(bx,by+0.8,'B',color='#FF3333',fontsize=10,ha='center',fontweight='bold')

        sc = [get_mizan_color(sw[i],sb[i]) for i in range(N_STARS)]
        ax_cosmic.
