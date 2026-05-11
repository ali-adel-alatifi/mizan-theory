import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import random
import time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════
# إعداد الصفحة
# ═══════════════════════════════════
st.set_page_config(
    page_title="مختبر الميزان – القانون الواحد",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════
# اللغة
# ═══════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(ar_text, en_text):
    return ar_text if LANG == "ar" else en_text

# ═══════════════════════════════════
# دوال الحساب الأساسية
# ═══════════════════════════════════
def get_star_color(w, b):
    """لون النجمة يعكس موقعها الوجودي في فضاء (W, B)."""
    if w >= 0.55 and b >= 0.55:
        return '#FFD700'      # ذهبي: مؤمن
    elif w >= 0.55 and b < 0.45:
        return '#E0E0E0'      # رمادي: ولاء بلا براءة
    elif w < 0.45 and b >= 0.55:
        return '#FF5252'      # أحمر: براءة بلا ولاء
    elif w < 0.45 and b < 0.45:
        return '#FFB6C1'      # وردي: منافق
    else:
        return '#888888'      # رمادي غامق: منطقة انتقالية

def classify_quadrant(W_val, B_val):
    """يصنف الإنسان أو الأمة إلى أحد الأرباع الوجودية الأربعة."""
    if W_val >= 0.5 and B_val >= 0.5:
        return ("believer", '#FFD700')
    elif W_val < 0.5 and B_val >= 0.5:
        return ("disbeliever", '#FF5252')
    elif W_val < 0.5 and B_val < 0.5:
        return ("hypocrite", '#FFB6C1')
    else:
        return ("polytheist", '#FFA500')

def compute_curvature(W_hist, B_hist):
    """يحسب انحناء المسار (κ) في فضاء (W, B). κ=0 يعني الصراط المستقيم."""
    if len(W_hist) < 3:
        return 0.0
    dW = np.gradient(W_hist)
    dB = np.gradient(B_hist)
    ddW = np.gradient(dW)
    ddB = np.gradient(dB)
    last = -1
    numerator = abs(dW[last] * ddB[last] - dB[last] * ddW[last])
    denominator = (dW[last]**2 + dB[last]**2 + 1e-10)**(1.5)
    return numerator / denominator

def calc_S(W, B, E, q_intensity=1.0):
    """المعادلة المركزية: S = W × B، مضخمة بمعامل الحق (ق)."""
    base = W * B
    divine_factor = 1.0 + q_intensity * 0.5
    return np.clip(base * divine_factor, 0.001, 1.0)

# ═══════════════════════════════════
# ثوابت كونية
# ═══════════════════════════════════
QAF_VALUE = 100      # ق = الحق = الميزان
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2

print("✅ المرحلة الأولى مكتملة: الأساسات والثوابت والدوال.")

# ═══════════════════════════════════
# الشريط الجانبي – لوحة القيادة
# ═══════════════════════════════════
with st.sidebar:
    st.markdown("### 🕋 لوحة القيادة")
    
    # اللغة
    lang_choice = st.radio("🌐 اللغة", ["العربية", "English"], index=0 if LANG == "ar" else 1)
    if (lang_choice == "English" and LANG == "ar") or (lang_choice == "العربية" and LANG == "en"):
        st.session_state.lang = "en" if lang_choice == "English" else "ar"
        st.rerun()
    
    st.markdown("---")
    
    # إعدادات عامة
    st.markdown("#### ⚙️ إعدادات عامة")
    W_global = st.slider(t("W (الولاء)", "W (Loyalty)"), 0.0, 1.0, 0.55, 0.01, key="w_global")
    B_global = st.slider(t("B (البراءة)", "B (Disavowal)"), 0.0, 1.0, 0.52, 0.01, key="b_global")
    lag_frames = st.slider(t("فجوة الاستدراج", "Istidraj Gap"), 5, 50, 25, 1, key="lag_global")
    q_intensity = st.slider(t("⚖️ ق (الميزان)", "⚖️ Q (Balance)"), 0.0, 1.0, 1.0, 0.01, key="q_global")
    
    st.markdown("---")
    
    # أزرار التحكم العامة
    if st.button(t("▶️ تشغيل المحاكاة", "▶️ Run Simulation"), use_container_width=True, type="primary"):
        st.session_state.run = True
    if st.button(t("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True):
        st.session_state.run = False
    if st.button(t("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",):
                del st.session_state[k]
        st.rerun()

# ═══════════════════════════════════
# العنوان الرئيسي
# ═══════════════════════════════════
st.markdown(f"""
<div style="text-align: center; padding: 30px 0 10px 0;">
    <h1 style="color: #FFD700; font-size: 3.5em; margin-bottom: 5px; font-weight: 900;
               text-shadow: 0 0 30px rgba(255, 215, 0, 0.5); letter-spacing: 3px;">
        ⚖️ {t('مختبر الميزان', 'The Mizan Lab')}
    </h1>
    <h2 style="color: #CCC; font-size: 1.4em; margin-top: 0;">
        {t('القانون الواحد: S = W × B', 'The One Law: S = W × B')}
    </h2>
    <p style="color: #888; font-size: 1.1em; margin-top: 8px;">
        {t('من الذرة إلى الحضارة، ومن الدنيا إلى الآخرة', 'From Atom to Civilization, From World to Hereafter')}
    </p>
    <p style="color: #FFD700; font-size: 0.9em; margin-top: 5px;">
        {t('ق = ١٠٠ = الحق = الميزان', 'Q = 100 = Truth = Balance')}
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════
# التبويبات الرئيسية
# ═══════════════════════════════════
tab_labels = [
    t("🌌 المشهد الكوني", "🌌 The Cosmic Scene"),
    t("🧍 مختبر الفرد", "🧍 Individual Lab"),
    t("👥 مختبر المجتمع", "👥 Society Lab"),
    t("🏛️ مختبر الدولة", "🏛️ State Lab"),
    t("🌍 مختبر الأمة", "🌍 Nation Lab"),
    t("🏰 مختبر الحضارات", "🏰 Civilizations Lab"),
    t("📊 لوحة النتائج", "📊 Results Dashboard"),
]

tabs = st.tabs(tab_labels)

# ═══════════════════════════════════
# تهيئة الجلسة العامة
# ═══════════════════════════════════
if 'run' not in st.session_state:
    st.session_state.run = False

if 'init_global' not in st.session_state:
    np.random.seed(42)
    random.seed(42)
    
    # للكون
    N_STARS = 250
    cx, cy = 14, 10.0
    st.session_state.cx = cx
    st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx - 13, cx + 13, N_STARS)
    st.session_state.sy = np.random.uniform(cy - 9, cy + 9, N_STARS)
    st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.star_W_hist = [deque([st.session_state.sw[i]], maxlen=50) for i in range(N_STARS)]
    st.session_state.star_B_hist = [deque([st.session_state.sb[i]], maxlen=50) for i in range(N_STARS)]
    
    # للكوكبين
    W_init = W_global
    B_init = B_global
    E_init = 0.3
    S_init = calc_S(W_init, B_init, E_init, q_intensity)
    st.session_state.W = W_init
    st.session_state.B = B_init
    st.session_state.E = E_init
    st.session_state.S = S_init
    st.session_state.planet_W_hist = deque([W_init], maxlen=50)
    st.session_state.planet_B_hist = deque([B_init], maxlen=50)
    
    # للدورة الحضارية
    st.session_state.phase = t("توازن", "Balance")
    st.session_state.cycle_angle = 0.0
    st.session_state.angle_W = 0.0
    st.session_state.angle_B = np.pi * 0.5
    
    # للاستدراج
    st.session_state.empowerment_buffer = deque([S_init] * 30, maxlen=30)
    
    # للتاريخ
    st.session_state.history_S = deque(maxlen=400)
    st.session_state.history_E = deque(maxlen=400)
    st.session_state.history_x = deque(maxlen=400)
    st.session_state.frame_count = 0
    
    # للميزان الأخروي
    st.session_state.good_deeds = 10.0
    st.session_state.bad_deeds = 5.0
    
    st.session_state.init_global = True
    st.session_state.N_STARS = N_STARS

print("✅ المرحلة الثانية مكتملة: الشريط الجانبي، العنوان، التبويبات، والتهيئة العامة.")

# ═══════════════════════════════════
# تبويب ١: المشهد الكوني
# ═══════════════════════════════════
with tabs[0]:
    st.header(t("🌌 المشهد الكوني – المحاكاة الحية", "🌌 The Cosmic Scene – Live Simulation"))
    st.markdown(t(
        "شاهد كيف يتفاعل الولاء (W) والبراءة (B) تحت ميزان الحق (ق). "
        "كل نجمة تمثل فرداً، الذهب للمؤمنين، الأحمر للكافرين، الوردي للمنافقين. "
        "الهالة السماوية تمثل التمكين (E)، والنواة الذهبية تمثل الثبات (S).",
        
        "Watch how Loyalty (W) and Disavowal (B) interact under the Balance of Truth (Q). "
        "Each star represents an individual: gold for believers, red for disbelievers, pink for hypocrites. "
        "The cyan halo represents Empowerment (E), the golden core represents Stability (S)."
    ))

    if st.session_state.get("run", False):
        placeholder = st.empty()
        
        while st.session_state.get("run", False):
            # استرجاع المتغيرات
            W = st.session_state.W
            B = st.session_state.B
            E = st.session_state.E
            S = st.session_state.S
            phase = st.session_state.phase
            cycle_angle = st.session_state.cycle_angle
            angle_W = st.session_state.angle_W
            angle_B = st.session_state.angle_B
            
            sx = st.session_state.sx.copy()
            sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy()
            sb = st.session_state.sb.copy()
            star_W_hist = st.session_state.star_W_hist
            star_B_hist = st.session_state.star_B_hist
            
            cx = st.session_state.cx
            cy = st.session_state.cy
            eb = st.session_state.empowerment_buffer
            
            pS = st.session_state.history_S
            pE = st.session_state.history_E
            px = st.session_state.history_x
            frame_count = st.session_state.frame_count
            
            planet_W_hist = st.session_state.planet_W_hist
            planet_B_hist = st.session_state.planet_B_hist
            good_deeds = st.session_state.good_deeds
            bad_deeds = st.session_state.bad_deeds
            
            N_STARS = st.session_state.N_STARS

            # ١. تحديث الدورة الحضارية
            cycle_angle += 0.008
            sv = np.sin(cycle_angle)
            
            if sv > 0.5:
                phase = t('ذروة الاستقرار', 'Peak Stability')
            elif sv > 0:
                phase = t('صعود', 'Rising')
            elif sv > -0.5:
                phase = t('انهيار', 'Collapse')
            else:
                phase = t('القاع', 'Rock Bottom')
            if 0.3 < sv < 0.35:
                phase = t('>> استدراج <<', '>> Istidraj <<')
            if -0.35 < sv < -0.3:
                phase = t('>> تعافٍ <<', '>> Recovery <<')
            
            target_S = 0.5 + 0.45 * sv

            # ٢. تحديث النجوم (الأفراد)
            for i in range(N_STARS):
                # تأثير الجوار (الشورى)
                dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                close = np.where((dist < 2.0) & (np.arange(N_STARS) != i))[0]
                
                # قوى السوق نحو التوازن
                sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                
                # تأثير الجيران (الجماعة تقوي الفرد)
                if len(close) > 0:
                    sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03
                    sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03
                
                # حدود القيم
                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)
                
                # تحديث تاريخ المسار لكل نجمة
                star_W_hist[i].append(sw[i])
                star_B_hist[i].append(sb[i])

            # ٣. الصدمات العشوائية (سنن الابتلاء)
            if random.random() < 0.005:
                affected = np.random.choice(N_STARS, size=int(N_STARS * 0.2), replace=False)
                sw[affected] *= np.random.uniform(0.5, 0.8)
                sb[affected] *= np.random.uniform(0.5, 0.8)

            # ٤. تحديث الكوكبين (W, B) بناءً على متوسط المجتمع
            avgW = np.mean(sw)
            avgB = np.mean(sb)
            
            W += (avgW - W) * 0.04
            B += (avgB - B) * 0.04
            W = np.clip(W, 0.01, 1.0)
            B = np.clip(B, 0.01, 1.0)

            # ٥. حساب الثبات S
            S = calc_S(W, B, E, q_intensity)

            # ٦. آلية الاستدراج (تأخر التمكين E عن الثبات S)
            eb.append(S)
            E_target = list(eb)[-lag_frames] if len(eb) >= lag_frames else S
            E += 0.03 * (E_target - E)

            # ٧. ديناميكيات التأثير المتبادل
            W = W - 0.015 * E + 0.03 / (S + 0.1) - 0.007 * (1 - B)
            B = B - 0.012 * E + 0.006 * (1 - B) * W * (1 - W)
            W = np.clip(W, 0.01, 1.0)
            B = np.clip(B, 0.01, 1.0)

            # ٨. إعادة حساب S بعد التحديثات
            S = calc_S(W, B, E, q_intensity)

            # ٩. تحديث التاريخ
            planet_W_hist.append(W)
            planet_B_hist.append(B)
            frame_count += 1
            if frame_count % 2 == 0:
                pS.append(S)
                pE.append(E)
                px.append(len(px))

            # ١٠. حركة الكوكبين في مداريهما
            angle_W += 0.02 + random.uniform(-0.025, 0.025) * (1 - W)**2
            angle_B += 0.02 + random.uniform(-0.025, 0.025) * (1 - B)**2
            
            orbit_W = 7 - 2.5 * W
            orbit_B = 5 - 1.5 * B
            
            wx = cx + orbit_W * np.cos(angle_W)
            wy = cy + orbit_W * np.sin(angle_W) * 0.7
            bx = cx + orbit_B * np.cos(angle_B)
            by = cy + orbit_B * np.sin(angle_B) * 0.7

            # ١١. حركة النجوم العشوائية
            instability = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.07, 0.07, N_STARS) * instability
            sy += np.random.uniform(-0.07, 0.07, N_STARS) * instability
            sx = np.clip(sx, cx - 13, cx + 13)
            sy = np.clip(sy, cy - 9, cy + 9)

            # ١٢. الميزان الأخروي
            good_deeds += W * 0.1
            bad_deeds += (1 - B) * 0.1

            # ١٣. حفظ المتغيرات
            st.session_state.W = W
            st.session_state.B = B
            st.session_state.E = E
            st.session_state.S = S
            st.session_state.phase = phase
            st.session_state.cycle_angle = cycle_angle
            st.session_state.angle_W = angle_W
            st.session_state.angle_B = angle_B
            st.session_state.empowerment_buffer = eb
            st.session_state.sx = sx
            st.session_state.sy = sy
            st.session_state.sw = sw
            st.session_state.sb = sb
            st.session_state.star_W_hist = star_W_hist
            st.session_state.star_B_hist = star_B_hist
            st.session_state.planet_W_hist = planet_W_hist
            st.session_state.planet_B_hist = planet_B_hist
            st.session_state.history_S = pS
            st.session_state.history_E = pE
            st.session_state.history_x = px
            st.session_state.frame_count = frame_count
            st.session_state.good_deeds = good_deeds
            st.session_state.bad_deeds = bad_deeds

            # ١٤. رسم المشهد الكوني
            fig, ax = plt.subplots(figsize=(16, 12), facecolor='#000010')
            ax.set_xlim(0, 28)
            ax.set_ylim(0, 20)
            ax.axis('off')

            # النواة الذهبية (S) – ﴿الْعُرْوَةِ الْوُثْقَىٰ﴾
            for r, alpha, color in [
                (0.5, 0.98, '#FFFFFF'),
                (1.0, 0.65, '#FFD700'),
                (1.7, 0.30, '#FFD700'),
                (2.6, 0.12, '#FFA500'),
                (3.8, 0.05, '#FF6347'),
                (5.5, 0.02, '#FF4500')
            ]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=color, alpha=alpha, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')

            # هالة التمكين (E) – الاستدراج
            halo_alpha = 0.25 * (1 - min(E, 1)) + 0.04
            ax.add_patch(Circle((cx, cy), 0.5 + 17 * E, color='#00FFFF', alpha=halo_alpha, zorder=7))
            
            # الغشاء الحضاري (الحدود)
            ax.add_patch(Circle((cx, cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2.5, zorder=2))

            # الكوكب W (الولاء)
            ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFFFFF', alpha=1, zorder=13))
            ax.text(wx, wy + 0.8, 'W', color='#FFFFFF', fontsize=10, ha='center', fontweight='bold')

            # الكوكب B (البراءة)
            ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#FF3333', alpha=0.8, zorder=13))
            ax.text(bx, by + 0.8, 'B', color='#FF3333', fontsize=10, ha='center', fontweight='bold')

            # النجوم (الأفراد) بألوانها
            colors = [get_star_color(sw[i], sb[i]) for i in range(N_STARS)]
            ax.scatter(sx, sy, s=30, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)

            # 🔮 الميزان الأخروي داخل المشهد
            akh_x, akh_y, ms = 26.5, 18, 1.5
            ax.plot([akh_x, akh_x], [akh_y - 3, akh_y + 1.5], color='#FFD700', lw=1, alpha=0.4)
            ly = akh_y - 1.5 + ms * min(good_deeds / 50, 1.5)
            ry = akh_y - 1.5 - ms * min(bad_deeds / 50, 1.5)
            ax.add_patch(Circle((akh_x - 1, ly), 0.6, color='#FFD700', alpha=0.3, zorder=20))
            ax.text(akh_x - 1, ly - 1, f'حسنات', color='#FFD700', fontsize=6, ha='center')
            ax.add_patch(Circle((akh_x + 1, ry), 0.6, color='#FF4444', alpha=0.3, zorder=20))
            ax.text(akh_x + 1, ry - 1, f'سيئات', color='#FF4444', fontsize=6, ha='center')
            diff = (bad_deeds - good_deeds) / 50 * ms
            ax.plot([akh_x - 1, akh_x + 1], [akh_y - diff, akh_y + diff], color='#FFD700', lw=1.5, alpha=0.6)

            # 📈 لوحة الإثبات (منحنى الاستدراج)
            pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
            pax.set_xlim(0, 400)
            pax.set_ylim(0, 1.05)
            pax.set_title(t('إثبات: S يقود E – الاستدراج', 'Proof: S leads E – Istidraj'),
                         color='white', fontsize=7, fontweight='bold')
            pax.tick_params(colors='white', labelsize=4)
            pax.grid(True, alpha=0.12)
            
            pSl = list(pS)
            pEl = list(pE)
            pxl = list(px)
            if pSl:
                pax.plot(pxl, pSl, color='#FFD700', lw=2, label='S (الثبات)')
                pax.plot(pxl, pEl, color='#00FFFF', lw=1.5, label='E (التمكين)')
                pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=5)

            # نص الطور الحضاري
            ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f}',
                   color='white', fontsize=11, ha='center', fontweight='bold')

            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            plt.close(fig)

            time.sleep(0.08)

        st.success(t("✅ توقفت المحاكاة", "✅ Simulation stopped"))

    else:
        # عرض المشهد الثابت قبل التشغيل
        if st.session_state.get('init_global'):
            fig, ax = plt.subplots(figsize=(16, 12), facecolor='#000010')
            ax.set_xlim(0, 28)
            ax.set_ylim(0, 20)
            ax.axis('off')

            cx = st.session_state.cx
            cy = st.session_state.cy
            S = st.session_state.S
            E = st.session_state.E
            N_STARS = st.session_state.N_STARS

            # النواة
            for r, alpha, color in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'),
                                    (1.7, 0.3, '#FFD700'), (2.6, 0.12, '#FFA500'),
                                    (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=color, alpha=alpha, zorder=15))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')
            ax.add_patch(Circle((cx, cy), 0.5 + 17 * E, color='#0FF',
                               alpha=0.25 * (1 - min(E, 1)) + 0.04, zorder=7))
            ax.add_patch(Circle((cx, cy), 8.5, color='#0F8', alpha=0.15, fill=False, lw=2.5, zorder=2))

            # النجوم
            colors = [get_star_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(N_STARS)]
            ax.scatter(st.session_state.sx, st.session_state.sy, s=30, c=colors, alpha=0.9,
                      edgecolors='white', linewidths=0.3, zorder=5)

            ax.text(14, 1.2, t('في انتظار التشغيل...', 'Waiting to run...'),
                   color='white', fontsize=12, ha='center')
            plt.tight_layout(pad=0)
            st.pyplot(fig)
            plt.close(fig)

        st.info(t(
            "اضغط ▶️ تشغيل المحاكاة في لوحة القيادة لرؤية المشهد الكوني الحي.",
            "Press ▶️ Run Simulation in the dashboard to see the live cosmic scene."
        ))

print("✅ المرحلة الثالثة مكتملة: تبويب المشهد الكوني مع المحاكاة الحية.")

# ═══════════════════════════════════
# تبويب ٢: مختبر الفرد – البوصلة الشخصية
# ═══════════════════════════════════
with tabs[1]:
    st.header(t("🧍 مختبر الفرد – ميزانك الشخصي", "🧍 Individual Lab – Your Personal Balance"))
    st.markdown(t(
        "اكتشف موقعك في فضاء الولاء والبراءة. أجب عن 12 سؤالاً بصدق، "
        "لترى أين تقع في نظام الإحداثيات الوجودي، واحصل على برنامج عملي للتحسين.",
        
        "Discover your position in Loyalty-Disavowal space. Answer 12 questions honestly "
        "to see where you stand in the existential coordinate system, and get a practical improvement plan."
    ))

    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    # الأسئلة – 6 للولاء (W) و 6 للبراءة (B)
    questions = {
        "W": [
            (t("حياتي كلها لله، لا أبتغي بها إلا وجهه", "My whole life is for Allah alone"), 3),
            (t("أقيم الصلاة بخشوع، أستشعر الوقوف بين يدي الله", "I pray with devotion, feeling I stand before Allah"), 3),
            (t("أحب الله ورسوله أكثر من كل شيء", "I love Allah and His Messenger more than everything"), 3),
            (t("أتوكل على الله مع الأخذ بالأسباب", "I rely on Allah while using all means"), 3),
            (t("أشكر الله في الرخاء وأصبر في البلاء", "I thank Allah in ease and am patient in hardship"), 3),
            (t("أحمل هم الإسلام والمسلمين، وأسعى لنصرتهم", "I carry the concerns of Islam and Muslims"), 3),
        ],
        "B": [
            (t("آمر بالمعروف بالحكمة والموعظة الحسنة", "I enjoin good with wisdom and beautiful preaching"), 3),
            (t("أنكر المنكر بلساني أو قلبي", "I forbid evil with my tongue or heart"), 3),
            (t("أتبرأ من الشرك وأهله، وأعلن براءتي منهم", "I disavow polytheism and its people"), 3),
            (t("أجاهد نفسي على ترك الكذب والغيبة والظلم", "I struggle against lying, backbiting, and injustice"), 3),
            (t("أرفض الظلم بكل صوره، ولا أرضاه لأحد", "I reject all forms of injustice"), 3),
            (t("أحب في الله وأبغض في الله، أوالي أولياءه وأعادي أعداءه", "I love and hate for Allah's sake"), 3),
        ]
    }

    colA, colB = st.columns(2)

    with colA:
        st.subheader(t("🤍 أسئلة الولاء (W)", "🤍 Loyalty Questions (W)"))
        for i, (q, v) in enumerate(questions["W"]):
            ans = st.radio(
                q,
                [t(f"نعم (+{v})", f"Yes (+{v})"),
                 t("أحياناً (+1)", "Sometimes (+1)"),
                 t("لا (0)", "No (0)"),
                 t("العكس (-1)", "Opposite (-1)")],
                key=f"compass_w_{i}",
                index=None
            )
            if ans:
                if t("نعم", "Yes") in ans:
                    st.session_state.compass_answers[f"W{i}"] = v
                elif t("أحياناً", "Sometimes") in ans:
                    st.session_state.compass_answers[f"W{i}"] = 1
                elif "لا" in ans:
                    st.session_state.compass_answers[f"W{i}"] = 0
                else:
                    st.session_state.compass_answers[f"W{i}"] = -1

    with colB:
        st.subheader(t("❤️ أسئلة البراءة (B)", "❤️ Disavowal Questions (B)"))
        for i, (q, v) in enumerate(questions["B"]):
            ans = st.radio(
                q,
                [t(f"نعم (+{v})", f"Yes (+{v})"),
                 t("أحياناً (+1)", "Sometimes (+1)"),
                 t("لا (0)", "No (0)"),
                 t("العكس (-1)", "Opposite (-1)")],
                key=f"compass_b_{i}",
                index=None
            )
            if ans:
                if t("نعم", "Yes") in ans:
                    st.session_state.compass_answers[f"B{i}"] = v
                elif t("أحياناً", "Sometimes") in ans:
                    st.session_state.compass_answers[f"B{i}"] = 1
                elif "لا" in ans:
                    st.session_state.compass_answers[f"B{i}"] = 0
                else:
                    st.session_state.compass_answers[f"B{i}"] = -1

    # حساب النتيجة عند اكتمال الإجابات
    TOTAL_Q = 12
    if len(st.session_state.compass_answers) == TOTAL_Q:
        W_raw = sum(st.session_state.compass_answers[f"W{i}"] for i in range(6))
        B_raw = sum(st.session_state.compass_answers[f"B{i}"] for i in range(6))
        
        # تطبيع إلى [-1, 1]
        W_val = np.clip(W_raw / 18.0, -1, 1)
        B_val = np.clip(B_raw / 18.0, -1, 1)
        
        # تحويل إلى [0, 1] للحسابات
        W_norm = (W_val + 1) / 2
        B_norm = (B_val + 1) / 2
        S_val = W_norm * B_norm
        
        # تحديد الربع
        if W_val > 0.3 and B_val > 0.3:
            quadrant = "Q1"
        elif W_val < -0.3 and B_val > 0.3:
            quadrant = "Q2"
        elif W_val < -0.3 and B_val < -0.3:
            quadrant = "Q3"
        elif W_val > 0.3 and B_val < -0.3:
            quadrant = "Q4"
        else:
            quadrant = "GRAY"

        # أسماء الأرباع ونصائحها وبرامجها العملية
        quadrant_info = {
            "Q1": {
                "name": t("المؤمن (الربع الأول)", "The Believer (Q1)"),
                "color": "#FFD700",
                "advice": t(
                    "أنت في موقع المؤمن. حافظ على ثباتك واستمر في النمو نحو الكمال (1,1).",
                    "You are in the Believer's position. Maintain your stability and keep growing toward (1,1)."
                ),
                "program": [
                    t("حافظ على الصلاة في وقتها بخشوع", "Keep prayer on time with devotion"),
                    t("تصدق ولو بشيء يسير يومياً", "Give daily charity even if small"),
                    t("اختم القرآن كل شهر", "Complete Quran recitation monthly"),
                    t("جالس الصالحين وداوم على الذكر", "Sit with the righteous and remember Allah often"),
                    t("كن داعية إلى الله بعلمك وعملك", "Be a caller to Allah with your knowledge and deeds"),
                ]
            },
            "Q2": {
                "name": t("الكافر (الربع الثاني)", "The Disbeliever (Q2)"),
                "color": "#FF5252",
                "advice": t(
                    "باب التوبة مفتوح. أعد توجيه بوصلتك نحو الله. ابدأ بالتعرف على الله حق المعرفة.",
                    "The door of repentance is open. Redirect your compass toward Allah. Start by truly knowing Him."
                ),
                "program": [
                    t("تعرف على الله من خلال أسمائه الحسنى", "Learn Allah through His Beautiful Names"),
                    t("صل ركعتين في الليل وادع الله أن يهديك", "Pray two rak'ahs at night and ask for guidance"),
                    t("اقرأ سيرة النبي ﷺ", "Read the Prophet's biography"),
                    t("صاحب مؤمناً تقياً", "Befriend a pious believer"),
                    t("تدبر في خلق السماوات والأرض", "Reflect on the creation of heavens and earth"),
                ]
            },
            "Q3": {
                "name": t("المنافق (الربع الثالث)", "The Hypocrite (Q3)"),
                "color": "#FFB6C1",
                "advice": t(
                    "أنت في حالة تذبذب خطيرة. عليك بالصدق مع نفسك واتخاذ قرار حاسم.",
                    "You are in a dangerously unstable state. Be honest with yourself and make a decisive choice."
                ),
                "program": [
                    t("قف مع نفسك وقفة صدق: من أنت؟", "Stop and be honest with yourself: Who are you?"),
                    t("اختر طريقاً واحداً: إما الإيمان أو الكفر", "Choose one path: either faith or disbelief"),
                    t("استغفر الله مائة مرة كل يوم", "Seek Allah's forgiveness 100 times daily"),
                    t("ابدأ بصلاة الفجر في المسجد", "Start with Fajr prayer in the mosque"),
                    t("أكثر من قول: اللهم أرني الحق حقاً", "Repeat: O Allah, show me the truth as truth"),
                ]
            },
            "Q4": {
                "name": t("المشرك (الربع الرابع)", "The Polytheist (Q4)"),
                "color": "#FFA500",
                "advice": t(
                    "لديك إيمان لكنك تخلطه بشرك. قوِّ مناعتك الإيمانية وأخلص العبادة لله وحده.",
                    "You have faith but mix it with polytheism. Strengthen your immunity and purify your worship."
                ),
                "program": [
                    t("تعلم معنى لا إله إلا الله حقاً", "Learn the true meaning of La ilaha illa Allah"),
                    t("تخلص من كل مظاهر الشرك في حياتك", "Remove all manifestations of polytheism"),
                    t("أكثر من دعاء: اللهم إني أعوذ بك أن أشرك بك", "Seek refuge from shirk frequently"),
                    t("صاحب أهل التوحيد", "Befriend the people of Tawhid"),
                    t("اقرأ كتاب التوحيد", "Read books on Islamic monotheism"),
                ]
            },
            "GRAY": {
                "name": t("منطقة التذبذب", "The Gray Zone"),
                "color": "#888888",
                "advice": t(
                    "أنت في منطقة الخطر. حدد اتجاهك الآن قبل فوات الأوان.",
                    "You are in the danger zone. Decide your direction now before it's too late."
                ),
                "program": [
                    t("حدد أين تريد أن تكون بعد شهر", "Decide where you want to be in a month"),
                    t("اتخذ قراراً حاسماً اليوم", "Make a firm decision today"),
                    t("استشر عالماً ربانياً", "Consult a knowledgeable scholar"),
                    t("أكثر من الدعاء: اللهم أرني الحق حقاً", "Pray: O Allah, show me the truth as truth"),
                    t("اقرأ سورة الحديد كل يوم", "Read Surah Al-Hadid daily"),
                ]
            }
        }

        info = quadrant_info[quadrant]

        # عرض النتيجة
        st.divider()
        st.header(t("📊 نتيجتك", "📊 Your Result"))

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("W (الولاء)", f"{W_val:.2f}")
        with c2:
            st.metric("B (البراءة)", f"{B_val:.2f}")
        with c3:
            st.metric("S (الثبات)", f"{S_val:.2f}")

        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(10,10,46,0.9);
                    border-radius: 15px; border: 2px solid {info['color']}; margin: 15px 0;">
            <h2 style="color: {info['color']}; margin: 0;">{info['name']}</h2>
            <p style="color: #CCC; margin-top: 10px;">{info['advice']}</p>
            <p style="color: #FFD700; font-size: 1.3em; margin: 10px 0;">⚖️ S = W × B = {S_val:.3f}</p>
        </div>
        """, unsafe_allow_html=True)

        # برنامج عملي
        with st.expander(t("🛤️ برنامجك العملي للتحسين", "🛤️ Your Action Plan"), expanded=True):
            st.markdown(t(
                "**هذا برنامج عملي لتقوية موقعك الوجودي. التزم به لمدة ٣٠ يوماً، ثم أعد الاختبار لترى تحسنك.**",
                "**Follow this plan for 30 days, then retake the test to see your improvement.**"
            ))
            for i, step in enumerate(info["program"]):
                st.markdown(f"**{i+1}.** {step}")

        # رسم الخريطة الرباعية
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5)
        ax.axvline(0, color='grey', lw=0.5)
        ax.set_xlabel("B (البراءة)", color='white')
        ax.set_ylabel("W (الولاء)", color='white')

        # تلوين الأرباع
        ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.15))
        ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF5252', alpha=0.15))
        ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.15))
        ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA500', alpha=0.15))

        # تسمية الأرباع
        ax.text(0.5, 0.5, t("مؤمن", "Believer"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, 0.5, t("كافر", "Disbeliever"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, -0.5, t("منافق", "Hypocrite"), ha='center', color='white', alpha=0.6)
        ax.text(0.5, -0.5, t("مشرك", "Polytheist"), ha='center', color='white', alpha=0.6)

        # نقطة المستخدم
        ax.scatter(B_val, W_val, s=250, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
        ax.tick_params(colors='white')
        st.pyplot(fig)

        # زر إعادة الاختبار
        if st.button(t("🔄 أعد الميزان", "🔄 Retake Test"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

    elif len(st.session_state.compass_answers) > 0:
        remaining = TOTAL_Q - len(st.session_state.compass_answers)
        st.info(t(
            f"أجب عن {remaining} سؤالاً متبقياً لاكتمال البوصلة.",
            f"Answer {remaining} remaining questions to complete the compass."
        ))

print("✅ المرحلة الرابعة مكتملة: تبويب مختبر الفرد مع البوصلة الشخصية والبرنامج العملي.")

# ═══════════════════════════════════
# تبويب ٣: مختبر المجتمع
# ═══════════════════════════════════
with tabs[2]:
    st.header(t("👥 مختبر المجتمع – المحاكاة الاجتماعية", "👥 Society Lab – Social Simulation"))
    st.markdown(t(
        "شاهد كيف تنتشر قيم الولاء (W) والبراءة (B) في مجتمع حي. "
        "كل نقطة تمثل فرداً، واللون يعكس موقعه الوجودي. "
        "اضبط معاملات الأمر بالمعروف والنهي عن المنكر لترى أثرها على تماسك المجتمع.",
        
        "Watch how Loyalty (W) and Disavowal (B) values spread in a living society. "
        "Each dot represents an individual, color reflects their existential position. "
        "Adjust enjoining good and forbidding evil to see their impact on social cohesion."
    ))

    # معاملات المجتمع
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pop_size = st.slider(t("عدد الأفراد", "Population Size"), 50, 300, 150, 25, key="soc_pop")
    with col2:
        influence_radius = st.slider(t("مدى التأثر بالجيران", "Neighbor Influence Radius"), 0.5, 5.0, 2.0, 0.5, key="soc_radius")
    with col3:
        soc_amr = st.slider(t("الأمر بالمعروف", "Enjoining Good"), 0.0, 1.0, 0.5, 0.05, key="soc_amr")
    with col4:
        soc_nahy = st.slider(t("النهي عن المنكر", "Forbidding Evil"), 0.0, 1.0, 0.5, 0.05, key="soc_nahy")

    # زر تشغيل المحاكاة الاجتماعية
    if st.button(t("▶️ شغّل محاكاة المجتمع", "▶️ Run Society Simulation"), use_container_width=True, type="primary"):
        with st.spinner(t("المحاكاة الاجتماعية تعمل...", "Society simulation running...")):
            # تهيئة المجتمع
            np.random.seed(42)
            pop_W = np.random.uniform(0.2, 0.9, pop_size)
            pop_B = np.random.uniform(0.2, 0.9, pop_size)
            pos_x = np.random.uniform(0, 30, pop_size)
            pos_y = np.random.uniform(0, 30, pop_size)

            # مصفوفة تاريخية لتخزين تطور المجتمع
            history_W_mean = []
            history_B_mean = []
            history_believers_pct = []

            # محاكاة 100 خطوة زمنية
            sim_steps = 100
            for step in range(sim_steps):
                new_W = pop_W.copy()
                new_B = pop_B.copy()

                for i in range(pop_size):
                    # حساب تأثير الجيران
                    distances = np.sqrt((pos_x - pos_x[i])**2 + (pos_y - pos_y[i])**2)
                    neighbors = np.where((distances < influence_radius) & (np.arange(pop_size) != i))[0]

                    if len(neighbors) > 0:
                        # تأثير الجيران (الشورى والجماعة)
                        new_W[i] += 0.03 * (np.mean(pop_W[neighbors]) - pop_W[i])
                        new_B[i] += 0.03 * (np.mean(pop_B[neighbors]) - pop_B[i])

                    # تأثير الأمر بالمعروف والنهي عن المنكر
                    new_W[i] += 0.02 * soc_amr * (1 - pop_W[i])
                    new_B[i] += 0.02 * soc_nahy * (1 - pop_B[i])

                    # ضوضاء عشوائية (أحداث الحياة)
                    new_W[i] += 0.01 * (np.random.rand() - 0.5)
                    new_B[i] += 0.01 * (np.random.rand() - 0.5)

                    # حدود القيم
                    new_W[i] = np.clip(new_W[i], 0.01, 1.0)
                    new_B[i] = np.clip(new_B[i], 0.01, 1.0)

                pop_W = new_W
                pop_B = new_B

                # حركة عشوائية للأفراد
                pos_x += np.random.randint(-1, 2, pop_size)
                pos_y += np.random.randint(-1, 2, pop_size)
                pos_x = np.clip(pos_x, 0, 29)
                pos_y = np.clip(pos_y, 0, 29)

                # تسجيل التاريخ
                history_W_mean.append(np.mean(pop_W))
                history_B_mean.append(np.mean(pop_B))
                believers = np.sum((pop_W >= 0.5) & (pop_B >= 0.5))
                history_believers_pct.append(believers / pop_size * 100)

            # رسم النتائج
            fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#000010')

            # الخريطة الاجتماعية النهائية
            ax1 = axes[0]
            ax1.set_facecolor('#0a0a1a')
            colors_final = [get_star_color(pop_W[i], pop_B[i]) for i in range(pop_size)]
            ax1.scatter(pos_x, pos_y, c=colors_final, s=40, alpha=0.8, edgecolors='white', linewidths=0.3)
            ax1.set_xlim(0, 30)
            ax1.set_ylim(0, 30)
            ax1.set_title(t('خريطة المجتمع النهائية', 'Final Society Map'), color='white', fontsize=13)
            ax1.grid(True, alpha=0.2)
            ax1.tick_params(colors='white')

            # إضافة وسيلة إيضاح
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFD700', markersize=8, label=t('مؤمن', 'Believer')),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF5252', markersize=8, label=t('كافر', 'Disbeliever')),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFB6C1', markersize=8, label=t('منافق', 'Hypocrite')),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#E0E0E0', markersize=8, label=t('ضعيف', 'Weak')),
            ]
            ax1.legend(handles=legend_elements, loc='upper right', facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=8)

            # تطور المجتمع عبر الزمن
            ax2 = axes[1]
            ax2.set_facecolor('#0a0a1a')
            ax2.plot(history_W_mean, color='#FFD700', lw=2, label='W (متوسط الولاء)')
            ax2.plot(history_B_mean, color='#FF5252', lw=2, label='B (متوسط البراءة)')
            ax2.plot(history_believers_pct, color='#00FF88', lw=2, label='% المؤمنين')
            ax2.set_xlabel(t('الزمن (خطوات)', 'Time (Steps)'), color='white')
            ax2.set_ylabel(t('القيمة', 'Value'), color='white')
            ax2.set_title(t('تطور المجتمع عبر الزمن', 'Society Evolution Over Time'), color='white', fontsize=13)
            ax2.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax2.grid(True, alpha=0.2)
            ax2.tick_params(colors='white')
            ax2.set_ylim(0, 105)

            plt.tight_layout()
            st.pyplot(fig)

            # إحصائيات المجتمع
            st.divider()
            st.subheader(t("📊 إحصائيات المجتمع", "📊 Society Statistics"))

            c1, c2, c3, c4 = st.columns(4)
            final_believers = np.sum((pop_W >= 0.5) & (pop_B >= 0.5))
            final_disbelievers = np.sum((pop_W < 0.5) & (pop_B >= 0.5))
            final_hypocrites = np.sum((pop_W < 0.5) & (pop_B < 0.5))
            final_polytheists = np.sum((pop_W >= 0.5) & (pop_B < 0.5))

            with c1:
                st.metric(t("🟡 المؤمنون", "🟡 Believers"), f"{final_believers}", f"{final_believers/pop_size*100:.0f}%")
            with c2:
                st.metric(t("🔴 الكافرون", "🔴 Disbelievers"), f"{final_disbelievers}", f"{final_disbelievers/pop_size*100:.0f}%")
            with c3:
                st.metric(t("🩷 المنافقون", "🩷 Hypocrites"), f"{final_hypocrites}", f"{final_hypocrites/pop_size*100:.0f}%")
            with c4:
                st.metric(t("🟠 المشركون", "🟠 Polytheists"), f"{final_polytheists}", f"{final_polytheists/pop_size*100:.0f}%")

            # متوسط الثبات
            S_mean = np.mean(pop_W * pop_B)
            st.metric(t("⚖️ متوسط الثبات (S) في المجتمع", "⚖️ Average Stability (S)"), f"{S_mean:.3f}")

print("✅ المرحلة الخامسة مكتملة: تبويب مختبر المجتمع مع المحاكاة الاجتماعية.")

# ═══════════════════════════════════
# تبويب ٤: مختبر الدولة
# ═══════════════════════════════════
with tabs[3]:
    st.header(t("🏛️ مختبر الدولة – محاكاة الحكم", "🏛️ State Lab – Governance Simulation"))
    st.markdown(t(
        "شاهد كيف تؤثر أسس الحكم على استقرار الدولة. "
        "اضبط معاملات العدل، الشورى، وتحكيم الشرع، وراقب كيف تتغير منحنيات الثبات (S) والتمكين (E) عبر 100 عام.",
        
        "Watch how governance foundations affect state stability. "
        "Adjust justice, consultation, and Sharia implementation, and observe how Stability (S) and Empowerment (E) curves change over 100 years."
    ))

    # معاملات الحكم
    col1, col2, col3 = st.columns(3)
    with col1:
        state_justice = st.slider(
            t("⚖️ العدل", "⚖️ Justice"),
            0.0, 1.0, 0.6, 0.05,
            key="state_justice",
            help=t("العدل أساس الملك. ﴿إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالْإِحْسَانِ﴾", "Justice is the foundation of dominion.")
        )
    with col2:
        state_shura = st.slider(
            t("🤝 الشورى", "🤝 Consultation"),
            0.0, 1.0, 0.5, 0.05,
            key="state_shura",
            help=t("الشورى تنشر المسؤولية وتقوي التماسك. ﴿وَأَمْرُهُمْ شُورَىٰ بَيْنَهُمْ﴾", "Consultation spreads responsibility.")
        )
    with col3:
        state_sharia = st.slider(
            t("📜 تحكيم الشرع", "📜 Applying Sharia"),
            0.0, 1.0, 0.5, 0.05,
            key="state_sharia",
            help=t("تحكيم شرع الله يحفظ الحقوق. ﴿وَمَن لَّمْ يَحْكُم بِمَا أَنزَلَ اللَّهُ فَأُولَٰئِكَ هُمُ الْكَافِرُونَ﴾", "Applying Allah's law preserves rights.")
        )

    # معاملات الفساد
    col4, col5 = st.columns(2)
    with col4:
        state_corruption = st.slider(
            t("💀 الفساد", "💀 Corruption"),
            0.0, 1.0, 0.2, 0.05,
            key="state_corruption",
            help=t("الفساد ينخر الثقة ويهدم المؤسسات.", "Corruption erodes trust and destroys institutions.")
        )
    with col5:
        state_oppression = st.slider(
            t("👊 الظلم", "👊 Oppression"),
            0.0, 1.0, 0.1, 0.05,
            key="state_oppression",
            help=t("الظلم ظلمات يوم القيامة. ﴿وَلَا تَحْسَبَنَّ اللَّهَ غَافِلًا عَمَّا يَعْمَلُ الظَّالِمُونَ﴾", "Oppression is darkness on Judgment Day.")
        )

    # زر تشغيل محاكاة الدولة
    if st.button(t("🚀 شغّل محاكاة الدولة", "🚀 Run State Simulation"), use_container_width=True, type="primary"):
        with st.spinner(t("محاكاة الدولة تعمل...", "State simulation running...")):
            # المدة الزمنية (100 عام)
            years = 100
            W_state = np.zeros(years)
            B_state = np.zeros(years)
            S_state = np.zeros(years)
            E_state = np.zeros(years)

            # القيم الابتدائية للدولة
            W_state[0] = state_sharia * state_justice
            B_state[0] = state_sharia * (1 - state_corruption)
            W_state[0] = np.clip(W_state[0], 0.01, 1.0)
            B_state[0] = np.clip(B_state[0], 0.01, 1.0)
            S_state[0] = W_state[0] * B_state[0]
            E_state[0] = 0.1

            for t in range(1, years):
                # تأثير الحكم على W (الولاء)
                W_growth = state_justice * 0.015 + state_sharia * 0.02 + state_shura * 0.01
                W_decay = state_corruption * 0.02 + state_oppression * 0.025

                # تأثير الحكم على B (البراءة)
                B_growth = state_sharia * 0.025 + state_justice * 0.01
                B_decay = state_corruption * 0.03 + state_oppression * 0.02

                # تحديث W و B
                W_state[t] = W_state[t-1] + W_growth - W_decay * E_state[t-1]
                B_state[t] = B_state[t-1] + B_growth - B_decay * E_state[t-1]

                # تأثير الشورى (يمنع التطرف)
                W_state[t] += state_shura * 0.005 * (1 - abs(W_state[t-1] - B_state[t-1]))
                B_state[t] += state_shura * 0.005 * (1 - abs(W_state[t-1] - B_state[t-1]))

                W_state[t] = np.clip(W_state[t], 0.01, 1.0)
                B_state[t] = np.clip(B_state[t], 0.01, 1.0)

                # حساب الثبات
                S_state[t] = W_state[t] * B_state[t]

                # الاستدراج: التمكين يتأخر عن الثبات
                lag = int(15 * (1 + state_corruption * 0.5))
                past_idx = max(0, t - lag)
                E_state[t] = E_state[t-1] + 0.04 * (S_state[past_idx] - E_state[t-1])
                E_state[t] = np.clip(E_state[t], 0.01, 1.0)

            # رسم النتائج
            fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#000010')

            # الرسم الأول: دورة الدولة
            ax1 = axes[0]
            ax1.set_facecolor('#0a0a1a')
            ax1.plot(S_state, 'g-', lw=2.5, label=t('S (الثبات)', 'S (Stability)'))
            ax1.plot(E_state, 'b--', lw=2.0, label=t('E (التمكين)', 'E (Empowerment)'))
            ax1.plot(W_state, color='gold', lw=1.5, alpha=0.7, label=t('W (الولاء)', 'W (Loyalty)'))
            ax1.plot(B_state, color='#FF5252', lw=1.5, alpha=0.7, label=t('B (البراءة)', 'B (Disavowal)'))

            # فجوة الاستدراج
            idx_S_max = np.argmax(S_state)
            idx_E_max = np.argmax(E_state)
            if idx_S_max < idx_E_max:
                ax1.axvspan(idx_S_max, idx_E_max, alpha=0.2, color='red',
                           label=t('فجوة الاستدراج', 'Istidraj Gap'))

            ax1.set_title(t('دورة الدولة عبر ١٠٠ عام', 'State Cycle Over 100 Years'),
                         color='white', fontsize=13, fontweight='bold')
            ax1.set_xlabel(t('السنوات', 'Years'), color='white')
            ax1.set_ylabel(t('القيمة', 'Value'), color='white')
            ax1.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax1.grid(True, alpha=0.2)
            ax1.tick_params(colors='white')
            ax1.set_ylim(0, 1.05)

            # الرسم الثاني: مسار الدولة في فضاء (W, B)
            ax2 = axes[1]
            ax2.set_facecolor('#0a0a1a')
            ax2.plot(B_state, W_state, 'w-', alpha=0.4, lw=0.8)
            ax2.scatter(B_state[0], W_state[0], s=150, c='green', edgecolors='white',
                       linewidth=2, zorder=10, label=t('البداية', 'Start'))
            ax2.scatter(B_state[-1], W_state[-1], s=150, c='red', edgecolors='white',
                       linewidth=2, zorder=10, label=t('النهاية', 'End'))
            ax2.axhline(0.5, color='grey', ls=':', lw=1)
            ax2.axvline(0.5, color='grey', ls=':', lw=1)
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.set_xlabel('B (البراءة)', color='white')
            ax2.set_ylabel('W (الولاء)', color='white')
            ax2.set_title(t('مسار الدولة في فضاء (W, B)', 'State Path in (W, B) Space'),
                         color='white', fontsize=13, fontweight='bold')

            # تلوين الأرباع
            ax2.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green')
            ax2.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='orange')
            ax2.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='blue')
            ax2.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='red')
            ax2.text(0.75, 0.75, t('مستقرة', 'Stable'), color='green', fontsize=9, ha='center')
            ax2.text(0.25, 0.75, t('متطرفة', 'Extremist'), color='orange', fontsize=9, ha='center')
            ax2.text(0.25, 0.25, t('فاشلة', 'Failed'), color='red', fontsize=9, ha='center')
            ax2.text(0.75, 0.25, t('متناقضة', 'Contradictory'), color='blue', fontsize=9, ha='center')
            ax2.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax2.grid(True, alpha=0.2)
            ax2.tick_params(colors='white')

            plt.tight_layout()
            st.pyplot(fig)

            # مؤشرات حية
            st.divider()
            st.subheader(t("📊 مؤشرات الدولة", "📊 State Indicators"))

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric(t("W النهائي", "Final W"), f"{W_state[-1]:.3f}")
            with c2:
                st.metric(t("B النهائي", "Final B"), f"{B_state[-1]:.3f}")
            with c3:
                st.metric(t("S النهائي", "Final S"), f"{S_state[-1]:.3f}")
            with c4:
                # حساب عام الانهيار (إذا انخفض S تحت 0.2)
                collapse_year = None
                for t in range(1, years):
                    if S_state[t] < 0.2 and S_state[t-1] >= 0.2:
                        collapse_year = t
                        break
                if collapse_year:
                    st.metric(t("عام الانهيار", "Collapse Year"), f"{collapse_year}")
                else:
                    st.metric(t("الحالة", "Status"), t("مستقرة", "Stable"))
            with c5:
                istidraj_gap = max(0, np.argmax(E_state) - np.argmax(S_state))
                st.metric(t("فجوة الاستدراج", "Istidraj Gap"), f"{istidraj_gap} {t('عام', 'yrs')}")

            # تحليل الحالة
            st.divider()
            st.subheader(t("🔍 تحليل الحالة", "🔍 Status Analysis"))

            if S_state[-1] > 0.7:
                st.success(t(
                    "✅ الدولة في حالة استقرار عالٍ. W و B متوازنتان والتمكين يتبع الثبات بشكل صحي.",
                    "✅ The state is highly stable. W and B are balanced, and empowerment follows stability healthily."
                ))
            elif S_state[-1] > 0.4:
                st.warning(t(
                    "⚠️ الدولة في حالة متوسطة. هناك مؤشرات على بداية تراجع. انتبه لفجوة الاستدراج.",
                    "⚠️ The state is in a moderate condition. There are signs of decline. Watch the Istidraj gap."
                ))
            else:
                st.error(t(
                    "🔴 الدولة في حالة انهيار أو تقترب منه. يجب إصلاح أسس الحكم فوراً.",
                    "🔴 The state is collapsing or approaching collapse. Governance foundations must be reformed immediately."
                ))

