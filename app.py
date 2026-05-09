import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
from matplotlib.lines import Line2D
import random
import time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(page_title="الْمَنْصَةُ الذَّهَبِيَّةُ – The Golden Platform", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# =============================================
# DIVINE CONSTANTS – ABJAD VALUES (حساب الجمل)
# =============================================
ABJAD = {
    'أ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

# Core Divine Constants (الثوابت الإلهية)
QAF = 100    # الميزان – The Balance
NOON = 50    # النور – The Light
SAD = 90     # الصمد – The Eternal
KAF = 20     # الأمر – The Command (كُن)
ALIF = 1     # الوحدانية – The Oneness
LAM = 30     # المُلك – The Sovereignty
MEEM = 40    # الجمع – The Gathering
RA = 200     # اليقظة – The Vigilance
HA = 5       # الهوية – The Identity
YA = 10      # الاستجابة – The Response
AYN = 70     # الإدراك – The Perception
SEEN = 60    # السمع – The Hearing
HA_L = 8     # الحياة – The Life
TA = 9       # الطهارة – The Purity

# The Fundamental Equation Constants (from Quran 2:256)
# فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ
KFR_BIL_TAGHUT = 1  # B (Disavowal) – الكفر بالطاغوت
IMAN_BILLAH = 1     # W (Loyalty) – الإيمان بالله
URWA_WUTHQA = 1     # S (Stability) – العروة الوثقى

# =============================================
# THE GRAND UNIFIED EQUATION (S = W × B)
# With Exponential and Logarithmic Dynamics
# =============================================
def compute_S(W_val, B_val, Q=QAF, N=NOON, S=SAD, K=KAF, lag=25):
    """
    The Grand Unified Equation of Existential Stability.
    S = W × B  (multiplicative, not additive)
    Enhanced with divine constants and exponential/logarithmic dynamics.
    """
    # Base equation: S = W × B (the firm handhold)
    S_base = W_val * B_val
    
    # Divine amplification: The stronger the light (N), the more stability
    # S_final = S_base × (N/50)^(K/20) × e^(Q/100)
    divine_amplifier = (N / 50.0) ** (K / 20.0) * np.exp(Q / 100.0 - 1)
    
    # The Istidraj Factor (lag effect)
    # ΔE = α (S_past - E_present)
    # This creates the deceptive gap where E lags behind S
    istidraj_factor = 1.0  # Will be applied in the dynamic simulation
    
    S_final = S_base * divine_amplifier * istidraj_factor
    
    return np.clip(S_final, 0.001, 1.0)

# =============================================
# THE COSMIC SIMULATION ENGINE
# (Dynamic System of Differential Equations)
# =============================================
def cosmic_engine(W0, B0, E0, years=200, lag=25):
    """
    Simulates the Mizan dynamics as a system of coupled differential equations.
    
    dW/dt = -α₁·E + α₂·H - α₃·(1-B)
    dB/dt = -β₁·E + β₂·W·(1-W)·(1-B)
    dE/dt = γ·(S(t-lag) - E)
    
    where H (Hardship) = 10 / (S + 0.1)
    """
    W = np.zeros(years)
    B = np.zeros(years)
    S = np.zeros(years)
    E = np.zeros(years)
    
    W[0], B[0], E[0] = W0, B0, E0
    S[0] = compute_S(W0, B0, QAF, NOON, SAD, KAF)
    
    for t in range(1, years):
        # Hardship awakens loyalty (Quran 2:155-157)
        H_t = 10.0 / (S[t-1] + 0.1)
        
        # --- DIFFERENTIAL EQUATIONS ---
        # dW/dt: Loyalty changes due to hardship, empowerment, and disavowal
        dW = (0.08 * H_t) - (0.05 * E[t-1]) - (0.04 * (1 - B[t-1]))
        
        # dB/dt: Disavowal changes due to empowerment and self-regeneration
        dB = (-0.04 * E[t-1]) + (0.01 * (1 - B[t-1]) * W[t-1] * (1 - W[t-1]))
        
        # Update W and B with clipping
        W[t] = max(0.01, min(1.0, W[t-1] + dW))
        B[t] = max(0.01, min(1.0, B[t-1] + dB))
        
        # Compute S with divine constants
        S[t] = compute_S(W[t], B[t], QAF, NOON, SAD, KAF)
        
        # --- ISTIDRAJ (LAG EFFECT) ---
        # Empowerment (E) follows past stability, not current stability
        # E(t) = E(t-1) + γ × (S(t-lag) - E(t-1))
        past_idx = max(0, t - lag)
        S_past = S[past_idx]
        dE = 0.05 * (S_past - E[t-1])
        E[t] = max(0.01, min(1.0, E[t-1] + dE))
    
    return W, B, S, E

# =============================================
# THE FOUR QUADRANTS CLASSIFICATION
# Based on: W (Loyalty) and B (Disavowal)
# =============================================
def classify_human(W_val, B_val):
    """
    Classifies a human being into one of four Quranic categories:
    - Believer (مؤمن): +W, +B → S = +1
    - Disbeliever (كافر): -W, +B → S = -1
    - Hypocrite (منافق): ~0, ~0 → S = 0
    - Polytheist (مشرك): +W, -B → S = -1
    """
    if W_val >= 0.5 and B_val >= 0.5:
        return "believer", '#FFD700'
    elif W_val < 0.4 and B_val >= 0.5:
        return "disbeliever", '#FF5252'
    elif W_val < 0.4 and B_val < 0.4:
        return "hypocrite", '#FFB6C1'
    elif W_val >= 0.5 and B_val < 0.4:
        return "polytheist", '#FFA07A'
    else:
        return "borderline", '#888888'

# =============================================
# THE GEOMETRIC CURVATURE (الهندسة التفاضلية)
# =============================================
def compute_path_curvature(S_values, W_values, B_values):
    """
    Computes the curvature of the path in (W, B) space.
    The Straight Path (الصراط المستقيم) has curvature = 0.
    Deviation (المعصية) increases curvature.
    Repentance (التوبة) reduces curvature.
    """
    if len(S_values) < 3:
        return 0.0
    
    # Curvature κ = |W'B'' - B'W''| / (W'² + B'²)^(3/2)
    dW = np.gradient(W_values)
    dB = np.gradient(B_values)
    ddW = np.gradient(dW)
    ddB = np.gradient(dB)
    
    last = -1
    numerator = abs(dW[last] * ddB[last] - dB[last] * ddW[last])
    denominator = (dW[last]**2 + dB[last]**2)**(1.5)
    
    if denominator > 1e-6:
        return numerator / denominator
    
    return 0.0

# =============================================
# LANGUAGE & SESSION STATE
# =============================================
if 'entered' not in st.session_state: st.session_state.entered = False
if "lang" not in st.session_state: st.session_state.lang = "ar"
if "compass_answers" not in st.session_state: st.session_state.compass_answers = {}
LANG = st.session_state.lang

# =============================================
# TRANSLATION DICTIONARY
# =============================================
T = {
    "welcome_html": {
        "ar": """<div style="direction: rtl; text-align: center; background: linear-gradient(180deg, #000000 0%, #0a1a0a 30%, #1a2e1a 70%, #0a1a0a 100%); padding: 40px 20px; border-radius: 25px; border: 3px solid #FFD700; margin: 30px 0; box-shadow: 0 0 60px rgba(255, 215, 0, 0.7);"><span style="font-size: 70px; display: block;">⚖️</span><h1 style="color: #FFD700; font-size: 2.5em; margin: 15px 0; font-weight: 900;">الْمَنْصَةُ الذَّهَبِيَّةُ</h1><span style="font-size: 50px; display: block;">🧪</span><h2 style="color: #FFD700; font-size: 1.5em; margin: 10px 0;">مُخْتَبَرُ نَظَرِيَّةِ الْمِيزَان</h2><p style="color: #e0e0e0; font-size: 1.2em; margin: 30px 10px; line-height: 2.2; font-style: italic;">"هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟<br>هَذَا هُوَ نَمُوذَجُ الْمِيزَانِ الَّذِي يُثْبِتُ أَنَّ <b style="color: #FFD700;">S = W × B</b>"</p><p style="color: #FFD700; font-size: 1.5em; margin: 30px 0 0 0; font-weight: bold;">علي عادل العاطفي</p><p style="color: #FFD700; font-size: 1em; margin: 5px 0 0 0; font-style: italic; opacity: 0.8;">Ali Adel Alatifi | 2026</p></div>""",
        "en": """<div style="text-align: center; background: linear-gradient(180deg, #000000 0%, #0a0a1a 30%, #0d0d2b 70%, #000000 100%); padding: 40px 20px; border-radius: 25px; border: 3px solid #FFD700; margin: 30px 0; box-shadow: 0 0 60px rgba(255, 215, 0, 0.7);"><span style="font-size: 70px; display: block;">⚖️</span><h1 style="color: #FFD700; font-size: 2.5em; margin: 15px 0; font-weight: 900;">THE GOLDEN PLATFORM</h1><span style="font-size: 50px; display: block;">🧪</span><h2 style="color: #FFD700; font-size: 1.5em; margin: 10px 0;">The Mizan Theory Lab</h2><p style="color: #e0e0e0; font-size: 1.2em; margin: 30px 10px; line-height: 2.2; font-style: italic;">"Is there a single law governing the atom and civilization?<br>This is the Mizan Model that proves <b style="color: #FFD700;">S = W × B</b>"</p><p style="color: #FFD700; font-size: 1.5em; margin: 30px 0 0 0; font-weight: bold;">Ali Adel Alatifi</p><p style="color: #FFD700; font-size: 1em; margin: 5px 0 0 0; font-style: italic; opacity: 0.8;">2026</p></div>"""
    },
    "enter_lab": {"ar": "🚀 ادْخُلْ إِلَى الْمُخْتَبَرِ", "en": "🚀 Enter the Lab"},
    "tab_equation": {"ar": "⚖️ الْمُعَادَلَة", "en": "⚖️ The Equation"},
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
    "divine_constants": {"ar": "🔮 الثَّوَابِتُ الْإِلَهِيَّةُ", "en": "🔮 Divine Constants"},
    "param_qaf": {"ar": "ق (الْمِيزَانُ)", "en": "Qaf (The Balance)"},
    "param_noon": {"ar": "ن (النُّورُ)", "en": "Noon (The Light)"},
    "param_sad": {"ar": "ص (الصَّمَدُ)", "en": "Sad (The Eternal)"},
    "param_kaf": {"ar": "ك (الْأَمْرُ)", "en": "Kaf (The Command)"},
    "dashboard": {"ar": "لَوْحَةُ الْمُؤَشِّرَاتِ", "en": "Dashboard"},
    "footer": {"ar": "© 2026 علي عادل العاطفي | الْمَنْصَةُ الذَّهَبِيَّةُ", "en": "© 2026 Ali Adel Alatifi | The Golden Platform"},
    "lang_selector": {"ar": "اللُّغَةُ", "en": "Language"},
    "equation_title": {"ar": "⚖️ مُعَادَلَةُ الثَّبَاتِ الْوُجُودِيِّ", "en": "⚖️ The Existential Stability Equation"},
    "equation_desc": {"ar": "اِسْتِنَادًا إِلَى قَوْلِهِ تَعَالَى: ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256] وَقَوْلِهِ ﷺ: «الْحُبُّ فِي اللَّهِ وَالْبُغْضُ فِي اللَّهِ أَوْثَقُ عُرَى الْإِيمَانِ».", "en": "Based on: {Whoever disbelieves in false deities and believes in Allah has grasped the firm handhold} [2:256] and the Hadith: «Loving for Allah's sake and hating for Allah's sake is the firmest handhold of faith.»"},
    "equation_formula": {"ar": "S = W × B × (ن/50)^(ك/20) × e^(ق/100 - 1)", "en": "S = W × B × (N/50)^(K/20) × e^(Q/100 - 1)"},
    "active_constants": {"ar": "الثَّوَابِتُ النَّشِطَةُ حَالِيًّا:", "en": "Currently Active Constants:"},
    "curvature_title": {"ar": "📐 هَنْدَسَةُ الصِّرَاطِ الْمُسْتَقِيمِ", "en": "📐 Geometry of the Straight Path"},
    "curvature_desc": {"ar": "اِنْحِنَاءُ الْمَسَارِ (∇ᵧ̇ᵧ̇). الصِّرَاطُ الْمُسْتَقِيمُ: اِنْحِنَاؤُهُ = 0. الْمَعْصِيَةُ تَزِيدُ الِانْحِنَاءَ. التَّوْبَةُ تُقَلِّلُهُ.", "en": "Path curvature (∇ᵧ̇ᵧ̇). The Straight Path: curvature = 0. Sin increases curvature. Repentance reduces it."},
}

def t(key, subkey=None):
    val = T.get(key, {}).get(LANG, key)
    if subkey and isinstance(val, dict):
        return val.get(LANG, subkey)
    return val

# =============================================
# SUPER ADVISOR
# =============================================
def get_super_advisor_response(user_query, lang="ar"):
    try:
        api_key = st.secrets.get("OPENROUTER_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
        if api_key:
            import requests
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "model": "openai/gpt-4o",
                "messages": [{"role": "system", "content": "You are the Super Advisor of The Mizan Theory by Ali Adel Alatifi. Core: S=W×B with divine constants Q=100, N=50, S=90, K=20. Istidraj: E lags S."}, {"role": "user", "content": user_query}],
                "temperature": 0.7, "max_tokens": 600
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=15)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
    except: pass
    q = user_query.lower()
    if "istidraj" in q or "استدراج" in q: return {"ar": "الِاسْتِدْرَاجُ: E يَتَأَخَّرُ عَنْ S ثُمَّ يَنْهَارُ فَجْأَةً. ﴿فَلَمَّا نَسُوا... أَخَذْنَاهُم بَغْتَةً﴾ [الأنعام:44].", "en": "Istidraj: E lags behind S then collapses suddenly. [Al-An'am:44]"}.get(lang, "")
    if "mizan" in q or "ميزان" in q: return {"ar": "S = W × B × (ن/50)^(ك/20) × e^(ق/100-1). ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾.", "en": "S = W × B × (N/50)^(K/20) × e^(Q/100-1). {Whoever disbelieves in false deities and believes in Allah has grasped the firm handhold}."}.get(lang, "")
    return {"ar": "لَمْ أَجِدْ إِجَابَةً. جَرِّبْ: الِاسْتِدْرَاج، الْمِيزَان.", "en": "Not found. Try: Istidraj, Mizan."}.get(lang, "")

# =============================================
# SOCIETY SIMULATION (AGENT-BASED)
# =============================================
def classify_agent(w, b):
    if w >= 0.5 and b >= 0.5: return "believer"
    elif w < 0.4 and b >= 0.5: return "disbeliever"
    elif w < 0.4 and b < 0.4: return "hypocrite"
    elif w >= 0.5 and b < 0.4: return "polytheist"
    else: return "average"

def get_agent_color(classification):
    return {"believer": '#FFD700', "disbeliever": '#FF5252', "hypocrite": '#FFB6C1', "polytheist": '#FFA07A', "average": '#888888'}.get(classification, '#888888')

def run_society_simulation(pop_size, influence_radius, years):
    np.random.seed(42)
    W = np.random.uniform(0.1, 0.9, pop_size); B = np.random.uniform(0.1, 0.9, pop_size)
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
            new_W[i] = max(0.01, min(1.0, new_W[i])); new_B[i] = max(0.01, min(1.0, new_B[i]))
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
            st.session_state.entered = True; st.rerun()
    st.stop()

# =============================================
# 🧭 SIDEBAR WITH DIVINE CONSTANTS
# =============================================
with st.sidebar:
    st.markdown(f"## {t('control_panel')}")
    
    # Language
    lang_option = st.selectbox(t('lang_selector'), ["🇸🇦 العربية", "🇬🇧 English"], index=0 if LANG == "ar" else 1)
    new_lang = "ar" if "العربية" in lang_option else "en"
    if new_lang != LANG: st.session_state.lang = new_lang; st.rerun()
    st.markdown("---")
    
    # Mizan Parameters
    st.subheader("⚙️ " + ("مُعَامَلَاتُ الْمِيزَانِ" if LANG == "ar" else "Mizan Parameters"))
    W_global = st.slider(t('param_w'), 0.0, 1.0, 0.7, 0.05)
    B_global = st.slider(t('param_b'), 0.0, 1.0, 0.6, 0.05)
    E_global = st.slider(t('param_e'), 0.0, 1.0, 0.3, 0.05)
    lag_global = st.slider(t('param_lag'), 5, 50, 22, 1)
    st.markdown("---")
    
    # Divine Constants
    st.subheader(t('divine_constants'))
    c1, c2 = st.columns(2)
    with c1:
        Q_global = st.slider(t('param_qaf'), 10, 200, 100, 10)
        N_global = st.slider(t('param_noon'), 5, 100, 50, 5)
    with c2:
        S_global = st.slider(t('param_sad'), 10, 200, 90, 10)
        K_global = st.slider(t('param_kaf'), 2, 50, 20, 2)
    
    st.markdown("---")
    st.markdown(f"<p style='text-align:center;color:#888;font-size:0.8em;'>{t('footer')}</p>", unsafe_allow_html=True)

# =============================================
# 🗂️ MAIN TABS
# =============================================
tab_labels = [
    t('tab_equation'), t('tab_advisor'), t('tab_observe'),
    t('tab_judge'), t('tab_society'), t('tab_history'),
    t('tab_heatmap'), t('tab_compass'), t('tab_library')
]
tabs = st.tabs(tab_labels)

# =============================================
# TAB 0: THE GRAND EQUATION
# =============================================
with tabs[0]:
    st.header(t("equation_title"))
    st.markdown(t("equation_desc"))
    st.markdown("---")
    
    # Show the equation in large format
    st.latex(r"S = W \times B \times \left(\frac{N}{50}\right)^{\frac{K}{20}} \times e^{\frac{Q}{100} - 1}")
    st.caption(t("equation_formula"))
    
    # Show active constants
    st.subheader(t("active_constants"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("ق (Qaf)", f"{Q_global}", "الميزان")
    c2.metric("ن (Noon)", f"{N_global}", "النور")
    c3.metric("ص (Sad)", f"{S_global}", "الصمد")
    c4.metric("ك (Kaf)", f"{K_global}", "الأمر")
    
    # Compute and show S with current values
    S_now = compute_S(W_global, B_global, Q_global, N_global, S_global, K_global)
    st.markdown("---")
    st.subheader("🧮 " + ("النَّتِيجَةُ الْآنِيَّةُ" if LANG == "ar" else "Current Result"))
    col1, col2, col3 = st.columns(3)
    col1.metric("W (الولاء)" if LANG == "ar" else "W (Loyalty)", f"{W_global:.3f}")
    col2.metric("B (البراءة)" if LANG == "ar" else "B (Disavowal)", f"{B_global:.3f}")
    col3.metric("S (الثبات)" if LANG == "ar" else "S (Stability)", f"{S_now:.4f}")
    
    # Run simulation to show dynamics
    W_s, B_s, S_s, E_s = cosmic_engine(W_global, B_global, E_global, 200, lag_global)
    
    st.markdown("---")
    st.subheader(t("curvature_title"))
    st.markdown(t("curvature_desc"))
    curvature = compute_path_curvature(S_s, W_s, B_s)
    st.metric("κ (الِانْحِنَاءُ)" if LANG == "ar" else "κ (Curvature)", f"{curvature:.4f}")
    
    # Civilization Cycle
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    ax.plot(S_s, 'g-', linewidth=2.5, label='S (Stability)' if LANG == "en" else 'S (الثَّبَاتُ)')
    ax.plot(E_s, 'b--', linewidth=2.5, label='E (Empowerment)' if LANG == "en" else 'E (التَّمْكِينُ)')
    max_S_idx = np.argmax(S_s); max_E_idx = np.argmax(E_s)
    if max_S_idx < max_E_idx:
        ax.axvspan(max_S_idx, max_E_idx, alpha=0.25, color='red', label=t('param_lag'))
    ax.set_title(t("equation_title"), color='white', fontsize=14, fontweight='bold')
    ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=10)
    ax.grid(True, alpha=0.2); ax.set_ylim(0, 1.05); ax.tick_params(colors='white')
    plt.tight_layout(); st.pyplot(fig)

# =============================================
# TAB 1: SUPER ADVISOR
# =============================================
with tabs[1]:
    st.header(t('advisor_title'))
    st.markdown(t('advisor_subtitle'))
    user_q = st.text_input("✍️ " + ("سُؤَالُكَ:" if LANG == "ar" else "Your question:"), placeholder="مِثَال: مَا هُوَ الِاسْتِدْرَاجُ؟" if LANG == "ar" else "E.g., What is Istidraj?")
    if user_q:
        with st.spinner(t('analyzing')):
            ans = get_super_advisor_response(user_q, LANG)
            st.markdown("### 💡 " + ("الْجَوَابُ:" if LANG == "ar" else "Answer:")); st.markdown(ans)
            w0, b0, e0 = (0.3, 0.3, 0.9) if "istidraj" in user_q.lower() or "استدراج" in user_q.lower() else (0.7, 0.6, 0.3)
            W_s, B_s, S_s, E_s = cosmic_engine(w0, b0, e0, 100, lag_global)
            fig, ax = plt.subplots(figsize=(10, 3), facecolor='#0a0a1a'); ax.set_facecolor('#0a0a1a')
            ax.plot(S_s, 'g-', label='S'); ax.plot(E_s, 'b--', label='E')
            ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white'); ax.grid(True, alpha=0.2)
            ax.set_ylim(0, 1.05); ax.tick_params(colors='white'); st.pyplot(fig)

# =============================================
# TAB 2: PERSONAL LAB (SIMPLIFIED – uses global W, B for now)
# =============================================
with tabs[2]:
    st.header(t('personal_title'))
    st.markdown(t('personal_subtitle'))
    human_type, human_color = classify_human(W_global, B_global)
    S_personal = compute_S(W_global, B_global, Q_global, N_global, S_global, K_global)
    
    c1, c2, c3 = st.columns(3)
    c1.metric(t('result_w'), f"{W_global:.2f}")
    c2.metric(t('result_b'), f"{B_global:.2f}")
    c3.metric(t('result_s'), f"{S_personal:.3f}")
    
    st.markdown(f"### " + ("تَصْنِيفُكَ:" if LANG == "ar" else "Your Classification:"))
    st.markdown(f"<h2 style='color:{human_color}; text-align:center;'>{human_type.upper()}</h2>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a1a'); ax.set_facecolor('#0a0a1a')
    ax.axhline(0.5, color='gray', ls=':', lw=1); ax.axvline(0.5, color='gray', ls=':', lw=1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel('B', color='white'); ax.set_ylabel('W', color='white')
    ax.scatter(B_global, W_global, s=400, c=human_color, edgecolors='white', linewidth=3)
    ax.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green')
    ax.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='red')
    ax.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='pink')
    ax.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='orange')
    for lbl, x, y, c in [("believer", 0.75, 0.75, 'green'), ("disbeliever", 0.25, 0.75, 'red'), ("hypocrite", 0.25, 0.25, 'pink'), ("polytheist", 0.75, 0.25, 'orange')]:
        ax.text(x, y, lbl.capitalize(), color=c, fontsize=10, ha='center', fontweight='bold')
    ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); st.pyplot(fig)

# =============================================
# TAB 3: NATIONS CLASH
# =============================================
with tabs[3]:
    st.header(t("nations_board_title"))
    nations = {
        "أُمَّةُ الْإِيمَانِ" if LANG == "ar" else "Faith": (0.9, 0.9, 0.1, "gold"),
        "أُمَّةُ التَّرَفِ" if LANG == "ar" else "Luxury": (0.3, 0.2, 0.9, "orange"),
        "الظَّالِمَةُ" if LANG == "ar" else "Tyrant": (0.1, 0.9, 0.8, "red"),
        "الْعِلْمِ" if LANG == "ar" else "Knowledge": (0.8, 0.6, 0.4, "cyan"),
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
# TAB 5: HISTORICAL LAB
# =============================================
with tabs[5]:
    st.header(t("history_title")); st.markdown(t("history_subtitle"))
    col1, col2 = st.columns(2)
    with col1: W_nat = st.slider("W " + ("الْأُمَّة" if LANG == "ar" else "Nation"), 0.0, 1.0, 0.9, 0.05)
    with col2: B_nat = st.slider("B " + ("الْأُمَّة" if LANG == "ar" else "Nation"), 0.0, 1.0, 0.8, 0.05)
    if st.button(t("run_history"), use_container_width=True, type="primary"):
        W_s, B_s, S_s, E_s = cosmic_engine(W_nat, B_nat, E_global, 300, lag_global)
        fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#0a0a1a')
        ax = axes[0]; ax.set_facecolor('#0a0a1a')
        ax.plot(S_s, 'g-', linewidth=2, label='S'); ax.plot(E_s, 'b--', linewidth=2, label='E')
        max_S = np.argmax(S_s); max_E = np.argmax(E_s)
        if max_S < max_E: ax.axvspan(max_S, max_E, alpha=0.2, color='red', label=t('param_lag'))
        collapse_year = next((t for t in range(max_S, len(E_s)) if E_s[t] < 0.3), None)
        if collapse_year: ax.axvline(x=collapse_year, color='red', linestyle='--', linewidth=2, label=f"{'Collapse' if LANG == 'en' else 'الِانْهِيَار'} ({collapse_year})")
        ax.set_title(t("cycle_title"), color='white'); ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2); ax.set_ylim(0, 1.05); ax.tick_params(colors='white')
        ax2 = axes[1]; ax2.set_facecolor('#0a0a1a')
        ax2.axhline(0.5, color='gray', ls=':', lw=1); ax2.axvline(0.5, color='gray', ls=':', lw=1)
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.set_xlabel('B', color='white'); ax2.set_ylabel('W', color='white')
        ax2.plot(B_s, W_s, 'w-', alpha=0.4, linewidth=0.8)
        ax2.scatter(B_s[0], W_s[0], s=100, c='green', edgecolors='white', linewidth=2); ax2.scatter(B_s[-1], W_s[-1], s=100, c='red', edgecolors='white', linewidth=2)
        ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
        plt.tight_layout(); st.pyplot(fig)

# =============================================
# TAB 6: HEATMAP
# =============================================
with tabs[6]:
    st.header(t("heatmap_title")); st.markdown(t("heatmap_subtitle"))
    if st.button(t("run_heatmap"), use_container_width=True, type="primary"):
        N = 1000; W = np.random.uniform(0, 1, N); B = np.random.uniform(0, 1, N); S = W * B
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a1a'); ax.set_facecolor('#0a0a1a')
        ax.scatter(B, W, c=S, cmap='RdYlGn', s=30, alpha=0.8, edgecolors='white', linewidths=0.2)
        ax.axhline(0.5, color='gray', ls=':', lw=1); ax.axvline(0.5, color='gray', ls=':', lw=1)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel('B', color='white'); ax.set_ylabel('W', color='white')
        ax.set_title('Mizan Heatmap' if LANG == "en" else 'خَرِيطَةُ حَرَارَةِ الْمِيزَانِ', color='white', fontsize=16, fontweight='bold')
        for lbl, x, y in [("believer", 0.75, 0.75), ("disbeliever", 0.25, 0.75), ("hypocrite", 0.25, 0.25), ("polytheist", 0.75, 0.25)]:
            ax.text(x, y, lbl.capitalize(), color='white', fontsize=10, ha='center', fontweight='bold')
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); st.pyplot(fig)

