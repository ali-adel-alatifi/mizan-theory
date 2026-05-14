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

# =============================================
# الإعدادات العامة
# =============================================
st.set_page_config(
    page_title="⚖️ الدين القيم – قانون التوازن الكوني",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# النظام اللغوي المتعدد
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

LANG = st.session_state.lang

def TXT(ar_text, en_text):
    """ترجمة فورية بين العربية والإنجليزية"""
    return ar_text if LANG == "ar" else en_text

# =============================================
# الثوابت الوجودية – المعجم الهندسي (28 حرفاً)
# =============================================
LETTERS_DB = {
    'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60,
    'ح': 8, 'ط': 9, 'ق': 100, 'ك': 20, 'ص': 90,
    'ع': 70, 'ي': 10, 'هـ': 5, 'ن': 50, 'ف': 80,
    'و': 6, 'ب': 2, 'ظ': 900, 'ض': 800, 'غ': 1000,
    'ذ': 700, 'خ': 600, 'ش': 300, 'ز': 7, 'ج': 3,
    'ت': 400, 'ث': 500
}

# =============================================
# المؤشرات الوجودية – مجموعة واحدة متكاملة
# =============================================
INDICATORS_AR = [
    "الصلاة (إقامة/تضييع)",
    "الزكاة والصدقات (إيتاء/منع)",
    "الولاء لله ورسوله والمؤمنين (موالاة/معاداة)",
    "تحكيم الشريعة (تحكيم/رفض)",
    "العدل (عدل/ظلم)",
    "الشورى (تشاور/استبداد)",
    "البراءة من الطاغوت (براءة/موالاة)",
    "الرحمة والعطاء – الماعون (رحمة/قسوة)",
    "الأمر بالمعروف (أمر/نهي عن المعروف)",
    "النهي عن المنكر (نهي/أمر بالمنكر)",
    "النزاهة ومكافحة الفساد (نزاهة/فساد)",
    "السيادة والاستقلال (استقلال/تبعية)",
    "الاكتفاء الذاتي (اكتفاء/اعتماد)",
    "الإنتاج الزراعي (إنتاج/إهمال)",
    "الإنتاج الصناعي (صناعة/تخلف)",
    "القوة العسكرية (قوة/ضعف)",
    "التصميم والهندسة – ك (إبداع/جمود)",
    "التصنيع والتشكيل – هـ (إتقان/فوضى)",
    "التطوير والتحسين – ي (تجديد/ركود)",
    "البحث والتطوير – ع (علم/جهل)",
    "الجودة والاستدامة – ص (ثبات/انهيار)",
]

INDICATORS_EN = [
    "Prayer (Establish/Neglect)",
    "Zakat & Charity (Give/Withhold)",
    "Loyalty to Allah, Messenger & Believers (Ally/Oppose)",
    "Applying Sharia (Apply/Reject)",
    "Justice (Just/Unjust)",
    "Consultation - Shura (Consult/Tyranny)",
    "Disavowal of Taghut (Disavow/Ally)",
    "Mercy & Giving - Al-Ma'un (Merciful/Harsh)",
    "Enjoining Good (Enjoin/Forbid Good)",
    "Forbidding Evil (Forbid/Enjoin Evil)",
    "Integrity & Anti-Corruption (Honest/Corrupt)",
    "Sovereignty & Independence (Independent/Dependent)",
    "Self-Sufficiency (Sufficient/Needy)",
    "Agricultural Production (Produce/Neglect)",
    "Industrial Production (Industry/Backward)",
    "Military Power (Strong/Weak)",
    "Design & Engineering - K (Creative/Stagnant)",
    "Manufacturing & Forming - H (Quality/Chaos)",
    "Development & Improvement - Y (Renew/Stagnate)",
    "Research & Development - A (Knowledge/Ignorance)",
    "Quality & Sustainability - S (Stable/Collapse)",
]

def get_indicators():
    """إرجاع المؤشرات حسب اللغة المختارة"""
    return INDICATORS_AR if LANG == "ar" else INDICATORS_EN

# =============================================
# المحكمة العليا – أربع بوابات منطقية قرآنية
# =============================================
def supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal):
    """
    المحكمة العليا لنظام الميزان.
    الترتيب: الشرك → الماعون → الإخلاص → الوعد
    """
    # البوابة 0: بوابة الشرك (النساء: 48)
    if not W_pure:
        return (0,
                TXT("بوابة الشرك", "Shirk Gate"),
                TXT("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾ – كل عمل محبط",
                    "⚠️ Unforgivable: 'Allah does not forgive association with Him'"),
                "🔴")

    # البوابة 1: بوابة الماعون (الماعون: 7)
    if B_compassion <= 0:
        return (-1,
                TXT("بوابة الماعون", "Al-Ma'un Gate"),
                TXT("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾",
                    "⚠️ Collapse: 'So woe to those who pray... who withhold simple assistance'"),
                "🔴")

    # البوابة 2: بوابة الإخلاص (النور: 55)
    if W_raw > 0 and B_disavowal <= 0:
        return (0,
                TXT("بوابة الإخلاص", "Sincerity Gate"),
                TXT("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي وَلَا يُشْرِكُونَ بِي شَيْئًا﴾",
                    "⚠️ Void worship: 'They worship Me, not associating anything with Me'"),
                "🟡")

    # البوابة 3: بوابة الوعد (الانشقاق: 25، التين: 6)
    if W_raw > 0 and B_raw > 0:
        return (1,
                TXT("بوابة الوعد", "Promise Gate"),
                TXT("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾",
                    "🟢 Stability: 'For them is a reward uninterrupted'"),
                "🟢")

    return None, None, None, None

# =============================================
# دالة حساب S – المعادلة الكاملة
# =============================================
def calculate_S(W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal):
    """حساب الثبات S باستخدام المعادلة الكاملة"""
    # تحقق من المحكمة العليا أولاً
    S_gate, gate_name, gate_msg, gate_color = supreme_court(
        W_raw, B_raw, W_pure, B_compassion, B_disavowal
    )
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0

    # المعادلة العامة
    W = (W_raw + 1) / 2
    B = (B_raw + 1) / 2
    E = (E_raw + 1) / 2

    # تضخيم الحروف
    W_boost = 1 + (LETTERS_DB['أ'] + LETTERS_DB['ر'] + LETTERS_DB['س'] + LETTERS_DB['ط']) / 1000
    B_boost = 1 + (LETTERS_DB['ل'] + LETTERS_DB['ح'] + LETTERS_DB['ط']) / 1000
    W_eff = W * W_boost
    B_eff = B * B_boost
    S_raw = W_eff * B_eff * (1 + LETTERS_DB['م'] / 1000)

    istidraj_gap = max(0, E - S_raw)
    return min(1.0, S_raw), E, TXT("المعادلة العامة", "General Equation"), "", "⚪", istidraj_gap

