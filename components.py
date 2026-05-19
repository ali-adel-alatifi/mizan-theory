# mizan/components.py
"""
وحدة مكونات الواجهة
تحتوي: دوال عرض جميع التبويبات
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random, time
from matplotlib.patches import Circle, Rectangle

from config import (TXT, LETTERS_DB, INDICATORS_META, N_IND, COMPASS_DATA,
                    HISTORICAL_DATA, get_indicator_label)
from logic import (calculate_S, simulate_future, compute_compass, curvature, star_color)
from utils import (ai_analyze_compass, ai_fill_sliders, plot_quadrant_map, get_spiritual_nudge,
                   export_session_data, import_session_data)

# استيراد الملفات المنفصلة
from observatory import render_observatory
from healer import render_healer
from network import render_network
from academy import render_academy
from ahlulbayt import render_ahlulbayt
from appendices import render_appendices
from lexicon import render_lexicon
from the_one_law import render_the_one_law
from spiritual_energy import render_spiritual_energy
from civilization_cycle import render_civilization_cycle  # ← الجديد

# =============================================
# رسالة الترحيب ودليل المستخدم
# =============================================
def render_welcome():
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

        <p style="color:#FFD700;font-weight:bold;">{TXT(
        'هذه المنصة ليست كتاباً ولا تطبيقاً. إنها مختبر. مختبرٌ لتكتشف فيه موقعك، وتشخص فيه داءك، وتجد فيه دواءك. هنا، لديك:',
        'This platform is not a book nor an app. It is a lab. A lab for you to discover your position, diagnose your ailment, and find your remedy. Here you have:'
        )}</p>
        <ul style="color:#CCC;line-height:2.2;">
            <li>{TXT('🧭 <b>بوصلة</b> تحدد موقعك من إبراهيم عليه السلام.', '🧭 A <b>Compass</b> to locate your position relative to Abraham.')}</li>
            <li>{TXT('🩺 <b>طبيب قلوب</b> يشخص أمراض الروح ويصف روشتة من الكتاب والسنة.', '🩺 A <b>Heart Healer</b> diagnosing spiritual ailments and prescribing from the Quran and Sunnah.')}</li>
            <li>{TXT('🌍 <b>مرصد عالمي</b> يطبق المعادلة على دول العالم في الزمن الحقيقي.', '🌍 A <b>Global Observatory</b> applying the equation to world nations in real-time.')}</li>
            <li>{TXT('🤝 <b>شبكة الناجين</b> لتصاحب من يعينك على الثبات.', '🤝 A <b>Survivors Network</b> to befriend those who help you remain steadfast.')}</li>
            <li>{TXT('🎓 <b>جامعة</b> لتعلم أصول هذا القانون.', '🎓 A <b>University</b> to learn the foundations of this law.')}</li>
            <li>{TXT('📜 <b>شواهد تاريخية</b> تثبت أن سنة الله لا تتبدل.', '📜 <b>Historical Evidence</b> proving that Allah\'s law does not change.')}</li>
        </ul>

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
        **٤. المعجم الهندسي:** تعرف على الحروف وقيمها وأسرارها والمشغلات.
        **٥. الشواهد التاريخية:** قارن بين الدول التاريخية.
        **٦. هندسة الصراط:** تتبع مسارك نحو مقام إبراهيم.
        **٧. المرصد العالمي:** شاهد تطبيق المعادلة على دول العالم.
        **٨. طبيب القلوب:** احصل على تشخيص وروشتة علاجية.
        **٩. شبكة الناجين:** تواصل مع المؤمنين الثابتين.
        **١٠. جامعة الميزان:** تعلم النظرية عبر دورات تفاعلية.
        **١١. مدرسة آل البيت:** نماذج الثبات في الفتنة.
        **١٢. الملاحق الموسوعية:** مراجع متخصصة.
        **١٣. القانون الواحد:** تجليات القانون من الذرة إلى المجرة.
        **١٤. الطاقة الروحية:** محاكاة قوانين الطاقة الروحية.
        **١٥. الدورة الحضارية:** محاكاة صعود وسقوط الأمم.

        **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
        """,
        """
        ### 🎯 How to Use This Lab

        **1. Compass:** Answer 19 questions.
        **2. Nation Lab:** Use sliders or AI.
        **3. Cosmic Scene:** Watch stars interact.
        **4. Lexicon:** Explore letters, values, secrets, and operators.
        **5. Evidence:** Compare historical nations.
        **6. Path Geometry:** Track your path.
        **7. Observatory:** Apply the equation to world nations.
        **8. Healer:** Get diagnosis and prescription.
        **9. Network:** Connect with steadfast believers.
        **10. Academy:** Learn the theory via courses.
        **11. Ahlul Bayt:** Models of stability in strife.
        **12. Appendices:** Specialized references.
        **13. The One Law:** Manifestations from atom to galaxy.
        **14. Spiritual Energy:** Simulate spiritual energy laws.
        **15. Civilization Cycle:** Simulate the rise and fall of nations.

        **Central Equation:** **S = W x B** (multiplication, not addition).
        """))


