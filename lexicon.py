# mizan/lexicon.py
"""
المعجم الهندسي للقرآن – النسخة النهائية الشاملة
يجمع بين: قدسية الوحي، دقة العلم، عمق الفلسفة، حكمة التاريخ، وتواضع العارفين
"""

import streamlit as st
import pandas as pd
from config import TXT, LETTERS_DB

def render_lexicon():
    st.header(TXT("📖 المعجم الهندسي للقرآن", "📖 The Geometric Lexicon of the Quran"))
    
    # ─────────────────────────────────────────
    # مقدمة: روح المعجم
    # ─────────────────────────────────────────
    with st.expander(TXT("🕋 مقدمة: روح المعجم", "🕋 Introduction: The Spirit of the Lexicon"), expanded=True):
        st.markdown(TXT(
            """
            ### ﴿كِتَابٌ أُحْكِمَتْ آيَاتُهُ ثُمَّ فُصِّلَتْ مِن لَّدُنْ حَكِيمٍ خَبِيرٍ﴾ [هود: ١]
            
            هذا المعجم ليس مجرد جدول حروف وأرقام. إنه محاولة متواضعة لقراءة **الوجه الهندسي للوحي**. 
            فكما أن للكون لغة رياضية (الفيزياء)، فللقرآن لغة رياضية (حساب الجمل والتصنيف الوجودي).
            
            **نحن لا ندّعي الإحاطة، بل نقرع الباب.** نحن لا نزعم أننا فككنا الشفرة، بل نقول: 
            "هذا ما فهمناه، وهذا ما انتهى إليه اجتهادنا، فإن كان صواباً فمن الله، وإن كان خطأً فمن أنفسنا".
            
            **المصادر التي استندنا إليها:**
            - **الوحي:** القرآن الكريم، والسنة النبوية المطهرة.
            - **العقل:** قواعد المنطق والرياضيات (حساب الجمل، النسب، المعادلات).
            - **الكون:** تجليات القانون الواحد في الفيزياء والكيمياء والبيولوجيا.
            - **التاريخ:** سنن الله في صعود الحضارات وسقوطها.
            - **الفطرة:** ما استقر في قلوب العارفين من تواضع أمام عظمة الخالق.
            """,
            """
            ### ﴿A Book whose verses are perfected and then presented in detail from [one who is] Wise and Acquainted.﴾ [Hud: 1]
            
            This lexicon is not merely a table of letters and numbers. It is a humble attempt to read **the geometric face of revelation**.
            Just as the universe has a mathematical language (physics), the Quran has a mathematical language (Abjad numerology and existential classification).
            
            **We do not claim comprehensive knowledge; we are merely knocking on the door.** We do not claim to have cracked the code; rather, we say:
            "This is what we have understood, and this is what our efforts have reached. If it is correct, it is from Allah; if it is wrong, it is from ourselves."
            
            **Sources we relied upon:**
            - **Revelation:** The Holy Quran and the purified Sunnah.
            - **Reason:** Logic and mathematics (Abjad calculation, proportions, equations).
            - **The Universe:** Manifestations of the One Law in physics, chemistry, and biology.
            - **History:** Allah's laws in the rise and fall of civilizations.
            - **Innate Nature:** What resides in the hearts of the wise: humility before the greatness of the Creator.
            """
        ))

    # ─────────────────────────────────────────
    # الباب الأول: أصل النظام – نظام أبجد هوز
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🏛️ الباب الأول: أصل النظام", "🏛️ Chapter One: The Origin of the System"))
    
    with st.expander(TXT("١. نظام أبجد هوز – أساس حساب الجمل", "1. The Abjad Hawaz System – Foundation of Gematria"), expanded=False):
        st.markdown(TXT(
            """
            ### أصل النظام وتاريخه
            
            نظام "أبجد هوز" هو نظام عددي استخدمه العرب قبل الإسلام، حيث يُعطى كل حرف من الحروف الأبجدية قيمة عددية ثابتة.
            وقد استخدم هذا النظام في التأريخ للأحداث، وفي بعض العلوم الإسلامية. ونحن نستخدمه هنا ليس كـ "دليل مستقل"،
            بل كـ **أداة لفهم البنية الرياضية** التي أشار إليها القرآن في فواتح السور (الحروف المقطعة).
            
            ### الجدول الأساسي لنظام أبجد هوز
            
            | المجموعة | الحروف | القيم |
            |:---|:---|:---|
            | **الآحاد** | أ ب ج د هـ و ز ح ط | 1 2 3 4 5 6 7 8 9 |
            | **العشرات** | ي ك ل م ن س ع ف ص | 10 20 30 40 50 60 70 80 90 |
            | **المئات** | ق ر ش ت ث خ ذ ض ظ | 100 200 300 400 500 600 700 800 900 |
            | **الألف** | غ | 1000 |
            
            > **تنبيه منهجي:** هذا الجدول ليس "اختراعاً" شخصياً. إنه جزء من التراث اللغوي العربي.
            > ونحن نستخدم هذه القيم كمُدخلات في نظام حاسوبي حي، لا كأدلة مستقلة.
            """,
            """
            ### The Origin and History of the System
            
            The "Abjad Hawaz" system is a numerical system used by Arabs before Islam, where each letter of the alphabet is assigned a fixed numerical value.
            We use it here not as an "independent proof", but as a **tool for understanding the mathematical structure** indicated by the Quran in the openings of its chapters (the disjointed letters).
            
            ### The Basic Table of the Abjad Hawaz System
            
            | Group | Letters | Values |
            |:---|:---|:---|
            | **Units** | أ ب ج د هـ و ز ح ط | 1 2 3 4 5 6 7 8 9 |
            | **Tens** | ي ك ل م ن س ع ف ص | 10 20 30 40 50 60 70 80 90 |
            | **Hundreds** | ق ر ش ت ث خ ذ ض ظ | 100 200 300 400 500 600 700 800 900 |
            | **Thousands** | غ | 1000 |
            
            > **Methodological Note:** This table is not a personal "invention". It is part of the Arabic linguistic heritage.
            > We use these values as inputs in a live computational system, not as independent proofs.
            """
        ))

    # ─────────────────────────────────────────
    # الباب الثاني: التصنيف الوجودي للحروف
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🔬 الباب الثاني: التصنيف الوجودي للحروف", "🔬 Chapter Two: The Existential Classification of Letters"))

    with st.expander(TXT("٢. الفئات الست – منطق التصنيف", "2. The Six Categories – Logic of Classification"), expanded=False):
        st.markdown(TXT(
            """
            ### لماذا ست فئات؟
            
            العدد **ستة** له دلالة قرآنية عميقة: ﴿وَلَقَدْ خَلَقْنَا السَّمَاوَاتِ وَالْأَرْضَ وَمَا بَيْنَهُمَا فِي سِتَّةِ أَيَّامٍ﴾ [ق: ٣٨].
            وكما أن الخلق تم في ستة أيام، فكذلك الكلام الإلهي (القرآن) يحمل في طياته نظاماً سداسياً.
            
            **كل حرف** من الحروف الثمانية والعشرين له:
            - **قيمة عددية** (حساب الجمل).
            - **تصنيف وجودي** (موقعه في نظام الوجود).
            - **دور رياضي** (كيف يؤثر في معادلة S = W × B).
            
            ### الفئات الست:
            
            | الفئة | الوصف | عدد الحروف |
            |:---|:---|:---|
            | **الأولى: الذات الإلهية (المصدر)** | حروف تمثل صفات الله الخاصة. هي "المصدر" الذي تنبثق منه كل الصفات. | 2 |
            | **الثانية: الازدواج** | حروف لها وجهان: وجه إلى الله ثابت، ووجه إلى الخلق متغير. | 2 |
            | **الثالثة: التجلي الإلهي** | حروف تمثل صفات الله المتجلية في خلقه. تكرارها في الفواتح كثير. | 7 |
            | **الرابعة: الاشتراك (الجسور)** | حروف تمثل القنوات التي تربط عالم الغيب بعالم الشهادة. | 3 |
            | **الخامسة: المشغلات** | حروف تمثل أدوات المنطق والسببية في كلام الله. | 4 |
            | **السادسة: أعمال الخلق** | حروف تمثل صفات وأفعال خاصة بالخلق، ذات وجهين (±). | 10 |
            """,
            """
            ### Why Six Categories?
            
            The number **six** has a profound Quranic significance: ﴿And We certainly created the heavens and the earth and whatever is between them in six days.﴾ [Qaf: 38].
            Just as creation was completed in six days, divine speech (the Quran) carries within it a sixfold system.
            
            **Each letter** of the twenty-eight has:
            - **A numerical value** (Abjad gematria).
            - **An existential classification** (its position in the system of existence).
            - **A mathematical role** (how it affects the equation S = W × B).
            
            ### The Six Categories:
            
            | Category | Description | Number of Letters |
            |:---|:---|:---|
            | **First: Divine Essence (Source)** | Letters representing Allah's exclusive attributes. The "Source" from which all attributes emanate. | 2 |
            | **Second: Duality** | Letters with two faces: one fixed towards Allah, one variable towards creation. | 2 |
            | **Third: Divine Manifestation** | Letters representing Allah's attributes manifested in His creation. Their frequency in Quranic openings is high. | 7 |
            | **Fourth: Connection (Bridges)** | Letters representing the channels connecting the Unseen world with the Seen world. | 3 |
            | **Fifth: Operators** | Letters representing logical and causal tools in Allah's speech. | 4 |
            | **Sixth: Actions of Creation** | Letters representing qualities and actions specific to creation, with two faces (±). | 10 |
            """
        ))

    # ─────────────────────────────────────────
    # الباب الثالث: تفصيل الفئات الست
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("📊 الباب الثالث: تفصيل الفئات الست", "📊 Chapter Three: Detailing the Six Categories"))

    # تفصيل الفئات
    categories_detail = [
        {
            "name": TXT("الفئة الأولى: الذات الإلهية (المصدر)", "Category 1: Divine Essence (Source)"),
            "icon": "🔆",
            "letters": [
                {"letter": "ك", "value": 20, "attribute": TXT("الأمر (كُن)", "The Command (Be)"), "verse": "﴿إِنَّمَا أَمْرُهُ إِذَا أَرَادَ شَيْئًا أَنْ يَقُولَ لَهُ كُنْ فَيَكُونُ﴾ [يس: ٨٢]"},
                {"letter": "ن", "value": 50, "attribute": TXT("النور الذاتي", "The Intrinsic Light"), "verse": "﴿اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ﴾ [النور: ٣٥]"},
            ],
            "secret": TXT(
                "**المعادلة الأولى للوجود:** ك + ن = ع (20 + 50 = 70). الأمر + النور = الإدراك. الوجود لا يُدرك إلا بالنور.",
                "**The First Equation of Existence:** K + N = A (20 + 50 = 70). Command + Light = Perception. Existence is only perceived through light."
            )
        },
        {
            "name": TXT("الفئة الثانية: الازدواج", "Category 2: Duality"),
            "icon": "⚖️",
            "letters": [
                {"letter": "ق", "value": 100, "attribute": TXT("الثابت: الميزان / المتجلي: القسط والعدل", "Fixed: The Balance / Manifest: Justice"), "verse": "﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ [الرحمن: ٧]"},
                {"letter": "ص", "value": 90, "attribute": TXT("الثابت: الصمد / المتجلي: الصبر والصدق", "Fixed: The Eternal / Manifest: Patience & Truthfulness"), "verse": "﴿ص ۚ وَالْقُرْآنِ ذِي الذِّكْرِ﴾ [ص: ١]"},
            ],
            "secret": TXT(
                "للقاف وجهان: وجه إلى الله (الحق، القيوم) ووجه إلى الخلق (القسط، الدين القيم). وقيمته 100 تمثل تمام العدل وكمال الميزان.",
                "Qaf has two faces: one towards Allah (The Truth, The Self-Subsisting) and one towards creation (Justice, The Upright Religion). Its value 100 represents perfect justice."
            )
        },
        {
            "name": TXT("الفئة الثالثة: التجلي الإلهي", "Category 3: Divine Manifestation"),
            "icon": "🌟",
            "letters": [
                {"letter": "أ", "value": 1, "attribute": TXT("الوحدانية", "Oneness"), "freq": 13},
                {"letter": "ل", "value": 30, "attribute": TXT("المُلك والعدل", "Kingship & Justice"), "freq": 13},
                {"letter": "م", "value": 40, "attribute": TXT("الجمع والتماسك", "Gathering & Cohesion"), "freq": 17},
                {"letter": "ر", "value": 200, "attribute": TXT("اليقظة والمراقبة", "Wakefulness & Watchfulness"), "freq": 6},
                {"letter": "س", "value": 60, "attribute": TXT("السمع والاستجابة", "Hearing & Response"), "freq": 5},
                {"letter": "ح", "value": 8, "attribute": TXT("الحياة والاستدامة", "Life & Sustainability"), "freq": 7},
                {"letter": "ط", "value": 9, "attribute": TXT("الطهارة والمناعة", "Purity & Immunity"), "freq": 4},
            ],
            "secret": TXT(
                "الألف (1) يتكرر 13 مرة: الوحدانية في الكثرة. والميم (40) الأكثر تكراراً (17): سر الجمع والتماسك. هذه الحروف ترفع W وB في المعادلة.",
                "Alif (1) appears 13 times: Oneness in multiplicity. Meem (40) is the most frequent (17): the secret of gathering. These letters raise W and B in the equation."
            )
        },
        {
            "name": TXT("الفئة الرابعة: الاشتراك (الجسور)", "Category 4: Connection (Bridges)"),
            "icon": "🌉",
            "letters": [
                {"letter": "ع", "value": 70, "attribute": TXT("جسر الإدراك والرؤية", "Bridge of Perception"), "desc": TXT("يربط عالم الغيب بعالم الشهادة عبر الإدراك", "Connects the Unseen with the Seen through perception")},
                {"letter": "ي", "value": 10, "attribute": TXT("جسر النداء والنسبة", "Bridge of Calling & Belonging"), "desc": TXT("يربط العبد بربه عبر الدعاء (يا رب) والوحي (يا أيها)", "Connects servant to Lord through supplication and revelation")},
                {"letter": "هـ", "value": 5, "attribute": TXT("جسر الهوية والحضور", "Bridge of Identity & Presence"), "desc": TXT("يحدد هوية الشيء: هو الله، هم المهتدون", "Determines identity: He is Allah, they are the guided")},
            ],
            "secret": TXT(
                "هذه الحروف تشكل سلسلة: ك+ن=ع (المصدر ينتج الإدراك)، ع+ي=الاستجابة (الإدراك يثمر النداء)، ي+هـ=الهوية (النداء يثبت الهوية).",
                "These letters form a chain: K+N=A (source produces perception), A+Y=response (perception bears calling), Y+H=identity (calling establishes identity)."
            )
        },
        {
            "name": TXT("الفئة الخامسة: المشغلات", "Category 5: Operators"),
            "icon": "⚡",
            "letters": [
                {"letter": "ف", "value": 80, "symbol": "=", "role": TXT("فاء السببية: تربط السبب بالنتيجة حتماً", "Causative Fa: links cause to effect inevitably")},
                {"letter": "و", "value": 6, "symbol": "× / +", "role": TXT("واو العطف: تجمع بين طرفين (ضرباً أو جمعاً)", "Conjunctive Waw: combines two sides (multiplication or addition)")},
                {"letter": "ب", "value": 2, "symbol": TXT("بـ", "by"), "role": TXT("باء الاستعانة: أداة التوسل", "Instrumental Ba: the tool of seeking help")},
                {"letter": "ل", "value": 30, "symbol": "→", "role": TXT("لام التعليل: سهم يوضح اتجاه الغاية", "Purposive Lam: an arrow clarifying the direction of purpose")},
            ],
            "secret": TXT(
                "هذه الحروف هي 'أوامر التشغيل' في لغة القرآن. 'ف' تخبرك أن ما قبلها سبب وما بعدها نتيجة. 'و' تخبرك أن تجمع بين شيئين. 'ب' تخبرك أن تستعين. 'ل' تخبرك عن الغاية. إنها مشغلات المعادلة الكونية.",
                "These letters are the 'operating commands' in the Quranic language. 'F' tells you the cause and effect. 'W' tells you to combine. 'B' tells you to seek help. 'L' tells you the purpose. They are the operators of the cosmic equation."
            )
        },
        {
            "name": TXT("الفئة السادسة: أعمال الخلق", "Category 6: Actions of Creation"),
            "icon": "🧬",
            "letters": [
                {"letter": "ج", "value": 3, "positive": TXT("الجهاد، الجود", "Striving, Generosity"), "negative": TXT("الجهل، الجحود", "Ignorance, Ingratitude")},
                {"letter": "خ", "value": 600, "positive": TXT("الخير، الخشية", "Goodness, Awe"), "negative": TXT("الخيانة، الخذلان", "Betrayal, Abandonment")},
                {"letter": "ت", "value": 400, "positive": TXT("التوبة، التقوى", "Repentance, Piety"), "negative": TXT("التيه", "Arrogance, Loss")},
                {"letter": "ش", "value": 300, "positive": TXT("الشكر، الشجاعة", "Gratitude, Courage"), "negative": TXT("الشهوة، الشرك", "Lust, Polytheism")},
                {"letter": "غ", "value": 1000, "positive": TXT("الغفران", "Forgiveness"), "negative": TXT("الغل", "Malice")},
            ],
            "secret": TXT(
                "هذه الحروف تمثل الإرادة البشرية الحرة. قيمها تحددها اختيارات الإنسان (±). وهي وحدها القادرة على رفع S أو خفضه بشكل كبير، لأنها ثمرة الامتحان.",
                "These letters represent free human will. Their values are determined by human choices (±). They alone can significantly raise or lower S, because they are the fruit of the test."
            )
        },
    ]

    for cat in categories_detail:
        with st.expander(f"{cat['icon']} **{cat['name']}**", expanded=False):
            st.markdown(TXT("#### الحروف:", "#### Letters:"))
            for l in cat['letters']:
                st.markdown(f"- **{l['letter']}** = {l['value']} ({l.get('attribute', l.get('desc', ''))})")
            if 'secret' in cat:
                st.info(cat['secret'])

    # ─────────────────────────────────────────
    # الباب الرابع: أسرار الحروف – تأملات عميقة
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🔍 الباب الرابع: أسرار الحروف – تأملات عميقة", "🔍 Chapter Four: Secrets of the Letters – Deep Reflections"))

    # سر الألف
    with st.expander(TXT("🌟 سر الألف (ا = 1): الوحدانية في الكثرة", "🌟 The Secret of Alif (ا = 1): Oneness in Multiplicity"), expanded=False):
        st.markdown(TXT(
            """
            **القيمة 1 = الوحدانية المطلقة.**
            **التكرار 13 مرة في فواتح السور = التجلي في عالم الكثرة (الخلق).**
            
            هذا ليس تناقضاً، بل هو السر الأعظم:
            - الله واحد في ذاته (قيمته 1)، ولكنه متجلي في خلقه (تكراره 13).
            - الـ 1 لا يتجزأ، ولكنه يظهر في كل مكان.
            - الألف هو الحرف الوحيد الذي لا ينطق بذاته (لا حركة له)، ومع ذلك هو أساس كل كلمة.
            - إنه مثل "الله": لا تدركه الأبصار، ولكن كل شيء يدل عليه.
            
            **العلاقة مع الأسماء الحسنى:**
            الألف هو حرف "الأحد"، "الأول"، "الآخر"، "الظاهر"، "الباطن".
            قيمته 1، لأنه واحد في كل هذه الأسماء، لا شريك له.
            
            > **تأمل:** كما أن الألف لا يُنطق به وحده، بل يحتاج إلى غيره ليظهر، فكذلك الله: لا يُرى في الدنيا، ولكن آثاره في كل مكان.
            """,
            """
            **Value 1 = Absolute Oneness.**
            **Frequency 13 in Quranic openings = Manifestation in the world of multiplicity.**
            
            This is the greatest secret:
            - Allah is One in His Essence (value 1), yet manifested in His creation (frequency 13).
            - The 1 is indivisible, yet appears everywhere.
            - Alif has no sound of its own, yet it is the basis of every word.
            - It is like "Allah": vision does not perceive Him, yet everything points to Him.
            
            **Relation to the Beautiful Names:**
            Alif is the letter of "The One", "The First", "The Last", "The Manifest", "The Hidden".
            
            > **Reflection:** Just as Alif cannot be pronounced alone but needs others to appear, so too Allah is not seen in this world, but His signs are everywhere.
            """
        ))

    # سر منظومة (الم)
    with st.expander(TXT("🕋 منظومة (الم): البصمة الصوتية لاسم الله", "🕋 The (ALM) System: The Sound Signature of Allah"), expanded=False):
        st.markdown(TXT(
            """
            الحروف الثلاثة (ا، ل، م) هي "البصمة الصوتية" لأعظم اسم: **الله**.
            والقرآن يفتتح بها 6 سور (بعدد أيام الخلق)، لأنها "أم الكتاب" و"أم الأسماء".
            
            انظر كيف تتجلى هذه الحروف في أسماء الله وصفاته:
            
            | الحرف | الرمز | أمثلة من أسماء الله التي تبدأ به | معانيها |
            |:---|:---|:---|:---|
            | **أ** | الوحدانية، البداية | الأحد، الأول، الآخر | أصل كل شيء |
            | **ل** | المُلك، اللطف، العدل | الملك، اللطيف، العدل، الحليم | الله هو المَلِك |
            | **م** | الجمع، العطاء، المنع | المعطي، المانع، المحيي، المميت | أسماء الأفعال |
            
            عندما تقرأ "الم"، فأنت تستحضر كل هذه الأسماء. ولهذا كان النبي ﷺ يقول:
            "لا أقول الم حرف، ولكن ألف حرف، ولام حرف، وميم حرف". لأن كل حرف منها كنز من الأسماء.
            """,
            """
            The three letters (A, L, M) are the "sound signature" of the greatest name: **Allah**.
            The Quran opens with them in 6 suras (the days of creation), because they are "the mother of the book" and "the mother of names".
            
            | Letter | Symbol | Examples of Allah's Names | Meanings |
            |:---|:---|:---|:---|
            | **A** | Oneness | The One, The First, The Last | Origin of all |
            | **L** | Kingship | The King, The Subtle, The Just | Allah is the King |
            | **M** | Giving | The Giver, The Withholder | Names of actions |
            
            When you recite "ALM", you evoke all these names. Hence the Prophet ﷺ said:
            "I do not say ALM is one letter, but Alif is a letter, Lam is a letter, and Meem is a letter."
            """
        ))

    # سر حرف القاف
    with st.expander(TXT("⚖️ سر حرف القاف (ق = 100): حرف الميزان", "⚖️ The Secret of Qaf (ق = 100): The Letter of the Balance"), expanded=False):
        st.markdown(TXT(
            """
            حرف **القاف** هو حرف "الحق" و"القيوم" و"القسط" و"الدِّينُ القَيِّم". قيمته 100 هي كمال العدد وأساس النسب.
            
            للقاف وجهان:
            - **وجه ثابت في الذات الإلهية:** ﴿الْحَقُّ﴾، ﴿الْقَيُّومُ﴾. وهذا ثابت لا يتغير.
            - **وجه متجلي في الخلق:** ﴿الْقِسْطُ﴾ (العدل)، ﴿الدِّينُ الْقَيِّمُ﴾. وهذا ما أُمر الناس بإقامته.
            
            و"الدِّينُ الْقَيِّمُ" هو القانون الإلهي الحق الثابت، ميزان الله الذي فطر الناس عليه، والذي لا تبديل فيه.
            
            > **تأمل:** القاف في "الحق" (مكسورة) تدل على الثبات. والقاف في "القسط" (ساكنة) تدل على التجلي. الحركة فرق!
            """,
            """
            The letter **Qaf** is the letter of "The Truth", "The Self-Subsisting", "Justice", and "The Upright Religion". Its value 100 is numerical perfection.
            
            Qaf has two faces:
            - **Fixed in the Divine Essence:** "The Truth", "The Self-Subsisting". Unchanging.
            - **Manifested in creation:** "Justice", "The Upright Religion". Commanded to be established.
            
            "Ad-Deen Al-Qayyim" is the divine law, the balance of Allah upon which people were created, with no alteration.
            
            > **Reflection:** The Qaf in "Al-Haqq" (with kasra) indicates fixity. The Qaf in "Al-Qist" (with sukun) indicates manifestation. The vowel makes the difference!
            """
        ))

    # سر حرف التاء
    with st.expander(TXT("🅃 سر حرف التاء (ت = 400): حرف القرار والمصير", "🅃 The Secret of Taa (ت = 400): The Letter of Decision"), expanded=False):
        st.markdown(TXT(
            """
            حرف **التاء** هو حرف **الاتخاذ** و**التبعية**. قيمته 400 تشير إلى ثقل الاختيار.
            
            **الاتخاذ الإيجابي (الولاء):**
            > ﴿وَاتَّخَذَ اللَّهُ إِبْرَاهِيمَ خَلِيلًا﴾ [النساء: ١٢٥]
            
            **الاتخاذ السلبي (الولاء للطاغوت):**
            > ﴿أَفَرَأَيْتَ مَنِ اتَّخَذَ إِلَٰهَهُ هَوَاهُ﴾ [الجاثية: ٢٣]
            > ﴿وَالَّذِينَ اتَّخَذُوا مِن دُونِهِ أَوْلِيَاءَ﴾ [الزمر: ٣]
            
            **التبعية الإيجابية:**
            > ﴿وَاتَّبِعْ مِلَّةَ إِبْرَاهِيمَ حَنِيفًا﴾ [النحل: ١٢٣]
            
            **التبعية السلبية:**
            > ﴿قَالُوا بَلْ نَتَّبِعُ مَا وَجَدْنَا عَلَيْهِ آبَاءَنَا﴾ [البقرة: ١٧٠]
            
            التاء هو حرف القرار. إما أن تتخذ الله وأولياءه، وإما أن تتخذ الطاغوت. إما أن تتبع ملة إبراهيم، وإما أن تتبع الأهواء. وهذا هو جوهر معادلة الميزان: **S = W × B**.
            """,
            """
            The letter **Taa** is the letter of **taking (ittikhaadh)** and **following (ittibaa')**. Its value 400 indicates the weight of choice.
            
            **Positive Taking (Loyalty):** ﴿And Allah took Abraham as a friend.﴾
            **Negative Taking (Taghut):** ﴿Have you seen the one who takes his desire as his god?﴾
            **Positive Following:** ﴿And follow the way of Abraham.﴾
            **Negative Following:** ﴿They said, "Rather, we will follow that which we found our fathers doing."﴾
            
            Taa is the letter of decision. Either you take Allah and His allies, or you take Taghut. This is the essence of the Mizan equation: **S = W × B**.
            """
        ))

    # ─────────────────────────────────────────
    # الباب الخامس: جدول الحروف الكامل
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("📋 الباب الخامس: جدول الحروف الكامل", "📋 Chapter Five: The Complete Letter Table"))

    with st.expander(TXT("🗂️ الجدول الكامل للحروف الثمانية والعشرين", "🗂️ Complete Table of the 28 Letters"), expanded=False):
        all_letters = [
            ("ك", 20, TXT("الذات الإلهية", "Divine Essence"), TXT("الأمر (كُن)", "The Command (Be)"), TXT("ثابت", "Constant")),
            ("ن", 50, TXT("الذات الإلهية", "Divine Essence"), TXT("النور الذاتي", "Intrinsic Light"), TXT("ثابت", "Constant")),
            ("ق", 100, TXT("الازدواج", "Duality"), TXT("الميزان / القسط", "Balance / Justice"), TXT("ثابت/متغير", "Fixed/Variable")),
            ("ص", 90, TXT("الازدواج", "Duality"), TXT("الصمد / الصبر", "Eternal / Patience"), TXT("ثابت/متغير", "Fixed/Variable")),
            ("أ", 1, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("الوحدانية", "Oneness"), TXT("مُوَلِّد W", "W Generator")),
            ("ل", 30, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("المُلك والعدل", "Kingship & Justice"), TXT("مُوَلِّد B", "B Generator")),
            ("م", 40, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("الجمع", "Gathering"), TXT("مُوَلِّد S", "S Generator")),
            ("ر", 200, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("اليقظة", "Wakefulness"), TXT("مُوَلِّد المقاومة", "Resistance Generator")),
            ("س", 60, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("السمع", "Hearing"), TXT("مُوَلِّد الاستجابة", "Response Generator")),
            ("ح", 8, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("الحياة", "Life"), TXT("مُوَلِّد الاستدامة", "Sustainability Gen.")),
            ("ط", 9, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("الطهارة", "Purity"), TXT("مُوَلِّد المناعة", "Immunity Generator")),
            ("ع", 70, TXT("الاشتراك", "Connection"), TXT("الإدراك", "Perception"), TXT("جسر", "Bridge")),
            ("ي", 10, TXT("الاشتراك", "Connection"), TXT("النداء والنسبة", "Calling & Belonging"), TXT("جسر", "Bridge")),
            ("هـ", 5, TXT("الاشتراك", "Connection"), TXT("الهوية", "Identity"), TXT("جسر", "Bridge")),
            ("ف", 80, TXT("المشغلات", "Operators"), TXT("السببية (=)", "Causality (=)"), TXT("مشغّل", "Operator")),
            ("و", 6, TXT("المشغلات", "Operators"), TXT("العطف (×/+)", "Conjunction (×/+)"), TXT("مشغّل", "Operator")),
            ("ب", 2, TXT("المشغلات", "Operators"), TXT("الاستعانة (بـ)", "Assistance (by)"), TXT("مشغّل", "Operator")),
            ("ل", 30, TXT("المشغلات", "Operators"), TXT("التعليل (→)", "Purpose (→)"), TXT("مشغّل", "Operator")),
            ("ت", 400, TXT("أعمال الخلق", "Actions of Creation"), TXT("التوبة / التيه", "Repentance / Arrogance"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("ث", 500, TXT("أعمال الخلق", "Actions of Creation"), TXT("الثبات / الثبور", "Steadfastness / Perdition"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("ج", 3, TXT("أعمال الخلق", "Actions of Creation"), TXT("الجهاد / الجهل", "Striving / Ignorance"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("خ", 600, TXT("أعمال الخلق", "Actions of Creation"), TXT("الخير / الخيانة", "Good / Betrayal"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("ذ", 700, TXT("أعمال الخلق", "Actions of Creation"), TXT("الذكر / الذل", "Remembrance / Humiliation"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("ز", 7, TXT("أعمال الخلق", "Actions of Creation"), TXT("الزكاة / الزور", "Purification / Falsehood"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("ش", 300, TXT("أعمال الخلق", "Actions of Creation"), TXT("الشكر / الشهوة", "Gratitude / Lust"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("ض", 800, TXT("أعمال الخلق", "Actions of Creation"), TXT("الضبط / الضلال", "Precision / Misguidance"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("ظ", 900, TXT("أعمال الخلق", "Actions of Creation"), TXT("الظفر / الظلم", "Victory / Injustice"), TXT("إرادة حرة (±)", "Free Will (±)")),
            ("غ", 1000, TXT("أعمال الخلق", "Actions of Creation"), TXT("الغفران / الغل", "Forgiveness / Malice"), TXT("إرادة حرة (±)", "Free Will (±)")),
        ]
        
        df_all = pd.DataFrame(all_letters, columns=[
            TXT("الحرف", "Letter"),
            TXT("القيمة", "Value"),
            TXT("الفئة", "Category"),
            TXT("الدلالة", "Meaning"),
            TXT("الدور", "Role")
        ])
        st.dataframe(df_all, hide_index=True, use_container_width=True)

    # ─────────────────────────────────────────
    # خاتمة المعجم: كلمة التواضع
    # ─────────────────────────────────────────
    st.markdown("---")
    with st.expander(TXT("🙏 خاتمة: كلمة التواضع", "🙏 Conclusion: A Word of Humility"), expanded=False):
        st.markdown(TXT(
            """
            ### ﴿وَمَا أُوتِيتُم مِّنَ الْعِلْمِ إِلَّا قَلِيلًا﴾ [الإسراء: ٨٥]
            
            هذا المعجم – بكل ما فيه من جداول وتصنيفات ومعادلات – ليس إلا **محاولة متواضعة** لفهم شيء من أسرار كتاب الله.
            إنه ليس "العلم المطلق"، بل هو **اجتهاد بشري** يحتمل الصواب والخطأ.
            
            **نحن نقر بما يلي:**
            1. أن علم الله لا يحاط به، وأن كلماته لا تنفد.
            2. أن هذا المعجم هو "قراءة" من بين قراءات محتملة كثيرة.
            3. أنه ليس بديلاً عن التدبر المباشر للقرآن، بل هو **أداة مساعدة** للتفكر.
            4. أن الباب مفتوح لكل ناقد ومصحح ومضيف، فنحن طلاب علم، لا أرباب مذاهب.
            
            **فإن كان في هذا المعجم صواب، فمن الله وحده. وإن كان فيه خطأ، فمن أنفسنا والشيطان.**
            ونسأل الله أن ينفع به، وأن يجعله خالصاً لوجهه، وأن يغفر لنا تقصيرنا وجهالتنا.
            
            > **تأمل أخير:** هذا المعجم هو "محاولة للفهم"، لا "ادعاء للحقيقة". وهو "خطوة على الطريق"، لا "نهاية المطاف". فكلما ازددنا علماً، ازددنا يقيناً بجهلنا. وكلما تعمقنا في بحر القرآن، أدركنا أننا لم نبلغ بعدُ شاطئه.
            """,
            """
            ### ﴿And you have not been given of knowledge except a little.﴾ [Al-Isra: 85]
            
            This lexicon – with all its tables, classifications, and equations – is nothing but a **humble attempt** to understand something of the secrets of Allah's Book.
            It is not "absolute knowledge", but rather **human effort** liable to correctness and error.
            
            **We acknowledge the following:**
            1. That Allah's knowledge cannot be encompassed, and His words never end.
            2. That this lexicon is one "reading" among many possible readings.
            3. That it is not a substitute for direct reflection on the Quran, but an **aid** for contemplation.
            4. That the door is open to every critic, corrector, and contributor, for we are students of knowledge, not founders of doctrines.
            
            **If there is correctness in this lexicon, it is from Allah alone. And if there is error, it is from ourselves and Satan.**
            We ask Allah to benefit by it, to make it purely for His sake, and to forgive our shortcomings and ignorance.
            
            > **A Final Reflection:** This lexicon is "an attempt to understand", not "a claim to truth". It is "a step on the path", not "the end of the journey". For the more we increase in knowledge, the more certain we become of our ignorance. And the deeper we dive into the ocean of the Quran, the more we realize we have not yet reached its shore.
            """
        ))