# =============================================
# دالة المحاكاة الزمنية
# =============================================
def simulate_future(S, E, W_raw, B_raw, years=50):
    """محاكاة زمنية للمستقبل"""
    Sh, Eh = [S], [E]
    for _ in range(years):
        nE = Eh[-1] + 0.02 * (Sh[-1] - Eh[-1])
        nB = B_raw
        if nE > Sh[-1] + 0.2:
            nB -= 0.03
        elif nE < Sh[-1]:
            nB += 0.01
        nS = ((W_raw + 1) / 2) * ((nB + 1) / 2) * (1 + sum(LETTERS_DB.values()) / 1000)
        Sh.append(nS)
        Eh.append(nE)
    return Sh, Eh

# =============================================
# دالة الذكاء الاصطناعي
# =============================================
def call_ai_api(user_text):
    """استدعاء GPT-4 لتحليل النص وإرجاع تقديرات المؤشرات"""
    try:
        import openai
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        indicators_list = get_indicators()
        prompt = f"""أنت محلل خبير في نظرية الميزان (S = W × B). اقرأ وصف الكيان وأعد تقديرات رقمية بصيغة JSON فقط.

لديك 21 مؤشرًا، كل منها بين -1 (سلبي) و +1 (إيجابي):
{chr(10).join([f"{i+1}. {ind}" for i, ind in enumerate(indicators_list)])}

W_pure: true/false (هل الولاء خالص لله؟)
analysis: تحليل موجز بالعربية

أعد النتيجة بصيغة JSON فقط، بدون أي نص إضافي.
مثال: {{"values":[0.5,0.4,0.7,0.3,0.6,0.2,0.6,0.5,0.4,0.3,0.4,0.5,0.4,0.6,0.4,0.7,0.3,0.4,0.5,0.2,0.4],"W_pure":true,"analysis":"تحليل موجز"}}

الوصف: {user_text}"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت محلل خبير. ترد بصيغة JSON فقط بدون أي نص إضافي."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600
        )

        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        content = content.strip()
        return json.loads(content)

    except Exception as e:
        st.error(TXT(f"خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}",
                     f"AI connection error: {str(e)}"))
        return None

# =============================================
# دالة رسم الخريطة الرباعية
# =============================================
def plot_quadrant_map(B_raw, W_raw, istidraj_gap):
    """رسم خريطة فضاء القيم الرباعية"""
    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='grey', lw=0.5)
    ax.axvline(0, color='grey', lw=0.5)
    ax.set_xlabel(TXT("B (الكفر بالطاغوت)", "B (Disavowal of Taghut)"), color='white')
    ax.set_ylabel(TXT("W (الإيمان بالله)", "W (Faith in Allah)"), color='white')

    # الأرباع
    ax.fill_between([0, 1.2], 0, 1.2, color='#FFD700', alpha=0.3,
                    label=TXT('المؤمنون (الثبات)', 'Believers (Stability)'))
    ax.fill_between([-1.2, 0], 0, 1.2, color='#FF5252', alpha=0.2,
                    label=TXT('المغضوب عليهم', 'Those with Wrath'))
    ax.fill_between([-1.2, 0], -1.2, 0, color='#FFB6C1', alpha=0.2,
                    label=TXT('المنافقون', 'Hypocrites'))
    ax.fill_between([0, 1.2], -1.2, 0, color='#FFA500', alpha=0.2,
                    label=TXT('الضالون', 'Those Astray'))

    # نقطة الكيان
    ax.scatter(B_raw, W_raw, s=400, c='cyan', edgecolors='white', linewidth=3, zorder=10)

    # مقام إبراهيم
    ax.scatter(1, 1, s=150, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, marker='*')
    ax.text(1, 1.15, TXT('مقام إبراهيم', 'Station of Abraham'),
            color='#FFD700', fontsize=9, ha='center', fontweight='bold')

    # فجوة الاستدراج
    if istidraj_gap > 0:
        ax.text(0.5, -0.9,
                TXT(f"فجوة استدراج: {istidraj_gap:.2f}", f"Istidraj Gap: {istidraj_gap:.2f}"),
                color='red', fontsize=10, ha='center', fontweight='bold')

    ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower left')
    ax.tick_params(colors='white')
    return fig

print("✅ المرحلة الأولى مكتملة: الأساسيات، الثوابت، المؤشرات، المحكمة العليا، دوال الحساب، الذكاء الاصطناعي")

# =============================================
# المرحلة الثانية: الشريط الجانبي والمنزلقات الموحدة
# =============================================

# تهيئة حالة الجلسة للقيم الافتراضية
if "slider_values" not in st.session_state:
    st.session_state.slider_values = {f"V{i}": 0.0 for i in range(21)}
    st.session_state.slider_values["W_pure"] = True

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

with st.sidebar:
    # شعار المنصة
    st.markdown(f"""
    <div style='text-align:center;padding:10px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <h2 style='color:#FFD700;margin:0;'>⚖️ {TXT('الدين القيم', 'Al-Deen Al-Qayyim')} ⚖️</h2>
        <p style='color:#e0e0e0;font-size:12px;margin:5px 0;'>{TXT('قانون التوازن الكوني', 'The Cosmic Law of Balance')}</p>
        <p style='color:#FFD700;font-size:14px;margin:3px 0;'>S = W × B</p>
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
        [TXT("🧑‍⚖️ التقدير اليدوي (المنزلقات)", "🧑‍⚖️ Manual Estimation (Sliders)"),
         TXT("🤖 مساعد الذكاء الاصطناعي", "🤖 AI Assistant")]
    )

    # الحصول على قائمة المؤشرات
    indicators = get_indicators()
    N_IND = len(indicators)  # 21 مؤشرًا

    # متغيرات المنزلقات
    slider_vals = [0.0] * N_IND
    W_pure = True

    if TXT("يدوي", "Manual") in mode:
        # جميع المؤشرات في مجموعة واحدة
        with st.expander(TXT("🎛️ مولدات الطاقة الوجودية", "🎛️ Existential Energy Generators"), expanded=True):
            st.caption(TXT(
                "كل حركة وسكنة في حياة الإنسان هي مولد طاقة دافعة نحو الولاية والبراءة معًا. حرّك المنزلقات لتقدير حالة الكيان.",
                "Every movement and stillness in human life is an energy generator pushing toward loyalty and disavowal together. Adjust the sliders to estimate the entity's state."
            ))

            # عرض المنزلقات في عمودين لتوفير المساحة
            for i in range(0, N_IND, 2):
                col_a, col_b = st.columns(2)
                with col_a:
                    if i < N_IND:
                        slider_vals[i] = st.slider(
                            indicators[i],
                            -1.0, 1.0,
                            st.session_state.slider_values.get(f"V{i}", 0.0),
                            0.1,
                            key=f"s_V{i}"
                        )
                with col_b:
                    if i + 1 < N_IND:
                        slider_vals[i+1] = st.slider(
                            indicators[i+1],
                            -1.0, 1.0,
                            st.session_state.slider_values.get(f"V{i+1}", 0.0),
                            0.1,
                            key=f"s_V{i+1}"
                        )

            # مربع الإخلاص
            W_pure = st.checkbox(
                TXT("الإخلاص لله (عدم الشرك)", "Sincerity to Allah (No Shirk)"),
                value=st.session_state.slider_values.get("W_pure", True),
                help=TXT("هل الولاء خالص لله وحده؟", "Is loyalty purely for Allah alone?")
            )

        # تحديث حالة الجلسة
        for i in range(N_IND):
            st.session_state.slider_values[f"V{i}"] = slider_vals[i]
        st.session_state.slider_values["W_pure"] = W_pure

    else:
        # وضع الذكاء الاصطناعي
        st.info(TXT(
            "🤖 اكتب وصفًا للكيان (دولة، مجتمع، فرد) ليقوم الذكاء الاصطناعي بتقدير المؤشرات.",
            "🤖 Describe the entity (country, community, individual) for AI to estimate indicators."
        ))

        ai_text = st.text_area(
            TXT("الوصف النصي:", "Description:"),
            height=200,
            placeholder=TXT(
                "مثال: دولة إسلامية ذات أغلبية شابة، تعاني من فساد إداري لكنها تملك جيشًا قويًا واقتصادًا زراعيًا...",
                "Example: An Islamic country with a young majority, suffering from administrative corruption but with a strong military and agricultural economy..."
            )
        )

        if st.button(TXT("تحليل بالذكاء الاصطناعي", "Analyze with AI"), type="primary", use_container_width=True):
            if not ai_text.strip():
                st.warning(TXT("يرجى إدخال وصف نصي أولاً.", "Please enter a description first."))
            else:
                with st.spinner(TXT("جاري التحليل بالذكاء الاصطناعي...", "Analyzing with AI...")):
                    ai_result = call_ai_api(ai_text)
                    if ai_result:
                        st.session_state.ai_result = ai_result
                        st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
                        if "analysis" in ai_result:
                            st.info(ai_result["analysis"])

        # إذا كان هناك نتيجة سابقة من الذكاء الاصطناعي، استخدمها
        if st.session_state.ai_result is not None:
            r = st.session_state.ai_result
            vals = r.get("values", [0.0] * N_IND)
            # التأكد من الطول الصحيح
            if len(vals) >= N_IND:
                slider_vals = vals[:N_IND]
            else:
                slider_vals = vals + [0.0] * (N_IND - len(vals))
            W_pure = r.get("W_pure", True)
            # تحديث حالة الجلسة
            for i in range(N_IND):
                st.session_state.slider_values[f"V{i}"] = slider_vals[i]
            st.session_state.slider_values["W_pure"] = W_pure

    # زر إعادة الضبط
    st.markdown("---")
    if st.button(TXT("🔄 إعادة ضبط جميع القيم", "🔄 Reset All Values"), use_container_width=True):
        for i in range(N_IND):
            st.session_state.slider_values[f"V{i}"] = 0.0
        st.session_state.slider_values["W_pure"] = True
        st.session_state.ai_result = None
        st.rerun()

