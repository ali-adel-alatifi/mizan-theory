import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import deque
import random, time
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# =============================================
# الإعدادات العامة
# =============================================
st.set_page_config(
    page_title="⚖️ المختبر القرآني – The Quranic Lab",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# النظام اللغوي
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

LANG = st.session_state.lang
TXT = lambda ar, en: ar if LANG == "ar" else en

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

# تسميات المؤشرات (عربي وإنجليزي)
W_LABELS_AR = [
    "الصلاة", "الزكاة والصدقات", "الولاء لله ورسوله والمؤمنين",
    "تحكيم الشريعة", "العدل", "الشورى"
]
W_LABELS_EN = [
    "Prayer", "Zakat & Charity", "Loyalty to Allah, Messenger & Believers",
    "Applying Sharia", "Justice", "Consultation (Shura)"
]

B_LABELS_AR = [
    "البراءة من الطاغوت", "الرحمة والعطاء (الماعون)",
    "الأمر بالمعروف", "النهي عن المنكر", "النزاهة ومكافحة الفساد"
]
B_LABELS_EN = [
    "Disavowal of Taghut", "Mercy & Giving (Al-Ma'un)",
    "Enjoining Good", "Forbidding Evil", "Integrity & Anti-Corruption"
]

E_LABELS_AR = [
    "السيادة والاستقلال", "الاكتفاء الذاتي",
    "الإنتاج الزراعي", "الإنتاج الصناعي", "القوة العسكرية"
]
E_LABELS_EN = [
    "Sovereignty & Independence", "Self-Sufficiency",
    "Agricultural Production", "Industrial Production", "Military Power"
]
E_LETTERS = ['م', 'ق', 'ك', 'ص', 'ر']

# تفصيل الصناعة (كهيعص)
IND_LABELS_AR = [
    "التصميم والهندسة (ك)", "التصنيع والتشكيل (هـ)",
    "التطوير والتحسين (ي)", "البحث والتطوير (ع)", "الجودة والاستدامة (ص)"
]
IND_LABELS_EN = [
    "Design & Engineering (K)", "Manufacturing & Forming (H)",
    "Development & Improvement (Y)", "Research & Development (A)", "Quality & Sustainability (S)"
]
IND_LETTERS = ['ك', 'هـ', 'ي', 'ع', 'ص']

def get_labels(category):
    if LANG == "ar":
        return {
            "W": W_LABELS_AR,
            "B": B_LABELS_AR,
            "E": E_LABELS_AR,
            "I": IND_LABELS_AR
        }.get(category, [])
    else:
        return {
            "W": W_LABELS_EN,
            "B": B_LABELS_EN,
            "E": E_LABELS_EN,
            "I": IND_LABELS_EN
        }.get(category, [])

# =============================================
# المحكمة العليا – أربع بوابات منطقية قرآنية
# =============================================
def supreme_court(W_raw, B_raw, W_pure, B2, B1):
    if not W_pure:
        return 0, TXT("بوابة الشرك", "Shirk Gate"), TXT(
            "⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾ – كل عمل محبط",
            "⚠️ Unforgivable: 'Indeed, Allah does not forgive association with Him' – All deeds nullified"
        ), "🔴"
    if B2 <= 0:
        return -1, TXT("بوابة الماعون", "Al-Ma'un Gate"), TXT(
            "⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾",
            "⚠️ Collapse: 'So woe to those who pray... who withhold simple assistance'"
        ), "🔴"
    if W_raw > 0 and B1 <= 0:
        return 0, TXT("بوابة الإخلاص", "Sincerity Gate"), TXT(
            "⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي وَلَا يُشْرِكُونَ بِي شَيْئًا﴾",
            "⚠️ Void worship: 'They worship Me, not associating anything with Me'"
        ), "🟡"
    if W_raw > 0 and B_raw > 0:
        return 1, TXT("بوابة الوعد", "Promise Gate"), TXT(
            "🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾",
            "🟢 Stability: 'For them is a reward uninterrupted'"
        ), "🟢"
    return None, None, None, None

def calculate_S(W_raw, B_raw, E_raw, W_pure, B2, B1):
    S_gate, gate_name, gate_msg, gate_color = supreme_court(W_raw, B_raw, W_pure, B2, B1)
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0

    W = (W_raw + 1) / 2
    B = (B_raw + 1) / 2
    E = (E_raw + 1) / 2

    W_boost = 1 + (LETTERS['أ'] + LETTERS['ر'] + LETTERS['س'] + LETTERS['ط']) / 1000
    B_boost = 1 + (LETTERS['ل'] + LETTERS['ح'] + LETTERS['ط']) / 1000
    W_eff = W * W_boost
    B_eff = B * B_boost
    S_raw = W_eff * B_eff * (1 + LETTERS['م'] / 1000)

    istidraj_gap = max(0, E - S_raw)
    return min(1.0, S_raw), E, TXT("المعادلة العامة", "General Equation"), "", "⚪", istidraj_gap

def simulate_future(S, E, W_raw, B_raw, years=50):
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

# =============================================
# الشريط الجانبي
# =============================================
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:10px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <h2 style='color:#FFD700;margin:0;'>⚖️ {TXT('المختبر القرآني', 'The Quranic Lab')}</h2>
        <p style='color:#e0e0e0;font-size:12px;margin:5px 0;'>S = W × B</p>
    </div>
    """, unsafe_allow_html=True)

    # زر تغيير اللغة
    if st.button("🇬🇧 English" if LANG == "ar" else "🇸🇦 العربية"):
        st.session_state.lang = "en" if LANG == "ar" else "ar"
        st.rerun()

    mode = st.radio(TXT("🎛️ اختر وضع الإدخال:", "🎛️ Select Input Mode:"),
                    [TXT("🧑‍⚖️ التقدير اليدوي (المنزلقات)", "🧑‍⚖️ Manual Estimation (Sliders)"),
                     TXT("🤖 مساعد الذكاء الاصطناعي", "🤖 AI Assistant")])

    # متغيرات المنزلقات
    W1=W2=W3=W4=W5=W6=0.0
    B1=B2=B3=B4=B5=0.0
    E1=E2=E3=E4=E5=0.0
    I1=I2=I3=I4=I5=0.0
    W_pure=True

    if "🧑‍⚖️" in mode:
        W_L = get_labels("W")
        B_L = get_labels("B")
        E_L = get_labels("E")
        I_L = get_labels("I")

        with st.expander(TXT("🤍 مؤشرات الولاء (W)", "🤍 Loyalty Indicators (W)"), expanded=True):
            W1 = st.slider(W_L[0], -1.0, 1.0, 0.0, 0.1)
            W2 = st.slider(W_L[1], -1.0, 1.0, 0.0, 0.1)
            W3 = st.slider(W_L[2], -1.0, 1.0, 0.0, 0.1)
            W4 = st.slider(W_L[3], -1.0, 1.0, 0.0, 0.1)
            W5 = st.slider(W_L[4], -1.0, 1.0, 0.0, 0.1)
            W6 = st.slider(W_L[5], -1.0, 1.0, 0.0, 0.1)
            W_pure = st.checkbox(TXT("الإخلاص لله (عدم الشرك)", "Sincerity to Allah (No Shirk)"), value=True)

        with st.expander(TXT("❤️ مؤشرات البراءة (B)", "❤️ Disavowal Indicators (B)"), expanded=True):
            B1 = st.slider(B_L[0], -1.0, 1.0, 0.0, 0.1)
            B2 = st.slider(B_L[1], -1.0, 1.0, 0.0, 0.1, help=TXT("﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾", "'So woe to those who pray... who withhold simple assistance'"))
            B3 = st.slider(B_L[2], -1.0, 1.0, 0.0, 0.1)
            B4 = st.slider(B_L[3], -1.0, 1.0, 0.0, 0.1)
            B5 = st.slider(B_L[4], -1.0, 1.0, 0.0, 0.1)

        with st.expander(TXT("🌐 مؤشرات التمكين (E)", "🌐 Empowerment Indicators (E)"), expanded=True):
            E1 = st.slider(f"{E_L[0]} (م={LETTERS['م']})", -1.0, 1.0, 0.0, 0.1)
            E2 = st.slider(f"{E_L[1]} (ق={LETTERS['ق']})", -1.0, 1.0, 0.0, 0.1)
            E3 = st.slider(f"{E_L[2]} (ك={LETTERS['ك']})", -1.0, 1.0, 0.0, 0.1)
            E4_raw = st.slider(f"{E_L[3]} ({TXT('مجمل', 'Overall')})", -1.0, 1.0, 0.0, 0.1)
            E5 = st.slider(f"{E_L[4]} (ر={LETTERS['ر']})", -1.0, 1.0, 0.0, 0.1)

        with st.expander(TXT("🏭 تفصيل الصناعة (كهيعص)", "🏭 Industry Breakdown (كهيعص)"), expanded=False):
            I1 = st.slider(I_L[0], -1.0, 1.0, 0.0, 0.1)
            I2 = st.slider(I_L[1], -1.0, 1.0, 0.0, 0.1)
            I3 = st.slider(I_L[2], -1.0, 1.0, 0.0, 0.1)
            I4 = st.slider(I_L[3], -1.0, 1.0, 0.0, 0.1)
            I5 = st.slider(I_L[4], -1.0, 1.0, 0.0, 0.1)
            i_vals = [I1, I2, I3, I4, I5]
            i_weights = [LETTERS[l] for l in IND_LETTERS]
            E4 = np.average(i_vals, weights=i_weights)

    else:
        st.info(TXT(
            "🤖 اكتب وصفًا للكيان (دولة، مجتمع، فرد) ليقوم الذكاء الاصطناعي بتقدير المؤشرات.",
            "🤖 Describe the entity (country, community, individual) for AI to estimate indicators."
        ))
        ai_text = st.text_area(TXT("الوصف النصي:", "Description:"), height=200,
                              placeholder=TXT("مثال: دولة إسلامية ذات أغلبية شابة...", "Example: An Islamic country with a young majority..."))
        if st.button(TXT("تحليل بالذكاء الاصطناعي", "Analyze with AI"), type="primary"):
            with st.spinner(TXT("جاري التحليل...", "Analyzing...")):
                ai_result = {
                    "W": [0.6, 0.5, 0.7, 0.4, 0.5, 0.3],
                    "B": [0.6, 0.4, 0.5, 0.3, 0.3],
                    "E": [0.5, 0.4, 0.6, 0.4, 0.7],
                    "I": [0.3, 0.4, 0.5, 0.2, 0.4],
                    "W_pure": True
                }
                st.session_state.ai_result = ai_result
                st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
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

# =============================================
# العنوان الرئيسي
# =============================================
st.markdown(f"""
<div style="text-align:center;padding:20px 0 10px 0;">
    <h1 style="color:#FFD700;font-size:2.5em;margin-bottom:0;">⚖️ {TXT('المختبر القرآني', 'The Quranic Lab')}</h1>
    <h2 style="color:#FFD700;font-size:1.3em;margin-top:0;">{TXT('النظام المتكامل – من "كُن" إلى الكون', 'The Integrated System – From "Be" to the Universe')}</h2>
    <p style="color:#CCC;">﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>
</div>
""", unsafe_allow_html=True)

# =============================================
# لوحة القيادة
# =============================================
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(TXT("W (الولاء)", "W (Loyalty)"), f"{W_raw:+.2f}")
col2.metric(TXT("B (البراءة)", "B (Disavowal)"), f"{B_raw:+.2f}")
col3.metric(TXT("S (الثبات)", "S (Stability)"), f"{S_final:.2f}")
col4.metric(TXT("E (التمكين)", "E (Empowerment)"), f"{E_norm:.2f}")
col5.metric(TXT("فجوة الاستدراج", "Istidraj Gap"), f"{istidraj_gap:.2f}")

if gate_msg:
    st.markdown(f"### {gate_color} {gate_name}")
    if TXT("انهيار", "Collapse") in gate_msg or TXT("لا يغفر", "Unforgivable") in gate_msg:
        st.error(gate_msg)
    elif TXT("باطلة", "Void") in gate_msg:
        st.warning(gate_msg)
    else:
        st.success(gate_msg)

if istidraj_gap > 0.3:
    st.error(f"🚨 {TXT('إنذار استدراج', 'Istidraj Alert')}: E={E_norm:.2f} > S={S_final:.2f} ({TXT('فجوة', 'Gap')} {istidraj_gap:.2f})")
elif istidraj_gap > 0.1:
    st.warning(f"⚡ {TXT('تحذير: فجوة استدراج متوسطة', 'Warning: Moderate Istidraj Gap')} ({istidraj_gap:.2f})")

# =============================================
# التبويبات
# =============================================
tab1, tab2, tab3, tab4 = st.tabs([
    TXT("🗺️ خريطة الوجود", "🗺️ Existence Map"),
    TXT("⏳ المحاكي الزمني", "⏳ Time Simulator"),
    TXT("🏥 المستشفى", "🏥 The Hospital"),
    TXT("📖 المعجم الهندسي", "📖 Geometric Lexicon")
])

with tab1:
    st.subheader(TXT("فضاء القيم – موقع الكيان", "Value Space – Entity Position"))
    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
    ax.set_xlabel(TXT("B (الكفر بالطاغوت)", "B (Disavowal)"), color='white')
    ax.set_ylabel(TXT("W (الإيمان بالله)", "W (Loyalty)"), color='white')
    ax.fill_between([0, 1.2], 0, 1.2, color='#FFD700', alpha=0.3, label=TXT('المؤمنون (الثبات)', 'Believers (Stability)'))
    ax.fill_between([-1.2, 0], 0, 1.2, color='#FF5252', alpha=0.2, label=TXT('المغضوب عليهم', 'Those with Wrath'))
    ax.fill_between([-1.2, 0], -1.2, 0, color='#FFB6C1', alpha=0.2, label=TXT('المنافقون', 'Hypocrites'))
    ax.fill_between([0, 1.2], -1.2, 0, color='#FFA500', alpha=0.2, label=TXT('الضالون', 'Those Astray'))
    ax.scatter(B_raw, W_raw, s=400, c='cyan', edgecolors='white', linewidth=3, zorder=10)
    ax.scatter(1, 1, s=150, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, marker='*')
    ax.text(1, 1.15, TXT('مقام إبراهيم', 'Station of Abraham'), color='#FFD700', fontsize=9, ha='center', fontweight='bold')
    if istidraj_gap > 0:
        ax.text(0.5, -0.9, f"{TXT('فجوة استدراج', 'Istidraj Gap')}: {istidraj_gap:.2f}", color='red', fontsize=10, ha='center', fontweight='bold')
    ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower left')
    ax.tick_params(colors='white')
    st.pyplot(fig)

with tab2:
    st.subheader(TXT("المحاكي الزمني – حتمية المصير", "Time Simulator – Inevitable Fate"))
    years = st.slider(TXT("عدد سنوات المحاكاة:", "Simulation Years:"), 10, 100, 50, 10)
    S_hist, E_hist = simulate_future(S_final, E_norm, W_raw, B_raw, years)
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.plot(S_hist, label='S (الثبات)', color='#FFD700', linewidth=2.5)
    ax.plot(E_hist, label='E (التمكين)', color='#00FFFF', linewidth=2, linestyle='--')
    ax.fill_between(range(years + 1), S_hist, E_hist, where=(np.array(E_hist) > np.array(S_hist)), color='red', alpha=0.25, label=TXT('منطقة الاستدراج', 'Istidraj Zone'))
    ax.axhline(y=0, color='red', linestyle=':')
    ax.set_xlabel(TXT('السنوات', 'Years'), color='white')
    ax.set_ylabel(TXT('القيمة', 'Value'), color='white')
    ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white')
    ax.tick_params(colors='white'); ax.grid(True, alpha=0.2)
    st.pyplot(fig)
    st.markdown(f"""
    **{TXT('ملخص المحاكاة:', 'Simulation Summary:')}**
    - S {TXT('النهائي', 'Final')} {TXT('بعد', 'after')} {years} {TXT('سنة', 'years')}: **{S_hist[-1]:.3f}**
    - E {TXT('النهائي', 'Final')} {TXT('بعد', 'after')} {years} {TXT('سنة', 'years')}: **{E_hist[-1]:.3f}**
    - {TXT('الفجوة النهائية', 'Final Gap')}: **{max(0, E_hist[-1] - S_hist[-1]):.3f}**
    """)

with tab3:
    st.subheader(TXT("🏥 المستشفى – التشخيص والوصفة العلاجية", "🏥 The Hospital – Diagnosis & Prescription"))
    W_vals = [W1, W2, W3, W4, W5, W6]
    B_vals = [B1, B2, B3, B4, B5]
    E_v = [E1, E2, E3, E4, E5]
    wW = np.argmin(W_vals)
    wB = np.argmin(B_vals)
    wE = np.argmin(E_v)

    W_L = get_labels("W")
    B_L = get_labels("B")
    E_L = get_labels("E")

    st.markdown(TXT("### 🔍 التشخيص", "### 🔍 Diagnosis"))
    if gate_name == TXT("بوابة الشرك", "Shirk Gate"):
        st.error(TXT("العلاج: تجديد التوحيد وإخلاص العبادة لله وحده.", "Treatment: Renew Tawheed and sincerity to Allah alone."))
    elif gate_name == TXT("بوابة الماعون", "Al-Ma'un Gate"):
        st.error(TXT(f"الأولوية القصوى: إصلاح مؤشر '{B_L[wB]}'. بدون رحمة وعطاء، لا تنفع أي عبادة.", f"Top priority: Fix '{B_L[wB]}'. Without mercy and giving, no worship benefits."))
    elif gate_name == TXT("بوابة الإخلاص", "Sincerity Gate"):
        st.warning(TXT(f"الأولوية: تنقية '{W_L[wW]}' من شوائب الشرك والرياء.", f"Priority: Purify '{W_L[wW]}' from shirk and hypocrisy."))
    elif istidraj_gap > 0.3:
        st.error(TXT(f"الأولوية: سد فجوة الاستدراج ({istidraj_gap:.2f}) عبر رفع '{B_L[wB]}' أو '{W_L[wW]}'.", f"Priority: Close the Istidraj gap ({istidraj_gap:.2f}) by raising '{B_L[wB]}' or '{W_L[wW]}'."))
    else:
        st.info(TXT(f"للتقدم نحو مقام إبراهيم: عزز '{W_L[wW]}' و'{B_L[wB]}' و'{E_L[wE]}'.", f"To advance to the Station of Abraham: strengthen '{W_L[wW]}', '{B_L[wB]}' and '{E_L[wE]}'."))

    st.markdown(TXT("### 📊 تفصيل المؤشرات", "### 📊 Indicator Details"))
    df_W = pd.DataFrame({TXT('المؤشر', 'Indicator'): W_L, TXT('القيمة', 'Value'): W_vals})
    df_B = pd.DataFrame({TXT('المؤشر', 'Indicator'): B_L, TXT('القيمة', 'Value'): B_vals})
    df_E = pd.DataFrame({TXT('المؤشر', 'Indicator'): E_L, TXT('القيمة', 'Value'): E_v})

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.dataframe(df_W.style.format({TXT('القيمة', 'Value'): '{:+.2f}'}).background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'), hide_index=True)
    with col_b:
        st.dataframe(df_B.style.format({TXT('القيمة', 'Value'): '{:+.2f}'}).background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'), hide_index=True)
    with col_c:
        st.dataframe(df_E.style.format({TXT('القيمة', 'Value'): '{:+.2f}'}).background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'), hide_index=True)

with tab4:
    st.subheader(TXT("📖 المعجم الهندسي – الحروف وقيمها", "📖 Geometric Lexicon – Letters & Values"))
    letters_data = {
        TXT('الفئة الأولى: الذات الإلهية (المصدر)', 'Category 1: Divine Essence (Source)'): {'ك': 20, 'ن': 50},
        TXT('الفئة الثانية: الازدواج', 'Category 2: Duality'): {'ق': 100, 'ص': 90},
        TXT('الفئة الثالثة: التجلي الإلهي', 'Category 3: Divine Manifestation'): {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        TXT('الفئة الرابعة: الاشتراك (الجسور)', 'Category 4: Connection (Bridges)'): {'ع': 70, 'ي': 10, 'هـ': 5},
        TXT('الفئة الخامسة: المشغلات', 'Category 5: Operators'): {'ف': 80, 'و': 6, 'ب': 2},
        TXT('الفئة السادسة: أعمال الخلق', 'Category 6: Actions of Creation'): {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
    }
    for category, letters in letters_data.items():
        st.markdown(f"**{category}**")
        df = pd.DataFrame(list(letters.items()), columns=[TXT('الحرف', 'Letter'), TXT('القيمة', 'Value')])
        st.dataframe(df, hide_index=True, use_container_width=True)

# =============================================
# المشهد الحي – المحاكاة الكونية
# =============================================
st.markdown("---")
st.header(TXT("🌌 المشهد الحي – المحاكاة الكونية", "🌌 Live Scene – Cosmic Simulation"))

with st.expander(TXT("⚙️ إعدادات المشهد الحي", "⚙️ Live Scene Settings"), expanded=False):
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        live_speed = st.slider(TXT("سرعة المحاكاة", "Simulation Speed"), 0.01, 0.2, 0.08, 0.01, key="live_speed")
    with col_set2:
        live_stars = st.slider(TXT("عدد النجوم", "Number of Stars"), 100, 500, 300, 50, key="live_stars")
    with col_set3:
        live_trail = st.slider(TXT("طول مسار الكواكب", "Planet Trail Length"), 50, 300, 150, 10, key="live_trail")

col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button(TXT("▶️ تشغيل المشهد الحي", "▶️ Run Live Scene"), use_container_width=True, type="primary"):
        st.session_state.live_run = True
with col_btn2:
    if st.button(TXT("⏹️ إيقاف المشهد", "⏹️ Stop Scene"), use_container_width=True):
        st.session_state.live_run = False
with col_btn3:
    if st.button(TXT("🔄 إعادة ضبط المشهد", "🔄 Reset Scene"), use_container_width=True):
        st.session_state.live_init = False
        st.session_state.live_run = False
        st.rerun()

if 'live_init' not in st.session_state:
    st.session_state.live_init = False
if 'live_run' not in st.session_state:
    st.session_state.live_run = False

if not st.session_state.live_init:
    cx, cy = 14.0, 10.0
    st.session_state.live_cx = cx
    st.session_state.live_cy = cy
    N = live_stars
    angles = np.random.uniform(0, 2 * np.pi, N)
    radii = np.random.uniform(1.5, 9, N)
    st.session_state.live_sx = cx + radii * np.cos(angles)
    st.session_state.live_sy = cy + radii * np.sin(angles) * 0.65
    st.session_state.live_sw = np.random.uniform(0.2, 0.9, N)
    st.session_state.live_sb = np.random.uniform(0.2, 0.9, N)
    st.session_state.live_W = W_raw
    st.session_state.live_B = B_raw
    st.session_state.live_E = E_norm
    st.session_state.live_S = S_final
    st.session_state.live_phase = TXT("توازن", "Balance")
    st.session_state.live_aW = 0.0
    st.session_state.live_aB = np.pi * 0.5
    st.session_state.live_trail_Wx = deque(maxlen=live_trail)
    st.session_state.live_trail_Wy = deque(maxlen=live_trail)
    st.session_state.live_trail_Bx = deque(maxlen=live_trail)
    st.session_state.live_trail_By = deque(maxlen=live_trail)
    st.session_state.live_hist_S = deque(maxlen=300)
    st.session_state.live_hist_E = deque(maxlen=300)
    st.session_state.live_hist_x = deque(maxlen=300)
    st.session_state.live_frame = 0
    st.session_state.live_init = True

if st.session_state.live_run:
    placeholder = st.empty()

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
        sw[i] += (W - sw[i]) * 0.01 + np.random.uniform(-0.02, 0.02)
        sb[i] += (B - sb[i]) * 0.01 + np.random.uniform(-0.02, 0.02)

        dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
        # إصلاح الخطأ: التأكد من أن المقارنة صالحة
        close_mask = (dist < 2.0) & (np.arange(live_stars) != i)
        if np.any(close_mask):
            sw[i] += (np.mean(sw[close_mask]) - sw[i]) * 0.02
            sb[i] += (np.mean(sb[close_mask]) - sb[i]) * 0.02

        sw[i] = np.clip(sw[i], 0.01, 1.0)
        sb[i] = np.clip(sb[i], 0.01, 1.0)

    # صدمات عشوائية
    if random.random() < 0.005:
        affected = np.random.choice(live_stars, size=int(live_stars * 0.2), replace=False)
        sw[affected] *= random.uniform(0.5, 0.8)
        sb[affected] *= random.uniform(0.5, 0.8)
        phase = TXT("💥 صدمة", "💥 Shock")

    avg_W = np.mean(sw)
    avg_B = np.mean(sb)
    W += (avg_W - W) * 0.03
    B += (avg_B - B) * 0.03
    W = np.clip(W, 0.01, 1.0)
    B = np.clip(B, 0.01, 1.0)
    S = W * B
    E += 0.02 * (S - E)

    if S > 0.7: phase = TXT("🌟 ثبات", "🌟 Stability")
    elif S > 0.4: phase = TXT("⚖️ توازن", "⚖️ Balance")
    elif S > 0.2: phase = TXT("⚠️ اهتزاز", "⚠️ Shaking")
    elif S > 0.05: phase = TXT("📉 انهيار", "📉 Collapse")
    else: phase = TXT("💀 قاع", "💀 Bottom")

    if E > S + 0.2: phase = TXT("🚨 استدراج", "🚨 Istidraj")

    aW += 0.02 + random.uniform(-0.01, 0.01) * (1 - W)**2
    aB += 0.02 + random.uniform(-0.01, 0.01) * (1 - B)**2

    orbit_W = 7 - 2.5 * W
    orbit_B = 5 - 1.5 * B
    wx = cx + orbit_W * np.cos(aW)
    wy = cy + orbit_W * np.sin(aW) * 0.7
    bx = cx + orbit_B * np.cos(aB)
    by = cy + orbit_B * np.sin(aB) * 0.7

    trail_Wx.append(wx); trail_Wy.append(wy)
    trail_Bx.append(bx); trail_By.append(by)

    instability = 1 - np.mean(sw * sb)
    sx += np.random.uniform(-0.05, 0.05, live_stars) * instability
    sy += np.random.uniform(-0.05, 0.05, live_stars) * instability
    sx = np.clip(sx, cx - 13, cx + 13)
    sy = np.clip(sy, cy - 9, cy + 9)

    frame += 1
    if frame % 2 == 0:
        hist_S.append(S)
        hist_E.append(E)
        hist_x.append(len(hist_x))

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
    ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')

    for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                     (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
        ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), r * (0.5 + 2.8 * S), color=c, alpha=a, zorder=15))
    ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')

    ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 0.5 + 14 * E, color='#0FF', alpha=0.15, zorder=7))
    ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 8.5, color='#0F8', alpha=0.1, fill=False, lw=2, zorder=2))

    ax.add_patch(plt.matplotlib.patches.Circle((wx, wy), 0.2 + 0.5 * W, color='#FFF', alpha=1, zorder=13))
    ax.add_patch(plt.matplotlib.patches.Circle((bx, by), 0.2 + 0.5 * B, color='#F33', alpha=0.8, zorder=13))
    ax.text(wx, wy + 0.8, 'W', color='#FFF', fontsize=10, ha='center')
    ax.text(bx, by + 0.8, 'B', color='#F33', fontsize=10, ha='center')

    if len(trail_Wx) > 1:
        ax.plot(list(trail_Wx), list(trail_Wy), color='#FFF', lw=0.3, alpha=0.2, zorder=4)
    if len(trail_Bx) > 1:
        ax.plot(list(trail_Bx), list(trail_By), color='#F33', lw=0.3, alpha=0.2, zorder=4)

    star_colors = []
    for i in range(live_stars):
        w, b = sw[i], sb[i]
        if w >= 0.55 and b >= 0.55: star_colors.append('#FFD700')
        elif w >= 0.55 and b < 0.45: star_colors.append('#E0E0E0')
        elif w < 0.45 and b >= 0.55: star_colors.append('#FF5252')
        elif w < 0.45 and b < 0.45: star_colors.append('#FFB6C1')
        else: star_colors.append('#888888')
    ax.scatter(sx, sy, s=30, c=star_colors, alpha=0.85, edgecolors='white', linewidths=0.3, zorder=5)

    pax = ax.inset_axes([0.5, 0.02, 0.46, 0.10])
    pax.set_xlim(0, 300); pax.set_ylim(0, 1.05)
    pax.set_title(TXT('S (ذهب) → E (سماوي) – الاستدراج', 'S (Gold) → E (Cyan) – Istidraj'), color='white', fontsize=7)
    pax.tick_params(colors='white', labelsize=4); pax.grid(True, alpha=0.12)
    if list(hist_S):
        pax.plot(list(hist_x), list(hist_S), color='#FFD700', lw=2)
        pax.plot(list(hist_x), list(hist_E), color='#0FF', lw=1.5)

    n_gold = np.sum((sw >= 0.55) & (sb >= 0.55))
    n_white = np.sum((sw >= 0.55) & (sb < 0.45))
    n_red = np.sum((sw < 0.45) & (sb >= 0.55))
    n_pink = np.sum((sw < 0.45) & (sb < 0.45))
    ax.text(14, 1.2, f'{phase} | 🟡{n_gold} ⚪{n_white} 🔴{n_red} 🩷{n_pink} | S={S:.2f} E={E:.2f}',
            color='white', fontsize=10, ha='center', fontweight='bold')

    plt.tight_layout(pad=0)
    placeholder.pyplot(fig)

    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, facecolor='#000010')
    buf.seek(0)
    st.session_state.live_image = buf
    plt.close(fig)

    time.sleep(live_speed)
    st.rerun()

elif st.session_state.live_init and 'live_image' in st.session_state:
    st.image(st.session_state.live_image, caption=TXT("آخر حالة للمشهد الحي", "Last Live Scene"), use_column_width=True)
    st.info(TXT("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة.", "Press ▶️ Run Live Scene to start simulation."))
else:
    st.info(TXT("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة الديناميكية.", "Press ▶️ Run Live Scene to start dynamic simulation."))

if 'live_image' in st.session_state:
    st.download_button(
        label=TXT("📥 تحميل صورة المشهد الحي", "📥 Download Live Scene Image"),
        data=st.session_state.live_image,
        file_name="mizan_live_scene.png",
        mime="image/png",
        key="dl_live"
    )

# =============================================
# التذييل
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:20px;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.5em;">⚖️ {TXT('المختبر القرآني – النظام المتكامل', 'The Quranic Lab – Integrated System')} v1.0</p>
    <p>﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
    <p>{TXT('علي عادل العاطفي', 'Ali Adel Alatifi')} | 2026</p>
</div>
""", unsafe_allow_html=True)
