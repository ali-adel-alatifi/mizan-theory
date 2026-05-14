import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import deque
import random, time
from io import BytesIO
import json
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="⚖️ الدين القيم – المنارة العالمية", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

if "lang" not in st.session_state: st.session_state.lang = "ar"
LANG = st.session_state.lang
TXT = lambda ar, en: ar if LANG == "ar" else en

# المعجم الهندسي (28 حرفاً)
LETTERS_DB = {
    'أ':1,'ل':30,'م':40,'ر':200,'س':60,'ح':8,'ط':9,'ق':100,'ك':20,'ص':90,
    'ع':70,'ي':10,'هـ':5,'ن':50,'ف':80,'و':6,'ب':2,'ظ':900,'ض':800,
    'غ':1000,'ذ':700,'خ':600,'ش':300,'ز':7,'ج':3,'ت':400,'ث':500
}

# المؤشرات الأخلاقية الأساسية (11 مؤشراً)
INDICATORS_META = [
    {"ar": "الصلاة (إقامة/تضييع)", "en": "Prayer", "letter": "ن", "val": 50},
    {"ar": "الزكاة والصدقات (إيتاء/منع)", "en": "Zakat & Charity", "letter": "ص", "val": 90},
    {"ar": "الولاء لله ورسوله والمؤمنين", "en": "Loyalty to Allah & Believers", "letter": "أ", "val": 1},
    {"ar": "تحكيم الشريعة (تحكيم/رفض)", "en": "Applying Sharia", "letter": "ل", "val": 30},
    {"ar": "العدل (عدل/ظلم)", "en": "Justice", "letter": "ق", "val": 100},
    {"ar": "الشورى (تشاور/استبداد)", "en": "Consultation", "letter": "م", "val": 40},
    {"ar": "البراءة من الطاغوت (براءة/موالاة)", "en": "Disavowal of Taghut", "letter": "هـ", "val": 5},
    {"ar": "الرحمة والعطاء – الماعون (رحمة/قسوة)", "en": "Mercy & Giving", "letter": "ح", "val": 8},
    {"ar": "الأمر بالمعروف (أمر/نهي)", "en": "Enjoining Good", "letter": "ف", "val": 80},
    {"ar": "النهي عن المنكر (نهي/أمر)", "en": "Forbidding Evil", "letter": "و", "val": 6},
    {"ar": "النزاهة ومكافحة الفساد", "en": "Integrity & Anti-Corruption", "letter": "ب", "val": 2},
]
N_IND = len(INDICATORS_META)  # 11 مؤشراً

def get_indicator_label(i):
    meta = INDICATORS_META[i]
    name = meta["ar"] if LANG == "ar" else meta["en"]
    return f"{name}  [{meta['letter']}={meta['val']}]"

# المحكمة العليا (4 بوابات)
def supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal):
    if not W_pure:
        return (0, TXT("بوابة الشرك","Shirk Gate"), TXT("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾","⚠️ Unforgivable"), "🔴")
    if B_compassion <= 0:
        return (-1, TXT("بوابة الماعون","Al-Ma'un Gate"), TXT("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ...﴾","⚠️ Collapse"), "🔴")
    if W_raw > 0 and B_disavowal <= 0:
        return (0, TXT("بوابة الإخلاص","Sincerity Gate"), TXT("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي...﴾","⚠️ Void"), "🟡")
    if W_raw > 0 and B_raw > 0:
        return (1, TXT("بوابة الوعد","Promise Gate"), TXT("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾","🟢 Stability"), "🟢")
    return None, None, None, None

def calculate_S(W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal):
    S_gate, gate_name, gate_msg, gate_color = supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal)
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0
    W = (W_raw + 1) / 2; B = (B_raw + 1) / 2; E = (E_raw + 1) / 2
    W_boost = 1 + (LETTERS_DB['أ'] + LETTERS_DB['ر'] + LETTERS_DB['س'] + LETTERS_DB['ط']) / 1000
    B_boost = 1 + (LETTERS_DB['ل'] + LETTERS_DB['ح'] + LETTERS_DB['ط']) / 1000
    S_raw = (W * W_boost) * (B * B_boost) * (1 + LETTERS_DB['م'] / 1000)
    istidraj_gap = max(0, E - S_raw)
    return min(1.0, S_raw), E, TXT("المعادلة العامة","General"), "", "⚪", istidraj_gap

def simulate_future(S, E, W_raw, B_raw, years=50):
    Sh, Eh = [S], [E]
    for _ in range(years):
        nE = Eh[-1] + 0.02 * (Sh[-1] - Eh[-1]); nB = B_raw
        if nE > Sh[-1] + 0.2: nB -= 0.03
        elif nE < Sh[-1]: nB += 0.01
        Sh.append(((W_raw+1)/2) * ((nB+1)/2) * (1 + sum(LETTERS_DB.values())/1000))
        Eh.append(nE)
    return Sh, Eh

