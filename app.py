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
# المؤشرات الوجودية – مجموعة واحدة مع الحروف والقيم
# =============================================
# كل مؤشر له: الاسم، الحرف، القيمة
INDICATORS_META = [
    {"name_ar": "الصلاة (إقامة/تضييع)", "name_en": "Prayer (Establish/Neglect)", "letter": "ن", "value": 50},
    {"name_ar": "الزكاة والصدقات (إيتاء/منع)", "name_en": "Zakat & Charity (Give/Withhold)", "letter": "ص", "value": 90},
    {"name_ar": "الولاء لله ورسوله والمؤمنين (موالاة/معاداة)", "name_en": "Loyalty to Allah, Messenger & Believers", "letter": "أ", "value": 1},
    {"name_ar": "تحكيم الشريعة (تحكيم/رفض)", "name_en": "Applying Sharia (Apply/Reject)", "letter": "ل", "value": 30},
    {"name_ar": "العدل (عدل/ظلم)", "name_en": "Justice (Just/Unjust)", "letter": "ق", "value": 100},
    {"name_ar": "الشورى (تشاور/استبداد)", "name_en": "Consultation - Shura (Consult/Tyranny)", "letter": "م", "value": 40},
    {"name_ar": "البراءة من الطاغوت (براءة/موالاة)", "name_en": "Disavowal of Taghut (Disavow/Ally)", "letter": "هـ", "value": 5},
    {"name_ar": "الرحمة والعطاء – الماعون (رحمة/قسوة)", "name_en": "Mercy & Giving - Al-Ma'un", "letter": "ح", "value": 8},
    {"name_ar": "الأمر بالمعروف (أمر/نهي عن المعروف)", "name_en": "Enjoining Good", "letter": "ف", "value": 80},
    {"name_ar": "النهي عن المنكر (نهي/أمر بالمنكر)", "name_en": "Forbidding Evil", "letter": "و", "value": 6},
    {"name_ar": "النزاهة ومكافحة الفساد (نزاهة/فساد)", "name_en": "Integrity & Anti-Corruption", "letter": "ب", "value": 2},
    {"name_ar": "السيادة والاستقلال (استقلال/تبعية)", "name_en": "Sovereignty & Independence", "letter": "م", "value": 40},
    {"name_ar": "الاكتفاء الذاتي (اكتفاء/اعتماد)", "name_en": "Self-Sufficiency", "letter": "ق", "value": 100},
    {"name_ar": "الإنتاج الزراعي (إنتاج/إهمال)", "name_en": "Agricultural Production", "letter": "ك", "value": 20},
    {"name_ar": "الإنتاج الصناعي (صناعة/تخلف)", "name_en": "Industrial Production", "letter": "ص", "value": 90},
    {"name_ar": "القوة العسكرية (قوة/ضعف)", "name_en": "Military Power", "letter": "ر", "value": 200},
    {"name_ar": "التصميم والهندسة – ك (إبداع/جمود)", "name_en": "Design & Engineering - K", "letter": "ك", "value": 20},
    {"name_ar": "التصنيع والتشكيل – هـ (إتقان/فوضى)", "name_en": "Manufacturing & Forming - H", "letter": "هـ", "value": 5},
    {"name_ar": "التطوير والتحسين – ي (تجديد/ركود)", "name_en": "Development & Improvement - Y", "letter": "ي", "value": 10},
    {"name_ar": "البحث والتطوير – ع (علم/جهل)", "name_en": "Research & Development - A", "letter": "ع", "value": 70},
    {"name_ar": "الجودة والاستدامة – ص (ثبات/انهيار)", "name_en": "Quality & Sustainability - S", "letter": "ص", "value": 90},
]

def get_indicator_label(i):
    meta = INDICATORS_META[i]
    name = meta["name_ar"] if LANG == "ar" else meta["name_en"]
    letter = meta["letter"]
    value = meta["value"]
    return f"{name}  [{letter}={value}]"

# =============================================
# المحكمة العليا – أربع بوابات منطقية قرآنية
# =============================================
def supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal):
    if not W_pure:
        return (0, TXT("بوابة الشرك", "Shirk Gate"),
                TXT("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾", "⚠️ Unforgivable"),
                "🔴")
    if B_compassion <= 0:
        return (-1, TXT("بوابة الماعون", "Al-Ma'un Gate"),
                TXT("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾", "⚠️ Collapse"),
                "🔴")
    if W_raw > 0 and B_disavowal <= 0:
        return (0, TXT("بوابة الإخلاص", "Sincerity Gate"),
                TXT("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي وَلَا يُشْرِكُونَ بِي شَيْئًا﴾", "⚠️ Void worship"),
                "🟡")
    if W_raw > 0 and B_raw > 0:
        return (1, TXT("بوابة الوعد", "Promise Gate"),
                TXT("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾", "🟢 Stability"),
                "🟢")
    return None, None, None, None

