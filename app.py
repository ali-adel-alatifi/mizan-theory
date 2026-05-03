import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random, time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ====================== إعداد الصفحة ======================
st.set_page_config(
    page_title="الدين القيم – قانون التوازن الكوني",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed" # الشريط الجانبي مغلق افتراضياً للجوال
)

# ====================== تصميم CSS للجوال أولاً ======================
st.markdown("""
<style>
    /* تحسين الخطوط والألوان العامة */
    .stApp {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 100%);
    }
    /* تكبير الخطوط قليلاً لتناسب شاشات الجوال */
    html, body, [class*="css"] {
        font-size: 16px;
    }
    /* عنوان الصفحة */
    .main-title {
        font-size: 2.2em;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        text-shadow: 0 0 15px rgba(255,215,0,0.6);
        margin-bottom: 0;
    }
    .sub-title {
        font-size: 1.2em;
        color: #FFD700;
        text-align: center;
        margin-top: 0;
        margin-bottom: 20px;
    }
    /* بطاقات المؤشرات */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px 5px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 5px 0;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        margin: 0;
    }
    .metric-label {
        font-size: 0.8em;
        color: #aaa;
        margin: 0;
    }
    /* تحسين شكل الأزرار */
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
        height: 3em;
    }
    /* تحسين شكل أشرطة التمرير */
    .stSlider>div>div>div>div {
        background: #FFD700;
    }
    /* إخفاء عناصر غير ضرورية */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== عنوان التطبيق ======================
st.markdown('<p class="main-title">⚖️ الدِّينُ الْقَيِّم</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">قَانُونُ التَّوَازُنِ الْكَوْنِيّ | S = W × B</p>', unsafe_allow_html=True)

# ====================== القائمة الجانبية (تظهر كقائمة منسدلة في الجوال) ======================
with st.sidebar:
    st.markdown("### ⚙️ لوحة التحكم")
    
    tab_controls, tab_about = st.tabs(["🎛️ المتحكمات", "📜 عن النظرية"])
    
    with tab_controls:
        st.markdown("##### 🕌 أركان الإسلام")
        prayer = st.slider("الصلاة 🟣", 0.0, 1.0, 0.8, 0.01)
        zakat = st.slider("الزكاة 🟡", 0.0, 1.0, 0.6, 0.01)
        fasting = st.slider("الصوم 🟠", 0.0, 1.0, 0.7, 0.01)
        hajj = st.slider("الحج 🔵", 0.0, 1.0, 0.5, 0.01)

        st.markdown("##### 🏛️ أسس الحكم")
        amr = st.slider("الأمر بالمعروف 📢", 0.0, 1.0, 0.5, 0.01)
        nahy = st.slider("النهي عن المنكر 🚫", 0.0, 1.0, 0.5, 0.01)
        adl = st.slider("العدل ⚖️", 0.0, 1.0, 0.6, 0.01)
        shura = st.slider("الشورى 🤝", 0.0, 1.0, 0.5, 0.01)

        st.markdown("##### 🦠 الأمراض الأخلاقية")
        riba = st.slider("الربا 💸", 0.0, 1.0, 0.2, 0.01)
        ghish = st.slider("الغش 🎭", 0.0, 1.0, 0.2, 0.01)
        kadhib = st.slider("الكذب 🤥", 0.0, 1.0, 0.2, 0.01)

        st.markdown("##### ⚡ إعدادات المحاكاة")
        W_init = st.slider("W الابتدائي", 0.0, 1.0, 0.55, 0.01)
        B_init = st.slider("B الابتدائي", 0.0, 1.0, 0.52, 0.01)
        cycle_speed = st.slider("سرعة الدورة (ث)", 0.05, 0.5, 0.15, 0.01)
        delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1)

        cols = st.columns(3)
        if cols[0].button("▶️ تشغيل"): st.session_state.run = True
        if cols[1].button("⏹️ إيقاف"): st.session_state.run = False
        if cols[2].button("🔄 إعادة"): 
            st.session_state.init = False
            st.rerun()

    with tab_about:
        st.markdown("""
        ### ❓ كيف تقرأ المشهد؟
        - **النجوم (النقاط)** : كيانات (أفراد/مجتمعات).
        - **اللون الذهبي**: توازن مثالي (W و B مرتفعان).
        - **اللون الأحمر**: براءة مهيمنة.
        - **اللون الرمادي**: ولاء مهيمن.
        - **الدائرة المتوهجة**: قوة الاستقرار S.
        - **القرص الأزرق**: التمكين E (قد يكون استدراجاً).
        
        ### 📜 النظرية
        **S = W × B**
        *   **S**: الاستقرار
        *   **W**: الولاء (للقانون الإلهي)
        *   **B**: البراءة (من الباطل)
        
        من الذرة إلى الحضارة، كل شيء يسير بهذا القانون. استقراركم ليس صدفة، وانهياركم ليس حظاً سيئاً. إنها معادلة.
        """)

# ====================== دوال مساعدة (معدلة للكفاءة) ======================
def get_color(w, b):
    if w >= 0.7 and b >= 0.7: return '#FFD700'
    if w >= 0.55 and b < 0.45: return '#E0E0E0'
    if w < 0.45 and b >= 0.55: return '#FF5252'
    if w < 0.45 and b < 0.45: return '#FF8A80'
    return '#FFF9C4' if w > b else '#FFCCBC'

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

# ====================== تهيئة الحالة ======================
if 'run' not in st.session_state: st.session_state.run = False
if 'init' not in st.session_state: st.session_state.init = False
if not st.session_state.init:
    # إعدادات تناسب الأداء على الجوال
    N_STARS = 100
    np.random.seed(42); random.seed(42)
    st.session_state.cx, st.session_state.cy = 5, 5
    st.session_state.sx = np.random.uniform(0, 10, N_STARS)
    st.session_state.sy = np.random.uniform(0, 10, N_STARS)
    st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
    st.session_state.W = W_init; st.session_state.B = B_init
    st.session_state.E = 0.3; st.session_state.S = W_init * B_init
    st.session_state.ph = "استقرار"; st.session_state.ca = 0.0
    st.session_state.eb = deque([W_init * B_init] * 30, maxlen=30)
    st.session_state.pS = deque(maxlen=200); st.session_state.pE = deque(maxlen=200)
    st.session_state.px = deque(maxlen=200); st.session_state.pc = 0
    st.session_state.init = True

# ====================== لوحة المؤشرات العلوية ======================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FFD700;">{st.session_state.S:.3f}</p><p class="metric-label">⚖️ استقرار (S)</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FFFFFF;">{st.session_state.W:.3f}</p><p class="metric-label">🤍 ولاء (W)</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#FF5252;">{st.session_state.B:.3f}</p><p class="metric-label">❤️ براءة (B)</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#00FFFF;">{st.session_state.E:.3f}</p><p class="metric-label">💫 تمكين (E)</p></div>', unsafe_allow_html=True)

# ====================== منطقة الرسم البياني ======================
plot_placeholder = st.empty()

# ====================== المحاكاة الحية (مُحسَّنة للجوال) ======================
if st.session_state.get("run", False):
    while st.session_state.get("run", False):
        try:
            # نسخ الحالة
            W, B, E = st.session_state.W, st.session_state.B, st.session_state.E
            S, ph, ca = st.session_state.S, st.session_state.ph, st.session_state.ca
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx, cy = st.session_state.cx, st.session_state.cy
            eb = st.session_state.eb
            pS = st.session_state.pS; pE = st.session_state.pE; px = st.session_state.px
            
            # --- المنطق الأساسي (مبسط قليلاً للأداء) ---
            ca += 0.1; sv = np.sin(ca)
            target_S = 0.5 + 0.45 * sv
            if sv > 0.5: ph = 'استقرار تام'
            elif sv > 0: ph = 'صعود'
            elif sv > -0.5: ph = 'انهيار'
            else: ph = 'قاع'
            if 0.3 < sv < 0.35: ph = '⚠️ استدراج'
            if -0.35 < sv < -0.3: ph = '🌱 تعافي'

            n = len(sw)
            for i in range(n):
                sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

            avgW = np.mean(sw); avgB = np.mean(sb)
            W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            eb.append(S)
            E += 0.03 * (eb[-delay_frames] if len(eb) > delay_frames else S - E)
            W = W - 0.01 * E + 0.02 / (S + 0.1)
            B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
            W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, riba, ghish, kadhib)
            pS.append(S); pE.append(E); px.append(len(px))
            
            # حركة عشوائية للنجوم
            sx += np.random.uniform(-0.05, 0.05, n); sy += np.random.uniform(-0.05, 0.05, n)
            sx, sy = np.clip(sx, 0, 10), np.clip(sy, 0, 10)

            # حفظ الحالة
            st.session_state.W, st.session_state.B = W, B
            st.session_state.E, st.session_state.S = E, S
            st.session_state.ph, st.session_state.ca = ph, ca
            st.session_state.sx, st.session_state.sy = sx, sy
            st.session_state.sw, st.session_state.sb = sw, sb
            st.session_state.pS, st.session_state.pE, st.session_state.px = pS, pE, px

            # ---------- رسم بياني مُحسَّن للجوال (حجم أصغر) ----------
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
            
            # --- المشهد الكوني المبسط ---
            ax1.set_facecolor('#0a0a1a')
            colors = [get_color(sw[i], sb[i]) for i in range(n)]
            ax1.scatter(sx, sy, c=colors, s=40, alpha=0.8, edgecolors='white', linewidth=0.2)
            # هالة الاستقرار
            ax1.add_patch(plt.Circle((cx, cy), 2 * S, color='#FFD700', alpha=0.2, zorder=0))
            ax1.add_patch(plt.Circle((cx, cy), 1.5 * E, color='#00FFFF', alpha=0.15, zorder=0))
            ax1.text(cx, cy, '⚖️', fontsize=20, ha='center', va='center')
            ax1.set_xlim(0, 10); ax1.set_ylim(0, 10)
            ax1.axis('off')
            ax1.set_title(f'{ph} | S={S:.2f}', color='white', fontsize=14)

            # --- لوحة الإثبات (S vs E) ---
            ax2.set_facecolor('#0a0a1a')
            pSl, pEl, pxl = list(pS), list(pE), list(px)
            ax2.plot(pxl, pSl, color='#FFD700', lw=2, label='S (الاستقرار)')
            ax2.plot(pxl, pEl, color='#00FFFF', lw=2, label='E (التمكين)')
            ax2.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
            ax2.set_ylim(0, 1.05)
            ax2.set_title('📈 لوحة الإثبات', color='white', fontsize=14)
            ax2.tick_params(colors='white')
            ax2.grid(True, alpha=0.2)
            ax2.set_facecolor('#111122')

            plt.tight_layout(pad=2.0)
            plot_placeholder.pyplot(fig)
            plt.close(fig)
            
            time.sleep(cycle_speed)
        except Exception as e:
            st.error(f"خطأ: {str(e)}")
            st.session_state.run = False
            break
    st.success("⏸️ تم إيقاف المحاكاة")
else:
    # عرض ثابت عند عدم التشغيل
    if st.session_state.init:
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
        ax.set_facecolor('#0a0a1a')
        colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx, st.session_state.sy, c=colors, s=40, alpha=0.8, edgecolors='white', linewidth=0.2)
        ax.add_patch(plt.Circle((5, 5), 2 * st.session_state.S, color='#FFD700', alpha=0.2))
        ax.text(5, 5, '⚖️', fontsize=30, ha='center', va='center')
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
        ax.set_title(f'اضغط ▶️ تشغيل للبدء', color='white', fontsize=16)
        plot_placeholder.pyplot(fig)
        plt.close(fig)

# ====================== تذييل الصفحة ======================
st.markdown("---")
st.markdown("<p style='text-align:center;color:gray; font-size:0.8em;'>© 2026 علي عادل العاطفي | v12.0 – مُحسَّن للجوال</p>", unsafe_allow_html=True)
