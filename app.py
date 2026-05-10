import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# إعداد الصفحة
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="المنصة الذهبية | The Golden Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# حقوق المؤلف والترخيص
# ═══════════════════════════════════════════════════════════════
__AUTHOR__ = "علي عادل العاطفي | Ali Adel Alatifi"
__YEAR__ = 2026
__LICENSE__ = "MIT License"
__VERSION__ = "7.0.0 – النسخة النهائية المتكاملة"
__SIGNATURE__ = "⚖️ S = W × B | فَـ(B) × (W) = S | ق = الحق = الميزان"

# ═══════════════════════════════════════════════════════════════
# النظام اللغوي
# ═══════════════════════════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(ar_text, en_text):
    return ar_text if LANG == "ar" else en_text

# ═══════════════════════════════════════════════════════════════
# الثوابت الإلهية – من الكتاب المسطور والكتاب المنظور
# ═══════════════════════════════════════════════════════════════
QAF_TRUTH = 100
PHI = (1 + np.sqrt(5)) / 2
ISTIDRAJ_LAG_DEFAULT = 22

# القيم المعيارية الثابتة (من الفاء)
B_STANDARD = 1.0  # القيمة المعيارية للكفر بالطاغوت
W_STANDARD = 1.0  # القيمة المعيارية للإيمان بالله

# ═══════════════════════════════════════════════════════════════
# قاعدة بيانات الحروف الـ 28
# ═══════════════════════════════════════════════════════════════
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
        "ق": {"value": 100, "label": {"ar":"الحق • الميزان","en":"Truth • Balance"}, "aya": "وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ"},
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

# ═══════════════════════════════════════════════════════════════
# التصنيف الوجودي للحروف (الفئات الست)
# ═══════════════════════════════════════════════════════════════
LETTER_CATEGORIES = {
    "source": {
        "ك": {"value": 20, "role_ar": "الأمر – كُن فَيَكُون", "role_en": "Command – Be!"},
        "ن": {"value": 50, "role_ar": "النور – الهداية", "role_en": "Light – Guidance"},
    },
    "tajalli": {
        "أ": {"value": 1, "role_ar": "الوحدانية", "role_en": "Oneness", "affects": "w"},
        "ل": {"value": 30, "role_ar": "المُلك والعدل", "role_en": "Sovereignty", "affects": "w"},
        "م": {"value": 40, "role_ar": "الجمع والتماسك", "role_en": "Gathering", "affects": "b"},
        "ر": {"value": 200, "role_ar": "اليقظة والمراقبة", "role_en": "Vigilance", "affects": "resistance"},
        "س": {"value": 60, "role_ar": "السمع والاستجابة", "role_en": "Hearing", "affects": "responsiveness"},
        "ح": {"value": 8, "role_ar": "الحياة والاستدامة", "role_en": "Life", "affects": "sustainability"},
        "ط": {"value": 9, "role_ar": "الطهارة والمناعة", "role_en": "Purity", "affects": "b"},
    },
    "ishtirak": {
        "ع": {"value": 70, "role_ar": "الإدراك والعلم", "role_en": "Perception", "affects": "w"},
        "ي": {"value": 10, "role_ar": "الاستجابة والدعاء", "role_en": "Response", "affects": "b"},
        "هـ": {"value": 5, "role_ar": "الهوية والمعية", "role_en": "Identity", "affects": "e_resist"},
        "ق": {"value": 100, "role_ar": "الحق • الميزان", "role_en": "Truth • Balance", "affects": "balance"},
    },
    "dual": {
        "ص": {"value": 90, "constant_role_ar": "الصمد", "variable_role_ar": "الصبر والصدق والصلاة",
              "constant_role_en": "The Eternal", "variable_role_en": "Patience & Truthfulness & Prayer", "affects": "w"},
    },
    "operators": {
        "ف": {"value": 80, "operator": "فَـ(قيمة)", "role_ar": "مُشغّل القيمة المعيارية", "role_en": "Standard Value Operator"},
        "و": {"value": 6, "operator": "×/+", "role_ar": "واو العطف – شرط أو جمع", "role_en": "Conjunctive Waw"},
        "ب": {"value": 2, "operator": "بـ", "role_ar": "باء الاستعانة – غاية", "role_en": "Instrumental Ba"},
        "ل": {"value": 30, "operator": "←/=", "role_ar": "لام الاستحقاق – عطاء مباشر", "role_en": "Lām of Entitlement"},
    },
    "actions": {
        "ج": {"value": 3, "positive_ar": "الجهاد والجود", "negative_ar": "الجهل والجحود", "affects": "b"},
        "خ": {"value": 600, "positive_ar": "الخير والخشية", "negative_ar": "الخيانة والخذلان", "affects": "w"},
        "د": {"value": 4, "positive_ar": "الدين والدعوة", "negative_ar": "الدولة والغلبة", "affects": "w"},
        "ذ": {"value": 700, "positive_ar": "الذكر والذوق", "negative_ar": "الذل والذنب", "affects": "b"},
        "ز": {"value": 7, "positive_ar": "الزكاة والزهد", "negative_ar": "الزور والزيغ", "affects": "b"},
        "ش": {"value": 300, "positive_ar": "الشكر والشجاعة", "negative_ar": "الشهوة والشرك", "affects": "w"},
        "ت": {"value": 400, "positive_ar": "التوبة والتقوى", "negative_ar": "التيه", "affects": "w"},
        "ث": {"value": 500, "positive_ar": "الثبات والثواب", "negative_ar": "الثبور", "affects": "w"},
        "ض": {"value": 800, "positive_ar": "الضياء", "negative_ar": "الضلال", "affects": "b"},
        "ظ": {"value": 900, "positive_ar": "الظفر", "negative_ar": "الظلم", "affects": "both"},
        "غ": {"value": 1000, "positive_ar": "الغفران", "negative_ar": "الغش", "affects": "b"},
    }
}

