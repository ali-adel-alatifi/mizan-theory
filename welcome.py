# mizan/welcome.py
"""
تبويب البداية – بوابة العبور من الحيرة إلى اليقين
رسالة ترحيب ودليل مستخدم
"""

import streamlit as st
from config import TXT

# =============================================
# دالة إصلاح النصوص العربية
# =============================================
def fix_rtl_display():
    """إصلاح مشكلة عرض النصوص العربية في Streamlit"""
    st.markdown("""
    <style>
    /* إجبار كل النصوص على أن تكون من اليمين لليسار */
    div, p, h1, h2, h3, h4, h5, h6, span, strong, em, li, label, .stMarkdown, .stText {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: plaintext !important;
    }
    /* العناوين الرئيسية */
    .stTitle, .stHeader, .stSubheader {
        direction: rtl !important;
        text-align: right !important;
    }
    /* صناديق المعلومات */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        direction: rtl !important;
        text-align: right !important;
    }
    /* الأزرار */
    button {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_welcome():
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
    # ─────────────────────────────────────────
    # ١. رسالة الترحيب – النداء الأول
    # ─────────────────────────────────────────
    with st.expander(TXT("📜 رسالة ترحيب", "📜 Welcome Message"), expanded=True):
        st.markdown(f"""
        <div class="message-box">
        
        <p style="text-align:center;font-style:italic;color:#FFD700;font-size:1.3em;margin-bottom:30px;line-height:2.2;">
        "{TXT(
        'وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ',
        'And the heaven He raised and imposed the balance. That you not transgress within the balance.'
        )}"
        </p>
        
        <p style="text-align:center;color:#FFD700;font-style:italic;font-size:1.1em;margin:15px 0;">
        ﴿وَمَا أُوتِيتُم مِّنَ الْعِلْمِ إِلَّا قَلِيلًا﴾ [الإسراء: ٨٥]
        </p>
        
        <p style="text-align:center;color:#FFD700;font-style:italic;font-size:1.1em;margin:15px 0;">
        ﴿وَفِي الْأَرْضِ آيَاتٌ لِّلْمُوقِنِينَ * وَفِي أَنفُسِكُمْ ۚ أَفَلَا تُبْصِرُونَ﴾ [الذاريات: ٢٠-٢١]
        </p>

        <p style="color:#FFD700;font-size:1.2em;font-weight:bold;text-align:center;margin-bottom:25px;">{TXT(
        '⚖️ هل يوجد حقاً قانون واحد يحكم الذرة والمجرة... والقلب والحضارة؟',
        '⚖️ Is there truly one law governing the atom and the galaxy... the heart and civilization?'
        )}</p>

        <p>{TXT(
        'أنت تقف الآن على عتبة مختبر فريد. ليس كمختبرات الكيمياء والفيزياء التي تبحث في المادة وحدها، بل مختبرٌ ينظر إلى <b>الذرة والمجرة</b>، وإلى <b>القلب والضمير</b>، وإلى <b>الفرد والحضارة</b>، عبر عدسةٍ واحدة لا تتغير. عدسةٌ تعلن أن لهذا الوجود <b>قانوناً واحداً</b>، يسري في نسيج الخلق كما يسري في نسيج الوحي، لا يتبدل ولا يتحول. هذا القانون هو <b>"الميزان"</b>.',
        'You are standing at the threshold of a unique lab. Not one of chemistry or physics that studies matter alone, but a lab that looks at <b>the atom and the galaxy</b>, at <b>the heart and the conscience</b>, at <b>the individual and civilization</b>, through a single, unchanging lens. A lens that proclaims that this existence has <b>one law</b>, flowing through the fabric of creation as it flows through the fabric of revelation, never changing or transforming. This law is <b>"Al-Mizan"</b>.'
        )}</p>

        <p style="color:#FFD700;font-size:1.1em;font-weight:bold;text-align:center;margin:20px 0;">{TXT(
        '🔬 هل لاحظت أن الذرة لا تستقر إلا بقوتين؟ جاذبية تجمع، وتنافر يمنع التصادم. هل هذه مصادفة؟',
        '🔬 Have you noticed that the atom only stabilizes with two forces? Attraction that gathers, and repulsion that prevents collision. Is this coincidence?'
        )}</p>

        <p>{TXT(
        'من الذرة التي تتآلف بقوة الجذب وتستقر بقوة التنافر، إلى الخلية التي تحمي ذاتها وتهاجم غريبها، إلى الكيمياء التي تتحد فيها الذرات وتحتاج إلى "طاقة تنشيط" لتكسر روابطها القديمة – توبتها – إلى المجتمعات التي تجمعها القيم وتحميها من الفساد... كل شيء في هذا الوجود يصرخ بقانونٍ واحد، يهمس به في أذن كل متدبر: <b>S = W × B</b>.',
        'From the atom that unites by attraction and stabilizes by repulsion, to the cell that protects itself and attacks intruders, to chemistry where atoms unite and need "activation energy" to break old bonds – its repentance – to societies gathered by values and protected from corruption... everything in this existence screams one law, whispering in the ear of every contemplator: <b>S = W x B</b>.'
        )}</p>

        <p style="color:#FFD700;font-size:1.1em;font-weight:bold;text-align:center;margin:20px 0;">{TXT(
        '🧭 ما هو هذا القانون؟ ولماذا هو ضرب وليس جمع؟',
        '🧭 What is this law? And why is it multiplication, not addition?'
        )}</p>

        <p>{TXT(
        '<b>W (الولاء لله وأوليائه):</b> قوة الجذب نحو الحق. هي طاقة الحب والطاعة والنصرة، توجهها إلى الله ورسوله والمؤمنين. <b>B (البراءة من الطاغوت وأوليائه):</b> قوة التنافر عن الباطل. هي طاقة البغض والمفاصلة، تصرفها عن كل ما يعبد من دون الله. <b>S (الثبات الوجودي):</b> حاصل ضربهما معاً. إنها معادلة <b>ضرب لا جمع</b>، لأن القلب لا يجتمع فيه ولاءان، ولأن الثبات لا يقوم إلا على ركنين، ولأن انعدام أحدهما يعني انهيار الكل مهما بلغ الآخر. هل عرفت الآن لماذا يسقط المنافق؟ ولماذا يفشل المتردد؟ ولماذا ينتصر الصادق؟ هذا هو <b>"الدين القيم"</b> الذي فطر الله الناس عليه، وهذا هو <b>"الإسلام الحنيف"</b> الذي هو الاستجابة الديناميكية الحية لهذا القانون في كل زمان ومكان.',
        '<b>W (Loyalty to Allah & His allies):</b> The force of attraction to truth. <b>B (Disavowal of Taghut & its allies):</b> The force of repulsion from falsehood. <b>S (Existential Stability):</b> Their product. It is <b>multiplication, not addition</b>, because a heart cannot contain two loyalties, because stability only rests on two pillars, and because the absence of one means the collapse of the whole no matter how high the other. Do you now see why the hypocrite falls? Why the hesitant fails? Why the sincere triumphs? This is <b>"Al-Deen Al-Qayyim"</b> upon which Allah created people, and this is <b>"Al-Islam Al-Hanif"</b>, the dynamic, living response to this law in every time and place.'
        )}</p>

        <p style="color:#FFD700;font-size:1.1em;font-weight:bold;text-align:center;margin:20px 0;">{TXT(
        '🕋 هل مشى هذا الطريق أحد قبلك؟ أم أنك أول السالكين؟',
        '🕋 Has anyone walked this path before you? Or are you the first traveler?'
        )}</p>

        <p>{TXT(
        'لم تكن هذه المعادلة مجرد نظرية بشرية اخترعها عقل فيلسوف، ولا كشفاً رياضياً توصل إليه عالم في معمله. لقد <b>جسّدها بشرٌ صدقوا ما عاهدوا الله عليه</b>، رجالاً ونساءً، في كل الظروف والأحوال. على رأسهم وإمامهم <b>محمد</b> صلى الله عليه وعلى آله وسلم، خاتم النبيين وسيد المرسلين، الأسوة العظمى والقدوة المثلى، الذي قال مؤصلاً لهذا القانون: "أوثق عرى الإيمان: الحب في الله، والبغض في الله". ثم <b>إبراهيم</b> خليل الله، الذي أعلنها في وجه أبيه وقومه: "إنني براء مما تعبدون". و<b>موسى</b> كليم الله، الذي وقف في وجه الطاغوت السياسي. و<b>يوسف</b> الصديق، الذي اختار السجن على المعصية. و<b>أصحاب الكهف</b> الفتية، الذين اعتزلوا مجتمعهم الفاسد. و<b>علي والحسن والحسين</b>، الذين جسّدوا قمم الثبات في أقسى الفتن. و<b>أم موسى</b> التي ألقت بولدها في اليم ثقةً بوعد الله: "إنا رادوه إليك". و<b>آسيا امرأة فرعون</b> التي قالت تحت التعذيب: "رب ابن لي عندك بيتاً في الجنة"، متبرئةً من مُلك الطاغوت. <b>هؤلاء ليسوا من عالم الملائكة</b>. هم بشرٌ مثلنا، أكلوا الطعام ومشوا في الأسواق. ولكنهم عرفوا ما فضلهم الله به، وما أكرمهم به كبشر، فعملوا بهذا القانون، فارتقوا إلى أعلى عليين. <b>فهل تسير على آثارهم؟</b>',
        'This equation was not merely a human theory invented by a philosopher\'s mind. It was <b>embodied by humans who were true to their covenant with Allah</b>, men and women, in all circumstances. <b>These were not angels.</b> They were humans like us. But they recognized what Allah had favored them with, so they acted upon this law, and ascended to the highest of heights. <b>Will you walk in their footsteps?</b>'
        )}</p>

        <p style="color:#FFD700;font-weight:bold;text-align:center;font-size:1.1em;margin:25px 0;">{TXT(
        '🧪 هذه المنصة ليست كتاباً ولا تطبيقاً. إنها مختبر. مختبرٌ لتكتشف فيه موقعك، وتشخص فيه داءك، وتجد فيه دواءك. ولتنتقل من ظنك الهوى إلى طمأنينة الهدى، ومن شتات الفكر إلى نظام الدين، ومن ظلمات الحيرة إلى نور اليقين. فهل أنت مستعد؟',
        '🧪 This platform is not a book nor an app. It is a lab. A lab for you to discover your position, diagnose your ailment, and find your remedy. To move from the conjecture of desire to the tranquility of guidance, from the fragmentation of thought to the system of the Deen, from the darkness of confusion to the light of certainty. Are you ready?'
        )}</p>
        
        <p style="text-align:center;color:#FFD700;font-size:1.4em;font-weight:bold;margin:25px 0;">S = W × B</p>
        
        <p style="text-align:center;font-style:italic;color:#AAA;font-size:1.1em;line-height:2.2;">{TXT(
        'هذا المختبر ليس بديلاً عن الوحي، بل هو شاهد من عالم الشهادة على صدق عالم الغيب. ﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ تَبَارَكَ اللَّهُ رَبُّ الْعَالَمِينَ﴾. إنه تحقيق لقوله تعالى: ﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ حَتَّىٰ يَتَبَيَّنَ لَهُمْ أَنَّهُ الْحَقُّ﴾. إنه محاولة متواضعة لنريك كيف يلتقي كتاب الله المسطور بكتابه المنظور، على ميزان واحد. فإن رأيت الحق فيه، فاحمد الله الذي هداك. وإن وجدت فيه نقصاً، فاعلم أنه من صنع البشر، ولا يضير الحق نقص في التعبير عنه.',
        'This lab is not a substitute for revelation, but a witness from the seen world to the truth of the unseen. ﴿Unquestionably, to Him belongs the creation and the command; blessed is Allah, Lord of the worlds.﴾ It is a fulfillment of His promise: ﴿We will show them Our signs in the horizons and within themselves until it becomes clear to them that it is the truth.﴾ It is a humble attempt to show you how Allah\'s written Book meets His observed Book, on a single balance. If you see truth in it, praise Allah who guided you. If you find deficiency, know that it is human craft, and the truth is not harmed by deficiency in its expression.'
        )}</p>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # ٢. دليل المستخدم
    # ─────────────────────────────────────────
    with st.expander(TXT("📖 دليل المستخدم – كيف تبحر في هذا المختبر؟", "📖 User Guide – How to Navigate This Lab?"), expanded=False):
        st.markdown(TXT("""
        ### 🎯 كيف تستخدم هذا المختبر؟

        **١. البوصلة:** أجب عن ١٩ سؤالاً لتعرف موقعك الدقيق في فضاء القيم (W, B). ستكتشف إن كنت في دائرة المؤمنين، أم المغضوب عليهم، أم الضالين، أم المنافقين.
        **٢. مختبر الأمة:** استخدم المنزلقات أو الذكاء الاصطناعي لتحليل أي دولة أو مجتمع، وشاهد كيف تنطبق المعادلة عليه في الزمن الحقيقي.
        **٣. المشهد الكوني:** شاهد تفاعل مئات "النجوم" (الأفراد) مع قطبي الميزان. النجوم الذهبية هي المتوازنة، والحمراء هي المنحرفة.
        **٤. محاكي المجتمع:** شاهد كيف يترابط الأفراد المتوازنون (S عالٍ) وينفرط عقد غير المتوازنين. المجتمع كخلية حية.
        **٥. المرصد العالمي:** شاهد تطبيق المعادلة على أكثر من 80 دولة حول العالم. من هي الدول الذهبية؟ ومن في حالة الاستدراج؟
        **٦. طبيب القلوب:** أجب عن 5 أسئلة بصدق، تحصل على تشخيص دقيق لقلبك، وروشتة علاجية من الكتاب والسنة.
        **٧. شبكة الناجين:** انضم إلى "حبل الله" الرقمي. تواصل مع المؤمنين الثابتين، واجعل لك رفيقاً في طريق الصراط.
        **٨. جامعة الميزان:** تعلم نظرية "الدين القيم" عبر 3 دورات تفاعلية قصيرة، واحصل على شهاداتك.
        **٩. مدرسة آل البيت:** نماذج الثبات في الفتنة: الإمام علي، الحسن، الحسين. تعلم من سيرهم كيف تكون S = 1.
        **١٠. هندسة الصراط المستقيم:** شاهد نموذج إبراهيم عليه السلام (الخط المستقيم κ = 0)، وتتبع مسارك نحو مقامه.
        **١١. الدليل المرجعي والمعجم الهندسي:** كل ما تحتاجه من آيات جامعات، ومفاتيح لغوية، ودورة إلهية، وميزان ذهبي، ومعجم الحروف، وأسرارها في مرجع واحد.

        **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
        """,
        """
        ### 🎯 How to Use This Lab

        **1. Compass:** Answer 19 questions to discover your exact position in the values space (W, B).
        **2. Nation Lab:** Use sliders or AI to analyze any nation or community.
        **3. Cosmic Scene:** Watch hundreds of "stars" (individuals) interact with the two poles of the balance.
        **4. Social Fabric:** See how balanced individuals link up and the unbalanced fall apart.
        **5. Global Observatory:** Apply the equation to 80+ nations. Who is golden, and who is in Istidraj?
        **6. Heart Healer:** Answer 5 questions honestly, get a precise diagnosis and a prescription from Quran and Sunnah.
        **7. Survivors Network:** Join the digital "Rope of Allah". Connect with steadfast believers.
        **8. Mizan University:** Learn the theory through 3 short interactive courses and earn certificates.
        **9. Ahlul Bayt School:** Models of stability in strife: Imam Ali, Hassan, Hussein.
        **10. Geometry of the Straight Path:** See the Abrahamic model (κ = 0) and trace your path to his station.
        **11. Reference Guide & Lexicon:** Key verses, linguistic keys, divine cycle, golden criterion, lexicon, and letter secrets.

        **Central Equation:** **S = W x B** (multiplication, not addition).
        """))
