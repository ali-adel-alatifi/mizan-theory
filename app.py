import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import deque
import random
import time
from io import BytesIO
import json
import warnings
warnings.filterwarnings('ignore')

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
# تسميات المؤشرات (عربي)
# =============================================
W_LABELS_AR = [
    "الصلاة", "الزكاة والصدقات", "الولاء لله ورسوله والمؤمنين",
    "تحكيم الشريعة", "العدل", "الشورى"
]

B_LABELS_AR = [
    "البراءة من الطاغوت", "الرحمة والعطاء (الماعون)",
    "الأمر بالمعروف", "النهي عن المنكر", "النزاهة ومكافحة الفساد"
]

E_LABELS_AR = [
    "السيادة والاستقلال", "الاكتفاء الذاتي",
    "الإنتاج الزراعي", "الإنتاج الصناعي", "القوة العسكرية"
]

E_LETTERS = ['م', 'ق', 'ك', 'ص', 'ر']

# تفصيل الصناعة (كهيعص)
IND_LABELS_AR = [
    "التصميم والهندسة (ك)", "التصنيع والتشكيل (هـ)",
    "التطوير والتحسين (ي)", "البحث والتطوير (ع)", "الجودة والاستدامة (ص)"
]
IND_LETTERS = ['ك', 'هـ', 'ي', 'ع', 'ص']

# =============================================
# تسميات المؤشرات (إنجليزي)
# =============================================
W_LABELS_EN = [
    "Prayer", "Zakat & Charity", "Loyalty to Allah, Messenger & Believers",
    "Applying Sharia", "Justice", "Consultation (Shura)"
]

B_LABELS_EN = [
    "Disavowal of Taghut", "Mercy & Giving (Al-Ma'un)",
    "Enjoining Good", "Forbidding Evil", "Integrity & Anti-Corruption"
]

E_LABELS_EN = [
    "Sovereignty & Independence", "Self-Sufficiency",
    "Agricultural Production", "Industrial Production", "Military Power"
]

IND_LABELS_EN = [
    "Design & Engineering (K)", "Manufacturing & Forming (H)",
    "Development & Improvement (Y)", "Research & Development (A)",
    "Quality & Sustainability (S)"
]

def get_labels(category):
    """إرجاع التسميات حسب اللغة المختارة"""
    if LANG == "ar":
        labels = {
            "W": W_LABELS_AR, "B": B_LABELS_AR,
            "E": E_LABELS_AR, "I": IND_LABELS_AR
        }
    else:
        labels = {
            "W": W_LABELS_EN, "B": B_LABELS_EN,
            "E": E_LABELS_EN, "I": IND_LABELS_EN
        }
    return labels.get(category, [])

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
        return (0, 
                TXT("بوابة الشرك", "Shirk Gate"),
                TXT("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾ – كل عمل محبط",
                    "⚠️ Unforgivable: 'Allah does not forgive association with Him' – All deeds nullified"),
                "🔴")

    # البوابة 1: بوابة الماعون (الماعون: 7)
    if B2 <= 0:
        return (-1,
                TXT("بوابة الماعون", "Al-Ma'un Gate"),
                TXT("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾",
                    "⚠️ Collapse: 'So woe to those who pray... who withhold simple assistance'"),
                "🔴")

    # البوابة 2: بوابة الإخلاص (النور: 55)
    if W_raw > 0 and B1 <= 0:
        return (0,
                TXT("بوابة الإخلاص", "Sincerity Gate"),
                TXT("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي وَلَا يُشْرِكُونَ بِي شَيْئًا﴾",
                    "⚠️ Void worship: 'They worship Me, not associating anything with Me'"),
                "🟡")

    # البوابة 3: بوابة الوعد (الانشقاق: 25)
    if W_raw > 0 and B_raw > 0:
        return (1,
                TXT("بوابة الوعد", "Promise Gate"),
                TXT("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾",
                    "🟢 Stability: 'For them is a reward uninterrupted'"),
                "🟢")

    return None, None, None, None