print("✅ المرحلة السادسة مكتملة: تبويب مختبر الدولة مع محاكاة الحكم.")

# ═══════════════════════════════════
# تبويب ٥: مختبر الأمة
# ═══════════════════════════════════
with tabs[4]:
    st.header(t("🌍 مختبر الأمة – دورة الحضارة", "🌍 Nation Lab – Civilization Cycle"))
    st.markdown(t(
        "هذا هو المختبر الإلهي للأمم. اضبط مولدات الطاقة وحدود البراءة، "
        "وشاهد كيف تنهض الأمة أو تنهار عبر ٣٠٠ عام. المعادلة واحدة: **S = W × B**.",
        
        "This is the divine lab for nations. Adjust energy generators and disavowal boundaries, "
        "and watch the nation rise or fall over 300 years. One equation: **S = W × B**."
    ))

    # معاملات الأمة
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🕌 مولدات الطاقة (العبادات)")
        nation_prayer = st.slider(
            t("الصلاة (W)", "Prayer (W)"), 0.0, 1.0, 0.7, 0.01,
            key="nation_prayer",
            help=t("الصلاة عماد الدين، تقوي الولاء لله. ﴿إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ﴾", "Prayer strengthens loyalty to Allah.")
        )
        nation_fasting = st.slider(
            t("الصوم (B)", "Fasting (B)"), 0.0, 1.0, 0.6, 0.01,
            key="nation_fasting",
            help=t("الصوم يقوي البراءة من الشهوات. ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ﴾", "Fasting strengthens disavowal of desires.")
        )
        nation_zakat = st.slider(
            t("الزكاة (B)", "Zakat (B)"), 0.0, 1.0, 0.5, 0.01,
            key="nation_zakat",
            help=t("الزكاة تطهر المال وتقوي البراءة من الشح. ﴿خُذْ مِنْ أَمْوَالِهِمْ صَدَقَةً تُطَهِّرُهُمْ﴾", "Zakat purifies wealth and strengthens disavowal of greed.")
        )
        nation_hajj = st.slider(
            t("الحج (W)", "Hajj (W)"), 0.0, 1.0, 0.4, 0.01,
            key="nation_hajj",
            help=t("الحج يجدد الولاء لله. ﴿وَلِلَّهِ عَلَى النَّاسِ حِجُّ الْبَيْتِ﴾", "Hajj renews loyalty to Allah.")
        )

    with col2:
        st.markdown("### 🛡️ حدود البراءة والجهاد")
        nation_jihad_self = st.slider(
            t("جهاد النفس (B)", "Jihad of Self (B)"), 0.0, 1.0, 0.8, 0.01,
            key="nation_jihad_self",
            help=t("المجاهد من جاهد نفسه في طاعة الله.", "The true mujahid struggles against his own self.")
        )
        nation_jihad_wealth = st.slider(
            t("جهاد المال (B)", "Jihad with Wealth (B)"), 0.0, 1.0, 0.5, 0.01,
            key="nation_jihad_wealth",
            help=t("﴿وَجَاهِدُوا بِأَمْوَالِكُمْ وَأَنفُسِكُمْ فِي سَبِيلِ اللَّهِ﴾", "Strive with your wealth and lives in Allah's cause.")
        )
        nation_disavowal = st.slider(
            t("البراءة من الطاغوت (B)", "Disavowal of Taghut (B)"), 0.0, 1.0, 0.9, 0.01,
            key="nation_disavowal",
            help=t("﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ﴾", "Whoever disbelieves in Taghut and believes in Allah.")
        )
        nation_alliance = st.slider(
            t("موالاة المؤمنين (W)", "Alliance with Believers (W)"), 0.0, 1.0, 0.8, 0.01,
            key="nation_alliance",
            help=t("﴿إِنَّمَا وَلِيُّكُمُ اللَّهُ وَرَسُولُهُ وَالَّذِينَ آمَنُوا﴾", "Your ally is none but Allah, His Messenger, and the believers.")
        )

    with col3:
        st.markdown("### ⚖️ أسس الحكم")
        nation_justice = st.slider(
            t("العدل", "Justice"), 0.0, 1.0, 0.6, 0.01,
            key="nation_justice",
            help=t("العدل أساس الملك. ﴿إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالْإِحْسَانِ﴾", "Justice is the foundation of dominion.")
        )
        nation_shura = st.slider(
            t("الشورى", "Consultation"), 0.0, 1.0, 0.5, 0.01,
            key="nation_shura",
            help=t("الشورى تنشر المسؤولية. ﴿وَأَمْرُهُمْ شُورَىٰ بَيْنَهُمْ﴾", "Consultation spreads responsibility.")
        )
        nation_sharia = st.slider(
            t("تحكيم الشرع", "Applying Sharia"), 0.0, 1.0, 0.5, 0.01,
            key="nation_sharia",
            help=t("تحكيم شرع الله يحفظ الحقوق. ﴿وَمَن لَّمْ يَحْكُم بِمَا أَنزَلَ اللَّهُ﴾", "Applying Allah's law preserves rights.")
        )

    # السيناريوهات التاريخية
    st.markdown("---")
    st.markdown(t("### 📜 سيناريوهات تاريخية", "### 📜 Historical Presets"))
    pcol = st.columns(4)
    
    if pcol[0].button(t("🏴 الخلافة الراشدة", "🏴 Rashidun Caliphate"), use_container_width=True):
        nation_prayer = 0.9; nation_fasting = 0.8; nation_zakat = 0.9; nation_hajj = 0.7
        nation_jihad_self = 0.9; nation_jihad_wealth = 0.8; nation_disavowal = 0.9; nation_alliance = 0.9
        nation_justice = 0.9; nation_shura = 0.8; nation_sharia = 0.9
        st.rerun()
    
    if pcol[1].button(t("🏳️ العثمانيون ١٨٠٠", "🏳️ Ottomans 1800"), use_container_width=True):
        nation_prayer = 0.5; nation_fasting = 0.4; nation_zakat = 0.3; nation_hajj = 0.3
        nation_jihad_self = 0.4; nation_jihad_wealth = 0.2; nation_disavowal = 0.3; nation_alliance = 0.5
        nation_justice = 0.4; nation_shura = 0.3; nation_sharia = 0.4
        st.rerun()
    
    if pcol[2].button(t("🔻 الاتحاد السوفيتي", "🔻 Soviet Union"), use_container_width=True):
        nation_prayer = 0.0; nation_fasting = 0.0; nation_zakat = 0.0; nation_hajj = 0.0
        nation_jihad_self = 0.0; nation_jihad_wealth = 0.0; nation_disavowal = 0.0; nation_alliance = 0.0
        nation_justice = 0.0; nation_shura = 0.0; nation_sharia = 0.0
        st.rerun()
    
    if pcol[3].button(t("🕌 الأندلس قبل السقوط", "🕌 Andalusia Before Fall"), use_container_width=True):
        nation_prayer = 0.4; nation_fasting = 0.3; nation_zakat = 0.2; nation_hajj = 0.2
        nation_jihad_self = 0.2; nation_jihad_wealth = 0.1; nation_disavowal = 0.2; nation_alliance = 0.3
        nation_justice = 0.3; nation_shura = 0.2; nation_sharia = 0.3
        st.rerun()

    # زر تشغيل محاكاة الأمة
    st.markdown("---")
    if st.button(t("🚀 أطلق محاكاة الأمة", "🚀 Launch Nation Simulation"), use_container_width=True, type="primary"):
        with st.spinner(t("محاكاة الأمة تعمل...", "Nation simulation running...")):
            # حساب W و B الابتدائيين
            W_nation = (nation_prayer + nation_hajj + nation_alliance + nation_sharia + nation_justice * 0.5) / 4.5
            B_nation = (nation_fasting + nation_zakat + nation_jihad_self + nation_jihad_wealth + nation_disavowal + nation_justice * 0.5) / 5.5
            W_nation = np.clip(W_nation, 0.01, 1.0)
            B_nation = np.clip(B_nation, 0.01, 1.0)

            # محاكاة ٣٠٠ سنة
            years = 300
            W_hist = np.zeros(years)
            B_hist = np.zeros(years)
            S_hist = np.zeros(years)
            E_hist = np.zeros(years)

            W_hist[0] = W_nation
            B_hist[0] = B_nation
            S_hist[0] = W_nation * B_nation
            E_hist[0] = 0.1

            for t in range(1, years):
                # الاستدراج: التمكين يضعف الولاء والبراءة
                W_hist[t] = W_hist[t-1] - 0.01 * E_hist[t-1] + 0.01 * nation_prayer * nation_alliance
                B_hist[t] = B_hist[t-1] - 0.008 * E_hist[t-1] + 0.01 * nation_disavowal * nation_jihad_self

                # أسس الحكم تمنع الانهيار
                W_hist[t] += 0.005 * nation_sharia * nation_justice
                B_hist[t] += 0.005 * nation_sharia * nation_justice

                W_hist[t] = np.clip(W_hist[t], 0.01, 1.0)
                B_hist[t] = np.clip(B_hist[t], 0.01, 1.0)

                S_hist[t] = W_hist[t] * B_hist[t]

                # التمكين يتأخر عن الثبات (الاستدراج)
                E_target = S_hist[max(0, t - lag_frames)]
                E_hist[t] = E_hist[t-1] + 0.03 * (E_target - E_hist[t-1])
                E_hist[t] = np.clip(E_hist[t], 0.01, 1.0)

            # رسم النتائج
            fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#000010')

            # الرسم الأول: دورة الأمة
            ax1 = axes[0]
            ax1.set_facecolor('#0a0a1a')
            ax1.plot(S_hist, 'g-', lw=2.5, label=t('S (الثبات)', 'S (Stability)'))
            ax1.plot(E_hist, 'b--', lw=2.0, label=t('E (التمكين)', 'E (Empowerment)'))
            ax1.plot(W_hist, color='gold', lw=1.5, alpha=0.7, label=t('W (الولاء)', 'W (Loyalty)'))
            ax1.plot(B_hist, color='#FF5252', lw=1.5, alpha=0.7, label=t('B (البراءة)', 'B (Disavowal)'))

            # فجوة الاستدراج
            idx_S_max = np.argmax(S_hist)
            idx_E_max = np.argmax(E_hist)
            if idx_S_max < idx_E_max:
                ax1.axvspan(idx_S_max, idx_E_max, alpha=0.2, color='red',
                           label=t('فجوة الاستدراج', 'Istidraj Gap'))

            ax1.set_title(t('دورة الأمة عبر ٣٠٠ عام', 'Nation Cycle Over 300 Years'),
                         color='white', fontsize=14, fontweight='bold')
            ax1.set_xlabel(t('السنوات', 'Years'), color='white')
            ax1.set_ylabel(t('القيمة', 'Value'), color='white')
            ax1.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax1.grid(True, alpha=0.2)
            ax1.tick_params(colors='white')
            ax1.set_ylim(0, 1.05)

            # الرسم الثاني: مسار الأمة في فضاء (W, B)
            ax2 = axes[1]
            ax2.set_facecolor('#0a0a1a')
            ax2.plot(B_hist, W_hist, 'w-', alpha=0.4, lw=0.8)
            ax2.scatter(B_hist[0], W_hist[0], s=150, c='green', edgecolors='white',
                       linewidth=2, zorder=10, label=t('البداية', 'Start'))
            ax2.scatter(B_hist[-1], W_hist[-1], s=150, c='red', edgecolors='white',
                       linewidth=2, zorder=10, label=t('النهاية', 'End'))
            ax2.axhline(0.5, color='grey', ls=':', lw=1)
            ax2.axvline(0.5, color='grey', ls=':', lw=1)
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.set_xlabel('B (البراءة)', color='white')
            ax2.set_ylabel('W (الولاء)', color='white')
            ax2.set_title(t('مسار الأمة في فضاء (W, B)', 'Nation Path in (W, B) Space'),
                         color='white', fontsize=14, fontweight='bold')

            # تلوين الأرباع
            ax2.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green')
            ax2.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='orange')
            ax2.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='blue')
            ax2.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='red')
            ax2.text(0.75, 0.75, t('مؤمنة', 'Believing'), color='green', fontsize=9, ha='center')
            ax2.text(0.25, 0.75, t('كافرة', 'Disbelieving'), color='orange', fontsize=9, ha='center')
            ax2.text(0.25, 0.25, t('منافقة', 'Hypocritical'), color='red', fontsize=9, ha='center')
            ax2.text(0.75, 0.25, t('مشركة', 'Polytheistic'), color='blue', fontsize=9, ha='center')
            ax2.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax2.grid(True, alpha=0.2)
            ax2.tick_params(colors='white')

            plt.tight_layout()
            st.pyplot(fig)

            # مؤشرات حية
            st.divider()
            st.subheader(t("📊 مؤشرات الأمة", "📊 Nation Indicators"))

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric(t("W النهائي", "Final W"), f"{W_hist[-1]:.3f}")
            with c2:
                st.metric(t("B النهائي", "Final B"), f"{B_hist[-1]:.3f}")
            with c3:
                st.metric(t("S النهائي", "Final S"), f"{S_hist[-1]:.3f}")
            with c4:
                collapse_year = np.argmin(S_hist)
                if S_hist[collapse_year] < 0.2:
                    st.metric(t("عام الانهيار", "Collapse Year"), f"{collapse_year}")
                else:
                    st.metric(t("الحالة", "Status"), t("مستقرة", "Stable"))
            with c5:
                istidraj_gap = max(0, np.argmax(E_hist) - np.argmax(S_hist))
                st.metric(t("فجوة الاستدراج", "Istidraj Gap"), f"{istidraj_gap} {t('عام', 'yrs')}")

            # تحليل الحالة
            st.divider()
            if S_hist[-1] > 0.7:
                st.success(t(
                    "✅ الأمة في حالة استقرار عالٍ. مولدات الطاقة تعمل وحدود البراءة قوية.",
                    "✅ The nation is highly stable. Energy generators work and disavowal boundaries are strong."
                ))
            elif S_hist[-1] > 0.4:
                st.warning(t(
                    "⚠️ الأمة في حالة متوسطة. توجد مؤشرات تراجع. انتبه لفجوة الاستدراج.",
                    "⚠️ The nation is moderate. There are signs of decline. Watch the Istidraj gap."
                ))
            else:
                st.error(t(
                    "🔴 الأمة في حالة انهيار أو تقترب منه. يجب إصلاح شامل لمولدات الطاقة وحدود البراءة.",
                    "🔴 The nation is collapsing. Comprehensive reform of energy generators and disavowal boundaries is needed."
                ))