def plot_quadrant_map(B_raw, W_raw, istidraj_gap):
    fig, ax = plt.subplots(figsize=(6,6), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e'); ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
    ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
    ax.set_xlabel(TXT("B (الكفر بالطاغوت)","B (Disavowal)"), color='white')
    ax.set_ylabel(TXT("W (الإيمان بالله)","W (Faith)"), color='white')
    ax.fill_between([0,1.2],0,1.2,color='#FFD700',alpha=0.3,label=TXT('المؤمنون','Believers'))
    ax.fill_between([-1.2,0],0,1.2,color='#FF5252',alpha=0.2,label=TXT('المغضوب عليهم','Wrath'))
    ax.fill_between([-1.2,0],-1.2,0,color='#FFB6C1',alpha=0.2,label=TXT('المنافقون','Hypocrites'))
    ax.fill_between([0,1.2],-1.2,0,color='#FFA500',alpha=0.2,label=TXT('الضالون','Astray'))
    ax.scatter(B_raw,W_raw,s=300,c='cyan',edgecolors='white',linewidth=2,zorder=10)
    ax.scatter(1,1,s=100,c='#FFD700',edgecolors='white',linewidth=2,zorder=10,marker='*')
    ax.text(1,1.15,TXT('مقام إبراهيم','Abraham'),color='#FFD700',fontsize=8,ha='center')
    if istidraj_gap>0: ax.text(0.5,-0.9,TXT(f"فجوة:{istidraj_gap:.2f}",f"Gap:{istidraj_gap:.2f}"),color='red',fontsize=9,ha='center',fontweight='bold')
    ax.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=7,loc='lower left')
    ax.tick_params(colors='white')
    return fig

print("✅ المرحلة الأولى مكتملة")

# =============================================
# المرحلة الثانية: الشريط الجانبي، المنزلقات، والحسابات
# =============================================

# تهيئة حالة الجلسة
if "slider_values" not in st.session_state:
    st.session_state.slider_values = {f"V{i}": 0.0 for i in range(N_IND)}
    st.session_state.slider_values["W_pure"] = True
    st.session_state.slider_values["E_val"] = 0.5  # قيمة افتراضية للتمكين المادي

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