def calculate_S(W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal):
    S_gate, gate_name, gate_msg, gate_color = supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal)
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0
    W = (W_raw + 1) / 2
    B = (B_raw + 1) / 2
    E = (E_raw + 1) / 2
    W_boost = 1 + (LETTERS_DB['أ'] + LETTERS_DB['ر'] + LETTERS_DB['س'] + LETTERS_DB['ط']) / 1000
    B_boost = 1 + (LETTERS_DB['ل'] + LETTERS_DB['ح'] + LETTERS_DB['ط']) / 1000
    S_raw = (W * W_boost) * (B * B_boost) * (1 + LETTERS_DB['م'] / 1000)
    istidraj_gap = max(0, E - S_raw)
    return min(1.0, S_raw), E, TXT("المعادلة العامة", "General Equation"), "", "⚪", istidraj_gap

def simulate_future(S, E, W_raw, B_raw, years=50):
    Sh, Eh = [S], [E]
    for _ in range(years):
        nE = Eh[-1] + 0.02 * (Sh[-1] - Eh[-1])
        nB = B_raw
        if nE > Sh[-1] + 0.2: nB -= 0.03
        elif nE < Sh[-1]: nB += 0.01
        nS = ((W_raw + 1) / 2) * ((nB + 1) / 2) * (1 + sum(LETTERS_DB.values()) / 1000)
        Sh.append(nS); Eh.append(nE)
    return Sh, Eh

def call_ai_api(user_text):
    try:
        import openai
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        indicators_desc = "\n".join([f"{i+1}. {get_indicator_label(i)}" for i in range(len(INDICATORS_META))])
        prompt = f"""أنت محلل خبير في نظرية الميزان (S = W × B). اقرأ وصف الكيان وأعد تقديرات رقمية بصيغة JSON فقط.
لديك {len(INDICATORS_META)} مؤشراً، كل منها بين -1 (سلبي) و +1 (إيجابي):
{indicators_desc}
W_pure: true/false
analysis: تحليل موجز بالعربية
أعد النتيجة بصيغة JSON فقط.
مثال: {{"values":[0.5,0.4,...], "W_pure":true, "analysis":"..."}}
الوصف: {user_text}"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"system","content":"ترد بصيغة JSON فقط."},
                      {"role":"user","content":prompt}],
            temperature=0.3, max_tokens=600)
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        return json.loads(content)
    except Exception as e:
        st.error(TXT(f"خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}", f"AI connection error: {str(e)}"))
        return None

def plot_quadrant_map(B_raw, W_raw, istidraj_gap):
    fig, ax = plt.subplots(figsize=(7,7), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
    ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
    ax.set_xlabel(TXT("B (الكفر بالطاغوت)", "B (Disavowal)"), color='white')
    ax.set_ylabel(TXT("W (الإيمان بالله)", "W (Faith)"), color='white')
    ax.fill_between([0,1.2],0,1.2,color='#FFD700',alpha=0.3,label=TXT('المؤمنون','Believers'))
    ax.fill_between([-1.2,0],0,1.2,color='#FF5252',alpha=0.2,label=TXT('المغضوب عليهم','Those with Wrath'))
    ax.fill_between([-1.2,0],-1.2,0,color='#FFB6C1',alpha=0.2,label=TXT('المنافقون','Hypocrites'))
    ax.fill_between([0,1.2],-1.2,0,color='#FFA500',alpha=0.2,label=TXT('الضالون','Those Astray'))
    ax.scatter(B_raw,W_raw,s=400,c='cyan',edgecolors='white',linewidth=3,zorder=10)
    ax.scatter(1,1,s=150,c='#FFD700',edgecolors='white',linewidth=2,zorder=10,marker='*')
    ax.text(1,1.15,TXT('مقام إبراهيم','Station of Abraham'),color='#FFD700',fontsize=9,ha='center',fontweight='bold')
    if istidraj_gap>0:
        ax.text(0.5,-0.9,TXT(f"فجوة استدراج: {istidraj_gap:.2f}",f"Istidraj Gap: {istidraj_gap:.2f}"),
                color='red',fontsize=10,ha='center',fontweight='bold')
    ax.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=8,loc='lower left')
    ax.tick_params(colors='white')
    return fig

print("✅ المرحلة الأولى مكتملة: الأساسيات، الثوابت، المؤشرات مع الحروف، المحكمة العليا، دوال الحساب، الذكاء الاصطناعي")

# =============================================
# المرحلة الثانية: الشريط الجانبي والمنزلقات الموحدة
# =============================================

# تهيئة حالة الجلسة للقيم الافتراضية
if "slider_values" not in st.session_state:
    st.session_state.slider_values = {f"V{i}": 0.0 for i in range(len(INDICATORS_META))}
    st.session_state.slider_values["W_pure"] = True

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

with st.sidebar:
    # شعار المنصة
    st.markdown(f"""
    <div style='text-align:center;padding:10px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <p style='font-size:2.5em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:0;'>{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h2>
        <p style='color:#e0e0e0;font-size:11px;margin:5px 0;'>{TXT('قانون التوازن الكوني', 'The Cosmic Law of Balance')}</p>
        <p style='color:#FFD700;font-size:15px;margin:3px 0;font-weight:bold;'>S = W × B</p>
        <p style='font-size:2.5em;margin:0;'>⚖️</p>
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

    N_IND = len(INDICATORS_META)  # 21 مؤشراً
    slider_vals = [0.0] * N_IND
    W_pure = True

    if TXT("يدوي", "Manual") in mode:
        # جميع المؤشرات في مجموعة واحدة – كل حركة مولد طاقة
        with st.expander(TXT("🎛️ مولدات الطاقة الوجودية", "🎛️ Existential Energy Generators"), expanded=True):
            st.caption(TXT(
                "كل حركة وسكنة في حياة الإنسان هي مولد طاقة دافعة نحو الولاية والبراءة معاً. حرّك المنزلقات لتقدير حالة الكيان. [الحرف=القيمة]",
                "Every movement is an energy generator toward loyalty and disavowal. Adjust sliders. [Letter=Value]"
            ))

            # عرض المنزلقات في عمودين لتوفير المساحة
            for i in range(0, N_IND, 2):
                col_a, col_b = st.columns(2)
                with col_a:
                    if i < N_IND:
                        slider_vals[i] = st.slider(
                            get_indicator_label(i),
                            -1.0, 1.0,
                            st.session_state.slider_values.get(f"V{i}", 0.0),
                            0.1,
                            key=f"s_V{i}"
                        )
                with col_b:
                    if i + 1 < N_IND:
                        slider_vals[i+1] = st.slider(
                            get_indicator_label(i+1),
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
            "🤖 اكتب وصفاً للكيان (دولة، مجتمع، فرد) ليقوم الذكاء الاصطناعي بتقدير المؤشرات.",
            "🤖 Describe the entity for AI to estimate indicators."
        ))

        ai_text = st.text_area(
            TXT("الوصف النصي:", "Description:"),
            height=200,
            placeholder=TXT(
                "مثال: دولة إسلامية ذات أغلبية شابة، تعاني من فساد إداري لكنها تملك جيشاً قوياً...",
                "Example: An Islamic country with a young majority..."
            )
        )

        if st.button(TXT("تحليل بالذكاء الاصطناعي", "Analyze with AI"), type="primary", use_container_width=True):
            if not ai_text.strip():
                st.warning(TXT("يرجى إدخال وصف نصي أولاً.", "Please enter a description first."))
            else:
                with st.spinner(TXT("جاري التحليل...", "Analyzing...")):
                    ai_result = call_ai_api(ai_text)
                    if ai_result:
                        st.session_state.ai_result = ai_result
                        st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
                        if "analysis" in ai_result:
                            st.info(ai_result["analysis"])

        # إذا كان هناك نتيجة سابقة من الذكاء الاصطناعي
        if st.session_state.ai_result is not None:
            r = st.session_state.ai_result
            vals = r.get("values", [0.0] * N_IND)
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
# 0-5: W, 6-10: B, 11-15: E, 16-20: I
W_vals = vals[0:6]
B_vals = vals[6:11]
E_vals = vals[11:16]
I_vals = vals[16:21]

