import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(
    page_title="The Golden Platform – Mizan Lab",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# MULTILINGUAL TRANSLATION DICTIONARY
# =============================================
T = {
    # --- Welcome Screen ---
    "welcome_html": {
        "ar": """
        <div style="direction: rtl; text-align: center; background: linear-gradient(180deg, #000000 0%, #0a1a0a 30%, #1a2e1a 70%, #0a1a0a 100%); 
        padding: 40px 20px; border-radius: 25px; border: 3px solid #FFD700; margin: 30px 0;
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.7);">
            <span style="font-size: 70px; display: block;">⚖️</span>
            <h1 style="color: #FFD700; font-size: 2.5em; margin: 15px 0; font-weight: 900; letter-spacing: 3px;">
                الْمَنْصَةُ الذَّهَبِيَّةُ
            </h1>
            <span style="font-size: 50px; display: block;">🧪</span>
            <h2 style="color: #FFD700; font-size: 1.5em; margin: 10px 0;">
                مُخْتَبَرُ نَظَرِيَّةِ الْمِيزَان
            </h2>
            <p style="color: #e0e0e0; font-size: 1.2em; margin: 30px 10px; line-height: 2.2; font-style: italic;">
                "هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟<br>
                هَذَا هُوَ نَمُوذَجُ الْمِيزَانِ الَّذِي يُثْبِتُ أَنَّ <b style="color: #FFD700;">S = W × B</b>"
            </p>
            <p style="color: #FFD700; font-size: 1.5em; margin: 30px 0 0 0; font-weight: bold;">علي عادل العاطفي</p>
            <p style="color: #FFD700; font-size: 1em; margin: 5px 0 0 0; font-style: italic; opacity: 0.8;">Ali Adel Alatifi | 2026</p>
        </div>
        """,
        "en": """
        <div style="text-align: center; background: linear-gradient(180deg, #000000 0%, #0a0a1a 30%, #0d0d2b 70%, #000000 100%); 
        padding: 40px 20px; border-radius: 25px; border: 3px solid #FFD700; margin: 30px 0;
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.7);">
            <span style="font-size: 70px; display: block;">⚖️</span>
            <h1 style="color: #FFD700; font-size: 2.5em; margin: 15px 0; font-weight: 900;">
                THE GOLDEN PLATFORM
            </h1>
            <span style="font-size: 50px; display: block;">🧪</span>
            <h2 style="color: #FFD700; font-size: 1.5em; margin: 10px 0;">
                The Mizan Theory Lab
            </h2>
            <p style="color: #e0e0e0; font-size: 1.2em; margin: 30px 10px; line-height: 2.2; font-style: italic;">
                "Is there a single law governing the atom and civilization?<br>
                This is the Mizan Model that proves <b style="color: #FFD700;">S = W × B</b>"
            </p>
            <p style="color: #FFD700; font-size: 1.5em; margin: 30px 0 0 0; font-weight: bold;">Ali Adel Alatifi</p>
            <p style="color: #FFD700; font-size: 1em; margin: 5px 0 0 0; font-style: italic; opacity: 0.8;">2026</p>
        </div>
        """
    },
    "enter_lab": {"ar": "🚀 ادْخُلْ إِلَى الْمُخْتَبَرِ", "en": "🚀 Enter the Lab"},
    "tab_believe": {"ar": "🛡️ آمِن", "en": "🛡️ Believe"},
    "tab_advisor": {"ar": "🧠 اسْتَشِرْ", "en": "🧠 Consult"},
    "tab_observe": {"ar": "🧍 رَاقِبْ", "en": "🧍 Observe"},
    "tab_judge": {"ar": "🌍 احْكُمْ", "en": "🌍 Judge"},
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
    "safe_zone": {"ar": "🟢 أَنْتَ فِي رَبْعِ الْمُؤْمِنِينَ.", "en": "🟢 You are in the Believer's quadrant."},
    "warning_zone": {"ar": "🟡 مَوْقِعُكَ هَشٌّ.", "en": "🟡 Your position is fragile."},
    "danger_zone": {"ar": "🔴 أَنْتَ فِي مَنْطِقَةِ الْخَطَرِ.", "en": "🔴 You are in the danger zone."},
    "map_caption": {"ar": "📍 مَوْقِعُكَ عَلَى خَرِيطَةِ (W, B)", "en": "📍 Your position on the (W, B) map"},
    "library_title": {"ar": "📚 الْمَكْتَبَةُ", "en": "📚 Library"},
    "summary_title": {"ar": "📜 خُلَاصَةُ النَّظَرِيَّةِ", "en": "📜 Theory Summary"},
    "lexicon_title": {"ar": "🔤 الْمُعْجَمُ الْهَنْدَسِيُّ", "en": "🔤 Geometric Lexicon"},
    "select_tool": {"ar": "اخْتَرْ أَدَاةً:", "en": "Select a tool:"},
    "command_center_title": {"ar": "🛡️ مَرْكَزُ الْقِيَادَةِ", "en": "🛡️ Command Center"},
    "civilization_cycle_title": {"ar": "دَوْرَةُ الْحَضَارَةِ", "en": "Civilization Cycle"},
    "nations_board_title": {"ar": "🌍 لَوْحَةُ الْأُمَمِ", "en": "🌍 Nations Board"},
    "cycle_title": {"ar": "دَوْرَةُ الْحَضَارَةِ", "en": "Civilization Cycle"},
    "result_title": {"ar": "📊 النَّتِيجَةُ", "en": "📊 Result"},
    "quadrant_labels": {
        "believer": {"ar": "الْمُؤْمِنُ", "en": "Believer"},
        "harsh": {"ar": "الْمُتَشَدِّدُ", "en": "Harsh"},
        "hypocrite": {"ar": "الْمُنَافِقُ", "en": "Hypocrite"},
        "weak": {"ar": "الضَّعِيفُ", "en": "Weak"},
    },
    # --- Personal Lab Factors (Arabic / English) ---
    "w_shahada": {"ar": "الشَّهَادَتَانِ", "en": "The Two Shahadas"},
    "w_salat": {"ar": "الصَّلَاةُ", "en": "Prayer (Salat)"},
    "w_zakat": {"ar": "الزَّكَاةُ وَالصَّدَقَةُ", "en": "Zakat & Charity"},
    "w_sawm": {"ar": "الصَّوْمُ", "en": "Fasting (Sawm)"},
    "w_hajj": {"ar": "الْحَجُّ وَالْعُمْرَةُ", "en": "Hajj & Umrah"},
    "w_quran": {"ar": "تِلَاوَةُ الْقُرْآنِ وَتَدَبُّرُهُ", "en": "Reciting & Pondering Quran"},
    "w_dhikr": {"ar": "الذِّكْرُ وَالدُّعَاءُ", "en": "Remembrance & Supplication"},
    "w_tawakkul": {"ar": "التَّوَكُّلُ عَلَى اللَّهِ", "en": "Reliance on Allah (Tawakkul)"},
    "w_hubb": {"ar": "حُبُّ اللَّهِ وَرَسُولِهِ ﷺ", "en": "Love of Allah & His Messenger"},
    "w_birr": {"ar": "بِرُّ الْوَالِدَيْنِ وَصِلَةُ الرَّحِمِ", "en": "Kindness to Parents & Kin"},
    "w_ihsan": {"ar": "الْإِحْسَانُ وَحُسْنُ الْخُلُقِ", "en": "Excellence & Good Character"},
    "w_taawun": {"ar": "التَّعَاوُنُ عَلَى الْبِرِّ وَالتَّقْوَى", "en": "Cooperating in Righteousness"},
    "b_taghut": {"ar": "الْكُفْرُ بِالطَّاغُوتِ", "en": "Disbelief in False Deities"},
    "b_shirk": {"ar": "الْبَرَاءَةُ مِنَ الشِّرْكِ وَأَهْلِهِ", "en": "Disavowal of Polytheism"},
    "b_kufr": {"ar": "الْبَرَاءَةُ مِنَ الْكُفْرِ وَالْإِلْحَادِ", "en": "Disavowal of Disbelief/Atheism"},
    "b_nifaq": {"ar": "الْبَرَاءَةُ مِنَ النِّفَاقِ", "en": "Disavowal of Hypocrisy"},
    "b_amr": {"ar": "الْأَمْرُ بِالْمَعْرُوفِ", "en": "Enjoining Good"},
    "b_nahy": {"ar": "النَّهْيُ عَنِ الْمُنْكَرِ", "en": "Forbidding Evil"},
    "b_jihad_nafs": {"ar": "جِهَادُ النَّفْسِ", "en": "Struggle Against the Self"},
    "b_jihad": {"ar": "الْجِهَادُ فِي سَبِيلِ اللَّهِ", "en": "Striving in Allah's Cause"},
    "b_ghadd": {"ar": "غَضُّ الْبَصَرِ", "en": "Lowering the Gaze"},
    "b_farj": {"ar": "حِفْظُ الْفَرْجِ", "en": "Guarding Chastity"},
    "b_kadhib": {"ar": "تَرْكُ الْكَذِبِ", "en": "Abandoning Lying"},
    "b_ghiba": {"ar": "تَرْكُ الْغِيبَةِ وَالنَّمِيمَةِ", "en": "Avoiding Backbiting & Slander"},
    "b_zulm": {"ar": "تَرْكُ الظُّلْمِ", "en": "Abandoning Injustice"},
    "b_riba": {"ar": "تَرْكُ الرِّبَا وَالْغِشِّ", "en": "Avoiding Usury & Fraud"},
}

# =============================================
# LANGUAGE INITIALIZATION
# =============================================
if "lang" not in st.session_state: st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(key):
    """Retrieve translated text for the given key based on current language."""
    return T.get(key, {}).get(LANG, key)

# =============================================
# COSMIC SIMULATION ENGINE
# =============================================
def cosmic_engine(W0, B0, E0, years=200, lag=25):
    """Simulates the Mizan dynamics: S = W × B with delayed Istidraj effect."""
    W = np.zeros(years); B = np.zeros(years); S = np.zeros(years); E = np.zeros(years)
    W[0], B[0], E[0] = W0, B0, E0; S[0] = W0 * B0
    for t in range(1, years):
        # The Collapse Loop: Empowerment erodes Loyalty and Disavowal
        W[t] = max(0.01, min(1.0, W[t-1] - 0.05 * E[t-1]))
        B[t] = max(0.01, min(1.0, B[t-1] - 0.04 * E[t-1]))
        # The Stability Equation
        S[t] = W[t] * B[t]
        # The Recovery/Istidraj Loop: Empowerment lags behind Stability
        past_idx = t - lag
        S_past = S[past_idx] if past_idx >= 0 else S[t]
        E[t] = max(0.01, min(1.0, E[t-1] + 0.05 * (S_past - E[t-1])))
    return W, B, S, E

def get_mizan_color(w, b):
    """Returns a color based on the (W, B) quadrant."""
    if w >= 0.7 and b >= 0.7: return '#FFD700'   # Believer (Gold)
    elif w >= 0.5 and b < 0.4: return '#E0E0E0'   # Weak Disavowal (Gray)
    elif w < 0.4 and b >= 0.5: return '#FF5252'   # Weak Loyalty (Red)
    elif w < 0.4 and b < 0.4: return '#FFB6C1'    # Hypocrite (Pink)
    else: return '#888888'                         # Average

# =============================================
# SUPER ADVISOR (AI-Powered with Local Fallback)
# =============================================
def get_super_advisor_response(user_query, lang="ar"):
    """Attempts to use GPT-4o, falls back to a local knowledge base."""
    # 1. Try using OpenAI's GPT-4o if API key is available
    try:
        import openai
        client = openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        if st.secrets.get("OPENAI_API_KEY"):
            system_prompt = "You are the Super Advisor of The Mizan Theory by Ali Adel Alatifi. Core equation: S = W × B. Istidraj: E lags S."
            response = client.chat.completions.create(
                model="gpt-4o", temperature=0.7, max_tokens=800,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            return response.choices[0].message.content
    except:
        pass

    # 2. Local fallback knowledge base
    q = user_query.lower()
    if "istidraj" in q or "استدراج" in q:
        return {
            "ar": "الِاسْتِدْرَاجُ: التَّمْكِينُ (E) يَتَأَخَّرُ فِي الِانْهِيَارِ عَنِ الثَّبَاتِ (S)، ثُمَّ يَنْهَارُ فَجْأَةً. ﴿فَلَمَّا نَسُوا... أَخَذْنَاهُم بَغْتَةً﴾ [الأنعام: 44].",
            "en": "Istidraj: Material empowerment (E) lags behind moral stability (S) and collapses suddenly. {So when they forgot... We seized them suddenly} [Al-An'am:44]."
        }.get(lang, "")
    if "mizan" in q or "ميزان" in q:
        return {
            "ar": "مُعَادَلَةُ الْمِيزَانِ: S = W × B. ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256].",
            "en": "The Mizan Equation: S = W × B. {Whoever disbelieves in false deities and believes in Allah has grasped the firm handhold} [Al-Baqarah:256]."
        }.get(lang, "")
    return {
        "ar": "لَمْ أَجِدْ إِجَابَةً. جَرِّبِ السُّؤَالَ عَنِ: الِاسْتِدْرَاجِ، أَوِ الْمِيزَانِ.",
        "en": "I couldn't find a specific answer. Try asking about Istidraj or Mizan."
    }.get(lang, "")

# =============================================
# 🏠 WELCOME SCREEN
# =============================================
if 'entered' not in st.session_state:
    st.session_state.entered = False

if not st.session_state.entered:
    # Display the fully translated welcome page
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
        index=0 if LANG == "ar" else 1
    )
    new_lang = "ar" if "العربية" in lang_option else "en"
    if new_lang != LANG:
        st.session_state.lang = new_lang
        st.rerun()
    
    st.markdown("---")
    
    # Global Mizan Parameters
    W_global = st.slider(t('param_w'), 0.0, 1.0, 0.7, 0.05)
    B_global = st.slider(t('param_b'), 0.0, 1.0, 0.6, 0.05)
    E_global = st.slider(t('param_e'), 0.0, 1.0, 0.3, 0.05)
    lag_global = st.slider(t('param_lag'), 5, 50, 22, 1)
    
    st.markdown("---")
    st.markdown(f"*{t('footer')}*")

# =============================================
# 🗂️ MAIN TABS
# =============================================
tabs = st.tabs([t('tab_believe'), t('tab_advisor'), t('tab_observe'), t('tab_judge'), t('tab_understand')])

# =============================================
# TAB 0: COMMAND CENTER
# =============================================
with tabs[0]:
    st.header(t("command_center_title"))
    W_s, B_s, S_s, E_s = cosmic_engine(W_global, B_global, E_global, 200, lag_global)
    
    # Dashboard Metrics
    st.subheader(t('dashboard'))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🤍 W", f"{W_global:.2f}")
    c2.metric("❤️ B", f"{B_global:.2f}")
    c3.metric("⚖️ S", f"{W_global * B_global:.2f}")
    c4.metric("💫 E", f"{E_global:.2f}")
    
    st.markdown("---")
    # Civilization Cycle Chart
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    ax.plot(S_s, 'g-', linewidth=2, label='S')
    ax.plot(E_s, 'b--', linewidth=2, label='E')
    ax.set_title(t("cycle_title"), color='white')
    ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
    ax.grid(True, alpha=0.2); ax.set_ylim(0, 1.05); ax.tick_params(colors='white')
    st.pyplot(fig)

# =============================================
# TAB 1: SUPER ADVISOR
# =============================================
with tabs[1]:
    st.header(t('advisor_title'))
    st.markdown(t('advisor_subtitle'))
    
    user_q = st.text_input("✍️ " + ("سُؤَالُكَ:" if LANG == "ar" else "Your question:"), placeholder=t('ask_placeholder'))
    
    if user_q:
        with st.spinner(t('analyzing')):
            answer = get_super_advisor_response(user_q, LANG)
            st.markdown("### 💡 " + ("الْجَوَابُ:" if LANG == "ar" else "Answer:"))
            st.markdown(answer)
            
            # Run a contextual simulation
            w0, b0, e0 = (0.3, 0.3, 0.9) if "istidraj" in user_q.lower() or "استدراج" in user_q.lower() else (0.7, 0.6, 0.3)
            W_sim, B_sim, S_sim, E_sim = cosmic_engine(w0, b0, e0, 100, lag_global)
            
            st.markdown(t('simulation_note'))
            fig, ax = plt.subplots(figsize=(10, 3), facecolor='#0a0a1a')
            ax.set_facecolor('#0a0a1a')
            ax.plot(S_sim, 'g-', linewidth=2, label='S')
            ax.plot(E_sim, 'b--', linewidth=2, label='E')
            ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
            ax.grid(True, alpha=0.2); ax.set_ylim(0, 1.05); ax.tick_params(colors='white')
            st.pyplot(fig)

# =============================================
# TAB 2: PERSONAL LAB (LOYALTY & DISAVOWAL)
# =============================================
with tabs[2]:
    st.header(t('personal_title'))
    st.markdown(t('personal_subtitle'))
    st.markdown("---")

    # --- LOYALTY BOOSTERS (W) ---
    st.subheader(t('w_group_label'))
    st.caption("Score each factor from 0 to 10 (The firmest handhold of faith is love for Allah's sake)")

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        w_shahada = st.slider(t("w_shahada"), 0, 10, 8, 1)
        w_salat = st.slider(t("w_salat"), 0, 10, 7, 1)
        w_zakat = st.slider(t("w_zakat"), 0, 10, 6, 1)
        w_sawm = st.slider(t("w_sawm"), 0, 10, 7, 1)
        w_hajj = st.slider(t("w_hajj"), 0, 10, 5, 1)
        w_quran = st.slider(t("w_quran"), 0, 10, 6, 1)
    with col_w2:
        w_dhikr = st.slider(t("w_dhikr"), 0, 10, 7, 1)
        w_tawakkul = st.slider(t("w_tawakkul"), 0, 10, 8, 1)
        w_hubb = st.slider(t("w_hubb"), 0, 10, 9, 1)
        w_birr = st.slider(t("w_birr"), 0, 10, 8, 1)
        w_ihsan = st.slider(t("w_ihsan"), 0, 10, 8, 1)
        w_taawun = st.slider(t("w_taawun"), 0, 10, 7, 1)

    # --- DISAVOWAL BOOSTERS (B) ---
    st.subheader(t('b_group_label'))
    st.caption("Score each factor from 0 to 10 (The firmest handhold of faith is hatred for Allah's sake)")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        b_taghut = st.slider(t("b_taghut"), 0, 10, 9, 1)
        b_shirk = st.slider(t("b_shirk"), 0, 10, 9, 1)
        b_kufr = st.slider(t("b_kufr"), 0, 10, 8, 1)
        b_nifaq = st.slider(t("b_nifaq"), 0, 10, 8, 1)
        b_amr = st.slider(t("b_amr"), 0, 10, 7, 1)
        b_nahy = st.slider(t("b_nahy"), 0, 10, 7, 1)
        b_jihad_nafs = st.slider(t("b_jihad_nafs"), 0, 10, 9, 1)
    with col_b2:
        b_jihad = st.slider(t("b_jihad"), 0, 10, 7, 1)
        b_ghadd = st.slider(t("b_ghadd"), 0, 10, 8, 1)
        b_farj = st.slider(t("b_farj"), 0, 10, 9, 1)
        b_kadhib = st.slider(t("b_kadhib"), 0, 10, 9, 1)
        b_ghiba = st.slider(t("b_ghiba"), 0, 10, 8, 1)
        b_zulm = st.slider(t("b_zulm"), 0, 10, 9, 1)
        b_riba = st.slider(t("b_riba"), 0, 10, 9, 1)

    # --- CALCULATE RESULT ---
    W_list = [w_shahada, w_salat, w_zakat, w_sawm, w_hajj, w_quran, w_dhikr, w_tawakkul, w_hubb, w_birr, w_ihsan, w_taawun]
    B_list = [b_taghut, b_shirk, b_kufr, b_nifaq, b_amr, b_nahy, b_jihad_nafs, b_jihad, b_ghadd, b_farj, b_kadhib, b_ghiba, b_zulm, b_riba]
    
    W_personal = sum(W_list) / (12 * 10)
    B_personal = sum(B_list) / (14 * 10)
    S_personal = W_personal * B_personal

    st.markdown("---")
    st.subheader(t("result_title"))
    
    col1, col2, col3 = st.columns(3)
    col1.metric(t('result_w'), f"{W_personal:.2f}")
    col2.metric(t('result_b'), f"{B_personal:.2f}")
    col3.metric(t('result_s'), f"{S_personal:.2f}")
    
    if S_personal > 0.7:
        st.success(t('safe_zone'))
    elif S_personal > 0.4:
        st.warning(t('warning_zone'))
    else:
        st.error(t('danger_zone'))
    
    # Quadrant Map
    st.markdown("---")
    st.caption(t("map_caption"))
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    ax.axhline(0.5, color='gray', ls=':', lw=1)
    ax.axvline(0.5, color='gray', ls=':', lw=1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel('B (Disavowal)' if LANG == "en" else 'B (الْبَرَاءَةُ)', color='white')
    ax.set_ylabel('W (Loyalty)' if LANG == "en" else 'W (الْوَلَاءُ)', color='white')
    ax.scatter(B_personal, W_personal, s=400, c='cyan', edgecolors='white', linewidth=3, zorder=10)
    ax.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green')
    ax.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='orange')
    ax.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='blue')
    ax.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='red')
    ax.text(0.75, 0.75, t("quadrant_labels")["believer"], color='green', fontsize=12, ha='center', fontweight='bold')
    ax.text(0.25, 0.75, t("quadrant_labels")["harsh"], color='orange', fontsize=12, ha='center', fontweight='bold')
    ax.text(0.25, 0.25, t("quadrant_labels")["hypocrite"], color='red', fontsize=12, ha='center', fontweight='bold')
    ax.text(0.75, 0.25, t("quadrant_labels")["weak"], color='blue', fontsize=12, ha='center', fontweight='bold')
    ax.grid(True, alpha=0.2); ax.tick_params(colors='white')
    st.pyplot(fig)

