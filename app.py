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
st.set_page_config(page_title="The Golden Platform – Mizan Lab", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# =============================================
# MULTILINGUAL TRANSLATION DICTIONARY (AR/EN)
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
    "tab_understand": {"ar": "📚 افْهَمْ", "en": "📚 Understand"},
    "control_panel": {"ar": "🧭 لَوْحَةُ التَّحَكُّمِ", "en": "🧭 Control Panel"},
    "param_w": {"ar": "W (الْوَلَاءُ)", "en": "W (Loyalty)"},
    "param_b": {"ar": "B (الْبَرَاءَةُ)", "en": "B (Disavowal)"},
    "param_e": {"ar": "E (التَّمْكِينُ)", "en": "E (Empowerment)"},
    "param_lag": {"ar": "فَجْوَةُ الِاسْتِدْرَاجِ", "en": "Istidraj Gap"},
    "dashboard": {"ar": "لَوْحَةُ الْمُؤَشِّرَاتِ", "en": "Dashboard"},
    "footer": {"ar": "© 2026 علي عادل العاطفي | الْمَنْصَةُ الذَّهَبِيَّةُ", "en": "© 2026 Ali Adel Alatifi | The Golden Platform"},
    "lang_selector": {"ar": "اللُّغَةُ", "en": "Language"},
    "advisor_title": {"ar": "🧠 الْمُسْتَشَارُ الْفَائِقُ", "en": "🧠 The Super Advisor"},
    "advisor_subtitle": {"ar": "اسْأَلْ عَنْ أَيِّ شَيْءٍ فِي نَظَرِيَّةِ الْمِيزَانِ.", "en": "Ask about anything in the Mizan Theory."},
    "ask_placeholder": {"ar": "مِثَال: مَا هُوَ الِاسْتِدْرَاجُ؟", "en": "E.g., What is Istidraj?"},
    "analyzing": {"ar": "🧠 يُحَلِّلُ...", "en": "🧠 Analyzing..."},
    "simulation_note": {"ar": "📊 مُحَاكَاةٌ حَيَّةٌ:", "en": "📊 Live simulation:"},
    "launch_clash": {"ar": "🚀 أَطْلِقْ صِرَاعَ الْحَضَارَاتِ", "en": "🚀 Launch Clash"},
    "clash_success": {"ar": "الْبَقَاءُ لِلْأَقْوَى مِيزَانًا.", "en": "Survival of the fittest Mizan."},
    "personal_title": {"ar": "🧍 مُخْتَبَرُ الْوَلَاءِ وَالْبَرَاءَةِ", "en": "🧍 Loyalty & Disavowal Lab"},
    "personal_subtitle": {"ar": "اضْبِطْ مُؤَثِّرَاتِ W وَ B كَمَا وَرَدَتْ فِي الْكِتَابِ وَالسُّنَّةِ.", "en": "Adjust the factors of W & B as per the Quran & Sunnah."},
    "w_group_label": {"ar": "🤍 مُقَوِّيَاتُ الْوَلَاءِ (W)", "en": "🤍 Loyalty Boosters (W)"},
    "b_group_label": {"ar": "❤️ مُقَوِّيَاتُ الْبَرَاءَةِ (B)", "en": "❤️ Disavowal Boosters (B)"},
    "result_w": {"ar": "وَلَاءٌ (W)", "en": "Loyalty (W)"},
    "result_b": {"ar": "بَرَاءَةٌ (B)", "en": "Disavowal (B)"},
    "result_s": {"ar": "ثَبَاتٌ (S)", "en": "Stability (S)"},
    "safe_zone": {"ar": "🟢 أَنْتَ فِي رَبْعِ الْمُؤْمِنِينَ.", "en": "🟢 Believer's quadrant."},
    "warning_zone": {"ar": "🟡 مَوْقِعُكَ هَشٌّ.", "en": "🟡 Fragile position."},
    "danger_zone": {"ar": "🔴 أَنْتَ فِي مَنْطِقَةِ الْخَطَرِ.", "en": "🔴 Danger zone."},
    "map_caption": {"ar": "📍 مَوْقِعُكَ عَلَى خَرِيطَةِ (W, B)", "en": "📍 Your position on the (W, B) map"},
    "library_title": {"ar": "📚 الْمَكْتَبَةُ", "en": "📚 Library"},
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
    "society_subtitle": {"ar": "شَاهِدْ كَيْفَ تَنْتَشِرُ قِيَمُ W وَ B فِي مُجْتَمَعٍ افْتِرَاضِيٍّ.", "en": "Watch how W & B values spread in a virtual society."},
    "pop_size": {"ar": "عَدَدُ الْأَفْرَادِ", "en": "Population Size"},
    "influence_radius": {"ar": "مَدَى التَّأَثُّرِ بِالْجِيرَانِ", "en": "Neighbor Influence Radius"},
    "sim_years": {"ar": "سَنَوَاتُ الْمُحَاكَاةِ", "en": "Simulation Years"},
    "run_society": {"ar": "▶️ تَشْغِيلُ الْمُحَاكَاةِ", "en": "▶️ Run Simulation"},
    "society_map_title": {"ar": "خَرِيطَةُ الْمُجْتَمَعِ بَعْدَ ", "en": "Society Map After "},
    "legend_believer": {"ar": "مُؤْمِن", "en": "Believer"},
    "legend_hypocrite": {"ar": "مُنَافِق", "en": "Hypocrite"},
    "legend_weak": {"ar": "ضَعِيف", "en": "Weak"},
    # Personal Lab factors
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
# LANGUAGE INITIALIZATION
# =============================================
if "lang" not in st.session_state: st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(key):
    return T.get(key, {}).get(LANG, key)

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
# SUPER ADVISOR
# =============================================
def get_super_advisor_response(user_query, lang="ar"):
    try:
        import openai
        client = openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        if st.secrets.get("OPENAI_API_KEY"):
            response = client.chat.completions.create(
                model="gpt-4o", temperature=0.7, max_tokens=800,
                messages=[{"role": "system", "content": "You are the Super Advisor of The Mizan Theory by Ali Adel Alatifi. Core: S=W×B."}, {"role": "user", "content": user_query}]
            )
            return response.choices[0].message.content
    except: pass
    q = user_query.lower()
    if "istidraj" in q or "استدراج" in q: return {"ar": "الِاسْتِدْرَاجُ: E يَتَأَخَّرُ عَنْ S ثُمَّ يَنْهَارُ فَجْأَةً. ﴿فَلَمَّا نَسُوا... أَخَذْنَاهُم بَغْتَةً﴾ [الأنعام: 44].", "en": "Istidraj: E lags behind S then collapses suddenly. {So when they forgot... We seized them suddenly} [Al-An'am:44]."}.get(lang, "")
    if "mizan" in q or "ميزان" in q: return {"ar": "S = W × B. ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256].", "en": "S = W × B. {Whoever disbelieves in false deities and believes in Allah has grasped the firm handhold} [Al-Baqarah:256]."}.get(lang, "")
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
    colors_map = {"believer": '#FFD700', "hypocrite": '#FF5252', "weak": '#E0E0E0', "harsh": '#FF8C00', "average": '#888888'}
    return colors_map.get(classification, '#888888')

def run_society_simulation(pop_size, influence_radius, years):
    np.random.seed(42)
    W = np.random.uniform(0.3, 0.9, pop_size)
    B = np.random.uniform(0.3, 0.9, pop_size)
    pos_x = np.random.uniform(0, 30, pop_size)
    pos_y = np.random.uniform(0, 30, pop_size)
    for step in range(years):
        new_W = W.copy(); new_B = B.copy()
        for i in range(pop_size):
            distances = np.sqrt((pos_x - pos_x[i])**2 + (pos_y - pos_y[i])**2)
            neighbors = np.where(distances < influence_radius)[0]
            neighbors = neighbors[neighbors != i]
            if len(neighbors) > 0:
                new_W[i] += 0.02 * (np.mean(W[neighbors]) - W[i])
                new_B[i] += 0.02 * (np.mean(B[neighbors]) - B[i])
            new_W[i] += 0.01 * (np.random.rand() - 0.5)
            new_B[i] += 0.01 * (np.random.rand() - 0.5)
            if W[i] > 0.7 and B[i] > 0.7: new_B[i] -= 0.005 * np.random.rand()
            new_W[i] = max(0.05, min(1.0, new_W[i])); new_B[i] = max(0.05, min(1.0, new_B[i]))
        W = new_W; B = new_B
        pos_x = np.clip(pos_x + np.random.randint(-1, 2, pop_size), 0, 29)
        pos_y = np.clip(pos_y + np.random.randint(-1, 2, pop_size), 0, 29)
    return W, B, pos_x, pos_y

# =============================================
# 🏠 WELCOME SCREEN
# =============================================
if 'entered' not in st.session_state: st.session_state.entered = False
if not st.session_state.entered:
    st.markdown(t("welcome_html"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t("enter_lab"), use_container_width=True, type="primary"):
            st.session_state.entered = True; st.rerun()
    st.stop()

# =============================================
# 🧭 SIDEBAR
# =============================================
with st.sidebar:
    st.markdown(f"## {t('control_panel')}")
    lang_option = st.selectbox(t('lang_selector'), ["🇸🇦 العربية", "🇬🇧 English"], index=0 if LANG == "ar" else 1)
    new_lang = "ar" if "العربية" in lang_option else "en"
    if new_lang != LANG: st.session_state.lang = new_lang; st.rerun()
    st.markdown("---")
    W_global = st.slider(t('param_w'), 0.0, 1.0, 0.7, 0.05)
    B_global = st.slider(t('param_b'), 0.0, 1.0, 0.6, 0.05)
    E_global = st.slider(t('param_e'), 0.0, 1.0, 0.3, 0.05)
    lag_global = st.slider(t('param_lag'), 5, 50, 22, 1)
    st.markdown("---"); st.markdown(f"*{t('footer')}*")

# =============================================
# 🗂️ MAIN TABS
# =============================================
tabs = st.tabs([t('tab_believe'), t('tab_advisor'), t('tab_observe'), t('tab_judge'), t('tab_society'), t('tab_understand')])

# =============================================
# TAB 0: COMMAND CENTER
# =============================================
with tabs[0]:
    st.header(t("command_center_title"))
    W_s, B_s, S_s, E_s = cosmic_engine(W_global, B_global, E_global, 200, lag_global)
    st.subheader(t('dashboard'))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🤍 W", f"{W_global:.2f}"); c2.metric("❤️ B", f"{B_global:.2f}")
    c3.metric("⚖️ S", f"{W_global*B_global:.2f}"); c4.metric("💫 E", f"{E_global:.2f}")
    st.markdown("---")
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a'); ax.set_facecolor('#0a0a1a')
    ax.plot(S_s, 'g-', linewidth=2, label='S'); ax.plot(E_s, 'b--', linewidth=2, label='E')
    ax.set_title(t("cycle_title"), color='white'); ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
    ax.grid(True, alpha=0.2); ax.set_ylim(0, 1.05); ax.tick_params(colors='white'); st.pyplot(fig)

# =============================================
# TAB 1: SUPER ADVISOR
# =============================================
with tabs[1]:
    st.header(t('advisor_title')); st.markdown(t('advisor_subtitle'))
    user_q = st.text_input("✍️ " + ("سُؤَالُكَ:" if LANG == "ar" else "Question:"), placeholder=t('ask_placeholder'))
    if user_q:
        with st.spinner(t('analyzing')):
            ans = get_super_advisor_response(user_q, LANG)
            st.markdown("### 💡 " + ("الْجَوَابُ:" if LANG == "ar" else "Answer:")); st.markdown(ans)
            w0, b0, e0 = (0.3, 0.3, 0.9) if "istidraj" in user_q.lower() or "استدراج" in user_q.lower() else (0.7, 0.6, 0.3)
            W_s, B_s, S_s, E_s = cosmic_engine(w0, b0, e0, 100, lag_global)
            st.markdown(t('simulation_note'))
            fig, ax = plt.subplots(figsize=(10, 3), facecolor='#0a0a1a'); ax.set_facecolor('#0a0a1a')
            ax.plot(S_s, 'g-', label='S'); ax.plot(E_s, 'b--', label='E')
            ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white'); ax.grid(True, alpha=0.2)
            ax.set_ylim(0, 1.05); ax.tick_params(colors='white'); st.pyplot(fig)

# =============================================
# TAB 2: PERSONAL LAB
# =============================================
with tabs[2]:
    st.header(t('personal_title')); st.markdown(t('personal_subtitle')); st.markdown("---")
    st.subheader(t('w_group_label'))
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        w_shahada = st.slider(t("w_shahada"), 0, 10, 8, 1); w_salat = st.slider(t("w_salat"), 0, 10, 7, 1)
        w_zakat = st.slider(t("w_zakat"), 0, 10, 6, 1); w_sawm = st.slider(t("w_sawm"), 0, 10, 7, 1)
        w_hajj = st.slider(t("w_hajj"), 0, 10, 5, 1); w_quran = st.slider(t("w_quran"), 0, 10, 6, 1)
    with col_w2:
        w_dhikr = st.slider(t("w_dhikr"), 0, 10, 7, 1); w_tawakkul = st.slider(t("w_tawakkul"), 0, 10, 8, 1)
        w_hubb = st.slider(t("w_hubb"), 0, 10, 9, 1); w_birr = st.slider(t("w_birr"), 0, 10, 8, 1)
        w_ihsan = st.slider(t("w_ihsan"), 0, 10, 8, 1); w_taawun = st.slider(t("w_taawun"), 0, 10, 7, 1)

    st.subheader(t('b_group_label'))
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        b_taghut = st.slider(t("b_taghut"), 0, 10, 9, 1); b_shirk = st.slider(t("b_shirk"), 0, 10, 9, 1)
        b_kufr = st.slider(t("b_kufr"), 0, 10, 8, 1); b_nifaq = st.slider(t("b_nifaq"), 0, 10, 8, 1)
        b_amr = st.slider(t("b_amr"), 0, 10, 7, 1); b_nahy = st.slider(t("b_nahy"), 0, 10, 7, 1)
        b_jihad_nafs = st.slider(t("b_jihad_nafs"), 0, 10, 9, 1)
    with col_b2:
        b_jihad = st.slider(t("b_jihad"), 0, 10, 7, 1); b_ghadd = st.slider(t("b_ghadd"), 0, 10, 8, 1)
        b_farj = st.slider(t("b_farj"), 0, 10, 9, 1); b_kadhib = st.slider(t("b_kadhib"), 0, 10, 9, 1)
        b_ghiba = st.slider(t("b_ghiba"), 0, 10, 8, 1); b_zulm = st.slider(t("b_zulm"), 0, 10, 9, 1)
        b_riba = st.slider(t("b_riba"), 0, 10, 9, 1)

    W_list = [w_shahada, w_salat, w_zakat, w_sawm, w_hajj, w_quran, w_dhikr, w_tawakkul, w_hubb, w_birr, w_ihsan, w_taawun]
    B_list = [b_taghut, b_shirk, b_kufr, b_nifaq, b_amr, b_nahy, b_jihad_nafs, b_jihad, b_ghadd, b_farj, b_kadhib, b_ghiba, b_zulm, b_riba]
    W_personal = sum(W_list) / 120.0; B_personal = sum(B_list) / 140.0; S_personal = W_personal * B_personal

    st.markdown("---"); st.subheader(t("result_title"))
    col1, col2, col3 = st.columns(3)
    col1.metric(t('result_w'), f"{W_personal:.2f}"); col2.metric(t('result_b'), f"{B_personal:.2f}"); col3.metric(t('result_s'), f"{S_personal:.2f}")
    if S_personal > 0.7: st.success(t('safe_zone'))
    elif S_personal > 0.4: st.warning(t('warning_zone'))
    else: st.error(t('danger_zone'))

    st.caption(t("map_caption"))
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a1a'); ax.set_facecolor('#0a0a1a')
    ax.axhline(0.5, color='gray', ls=':', lw=1); ax.axvline(0.5, color='gray', ls=':', lw=1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel('B', color='white'); ax.set_ylabel('W', color='white')
    ax.scatter(B_personal, W_personal, s=400, c='cyan', edgecolors='white', linewidth=3)
    ax.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green'); ax.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='orange')
    ax.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='blue'); ax.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='red')
    ax.text(0.75, 0.75, t("quadrant_labels")["believer"], color='green', fontsize=12, ha='center', fontweight='bold')
    ax.text(0.25, 0.75, t("quadrant_labels")["harsh"], color='orange', fontsize=12, ha='center', fontweight='bold')
    ax.text(0.25, 0.25, t("quadrant_labels")["hypocrite"], color='red', fontsize=12, ha='center', fontweight='bold')
    ax.text(0.75, 0.25, t("quadrant_labels")["weak"], color='blue', fontsize=12, ha='center', fontweight='bold')
    ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); st.pyplot(fig)