print("✅ المرحلة الأولى مكتملة: الأساسات والثوابت والحقوق وقاعدة البيانات.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثانية: دوال المعادلة والهندسة التفاضلية والبذور
# ═══════════════════════════════════════════════════════════════

# --- ١. دالة حساب الثبات (S) – المعادلة المركزية ---
def calc_S(W, B, E,
          q_intensity=1.0, k_val=20, n_val=50,
          worship_intensity=None,
          ethics_intensity=None,
          loyalty_disavowal_intensity=None,
          amr_val=0.5, nahy_val=0.5, adl_val=0.6, shura_val=0.5,
          riba_val=0.2, zulm_val=0.2, khianah_val=0.2,
          tajalli_intensity=None,
          ishtirak_intensity=None,
          dual_intensity=None,
          actions_intensity=None):
    """
    تحسب الثبات الوجودي (S) من معادلة الميزان المعممة.
    S = [فَـ(B)] × [فَـ(W)] = S_معياري
    حيث فَـ هي مُشغّل القيمة المعيارية.
    """
    W_eff, B_eff = W, B
    source_factor = (k_val * n_val) / 1000.0

    # --- ١. العبادات (محطات الشحن) ---
    if worship_intensity:
        if 'prayer' in worship_intensity: W_eff *= (1 + 0.15 * worship_intensity['prayer'])
        if 'zakat' in worship_intensity: B_eff *= (1 + 0.12 * worship_intensity['zakat'])
        if 'fasting' in worship_intensity: B_eff *= (1 + 0.18 * worship_intensity['fasting'])
        if 'hajj' in worship_intensity: W_eff *= (1 + 0.10 * worship_intensity['hajj'])

    # --- ٢. الأخلاق والمعاملات ---
    if ethics_intensity:
        w_qualities = ['truthfulness','trustworthiness','keeping_promises','kindness_parents',
                       'family_ties','good_neighbor','mercy','humility','generosity','gentleness']
        for q in w_qualities:
            if q in ethics_intensity: W_eff *= (1 + 0.05 * ethics_intensity[q])
        b_qualities = ['chastity','truthful_testimony']
        for q in b_qualities:
            if q in ethics_intensity: B_eff *= (1 + 0.08 * ethics_intensity[q])

    # --- ٣. الموالاة والبراءة والجهاد ---
    if loyalty_disavowal_intensity:
        if 'alliance_believers' in loyalty_disavowal_intensity: W_eff *= (1 + 0.20 * loyalty_disavowal_intensity['alliance_believers'])
        if 'support_oppressed' in loyalty_disavowal_intensity: W_eff *= (1 + 0.18 * loyalty_disavowal_intensity['support_oppressed'])
        if 'apply_sharia' in loyalty_disavowal_intensity: W_eff *= (1 + 0.25 * loyalty_disavowal_intensity['apply_sharia'])
        if 'disavowal_disbelievers' in loyalty_disavowal_intensity: B_eff *= (1 + 0.20 * loyalty_disavowal_intensity['disavowal_disbelievers'])
        if 'hatred_sins' in loyalty_disavowal_intensity: B_eff *= (1 + 0.15 * loyalty_disavowal_intensity['hatred_sins'])
        if 'jihad_self' in loyalty_disavowal_intensity: B_eff *= (1 + 0.25 * loyalty_disavowal_intensity['jihad_self'])
        if 'jihad_wealth' in loyalty_disavowal_intensity: B_eff *= (1 + 0.15 * loyalty_disavowal_intensity['jihad_wealth'])
        if 'jihad_combat' in loyalty_disavowal_intensity: B_eff *= (1 + 0.30 * loyalty_disavowal_intensity['jihad_combat'])

    # --- ٤. حروف التجلي والاشتراك والازدواج والأعمال ---
    resistance = decay_resist = purity = unity = 1.0
    if tajalli_intensity:
        if 'ل' in tajalli_intensity: W_eff *= (1 + 30 * tajalli_intensity['ل'] / 1000)
        if 'م' in tajalli_intensity: B_eff *= (1 + 40 * tajalli_intensity['م'] / 1000)
        if 'ر' in tajalli_intensity: resistance = 1 + 200 * tajalli_intensity['ر'] / 1000
        if 'ح' in tajalli_intensity: decay_resist = 1 + 8 * tajalli_intensity['ح'] / 100
        if 'ط' in tajalli_intensity: purity = 1 + 9 * tajalli_intensity['ط'] / 100
        if 'أ' in tajalli_intensity: unity = 1 + 1 * tajalli_intensity['أ'] / 100
    if ishtirak_intensity:
        if 'ع' in ishtirak_intensity: W_eff *= (1 + 70 * ishtirak_intensity['ع'] / 1000)
        if 'ي' in ishtirak_intensity: B_eff *= (1 + 10 * ishtirak_intensity['ي'] / 100)
    if dual_intensity:
        if 'ص' in dual_intensity: W_eff *= (1 + 90 * dual_intensity['ص'] / 1000)
    pos_sum = neg_sum = 0
    if actions_intensity:
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
                nv = abs(val); neg_sum += nv * lv
                factor = 1 - nv * lv / 1000
                if aff == "w": W_eff *= factor
                elif aff == "b": B_eff *= factor
                elif aff == "both": W_eff *= (1 - nv * lv / 2000); B_eff *= (1 - nv * lv / 2000)

    S_raw = W_eff * B_eff * (1 + source_factor) * resistance * decay_resist * purity * unity
    S_raw *= (1 + pos_sum / 10000) / (1 + max(neg_sum / 10000, 0.001))

    # --- ٥. معامل الحق والميزان (ق) ---
    imbalance = abs(W_eff - B_eff)
    q_balance = (q_intensity * QAF_TRUTH) / (q_intensity * QAF_TRUTH + imbalance * 50)
    S_raw *= q_balance

    # --- ٦. أسس الحكم ---
    S_raw *= (0.5 + 0.5 * (amr_val * nahy_val))
    S_raw *= (0.8 + 0.4 * adl_val)
    S_raw *= (0.85 + 0.3 * shura_val)

    # --- ٧. قوى الضلال (الحدود) ---
    S_raw *= (1 - 0.3 * riba_val)
    S_raw *= (1 - 0.25 * zulm_val)
    S_raw *= (1 - 0.15 * khianah_val)

    return np.clip(S_raw, 0.001, 1.0)


# --- ٢. دالة حساب انحناء المسار (κ) ---
def compute_curvature(W_hist, B_hist):
    if len(W_hist) < 3: return 0.0
    dW = np.gradient(W_hist); dB = np.gradient(B_hist)
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    last = -1
    num = abs(dW[last] * ddB[last] - dB[last] * ddW[last])
    denom = (dW[last]**2 + dB[last]**2 + 1e-10)**(1.5)
    return num / denom


# --- ٣. دالة التوبة (قوة تصحيحية) ---
def apply_tawbah(W, B, W_hist, B_hist, sincerity=0.8):
    kappa = compute_curvature(W_hist, B_hist)
    if kappa > 0.01:
        corr_W = (1.0 - W) * sincerity * kappa
        corr_B = (1.0 - B) * sincerity * kappa
        return np.clip(W + corr_W, 0.01, 1.0), np.clip(B + corr_B, 0.01, 1.0), kappa
    return W, B, kappa


# --- ٤. دالة الاستدراج ---
def update_empowerment(E_current, S_buffer, lag=22, gamma=0.03):
    if len(S_buffer) >= lag:
        S_target = S_buffer[-lag]
    elif S_buffer:
        S_target = S_buffer[0]
    else:
        S_target = E_current
    return np.clip(E_current + gamma * (S_target - E_current), 0.01, 1.0)


# --- ٥. دوال التصنيف والألوان ---
def get_star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    else: return '#888888'

def classify_quadrant(W_val, B_val):
    if W_val >= 0.5 and B_val >= 0.5: return ("believer", '#FFD700')
    elif W_val < 0.5 and B_val >= 0.5: return ("disbeliever", '#FF5252')
    elif W_val < 0.5 and B_val < 0.5: return ("hypocrite", '#FFB6C1')
    else: return ("polytheist", '#FFA500')


# --- ٦. السيناريوهات التاريخية ---
HISTORICAL_PRESETS = {
    "الخلافة الراشدة (W=0.9, B=0.9)": (0.9, 0.9, 0.1),
    "الدولة العثمانية 1800 (W=0.5, B=0.3)": (0.5, 0.3, 0.7),
    "الاتحاد السوفيتي 1922 (W=0.1, B=0.8)": (0.1, 0.8, 0.6),
    "الأندلس قبل السقوط (W=0.4, B=0.15)": (0.4, 0.15, 0.85),
}


# --- ٧. 🌟 بذرة: طبقة الآخرة المرئية ---
# عداد الحسنات والسيئات
def update_akhirah_ledger(good_deeds, bad_deeds, W, B):
    """
    يحسب تراكم الحسنات والسيئات.
    الحسنات تزيد مع W (الولاء)، والسيئات تزيد مع ضعف B (البراءة).
    """
    good_deeds += W * 0.1
    bad_deeds += (1 - B) * 0.1
    return good_deeds, bad_deeds


# --- ٨. 🌟 بذرة: المختبر الشخصي الديناميكي ---
# دالة لحفظ مسار المستخدم عبر الزمن
def update_personal_path(personal_history, W_val, B_val, S_val):
    """
    يحفظ مسار المستخدم الشخصي عبر الزمن.
    personal_history: قائمة من النقاط (W, B, S, timestamp)
    """
    personal_history.append({
        'W': W_val,
        'B': B_val,
        'S': S_val,
        'timestamp': time.time()
    })
    if len(personal_history) > 200:
        personal_history.pop(0)
    return personal_history


# --- ٩. 🌟 بذرة: تصدير البيانات (طبقة القياس الواقعي) ---
def export_simulation_data(history_S, history_E, history_x):
    """
    يصدر بيانات المحاكاة كملف CSV.
    """
    import pandas as pd
    data = {
        'Time': list(history_x),
        'S (Stability)': list(history_S),
        'E (Empowerment)': list(history_E),
    }
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')


# --- ١٠. 🌟 بذرة: نظام الفرضيات المفتوح ---
def record_hypothesis(hypothesis_name, parameters, result_S):
    """
    يسجل فرضية المستخدم ونتيجتها.
    """
    if 'hypotheses' not in st.session_state:
        st.session_state.hypotheses = []
    st.session_state.hypotheses.append({
        'name': hypothesis_name,
        'parameters': parameters.copy(),
        'S': result_S,
        'timestamp': time.time()
    })

print("✅ المرحلة الثانية مكتملة: دوال المعادلة، الهندسة التفاضلية، والبذور الخمس.")

# ═══════════════════════════════════════════════════════════════
# 🎛️ الشريط الجانبي – لوحة التحكم الكاملة القابلة للطي
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    lang_choice = st.radio("اللغة / Language", ["العربية", "English"],
                          index=0 if LANG == "ar" else 1, key="lang_radio")
    new_lang = "ar" if "العربية" in lang_choice else "en"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()
    st.markdown("---")

    with st.container():
        st.markdown(f"""
        <div style="text-align:center;padding:15px;background:linear-gradient(135deg,#1a1a2e,#0d0d1a);
                    border-radius:15px;margin-bottom:15px;border:2px solid #FFD700;
                    box-shadow:0 0 25px rgba(255,215,0,0.3);">
            <h2 style="color:#FFD700;margin:0;font-size:1.5em;font-weight:900;">⚖️ {t('ق – الْحَقُّ وَالْمِيزَان','Qaf – Truth & Balance')}</h2>
            <p style="color:#CCC;font-size:0.8em;margin:8px 0 0 0;">
                {t('﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾','﴿And the heaven He raised and imposed the balance﴾')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        q_intensity = st.slider(
            t("⚖️ شِدَّةُ تَجَلِّي الْحَقِّ وَالْمِيزَان","⚖️ Intensity of Truth & Balance"),
            0.0, 1.0, 1.0, 0.01, key="s_q_intensity",
            help=t("ق = ١٠٠ = الحق = الميزان.","Qaf = 100 = Truth = Balance."))

    st.markdown("---")

    with st.expander(t("⚙️ الْمُعَامَلَاتُ الْأَسَاسِيَّة","⚙️ Basic Parameters"), expanded=False):
        W_init = st.slider(t("W – الْوَلَاءُ الِابْتِدَائِي","W – Initial Loyalty"),0.0,1.0,0.55,0.01,key="s_W")
        B_init = st.slider(t("B – الْبَرَاءَةُ الِابْتِدَائِيَّة","B – Initial Disavowal"),0.0,1.0,0.52,0.01,key="s_B")
        lag_frames = st.slider(t("Δt – فَجْوَةُ الِاسْتِدْرَاج","Δt – Istidraj Gap"),5,50,22,1,key="s_lag")
        N_STARS = st.slider(t("★ – عَدَدُ النُّجُوم","★ – Number of Stars"),100,600,300,50,key="s_N")

    with st.expander(t("🏛️ سِينَارِيُوهَات تَارِيخِيَّة","🏛️ Historical Presets"), expanded=False):
        preset_choice = st.selectbox(t("اخْتَرْ سِينَارِيُو:","Select a scenario:"),
                                   [t("لا شيء","None")] + list(HISTORICAL_PRESETS.keys()), key="s_preset")
        if preset_choice != t("لا شيء","None") and preset_choice in HISTORICAL_PRESETS:
            preset_W, preset_B, preset_E = HISTORICAL_PRESETS[preset_choice]
            st.info(t(f"W={preset_W}, B={preset_B}, E={preset_E}",f"Loaded: W={preset_W}, B={preset_B}, E={preset_E}"))
            W_init, B_init, E_init = preset_W, preset_B, preset_E
        else:
            E_init = 0.3

    with st.expander(t("🔮 الثَّوَابِتُ الْإِلَهِيَّة","🔮 Divine Constants"), expanded=False):
        k_val = st.slider(t("ك – الْأَمْر (كُنْ)","Kaf – Command"),10,200,20,10,key="s_k")
        n_val = st.slider(t("ن – النُّور","Nun – Light"),5,100,50,5,key="s_n")

    st.markdown("---")

    with st.expander(t("🕌 مُوَلِّدَاتُ الطَّاقَة: الْعِبَادَات","🕌 Energy Generators: Worship"), expanded=False):
        worship_intensity = {}
        worship_intensity['prayer'] = st.slider(t("الصَّلَاة (W)","Prayer (W)"),0.0,1.0,0.8,0.01,key="s_w_prayer")
        worship_intensity['zakat'] = st.slider(t("الزَّكَاة (B)","Zakat (B)"),0.0,1.0,0.6,0.01,key="s_w_zakat")
        worship_intensity['fasting'] = st.slider(t("الصَّوْم (B)","Fasting (B)"),0.0,1.0,0.7,0.01,key="s_w_fasting")
        worship_intensity['hajj'] = st.slider(t("الْحَجّ (W)","Hajj (W)"),0.0,1.0,0.5,0.01,key="s_w_hajj")

    with st.expander(t("🌸 مُوَلِّدَاتُ الطَّاقَة: الْأَخْلَاق","🌸 Ethics & Dealings"), expanded=False):
        ethics_intensity = {}
        st.markdown(t("**– تُقَوِّي الْوَلَاء (W):**","**– Strengthen Loyalty (W):**"))
        for key, label_ar, label_en in [
            ('truthfulness','الصِّدْق','Truthfulness'),('trustworthiness','الْأَمَانَة','Trustworthiness'),
            ('keeping_promises','الْوَفَاء','Promises'),('kindness_parents','بِرّ الْوَالِدَيْن','Kindness to Parents'),
            ('family_ties','صِلَة الرَّحِم','Family Ties'),('good_neighbor','حُسْن الْجِوَار','Good Neighbor'),
            ('mercy','الرَّحْمَة','Mercy'),('humility','التَّوَاضُع','Humility'),
            ('generosity','الْكَرَم','Generosity'),('gentleness','الرِّفْق','Gentleness')]:
            ethics_intensity[key] = st.slider(t(label_ar,label_en),0.0,1.0,0.7,0.01,key=f"s_e_{key}")
        st.markdown(t("**– تُقَوِّي الْبَرَاءَة (B):**","**– Strengthen Disavowal (B):**"))
        for key, label_ar, label_en in [('chastity','الْعَفَّة','Chastity'),('truthful_testimony','الشَّهَادَة بِالْحَقّ','Truthful Testimony')]:
            ethics_intensity[key] = st.slider(t(label_ar,label_en),0.0,1.0,0.7,0.01,key=f"s_e_{key}")

    with st.expander(t("🛡️ الْمُوَالَاة وَالْبَرَاءَة وَالْجِهَاد","🛡️ Loyalty, Disavowal & Jihad"), expanded=False):
        loyalty_disavowal_intensity = {}
        st.markdown(t("**– تُقَوِّي الْوَلَاء (W):**","**– Strengthen Loyalty (W):**"))
        loyalty_disavowal_intensity['alliance_believers'] = st.slider(t("مُوَالَاة الْمُؤْمِنِين","Alliance with Believers"),0.0,1.0,0.8,0.01,key="s_ld_alliance")
        loyalty_disavowal_intensity['support_oppressed'] = st.slider(t("نُصْرَة الْمَظْلُومِين","Supporting Oppressed"),0.0,1.0,0.7,0.01,key="s_ld_oppressed")
        loyalty_disavowal_intensity['apply_sharia'] = st.slider(t("تَحْكِيم شَرْع الله","Applying Sharia"),0.0,1.0,0.6,0.01,key="s_ld_sharia")
        st.markdown(t("**– تُقَوِّي الْبَرَاءَة (B):**","**– Strengthen Disavowal (B):**"))
        loyalty_disavowal_intensity['disavowal_disbelievers'] = st.slider(t("الْبَرَاءَة مِن الْكُفَّار","Disavowal of Disbelievers"),0.0,1.0,0.9,0.01,key="s_ld_disavowal")
        loyalty_disavowal_intensity['hatred_sins'] = st.slider(t("بُغْض الْمَعَاصِي","Hatred of Sins"),0.0,1.0,0.8,0.01,key="s_ld_sins")
        loyalty_disavowal_intensity['jihad_self'] = st.slider(t("جِهَاد النَّفْس","Jihad of Self"),0.0,1.0,0.9,0.01,key="s_ld_jihad_self")
        loyalty_disavowal_intensity['jihad_wealth'] = st.slider(t("جِهَاد بِالْمَال","Jihad with Wealth"),0.0,1.0,0.6,0.01,key="s_ld_jihad_wealth")
        loyalty_disavowal_intensity['jihad_combat'] = st.slider(t("جِهَاد فِي سَبِيل الله","Jihad in Allah's Cause"),0.0,1.0,0.5,0.01,key="s_ld_jihad_combat")

    st.markdown("---")

    with st.expander(t("🏛️ أُسُس الْحُكْم","🏛️ Governance"), expanded=False):
        amr_val = st.slider(t("الْأَمْر بِالْمَعْرُوف","Enjoining Good"),0.0,1.0,0.5,0.01,key="s_amr")
        nahy_val = st.slider(t("النَّهْي عَن الْمُنْكَر","Forbidding Evil"),0.0,1.0,0.5,0.01,key="s_nahy")
        adl_val = st.slider(t("الْعَدْل","Justice"),0.0,1.0,0.6,0.01,key="s_adl")
        shura_val = st.slider(t("الشُّورَى","Consultation"),0.0,1.0,0.5,0.01,key="s_shura")

    with st.expander(t("💀 قُوَى الضَّلَال","💀 Forces of Darkness"), expanded=False):
        riba_val = st.slider(t("الرِّبَا","Usury"),0.0,1.0,0.2,0.01,key="s_riba")
        zulm_val = st.slider(t("الظُّلْم","Injustice"),0.0,1.0,0.2,0.01,key="s_zulm")
        khianah_val = st.slider(t("الْخِيَانَة","Betrayal"),0.0,1.0,0.2,0.01,key="s_khianah")

    st.markdown("---")

    with st.expander(t("🔆 حُرُوف التَّجَلِّي","🔆 Tajalli Letters"), expanded=False):
        tajalli_intensity = {}
        for letter, data in LETTER_CATEGORIES["tajalli"].items():
            role = data.get("role_ar","") if LANG=="ar" else data.get("role_en","")
            tajalli_intensity[letter] = st.slider(f"{letter} ({role})",0.0,1.0,0.7,0.01,key=f"s_taj_{letter}")

    with st.expander(t("🔄 حُرُوف الِاشْتِرَاك","🔄 Ishtirak Letters"), expanded=False):
        ishtirak_intensity = {}
        for letter, data in LETTER_CATEGORIES["ishtirak"].items():
            role = data.get("role_ar","") if LANG=="ar" else data.get("role_en","")
            ishtirak_intensity[letter] = st.slider(f"{letter} ({role})",0.0,1.0,0.7,0.01,key=f"s_ish_{letter}")

    with st.expander(t("⚖️ حُرُوف الِازْدِوَاج","⚖️ Dual Letters"), expanded=False):
        dual_intensity = {}
        for letter, data in LETTER_CATEGORIES["dual"].items():
            role = data.get("variable_role_ar","") if LANG=="ar" else data.get("variable_role_en","")
            dual_intensity[letter] = st.slider(f"{letter} ({role})",0.0,1.0,0.7,0.01,key=f"s_dual_{letter}")

    with st.expander(t("⚡ حُرُوف الْأَعْمَال","⚡ Action Letters"), expanded=False):
        actions_intensity = {}
        for letter, data in LETTER_CATEGORIES["actions"].items():
            pos = data.get("positive_ar","") if LANG=="ar" else data.get("positive_en","")
            neg = data.get("negative_ar","") if LANG=="ar" else data.get("negative_en","")
            actions_intensity[letter] = st.slider(f"{letter} ({pos} / {neg})",-1.0,1.0,0.0,0.1,key=f"s_act_{letter}")

    st.markdown("---")

    with st.expander(t("🔤 الْمُعْجَم الْهَنْدَسِيّ","🔤 Geometric Lexicon"), expanded=False):
        use_geometry = st.checkbox(t("تفعيل فِي الْمُحَاكَاة","Activate in Simulation"),value=False,key="s_use_geometry")
        if use_geometry:
            geometry_mode = st.radio(t("نَوْع الْعَلَاقَة:","Relation type:"),
                                   [t("واو الضَّرْب (×) – شَرْطِيَّة","Waw × – Conditional"),
                                    t("واو الْجَمْع (+) – تَرَاكُم","Waw + – Cumulative")],key="s_geometry_mode")

    st.markdown("---")
    col1,col2,col3 = st.columns(3)
    with col1:
        if st.button(t("▶️ تَشْغِيل","▶️ Run"),use_container_width=True,type="primary"):st.session_state.run=True
    with col2:
        if st.button(t("⏹️ إِيقَاف","⏹️ Stop"),use_container_width=True):st.session_state.run=False
    with col3:
        if st.button(t("🔄 إِعَادَة","🔄 Reset"),use_container_width=True):
            for k in list(st.session_state.keys()):
                if k not in ("lang","lang_radio"):del st.session_state[k]
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# 🏛️ العنوان الرئيسي
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="text-align:center;padding:30px 20px 15px 20px;
            background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(13,13,26,0.5) 100%);">
    <h1 style="color:#FFD700;font-size:2.8em;margin-bottom:5px;font-weight:900;
               text-shadow:0 0 30px rgba(255,215,0,0.5);letter-spacing:3px;">
        ⚖️ {t('الْمَنْصَة الذَّهَبِيَّة','THE GOLDEN PLATFORM')}
    </h1>
    <h2 style="color:#FFD700;font-size:1.4em;margin-top:0;font-weight:600;">
        {t('نِظَام الْإِثْبَات الرَّقْمِيّ • نَظَرِيَّة الْمِيزَان','Digital Proof System • The Mizan Theory')}
    </h2>
    <p style="color:#AAA;font-size:1em;margin-top:10px;line-height:2;">
        {t('﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾',
           '﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾')}
    </p>
    <p style="color:#FFD700;font-size:1.1em;margin-top:8px;font-weight:600;">
        ⚖️ {t('فَـ(B) × (W) = S','Fa(B) × (W) = S')} &nbsp;|&nbsp; {t('ق = ١٠٠ = الْحَقّ = الْمِيزَان','Qaf = 100 = Truth = Balance')}
    </p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 📑 التبويبات
# ═══════════════════════════════════════════════════════════════
tab1, tab_math, tab_compass, tab_book, tab_lexicon, tab_welcome = st.tabs([
    t("🏛️ الْمُخْتَبَر الْجَمَاعِيّ","🏛️ The Collective Lab"),
    t("📐 الرِّيَاضِيَّات الْمِيزَانِيَّة","📐 Mizan Mathematics"),
    t("🧭 الْبَوْصَلَة الشَّخْصِيَّة","🧭 Personal Compass"),
    t("📖 كِتَاب الْمِيزَان","📖 Book of Mizan"),
    t("🔤 الْمُعْجَم الْهَنْدَسِيّ","🔤 Geometric Lexicon"),
    t("📜 رِسَالَة التَّرْحِيب","📜 Welcome Message"),
])


# ═══════════════════════════════════════════════════════════════
# 🏛️ تبويب ١: المختبر الجماعي – التهيئة
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.header(t("🏛️ الْمُخْتَبَر الْجَمَاعِيّ – مُحَاكَاة إِثْبَات الْحَقّ","🏛️ The Collective Lab – Proving the Truth"))
    st.markdown(t(
        "شَاهِد كَيْف يَتَفَاعَل الْوَلَاء (W) وَالْبَرَاءَة (B) تَحْت مِيزَان الْحَقّ (ق). "
        "الْجَزَاء مِن جِنْس الْعَمَل يَظْهَر فِي حَرَكَة الْأَفْرَاد نَحْو الذَّهَب أَو الْهَاوِيَة.",
        "Watch how Loyalty (W) and Disavowal (B) interact under the Balance of Truth (Qaf)."))

    # تطبيق السيناريو
    if preset_choice != t("لا شيء","None") and preset_choice in HISTORICAL_PRESETS:
        W_init, B_init, E_init = HISTORICAL_PRESETS[preset_choice]
    else:
        E_init = 0.3

    # تهيئة حالة المحاكاة
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init' not in st.session_state: st.session_state.init = False

    if not st.session_state.init:
        np.random.seed(42); random.seed(42)
        cx,cy = 14,10.0
        sx = np.random.uniform(cx-13,cx+13,N_STARS); sy = np.random.uniform(cy-9,cy+9,N_STARS)
        sw = np.random.uniform(0.1,1.0,N_STARS); sb = np.random.uniform(0.1,1.0,N_STARS)
        star_W_hist = [deque([sw[i]],maxlen=50) for i in range(N_STARS)]
        star_B_hist = [deque([sb[i]],maxlen=50) for i in range(N_STARS)]
        W=W_init; B=B_init; E=E_init
        S = calc_S(W,B,E,q_intensity=q_intensity,k_val=k_val,n_val=n_val,
                   worship_intensity=worship_intensity,ethics_intensity=ethics_intensity,
                   loyalty_disavowal_intensity=loyalty_disavowal_intensity,
                   amr_val=amr_val,nahy_val=nahy_val,adl_val=adl_val,shura_val=shura_val,
                   riba_val=riba_val,zulm_val=zulm_val,khianah_val=khianah_val,
                   tajalli_intensity=tajalli_intensity,ishtirak_intensity=ishtirak_intensity,
                   dual_intensity=dual_intensity,actions_intensity=actions_intensity)
        planet_W_hist = deque([W],maxlen=50); planet_B_hist = deque([B],maxlen=50)
        phase = t("تَوَازُن","Balance"); cycle_angle=0.0; angle_W=0.0; angle_B=np.pi*0.5
        empowerment_buffer = deque([S]*30,maxlen=30)
        history_S = deque(maxlen=400); history_E = deque(maxlen=400); history_x = deque(maxlen=400)
        frame_count=0
        # بذور جديدة
        good_deeds = 10.0; bad_deeds = 5.0
        personal_history = []

        st.session_state.update({
            'cx':cx,'cy':cy,'sx':sx,'sy':sy,'sw':sw,'sb':sb,
            'star_W_hist':star_W_hist,'star_B_hist':star_B_hist,
            'W':W,'B':B,'E':E,'S':S,'phase':phase,'cycle_angle':cycle_angle,
            'angle_W':angle_W,'angle_B':angle_B,'empowerment_buffer':empowerment_buffer,
            'history_S':history_S,'history_E':history_E,'history_x':history_x,'frame_count':frame_count,
            'planet_W_hist':planet_W_hist,'planet_B_hist':planet_B_hist,
            'good_deeds':good_deeds,'bad_deeds':bad_deeds,'personal_history':personal_history,
            'init':True
        })

    if st.session_state.init and not st.session_state.run:
        col1,col2,col3,col4,col5,col6 = st.columns(6)
        col1.metric("W – الْوَلَاء",f"{st.session_state.W:.3f}")
        col2.metric("B – الْبَرَاءَة",f"{st.session_state.B:.3f}")
        col3.metric("S – الثَّبَات",f"{st.session_state.S:.3f}")
        col4.metric("E – التَّمْكِين",f"{st.session_state.E:.3f}")
        col5.metric(t("الطَّوْر","Phase"),st.session_state.phase)
        col6.metric(t("κ – الِانْحِنَاء","κ – Curvature"),
                   f"{compute_curvature(list(st.session_state.planet_W_hist),list(st.session_state.planet_B_hist)):.4f}")
        st.info(t("اضْغَط ▶️ تَشْغِيل لِرُؤْيَة الْمُحَاكَاة.","Press ▶️ Run to see the simulation."))

print("✅ المرحلة الثالثة مكتملة: الشريط الجانبي، العنوان، التبويبات، والتهيئة مع البذور الجديدة.")

# ═══════════════════════════════════════════════════════════════
# 🎬 حلقة المحاكاة الرئيسية (المختبر الجماعي)
# ═══════════════════════════════════════════════════════════════
if st.session_state.get("run", False):
    placeholder = st.empty()
    
    while st.session_state.get("run", False):
        W=st.session_state.W; B=st.session_state.B; E=st.session_state.E; S=st.session_state.S
        phase=st.session_state.phase; cycle_angle=st.session_state.cycle_angle
        angle_W=st.session_state.angle_W; angle_B=st.session_state.angle_B
        sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
        sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
        star_W_hist=st.session_state.star_W_hist; star_B_hist=st.session_state.star_B_hist
        cx=st.session_state.cx; cy=st.session_state.cy; eb=st.session_state.empowerment_buffer
        pS=st.session_state.history_S; pE=st.session_state.history_E; px=st.session_state.history_x
        frame_count=st.session_state.frame_count
        planet_W_hist=st.session_state.planet_W_hist; planet_B_hist=st.session_state.planet_B_hist
        good_deeds=st.session_state.good_deeds; bad_deeds=st.session_state.bad_deeds
        personal_history=st.session_state.personal_history

        cycle_angle += 0.008; sv = np.sin(cycle_angle)
        if sv>0.5: phase=t('ذُرْوَة الِاسْتِقْرَار','Peak Stability')
        elif sv>0: phase=t('صُعُود','Rising')
        elif sv>-0.5: phase=t('انْهِيَار','Collapse')
        else: phase=t('الْقَاع','Rock Bottom')
        if 0.3<sv<0.35: phase=t('>> اسْتِدْرَاج <<','>> Istidraj <<')
        if -0.35<sv<-0.3: phase=t('>> تَعَافٍ <<','>> Recovery <<')
        target_S = 0.5 + 0.45*sv

        for i in range(N_STARS):
            dist=np.sqrt((sx[i]-sx)**2+(sy[i]-sy)**2)
            close=(dist<2.0)&(np.arange(N_STARS)!=i)
            sw[i]+=(target_S-sw[i])*0.02+np.random.uniform(-0.02,0.02)
            sb[i]+=(target_S-sb[i])*0.02+np.random.uniform(-0.02,0.02)
            if np.any(close): sw[i]+=(np.mean(sw[close])-sw[i])*0.03; sb[i]+=(np.mean(sb[close])-sb[i])*0.03
            sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)
            if random.random()<0.01: sw[i],sb[i],_=apply_tawbah(sw[i],sb[i],list(star_W_hist[i]),list(star_B_hist[i]),0.8)
            star_W_hist[i].append(sw[i]); star_B_hist[i].append(sb[i])

        if random.random()<0.005:
            aff=np.random.choice(N_STARS,size=int(N_STARS*0.2),replace=False)
            sw[aff]*=np.random.uniform(0.5,0.8); sb[aff]*=np.random.uniform(0.5,0.8)

        avgW=np.mean(sw); avgB=np.mean(sb)
        W+=(avgW-W)*0.04; B+=(avgB-B)*0.04; W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

        if use_geometry and geometry_mode is not None:
            if "الضَّرْب" in geometry_mode or "Multiplication" in geometry_mode: S_raw = W * B
            else: S_raw = (W+B)/2
            S = S_raw
        else:
            S = calc_S(W,B,E,q_intensity=q_intensity,k_val=k_val,n_val=n_val,
                       worship_intensity=worship_intensity,ethics_intensity=ethics_intensity,
                       loyalty_disavowal_intensity=loyalty_disavowal_intensity,
                       amr_val=amr_val,nahy_val=nahy_val,adl_val=adl_val,shura_val=shura_val,
                       riba_val=riba_val,zulm_val=zulm_val,khianah_val=khianah_val,
                       tajalli_intensity=tajalli_intensity,ishtirak_intensity=ishtirak_intensity,
                       dual_intensity=dual_intensity,actions_intensity=actions_intensity)

        eb.append(S)
        E_target = list(eb)[-lag_frames] if len(eb) >= lag_frames else S
        E += 0.03*(E_target - E)

        W = W - 0.015*E + 0.03/(S+0.1) - 0.007*(1-B)
        B = B - 0.012*E + 0.006*(1-B)*W*(1-W)
        W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

        if use_geometry and geometry_mode is not None:
            if "الضَّرْب" in geometry_mode or "Multiplication" in geometry_mode: S_raw = W * B
            else: S_raw = (W+B)/2
            S = S_raw
        else:
            S = calc_S(W,B,E,q_intensity=q_intensity,k_val=k_val,n_val=n_val,
                       worship_intensity=worship_intensity,ethics_intensity=ethics_intensity,
                       loyalty_disavowal_intensity=loyalty_disavowal_intensity,
                       amr_val=amr_val,nahy_val=nahy_val,adl_val=adl_val,shura_val=shura_val,
                       riba_val=riba_val,zulm_val=zulm_val,khianah_val=khianah_val,
                       tajalli_intensity=tajalli_intensity,ishtirak_intensity=ishtirak_intensity,
                       dual_intensity=dual_intensity,actions_intensity=actions_intensity)

        planet_W_hist.append(W); planet_B_hist.append(B)
        frame_count += 1
        if frame_count % 2 == 0: pS.append(S); pE.append(E); px.append(len(px))

        angle_W += 0.02+random.uniform(-0.025,0.025)*(1-W)**2
        angle_B += 0.02+random.uniform(-0.025,0.025)*(1-B)**2
        wx=cx+(7-2.5*W)*np.cos(angle_W); wy=cy+(7-2.5*W)*np.sin(angle_W)*0.7
        bx=cx+(5-1.5*B)*np.cos(angle_B); by=cy+(5-1.5*B)*np.sin(angle_B)*0.7

        instability = 1-np.mean(sw*sb)
        sx+=np.random.uniform(-0.07,0.07,N_STARS)*instability
        sy+=np.random.uniform(-0.07,0.07,N_STARS)*instability
        sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)

        # بذرة: طبقة الآخرة
        good_deeds, bad_deeds = update_akhirah_ledger(good_deeds, bad_deeds, W, B)

        # بذرة: المسار الشخصي
        personal_history = update_personal_path(personal_history, W, B, S)

        st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
        st.session_state.phase=phase; st.session_state.cycle_angle=cycle_angle
        st.session_state.angle_W=angle_W; st.session_state.angle_B=angle_B; st.session_state.empowerment_buffer=eb
        st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
        st.session_state.star_W_hist=star_W_hist; st.session_state.star_B_hist=star_B_hist
        st.session_state.planet_W_hist=planet_W_hist; st.session_state.planet_B_hist=planet_B_hist
        st.session_state.history_S=pS; st.session_state.history_E=pE; st.session_state.history_x=px
        st.session_state.frame_count=frame_count
        st.session_state.good_deeds=good_deeds; st.session_state.bad_deeds=bad_deeds
        st.session_state.personal_history=personal_history

        fig, ax = plt.subplots(figsize=(16,12), facecolor='#000010')
        ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
        for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                      (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
            ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
        ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
        ax.add_patch(Circle((cx,cy), 0.5+17*E, color='#0FF', alpha=0.25*(1-min(E,1))+0.04, zorder=7))
        ax.add_patch(Circle((cx,cy), 8.5, color='#0F8', alpha=0.15, fill=False, lw=2.5, zorder=2))
        ax.add_patch(Circle((wx,wy), 0.2+0.6*W, color='#FFF', alpha=1, zorder=13))
        ax.add_patch(Circle((bx,by), 0.2+0.6*B, color='#F33', alpha=0.8, zorder=13))
        ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center',fontweight='bold')
        ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center',fontweight='bold')
        colors = [get_star_color(sw[i],sb[i]) for i in range(N_STARS)]
        ax.scatter(sx, sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)

        kappa_val = compute_curvature(list(planet_W_hist), list(planet_B_hist))
        if kappa_val > 0.05:
            ax.add_patch(Circle((cx,cy), 9.8, color='#FF4444', alpha=0.3, fill=False, lw=2, zorder=4))
            ax.text(cx, cy-3.8, f'⚠ κ={kappa_val:.3f}', color='#FF4444', fontsize=8, ha='center')

        # 🌟 كفتا الميزان الأخروي داخل المشهد (بذرة)
        akhirah_x = 26.5; akhirah_y = 18
        mizan_scale = 1.5
        ax.plot([akhirah_x, akhirah_x], [akhirah_y-3, akhirah_y+1.5], color='#FFD700', lw=1, alpha=0.4)
        # الكفة اليسرى (حسنات)
        left_y = akhirah_y - 1.5 + mizan_scale * min(good_deeds/50, 1.5)
        ax.add_patch(Circle((akhirah_x-1, left_y), 0.6, color='#FFD700', alpha=0.3, zorder=20))
        ax.text(akhirah_x-1, left_y-1, f'ح {good_deeds:.0f}', color='#FFD700', fontsize=7, ha='center')
        # الكفة اليمنى (سيئات)
        right_y = akhirah_y - 1.5 - mizan_scale * min(bad_deeds/50, 1.5)
        ax.add_patch(Circle((akhirah_x+1, right_y), 0.6, color='#FF4444', alpha=0.3, zorder=20))
        ax.text(akhirah_x+1, right_y-1, f'س {bad_deeds:.0f}', color='#FF4444', fontsize=7, ha='center')
        # العارضة
        diff = (bad_deeds - good_deeds) / 50 * mizan_scale
        ax.plot([akhirah_x-1, akhirah_x+1], [akhirah_y - diff, akhirah_y + diff], color='#FFD700', lw=1.5, alpha=0.6)

        # لوحة الإثبات
        pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
        pax.set_xlim(0,400); pax.set_ylim(0,1.05)
        pax.set_title(t('إِثْبَات: S يَقُود E – الِاسْتِدْرَاج','Proof: S leads E – Istidraj'),
                     color='white',fontsize=7,fontweight='bold')
        pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
        if pS: pax.plot(list(px),list(pS),color='#FFD700',lw=2); pax.plot(list(px),list(pE),color='#0FF',lw=1.5)

        ax.text(14,1.2,f'{phase} | S={S:.2f} | E={E:.2f} | κ={kappa_val:.3f}',
               color='white',fontsize=11,ha='center',fontweight='bold')
        plt.tight_layout(pad=0)
        placeholder.pyplot(fig); plt.close(fig)
        time.sleep(0.08)

    st.success(t("✅ تَمَّ إِيقَاف الْمُحَاكَاة.","✅ Simulation stopped."))

    # 🌟 تصدير البيانات (بذرة)
    if st.button(t("📥 تَصْدِير بَيَانَات الْمُحَاكَاة","📥 Export Simulation Data"), use_container_width=True):
        csv_data = export_simulation_data(st.session_state.history_S, st.session_state.history_E, st.session_state.history_x)
        st.download_button(label=t("📥 تَحْمِيل CSV","📥 Download CSV"), data=csv_data, file_name="mizan_simulation.csv", mime="text/csv")

elif st.session_state.init and not st.session_state.run:
    fig, ax = plt.subplots(figsize=(14,10), facecolor='#000010')
    ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
    cx=st.session_state.cx; cy=st.session_state.cy; S=st.session_state.S; E=st.session_state.E
    for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                  (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
        ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
    ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
    ax.add_patch(Circle((cx,cy), 0.5+16*E, color='#0FF', alpha=0.25*(1-min(E,1))+0.04, zorder=7))
    ax.add_patch(Circle((cx,cy), 8.5, color='#0F8', alpha=0.15, fill=False, lw=2.5, zorder=2))
    colors=[get_star_color(st.session_state.sw[i],st.session_state.sb[i]) for i in range(N_STARS)]
    ax.scatter(st.session_state.sx,st.session_state.sy,s=35,c=colors,alpha=0.9,edgecolors='white',linewidths=0.4,zorder=5)
    ax.text(14,1.2,t('فِي انْتِظَار التَّشْغِيل...','Waiting to run...'),color='white',fontsize=12,ha='center')
    plt.tight_layout(pad=0); st.pyplot(fig); plt.close(fig)


# ═══════════════════════════════════════════════════════════════
# 📐 تبويب: الرياضيات الميزانية
# ═══════════════════════════════════════════════════════════════
with tab_math:
    st.header(t("📐 الرِّيَاضِيَّات الْمِيزَانِيَّة","📐 Mizan Mathematics"))
    st.markdown(t("""
    **المسار:** $\\gamma(t) = (B(t), W(t))$
    **الانحناء (κ):** $\\kappa(t) = \\frac{|W' B'' - B' W''|}{(W'^2 + B'^2)^{3/2}}$
    - $\\kappa = 0$ → الصراط المستقيم.
    - $\\kappa > 0$ → انحراف (معصية).
    **التوبة:** $\\vec{F}_{\\text{توبة}} = -\\alpha \\cdot \\vec{\\nabla}\\kappa$
    **النموذج الإبراهيمي:** $\\gamma_{\\text{إبراهيم}}: \\kappa = 0,\\ \\|\\dot{\\gamma}\\| = \\text{const}$
    """,
    """
    **Path:** $\\gamma(t) = (B(t), W(t))$
    **Curvature:** $\\kappa(t) = \\frac{|W' B'' - B' W''|}{(W'^2 + B'^2)^{3/2}}$
    - $\\kappa = 0$ → Straight Path.
    - $\\kappa > 0$ → Deviation.
    **Repentance:** $\\vec{F}_{\\text{rep}} = -\\alpha \\cdot \\vec{\\nabla}\\kappa$
    **Abrahamic Model:** $\\gamma_{\\text{Ab}}: \\kappa = 0$
    """))


# ═══════════════════════════════════════════════════════════════
# 🧭 تبويب: البوصلة الشخصية (بروح الإسلام الحنيف)
# ═══════════════════════════════════════════════════════════════
with tab_compass:
    st.header(t("🧭 الْبَوْصَلَة الشَّخْصِيَّة","🧭 Personal Compass"))
    if 'compass_answers' not in st.session_state: st.session_state.compass_answers = {}
    questions = {
        "W": [
            (t("هَلْ تَعِيش لِلهِ وَحْدَه، مُخْلِصًا لَه الدِّين؟","Do you live for Allah alone?"),10),
            (t("هَلْ تُقِيم الصَّلَاة بِخُشُوع؟","Do you pray with devotion?"),10),
            (t("هَلْ تُؤَدِّي الزَّكَاة طَيِّبَة بِهَا نَفْسُك؟","Do you give Zakat willingly?"),10),
            (t("هَلْ تَصُوم رَمَضَان إِيمَانًا وَاحْتِسَابًا؟","Do you fast with faith?"),10),
            (t("هَلْ فِي قَلْبِك شَوْق لِبَيْت الله؟","Do you long for Allah's House?"),10),
            (t("هَلْ تُحِبّ الله وَرَسُولَه أَكْثَر مِن كُلّ شَيْء؟","Do you love Allah & Messenger most?"),10),
            (t("هَلْ أَنْت صَادِق فِي أَقْوَالِك وَأَفْعَالِك؟","Are you truthful?"),10),
            (t("هَلْ تُؤَدِّي الْأَمَانَات؟","Do you fulfill trusts?"),10),
            (t("هَلْ تَتَوَكَّل عَلَى الله حَقّ تَوَكُّلِه؟","Do you truly rely on Allah?"),10),
            (t("هَلْ تَشْكُر فِي الرَّخَاء وَتَصْبِر فِي الْبَلَاء؟","Are you grateful & patient?"),10),
            (t("هَلْ تَحْمِل هَمّ الْإِسْلَام وَالْمُسْلِمِين؟","Do you care for Islam?"),10),
            (t("هَلْ تَفِي بِالْعَهْد؟","Do you keep promises?"),10),
            (t("هَلْ أَنْت رَاضٍ بِمَا قَسَم الله لَك؟","Are you content?"),10),
            (t("هَلْ تَنْصُر الْمُؤْمِن إِذَا ظُلِم؟","Do you help the oppressed?"),10),
        ],
        "B": [
            (t("هَلْ تَأْمُر بِالْمَعْرُوف بِالْحِكْمَة؟","Do you enjoin good wisely?"),10),
            (t("هَلْ تَنْهَى عَن الْمُنْكَر؟","Do you forbid evil?"),10),
            (t("هَلْ أَنْت مُسْتَعِدّ لِبَذْل النَّفْس لِإِعْلَاء كَلِمَة الله؟","Ready to sacrifice for Allah?"),10),
            (t("هَلْ تَتَبَرَّأ مِن الشِّرْك وَأَهْلِه؟","Do you disavow polytheism?"),10),
            (t("هَلْ تَرْفُض الْكُفْر وَالْإِلْحَاد؟","Do you reject disbelief?"),10),
            (t("هَلْ تَكْرَه النِّفَاق وَالتَّلَوُّن؟","Do you hate hypocrisy?"),10),
            (t("هَلْ تُجَاهِد نَفْسَك عَلَى تَرْك الْكَذِب؟","Do you struggle against lying?"),10),
            (t("هَلْ تَتَجَنَّب الْغِشّ؟","Do you avoid fraud?"),10),
            (t("هَلْ تَفِي بِعُهُودِك وَلَا تَخُون؟","Do you keep trusts?"),10),
            (t("هَلْ تَرْفُض الظُّلْم بِكُلّ صُوَرِه؟","Do you reject all injustice?"),10),
            (t("هَلْ تُجَاهِد نَفْسَك عَلَى تَرْك الْفَوَاحِش؟","Do you struggle against immorality?"),10),
            (t("هَلْ تُخْلِص عَمَلَك لِله؟","Is your work sincere?"),10),
            (t("هَلْ تُسَلِّم لِله وَلَا تَحْسُد؟","Do you accept Allah's decree?"),10),
            (t("هَلْ تُحِبّ فِي الله وَتُبْغِض فِي الله؟","Do you love & hate for Allah?"),10),
        ]
    }
    colA,colB=st.columns(2)
    with colA:
        st.subheader(t("🤍 الْوَلَاء (W)","🤍 Loyalty (W)"))
        for i,(q,v) in enumerate(questions["W"]):
            ans=st.radio(q,[t(f"نَعَم ({v})",f"Yes ({v})"),t(f"أَحْيَانًا ({v//2})",f"Sometimes ({v//2})"),t(f"لَا (0)",f"No (0)")],key=f"cw_{i}",index=None)
            if ans:
                if t("نَعَم","Yes") in ans: st.session_state.compass_answers[f"W{i}"]=v
                elif t("أَحْيَانًا","Sometimes") in ans: st.session_state.compass_answers[f"W{i}"]=v//2
                else: st.session_state.compass_answers[f"W{i}"]=0
    with colB:
        st.subheader(t("❤️ الْبَرَاءَة (B)","❤️ Disavowal (B)"))
        for i,(q,v) in enumerate(questions["B"]):
            ans=st.radio(q,[t(f"نَعَم ({v})",f"Yes ({v})"),t(f"أَحْيَانًا ({v//2})",f"Sometimes ({v//2})"),t(f"لَا (0)",f"No (0)")],key=f"cb_{i}",index=None)
            if ans:
                if t("نَعَم","Yes") in ans: st.session_state.compass_answers[f"B{i}"]=v
                elif t("أَحْيَانًا","Sometimes") in ans: st.session_state.compass_answers[f"B{i}"]=v//2
                else: st.session_state.compass_answers[f"B{i}"]=0

    if len(st.session_state.compass_answers)==28:
        Ws=sum(st.session_state.compass_answers[f"W{i}"] for i in range(14))/140.0
        Bs=sum(st.session_state.compass_answers[f"B{i}"] for i in range(14))/140.0
        Ss=Ws*Bs
        qn,qc=classify_quadrant(Ws,Bs)
        names={"believer":t("مُؤْمِن (Q1)","Believer (Q1)"),"disbeliever":t("كَافِر (Q2)","Disbeliever (Q2)"),
               "hypocrite":t("مُنَافِق (Q3)","Hypocrite (Q3)"),"polytheist":t("مُشْرِك (Q4)","Polytheist (Q4)")}
        advice={"believer":t("حَافِظ عَلَى ثَبَاتِك.","Keep your stability."),
                "disbeliever":t("بَاب التَّوْبَة مَفْتُوح.","Door of repentance is open."),
                "hypocrite":t("اصْدُق مَع نَفْسِك.","Be honest with yourself."),
                "polytheist":t("قَوِّ مَنَاعَتَك.","Strengthen your immunity.")}
        st.divider(); st.header(t("📊 نَتِيجَة الْبَوْصَلَة","📊 Compass Result"))
        c1,c2,c3=st.columns(3); c1.metric("W",f"{Ws:.2f}"); c2.metric("B",f"{Bs:.2f}"); c3.metric("S",f"{Ss:.2f}")
        st.markdown(f"<div style='text-align:center;padding:20px;background:rgba(10,10,46,0.8);border-radius:15px;border:2px solid {qc};margin:15px 0;'><h2 style='color:{qc};'>{names.get(qn,qn)}</h2><p style='color:#CCC;'>{advice.get(qn,'')}</p></div>",unsafe_allow_html=True)
        fig,ax=plt.subplots(figsize=(6,6),facecolor='#0a0a2e');ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2,1.2);ax.set_ylim(-1.2,1.2)
        ax.axhline(0,color='grey',lw=0.5);ax.axvline(0,color='grey',lw=0.5)
        ax.scatter(Bs*2-1,Ws*2-1,s=250,c='cyan',edgecolors='white',linewidth=3,zorder=10)
        ax.fill_between([0,1],0,1,alpha=0.15,color='#FFD700');ax.fill_between([-1,0],0,1,alpha=0.15,color='#FF5252')
        ax.fill_between([-1,0],-1,0,alpha=0.15,color='#FFB6C1');ax.fill_between([0,1],-1,0,alpha=0.15,color='#FFA500')
        ax.set_xlabel("B",color='white');ax.set_ylabel("W",color='white');ax.tick_params(colors='white')
        st.pyplot(fig)
        if st.button(t("🔄 إِعَادَة","🔄 Retake")): st.session_state.compass_answers={}; st.rerun()


# ═══════════════════════════════════════════════════════════════
# 📖 تبويب: كتاب الميزان (موسع)
# ═══════════════════════════════════════════════════════════════
with tab_book:
    st.header(t("📖 كِتَاب الْمِيزَان","📖 The Book of Mizan"))
    with st.expander(t("📜 الْإِهْدَاء وَالْمُقَدِّمَة","📜 Dedication & Introduction"),expanded=False):
        st.markdown(t("""
        **الْإِهْدَاء**: إِلَى كُلّ بَاحِث عَن الْحَقِيقَة، وَكُلّ قَلْب حَائِر، وَكُلّ عَقْل مُتَعَطِّش لِرُؤْيَة كَيْف يَلْتَقِي الْوَحْي بِالْعِلْم.
        **مُقَدِّمَة الْمُؤَلِّف**: الْحَمْد لِله الَّذِي رَفَع السَّمَاء وَوَضَع الْمِيزَان. هَذَا كِتَاب "الْمِيزَان". يُقَدِّم "الدِّين الْقَيِّم" وَ"الْإِسْلَام الْحَنِيف" كَمَنْظُومَة مُتَكَامِلَة.
        """,
        """
        **Dedication**: To every seeker of truth...
        **Author's Introduction**: Praise be to Allah. This is the Book of Mizan.
        """))
    with st.expander(t("⚖️ مُعَادَلَة الثَّبَات الْوُجُودِيّ","⚖️ Existential Stability Equation"),expanded=False):
        st.markdown(t("""
        **S = W × B**
        - **W (الْوَلَاء)**: طَاقَة الْحُبّ وَالطَّاعَة وَالنُّصْرَة لِله وَرَسُولِه وَالْمُؤْمِنِين.
        - **B (الْبَرَاءَة)**: طَاقَة الْبُغْض وَالْمُفَاصَلَة وَالْمَنَاعَة مِن الْكُفْر وَالشِّرْك وَالطَّاغُوت.
        - **S (الثَّبَات)**: الْعُرْوَة الْوُثْقَى – حَالَة الِاسْتِقْرَار الْوُجُودِيّ.
        لِمَاذَا الضَّرْب؟ لِأَن الْعَلَاقَة شَرْطِيَّة. لَا يَصِحّ إِيمَان بِلَا بَرَاءَة.
        """,
        """
        **S = W × B**
        - **W (Loyalty)**: Energy of love, obedience, support.
        - **B (Disavowal)**: Energy of hatred, dissociation, immunity.
        - **S (Stability)**: The firm handhold.
        Why multiplication? Because the relationship is conditional.
        """))
    with st.expander(t("💫 الِاسْتِدْرَاج","💫 Istidraj"),expanded=False):
        st.markdown(t("""
        تَأَخُّر انْهِيَار التَّمْكِين الْمَادِّيّ (E) عَن انْهِيَار الثَّبَات الْأَخْلَاقِيّ (S).
        ﴿فَلَمَّا نَسُوا مَا ذُكِّرُوا بِه فَتَحْنَا عَلَيْهِم أَبْوَاب كُلّ شَيْء حَتَّى إِذَا فَرِحُوا بِمَا أُوتُوا أَخَذْنَاهُم بَغْتَة﴾
        """,
        """
        Delayed collapse of material empowerment (E) after moral stability (S).
        """))
    with st.expander(t("🕌 مَوْلِدَات الطَّاقَة","🕌 Energy Generators"),expanded=False):
        st.markdown(t("""
        - **الْعِبَادَات**: الصَّلَاة (W)، الزَّكَاة (B)، الصَّوْم (B)، الْحَجّ (W).
        - **الْأَخْلَاق**: الصِّدْق، الْأَمَانَة، الْوَفَاء (W)، الْعَفَّة، الشَّهَادَة بِالْحَقّ (B).
        - **الْمُوَالَاة وَالْبَرَاءَة**: مُوَالَاة الْمُؤْمِنِين (W)، الْبَرَاءَة مِن الْكُفَّار (B)، الْجِهَاد بِأَنْوَاعِه (B).
        """,
        """
        - **Worship**: Prayer (W), Zakat (B), Fasting (B), Hajj (W).
        - **Ethics**: Truthfulness (W), Chastity (B)...
        - **Loyalty & Disavowal**: Alliance with believers (W), Disavowal of disbelievers (B), Jihad (B).
        """))
    with st.expander(t("🌍 وَحْدَة الْخَلْق وَالْأَمْر","🌍 Unity of Creation & Command"),expanded=False):
        st.markdown(t("""
        ﴿أَلَا لَه الْخَلْق وَالْأَمْر﴾
        - الذَّرَّة تَسْتَقِرّ بِتَوَازُن الْجَذْب (W) وَالتَّنَافُر (B).
        - الْخَلِيَّة تَحْيَا بِتَوَازُن التَّغْذِيَة (W) وَالْمَنَاعَة (B).
        - الْحَضَارَة تَصْمُد بِتَوَازُن الْوَلَاء (W) وَالْبَرَاءَة (B).
        """,
        """
        ﴿Unquestionably, His is the creation and the command﴾
        - Atom: stable by attraction (W) and repulsion (B).
        - Cell: alive by nutrition (W) and immunity (B).
        - Civilization: stands by loyalty (W) and disavowal (B).
        """))


# ═══════════════════════════════════════════════════════════════
# 🔤 تبويب: المعجم الهندسي
# ═══════════════════════════════════════════════════════════════
with tab_lexicon:
    st.header(t("🔤 الْمُعْجَم الْهَنْدَسِيّ لِلْقُرْآن","🔤 Geometric Lexicon of the Quran"))
    tools = {
        t("فَاء السَّبَبِيَّة (فَـ)","Causative Fa"): ("فَـ(قيمة)", t("مُشَغِّل الْقِيمَة الْمِعْيَارِيَّة. يَجْعَل مَا بَعْدَه سَبَبًا ثَابِتًا.","Standard Value Operator.")),
        t("وَاو الْمَعِيَّة – الضَّرْب","Waw Multiplication"): ("×", t("رَبْط شَرْطِيّ.","Conditional conjunction.")),
        t("وَاو الِاسْتِئْنَاف – الْجَمْع","Waw Addition"): ("+", t("جَمْع تَرَاكُمِيّ.","Cumulative addition.")),
        t("لَام الِاسْتِحْقَاق","Lām of Entitlement"): ("→/=", t("سَهْم وَعَلَامَة تَسْوِيَة مَعًا. عَطَاء مُبَاشِر.","Arrow & Equals.")),
        t("إِلَّا","Illa (Except)"): ("{}", t("حُدُود الْمَجْمُوعَة.","Set boundaries.")),
        t("حَتَّى الْغَائِيَّة","Hatta"): ("...", t("اسْتِمْرَار السَّبَب.","Continuation.")),
        t("كَلَّا","Kalla"): ("⛔", t("قَطْع الْمُعَادَلَات الْفَاسِدَة.","Severing false equations.")),
    }
    sel = st.selectbox(t("اخْتَر أَدَاة:","Select tool:"),list(tools.keys()))
    if sel: st.metric(t("الرَّمْز","Symbol"),tools[sel][0]); st.info(tools[sel][1])


# ═══════════════════════════════════════════════════════════════
# 📜 تبويب: رسالة الترحيب
# ═══════════════════════════════════════════════════════════════
with tab_welcome:
    st.header(t("📜 رِسَالَة التَّرْحِيب","📜 Welcome Message"))
    st.markdown(t("""
    <div style="text-align:center;font-size:1.1em;line-height:2.2;color:#CCC;">
    > "هَلْ يُوجَد قَانُون وَاحِد يَحْكُم الذَّرَّة وَالْحَضَارَة؟"<br>
    > هَذَا هُو نَمُوذَج الْمِيزَان الَّذِي يُثْبِت أَن <b style="color:#FFD700;">S = W × B</b>
    ---
    <b>الْمَنْصَة الذَّهَبِيَّة</b> هِي نِظَام إِثْبَات رَقْمِيّ. تَجْمَع بَيْن الْكِتَاب الْمَسْطُور وَالْكِتَاب الْمَنْظُور،
    وَتَسْتَنِد إِلَى الْفِطْرَة وَالْعَقْل وَالسُّنَن الْإِلَهِيَّة.
    ---
    <b style="color:#FFD700;">
    ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾<br>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    </b>
    ---
    > "أَيُّهَا الْبَشَر، لَسْتُمْ فِي فَوْضَى. هُنَاك قَانُون. هُنَاك نِظَام. هُنَاك مِيزَان."
    </div>
    """,
    """
    <div style="text-align:center;font-size:1.1em;line-height:2.2;color:#CCC;">
    > "Is there a single law governing the atom and civilization?"<br>
    > This is the Mizan Model that proves <b style="color:#FFD700;">S = W × B</b>
    ---
    <b>The Golden Platform</b> is a digital proof system.
    ---
    <b style="color:#FFD700;">
    ﴿And the heaven He raised and imposed the balance﴾<br>
    ﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾
    </b>
    ---
    > "O humanity, you are not in chaos. There is a law. There is a system. There is a balance."
    </div>
    """), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 🏁 التذييل – شهادة الحق
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:25px;color:#888;font-size:0.9em;line-height:1.8;">
    <p>© {__YEAR__} {__AUTHOR__}</p>
    <p>{__LICENSE__} | {__VERSION__}</p>
    <p style="color:#FFD700;font-size:1.5em;margin-top:10px;">⚖️ {__SIGNATURE__}</p>
    <p style="font-size:0.8em;">{t('عِلْم الْمِيزَان – عِلْم الثَّبَات الْوُجُودِيّ','Mizan Science – The Science of Existential Stability')}</p>
</div>
""", unsafe_allow_html=True)

print("✅✅✅ النُّسْخَة النِّهَائِيَّة الْكَامِلَة جَاهِزَة لِلنَّشْر. ⚖️")
