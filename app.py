# =============================================
# ⚖️ AL-DEEN AL-QAYYIM – THE COSMIC BALANCE LAW
# S = W × B | W = الولاء (Allegiance) | B = البراءة (Disavowal)
# © 2026 Ali Adel Alatifi | All rights reserved.
# =============================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="الدين القيم – المختبر القرآني", page_icon="⚖️", layout="wide", initial_sidebar_state="auto")

# =============================================
# 🎨 CSS
# =============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); }
    .big-title { font-size: 2.5em; font-weight: 900; color: #FFD700; text-align: center; margin: 10px 0 0 0; }
    .sub-title { font-size: 1.1em; color: #CCCCCC; text-align: center; margin: 0 0 20px 0; }
    .stButton > button { border: 1px solid #FFD700; color: #FFD700; background: #1a1a3e; border-radius: 8px; height: 2.5em; }
    .metric-box { background: rgba(10,10,46,0.8); border-radius: 10px; padding: 8px 5px; text-align: center; border: 1px solid rgba(218,165,32,0.3); }
    .metric-val { font-size: 1.6em; font-weight: bold; margin: 0; }
    .metric-lbl { font-size: 0.7em; color: #aaa; margin: 0; }
    [data-testid="stExpander"] details { background: rgba(10,10,40,0.5); border: 1px solid rgba(218,165,32,0.3); border-radius: 8px; }
    [data-testid="stExpander"] summary { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ العنوان الرئيسي
# =============================================
st.markdown('<p class="big-title">⚖️ الدِّينُ الْقَيِّم ⚖️</p>', unsafe_allow_html=True)
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
# 🎨 نظام الألوان الموحد (للمختبر والبوصلة)
# =============================================
COLORS = {
    "مؤمن": "#FFD700",    # ذهبي
    "كافر": "#FF3333",    # أحمر
    "منافق": "#FFB6C1",   # وردي
    "مشرك": "#FFFFFF",    # أبيض (ولاء بلا براءة = راهب/صوفي)
}

def get_mizan_color(w, b):
    """
    تُرجع لون النجمة بناءً على معادلة الميزان S = W × B.
    التصنيف:
    - ذهبي: مؤمن (W عالية، B عالية)
    - أحمر: كافر (W منخفضة، B عالية)
    - وردي: منافق (W منخفضة، B منخفضة)
    - أبيض: مشرك/راهب (W عالية، B منخفضة)
    """
    if w >= 0.6 and b >= 0.6:
        return COLORS["مؤمن"]     # ذهبي
    elif w >= 0.6 and b < 0.4:
        return COLORS["مشرك"]     # أبيض (ولاء بلا براءة)
    elif w < 0.4 and b >= 0.6:
        return COLORS["كافر"]     # أحمر (براءة بلا ولاء)
    elif w < 0.4 and b < 0.4:
        return COLORS["منافق"]    # وردي (لا ولاء ولا براءة)
    else:
        # حالات وسطية
        if w > b: return '#FFF8DC'
        elif b > w: return '#FFA07A'
        else: return '#FFBF00'

def get_quadrant_name(L_map, D_map):
    """تُرجع اسم الربع بناءً على إحداثيات (L, D)."""
    if L_map > 0 and D_map > 0: return "مؤمن (الربع الأول)"
    elif L_map < 0 and D_map > 0: return "كافر (الربع الثاني)"
    elif L_map < 0 and D_map < 0: return "منافق (الربع الثالث)"
    elif L_map > 0 and D_map < 0: return "مشرك/راهب (الربع الرابع)"
    else: return "منطقة محايدة"

def get_quadrant_color(L_map, D_map):
    """تُرجع لون الربع بناءً على إحداثيات (L, D)."""
    if L_map > 0 and D_map > 0: return COLORS["مؤمن"]
    elif L_map < 0 and D_map > 0: return COLORS["كافر"]
    elif L_map < 0 and D_map < 0: return COLORS["منافق"]
    elif L_map > 0 and D_map < 0: return COLORS["مشرك"]
    else: return "#888888"
        # =============================================
# 🌌 تبويب المختبر الحي
# =============================================
with tab1:
    # --- دالة حساب S باستخدام الحروف الـ 28 ---
    def calc_S(W, B, E, n_A, n_L, n_M, n_S, n_R, n_K, n_H, n_Y, n_Ain, n_Ta, n_Sin, n_Ha, n_Q, n_N,
               n_Za, n_Da, n_Dh, n_Kh, n_Sh, n_Z, n_Gh, n_J,
               n_Fa, n_Waw, n_Ba, n_La, n_Ta_m, n_Th):
        Sb = W * B
        # أركان الإسلام (من الحروف النورانية)
        pillars_boost = (n_A * 1 + n_L * 30 + n_M * 40 + n_S * 90 + n_K * 20) / 5
        Sb *= (0.5 + 0.5 * pillars_boost)
        # الحماية (من الحروف النورانية)
        protection = (n_R * 200 + n_H * 5 + n_Y * 10 + n_Ain * 70 + n_Ta * 9 + n_Sin * 60 + n_Ha * 8) / 7
        Sb *= (0.8 + 0.4 * protection)
        # الميزان والنور
        Sb *= (0.9 + 0.2 * n_Q * 100)
        Sb *= (0.85 + 0.3 * n_N * 50)
        # التآكل الظلامي
        dark_factor = 1 - 0.05 * (n_Za * 900) - 0.03 * (n_Da * 800) - 0.02 * (n_Dh * 700) - 0.04 * (n_Kh * 600) - 0.03 * (n_Sh * 300) - 0.01 * (n_Z * 7) - 0.05 * (n_Gh * 1000) - 0.02 * (n_J * 3)
        Sb *= max(0.1, dark_factor)
        # المشغلات
        operator_effect = (n_Fa * 80 + n_Waw * 6 + n_Ba * 2 + n_La * 30 + n_Ta_m * 400 + n_Th * 500) / 6
        Sb *= (0.5 + 0.5 * operator_effect)
        if E > Sb: Sb -= (n_Gh * 1000 / 1000) * (E - Sb) * 0.3
        return np.clip(Sb, 0.001, 1.0)

    # --- الشريط الجانبي: لوحة التحكم بالحروف الـ 28 ---
    with st.sidebar:
        st.header("🎛️ لوحة التحكم – الحروف الـ 28")

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

        # 1. الحروف النورانية (14 حرفاً) – مولدات W
        with st.expander("🔆 الحروف النورانية (14) – مولدات الولاء", expanded=False):
            st.caption("زيادة هذه القيم ترفع من قوة الولاء (W) في النظام.")
            n_A = st.slider("أ (1) – الوحدانية", 0.0, 1.0, 0.7, 0.01, key="n_A")
            n_L = st.slider("ل (30) – المُلك والعدل", 0.0, 1.0, 0.6, 0.01, key="n_L")
            n_M = st.slider("م (40) – الجمع", 0.0, 1.0, 0.6, 0.01, key="n_M")
            n_S = st.slider("ص (90) – الصمد", 0.0, 1.0, 0.6, 0.01, key="n_S")
            n_R = st.slider("ر (200) – اليقظة", 0.0, 1.0, 0.6, 0.01, key="n_R")
            n_K = st.slider("ك (20) – الأمر", 0.0, 1.0, 0.6, 0.01, key="n_K")
            n_H = st.slider("هـ (5) – الهوية", 0.0, 1.0, 0.6, 0.01, key="n_H")
            n_Y = st.slider("ي (10) – الاستجابة", 0.0, 1.0, 0.6, 0.01, key="n_Y")
            n_Ain = st.slider("ع (70) – الإدراك", 0.0, 1.0, 0.6, 0.01, key="n_Ain")
            n_Ta = st.slider("ط (9) – الطهارة", 0.0, 1.0, 0.6, 0.01, key="n_Ta")
            n_Sin = st.slider("س (60) – السمع", 0.0, 1.0, 0.6, 0.01, key="n_Sin")
            n_Ha = st.slider("ح (8) – الحياة", 0.0, 1.0, 0.6, 0.01, key="n_Ha")
            n_Q = st.slider("ق (100) – الميزان", 0.0, 1.0, 0.8, 0.01, key="n_Q")
            n_N = st.slider("ن (50) – النور", 0.0, 1.0, 0.7, 0.01, key="n_N")

        # 2. الحروف الظلامية (8 حروف) – مثبطات B
        with st.expander("🌑 الحروف الظلامية (8) – مثبطات البراءة", expanded=False):
            st.caption("زيادة هذه القيم تزيد من الفوضى وتقلل البراءة (B) في النظام.")
            n_Za = st.slider("ظ (900) – الظلم", 0.0, 1.0, 0.2, 0.01, key="n_Za")
            n_Da = st.slider("ض (800) – الضلال", 0.0, 1.0, 0.2, 0.01, key="n_Da")
            n_Dh = st.slider("ذ (700) – الذل", 0.0, 1.0, 0.2, 0.01, key="n_Dh")
            n_Kh = st.slider("خ (600) – الخيانة", 0.0, 1.0, 0.2, 0.01, key="n_Kh")
            n_Sh = st.slider("ش (300) – الشهوة", 0.0, 1.0, 0.2, 0.01, key="n_Sh")
            n_Z = st.slider("ز (7) – الزور", 0.0, 1.0, 0.2, 0.01, key="n_Z")
            n_Gh = st.slider("غ (1000) – الغش", 0.0, 1.0, 0.2, 0.01, key="n_Gh")
            n_J = st.slider("ج (3) – الجهل", 0.0, 1.0, 0.2, 0.01, key="n_J")

        # 3. الحروف المحايدة (6 حروف) – المشغلات
        with st.expander("⚙️ الحروف المحايدة (6) – المشغلات", expanded=False):
            st.caption("تؤثر على كيفية تفاعل القوى النورانية والظلامية.")
            n_Fa = st.slider("ف (80) – السببية", 0.0, 1.0, 0.5, 0.01, key="n_Fa")
            n_Waw = st.slider("و (6) – العطف", 0.0, 1.0, 0.5, 0.01, key="n_Waw")
            n_Ba = st.slider("ب (2) – الاستعانة", 0.0, 1.0, 0.5, 0.01, key="n_Ba")
            n_La = st.slider("ل (30) – التعليل", 0.0, 1.0, 0.5, 0.01, key="n_La")
            n_Ta_m = st.slider("ت (400) – التأني", 0.0, 1.0, 0.5, 0.01, key="n_Ta_m")
            n_Th = st.slider("ث (500) – الثبات", 0.0, 1.0, 0.5, 0.01, key="n_Th")

        with st.expander("⚙️ إعدادات المحاكاة", expanded=True):
            cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001, key="spd")
            delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1, key="dly")
            N_STARS = st.slider("عدد النجوم", 50, 300, 150, 10, key="nst")

    # --- تهيئة المحاكاة ---
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
        st.session_state.hasanat = 10.0; st.session_state.sayyiat = 5.0
        st.session_state.init = True

    # --- مؤشرات ---
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
            mizan_akhira = st.session_state.hasanat - st.session_state.sayyiat
            color = "#FFD700" if mizan_akhira >= 0 else "#FF3333"
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:{color};">{mizan_akhira:.3f}</p><p class="metric-lbl">📜 الميزان الأخروي</p></div>', unsafe_allow_html=True)

    plot_placeholder = st.empty()

    # --- المحاكاة الحية ---
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

                n = len(sw)
                for i in range(n):
                    # تأثير النورانيات على W
                    w_boost = (n_A * 1 + n_L * 30 + n_M * 40 + n_S * 90 + n_R * 200 + n_K * 20 + n_H * 5 + n_Y * 10 + n_Ain * 70 + n_Ta * 9 + n_Sin * 60 + n_Ha * 8 + n_Q * 100 + n_N * 50) / 14.0 * 0.01
                    sw[i] += w_boost
                    
                    # تأثير النورانيات على B
                    b_boost = (n_Q * 100 + n_N * 50) / 2.0 * 0.01
                    sb[i] += b_boost
                    
                    # تأثير الظلاميات (تثبيط)
                    dark_effect = (n_Za * 900 + n_Da * 800 + n_Dh * 700 + n_Kh * 600 + n_Sh * 300 + n_Z * 7 + n_Gh * 1000 + n_J * 3) / 8.0 * 0.01
                    sw[i] -= dark_effect
                    sb[i] -= dark_effect
                    
                    # تأثير المشغلات
                    op_effect = (n_Fa * 80 + n_Waw * 6 + n_Ba * 2 + n_La * 30 + n_Ta_m * 400 + n_Th * 500) / 6.0 * 0.005
                    sw[i] += op_effect
                    sb[i] += op_effect
                    
                    # الجاذبية نحو الهدف
                    sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                    sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                    
                    # تأثير الشورى (من حرف الشين)
                    dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                    close = (dist < 2.0) & (np.arange(n) != i)
                    if np.any(close):
                        sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03 * (0.5 + 0.5 * n_Sh * 300)
                        sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03 * (0.5 + 0.5 * n_Sh * 300)
                    
                    sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

                shock_p = 0.005 * (1 - n_Q * 100 * 0.8)
                if random.random() < shock_p:
                    aff = np.random.choice(n, size=int(n * 0.3), replace=False)
                    sw[aff] *= np.random.uniform(0.5, 0.8); sb[aff] *= np.random.uniform(0.5, 0.8)

                avgW = np.mean(sw); avgB = np.mean(sb)
                W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
                W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
                S = calc_S(W, B, E, n_A, n_L, n_M, n_S, n_R, n_K, n_H, n_Y, n_Ain, n_Ta, n_Sin, n_Ha, n_Q, n_N,
                           n_Za, n_Da, n_Dh, n_Kh, n_Sh, n_Z, n_Gh, n_J,
                           n_Fa, n_Waw, n_Ba, n_La, n_Ta_m, n_Th)
                eb.append(S)
                if len(eb) > 30: eb.pop(0)
                E_target = eb[-delay_frames] if len(eb) >= delay_frames else S
                E += 0.03 * (E_target - E)
                W = W - 0.01 * E + 0.02 / (S + 0.1)
                B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
                W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
                S = calc_S(W, B, E, n_A, n_L, n_M, n_S, n_R, n_K, n_H, n_Y, n_Ain, n_Ta, n_Sin, n_Ha, n_Q, n_N,
                           n_Za, n_Da, n_Dh, n_Kh, n_Sh, n_Z, n_Gh, n_J,
                           n_Fa, n_Waw, n_Ba, n_La, n_Ta_m, n_Th)
                pS.append(S); pE.append(E); px.append(len(px))
                if len(px) > 400: pS.popleft(); pE.popleft(); px.popleft()

                st.session_state.hasanat += np.mean(sw) * 0.1
                st.session_state.sayyiat += (1 - np.mean(sb)) * 0.1

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
                colors = [get_mizan_color(sw[i], sb[i]) for i in range(n)]
                ax.scatter(sx, sy, s=40, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)
                ax.add_patch(Circle((wx,wy), 0.2+0.5*W, color='#FFF', alpha=1, zorder=13))
                ax.add_patch(Circle((bx,by), 0.2+0.5*B, color='#F33', alpha=0.8, zorder=13))
                ax.text(wx, wy-1.2, 'W', color='#FFF', fontsize=12, ha='center')
                ax.text(bx, by-1.2, 'B', color='#F33', fontsize=12, ha='center')
                pSl, pEl, pxl = list(pS), list(pE), list(px)
                if pSl:
                    pax = ax.inset_axes([0.3, 0.02, 0.65, 0.18])
                    pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
                    pax.set_title('📈 S (الذهب) يقود E (السماوي) — الاستدراج', color='white', fontsize=10, fontweight='bold')
                    pax.tick_params(colors='white', labelsize=7); pax.grid(True, alpha=0.3)
                    pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S')
                    pax.plot(pxl, pEl, color='#00FFFF', lw=2, label='E')
                    pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=8)
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
            colors = [get_mizan_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
            ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9)
            ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
            plot_placeholder.pyplot(fig)
            plt.close(fig)

    if 'latest_image' in st.session_state:
        st.download_button("📥 تحميل صورة المشهد", st.session_state.latest_image, "mizan_scene.png", "image/png")
        # =============================================
# 🧭 تبويب البوصلة الكونية (28 سؤالاً – نظام الحروف الـ 28)
# =============================================
with tab2:
    st.header("🧭 البوصلة الكونية")
    st.subheader("اختبار الإحداثيات الوجودية – 28 سؤالاً على نظام الحروف العربية")
    st.caption("14 سؤالاً للولاء + 14 سؤالاً للبراءة = 28 سؤالاً | أقصى درجة = 280 | S = L × D")

    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    questions = {
        "L": [
            # أركان الإسلام (5)
            {"id": "L1", "q": "الشهادتان (أ = 1): هل تعيش لله وحده، مخلصاً له الدين؟", "a": [("نعم، هو محور حياتي (10)", 10), ("غالباً، لكني أنسى أحياناً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا (0)", 0)]},
            {"id": "L2", "q": "الصلاة (ل = 30): هل تقيم الصلاة بخشوع وفي وقتها؟", "a": [("نعم، كل الفروض في وقتها (10)", 10), ("معظمها، مع بعض التقصير (7)", 7), ("بعضها (4)", 4), ("نادراً (1)", 1), ("لا أصلي (0)", 0)]},
            {"id": "L3", "q": "الزكاة (م = 40): هل تؤدي الزكاة وتتصدق ابتغاء وجه الله؟", "a": [("نعم، وأزيد (10)", 10), ("أؤدي الفرض فقط (7)", 7), ("أخرج شيئاً دون حساب (4)", 4), ("نادراً (1)", 1), ("لا أخرج (0)", 0)]},
            {"id": "L4", "q": "الصوم (ص = 90): هل تصوم الفرض وتصوم تطوعاً؟", "a": [("نعم، وأزيد النوافل (10)", 10), ("أصوم الفرض كاملاً (7)", 7), ("أصوم معظمه (4)", 4), ("أصوم القليل (1)", 1), ("لا أصوم (0)", 0)]},
            {"id": "L5", "q": "الحج (ك = 20): هل أديت الفريضة أو تسعى جاداً لأدائها؟", "a": [("أديته أو لدي خطة واضحة (10)", 10), ("لدي نية جادة (7)", 7), ("أتمنى فقط (4)", 4), ("لا أفكر فيه (1)", 1), ("لا أهتم (0)", 0)]},
            # الأخلاق الحميدة (9)
            {"id": "L6", "q": "قول الحق (ر = 200): هل تقول الحق ولو على نفسك؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أقول الحق (0)", 0)]},
            {"id": "L7", "q": "الصدق (ن = 50): هل أنت صادق في أقوالك وأفعالك؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أصدق (0)", 0)]},
            {"id": "L8", "q": "الأمانة (هـ = 5): هل تؤدي الأمانات إلى أهلها؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أؤديها (0)", 0)]},
            {"id": "L9", "q": "شهادة الحق (ي = 10): هل تشهد بالحق ولا تكتمه؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أشهد (0)", 0)]},
            {"id": "L10", "q": "المسؤولية (ع = 70): هل تتحمل مسؤولية أهلك ومجتمعك؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أتحمل (0)", 0)]},
            {"id": "L11", "q": "الوفاء بالعهد (ط = 9): هل تفي بعهودك ووعودك؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أفي (0)", 0)]},
            {"id": "L12", "q": "الحب للمؤمنين (س = 60): هل تحب لإخوانك ما تحب لنفسك؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أحب (0)", 0)]},
            {"id": "L13", "q": "القناعة (ح = 8): هل أنت قانع بما قسم الله لك؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أقنع (0)", 0)]},
            {"id": "L14", "q": "الولاء للمؤمنين (ق = 100): هل تنصر المؤمنين وتوالي من يوالي الله؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أوالي (0)", 0)]},
        ],
        "D": [
            # أركان البراءة (6)
            {"id": "D1", "q": "الأمر بالمعروف (ف = 80): هل تأمر بالمعروف؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا آمر (0)", 0)]},
            {"id": "D2", "q": "النهي عن المنكر (ش = 300): هل تنهى عن المنكر؟", "a": [("دائماً (10)", 10), ("غالباً (7)", 7), ("أحياناً (4)", 4), ("نادراً (1)", 1), ("لا أنهى (0)", 0)]},
            {"id": "D3", "q": "الجهاد (ظ = 900): هل تجاهد بكل أشكاله لإعلاء كلمة الله؟", "a": [("نعم، بكل أشكاله (10)", 10), ("أجاهد نفسي فقط (7)", 7), ("أدعمه مالياً (4)", 4), ("لا أجاهد (1)", 1), ("أرفضه (0)", 0)]},
            {"id": "D4", "q": "البراءة من الشرك (ض = 800): هل تتبرأ من الشرك وأهله؟", "a": [("أتبرأ منهم تماماً (10)", 10), ("أرفضهم لكني لا أجاهر (7)", 7), ("لا أهتم (4)", 4), ("أتعامل معهم عادي (1)", 1), ("أحبهم (0)", 0)]},
            {"id": "D5", "q": "البراءة من الكفر (ذ = 700): هل ترفض الكفر والإلحاد؟", "a": [("أرفضهما تماماً (10)", 10), ("أرفضهما لكني لا أجاهر (7)", 7), ("لا أهتم (4)", 4), ("أرى فيهما تقدماً (1)", 1), ("أفضلهما (0)", 0)]},
            {"id": "D6", "q": "البراءة من النفاق (خ = 600): هل ترفض النفاق والتلون؟", "a": [("أرفضه وأحذر منه (10)", 10), ("أرفضه لكني أتلون أحياناً (7)", 7), ("لا أهتم (4)", 4), ("أراه ضرورة أحياناً (1)", 1), ("أراه ذكاء (0)", 0)]},
            # الأخلاق الذميمة (8)
            {"id": "D7", "q": "الكذب (غ = 1000): هل تترك الكذب وتتبرأ منه؟", "a": [("لا أكذب أبداً (10)", 10), ("نادراً ما أكذب (7)", 7), ("أكذب أحياناً (4)", 4), ("أكذب كثيراً (1)", 1), ("الكذب أسلوبي (0)", 0)]},
            {"id": "D8", "q": "الغش (ز = 7): هل تترك الغش في كل معاملاتك؟", "a": [("لا أغش أبداً (10)", 10), ("نادراً ما أغش (7)", 7), ("أغش أحياناً (4)", 4), ("أغش كثيراً (1)", 1), ("الغش أسلوبي (0)", 0)]},
            {"id": "D9", "q": "الخيانة (ج = 3): هل تترك الخيانة وتتبرأ منها؟", "a": [("لا أخون أبداً (10)", 10), ("نادراً ما أخون (7)", 7), ("أخون أحياناً (4)", 4), ("أخون كثيراً (1)", 1), ("الخيانة أسلوبي (0)", 0)]},
            {"id": "D10", "q": "الظلم (ت = 400): هل تترك الظلم وتتبرأ منه؟", "a": [("لا أظلم أبداً (10)", 10), ("نادراً ما أظلم (7)", 7), ("أظلم أحياناً (4)", 4), ("أظلم كثيراً (1)", 1), ("الظلم أسلوبي (0)", 0)]},
            {"id": "D11", "q": "السرقة (ث = 500): هل تترك السرقة وتتبرأ منها؟", "a": [("لا أسرق أبداً (10)", 10), ("نادراً ما أسرق (7)", 7), ("أسرق أحياناً (4)", 4), ("أسرق كثيراً (1)", 1), ("السرقة أسلوبي (0)", 0)]},
            {"id": "D12", "q": "الزنا (ب = 2): هل تترك الفواحش وتتبرأ منها؟", "a": [("لا أقربها أبداً (10)", 10), ("نادراً ما أقع فيها (7)", 7), ("أقع فيها أحياناً (4)", 4), ("أقع فيها كثيراً (1)", 1), ("لا أتركها (0)", 0)]},
            {"id": "D13", "q": "الرياء (و = 6): هل تترك الرياء وتتبرأ منه؟", "a": [("لا أرائي أبداً (10)", 10), ("نادراً ما أرائي (7)", 7), ("أرائي أحياناً (4)", 4), ("أرائي كثيراً (1)", 1), ("الرياء أسلوبي (0)", 0)]},
            {"id": "D14", "q": "الحسد (د = 4): هل تترك الحسد وتتبرأ منه؟", "a": [("لا أحسد أبداً (10)", 10), ("نادراً ما أحسد (7)", 7), ("أحسد أحياناً (4)", 4), ("أحسد كثيراً (1)", 1), ("الحسد أسلوبي (0)", 0)]},
        ]
    }

    st.markdown("### 📝 أجب بصراحة كاملة عن الأسئلة الـ 28")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### 🤍 أسئلة الولاء (L) – {len(questions['L'])} سؤالاً")
        for q in questions["L"]:
            ans = st.radio(f"**{q['q']}**", [a[0] for a in q['a']], key=q['id'], index=None)
            if ans:
                st.session_state.compass_answers[q['id']] = [a[1] for a in q['a'] if a[0] == ans][0]

    with col2:
        st.markdown(f"#### ❤️ أسئلة البراءة (D) – {len(questions['D'])} سؤالاً")
        for q in questions["D"]:
            ans = st.radio(f"**{q['q']}**", [a[0] for a in q['a']], key=q['id'], index=None)
            if ans:
                st.session_state.compass_answers[q['id']] = [a[1] for a in q['a'] if a[0] == ans][0]

    total_questions = 28

    if len(st.session_state.compass_answers) == total_questions:
        L_score = sum([st.session_state.compass_answers[f"L{i}"] for i in range(1, 15)])
        D_score = sum([st.session_state.compass_answers[f"D{i}"] for i in range(1, 15)])
        
        L = L_score / 140.0
        D = D_score / 140.0
        
        L_map = (L * 2) - 1
        D_map = (D * 2) - 1
        
        S = L * D

        quadrant_name = get_quadrant_name(L_map, D_map)
        quadrant_color = get_quadrant_color(L_map, D_map)
        
        q_advice = {
            "مؤمن (الربع الأول)": "أنت في الطريق الصحيح. حافظ على ثباتك، واستمر في النمو نحو (1,1).",
            "كافر (الربع الثاني)": "ولاؤك لغير الله. أنت بحاجة إلى توبة جذرية وتحويل بوصلتك نحو الخالق.",
            "منافق (الربع الثالث)": "أنت في حالة تذبذب خطيرة. أنت بحاجة إلى الصدق مع نفسك واتخاذ قرار حاسم.",
            "مشرك/راهب (الربع الرابع)": "لديك ولاء عالي لكن براءتك منهارة. أنت بحاجة إلى تقوية مناعتك الإيمانية.",
        }

        st.divider()
        st.header("📊 نتائج اختبار البوصلة الكونية")

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f"""
            <div style="background: rgba(10,10,46,0.8); border-radius: 15px; padding: 20px; border: 2px solid {quadrant_color}; margin: 10px 0; text-align: center;">
                <p style="font-size: 2em; font-weight: bold; color: {quadrant_color};">{quadrant_name}</p>
                <p>إحداثياتك على الخريطة: <b>L = {L_map:.2f}</b> | <b>D = {D_map:.2f}</b></p>
                <p style="font-size: 1.2em; margin-top: 10px; color: #FFD700;">⚖️ ثباتك الوجودي (العروة الوثقى): <b>S = L × D = {S:.2f}</b></p>
                <p style="font-size: 0.8em; color: #aaa;">الدرجة الخام: L = {L_score} / 140 | D = {D_score} / 140</p>
                <p>{q_advice.get(quadrant_name, '')}</p>
            </div>
            """, unsafe_allow_html=True)

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

        ax.text(0.5, 0.5, "مؤمن\n(W+, B+)", color='black', ha='center', alpha=0.7)
        ax.text(-0.5, 0.5, "كافر\n(W-, B+)", color='white', ha='center', alpha=0.7)
        ax.text(-0.5, -0.5, "منافق\n(W-, B-)", color='white', ha='center', alpha=0.7)
        ax.text(0.5, -0.5, "مشرك/راهب\n(W+, B-)", color='black', ha='center', alpha=0.7)
        
        ax.scatter(D_map, L_map, c='#00FFFF', s=200, edgecolors='white', linewidth=2, zorder=5)
        ax.tick_params(colors='white')
        st.pyplot(fig)

        if st.button("🔄 إعادة الاختبار"):
            st.session_state.compass_answers = {}
            st.rerun()
            # =============================================
