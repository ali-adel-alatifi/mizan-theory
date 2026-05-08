import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
import random
import time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# إعداد الصفحة
# =============================================
st.set_page_config(
    page_title="الْمَنْصَةُ الذَّهَبِيَّةُ – The Golden Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# 🌐 نظام الترجمة ثنائي اللغة
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

LANG = st.session_state.lang

T = {
    "platform_title": {"ar": "الْمَنْصَةُ الذَّهَبِيَّةُ", "en": "The Golden Platform"},
    "platform_subtitle": {"ar": "مُخْتَبَرُ نَظَرِيَّةِ الْمِيزَان", "en": "The Mizan Theory Lab"},
    "enter_lab": {"ar": "🚀 ادْخُلْ إِلَى الْمُخْتَبَرِ", "en": "🚀 Enter the Lab"},
    "welcome_quote": {
        "ar": '"هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟ هَذَا هُوَ نَمُوذَجُ الْمِيزَانِ الَّذِي يُثْبِتُ أَنَّ S = W × B"',
        "en": '"Is there a single law governing the atom and civilization? This is the Mizan Model that proves S = W × B"'
    },
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
    "metric_w_label": {"ar": "🤍 W", "en": "🤍 W"},
    "metric_b_label": {"ar": "❤️ B", "en": "❤️ B"},
    "metric_s_label": {"ar": "⚖️ S", "en": "⚖️ S"},
    "metric_e_label": {"ar": "💫 E", "en": "💫 E"},
    "footer": {"ar": "© 2026 علي عادل العاطفي | الْمَنْصَةُ الذَّهَبِيَّةُ", "en": "© 2026 Ali Adel Alatifi | The Golden Platform"},
    "language_selector": {"ar": "اللُّغَةُ", "en": "Language"},
    "advisor_title": {"ar": "🧠 الْمُسْتَشَارُ الْفَائِقُ", "en": "🧠 The Super Advisor"},
    "advisor_subtitle": {"ar": "اسْأَلْ عَنْ أَيِّ شَيْءٍ فِي نَظَرِيَّةِ الْمِيزَانِ. الْمُسْتَشَارُ يَعْتَمِدُ عَلَى الذَّكَاءِ الِاصْطِنَاعِيِّ.", "en": "Ask about anything in the Mizan Theory. The advisor uses AI."},
    "ask_placeholder": {"ar": "مِثَال: مَا هُوَ الِاسْتِدْرَاجُ؟", "en": "E.g., What is Istidraj?"},
    "analyzing": {"ar": "🧠 الْمُسْتَشَارُ يُحَلِّلُ...", "en": "🧠 Analyzing..."},
    "simulation_note": {"ar": "📊 تَمَّ تَشْغِيلُ مُحَاكَاةٍ حَيَّةٍ:", "en": "📊 Live simulation run:"},
    "launch_clash": {"ar": "🚀 أَطْلِقْ صِرَاعَ الْحَضَارَاتِ", "en": "🚀 Launch Clash"},
    "clash_success": {"ar": "الْبَقَاءُ لِلْأَقْوَى مِيزَانًا.", "en": "Survival of the fittest Mizan."},
    "personal_title": {"ar": "🧍 الْمُخْتَبَرُ الْفَرْدِيُّ", "en": "🧍 Personal Lab"},
    "personal_subtitle": {"ar": "اِكْتَشِفْ مِيزَانَكَ.", "en": "Discover your Mizan."},
    "library_title": {"ar": "📚 الْمَكْتَبَةُ", "en": "📚 Library"},
    "select_tool": {"ar": "اخْتَرْ أَدَاةً:", "en": "Select a tool:"},
}

def t(key):
    return T.get(key, {}).get(LANG, key)

# =============================================
# الدالة الأم: المُشغِّل الكوني
# =============================================
def cosmic_engine(W0, B0, E0, years=200, lag=25):
    W = np.zeros(years); B = np.zeros(years); S = np.zeros(years); E = np.zeros(years)
    W[0], B[0], E[0] = W0, B0, E0; S[0] = W0 * B0
    for t in range(1, years):
        W[t] = max(0.01, min(1.0, W[t-1] - 0.05 * E[t-1]))
        B[t] = max(0.01, min(1.0, B[t-1] - 0.04 * E[t-1]))
        S[t] = W[t] * B[t]
        past_idx = t - lag
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
# 🧠 الْمُسْتَشَارُ الْفَائِقُ (The Super Advisor)
# =============================================
def get_super_advisor_response(user_query, lang="ar"):
    """
    يستخدم GPT-4o للإجابة. إذا لم يتوفر المفتاح، يستخدم قاعدة المعرفة المحلية.
    """
    # رسالة النظام: خلاصة معرفتنا
    system_prompt = """
    You are the "Super Advisor" of "The Mizan Theory" by Ali Adel Alatifi.
    Core theory: The cosmic law of causality (Al-Deen Al-Qayyim) and the dynamic response (Al-Islam Al-Hanif).
    Equation: S = W × B (Stability = Loyalty × Disavowal).
    Istidraj: E (material empowerment) lags behind S (moral stability) and collapses suddenly.
    Applies to: Physics (gravity=W, repulsion=B), Biology (immune system: W=self, B=non-self), History (civilization cycles).
    Quranic classification: Believer (+W,+B), Disbeliever (-W,+B), Hypocrite (0,0), Polytheist (+W,-B).
    Answer based on this knowledge. Connect to the equation always.
    """
    
    # محاولة استخدام GPT-4o أولاً
    try:
        import openai
        client = openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        if st.secrets.get("OPENAI_API_KEY"):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
    except:
        pass
    
    # الرجوع إلى قاعدة المعرفة المحلية
    knowledge = {
        "istidraj": "Istidraj is a divine law where material empowerment (E) lags behind moral stability (S). When S collapses, E remains high for a period, deceiving people, then suddenly collapses. Quran: {So when they forgot that by which they had been reminded, We opened to them the doors of every good thing until, when they rejoiced, We seized them suddenly} [Al-An'am:44].",
        "mizan": "The Mizan Equation: S = W × B. Stability is achieved only by combining loyalty to God (W) and disavowal of false deities (B). The relationship is multiplicative: if either is zero, stability is null. Quran: {Whoever disbelieves in false deities and believes in Allah has grasped the firm handhold} [Al-Baqarah:256].",
        "fitrah": "Fitrah is the primordial nature, the original operating system. Quran: {The Fitrah of Allah upon which He created mankind} [Ar-Rum:30]. Prophet: 'Every child is born upon Fitrah.'",
        "ibrahim": "Prophet Abraham is the perfect model: W=1 (willing to sacrifice his son), B=1 (smashed idols, declared innocence). Result: Khaleel (intimate friend) and Imam (leader).",
    }
    
    query_lower = user_query.lower()
    for key, answer in knowledge.items():
        if key in query_lower:
            return answer
    
    return "I couldn't find a specific answer in my local knowledge base. For a more comprehensive answer, please configure the GPT-4o API key in the app secrets, or try asking about: Istidraj, Mizan, Fitrah, or Prophet Abraham."

# =============================================
# 🏠 واجهة الترحيب
# =============================================
if 'entered' not in st.session_state:
    st.session_state.entered = False

if not st.session_state.entered:
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(180deg, #000000 0%, #0a1a0a 30%, #1a2e1a 70%, #0a1a0a 100%); 
    padding: 40px 15px; border-radius: 20px; border: 3px solid #FFD700; margin: 30px 0;
    box-shadow: 0 0 50px rgba(255, 215, 0, 0.7);">
        <span style="font-size: 60px; display: block;">⚖️</span>
        <h1 style="color: #FFD700; font-size: 2em; margin: 15px 0; font-weight: 900;">
            {t('platform_title')}
        </h1>
        <span style="font-size: 40px; display: block;">🧪</span>
        <h2 style="color: #FFD700; font-size: 1.3em; margin: 10px 0;">{t('platform_subtitle')}</h2>
        <p style="color: #e0e0e0; font-size: 1em; margin: 20px 10px; line-height: 1.8; font-style: italic;">
            {t('welcome_quote')}
        </p>
        <p style="color: #FFD700; font-size: 1.2em; margin: 20px 0 0 0; font-weight: bold;">علي عادل العاطفي</p>
        <p style="color: #FFD700; font-size: 0.9em; margin: 5px 0 0 0; font-style: italic; opacity: 0.8;">Ali Adel Alatifi | 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(t('enter_lab'), use_container_width=True, type="primary"):
            st.session_state.entered = True
            st.rerun()
    st.stop()

# =============================================
# الشريط الجانبي
# =============================================
with st.sidebar:
    st.markdown(f"## {t('control_panel')}")
    
    lang_option = st.selectbox(
        t('language_selector'),
        options=["🇸🇦 العربية", "🇬🇧 English"],
        index=0 if LANG == "ar" else 1
    )
    new_lang = "ar" if "العربية" in lang_option else "en"
    if new_lang != LANG:
        st.session_state.lang = new_lang
        st.rerun()
    
    st.markdown("---")
    
    st.subheader("⚙️ " + ("مُعَامَلَاتُ الْمِيزَانِ" if LANG == "ar" else "Mizan Parameters"))
    W_global = st.slider(t('param_w'), 0.0, 1.0, 0.7, 0.05)
    B_global = st.slider(t('param_b'), 0.0, 1.0, 0.6, 0.05)
    E_global = st.slider(t('param_e'), 0.0, 1.0, 0.3, 0.05)
    lag_global = st.slider(t('param_lag'), 5, 50, 22, 1)
    
    st.markdown("---")
    st.markdown(f"*{t('footer')}*")

# =============================================
# الألسنة
# =============================================
tabs = st.tabs([t('tab_believe'), t('tab_advisor'), t('tab_observe'), t('tab_judge'), t('tab_understand')])

# --- تبويب 0: آمِن ---
with tabs[0]:
    st.header("🛡️ " + ("مَرْكَزُ الْقِيَادَةِ" if LANG == "ar" else "Command Center"))
    W_s, B_s, S_s, E_s = cosmic_engine(W_global, B_global, E_global, 200, lag_global)
    
    st.subheader(t('dashboard'))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t('metric_w_label'), f"{W_global:.2f}")
    col2.metric(t('metric_b_label'), f"{B_global:.2f}")
    col3.metric(t('metric_s_label'), f"{W_global * B_global:.2f}")
    col4.metric(t('metric_e_label'), f"{E_global:.2f}")
    
    st.markdown("---")
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    ax.plot(S_s, 'g-', linewidth=2, label='S')
    ax.plot(E_s, 'b--', linewidth=2, label='E')
    max_S_idx = np.argmax(S_s); max_E_idx = np.argmax(E_s)
    if max_S_idx < max_E_idx:
        ax.axvspan(max_S_idx, max_E_idx, alpha=0.3, color='red', label=f'Gap ({max_E_idx - max_S_idx}y)')
    ax.set_title('Civilization Cycle' if LANG == "en" else 'دَوْرَةُ الْحَضَارَةِ', color='white')
    ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
    ax.grid(True, alpha=0.2); ax.set_ylim(0, 1.05); ax.tick_params(colors='white')
    st.pyplot(fig)

# --- تبويب 1: المستشار الفائق ---
with tabs[1]:
    st.header(t('advisor_title'))
    st.markdown(t('advisor_subtitle'))
    
    user_q = st.text_input("✍️ " + ("سُؤَالُكَ:" if LANG == "ar" else "Your question:"), 
                           placeholder=t('ask_placeholder'))
    
    if user_q:
        with st.spinner(t('analyzing')):
            answer = get_super_advisor_response(user_q, LANG)
            st.markdown(f"### 💡 " + ("الْجَوَابُ:" if LANG == "ar" else "Answer:"))
            st.markdown(answer)
            
            # تشغيل محاكاة حية
            w0, b0, e0 = 0.7, 0.6, 0.3
            if "istidraj" in user_q.lower() or "استدراج" in user_q.lower():
                w0, b0, e0 = 0.3, 0.3, 0.9
            W_sim, B_sim, S_sim, E_sim = cosmic_engine(w0, b0, e0, 100, lag_global)
            
            st.markdown(t('simulation_note'))
            fig, ax = plt.subplots(figsize=(10, 3), facecolor='#0a0a1a')
            ax.set_facecolor('#0a0a1a')
            ax.plot(S_sim, 'g-', linewidth=2, label='S')
            ax.plot(E_sim, 'b--', linewidth=2, label='E')
            ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white')
            ax.grid(True, alpha=0.2); ax.set_ylim(0, 1.05); ax.tick_params(colors='white')
            st.pyplot(fig)

# --- تبويب 2: راقب ---
with tabs[2]:
    st.header(t('personal_title'))
    st.markdown(t('personal_subtitle'))
    c1, c2, c3 = st.columns(3)
    with c1:
        w1 = st.slider("الصَّلَاةُ" if LANG == "ar" else "Prayer", 0.0, 1.0, 0.8, 0.05)
        w2 = st.slider("بِرُّ الْوَالِدَيْنِ" if LANG == "ar" else "Parents", 0.0, 1.0, 0.8, 0.05)
    with c2:
        b1 = st.slider("غَضُّ الْبَصَرِ" if LANG == "ar" else "Lower Gaze", 0.0, 1.0, 0.7, 0.05)
        b2 = st.slider("اجْتِنَابُ الْغِيبَةِ" if LANG == "ar" else "No Backbiting", 0.0, 1.0, 0.6, 0.05)
    with c3:
        w3 = st.slider("الذِّكْرُ" if LANG == "ar" else "Dhikr", 0.0, 1.0, 0.6, 0.05)
        b3 = st.slider("الشُّبُهَاتُ" if LANG == "ar" else "Dubious", 0.0, 1.0, 0.9, 0.05)
    
    W_p = (w1+w2+w3)/3; B_p = (b1+b2+b3)/3; S_p = W_p * B_p
    col1, col2, col3 = st.columns(3)
    col1.metric("W", f"{W_p:.2f}"); col2.metric("B", f"{B_p:.2f}"); col3.metric("S", f"{S_p:.2f}")
    if S_p > 0.7: st.success("🟢 " + ("آمِن" if LANG == "ar" else "Safe"))
    elif S_p > 0.4: st.warning("🟡 " + ("هَشّ" if LANG == "ar" else "Fragile"))
    else: st.error("🔴 " + ("خَطَر" if LANG == "ar" else "Danger"))

# --- تبويب 3: احكم ---
with tabs[3]:
    st.header("🌍 " + ("لَوْحَةُ الْأُمَمِ" if LANG == "ar" else "Nations Board"))
    nations = {
        ("أُمَّةُ الْإِيمَانِ" if LANG == "ar" else "Faith"): (0.9, 0.9, 0.1, "gold"),
        ("أُمَّةُ التَّرَفِ" if LANG == "ar" else "Luxury"): (0.3, 0.2, 0.9, "orange"),
        ("الظَّالِمَةُ" if LANG == "ar" else "Tyrant"): (0.1, 0.9, 0.8, "red"),
        ("الْعِلْمِ" if LANG == "ar" else "Knowledge"): (0.8, 0.6, 0.4, "cyan"),
    }
    if st.button(t('launch_clash'), use_container_width=True, type="primary"):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='#000010')
        for idx, (name, (w0, b0, e0, col)) in enumerate(nations.items()):
            ax = axes[idx//2, idx%2]; ax.set_facecolor('#0a0a1a')
            W_s, B_s, S_s, E_s = cosmic_engine(w0, b0, e0, 200, lag_global)
            ax.plot(S_s, color=col, linewidth=2, label='S')
            ax.plot(E_s, color=col, linestyle='--', alpha=0.6, label='E')
            ax.set_title(name, color=col, fontweight='bold')
            ax.set_ylim(0, 1.05); ax.grid(True, alpha=0.2)
            ax.tick_params(colors='white'); ax.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=8)
        plt.tight_layout(); st.pyplot(fig)
        st.success(t('clash_success'))