# =============================================
# تبويب ١: بوصلة الإسلام الحنيف
# =============================================
def render_compass():
    st.header(TXT("🧍 بوصلة الإسلام الحنيف – اكتشف موقعك بدقة", "🧍 Compass – Discover Your Precise Position"))

    col_set1, col_set2 = st.columns([3, 1])
    with col_set1:
        st.markdown(TXT(
            "أجب عن الأسئلة الـ 19. كل إجابة تؤثر على W و B معًا. المعادلة: S = W x B",
            "Answer the 19 questions. Each answer affects both W and B."
        ))
    with col_set2:
        use_ai = st.checkbox(TXT("🤖 استخدام الذكاء الاصطناعي", "🤖 Use AI"), key="compass_ai")

    if use_ai:
        st.info(TXT("اكتب وصفًا لحالتك ليقوم الذكاء الاصطناعي بتقدير إجاباتك.", "Describe your condition for AI to estimate."))
        ai_text = st.text_area(TXT("الوصف:", "Description:"), height=100, key="ai_compass_text")
        if st.button(TXT("تحليل بالذكاء الاصطناعي", "Analyze with AI"), key="btn_ai_compass"):
            with st.spinner(TXT("جاري التحليل...", "Analyzing...")):
                answers = ai_analyze_compass(ai_text, COMPASS_DATA)
                if answers:
                    for i, val in enumerate(answers[:19]):
                        st.session_state.compass_answers[f"q_{i+1}"] = val
                    st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
                    st.rerun()
                else:
                    st.warning(TXT(
                        "تعذر الاتصال بالذكاء الاصطناعي. تأكد من إعدادات API أو أجب يدويًا.",
                        "Could not connect to AI. Please check API settings or answer manually."
                    ))

    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    for q in COMPASS_DATA:
        with st.expander(f"**{q['id']}. {q['topic']}**  [{q['letter']}={q['value']}]"):
            st.markdown(f"*{q['text']}*")
            key = f"q_{q['id']}"
            ans = st.radio(
                TXT("اختر:", "Choose:"),
                [a[0] for a in q['answers']],
                key=key, index=None
            )
            if ans is not None:
                idx = [a[0] for a in q['answers']].index(ans)
                st.session_state.compass_answers[key] = idx

    if len(st.session_state.compass_answers) == 19:
        W_raw, B_raw, S_score = compute_compass(st.session_state.compass_answers, COMPASS_DATA)

        if W_raw >= 0.5 and B_raw >= 0.5:
            q_name, q_color = TXT("مؤمن", "Believer"), '#FFD700'
        elif W_raw < 0.5 and B_raw >= 0.5:
            q_name, q_color = TXT("كافر", "Disbeliever"), '#FF5252'
        elif W_raw < 0.5 and B_raw < 0.5:
            q_name, q_color = TXT("منافق", "Hypocrite"), '#FFB6C1'
        else:
            q_name, q_color = TXT("مشرك", "Polytheist"), '#FFA500'

        st.divider()
        st.subheader(TXT("📊 موقعك", "📊 Your Position"))
        c1, c2, c3 = st.columns(3)
        c1.metric("W (الولاء)", f"{W_raw:+.2f}")
        c2.metric("B (البراءة)", f"{B_raw:+.2f}")
        c3.metric("S (الثبات)", f"{S_score:.2f}")
        st.markdown(f"<h2 style='color:{q_color};text-align:center;'>{q_name}</h2>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.fill_between([0, 1.2], 0, 1.2, color='#FFD700', alpha=0.3)
        ax.fill_between([-1.2, 0], 0, 1.2, color='#FF5252', alpha=0.2)
        ax.fill_between([-1.2, 0], -1.2, 0, color='#FFB6C1', alpha=0.2)
        ax.fill_between([0, 1.2], -1.2, 0, color='#FFA500', alpha=0.2)
        ax.scatter(B_raw, W_raw, s=200, c='cyan', edgecolors='white', linewidth=2, zorder=10)
        ax.scatter(1, 1, s=80, c='#FFD700', marker='*', zorder=10)
        ax.text(1, 1.1, TXT('إبراهيم', 'Abraham'), color='#FFD700', fontsize=7, ha='center')
        ax.tick_params(colors='white')
        st.pyplot(fig)

        st.markdown("---")
        col_save, col_load = st.columns(2)
        with col_save:
            export_session_data(
                {"compass_answers": st.session_state.compass_answers},
                "mizan_compass"
            )
        with col_load:
            import_session_data(["compass_answers"])

        if st.button(TXT("🔄 إعادة", "🔄 Retake"), use_container_width=True, key="btn_compass_reset"):
            st.session_state.compass_answers = {}
            st.rerun()


# =============================================
# تبويب ٢: مختبر الأمة المتكامل
# =============================================
def render_nation_lab():
    st.header(TXT("🏛️ مختبر الأمة – المنزلقات والذكاء الاصطناعي", "🏛️ Nation Lab – Sliders & AI"))

    with st.expander(TXT("🎛️ مؤشرات الطاقة الروحية", "🎛️ Spiritual Energy Indicators"), expanded=True):
        st.caption(TXT(
            "كل حركة وسكنة مولد طاقة نحو الولاية والبراءة. [الحرف=القيمة]",
            "Every movement generates energy. [Letter=Value]"
        ))

        slider_vals = []
        for i in range(0, N_IND, 2):
            col_a, col_b = st.columns(2)
            with col_a:
                if i < N_IND:
                    val = st.slider(get_indicator_label(i), -1.0, 1.0,
                                   st.session_state.slider_values.get(f"V{i}", 0.0), 0.1,
                                   key=f"lab_V{i}")
                    slider_vals.append(val)
                    st.session_state.slider_values[f"V{i}"] = val
            with col_b:
                if i + 1 < N_IND:
                    val = st.slider(get_indicator_label(i+1), -1.0, 1.0,
                                   st.session_state.slider_values.get(f"V{i+1}", 0.0), 0.1,
                                   key=f"lab_V{i+1}")
                    slider_vals.append(val)
                    st.session_state.slider_values[f"V{i+1}"] = val

        st.markdown("---")
        col_pure, col_E = st.columns(2)
        with col_pure:
            W_pure = st.checkbox(
                TXT("الإخلاص لله (عدم الشرك) [أ=1]", "Sincerity [A=1]"),
                value=st.session_state.slider_values.get("W_pure", True)
            )
            st.session_state.slider_values["W_pure"] = W_pure
        with col_E:
            E_val = st.slider(
                TXT("التمكين (E) [ق=100]", "Empowerment [Q=100]"),
                0.0, 1.0, st.session_state.slider_values.get("E_val", 0.5), 0.05, key="lab_E"
            )
            st.session_state.slider_values["E_val"] = E_val

    st.markdown("---")
    st.subheader(TXT("🤖 مساعد الذكاء الاصطناعي", "🤖 AI Assistant"))
    ai_text = st.text_area(
        TXT("الوصف النصي:", "Description:"), height=100, key="ai_nation_text",
        placeholder=TXT("مثال: دولة إسلامية ذات أغلبية شابة...", "Example: An Islamic country...")
    )
    if st.button(TXT("تحليل بالذكاء الاصطناعي وملء المنزلقات", "Analyze with AI & Fill Sliders"),
                 type="primary", use_container_width=True, key="btn_ai_nation"):
        if not ai_text.strip():
            st.warning(TXT("يرجى إدخال وصف نصي أولاً.", "Please enter a description first."))
        else:
            with st.spinner(TXT("جاري التحليل...", "Analyzing...")):
                result = ai_fill_sliders(ai_text, INDICATORS_META)
                if result:
                    vals = result.get("values", [0.0] * N_IND)[:N_IND]
                    for i in range(N_IND):
                        st.session_state.slider_values[f"V{i}"] = vals[i]
                    st.session_state.slider_values["W_pure"] = result.get("W_pure", True)
                    st.session_state.slider_values["E_val"] = result.get("E_val", 0.5)
                    st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
                    if "analysis" in result:
                        st.info(result["analysis"])
                    st.rerun()
                else:
                    st.warning(TXT(
                        "تعذر الاتصال بالذكاء الاصطناعي.",
                        "Could not connect to AI."
                    ))

    st.markdown("---")
    vals = [st.session_state.slider_values.get(f"V{i}", 0.0) for i in range(N_IND)]
    W_pure = st.session_state.slider_values.get("W_pure", True)
    E_val = st.session_state.slider_values.get("E_val", 0.5)
    W_vals = vals[0:6]; B_vals = vals[6:11]
    W_raw = np.mean(W_vals); B_raw = np.mean(B_vals)
    B_compassion = B_vals[1]; B_disavowal = B_vals[0]

    S_final, E_norm, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
        W_raw, B_raw, E_val, W_pure, B_compassion, B_disavowal
    )

    if W_raw >= 0.1 and B_raw >= 0.1:
        q_name, q_color = TXT("الربع الأول: المؤمنون", "Q1: Believers"), '#FFD700'
    elif W_raw >= 0.1 and B_raw < 0.1:
        q_name, q_color = TXT("الربع الثاني: المغضوب عليهم", "Q2: Those with Wrath"), '#FF5252'
    elif W_raw < 0.1 and B_raw >= 0.1:
        q_name, q_color = TXT("الربع الرابع: الضالون", "Q4: Those Astray"), '#FFA500'
    else:
        q_name, q_color = TXT("الربع الثالث: المنافقون", "Q3: Hypocrites"), '#FFB6C1'

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("W (الولاء)", f"{W_raw:+.2f}")
    col2.metric("B (البراءة)", f"{B_raw:+.2f}")
    col3.metric("S (الثبات)", f"{S_final:.2f}")
    col4.metric("E (التمكين)", f"{E_val:.2f}")
    col5.metric(TXT("فجوة", "Gap"), f"{istidraj_gap:.2f}")

    st.markdown(f"""
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;border:2px solid {q_color};margin:15px 0;">
        <h3 style="color:{q_color};text-align:center;">📍 {q_name}</h3>
    </div>
    """, unsafe_allow_html=True)

    if gate_msg:
        st.markdown(f"### {gate_color} {gate_name}")
        if "انهيار" in gate_msg or "Collapse" in gate_msg or "لا يغفر" in gate_msg:
            st.error(gate_msg)
        elif "باطلة" in gate_msg or "Void" in gate_msg:
            st.warning(gate_msg)
        else:
            st.success(gate_msg)

    if istidraj_gap > 0.3:
        st.error(f"🚨 {TXT('إنذار استدراج', 'Istidraj Alert')}: E={E_val:.2f} > S={S_final:.2f}")
    elif istidraj_gap > 0.1:
        st.warning(f"⚡ {TXT('فجوة استدراج متوسطة', 'Moderate Gap')}: {istidraj_gap:.2f}")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(TXT("### 🗺️ خريطة الوجود", "### 🗺️ Existence Map"))
        fig = plot_quadrant_map(B_raw, W_raw, istidraj_gap)
        st.pyplot(fig)
    with col_b:
        st.markdown(TXT("### ⏳ المحاكي الزمني", "### ⏳ Time Simulator"))
        years = st.slider(TXT("سنوات", "Years"), 10, 100, 50, 10, key="yrs_lab")
        S_hist, E_hist = simulate_future(S_final, E_val, W_raw, B_raw, years)
        fig, ax = plt.subplots(figsize=(5, 3), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(S_hist, label='S', color='#FFD700', lw=2)
        ax.plot(E_hist, label='E', color='#0FF', lw=1.5, ls='--')
        ax.fill_between(range(years+1), S_hist, E_hist,
                        where=(np.array(E_hist) > np.array(S_hist)),
                        color='red', alpha=0.2)
        ax.set_xlabel(TXT('سنوات', 'Years'), color='white')
        ax.set_ylabel(TXT('قيمة', 'Value'), color='white')
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=6)
        ax.tick_params(colors='white', labelsize=6); ax.grid(True, alpha=0.2)
        st.pyplot(fig)

    st.markdown("---")
    st.markdown(TXT("### 🏥 المستشفى – الوصفة العلاجية", "### 🏥 Hospital – Prescription"))
    wW, wB = np.argmin(W_vals), np.argmin(B_vals)
    W_L = [get_indicator_label(i) for i in range(6)]
    B_L = [get_indicator_label(i+6) for i in range(5)]

    if gate_name == TXT("بوابة الشرك", "Shirk Gate"):
        st.error(TXT(f"**العلاج:** تجديد التوحيد وإخلاص العبادة لله وحده.", f"**Treatment:** Renew Tawheed."))
    elif gate_name == TXT("بوابة الماعون", "Al-Ma'un Gate"):
        st.error(TXT(f"**العلاج:** إصلاح مؤشر '{B_L[wB]}' فورًا.", f"**Treatment:** Fix '{B_L[wB]}'."))
    elif gate_name == TXT("بوابة الإخلاص", "Sincerity Gate"):
        st.warning(TXT(f"**العلاج:** تنقية '{W_L[wW]}' من شوائب الشرك.", f"**Treatment:** Purify '{W_L[wW]}'."))
    elif istidraj_gap > 0.3:
        st.error(TXT(f"**العلاج:** سد فجوة الاستدراج عبر رفع '{W_L[wW]}' أو '{B_L[wB]}'.", f"**Treatment:** Close the gap."))
    else:
        st.info(TXT(f"**للتقدم:** تعزيز '{W_L[wW]}' و '{B_L[wB]}' معًا.", f"**To advance:** Strengthen both."))

    with st.expander(TXT("📊 تفصيل المؤشرات", "📊 Indicator Details"), expanded=False):
        all_vals = vals.copy()
        groups = [TXT('ولاء', 'Loyalty')] * 6 + [TXT('براءة', 'Disavowal')] * 5
        inds = [get_indicator_label(i) for i in range(N_IND)]
        import pandas as pd
        df_all = pd.DataFrame({
            TXT('المؤشر', 'Indicator'): inds,
            TXT('القيمة', 'Value'): all_vals,
            TXT('المجموعة', 'Group'): groups
        })
        st.dataframe(
            df_all.style.format({TXT('القيمة', 'Value'): '{:+.2f}'})
            .background_gradient(subset=[TXT('القيمة', 'Value')], cmap='RdYlGn'),
            hide_index=True, use_container_width=True
        )