# =============================================
# المحرك الوجودي – الحساب
# =============================================

# استخراج القيم من المنزلقات أو الذكاء الاصطناعي
vals = [st.session_state.slider_values.get(f"V{i}", 0.0) for i in range(N_IND)]
W_pure = st.session_state.slider_values.get("W_pure", True)

# توزيع المؤشرات:
# المؤشرات 0-5: الولاء (W)
# المؤشرات 6-10: البراءة (B)
# المؤشرات 11-15: التمكين (E)
# المؤشرات 16-20: تفصيل الصناعة (I)

W_vals = vals[0:6]   # 6 مؤشرات
B_vals = vals[6:11]  # 5 مؤشرات
E_vals = vals[11:16] # 5 مؤشرات
I_vals = vals[16:21] # 5 مؤشرات

# حساب المتوسطات الخام
W_raw = np.mean(W_vals)
B_raw = np.mean(B_vals)

# حساب E المرجح بقيم الحروف
E_LETTERS = ['م', 'ق', 'ك', 'ص', 'ر']
E_weights_list = [LETTERS_DB[l] for l in E_LETTERS]
E_raw = np.average(E_vals, weights=E_weights_list)

# حساب مؤشر الصناعة المرجح من تفصيل الكهيعص
IND_LETTERS = ['ك', 'هـ', 'ي', 'ع', 'ص']
i_weights = [LETTERS_DB[l] for l in IND_LETTERS]
I_weighted = np.average(I_vals, weights=i_weights)

# نستخدم مؤشر الصناعة المفصل لاستبدال المؤشر الصناعي في E (المؤشر الرابع، الفهرس 3)
E_vals_updated = E_vals.copy()
E_vals_updated[3] = I_weighted

# إعادة حساب E_raw مع المؤشر الصناعي المفصل
E_raw = np.average(E_vals_updated, weights=E_weights_list)

# استخراج قيم البوابات
B_compassion = B_vals[1]  # الرحمة والعطاء (الماعون) – المؤشر الثاني في B
B_disavowal = B_vals[0]   # البراءة من الطاغوت – المؤشر الأول في B

# حساب S والبوابات
S_final, E_norm, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
    W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal
)

print("✅ المرحلة الثانية مكتملة: الشريط الجانبي، المنزلقات الموحدة، الذكاء الاصطناعي، الحسابات")