with st.sidebar:
    # شعار المنصة
    st.markdown(f"""
    <div style='text-align:center;padding:8px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <p style='font-size:2em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:0;'>{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h2>
        <p style='color:#e0e0e0;font-size:10px;margin:2px 0;'>{TXT('المنارة العالمية', 'The Global Beacon')}</p>
        <p style='color:#FFD700;font-size:14px;margin:2px 0;font-weight:bold;'>S = W × B</p>
        <p style='font-size:2em;margin:0;'>⚖️</p>
    </div>
    """, unsafe_allow_html=True)

    # زر تغيير اللغة
    if st.button(TXT("🇬🇧 English", "🇸🇦 العربية"), use_container_width=True):
        st.session_state.lang = "en" if LANG == "ar" else "ar"
        st.rerun()

    st.markdown("---")

    # اختيار وضع الإدخال
    mode = st.radio(
        TXT("🎛️ اختر وضع الإدخال:", "🎛️ Select Input Mode:"),
        [TXT("🧑‍⚖️ التقدير اليدوي", "🧑‍⚖️ Manual Estimation"),
         TXT("🤖 مساعد الذكاء الاصطناعي", "🤖 AI Assistant")]
    )

    slider_vals = [0.0] * N_IND
    W_pure = True
    E_val = 0.5

    if TXT("يدوي", "Manual") in mode:
        with st.expander(TXT("🎛️ مولدات الطاقة الروحية", "🎛️ Spiritual Energy Generators"), expanded=True):
            st.caption(TXT(
                "كل حركة وسكنة في حياة الإنسان هي مولد طاقة دافعة نحو الولاية والبراءة معاً. حرّك المنزلقات لتقدير حالة الكيان. [الحرف=القيمة]",
                "Every movement is an energy generator toward loyalty and disavowal. Adjust sliders."
            ))

            for i in range(0, N_IND, 2):
                col_a, col_b = st.columns(2)
                with col_a:
                    if i < N_IND:
                        slider_vals[i] = st.slider(
                            get_indicator_label(i), -1.0, 1.0,
                            st.session_state.slider_values.get(f"V{i}", 0.0), 0.1, key=f"s_V{i}"
                        )
                with col_b:
                    if i + 1 < N_IND:
                        slider_vals[i+1] = st.slider(
                            get_indicator_label(i+1), -1.0, 1.0,
                            st.session_state.slider_values.get(f"V{i+1}", 0.0), 0.1, key=f"s_V{i+1}"
                        )

            W_pure = st.checkbox(
                TXT("الإخلاص لله (عدم الشرك)", "Sincerity to Allah (No Shirk)"),
                value=st.session_state.slider_values.get("W_pure", True)
            )

        with st.expander(TXT("🌐 التمكين المادي (E)", "🌐 Material Empowerment (E)"), expanded=False):
            E_val = st.slider(
                TXT("مستوى التمكين (اقتصاد، قوة، نفوذ)", "Empowerment Level (Economy, Power, Influence)"),
                0.0, 1.0, st.session_state.slider_values.get("E_val", 0.5), 0.05, key="s_E"
            )

        # تحديث حالة الجلسة
        for i in range(N_IND):
            st.session_state.slider_values[f"V{i}"] = slider_vals[i]
        st.session_state.slider_values["W_pure"] = W_pure
        st.session_state.slider_values["E_val"] = E_val

    else:
        st.info(TXT(
            "🤖 اكتب وصفاً للكيان ليقوم الذكاء الاصطناعي بتقدير المؤشرات.",
            "🤖 Describe the entity for AI to estimate indicators."
        ))
        ai_text = st.text_area(
            TXT("الوصف النصي:", "Description:"), height=200,
            placeholder=TXT("مثال: شاب في الثلاثين، يصلي ويصوم لكنه يعاني من شح عاطفي...", "Example: A young man who prays but struggles with compassion...")
        )
        if st.button(TXT("تحليل بالذكاء الاصطناعي", "Analyze with AI"), type="primary", use_container_width=True):
            if not ai_text.strip():
                st.warning(TXT("يرجى إدخال وصف نصي أولاً.", "Please enter a description first."))
            else:
                with st.spinner(TXT("جاري التحليل...", "Analyzing...")):
                    # هنا يستدعي الذكاء الاصطناعي (يحتاج API)
                    try:
                        import openai
                        openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
                        if not openai.api_key:
                            raise ValueError("API key not found")
                        prompt = f"""You are an expert in the Mizan theory. Analyze this entity and return JSON with these indicators (values between -1 and 1):
{[f"{i+1}. {get_indicator_label(i)}" for i in range(N_IND)]}
Also include "W_pure": true/false, "analysis": "brief analysis in Arabic", "E_val": 0.0-1.0.
Return ONLY valid JSON. Description: {ai_text}"""
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role":"system","content":"Return ONLY JSON."}, {"role":"user","content":prompt}],
                            temperature=0.3, max_tokens=500
                        )
                        content = response.choices[0].message.content.strip()
                        if content.startswith("```"): content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
                        ai_result = json.loads(content)
                        st.session_state.ai_result = ai_result
                        st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
                        if "analysis" in ai_result: st.info(ai_result["analysis"])
                    except Exception as e:
                        st.error(f"AI Error: {e}")

        if st.session_state.ai_result:
            r = st.session_state.ai_result
            vals = r.get("values", [0.0]*N_IND)[:N_IND]
            slider_vals = vals + [0.0]*(N_IND - len(vals))
            W_pure = r.get("W_pure", True)
            E_val = r.get("E_val", 0.5)
            for i in range(N_IND):
                st.session_state.slider_values[f"V{i}"] = slider_vals[i]
            st.session_state.slider_values["W_pure"] = W_pure
            st.session_state.slider_values["E_val"] = E_val

    # زر إعادة الضبط
    st.markdown("---")
    if st.button(TXT("🔄 إعادة ضبط جميع القيم", "🔄 Reset All Values"), use_container_width=True):
        for i in range(N_IND): st.session_state.slider_values[f"V{i}"] = 0.0
        st.session_state.slider_values["W_pure"] = True
        st.session_state.slider_values["E_val"] = 0.5
        st.session_state.ai_result = None
        st.rerun()

# =============================================
# المحرك الوجودي – الحسابات
# =============================================
vals = [st.session_state.slider_values.get(f"V{i}", 0.0) for i in range(N_IND)]
W_pure = st.session_state.slider_values.get("W_pure", True)
E_val = st.session_state.slider_values.get("E_val", 0.5)

# تقسيم المؤشرات: أول 6 = W (الولاء)، آخر 5 = B (البراءة)
W_vals = vals[0:6]
B_vals = vals[6:11]
W_raw = np.mean(W_vals)
B_raw = np.mean(B_vals)

# قيم البوابات
B_compassion = B_vals[1]  # الرحمة والعطاء (الماعون) – الفهرس 7
B_disavowal = B_vals[0]   # البراءة من الطاغوت – الفهرس 6

# حساب S النهائي
S_final, E_norm, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
    W_raw, B_raw, E_val, W_pure, B_compassion, B_disavowal
)