# =============================================
# تبويب ٣: المشهد الكوني الحي
# =============================================
def render_cosmic_scene():
    st.header(TXT("🌌 المشهد الكوني الحي", "🌌 Live Cosmic Scene"))

    with st.expander(TXT("⚙️ إعدادات المشهد", "⚙️ Scene Settings"), expanded=False):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            live_speed = st.slider(TXT("السرعة", "Speed"), 0.05, 0.3, 0.1, 0.05, key="live_speed")
        with col_s2:
            live_stars = st.slider(TXT("عدد النجوم", "Stars"), 50, 200, 100, 25, key="live_stars")

    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button(TXT("▶️ تشغيل", "▶️ Run"), use_container_width=True, type="primary", key="btn_live_run"):
            st.session_state.live_run = True
    with col_btn2:
        if st.button(TXT("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True, key="btn_live_stop"):
            st.session_state.live_run = False
    with col_btn3:
        if st.button(TXT("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True, key="btn_live_reset"):
            for k in list(st.session_state.keys()):
                if k.startswith("live_"):
                    del st.session_state[k]
            st.rerun()

    placeholder = st.empty()

    if st.session_state.get("live_run", False):
        if not st.session_state.get("live_init", False):
            N = live_stars
            cx, cy = 14, 10.0
            st.session_state.live_cx = cx
            st.session_state.live_cy = cy
            st.session_state.live_sx = np.random.uniform(cx-13, cx+13, N)
            st.session_state.live_sy = np.random.uniform(cy-9, cy+9, N)
            st.session_state.live_sw = np.random.uniform(0.1, 1.0, N)
            st.session_state.live_sb = np.random.uniform(0.1, 1.0, N)
            st.session_state.live_W = 0.55
            st.session_state.live_B = 0.52
            st.session_state.live_E = 0.3
            st.session_state.live_S = 0.55 * 0.52
            st.session_state.live_aW = 0.0
            st.session_state.live_aB = np.pi * 0.5
            st.session_state.live_frame = 0
            st.session_state.live_init = True

        try:
            cx = st.session_state.live_cx; cy = st.session_state.live_cy
            sx = st.session_state.live_sx.copy(); sy = st.session_state.live_sy.copy()
            sw = st.session_state.live_sw.copy(); sb = st.session_state.live_sb.copy()
            W = st.session_state.live_W; B = st.session_state.live_B
            E = st.session_state.live_E; aW = st.session_state.live_aW; aB = st.session_state.live_aB
            frame = st.session_state.live_frame; N = len(sx)

            for i in range(N):
                sw[i] += (W - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (B - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

            if random.random() < 0.005:
                aff = np.random.choice(N, size=int(N * 0.2), replace=False)
                sw[aff] *= random.uniform(0.5, 0.8); sb[aff] *= random.uniform(0.5, 0.8)

            avgW = np.mean(sw); avgB = np.mean(sb)
            W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B; E += 0.03 * (S - E)

            aW += 0.02 + random.uniform(-0.02, 0.02) * (1 - W)**2
            aB += 0.02 + random.uniform(-0.02, 0.02) * (1 - B)**2
            wx = cx + (7 - 2.5 * W) * np.cos(aW); wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB); by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7

            fig, ax = plt.subplots(figsize=(14, 10), facecolor='#0a0f1e')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.6, '#FFD700'), (1.8, 0.3, '#FFD700'),
                             (2.8, 0.1, '#FFA500'), (4, 0.03, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 3 * S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#000', fontsize=14, ha='center', va='center', fontweight='bold')
            ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#0FF', alpha=0.15, zorder=7))
            ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy + 0.8, 'W', color='#FFF', fontsize=10, ha='center')
            ax.text(bx, by + 0.8, 'B', color='#F33', fontsize=10, ha='center')

            colors = [star_color(sw[i], sb[i]) for i in range(N)]
            ax.scatter(sx, sy, s=20, c=colors, alpha=0.9, edgecolors='white', linewidths=0.2, zorder=5)
            ax.text(14, 1.2, f'S={S:.2f} | E={E:.2f}', color='#CCC', fontsize=9, ha='center')
            plt.tight_layout(pad=0); placeholder.pyplot(fig); plt.close(fig)

            st.session_state.live_sx = sx; st.session_state.live_sy = sy
            st.session_state.live_sw = sw; st.session_state.live_sb = sb
            st.session_state.live_W = W; st.session_state.live_B = B
            st.session_state.live_E = E; st.session_state.live_S = S
            st.session_state.live_aW = aW; st.session_state.live_aB = aB
            st.session_state.live_frame = frame + 1

            time.sleep(live_speed)
            st.rerun()
        except Exception as e:
            st.error(f"Simulation error: {e}")
            st.session_state.live_run = False
    else:
        st.info(TXT("اضغط ▶️ تشغيل", "Press ▶️ Run"))


# =============================================
# تبويب ٥: الشواهد التاريخية
# =============================================
def render_evidence():
    st.header(TXT("📜 الشواهد التاريخية – حين ينطق التاريخ مصدقًا للمعادلة",
                   "📜 Historical Evidence – When History Bears Witness"))

    selected_nation = st.selectbox(TXT("اختر دولة:", "Select a nation:"), list(HISTORICAL_DATA.keys()))

    if selected_nation:
        data = HISTORICAL_DATA[selected_nation]
        W_hist, B_hist, E_hist = data["W"], data["B"], data["E"]
        S_hist = W_hist * B_hist; gap = E_hist - S_hist

        st.markdown(f"### {selected_nation}")
        st.markdown(f"**{data['era']}**")
        st.markdown(data["desc"])

        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        col_m1.metric("W", f"{W_hist:.2f}"); col_m2.metric("B", f"{B_hist:.2f}")
        col_m3.metric("S", f"{S_hist:.2f}"); col_m4.metric("E", f"{E_hist:.2f}")
        col_m5.metric(TXT("فجوة", "Gap"), f"{gap:.2f}")

        fig_hist, (ax_bar, ax_gauge) = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0a0f1e')
        ax_bar.set_facecolor('#0a0f1e')
        categories = ['W', 'B', 'S', 'E']; values = [W_hist, B_hist, S_hist, E_hist]
        colors_bar = ['#FFD700', '#FF5252', '#00FF88', '#00FFFF']
        bars = ax_bar.bar(categories, values, color=colors_bar, edgecolor='white', linewidth=1.5)
        for bar, val in zip(bars, values):
            ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                       f'{val:.2f}', ha='center', color='white', fontsize=11, fontweight='bold')
        ax_bar.set_ylim(0, 1.15); ax_bar.set_title(TXT("مؤشرات الدولة", "State Indicators"), color='white', fontsize=13)
        ax_bar.tick_params(colors='white'); ax_bar.grid(True, alpha=0.2, axis='y')

        ax_gauge.set_facecolor('#0a0f1e')
        ax_gauge.set_xlim(-1.5, 1.5); ax_gauge.set_ylim(-1.5, 1.5)
        ax_gauge.set_aspect('equal'); ax_gauge.axis('off')
        ax_gauge.add_patch(Rectangle((0, 0), 1.4, 1.4, color='#FFD700', alpha=0.2))
        ax_gauge.add_patch(Rectangle((-1.4, 0), 1.4, 1.4, color='#FF5252', alpha=0.2))
        ax_gauge.add_patch(Rectangle((-1.4, -1.4), 1.4, 1.4, color='#FFB6C1', alpha=0.2))
        ax_gauge.add_patch(Rectangle((0, -1.4), 1.4, 1.4, color='#FFA500', alpha=0.2))
        ax_gauge.axhline(0, color='white', lw=0.5, alpha=0.5); ax_gauge.axvline(0, color='white', lw=0.5, alpha=0.5)
        b_pos = (B_hist * 2 - 1) * 1.3; w_pos = (W_hist * 2 - 1) * 1.3
        ax_gauge.scatter([b_pos], [w_pos], s=400, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
        ax_gauge.scatter([1.3], [1.3], s=150, c='#FFD700', marker='*', zorder=10)
        ax_gauge.text(1.3, 1.4, TXT("إبراهيم", "Abraham"), ha='center', color='#FFD700', fontsize=8)
        ax_gauge.set_title(TXT("الموقع في فضاء (W, B)", "Position in (W, B) Space"), color='white', fontsize=13)
        plt.tight_layout(); st.pyplot(fig_hist)

        if gap > 0.4: st.error(TXT(f"⚠️ حالة استدراج: فجوة = {gap:.2f}", f"⚠️ Istidraj: Gap = {gap:.2f}"))
        elif S_hist > 0.7: st.success(TXT(f"✅ توازن عالٍ: S = {S_hist:.2f}", f"✅ High Balance: S = {S_hist:.2f}"))
        else: st.info(TXT(f"ℹ️ حالة متوسطة: S = {S_hist:.2f}", f"ℹ️ Moderate: S = {S_hist:.2f}"))

        st.markdown("---"); st.subheader(TXT("💡 الدروس المستفادة", "💡 Lessons Learned"))
        st.markdown(data["lessons"])

    st.markdown("---")
    st.subheader(TXT("🔍 مقارنة بين دولتين", "🔍 Compare Two Nations"))
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        nation_a = st.selectbox(TXT("الدولة الأولى:", "First nation:"), list(HISTORICAL_DATA.keys()), key="nation_a")
    with col_c2:
        nation_b = st.selectbox(TXT("الدولة الثانية:", "Second nation:"), list(HISTORICAL_DATA.keys()), index=1, key="nation_b")

    if nation_a and nation_b:
        data_a = HISTORICAL_DATA[nation_a]; data_b = HISTORICAL_DATA[nation_b]
        fig_comp, ax_comp = plt.subplots(figsize=(10, 6), facecolor='#0a0f1e')
        ax_comp.set_facecolor('#0a0f1e')
        x = np.arange(4); width = 0.35; labels = ['W', 'B', 'S', 'E']
        values_a = [data_a["W"], data_a["B"], data_a["W"]*data_a["B"], data_a["E"]]
        values_b = [data_b["W"], data_b["B"], data_b["W"]*data_b["B"], data_b["E"]]
        ax_comp.bar(x - width/2, values_a, width, color='#FFD700', edgecolor='white', linewidth=1.5, label=nation_a[:40])
        ax_comp.bar(x + width/2, values_b, width, color='#00BFFF', edgecolor='white', linewidth=1.5, label=nation_b[:40])
        ax_comp.set_xticks(x); ax_comp.set_xticklabels(labels, color='white', fontsize=12)
        ax_comp.set_ylim(0, 1.15)
        ax_comp.set_title(TXT("مقارنة المؤشرات", "Indicator Comparison"), color='white', fontsize=13)
        ax_comp.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=10)
        ax_comp.tick_params(colors='white'); ax_comp.grid(True, alpha=0.2, axis='y')
        plt.tight_layout(); st.pyplot(fig_comp)


# =============================================
# تبويب ٦: هندسة الصراط
# =============================================
def render_path_geometry():
    st.header(TXT("📐 هندسة الصراط – البرهان النبوي والنموذج الإبراهيمي",
                   "📐 Path Geometry – Prophetic Proof & Abrahamic Model"))

    st.markdown(TXT("""
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:25px;border:2px solid #FFD700;margin:20px 0;text-align:center;">
        <h3 style="color:#FFD700;margin-top:0;">🕋 البرهان النبوي</h3>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;">«أَوْثَقُ عُرَى الْإِيمَانِ: الْحُبّ فِي اللَّهِ، وَالْبُغْضُ فِي اللَّهِ»</p>
        <p style="color:#FFD700;font-size:1.2em;">⬇️</p>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;">«مَنْ أَحَبَّ لِلَّهِ، وَأَبْغَضَ لِلَّهِ، وَأَعْطَى لِلَّهِ، وَمَنَعَ لِلَّهِ، فَقَدِ اسْتَكْمَلَ الْإِيمَانَ»</p>
        <hr style="border-color:rgba(255,215,0,0.3);">
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W x B</p>
        <p style="color:#AAA;">الحب في الله = W. البغض في الله = B. الواو هنا واو المعية (x) لا واو الجمع (+).</p>
    </div>
    """, """
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:25px;border:2px solid #FFD700;margin:20px 0;text-align:center;">
        <h3 style="color:#FFD700;">🕋 The Prophetic Proof</h3>
        <p style="color:#CCC;">"The firmest handhold of faith is: love for the sake of Allah, and hatred for the sake of Allah."</p>
        <p style="color:#FFD700;font-size:1.2em;">⬇️</p>
        <p style="color:#CCC;">"Whoever loves for Allah, hates for Allah... has completed faith."</p>
        <hr style="border-color:rgba(255,215,0,0.3);">
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W x B</p>
    </div>
    """), unsafe_allow_html=True)

    st.markdown(TXT("""
    ### 🕋 النموذج الإبراهيمي: الجيوديسي المثالي
    إبراهيم عليه السلام هو الجيوديسي المثالي: الخط المستقيم الذي انحناؤه صفر (κ = 0).
    """, """
    ### 🕋 The Abrahamic Model: The Ideal Geodesic
    Abraham (AS) is the ideal geodesic: the straight line with zero curvature (κ = 0).
    """))

    st.markdown("---")

    if 'path_W' not in st.session_state:
        st.session_state.path_W = [0.5]
    if 'path_B' not in st.session_state:
        st.session_state.path_B = [0.5]
    if 'path_kappa' not in st.session_state:
        st.session_state.path_kappa = [0.0]
    if 'spiritual_nudge' not in st.session_state:
        st.session_state.spiritual_nudge = None

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(TXT("▶️ خطوة نحو الكمال", "▶️ Step Toward Perfection"), use_container_width=True, key="btn_path_step"):
            cW = st.session_state.path_W[-1]; cB = st.session_state.path_B[-1]
            nW = min(1.0, cW + 0.05); nB = min(1.0, cB + 0.05)
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            d = np.sqrt((1 - nW)**2 + (1 - nB)**2)
            if d < 0.3: st.session_state.spiritual_nudge = get_spiritual_nudge("approaching")
            elif d < 0.5: st.session_state.spiritual_nudge = get_spiritual_nudge("progressing")
            else: st.session_state.spiritual_nudge = None
            st.rerun()

    with c2:
        sin_str = st.slider(TXT("⚡ شدة المعصية", "⚡ Sin Strength"), 0.01, 0.3, 0.1, 0.01, key="sin_path")
        if st.button(TXT("⚠️ معصية", "⚠️ Sin"), use_container_width=True, key="btn_path_sin"):
            cW = st.session_state.path_W[-1]; cB = st.session_state.path_B[-1]
            nW = max(0.0, cW - sin_str * random.uniform(0.5, 1.5))
            nB = max(0.0, cB - sin_str * random.uniform(0.5, 1.5))
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            st.session_state.spiritual_nudge = get_spiritual_nudge("sin")
            st.rerun()

    with c3:
        if st.button(TXT("🕌 توبة نصوح", "🕌 Sincere Repentance"), use_container_width=True, key="btn_path_repent"):
            cW = st.session_state.path_W[-1]; cB = st.session_state.path_B[-1]
            nW = min(1.0, cW + 0.8 * (1.0 - cW)); nB = min(1.0, cB + 0.8 * (1.0 - cB))
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.path_kappa.append(0.0)
            st.session_state.spiritual_nudge = get_spiritual_nudge("repentance")
            st.rerun()

    if st.session_state.spiritual_nudge:
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.9);border-radius:12px;padding:20px;border:1px solid #FFD700;margin:15px 0;text-align:center;line-height:2.2;'>
            <p style='color:#FFD700;font-size:1.1em;margin:0;white-space:pre-line;'>{st.session_state.spiritual_nudge}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button(TXT("🔄 إعادة الرحلة", "🔄 Reset Path"), use_container_width=True, key="btn_path_reset"):
        st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
        st.session_state.path_kappa = [0.0]; st.session_state.spiritual_nudge = None
        st.rerun()

    pW = st.session_state.path_W; pB = st.session_state.path_B
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
    ax1 = axes[0]; ax1.set_facecolor('#0a0f1e')
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_xlabel("B (البراءة)", color='white'); ax1.set_ylabel("W (الولاء)", color='white')
    ax1.set_title(TXT("مسارك في فضاء (W, B)", "Your Path in (W, B) Space"), color='white', fontsize=13)
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=3, alpha=0.8, label=TXT("مسار إبراهيم", "Abraham's Path"))
    ax1.scatter([1], [1], s=200, c='#FFD700', edgecolors='white', linewidth=3, zorder=10, label=TXT("مقام إبراهيم", "Station of Abraham"))
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.path_kappa[i] if i < len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label=TXT("البداية", "Start"))
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label=TXT("الآن", "Now"))
    ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')

    ax2 = axes[1]; ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.path_kappa, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label=TXT("حد الخطر", "Danger"))
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label=TXT("الصراط (κ=0)", "Straight Path"))
    ax2.set_title(TXT("منحنى الانحناء (κ)", "Curvature Over Time"), color='white', fontsize=13)
    ax2.set_xlabel(TXT("الخطوات", "Steps"), color='white'); ax2.set_ylabel("κ", color='white')
    ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
    mk = max(st.session_state.path_kappa) if st.session_state.path_kappa else 0.1
    ax2.set_ylim(-0.01, max(0.2, mk * 1.2))
    plt.tight_layout(); st.pyplot(fig)

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("W (الولاء)", f"{pW[-1]:.3f}"); c2.metric("B (البراءة)", f"{pB[-1]:.3f}")
    ck = st.session_state.path_kappa[-1] if st.session_state.path_kappa else 0.0
    c3.metric("κ (الانحناء)", f"{ck:.4f}")
    c4.metric(TXT("الصراط؟", "On Path?"), TXT("✅ نعم", "✅ YES") if ck < 0.03 else TXT("⚠️ لا", "⚠️ NO"))

    d_abraham = np.sqrt((1 - pW[-1])**2 + (1 - pB[-1])**2)
    st.markdown(f"""
    <div style='text-align:center;padding:15px;background:rgba(20,30,60,0.8);border-radius:10px;border:1px solid #FFD700;'>
        <p style='color:#FFD700;font-size:1em;margin:0;'>
            {TXT(f'📏 المسافة إلى مقام إبراهيم: {d_abraham:.3f}', f'📏 Distance to Station of Abraham: {d_abraham:.3f}')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# دوال استدعاء التبويبات الجديدة
# =============================================
def render_new_observatory():
    render_observatory()

def render_new_healer():
    render_healer()

def render_new_network():
    render_network()

def render_new_academy():
    render_academy()

def render_new_ahlulbayt():
    render_ahlulbayt()

def render_new_appendices():
    render_appendices()

def render_new_lexicon():
    render_lexicon()

def render_new_the_one_law():
    render_the_one_law()

def render_new_spiritual_energy():
    render_spiritual_energy()

def render_new_civilization_cycle():  # ← الجديد
    render_civilization_cycle()