# --- تبويب 4: افهم ---
with tabs[4]:
    st.header(t('library_title'))
    with st.expander("📜 " + ("خُلَاصَةُ النَّظَرِيَّةِ" if LANG == "ar" else "Theory Summary"), expanded=True):
        st.markdown(f"""
        **{('الدِّينُ الْقَيِّمُ' if LANG == 'ar' else 'The Upright Religion')}**: {('قَانُونُ السَّبَبِيَّةِ الْكَوْنِيِّ.' if LANG == 'ar' else 'The cosmic law of causality.')}
        **{('الْإِسْلَامُ الْحَنِيفُ' if LANG == 'ar' else 'The Upright Islam')}**: {('الِاسْتِجَابَةُ الدِّينَامِيكِيَّةُ.' if LANG == 'ar' else 'The dynamic response.')}
        **{('مُعَادَلَةُ الثَّبَاتِ' if LANG == 'ar' else 'Stability Equation')}**: `S = W × B`
        """)
    with st.expander("🔤 " + ("الْمُعْجَمُ الْهَنْدَسِيُّ" if LANG == "ar" else "Geometric Lexicon"), expanded=False):
        tools = {
            "فَاءُ السَّبَبِيَّةِ (فَـ)": ("=", "تَرْبِطُ السَّبَبَ بِالنَّتِيجَةِ حَتْمًا."),
            "لَامُ التَّعْلِيلِ (لِـ)": ("→", "سَهْمُ الْغَايَةِ."),
            "إِلَّا": ("{}", "حُدُودُ الْمَجْمُوعَةِ."),
        }
        sel = st.selectbox(t('select_tool'), list(tools.keys()))
        if sel:
            st.metric("الرَّمْزُ", tools[sel][0])
            st.info(tools[sel][1])

st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#666;'>{t('footer')}</p>", unsafe_allow_html=True)