print("✅ المرحلة الثانية مكتملة: الشريط الجانبي، المنزلقات، الذكاء الاصطناعي، الحسابات")

# =============================================
# المرحلة الثالثة: العنوان، لوحة القيادة، التبويبات
# =============================================

# العنوان الرئيسي – بتنسيق خاص
st.markdown(f"""
<div style="text-align:center;padding:25px 0 15px 0;">
    <p style="font-size:2.8em;margin:0;">⚖️</p>
    <h1 style="color:#FFD700;font-size:2.8em;margin:5px 0;font-weight:900;letter-spacing:3px;">{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h1>
    <h2 style="color:#FFD700;font-size:1.3em;margin-top:0;font-weight:400;">{TXT('المنارة العالمية – بوصلة التائهين وحبل نجاة الغارقين', 'The Global Beacon – Compass for the Lost, Lifeline for the Drowning')}</h2>
    <p style="font-size:2.2em;color:#FFD700;margin:15px 0;font-weight:bold;">S = W × B</p>
    <p style="color:#CCC;font-size:1.1em;line-height:2;">﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>
    <p style="font-size:2.8em;margin:0;">⚖️</p>
</div>
""", unsafe_allow_html=True)

# =============================================
# لوحة القيادة – النتائج الرئيسية
# =============================================
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(TXT("W (الولاء)", "W (Loyalty)"), f"{W_raw:+.2f}")
col2.metric(TXT("B (البراءة)", "B (Disavowal)"), f"{B_raw:+.2f}")
col3.metric(TXT("S (الثبات)", "S (Stability)"), f"{S_final:.2f}")
col4.metric(TXT("E (التمكين)", "E (Empowerment)"), f"{E_val:.2f}")
col5.metric(TXT("فجوة الاستدراج", "Istidraj Gap"), f"{istidraj_gap:.2f}")

# عرض حكم المحكمة العليا
if gate_msg:
    st.markdown(f"### {gate_color} {gate_name}")
    if TXT("انهيار", "Collapse") in gate_msg or TXT("لا يغفر", "Unforgivable") in gate_msg:
        st.error(gate_msg)
    elif TXT("باطلة", "Void") in gate_msg:
        st.warning(gate_msg)
    else:
        st.success(gate_msg)

# إنذار الاستدراج
if istidraj_gap > 0.3:
    st.error(f"🚨 {TXT('إنذار استدراج', 'Istidraj Alert')}: E={E_val:.2f} > S={S_final:.2f} ({TXT('فجوة', 'Gap')} {istidraj_gap:.2f})")
elif istidraj_gap > 0.1:
    st.warning(f"⚡ {TXT('تحذير: فجوة استدراج متوسطة', 'Warning: Moderate Istidraj Gap')} ({istidraj_gap:.2f})")

# =============================================
# التبويبات الرئيسية
# =============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    TXT("🗺️ المختبر الجماعي", "🗺️ Collective Lab"),
    TXT("🧍 البوصلة الشخصية", "🧍 Personal Compass"),
    TXT("📐 هندسة الصراط", "📐 Path Geometry"),
    TXT("📖 المعجم الهندسي", "📖 Geometric Lexicon"),
    TXT("📜 رسالة الترحيب", "📜 Welcome Message")
])

# =============================================
# تبويب 1: المختبر الجماعي (الخريطة + المحاكي + المستشفى)
# =============================================
with tab1:
    st.subheader(TXT("المختبر الجماعي – تشخيص الأمة", "Collective Lab – Nation Diagnosis"))
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(TXT("### 🗺️ خريطة الوجود", "### 🗺️ Existence Map"))
        fig = plot_quadrant_map(B_raw, W_raw, istidraj_gap)
        st.pyplot(fig)
    with col_b:
        st.markdown(TXT("### ⏳ المحاكي الزمني", "### ⏳ Time Simulator"))
        years = st.slider(TXT("سنوات", "Years"), 10, 100, 50, 10, key="yrs_lab")
        S_hist, E_hist = simulate_future(S_final, E_val, W_raw, B_raw, years)
        fig, ax = plt.subplots(figsize=(5, 3), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.plot(S_hist, label='S', color='#FFD700', lw=2)
        ax.plot(E_hist, label='E', color='#0FF', lw=1.5, ls='--')
        ax.fill_between(range(years + 1), S_hist, E_hist, where=(np.array(E_hist) > np.array(S_hist)), color='red', alpha=0.2)
        ax.set_xlabel(TXT('سنوات', 'Years'), color='white')
        ax.set_ylabel(TXT('قيمة', 'Value'), color='white')
        ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=6)
        ax.tick_params(colors='white', labelsize=6)
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown(TXT("### 🏥 المستشفى – التشخيص والوصفة", "### 🏥 The Hospital – Diagnosis & Prescription"))
    wW = np.argmin(W_vals)
    wB = np.argmin(B_vals)
    W_L = [get_indicator_label(i) for i in range(6)]
    B_L = [get_indicator_label(i+6) for i in range(5)]
    
    if gate_name == TXT("بوابة الشرك", "Shirk Gate"):
        st.error(TXT("العلاج: تجديد التوحيد وإخلاص العبادة لله.", "Treatment: Renew Tawheed and sincerity."))
    elif gate_name == TXT("بوابة الماعون", "Al-Ma'un Gate"):
        st.error(f"🎯 أصلح '{B_L[wB]}' أولاً. بدون رحمة لا تنفع عبادة.")
    elif gate_name == TXT("بوابة الإخلاص", "Sincerity Gate"):
        st.warning(f"🎯 نقِّ '{W_L[wW]}' من شوائب الشرك.")
    elif istidraj_gap > 0.3:
        st.error(f"🎯 سد فجوة الاستدراج عبر '{W_L[wW]}' أو '{B_L[wB]}'.")
    else:
        st.info(f"🎯 للتقدم نحو مقام إبراهيم: عزز '{W_L[wW]}' و'{B_L[wB]}'.")

