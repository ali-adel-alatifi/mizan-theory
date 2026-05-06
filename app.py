# =============================================
# ⚖️ الدِّينُ الْقَيِّم – قَانُونُ التَّوَازُنِ الْكَوْنِيّ
# S = W × B | W = الولاء | B = البراءة
# المؤلف: علي عادل العاطفي | Ali Adel Alatifi
# © 2026 جميع الحقوق محفوظة
# =============================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import random
import time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# ⚙️ إعداد الصفحة
# =============================================
st.set_page_config(
    page_title="الدين القيم – المختبر القرآني",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"  # الشريط الجانبي مخفي
)

# =============================================
# 🎨 التنسيق العام
# =============================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%);
    }
    .main-title {
        font-size: 2.5em;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        margin: 10px 0 0 0;
        text-shadow: 0 0 20px rgba(255,215,0,0.3);
    }
    .sub-title {
        font-size: 1.1em;
        color: #CCCCCC;
        text-align: center;
        margin: 0 0 20px 0;
    }
    .stButton > button {
        border: 1px solid #FFD700;
        color: #FFD700;
        background: #1a1a3e;
        border-radius: 8px;
        height: 2.5em;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: #FFD700;
        color: black;
    }
    .metric-box {
        background: rgba(10,10,46,0.8);
        border-radius: 10px;
        padding: 8px 5px;
        text-align: center;
        border: 1px solid rgba(218,165,32,0.3);
    }
    .metric-val {
        font-size: 1.6em;
        font-weight: bold;
        margin: 0;
    }
    .metric-lbl {
        font-size: 0.7em;
        color: #aaa;
        margin: 0;
    }
    [data-testid="stExpander"] details {
        background: rgba(10,10,40,0.5);
        border: 1px solid rgba(218,165,32,0.3);
        border-radius: 8px;
    }
    [data-testid="stExpander"] summary {
        color: #FFD700;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ العنوان الرئيسي
# =============================================
st.markdown('<p class="main-title">⚖️ الدِّينُ الْقَيِّم ⚖️</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">المختبر القرآني – نظرية الميزان | S = W × B</p>', unsafe_allow_html=True)
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi")

# =============================================
# 📑 ألسنة التبويب الرئيسية
# =============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌌 المختبر الحي",
    "🧭 البوصلة الكونية",
    "📖 كتاب الميزان",
    "📜 رسالة الترحيب",
    "📋 الدليل المرجعي"
])

# =============================================
# 🎨 نظام الألوان الموحد
# =============================================
# ذهبي = مؤمن، أحمر = كافر، وردي = منافق، برتقالي = مشرك
COLORS = {
    "مؤمن":   "#FFD700",
    "كافر":   "#FF3333",
    "منافق":  "#FFB6C1",
    "مشرك":   "#FFA500"
}

def get_mizan_color(w, b):
    """
    تُرجع لون النجمة بناءً على معادلة الميزان.
    """
    if w >= 0.6 and b >= 0.6:
        return COLORS["مؤمن"]      # ذهبي
    elif w >= 0.6 and b < 0.4:
        return COLORS["مشرك"]      # برتقالي
    elif w < 0.4 and b >= 0.6:
        return COLORS["كافر"]      # أحمر
    elif w < 0.4 and b < 0.4:
        return COLORS["منافق"]     # وردي
    else:
        # حالات وسطية
        if w > b:
            return '#FFF8DC'
        elif b > w:
            return '#FFA07A'
        else:
            return '#FFBF00'

def get_quadrant_name(L_map, D_map):
    """تُرجع اسم الربع بناءً على إحداثيات (L, D)."""
    if L_map > 0 and D_map > 0:
        return "مؤمن (الربع الأول)"
    elif L_map < 0 and D_map > 0:
        return "كافر (الربع الثاني)"
    elif L_map < 0 and D_map < 0:
        return "منافق (الربع الثالث)"
    elif L_map > 0 and D_map < 0:
        return "مشرك (الربع الرابع)"
    else:
        return "منطقة محايدة"

def get_quadrant_color(L_map, D_map):
    """تُرجع لون الربع بناءً على إحداثيات (L, D)."""
    if L_map > 0 and D_map > 0:
        return COLORS["مؤمن"]
    elif L_map < 0 and D_map > 0:
        return COLORS["كافر"]
    elif L_map < 0 and D_map < 0:
        return COLORS["منافق"]
    elif L_map > 0 and D_map < 0:
        return COLORS["مشرك"]
    else:
        return "#888888"
        # =============================================