# 📖 تبويب كتاب الميزان
# =============================================
with tab3:
    st.header("📖 كتاب الميزان")
    st.subheader("المختبر القرآني – من الثنائية الكونية إلى معادلة الوجود")
    st.caption("تأليف: علي عادل العاطفي | © 2026")
    st.divider()

    with st.expander("📜 الإهداء والمقدمة", expanded=False):
        st.markdown("""
        ### الإهداء
        إلى كل باحث عن الحقيقة، يبحث عن الخيط الناظم الذي يربط شتات هذا الوجود.
        إلى كل قلب حائر، يبحث عن الطمأنينة في زمن القلق.
        وإلى كل عقل متعطش، يريد أن يرى كيف يلتقي الوحي بالعلم.
        
        هذا الكتاب هو محاولة متواضعة لإعادة الأمور إلى نصابها، ولإثبات أن "الدين" ليس مجرد طقوس،
        بل هو "نظام التشغيل" الذي صممه الخالق لهذا الكون. إنه "الميزان" الذي وضعه الله،
        والذي يجب أن نتعلم كيف نقرأه في كتابه المسطور (القرآن) وكتابه المنظور (الكون).
        
        ### مقدمة المؤلف
        الحمد لله الذي رفع السماء ووضع الميزان، وجعل في كل شيء آية تدل على أنه الواحد الديان.
        والصلاة والسلام على النبي الأمي الذي أرسله الله بالدين القيم والإسلام الحنيف،
        رحمة للعالمين، وقدوة للسالكين.
        
        أما بعد، فهذا كتاب "الميزان". وهو ليس كتابًا كغيره من الكتب. إنه محاولة متواضعة،
        ولكنها جادة، لإعادة بناء "نظرية كل شيء" على أسس الوحي، بدلًا من أسس الفلسفة البشرية القاصرة.
        إنه يقدم "الدين القيم" (قانون السببية الأعظم) و"الإسلام الحنيف" (الاستجابة المثلى لهذا القانون)
        كمنظومة متكاملة تفسر الوجود من الذرة إلى الحضارة، ومن الأزل إلى الخلود.
        
        لقد حاولتُ أن أتتبع هذه المنظومة في كتاب الله المسطور (القرآن)، وفي كتابه المنظور (الآفاق والأنفس)،
        وأن أثبت أنهما يلتقيان على "ميزان" واحد دقيق، هو المعادلة:
        
        **S = W × B**
        
        حيث S هو الثبات الوجودي (Stability)، وW هو الولاء لله (Wala')، وB هي البراءة من الطاغوت (Bara'a).
        هذه المعادلة البسيطة في لفظها، العميقة في معناها، هي المفتاح الذي يفتح مغاليق كثيرة،
        ويجيب عن أسئلة حائرة.
        
        هذا الكتاب هو ثمرة تدبر وبحث. وهو ليس "علمًا" يضاف إلى العلوم، بل هو "أم العلم"
        التي تنتظم تحتها كل العلوم. والله أسأل أن يجعله خالصًا لوجهه، وأن ينفع به كاتبه وقارئه.
        """)

    with st.expander("🔍 تمهيد: البحث عن نظرية كل شيء", expanded=False):
        st.markdown("""
        منذ فجر الوعي، والبشرية تبحث عن إجابة لسؤال واحد:
        ما هو القانون الذي يحكم هذا الوجود؟
        لماذا تسقط ورقة الشجر بهذه الطريقة؟ ولماذا تسقط الحضارات العظيمة بعد أن تبلغ ذروتها؟
        هل هناك نظام واحد يفسر حركة الذرة والمجرة، ونبض الخلية وفناء الأمم؟
        
        في الفيزياء، قضى أينشتاين عقوده الأخيرة باحثًا عن "نظرية المجال الموحد"
        التي تجمع قوى الكون في معادلة واحدة. وفي الفلسفة، حاول الفلاسفة منذ أفلاطون وهيغل
        صياغة "نظرية كل شيء" تشرح المعنى الكلي للحياة. كان هذا هو "الكأس المقدسة" للعلم والفلسفة.
        لكنهم لم يصلوا.
        
        هذا الكتاب يقدم الإجابة التي بحثوا عنها. إجابة ليست من عند فيزيائي، ولا من عند فيلسوف،
        بل من عند خالق الكون نفسه. الإجابة كانت هنا دائمًا، في كتابه المسطور (القرآن)،
        وفي كتابه المنظور (الكون). إنها نظرية "الدين القيم"، أو ما نسميه "الميزان".
        إنها تثبت أن هناك قانونًا واحدًا فقط، هو "قانون السببية"، يحكم كل شيء:
        الذرة، الخلية، النفس، الأسرة، المجتمع، الأمة، الحضارة، والتاريخ.
        
        وهذا القانون يجد تعبيره الأكمل في معادلة الثبات الوجودي: **S = W × B**.
        
        هذه المعادلة ليست اختراعًا بشريًا، بل هي ترجمة رياضية لقوله تعالى:
        ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256].
        
        في زمن طغت فيه المادة على الروح، يأتي هذا الكتاب ليعيد للروح مكانتها،
        وليثبت أن "الغيب" هو أصل "الشهادة"، وأن "الوحي" هو مرشد "العقل"،
        وأن "الإيمان" هو "طاقة روحية" يمكن قياسها ومحاكاتها.
        """)

    with st.expander("الباب الأول: الأصول – من أين بدأنا؟", expanded=False):
        st.markdown("""
        ### الفصل الأول: ﴿اقْرَأْ بِاسْمِ رَبِّكَ﴾ – المنهج الإلهي لاكتشاف النظام
        
        في لحظة فارقة من تاريخ البشرية، تنزلت أول كلمة من السماء إلى الأرض.
        لم تكن أمرًا عسكريًا، ولا قانونًا اجتماعيًا، بل كانت أمرًا معرفيًا: ﴿اقْرَأْ﴾.
        إنه الإعلان عن مولد "منهج" جديد في النظر إلى الوجود.
        
        "اقرأ" لم تقتصر على تلاوة الحروف المكتوبة في المصحف، بل شملت قراءة "الكتاب المنظور"
        (الكون والأنفس) وقراءة "الكتاب المسطور" (الوحي). إنها دعوة مزدوجة للجمع بين العلم والإيمان،
        بين الفيزياء والميتافيزيقا، بين الخلق والأمر.
        
        والأمر لم يكن مطلقًا، بل كان مقيدًا بقيد هو "المفتاح" لهذا المنهج: ﴿بِاسْمِ رَبِّكَ﴾.
        هذه هي "عدسة الدين القيم". إنها التي تحول القراءة المادية المحايدة إلى قراءة إيمانية غائية.
        أن تقرأ "باسم ربك" يعني أن تسأل عن "لماذا" و"من" وراء كل ظاهرة، لا أن تكتفي بـ "كيف" حدثت.
        هذا القيد هو "الولاء" (W) الذي يوجه العقل نحو اكتشاف "القانون".
        
        ### الفصل الثاني: ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ – الإعلان عن القانون الأعظم
        
        بعد الأمر بالقراءة، يأتي الإعلان عن "القانون" نفسه. يقول الله تعالى:
        ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ﴾ [الرحمن: 7-8].
        
        هذا هو "الدين القيم". إنه ليس مجرد قوانين فيزيائية تحكم الكون، بل هو أيضًا
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
        
        ### ثانيًا: الإسلام الحنيف – الاستجابة الكونية الديناميكية
        
        الإسلام الحنيف هو: الاستجابة الكونية الديناميكية للدين القيم، من خلال آلية
        "الولاء لله" (W) و"البراءة من الطاغوت" (B)، كل عالم بما يناسب فطرته.
        
        - إسلام الجماد: الجاذبية (W) والتنافر (B). S = W × B.
        - إسلام النبات والحيوان: النمو (W) والمناعة (B).
        - إسلام الملائكة: التسبيح والعبادة.
        - إسلام الإنسان: الولاء والبراءة طوعًا. S = W × B.
        
        ### ثالثًا: العقيدة – الإيمان القلبي بعدالة القانون
        ### رابعًا: العبادة – محطات شحن الميزان
        ### خامسًا: الشريعة – المنهج والنظام
        """)

    with st.expander("الباب الثالث: الثنائية الكونية – الولاء والبراء في مرآة الوجود", expanded=False):
        st.markdown("""
        ### الكون يتكلم بلغة الثنائيات
        النور والظلام، الليل والنهار، الذكر والأنثى، الموجب والسالب، الجذب والتنافر.
        هذه الثنائيات ليست عشوائية، بل هي تعبير عن قانون واحد هو "الميزان".
        
        ### التطابق مع قوانين الفيزياء والبيولوجيا والكيمياء
        ### الدليل من الحروف المقطعة والأنظمة العددية
        """)

    with st.expander("الباب الرابع: وحدة الخلق والأمر – الدليل الكوني", expanded=False):
        st.markdown("""
        ### ﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ﴾ – وحدة المصدر
        الخالق والشارع واحد. القانون الذي يحكم الذرة (الخلق) هو نفسه الذي شرعه الله للإنسان (الأمر).
        
        ### الميزان في الآفاق – فيزياء الميزان
        الجاذبية (W) والتنافر (B) في الذرة. استقرار الذرة (S) = W × B.
        
        ### الميزان في الكيمياء
        الاتحاد (W) والتفكك (B) في التفاعلات. طاقة التنشيط = التوبة.
        
        ### الميزان في الأنفس – بيولوجيا الميزان
        جهاز المناعة: ذات (W) ولاذات (B). السرطان = استدراج بيولوجي.
        
        ### الميزان في التاريخ – سنة الله في الأمم
        الدولة الأموية، الاتحاد السوفيتي، الدولة العثمانية. كلها انهارت بانهيار W أو B.
        """)

    with st.expander("الباب الخامس: المختبر – تشغيل المحاكاة ورؤية الاستدراج", expanded=False):
        st.markdown("""
        ### لماذا النمذجة الحاسوبية؟
        لترجمة الوحي إلى لغة العصر.
        
        ### الحالات الأربع للكائن البشري
        - **الذهبي**: المؤمن (W و B عاليتان).
        - **الأبيض**: الراهب أو الصوفي (W عالية، B منهارة).
        - **الأحمر**: الكافر (W منهارة، B عالية).
        - **الوردي**: المنافق (W و B منهارتان).
        
        ### سرعة الضوء الأخلاقية
        S يسبق E دائمًا. هذه هي فجوة الاستدراج.
        """)

    with st.expander("الباب السادس: نحو الأمة الذهبية – من المختبر إلى الواقع", expanded=False):
        st.markdown("""
        ### إعادة تعريف الذات
        أين أنت على خريطة الميزان؟
        
        ### ورشة البناء
        توليد W (محطات الشحن). بناء B (تقوية المناعة). التوازن بينهما.
        
        ### هندسة المجتمع الذهبي
        خلايا النحل، صناعة القدوة، بناء المؤسسات.
        """)

    with st.expander("الباب السابع: الفطرة – نظام التشغيل الأصلي", expanded=False):
        st.markdown("""
        ### الميثاق الغليظ – يوم قالوا بلى
        ﴿أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾. هذه هي بذرة W.
        
        ### بنية الفطرة
        التطلع إلى المطلق، حب الخلود، حب الخير، الحاجة إلى المعنى.
        
        ### محاولات إسكات الفطرة
        عبادة العقل، عبادة المادة، عبادة الذات.
        """)

    with st.expander("الباب الثامن: التشخيص – واقع الأمة في ميزان S = W × B", expanded=False):
        st.markdown("""
        ### حال الميزان اليوم
        W ضعيفة، B منهارة، S تقترب من الصفر.
        
        ### الانفصام الخماسي
        عقدي، تشريعي، أخلاقي، اجتماعي، سياسي.
        
        ### الأسباب الجذرية
        الخلل في فهم "لا إله إلا الله"، الانهيار التربوي، الغزو الفكري، التبعية الاقتصادية.
        """)

    with st.expander("الباب التاسع: سبل العودة إلى القانون – كيف نعيد ضبط الميزان؟", expanded=False):
        st.markdown("""
        ### الإصلاح الفردي
        علاج معرفي (فهم التوحيد)، علاج قلبي (تطهير القلب)، علاج سلوكي (ربط العبادة بالسلوك).
        
        ### الإصلاح الأسري
        التأسيس السليم، التربية الواعية، العلاج الحكيم.
        
        ### الإصلاح المجتمعي
        إحياء روح الجماعة، بناء المؤسسات، تفعيل الأمر بالمعروف والنهي عن المنكر.
        
        ### انتظار سنة التمكين
        الصبر الاستراتيجي بعد استيفاء الشروط.
        """)

    with st.expander("الباب العاشر: اكتمال الدائرة – من الأزل إلى الخلود", expanded=False):
        st.markdown("""
        ### الطور الأول: الأزل – الميثاق الغليظ
        ### الطور الثاني: الخلق – كلمة "كُنْ"
        ### الطور الثالث: عالم الشهادة – الاستجابة للقانون
        ### الطور الرابع: الميزان يوم القيامة
        ### الطور الخامس: الخلود – دار القرار
        
        اكتملت الدائرة. من "اقرأ" إلى "الميزان"، من الأزل إلى الخلود.
        """)
