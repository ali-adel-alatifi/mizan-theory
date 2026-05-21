# mizan/welcome.py
"""
تبويب البداية – رسالة الترحيب ودليل المستخدم
"""

import streamlit as st
from config import TXT

def render_welcome():
    st.header(TXT("⚖️ مرحباً بك في مختبر الميزان", "⚖️ Welcome to The Mizan Lab"))
    
    # ─────────────────────────────────────────
    # ١. رسالة الترحيب
    # ─────────────────────────────────────────
    with st.expander(TXT("📜 رسالة الترحيب", "📜 Welcome Message"), expanded=True):
        st.markdown(f"""
        <div class="message-box">
        <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;margin-bottom:20px;">
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

    # ─────────────────────────────────────────
    # ٢. دليل المستخدم
    # ─────────────────────────────────────────
    with st.expander(TXT("📖 دليل المستخدم", "📖 User Guide"), expanded=False):
        st.markdown(TXT("""
        ### 🎯 كيف تستخدم هذا المختبر؟

        **١. البوصلة:** أجب عن ١٩ سؤالاً لتعرف موقعك الدقيق في فضاء القيم.
        **٢. مختبر الأمة:** استخدم المنزلقات أو الذكاء الاصطناعي لتحليل الدول والمجتمعات.
        **٣. المشهد الكوني:** شاهد تفاعل النجوم (الأفراد) مع قطبي الميزان.
        **٤. محاكي المجتمع:** شاهد كيف يترابط الأفراد المتوازنون ويتنافر غير المتوازنين.
        **٥. الشواهد التاريخية:** قارن بين الدول التاريخية لترى كيف تنطبق المعادلة.
        **٦. هندسة الصراط المستقيم:** شاهد نموذج إبراهيم عليه السلام وتتبع مسارك نحو مقامه.
        **٧. المرصد العالمي:** شاهد تطبيق المعادلة على دول العالم الحية.
        **٨. طبيب القلوب:** احصل على تشخيص وروشتة علاجية من الكتاب والسنة.
        **٩. شبكة الناجين:** تواصل مع المؤمنين الثابتين، واجعل لك رفيقاً في طريق الصراط.
        **١٠. جامعة الميزان:** تعلم نظرية الدين القيم عبر دورات تفاعلية قصيرة.
        **١١. مدرسة آل البيت:** نماذج الثبات في الفتنة (علي، الحسن، الحسين).
        **١٢. الدليل المرجعي والمعجم الهندسي:** كل ما تحتاجه من آيات ومفاتيح ودورات وأسرار الحروف في مرجع واحد.

        **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
        """,
        """
        ### 🎯 How to Use This Lab

        **1. Compass:** Answer 19 questions to find your precise position.
        **2. Nation Lab:** Use sliders or AI to analyze nations and communities.
        **3. Cosmic Scene:** Watch stars interact with the two poles of the balance.
        **4. Social Fabric:** Watch how balanced individuals link up and the unbalanced repel.
        **5. Historical Evidence:** Compare nations to see how the equation applies.
        **6. Geometry of the Straight Path:** See the Abrahamic model and trace your path to his station.
        **7. Global Observatory:** Apply the equation to world nations.
        **8. Heart Healer:** Get diagnosis and prescription from Quran and Sunnah.
        **9. Survivors Network:** Connect with steadfast believers and find a path companion.
        **10. Mizan University:** Learn the theory through short interactive courses.
        **11. Ahlul Bayt School:** Models of stability in strife (Ali, Hassan, Hussein).
        **12. Reference Guide & Lexicon:** All verses, keys, cycles, and letter secrets in one reference.

        **Central Equation:** **S = W x B** (multiplication, not addition).
        """))


    # ─────────────────────────────────────────
    # ٣. أقسام المنصة
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🧭 أقسام المنصة", "🧭 Platform Sections"))
    
    tabs_info = [
        ("🧍", TXT("البوصلة", "Compass"), TXT("تحديد موقعك", "Find your position")),
        ("🏛️", TXT("مختبر الأمة", "Nation Lab"), TXT("تحليل الدول", "Analyze nations")),
        ("🌌", TXT("المشهد الكوني", "Cosmic Scene"), TXT("محاكاة حية", "Live simulation")),
        ("🧬", TXT("محاكي المجتمع", "Social Fabric"), TXT("النسيج الاجتماعي", "Social fabric")),
        ("📜", TXT("الشواهد", "Evidence"), TXT("مقارنة التاريخ", "Compare history")),
        ("📐", TXT("هندسة الصراط", "Path Geometry"), TXT("مسارك", "Your path")),
        ("🌍", TXT("المرصد العالمي", "Observatory"), TXT("خريطة العالم", "World map")),
        ("🩺", TXT("طبيب القلوب", "Healer"), TXT("روشتة علاجية", "Prescription")),
        ("🤝", TXT("شبكة الناجين", "Network"), TXT("تواصل", "Connect")),
        ("🎓", TXT("الجامعة", "Academy"), TXT("دورات", "Courses")),
        ("🏴", TXT("آل البيت", "Ahlul Bayt"), TXT("نماذج", "Models")),
        ("📚", TXT("الدليل المرجعي", "Reference"), TXT("مراجع ومعجم", "References & Lexicon")),
    ]
    
    for icon, name, desc in tabs_info:
        st.markdown(f"{icon} **{name}** — *{desc}*")