# =============================================
# TAB 3: NATIONS CLASH
# =============================================
with tabs[3]:
    st.header(t("nations_board_title"))
    nations = {
        ("أُمَّةُ الْإِيمَانِ" if LANG == "ar" else "Faith"): (0.9, 0.9, 0.1, "gold"),
        ("أُمَّةُ التَّرَفِ" if LANG == "ar" else "Luxury"): (0.3, 0.2, 0.9, "orange"),
        ("الظَّالِمَةُ" if LANG == "ar" else "Tyrant"): (0.1, 0.9, 0.8, "red"),
        ("الْعِلْمِ" if LANG == "ar" else "Knowledge"): (0.8, 0.6, 0.4, "cyan"),
    }
    if st.button(t('launch_clash'), use_container_width=True, type="primary"):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='#000010')
        for i, (name, (w0, b0, e0, col)) in enumerate(nations.items()):
            ax = axes[i//2, i%2]; ax.set_facecolor('#0a0a1a')
            W_s, B_s, S_s, E_s = cosmic_engine(w0, b0, e0, 200, lag_global)
            ax.plot(S_s, color=col, linewidth=2, label='S'); ax.plot(E_s, color=col, linestyle='--', alpha=0.6, label='E')
            ax.set_title(name, color=col, fontweight='bold'); ax.set_ylim(0, 1.05)
            ax.grid(True, alpha=0.2); ax.tick_params(colors='white')
            ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=8)
        plt.tight_layout(); st.pyplot(fig); st.success(t('clash_success'))