# =============================================
# تبويب 2: البوصلة الشخصية (28 سؤالاً)
# =============================================
with tab2:
    st.subheader(TXT("البوصلة الشخصية – اكتشف موقعك", "Personal Compass – Discover Your Position"))
    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}
    
    q_w = [
        "هل تعيش لله وحده؟", "هل تقيم الصلاة بخشوع؟", "هل تؤدي الزكاة وتتصدق؟",
        "هل تصوم رمضان وتطوعاً؟", "هل تحج أو تسعى للحج؟", "هل تحب الله ورسوله أكثر من كل شيء؟",
        "هل تصدق في أقوالك وأفعالك؟", "هل تؤدي الأمانات؟", "هل تتوكل على الله مع الأخذ بالأسباب؟",
        "هل تشكر في الرخاء وتصبر في البلاء؟", "هل تحمل هم الإسلام والمسلمين؟", "هل تفي بالعهد؟",
        "هل أنت راضٍ بما قسم الله لك؟", "هل تنصر المؤمن إذا ظُلم؟"
    ]
    q_b = [
        "هل تأمر بالمعروف؟", "هل تنهى عن المنكر؟", "هل أنت مستعد لبذل النفس والمال في سبيل الله؟",
        "هل تتبرأ من الشرك وأهله؟", "هل ترفض الكفر والإلحاد؟", "هل تكره النفاق والتلون؟",
        "هل تجاهد نفسك على ترك الكذب؟", "هل تتجنب الغش في معاملاتك؟", "هل تفي بعهودك ولا تخون؟",
        "هل ترفض الظلم بكل صوره؟", "هل تجاهد نفسك على ترك الفواحش؟", "هل تخلص عملك لله وتجتنب الرياء؟",
        "هل تسلم لله في قسمته ولا تحسد؟", "هل تحب في الله وتبغض في الله؟"
    ]
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.markdown("##### 🤍 أسئلة الولاء (W)")
        for i, q in enumerate(q_w):
            key = f"cw_{i}"
            ans = st.radio(q, [TXT("نعم (10)", "Yes (10)"), TXT("أحياناً (5)", "Sometimes (5)"), TXT("لا (0)", "No (0)")], key=key, index=None)
            if ans:
                st.session_state.compass_answers[key] = 10 if TXT("نعم", "Yes") in ans else (5 if TXT("أحياناً", "Sometimes") in ans else 0)
    with col_q2:
        st.markdown("##### ❤️ أسئلة البراءة (B)")
        for i, q in enumerate(q_b):
            key = f"cb_{i}"
            ans = st.radio(q, [TXT("نعم (10)", "Yes (10)"), TXT("أحياناً (5)", "Sometimes (5)"), TXT("لا (0)", "No (0)")], key=key, index=None)
            if ans:
                st.session_state.compass_answers[key] = 10 if TXT("نعم", "Yes") in ans else (5 if TXT("أحياناً", "Sometimes") in ans else 0)
    
    if len(st.session_state.compass_answers) == 28:
        w_score = sum(st.session_state.compass_answers[f"cw_{i}"] for i in range(14)) / 140.0
        b_score = sum(st.session_state.compass_answers[f"cb_{i}"] for i in range(14)) / 140.0
        s_score = w_score * b_score
        
        q_name, q_color = "", "#888"
        if w_score >= 0.5 and b_score >= 0.5:
            q_name, q_color = TXT("مؤمن", "Believer"), '#FFD700'
        elif w_score >= 0.5 and b_score < 0.5:
            q_name, q_color = TXT("مغضوب عليه", "Wrath"), '#FF5252'
        elif w_score < 0.5 and b_score < 0.5:
            q_name, q_color = TXT("منافق", "Hypocrite"), '#FFB6C1'
        else:
            q_name, q_color = TXT("ضال", "Astray"), '#FFA500'
        
        st.divider()
        st.subheader("📊 نتيجة البوصلة")
        c1, c2, c3 = st.columns(3)
        c1.metric("W", f"{w_score:.2f}")
        c2.metric("B", f"{b_score:.2f}")
        c3.metric("S", f"{s_score:.2f}")
        st.markdown(f"<h2 style='color:{q_color};text-align:center;'>{q_name}</h2>", unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.fill_between([0, 1], 0, 1, color='#FFD700', alpha=0.2)
        ax.fill_between([-1, 0], 0, 1, color='#FF5252', alpha=0.2)
        ax.fill_between([-1, 0], -1, 0, color='#FFB6C1', alpha=0.2)
        ax.fill_between([0, 1], -1, 0, color='#FFA500', alpha=0.2)
        ax.scatter(b_score*2-1, w_score*2-1, s=200, c='cyan', edgecolors='white', linewidth=2, zorder=10)
        ax.scatter(1, 1, s=80, c='#FFD700', marker='*', zorder=10)
        ax.text(1, 1.1, TXT('إبراهيم', 'Abraham'), color='#FFD700', fontsize=7, ha='center')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        if st.button(TXT("🔄 إعادة الاختبار", "🔄 Retake Test"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

# =============================================
# تبويب 3: هندسة الصراط
# =============================================
with tab3:
    st.subheader(TXT("هندسة الصراط – انحناء المسار", "Path Geometry – Curvature"))
    st.markdown(TXT(
        "الصراط المستقيم هو المسار الذي انحناؤه صفر (κ=0). أي انحراف عن هذا المسار هو معصية أو فتنة. الهدف هو الوصول إلى مقام إبراهيم (1,1).",
        "The straight path has zero curvature (κ=0). Any deviation is sin or trial. The goal is Abraham's Station (1,1)."
    ))
    
    if 'path_W' not in st.session_state:
        st.session_state.path_W = [W_raw]
    if 'path_B' not in st.session_state:
        st.session_state.path_B = [B_raw]
    
    if st.button(TXT("➕ سجل حالتك الحالية", "➕ Record Current State")):
        st.session_state.path_W.append(W_raw)
        st.session_state.path_B.append(B_raw)
        st.rerun()
    
    pW = st.session_state.path_W
    pB = st.session_state.path_B
    
    if len(pW) > 1:
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.plot([pB[0], 1], [pW[0], 1], '--', color='#FFD700', lw=1.5, alpha=0.6, label=TXT('الجيوديسي (κ=0)', 'Geodesic (κ=0)'))
        ax.plot(pB, pW, 'o-', color='#0FF', lw=2, markersize=4, label=TXT('مسارك', 'Your Path'))
        ax.scatter(pB[-1], pW[-1], s=100, c='cyan', edgecolors='white', linewidth=2, zorder=10)
        ax.scatter(1, 1, s=100, c='#FFD700', marker='*', zorder=10, label=TXT('مقام إبراهيم', 'Abraham'))
        ax.set_xlabel("B", color='white'); ax.set_ylabel("W", color='white')
        ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=7)
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        try:
            dW = np.gradient(pW); dB = np.gradient(pB)
            ddW = np.gradient(dW); ddB = np.gradient(dB)
            num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
            denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
            kappa = num / denom
            st.metric(TXT("انحناء المسار (κ)", "Path Curvature (κ)"), f"{kappa:.4f}")
            if kappa < 0.03: st.success(TXT("✅ أنت على الصراط المستقيم", "✅ You are on the straight path"))
            elif kappa < 0.1: st.warning(TXT("⚠️ انحراف طفيف", "⚠️ Slight deviation"))
            else: st.error(TXT("🚨 انحراف خطير", "🚨 Dangerous deviation"))
        except:
            st.info(TXT("تحتاج إلى 3 نقاط على الأقل لحساب الانحناء", "Need at least 3 points to calculate curvature"))
    else:
        st.info(TXT("سجل حالتك الحالية لتتبع مسارك نحو مقام إبراهيم.", "Record your current state to track your path."))

# =============================================
# تبويب 4: المعجم الهندسي
# =============================================
with tab4:
    st.subheader(TXT("📖 المعجم الهندسي – الحروف وقيمها", "📖 Geometric Lexicon"))
    letters_data = {
        TXT('الفئة الأولى: الذات الإلهية', 'Category 1: Divine Essence'): {'ك': 20, 'ن': 50},
        TXT('الفئة الثانية: الازدواج', 'Category 2: Duality'): {'ق': 100, 'ص': 90},
        TXT('الفئة الثالثة: التجلي الإلهي', 'Category 3: Manifestation'): {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        TXT('الفئة الرابعة: الاشتراك', 'Category 4: Bridges'): {'ع': 70, 'ي': 10, 'هـ': 5},
        TXT('الفئة الخامسة: المشغلات', 'Category 5: Operators'): {'ف': 80, 'و': 6, 'ب': 2},
        TXT('الفئة السادسة: أعمال الخلق', 'Category 6: Actions'): {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
    }
    for cat, lets in letters_data.items():
        st.markdown(f"**{cat}**")
        st.dataframe(pd.DataFrame(list(lets.items()), columns=[TXT('حرف', 'Letter'), TXT('قيمة', 'Value')]), hide_index=True)

# =============================================
# تبويب 5: رسالة الترحيب
# =============================================
with tab5:
    st.subheader(TXT("📜 رسالة الترحيب", "📜 Welcome Message"))
    st.markdown(f"""
    <div style="text-align:center;color:#CCC;line-height:2.2;font-size:1.1em;">
    > "{TXT('هل يوجد قانون واحد يحكم الذرة والحضارة؟', 'Is there a single law?')}"<br>
    > {TXT('نعم. إنه', 'Yes. It is')} <b style="color:#FFD700;">S = W × B</b>.
    <br><br>
    <b style="color:#FFD700;">﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ...﴾</b>
    <br><br>
    {TXT('هذه المنصة هي منارة للعالمين، وبوصلة للتائهين، وحبل نجاة للغارقين، ومشفى لكل ضر، ومحكمة عادلة لا تستأنف.', 
    'This platform is a beacon for the world, a compass for the lost, and a just court.')}
    <br><br>
    > "{TXT('أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.', 'O humanity, you are not in chaos.')}"
    </div>
    """, unsafe_allow_html=True)

print("✅ المرحلة الثالثة مكتملة")

    # =============================================
# المرحلة الرابعة: المشهد الحي المستقر + التذييل
# =============================================

# نضيف المشهد الحي إلى أسفل تبويب "المختبر الجماعي" (tab1)
with tab1:
    st.markdown("---")
    st.subheader(TXT("🌌 المشهد الحي – المحاكاة الكونية", "🌌 Live Scene – Cosmic Simulation"))
    st.markdown(TXT(
        "النجوم (الأفراد) تتفاعل مع قطبي الميزان. 🟡 ذهبي = متوازن، ⚪ أبيض = ولاء بلا براءة، 🔴 أحمر = براءة بلا ولاء، 🩷 وردي = لا هذا ولا ذاك.",
        "Stars (individuals) interact with the Mizan poles. Gold=Balanced, White=Loyalty only, Red=Disavowal only, Pink=Neither."
    ))

    # إعدادات المشهد الحي
    with st.expander(TXT("⚙️ إعدادات المشهد", "⚙️ Scene Settings"), expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            live_speed = st.slider(TXT("السرعة", "Speed"), 0.05, 0.3, 0.12, 0.01, key="live_speed")
        with c2:
            live_stars = st.slider(TXT("عدد النجوم", "Stars"), 30, 200, 100, 10, key="live_stars")

    # أزرار التحكم
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button(TXT("▶️ تشغيل المشهد", "▶️ Run Scene"), use_container_width=True, type="primary"):
            st.session_state.live_run = True
    with col_btn2:
        if st.button(TXT("⏹️ إيقاف المشهد", "⏹️ Stop Scene"), use_container_width=True):
            st.session_state.live_run = False
    with col_btn3:
        if st.button(TXT("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
            for k in list(st.session_state.keys()):
                if k.startswith("live_"): del st.session_state[k]
            st.rerun()

    # --- التهيئة السريعة ---
    if 'live_run' not in st.session_state:
        st.session_state.live_run = False

    if not st.session_state.get("live_init", False):
        N = min(live_stars, 200)
        st.session_state.live_sx = np.random.uniform(1, 27, N)
        st.session_state.live_sy = np.random.uniform(2, 18, N)
        st.session_state.live_sw = np.random.uniform(0.2, 0.9, N)
        st.session_state.live_sb = np.random.uniform(0.2, 0.9, N)
        st.session_state.live_W = 0.5
        st.session_state.live_B = 0.5
        st.session_state.live_S = 0.25
        st.session_state.live_E = 0.3
        st.session_state.live_frame = 0
        st.session_state.live_init = True

    # --- تشغيل المحاكاة ---
    if st.session_state.live_run:
        placeholder = st.empty()
        try:
            N = len(st.session_state.live_sx)
            cx, cy = 14.0, 10.0
            mr = 8.5

            sx = st.session_state.live_sx
            sy = st.session_state.live_sy
            sw = st.session_state.live_sw
            sb = st.session_state.live_sb
            W = st.session_state.live_W
            B = st.session_state.live_B
            S = st.session_state.live_S
            E = st.session_state.live_E
            frame = st.session_state.live_frame

            # تحديث القيم بشكل أبسط
            sw += (W - sw) * 0.02 + np.random.uniform(-0.02, 0.02, N)
            sb += (B - sb) * 0.02 + np.random.uniform(-0.02, 0.02, N)
            sw = np.clip(sw, 0.01, 1.0)
            sb = np.clip(sb, 0.01, 1.0)

            avg_W = np.mean(sw)
            avg_B = np.mean(sb)
            W += (avg_W - W) * 0.05
            B += (avg_B - B) * 0.05
            W = np.clip(W, 0.01, 1.0)
            B = np.clip(B, 0.01, 1.0)
            S = W * B
            E += 0.02 * (S - E)

            # حركة النجوم
            sx += np.random.uniform(-0.08, 0.08, N)
            sy += np.random.uniform(-0.08, 0.08, N)
            sx = np.clip(sx, cx - 13, cx + 13)
            sy = np.clip(sy, cy - 9, cy + 9)

            frame += 1

            # حفظ الحالة
            st.session_state.live_sx = sx
            st.session_state.live_sy = sy
            st.session_state.live_sw = sw
            st.session_state.live_sb = sb
            st.session_state.live_W = W
            st.session_state.live_B = B
            st.session_state.live_S = S
            st.session_state.live_E = E
            st.session_state.live_frame = frame

            # --- الرسم ---
            fig, ax = plt.subplots(figsize=(12, 8), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')

            # نواة S
            ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 0.5 + 3.0 * S, color='#FFD700', alpha=0.8, zorder=10))
            ax.text(cx, cy, 'S', color='#1a1000', fontsize=12, ha='center', va='center', fontweight='bold')

            # هالة E
            ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 0.5 + 14 * E, color='#0FF', alpha=0.15, zorder=5))

            # غشاء
            ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), mr, color='#0F8', alpha=0.1, fill=False, lw=2, zorder=3))

            # نجوم
            colors = []
            for i in range(N):
                w, b = sw[i], sb[i]
                if w >= 0.55 and b >= 0.55: colors.append('#FFD700')
                elif w >= 0.55 and b < 0.45: colors.append('#E0E0E0')
                elif w < 0.45 and b >= 0.55: colors.append('#FF5252')
                elif w < 0.45 and b < 0.45: colors.append('#FFB6C1')
                else: colors.append('#888888')
            ax.scatter(sx, sy, s=30, c=colors, alpha=0.85, edgecolors='white', linewidths=0.3, zorder=8)

            # شريط الحالة
            ng = int(np.sum((sw >= 0.55) & (sb >= 0.55)))
            nw = int(np.sum((sw >= 0.55) & (sb < 0.45)))
            nr = int(np.sum((sw < 0.45) & (sb >= 0.55)))
            npk = int(np.sum((sw < 0.45) & (sb < 0.45)))
            phase = "⚖️"
            if S > 0.7: phase = "🌟"
            elif S < 0.2: phase = "⚠️"
            if E > S + 0.2: phase = "🚨"
            ax.text(14, 1.2, f'{phase} | 🟡{ng} ⚪{nw} 🔴{nr} 🩷{npk} | S={S:.2f} E={E:.2f}', 
                    color='white', fontsize=10, ha='center', fontweight='bold')

            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            plt.close(fig)

            time.sleep(live_speed)
            st.rerun()

        except Exception as e:
            st.error(f"Simulation error: {e}")
            st.session_state.live_run = False

    elif st.session_state.get("live_init", False):
        st.info(TXT("اضغط ▶️ تشغيل المشهد لبدء المحاكاة", "Press ▶️ Run Scene to start simulation"))

# =============================================
# التذييل النهائي
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:20px;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="font-size:2em;margin:0;">⚖️</p>
    <p style="color:#FFD700;font-size:1.5em;font-weight:bold;">{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</p>
    <p style="color:#FFD700;font-size:1.2em;">S = W × B</p>
    <p>{TXT('المنارة العالمية – بوصلة التائهين وحبل نجاة الغارقين', 'The Global Beacon – Compass for the Lost, Lifeline for the Drowning')}</p>
    <p>﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
    <p>{TXT('علي عادل العاطفي', 'Ali Adel Alatifi')} | 2026</p>
    <p style="font-size:0.8em;margin-top:10px;">MIT License | {TXT('المنصة الذهبية v3.0', 'Golden Platform v3.0')}</p>
    <p style="font-size:2em;margin:0;">⚖️</p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الرابعة مكتملة: المشهد الحي المستقر + التذييل")
print("✅✅✅ تم بناء المنصة الذهبية – الدين القيم – المنارة العالمية بنجاح!")
