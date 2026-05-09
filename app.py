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

st.set_page_config(page_title="المنصة الذهبية – The Golden Platform", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

__AUTHOR__ = "علي عادل العاطفي | Ali Adel Alatifi"
__YEAR__ = 2026
__LICENSE__ = "MIT License"
__VERSION__ = "2.0.0 – The Golden Platform (The New Science)"
__SIGNATURE__ = "⚖️ S = W × B"

if "lang" not in st.session_state: st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(ar_text, en_text): return ar_text if LANG == "ar" else en_text

MIZAN_LETTERS = {
    "light": {
        "أ":{"value":1,"label":{"ar":"الوحدانية","en":"Oneness"},"aya":"إِيَّاكَ نَعْبُدُ"},
        "ل":{"value":30,"label":{"ar":"المُلك","en":"Sovereignty"},"aya":"إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ"},
        "م":{"value":40,"label":{"ar":"الجمع","en":"Gathering"},"aya":"إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ"},
        "ر":{"value":200,"label":{"ar":"اليقظة","en":"Vigilance"},"aya":"فَإِذَا فَرَغْتَ فَانصَبْ"},
        "ك":{"value":20,"label":{"ar":"الأمر","en":"Command"},"aya":"كُن فَيَكُونُ"},
        "هـ":{"value":5,"label":{"ar":"الهوية","en":"Identity"},"aya":"وَاجْتَنِبُوا الطَّاغُوتَ"},
        "ي":{"value":10,"label":{"ar":"الاستجابة","en":"Response"},"aya":"اسْتَجِيبُوا لِلَّهِ وَلِلرَّسُولِ"},
        "ع":{"value":70,"label":{"ar":"الإدراك","en":"Perception"},"aya":"وَقُل رَّبِّ زِدْنِي عِلْمًا"},
        "ص":{"value":90,"label":{"ar":"الصمد","en":"The Eternal"},"aya":"اللَّهُ الصَّمَدُ"},
        "ق":{"value":100,"label":{"ar":"الميزان","en":"The Balance"},"aya":"وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ"},
        "ن":{"value":50,"label":{"ar":"النور","en":"Light"},"aya":"اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ"},
        "س":{"value":60,"label":{"ar":"السمع","en":"Hearing"},"aya":"سَمِعْنَا وَأَطَعْنَا"},
        "ح":{"value":8,"label":{"ar":"الحياة","en":"Life"},"aya":"فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً"},
        "ط":{"value":9,"label":{"ar":"الطهارة","en":"Purity"},"aya":"إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ"},
    },
    "neutral": {
        "ف":{"value":80,"label":{"ar":"فاء السببية","en":"Causative Fa"},"role":"=","aya":"فَمَن يَكْفُرْ بِالطَّاغُوتِ..."},
        "و":{"value":6,"label":{"ar":"واو العطف","en":"Conjunctive Waw"},"role":"×/+","aya":"وَيُؤْمِن بِاللَّهِ"},
        "ب":{"value":2,"label":{"ar":"باء الاستعانة","en":"Instrumental Ba"},"role":"بـ","aya":"بِسْمِ اللَّهِ الرَّحْمَٰنِ"},
        "ل":{"value":30,"label":{"ar":"لام التعليل","en":"Purpose Lam"},"role":"→","aya":"لِيَعْبُدُونِ"},
        "ت":{"value":400,"label":{"ar":"تاء الفاعل","en":"Subject Ta"},"role":"ف","aya":"قَالَتِ امْرَأَتُ فِرْعَوْنَ"},
        "ث":{"value":500,"label":{"ar":"ثم العطف","en":"Then Tha"},"role":"ت","aya":"ثُمَّ خَلَقْنَا النُّطْفَةَ"},
    },
    "dark": {
        "ظ":{"value":900,"label":{"ar":"الظلم","en":"Injustice"},"aya":"إِنَّ الظَّالِمِينَ لَهُمْ عَذَابٌ أَلِيمٌ"},
        "ض":{"value":800,"label":{"ar":"الضلال","en":"Misguidance"},"aya":"وَمَن يُضْلِلِ اللَّهُ فَمَا لَهُ مِنْ هَادٍ"},
        "غ":{"value":1000,"label":{"ar":"الغش","en":"Fraud"},"aya":"مَنْ غَشَّنَا فَلَيْسَ مِنَّا"},
        "ذ":{"value":700,"label":{"ar":"الذل","en":"Humiliation"},"aya":"أَذِلَّةٍ عَلَى الْمُؤْمِنِينَ"},
        "خ":{"value":600,"label":{"ar":"الخيانة","en":"Betrayal"},"aya":"لَا تَخُونُوا اللَّهَ وَالرَّسُولَ"},
        "ش":{"value":300,"label":{"ar":"الشهوة","en":"Lust"},"aya":"وَلَا تَتَّبِعِ الْهَوَىٰ"},
        "ز":{"value":7,"label":{"ar":"الزور","en":"Falsehood"},"aya":"وَاجْتَنِبُوا قَوْلَ الزُّورِ"},
        "ج":{"value":3,"label":{"ar":"الجهل","en":"Ignorance"},"aya":"بَلْ أَكْثَرُهُمْ يَجْهَلُونَ"},
    }
}

LETTER_CATEGORIES = {
    "source": {
        "ك":{"value":20,"role":"الأمر - التفعيل","equation_role":"activation"},
        "ن":{"value":50,"role":"النور - الوضوح","equation_role":"clarity"},
    },
    "tajalli": {
        "أ":{"value":1,"role":"الوحدانية","affects":"unity","equation_role":"w_boost"},
        "ل":{"value":30,"role":"المُلك والعدل","affects":"w","equation_role":"w_boost"},
        "م":{"value":40,"role":"الجمع والتماسك","affects":"b","equation_role":"b_boost"},
        "ر":{"value":200,"role":"اليقظة والمراقبة","affects":"resistance","equation_role":"resistance"},
        "س":{"value":60,"role":"السمع والاستجابة","affects":"responsiveness","equation_role":"learning_rate"},
        "ح":{"value":8,"role":"الحياة والاستدامة","affects":"sustainability","equation_role":"decay_resist"},
        "ط":{"value":9,"role":"الطهارة والمناعة","affects":"b","equation_role":"purification"},
    },
    "ishtirak": {
        "ع":{"value":70,"role":"الإدراك والعلم","affects":"w","equation_role":"w_multiplier"},
        "ي":{"value":10,"role":"الاستجابة والدعاء","affects":"b","equation_role":"b_multiplier"},
        "هـ":{"value":5,"role":"الهوية والمعية","affects":"e_resist","equation_role":"e_dampener"},
        "ق":{"value":100,"role":"الميزان والقسط","affects":"balance","equation_role":"normalizer"},
    },
    "dual": {
        "ص":{"value":90,"constant_role":"الصمد","variable_role":"الصبر والصدق والصلاة","affects":"w","equation_role":"w_boost"},
        "ق_متغير":{"value":100,"variable_role":"القسط والعدل","affects":"b","equation_role":"b_boost"},
    },
    "operators": {
        "ف":{"value":80,"operator":"=","role":"فاء السببية - حتمية"},
        "و":{"value":6,"operator":"×/+","role":"واو العطف - شرط أو جمع"},
        "ب":{"value":2,"operator":"بـ","role":"باء الاستعانة - غاية"},
        "ل":{"value":30,"operator":"→","role":"لام التعليل - اتجاه"},
    },
    "actions": {
        "ج":{"value":3,"positive":"الجهاد والجود","negative":"الجهل والجحود","affects":"b"},
        "خ":{"value":600,"positive":"الخير والخشية","negative":"الخيانة والخذلان","affects":"w"},
        "د":{"value":4,"positive":"الدين والدعوة","negative":"الدولة والغلبة","affects":"w"},
        "ذ":{"value":700,"positive":"الذكر والذوق","negative":"الذل والذنب","affects":"b"},
        "ز":{"value":7,"positive":"الزكاة والزهد","negative":"الزور والزيغ","affects":"b"},
        "ش":{"value":300,"positive":"الشكر والشجاعة","negative":"الشهوة والشرك","affects":"w"},
        "ت":{"value":400,"positive":"التوبة والتقوى","negative":"التيه","affects":"w"},
        "ث":{"value":500,"positive":"الثبات والثواب","negative":"الثبور","affects":"w"},
        "ض":{"value":800,"positive":"الضياء","negative":"الضلال","affects":"b"},
        "ظ":{"value":900,"positive":"الظفر","negative":"الظلم","affects":"both"},
        "غ":{"value":1000,"positive":"الغفران","negative":"الغش","affects":"b"},
    }
}

LETTER_TOOLTIPS = {
    "taj_أ":{"ar":"الوحدانية – أصل الولاء: كلما تجلت، زاد تماسك النظام.","en":"Oneness – root of loyalty."},
    "taj_ل":{"ar":"المُلك والعدل – يقوي W: السيادة لله والعدل في الحكم.","en":"Sovereignty & justice – boosts W."},
    "taj_م":{"ar":"الجمع والتماسك – يقوي B: وحدة الصف والجماعة.","en":"Gathering – boosts B."},
    "taj_ر":{"ar":"اليقظة والمراقبة – المقاومة: الخوف من الله والحياء (يمنع الانهيار).","en":"Vigilance – resistance."},
    "taj_س":{"ar":"السمع والاستجابة – سرعة التوبة: ﴿سَمِعْنَا وَأَطَعْنَا﴾.","en":"Hearing & response – repentance speed."},
    "taj_ح":{"ar":"الحياة والاستدامة – الحج: يجدد الإيمان ويمنع التآكل.","en":"Life & sustainability – Hajj."},
    "taj_ط":{"ar":"الطهارة والمناعة – الصيام: يطهر الروح ويقوي البراءة.","en":"Purity & immunity – Fasting."},
    "ish_ع":{"ar":"الإدراك والعلم – يضاعف W: ﴿رَّبِّ زِدْنِي عِلْمًا﴾.","en":"Perception & knowledge – multiplies W."},
    "ish_ي":{"ar":"الاستجابة والدعاء – يضاعف B: دعاء الله والتضرع.","en":"Response & supplication – multiplies B."},
    "ish_هـ":{"ar":"الهوية والمعية – يقلل تأثير الدنيا (E): حب الله.","en":"Identity & closeness – dampens E."},
    "ish_ق":{"ar":"الميزان والقسط – يضبط المعادلة كلها.","en":"Balance & equity – normalizes equation."},
    "dual_ص":{"ar":"الصبر والصدق والصلاة – الوجه المتغير للصمد: يقوي W.","en":"Patience & truthfulness – boosts W."},
    "dual_ق_متغير":{"ar":"القسط والعدل – الوجه المتغير للقاف: يقوي B.","en":"Equity & justice – boosts B."},
    "act_ج":{"ar":"الجهاد والجود (+) / الجهل والجحود (-) – يؤثر على B.","en":"Jihad & generosity (+) / Ignorance (-) – affects B."},
    "act_خ":{"ar":"الخير والخشية (+) / الخيانة والخذلان (-) – يؤثر على W.","en":"Goodness (+) / Betrayal (-) – affects W."},
    "act_د":{"ar":"الدين والدعوة (+) / الدولة والغلبة (-) – يؤثر على W.","en":"Religion & calling (+) / Mere power (-) – affects W."},
    "act_ذ":{"ar":"الذكر والذوق (+) / الذل والذنب (-) – يؤثر على B.","en":"Remembrance (+) / Humiliation (-) – affects B."},
    "act_ز":{"ar":"الزكاة والزهد (+) / الزور والزيغ (-) – يؤثر على B.","en":"Zakat & asceticism (+) / Falsehood (-) – affects B."},
    "act_ش":{"ar":"الشكر والشجاعة (+) / الشهوة والشرك (-) – يؤثر على W.","en":"Gratitude & courage (+) / Lust (-) – affects W."},
    "act_ت":{"ar":"التوبة والتقوى (+) / التيه (-) – يؤثر على W.","en":"Repentance & piety (+) / Wandering (-) – affects W."},
    "act_ث":{"ar":"الثبات والثواب (+) / الثبور (-) – يؤثر على W.","en":"Steadfastness (+) / Destruction (-) – affects W."},
    "act_ض":{"ar":"الضياء (+) / الضلال (-) – يؤثر على B.","en":"Radiance (+) / Misguidance (-) – affects B."},
    "act_ظ":{"ar":"الظفر (+) / الظلم (-) – يؤثر على W و B معًا.","en":"Victory (+) / Injustice (-) – affects both."},
    "act_غ":{"ar":"الغفران (+) / الغش (-) – يؤثر على B.","en":"Forgiveness (+) / Fraud (-) – affects B."},
}

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

def calc_S(W, B, E, q_val=100, n_val=50, k_val=20,
          tajalli_intensity=None, ishtirak_intensity=None,
          dual_intensity=None, actions_intensity=None,
          amr_val=0.5, nahy_val=0.5, adl_val=0.6, shura_val=0.5,
          riba_val=0.2, zulm_val=0.2, khianah_val=0.2):
    W_eff, B_eff = W, B
    source_factor = (k_val * n_val) / 1000.0
    S_base = W_eff * B_eff * (1 + source_factor)
    resistance, decay_resist, purity, unity = 1.0, 1.0, 1.0, 1.0
    
    if tajalli_intensity is not None:
        if 'ل' in tajalli_intensity: W_eff *= (1 + 30 * tajalli_intensity['ل'] / 1000)
        if 'م' in tajalli_intensity: B_eff *= (1 + 40 * tajalli_intensity['م'] / 1000)
        if 'ر' in tajalli_intensity: resistance = 1 + 200 * tajalli_intensity['ر'] / 1000
        if 'ح' in tajalli_intensity: decay_resist = 1 + 8 * tajalli_intensity['ح'] / 100
        if 'ط' in tajalli_intensity: purity = 1 + 9 * tajalli_intensity['ط'] / 100
        if 'أ' in tajalli_intensity: unity = 1 + 1 * tajalli_intensity['أ'] / 100
        S_base = W_eff * B_eff * (1 + source_factor)
        S_base *= resistance * decay_resist * purity * unity
    
    normalizer = 1.0
    if ishtirak_intensity is not None:
        if 'ع' in ishtirak_intensity: W_eff *= (1 + 70 * ishtirak_intensity['ع'] / 1000)
        if 'ي' in ishtirak_intensity: B_eff *= (1 + 10 * ishtirak_intensity['ي'] / 100)
        if 'ق' in ishtirak_intensity: normalizer = 1 + 100 * ishtirak_intensity['ق'] / 1000
        S_base = W_eff * B_eff * (1 + source_factor) * normalizer
    
    if dual_intensity is not None:
        if 'ص' in dual_intensity: W_eff *= (1 + 90 * dual_intensity['ص'] / 1000)
        if 'ق_متغير' in dual_intensity: B_eff *= (1 + 100 * dual_intensity['ق_متغير'] / 1000)
        S_base = W_eff * B_eff * (1 + source_factor)
    
    if actions_intensity is not None:
        positive_sum, negative_sum = 0, 0
        for letter, intensity in actions_intensity.items():
            if letter not in LETTER_CATEGORIES["actions"]: continue
            lv = LETTER_CATEGORIES["actions"][letter]["value"]
            aff = LETTER_CATEGORIES["actions"][letter]["affects"]
            if intensity > 0:
                positive_sum += intensity * lv
                f = 1 + intensity * lv / 1000
                if aff == "w": W_eff *= f
                elif aff == "b": B_eff *= f
                elif aff == "both": W_eff *= (1 + intensity * lv / 2000); B_eff *= (1 + intensity * lv / 2000)
            elif intensity < 0:
                ni = abs(intensity)
                negative_sum += ni * lv
                f = 1 - ni * lv / 1000
                if aff == "w": W_eff *= f
                elif aff == "b": B_eff *= f
                elif aff == "both": W_eff *= (1 - ni * lv / 2000); B_eff *= (1 - ni * lv / 2000)
        inhibitor = negative_sum / 10000
        enhancer = positive_sum / 10000
        S_base = W_eff * B_eff * (1 + source_factor)
        S_base *= (1 + enhancer) / (1 + max(inhibitor, 0.001))
    
    S_base *= (0.5 + 0.5 * (amr_val * nahy_val))
    S_base *= (0.8 + 0.4 * adl_val)
    S_base *= (0.85 + 0.3 * shura_val)
    S_base *= (1 - 0.3 * riba_val)
    S_base *= (1 - 0.25 * zulm_val)
    S_base *= (1 - 0.15 * khianah_val)
    if tajalli_intensity and 'ط' in tajalli_intensity: S_base *= purity
    if tajalli_intensity and 'ح' in tajalli_intensity: S_base *= decay_resist
    return np.clip(S_base, 0.001, 1.0)
              
with st.sidebar:
    lang_choice = st.radio("اللغة / Language", ["العربية", "English"], index=0 if LANG == "ar" else 1)
    if (lang_choice == "English" and LANG == "ar") or (lang_choice == "العربية" and LANG == "en"):
        st.session_state.lang = "en" if lang_choice == "English" else "ar"
        st.rerun()
    st.markdown("---")
    
    st.header(t("⚙️ المعاملات الأساسية", "⚙️ Basic Parameters"))
    W_init = st.slider(t("W الابتدائي", "Initial W"), 0.0, 1.0, 0.55, 0.01, key="s_W")
    B_init = st.slider(t("B الابتدائي", "Initial B"), 0.0, 1.0, 0.52, 0.01, key="s_B")
    delay = st.slider(t("فجوة الاستدراج", "Istidraj Gap"), 5, 50, 22, 1, key="s_delay")
    N_STARS = st.slider(t("عدد النجوم", "Number of Stars"), 100, 600, 300, 50, key="s_N")
    st.markdown("---")
    
    st.header(t("🔮 الثوابت الإلهية (المصدر)", "🔮 Divine Constants (Source)"))
    k_val = st.slider(t("ك (الأمر)", "Kaf (Command)"), 10, 200, 20, 10, key="s_k")
    n_val = st.slider(t("ن (النور)", "Nun (Light)"), 5, 100, 50, 5, key="s_n")
    s_val = st.slider(t("ص (الصمد)", "Sad (Eternal)"), 10, 200, 90, 10, key="s_s")
    q_val = st.slider(t("ق (الميزان)", "Qaf (Balance)"), 10, 200, 100, 10, key="s_q")
    st.markdown("---")
    
    st.header(t("🏛️ أسس الحكم", "🏛️ Governance"))
    amr_val = st.slider(t("الأمر بالمعروف", "Enjoining Good"), 0.0, 1.0, 0.5, 0.01, key="s_amr")
    nahy_val = st.slider(t("النهي عن المنكر", "Forbidding Evil"), 0.0, 1.0, 0.5, 0.01, key="s_nahy")
    adl_val = st.slider(t("العدل", "Justice"), 0.0, 1.0, 0.6, 0.01, key="s_adl")
    shura_val = st.slider(t("الشورى", "Consultation"), 0.0, 1.0, 0.5, 0.01, key="s_shura")
    st.markdown("---")
    
    st.header(t("💀 قوى الضلال", "💀 Forces of Darkness"))
    riba_val = st.slider(t("الربا", "Usury"), 0.0, 1.0, 0.2, 0.01, key="s_riba")
    zulm_val = st.slider(t("الظلم", "Injustice"), 0.0, 1.0, 0.2, 0.01, key="s_zulm")
    khianah_val = st.slider(t("الخيانة", "Betrayal"), 0.0, 1.0, 0.2, 0.01, key="s_khianah")
    st.markdown("---")
    
    st.header(t("🔆 حروف التجلي (صفات الله)", "🔆 Tajalli Letters"))
    tajalli_intensity = {}
    for letter, data in LETTER_CATEGORIES["tajalli"].items():
        key = f"s_taj_{letter}"
        help_text = LETTER_TOOLTIPS.get(f"taj_{letter}", {}).get(LANG, "")
        tajalli_intensity[letter] = st.slider(f"{letter} ({data['role']})", 0.0, 1.0, 0.7, 0.01, key=key, help=help_text)
    st.markdown("---")
    
    st.header(t("🔄 حروف الاشتراك (قنوات)", "🔄 Ishtirak Letters"))
    ishtirak_intensity = {}
    for letter, data in LETTER_CATEGORIES["ishtirak"].items():
        key = f"s_ish_{letter}"
        help_text = LETTER_TOOLTIPS.get(f"ish_{letter}", {}).get(LANG, "")
        ishtirak_intensity[letter] = st.slider(f"{letter} ({data['role']})", 0.0, 1.0, 0.7, 0.01, key=key, help=help_text)
    st.markdown("---")
    
    st.header(t("⚖️ حروف الازدواج (وجه متغير)", "⚖️ Dual Letters"))
    dual_intensity = {}
    for letter, data in LETTER_CATEGORIES["dual"].items():
        key = f"s_dual_{letter}"
        help_text = LETTER_TOOLTIPS.get(f"dual_{letter}", {}).get(LANG, "")
        role_text = data.get("variable_role", data.get("constant_role", ""))
        dual_intensity[letter] = st.slider(f"{letter} ({role_text})", 0.0, 1.0, 0.7, 0.01, key=key, help=help_text)
    st.markdown("---")
    
    st.header(t("⚡ حروف الأعمال (إيجابي/سلبي)", "⚡ Action Letters"))
    actions_intensity = {}
    for letter, data in LETTER_CATEGORIES["actions"].items():
        key = f"s_act_{letter}"
        help_text = LETTER_TOOLTIPS.get(f"act_{letter}", {}).get(LANG, "")
        pos_label = data["positive"]
        neg_label = data["negative"]
        actions_intensity[letter] = st.slider(f"{letter} ({pos_label} / {neg_label})", -1.0, 1.0, 0.0, 0.1, key=key, help=help_text)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(t("▶️ تشغيل المحاكاة", "▶️ Run Simulation"), use_container_width=True, type="primary"):
            st.session_state.run = True
    with col2:
        if st.button(t("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True):
            st.session_state.run = False
    with col3:
        if st.button(t("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
            keys_to_keep = ["lang"]
            for k in list(st.session_state.keys()):
                if k not in keys_to_keep: del st.session_state[k]
            st.rerun()
            
    st.markdown(f"""
<div style="text-align: center; padding: 20px 0 10px 0;">
    <h1 style="color: #FFD700; font-size: 2.5em; margin-bottom: 0;">⚖️ {t('المنصة الذهبية', 'The Golden Platform')}</h1>
    <h2 style="color: #FFD700; font-size: 1.3em; margin-top: 0;">{t('S = W × B | من الذرة إلى الحضارة', 'S = W × B | From Atom to Civilization')}</h2>
    <p style="color: #AAA; font-size: 0.9em; margin-top: 5px;">{t('نظرية الميزان – علم الثبات الوجودي', 'The Mizan Theory – Science of Existential Stability')}</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t("🏛️ المختبر الجماعي", "🏛️ The Collective Lab"),
    t("🧍 البوصلة الشخصية", "🧍 Personal Compass"),
    t("📖 كتاب الميزان", "📖 The Book of Mizan"),
    t("🔤 المعجم الهندسي", "🔤 Geometric Lexicon"),
    t("📜 رسالة الترحيب", "📜 Welcome Message"),
])

with tab1:
    st.header(t("🏛️ المختبر الجماعي – محاكاة الثبات الحي", "🏛️ The Collective Lab – Live Stability Simulation"))
    st.markdown(t(
        "شاهد كيف يتفاعل الولاء (W) والبراءة (B) في مجتمع حي. كل نجمة تمثل فرداً، ولونها يعكس موقعه في الأرباع الوجودية الأربعة.",
        "Watch how Loyalty (W) and Disavowal (B) interact in a living society. Each star represents an individual."
    ))

    if 'run' not in st.session_state: st.session_state.run = False
    if 'init' not in st.session_state: st.session_state.init = False

    if not st.session_state.init:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        sx = np.random.uniform(cx - 13, cx + 13, N_STARS)
        sy = np.random.uniform(cy - 9, cy + 9, N_STARS)
        sw = np.random.uniform(0.1, 1.0, N_STARS)
        sb = np.random.uniform(0.1, 1.0, N_STARS)
        W, B, E = W_init, B_init, 0.3
        S = calc_S(W, B, E, q_val=q_val, n_val=n_val, k_val=k_val,
                   tajalli_intensity=tajalli_intensity, ishtirak_intensity=ishtirak_intensity,
                   dual_intensity=dual_intensity, actions_intensity=actions_intensity,
                   amr_val=amr_val, nahy_val=nahy_val, adl_val=adl_val, shura_val=shura_val,
                   riba_val=riba_val, zulm_val=zulm_val, khianah_val=khianah_val)
        phase = t("توازن", "Balance")
        cycle_angle, angle_W, angle_B = 0.0, 0.0, np.pi * 0.5
        eb = deque([S] * 30, maxlen=30)
        pS, pE, px, pc = deque(maxlen=400), deque(maxlen=400), deque(maxlen=400), 0
        
        st.session_state.cx, st.session_state.cy = cx, cy
        st.session_state.sx, st.session_state.sy = sx, sy
        st.session_state.sw, st.session_state.sb = sw, sb
        st.session_state.W, st.session_state.B, st.session_state.E, st.session_state.S = W, B, E, S
        st.session_state.phase, st.session_state.cycle_angle = phase, cycle_angle
        st.session_state.angle_W, st.session_state.angle_B = angle_W, angle_B
        st.session_state.empowerment_buffer = eb
        st.session_state.history_S, st.session_state.history_E, st.session_state.history_x = pS, pE, px
        st.session_state.frame_count = pc
        st.session_state.init = True

    if st.session_state.init and not st.session_state.run:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric(t("W (الولاء)", "W (Loyalty)"), f"{st.session_state.W:.3f}")
        col2.metric(t("B (البراءة)", "B (Disavowal)"), f"{st.session_state.B:.3f}")
        col3.metric(t("S (الثبات)", "S (Stability)"), f"{st.session_state.S:.3f}")
        col4.metric(t("E (التمكين)", "E (Empowerment)"), f"{st.session_state.E:.3f}")
        col5.metric(t("الطور", "Phase"), st.session_state.phase)
        st.info(t("اضغط على ▶️ تشغيل المحاكاة في الشريط الجانبي.", "Press ▶️ Run Simulation in the sidebar."))
        
        if st.session_state.get("run", False):
    placeholder = st.empty()
    while st.session_state.get("run", False):
        W = st.session_state.W; B = st.session_state.B; E = st.session_state.E
        S = st.session_state.S; phase = st.session_state.phase
        cycle_angle = st.session_state.cycle_angle
        angle_W = st.session_state.angle_W; angle_B = st.session_state.angle_B
        sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
        sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
        cx = st.session_state.cx; cy = st.session_state.cy
        eb = st.session_state.empowerment_buffer
        pS = st.session_state.history_S.copy(); pE = st.session_state.history_E.copy()
        px = st.session_state.history_x.copy(); pc = st.session_state.frame_count

        cycle_angle += 0.008; sv = np.sin(cycle_angle)
        if sv > 0.5: phase = t('ذروة الاستقرار', 'Peak Stability')
        elif sv > 0: phase = t('صعود', 'Rising')
        elif sv > -0.5: phase = t('انهيار', 'Collapse')
        else: phase = t('القاع', 'Rock Bottom')
        if 0.3 < sv < 0.35: phase = t('>> استدراج <<', '>> Istidraj <<')
        target_S = 0.5 + 0.45 * sv

        for i in range(N_STARS):
            dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
            close = (dist < 2.0) & (np.arange(N_STARS) != i)
            sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
            sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
            if np.any(close):
                sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03
                sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03
            sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

        if random.random() < 0.005:
            aff = np.random.choice(N_STARS, size=int(N_STARS * 0.2), replace=False)
            sw[aff] *= np.random.uniform(0.5, 0.8); sb[aff] *= np.random.uniform(0.5, 0.8)

        avgW, avgB = np.mean(sw), np.mean(sb)
        W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
        W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)

        S = calc_S(W, B, E, q_val=q_val, n_val=n_val, k_val=k_val,
                   tajalli_intensity=tajalli_intensity, ishtirak_intensity=ishtirak_intensity,
                   dual_intensity=dual_intensity, actions_intensity=actions_intensity,
                   amr_val=amr_val, nahy_val=nahy_val, adl_val=adl_val, shura_val=shura_val,
                   riba_val=riba_val, zulm_val=zulm_val, khianah_val=khianah_val)

        eb.append(S)
        E_target = list(eb)[-delay] if len(eb) >= delay else S
        E += 0.03 * (E_target - E)
        W = W - 0.015 * E + 0.03 / (S + 0.1) - 0.007 * (1 - B)
        B = B - 0.012 * E + 0.006 * (1 - B) * W * (1 - W)
        W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)

        S = calc_S(W, B, E, q_val=q_val, n_val=n_val, k_val=k_val,
                   tajalli_intensity=tajalli_intensity, ishtirak_intensity=ishtirak_intensity,
                   dual_intensity=dual_intensity, actions_intensity=actions_intensity,
                   amr_val=amr_val, nahy_val=nahy_val, adl_val=adl_val, shura_val=shura_val,
                   riba_val=riba_val, zulm_val=zulm_val, khianah_val=khianah_val)

        pc += 1
        if pc % 2 == 0: pS.append(S); pE.append(E); px.append(len(px))

        angle_W += 0.02 + random.uniform(-0.025, 0.025) * (1 - W)**2
        angle_B += 0.02 + random.uniform(-0.025, 0.025) * (1 - B)**2
        wx = cx + (7 - 2.5 * W) * np.cos(angle_W)
        wy = cy + (7 - 2.5 * W) * np.sin(angle_W) * 0.7
        bx = cx + (5 - 1.5 * B) * np.cos(angle_B)
        by = cy + (5 - 1.5 * B) * np.sin(angle_B) * 0.7

        instability = 1 - np.mean(sw * sb)
        sx += np.random.uniform(-0.07, 0.07, N_STARS) * instability
        sy += np.random.uniform(-0.07, 0.07, N_STARS) * instability
        sx = np.clip(sx, cx - 13, cx + 13); sy = np.clip(sy, cy - 9, cy + 9)

        st.session_state.W, st.session_state.B, st.session_state.E, st.session_state.S = W, B, E, S
        st.session_state.phase, st.session_state.cycle_angle = phase, cycle_angle
        st.session_state.angle_W, st.session_state.angle_B = angle_W, angle_B
        st.session_state.empowerment_buffer = eb
        st.session_state.sx, st.session_state.sy = sx, sy
        st.session_state.sw, st.session_state.sb = sw, sb
        st.session_state.history_S, st.session_state.history_E, st.session_state.history_x = pS, pE, px
        st.session_state.frame_count = pc

        fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000010')
        ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
        for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                        (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
            ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=c, alpha=a, zorder=15))
        ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')
        ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#0FF', alpha=0.25 * (1 - min(E, 1)) + 0.04, zorder=7))
        ax.add_patch(Circle((cx, cy), 8.5, color='#0F8', alpha=0.15, fill=False, lw=2.5, zorder=2))
        ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFF', alpha=1, zorder=13))
        ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#F33', alpha=0.8, zorder=13))
        ax.text(wx, wy + 0.8, 'W', color='#FFF', fontsize=10, ha='center')
        ax.text(bx, by + 0.8, 'B', color='#F33', fontsize=10, ha='center')
        colors = [get_color(sw[i], sb[i]) for i in range(N_STARS)]
        ax.scatter(sx, sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)
        pax = ax.inset_axes([0.5, 0.02, 0.46, 0.10])
        pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
        pax.set_title(t('S (الذهب) يقود E (السماوي) – الاستدراج', 'S (Gold) leads E (Cyan) – Istidraj'), color='white', fontsize=7)
        pax.tick_params(colors='white', labelsize=4); pax.grid(True, alpha=0.12)
        if list(pS): pax.plot(list(px), list(pS), color='#FFD700', lw=2); pax.plot(list(px), list(pE), color='#0FF', lw=1.5)
        ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f}', color='white', fontsize=12, ha='center')
        plt.tight_layout(pad=0); placeholder.pyplot(fig); plt.close(fig)
        time.sleep(0.08)
    st.success(t("✅ تم إيقاف المحاكاة.", "✅ Simulation stopped."))
elif st.session_state.init and not st.session_state.run:
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000010')
    ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
    S_curr, E_curr = st.session_state.S, st.session_state.E
    for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.65, '#FFD700'), (1.7, 0.3, '#FFD700'),
                    (2.6, 0.12, '#FFA500'), (3.8, 0.05, '#FF6347'), (5.5, 0.02, '#FF4500')]:
        ax.add_patch(Circle((14, 10), r * (0.5 + 2.8 * S_curr), color=c, alpha=a, zorder=15))
    ax.text(14, 10, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')
    ax.add_patch(Circle((14, 10), 0.5 + 16 * E_curr, color='#0FF', alpha=0.25 * (1 - min(E_curr, 1)) + 0.04, zorder=7))
    ax.add_patch(Circle((14, 10), 8.5, color='#0F8', alpha=0.15, fill=False, lw=2.5, zorder=2))
    colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(N_STARS)]
    ax.scatter(st.session_state.sx, st.session_state.sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)
    ax.text(14, 1.2, t('في انتظار التشغيل...', 'Waiting to run...'), color='white', fontsize=12, ha='center')
    plt.tight_layout(pad=0); st.pyplot(fig); plt.close(fig)with tab2:
    st.header(t("🧭 البوصلة الشخصية", "🧭 Personal Compass"))
    st.markdown(t("أجب عن 28 سؤالاً لتكتشف موقعك في فضاء الولاء والبراءة.", "Answer 28 questions to discover your position."))
    if 'compass_answers' not in st.session_state: st.session_state.compass_answers = {}
    questions = {
        "W": [
            (t("هل تعيش لله وحده؟", "Do you live for Allah alone?"), 10),
            (t("هل تقيم الصلاة بخشوع؟", "Do you pray with devotion?"), 10),
            (t("هل تؤدي الزكاة وتتصدق؟", "Do you pay Zakat?"), 10),
            (t("هل تصوم رمضان وتطوعًا؟", "Do you fast?"), 10),
            (t("هل تحج أو تسعى للحج؟", "Do you perform/seek Hajj?"), 10),
            (t("هل تحب الله ورسوله أكثر من كل شيء؟", "Do you love Allah & Messenger most?"), 10),
            (t("هل تصدق في أقوالك وأفعالك؟", "Are you truthful?"), 10),
            (t("هل تؤدي الأمانات؟", "Do you fulfill trusts?"), 10),
            (t("هل تتوكل على الله مع الأخذ بالأسباب؟", "Do you rely on Allah?"), 10),
            (t("هل تشكر في الرخاء وتصبر في البلاء؟", "Are you grateful & patient?"), 10),
            (t("هل تحمل هم الإسلام والمسلمين؟", "Do you care for Islam?"), 10),
            (t("هل تفي بالعهد؟", "Do you keep promises?"), 10),
            (t("هل أنت راضٍ بما قسم الله لك؟", "Are you content?"), 10),
            (t("هل تنصر المؤمن إذا ظُلم؟", "Do you help the oppressed?"), 10),
        ],
        "B": [
            (t("هل تأمر بالمعروف؟", "Do you enjoin good?"), 10),
            (t("هل تنهى عن المنكر؟", "Do you forbid evil?"), 10),
            (t("هل أنت مستعد لبذل النفس والمال في سبيل الله؟", "Ready to sacrifice?"), 10),
            (t("هل تتبرأ من الشرك وأهله؟", "Do you disavow polytheism?"), 10),
            (t("هل ترفض الكفر والإلحاد؟", "Do you reject disbelief?"), 10),
            (t("هل تكره النفاق والتلون؟", "Do you hate hypocrisy?"), 10),
            (t("هل تجاهد نفسك على ترك الكذب؟", "Do you struggle against lying?"), 10),
            (t("هل تتجنب الغش في معاملاتك؟", "Do you avoid fraud?"), 10),
            (t("هل تفي بعهودك ولا تخون؟", "Do you keep trusts?"), 10),
            (t("هل ترفض الظلم بكل صوره؟", "Do you reject injustice?"), 10),
            (t("هل تجاهد نفسك على ترك الفواحش؟", "Do you struggle against immorality?"), 10),
            (t("هل تخلص عملك لله وتجتنب الرياء؟", "Is your work sincere?"), 10),
            (t("هل تسلم لله في قسمته ولا تحسد؟", "Do you accept Allah's decree?"), 10),
            (t("هل تحب في الله وتبغض في الله؟", "Do you love & hate for Allah?"), 10),
        ]
    }
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("🤍 أسئلة الولاء (W)", "🤍 Loyalty Questions (W)"))
        for i, (q, mx) in enumerate(questions["W"]):
            opts = [t(f"نعم ({mx})", f"Yes ({mx})"), t(f"أحيانًا ({mx//2})", f"Sometimes ({mx//2})"), t("لا (0)", "No (0)")]
            ans = st.radio(q, opts, key=f"cw_{i}", index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"W{i}"] = mx
                elif t("أحيانًا","Sometimes") in ans: st.session_state.compass_answers[f"W{i}"] = mx // 2
                else: st.session_state.compass_answers[f"W{i}"] = 0
    with col2:
        st.subheader(t("❤️ أسئلة البراءة (B)", "❤️ Disavowal Questions (B)"))
        for i, (q, mx) in enumerate(questions["B"]):
            opts = [t(f"نعم ({mx})", f"Yes ({mx})"), t(f"أحيانًا ({mx//2})", f"Sometimes ({mx//2})"), t("لا (0)", "No (0)")]
            ans = st.radio(q, opts, key=f"cb_{i}", index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"B{i}"] = mx
                elif t("أحيانًا","Sometimes") in ans: st.session_state.compass_answers[f"B{i}"] = mx // 2
                else: st.session_state.compass_answers[f"B{i}"] = 0

    TOTAL_Q = 28
    if len(st.session_state.compass_answers) == TOTAL_Q:
        W_score = sum(st.session_state.compass_answers[f"W{i}"] for i in range(14))
        B_score = sum(st.session_state.compass_answers[f"B{i}"] for i in range(14))
        W_val, B_val = W_score / 140.0, B_score / 140.0; S_val = W_val * B_val
        q_name, q_color = classify_human(W_val, B_val)
        names = {"believer": t("مؤمن (الربع الأول)", "Believer (Q1)"),
                 "disbeliever": t("كافر (الربع الثاني)", "Disbeliever (Q2)"),
                 "hypocrite": t("منافق (الربع الثالث)", "Hypocrite (Q3)"),
                 "polytheist": t("مشرك (الربع الرابع)", "Polytheist (Q4)")}
        display_name = names.get(q_name, q_name)
        st.divider(); st.header(t("📊 نتيجة البوصلة", "📊 Compass Result"))
        cr1, cr2, cr3 = st.columns(3)
        cr1.metric("W", f"{W_val:.2f}"); cr2.metric("B", f"{B_val:.2f}"); cr3.metric("S", f"{S_val:.2f}")
        st.markdown(f"""<div style="text-align:center;padding:20px;background:rgba(10,10,46,0.9);border-radius:15px;border:2px solid {q_color};margin:20px 0;"><h2 style="color:{q_color};">{display_name}</h2><p style="color:#FFD700;font-size:1.5em;">⚖️ S = W × B = {S_val:.3f}</p></div>""", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6,6), facecolor='#0a0a2e'); ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2); ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
        ax.set_xlabel("B", color='white'); ax.set_ylabel("W", color='white')
        L_map, D_map = W_val*2-1, B_val*2-1
        ax.fill_between([0,1],0,1,alpha=0.15,color='#FFD700'); ax.fill_between([-1,0],0,1,alpha=0.15,color='#FF5252')
        ax.fill_between([-1,0],-1,0,alpha=0.15,color='#FFB6C1'); ax.fill_between([0,1],-1,0,alpha=0.15,color='#FFA500')
        for lbl, x, y in [("مؤمن",0.5,0.5),("كافر",-0.5,0.5),("منافق",-0.5,-0.5),("مشرك",0.5,-0.5)]:
            ax.text(x,y,lbl,ha='center',color='white',alpha=0.8)
        ax.scatter(D_map, L_map, c='cyan', s=250, edgecolors='white', linewidth=3, zorder=10)
        ax.tick_params(colors='white'); st.pyplot(fig)
        if st.button(t("🔄 إعادة الاختبار", "🔄 Retake Test")): st.session_state.compass_answers = {}; st.rerun()with tab3:
    st.header(t("📖 كتاب الميزان", "📖 The Book of Mizan"))
    with st.expander(t("📜 الإهداء والمقدمة", "📜 Dedication & Introduction"), expanded=False):
        st.markdown(t("""
        ### الإهداء
        إلى كل باحث عن الحقيقة، يبحث عن الخيط الناظم الذي يربط شتات هذا الوجود.
        ### مقدمة المؤلف
        الحمد لله الذي رفع السماء ووضع الميزان. أما بعد، فهذا كتاب "الميزان".
        المعادلة المركزية: **S = W × B**
        """,
        """
        ### Dedication
        To every seeker of truth.
        ### Author's Introduction
        This is the Book of Mizan. The central equation: **S = W × B**
        """))
    with st.expander(t("⚖️ معادلة الثبات الوجودي", "⚖️ The Existential Stability Equation"), expanded=False):
        st.markdown(t("""
        **S = W × B**
        - **W**: طاقة الحب والطاعة والنصرة نحو الله ورسوله والمؤمنين.
        - **B**: طاقة البغض والمفاصلة والمناعة من الكفر والشرك والطاغوت.
        - **S**: العروة الوثقى – حالة الاستقرار الوجودي.
        لماذا الضرب وليس الجمع؟ لأن العلاقة شرطية: لا يصح إيمان بلا براءة.
        """,
        """
        **S = W × B**
        - **W**: Love, obedience, and support towards Allah.
        - **B**: Disavowal and immunity from disbelief and false deities.
        - **S**: The Firm Handhold – existential stability.
        Why multiplication? Because the relationship is conditional.
        """))
    with st.expander(t("💫 الاستدراج – فخ التمكين الزائف", "💫 Istidraj – The Trap"), expanded=False):
        st.markdown(t("""
        الاستدراج هو تأخر انهيار التمكين المادي (E) عن انهيار الثبات الأخلاقي (S).
        """,
        """
        Istidraj is the delayed collapse of material empowerment (E) after moral stability (S) has collapsed.
        """))with tab4:
    st.header(t("🔤 المعجم الهندسي للقرآن", "🔤 Geometric Lexicon of the Quran"))
    st.markdown(t("اكتشف كيف تترجم أدوات اللغة القرآنية إلى مشغلات رياضية.", "Discover how Quranic linguistic tools translate into mathematical operators."))
    geometric_tools = {
        t("فاء السببية (فَـ)", "Causative Fa"): {"symbol": "=", "description": t("علامة التساوي: تربط السبب بالنتيجة حتمًا.", "Equals sign.")},
        t("واو المعية – الضرب (وَ)", "Conjunctive Waw – ×"): {"symbol": "×", "description": t("واو الضرب: لا يتم الأمر إلا باجتماع الطرفين.", "Conditional conjunction.")},
        t("واو الاستئناف – الجمع (وَ)", "Conjunctive Waw – +"): {"symbol": "+", "description": t("واو الجمع: في مقام الحساب والجزاء.", "Cumulative addition.")},
        t("لام التعليل (لِـ)", "Purpose Lam"): {"symbol": "→", "description": t("سهم الغاية: يوضح اتجاه المقصد.", "Arrow of purpose.")},
        t("حتى الغائية", "Hatta (Until)"): {"symbol": "...", "description": t("استمرار السبب حتى تتحقق النتيجة.", "Continuation.")},
        t("إن الشرطية", "In (If)"): {"symbol": "( )ᵒ", "description": t("قوس الشرط الاختياري.", "Optional condition.")},
        t("إذا الشرطية", "Idha (When)"): {"symbol": "( )ᶜ", "description": t("قوس الشرط المحقق.", "Certain condition.")},
        t("إلا – أداة الاستثناء", "Illa (Except)"): {"symbol": "{}", "description": t("حدود المجموعة.", "Set boundaries.")},
        t("كلا – حرف ردع", "Kalla (No!)"): {"symbol": "⛔", "description": t("قطع الأسباب الباطلة.", "Severing false causes.")},
    }
    sel_tool = st.selectbox(t("اختر أداة قرآنية:", "Select a Quranic tool:"), list(geometric_tools.keys()))
    if sel_tool:
        td = geometric_tools[sel_tool]
        ca, cb = st.columns([1, 3])
        with ca:
            st.markdown(f"""<div style="text-align:center;padding:20px;background:rgba(10,10,46,0.9);border-radius:15px;border:2px solid #FFD700;"><p style="color:#AAA;font-size:0.8em;">{t('الرمز الهندسي', 'Symbol')}</p><p style="color:#FFD700;font-size:3em;">{td['symbol']}</p></div>""", unsafe_allow_html=True)
        with cb: st.info(td["description"])

with tab5:
    st.header(t("📜 رسالة الترحيب", "📜 Welcome Message"))
    st.markdown(t("""
    <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">
    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
    > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"
    ---
    <b style="color: #FFD700;">﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ
    لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ وَلَٰكِنَّ أَكْثَرَ النَّاسِ لَا يَعْلَمُونَ﴾</b>
    ---
    > "أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان."
    </div>
    """,
    """
    <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">
    > "Is there a single law governing the atom and civilization?<br>
    > This is the Mizan Model that proves <b style="color: #FFD700;">S = W × B</b>"
    </div>
    """), unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: #888; font-size: 0.9em;">
    <p>© {__YEAR__} {__AUTHOR__}</p>
    <p>{__LICENSE__} | {__VERSION__}</p>
    <p style="color: #FFD700; font-size: 1.5em;">⚖️ {__SIGNATURE__}</p>
    <p>{t('علم الميزان – علم الثبات الوجودي', 'Mizan Science – The Science of Existential Stability')}</p>
</div>
""", unsafe_allow_html=True)