# =============================================
# TAB 4: SOCIETY LAB
# =============================================
with tabs[4]:
    st.header(t("society_title")); st.markdown(t("society_subtitle"))
    col1, col2, col3 = st.columns(3)
    with col1: pop_size = st.slider(t("pop_size"), 100, 800, 400, 50)
    with col2: influence_radius = st.slider(t("influence_radius"), 0.5, 5.0, 2.0, 0.5)
    with col3: sim_years = st.slider(t("sim_years"), 10, 100, 50, 10)
    if st.button(t("run_society"), use_container_width=True, type="primary"):
        with st.spinner(t('analyzing')):
            W_final, B_final, x_final, y_final = run_society_simulation(pop_size, influence_radius, sim_years)
            classifications = [classify_agent(W_final[i], B_final[i]) for i in range(pop_size)]
            colors = [get_agent_color(c) for c in classifications]
            fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a1a'); ax.set_facecolor('#0a0a1a')
            ax.scatter(x_final, y_final, c=colors, s=30, alpha=0.8, edgecolors='white', linewidths=0.3)
            ax.set_xlim(0, 30); ax.set_ylim(0, 30)
            ax.set_title(f"{t('society_map_title')}{sim_years} " + ("سَنَةً" if LANG == "ar" else "Years"), color='white', fontsize=16, fontweight='bold')
            ax.grid(False); ax.tick_params(colors='white')
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFD700', markersize=10, label=t('legend_believer')),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF5252', markersize=10, label=t('legend_hypocrite')),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='#E0E0E0', markersize=10, label=t('legend_weak')),
            ]
            ax.legend(handles=legend_elements, loc='upper right', facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
            st.pyplot(fig)

# =============================================
# TAB 5: LIBRARY
# =============================================
with tabs[5]:
    st.header(t('library_title'))
    with st.expander(t("summary_title"), expanded=True):
        st.markdown(f"""
        - **{('الدِّينُ الْقَيِّمُ' if LANG == 'ar' else 'Al-Deen Al-Qayyim')}**: {('قَانُونُ السَّبَبِيَّةِ الْكَوْنِيِّ.' if LANG == 'ar' else 'The cosmic law of causality.')}
        - **{('الْإِسْلَامُ الْحَنِيفُ' if LANG == 'ar' else 'Al-Islam Al-Hanif')}**: {('الِاسْتِجَابَةُ الدِّينَامِيكِيَّةُ.' if LANG == 'ar' else 'The dynamic response.')}
        - **{('مُعَادَلَةُ الثَّبَاتِ' if LANG == 'ar' else 'Stability Equation')}**: `S = W × B`
        - **W**: {('الْوَلَاءُ لِلهِ.' if LANG == 'ar' else 'Loyalty to God.')}
        - **B**: {('الْبَرَاءَةُ مِنَ الطَّاغُوتِ.' if LANG == 'ar' else 'Disavowal of False Deities.')}
        """)
    with st.expander(t("lexicon_title"), expanded=False):
        tools = {
            "فَاءُ السَّبَبِيَّةِ (فَـ)": ("=", {"ar": "تَرْبِطُ السَّبَبَ بِالنَّتِيجَةِ حَتْمًا.", "en": "Inevitably connects cause to effect."}),
            "لَامُ التَّعْلِيلِ (لِـ)": ("→", {"ar": "سَهْمُ الْغَايَةِ.", "en": "Arrow of purpose."}),
            "حَتَّى الْغَائِيَّةِ": ("...", {"ar": "اسْتِمْرَارُ السَّبَبِ حَتَّى النَّتِيجَةِ.", "en": "Continuation of cause until result."}),
            "إِلَّا": ("{}", {"ar": "حُدُودُ الْمَجْمُوعَةِ.", "en": "Boundaries of the set."}),
        }
        sel = st.selectbox(t('select_tool'), list(tools.keys()))
        if sel: st.metric("الرَّمْزُ" if LANG == "ar" else "Symbol", tools[sel][0]); st.info(tools[sel][1][LANG])

st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#666;'>{t('footer')}</p>", unsafe_allow_html=True)