print("✅ المرحلة السابعة مكتملة: تبويب مختبر الأمة مع دورة الـ ٣٠٠ عام.")

# ═══════════════════════════════════
# تبويب ٦: مختبر الحضارات
# ═══════════════════════════════════
with tabs[5]:
    st.header(t("🏰 مختبر الحضارات – صراع البقاء", "🏰 Civilizations Lab – Survival of the Fittest"))
    st.markdown(t(
        "قارن بين أربع حضارات تبدأ من قيم W و B مختلفة. شاهد كيف تتفاعل تحت ميزان الحق (ق)، "
        "وكيف أن البقاء للأصلح: الأصلح ميزاناً.",
        
        "Compare four civilizations starting from different W and B values. Watch how they interact "
        "under the Balance of Truth (Q), and how the fittest survives: fittest in Mizan."
    ))

    # تعريف الحضارات الأربع
    civilizations = {
        t("🟡 حضارة الإيمان", "🟡 Civilization of Faith"): (0.9, 0.9, 0.1, '#FFD700'),
        t("🔴 حضارة الإلحاد", "🔴 Civilization of Atheism"): (0.1, 0.8, 0.6, '#FF5252'),
        t("🩷 حضارة النفاق", "🩷 Civilization of Hypocrisy"): (0.3, 0.2, 0.7, '#FFB6C1'),
        t("🟠 حضارة الترف", "🟠 Civilization of Luxury"): (0.7, 0.1, 0.5, '#FFA500'),
    }

    if st.button(t("🚀 أطلق صراع الحضارات", "🚀 Launch Clash of Civilizations"), use_container_width=True, type="primary"):
        with st.spinner(t("صراع الحضارات جارٍ...", "Clash of civilizations in progress...")):
            fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#000010')
            
            for idx, (name, (w0, b0, e0, color)) in enumerate(civilizations.items()):
                ax = axes[idx // 2, idx % 2]
                ax.set_facecolor('#0a0a1a')
                
                # محاكاة ٢٠٠ سنة لكل حضارة
                years = 200
                W_civ = np.zeros(years)
                B_civ = np.zeros(years)
                S_civ = np.zeros(years)
                E_civ = np.zeros(years)
                
                W_civ[0], B_civ[0], E_civ[0] = w0, b0, e0
                S_civ[0] = w0 * b0
                
                for t in range(1, years):
                    # التمكين يضعف الولاء والبراءة (الاستدراج)
                    W_civ[t] = W_civ[t-1] - 0.02 * E_civ[t-1]
                    B_civ[t] = B_civ[t-1] - 0.015 * E_civ[t-1]
                    
                    # إذا انهارت B، تنهار W أسرع، والعكس
                    if B_civ[t-1] < 0.3:
                        W_civ[t] -= 0.01
                    if W_civ[t-1] < 0.3:
                        B_civ[t] -= 0.01
                    
                    W_civ[t] = np.clip(W_civ[t], 0.01, 1.0)
                    B_civ[t] = np.clip(B_civ[t], 0.01, 1.0)
                    S_civ[t] = W_civ[t] * B_civ[t]
                    
                    # الاستدراج
                    lag = 22
                    past = S_civ[max(0, t-lag)]
                    E_civ[t] = E_civ[t-1] + 0.04 * (past - E_civ[t-1])
                    E_civ[t] = np.clip(E_civ[t], 0.01, 1.0)
                
                # رسم منحنيات الحضارة
                ax.plot(S_civ, color=color, lw=2.5, label='S (الثبات)')
                ax.plot(E_civ, color=color, lw=1.5, ls='--', alpha=0.6, label='E (التمكين)')
                
                # فجوة الاستدراج
                idx_S = np.argmax(S_civ)
                idx_E = np.argmax(E_civ)
                if idx_S < idx_E:
                    ax.axvspan(idx_S, idx_E, alpha=0.15, color='red')
                
                # نتيجة الحضارة
                if S_civ[-1] > 0.5:
                    status = t("✅ باقية", "✅ Survived")
                    status_color = 'green'
                elif S_civ[-1] > 0.2:
                    status = t("⚠️ مهددة", "⚠️ Threatened")
                    status_color = 'orange'
                else:
                    status = t("🔴 منهارة", "🔴 Collapsed")
                    status_color = 'red'
                
                ax.set_title(f"{name}\n{status}", color=color, fontsize=12, fontweight='bold')
                ax.set_ylim(0, 1.05)
                ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=7)
                ax.grid(True, alpha=0.2)
                ax.tick_params(colors='white')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            st.success(t(
                "✅ البقاء للأصلح ميزاناً. الحضارة التي تحافظ على توازن W و B هي التي تبقى.",
                "✅ Survival of the fittest in Mizan. The civilization that maintains W-B balance survives."
            ))

