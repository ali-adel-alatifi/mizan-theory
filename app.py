import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random
import time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ================================================================
# إعداد الصفحة
# ================================================================
st.set_page_config(
    page_title="المنصة الذهبية – The Golden Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# حقوق المؤلف والترخيص
# ================================================================
__AUTHOR__ = "علي عادل العاطفي | Ali Adel Alatifi"
__YEAR__ = 2026
__LICENSE__ = "MIT License"
__VERSION__ = "2.0.0 – The Golden Platform (The New Science)"
__SIGNATURE__ = "⚖️ S = W × B"

# ================================================================
# النظام اللغوي
# ================================================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(ar_text, en_text):
    return ar_text if LANG == "ar" else en_text

def tl(letter_dict):
    return letter_dict["label"][LANG]

# ================================================================
# قاعدة بيانات الحروف الـ 28 الأصلية
# ================================================================
MIZAN_LETTERS = {
    "light": {
        "أ": {"value": 1,   "label": {"ar":"الوحدانية","en":"Oneness"},        "aya": "إِيَّاكَ نَعْبُدُ"},
        "ل": {"value": 30,  "label": {"ar":"المُلك","en":"Sovereignty"},       "aya": "إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ"},
        "م": {"value": 40,  "label": {"ar":"الجمع","en":"Gathering"},          "aya": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ"},
        "ر": {"value": 200, "label": {"ar":"اليقظة","en":"Vigilance"},         "aya": "فَإِذَا فَرَغْتَ فَانصَبْ"},
        "ك": {"value": 20,  "label": {"ar":"الأمر","en":"Command"},            "aya": "كُن فَيَكُونُ"},
        "هـ": {"value": 5,   "label": {"ar":"الهوية","en":"Identity"},          "aya": "وَاجْتَنِبُوا الطَّاغُوتَ"},
        "ي": {"value": 10,  "label": {"ar":"الاستجابة","en":"Response"},       "aya": "اسْتَجِيبُوا لِلَّهِ وَلِلرَّسُولِ"},
        "ع": {"value": 70,  "label": {"ar":"الإدراك","en":"Perception"},       "aya": "وَقُل رَّبِّ زِدْنِي عِلْمًا"},
        "ص": {"value": 90,  "label": {"ar":"الصمد","en":"The Eternal"},        "aya": "اللَّهُ الصَّمَدُ"},
        "ق": {"value": 100, "label": {"ar":"الميزان","en":"The Balance"},      "aya": "وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ"},
        "ن": {"value": 50,  "label": {"ar":"النور","en":"Light"},              "aya": "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ"},
        "س": {"value": 60,  "label": {"ar":"السمع","en":"Hearing"},            "aya": "سَمِعْنَا وَأَطَعْنَا"},
        "ح": {"value": 8,   "label": {"ar":"الحياة","en":"Life"},              "aya": "فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً"},
        "ط": {"value": 9,   "label": {"ar":"الطهارة","en":"Purity"},           "aya": "إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ"},
    },
    "neutral": {
        "ف": {"value": 80,  "label": {"ar":"فاء السببية","en":"Causative Fa"}, "role": "=",  "aya": "فَمَن يَكْفُرْ بِالطَّاغُوتِ..."},
        "و": {"value": 6,   "label": {"ar":"واو العطف","en":"Conjunctive Waw"},"role": "×/+","aya": "وَيُؤْمِن بِاللَّهِ"},
        "ب": {"value": 2,   "label": {"ar":"باء الاستعانة","en":"Instrumental Ba"},"role": "بـ","aya": "بِسْمِ اللَّهِ الرَّحْمَٰنِ"},
        "ل": {"value": 30,  "label": {"ar":"لام التعليل","en":"Purpose Lam"}, "role": "→",  "aya": "لِيَعْبُدُونِ"},
        "ت": {"value": 400, "label": {"ar":"تاء الفاعل","en":"Subject Ta"},   "role": "ف",  "aya": "قَالَتِ امْرَأَتُ فِرْعَوْنَ"},
        "ث": {"value": 500, "label": {"ar":"ثم العطف","en":"Then Tha"},       "role": "ت",  "aya": "ثُمَّ خَلَقْنَا النُّطْفَةَ"},
    },
    "dark": {
        "ظ": {"value": 900, "label": {"ar":"الظلم","en":"Injustice"},          "aya": "إِنَّ الظَّالِمِينَ لَهُمْ عَذَابٌ أَلِيمٌ"},
        "ض": {"value": 800, "label": {"ar":"الضلال","en":"Misguidance"},       "aya": "وَمَن يُضْلِلِ اللَّهُ فَمَا لَهُ مِنْ هَادٍ"},
        "غ": {"value": 1000,"label": {"ar":"الغش","en":"Fraud"},               "aya": "مَنْ غَشَّنَا فَلَيْسَ مِنَّا"},
        "ذ": {"value": 700, "label": {"ar":"الذل","en":"Humiliation"},         "aya": "أَذِلَّةٍ عَلَى الْمُؤْمِنِينَ"},
        "خ": {"value": 600, "label": {"ar":"الخيانة","en":"Betrayal"},         "aya": "لَا تَخُونُوا اللَّهَ وَالرَّسُولَ"},
        "ش": {"value": 300, "label": {"ar":"الشهوة","en":"Lust"},              "aya": "وَلَا تَتَّبِعِ الْهَوَىٰ"},
        "ز": {"value": 7,   "label": {"ar":"الزور","en":"Falsehood"},          "aya": "وَاجْتَنِبُوا قَوْلَ الزُّورِ"},
        "ج": {"value": 3,   "label": {"ar":"الجهل","en":"Ignorance"},          "aya": "بَلْ أَكْثَرُهُمْ يَجْهَلُونَ"},
    }
}

# ================================================================
# التصنيف الجديد للحروف (الفئات الست)
# ================================================================
LETTER_CATEGORIES = {
    "source": {
        "ك": {"value": 20, "role": "الأمر - التفعيل", "equation_role": "activation"},
        "ن": {"value": 50, "role": "النور - الوضوح", "equation_role": "clarity"},
    },
    "tajalli": {
        "أ": {"value": 1, "role": "الوحدانية", "affects": "unity", "equation_role": "w_boost"},
        "ل": {"value": 30, "role": "المُلك والعدل", "affects": "w", "equation_role": "w_boost"},
        "م": {"value": 40, "role": "الجمع والتماسك", "affects": "b", "equation_role": "b_boost"},
        "ر": {"value": 200, "role": "اليقظة والمراقبة", "affects": "resistance", "equation_role": "resistance"},
        "س": {"value": 60, "role": "السمع والاستجابة", "affects": "responsiveness", "equation_role": "learning_rate"},
        "ح": {"value": 8, "role": "الحياة والاستدامة", "affects": "sustainability", "equation_role": "decay_resist"},
        "ط": {"value": 9, "role": "الطهارة والمناعة", "affects": "b", "equation_role": "purification"},
    },
    "ishtirak": {
        "ع": {"value": 70, "role": "الإدراك والعلم", "affects": "w", "equation_role": "w_multiplier"},
        "ي": {"value": 10, "role": "الاستجابة والدعاء", "affects": "b", "equation_role": "b_multiplier"},
        "هـ": {"value": 5, "role": "الهوية والمعية", "affects": "e_resist", "equation_role": "e_dampener"},
        "ق": {"value": 100, "role": "الميزان والقسط", "affects": "balance", "equation_role": "normalizer"},
    },
    "dual": {
        "ص": {"value": 90, "constant_role": "الصمد", "variable_role": "الصبر والصدق", "affects": "w", "equation_role": "w_boost"},
        "ق_متغير": {"value": 100, "variable_role": "القسط والعدل", "affects": "b", "equation_role": "b_boost"},
    },
    "operators": {
        "ف": {"value": 80, "operator": "=", "role": "فاء السببية - حتمية"},
        "و": {"value": 6, "operator": "×/+", "role": "واو العطف - شرط أو جمع"},
        "ب": {"value": 2, "operator": "بـ", "role": "باء الاستعانة - غاية"},
        "ل": {"value": 30, "operator": "→", "role": "لام التعليل - اتجاه"},
    },
    "actions": {
        "ج": {"value": 3, "positive": "الجهاد والجود", "negative": "الجهل والجحود", "affects": "b"},
        "خ": {"value": 600, "positive": "الخير والخشية", "negative": "الخيانة والخذلان", "affects": "w"},
        "د": {"value": 4, "positive": "الدين والدعوة", "negative": "الدولة والغلبة", "affects": "w"},
        "ذ": {"value": 700, "positive": "الذكر والذوق", "negative": "الذل والذنب", "affects": "b"},
        "ز": {"value": 7, "positive": "الزكاة والزهد", "negative": "الزور والزيغ", "affects": "b"},
        "ش": {"value": 300, "positive": "الشكر والشجاعة", "negative": "الشهوة والشرك", "affects": "w"},
        "ت": {"value": 400, "positive": "التوبة والتقوى", "negative": "التيه", "affects": "w"},
        "ث": {"value": 500, "positive": "الثبات والثواب", "negative": "الثبور", "affects": "w"},
        "ض": {"value": 800, "positive": "الضياء", "negative": "الضلال", "affects": "b"},
        "ظ": {"value": 900, "positive": "الظفر", "negative": "الظلم", "affects": "both"},
        "غ": {"value": 1000, "positive": "الغفران", "negative": "الغش", "affects": "b"},
    }
}

# ================================================================
# دوال مساعدة
# ================================================================
def get_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    else: return '#888888'

def classify_human(W_val, B_val):
    if W_val >= 0.5 and B_val >= 0.5: return ("believer", '#FFD700')
    elif W_val < 0.5 and B_val >= 0.5: return ("disbeliever", '#FF5252')
    elif W_val < 0.5 and B_val < 0.5: return ("hypocrite", '#FFB6C1')
    else: return ("polytheist", '#FFA500')

# ================================================================
# دالة حساب الثبات – المعادلة المعممة
# ================================================================
def calc_S(W, B, E,
          q_val=100, n_val=50, k_val=20,
          tajalli_intensity=None,
          ishtirak_intensity=None,
          dual_intensity=None,
          actions_intensity=None,
          amr_val=0.5, nahy_val=0.5, adl_val=0.6, shura_val=0.5,
          riba_val=0.2, zulm_val=0.2, khianah_val=0.2):
    W_eff, B_eff = W, B
    source_factor = (k_val * n_val) / 1000.0
    S_base = W_eff * B_eff * (1 + source_factor)
    resistance = decay_resist = purity = unity = 1.0
    if tajalli_intensity:
        if 'ل' in tajalli_intensity: W_eff *= (1 + 30 * tajalli_intensity['ل'] / 1000)
        if 'م' in tajalli_intensity: B_eff *= (1 + 40 * tajalli_intensity['م'] / 1000)
        if 'ر' in tajalli_intensity: resistance = 1 + 200 * tajalli_intensity['ر'] / 1000
        if 'ح' in tajalli_intensity: decay_resist = 1 + 8 * tajalli_intensity['ح'] / 100
        if 'ط' in tajalli_intensity: purity = 1 + 9 * tajalli_intensity['ط'] / 100
        if 'أ' in tajalli_intensity: unity = 1 + 1 * tajalli_intensity['أ'] / 100
        S_base = W_eff * B_eff * (1 + source_factor) * resistance * decay_resist * purity * unity

    normalizer = 1.0
    if ishtirak_intensity:
        if 'ع' in ishtirak_intensity: W_eff *= (1 + 70 * ishtirak_intensity['ع'] / 1000)
        if 'ي' in ishtirak_intensity: B_eff *= (1 + 10 * ishtirak_intensity['ي'] / 100)
        if 'ق' in ishtirak_intensity: normalizer = 1 + 100 * ishtirak_intensity['ق'] / 1000
        S_base = W_eff * B_eff * (1 + source_factor) * normalizer

    if dual_intensity:
        if 'ص' in dual_intensity: W_eff *= (1 + 90 * dual_intensity['ص'] / 1000)
        if 'ق_متغير' in dual_intensity: B_eff *= (1 + 100 * dual_intensity['ق_متغير'] / 1000)
        S_base = W_eff * B_eff * (1 + source_factor)

    if actions_intensity:
        pos_sum = neg_sum = 0
        for letter, val in actions_intensity.items():
            if letter not in LETTER_CATEGORIES["actions"]: continue
            lv = LETTER_CATEGORIES["actions"][letter]["value"]
            aff = LETTER_CATEGORIES["actions"][letter]["affects"]
            if val > 0:
                pos_sum += val * lv
                factor = 1 + val * lv / 1000
                if aff == "w": W_eff *= factor
                elif aff == "b": B_eff *= factor
                elif aff == "both": W_eff *= (1 + val * lv / 2000); B_eff *= (1 + val * lv / 2000)
            elif val < 0:
                nv = abs(val)
                neg_sum += nv * lv
                factor = 1 - nv * lv / 1000
                if aff == "w": W_eff *= factor
                elif aff == "b": B_eff *= factor
                elif aff == "both": W_eff *= (1 - nv * lv / 2000); B_eff *= (1 - nv * lv / 2000)
        inhibitor = neg_sum / 10000
        enhancer = pos_sum / 10000
        S_base = W_eff * B_eff * (1 + source_factor) * (1 + enhancer) / (1 + max(inhibitor, 0.001))

    S_base *= (0.5 + 0.5 * (amr_val * nahy_val))
    S_base *= (0.8 + 0.4 * adl_val)
    S_base *= (0.85 + 0.3 * shura_val)
    S_base *= (1 - 0.3 * riba_val)
    S_base *= (1 - 0.25 * zulm_val)
    S_base *= (1 - 0.15 * khianah_val)
    if tajalli_intensity:
        if 'ط' in tajalli_intensity: S_base *= purity
        if 'ح' in tajalli_intensity: S_base *= decay_resist
    return np.clip(S_base, 0.001, 1.0)

# ================================================================
# قاعدة بيانات التلميحات – ربط الحروف بالعبادات والأخلاق
# ================================================================
LETTER_TOOLTIPS = {
    "taj_أ": {"ar":"الوحدانية – أصل الولاء","en":"Oneness – root of loyalty"},
    "taj_ل": {"ar":"المُلك والعدل – يقوي W (الولاء)","en":"Sovereignty & justice – boosts W"},
    "taj_م": {"ar":"الجمع والتماسك – يقوي B (البراءة)","en":"Gathering – boosts B"},
    "taj_ر": {"ar":"اليقظة والمراقبة – المقاومة","en":"Vigilance – resistance"},
    "taj_س": {"ar":"السمع والاستجابة – سرعة التوبة","en":"Hearing & response – repentance speed"},
    "taj_ح": {"ar":"الحياة والاستدامة – الحج يجدد الإيمان","en":"Life & sustainability – Hajj"},
    "taj_ط": {"ar":"الطهارة والمناعة – الصيام","en":"Purity & immunity – Fasting"},
    "ish_ع": {"ar":"الإدراك والعلم – يضاعف W","en":"Perception & knowledge – multiplies W"},
    "ish_ي": {"ar":"الاستجابة والدعاء – يضاعف B","en":"Response & supplication – multiplies B"},
    "ish_هـ": {"ar":"الهوية والمعية – يقلل تأثير الدنيا","en":"Identity & closeness – dampens E"},
    "ish_ق": {"ar":"الميزان والقسط – يضبط المعادلة","en":"Balance & equity – normalizes"},
    "dual_ص": {"ar":"الصبر والصدق والصلاة – يقوي W","en":"Patience & truthfulness – boosts W"},
    "dual_ق_متغير": {"ar":"القسط والعدل – يقوي B","en":"Equity & justice – boosts B"},
    "act_ج": {"ar":"الجهاد والجود (+) / الجهل (-) – يؤثر على B","en":"Jihad & generosity / Ignorance – affects B"},
    "act_خ": {"ar":"الخير والخشية (+) / الخيانة (-) – يؤثر على W","en":"Goodness / Betrayal – affects W"},
    "act_د": {"ar":"الدين والدعوة (+) / الدولة والغلبة (-) – يؤثر على W","en":"Religion / Mere power – affects W"},
    "act_ذ": {"ar":"الذكر (+) / الذل والذنب (-) – يؤثر على B","en":"Remembrance / Humiliation – affects B"},
    "act_ز": {"ar":"الزكاة والزهد (+) / الزور (-) – يؤثر على B","en":"Zakat / Falsehood – affects B"},
    "act_ش": {"ar":"الشكر والشجاعة (+) / الشهوة والشرك (-) – يؤثر على W","en":"Gratitude / Lust – affects W"},
    "act_ت": {"ar":"التوبة والتقوى (+) / التيه (-) – يؤثر على W","en":"Repentance / Wandering – affects W"},
    "act_ث": {"ar":"الثبات والثواب (+) / الثبور (-) – يؤثر على W","en":"Steadfastness / Destruction – affects W"},
    "act_ض": {"ar":"الضياء (+) / الضلال (-) – يؤثر على B","en":"Radiance / Misguidance – affects B"},
    "act_ظ": {"ar":"الظفر (+) / الظلم (-) – يؤثر على W و B","en":"Victory / Injustice – affects both"},
    "act_غ": {"ar":"الغفران (+) / الغش (-) – يؤثر على B","en":"Forgiveness / Fraud – affects B"},
}

# ================================================================
# الشريط الجانبي – لوحة التحكم الكاملة
# ================================================================
with st.sidebar:
    lang_choice = st.radio("اللغة / Language", ["العربية", "English"], index=0 if LANG=="ar" else 1)
    if (lang_choice=="English" and LANG=="ar") or (lang_choice=="العربية" and LANG=="en"):
        st.session_state.lang = "en" if lang_choice=="English" else "ar"
        st.rerun()

    st.markdown("---")
    st.header(t("⚙️ المعاملات الأساسية","⚙️ Basic Parameters"))
    W_init = st.slider(t("W الابتدائي","Initial W"), 0.0,1.0,0.55,0.01,key="s_W")
    B_init = st.slider(t("B الابتدائي","Initial B"), 0.0,1.0,0.52,0.01,key="s_B")
    delay = st.slider(t("فجوة الاستدراج","Istidraj Gap"),5,50,22,1,key="s_delay")
    N_STARS = st.slider(t("عدد النجوم","Number of Stars"),100,600,300,50,key="s_N")

    st.markdown("---")
    st.header(t("🔮 الثوابت الإلهية (المصدر)","🔮 Divine Constants (Source)"))
    k_val = st.slider(t("ك (الأمر)","Kaf (Command)"),10,200,20,10,key="s_k")
    n_val = st.slider(t("ن (النور)","Nun (Light)"),5,100,50,5,key="s_n")
    s_val = st.slider(t("ص (الصمد)","Sad (Eternal)"),10,200,90,10,key="s_s")
    q_val = st.slider(t("ق (الميزان)","Qaf (Balance)"),10,200,100,10,key="s_q")

    st.markdown("---")
    st.header(t("🏛️ أسس الحكم","🏛️ Governance"))
    amr_val = st.slider(t("الأمر بالمعروف","Enjoining Good"),0.0,1.0,0.5,0.01,key="s_amr")
    nahy_val = st.slider(t("النهي عن المنكر","Forbidding Evil"),0.0,1.0,0.5,0.01,key="s_nahy")
    adl_val = st.slider(t("العدل","Justice"),0.0,1.0,0.6,0.01,key="s_adl")
    shura_val = st.slider(t("الشورى","Consultation"),0.0,1.0,0.5,0.01,key="s_shura")

    st.markdown("---")
    st.header(t("💀 قوى الضلال","💀 Forces of Darkness"))
    riba_val = st.slider(t("الربا","Usury"),0.0,1.0,0.2,0.01,key="s_riba")
    zulm_val = st.slider(t("الظلم","Injustice"),0.0,1.0,0.2,0.01,key="s_zulm")
    khianah_val = st.slider(t("الخيانة","Betrayal"),0.0,1.0,0.2,0.01,key="s_khianah")

    st.markdown("---")
    st.header(t("🔆 حروف التجلي (صفات الله)","🔆 Tajalli Letters"))
    tajalli_intensity = {}
    for L, D in LETTER_CATEGORIES["tajalli"].items():
        tajalli_intensity[L] = st.slider(f"{L} ({D['role']})",0.0,1.0,0.7,0.01,
                                         key=f"s_taj_{L}",
                                         help=LETTER_TOOLTIPS.get(f"taj_{L}",{}).get(LANG,""))

    st.markdown("---")
    st.header(t("🔄 حروف الاشتراك (قنوات)","🔄 Ishtirak Letters"))
    ishtirak_intensity = {}
    for L, D in LETTER_CATEGORIES["ishtirak"].items():
        ishtirak_intensity[L] = st.slider(f"{L} ({D['role']})",0.0,1.0,0.7,0.01,
                                          key=f"s_ish_{L}",
                                          help=LETTER_TOOLTIPS.get(f"ish_{L}",{}).get(LANG,""))

    st.markdown("---")
    st.header(t("⚖️ حروف الازدواج (وجه متغير)","⚖️ Dual Letters"))
    dual_intensity = {}
    for L, D in LETTER_CATEGORIES["dual"].items():
        role = D.get("variable_role", D.get("constant_role",""))
        dual_intensity[L] = st.slider(f"{L} ({role})",0.0,1.0,0.7,0.01,
                                      key=f"s_dual_{L}",
                                      help=LETTER_TOOLTIPS.get(f"dual_{L}",{}).get(LANG,""))

    st.markdown("---")
    st.header(t("⚡ حروف الأعمال (إيجابي/سلبي)","⚡ Action Letters"))
    actions_intensity = {}
    for L, D in LETTER_CATEGORIES["actions"].items():
        actions_intensity[L] = st.slider(f"{L} ({D['positive']} / {D['negative']})",
                                         -1.0,1.0,0.0,0.1,
                                         key=f"s_act_{L}",
                                         help=LETTER_TOOLTIPS.get(f"act_{L}",{}).get(LANG,""))

    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    if c1.button(t("▶️ تشغيل المحاكاة","▶️ Run"), use_container_width=True): st.session_state.run = True
    if c2.button(t("⏹️ إيقاف","⏹️ Stop"), use_container_width=True): st.session_state.run = False
    if c3.button(t("🔄 إعادة ضبط","🔄 Reset"), use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang","lang_radio"): del st.session_state[k]
        st.rerun()

# ================================================================
# العنوان الرئيسي والتبويبات
# ================================================================
st.markdown(f"""
<div style="text-align:center;padding:20px 0 10px 0;">
<h1 style="color:#FFD700;font-size:2.5em;margin-bottom:0;">⚖️ {t('المنصة الذهبية','The Golden Platform')}</h1>
<h2 style="color:#FFD700;font-size:1.3em;margin-top:0;">{t('S = W × B | من الذرة إلى الحضارة','S = W × B | From Atom to Civilization')}</h2>
<p style="color:#AAA;font-size:0.9em;">{t('نظرية الميزان – علم الثبات الوجودي','The Mizan Theory – Science of Existential Stability')}</p>
</div>""", unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5 = st.tabs([
    t("🏛️ المختبر الجماعي","🏛️ The Collective Lab"),
    t("🧍 البوصلة الشخصية","🧍 Personal Compass"),
    t("📖 كتاب الميزان","📖 The Book of Mizan"),
    t("🔤 المعجم الهندسي","🔤 Geometric Lexicon"),
    t("📜 رسالة الترحيب","📜 Welcome Message"),
])

# ================================================================
# تبويب 1: المختبر الجماعي
# ================================================================
with tab1:
    st.header(t("🏛️ المختبر الجماعي","🏛️ The Collective Lab"))
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init' not in st.session_state: st.session_state.init = False

    if not st.session_state.init:
        np.random.seed(42); random.seed(42)
        cx,cy = 14,10.0
        st.session_state.cx=cx; st.session_state.cy=cy
        st.session_state.sx = np.random.uniform(cx-13,cx+13,N_STARS)
        st.session_state.sy = np.random.uniform(cy-9,cy+9,N_STARS)
        st.session_state.sw = np.random.uniform(0.1,1.0,N_STARS)
        st.session_state.sb = np.random.uniform(0.1,1.0,N_STARS)
        S = calc_S(W_init,B_init,0.3,
                   q_val,n_val,k_val,
                   tajalli_intensity,ishtirak_intensity,dual_intensity,actions_intensity,
                   amr_val,nahy_val,adl_val,shura_val,riba_val,zulm_val,khianah_val)
        st.session_state.W=W_init; st.session_state.B=B_init
        st.session_state.E=0.3; st.session_state.S=S
        st.session_state.ph=t("توازن","Balance"); st.session_state.ca=0.0
        st.session_state.aW=0.0; st.session_state.aB=np.pi*0.5
        st.session_state.eb=deque([S]*30,maxlen=30)
        st.session_state.pS=deque(maxlen=400); st.session_state.pE=deque(maxlen=400)
        st.session_state.px=deque(maxlen=400); st.session_state.pc=0
        st.session_state.init=True

    if st.session_state.get("run",False):
        placeholder=st.empty()
        while st.session_state.get("run",False):
            W=st.session_state.W; B=st.session_state.B; E=st.session_state.E
            S=st.session_state.S; ph=st.session_state.ph; ca=st.session_state.ca
            aW=st.session_state.aW; aB=st.session_state.aB
            sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
            sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
            cx=st.session_state.cx; cy=st.session_state.cy
            eb=st.session_state.eb
            pS=st.session_state.pS.copy(); pE=st.session_state.pE.copy()
            px=st.session_state.px.copy(); pc=st.session_state.pc

            ca+=0.008; sv=np.sin(ca)
            if sv>0.5: ph=t('ذروة الاستقرار','Peak Stability')
            elif sv>0: ph=t('صعود','Rising')
            elif sv>-0.5: ph=t('انهيار','Collapse')
            else: ph=t('القاع','Rock Bottom')
            if 0.3<sv<0.35: ph=t('>> استدراج <<','>> Istidraj <<')
            target_S = 0.5+0.45*sv

            for i in range(N_STARS):
                dist = np.sqrt((sx[i]-sx)**2+(sy[i]-sy)**2)
                close = (dist<2.0)&(np.arange(N_STARS)!=i)
                sw[i] += (target_S-sw[i])*0.02+np.random.uniform(-0.02,0.02)
                sb[i] += (target_S-sb[i])*0.02+np.random.uniform(-0.02,0.02)
                if np.any(close):
                    sw[i] += (np.mean(sw[close])-sw[i])*0.03
                    sb[i] += (np.mean(sb[close])-sb[i])*0.03
                sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)

            if random.random()<0.005:
                aff=np.random.choice(N_STARS,size=int(N_STARS*0.2),replace=False)
                sw[aff]*=np.random.uniform(0.5,0.8); sb[aff]*=np.random.uniform(0.5,0.8)

            avgW=np.mean(sw); avgB=np.mean(sb)
            W+=(avgW-W)*0.04; B+=(avgB-B)*0.04
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

            S = calc_S(W,B,E,
                       q_val,n_val,k_val,
                       tajalli_intensity,ishtirak_intensity,dual_intensity,actions_intensity,
                       amr_val,nahy_val,adl_val,shura_val,riba_val,zulm_val,khianah_val)
            eb.append(S)
            E_target=list(eb)[-delay] if len(eb)>=delay else S
            E+=0.03*(E_target-E)

            W=W-0.015*E+0.03/(S+0.1)-0.007*(1-B)
            B=B-0.012*E+0.006*(1-B)*W*(1-W)
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

            S = calc_S(W,B,E,
                       q_val,n_val,k_val,
                       tajalli_intensity,ishtirak_intensity,dual_intensity,actions_intensity,
                       amr_val,nahy_val,adl_val,shura_val,riba_val,zulm_val,khianah_val)

            pc+=1
            if pc%2==0:
                pS.append(S); pE.append(E); px.append(len(px))

            aW+=0.02+random.uniform(-0.025,0.025)*(1-W)**2
            aB+=0.02+random.uniform(-0.025,0.025)*(1-B)**2
            wx=cx+(7-2.5*W)*np.cos(aW); wy=cy+(7-2.5*W)*np.sin(aW)*0.7
            bx=cx+(5-1.5*B)*np.cos(aB); by=cy+(5-1.5*B)*np.sin(aB)*0.7

            inst=1-np.mean(sw*sb)
            sx+=np.random.uniform(-0.07,0.07,N_STARS)*inst
            sy+=np.random.uniform(-0.07,0.07,N_STARS)*inst
            sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)

            st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
            st.session_state.ph=ph; st.session_state.ca=ca
            st.session_state.aW=aW; st.session_state.aB=aB; st.session_state.eb=eb
            st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
            st.session_state.pS=pS; st.session_state.pE=pE; st.session_state.px=px; st.session_state.pc=pc

            fig,ax=plt.subplots(figsize=(14,10),facecolor='#000010')
            ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
            for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                          (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy),r*(0.5+2.8*S),color=c,alpha=a,zorder=15))
            ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
            ax.add_patch(Circle((cx,cy),0.5+16*E,color='#0FF',alpha=0.25*(1-min(E,1))+0.04,zorder=7))
            ax.add_patch(Circle((cx,cy),8.5,color='#0F8',alpha=0.15,fill=False,lw=2.5,zorder=2))
            ax.add_patch(Circle((wx,wy),0.2+0.6*W,color='#FFF',alpha=1,zorder=13))
            ax.add_patch(Circle((bx,by),0.2+0.6*B,color='#F33',alpha=0.8,zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            colors=[get_color(sw[i],sb[i]) for i in range(N_STARS)]
            ax.scatter(sx,sy,s=35,c=colors,alpha=0.9,edgecolors='white',linewidths=0.4,zorder=5)
            pax=ax.inset_axes([0.5,0.02,0.46,0.10])
            pax.set_xlim(0,400); pax.set_ylim(0,1.05)
            pax.set_title(t('S (الذهب) يقود E (السماوي) – الاستدراج','S (Gold) leads E (Cyan) – Istidraj'),color='white',fontsize=7)
            pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
            if list(pS): pax.plot(list(px),list(pS),color='#FFD700',lw=2); pax.plot(list(px),list(pE),color='#0FF',lw=1.5)
            ax.text(14,1.2,f'{ph} | S={S:.2f} | E={E:.2f}',color='white',fontsize=12,ha='center',fontweight='bold')
            plt.tight_layout(pad=0); placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.08)
        st.success(t("✅ تم إيقاف المحاكاة.","✅ Simulation stopped."))
    else:
        st.info(t("اضغط ▶️ تشغيل المحاكاة في الشريط الجانبي.","Press ▶️ Run Simulation in the sidebar."))

# ================================================================
# تبويب 2: البوصلة الشخصية
# ================================================================
with tab2:
    st.header(t("🧭 البوصلة الشخصية","🧭 Personal Compass"))
    if 'compass_answers' not in st.session_state: st.session_state.compass_answers = {}
    questions = {
        "W": [
            (t("هل تعيش لله وحده؟","Do you live for Allah alone?"),10),
            (t("هل تقيم الصلاة بخشوع؟","Do you pray with devotion?"),10),
            (t("هل تؤدي الزكاة وتتصدق؟","Do you pay Zakat & give charity?"),10),
            (t("هل تصوم رمضان وتطوعًا؟","Do you fast Ramadan & voluntarily?"),10),
            (t("هل تحج أو تسعى للحج؟","Do you perform/seek Hajj?"),10),
            (t("هل تحب الله ورسوله أكثر من كل شيء؟","Do you love Allah & Messenger most?"),10),
            (t("هل تصدق في أقوالك وأفعالك؟","Are you truthful?"),10),
            (t("هل تؤدي الأمانات؟","Do you fulfill trusts?"),10),
            (t("هل تتوكل على الله مع الأخذ بالأسباب؟","Do you rely on Allah while using means?"),10),
            (t("هل تشكر في الرخاء وتصبر في البلاء؟","Are you grateful & patient?"),10),
            (t("هل تحمل هم الإسلام والمسلمين؟","Do you care for Islam & Muslims?"),10),
            (t("هل تفي بالعهد؟","Do you keep your promises?"),10),
            (t("هل أنت راضٍ بما قسم الله لك؟","Are you content with Allah's decree?"),10),
            (t("هل تنصر المؤمن إذا ظُلم؟","Do you help the oppressed believer?"),10),
        ],
        "B": [
            (t("هل تأمر بالمعروف؟","Do you enjoin good?"),10),
            (t("هل تنهى عن المنكر؟","Do you forbid evil?"),10),
            (t("هل أنت مستعد لبذل النفس والمال في سبيل الله؟","Ready to sacrifice for Allah?"),10),
            (t("هل تتبرأ من الشرك وأهله؟","Do you disavow polytheism?"),10),
            (t("هل ترفض الكفر والإلحاد؟","Do you reject disbelief/atheism?"),10),
            (t("هل تكره النفاق والتلون؟","Do you hate hypocrisy?"),10),
            (t("هل تجاهد نفسك على ترك الكذب؟","Do you struggle against lying?"),10),
            (t("هل تتجنب الغش في معاملاتك؟","Do you avoid fraud?"),10),
            (t("هل تفي بعهودك ولا تخون؟","Do you keep trusts, no betrayal?"),10),
            (t("هل ترفض الظلم بكل صوره؟","Do you reject all injustice?"),10),
            (t("هل تجاهد نفسك على ترك الفواحش؟","Do you struggle against immorality?"),10),
            (t("هل تخلص عملك لله وتجتنب الرياء؟","Is your work sincere?"),10),
            (t("هل تسلم لله في قسمته ولا تحسد؟","Do you accept Allah's decree, no envy?"),10),
            (t("هل تحب في الله وتبغض في الله؟","Do you love & hate for Allah's sake?"),10),
        ]
    }
    cA,cB=st.columns(2)
    with cA:
        st.subheader(t("🤍 أسئلة الولاء (W)","🤍 Loyalty Questions (W)"))
        for i,(q,v) in enumerate(questions["W"]):
            ans=st.radio(q,[t(f"نعم ({v})",f"Yes ({v})"),t(f"أحيانًا ({v//2})",f"Sometimes ({v//2})"),t(f"لا (0)",f"No (0)")],key=f"cw_{i}",index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"W{i}"]=v
                elif t("أحيانًا","Sometimes") in ans: st.session_state.compass_answers[f"W{i}"]=v//2
                else: st.session_state.compass_answers[f"W{i}"]=0
    with cB:
        st.subheader(t("❤️ أسئلة البراءة (B)","❤️ Disavowal Questions (B)"))
        for i,(q,v) in enumerate(questions["B"]):
            ans=st.radio(q,[t(f"نعم ({v})",f"Yes ({v})"),t(f"أحيانًا ({v//2})",f"Sometimes ({v//2})"),t(f"لا (0)",f"No (0)")],key=f"cb_{i}",index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"B{i}"]=v
                elif t("أحيانًا","Sometimes") in ans: st.session_state.compass_answers[f"B{i}"]=v//2
                else: st.session_state.compass_answers[f"B{i}"]=0
    if len(st.session_state.compass_answers)==28:
        Ws=sum(st.session_state.compass_answers[f"W{i}"] for i in range(14))/140.0
        Bs=sum(st.session_state.compass_answers[f"B{i}"] for i in range(14))/140.0
        Ss=Ws*Bs
        qn,qc=classify_human(Ws,Bs)
        names={"believer":t("مؤمن (الربع الأول)","Believer (Q1)"),"disbeliever":t("كافر (الربع الثاني)","Disbeliever (Q2)"),
               "hypocrite":t("منافق (الربع الثالث)","Hypocrite (Q3)"),"polytheist":t("مشرك (الربع الرابع)","Polytheist (Q4)")}
        st.divider(); st.header(t("📊 نتيجة البوصلة","📊 Compass Result"))
        c1,c2,c3=st.columns(3)
        c1.metric("W",f"{Ws:.2f}"); c2.metric("B",f"{Bs:.2f}"); c3.metric("S",f"{Ss:.2f}")
        st.markdown(f"<h2 style='color:{qc};text-align:center;'>{names.get(qn,qn)}</h2>",unsafe_allow_html=True)
        fig,ax=plt.subplots(figsize=(6,6),facecolor='#0a0a2e'); ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
        ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
        ax.set_xlabel("B",color='white'); ax.set_ylabel("W",color='white')
        ax.fill_between([0,1],0,1,alpha=0.15,color='#FFD700'); ax.fill_between([-1,0],0,1,alpha=0.15,color='#FF5252')
        ax.fill_between([-1,0],-1,0,alpha=0.15,color='#FFB6C1'); ax.fill_between([0,1],-1,0,alpha=0.15,color='#FFA500')
        ax.scatter(Bs*2-1,Ws*2-1,s=250,c='cyan',edgecolors='white',linewidth=3,zorder=10)
        ax.tick_params(colors='white')
        st.pyplot(fig)
        if st.button(t("🔄 إعادة الاختبار","🔄 Retake Test"),use_container_width=True):
            st.session_state.compass_answers={}; st.rerun()

# ================================================================
# تبويب 3: كتاب الميزان
# ================================================================
with tab3:
    st.header(t("📖 كتاب الميزان","📖 The Book of Mizan"))
    with st.expander(t("📜 الإهداء والمقدمة","📜 Dedication & Introduction")):
        st.markdown(t(
            "### الإهداء\nإلى كل باحث عن الحقيقة...\n### مقدمة المؤلف\nالحمد لله... المعادلة المركزية: **S = W × B**",
            "### Dedication\nTo every seeker of truth...\n### Author's Introduction\nThe central equation: **S = W × B**"))
    with st.expander(t("⚖️ معادلة الثبات الوجودي","⚖️ The Existential Stability Equation")):
        st.markdown(t(
            "**S = W × B**\n- **W (الولاء)**: طاقة الحب والطاعة...\n- **B (البراءة)**: طاقة البغض والمفاصلة...\n- **S (الثبات)**: العروة الوثقى...",
            "**S = W × B**\n- **W (Loyalty)**: energy of love and obedience...\n- **B (Disavowal)**: energy of hatred and immunity...\n- **S (Stability)**: the firm handhold..."))
    with st.expander(t("💫 الاستدراج","💫 Istidraj")):
        st.markdown(t(
            "الاستدراج هو تأخر انهيار التمكين المادي (E) عن انهيار الثبات الأخلاقي (S)...",
            "Istidraj is the delayed collapse of material empowerment (E) after moral stability (S)..."))

# ================================================================
# تبويب 4: المعجم الهندسي
# ================================================================
with tab4:
    st.header(t("🔤 المعجم الهندسي للقرآن","🔤 Geometric Lexicon of the Quran"))
    tools = {
        t("فاء السببية (فَـ)","Causative Fa"): ("=", t("تربط السبب بالنتيجة حتمًا.","Inevitably connects cause to effect.")),
        t("واو المعية – الضرب","Conjunctive Waw – Multiplication"): ("×", t("لا يتم الأمر إلا باجتماع الطرفين.","Only complete with both factors.")),
        t("واو الاستئناف – الجمع","Conjunctive Waw – Addition"): ("+", t("جمع تراكمي في مقام الحساب.","Cumulative addition in reckoning.")),
        t("لام التعليل (لِـ)","Purpose Lam"): ("→", t("سهم الغاية. يوضح اتجاه المقصد.","Arrow of purpose.")),
        t("حتى الغائية","Hatta"): ("...", t("استمرار السبب حتى تتحقق النتيجة.","Continuation of cause until result.")),
        t("إن الشرطية","In (If)"): ("( )ᵒ", t("قوس الشرط الاختياري.","Optional condition.")),
        t("إذا الشرطية","Idha (When)"): ("( )ᶜ", t("قوس الشرط المحقق.","Certain condition.")),
        t("إلا","Illa (Except)"): ("{}", t("حدود المجموعة.","Set boundaries.")),
        t("كلا","Kalla (No!)"): ("⛔", t("قطع الأسباب الباطلة.","Severing false causes.")),
    }
    sel = st.selectbox(t("اختر أداة:","Select a tool:"), list(tools.keys()))
    if sel: st.metric(t("الرمز","Symbol"), tools[sel][0]); st.info(tools[sel][1])

# ================================================================
# تبويب 5: رسالة الترحيب
# ================================================================
with tab5:
    st.header(t("📜 رسالة الترحيب","📜 Welcome Message"))
    st.markdown(t("""
    <div style="text-align:center;color:#CCC;line-height:2;">
    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
    > هذا هو نموذج الميزان الذي يثبت أن <b style="color:#FFD700;">S = W × B</b>"
    <br><br>
    <b style="color:#FFD700;">﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا...﴾ — الروم 30</b>
    <br><br>
    > "أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.<br>
    > إنها معادلة. إنها <b style="color:#FFD700;">S = W × B</b>."
    </div>""",
    """
    <div style="text-align:center;color:#CCC;line-height:2;">
    > "Is there a single law governing the atom and civilization?"<br>
    > This is the Mizan Model that proves <b style="color:#FFD700;">S = W × B</b>"
    <br><br>
    <b style="color:#FFD700;">﴿So direct your face toward the religion...﴾ — Ar-Rum 30</b>
    <br><br>
    > "O humanity, you are not in chaos. There is a law. There is a system. There is a balance.<br>
    > It is an equation. It is <b style="color:#FFD700;">S = W × B</b>."
    </div>"""), unsafe_allow_html=True)

# ================================================================
# التذييل
# ================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:20px;color:#888;font-size:0.9em;line-height:1.8;">
<p>© {__YEAR__} {__AUTHOR__}</p>
<p>{__LICENSE__} | {__VERSION__}</p>
<p style="color:#FFD700;font-size:1.5em;margin-top:10px;">⚖️ {__SIGNATURE__}</p>
<p style="font-size:0.8em;">{t('علم الميزان – علم الثبات الوجودي','Mizan Science – The Science of Existential Stability')}</p>
</div>""", unsafe_allow_html=True)