# =============================================
# المرحلة الثالثة: العنوان، لوحة القيادة، التبويبات
# =============================================

# العنوان الرئيسي – الدين القيم بين أيقونتي الميزان
st.markdown(f"""
<div style="text-align:center;padding:20px 0 10px 0;">
    <p style="font-size:3em;margin:0;">⚖️</p>
    <h1 style="color:#FFD700;font-size:2.5em;margin:0 0 10px 0;">{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h1>
    <h2 style="color:#FFD700;font-size:1.3em;margin-top:0;">{TXT('قانون التوازن الكوني', 'The Cosmic Law of Balance')}</h2>
    <p style="font-size:2.5em;color:#FFD700;margin:10px 0;">S = W × B</p>
    <p style="color:#CCC;font-size:1.1em;">﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>
    <p style="font-size:3em;margin:0;">⚖️</p>
</div>
""", unsafe_allow_html=True)

# =============================================
# لوحة القيادة – النتائج الرئيسية
# =============================================
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(TXT("W (الولاء)", "W (Loyalty)"), f"{W_raw:+.2f}")
col2.metric(TXT("B (البراءة)", "B (Disavowal)"), f"{B_raw:+.2f}")
col3.metric(TXT("S (الثبات)", "S (Stability)"), f"{S_final:.2f}")
col4.metric(TXT("E (التمكين)", "E (Empowerment)"), f"{E_norm:.2f}")
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
    st.error(f"🚨 {TXT('إنذار استدراج', 'Istidraj Alert')}: E={E_norm:.2f} > S={S_final:.2f} ({TXT('فجوة', 'Gap')} {istidraj_gap:.2f})")
elif istidraj_gap > 0.1:
    st.warning(f"⚡ {TXT('تحذير: فجوة استدراج متوسطة', 'Warning: Moderate Istidraj Gap')} ({istidraj_gap:.2f})")

# =============================================
# التبويبات الرئيسية
# =============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    TXT("🗺️ خريطة الوجود", "🗺️ Existence Map"),
    TXT("⏳ المحاكي الزمني", "⏳ Time Simulator"),
    TXT("🏥 المستشفى", "🏥 The Hospital"),
    TXT("📖 المعجم الهندسي", "📖 Geometric Lexicon"),
    TXT("📜 رسالة الترحيب", "📜 Welcome Message"),
    TXT("🌌 المشهد الحي", "🌌 Live Scene")
])

# =============================================
# تبويب 1: خريطة الوجود
# =============================================
with tab1:
    st.subheader(TXT("فضاء القيم – موقع الكيان", "Value Space – Entity Position"))
    st.markdown(TXT(
        "الخريطة الرباعية تُظهر موقعك في فضاء القيم بناءً على قيمتي الولاء (W) والبراءة (B). النقطة الزرقاء هي موقع الكيان الحالي.",
        "The quadrant map shows your position in the Value Space based on Loyalty (W) and Disavowal (B). The blue point is the current entity position."
    ))
    
    fig = plot_quadrant_map(B_raw, W_raw, istidraj_gap)
    st.pyplot(fig)
    
    # إحصائيات إضافية
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        dist_to_abraham = np.sqrt((1 - (W_raw + 1) / 2)**2 + (1 - (B_raw + 1) / 2)**2)
        st.metric(TXT("المسافة إلى مقام إبراهيم", "Distance to Abraham's Station"), f"{dist_to_abraham:.3f}")
    with col_b:
        if W_raw >= 0 and B_raw >= 0:
            quadrant_name = TXT("الربع الأول (المؤمنون)", "Q1 (Believers)")
        elif W_raw >= 0 and B_raw < 0:
            quadrant_name = TXT("الربع الثاني (المغضوب عليهم)", "Q2 (Those with Wrath)")
        elif W_raw < 0 and B_raw < 0:
            quadrant_name = TXT("الربع الثالث (المنافقون)", "Q3 (Hypocrites)")
        else:
            quadrant_name = TXT("الربع الرابع (الضالون)", "Q4 (Those Astray)")
        st.metric(TXT("الربع الحالي", "Current Quadrant"), quadrant_name)
    with col_c:
        st.metric(TXT("نوع البوابة", "Gate Type"), gate_name if gate_name else TXT("لا يوجد", "None"))

# =============================================
# تبويب 2: المحاكي الزمني
# =============================================
with tab2:
    st.subheader(TXT("المحاكي الزمني – حتمية المصير", "Time Simulator – Inevitable Fate"))
    st.markdown(TXT(
        "هذه المحاكاة تظهر كيف ستتغير قيم S وE عبر الزمن بناءً على القيم الحالية. منطقة الاستدراج تظهر عندما يتجاوز التمكين (E) الثبات (S).",
        "This simulation shows how S and E values will change over time based on current values. The Istidraj zone appears when Empowerment (E) exceeds Stability (S)."
    ))
    
    years = st.slider(TXT("عدد سنوات المحاكاة:", "Simulation Years:"), 10, 100, 50, 10)
    S_hist, E_hist = simulate_future(S_final, E_norm, W_raw, B_raw, years)
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.plot(S_hist, label=TXT('S (الثبات)', 'S (Stability)'), color='#FFD700', linewidth=2.5)
    ax.plot(E_hist, label=TXT('E (التمكين)', 'E (Empowerment)'), color='#00FFFF', linewidth=2, linestyle='--')
    ax.fill_between(range(years + 1), S_hist, E_hist, 
                     where=(np.array(E_hist) > np.array(S_hist)), 
                     color='red', alpha=0.25, label=TXT('منطقة الاستدراج', 'Istidraj Zone'))
    ax.axhline(y=0, color='red', linestyle=':')
    ax.set_xlabel(TXT('السنوات', 'Years'), color='white')
    ax.set_ylabel(TXT('القيمة', 'Value'), color='white')
    ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2)
    st.pyplot(fig)
    
    # ملخص المحاكاة
    st.markdown(f"""
    **{TXT('ملخص المحاكاة:', 'Simulation Summary:')}**
    - S {TXT('النهائي بعد', 'final after')} {years} {TXT('سنة:', 'years:')} **{S_hist[-1]:.3f}**
    - E {TXT('النهائي بعد', 'final after')} {years} {TXT('سنة:', 'years:')} **{E_hist[-1]:.3f}**
    - {TXT('الفجوة النهائية:', 'Final Gap:')} **{max(0, E_hist[-1] - S_hist[-1]):.3f}**
    """)