def calculate_S(W_raw, B_raw, E_raw, W_pure, B2, B1):
    """حساب الثبات S باستخدام المعادلة الكاملة"""
    # تحقق من المحكمة العليا أولاً
    S_gate, gate_name, gate_msg, gate_color = supreme_court(W_raw, B_raw, W_pure, B2, B1)
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
        
        prompt = f"""أنت محلل خبير في نظرية الميزان (S = W × B). اقرأ وصف الكيان وأعد تقديرات رقمية بصيغة JSON فقط.

W (الولاء) – 6 مؤشرات بين -1 و+1:
1. الصلاة: مدى إقامة الصلاة
2. الزكاة والصدقات: مدى تفعيل الزكاة والتكافل
3. الولاء لله ورسوله والمؤمنين: مدى التماسك
4. تحكيم الشريعة: مدى تطبيق الشريعة
5. العدل: مدى سيادة العدل
6. الشورى: مدى تطبيق الشورى

B (البراءة) – 5 مؤشرات بين -1 و+1:
1. البراءة من الطاغوت
2. الرحمة والعطاء (الماعون)
3. الأمر بالمعروف
4. النهي عن المنكر
5. النزاهة ومكافحة الفساد

E (التمكين) – 5 مؤشرات بين -1 و+1:
1. السيادة والاستقلال
2. الاكتفاء الذاتي
3. الإنتاج الزراعي
4. الإنتاج الصناعي
5. القوة العسكرية

I (تفصيل الصناعة) – 5 مؤشرات بين -1 و+1:
1. التصميم والهندسة
2. التصنيع والتشكيل
3. التطوير والتحسين
4. البحث والتطوير
5. الجودة والاستدامة

W_pure: true/false (هل الولاء خالص لله؟)

analysis: تحليل موجز بالعربية

مثال للصيغة المطلوبة:
{{"W":[0.5,0.4,0.7,0.3,0.6,0.2],"B":[0.6,0.5,0.4,0.3,0.4],"E":[0.5,0.4,0.6,0.4,0.7],"I":[0.3,0.4,0.5,0.2,0.4],"W_pure":true,"analysis":"تحليل موجز"}}

الوصف: {user_text}"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت محلل خبير. ترد بصيغة JSON فقط بدون أي نص إضافي."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        
        # تنظيف النص من علامات markdown
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

print("✅ المرحلة الأولى مكتملة: الأساسيات، المحكمة العليا، دوال الحساب، الذكاء الاصطناعي")

# =============================================
# المرحلة الثانية: الشريط الجانبي والمنزلقات
# =============================================

# تهيئة حالة الجلسة للقيم الافتراضية
if "slider_values" not in st.session_state:
    st.session_state.slider_values = {
        "W1": 0.0, "W2": 0.0, "W3": 0.0, "W4": 0.0, "W5": 0.0, "W6": 0.0,
        "B1": 0.0, "B2": 0.0, "B3": 0.0, "B4": 0.0, "B5": 0.0,
        "E1": 0.0, "E2": 0.0, "E3": 0.0, "E4": 0.0, "E5": 0.0,
        "I1": 0.0, "I2": 0.0, "I3": 0.0, "I4": 0.0, "I5": 0.0,
        "W_pure": True
    }

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

with st.sidebar:
    # شعار المنصة
    st.markdown(f"""
    <div style='text-align:center;padding:10px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <h2 style='color:#FFD700;margin:0;'>⚖️ {TXT('المختبر القرآني', 'The Quranic Lab')}</h2>
        <p style='color:#e0e0e0;font-size:12px;margin:5px 0;'>S = W × B</p>
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

    # متغيرات المنزلقات (قيم افتراضية)
    W1 = W2 = W3 = W4 = W5 = W6 = 0.0
    B1 = B2 = B3 = B4 = B5 = 0.0
    E1 = E2 = E3 = E4 = E5 = 0.0
    I1 = I2 = I3 = I4 = I5 = 0.0
    W_pure = True

    if TXT("يدوي", "Manual") in mode:
        # الحصول على التسميات المناسبة
        W_L = get_labels("W")
        B_L = get_labels("B")
        E_L = get_labels("E")
        I_L = get_labels("I")

        # مؤشرات الولاء (W)
        with st.expander(TXT("🤍 مؤشرات الولاء (W)", "🤍 Loyalty Indicators (W)"), expanded=True):
            W1 = st.slider(W_L[0], -1.0, 1.0, 
                          st.session_state.slider_values["W1"], 0.1, key="s_W1")
            W2 = st.slider(W_L[1], -1.0, 1.0, 
                          st.session_state.slider_values["W2"], 0.1, key="s_W2")
            W3 = st.slider(W_L[2], -1.0, 1.0, 
                          st.session_state.slider_values["W3"], 0.1, key="s_W3")
            W4 = st.slider(W_L[3], -1.0, 1.0, 
                          st.session_state.slider_values["W4"], 0.1, key="s_W4")
            W5 = st.slider(W_L[4], -1.0, 1.0, 
                          st.session_state.slider_values["W5"], 0.1, key="s_W5")
            W6 = st.slider(W_L[5], -1.0, 1.0, 
                          st.session_state.slider_values["W6"], 0.1, key="s_W6")
            
            W_pure = st.checkbox(
                TXT("الإخلاص لله (عدم الشرك)", "Sincerity to Allah (No Shirk)"),
                value=st.session_state.slider_values["W_pure"],
                help=TXT("هل الولاء خالص لله وحده؟", "Is loyalty purely for Allah alone?")
            )
            
            # تحديث حالة الجلسة
            st.session_state.slider_values.update({
                "W1": W1, "W2": W2, "W3": W3, "W4": W4, "W5": W5, "W6": W6,
                "W_pure": W_pure
            })

        # مؤشرات البراءة (B)
        with st.expander(TXT("❤️ مؤشرات البراءة (B)", "❤️ Disavowal Indicators (B)"), expanded=True):
            B1 = st.slider(B_L[0], -1.0, 1.0, 
                          st.session_state.slider_values["B1"], 0.1, key="s_B1")
            B2 = st.slider(B_L[1], -1.0, 1.0, 
                          st.session_state.slider_values["B2"], 0.1, key="s_B2",
                          help=TXT("﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾",
                                  "'So woe to those who pray... who withhold simple assistance'"))
            B3 = st.slider(B_L[2], -1.0, 1.0, 
                          st.session_state.slider_values["B3"], 0.1, key="s_B3")
            B4 = st.slider(B_L[3], -1.0, 1.0, 
                          st.session_state.slider_values["B4"], 0.1, key="s_B4")
            B5 = st.slider(B_L[4], -1.0, 1.0, 
                          st.session_state.slider_values["B5"], 0.1, key="s_B5")
            
            st.session_state.slider_values.update({
                "B1": B1, "B2": B2, "B3": B3, "B4": B4, "B5": B5
            })

        # مؤشرات التمكين (E)
        with st.expander(TXT("🌐 مؤشرات التمكين (E)", "🌐 Empowerment Indicators (E)"), expanded=True):
            E1 = st.slider(f"{E_L[0]} (م={LETTERS_DB['م']})", -1.0, 1.0, 
                          st.session_state.slider_values["E1"], 0.1, key="s_E1")
            E2 = st.slider(f"{E_L[1]} (ق={LETTERS_DB['ق']})", -1.0, 1.0, 
                          st.session_state.slider_values["E2"], 0.1, key="s_E2")
            E3 = st.slider(f"{E_L[2]} (ك={LETTERS_DB['ك']})", -1.0, 1.0, 
                          st.session_state.slider_values["E3"], 0.1, key="s_E3")
            E4_raw = st.slider(f"{E_L[3]} ({TXT('مجمل', 'Overall')})", -1.0, 1.0, 
                              st.session_state.slider_values["E4"], 0.1, key="s_E4_raw")
            E5 = st.slider(f"{E_L[4]} (ر={LETTERS_DB['ر']})", -1.0, 1.0, 
                          st.session_state.slider_values["E5"], 0.1, key="s_E5")
            
            st.session_state.slider_values.update({
                "E1": E1, "E2": E2, "E3": E3, "E4": E4_raw, "E5": E5
            })

        # تفصيل الصناعة (كهيعص)
        with st.expander(TXT("🏭 تفصيل الصناعة (كهيعص)", "🏭 Industry Breakdown (كهيعص)"), expanded=False):
            st.caption(TXT("تفكيك مؤشر الصناعة إلى مكوناته الحرفية",
                          "Breaking down the industry indicator into its letter components"))
            I1 = st.slider(I_L[0], -1.0, 1.0, 
                          st.session_state.slider_values["I1"], 0.1, key="s_I1")
            I2 = st.slider(I_L[1], -1.0, 1.0, 
                          st.session_state.slider_values["I2"], 0.1, key="s_I2")
            I3 = st.slider(I_L[2], -1.0, 1.0, 
                          st.session_state.slider_values["I3"], 0.1, key="s_I3")
            I4 = st.slider(I_L[3], -1.0, 1.0, 
                          st.session_state.slider_values["I4"], 0.1, key="s_I4")
            I5 = st.slider(I_L[4], -1.0, 1.0, 
                          st.session_state.slider_values["I5"], 0.1, key="s_I5")
            
            # حساب المرجح للصناعة
            i_vals = [I1, I2, I3, I4, I5]
            i_weights = [LETTERS_DB[l] for l in IND_LETTERS]
            E4 = np.average(i_vals, weights=i_weights)
            
            st.session_state.slider_values.update({
                "I1": I1, "I2": I2, "I3": I3, "I4": I4, "I5": I5
            })

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
                with st.spinner(TXT("جاري التحليل بالذكاء الاصطناعي... قد يستغرق ذلك بضع ثوانٍ.", 
                                   "Analyzing with AI... This may take a few seconds.")):
                    ai_result = call_ai_api(ai_text)
                    if ai_result:
                        st.session_state.ai_result = ai_result
                        st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
                        if "analysis" in ai_result:
                            st.info(ai_result["analysis"])

        # إذا كان هناك نتيجة سابقة من الذكاء الاصطناعي، استخدمها
        if st.session_state.ai_result is not None:
            r = st.session_state.ai_result
            W1, W2, W3, W4, W5, W6 = r.get("W", [0.0]*6)
            B1, B2, B3, B4, B5 = r.get("B", [0.0]*5)
            E1, E2, E3, E4_raw, E5 = r.get("E", [0.0]*5)
            I1, I2, I3, I4, I5 = r.get("I", [0.0]*5)
            W_pure = r.get("W_pure", True)
            
            # حساب المرجح للصناعة
            i_vals = [I1, I2, I3, I4, I5]
            i_weights = [LETTERS_DB[l] for l in IND_LETTERS]
            E4 = np.average(i_vals, weights=i_weights)

    # زر إعادة الضبط
    st.markdown("---")
    if st.button(TXT("🔄 إعادة ضبط جميع القيم", "🔄 Reset All Values"), use_container_width=True):
        st.session_state.slider_values = {
            "W1": 0.0, "W2": 0.0, "W3": 0.0, "W4": 0.0, "W5": 0.0, "W6": 0.0,
            "B1": 0.0, "B2": 0.0, "B3": 0.0, "B4": 0.0, "B5": 0.0,
            "E1": 0.0, "E2": 0.0, "E3": 0.0, "E4": 0.0, "E5": 0.0,
            "I1": 0.0, "I2": 0.0, "I3": 0.0, "I4": 0.0, "I5": 0.0,
            "W_pure": True
        }
        st.session_state.ai_result = None
        st.rerun()

