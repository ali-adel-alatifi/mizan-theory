import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
from matplotlib.lines import Line2D
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(
    page_title="الْمَنْصَةُ الذَّهَبِيَّةُ – The Golden Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# SESSION STATE INITIALIZATION
# =============================================
if 'entered' not in st.session_state:
    st.session_state.entered = False
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "compass_answers" not in st.session_state:
    st.session_state.compass_answers = {}

LANG = st.session_state.lang

# =============================================
# MULTILINGUAL TRANSLATION DICTIONARY
# =============================================
T = {
    "welcome_html": {
        "ar": """<div style="direction: rtl; text-align: center; background: linear-gradient(180deg, #000000 0%, #0a1a0a 30%, #1a2e1a 70%, #0a1a0a 100%); padding: 40px 20px; border-radius: 25px; border: 3px solid #FFD700; margin: 30px 0; box-shadow: 0 0 60px rgba(255, 215, 0, 0.7);"><span style="font-size: 70px; display: block;">⚖️</span><h1 style="color: #FFD700; font-size: 2.5em; margin: 15px 0; font-weight: 900;">الْمَنْصَةُ الذَّهَبِيَّةُ</h1><span style="font-size: 50px; display: block;">🧪</span><h2 style="color: #FFD700; font-size: 1.5em; margin: 10px 0;">مُخْتَبَرُ نَظَرِيَّةِ الْمِيزَان</h2><p style="color: #e0e0e0; font-size: 1.2em; margin: 30px 10px; line-height: 2.2; font-style: italic;">"هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟<br>هَذَا هُوَ نَمُوذَجُ الْمِيزَانِ الَّذِي يُثْبِتُ أَنَّ <b style="color: #FFD700;">S = W × B</b>"</p><p style="color: #FFD700; font-size: 1.5em; margin: 30px 0 0 0; font-weight: bold;">علي عادل العاطفي</p><p style="color: #FFD700; font-size: 1em; margin: 5px 0 0 0; font-style: italic; opacity: 0.8;">Ali Adel Alatifi | 2026</p></div>""",
        "en": """<div style="text-align: center; background: linear-gradient(180deg, #000000 0%, #0a0a1a 30%, #0d0d2b 70%, #000000 100%); padding: 40px 20px; border-radius: 25px; border: 3px solid #FFD700; margin: 30px 0; box-shadow: 0 0 60px rgba(255, 215, 0, 0.7);"><span style="font-size: 70px; display: block;">⚖️</span><h1 style="color: #FFD700; font-size: 2.5em; margin: 15px 0; font-weight: 900;">THE GOLDEN PLATFORM</h1><span style="font-size: 50px; display: block;">🧪</span><h2 style="color: #FFD700; font-size: 1.5em; margin: 10px 0;">The Mizan Theory Lab</h2><p style="color: #e0e0e0; font-size: 1.2em; margin: 30px 10px; line-height: 2.2; font-style: italic;">"Is there a single law governing the atom and civilization?<br>This is the Mizan Model that proves <b style="color: #FFD700;">S = W × B</b>"</p><p style="color: #FFD700; font-size: 1.5em; margin: 30px 0 0 0; font-weight: bold;">Ali Adel Alatifi</p><p style="color: #FFD700; font-size: 1em; margin: 5px 0 0 0; font-style: italic; opacity: 0.8;">2026</p></div>"""
    },
    "enter_lab": {"ar": "🚀 ادْخُلْ إِلَى الْمُخْتَبَرِ", "en": "🚀 Enter the Lab"},
    "tab_believe": {"ar": "🛡️ آمِن", "en": "🛡️ Believe"},
    "tab_advisor": {"ar": "🧠 اسْتَشِرْ", "en": "🧠 Consult"},
    "tab_observe": {"ar": "🧍 رَاقِبْ", "en": "🧍 Observe"},
    "tab_judge": {"ar": "🌍 احْكُمْ", "en": "🌍 Judge"},
    "tab_society": {"ar": "👥 جَامِعْ", "en": "👥 Society"},
    "tab_history": {"ar": "📜 تَارِيخ", "en": "📜 History"},
    "tab_heatmap": {"ar": "🔥 خَرِيطَة", "en": "🔥 Heatmap"},
    "tab_compass": {"ar": "🧭 بَوْصَلَة", "en": "🧭 Compass"},
    "tab_library": {"ar": "📚 افْهَمْ", "en": "📚 Understand"},
    "control_panel": {"ar": "🧭 لَوْحَةُ التَّحَكُّمِ", "en": "🧭 Control Panel"},
    "param_w": {"ar": "W (الْوَلَاءُ)", "en": "W (Loyalty)"},
    "param_b": {"ar": "B (الْبَرَاءَةُ)", "en": "B (Disavowal)"},
    "param_e": {"ar": "E (التَّمْكِينُ)", "en": "E (Empowerment)"},
    "param_lag": {"ar": "فَجْوَةُ الِاسْتِدْرَاجِ", "en": "Istidraj Gap"},
    "dashboard": {"ar": "لَوْحَةُ الْمُؤَشِّرَاتِ", "en": "Dashboard"},
    "footer": {"ar": "© 2026 علي عادل العاطفي | الْمَنْصَةُ الذَّهَبِيَّةُ", "en": "© 2026 Ali Adel Alatifi | The Golden Platform"},
    "lang_selector": {"ar": "اللُّغَةُ", "en": "Language"},
    "advisor_title": {"ar": "🧠 الْمُسْتَشَارُ الْفَائِقُ", "en": "🧠 The Super Advisor"},
    "advisor_subtitle": {"ar": "اسْأَلْ عَنْ أَيِّ شَيْءٍ. يَدْعَمُ GPT-4o وَ Claude.", "en": "Ask anything. Supports GPT-4o & Claude."},
    "ask_placeholder": {"ar": "مِثَال: مَا هُوَ الِاسْتِدْرَاجُ؟", "en": "E.g., What is Istidraj?"},
    "analyzing": {"ar": "🧠 يُحَلِّلُ...", "en": "🧠 Analyzing..."},
    "simulation_note": {"ar": "📊 مُحَاكَاةٌ حَيَّةٌ:", "en": "📊 Live simulation:"},
    "launch_clash": {"ar": "🚀 أَطْلِقْ صِرَاعَ الْحَضَارَاتِ", "en": "🚀 Launch Clash"},
    "clash_success": {"ar": "الْبَقَاءُ لِلْأَقْوَى مِيزَانًا.", "en": "Survival of the fittest Mizan."},
    "personal_title": {"ar": "🧍 مُخْتَبَرُ الْوَلَاءِ وَالْبَرَاءَةِ", "en": "🧍 Loyalty & Disavowal Lab"},
    "personal_subtitle": {"ar": "اضْبِطْ مُؤَثِّرَاتِ W وَ B.", "en": "Adjust W & B factors."},
    "w_group_label": {"ar": "🤍 مُقَوِّيَاتُ الْوَلَاءِ (W)", "en": "🤍 Loyalty Boosters (W)"},
    "b_group_label": {"ar": "❤️ مُقَوِّيَاتُ الْبَرَاءَةِ (B)", "en": "❤️ Disavowal Boosters (B)"},
    "result_w": {"ar": "وَلَاءٌ (W)", "en": "Loyalty (W)"},
    "result_b": {"ar": "بَرَاءَةٌ (B)", "en": "Disavowal (B)"},
    "result_s": {"ar": "ثَبَاتٌ (S)", "en": "Stability (S)"},
    "safe_zone": {"ar": "🟢 أَنْتَ فِي رَبْعِ الْمُؤْمِنِينَ.", "en": "🟢 Believer's quadrant."},
    "warning_zone": {"ar": "🟡 مَوْقِعُكَ هَشٌّ.", "en": "🟡 Fragile position."},
    "danger_zone": {"ar": "🔴 أَنْتَ فِي مَنْطِقَةِ الْخَطَرِ.", "en": "🔴 Danger zone."},
    "map_caption": {"ar": "📍 مَوْقِعُكَ عَلَى خَرِيطَةِ (W, B)", "en": "📍 Your position on the (W, B) map"},
    "library_title": {"ar": "📚 مَكْتَبَةُ الْمُوسُوعَةِ", "en": "📚 Encyclopedia Library"},
    "summary_title": {"ar": "📜 خُلَاصَةُ النَّظَرِيَّةِ", "en": "📜 Theory Summary"},
    "lexicon_title": {"ar": "🔤 الْمُعْجَمُ الْهَنْدَسِيُّ", "en": "🔤 Geometric Lexicon"},
    "select_tool": {"ar": "اخْتَرْ أَدَاةً:", "en": "Select a tool:"},
    "command_center_title": {"ar": "🛡️ مَرْكَزُ الْقِيَادَةِ", "en": "🛡️ Command Center"},
    "nations_board_title": {"ar": "🌍 لَوْحَةُ الْأُمَمِ", "en": "🌍 Nations Board"},
    "cycle_title": {"ar": "دَوْرَةُ الْحَضَارَةِ", "en": "Civilization Cycle"},
    "result_title": {"ar": "📊 النَّتِيجَةُ", "en": "📊 Result"},
    "quadrant_labels": {
        "believer": {"ar": "الْمُؤْمِنُ", "en": "Believer"},
        "harsh": {"ar": "الْمُتَشَدِّدُ", "en": "Harsh"},
        "hypocrite": {"ar": "الْمُنَافِقُ", "en": "Hypocrite"},
        "weak": {"ar": "الضَّعِيفُ", "en": "Weak"},
    },
    "society_title": {"ar": "👥 مُخْتَبَرُ الْمُجْتَمَعِ", "en": "👥 The Society Lab"},
    "society_subtitle": {"ar": "شَاهِدْ كَيْفَ تَنْتَشِرُ قِيَمُ W وَ B.", "en": "Watch W & B values spread."},
    "pop_size": {"ar": "عَدَدُ الْأَفْرَادِ", "en": "Population Size"},
    "influence_radius": {"ar": "مَدَى التَّأَثُّرِ بِالْجِيرَانِ", "en": "Neighbor Influence"},
    "sim_years": {"ar": "سَنَوَاتُ الْمُحَاكَاةِ", "en": "Simulation Years"},
    "run_society": {"ar": "▶️ تَشْغِيلُ الْمُحَاكَاةِ", "en": "▶️ Run Simulation"},
    "society_map_title": {"ar": "خَرِيطَةُ الْمُجْتَمَعِ بَعْدَ ", "en": "Society Map After "},
    "legend_believer": {"ar": "مُؤْمِن", "en": "Believer"},
    "legend_hypocrite": {"ar": "مُنَافِق", "en": "Hypocrite"},
    "legend_weak": {"ar": "ضَعِيف", "en": "Weak"},
    "history_title": {"ar": "📜 الْمُخْتَبَرُ التَّارِيخِيُّ", "en": "📜 Historical Lab"},
    "history_subtitle": {"ar": "حَاكِ دَوْرَةَ حَيَاةِ أُمَّةٍ.", "en": "Simulate a nation's life cycle."},
    "run_history": {"ar": "📜 تَشْغِيلُ الْمُحَاكَاةِ", "en": "📜 Run Simulation"},
    "heatmap_title": {"ar": "🔥 خَرِيطَةُ حَرَارَةِ الْمِيزَانِ", "en": "🔥 Mizan Heatmap"},
    "heatmap_subtitle": {"ar": "1000 فَرْدٍ فِي فَضَاءِ (W, B).", "en": "1000 individuals in (W, B) space."},
    "run_heatmap": {"ar": "🔥 تَوْلِيدُ الْخَرِيطَةِ", "en": "🔥 Generate Heatmap"},
    "compass_title": {"ar": "🧭 الْبَوْصَلَةُ الذَّاتِيَّةُ", "en": "🧭 Personal Compass"},
    "compass_subtitle": {"ar": "أَجِبْ عَنْ 28 سُؤَالاً.", "en": "Answer 28 questions."},
    "compass_loyalty": {"ar": "🤍 أَسْئِلَةُ الْوَلَاءِ (W)", "en": "🤍 Loyalty Questions (W)"},
    "compass_disavowal": {"ar": "❤️ أَسْئِلَةُ الْبَرَاءَةِ (B)", "en": "❤️ Disavowal Questions (B)"},
    "compass_result": {"ar": "📊 نَتِيجَةُ الْبَوْصَلَةِ", "en": "📊 Compass Result"},
    "compass_reset": {"ar": "🔄 إِعَادَةُ الِاخْتِبَارِ", "en": "🔄 Retake Test"},
    "w_shahada": {"ar": "الشَّهَادَتَانِ", "en": "The Two Shahadas"},
    "w_salat": {"ar": "الصَّلَاةُ", "en": "Prayer"},
    "w_zakat": {"ar": "الزَّكَاةُ وَالصَّدَقَةُ", "en": "Zakat & Charity"},
    "w_sawm": {"ar": "الصَّوْمُ", "en": "Fasting"},
    "w_hajj": {"ar": "الْحَجُّ وَالْعُمْرَةُ", "en": "Hajj & Umrah"},
    "w_quran": {"ar": "تِلَاوَةُ الْقُرْآنِ", "en": "Reciting Quran"},
    "w_dhikr": {"ar": "الذِّكْرُ وَالدُّعَاءُ", "en": "Dhikr & Dua"},
    "w_tawakkul": {"ar": "التَّوَكُّلُ عَلَى اللَّهِ", "en": "Reliance on Allah"},
    "w_hubb": {"ar": "حُبُّ اللَّهِ وَرَسُولِهِ ﷺ", "en": "Love of Allah & Messenger"},
    "w_birr": {"ar": "بِرُّ الْوَالِدَيْنِ", "en": "Kindness to Parents"},
    "w_ihsan": {"ar": "الْإِحْسَانُ وَحُسْنُ الْخُلُقِ", "en": "Good Character"},
    "w_taawun": {"ar": "التَّعَاوُنُ عَلَى الْبِرِّ", "en": "Cooperating in Good"},
    "b_taghut": {"ar": "الْكُفْرُ بِالطَّاغُوتِ", "en": "Disbelief in Taghut"},
    "b_shirk": {"ar": "الْبَرَاءَةُ مِنَ الشِّرْكِ", "en": "Disavowal of Polytheism"},
    "b_kufr": {"ar": "الْبَرَاءَةُ مِنَ الْكُفْرِ", "en": "Disavowal of Kufr"},
    "b_nifaq": {"ar": "الْبَرَاءَةُ مِنَ النِّفَاقِ", "en": "Disavowal of Hypocrisy"},
    "b_amr": {"ar": "الْأَمْرُ بِالْمَعْرُوفِ", "en": "Enjoining Good"},
    "b_nahy": {"ar": "النَّهْيُ عَنِ الْمُنْكَرِ", "en": "Forbidding Evil"},
    "b_jihad_nafs": {"ar": "جِهَادُ النَّفْسِ", "en": "Jihad of the Self"},
    "b_jihad": {"ar": "الْجِهَادُ فِي سَبِيلِ اللَّهِ", "en": "Jihad in Allah's Cause"},
    "b_ghadd": {"ar": "غَضُّ الْبَصَرِ", "en": "Lowering the Gaze"},
    "b_farj": {"ar": "حِفْظُ الْفَرْجِ", "en": "Guarding Chastity"},
    "b_kadhib": {"ar": "تَرْكُ الْكَذِبِ", "en": "Abandoning Lying"},
    "b_ghiba": {"ar": "تَرْكُ الْغِيبَةِ", "en": "Avoiding Backbiting"},
    "b_zulm": {"ar": "تَرْكُ الظُّلْمِ", "en": "Abandoning Injustice"},
    "b_riba": {"ar": "تَرْكُ الرِّبَا", "en": "Avoiding Usury"},
}

# =============================================
# ENHANCED TRANSLATION FUNCTION
# =============================================
def t(key, subkey=None):
    """Retrieve translated text. If subkey is provided, retrieves from nested dict."""
    val = T.get(key, {}).get(LANG, key)
    if subkey and isinstance(val, dict):
        return val.get(LANG, subkey)
    return val

# =============================================
# COSMIC SIMULATION ENGINE
# =============================================
def cosmic_engine(W0, B0, E0, years=200, lag=25):
    W = np.zeros(years); B = np.zeros(years); S = np.zeros(years); E = np.zeros(years)
    W[0], B[0], E[0] = W0, B0, E0; S[0] = W0 * B0
    for t in range(1, years):
        W[t] = max(0.01, min(1.0, W[t-1] - 0.05 * E[t-1]))
        B[t] = max(0.01, min(1.0, B[t-1] - 0.04 * E[t-1]))
        S[t] = W[t] * B[t]; past_idx = t - lag
        S_past = S[past_idx] if past_idx >= 0 else S[t]
        E[t] = max(0.01, min(1.0, E[t-1] + 0.05 * (S_past - E[t-1])))
    return W, B, S, E

def get_mizan_color(w, b):
    if w >= 0.7 and b >= 0.7: return '#FFD700'
    elif w >= 0.5 and b < 0.4: return '#E0E0E0'
    elif w < 0.4 and b >= 0.5: return '#FF5252'
    elif w < 0.4 and b < 0.4: return '#FFB6C1'
    else: return '#888888'

# =============================================
# SUPER ADVISOR (GPT-4o + Claude via OpenRouter)
# =============================================
def get_super_advisor_response(user_query, lang="ar"):
    try:
        api_key = st.secrets.get("OPENROUTER_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
        if api_key:
            import requests
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "model": "openai/gpt-4o",
                "messages": [
                    {"role": "system", "content": "You are the Super Advisor of The Mizan Theory by Ali Adel Alatifi. Core: S=W×B. Istidraj: E lags S."},
                    {"role": "user", "content": user_query}
                ],
                "temperature": 0.7, "max_tokens": 800
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=15)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
    except: pass
    
    q = user_query.lower()
    if "istidraj" in q or "استدراج" in q:
        return {"ar": "الِاسْتِدْرَاجُ: E يَتَأَخَّرُ عَنْ S ثُمَّ يَنْهَارُ فَجْأَةً. ﴿فَلَمَّا نَسُوا... أَخَذْنَاهُم بَغْتَةً﴾ [الأنعام:44].", "en": "Istidraj: E lags behind S then collapses suddenly. [Al-An'am:44]"}.get(lang, "")
    if "mizan" in q or "ميزان" in q:
        return {"ar": "S = W × B. ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة:256].", "en": "S = W × B. [Al-Baqarah:256]"}.get(lang, "")
    return {"ar": "لَمْ أَجِدْ إِجَابَةً. جَرِّبْ: الِاسْتِدْرَاج، الْمِيزَان.", "en": "Not found. Try: Istidraj, Mizan."}.get(lang, "")

# =============================================
# SOCIETY SIMULATION ENGINE (AGENT-BASED)
# =============================================
def classify_agent(w, b):
    if w >= 0.6 and b >= 0.6: return "believer"
    elif w < 0.4 and b < 0.4: return "hypocrite"
    elif w >= 0.5 and b < 0.4: return "weak"
    elif w < 0.4 and b >= 0.5: return "harsh"
    else: return "average"

def get_agent_color(classification):
    return {"believer": '#FFD700', "hypocrite": '#FF5252', "weak": '#E0E0E0', "harsh": '#FF8C00', "average": '#888888'}.get(classification, '#888888')

def run_society_simulation(pop_size, influence_radius, years):
    np.random.seed(42)
    W = np.random.uniform(0.3, 0.9, pop_size); B = np.random.uniform(0.3, 0.9, pop_size)
    pos_x = np.random.uniform(0, 30, pop_size); pos_y = np.random.uniform(0, 30, pop_size)
    for _ in range(years):
        new_W = W.copy(); new_B = B.copy()
        for i in range(pop_size):
            distances = np.sqrt((pos_x - pos_x[i])**2 + (pos_y - pos_y[i])**2)
            neighbors = np.where(distances < influence_radius)[0]; neighbors = neighbors[neighbors != i]
            if len(neighbors) > 0:
                new_W[i] += 0.02 * (np.mean(W[neighbors]) - W[i]); new_B[i] += 0.02 * (np.mean(B[neighbors]) - B[i])
            new_W[i] += 0.01 * (np.random.rand() - 0.5); new_B[i] += 0.01 * (np.random.rand() - 0.5)
            if W[i] > 0.7 and B[i] > 0.7: new_B[i] -= 0.005 * np.random.rand()
            new_W[i] = max(0.05, min(1.0, new_W[i])); new_B[i] = max(0.05, min(1.0, new_B[i]))
        W = new_W; B = new_B
        pos_x = np.clip(pos_x + np.random.randint(-1, 2, pop_size), 0, 29)
        pos_y = np.clip(pos_y + np.random.randint(-1, 2, pop_size), 0, 29)
    return W, B, pos_x, pos_y

# =============================================
# 🏠 WELCOME SCREEN
# =============================================
if not st.session_state.entered:
    st.markdown(t("welcome_html"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t("enter_lab"), use_container_width=True, type="primary"):
            st.session_state.entered = True
            st.rerun()
    st.stop()
# =============================================
# 🧭 SIDEBAR (CONTROL PANEL + LANGUAGE)
# =============================================
with st.sidebar:
    st.markdown(f"## {t('control_panel')}")
    
    # Language Selector
    lang_option = st.selectbox(
        t('lang_selector'),
        options=["🇸🇦 العربية", "🇬🇧 English"],
        index=0 if LANG == "ar" else 1,
        key="sidebar_lang"
    )
    new_lang = "ar" if "العربية" in lang_option else "en"
    if new_lang != LANG:
        st.session_state.lang = new_lang
        st.rerun()
    
    st.markdown("---")
    
    # Global Mizan Parameters
    st.subheader("⚙️ " + ("مُعَامَلَاتُ الْمِيزَانِ" if LANG == "ar" else "Mizan Parameters"))
    W_global = st.slider(t('param_w'), 0.0, 1.0, 0.7, 0.05, key="sidebar_w")
    B_global = st.slider(t('param_b'), 0.0, 1.0, 0.6, 0.05, key="sidebar_b")
    E_global = st.slider(t('param_e'), 0.0, 1.0, 0.3, 0.05, key="sidebar_e")
    lag_global = st.slider(t('param_lag'), 5, 50, 22, 1, key="sidebar_lag")
    
    st.markdown("---")
    st.markdown(f"<p style='text-align:center;color:#888;font-size:0.8em;'>{t('footer')}</p>", unsafe_allow_html=True)

# =============================================
# 🗂️ MAIN TABS DEFINITION
# =============================================
tab_labels = [
    t('tab_believe'),    # 0: Command Center
    t('tab_advisor'),    # 1: Super Advisor
    t('tab_observe'),    # 2: Personal Lab
    t('tab_judge'),      # 3: Nations Clash
    t('tab_society'),    # 4: Society Lab
    t('tab_history'),    # 5: Historical Lab
    t('tab_heatmap'),    # 6: Heatmap
    t('tab_compass'),    # 7: Compass
    t('tab_library'),    # 8: Library
]
tabs = st.tabs(tab_labels)

# =============================================
# TAB 0: COMMAND CENTER (🛡️ آمِن)
# =============================================
with tabs[0]:
    st.header(t("command_center_title"))
    
    # Run the cosmic engine with global parameters
    W_s, B_s, S_s, E_s = cosmic_engine(W_global, B_global, E_global, 200, lag_global)
    
    # ---- Dashboard Metrics ----
    st.subheader(t('dashboard'))
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🤍 W", f"{W_global:.2f}")
    with c2:
        st.metric("❤️ B", f"{B_global:.2f}")
    with c3:
        st.metric("⚖️ S", f"{W_global * B_global:.2f}")
    with c4:
        st.metric("💫 E", f"{E_global:.2f}")
    
    st.markdown("---")
    
    # ---- Civilization Cycle Chart ----
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    
    # Plot Stability (S) and Empowerment (E)
    ax.plot(S_s, 'g-', linewidth=2.5, label='S (Stability)' if LANG == "en" else 'S (الثَّبَاتُ)')
    ax.plot(E_s, 'b--', linewidth=2.5, label='E (Empowerment)' if LANG == "en" else 'E (التَّمْكِينُ)')
    
    # Highlight Istidraj Gap
    max_S_idx = np.argmax(S_s)
    max_E_idx = np.argmax(E_s)
    if max_S_idx < max_E_idx:
        gap_label = f"{t('param_lag')} ({max_E_idx - max_S_idx} " + ("yrs)" if LANG == "en" else "سَنَةً)")
        ax.axvspan(max_S_idx, max_E_idx, alpha=0.25, color='red', label=gap_label)
    
    ax.set_title(t("cycle_title"), color='white', fontsize=14, fontweight='bold')
    ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=10)
    ax.grid(True, alpha=0.2)
    ax.set_ylim(0, 1.05)
    ax.tick_params(colors='white')
    ax.set_xlabel(("Years" if LANG == "en" else "السَّنَوَاتُ"), color='white')
    ax.set_ylabel(("Value" if LANG == "en" else "الْقِيمَةُ"), color='white')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # ---- Quick Explanation ----
    with st.expander("ℹ️ " + ("How to read this?" if LANG == "en" else "كَيْفَ تَقْرَأُ هَذَا؟")):
        if LANG == "ar":
            st.markdown("""
            - **الْخَطُّ الْأَخْضَرُ (S)**: يُمَثِّلُ الثَّبَاتَ الْحَقِيقِيَّ لِلْحَضَارَةِ (الْإِيمَانُ وَالْأَخْلَاقُ).
            - **الْخَطُّ الْأَزْرَقُ (E)**: يُمَثِّلُ التَّمْكِينَ الْمَادِّيَّ (الْقُوَّةُ، الثَّرْوَةُ).
            - **الْمِنْطَقَةُ الْحَمْرَاءُ**: هِيَ "فَجْوَةُ الِاسْتِدْرَاجِ". يَنْهَارُ الثَّبَاتُ (S) بَيْنَمَا يَبْدُو التَّمْكِينُ (E) قَوِيًّا، ثُمَّ يَنْهَارُ فَجْأَةً.
            """)
        else:
            st.markdown("""
            - **Green Line (S)**: Represents the real stability of civilization (faith & morals).
            - **Blue Dashed Line (E)**: Represents material empowerment (power, wealth).
            - **Red Zone**: The "Istidraj Gap". Stability (S) collapses while empowerment (E) appears strong, then suddenly crashes.
            """)

# =============================================
# PLACEHOLDER FOR REMAINING TABS
# (Will be filled in subsequent phases)
# =============================================
# Tabs 1-8 will be populated in the next phases.
# For now, we leave them empty or with a coming-soon message.
for i in range(1, 9):
    with tabs[i]:
        st.info(f"🚧 {('Coming Soon' if LANG == 'en' else 'قَيْدَ الْإِنْشَاءِ...')}")
# =============================================
# TAB 1: SUPER ADVISOR (🧠 اسْتَشِرْ)
# =============================================
with tabs[1]:
    st.header(t('advisor_title'))
    st.markdown(t('advisor_subtitle'))
    
    # User input
    user_q = st.text_input(
        "✍️ " + ("سُؤَالُكَ:" if LANG == "ar" else "Your question:"),
        placeholder=t('ask_placeholder'),
        key="advisor_input"
    )
    
    if user_q:
        with st.spinner(t('analyzing')):
            # Get the advisor's response
            ans = get_super_advisor_response(user_q, LANG)
            
            # Display the answer
            st.markdown("### 💡 " + ("الْجَوَابُ:" if LANG == "ar" else "Answer:"))
            st.markdown(ans)
            
            # Determine simulation parameters based on the question
            if "istidraj" in user_q.lower() or "استدراج" in user_q.lower():
                w0, b0, e0 = 0.3, 0.3, 0.9
            elif "mizan" in user_q.lower() or "ميزان" in user_q.lower() or "equation" in user_q.lower() or "معادلة" in user_q.lower():
                w0, b0, e0 = 0.7, 0.6, 0.3
            elif "collapse" in user_q.lower() or "انهيار" in user_q.lower() or "سقوط" in user_q.lower():
                w0, b0, e0 = 0.2, 0.2, 0.8
            elif "faith" in user_q.lower() or "إيمان" in user_q.lower() or "rise" in user_q.lower() or "صعود" in user_q.lower():
                w0, b0, e0 = 0.9, 0.9, 0.1
            else:
                w0, b0, e0 = 0.6, 0.5, 0.4
            
            # Run a contextual simulation
            W_sim, B_sim, S_sim, E_sim = cosmic_engine(w0, b0, e0, 100, lag_global)
            
            st.markdown(t('simulation_note'))
            fig, ax = plt.subplots(figsize=(10, 3), facecolor='#0a0a1a')
            ax.set_facecolor('#0a0a1a')
            ax.plot(S_sim, 'g-', linewidth=2, label='S (Stability)' if LANG == "en" else 'S (الثَّبَاتُ)')
            ax.plot(E_sim, 'b--', linewidth=2, label='E (Empowerment)' if LANG == "en" else 'E (التَّمْكِينُ)')
            
            # Find Istidraj gap
            max_S = np.argmax(S_sim)
            max_E = np.argmax(E_sim)
            if max_S < max_E:
                ax.axvspan(max_S, max_E, alpha=0.2, color='red')
            
            ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax.grid(True, alpha=0.2)
            ax.set_ylim(0, 1.05)
            ax.tick_params(colors='white')
            ax.set_xlabel(("Years" if LANG == "en" else "السَّنَوَاتُ"), color='white')
            ax.set_ylabel(("Value" if LANG == "en" else "الْقِيمَةُ"), color='white')
            plt.tight_layout()
            st.pyplot(fig)

# =============================================
# TAB 2: PERSONAL LAB (🧍 رَاقِبْ)
# =============================================
with tabs[2]:
    st.header(t('personal_title'))
    st.markdown(t('personal_subtitle'))
    st.markdown("---")
    
    # ---- LOYALTY BOOSTERS (W) ----
    st.subheader(t('w_group_label'))
    st.caption(("Score each factor from 0 to 10" if LANG == "en" else "اخْتَرْ مُسْتَوَى كُلِّ مُؤَثِّرٍ مِنْ 0 إِلَى 10"))
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        w_shahada = st.slider(t("w_shahada"), 0, 10, 8, 1, key="w1")
        w_salat = st.slider(t("w_salat"), 0, 10, 7, 1, key="w2")
        w_zakat = st.slider(t("w_zakat"), 0, 10, 6, 1, key="w3")
        w_sawm = st.slider(t("w_sawm"), 0, 10, 7, 1, key="w4")
        w_hajj = st.slider(t("w_hajj"), 0, 10, 5, 1, key="w5")
        w_quran = st.slider(t("w_quran"), 0, 10, 6, 1, key="w6")
    with col_w2:
        w_dhikr = st.slider(t("w_dhikr"), 0, 10, 7, 1, key="w7")
        w_tawakkul = st.slider(t("w_tawakkul"), 0, 10, 8, 1, key="w8")
        w_hubb = st.slider(t("w_hubb"), 0, 10, 9, 1, key="w9")
        w_birr = st.slider(t("w_birr"), 0, 10, 8, 1, key="w10")
        w_ihsan = st.slider(t("w_ihsan"), 0, 10, 8, 1, key="w11")
        w_taawun = st.slider(t("w_taawun"), 0, 10, 7, 1, key="w12")
    
    # ---- DISAVOWAL BOOSTERS (B) ----
    st.subheader(t('b_group_label'))
    st.caption(("Score each factor from 0 to 10" if LANG == "en" else "اخْتَرْ مُسْتَوَى كُلِّ مُؤَثِّرٍ مِنْ 0 إِلَى 10"))
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        b_taghut = st.slider(t("b_taghut"), 0, 10, 9, 1, key="b1")
        b_shirk = st.slider(t("b_shirk"), 0, 10, 9, 1, key="b2")
        b_kufr = st.slider(t("b_kufr"), 0, 10, 8, 1, key="b3")
        b_nifaq = st.slider(t("b_nifaq"), 0, 10, 8, 1, key="b4")
        b_amr = st.slider(t("b_amr"), 0, 10, 7, 1, key="b5")
        b_nahy = st.slider(t("b_nahy"), 0, 10, 7, 1, key="b6")
        b_jihad_nafs = st.slider(t("b_jihad_nafs"), 0, 10, 9, 1, key="b7")
    with col_b2:
        b_jihad = st.slider(t("b_jihad"), 0, 10, 7, 1, key="b8")
        b_ghadd = st.slider(t("b_ghadd"), 0, 10, 8, 1, key="b9")
        b_farj = st.slider(t("b_farj"), 0, 10, 9, 1, key="b10")
        b_kadhib = st.slider(t("b_kadhib"), 0, 10, 9, 1, key="b11")
        b_ghiba = st.slider(t("b_ghiba"), 0, 10, 8, 1, key="b12")
        b_zulm = st.slider(t("b_zulm"), 0, 10, 9, 1, key="b13")
        b_riba = st.slider(t("b_riba"), 0, 10, 9, 1, key="b14")
    
    # ---- CALCULATE RESULTS ----
    W_list = [w_shahada, w_salat, w_zakat, w_sawm, w_hajj, w_quran, w_dhikr, w_tawakkul, w_hubb, w_birr, w_ihsan, w_taawun]
    B_list = [b_taghut, b_shirk, b_kufr, b_nifaq, b_amr, b_nahy, b_jihad_nafs, b_jihad, b_ghadd, b_farj, b_kadhib, b_ghiba, b_zulm, b_riba]
    
    W_personal = sum(W_list) / 120.0
    B_personal = sum(B_list) / 140.0
    S_personal = W_personal * B_personal
    
    # ---- DISPLAY RESULTS ----
    st.markdown("---")
    st.subheader(t("result_title"))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t('result_w'), f"{W_personal:.2f}")
    with col2:
        st.metric(t('result_b'), f"{B_personal:.2f}")
    with col3:
        st.metric(t('result_s'), f"{S_personal:.2f}")
    
    # Status message
    if S_personal > 0.7:
        st.success(t('safe_zone'))
    elif S_personal > 0.4:
        st.warning(t('warning_zone'))
    else:
        st.error(t('danger_zone'))
    
    # ---- QUADRANT MAP ----
    st.markdown("---")
    st.caption(t("map_caption"))
    
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    
    # Draw quadrant lines
    ax.axhline(0.5, color='gray', ls=':', lw=1)
    ax.axvline(0.5, color='gray', ls=':', lw=1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel('B (Disavowal)' if LANG == "en" else 'B (الْبَرَاءَةُ)', color='white', fontsize=11)
    ax.set_ylabel('W (Loyalty)' if LANG == "en" else 'W (الْوَلَاءُ)', color='white', fontsize=11)
    
    # Draw the user's position
    ax.scatter(B_personal, W_personal, s=400, c='cyan', edgecolors='white', linewidth=3, zorder=10)
    
    # Color the quadrants
    ax.fill_between([0.5, 1], 0.5, 1, alpha=0.12, color='green')    # Believer
    ax.fill_between([0, 0.5], 0.5, 1, alpha=0.12, color='orange')   # Harsh
    ax.fill_between([0.5, 1], 0, 0.5, alpha=0.12, color='blue')     # Weak
    ax.fill_between([0, 0.5], 0, 0.5, alpha=0.12, color='red')      # Hypocrite
    
    # Label the quadrants (using the enhanced t() function with subkey)
    quadrants = [
        ("believer", 0.75, 0.75, 'green'),
        ("harsh", 0.25, 0.75, 'orange'),
        ("hypocrite", 0.25, 0.25, 'red'),
        ("weak", 0.75, 0.25, 'blue'),
    ]
    for lbl, x, y, col in quadrants:
        ax.text(x, y, t("quadrant_labels", lbl), color=col, fontsize=12, ha='center', fontweight='bold')
    
    ax.grid(True, alpha=0.2)
    ax.tick_params(colors='white')
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    
    plt.tight_layout()
    st.pyplot(fig)
# =============================================
# TAB 3: NATIONS CLASH (🌍 احْكُمْ)
# =============================================
with tabs[3]:
    st.header(t("nations_board_title"))
    st.markdown(("Compare 4 civilizations starting from different W, B, E values." if LANG == "en" else "قَارِنْ بَيْنَ أَرْبَعِ حَضَارَاتٍ تَبْدَأُ مِنْ قِيَمٍ مُخْتَلِفَةٍ."))
    
    # Define the 4 nations
    nations = {
        ("أُمَّةُ الْإِيمَانِ" if LANG == "ar" else "Nation of Faith"): (0.9, 0.9, 0.1, "gold"),
        ("أُمَّةُ التَّرَفِ" if LANG == "ar" else "Nation of Luxury"): (0.3, 0.2, 0.9, "orange"),
        ("الْإِمْبِرَاطُورِيَّةُ الظَّالِمَةُ" if LANG == "ar" else "The Tyrant Empire"): (0.1, 0.9, 0.8, "red"),
        ("أُمَّةُ الْعِلْمِ" if LANG == "ar" else "Nation of Knowledge"): (0.8, 0.6, 0.4, "cyan"),
    }
    
    if st.button(t('launch_clash'), use_container_width=True, type="primary"):
        with st.spinner(t('analyzing')):
            fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#000010')
            
            for i, (name, (w0, b0, e0, col)) in enumerate(nations.items()):
                ax = axes[i // 2, i % 2]
                ax.set_facecolor('#0a0a1a')
                
                # Run the simulation for each nation
                W_s, B_s, S_s, E_s = cosmic_engine(w0, b0, e0, 200, lag_global)
                
                # Plot S and E
                ax.plot(S_s, color=col, linewidth=2.5, label='S (Stability)' if LANG == "en" else 'S (الثَّبَاتُ)')
                ax.plot(E_s, color=col, linestyle='--', alpha=0.6, linewidth=2, label='E (Empowerment)' if LANG == "en" else 'E (التَّمْكِينُ)')
                
                # Highlight Istidraj gap
                max_S_idx = np.argmax(S_s)
                max_E_idx = np.argmax(E_s)
                if max_S_idx < max_E_idx:
                    ax.axvspan(max_S_idx, max_E_idx, alpha=0.2, color='red')
                
                ax.set_title(name, color=col, fontweight='bold', fontsize=12)
                ax.set_ylim(0, 1.05)
                ax.grid(True, alpha=0.2)
                ax.tick_params(colors='white')
                ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=8)
            
            plt.tight_layout()
            st.pyplot(fig)
            st.success(t('clash_success'))

# =============================================
# TAB 4: SOCIETY LAB (👥 جَامِعْ)
# =============================================
with tabs[4]:
    st.header(t("society_title"))
    st.markdown(t("society_subtitle"))
    
    # Control panel for society simulation
    col1, col2, col3 = st.columns(3)
    with col1:
        pop_size = st.slider(t("pop_size"), 100, 800, 400, 50, key="soc_pop")
    with col2:
        influence_radius = st.slider(t("influence_radius"), 0.5, 5.0, 2.0, 0.5, key="soc_inf")
    with col3:
        sim_years = st.slider(t("sim_years"), 10, 100, 50, 10, key="soc_yrs")
    
    if st.button(t("run_society"), use_container_width=True, type="primary"):
        with st.spinner(t('analyzing')):
            # Run the agent-based simulation
            W_final, B_final, x_final, y_final = run_society_simulation(pop_size, influence_radius, sim_years)
            
            # Classify each agent
            classifications = [classify_agent(W_final[i], B_final[i]) for i in range(pop_size)]
            colors = [get_agent_color(c) for c in classifications]
            
            # Create the visualization
            fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a1a')
            ax.set_facecolor('#0a0a1a')
            
            # Plot agents
            ax.scatter(x_final, y_final, c=colors, s=30, alpha=0.8, edgecolors='white', linewidths=0.3)
            ax.set_xlim(0, 30)
            ax.set_ylim(0, 30)
            
            # Title
            title_text = f"{t('society_map_title')}{sim_years} " + ("سَنَةً" if LANG == "ar" else "Years")
            ax.set_title(title_text, color='white', fontsize=16, fontweight='bold')
            ax.grid(False)
            ax.tick_params(colors='white')
            
            # Custom legend
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFD700', markersize=10, label=t('legend_believer')),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF5252', markersize=10, label=t('legend_hypocrite')),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='#E0E0E0', markersize=10, label=t('legend_weak')),
            ]
            ax.legend(handles=legend_elements, loc='upper right', facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=10)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Statistics
            st.markdown("---")
            st.subheader("📊 " + ("إِحْصَائِيَّاتُ الْمُجْتَمَعِ" if LANG == "ar" else "Society Statistics"))
            
            believers = sum(1 for c in classifications if c == "believer")
            hypocrites = sum(1 for c in classifications if c == "hypocrite")
            weak = sum(1 for c in classifications if c == "weak")
            harsh = sum(1 for c in classifications if c == "harsh")
            avg = pop_size - believers - hypocrites - weak - harsh
            
            s1, s2, s3, s4, s5 = st.columns(5)
            s1.metric("🟡 " + t('legend_believer'), believers, f"{believers/pop_size*100:.0f}%")
            s2.metric("🔴 " + t('legend_hypocrite'), hypocrites, f"{hypocrites/pop_size*100:.0f}%")
            s3.metric("⚪ " + t('legend_weak'), weak, f"{weak/pop_size*100:.0f}%")
            s4.metric("🟠 " + ("Harsh" if LANG == "en" else "شَدِيد"), harsh, f"{harsh/pop_size*100:.0f}%")
            s5.metric("⬜ " + ("Average" if LANG == "en" else "مُتَوَسِّط"), avg, f"{avg/pop_size*100:.0f}%")