# =============================================
# تبويب 3: المستشفى – التشخيص والوصفة العلاجية
# =============================================
with tab3:
    st.subheader(TXT("🏥 المستشفى – التشخيص والوصفة العلاجية", "🏥 The Hospital – Diagnosis & Prescription"))
    
    # أضعف المؤشرات
    all_vals = vals.copy()
    wW = np.argmin(W_vals)
    wB = np.argmin(B_vals)
    wE_idx = np.argmin(E_vals_updated)
    wAll = np.argmin(all_vals)
    
    inds = get_indicators()
    W_L = inds[0:6]
    B_L = inds[6:11]
    E_L = inds[11:16]
    I_L = inds[16:21]
    
    # التشخيص
    st.markdown(TXT("### 🔍 التشخيص", "### 🔍 Diagnosis"))
    if gate_name == TXT("بوابة الشرك", "Shirk Gate"):
        st.error(TXT(
            "العلاج: تجديد التوحيد وإخلاص العبادة لله وحده. لا ينفع مع الشرك أي عمل.",
            "Treatment: Renew Tawheed and sincerity to Allah alone. No deed benefits with shirk."
        ))
    elif gate_name == TXT("بوابة الماعون", "Al-Ma'un Gate"):
        st.error(TXT(
            f"الأولوية القصوى: إصلاح مؤشر '{B_L[wB]}'. بدون رحمة وعطاء، لا تنفع أي عبادة.",
            f"Top priority: Fix the '{B_L[wB]}' indicator. Without mercy and giving, no worship benefits."
        ))
    elif gate_name == TXT("بوابة الإخلاص", "Sincerity Gate"):
        st.warning(TXT(
            f"الأولوية: تنقية '{W_L[wW]}' من شوائب الشرك والرياء، وتصحيح '{B_L[wB]}'.",
            f"Priority: Purify '{W_L[wW]}' from shirk and hypocrisy, and correct '{B_L[wB]}'."
        ))
    elif istidraj_gap > 0.3:
        st.error(TXT(
            f"الأولوية: سد فجوة الاستدراج ({istidraj_gap:.2f}) عبر رفع '{inds[wAll]}'.",
            f"Priority: Close the Istidraj gap ({istidraj_gap:.2f}) by raising '{inds[wAll]}'."
        ))
    else:
        st.info(TXT(
            f"للتقدم نحو مقام إبراهيم: عزز '{inds[wAll]}'.",
            f"To advance to the Station of Abraham: strengthen '{inds[wAll]}'."
        ))
    
    # جدول المؤشرات
    st.markdown(TXT("### 📊 تفصيل المؤشرات", "### 📊 Indicator Details"))
    
    df_all = pd.DataFrame({
        TXT('المؤشر', 'Indicator'): inds,
        TXT('القيمة', 'Value'): all_vals,
        TXT('المجموعة', 'Group'): [
            TXT('ولاء', 'Loyalty')]*6 + 
            [TXT('براءة', 'Disavowal')]*5 + 
            [TXT('تمكين', 'Empowerment')]*5 + 
            [TXT('صناعة', 'Industry')]*5
    })
    
    st.dataframe(
        df_all.style.format({TXT('القيمة', 'Value'): '{:+.2f}'})
        .background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'),
        hide_index=True,
        use_container_width=True
    )