# 🌌 تبويب المختبر الحي
# =============================================
with tab1:

    # --- دالة حساب S ---
    def calc_S(W, B, E, V):
        Sb = W * B
        pillars_boost = (V['أ']*1 + V['ل']*30 + V['م']*40 + V['ص']*90 + V['ك']*20) / 5
        Sb *= (0.5 + 0.5 * pillars_boost)
        protection = (V['ر']*200 + V['هـ']*5 + V['ي']*10 + V['ع']*70 + V['ط']*9 + V['س']*60 + V['ح']*8) / 7
        Sb *= (0.8 + 0.4 * protection)
        Sb *= (0.9 + 0.2 * V['ق'] * 100)
        Sb *= (0.85 + 0.3 * V['ن'] * 50)
        dark_factor = 1 - 0.05*(V['ظ']*900) - 0.03*(V['ض']*800) - 0.02*(V['ذ']*700) - 0.04*(V['خ']*600) - 0.03*(V['ش']*300) - 0.01*(V['ز']*7) - 0.05*(V['غ']*1000) - 0.02*(V['ج']*3)
        Sb *= max(0.1, dark_factor)
        op_effect = (V['ف']*80 + V['و']*6 + V['ب']*2 + V['ل2']*30 + V['ت']*400 + V['ث']*500) / 6
        Sb *= (0.5 + 0.5 * op_effect)
        if E > Sb:
            Sb -= (V['غ']*1000 / 1000) * (E - Sb) * 0.3
        return np.clip(Sb, 0.001, 1.0)

    # --- لوحة التحكم المدمجة (قابلة للطي) ---
    with st.expander("🎛️ لوحة التحكم – مولدات ومثبطات الميزان", expanded=False):
        st.markdown("### ⚙️ اضبط قيم المولدات والمثبطات، ثم اضغط تشغيل")
        
        # صف الأزرار العلوي
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            play_btn = st.button("▶️ تشغيل", use_container_width=True)
        with c2:
            stop_btn = st.button("⏹️ إيقاف", use_container_width=True)
        with c3:
            reset_btn = st.button("🔄 إعادة ضبط", use_container_width=True)
        with c4:
            clear_btn = st.button("🧹 تنظيف", use_container_width=True)
            
        if play_btn: st.session_state.run = True
        if stop_btn: st.session_state.run = False
        if reset_btn:
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
        if clear_btn:
            st.cache_data.clear()
            st.cache_resource.clear()
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
        
        st.divider()
        
        # موسعات المتغيرات
        V = {}
        col_a, col_b = st.columns(2)
        
        with col_a:
            with st.expander("🔆 مولدات الولاء والبراءة (14)", expanded=False):
                V['أ'] = st.slider("الوحدانية (أ=1)", 0.0, 1.0, 0.7, 0.01)
                V['ل'] = st.slider("المُلك والعدل (ل=30)", 0.0, 1.0, 0.6, 0.01)
                V['م'] = st.slider("الجمع (م=40)", 0.0, 1.0, 0.6, 0.01)
                V['ص'] = st.slider("الصمد (ص=90)", 0.0, 1.0, 0.6, 0.01)
                V['ر'] = st.slider("اليقظة (ر=200)", 0.0, 1.0, 0.6, 0.01)
                V['ك'] = st.slider("الأمر (ك=20)", 0.0, 1.0, 0.6, 0.01)
                V['هـ'] = st.slider("الهوية (هـ=5)", 0.0, 1.0, 0.6, 0.01)
                V['ي'] = st.slider("الاستجابة (ي=10)", 0.0, 1.0, 0.6, 0.01)
                V['ع'] = st.slider("الإدراك (ع=70)", 0.0, 1.0, 0.6, 0.01)
                V['ط'] = st.slider("الطهارة (ط=9)", 0.0, 1.0, 0.6, 0.01)
                V['س'] = st.slider("السمع (س=60)", 0.0, 1.0, 0.6, 0.01)
                V['ح'] = st.slider("الحياة (ح=8)", 0.0, 1.0, 0.6, 0.01)
                V['ق'] = st.slider("الميزان (ق=100)", 0.0, 1.0, 0.8, 0.01)
                V['ن'] = st.slider("النور (ن=50)", 0.0, 1.0, 0.7, 0.01)
        
        with col_b:
            with st.expander("🌑 مثبطات الولاء والبراءة (8)", expanded=False):
                V['ظ'] = st.slider("الظلم (ظ=900)", 0.0, 1.0, 0.2, 0.01)
                V['ض'] = st.slider("الضلال (ض=800)", 0.0, 1.0, 0.2, 0.01)
                V['ذ'] = st.slider("الذل (ذ=700)", 0.0, 1.0, 0.2, 0.01)
                V['خ'] = st.slider("الخيانة (خ=600)", 0.0, 1.0, 0.2, 0.01)
                V['ش'] = st.slider("الشهوة (ش=300)", 0.0, 1.0, 0.2, 0.01)
                V['ز'] = st.slider("الزور (ز=7)", 0.0, 1.0, 0.2, 0.01)
                V['غ'] = st.slider("الغش (غ=1000)", 0.0, 1.0, 0.2, 0.01)
                V['ج'] = st.slider("الجهل (ج=3)", 0.0, 1.0, 0.2, 0.01)
            
            with st.expander("⚙️ المشغلات والمؤثرات (6)", expanded=False):
                V['ف'] = st.slider("السببية (ف=80)", 0.0, 1.0, 0.5, 0.01)
                V['و'] = st.slider("العطف (و=6)", 0.0, 1.0, 0.5, 0.01)
                V['ب'] = st.slider("الاستعانة (ب=2)", 0.0, 1.0, 0.5, 0.01)
                V['ل2'] = st.slider("التعليل (ل=30)", 0.0, 1.0, 0.5, 0.01)
                V['ت'] = st.slider("التأني (ت=400)", 0.0, 1.0, 0.5, 0.01)
                V['ث'] = st.slider("الثبات (ث=500)", 0.0, 1.0, 0.5, 0.01)
            
            with st.expander("⚙️ إعدادات المحاكاة", expanded=True):
                cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001)
                delay_frames = st.slider("تأخير التمكين (الاستدراج)", 5, 50, 22, 1)
                N_STARS = st.slider("عدد النجوم", 50, 300, 150, 10)

    # --- تهيئة المحاكاة ---
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init' not in st.session_state: st.session_state.init = False

    if not st.session_state.init:
        np.random.seed(42)
        random.seed(42)
        n = N_STARS if 'N_STARS' in locals() else 150
        cx, cy = 14, 10.0
        st.session_state.cx = cx
        st.session_state.cy = cy
        st.session_state.sx = np.random.uniform(cx-13, cx+13, n)
        st.session_state.sy = np.random.uniform(cy-9, cy+9, n)
        st.session_state.sw = np.random.uniform(0.1, 1.0, n)
        st.session_state.sb = np.random.uniform(0.1, 1.0, n)
        st.session_state.W = 0.55
        st.session_state.B = 0.52
        st.session_state.E = 0.3
        st.session_state.S = 0.286
        st.session_state.ph = "استقرار"
        st.session_state.ca = 0.0
        st.session_state.aW = 0.0
        st.session_state.aB = np.pi * 0.5
        st.session_state.aa = 0.0
        st.session_state.eb = deque([0.286]*30, maxlen=30)
        st.session_state.pS = deque(maxlen=400)
        st.session_state.pE = deque(maxlen=400)
        st.session_state.px = deque(maxlen=400)
        st.session_state.pc = 0
        st.session_state.hasanat = 10.0
        st.session_state.sayyiat = 5.0
        st.session_state.init = True

    # --- مؤشرات الميزان ---
    if st.session_state.init:
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFD700;">{st.session_state.S:.3f}</p><p class="metric-lbl">⚖️ S (الثبات)</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFF;">{st.session_state.W:.3f}</p><p class="metric-lbl">🤍 W (الولاء)</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FF5252;">{st.session_state.B:.3f}</p><p class="metric-lbl">❤️ B (البراءة)</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#00FFFF;">{st.session_state.E:.3f}</p><p class="metric-lbl">💫 E (التمكين)</p></div>', unsafe_allow_html=True)
        with m5:
            mizan_akhira = st.session_state.hasanat - st.session_state.sayyiat
            color = "#FFD700" if mizan_akhira >= 0 else "#FF3333"
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:{color};">{mizan_akhira:.3f}</p><p class="metric-lbl">📜 الميزان الأخروي</p></div>', unsafe_allow_html=True)

    plot_placeholder = st.empty()

    # --- المحاكاة الحية ---
    if st.session_state.get("run", False):
        while st.session_state.run:
            try:
                W = st.session_state.W
                B = st.session_state.B
                E = st.session_state.E
                S = st.session_state.S
                ph = st.session_state.ph
                ca = st.session_state.ca
                aW = st.session_state.aW
                aB = st.session_state.aB
                aa = st.session_state.aa
                sx = st.session_state.sx.copy()
                sy = st.session_state.sy.copy()
                sw = st.session_state.sw.copy()
                sb = st.session_state.sb.copy()
                cx, cy = st.session_state.cx, st.session_state.cy
                eb = st.session_state.eb
                pS = st.session_state.pS
                pE = st.session_state.pE
                px = st.session_state.px

                ca += cycle_speed
                sv = np.sin(ca)
                target_S = 0.5 + 0.45 * sv
                if sv > 0.5: ph = 'استقرار تام'
                elif sv > 0: ph = 'صعود'
                elif sv > -0.5: ph = 'انهيار'
                else: ph = 'قاع'
                if 0.3 < sv < 0.35: ph = '>> استدراج <<'
                if -0.35 < sv < -0.3: ph = '>> تعافي <<'

                n = len(sw)
                for i in range(n):
                    w_boost = (V['أ']*1 + V['ل']*30 + V['م']*40 + V['ص']*90 + V['ر']*200 + V['ك']*20 + V['هـ']*5 + V['ي']*10 + V['ع']*70 + V['ط']*9 + V['س']*60 + V['ح']*8 + V['ق']*100 + V['ن']*50) / 14.0 * 0.01
                    sw[i] += w_boost
                    b_boost = (V['ق']*100 + V['ن']*50) / 2.0 * 0.01
                    sb[i] += b_boost
                    dark_effect = (V['ظ']*900 + V['ض']*800 + V['ذ']*700 + V['خ']*600 + V['ش']*300 + V['ز']*7 + V['غ']*1000 + V['ج']*3) / 8.0 * 0.01
                    sw[i] -= dark_effect
                    sb[i] -= dark_effect
                    op_effect = (V['ف']*80 + V['و']*6 + V['ب']*2 + V['ل2']*30 + V['ت']*400 + V['ث']*500) / 6.0 * 0.005
                    sw[i] += op_effect
                    sb[i] += op_effect
                    sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                    sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                    dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                    close = (dist < 2.0) & (np.arange(n) != i)
                    if np.any(close):
                        sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03 * (0.5 + 0.5 * V['ش'] * 300)
                        sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03 * (0.5 + 0.5 * V['ش'] * 300)
                    sw[i] = np.clip(sw[i], 0.01, 1.0)
                    sb[i] = np.clip(sb[i], 0.01, 1.0)

                shock_p = 0.005 * (1 - V['ق'] * 100 * 0.8)
                if random.random() < shock_p:
                    aff = np.random.choice(n, size=int(n * 0.3), replace=False)
                    sw[aff] *= np.random.uniform(0.5, 0.8)
                    sb[aff] *= np.random.uniform(0.5, 0.8)

                avgW = np.mean(sw)
                avgB = np.mean(sb)
                W += (avgW - W) * 0.04
                B += (avgB - B) * 0.04
                W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
                S = calc_S(W, B, E, V)
                eb.append(S)
                if len(eb) > 30: eb.pop(0)
                E_target = eb[-delay_frames] if len(eb) >= delay_frames else S
                E += 0.03 * (E_target - E)
                W = W - 0.01 * E + 0.02 / (S + 0.1)
                B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
                W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
                S = calc_S(W, B, E, V)
                pS.append(S)
                pE.append(E)
                px.append(len(px))
                if len(px) > 400:
                    pS.popleft()
                    pE.popleft()
                    px.popleft()

                st.session_state.hasanat += np.mean(sw) * 0.1
                st.session_state.sayyiat += (1 - np.mean(sb)) * 0.1

                aW += 0.02 + random.uniform(-0.025, 0.025) * (1 - W)**2
                aB += 0.02 + random.uniform(-0.025, 0.025) * (1 - B)**2
                wx = cx + (7 - 2.5 * W) * np.cos(aW)
                wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
                bx = cx + (5 - 1.5 * B) * np.cos(aB)
                by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7
                ins = 1 - np.mean(sw * sb)
                sx += np.random.uniform(-0.07, 0.07, n) * ins
                sy += np.random.uniform(-0.07, 0.07, n) * ins
                sx, sy = np.clip(sx, cx-13, cx+13), np.clip(sy, cy-9, cy+9)

                st.session_state.W, st.session_state.B = W, B
                st.session_state.E, st.session_state.S = E, S
                st.session_state.ph, st.session_state.ca = ph, ca
                st.session_state.aW, st.session_state.aB, st.session_state.aa = aW, aB, aa + 0.12
                st.session_state.eb = eb
                st.session_state.sx, st.session_state.sy = sx, sy
                st.session_state.sw, st.session_state.sb = sw, sb
                st.session_state.pS, st.session_state.pE, st.session_state.px = pS, pE, px

                # ---------- المشهد الكوني ----------
                fig, ax = plt.subplots(figsize=(12, 9), facecolor='#000010')
                ax.set_xlim(0, 28)
                ax.set_ylim(0, 20)
                ax.axis('off')

                # نواة الاستقرار
                for r, a, c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),(2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                    ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
                ax.text(cx, cy, 'S', color='#1a1000', fontsize=18, ha='center', va='center', fontweight='bold')

                # هالة التمكين
                ax.add_patch(Circle((cx,cy), 0.5+14*E, color='#00FFFF', alpha=0.15, zorder=7))
                ax.add_patch(Circle((cx,cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2, zorder=2))

                # النجوم
                colors = [get_mizan_color(sw[i], sb[i]) for i in range(n)]
                ax.scatter(sx, sy, s=40, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)

                # كوكبا W و B
                ax.add_patch(Circle((wx,wy), 0.2+0.5*W, color='#FFF', alpha=1, zorder=13))
                ax.add_patch(Circle((bx,by), 0.2+0.5*B, color='#F33', alpha=0.8, zorder=13))
                ax.text(wx, wy-1.2, 'W', color='#FFF', fontsize=12, ha='center', fontweight='bold')
                ax.text(bx, by-1.2, 'B', color='#F33', fontsize=12, ha='center', fontweight='bold')

                # لوحة الإثبات (واضحة ومكبرة)
                pSl, pEl, pxl = list(pS), list(pE), list(px)
                if pSl:
                    pax = ax.inset_axes([0.25, 0.02, 0.70, 0.18])
                    pax.set_xlim(0, 400)
                    pax.set_ylim(0, 1.05)
                    pax.set_title('📈 لوحة الإثبات: S (الذهب) يقود E (السماوي) — الاستدراج', color='white', fontsize=10, fontweight='bold')
                    pax.tick_params(colors='white', labelsize=7)
                    pax.grid(True, alpha=0.3)
                    pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S (الثبات)')
                    pax.plot(pxl, pEl, color='#00FFFF', lw=2, label='E (التمكين)')
                    pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=8)

                # شريط الحالة
                ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, ha='center', fontweight='bold')
                plt.tight_layout(pad=0)
                plot_placeholder.pyplot(fig)

                # حفظ الصورة للتحميل
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
        # عرض أولي قبل التشغيل
        if st.session_state.init:
            fig, ax = plt.subplots(figsize=(6, 4), facecolor='#000010')
            ax.set_xlim(0, 28)
            ax.set_ylim(0, 20)
            ax.axis('off')
            colors = [get_mizan_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
            ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9)
            ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
            plot_placeholder.pyplot(fig)
            plt.close(fig)

    # --- زر التحميل أسفل المشهد ---
    if 'latest_image' in st.session_state:
        st.download_button("📥 تحميل صورة المشهد", st.session_state.latest_image, "الميزان_الكوني.png", "image/png")
        # =============================================