# =============================================
# TAB 5: HISTORICAL LAB (📜 تَارِيخ)
# =============================================
with tabs[5]:
    st.header(t("history_title"))
    st.markdown(t("history_subtitle"))
    
    # Controls for historical simulation
    col1, col2 = st.columns(2)
    with col1:
        W_nat = st.slider("W " + ("الْأُمَّةِ" if LANG == "ar" else "of Nation"), 0.0, 1.0, 0.9, 0.05, key="hist_w")
    with col2:
        B_nat = st.slider("B " + ("الْأُمَّةِ" if LANG == "ar" else "of Nation"), 0.0, 1.0, 0.8, 0.05, key="hist_b")
    
    if st.button(t("run_history"), use_container_width=True, type="primary"):
        with st.spinner(t('analyzing')):
            # Run 300-year simulation
            W_s, B_s, S_s, E_s = cosmic_engine(W_nat, B_nat, E_global, 300, lag_global)
            
            # Create two side-by-side charts
            fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#0a0a1a')
            
            # ---- CHART 1: Civilization Cycle ----
            ax = axes[0]
            ax.set_facecolor('#0a0a1a')
            ax.plot(S_s, 'g-', linewidth=2.5, label='S (Stability)' if LANG == "en" else 'S (الثَّبَاتُ)')
            ax.plot(E_s, 'b--', linewidth=2.5, label='E (Empowerment)' if LANG == "en" else 'E (التَّمْكِينُ)')
            
            # Find and highlight Istidraj gap
            max_S = np.argmax(S_s)
            max_E = np.argmax(E_s)
            if max_S < max_E:
                gap_label = f"{t('param_lag')} ({max_E - max_S} " + ("yrs)" if LANG == "en" else "سَنَةً)")
                ax.axvspan(max_S, max_E, alpha=0.25, color='red', label=gap_label)
            
            # Find collapse year
            collapse_year = None
            for t in range(max_S, len(E_s)):
                if E_s[t] < 0.3:
                    collapse_year = t
                    break
            if collapse_year:
                collapse_label = f"{'Collapse' if LANG == 'en' else 'الِانْهِيَارُ'} ({collapse_year})"
                ax.axvline(x=collapse_year, color='red', linestyle='--', linewidth=2, label=collapse_label)
            
            ax.set_title(t("cycle_title"), color='white', fontsize=14, fontweight='bold')
            ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax.grid(True, alpha=0.2)
            ax.set_ylim(0, 1.05)
            ax.tick_params(colors='white')
            ax.set_xlabel(("Years" if LANG == "en" else "السَّنَوَاتُ"), color='white')
            ax.set_ylabel(("Value" if LANG == "en" else "الْقِيمَةُ"), color='white')
            
            # ---- CHART 2: W-B Path ----
            ax2 = axes[1]
            ax2.set_facecolor('#0a0a1a')
            ax2.axhline(0.5, color='gray', ls=':', lw=1)
            ax2.axvline(0.5, color='gray', ls=':', lw=1)
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.set_xlabel('B (Disavowal)' if LANG == "en" else 'B (الْبَرَاءَةُ)', color='white')
            ax2.set_ylabel('W (Loyalty)' if LANG == "en" else 'W (الْوَلَاءُ)', color='white')
            ax2.set_title(('Civilization Path in (W, B) Space' if LANG == "en" else 'مَسَارُ الْحَضَارَةِ فِي فَضَاءِ (W, B)'), color='white', fontsize=14, fontweight='bold')
            
            # Plot the path
            ax2.plot(B_s, W_s, 'w-', alpha=0.4, linewidth=0.8)
            ax2.scatter(B_s[0], W_s[0], s=120, c='green', edgecolors='white', linewidth=2, label='Start' if LANG == "en" else 'الْبِدَايَةُ')
            ax2.scatter(B_s[-1], W_s[-1], s=120, c='red', edgecolors='white', linewidth=2, label='End' if LANG == "en" else 'النِّهَايَةُ')
            
            # Label quadrants
            for lbl, x, y, col in quadrants:
                ax2.text(x, y, t("quadrant_labels", lbl), color=col, fontsize=10, ha='center', fontweight='bold')
            
            ax2.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=9)
            ax2.grid(True, alpha=0.2)
            ax2.tick_params(colors='white')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Summary report
            if collapse_year:
                st.error(f"💥 " + (f"Predicted collapse around year {collapse_year}." if LANG == "en" else f"تَنَبُّؤٌ بِالِانْهِيَارِ حَوَالَيِ الْعَامِ {collapse_year}."))
            else:
                st.success("🛡️ " + ("Civilization remains stable for the next 300 years." if LANG == "en" else "الْحَضَارَةُ تَبْقَى مُسْتَقِرَّةً لِـ 300 عَامٍ."))