# =============================================
# تبويب 4: المعجم الهندسي
# =============================================
with tab4:
    st.subheader(TXT("📖 المعجم الهندسي – الحروف وقيمها", "📖 Geometric Lexicon – Letters & Values"))
    st.markdown(TXT(
        "هذا المعجم يربط كل حرف من الحروف العربية بقيمته العددية (حساب الجمل) ودوره الوجودي في معادلة الميزان. التصنيف مبني على الفئات الست التي تم استنباطها من القرآن.",
        "This lexicon links each Arabic letter to its numerical value (Abjad calculation) and its existential role in the Mizan equation. The classification is based on six categories derived from the Quran."
    ))
    
    letters_data = {
        TXT('الفئة الأولى: الذات الإلهية (المصدر)', 'Category 1: Divine Essence (Source)'): 
            {'ك': 20, 'ن': 50},
        TXT('الفئة الثانية: الازدواج', 'Category 2: Duality'): 
            {'ق': 100, 'ص': 90},
        TXT('الفئة الثالثة: التجلي الإلهي', 'Category 3: Divine Manifestation'): 
            {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        TXT('الفئة الرابعة: الاشتراك (الجسور)', 'Category 4: Connection (Bridges)'): 
            {'ع': 70, 'ي': 10, 'هـ': 5},
        TXT('الفئة الخامسة: المشغلات', 'Category 5: Operators'): 
            {'ف': 80, 'و': 6, 'ب': 2},
        TXT('الفئة السادسة: أعمال الخلق', 'Category 6: Actions of Creation'): 
            {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 
             'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
    }
    
    for category, letters in letters_data.items():
        st.markdown(f"**{category}**")
        df = pd.DataFrame(list(letters.items()), columns=[TXT('الحرف', 'Letter'), TXT('القيمة', 'Value')])
        st.dataframe(df, hide_index=True, use_container_width=True)

# =============================================
# تبويب 5: رسالة الترحيب
# =============================================
with tab5:
    st.subheader(TXT("📜 رسالة الترحيب", "📜 Welcome Message"))
    st.markdown(f"""
    <div style="text-align:center;color:#CCC;line-height:2.2;font-size:1.1em;">
    
    > "{TXT('هل يوجد قانون واحد يحكم الذرة والحضارة؟', 'Is there a single law governing the atom and civilization?')}"<br>
    > {TXT('هذا هو نموذج الميزان الذي يثبت أن', 'This is the Mizan Model that proves that')} <b style="color:#FFD700;">S = W × B</b>
    
    <br><br>
    
    **{TXT('الدين القيم', 'Al-Deen Al-Qayyim')}** = {TXT('قانون السببية الكوني', 'The cosmic law of causality')}.<br>
    **{TXT('الإسلام الحنيف', 'Al-Islam Al-Hanif')}** = {TXT('الاستجابة المثلى لهذا القانون', 'The optimal response to this law')}.<br>
    **{TXT('الميزان', 'Al-Mizan')}** = {TXT('المعادلة التي تحكم كل شيء', 'The equation that governs everything')}: <b style="color:#FFD700;">S = W × B</b>.
    
    <br><br>
    
    <b style="color:#FFD700;">﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ وَلَهُ أَسْلَمَ مَن فِي السَّمَاوَاتِ وَالْأَرْضِ طَوْعًا وَكَرْهًا﴾</b>
    
    <br><br>
    
    <b style="color:#FFD700;">﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ذَٰلِكَ الدِّينُ الْقَيِّمُ﴾</b>
    
    <br><br>
    
    > "{TXT('أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.', 'O humanity, you are not in chaos. There is a law. There is a system. There is a balance.')}"<br>
    > "{TXT('إنها معادلة. إنها', 'It is an equation. It is')} <b style="color:#FFD700;">S = W × B</b>."
    
    </div>
    """, unsafe_allow_html=True)

print("✅ المرحلة الثالثة مكتملة: العنوان، لوحة القيادة، خريطة الوجود، المحاكي الزمني، المستشفى، المعجم الهندسي، رسالة الترحيب")

    # =============================================
# المرحلة الرابعة: المشهد الحي والتذييل
# =============================================

with tab6:
    st.subheader(TXT("🌌 المشهد الحي – المحاكاة الكونية", "🌌 Live Scene – Cosmic Simulation"))
    st.markdown(TXT(
        "هذا المشهد الحي يحاكي تفاعل النجوم (الأفراد) مع قطبي الميزان W وB. النجوم الذهبية تمثل المؤمنين المتوازنين، والبيضاء تمثل من لديهم ولاء بلا براءة، والحمراء تمثل براءة بلا ولاء، والوردية تمثل من لا هذا ولا ذاك.",
        "This live scene simulates the interaction of stars (individuals) with the poles of the Mizan W and B. Golden stars represent balanced believers, white stars represent loyalty without disavowal, red stars represent disavowal without loyalty, and pink stars represent neither."
    ))

    # إعدادات المشهد الحي
    with st.expander(TXT("⚙️ إعدادات المشهد الحي", "⚙️ Live Scene Settings"), expanded=False):
        col_set1, col_set2, col_set3, col_set4 = st.columns(4)
        with col_set1:
            live_speed = st.slider(TXT("سرعة المحاكاة", "Simulation Speed"), 0.01, 0.2, 0.08, 0.01, key="live_speed")
        with col_set2:
            live_stars = st.slider(TXT("عدد النجوم", "Number of Stars"), 100, 500, 300, 50, key="live_stars")
        with col_set3:
            live_trail = st.slider(TXT("طول مسار الكواكب", "Planet Trail Length"), 50, 300, 150, 10, key="live_trail")
        with col_set4:
            live_chem = st.slider(TXT("عدد الجزيئات", "Number of Molecules"), 20, 120, 60, 10, key="live_chem")

    # أزرار التحكم
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button(TXT("▶️ تشغيل المشهد الحي", "▶️ Run Live Scene"), use_container_width=True, type="primary"):
            st.session_state.live_run = True
    with col_btn2:
        if st.button(TXT("⏹️ إيقاف المشهد", "⏹️ Stop Scene"), use_container_width=True):
            st.session_state.live_run = False
    with col_btn3:
        if st.button(TXT("🔄 إعادة ضبط المشهد", "🔄 Reset Scene"), use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith("live_"):
                    del st.session_state[key]
            st.rerun()

    # تهيئة المشهد الحي
    if 'live_init' not in st.session_state:
        st.session_state.live_init = False
    if 'live_run' not in st.session_state:
        st.session_state.live_run = False

    if not st.session_state.live_init:
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

        # توليد الجزيئات الكيميائية
        M = live_chem
        chem_angles = np.random.uniform(0, 2 * np.pi, M)
        chem_radii = np.random.uniform(2, 7, M)
        st.session_state.live_chem_x = cx + chem_radii * np.cos(chem_angles)
        st.session_state.live_chem_y = cy + chem_radii * np.sin(chem_angles) * 0.65
        st.session_state.live_chem_w = np.random.uniform(0.3, 0.9, M)
        st.session_state.live_chem_b = np.random.uniform(0.3, 0.9, M)

        # حالة الكواكب
        st.session_state.live_W = W_raw
        st.session_state.live_B = B_raw
        st.session_state.live_E = E_norm
        st.session_state.live_S = S_final
        st.session_state.live_phase = TXT("توازن", "Balance")

        # زوايا الكواكب
        st.session_state.live_aW = 0.0
        st.session_state.live_aB = np.pi * 0.5
        st.session_state.live_atom_angle = 0.0

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
        chem_x = st.session_state.live_chem_x.copy()
        chem_y = st.session_state.live_chem_y.copy()
        chem_w = st.session_state.live_chem_w.copy()
        chem_b = st.session_state.live_chem_b.copy()
        W = st.session_state.live_W
        B = st.session_state.live_B
        E = st.session_state.live_E
        S = st.session_state.live_S
        phase = st.session_state.live_phase
        aW = st.session_state.live_aW
        aB = st.session_state.live_aB
        atom_angle = st.session_state.live_atom_angle
        trail_Wx = st.session_state.live_trail_Wx
        trail_Wy = st.session_state.live_trail_Wy
        trail_Bx = st.session_state.live_trail_Bx
        trail_By = st.session_state.live_trail_By
        hist_S = st.session_state.live_hist_S
        hist_E = st.session_state.live_hist_E
        hist_x = st.session_state.live_hist_x
        frame = st.session_state.live_frame

        N_curr = len(sx)
        M_curr = len(chem_x)

        # تحديث النجوم
        for i in range(N_curr):
            sw[i] += (W - sw[i]) * 0.01 + np.random.uniform(-0.02, 0.02)
            sb[i] += (B - sb[i]) * 0.01 + np.random.uniform(-0.02, 0.02)

            dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
            close_mask = (dist < 2.0) & (np.arange(N_curr) != i)
            if np.any(close_mask):
                sw[i] += (np.mean(sw[close_mask]) - sw[i]) * 0.02
                sb[i] += (np.mean(sb[close_mask]) - sb[i]) * 0.02

            sw[i] = np.clip(sw[i], 0.01, 1.0)
            sb[i] = np.clip(sb[i], 0.01, 1.0)

        # تحديث الجزيئات الكيميائية
        for i in range(M_curr):
            chem_w[i] += (W - chem_w[i]) * 0.015 + np.random.uniform(-0.025, 0.025)
            chem_b[i] += (B - chem_b[i]) * 0.015 + np.random.uniform(-0.025, 0.025)
            chem_w[i] = np.clip(chem_w[i], 0.01, 1.0)
            chem_b[i] = np.clip(chem_b[i], 0.01, 1.0)

        # صدمات عشوائية
        if random.random() < 0.005:
            affected_stars = np.random.choice(N_curr, size=int(N_curr * 0.2), replace=False)
            sw[affected_stars] *= random.uniform(0.5, 0.8)
            sb[affected_stars] *= random.uniform(0.5, 0.8)
            affected_chem = np.random.choice(M_curr, size=int(M_curr * 0.2), replace=False)
            chem_w[affected_chem] *= random.uniform(0.6, 0.9)
            chem_b[affected_chem] *= random.uniform(0.6, 0.9)
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
        atom_angle += 0.12

        orbit_W = 7 - 2.5 * W
        orbit_B = 5 - 1.5 * B
        wx = cx + orbit_W * np.cos(aW)
        wy = cy + orbit_W * np.sin(aW) * 0.7
        bx = cx + orbit_B * np.cos(aB)
        by = cy + orbit_B * np.sin(aB) * 0.7

        trail_Wx.append(wx); trail_Wy.append(wy)
        trail_Bx.append(bx); trail_By.append(by)

        instability = 1 - np.mean(sw * sb)
        sx += np.random.uniform(-0.05, 0.05, N_curr) * instability
        sy += np.random.uniform(-0.05, 0.05, N_curr) * instability
        sx = np.clip(sx, cx - 13, cx + 13)
        sy = np.clip(sy, cy - 9, cy + 9)

        chem_x += np.random.uniform(-0.04, 0.04, M_curr) * instability
        chem_y += np.random.uniform(-0.04, 0.04, M_curr) * instability
        chem_x = np.clip(chem_x, cx - 8, cx + 8)
        chem_y = np.clip(chem_y, cy - 6, cy + 6)

        frame += 1
        if frame % 2 == 0:
            hist_S.append(S)
            hist_E.append(E)
            hist_x.append(len(hist_x))

        # حفظ الحالة
        st.session_state.live_sx = sx; st.session_state.live_sy = sy
        st.session_state.live_sw = sw; st.session_state.live_sb = sb
        st.session_state.live_chem_x = chem_x; st.session_state.live_chem_y = chem_y
        st.session_state.live_chem_w = chem_w; st.session_state.live_chem_b = chem_b
        st.session_state.live_W = W; st.session_state.live_B = B
        st.session_state.live_E = E; st.session_state.live_S = S
        st.session_state.live_phase = phase
        st.session_state.live_aW = aW; st.session_state.live_aB = aB
        st.session_state.live_atom_angle = atom_angle
        st.session_state.live_trail_Wx = trail_Wx; st.session_state.live_trail_Wy = trail_Wy
        st.session_state.live_trail_Bx = trail_Bx; st.session_state.live_trail_By = trail_By
        st.session_state.live_hist_S = hist_S; st.session_state.live_hist_E = hist_E
        st.session_state.live_hist_x = hist_x; st.session_state.live_frame = frame

        # رسم المشهد
        fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')

        # النواة الذهبية S
        for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                         (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
            ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), r * (0.5 + 2.8 * S), color=c, alpha=a, zorder=15))
        ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')
        ax.text(cx, cy - 2.5, f'S={S:.2f}', color='#FFD700', fontsize=10, ha='center', fontweight='bold')

        # هالة التمكين E
        halo_alpha = 0.25 * (1 - min(E, 1)) + 0.04
        ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 0.5 + 14 * E, color='#00FFFF', alpha=halo_alpha, zorder=7))

        # الغشاء
        ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 8.5, color='#00FF88', alpha=0.1, fill=False, lw=2, zorder=2))

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

        # الذرة (أسفل اليسار)
        atom_cx, atom_cy = 3.8, 3.2
        atom_orbit_rad = 0.5 + 0.35 * S
        ax.add_patch(plt.matplotlib.patches.Circle((atom_cx, atom_cy), 0.15 + 0.25 * S, color='#4488FF', alpha=0.8, zorder=7))
        ax.add_patch(plt.matplotlib.patches.Circle((atom_cx, atom_cy), atom_orbit_rad, color='#00FFFF', alpha=0.15, fill=False, lw=0.5, zorder=6))
        electron_x = atom_cx + atom_orbit_rad * np.cos(atom_angle)
        electron_y = atom_cy + atom_orbit_rad * np.sin(atom_angle)
        ax.add_patch(plt.matplotlib.patches.Circle((electron_x, electron_y), 0.04, color='white', alpha=0.95, zorder=8))
        ax.text(atom_cx, atom_cy - 1.1, TXT('الذرة (فيزياء)', 'Atom (Physics)'), color='#4488FF', fontsize=6, ha='center', alpha=0.8, fontweight='bold')

        # الجزيء الكيميائي (وسط اليسار)
        mol_cx, mol_cy = 3.8, 7.0
        mol_dist = 0.3 + 0.2 * S
        ax.add_patch(plt.matplotlib.patches.Circle((mol_cx - mol_dist, mol_cy), 0.15, color='#FFD700', alpha=0.7, zorder=7))
        ax.add_patch(plt.matplotlib.patches.Circle((mol_cx + mol_dist, mol_cy), 0.15, color='#FFD700', alpha=0.7, zorder=7))
        ax.plot([mol_cx - mol_dist, mol_cx + mol_dist], [mol_cy, mol_cy], color='#FFD700', lw=1.5, alpha=0.6, zorder=6)
        ax.text(mol_cx, mol_cy - 0.8, TXT('جزيء (كيمياء)', 'Molecule (Chemistry)'), color='#FFD700', fontsize=6, ha='center', alpha=0.8, fontweight='bold')

        # الخلية (أسفل اليمين)
        cell_cx, cell_cy = 24.2, 3.2
        ax.add_patch(plt.matplotlib.patches.Circle((cell_cx, cell_cy), 0.35 + 0.4 * S, color='#00FF88', alpha=0.3, zorder=7, ec='#00FF88', lw=1))
        ax.add_patch(plt.matplotlib.patches.Circle((cell_cx, cell_cy), 0.1 + 0.12 * S, color='white', alpha=0.8, zorder=8))
        ax.text(cell_cx, cell_cy - 1.1, TXT('الخلية (بيولوجيا)', 'Cell (Biology)'), color='#00FF88', fontsize=6, ha='center', alpha=0.8, fontweight='bold')

        # الجزيئات الكيميائية المتدفقة
        chem_colors = []
        for i in range(M_curr):
            cw, cb = chem_w[i], chem_b[i]
            if cw >= 0.55 and cb >= 0.55: chem_colors.append('#FFD700')
            elif cw >= 0.55 and cb < 0.45: chem_colors.append('#E0E0E0')
            elif cw < 0.45 and cb >= 0.55: chem_colors.append('#FF5252')
            elif cw < 0.45 and cb < 0.45: chem_colors.append('#FFB6C1')
            else: chem_colors.append('#888888')
        ax.scatter(chem_x, chem_y, s=20, c=chem_colors, alpha=0.7, edgecolors='white', linewidths=0.3, zorder=5, marker='s')

        # النجوم بألوانها
        star_colors = []
        for i in range(N_curr):
            w_val, b_val = sw[i], sb[i]
            if w_val >= 0.55 and b_val >= 0.55: star_colors.append('#FFD700')
            elif w_val >= 0.55 and b_val < 0.45: star_colors.append('#E0E0E0')
            elif w_val < 0.45 and b_val >= 0.55: star_colors.append('#FF5252')
            elif w_val < 0.45 and b_val < 0.45: star_colors.append('#FFB6C1')
            else: star_colors.append('#888888')
        ax.scatter(sx, sy, s=30, c=star_colors, alpha=0.85, edgecolors='white', linewidths=0.3, zorder=5)

        # الميزان الأخروي (أعلى اليمين)
        mizan_x, mizan_y = 24.5, 16.5
        hasanat = W * 200
        sayyiat = (1 - B) * 200
        ax.plot([mizan_x, mizan_x], [mizan_y - 2.5, mizan_y + 1], color='#FFD700', lw=1.5, alpha=0.6, zorder=10)
        balance_ratio = (hasanat - sayyiat) / max(hasanat + sayyiat, 1)
        beam_y = mizan_y - balance_ratio * 0.5
        ax.plot([mizan_x - 1.5, mizan_x + 1.5], [beam_y, beam_y], color='#FFD700', lw=2, alpha=0.7, zorder=10)
        left_y = mizan_y - 1.0 + min(hasanat / 30, 0.8)
        right_y = mizan_y - 1.0 + min(sayyiat / 30, 0.8)
        ax.plot([mizan_x - 1.5, mizan_x - 1.5], [beam_y, left_y], color='#FFD700', lw=1, alpha=0.5, zorder=9)
        ax.plot([mizan_x + 1.5, mizan_x + 1.5], [beam_y, right_y], color='#FFD700', lw=1, alpha=0.5, zorder=9)
        ax.add_patch(plt.matplotlib.patches.FancyBboxPatch((mizan_x - 2.2, left_y - 0.3), 1.4, 0.6, boxstyle="round,pad=0.05", color='white', alpha=0.3, zorder=8, ec='white', lw=0.7))
        ax.add_patch(plt.matplotlib.patches.FancyBboxPatch((mizan_x + 0.8, right_y - 0.3), 1.4, 0.6, boxstyle="round,pad=0.05", color='#220000', alpha=0.3, zorder=8, ec='#FF3333', lw=0.7))
        ax.text(mizan_x - 1.5, left_y - 0.8, f'{hasanat:.0f}', color='white', fontsize=7, ha='center', fontweight='bold', alpha=0.7)
        ax.text(mizan_x + 1.5, right_y - 0.8, f'{sayyiat:.0f}', color='#FF3333', fontsize=7, ha='center', fontweight='bold', alpha=0.7)
        ax.text(mizan_x, mizan_y + 1.5, TXT('الميزان الأخروي', 'Afterlife Scales'), color='#FFD700', fontsize=8, ha='center', fontweight='bold')

        # لوحة الإثبات
        pax = ax.inset_axes([0.5, 0.02, 0.46, 0.10])
        pax.set_xlim(0, 300); pax.set_ylim(0, 1.05)
        pax.set_title(TXT('S (ذهب) → E (سماوي) – الاستدراج', 'S (Gold) → E (Cyan) – Istidraj'), color='white', fontsize=7)
        pax.tick_params(colors='white', labelsize=4); pax.grid(True, alpha=0.12)
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

        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, facecolor='#000010')
        buf.seek(0)
        st.session_state.live_image = buf
        plt.close(fig)

        time.sleep(live_speed)
        st.rerun()

    elif st.session_state.live_init and 'live_image' in st.session_state:
        st.image(st.session_state.live_image, caption=TXT("آخر حالة للمشهد الحي", "Last Live Scene State"), use_column_width=True)
        st.info(TXT("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة.", "Press ▶️ Run Live Scene to start the simulation."))
    else:
        st.info(TXT("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة الديناميكية.", "Press ▶️ Run Live Scene to start the dynamic simulation."))