# =============================================
# TAB 3: NATIONS CLASH SIMULATOR
# =============================================
with tabs[3]:
    st.header(t("nations_board_title"))
    
    nations = {
        ("أُمَّةُ الْإِيمَانِ" if LANG == "ar" else "Nation of Faith"): (0.9, 0.9, 0.1, "gold"),
        ("أُمَّةُ التَّرَفِ" if LANG == "ar" else "Nation of Luxury"): (0.3, 0.2, 0.9, "orange"),
        ("الإِمْبِرَاطُورِيَّةُ الظَّالِمَةُ" if LANG == "ar" else "The Tyrant Empire"): (0.1, 0.9, 0.8, "red"),
        ("أُمَّةُ الْعِلْمِ" if LANG == "ar" else "Nation of Knowledge"): (0.8, 0.6, 0.4, "cyan"),
    }
    
    if st.button(t('launch_clash'), use_container_width=True, type="primary"):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='#000010')
        for i, (name, (w0, b0, e0, col)) in enumerate(nations.items()):
            ax = axes[i // 2, i % 2]; ax.set_facecolor('#0a0a1a')
            W_s, B_s, S_s, E_s = cosmic_engine(w0, b0, e0, 200, lag_global)
            ax.plot(S_s, color=col, linewidth=2, label='S')
            ax.plot(E_s, color=col, linestyle='--', alpha=0.6, label='E')
            ax.set_title(name, color=col, fontweight='bold')
            ax.set_ylim(0, 1.05); ax.grid(True, alpha=0.2)
            ax.tick_params(colors='white'); ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=8)
        plt.tight_layout(); st.pyplot(fig); st.success(t('clash_success'))