# =============================================
# المحرك الوجودي – الحساب
# =============================================

# حساب المتوسطات الخام
W_raw = np.mean([W1, W2, W3, W4, W5, W6])
B_raw = np.mean([B1, B2, B3, B4, B5])

# حساب E المرجح بقيم الحروف
E_vals = [E1, E2, E3, E4, E5]
E_weights_list = [LETTERS_DB[l] for l in E_LETTERS]
E_raw = np.average(E_vals, weights=E_weights_list)

# حساب S والبوابات
S_final, E_norm, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
    W_raw, B_raw, E_raw, W_pure, B2, B1
)

print("✅ المرحلة الثانية مكتملة: الشريط الجانبي، المنزلقات، الذكاء الاصطناعي، الحسابات")

# =============================================
# المرحلة الثالثة: العنوان، لوحة القيادة، التبويبات
# =============================================

# العنوان الرئيسي
st.markdown(f"""
<div style="text-align:center;padding:20px 0 10px 0;">
    <h1 style="color:#FFD700;font-size:2.5em;margin-bottom:0;">⚖️ {TXT('المختبر القرآني', 'The Quranic Lab')}</h1>
    <h2 style="color:#FFD700;font-size:1.3em;margin-top:0;">{TXT('النظام المتكامل – من "كُن" إلى الكون', 'The Integrated System – From "Be" to the Universe')}</h2>
    <p style="color:#CCC;">﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>
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
        quadrant_name = ""
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
    
    W_vals = [W1, W2, W3, W4, W5, W6]
    B_vals = [B1, B2, B3, B4, B5]
    E_v = [E1, E2, E3, E4, E5]
    
    wW = np.argmin(W_vals)
    wB = np.argmin(B_vals)
    wE = np.argmin(E_v)
    
    W_L = get_labels("W")
    B_L = get_labels("B")
    E_L = get_labels("E")
    
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
            f"الأولوية: سد فجوة الاستدراج ({istidraj_gap:.2f}) عبر رفع '{B_L[wB]}' أو '{W_L[wW]}'.",
            f"Priority: Close the Istidraj gap ({istidraj_gap:.2f}) by raising '{B_L[wB]}' or '{W_L[wW]}'."
        ))
    else:
        st.info(TXT(
            f"للتقدم نحو مقام إبراهيم: عزز '{W_L[wW]}' و'{B_L[wB]}' و'{E_L[wE]}'.",
            f"To advance to the Station of Abraham: strengthen '{W_L[wW]}', '{B_L[wB]}' and '{E_L[wE]}'."
        ))
    
    # جدول المؤشرات
    st.markdown(TXT("### 📊 تفصيل المؤشرات", "### 📊 Indicator Details"))
    
    df_W = pd.DataFrame({TXT('المؤشر', 'Indicator'): W_L, TXT('القيمة', 'Value'): W_vals})
    df_B = pd.DataFrame({TXT('المؤشر', 'Indicator'): B_L, TXT('القيمة', 'Value'): B_vals})
    df_E = pd.DataFrame({TXT('المؤشر', 'Indicator'): E_L, TXT('القيمة', 'Value'): E_v})
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.dataframe(
            df_W.style.format({TXT('القيمة', 'Value'): '{:+.2f}'})
            .background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'),
            hide_index=True
        )
    with col_b:
        st.dataframe(
            df_B.style.format({TXT('القيمة', 'Value'): '{:+.2f}'})
            .background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'),
            hide_index=True
        )
    with col_c:
        st.dataframe(
            df_E.style.format({TXT('القيمة', 'Value'): '{:+.2f}'})
            .background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'),
            hide_index=True
        )

# =============================================
# تبويب 4: المعجم الهندسي
# =============================================
with tab4:
    st.subheader(TXT("📖 المعجم الهندسي – الحروف وقيمها", "📖 Geometric Lexicon – Letters & Values"))
    st.markdown(TXT(
        "هذا المعجم يربط كل حرف من الحروف العربية بقيمته العددية (حساب الجمل) ودوره الوجودي في معادلة الميزان.",
        "This lexicon links each Arabic letter to its numerical value (Abjad calculation) and its existential role in the Mizan equation."
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
            {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
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
    <div style="text-align:center;color:#CCC;line-height:2;">
    > "{TXT('هل يوجد قانون واحد يحكم الذرة والحضارة؟', 'Is there a single law governing the atom and civilization?')}"<br>
    > {TXT('هذا هو نموذج الميزان الذي يثبت أن', 'This is the Mizan Model that proves that')} <b style="color:#FFD700;">S = W × B</b>
    <br><br>
    <b style="color:#FFD700;">﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا...﴾ — الروم 30</b>
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
        col_set1, col_set2, col_set3 = st.columns(3)
        with col_set1:
            live_speed = st.slider(TXT("سرعة المحاكاة", "Simulation Speed"), 0.01, 0.2, 0.08, 0.01, key="live_speed")
        with col_set2:
            live_stars = st.slider(TXT("عدد النجوم", "Number of Stars"), 100, 500, 300, 50, key="live_stars")
        with col_set3:
            live_trail = st.slider(TXT("طول مسار الكواكب", "Planet Trail Length"), 50, 300, 150, 10, key="live_trail")
    
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
            for key in ["live_init", "live_run", "live_cx", "live_cy", "live_sx", "live_sy", 
                       "live_sw", "live_sb", "live_W", "live_B", "live_E", "live_S", "live_phase",
                       "live_aW", "live_aB", "live_trail_Wx", "live_trail_Wy", 
                       "live_trail_Bx", "live_trail_By", "live_hist_S", "live_hist_E",
                       "live_hist_x", "live_frame", "live_image"]:
                if key in st.session_state:
                    del st.session_state[key]
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
        st.session_state.live_phase = TXT("توازن", "Balance")
        
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
        N_curr = len(sx)
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
        
        # صدمات عشوائية
        if random.random() < 0.005:
            affected = np.random.choice(N_curr, size=int(N_curr * 0.2), replace=False)
            sw[affected] *= random.uniform(0.5, 0.8)
            sb[affected] *= random.uniform(0.5, 0.8)
            phase = TXT("💥 صدمة", "💥 Shock")
        
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
        if S > 0.7: phase = TXT("🌟 ثبات", "🌟 Stability")
        elif S > 0.4: phase = TXT("⚖️ توازن", "⚖️ Balance")
        elif S > 0.2: phase = TXT("⚠️ اهتزاز", "⚠️ Shaking")
        elif S > 0.05: phase = TXT("📉 انهيار", "📉 Collapse")
        else: phase = TXT("💀 قاع", "💀 Bottom")
        
        if E > S + 0.2: phase = TXT("🚨 استدراج", "🚨 Istidraj")
        
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
        sx += np.random.uniform(-0.05, 0.05, N_curr) * instability
        sy += np.random.uniform(-0.05, 0.05, N_curr) * instability
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
        ax.text(cx, cy - 2.5, f'S={S:.2f}', color='#FFD700', fontsize=10, ha='center', fontweight='bold')
        
        # هالة التمكين E
        halo_alpha = 0.25 * (1 - min(E, 1)) + 0.04
        ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 0.5 + 14 * E, color='#00FFFF', alpha=halo_alpha, zorder=7))
        
        # الغشاء
        ax.add_patch(plt.matplotlib.patches.Circle((cx, cy), 8.5, color='#00FF88', alpha=0.1, fill=False, lw=2, zorder=2))
        
        # الذرة (أسفل اليسار)
        atom_center = (3.5, 3.5)
        ax.add_patch(plt.matplotlib.patches.Circle(atom_center, 0.15 + 0.25 * S, color='#4488FF', alpha=0.8, zorder=7))
        ax.add_patch(plt.matplotlib.patches.Circle(atom_center, 0.5 + 0.3 * S, color='#00FFFF', alpha=0.15, fill=False, lw=0.5, zorder=6))
        ax.text(atom_center[0], atom_center[1] - 1.2, TXT('الذرة (فيزياء)', 'Atom (Physics)'), 
                color='#4488FF', fontsize=6, ha='center', alpha=0.8)
        
        # الخلية (أسفل اليمين)
        cell_center = (24.5, 3.5)
        ax.add_patch(plt.matplotlib.patches.Circle(cell_center, 0.35 + 0.4 * S, color='#00FF88', alpha=0.3, zorder=7, ec='#00FF88', lw=1))
        ax.add_patch(plt.matplotlib.patches.Circle(cell_center, 0.1 + 0.12 * S, color='white', alpha=0.8, zorder=8))
        ax.text(cell_center[0], cell_center[1] - 1.2, TXT('الخلية (بيولوجيا)', 'Cell (Biology)'), 
                color='#00FF88', fontsize=6, ha='center', alpha=0.8)
        
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
        
        # عمود الميزان
        ax.plot([mizan_x, mizan_x], [mizan_y - 2.5, mizan_y + 1], color='#FFD700', lw=1.5, alpha=0.6, zorder=10)
        
        # العارضة
        balance_ratio = (hasanat - sayyiat) / max(hasanat + sayyiat, 1)
        ax.plot([mizan_x - 1.5, mizan_x + 1.5], [mizan_y, mizan_y], color='#FFD700', lw=2, alpha=0.7, zorder=10)
        
        # السلاسل
        left_y = mizan_y - 1.0 + min(hasanat / 30, 0.8)
        right_y = mizan_y - 1.0 + min(sayyiat / 30, 0.8)
        ax.plot([mizan_x - 1.5, mizan_x - 1.5], [mizan_y, left_y], color='#FFD700', lw=1, alpha=0.5, zorder=9)
        ax.plot([mizan_x + 1.5, mizan_x + 1.5], [mizan_y, right_y], color='#FFD700', lw=1, alpha=0.5, zorder=9)
        
        # كفتا الميزان
        ax.add_patch(plt.matplotlib.patches.FancyBboxPatch(
            (mizan_x - 2.2, left_y - 0.3), 1.4, 0.6, boxstyle="round,pad=0.05",
            color='white', alpha=0.3, zorder=8, ec='white', lw=0.7))
        ax.add_patch(plt.matplotlib.patches.FancyBboxPatch(
            (mizan_x + 0.8, right_y - 0.3), 1.4, 0.6, boxstyle="round,pad=0.05",
            color='#220000', alpha=0.3, zorder=8, ec='#FF3333', lw=0.7))
        
        # قيم الحسنات والسيئات
        ax.text(mizan_x - 1.5, left_y - 0.8, f'{hasanat:.0f}', color='white', fontsize=7, ha='center', fontweight='bold', alpha=0.7)
        ax.text(mizan_x + 1.5, right_y - 0.8, f'{sayyiat:.0f}', color='#FF3333', fontsize=7, ha='center', fontweight='bold', alpha=0.7)
        ax.text(mizan_x, mizan_y + 1.5, TXT('الميزان', 'Al-Mizan'), color='#FFD700', fontsize=8, ha='center', fontweight='bold')
        
        # لوحة الإثبات
        pax = ax.inset_axes([0.5, 0.02, 0.46, 0.10])
        pax.set_xlim(0, 300)
        pax.set_ylim(0, 1.05)
        pax.set_title(TXT('S (ذهب) → E (سماوي) – الاستدراج', 'S (Gold) → E (Cyan) – Istidraj'), color='white', fontsize=7)
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
        st.image(st.session_state.live_image, caption=TXT("آخر حالة للمشهد الحي", "Last Live Scene State"), use_column_width=True)
        st.info(TXT("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة.", "Press ▶️ Run Live Scene to start the simulation."))
    else:
        st.info(TXT("اضغط ▶️ تشغيل المشهد الحي لبدء المحاكاة الديناميكية.", "Press ▶️ Run Live Scene to start the dynamic simulation."))

# زر تحميل صورة المشهد الحي
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
    <p style="font-size:0.8em;margin-top:10px;">{TXT('جميع الحقوق محفوظة', 'All Rights Reserved')} | MIT License</p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الرابعة مكتملة: المشهد الحي، الذرة، الخلية، الميزان الأخروي، التذييل")
print("✅✅✅ تم بناء المختبر القرآني بكافة أركانه وأدواته ولوازمه بنجاح!")