# المتوسطات الخام
W_raw = np.mean(W_vals)
B_raw = np.mean(B_vals)

# حساب E المرجح بقيم الحروف (م، ق، ك، ص، ر)
E_LETTERS = ['م', 'ق', 'ك', 'ص', 'ر']
E_weights_list = [LETTERS_DB[l] for l in E_LETTERS]

# حساب مؤشر الصناعة المرجح من تفصيل الكهيعص
IND_LETTERS = ['ك', 'هـ', 'ي', 'ع', 'ص']
i_weights = [LETTERS_DB[l] for l in IND_LETTERS]
I_weighted = np.average(I_vals, weights=i_weights)

# استبدال المؤشر الصناعي في E (الفهرس 3) بالمؤشر المفصل
E_vals_updated = E_vals.copy()
E_vals_updated[3] = I_weighted
E_raw = np.average(E_vals_updated, weights=E_weights_list)

# قيم البوابات
B_compassion = B_vals[1]  # الرحمة والعطاء (الماعون)
B_disavowal = B_vals[0]   # البراءة من الطاغوت

# حساب S النهائي
S_final, E_norm, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
    W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal
)

print("✅ المرحلة الثانية مكتملة: الشريط الجانبي، المنزلقات مع الحروف والقيم، الذكاء الاصطناعي، الحسابات")

# =============================================
# المرحلة الثالثة: العنوان، لوحة القيادة، التبويبات
# =============================================