# =============================================
# TAB 6: MIZAN HEATMAP (🔥 خَرِيطَة)
# =============================================
with tabs[6]:
    st.header(t("heatmap_title"))
    st.markdown(t("heatmap_subtitle"))
    
    if st.button(t("run_heatmap"), use_container_width=True, type="primary"):
        with st.spinner(t('analyzing')):
            # Generate 1000 random individuals
            N = 1000
            np.random.seed(42)
            W_heat = np.random.uniform(0, 1, N)
            B_heat = np.random.uniform(0, 1, N)
            S_heat = W_heat * B_heat
            
            # Create the heatmap
            fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a1a')
            ax.set_facecolor('#0a0a1a')
            
            # Scatter plot colored by S value
            scatter = ax.scatter(B_heat, W_heat, c=S_heat, cmap='RdYlGn', s=30, alpha=0.8, edgecolors='white', linewidths=0.2)
            
            # Draw quadrant lines
            ax.axhline(0.5, color='gray', ls=':', lw=1)
            ax.axvline(0.5, color='gray', ls=':', lw=1)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xlabel('B (Disavowal)' if LANG == "en" else 'B (الْبَرَاءَةُ)', color='white', fontsize=12)
            ax.set_ylabel('W (Loyalty)' if LANG == "en" else 'W (الْوَلَاءُ)', color='white', fontsize=12)
            ax.set_title('Mizan Heatmap' if LANG == "en" else 'خَرِيطَةُ حَرَارَةِ الْمِيزَانِ', color='white', fontsize=16, fontweight='bold')
            
            # Label quadrants
            for lbl, x, y in [("believer", 0.75, 0.75), ("harsh", 0.25, 0.75), ("hypocrite", 0.25, 0.25), ("weak", 0.75, 0.25)]:
                ax.text(x, y, t("quadrant_labels", lbl), color='white', fontsize=14, ha='center', fontweight='bold', alpha=0.9)
            
            # Add colorbar
            cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label('S (Stability)' if LANG == "en" else 'S (الثَّبَاتُ)', color='white')
            cbar.ax.tick_params(colors='white')
            
            ax.grid(True, alpha=0.2)
            ax.tick_params(colors='white')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Statistics
            believers_count = np.sum((W_heat >= 0.5) & (B_heat >= 0.5))
            hypocrites_count = np.sum((W_heat < 0.5) & (B_heat < 0.5))
            st.info(
                f"🟢 {t('legend_believer')}: {believers_count} ({believers_count/N*100:.0f}%) | "
                f"🔴 {t('legend_hypocrite')}: {hypocrites_count} ({hypocrites_count/N*100:.0f}%)"
            )