# =============================================
# TAB 7: COMPASS (Simplified)
# =============================================
with tabs[7]:
    st.header(t("compass_title")); st.markdown(t("compass_subtitle"))
    st.info("🚧 " + ("قَيْدَ الْبِنَاءِ – سَيَتَمُّ إِضَافَةُ 28 سُؤَالاً قَرِيبًا." if LANG == "ar" else "Under construction – 28 questions will be added soon."))

# =============================================
# TAB 8: LIBRARY
# =============================================
with tabs[8]:
    st.header(t('library_title'))
    with st.expander(t("summary_title"), expanded=True):
        st.markdown(f"""
        - **{('الدِّينُ الْقَيِّمُ' if LANG == 'ar' else 'Al-Deen Al-Qayyim')}**: {('قَانُونُ السَّبَبِيَّةِ الْكَوْنِيِّ.' if LANG == 'ar' else 'The cosmic law of causality.')}
        - **{('الْإِسْلَامُ الْحَنِيفُ' if LANG == 'ar' else 'Al-Islam Al-Hanif')}**: {('الِاسْتِجَابَةُ الدِّينَامِيكِيَّةُ.' if LANG == 'ar' else 'The dynamic response.')}
        - **{('مُعَادَلَةُ الثَّبَاتِ' if LANG == 'ar' else 'Stability Equation')}**: `S = W × B × (N/50)^(K/20) × e^(Q/100-1)`
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