# زر تحميل صورة المشهد الحي
if 'live_image' in st.session_state:
    st.download_button(
        label=TXT("📥 تحميل صورة المشهد الحي", "📥 Download Live Scene Image"),
        data=st.session_state.live_image,
        file_name="al_deen_al_qayyim_live_scene.png",
        mime="image/png",
        key="dl_live"
    )

# =============================================
# التذييل
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:20px;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="font-size:2em;margin:0;">⚖️</p>
    <p style="color:#FFD700;font-size:1.5em;font-weight:bold;">{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</p>
    <p style="color:#FFD700;font-size:1.2em;">S = W × B</p>
    <p>{TXT('قانون التوازن الكوني – من الذرة إلى الحضارة', 'The Cosmic Law of Balance – From Atom to Civilization')}</p>
    <p>﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
    <p>{TXT('علي عادل العاطفي', 'Ali Adel Alatifi')} | 2026</p>
    <p style="font-size:0.8em;margin-top:10px;">{TXT('جميع الحقوق محفوظة', 'All Rights Reserved')} | MIT License</p>
    <p style="font-size:0.8em;">{TXT('المنصة الذهبية – مختبر الميزان', 'The Golden Platform – The Mizan Lab')} v3.0</p>
    <p style="font-size:2em;margin:0;">⚖️</p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الرابعة مكتملة: المشهد الحي، الذرة، الجزيء، الخلية، الميزان الأخروي، التذييل")
print("✅✅✅ تم بناء المنصة الذهبية – الدين القيم – بكافة أركانها وأدواتها ولوازمها بنجاح!")