# العنوان الرئيسي – بتنسيق خاص
st.markdown(f"""
<div style="text-align:center;padding:25px 0 15px 0;">
    <p style="font-size:2.8em;margin:0;">⚖️</p>
    <h1 style="color:#FFD700;font-size:2.8em;margin:5px 0;font-weight:900;letter-spacing:3px;">{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h1>
    <h2 style="color:#FFD700;font-size:1.3em;margin-top:0;font-weight:400;">{TXT('قانون التوازن الكوني من الأزل إلى الخلود', 'The Cosmic Law of Balance from Eternity to Eternity')}</h2>
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
        "الخريطة الرباعية تُظهر موقعك في فضاء القيم بناءً على قيمتي الولاء (W) والبراءة (B).",
        "The quadrant map shows your position in Value Space based on Loyalty (W) and Disavowal (B)."
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
        "هذه المحاكاة تظهر كيف ستتغير قيم S وE عبر الزمن. منطقة الاستدراج تظهر عندما يتجاوز التمكين (E) الثبات (S).",
        "This simulation shows how S and E will change over time. The Istidraj zone appears when Empowerment (E) exceeds Stability (S)."
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
    
    all_vals = vals.copy()
    wW = np.argmin(W_vals)
    wB = np.argmin(B_vals)
    wE_idx = np.argmin(E_vals_updated)
    wAll = np.argmin(all_vals)
    
    # الحصول على أسماء المؤشرات
    inds_ar = [m["name_ar"] for m in INDICATORS_META]
    inds_en = [m["name_en"] for m in INDICATORS_META]
    inds_display = inds_ar if LANG == "ar" else inds_en
    
    # التشخيص
    st.markdown(TXT("### 🔍 التشخيص", "### 🔍 Diagnosis"))
    if gate_name == TXT("بوابة الشرك", "Shirk Gate"):
        st.error(TXT(
            "العلاج: تجديد التوحيد وإخلاص العبادة لله وحده. لا ينفع مع الشرك أي عمل.",
            "Treatment: Renew Tawheed and sincerity to Allah alone. No deed benefits with shirk."
        ))
    elif gate_name == TXT("بوابة الماعون", "Al-Ma'un Gate"):
        st.error(TXT(
            f"الأولوية القصوى: إصلاح مؤشر '{inds_display[wAll]}'. بدون رحمة وعطاء، لا تنفع أي عبادة.",
            f"Top priority: Fix the '{inds_display[wAll]}' indicator. Without mercy and giving, no worship benefits."
        ))
    elif gate_name == TXT("بوابة الإخلاص", "Sincerity Gate"):
        st.warning(TXT(
            f"الأولوية: تنقية '{inds_display[wAll]}' من شوائب الشرك والرياء.",
            f"Priority: Purify '{inds_display[wAll]}' from shirk and hypocrisy."
        ))
    elif istidraj_gap > 0.3:
        st.error(TXT(
            f"الأولوية: سد فجوة الاستدراج ({istidraj_gap:.2f}) عبر رفع '{inds_display[wAll]}'.",
            f"Priority: Close the Istidraj gap ({istidraj_gap:.2f}) by raising '{inds_display[wAll]}'."
        ))
    else:
        st.info(TXT(
            f"للتقدم نحو مقام إبراهيم: عزز '{inds_display[wAll]}'.",
            f"To advance to the Station of Abraham: strengthen '{inds_display[wAll]}'."
        ))
    
    # جدول المؤشرات
    st.markdown(TXT("### 📊 تفصيل المؤشرات", "### 📊 Indicator Details"))
    
    groups = (
        [TXT('ولاء', 'Loyalty')]*6 + 
        [TXT('براءة', 'Disavowal')]*5 + 
        [TXT('تمكين', 'Empowerment')]*5 + 
        [TXT('صناعة', 'Industry')]*5
    )
    
    df_all = pd.DataFrame({
        TXT('المؤشر', 'Indicator'): inds_display,
        TXT('القيمة', 'Value'): all_vals,
        TXT('المجموعة', 'Group'): groups
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
        "هذا المعجم يربط كل حرف بقيمته العددية (حساب الجمل) ودوره الوجودي في معادلة الميزان.",
        "This lexicon links each letter to its numerical value and existential role in the Mizan equation."
    ))
    
    letters_data = {
        TXT('الفئة الأولى: الذات الإلهية (المصدر)', 'Category 1: Divine Essence'): 
            {'ك': 20, 'ن': 50},
        TXT('الفئة الثانية: الازدواج', 'Category 2: Duality'): 
            {'ق': 100, 'ص': 90},
        TXT('الفئة الثالثة: التجلي الإلهي', 'Category 3: Divine Manifestation'): 
            {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        TXT('الفئة الرابعة: الاشتراك (الجسور)', 'Category 4: Bridges'): 
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
# المرحلة الرابعة: المشهد الحي المتكامل والتذييل
# =============================================

with tab6:
    st.subheader(TXT("🌌 المشهد الحي – المحاكاة الكونية", "🌌 Live Scene – Cosmic Simulation"))
    st.markdown(TXT(
        "هذا المشهد الحي يحاكي تفاعل النجوم (الأفراد) مع قطبي الميزان W وB. "
        "النجوم الذهبية تمثل المؤمنين المتوازنين، والبيضاء تمثل من لديهم ولاء بلا براءة، "
        "والحمراء تمثل براءة بلا ولاء، والوردية تمثل من لا هذا ولا ذاك. "
        "الميزان الأخروي الخفي يظهر تدريجياً مع تراكم الحسنات والسيئات.",
        "This live scene simulates the interaction of stars with the poles of the Mizan. "
        "Golden stars: balanced believers. White: loyalty without disavowal. Red: disavowal without loyalty. Pink: neither. "
        "The invisible afterlife scales gradually appear as deeds accumulate."
    ))

    # إعدادات المشهد الحي
    with st.expander(TXT("⚙️ إعدادات المشهد الحي", "⚙️ Live Scene Settings"), expanded=False):
        col_set1, col_set2, col_set3, col_set4 = st.columns(4)
        with col_set1:
            live_speed = st.slider(TXT("سرعة المحاكاة", "Speed"), 0.01, 0.2, 0.08, 0.01, key="live_speed")
        with col_set2:
            live_stars = st.slider(TXT("عدد النجوم", "Stars"), 50, 400, 200, 50, key="live_stars")
        with col_set3:
            live_trail = st.slider(TXT("مسار الكواكب", "Trail"), 20, 200, 100, 10, key="live_trail")
        with col_set4:
            live_chem = st.slider(TXT("عدد الجزيئات", "Molecules"), 10, 80, 40, 10, key="live_chem")

    # أزرار التحكم
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button(TXT("▶️ تشغيل", "▶️ Run"), use_container_width=True, type="primary"):
            st.session_state.live_run = True
    with col_btn2:
        if st.button(TXT("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True):
            st.session_state.live_run = False
    with col_btn3:
        if st.button(TXT("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith("live_"):
                    del st.session_state[key]
            st.rerun()

    # التهيئة
    if 'live_init' not in st.session_state:
        st.session_state.live_init = False
    if 'live_run' not in st.session_state:
        st.session_state.live_run = False

    if not st.session_state.live_init:
        try:
            cx, cy = 14.0, 10.0
            st.session_state.live_cx = cx
            st.session_state.live_cy = cy

            N = max(10, live_stars)
            angles = np.random.uniform(0, 2 * np.pi, N)
            radii = np.random.uniform(1.5, 9, N)
            st.session_state.live_sx = cx + radii * np.cos(angles)
            st.session_state.live_sy = cy + radii * np.sin(angles) * 0.65
            st.session_state.live_sw = np.random.uniform(0.2, 0.9, N)
            st.session_state.live_sb = np.random.uniform(0.2, 0.9, N)

            M = max(5, live_chem)
            chem_angles = np.random.uniform(0, 2 * np.pi, M)
            chem_radii = np.random.uniform(2, 7, M)
            st.session_state.live_chem_x = cx + chem_radii * np.cos(chem_angles)
            st.session_state.live_chem_y = cy + chem_radii * np.sin(chem_angles) * 0.65
            st.session_state.live_chem_w = np.random.uniform(0.3, 0.9, M)
            st.session_state.live_chem_b = np.random.uniform(0.3, 0.9, M)

            st.session_state.live_W = W_raw
            st.session_state.live_B = B_raw
            st.session_state.live_E = E_norm
            st.session_state.live_S = S_final
            st.session_state.live_phase = TXT("توازن", "Balance")
            st.session_state.live_aW = 0.0
            st.session_state.live_aB = np.pi * 0.5
            st.session_state.live_atom_angle = 0.0
            st.session_state.live_flow_angle = 0.0

            st.session_state.live_trail_Wx = deque(maxlen=live_trail)
            st.session_state.live_trail_Wy = deque(maxlen=live_trail)
            st.session_state.live_trail_Bx = deque(maxlen=live_trail)
            st.session_state.live_trail_By = deque(maxlen=live_trail)

            st.session_state.live_hist_S = deque(maxlen=300)
            st.session_state.live_hist_E = deque(maxlen=300)
            st.session_state.live_hist_x = deque(maxlen=300)
            st.session_state.live_frame = 0

            st.session_state.live_init = True
        except Exception as e:
            st.error(f"خطأ في التهيئة: {e}")
            st.session_state.live_init = False

    # تشغيل المحاكاة
    if st.session_state.get("live_run", False):
        placeholder = st.empty()

        try:
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
            flow_angle = st.session_state.live_flow_angle
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
            mr = 8.5

            # تحديث النجوم
            for i in range(N_curr):
                sw[i] += (W - sw[i]) * 0.01 + np.random.uniform(-0.02, 0.02)
                sb[i] += (B - sb[i]) * 0.01 + np.random.uniform(-0.02, 0.02)
                close_mask = np.zeros(N_curr, dtype=bool)
                for j in range(N_curr):
                    if i != j:
                        dx = sx[i] - sx[j]
                        dy = sy[i] - sy[j]
                        if np.sqrt(dx*dx + dy*dy) < 2.0:
                            close_mask[j] = True
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

            # صدمات
            if random.random() < 0.005:
                aff_stars = np.random.choice(N_curr, size=max(1, int(N_curr*0.2)), replace=False)
                sw[aff_stars] *= random.uniform(0.5, 0.8)
                sb[aff_stars] *= random.uniform(0.5, 0.8)
                if M_curr > 0:
                    aff_chem = np.random.choice(M_curr, size=max(1, int(M_curr*0.2)), replace=False)
                    chem_w[aff_chem] *= random.uniform(0.6, 0.9)
                    chem_b[aff_chem] *= random.uniform(0.6, 0.9)
                phase = TXT("💥 صدمة", "💥 Shock")

            avg_W = np.mean(sw) if N_curr > 0 else W
            avg_B = np.mean(sb) if N_curr > 0 else B
            avg_S_stars = np.mean(sw * sb) if N_curr > 0 else S
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
            flow_angle += 0.05

            orbit_W = 7 - 2.5 * W
            orbit_B = 5 - 1.5 * B
            wx = cx + orbit_W * np.cos(aW)
            wy = cy + orbit_W * np.sin(aW) * 0.7
            bx = cx + orbit_B * np.cos(aB)
            by = cy + orbit_B * np.sin(aB) * 0.7

            trail_Wx.append(wx); trail_Wy.append(wy)
            trail_Bx.append(bx); trail_By.append(by)

            instability = 1 - avg_S_stars
            sx += np.random.uniform(-0.05, 0.05, N_curr) * instability
            sy += np.random.uniform(-0.05, 0.05, N_curr) * instability
            sx = np.clip(sx, cx - 13, cx + 13)
            sy = np.clip(sy, cy - 9, cy + 9)

            if M_curr > 0:
                chem_x += np.random.uniform(-0.04, 0.04, M_curr) * instability
                chem_y += np.random.uniform(-0.04, 0.04, M_curr) * instability
                chem_x = np.clip(chem_x, cx - 8, cx + 8)
                chem_y = np.clip(chem_y, cy - 6, cy + 6)

            frame += 1
            if frame % 2 == 0:
                hist_S.append(S); hist_E.append(E); hist_x.append(len(hist_x))

            # حفظ
            st.session_state.live_sx = sx; st.session_state.live_sy = sy
            st.session_state.live_sw = sw; st.session_state.live_sb = sb
            st.session_state.live_chem_x = chem_x; st.session_state.live_chem_y = chem_y
            st.session_state.live_chem_w = chem_w; st.session_state.live_chem_b = chem_b
            st.session_state.live_W = W; st.session_state.live_B = B
            st.session_state.live_E = E; st.session_state.live_S = S
            st.session_state.live_phase = phase
            st.session_state.live_aW = aW; st.session_state.live_aB = aB
            st.session_state.live_atom_angle = atom_angle
            st.session_state.live_flow_angle = flow_angle
            st.session_state.live_trail_Wx = trail_Wx; st.session_state.live_trail_Wy = trail_Wy
            st.session_state.live_trail_Bx = trail_Bx; st.session_state.live_trail_By = trail_By
            st.session_state.live_hist_S = hist_S; st.session_state.live_hist_E = hist_E
            st.session_state.live_hist_x = hist_x; st.session_state.live_frame = frame

            # رسم المشهد المتكامل
            fig, ax = plt.subplots(figsize=(16, 12), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')

            # النواة الذهبية
            for r, a, c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                             (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(plt.matplotlib.patches.Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
            ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
            ax.text(cx,cy-2.5,f'S={S:.2f}',color='#FFD700',fontsize=10,ha='center',fontweight='bold')

            # هالة E
            ax.add_patch(plt.matplotlib.patches.Circle((cx,cy), 0.5+16*E, color='#0FF', alpha=0.25*(1-min(E,1))+0.04, zorder=7))

            # الغشاء والحلقات
            ax.add_patch(plt.matplotlib.patches.Circle((cx,cy), mr, color='#0F8', alpha=0.12, fill=False, lw=2.5, zorder=2))
            for r in [10.0, 11.5, 13.0]:
                ax.add_patch(plt.matplotlib.patches.Circle((cx,cy), r, color='#FFD700', alpha=0.02, fill=False, lw=0.6, ls=':', zorder=0))

            # القنوات
            for i in range(6):
                ang = -np.pi/4 + i*(np.pi/2)/5
                chx = cx + mr*np.cos(ang); chy = cy + mr*np.sin(ang)
                ax.add_patch(plt.matplotlib.patches.Circle((chx,chy), 0.2+0.4*avg_W, color='#FFF', alpha=0.3+0.5*avg_W, zorder=8, ec='#FFD700', lw=1.5))
            for i in range(6):
                ang = np.pi - np.pi/4 + i*(np.pi/2)/5
                chx = cx + mr*np.cos(ang); chy = cy + mr*np.sin(ang)
                ax.add_patch(plt.matplotlib.patches.Circle((chx,chy), 0.2+0.4*avg_B, color='#F33', alpha=0.25+0.35*avg_B, zorder=8, ec='#F66', lw=1.5))

            # أسهم التدفق
            for i in range(3):
                a = -np.pi/5 + i*0.5 + 0.1*np.sin(flow_angle)
                r1, r2 = 3+S*2.5, 0.6
                x1, y1 = cx + r1*np.cos(a), cy + r1*np.sin(a)
                x2, y2 = cx + r2*np.cos(a), cy + r2*np.sin(a)
                arr = plt.matplotlib.patches.FancyArrowPatch((x1,y1),(x2,y2), color='white', alpha=0.15+0.4*avg_W, lw=0.6, arrowstyle='->')
                ax.add_patch(arr)
            for i in range(3):
                a = np.pi - np.pi/5 + i*0.5 + 0.1*np.cos(flow_angle)
                r1, r2 = 3+S*2.5, 0.6
                x1, y1 = cx + r1*np.cos(a), cy + r1*np.sin(a)
                x2, y2 = cx + r2*np.cos(a), cy + r2*np.sin(a)
                arr = plt.matplotlib.patches.FancyArrowPatch((x1,y1),(x2,y2), color='#F33', alpha=0.12+0.3*avg_B, lw=0.6, arrowstyle='->')
                ax.add_patch(arr)

            # الكوكبان
            ax.add_patch(plt.matplotlib.patches.Circle((wx,wy), 0.3+0.5*W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(plt.matplotlib.patches.Circle((bx,by), 0.3+0.5*B, color='#F33', alpha=0.85, zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            if len(trail_Wx)>1: ax.plot(list(trail_Wx),list(trail_Wy),color='#FFF',lw=0.3,alpha=0.12,zorder=4)
            if len(trail_Bx)>1: ax.plot(list(trail_Bx),list(trail_By),color='#F33',lw=0.3,alpha=0.12,zorder=4)

            # الذرة
            acx,acy=3.8,3.2; arad=0.5+0.35*S
            ax.add_patch(plt.matplotlib.patches.Circle((acx,acy),0.15+0.25*S,color='#4488FF',alpha=0.8,zorder=7))
            ax.add_patch(plt.matplotlib.patches.Circle((acx,acy),arad,color='#0FF',alpha=0.2,fill=False,lw=0.5,zorder=6))
            ax.add_patch(plt.matplotlib.patches.Circle((acx+arad*np.cos(atom_angle),acy+arad*np.sin(atom_angle)),0.04,color='white',alpha=0.95,zorder=8))
            ax.text(acx,acy-1.1,TXT('الذرة (فيزياء)','Atom'),color='#4488FF',fontsize=6,ha='center',alpha=0.8,fontweight='bold')

            # الجزيء
            mcx,mcy=3.8,7.0; mdist=0.3+0.2*S
            ax.add_patch(plt.matplotlib.patches.Circle((mcx-mdist,mcy),0.15,color='#FFD700',alpha=0.7,zorder=7))
            ax.add_patch(plt.matplotlib.patches.Circle((mcx+mdist,mcy),0.15,color='#FFD700',alpha=0.7,zorder=7))
            ax.plot([mcx-mdist,mcx+mdist],[mcy,mcy],color='#FFD700',lw=1.5,alpha=0.6,zorder=6)
            ax.text(mcx,mcy-0.8,TXT('جزيء (كيمياء)','Molecule'),color='#FFD700',fontsize=6,ha='center',alpha=0.8,fontweight='bold')

            # الخلية
            ccx,ccy=24.2,3.2
            ax.add_patch(plt.matplotlib.patches.Circle((ccx,ccy),0.35+0.45*S,color='#0F8',alpha=0.35,zorder=7,ec='#0F8',lw=1))
            ax.add_patch(plt.matplotlib.patches.Circle((ccx,ccy),0.1+0.15*S,color='white',alpha=0.8,zorder=8))
            ax.text(ccx,ccy-1.1,TXT('الخلية (بيولوجيا)','Cell'),color='#0F8',fontsize=6,ha='center',alpha=0.8,fontweight='bold')

            # النجوم
            if N_curr > 0:
                star_colors = []
                for i in range(N_curr):
                    wv, bv = sw[i], sb[i]
                    if wv>=0.55 and bv>=0.55: star_colors.append('#FFD700')
                    elif wv>=0.55 and bv<0.45: star_colors.append('#E0E0E0')
                    elif wv<0.45 and bv>=0.55: star_colors.append('#FF5252')
                    elif wv<0.45 and bv<0.45: star_colors.append('#FFB6C1')
                    else: star_colors.append('#888')
                ax.scatter(sx, sy, s=35, c=star_colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)

            # الجزيئات الكيميائية مع الروابط
            if M_curr > 0:
                chem_colors = []
                for i in range(M_curr):
                    cw, cb = chem_w[i], chem_b[i]
                    if cw>=0.55 and cb>=0.55: chem_colors.append('#FFD700')
                    elif cw>=0.55 and cb<0.45: chem_colors.append('#E0E0E0')
                    elif cw<0.45 and cb>=0.55: chem_colors.append('#FF5252')
                    elif cw<0.45 and cb<0.45: chem_colors.append('#FFB6C1')
                    else: chem_colors.append('#888')
                ax.scatter(chem_x, chem_y, s=25, c=chem_colors, alpha=0.8, edgecolors='white', linewidths=0.4, zorder=6)
                bonds = []
                for i in range(M_curr):
                    for j in range(i+1, M_curr):
                        d = np.sqrt((chem_x[i]-chem_x[j])**2 + (chem_y[i]-chem_y[j])**2)
                        si = chem_w[i]*chem_b[i]
                        sj = chem_w[j]*chem_b[j]
                        if d < 2.0 and si > 0.4 and sj > 0.4:
                            bonds.append((i, j, min(si, sj)))
                for (i, j, st) in bonds:
                    ax.plot([chem_x[i], chem_x[j]], [chem_y[i], chem_y[j]], color='#FFD700', lw=0.5+1.0*st, alpha=0.3+0.5*st, zorder=4)

            # الميزان الأخروي الخفي
            akh_x, akh_y, akh_scale = cx, cy, 12.0
            hasanat = W * 200
            sayyiat = (1 - B) * 200
            total_deeds = hasanat + sayyiat
            max_deeds = 600
            akh_alpha = min(0.25, total_deeds / max_deeds * 0.25)
            akh_flicker = 0.6 + 0.4 * np.sin(frame * 0.03)
            akh_alpha *= akh_flicker

            # عمود
            ax.plot([akh_x, akh_x], [1, 18], color='#FFD700', lw=0.3, alpha=akh_alpha*0.5, zorder=0, ls='-')
            # عارضة
            akh_balance = (hasanat - sayyiat) / max(hasanat + sayyiat, 1)
            ax.plot([akh_x-akh_scale, akh_x+akh_scale], [17.5-akh_balance*2.5, 17.5+akh_balance*2.5], color='#FFD700', lw=0.4, alpha=akh_alpha*1.2, zorder=0)
            # سلاسل
            lpy = 7 - akh_balance * 2.5
            rpy = 7 + akh_balance * 2.5
            ax.plot([akh_x-akh_scale, akh_x-akh_scale], [17.5-akh_balance*2.5, lpy], color='#FFD700', lw=0.2, alpha=akh_alpha*0.8, zorder=0, ls=':')
            ax.plot([akh_x+akh_scale, akh_x+akh_scale], [17.5+akh_balance*2.5, rpy], color='#FFD700', lw=0.2, alpha=akh_alpha*0.8, zorder=0, ls=':')
            # كفتان
            ax.add_patch(plt.matplotlib.patches.Circle((akh_x-akh_scale, lpy), 2.5, color='#FFF', alpha=akh_alpha*0.5, zorder=0, fill=False, lw=0.3, ls='--'))
            ax.add_patch(plt.matplotlib.patches.Circle((akh_x+akh_scale, rpy), 2.5, color='#FFF', alpha=akh_alpha*0.5, zorder=0, fill=False, lw=0.3, ls='--'))
            # أرقام
            ax.text(akh_x-akh_scale, lpy-3.2, f'{hasanat:.0f}', color='white', fontsize=5, ha='center', alpha=akh_alpha*0.4, zorder=0)
            ax.text(akh_x+akh_scale, rpy-3.2, f'{sayyiat:.0f}', color='white', fontsize=5, ha='center', alpha=akh_alpha*0.4, zorder=0)
            # هالة
            ax.add_patch(plt.matplotlib.patches.Circle((akh_x, akh_y), akh_scale+4+2*np.sin(frame*0.02), color='#FFD700', alpha=akh_alpha*0.25, zorder=0, fill=False, lw=0.2))
            # أشعة
            n_rays = 24
            for i in range(n_rays):
                angle = i * 2 * np.pi / n_rays
                rs = 2
                re = akh_scale + 5 + 2 * np.sin(frame * 0.02 + i)
                xs = akh_x + rs * np.cos(angle)
                ys = akh_y + rs * np.sin(angle)
                xe = akh_x + re * np.cos(angle)
                ye = akh_y + re * np.sin(angle)
                ax.plot([xs, xe], [ys, ye], color='#FFD700', lw=0.15, alpha=akh_alpha*0.12, zorder=0)
            # عين
            ax.add_patch(plt.matplotlib.patches.Circle((akh_x, akh_y), 0.3, color='#FFD700', alpha=akh_alpha*0.4, zorder=0, fill=True))
            ax.add_patch(plt.matplotlib.patches.Circle((akh_x, akh_y), 1.2+0.5*np.sin(frame*0.05), color='#FFD700', alpha=akh_alpha*0.3, zorder=0, fill=False, lw=0.2))

            # لوحة الإثبات
            pax = ax.inset_axes([0.5, 0.02, 0.46, 0.10])
            pax.set_xlim(0, 300); pax.set_ylim(0, 1.05)
            pax.set_title(TXT('S (ذهب) → E (سماوي) – الاستدراج', 'S (Gold) → E (Cyan) – Istidraj'), color='white', fontsize=7)
            pax.tick_params(colors='white', labelsize=4); pax.grid(True, alpha=0.12)
            if list(hist_S):
                pax.plot(list(hist_x), list(hist_S), color='#FFD700', lw=2)
                pax.plot(list(hist_x), list(hist_E), color='#0FF', lw=1.5)

            # شريط الحالة
            if N_curr > 0:
                ng = np.sum((sw>=0.55)&(sb>=0.55))
                nw = np.sum((sw>=0.55)&(sb<0.45))
                nr = np.sum((sw<0.45)&(sb>=0.55))
                npk = np.sum((sw<0.45)&(sb<0.45))
                nb = len(bonds) if M_curr > 0 else 0
                ax.text(14, 1.2, f'{phase} | 🟡{ng} ⚪{nw} 🔴{nr} 🩷{npk} | ⚗️{nb} | S={S:.2f} E={E:.2f}', color='white', fontsize=10, ha='center', fontweight='bold')

            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, facecolor='#000010')
            buf.seek(0)
            st.session_state.live_image = buf
            plt.close(fig)
            time.sleep(live_speed)
            st.rerun()

        except Exception as e:
            st.error(f"خطأ في المحاكاة: {e}")
            st.session_state.live_run = False

    elif st.session_state.live_init and 'live_image' in st.session_state:
        st.image(st.session_state.live_image, caption=TXT("آخر حالة", "Last State"), use_column_width=True)
        st.info(TXT("اضغط ▶️ تشغيل", "Press ▶️ Run"))
    else:
        st.info(TXT("اضغط ▶️ تشغيل لبدء المحاكاة", "Press ▶️ Run to start"))

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

print("✅ المرحلة الرابعة مكتملة: المشهد الحي المتكامل مع الذرة والجزيء والخلية والميزان الأخروي الخفي، والتذييل")
print("✅✅✅ تم بناء المنصة الذهبية – الدين القيم – بكافة أركانها وأدواتها ولوازمها بنجاح!")