# =============================================
# TAB 7: PERSONAL COMPASS (🧭 بَوْصَلَة)
# =============================================
with tabs[7]:
    st.header(t("compass_title"))
    st.markdown(t("compass_subtitle"))
    
    # Define the 28 questions (14 for W, 14 for B)
    compass_questions = {
        "W": [
            ("هَلْ تَعِيشُ لِلَّهِ وَحْدَهُ؟" if LANG == "ar" else "Do you live for Allah alone?", 3),
            ("هَلْ تُقِيمُ الصَّلَاةَ بِخُشُوعٍ؟" if LANG == "ar" else "Do you pray with devotion?", 3),
            ("هَلْ تُؤَدِّي الزَّكَاةَ وَتَتَصَدَّقُ؟" if LANG == "ar" else "Do you pay Zakat & give charity?", 3),
            ("هَلْ تَصُومُ رَمَضَانَ وَتَطَوَّعًا؟" if LANG == "ar" else "Do you fast Ramadan & voluntarily?", 3),
            ("هَلْ تَحُجُّ أَوْ تَسْعَى لِلْحَجِّ؟" if LANG == "ar" else "Do you perform/seek Hajj?", 3),
            ("هَلْ تُحِبُّ اللَّهَ وَرَسُولَهُ أَكْثَرَ مِنْ كُلِّ شَيْءٍ؟" if LANG == "ar" else "Do you love Allah & Messenger most?", 3),
            ("هَلْ تَصْدُقُ فِي أَقْوَالِكَ وَأَفْعَالِكَ؟" if LANG == "ar" else "Are you truthful in words & deeds?", 3),
            ("هَلْ تُؤَدِّي الْأَمَانَاتِ؟" if LANG == "ar" else "Do you fulfill trusts?", 3),
            ("هَلْ تَتَوَكَّلُ عَلَى اللَّهِ مَعَ الْأَخْذِ بِالْأَسْبَابِ؟" if LANG == "ar" else "Do you rely on Allah while using means?", 3),
            ("هَلْ تَشْكُرُ فِي الرَّخَاءِ وَتَصْبِرُ فِي الْبَلَاءِ؟" if LANG == "ar" else "Are you grateful & patient?", 3),
            ("هَلْ تَحْمِلُ هَمَّ الْإِسْلَامِ وَالْمُسْلِمِينَ؟" if LANG == "ar" else "Do you care for Islam & Muslims?", 3),
            ("هَلْ تَفِي بِالْعَهْدِ؟" if LANG == "ar" else "Do you keep your promises?", 3),
            ("هَلْ أَنْتَ رَاضٍ بِمَا قَسَمَ اللَّهُ لَكَ؟" if LANG == "ar" else "Are you content with Allah's decree?", 3),
            ("هَلْ تَنْصُرُ الْمُؤْمِنَ إِذَا ظُلِمَ؟" if LANG == "ar" else "Do you help the oppressed believer?", 3),
        ],
        "B": [
            ("هَلْ تَأْمُرُ بِالْمَعْرُوفِ؟" if LANG == "ar" else "Do you enjoin good?", 3),
            ("هَلْ تَنْهَى عَنِ الْمُنْكَرِ؟" if LANG == "ar" else "Do you forbid evil?", 3),
            ("هَلْ أَنْتَ مُسْتَعِدٌّ لِبَذْلِ النَّفْسِ وَالْمَالِ فِي سَبِيلِ اللَّهِ؟" if LANG == "ar" else "Ready to sacrifice for Allah?", 3),
            ("هَلْ تَتَبَرَّأُ مِنَ الشِّرْكِ وَأَهْلِهِ؟" if LANG == "ar" else "Do you disavow polytheism?", 3),
            ("هَلْ تَرْفُضُ الْكُفْرَ وَالْإِلْحَادَ؟" if LANG == "ar" else "Do you reject disbelief/atheism?", 3),
            ("هَلْ تَكْرَهُ النِّفَاقَ وَالتَّلَوُّنَ؟" if LANG == "ar" else "Do you hate hypocrisy?", 3),
            ("هَلْ تُجَاهِدُ نَفْسَكَ عَلَى تَرْكِ الْكَذِبِ؟" if LANG == "ar" else "Do you struggle against lying?", 3),
            ("هَلْ تَتَجَنَّبُ الْغِشَّ فِي مُعَامَلَاتِكَ؟" if LANG == "ar" else "Do you avoid fraud?", 3),
            ("هَلْ تَفِي بِعُهُودِكَ وَلَا تَخُونُ؟" if LANG == "ar" else "Do you keep trusts, no betrayal?", 3),
            ("هَلْ تَرْفُضُ الظُّلْمَ بِكُلِّ صُوَرِهِ؟" if LANG == "ar" else "Do you reject all injustice?", 3),
            ("هَلْ تُجَاهِدُ نَفْسَكَ عَلَى تَرْكِ الْفَوَاحِشِ؟" if LANG == "ar" else "Do you struggle against immorality?", 3),
            ("هَلْ تُخْلِصُ عَمَلَكَ لِلَّهِ وَتَجْتَنِبُ الرِّيَاءَ؟" if LANG == "ar" else "Is your work sincere, no showing off?", 3),
            ("هَلْ تَسْلَمُ لِلَّهِ فِي قِسْمَتِهِ وَلَا تَحْسُدُ؟" if LANG == "ar" else "Do you accept Allah's decree, no envy?", 3),
            ("هَلْ تُحِبُّ فِي اللَّهِ وَتُبْغِضُ فِي اللَّهِ؟" if LANG == "ar" else "Do you love & hate for Allah's sake?", 3),
        ]
    }
    
    # Display questions in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {t('compass_loyalty')}")
        for i, (q, _) in enumerate(compass_questions["W"]):
            options = [
                ("نَعَمْ" if LANG == "ar" else "Yes", 3),
                ("أَحْيَانًا" if LANG == "ar" else "Sometimes", 1),
                ("لَا" if LANG == "ar" else "No", 0)
            ]
            ans = st.radio(
                q,
                options,
                key=f"cw_{i}",
                index=None,
                format_func=lambda x: x[0]
            )
            if ans:
                st.session_state.compass_answers[f"W{i}"] = ans[1]
    
    with col2:
        st.markdown(f"#### {t('compass_disavowal')}")
        for i, (q, _) in enumerate(compass_questions["B"]):
            options = [
                ("نَعَمْ" if LANG == "ar" else "Yes", 3),
                ("أَحْيَانًا" if LANG == "ar" else "Sometimes", 1),
                ("لَا" if LANG == "ar" else "No", 0)
            ]
            ans = st.radio(
                q,
                options,
                key=f"cb_{i}",
                index=None,
                format_func=lambda x: x[0]
            )
            if ans:
                st.session_state.compass_answers[f"B{i}"] = ans[1]
    
    TOTAL_Q = 28
    
    # Show result when all questions are answered
    if len(st.session_state.compass_answers) == TOTAL_Q:
        # Calculate scores
        W_score = sum(st.session_state.compass_answers[f"W{i}"] for i in range(14))
        B_score = sum(st.session_state.compass_answers[f"B{i}"] for i in range(14))
        W_val = W_score / 42.0
        B_val = B_score / 42.0
        S_val = W_val * B_val
        
        st.divider()
        st.header(t("compass_result"))
        
        # Determine quadrant
        if W_val >= 0.5 and B_val >= 0.5:
            q_name = t("quadrant_labels", "believer")
            q_color = 'green'
        elif W_val < 0.5 and B_val >= 0.5:
            q_name = t("quadrant_labels", "harsh")
            q_color = 'orange'
        elif W_val < 0.5 and B_val < 0.5:
            q_name = t("quadrant_labels", "hypocrite")
            q_color = 'red'
        else:
            q_name = t("quadrant_labels", "weak")
            q_color = 'blue'
        
        # Display result card
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f"""
            <div style="background: rgba(10,10,46,0.8); border-radius: 15px; padding: 25px; border: 3px solid {q_color}; text-align: center;">
                <p style="font-size: 2.5em; font-weight: bold; color: {q_color}; margin: 0;">{q_name}</p>
                <p style="color: #FFD700; font-size: 1.3em; margin: 15px 0;">⚖️ S = {S_val:.2f}</p>
                <p style="color: #aaa; font-size: 0.9em;">W = {W_val:.2f} | B = {B_val:.2f}</p>
                <p style="color: #aaa; font-size: 0.8em;">({W_score}/42 | {B_score}/42)</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Draw the quadrant map
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a1a')
        ax.set_facecolor('#0a0a1a')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axhline(0.5, color='gray', ls=':')
        ax.axvline(0.5, color='gray', ls=':')
        ax.set_xlabel('B (Disavowal)' if LANG == "en" else 'B (الْبَرَاءَةُ)', color='white')
        ax.set_ylabel('W (Loyalty)' if LANG == "en" else 'W (الْوَلَاءُ)', color='white')
        
        # Plot the user's position
        ax.scatter(B_val, W_val, s=400, c='cyan', edgecolors='white', linewidth=3, zorder=10)
        
        # Color quadrants
        ax.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green')
        ax.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='orange')
        ax.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='blue')
        ax.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='red')
        
        # Label quadrants
        for lbl, x, y, col in [("believer", 0.75, 0.75, 'green'), ("harsh", 0.25, 0.75, 'orange'), ("hypocrite", 0.25, 0.25, 'red'), ("weak", 0.75, 0.25, 'blue')]:
            ax.text(x, y, t("quadrant_labels", lbl), color=col, fontsize=12, ha='center', fontweight='bold')
        
        ax.grid(True, alpha=0.2)
        ax.tick_params(colors='white')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Reset button
        if st.button(t("compass_reset"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

# =============================================
# TAB 8: ENCYCLOPEDIA LIBRARY (📚 افْهَمْ)
# =============================================
with tabs[8]:
    st.header(t('library_title'))
    
    # Create sub-tabs for library sections
    lib_sections = [
        ("summary", "📜 " + ("خُلَاصَةُ النَّظَرِيَّةِ" if LANG == "ar" else "Theory Summary")),
        ("cosmic", "🌌 " + ("الدَّلِيلُ الْكَوْنِيُّ" if LANG == "ar" else "Cosmic Proof")),
        ("lexicon", "🔤 " + ("الْمُعْجَمُ الْهَنْدَسِيُّ" if LANG == "ar" else "Geometric Lexicon")),
        ("paper", "📄 " + ("الْوَرَقَةُ الْأَكَادِيمِيَّةُ" if LANG == "ar" else "Academic Paper")),
    ]
    
    lib_tabs = st.tabs([name for _, name in lib_sections])
    
    # --- SECTION 1: Theory Summary ---
    with lib_tabs[0]:
        st.markdown(f"""
        ### {('خُلَاصَةُ نَظَرِيَّةِ الْمِيزَانِ' if LANG == 'ar' else 'Summary of The Mizan Theory')}
        
        **{('الدِّينُ الْقَيِّمُ' if LANG == 'ar' else 'Al-Deen Al-Qayyim (The Upright Religion)')}**:  
        {('قَانُونُ السَّبَبِيَّةِ الْكَوْنِيِّ الثَّابِتُ فِي أَصْلِهِ، الْمُتَجَدِّدُ فِي تَطْبِيقَاتِهِ. هُوَ الْمِيزَانُ الَّذِي فَطَرَ اللَّهُ عَلَيْهِ السَّمَاوَاتِ وَالْأَرْضَ.' if LANG == 'ar' else 'The cosmic law of causality, constant in its origin, dynamic in its applications. It is the balance upon which Allah created the heavens and the earth.')}
        
        **{('الْإِسْلَامُ الْحَنِيفُ' if LANG == 'ar' else 'Al-Islam Al-Hanif (The Upright Submission)')}**:  
        {('الِاسْتِجَابَةُ الدِّينَامِيكِيَّةُ الطَّوْعِيَّةُ لِهَذَا الْقَانُونِ، مِنْ خِلَالِ آلِيَّةِ الْوَلَاءِ لِلهِ وَالْبَرَاءَةِ مِنَ الطَّاغُوتِ.' if LANG == 'ar' else 'The dynamic, voluntary response to this law, through the mechanism of loyalty to God and disavowal of false deities.')}
        
        **{('مُعَادَلَةُ الثَّبَاتِ الْوُجُودِيِّ' if LANG == 'ar' else 'The Existential Stability Equation')}**:  
        `S = W × B`
        
        - **W (Al-Walaa - {('الْوَلَاءُ' if LANG == 'ar' else 'Loyalty')})**: {('طَاقَةُ الْحُبِّ وَالطَّاعَةِ وَالنُّصْرَةِ نَحْوَ اللَّهِ وَرَسُولِهِ وَالْمُؤْمِنِينَ.' if LANG == 'ar' else 'The energy of love, obedience, and support directed towards Allah, His Messenger, and the believers.')}
        - **B (Al-Baraa - {('الْبَرَاءَةُ' if LANG == 'ar' else 'Disavowal')})**: {('طَاقَةُ الْبُغْضِ وَالْمُفَاصَلَةِ وَالْمُنَاعَةِ مِنَ الْكُفْرِ وَالشِّرْكِ وَالطَّاغُوتِ.' if LANG == 'ar' else 'The energy of hatred, disassociation, and immunity from disbelief, polytheism, and false deities.')}
        - **S (Al-Thabat - {('الثَّبَاتُ' if LANG == 'ar' else 'Stability')})**: {('الْعُرْوَةُ الْوُثْقَى – حَالَةُ الِاسْتِقْرَارِ الْوُجُودِيِّ.' if LANG == 'ar' else 'The Firm Handhold – the state of existential stability.')}
        
        **{('التَّصْنِيفُ الْقُرْآنِيُّ لِلْبَشَرِ' if LANG == 'ar' else 'Quranic Classification of Humans')}**:
        - 🟢 **{('الْمُؤْمِنُ' if LANG == 'ar' else 'The Believer')}**: W+, B+, S=+1
        - 🔴 **{('الْكَافِرُ' if LANG == 'ar' else 'The Disbeliever')}**: W-, B+, S=-1
        - 🩷 **{('الْمُنَافِقُ' if LANG == 'ar' else 'The Hypocrite')}**: W≈0, B≈0, S=0
        - 🟠 **{('الْمُشْرِكُ' if LANG == 'ar' else 'The Polytheist')}**: W+, B-, S=-1
        """)
    
    # --- SECTION 2: Cosmic Proof ---
    with lib_tabs[1]:
        st.markdown(f"""
        ### {('الدَّلِيلُ الْكَوْنِيُّ عَلَى وِحْدَةِ الْخَلْقِ وَالْأَمْرِ' if LANG == 'ar' else 'The Cosmic Proof for the Unity of Creation and Command')}
        
        **{('الْفِيزِيَاءُ' if LANG == 'ar' else 'Physics')}**:  
        {('الْجَاذِبِيَّةُ (W) تَجْمَعُ الْكُتَلَ، وَالتَّنَافُرُ الْكَهْرُومِغْنَاطِيسِيُّ (B) يَمْنَعُ التَّصَادُمَ. تَوَازُنُهُمَا (S) يَحْفَظُ اسْتِقْرَارَ الذَّرَّةِ وَالْمَجَرَّةِ. لَوْ زَادَ أَحَدُهُمَا عَلَى الْآخَرِ لَانْهَارَ النِّظَامُ الْكَوْنِيُّ.' if LANG == 'ar' else 'Gravity (W) attracts masses, while electromagnetic repulsion (B) prevents collision. Their balance (S) preserves the stability of the atom and galaxy. If one overpowered the other, the cosmic system would collapse.')}
        
        **{('الْكِيمْيَاءُ' if LANG == 'ar' else 'Chemistry')}**:  
        {('التَّفَاعُلُ وَالِاتِّحَادُ (W) يُكَوِّنَانِ الْمُرَكَّبَاتِ، وَالتَّفَكُّكُ وَالِانْفِصَالُ (B) يُحَلِّلَانِهَا. كِلَاهُمَا ضَرُورِيَّانِ لِلتَّوَازُنِ الْكِيمْيَائِيِّ.' if LANG == 'ar' else 'Synthesis and union (W) form compounds, while decomposition and separation (B) break them down. Both are essential for chemical equilibrium.')}
        
        **{('الْبِيُولُوجْيَا' if LANG == 'ar' else 'Biology')}**:  
        {('جِهَازُ الْمَنَاعَةِ هُوَ التَّجَلِّي الْأَوْضَحُ: يُوَالِي خَلَايَا الذَّاتِ (W=1) وَيُهَاجِمُ الْأَجْسَامَ الْغَرِيبَةَ (B=1). اخْتِلَالُهُ يُسَبِّبُ أَمْرَاضَ الْمَنَاعَةِ الذَّاتِيَّةِ أَوِ السَّرَطَانَ.' if LANG == 'ar' else 'The immune system is the clearest manifestation: it protects self-cells (W=1) and attacks foreign bodies (B=1). Its imbalance causes autoimmune diseases or cancer.')}
        
        **{('التَّارِيخُ' if LANG == 'ar' else 'History')}**:  
        {('الْحَضَارَاتُ تَقُومُ بِتَوَازُنِ W وَ B، وَتَسْقُطُ بِاخْتِلَالِ أَحَدِهِمَا. الِاسْتِدْرَاجُ هُوَ تَأَخُّرُ انْهِيَارِ التَّمْكِينِ (E) عَنِ انْهِيَارِ الثَّبَاتِ (S)، كَمَا حَدَثَ لِلدَّوْلَةِ الْعُثْمَانِيَّةِ وَالِاتِّحَادِ السُّوفْيَتِيِّ.' if LANG == 'ar' else 'Civilizations rise with the balance of W and B, and fall when either is compromised. Istidraj is the delayed collapse of empowerment (E) after stability (S) falls, as happened to the Ottoman Empire and the Soviet Union.')}
        """)
    
    # --- SECTION 3: Geometric Lexicon ---
    with lib_tabs[2]:
        st.markdown(f"### {t('lexicon_title')}")
        st.markdown(("Select a Quranic tool to see its geometric symbol and function in the law of causality." if LANG == "en" else "اخْتَرْ أَدَاةً قُرْآنِيَّةً لِتَرَى رَمْزَهَا الْهَنْدَسِيَّ وَوَظِيفَتَهَا فِي قَانُونِ السَّبَبِيَّةِ."))
        
        tools = {
            "فَاءُ السَّبَبِيَّةِ (فَـ)": ("=", {
                "ar": "عَلَامَةُ يُسَاوِي. تَرْبِطُ السَّبَبَ بِالنَّتِيجَةِ حَتْمًا. مِثَال: ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَـ قَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾.",
                "en": "Equals sign. Inevitably connects cause to effect. E.g., {Whoever disbelieves in false deities and believes in Allah = has grasped the firm handhold}."
            }),
            "لَامُ التَّعْلِيلِ (لِـ)": ("→", {
                "ar": "سَهْمُ الْغَايَةِ. يُوَضِّحُ اتِّجَاهَ الْمَقْصِدِ مِنَ الْفِعْلِ. مِثَال: ﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِـ يَعْبُدُونِ﴾.",
                "en": "Arrow of purpose. Shows the direction of intent. E.g., {I have not created jinn and mankind except to → worship Me}."
            }),
            "حَتَّى الْغَائِيَّةِ": ("...", {
                "ar": "اسْتِمْرَارُ السَّبَبِ حَتَّى تَتَحَقَّقَ النَّتِيجَةُ. مِثَال: ﴿حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ﴾.",
                "en": "Continuation of cause until result is achieved. E.g., {Until they change what is within themselves}."
            }),
            "إِنْ الشَّرْطِيَّةُ": ("( )ᵒ", {
                "ar": "قَوْسُ الشَّرْطِ الِاخْتِيَارِيِّ. يُمَثِّلُ حُرِّيَّةَ الْإِنْسَانِ فِي اخْتِيَارِ السَّبَبِ. مِثَال: ﴿فَإِن تَابُوا وَأَقَامُوا الصَّلَاةَ﴾.",
                "en": "Optional condition. Represents human free will in choosing the cause. E.g., {If they repent and establish prayer}."
            }),
            "إِذَا الشَّرْطِيَّةُ": ("( )ᶜ", {
                "ar": "قَوْسُ الشَّرْطِ الْمُحَقَّقِ. يُمَثِّلُ حَتْمِيَّةَ الْجَزَاءِ عِنْدَ تَحَقُّقِ الشَّرْطِ. مِثَال: ﴿إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ﴾.",
                "en": "Certain condition. Represents the inevitability of recompense when the condition is met. E.g., {When the victory of Allah has come}."
            }),
            "إِلَّا (أَدَاةُ اسْتِثْنَاءٍ)": ("{}", {
                "ar": "حُدُودُ الْمَجْمُوعَةِ. تُحَدِّدُ مَنْ هُمْ أَهْلُ الْوِلَايَةِ وَالنَّجَاةِ. مِثَال: ﴿إِلَّا مَن رَّحِمَ﴾.",
                "en": "Set boundaries. Defines the group of loyalty and salvation. E.g., {Except those upon whom Allah has mercy}."
            }),
            "كَلَّا (حَرْفُ رَدْعٍ)": ("⛔", {
                "ar": "قَطْعُ الْأَسْبَابِ الْبَاطِلَةِ وَالْمَعَادَلَاتِ الْفَاسِدَةِ. مِثَال: ﴿كَلَّا إِنَّ الْإِنسَانَ لَيَطْغَىٰ﴾.",
                "en": "Severing false causes and corrupt equations. E.g., {No! Indeed, man transgresses}."
            }),
        }
        
        sel = st.selectbox(t('select_tool'), list(tools.keys()))
        if sel:
            st.metric("الرَّمْزُ الْهَنْدَسِيُّ" if LANG == "ar" else "Geometric Symbol", tools[sel][0])
            st.info(tools[sel][1][LANG])
    
    # --- SECTION 4: Academic Paper ---
    with lib_tabs[3]:
        st.markdown(f"""
        ### {('الْوَرَقَةُ الْأَكَادِيمِيَّةُ (مُلَخَّصٌ)' if LANG == 'ar' else 'Academic Paper (Abstract)')}
        
        **{('نَظَرِيَّةُ الْمِيزَانِ: نَمُوذَجٌ رِيَاضِيٌّ مُوَحَّدٌ لِلثَّبَاتِ الْوُجُودِيِّ مُسْتَنْبَطٌ مِنَ الْأُصُولِ الْقُرْآنِيَّةِ' if LANG == 'ar' else 'The Mizan Theory: A Unified Mathematical Model of Existential Stability Derived from Quranic Principles')}**
        
        **{('الْمُؤَلِّفُ: عَلِي عَادِل الْعَاطِفِيّ | 2026' if LANG == 'ar' else 'Author: Ali Adel Alatifi | 2026')}**
        
        ---
        
        {('تُقَدِّمُ هَذِهِ الْوَرَقَةُ نَظَرِيَّةَ الْمِيزَانِ، وَهِيَ نَمُوذَجٌ رِيَاضِيٌّ مُوَحَّدٌ مُسْتَنْبَطٌ مِنَ الْقُرْآنِ الْكَرِيمِ. الْمُعَادَلَةُ الْمَرْكَزِيَّةُ S = W × B تَصِفُ الثَّبَاتَ الْوُجُودِيَّ كَدَالَّةٍ ضَرْبِيَّةٍ لِلْوَلَاءِ (W) وَالْبَرَاءَةِ (B).' if LANG == 'ar' else 'This paper introduces The Mizan Theory, a novel unified mathematical model derived from the Holy Quran. The core equation S = W × B describes existential stability as a multiplicative function of Loyalty (W) and Disavowal (B).')}
        
        {('نُثْبِتُ، مِنْ خِلَالِ النَّمْذَجَةِ الرِّيَاضِيَّةِ وَالْمُحَاكَاةِ الْحَاسُوبِيَّةِ الْقَائِمَةِ عَلَى الْوُكَلَاءِ (Agent-Based Modeling)، أَنَّ هَذِهِ الْمُعَادَلَةَ الْوَاحِدَةَ تَحْكُمُ دِينَامِيكِيَّةَ الِاسْتِقْرَارِ فِي الْفِيزِيَاءِ (الْجَاذِبِيَّةُ وَالتَّنَافُرُ)، وَالْكِيمْيَاءِ (التَّفَاعُلُ وَالِانْفِصَالُ)، وَالْبِيُولُوجْيَا (جِهَازُ الْمَنَاعَةِ)، وَعِلْمِ النَّفْسِ، وَعِلْمِ الِاجْتِمَاعِ، وَالتَّارِيخِ (دَوْرَةُ صُعُودِ وَسُقُوطِ الْحَضَارَاتِ).' if LANG == 'ar' else 'We demonstrate, through mathematical modeling and agent-based computer simulation, that this single equation governs the dynamics of stability in physics (gravity and repulsion), chemistry (synthesis and decomposition), biology (the immune system), psychology, sociology, and history (the rise and fall of civilizations).')}
        
        {('يُنَجِّحُ النَّمُوذَجُ فِي تَكْرَارِ سُنَّةِ الِاسْتِدْرَاجِ الْقُرْآنِيَّةِ، حَيْثُ يَتَأَخَّرُ التَّمْكِينُ الْمَادِّيُّ (E) فِي الِانْهِيَارِ عَنِ الثَّبَاتِ الْأَخْلَاقِيِّ (S)، مِمَّا يُفَسِّرُ الِانْهِيَارَاتِ الْمُفَاجِئَةَ لِلْحَضَارَاتِ الَّتِي تَبْدُو قَوِيَّةً ظَاهِرِيًّا. كَمَا يُقَدِّمُ إِطَارًا كَمِّيًّا قَابِلًا لِلِاخْتِبَارِ لِلتَّصْنِيفِ الْقُرْآنِيِّ لِلْبَشَرِ إِلَى أَرْبَعَةِ أَرْبَاعٍ: الْمُؤْمِنُ، الْكَافِرُ، الْمُنَافِقُ، وَالْمُشْرِكُ.' if LANG == 'ar' else 'The model successfully replicates the Quranic law of Istidraj, where material empowerment (E) lags behind moral stability (S) in its collapse, explaining the sudden downfalls of seemingly powerful civilizations. It also provides a quantitative, falsifiable framework for the Quranic classification of humans into four quadrants: the Believer, the Disbeliever, the Hypocrite, and the Polytheist.')}
        
        **{('الْكَلِمَاتُ الْمِفْتَاحِيَّةُ' if LANG == 'ar' else 'Keywords')}:**  
        {('نَظَرِيَّةُ كُلِّ شَيْءٍ، الْقُرْآنُ، الْإِسْلَامُ، نَمُوذَجٌ رِيَاضِيٌّ، الثَّبَاتُ، الِاسْتِدْرَاجُ، مُحَاكَاةٌ قَائِمَةٌ عَلَى الْوُكَلَاءِ' if LANG == 'ar' else 'Theory of Everything, Quran, Islam, Mathematical Model, Stability, Istidraj, Agent-Based Simulation')}
        """)

# =============================================
# 🏁 FOOTER
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: #888; font-size: 0.9em; line-height: 1.8;">
    <p>{t('footer')}</p>
    <p style="font-size: 0.8em; margin-top: 10px;">
        ⚖️ S = W × B | 
        {'الدِّينُ الْقَيِّمُ وَالْإِسْلَامُ الْحَنِيفُ' if LANG == 'ar' else 'Al-Deen Al-Qayyim & Al-Islam Al-Hanif'} | 
        {'مَنْصَّةُ الْمِيزَانِ الْعَالَمِيَّةُ' if LANG == 'ar' else 'The Global Mizan Platform'}
    </p>
</div>
""", unsafe_allow_html=True)