# 🧭 تبويب البوصلة الكونية (تصميم الموسعات)
# =============================================
with tab2:
    st.header("🧭 البوصلة الكونية")
    st.subheader("اختبار الإحداثيات الوجودية – 28 سؤالاً")
    st.caption("14 سؤالاً للولاء + 14 سؤالاً للبراءة = 28 سؤالاً | S = L × D")

    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    questions = {
        "L": [
            ("الشهادتان: الإخلاص لله ورسوله", ["أساس حياتي (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("الصلاة: الخشوع والمواظبة", ["كل الفروض بخشوع (10)", "معظمها (7)", "بعضها (4)", "لا أصلي (0)"]),
            ("الزكاة: أداء الفريضة والإنفاق", ["أؤديها وأزيد (10)", "أؤدي الفرض (7)", "أخرج شيئاً (4)", "لا أخرج (0)"]),
            ("الصوم: الفرض والتطوع", ["أصوم وأزيد (10)", "أصوم الفرض (7)", "أصوم معظمه (4)", "لا أصوم (0)"]),
            ("الحج: النية والعمل", ["أديته أو أسعى (10)", "لدي نية (7)", "أتمنى فقط (4)", "لا أهتم (0)"]),
            ("قول الحق", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("الصدق", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("الأمانة", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("شهادة الحق", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("تحمل المسؤولية", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("الوفاء بالعهد", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("الحب للمؤمنين", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("القناعة", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("نصرة المؤمنين", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
        ],
        "D": [
            ("الأمر بالمعروف", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("النهي عن المنكر", ["دائماً (10)", "غالباً (7)", "أحياناً (4)", "لا (0)"]),
            ("الجهاد بكل أشكاله", ["بكل أشكاله (10)", "أجاهد نفسي (7)", "أدعم مالياً (4)", "لا أجاهد (0)"]),
            ("البراءة من الشرك", ["أتبرأ تماماً (10)", "أرفض (7)", "لا أهتم (4)", "أحبهم (0)"]),
            ("البراءة من الكفر", ["أرفضه تماماً (10)", "أرفض (7)", "لا أهتم (4)", "أفضله (0)"]),
            ("البراءة من النفاق", ["أرفضه وأحذر (10)", "أرفض (7)", "لا أهتم (4)", "أراه ذكاء (0)"]),
            ("ترك الكذب", ["لا أكذب (10)", "نادراً (7)", "أحياناً (4)", "الكذب أسلوبي (0)"]),
            ("ترك الغش", ["لا أغش (10)", "نادراً (7)", "أحياناً (4)", "الغش أسلوبي (0)"]),
            ("ترك الخيانة", ["لا أخون (10)", "نادراً (7)", "أحياناً (4)", "الخيانة أسلوبي (0)"]),
            ("ترك الظلم", ["لا أظلم (10)", "نادراً (7)", "أحياناً (4)", "الظلم أسلوبي (0)"]),
            ("ترك السرقة", ["لا أسرق (10)", "نادراً (7)", "أحياناً (4)", "السرقة أسلوبي (0)"]),
            ("ترك الزنا", ["لا أقربها (10)", "نادراً (7)", "أحياناً (4)", "لا أتركها (0)"]),
            ("ترك الرياء", ["لا أرائي (10)", "نادراً (7)", "أحياناً (4)", "الرياء أسلوبي (0)"]),
            ("ترك الحسد", ["لا أحسد (10)", "نادراً (7)", "أحياناً (4)", "الحسد أسلوبي (0)"]),
        ]
    }

    # قاموس النقاط
    points_map = {
        "أساس حياتي (10)":10, "غالباً (7)":7, "أحياناً (4)":4, "لا (0)":0,
        "كل الفروض بخشوع (10)":10, "معظمها (7)":7, "بعضها (4)":4, "لا أصلي (0)":0,
        "أؤديها وأزيد (10)":10, "أؤدي الفرض (7)":7, "أخرج شيئاً (4)":4, "لا أخرج (0)":0,
        "أصوم وأزيد (10)":10, "أصوم الفرض (7)":7, "أصوم معظمه (4)":4, "لا أصوم (0)":0,
        "أديته أو أسعى (10)":10, "لدي نية (7)":7, "أتمنى فقط (4)":4, "لا أهتم (0)":0,
        "دائماً (10)":10, "نادراً (7)":7,
        "بكل أشكاله (10)":10, "أجاهد نفسي (7)":7, "أدعم مالياً (4)":4, "لا أجاهد (0)":0,
        "أتبرأ تماماً (10)":10, "أرفض (7)":7, "لا أهتم (4)":4, "أحبهم (0)":0,
        "أرفضه تماماً (10)":10, "أفضله (0)":0,
        "أرفضه وأحذر (10)":10, "أراه ذكاء (0)":0,
        "لا أكذب (10)":10, "الكذب أسلوبي (0)":0,
        "لا أغش (10)":10, "الغش أسلوبي (0)":0,
        "لا أخون (10)":10, "الخيانة أسلوبي (0)":0,
        "لا أظلم (10)":10, "الظلم أسلوبي (0)":0,
        "لا أسرق (10)":10, "السرقة أسلوبي (0)":0,
        "لا أقربها (10)":10, "لا أتركها (0)":0,
        "لا أرائي (10)":10, "الرياء أسلوبي (0)":0,
        "لا أحسد (10)":10, "الحسد أسلوبي (0)":0
    }

    st.markdown("### 📝 أجب بصراحة (كل سؤال في موسع مستقل)")
    st.caption("اضغط على كل سؤال لتظهر خيارات الإجابة")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🤍 أسئلة الولاء (L)")
        for i, q in enumerate(questions["L"]):
            with st.expander(f"{q[0]}", expanded=False):
                ans = st.radio("اختر إجابة:", q[1], key=f"L{i}", index=None)
                if ans:
                    st.session_state.compass_answers[f"L{i}"] = points_map[ans]
                    st.success(f"تم التسجيل: {ans}")

    with col2:
        st.markdown("#### ❤️ أسئلة البراءة (D)")
        for i, q in enumerate(questions["D"]):
            with st.expander(f"{q[0]}", expanded=False):
                ans = st.radio("اختر إجابة:", q[1], key=f"D{i}", index=None)
                if ans:
                    st.session_state.compass_answers[f"D{i}"] = points_map[ans]
                    st.success(f"تم التسجيل: {ans}")

    # --- عرض النتيجة ---
    TOTAL_Q = 28
    if len(st.session_state.compass_answers) == TOTAL_Q:
        L_score = sum([st.session_state.compass_answers[f"L{i}"] for i in range(14)])
        D_score = sum([st.session_state.compass_answers[f"D{i}"] for i in range(14)])
        
        L = L_score / 140.0
        D = D_score / 140.0
        L_map = (L * 2) - 1
        D_map = (D * 2) - 1
        S_val = L * D

        q_name = get_quadrant_name(L_map, D_map)
        q_color = get_quadrant_color(L_map, D_map)
        
        advice = {
            "مؤمن (الربع الأول)": "حافظ على ثباتك واستمر في النمو.",
            "كافر (الربع الثاني)": "أنت بحاجة إلى توبة جذرية.",
            "منافق (الربع الثالث)": "أنت بحاجة إلى الصدق مع نفسك.",
            "مشرك (الربع الرابع)": "قوِّ مناعتك الإيمانية."
        }

        st.divider()
        st.header("📊 نتائج اختبار البوصلة الكونية")
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f"""
            <div style="background: rgba(10,10,46,0.8); border-radius: 15px; padding: 20px; border: 2px solid {q_color}; text-align: center;">
                <p style="font-size: 2em; font-weight: bold; color: {q_color};">{q_name}</p>
                <p>إحداثياتك: <b>L = {L_map:.2f}</b> | <b>D = {D_map:.2f}</b></p>
                <p style="font-size: 1.2em; color: #FFD700;">⚖️ ثباتك الوجودي: <b>S = L × D = {S_val:.2f}</b></p>
                <p style="font-size: 0.8em; color: #aaa;">الدرجة الخام: L = {L_score} / 140 | D = {D_score} / 140</p>
                <p>{advice.get(q_name, '')}</p>
            </div>
            """, unsafe_allow_html=True)

        # --- الخريطة التفاعلية ---
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5)
        ax.axvline(0, color='grey', lw=0.5)
        ax.set_xlabel("البراء (D)", color='white')
        ax.set_ylabel("الولاء (L)", color='white')

        ax.add_patch(Rectangle((0, 0), 1, 1, color=COLORS["مؤمن"], alpha=0.15))
        ax.add_patch(Rectangle((-1, 0), 1, 1, color=COLORS["كافر"], alpha=0.15))
        ax.add_patch(Rectangle((-1, -1), 1, 1, color=COLORS["منافق"], alpha=0.15))
        ax.add_patch(Rectangle((0, -1), 1, 1, color=COLORS["مشرك"], alpha=0.25))

        ax.text(0.5, 0.5, "مؤمن", color='black', ha='center', alpha=0.7)
        ax.text(-0.5, 0.5, "كافر", color='white', ha='center', alpha=0.7)
        ax.text(-0.5, -0.5, "منافق", color='white', ha='center', alpha=0.7)
        ax.text(0.5, -0.5, "مشرك", color='black', ha='center', alpha=0.7)
        
        ax.scatter(D_map, L_map, c='#00FFFF', s=200, edgecolors='white', linewidth=2, zorder=5)
        ax.tick_params(colors='white')
        st.pyplot(fig)

        if st.button("🔄 إعادة الاختبار"):
            st.session_state.compass_answers = {}
            st.rerun()# =============================================
# 📖 تبويب كتاب الميزان (مُراجَع ومُنقَّح)
# =============================================
with tab3:
    st.header("📖 كتاب الميزان")
    st.subheader("المختبر القرآني – من الثنائية الكونية إلى معادلة الوجود")
    st.caption("تأليف: علي عادل العاطفي | © 2026")
    st.divider()

    with st.expander("📜 الإهداء والمقدمة", expanded=False):
        st.markdown("""
        ### الإهداء
        إلى كل باحث عن الحقيقة، يفتش عن الخيط الناظم الذي يربط شتات هذا الوجود.
        إلى كل قلب حائر، يبحث عن الطمأنينة في زمن القلق.
        وإلى كل عقل متعطش، يريد أن يرى كيف يلتقي الوحي بالعلم.

        هذا الكتاب محاولة متواضعة لإعادة الأمور إلى نصابها، ولإثبات أن "الدين" ليس مجرد طقوس،
        بل هو "نظام التشغيل" الذي صممه الخالق لهذا الكون. إنه "الميزان" الذي وضعه الله،
        والذي يجب أن نتعلم كيف نقرأه في كتابه المسطور (القرآن) وكتابه المنظور (الكون).

        ### مقدمة المؤلف
        الحمد لله الذي رفع السماء ووضع الميزان، وجعل في كل شيء آية تدل على أنه الواحد الديان.
        والصلاة والسلام على النبي الأمي الذي أرسله الله بالدين القيم والإسلام الحنيف،
        رحمة للعالمين، وقدوة للسالكين.

        أما بعد، فهذا كتاب "الميزان". وهو ليس كتاباً كغيره من الكتب. إنه محاولة متواضعة،
        ولكنها جادة، لإعادة بناء "نظرية كل شيء" على أسس الوحي، بدلاً من أسس الفلسفة البشرية القاصرة.
        إنه يقدم "الدين القيم" (قانون السببية الأعظم) و"الإسلام الحنيف" (الاستجابة المثلى لهذا القانون)
        كمنظومة متكاملة تفسر الوجود من الذرة إلى الحضارة، ومن الأزل إلى الخلود.

        لقد حاولتُ أن أتتبع هذه المنظومة في كتاب الله المسطور (القرآن)، وفي كتابه المنظور (الآفاق والأنفس)،
        وأن أثبت أنهما يلتقيان على "ميزان" واحد دقيق، هو المعادلة:

        **S = W × B**

        حيث S هو الثبات الوجودي (Stability)، وW هو الولاء لله (Wala')، وB هي البراءة من الطاغوت (Bara'a).
        هذه المعادلة البسيطة في لفظها، العميقة في معناها، هي المفتاح الذي يفتح مغاليق كثيرة،
        ويجيب عن أسئلة حائرة.

        هذا الكتاب ثمرة تدبر وبحث. وهو ليس "علماً" يضاف إلى العلوم، بل هو "أم العلم"
        التي تنتظم تحتها كل العلوم. والله أسأل أن يجعله خالصاً لوجهه، وأن ينفع به كاتبه وقارئه.
        """)

    with st.expander("🔍 تمهيد: البحث عن نظرية كل شيء", expanded=False):
        st.markdown("""
        منذ فجر الوعي، والبشرية تبحث عن إجابة لسؤال واحد:
        ما هو القانون الذي يحكم هذا الوجود؟
        لماذا تسقط ورقة الشجر بهذه الطريقة؟ ولماذا تسقط الحضارات العظيمة بعد أن تبلغ ذروتها؟
        هل هناك نظام واحد يفسر حركة الذرة والمجرة، ونبض الخلية وفناء الأمم؟

        في الفيزياء، قضى أينشتاين عقوده الأخيرة باحثاً عن "نظرية المجال الموحد"
        التي تجمع قوى الكون في معادلة واحدة. وفي الفلسفة، حاول الفلاسفة منذ أفلاطون وهيغل
        صياغة "نظرية كل شيء" تشرح المعنى الكلي للحياة. كان هذا هو "الكأس المقدس" للعلم والفلسفة.
        لكنهم لم يصلوا.

        هذا الكتاب يقدم الإجابة التي بحثوا عنها. إجابة ليست من عند فيزيائي، ولا من عند فيلسوف،
        بل من عند خالق الكون نفسه. الإجابة كانت هنا دائماً، في كتابه المسطور (القرآن)،
        وفي كتابه المنظور (الكون). إنها نظرية "الدين القيم"، أو ما نسميه "الميزان".
        إنها تثبت أن هناك قانوناً واحداً فقط، هو "قانون السببية"، يحكم كل شيء:
        الذرة، الخلية، النفس، الأسرة، المجتمع، الأمة، الحضارة، والتاريخ.

        وهذا القانون يجد تعبيره الأكمل في معادلة الثبات الوجودي: **S = W × B**.

        هذه المعادلة ليست اختراعاً بشرياً، بل هي ترجمة رياضية لقوله تعالى:
        ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256].

        في زمن طغت فيه المادة على الروح، يأتي هذا الكتاب ليعيد للروح مكانتها،
        وليثبت أن "الغيب" هو أصل "الشهادة"، وأن "الوحي" هو مرشد "العقل"،
        وأن "الإيمان" هو "طاقة روحية" يمكن قياسها ومحاكاتها.
        """)

    with st.expander("الباب الأول: الأصول – من أين بدأنا؟", expanded=False):
        st.markdown("""
        ### الفصل الأول: ﴿اقْرَأْ بِاسْمِ رَبِّكَ﴾ – المنهج الإلهي لاكتشاف النظام

        في لحظة فارقة من تاريخ البشرية، تنزلت أول كلمة من السماء إلى الأرض.
        لم تكن أمراً عسكرياً، ولا قانوناً اجتماعياً، بل كانت أمراً معرفياً: ﴿اقْرَأْ﴾.
        إنه الإعلان عن ميلاد "منهج" جديد في النظر إلى الوجود.

        "اقرأ" لم تقتصر على تلاوة الحروف المكتوبة في المصحف، بل شملت قراءة "الكتاب المنظور"
        (الكون والأنفس) وقراءة "الكتاب المسطور" (الوحي). إنها دعوة مزدوجة للجمع بين العلم والإيمان،
        بين الفيزياء والميتافيزيقا، بين الخلق والأمر.

        والأمر لم يكن مطلقاً، بل كان مقيداً بقيد هو "المفتاح" لهذا المنهج: ﴿بِاسْمِ رَبِّكَ﴾.
        هذه هي "عدسة الدين القيم". إنها التي تحول القراءة المادية المحايدة إلى قراءة إيمانية غائية.
        أن تقرأ "باسم ربك" يعني أن تسأل عن "لماذا" و"من" وراء كل ظاهرة، لا أن تكتفي بـ "كيف" حدثت.
        هذا القيد هو "الولاء" (W) الذي يوجه العقل نحو اكتشاف "القانون".

        ### الفصل الثاني: ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ – الإعلان عن القانون الأعظم

        بعد الأمر بالقراءة، يأتي الإعلان عن "القانون" نفسه. يقول الله تعالى:
        ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ﴾ [الرحمن: 7-8].

        هذا هو "الدين القيم". إنه ليس مجرد قوانين فيزيائية تحكم الكون، بل هو أيضاً
        ناموس أخلاقي واجتماعي يحكم حياة الإنسان. إنه القانون الذي يجعل من الذرة مستقرة،
        ومن الخلية حية، ومن الحضارة صامدة.

        لماذا "الميزان"؟ لأن الميزان له كفتان. الكفة الأولى هي "الولاء لله" (W).
        والكفة الثانية هي "البراءة من الطاغوت" (B). والثبات (S) لا يتحقق إلا إذا توازنت الكفتان.

        ### الفصل الثالث: ﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ﴾ – المنهج التجريبي القرآني

        وهذه الآية هي "خريطة الطريق" لمشروعنا:
        ﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ حَتَّىٰ يَتَبَيَّنَ لَهُمْ أَنَّهُ الْحَقُّ﴾ [فصلت: 53].

        إنها دعوة إلهية للبحث العلمي، وللنمذجة والمحاكاة. نحن مدعوون للنظر في "الآفاق"
        (الكون والفيزياء والتاريخ) وفي "الأنفس" (البيولوجيا والنفس والمجتمع)
        لنكتشف "الميزان" الذي يحكم كل شيء.
        """)

    with st.expander("الباب الثاني: التعريفات المركزية – أركان النظرية", expanded=False):
        st.markdown("""
        ### أولاً: الدين القيم – قانون السببية الكوني الثابت

        الدين القيم هو: قانون السببية الأعظم، الثابت في أصله، والمتجدد في تطبيقاته (الحنيفية).
        إنه "الميزان" الذي فطر الله السماوات والأرض عليه، وأرسل به الرسل، وأنزل به الكتب،
        وخلق عليه الإنسان، وعليه الحساب، ومنه الجزاء.

        خصائصه: الربانية (مصدره الله وحده)، الثبات (أصله لا يتغير)، الشمول (يسري على كل العوالم)،
        الحتمية (النتيجة مرتبطة بالسبب)، الديناميكية (يتجدد في تطبيقاته مع ثبات أصله).

        ### ثانياً: الإسلام الحنيف – الاستجابة الكونية الديناميكية

        الإسلام الحنيف هو: الاستجابة الكونية الديناميكية للدين القيم، من خلال آلية
        "الولاء لله" (W) و"البراءة من الطاغوت" (B)، كل عالم بما يناسب فطرته.

        - إسلام الجماد: الجاذبية (W) والتنافر (B). ثباته S = W × B.
        - إسلام النبات والحيوان: النمو (W) والمناعة (B).
        - إسلام الملائكة: التسبيح والعبادة.
        - إسلام الإنسان: الولاء والبراءة طوعاً. S = W × B.

        ### ثالثاً: العقيدة – الإيمان القلبي بعدالة القانون
        العقيدة هي الإيمان القلبي بوحدانية خالق القانون، وعدالة هذا القانون، وحتمية نتائجه.
        وهي تشمل أركان الإيمان الستة. إنها "الطاقة الروحية" التي تولد W في القلب.

        ### رابعاً: العبادة – محطات شحن الميزان
        العبادات ليست طقوساً، بل هي "محطات شحن" للميزان:
        الصلاة تشحن W يومياً. الزكاة تمنع طغيان التمكين E على المناعة B.
        الصيام يدرب B على مقاومة الهوى. الحج محاكاة سنوية كاملة للمعادلة.

        ### خامساً: الشريعة – المنهج والنظام
        الشريعة هي المنهج التفصيلي للعقيدة، والنظام المتكامل للعبادة.
        إنها "دليل المستخدم" الذي يضمن صحة الإيمان وصحة العمل.
        """)

    with st.expander("الباب الثالث: الثنائية الكونية – الولاء والبراء في مرآة الوجود", expanded=False):
        st.markdown("""
        ### الكون يتكلم بلغة الثنائيات
        النور والظلام، الليل والنهار، الذكر والأنثى، الموجب والسالب، الجذب والتنافر.
        هذه الثنائيات ليست عشوائية، بل هي تعبير عن قانون واحد هو "الميزان".
        الولاء والبراء ليسا مفهومين أخلاقيين فقط، بل هما الثنائية الكونية الأساسية.

        ### التطابق مع قوانين الفيزياء
        الجاذبية (W) والتنافر (B) في الذرة. الديناميكا الحرارية: الولاء يقلل الفوضى والبراءة تمنعها.
        التشابك الكمومي: ترابط المؤمنين بالولاء. النفق الكمومي: التوبة تخترق حاجز المعصية.

        ### التطابق مع البيولوجيا
        جهاز المناعة: تمييز الذات (W) من اللاذات (B). السرطان: استدراج بيولوجي (W شاذ، B=0).

        ### الدليل من الحروف المقطعة والأنظمة العددية
        أربعة عشر حرفاً نورانياً (الثوابت) وأربعة عشر حرفاً (المتغيرات). النظام السداسي (أيام الخلق وسور الم).
        النظام الخماسي (الحواس وسور الر). النظام السباعي (السماوات وسور حم).
        """)

    with st.expander("الباب الرابع: وحدة الخلق والأمر – الدليل الكوني", expanded=False):
        st.markdown("""
        ### ﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ﴾ – وحدة المصدر
        الخالق والشارع واحد. القانون الذي يحكم الذرة (الخلق) هو نفسه الذي شرعه الله للإنسان (الأمر).
        لا يوجد تناقض بين "العلم" و"الدين". لا يوجد انفصام بين "الفيزياء" و"الشريعة".

        ### الميزان في الآفاق – فيزياء الميزان
        الجاذبية (W) والتنافر (B) في الذرة. استقرار الذرة S = W × B.
        اختبرنا هذا في مختبرنا الرقمي: نسبة W إلى B تقارب الواحد الصحيح في ذرة الهيدروجين.

        ### الميزان في الكيمياء
        الاتحاد (W) والتفكك (B) في التفاعلات. طاقة التنشيط = التوبة.
        العامل المساعد = الأنبياء والقرآن. الاتزان الكيميائي = الثبات الديناميكي.

        ### الميزان في الأنفس – بيولوجيا الميزان
        جهاز المناعة: ذات (W) ولاذات (B). أمراض المناعة الذاتية: خلل في W.
        السرطان = استدراج بيولوجي: نمو متسارع (W شاذ) ومناعة منهارة (B=0).

        ### الميزان في التاريخ – سنة الله في الأمم
        الدولة الأموية: انهارت بفساد المناعة B. الاتحاد السوفيتي: انهار بانهيار الإيمان W.
        الدولة العثمانية: استدراج طويل (تمكين E مرتفع وثبات S منهار).
        """)

    with st.expander("الباب الخامس: المختبر – تشغيل المحاكاة ورؤية الاستدراج", expanded=False):
        st.markdown("""
        ### لماذا النمذجة الحاسوبية؟
        لترجمة الوحي إلى لغة العصر. لإثبات أن السنن الإلهية قوانين قابلة للبرمجة والمحاكاة.

        ### الحالات الأربع للكائن البشري (ألوان النجوم)
        - **الذهبي**: المؤمن (W عالية، B عالية). الثبات الكامل.
        - **البرتقالي**: المشرك (W عالية، B منهارة). ولاء بلا مناعة.
        - **الأحمر**: الكافر (W منهارة، B عالية). براءة بلا ولاء.
        - **الوردي**: المنافق (W منهارة، B منهارة). تيه وضياع.

        ### سرعة الضوء الأخلاقية – إثبات الاستدراج
        في لوحة الإثبات، المنحنى الذهبي S يسبق دائماً المنحنى السماوي E.
        هذه هي فجوة الاستدراج: التمكين يتأخر عن الثبات.
        تنهار S أولاً، ثم يلحقها E بفارق زمني. هذا يفسر لماذا يزدهر الظالمون قبل سقوطهم.
        """)

    with st.expander("الباب السادس: نحو الأمة الذهبية – من المختبر إلى الواقع", expanded=False):
        st.markdown("""
        ### إعادة تعريف الذات
        أين أنت على خريطة الميزان؟ ما هو لون نجمتك؟
        التشخيص الذاتي هو أول خطوة في رحلة التحول.

        ### ورشة البناء – كيف نصنع إنساناً ذهبياً؟
        **توليد W (محطات الشحن):** الصلاة، القرآن، الذكر، الدعاء.
        **بناء B (تقوية المناعة):** مخالفة الهوى، الأمر بالمعروف، النهي عن المنكر، دراسة سيرة الأنبياء.
        **التوازن بين W و B:** فقه الأولويات. لا تقدم B على W قبل أوانها.

        ### هندسة المجتمع الذهبي
        **خلايا النحل:** بناء الجماعة التي تشحن W و B.
        **صناعة القدوة:** إنتاج ذهبيين في كل مجال (طب، هندسة، تجارة، فن).
        **بناء المؤسسات:** تحويل المبادئ إلى أنظمة تحفظ المسيرة عبر الأجيال.
        """)

    with st.expander("الباب السابع: الفطرة – نظام التشغيل الأصلي", expanded=False):
        st.markdown("""
        ### الميثاق الغليظ – يوم قالوا بلى
        ﴿أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾ [الأعراف: 172].
        هذه "البلى" الأزلية هي بذرة W المزروعة في أعماق كل نفس بشرية.
        كل طفل يولد على الفطرة. إنه "المسلم" بالفطرة.

        ### بنية الفطرة (نظام التشغيل)
        تتكون من أربع دوائر متداخلة:
        1. التطلع إلى المطلق (منبع W).
        2. حب الخلود وكراهية الفناء (منبع B).
        3. حب الخير وكراهية الشر (الميزان الداخلي S).
        4. الحاجة إلى المعنى (سؤال "لماذا").

        ### محاولات إسكات الفطرة (ثلاث طرق فاشلة)
        - عبادة العقل المجرد: تنتهي إلى قلق وجودي.
        - عبادة المادة والشهوة: تنتهي إلى فراغ أعمق.
        - عبادة الذات: تنتهي إلى عزلة وجودية.
        الوحي هو الماء الذي يروي ظمأ الفطرة.
        """)

    with st.expander("الباب الثامن: التشخيص – واقع الأمة في ميزان S = W × B", expanded=False):
        st.markdown("""
        ### حال الميزان اليوم
        W (الولاء) ضعيفة ومشتتة. B (البراءة) منهارة تقريباً.
        S (الثبات) في الحضيض. E (التمكين) إما منهار أو متضخم كالورم الخبيث.

        ### الانفصام الخماسي
        - الانفصام العقدي: تحولت "لا إله إلا الله" إلى شعار.
        - الانفصام التشريعي: استبدال شرع الله بقوانين وضعية.
        - الانفصام الأخلاقي: ازدواجية بين المسجد والسوق.
        - الانفصام الاجتماعي: تفكك الأسرة وضعف صلة الرحم.
        - الانفصام السياسي: تمزق الأمة إلى دويلات متناحرة.

        ### الأسباب الجذرية
        - الخلل في فهم "لا إله إلا الله".
        - الانهيار التربوي.
        - الغزو الفكري والثقافي.
        - التبعية الاقتصادية.
        - غياب القدوة الذهبية الجامعة.
        """)

    with st.expander("الباب التاسع: سبل العودة إلى القانون – كيف نعيد ضبط الميزان؟", expanded=False):
        st.markdown("""
        ### الحركة الأولى: الإصلاح الفردي – بناء الإنسان الذهبي
        - العلاج المعرفي: تصحيح فهم التوحيد.
        - العلاج القلبي: تطهير القلب بالذكر والقرآن والدعاء.
        - العلاج السلوكي: تحويل العبادة إلى سلوك.

        ### الحركة الثانية: الإصلاح الأسري – بناء الحصن الاجتماعي
        - التأسيس السليم: اختيار الزوج الصالح.
        - التربية الواعية: غرس حب الله في الأبناء.
        - العلاج الحكيم: حل المشكلات بالحوار.

        ### الحركة الثالثة: الإصلاح المجتمعي – بناء الجماعة المؤمنة
        - إحياء روح الجماعة: الهجرة من الفردانية.
        - بناء المؤسسات الفاعلة.
        - تفعيل الأمر بالمعروف والنهي عن المنكر.

        ### الحركة الرابعة: انتظار سنة التمكين – الصبر الاستراتيجي
        الصبر على فجوة الاستدراج. الثقة بوعد الله. البقاء ذهبياً حتى يأتي النصر.
        """)

    with st.expander("الباب العاشر: اكتمال الدائرة – من الأزل إلى الخلود", expanded=False):
        st.markdown("""
        ### المراحل الخمس للوجود
        **الطور الأول: الأزل – الميثاق الغليظ.**
        غُرس أصل W في الفطرة: ﴿أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾.

        **الطور الثاني: الخلق – كلمة "كُنْ".**
        الكاف (20) + النون (50) = العين (70). الأمر الإلهي + النور = الوجود المدرَك.

        **الطور الثالث: عالم الشهادة – الاستجابة للقانون.**
        الجماد قسراً، النبات والحيوان غريزةً، الملائكة روحاً، الإنسان اختياراً.

        **الطور الرابع: السنن الإلهية – القوانين الحاكمة.**
        سنة التغيير، سنة التمكين، سنة الاستدراج، سنة التدافع.

        **الطور الخامس: الخلود – الميزان يوم القيامة.**
        ﴿وَنَضَعُ الْمَوَازِينَ الْقِسْطَ لِيَوْمِ الْقِيَامَةِ﴾.
        فمن أقام الميزان في الدنيا، استقر ميزانه في الآخرة.

        ---
        اكتملت الدائرة. من ﴿اقْرَأْ﴾ إلى "الميزان"، من الأزل إلى الخلود.
        لم يعد الوجود فوضى، بل نظام. لم يعد التاريخ عبثاً، بل سنة. لم يعد الموت نهاية، بل عدالة.
        """)# =============================================
# 📜 تبويب رسالة الترحيب (مكتملة ومُنقَّحة)
# =============================================
with tab4:
    st.header("📜 رسالة الترحيب")
    st.markdown("""
    <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">

    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
    > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"

    ---

    <b>الدين القيم</b> هو قانون السببية الكوني، الحق لأن واضعه الحق،
    والقيم لأنه من القيوم نفسه. هو القانون الأعظم الذي أزال الله به العدم،
    وأوجد به الخلق، وأجرى به السنن، وسيكون به الجزاء.
    إنه <b>"الميزان"</b> الذي قامت به السماوات والأرض،
    والذي يدور حوله كل شيء، من الأزل إلى الخلود.

    ---

    التوازن والانهيار، السقوط والصمود، الثبات والاستقرار:
    في الذرة والمجرة، في المادة والروح، في الفرد والحضارة،
    في الفيزياء والكيمياء والبيولوجيا والأخلاق –
    كله نتيجة حتمية لمدى <b>الإسلام الحنيف</b>،
    وهو الاستجابة الديناميكية المثلى للقانون الإلهي
    من خلال تحقيق التوازن في الولاء والبراءة،
    كلٌّ بما يناسب فطرته.

    ---

    <div style="font-size: 1.2em; color: #FFD700; line-height: 2.5; text-align: center;">
    <b>
    ﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ وَلَهُ أَسْلَمَ مَن فِي السَّمَاوَاتِ وَالْأَرْضِ طَوْعًا وَكَرْهًا وَإِلَيْهِ يُرْجَعُونَ﴾
    <br>— سورة آل عمران، الآية 83
    </b>
    </div>

    ---

    > "أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.<br>
    > استقراركم ليس صدفة. انهياركم ليس حظاً سيئاً.<br>
    > إنها معادلة. إنها <b style="color: #FFD700;">S = W × B</b>."

    ---

    هذا المشهد المتكامل الذي يجمع الذرة والمجرة،
    الفرد والحضارة، المادة والروح،
    إنما يسير بقانون واحد هو <b style="color: #FFD700;">S = W × B</b>.

    ---

    **الدين القيم** = القانون الإلهي الذي يسري على كل شيء من الأزل إلى الخلود.

    **الإسلام الحنيف** = الاستجابة الديناميكية المثلى للقانون الإلهي من خلال تحقيق التوازن في الولاء والبراءة.

    ---

    <div style="font-size: 1.2em; color: #FFD700; line-height: 2.5; text-align: center;">
    <b>
    ﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ
    لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ وَلَٰكِنَّ أَكْثَرَ النَّاسِ لَا يَعْلَمُونَ﴾
    <br>— سورة الروم، الآية 30
    </b>
    </div>

    ---

    <b style="color: #FFD700;">© 2026 علي عادل العاطفي | Ali Adel Alatifi</b>

    </div>
    """, unsafe_allow_html=True)
    # =============================================
# 📋 تبويب الدليل المرجعي (مكتمل ومنقح)
# =============================================
with tab5:
    st.header("📋 الدليل المرجعي")
    st.markdown("""
    ---

    ### ⚖️ نظرية الميزان – المختبر القرآني

    **المشروع:** نظرية الميزان – المختبر القرآني
    **المعادلة المركزية:** S = W × B
    **المؤلف:** علي عادل العاطفي (Ali Adel Alatifi)
    **البريد الإلكتروني:** abwahmdalsbyhy925@gmail.com
    **الترخيص:** MIT License – يُسمح بالاستخدام والتعديل والنشر مع ذكر المصدر الأصلي والمؤلف.
    
    © 2026 علي عادل العاطفي. جميع الحقوق محفوظة.

    ---

    ### 📚 مكونات المشروع

    **1. المختبر الحي:** محاكاة تفاعلية لنظرية الميزان باستخدام 28 متغيراً تمثل الحروف العربية وقيمها في حساب الجمل. يراقب المستخدم تأثير مولدات الولاء والبراءة ومثبطاتها على استقرار المجتمع، ويرى لوحة الإثبات التي تفضح الاستدراج.

    **2. البوصلة الكونية:** اختبار تشخيصي ذاتي مكون من 28 سؤالاً (14 للولاء و14 للبراءة)، يحدد موقع الفرد على خريطة الأرباع الوجودية الأربعة (مؤمن، كافر، منافق، مشرك) ويحسب ثباته الوجودي S = L × D.

    **3. كتاب الميزان:** الأبواب العشرة الكاملة التي تشرح النظرية من جذورها الفلسفية إلى تطبيقاتها العملية.

    **4. المعجم الهندسي للقرآن:** قاموس يحول 45 مشغلاً قرآنياً (الفاء، الواو...) إلى رموز رياضية قابلة للبرمجة.

    ---

    ### 🛡️ حقوق الملكية الفكرية

    هذا المشروع هو نتاج بحث وتدبر في كتاب الله المسطور (القرآن) وكتابه المنظور (الكون). جميع الحقوق محفوظة للمؤلف. وهو محمي بموجب ترخيص MIT License الذي يسمح بالاستخدام والتعديل والنشر مع ذكر المصدر الأصلي.
    """)