# ═══════════════════════════════════
# تبويب ٧: لوحة النتائج
# ═══════════════════════════════════
with tabs[6]:
    st.header(t("📊 لوحة النتائج – المختبر الإلهي", "📊 Results Dashboard – The Divine Lab"))
    st.markdown(t(
        "هذه هي لوحة النتائج الشاملة. ترى فيها ملخصاً لكل ما جرى في المختبر: "
        "الكون، المجتمع، الدولة، الأمة، والحضارات. كلها تحكمها معادلة واحدة: **S = W × B**.",
        
        "This is the comprehensive results dashboard. You see a summary of everything in the lab: "
        "cosmos, society, state, nation, and civilizations. All governed by one equation: **S = W × B**."
    ))

    # عرض المؤشرات الحالية من حالة الجلسة
    if st.session_state.get('init_global'):
        st.markdown("### 🌌 المؤشرات الحية للمختبر")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric(t("W (الولاء)", "W (Loyalty)"), f"{st.session_state.W:.3f}")
        with col2:
            st.metric(t("B (البراءة)", "B (Disavowal)"), f"{st.session_state.B:.3f}")
        with col3:
            st.metric(t("S (الثبات)", "S (Stability)"), f"{st.session_state.S:.3f}")
        with col4:
            st.metric(t("E (التمكين)", "E (Empowerment)"), f"{st.session_state.E:.3f}")
        with col5:
            st.metric(t("الطور", "Phase"), st.session_state.phase)
        with col6:
            kappa = compute_curvature(
                list(st.session_state.planet_W_hist),
                list(st.session_state.planet_B_hist)
            )
            st.metric(t("κ (الانحناء)", "κ (Curvature)"), f"{kappa:.4f}")
        
        # الميزان الأخروي
        st.divider()
        st.markdown("### 📜 الميزان الأخروي")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(t("الحسنات", "Good Deeds"), f"{st.session_state.good_deeds:.1f}")
        with col2:
            st.metric(t("السيئات", "Bad Deeds"), f"{st.session_state.bad_deeds:.1f}")
        with col3:
            balance = st.session_state.good_deeds - st.session_state.bad_deeds
            st.metric(
                t("الميزان", "Balance"),
                f"{balance:+.1f}",
                delta=t("راجحة" if balance > 0 else "خاسرة", "Winning" if balance > 0 else "Losing")
            )
        
        # المعادلة المركزية
        st.divider()
        st.markdown(f"""
        <div style="text-align: center; padding: 25px; background: rgba(10,10,46,0.9);
                    border-radius: 15px; border: 2px solid #FFD700; margin: 20px 0;">
            <h2 style="color: #FFD700; font-size: 2em; margin: 0;">⚖️ S = W × B</h2>
            <p style="color: #CCC; font-size: 1.1em; margin-top: 10px;">
                {t('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}
            </p>
            <p style="color: #888; font-size: 0.9em; margin-top: 5px;">
                {t('ق = ١٠٠ = الحق = الميزان', 'Q = 100 = Truth = Balance')}
            </p>
            <p style="color: #AAA; font-size: 0.85em; margin-top: 10px;">
                {t('﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾',
                   '﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾')}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════
# التذييل النهائي
# ═══════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: #888; font-size: 0.9em; line-height: 1.8;">
    <p style="color: #FFD700; font-size: 1.5em; margin: 0;">⚖️ مختبر الميزان</p>
    <p style="margin: 5px 0;">{t('القانون الواحد: S = W × B', 'The One Law: S = W × B')}</p>
    <p style="margin: 5px 0;">{t('ق = ١٠٠ = الحق = الميزان', 'Q = 100 = Truth = Balance')}</p>
    <p style="margin: 5px 0;">© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size: 0.8em; margin-top: 10px;">
        {t('هذا المختبر شهادة رقمية على أن الله حق، وأن وعده حق، وأن لقاءه حق، وأن الجنة حق، وأن النار حق.',
           'This lab is a digital testimony that Allah is Truth, His promise is true, the meeting with Him is true, Paradise is true, and Hell is true.')}
    </p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الثامنة مكتملة: مختبر الحضارات ولوحة النتائج والتذييل.")
print("✅✅✅ المنصة الكاملة جاهزة: ٧ تبويبات، من الذرة إلى الحضارة.")
