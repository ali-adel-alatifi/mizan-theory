# mizan/app.py
"""
المدخل الرئيسي لتطبيق مختبر الميزان
يدعم الترجمة الكاملة واتجاه RTL/LTR
التبويبات المتاحة حالياً: البوصلة، مختبر الأمة، المشهد الكوني، الشواهد، الصراط، المرصد، طبيب القلوب، شبكة الناجين، الجامعة، آل البيت
"""

import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from config import TXT, INDICATORS_META, N_IND
from components import (render_compass, render_nation_lab,
                        render_cosmic_scene, render_evidence,
                        render_path_geometry, render_new_observatory,
                        render_new_healer, render_new_network,
                        render_new_academy, render_new_ahlulbayt)
from ui_enhancements import apply_global_css, render_enhanced_sidebar, render_enhanced_header, render_enhanced_footer

# =============================================
# إعدادات الصفحة
# =============================================
st.set_page_config(
    page_title=TXT("⚖️ مختبر الميزان", "⚖️ The Mizan Lab"),
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# الأنماط CSS
# =============================================
apply_global_css()

# =============================================
# تهيئة متغيرات الجلسة
# =============================================
if 'init' not in st.session_state:
    st.session_state.lang = "ar"
    st.session_state.slider_values = {f"V{i}": 0.0 for i in range(N_IND)}
    st.session_state.slider_values["W_pure"] = True
    st.session_state.slider_values["E_val"] = 0.5
    st.session_state.compass_answers = {}
    st.session_state.live_run = False
    st.session_state.live_init = False
    st.session_state.path_W = [0.5]
    st.session_state.path_B = [0.5]
    st.session_state.path_kappa = [0.0]
    st.session_state.spiritual_nudge = None
    st.session_state.init = True

# =============================================
# ضبط اتجاه الصفحة حسب اللغة
# =============================================
if st.session_state.lang == "ar":
    st.markdown("""
    <style>
    html, body, .stApp { direction: rtl; text-align: right; }
    .stMarkdown, .stText, .stInfo, .stSuccess, .stWarning, .stError { text-align: right; }
    [data-testid="stSidebar"] {
        left: auto !important;
        right: 0 !important;
    }
    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        margin-right: 300px !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    html, body, .stApp { direction: ltr; text-align: left; }
    .stMarkdown, .stText, .stInfo, .stSuccess, .stWarning, .stError { text-align: left; }
    [data-testid="stSidebar"] {
        left: 0 !important;
        right: auto !important;
    }
    [data-testid="stAppViewContainer"] {
        margin-left: 300px !important;
        margin-right: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================
# الشريط الجانبي
# =============================================
render_enhanced_sidebar()

# =============================================
# العنوان الرئيسي والآية
# =============================================
render_enhanced_header()

st.markdown("---")

# =============================================
# عرض الترحيب (مباشر بدون استيراد)
# =============================================
with st.expander(TXT("📜 رسالة ترحيب", "📜 Welcome Message"), expanded=True):
    st.markdown(f"""
    <div class="message-box">
    <h2 style="text-align:center;color:#FFD700;">⚖️ {TXT('مختبر الميزان', 'The Mizan Lab')}</h2>
    <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;">
    "{TXT('وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ', 'And the heaven He raised and imposed the balance. That you not transgress within the balance.')}"
    </p>
    <p>{TXT(
    'أنت تقف الآن على عتبة مختبر فريد. ليس كمختبرات الكيمياء والفيزياء، بل مختبرٌ ينظر إلى الذرة والمجرة، وإلى القلب والضمير، عبر عدسةٍ واحدة. عدسةٌ تزعم أن للوجود قانوناً واحداً، يسري في نسيج الخلق كما يسري في نسيج الوحي. هذا القانون هو <b>"الميزان"</b>.',
    'You are standing at the threshold of a unique lab. Not one of chemistry or physics, but a lab that looks at the atom and the galaxy, at the heart and the conscience, through a single lens. A lens that claims existence has one law, flowing through the fabric of creation as it flows through the fabric of revelation. This law is <b>"Al-Mizan"</b>.'
    )}</p>
    <p>{TXT(
    'من الذرة التي تتآلف بقوة الجذب وتستقر بقوة التنافر، إلى الخلية التي تحمي ذاتها وتهاجم غريبها، إلى الكيمياء التي تتحد فيها الذرات وتحتاج إلى "طاقة تنشيط" لتكسر روابطها القديمة (توبتها!)، إلى المجتمعات التي تجمعها القيم وتحميها من الفساد... كل شيء يصرخ بقانونٍ واحد: <b>S = W × B</b>.',
    'From the atom that unites by attraction and stabilizes by repulsion, to the cell that protects itself and attacks intruders, to chemistry where atoms unite and need "activation energy" to break old bonds (its repentance!), to societies gathered by values and protected from corruption... everything screams one law: <b>S = W x B</b>.'
    )}</p>
    <p>{TXT(
    '<b>W (الولاء لله وأوليائه):</b> قوة الجذب نحو الحق. <b>B (البراءة من الطاغوت وأوليائه):</b> قوة التنافر عن الباطل. <b>S (الثبات الوجودي):</b> حاصل ضربهما. إنها معادلة ضرب لا جمع، لأن القلب لا يجتمع فيه ولاءان، ولأن الثبات لا يقوم إلا على ركنين. هذا هو "الدين القيم" الذي فطر الله الناس عليه، وهذا هو "الإسلام الحنيف" الذي هو الاستجابة الديناميكية لهذا القانون.',
    '<b>W (Loyalty to Allah & His allies):</b> The force of attraction to truth. <b>B (Disavowal of Taghut & its allies):</b> The force of repulsion from falsehood. <b>S (Existential Stability):</b> Their product. It is multiplication, not addition, because a heart cannot hold two loyalties, and stability only rests on two pillars. This is "Al-Deen Al-Qayyim" upon which Allah created people, and this is "Al-Islam Al-Hanif", the dynamic response to this law.'
    )}</p>
    <p>{TXT(
    'لم تكن هذه المعادلة مجرد نظرية بشرية. لقد جسّدها بشرٌ صدقوا ما عاهدوا الله عليه، رجالاً ونساءً، في كل الظروف والأحوال. <b>محمد</b> صلى الله عليه وعلى آله وسلم، خاتم النبيين وسيد المرسلين، الأسوة العظمى والقدوة المثلى، الذي قال: "أوثق عرى الإيمان: الحب في الله، والبغض في الله". ثم <b>إبراهيم</b> خليل الله، الذي أعلنها في وجه أبيه وقومه: "إنني براء مما تعبدون". و<b>موسى</b> كليم الله، الذي وقف في وجه الطاغوت السياسي. و<b>يوسف</b> الصديق، الذي اختار السجن على المعصية. و<b>أصحاب الكهف</b> الفتية، الذين اعتزلوا مجتمعهم الفاسد. و<b>علي والحسن والحسين</b>، الذين جسّدوا قمم الثبات في أقسى الفتن. و<b>أم موسى</b> التي ألقت بولدها في اليم ثقةً بوعد الله: "إنا رادوه إليك". و<b>آسيا امرأة فرعون</b> التي قالت تحت التعذيب: "رب ابن لي عندك بيتاً في الجنة"، متبرئةً من مُلك الطاغوت. هؤلاء ليسوا من عالم الملائكة. هم بشرٌ مثلنا، أكلوا الطعام ومشوا في الأسواق. ولكنهم عرفوا ما فضلهم الله به، وما أكرمهم به كبشر، فعملوا بهذا القانون، فارتقوا إلى أعلى عليين. وهذه المنصة تدعوك أن تسير على آثارهم.',
    'This equation was not merely a human theory. It was embodied by humans who were true to their covenant with Allah, men and women, in all circumstances. <b>Muhammad</b> ﷺ, the Seal of the Prophets and Master of the Messengers, the supreme example, who said: "The firmest handhold of faith is: love for the sake of Allah, and hatred for the sake of Allah." Then <b>Abraham</b>, the Friend of Allah, who declared to his father and people: "I am disassociated from what you worship". <b>Moses</b>, the one who spoke with Allah, who stood against the political tyrant. <b>Joseph</b>, the truthful, who chose prison over sin. <b>The People of the Cave</b>, the youths, who isolated themselves from their corrupt society. <b>Ali, Hassan, and Hussein</b>, who embodied the peaks of stability in the harshest trials. And <b>the mother of Moses</b>, who cast her child into the river, trusting Allah\'s promise: "We will return him to you". And <b>Asiya, the wife of Pharaoh</b>, who said under torture: "My Lord, build for me a house in Paradise", disavowing the tyrant\'s kingdom. These were not angels. They were humans like us, who ate food and walked in the markets. But they recognized what Allah had favored them with, and what He honored them with as humans, so they acted upon this law, and thereby ascended to the highest of heights. This platform invites you to walk in their footsteps.'
    )}</p>
    <p style="text-align:center;color:#FFD700;font-size:1.2em;font-weight:bold;">S = W × B</p>
    <p style="text-align:center;font-style:italic;color:#AAA;">{TXT(
    'لا ندعي الحقيقة المطلقة. بل ندعوك لرؤية شيء قد يكون مر على قلبك ولم تلاحظه. جرب. تأمل. واسأل. الباب مفتوح.',
    'We do not claim absolute truth. We invite you to see something that may have passed your heart unnoticed. Try. Reflect. Ask. The door is open.'
    )}</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander(TXT("📖 دليل المستخدم", "📖 User Guide"), expanded=False):
    st.markdown(TXT("""
    ### 🎯 كيف تستخدم هذا المختبر؟

    **١. بوصلة الإسلام الحنيف:** أجب عن ١٩ سؤالاً لتعرف موقعك الدقيق.
    **٢. مختبر الأمة المتكاملة:** استخدم المنزلقات أو الذكاء الاصطناعي.
    **٣. المشهد الكوني الحي:** شاهد تفاعل النجوم مع قطبي الميزان.
    **٤. الشواهد التاريخية:** قارن بين الدول التاريخية.
    **٥. هندسة الصراط:** تتبع مسارك نحو مقام إبراهيم.
    **٦. المرصد العالمي:** شاهد تطبيق المعادلة على دول العالم.
    **٧. طبيب القلوب:** احصل على تشخيص وروشتة علاجية.
    **٨. شبكة الناجين:** تواصل مع المؤمنين الثابتين.
    **٩. جامعة الميزان:** تعلم النظرية عبر دورات تفاعلية.
    **١٠. مدرسة آل البيت:** نماذج الثبات في الفتنة.

    **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
    """,
    """
    ### 🎯 How to Use This Lab

    **1. Compass:** Answer 19 questions.
    **2. Nation Lab:** Use sliders or AI.
    **3. Cosmic Scene:** Watch stars interact.
    **4. Evidence:** Compare historical nations.
    **5. Path Geometry:** Track your path.
    **6. Observatory:** Apply the equation to world nations.
    **7. Healer:** Get diagnosis and prescription.
    **8. Network:** Connect with steadfast believers.
    **9. Academy:** Learn the theory via courses.
    **10. Ahlul Bayt:** Models of stability in strife.

    **Central Equation:** **S = W x B** (multiplication, not addition).
    """))

# =============================================
# التبويبات الـ 10
# =============================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    TXT("🧍 البوصلة", "🧍 Compass"),
    TXT("🏛️ مختبر الأمة", "🏛️ Nation Lab"),
    TXT("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    TXT("📜 الشواهد", "📜 Evidence"),
    TXT("📐 الصراط", "📐 Path"),
    TXT("🌍 المرصد", "🌍 Observatory"),
    TXT("🩺 طبيب القلوب", "🩺 Healer"),
    TXT("🤝 شبكة الناجين", "🤝 Network"),
    TXT("🎓 الجامعة", "🎓 Academy"),
    TXT("🏴 آل البيت", "🏴 Ahlul Bayt")
])

with tab1:
    render_compass()

with tab2:
    render_nation_lab()

with tab3:
    render_cosmic_scene()

with tab4:
    render_evidence()

with tab5:
    render_path_geometry()

with tab6:
    render_new_observatory()

with tab7:
    render_new_healer()

with tab8:
    render_new_network()

with tab9:
    render_new_academy()

with tab10:
    render_new_ahlulbayt()

# =============================================
# التذييل
# =============================================
render_enhanced_footer()