# =============================================
# TAB 4: LIBRARY & GEOMETRIC LEXICON
# =============================================
with tabs[4]:
    st.header(t('library_title'))
    
    with st.expander(t("summary_title"), expanded=True):
        st.markdown(f"""
        - **{('الدِّينُ الْقَيِّمُ' if LANG == 'ar' else 'Al-Deen Al-Qayyim')}**: {('قَانُونُ السَّبَبِيَّةِ الْكَوْنِيِّ.' if LANG == 'ar' else 'The cosmic law of causality.')}
        - **{('الْإِسْلَامُ الْحَنِيفُ' if LANG == 'ar' else 'Al-Islam Al-Hanif')}**: {('الِاسْتِجَابَةُ الدِّينَامِيكِيَّةُ.' if LANG == 'ar' else 'The dynamic response.')}
        - **{('مُعَادَلَةُ الثَّبَاتِ' if LANG == 'ar' else 'Stability Equation')}**: `S = W × B`
        - **W**: {('الْوَلَاءُ لِلهِ (الْحُبُّ، الطَّاعَةُ، النُّصْرَةُ).' if LANG == 'ar' else 'Loyalty to God (Love, Obedience, Support).')}
        - **B**: {('الْبَرَاءَةُ مِنَ الطَّاغُوتِ (الْبُغْضُ، الْمُفَاصَلَةُ، الْمُنَاعَةُ).' if LANG == 'ar' else 'Disavowal of False Deities (Hatred, Disassociation, Immunity).')}
        """)
    
    with st.expander(t("lexicon_title"), expanded=False):
        tools = {
            "فَاءُ السَّبَبِيَّةِ (فَـ)": ("=", {"ar": "تَرْبِطُ السَّبَبَ بِالنَّتِيجَةِ حَتْمًا.", "en": "Inevitably connects cause to effect."}),
            "لَامُ التَّعْلِيلِ (لِـ)": ("→", {"ar": "سَهْمُ الْغَايَةِ.", "en": "Arrow of purpose."}),
            "حَتَّى الْغَائِيَّةِ": ("...", {"ar": "اسْتِمْرَارُ السَّبَبِ حَتَّى النَّتِيجَةِ.", "en": "Continuation of cause until result."}),
            "إِلَّا": ("{}", {"ar": "حُدُودُ الْمَجْمُوعَةِ.", "en": "Boundaries of the set."}),
        }
        sel = st.selectbox(t('select_tool'), list(tools.keys()))
        if sel:
            st.metric("الرَّمْزُ" if LANG == "ar" else "Symbol", tools[sel][0])
            st.info(tools[sel][1][LANG])

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#666;'>{t('footer')}</p>", unsafe_allow_html=True)