# =============================================
# 📜 تبويب رسالة الترحيب
# =============================================
with tab4:
    st.header("📜 رسالة الترحيب")
    st.markdown("""
    <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">
    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
    > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"
    
    ---
    
    <b>الدين القيم</b> = قانون السببية الكوني، وهو الحق لأن واضعه الحق،
    وهو القيم لأنه من القيوم نفسه. هو القانون الأعظم، إنه "الدين القيم"
    الذي هو أصل الوجود وغايته.
    
    إنه <b>"الميزان"</b> الذي قامت به السماوات والأرض،
    والذي يدور حوله كل شيء، من الأزل إلى الخلود.
    
    ---
    
    ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ — الرحمن 7
    ﴿وَأَنزَلْنَا مَعَهُمُ الْكِتَابَ وَالْمِيزَانَ﴾ — الحديد 25
    ﴿اللَّهُ الَّذِي أَنزَلَ الْكِتَابَ بِالْحَقِّ وَالْمِيزَانَ﴾ — الشورى 17
    
    ---
    
    <b>© 2026 علي عادل العاطفي | Ali Adel Alatifi</b>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# 📋 تبويب الدليل المرجعي
# =============================================
with tab5:
    st.header("📋 الدليل المرجعي")
    st.markdown("""
    **المشروع:** نظرية الميزان – المختبر القرآني
    
    **المؤلف:** علي عادل العاطفي (Ali Adel Alatifi)
    
    **الترخيص:** MIT License
    
    ---
    
    ### 📚 المكتبة الرسمية
    الكتب والوثائق الكاملة متوفرة في مستودع المكتبة:
    [github.com/ali-adel-alatifi/mizan-library](https://github.com/ali-adel-alatifi/mizan-library)
    
    ---
    
    ### 🛡️ حقوق الملكية الفكرية
    © 2026 علي عادل العاطفي. جميع الحقوق محفوظة.
    هذا المشروع محمي بموجب ترخيص MIT License.
    يُسمح بالاستخدام والتعديل والنشر مع ذكر المصدر الأصلي والمؤلف.
    """)

# =============================================
# 📥 تذييل
# =============================================
st.divider()
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi | Al-Deen Al-Qayyim – The Cosmic Balance Law")
