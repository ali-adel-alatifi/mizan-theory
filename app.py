import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import deque
import random, time
from io import BytesIO

# =============================================
# الإعدادات العامة
# =============================================
st.set_page_config(
    page_title="⚖️ المختبر القرآني – النظام المتكامل",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# الثوابت الوجودية – المعجم الهندسي (28 حرفاً)
# =============================================
LETTERS = {
    'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60,
    'ح': 8, 'ط': 9, 'ق': 100, 'ك': 20, 'ص': 90,
    'ع': 70, 'ي': 10, 'هـ': 5, 'ن': 50, 'ف': 80,
    'و': 6, 'ب': 2, 'ظ': 900, 'ض': 800, 'غ': 1000,
    'ذ': 700, 'خ': 600, 'ش': 300, 'ز': 7, 'ج': 3,
    'ت': 400, 'ث': 500
}

# تسميات المؤشرات
W_LABELS = [
    "الصلاة", "الزكاة والصدقات", "الولاء لله ورسوله والمؤمنين",
    "تحكيم الشريعة", "العدل", "الشورى"
]
B_LABELS = [
    "البراءة من الطاغوت", "الرحمة والعطاء (الماعون)",
    "الأمر بالمعروف", "النهي عن المنكر", "النزاهة ومكافحة الفساد"
]
E_LABELS = [
    "السيادة والاستقلال", "الاكتفاء الذاتي",
    "الإنتاج الزراعي", "الإنتاج الصناعي", "القوة العسكرية"
]
E_LETTERS = ['م', 'ق', 'ك', 'ص', 'ر']

# تفصيل الصناعة (كهيعص)
IND_LABELS = [
    "التصميم والهندسة (ك)", "التصنيع والتشكيل (هـ)",
    "التطوير والتحسين (ي)", "البحث والتطوير (ع)", "الجودة والاستدامة (ص)"
]
IND_LETTERS = ['ك', 'هـ', 'ي', 'ع', 'ص']

# =============================================
# المحكمة العليا – أربع بوابات منطقية قرآنية
# =============================================
def supreme_court(W_raw, B_raw, W_pure, B2, B1):
    """
    المحكمة العليا لنظام الميزان.
    الترتيب: الشرك → الماعون → الإخلاص → الوعد
    """
    # البوابة 0: بوابة الشرك (النساء: 48)
    if not W_pure:
        return 0, "بوابة الشرك", "⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾ – كل عمل محبط", "🔴"

    # البوابة 1: بوابة الماعون (الماعون: 7)
    if B2 <= 0:
        return -1, "بوابة الماعون", "⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾", "🔴"

    # البوابة 2: بوابة الإخلاص (النور: 55)
    if W_raw > 0 and B1 <= 0:
        return 0, "بوابة الإخلاص", "⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي وَلَا يُشْرِكُونَ بِي شَيْئًا﴾", "🟡"

    # البوابة 3: بوابة الوعد (الانشقاق: 25)
    if W_raw > 0 and B_raw > 0:
        return 1, "بوابة الوعد", "🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾", "🟢"

    return None, None, None, None

def calculate_S(W_raw, B_raw, E_raw, W_pure, B2, B1):
    """حساب الثبات S باستخدام المعادلة الكاملة."""
    # تحقق من المحكمة العليا أولاً
    S_gate, gate_name, gate_msg, gate_color = supreme_court(W_raw, B_raw, W_pure, B2, B1)
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0

    # المعادلة العامة
    W = (W_raw + 1) / 2
    B = (B_raw + 1) / 2
    E = (E_raw + 1) / 2

    # تضخيم الحروف
    W_boost = 1 + (LETTERS['أ'] + LETTERS['ر'] + LETTERS['س'] + LETTERS['ط']) / 1000
    B_boost = 1 + (LETTERS['ل'] + LETTERS['ح'] + LETTERS['ط']) / 1000
    W_eff = W * W_boost
    B_eff = B * B_boost
    S_raw = W_eff * B_eff * (1 + LETTERS['م'] / 1000)

    istidraj_gap = max(0, E - S_raw)
    return min(1.0, S_raw), E, "المعادلة العامة", "", "⚪", istidraj_gap

def simulate_future(S, E, W_raw, B_raw, years=50):
    """محاكاة زمنية للمستقبل."""
    Sh, Eh = [S], [E]
    for _ in range(years):
        nE = Eh[-1] + 0.02 * (Sh[-1] - Eh[-1])
        nB = B_raw
        if nE > Sh[-1] + 0.2:
            nB -= 0.03
        elif nE < Sh[-1]:
            nB += 0.01
        nS = ((W_raw + 1) / 2) * ((nB + 1) / 2) * (1 + sum(LETTERS.values()) / 1000)
        Sh.append(nS)
        Eh.append(nE)
    return Sh, Eh

print("✅ المرحلة الأولى مكتملة: الأساسيات، قاعدة البيانات، دوال المحرك الوجودي.")

# =============================================
# المرحلة الثانية: الشريط الجانبي والمنزلقات
# =============================================

# حالة الجلسة لتخزين القيم الافتراضية
if "slider_values" not in st.session_state:
    st.session_state.slider_values = {
        "W1": 0.0, "W2": 0.0, "W3": 0.0, "W4": 0.0, "W5": 0.0, "W6": 0.0,
        "B1": 0.0, "B2": 0.0, "B3": 0.0, "B4": 0.0, "B5": 0.0,
        "E1": 0.0, "E2": 0.0, "E3": 0.0, "E4": 0.0, "E5": 0.0,
        "I1": 0.0, "I2": 0.0, "I3": 0.0, "I4": 0.0, "I5": 0.0,
        "W_pure": True
    }

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <h2 style='color:#FFD700;margin:0;'>⚖️ المختبر القرآني</h2>
        <p style='color:#e0e0e0;font-size:12px;margin:5px 0;'>S = W × B</p>
    </div>
    """, unsafe_allow_html=True)

    # اختيار وضع الإدخال
    mode = st.radio("🎛️ اختر وضع الإدخال:", 
                    ["🧑‍⚖️ التقدير اليدوي (المنزلقات)", "🤖 مساعد الذكاء الاصطناعي"])

    # متغيرات المنزلقات (قيم افتراضية)
    W1 = W2 = W3 = W4 = W5 = W6 = 0.0
    B1 = B2 = B3 = B4 = B5 = 0.0
    E1 = E2 = E3 = E4 = E5 = 0.0
    I1 = I2 = I3 = I4 = I5 = 0.0
    W_pure = True

    if mode == "🧑‍⚖️ التقدير اليدوي (المنزلقات)":
        # مؤشرات الولاء (W)
        with st.expander("🤍 مؤشرات الولاء (W)", expanded=True):
            W1 = st.slider(W_LABELS[0], -1.0, 1.0, 
                          st.session_state.slider_values["W1"], 0.1, key="s_W1")
            W2 = st.slider(W_LABELS[1], -1.0, 1.0, 
                          st.session_state.slider_values["W2"], 0.1, key="s_W2")
            W3 = st.slider(W_LABELS[2], -1.0, 1.0, 
                          st.session_state.slider_values["W3"], 0.1, key="s_W3")
            W4 = st.slider(W_LABELS[3], -1.0, 1.0, 
                          st.session_state.slider_values["W4"], 0.1, key="s_W4")
            W5 = st.slider(W_LABELS[4], -1.0, 1.0, 
                          st.session_state.slider_values["W5"], 0.1, key="s_W5")
            W6 = st.slider(W_LABELS[5], -1.0, 1.0, 
                          st.session_state.slider_values["W6"], 0.1, key="s_W6")
            W_pure = st.checkbox("الإخلاص لله (عدم الشرك)", 
                                value=st.session_state.slider_values["W_pure"],
                                help="هل الولاء خالص لله وحده؟")
            
            # تحديث حالة الجلسة
            st.session_state.slider_values.update({
                "W1": W1, "W2": W2, "W3": W3, "W4": W4, "W5": W5, "W6": W6,
                "W_pure": W_pure
            })

        # مؤشرات البراءة (B)
        with st.expander("❤️ مؤشرات البراءة (B)", expanded=True):
            B1 = st.slider(B_LABELS[0], -1.0, 1.0, 
                          st.session_state.slider_values["B1"], 0.1, key="s_B1")
            B2 = st.slider(B_LABELS[1], -1.0, 1.0, 
                          st.session_state.slider_values["B2"], 0.1, key="s_B2",
                          help="﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾")
            B3 = st.slider(B_LABELS[2], -1.0, 1.0, 
                          st.session_state.slider_values["B3"], 0.1, key="s_B3")
            B4 = st.slider(B_LABELS[3], -1.0, 1.0, 
                          st.session_state.slider_values["B4"], 0.1, key="s_B4")
            B5 = st.slider(B_LABELS[4], -1.0, 1.0, 
                          st.session_state.slider_values["B5"], 0.1, key="s_B5")
            
            st.session_state.slider_values.update({
                "B1": B1, "B2": B2, "B3": B3, "B4": B4, "B5": B5
            })

        # مؤشرات التمكين (E)
        with st.expander("🌐 مؤشرات التمكين (E)", expanded=True):
            E1 = st.slider(f"{E_LABELS[0]} (م={LETTERS['م']})", -1.0, 1.0, 
                          st.session_state.slider_values["E1"], 0.1, key="s_E1")
            E2 = st.slider(f"{E_LABELS[1]} (ق={LETTERS['ق']})", -1.0, 1.0, 
                          st.session_state.slider_values["E2"], 0.1, key="s_E2")
            E3 = st.slider(f"{E_LABELS[2]} (ك={LETTERS['ك']})", -1.0, 1.0, 
                          st.session_state.slider_values["E3"], 0.1, key="s_E3")
            E4_raw = st.slider(f"{E_LABELS[3]} (مجمل)", -1.0, 1.0, 
                              st.session_state.slider_values["E4"], 0.1, key="s_E4_raw")
            E5 = st.slider(f"{E_LABELS[4]} (ر={LETTERS['ر']})", -1.0, 1.0, 
                          st.session_state.slider_values["E5"], 0.1, key="s_E5")
            
            st.session_state.slider_values.update({
                "E1": E1, "E2": E2, "E3": E3, "E4": E4_raw, "E5": E5
            })

        # تفصيل الصناعة (كهيعص)
        with st.expander("🏭 تفصيل الصناعة (كهيعص)", expanded=False):
            st.caption("تفكيك مؤشر الصناعة إلى مكوناته الحرفية")
            I1 = st.slider(IND_LABELS[0], -1.0, 1.0, 
                          st.session_state.slider_values["I1"], 0.1, key="s_I1")
            I2 = st.slider(IND_LABELS[1], -1.0, 1.0, 
                          st.session_state.slider_values["I2"], 0.1, key="s_I2")
            I3 = st.slider(IND_LABELS[2], -1.0, 1.0, 
                          st.session_state.slider_values["I3"], 0.1, key="s_I3")
            I4 = st.slider(IND_LABELS[3], -1.0, 1.0, 
                          st.session_state.slider_values["I4"], 0.1, key="s_I4")
            I5 = st.slider(IND_LABELS[4], -1.0, 1.0, 
                          st.session_state.slider_values["I5"], 0.1, key="s_I5")
            
            # حساب المرجح للصناعة
            i_vals = [I1, I2, I3, I4, I5]
            i_weights = [LETTERS[l] for l in IND_LETTERS]
            E4 = np.average(i_vals, weights=i_weights)
            
            st.session_state.slider_values.update({
                "I1": I1, "I2": I2, "I3": I3, "I4": I4, "I5": I5
            })
    else:
        # وضع الذكاء الاصطناعي
        st.info("🤖 اكتب وصفًا للكيان (دولة، مجتمع، فرد) ليقوم الذكاء الاصطناعي بتقدير المؤشرات.")
        ai_text = st.text_area("الوصف النصي:", height=200, 
                              placeholder="مثال: دولة إسلامية ذات أغلبية شابة، تعاني من فساد إداري لكنها تملك جيشًا قويًا واقتصادًا زراعيًا...")
        if st.button("تحليل بالذكاء الاصطناعي", type="primary"):
            with st.spinner("جاري التحليل..."):
                # هنا يتم استبدال هذا بمكالمة API حقيقية
                ai_result = {
                    "W": [0.6, 0.5, 0.7, 0.4, 0.5, 0.3],
                    "B": [0.6, 0.4, 0.5, 0.3, 0.3],
                    "E": [0.5, 0.4, 0.6, 0.4, 0.7],
                    "I": [0.3, 0.4, 0.5, 0.2, 0.4],
                    "W_pure": True
                }
                st.session_state.ai_result = ai_result
                st.success("✅ تم التحليل!")
        else:
            st.session_state.ai_result = None

        if st.session_state.get("ai_result"):
            r = st.session_state.ai_result
            W1, W2, W3, W4, W5, W6 = r["W"]
            B1, B2, B3, B4, B5 = r["B"]
            E1, E2, E3, E4_raw, E5 = r["E"]
            I1, I2, I3, I4, I5 = r.get("I", [0]*5)
            W_pure = r.get("W_pure", True)
            i_vals = [I1, I2, I3, I4, I5]
            i_weights = [LETTERS[l] for l in IND_LETTERS]
            E4 = np.average(i_vals, weights=i_weights)

# =============================================
# المحرك الوجودي – الحساب
# =============================================
W_raw = np.mean([W1, W2, W3, W4, W5, W6])
B_raw = np.mean([B1, B2, B3, B4, B5])
E_vals = [E1, E2, E3, E4, E5]
E_weights = [LETTERS[l] for l in E_LETTERS]
E_raw = np.average(E_vals, weights=E_weights)

S_final, E_norm, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
    W_raw, B_raw, E_raw, W_pure, B2, B1
)

print("✅ المرحلة الثانية مكتملة: الشريط الجانبي، المنزلقات، الذكاء الاصطناعي، الحساب.")

# =============================================
# المرحلة الثالثة: عرض النتائج والتبويبات
# =============================================

# العنوان الرئيسي
st.markdown(f"""
<div style="text-align:center;padding:20px 0 10px 0;">
    <h1 style="color:#FFD700;font-size:2.5em;margin-bottom:0;">⚖️ المختبر القرآني</h1>
    <h2 style="color:#FFD700;font-size:1.3em;margin-top:0;">النظام المتكامل – من "كُن" إلى الكون</h2>
    <p style="color:#CCC;">﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>
</div>
""", unsafe_allow_html=True)

# =============================================
# لوحة القيادة – النتائج الرئيسية
# =============================================
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("W (الولاء)", f"{W_raw:+.2f}")
col2.metric("B (البراءة)", f"{B_raw:+.2f}")
col3.metric("S (الثبات)", f"{S_final:.2f}")
col4.metric("E (التمكين)", f"{E_norm:.2f}")
col5.metric("فجوة الاستدراج", f"{istidraj_gap:.2f}")

# عرض حكم المحكمة العليا
if gate_msg:
    st.markdown(f"### {gate_color} {gate_name}")
    if "انهيار" in gate_msg or "لا يغفر" in gate_msg:
        st.error(gate_msg)
    elif "باطلة" in gate_msg:
        st.warning(gate_msg)
    else:
        st.success(gate_msg)

# إنذار الاستدراج
if istidraj_gap > 0.3:
    st.error(f"🚨 إنذار استدراج: التمكين المادي (E={E_norm:.2f}) يتجاوز الثبات (S={S_final:.2f}) بفجوة {istidraj_gap:.2f}!")
elif istidraj_gap > 0.1:
    st.warning(f"⚡ تحذير: فجوة استدراج متوسطة ({istidraj_gap:.2f}).")

# =============================================
# التبويبات: الخريطة، المحاكي، المستشفى، المعجم
# =============================================
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ خريطة الوجود", "⏳ المحاكي الزمني", "🏥 المستشفى", "📖 المعجم الهندسي"])

with tab1:
    st.subheader("فضاء القيم – موقع الكيان")
    st.markdown("الخريطة الرباعية تُظهر موقعك في فضاء القيم بناءً على قيمتي الولاء (W) والبراءة (B).")
    
    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='grey', lw=0.5)
    ax.axvline(0, color='grey', lw=0.5)
    ax.set_xlabel("B (الكفر بالطاغوت)", color='white')
    ax.set_ylabel("W (الإيمان بالله)", color='white')
    
    # الأرباع
    ax.fill_between([0, 1.2], 0, 1.2, color='#FFD700', alpha=0.3, label='المؤمنون (الثبات)')
    ax.fill_between([-1.2, 0], 0, 1.2, color='#FF5252', alpha=0.2, label='المغضوب عليهم')
    ax.fill_between([-1.2, 0], -1.2, 0, color='#FFB6C1', alpha=0.2, label='المنافقون')
    ax.fill_between([0, 1.2], -1.2, 0, color='#FFA500', alpha=0.2, label='الضالون')
    
    # نقطة الكيان
    ax.scatter(B_raw, W_raw, s=400, c='cyan', edgecolors='white', linewidth=3, zorder=10)
    # مقام إبراهيم
    ax.scatter(1, 1, s=150, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, marker='*')
    ax.text(1, 1.15, 'مقام إبراهيم', color='#FFD700', fontsize=9, ha='center', fontweight='bold')
    
    # خط فجوة الاستدراج
    if istidraj_gap > 0:
        ax.text(0.5, -0.9, f"فجوة استدراج: {istidraj_gap:.2f}", color='red', fontsize=10, ha='center', fontweight='bold')
    
    ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower left')
    ax.tick_params(colors='white')
    st.pyplot(fig)

with tab2:
    st.subheader("المحاكي الزمني – حتمية المصير")
    st.markdown("هذه المحاكاة تظهر كيف ستتغير قيم S وE عبر الزمن بناءً على القيم الحالية.")
    
    years = st.slider("عدد سنوات المحاكاة:", 10, 100, 50, 10)
    S_hist, E_hist = simulate_future(S_final, E_norm, W_raw, B_raw, years)
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.plot(S_hist, label='S (الثبات)', color='#FFD700', linewidth=2.5)
    ax.plot(E_hist, label='E (التمكين)', color='#00FFFF', linewidth=2, linestyle='--')
    ax.fill_between(range(years + 1), S_hist, E_hist, 
                     where=(np.array(E_hist) > np.array(S_hist)), 
                     color='red', alpha=0.25, label='منطقة الاستدراج')
    ax.axhline(y=0, color='red', linestyle=':')
    ax.set_xlabel('السنوات', color='white')
    ax.set_ylabel('القيمة', color='white')
    ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2)
    st.pyplot(fig)
    
    # ملخص المحاكاة
    st.markdown(f"""
    **ملخص المحاكاة:**
    - S النهائي بعد {years} سنة: **{S_hist[-1]:.3f}**
    - E النهائي بعد {years} سنة: **{E_hist[-1]:.3f}**
    - الفجوة النهائية: **{max(0, E_hist[-1] - S_hist[-1]):.3f}**
    """)

with tab3:
    st.subheader("🏥 المستشفى – التشخيص والوصفة العلاجية")
    
    W_vals = [W1, W2, W3, W4, W5, W6]
    B_vals = [B1, B2, B3, B4, B5]
    E_v = [E1, E2, E3, E4, E5]
    
    wW = np.argmin(W_vals)
    wB = np.argmin(B_vals)
    wE = np.argmin(E_v)
    
    # التشخيص
    st.markdown("### 🔍 التشخيص")
    if gate_name == "بوابة الشرك":
        st.error("العلاج: تجديد التوحيد وإخلاص العبادة لله وحده.")
    elif gate_name == "بوابة الماعون":
        st.error(f"الأولوية القصوى: إصلاح مؤشر '{B_LABELS[wB]}'. بدون رحمة وعطاء، لا تنفع أي عبادة.")
    elif gate_name == "بوابة الإخلاص":
        st.warning(f"الأولوية: تنقية '{W_LABELS[wW]}' من شوائب الشرك والرياء، وتصحيح '{B_LABELS[wB]}'.")
    elif istidraj_gap > 0.3:
        st.error(f"الأولوية: سد فجوة الاستدراج ({istidraj_gap:.2f}) عبر رفع '{B_LABELS[wB]}' أو '{W_LABELS[wW]}'.")
    else:
        st.info(f"للتقدم نحو مقام إبراهيم: عزز '{W_LABELS[wW]}' و'{B_LABELS[wB]}' و'{E_LABELS[wE]}'.")
    
    # جدول المؤشرات
    st.markdown("### 📊 تفصيل المؤشرات")
    df_W = pd.DataFrame({'المؤشر': W_LABELS, 'القيمة': W_vals})
    df_B = pd.DataFrame({'المؤشر': B_LABELS, 'القيمة': B_vals})
    df_E = pd.DataFrame({'المؤشر': E_LABELS, 'القيمة': E_v})
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.dataframe(df_W.style.format({'القيمة': '{:+.2f}'}).background_gradient(subset=['القيمة'], cmap='RdYlGn'), hide_index=True)
    with col_b:
        st.dataframe(df_B.style.format({'القيمة': '{:+.2f}'}).background_gradient(subset=['القيمة'], cmap='RdYlGn'), hide_index=True)
    with col_c:
        st.dataframe(df_E.style.format({'القيمة': '{:+.2f}'}).background_gradient(subset=['القيمة'], cmap='RdYlGn'), hide_index=True)

with tab4:
    st.subheader("📖 المعجم الهندسي – الحروف وقيمها")
    st.markdown("""
    هذا المعجم يربط كل حرف من الحروف العربية بقيمته العددية (حساب الجمل) ودوره الوجودي في معادلة الميزان.
    """)
    
    letters_data = {
        'الفئة الأولى: الذات الإلهية (المصدر)': {'ك': 20, 'ن': 50},
        'الفئة الثانية: الازدواج': {'ق': 100, 'ص': 90},
        'الفئة الثالثة: التجلي الإلهي': {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        'الفئة الرابعة: الاشتراك (الجسور)': {'ع': 70, 'ي': 10, 'هـ': 5},
        'الفئة الخامسة: المشغلات': {'ف': 80, 'و': 6, 'ب': 2},
        'الفئة السادسة: أعمال الخلق': {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
    }
    
    for category, letters in letters_data.items():
        st.markdown(f"**{category}**")
        df = pd.DataFrame(list(letters.items()), columns=['الحرف', 'القيمة'])
        st.dataframe(df, hide_index=True, use_container_width=True)

# =============================================
# التذييل
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:20px;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.5em;">⚖️ المختبر القرآني – النظام المتكامل v1.0</p>
    <p>﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
    <p>علي عادل العاطفي | 2026</p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الثالثة مكتملة: عرض النتائج، الخريطة، المحاكي، المستشفى، المعجم الهندسي.")

# =============================================
# المرحلة الرابعة: المشهد الحي – المحاكاة الديناميكية
# =============================================

st.markdown("---")
st.header("🌌 المشهد الحي – المحاكاة الكونية")
st.markdown("هذه المحاكاة تظهر تفاعل النجوم (الأفراد) مع بعضها ومع قطبي الميزان W وB في الزمن الحقيقي.")

# إعدادات المشهد الحي
with st.expander("⚙️ إعدادات المشهد الحي", expanded=False):
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        live_speed = st.slider("سرعة المحاكاة", 0.01, 0.2, 0.08, 0.01, key="live_speed")
    with col_set2:
        live_stars = st.slider("عدد النجوم", 100, 500, 300, 50, key="live_stars")
    with col_set3:
        live_trail = st.slider("طول مسار الكواكب", 50, 300, 150, 10, key="live_trail")

# أزرار التحكم
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("▶️ تشغيل المشهد الحي", use_container_width=True, type="primary"):
        st.session_state.live_run = True
with col_btn2:
    if st.button("⏹️ إيقاف المشهد", use_container_width=True):
        st.session_state.live_run = False
with col_btn3:
    if st.button("🔄 إعادة ضبط المشهد", use_container_width=True):
        st.session_state.live_init = False
        st.session_state.live_run = False
        st.rerun()

# تهيئة المشهد الحي
if 'live_init' not in st.session_state:
    st.session_state.live_init = False
if 'live_run' not in st.session_state:
    st.session_state.live_run = False

if not st.session_state.live_init:
    # إعداد المركز
    cx, cy = 14.0, 10.0
    st.session_state.live_cx = cx
    st.session_state.live_cy = cy
    
    # توليد النجوم
    N = live_stars
    angles = np.random.uniform(0, 2 * np.pi, N)
    radii = np.random.uniform(1.5, 9, N)
    st.session_state.live_sx = cx + radii * np.cos(angles)
    st.session_state.live_sy = cy + radii * np.sin(angles) * 0.65
    st.session_state.live_sw = np.random.uniform(0.2, 0.9, N)
    st.session_state.live_sb = np.random.uniform(0.2, 0.9, N)
    
    # حالة الكواكب
    st.session_state.live_W = W_raw
    st.session_state.live_B = B_raw
    st.session_state.live_E = E_norm
    st.session_state.live_S = S_final
    st.session_state.live_phase = "توازن"
    
    # زوايا الكواكب
    st.session_state.live_aW = 0.0
    st.session_state.live_aB = np.pi * 0.5
    
    # مسارات الكواكب
    st.session_state.live_trail_Wx = deque(maxlen=live_trail)
    st.session_state.live_trail_Wy = deque(maxlen=live_trail)
    st.session_state.live_trail_Bx = deque(maxlen=live_trail)
    st.session_state.live_trail_By = deque(maxlen=live_trail)
    
    # تاريخ S وE
    st.session_state.live_hist_S = deque(maxlen=300)
    st.session_state.live_hist_E = deque(maxlen=300)
    st.session_state.live_hist_x = deque(maxlen=300)
    st.session_state.live_frame = 0
    
    st.session_state.live_init = True

# تشغيل المشهد الحي
if st.session_state.live_run:
    placeholder = st.empty()
    
    # استخراج الحالة الحالية
    cx = st.session_state.live_cx
    cy = st.session_state.live_cy
    sx = st.session_state.live_sx.copy()
    sy = st.session_state.live_sy.copy()
    sw = st.session_state.live_sw.copy()
    sb = st.session_state.live_sb.copy()
    W = st.session_state.live_W
    B = st.session_state.live_B
    E = st.session_state.live_E
    S = st.session_state.live_S
    phase = st.session_state.live_phase
    aW = st.session_state.live_aW
    aB = st.session_state.live_aB
    trail_Wx = st.session_state.live_trail_Wx
    trail_Wy = st.session_state.live_trail_Wy
    trail_Bx = st.session_state.live_trail_Bx
    trail_By = st.session_state.live_trail_By
    hist_S = st.session_state.live_hist_S
    hist_E = st.session_state.live_hist_E
    hist_x = st.session_state.live_hist_x
    frame = st.session_state.live_frame
    
    # تحديث النجوم
    for i in range(live_stars):
        # تأثير W وB العام
        sw[i] += (W - sw[i]) * 0.01 + np.random.uniform(-0.02, 0.02)
        sb[i] += (B - sb[i]) * 0.01 + np.random.uniform(-0.02, 0.02)
        
        # تأثير الجيران
        dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
        close = (dist < 2.0) & (np.arange(live_stars) != i)
        if np.any(close):
            sw[i] += (np.mean(sw[close]) - sw[i]) * 0.02
            sb[i] += (np.mean(sb[close]) - sb[i]) * 0.02
        
        sw[i] = np.clip(sw[i], 0.01, 1.0)
        sb[i] = np.clip(sb[i], 0.01, 1.0)
    
    # صدمات عشوائية
    if random.random() < 0.005:
        affected = np.random.choice(live_stars, size=int(live_stars * 0.2), replace=False)
        sw[affected] *= random.uniform(0.5, 0.8)
        sb[affected] *= random.uniform(0.5, 0.8)
        phase = "💥 صدمة"
    
    # تحديث W وB من متوسط النجوم
    avg_W = np.mean(sw)
    avg_B = np.mean(sb)
    W += (avg_W - W) * 0.03
    B += (avg_B - B) * 0.03
    W = np.clip(W, 0.01, 1.0)
    B = np.clip(B, 0.01, 1.0)
    S = W * B
    
    # تحديث E (التمكين) بتأخير
    E += 0.02 * (S - E)
    
    # تحديد الطور
    if S > 0.7: phase = "🌟 ثبات"
    elif S > 0.4: phase = "⚖️ توازن"
    elif S > 0.2: phase = "⚠️ اهتزاز"
    elif S > 0.05: phase = "📉 انهيار"
    else: phase = "💀 قاع"
    
    if E > S + 0.2: phase = "🚨 استدراج"
    
    # تحديث زوايا الكواكب
    aW += 0.02 + random.uniform(-0.01, 0.01) * (1 - W)**2
    aB += 0.02 + random.uniform(-0.01, 0.01) * (1 - B)**2
    
    # مواقع الكواكب
    orbit_W = 7 - 2.5 * W
    orbit_B = 5 - 1.5 * B
    wx = cx + orbit_W * np.cos(aW)
    wy = cy + orbit_W * np.sin(aW) * 0.7
    bx = cx + orbit_B * np.cos(aB)
    by = cy + orbit_B * np.sin(aB) * 0.7
    
    # تحديث المسارات
    trail_Wx.append(wx)
    trail_Wy.append(wy)
    trail_Bx.append(bx)
    trail_By.append(by)
    
    # حركة النجوم
    instability = 1 - np.mean(sw * sb)
    sx += np.random.uniform(-0.05, 0.05, live_stars) * instability
    sy += np.random.uniform(-0.05, 0.05, live_stars) * instability
    sx = np.clip(sx, cx - 13, cx + 13)
    sy = np.clip(sy, cy - 9, cy + 9)
    
    # تحديث التاريخ
    frame += 1
    if frame % 2 == 0:
        hist_S.append(S)
        hist_E.append(E)
        hist_x.append(len(hist_x))
    
    # حفظ الحالة
    st.session_state.live_sx = sx
    st.session_state.live_sy = sy
    st.session_state.live_sw = sw
    st.session_state.live_sb = sb
    st.session_state.live_W = W
    st.session_state.live_B = B
    st.session_state.live_E = E
    st.session_state.live_S = S
    st.session_state.live_phase = phase
    st.session_state.live_aW = aW
    st.session_state.live_aB = aB
    st.session_state.live_trail_Wx = trail_Wx
    st.session_state.live_trail_Wy = trail_Wy
    st.session_state.live_trail_Bx = trail_Bx
    st.session_state.live_trail_By = trail_By
    st.session_state.live_hist_S = hist_S
    st.session_state.live_hist_E = hist_E
    st.session_state.live_hist_x = hist_x
    st.session_state.live_frame = frame
    
    # رسم المشهد
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000010')
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 20)
    ax.axis('off')
    
    # النواة الذهبية S
    for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                     (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
        ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), r * (0.5 + 2.8 * S), color=c, alpha=a, zorder=15))
    ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')
    
    # هالة التمكين E
    ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 0.5 + 14 * E, color='#0FF', alpha=0.15, zorder=7))
    
    # الغشاء
    ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 8.5, color='#0F8', alpha=0.1, fill=False, lw=2, zorder=2))
    
    # الكوكبان W و B
    ax.add_patch(plt.matplotlib.patches.Circle((wx, wy), 0.2 + 0.5 * W, color='#FFF', alpha=1, zorder=13))
    ax.add_patch(plt.matplotlib.patches.Circle((bx, by), 0.2 + 0.5 * B, color='#F33', alpha=0.8, zorder=13))
    ax.text(wx, wy + 0.8, 'W', color='#FFF', fontsize=10, ha='center')
    ax.text(bx, by + 0.8, 'B', color='#F33', fontsize=10, ha='center')
    
    # مسارات الكواكب
    if len(trail_Wx) > 1:
        ax.plot(list(trail_Wx), list(trail_Wy), color='#FFF', lw=0.3, alpha=0.2, zorder=4)
    if len(trail_Bx) > 1:
        ax.plot(list(trail_Bx), list(trail_By), color='#F33', lw=0.3, alpha=0.2, zorder=4)
    
    # النجوم
    star_colors = []
    for i in range(live_stars):
        w, b = sw[i], sb[i]
        if w >= 0.55 and b >= 0.55: star_colors.append('#FFD700')
        elif w >= 0.55 and b < 0.45: star_colors.append('#E0E0E0')
        elif w < 0.45 and b >= 0.55: star_colors.append('#FF5252')
        elif w < 0.45 and b < 0.45: star_colors.append('#FFB6C1')
        else: star_colors.append('#888888')
    ax.scatter(sx, sy, s=30, c=star_colors, alpha=0.85, edgecolors='white', linewidths=0.3, zorder=5)
    
    # لوحة الإثبات
    pax = ax.inset_axes([0.5, 0.02, 0.46, 0.10])
    pax.set_xlim(0, 300)
    pax.set_ylim(0, 1.05)
    pax.set_title('S (ذهب) → E (سماوي) – الاستدراج', color='white', fontsize=7)
    pax.tick_params(colors='white', labelsize=4)
    pax.grid(True, alpha=0.12)
    if list(hist_S):
        pax.plot(list(hist_x), list(hist_S), color='#FFD700', lw=2)
        pax.plot(list(hist_x), list(hist_E), color='#0FF', lw=1.5)
    
    # شريط الحالة
    n_gold = np.sum((sw >= 0.55) & (sb >= 0.55))
    n_white = np.sum((sw >= 0.55) & (sb < 0.45))
    n_red = np.sum((sw < 0.45) & (sb >= 0.55))
    n_pink = np.sum((sw < 0.45) & (sb < 0.45))
    ax.text(14, 1.2, f'{phase} | 🟡{n_gold} ⚪{n_white} 🔴{n_red} 🩷{n_pink} | S={S:.2f} E={E:.2f}', 
            color='white', fontsize=10, ha='center', fontweight='bold')
    
    plt.tight_layout(pad=0)
    placeholder.pyplot(fig)
    
    # تحميل الصورة
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, facecolor='#000010')
    buf.seek(0)
    st.session_state.live_image = buf
    plt.close(fig)
    
    # إعادة التشغيل التلقائي
    time.sleep(live_speed)
    st.rerun()

elif st.session_state.live_init and 'live_image' in st.session_state:
    st.image(st.session_state.live_image, caption="آخر حالة للمشهد الحي", use_column_width=True)
    st.info("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة.")
else:
    st.info("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة الديناميكية.")

# زر تحميل صورة المشهد الحي
if 'live_image' in st.session_state:
    st.download_button(
        label="📥 تحميل صورة المشهد الحي",
        data=st.session_state.live_image,
        file_name="mizan_live_scene.png",
        mime="image/png",
        key="dl_live"
    )

print("✅ المرحلة الرابعة مكتملة: المشهد الحي – المحاكاة الكونية الديناميكية.")
print("✅✅✅ تم بناء المختبر القرآني بكافة أركانه وأدواته ولوازمه.")
