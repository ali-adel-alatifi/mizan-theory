# mizan/lexicon.py
"""
الدليل المرجعي والمعجم الهندسي
يجمع: الملاحق الموسوعية الأربعة + المعجم الهندسي + أسرار الحروف + المفاتيح اللغوية + المشغلات
"""

import streamlit as st
import pandas as pd
from config import TXT

def render_reference():
    st.header(TXT("📚 الدليل المرجعي والمعجم الهندسي", "📚 Reference Guide & Geometric Lexicon"))
    st.caption(TXT(
        "هذا الدليل يجمع كل المراجع المتخصصة في مكان واحد: الآيات الجامعات، المفاتيح اللغوية والمشغلات، "
        "الدورة الإلهية المحكمة، الميزان الذهبي، المعجم الهندسي الكامل، وأسرار الحروف.",
        "This guide gathers all specialized references in one place: Key Verses, Linguistic Keys & Operators, "
        "The Divine Cycle, The Golden Criterion, The Complete Geometric Lexicon, and Secrets of the Letters."
    ))

    # تبويبات فرعية داخل الدليل المرجعي
    ref_tab1, ref_tab2, ref_tab3, ref_tab4, ref_tab5, ref_tab6 = st.tabs([
        TXT("📖 الآيات الجامعات", "📖 Key Verses"),
        TXT("🔤 المفاتيح اللغوية والمشغلات", "🔤 Linguistic Keys & Operators"),
        TXT("🔄 الدورة الإلهية المحكمة", "🔄 The Divine Cycle"),
        TXT("⚖️ الميزان الذهبي", "⚖️ The Golden Criterion"),
        TXT("🔢 المعجم الهندسي الكامل", "🔢 Complete Geometric Lexicon"),
        TXT("🔍 أسرار الحروف", "🔍 Letter Secrets"),
    ])

    # =============================================
    # ١. الآيات الجامعات للنظرية
    # =============================================
    with ref_tab1:
        st.subheader(TXT("الآيات الجامعات للنظرية – الإطار المرجعي النهائي", "Key Verses – Final Reference Frame"))
        st.markdown(TXT(
            "هذه ست عشرة آية تمثل دستور النظرية وبرهانها، وتجمع أصول الدين القيم والإسلام الحنيف.",
            "These sixteen verses represent the constitution of the theory and its proof, gathering the foundations of Al-Deen Al-Qayyim and Al-Islam Al-Hanif."
        ))
        st.markdown("---")
        verses = [
            ("١. آية الفطرة والدين القيم والحنيفية", "﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ﴾ [الروم: ٣٠]", TXT("تأسيس العلاقة بين الفطرة والدين القيم والحنيفية كقانون كوني.", "Establishes the link between innate nature, the upright religion, and Hanifiyya as a cosmic law.")),
            ("٢. آية الغاية من الخلق (العبادة)", "﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ﴾ [الذاريات: ٥٦]", TXT("تحدد الغاية الكبرى من الوجود: العبادة التي هي تجسيد الولاء.", "Defines the ultimate purpose of existence: worship as the embodiment of loyalty.")),
            ("٣. آية الولاء والبراءة (دعوة كل الرسل)", "﴿وَلَقَدْ بَعَثْنَا فِي كُلِّ أُمَّةٍ رَّسُولًا أَنِ اعْبُدُوا اللَّهَ وَاجْتَنِبُوا الطَّاغُوتَ﴾ [النحل: ٣٦]", TXT("تثبت أن معادلة الولاء والبراءة هي رسالة الأنبياء جميعاً.", "Proves the equation of loyalty and disavowal is the message of all prophets.")),
            ("٤. آية العروة الوثقى (معادلة الثبات)", "﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾ [البقرة: ٢٥٦]", TXT("الآية المركزية: S = (الكفر بالطاغوت) × (الإيمان بالله).", "The central verse: S = (disbelief in Taghut) x (belief in Allah).")),
            ("٥. آية قانون الولاء والبراء الاجتماعي", "﴿وَالَّذِينَ كَفَرُوا بَعْضُهُمْ أَوْلِيَاءُ بَعْضٍ ۚ إِلَّا تَفْعَلُوهُ تَكُن فِتْنَةٌ فِي الْأَرْضِ وَفَسَادٌ كَبِيرٌ﴾ [الأنفال: ٧٣]", TXT("تنقل المعادلة من المستوى الفردي إلى المستوى الاجتماعي والتاريخي.", "Transfers the equation from the individual to the social and historical level.")),
            ("٦. آية الميزان (قانون السببية في الخلق والأمر)", "﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ﴾ [الرحمن: ٧-٨]", TXT("تربط بين النظام الكوني (رفع السماء) والنظام الأخلاقي (الميزان).", "Links the cosmic order (raising the sky) and the moral order (the balance).")),
            ("٧. آية نتيجة كسر القانون (الفساد)", "﴿ظَهَرَ الْفَسَادُ فِي الْبَرِّ وَالْبَحْرِ بِمَا كَسَبَتْ أَيْدِي النَّاسِ﴾ [الروم: ٤١]", TXT("تقدم الدليل التجريبي على قانون السببية: الفساد نتيجة كسب الأيدي.", "Provides empirical evidence of causality: corruption results from people's deeds.")),
            ("٨. آية ثبات القانون (الحق لا يتبع الهوى)", "﴿وَلَوِ اتَّبَعَ الْحَقُّ أَهْوَاءَهُمْ لَفَسَدَتِ السَّمَاوَاتُ وَالْأَرْضُ﴾ [المؤمنون: ٧١]", TXT("تؤكد ثبات القانون الإلهي وعدم خضوعه للأهواء البشرية.", "Affirms the fixity of divine law and its non-submission to human whims.")),
            ("٩. آية الإسلام الكوني (دين الكون كله)", "﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ وَلَهُ أَسْلَمَ مَن فِي السَّمَاوَاتِ وَالْأَرْضِ طَوْعًا وَكَرْهًا﴾ [آل عمران: ٨٣]", TXT("تعلن أن الإسلام بمعنى الخضوع للقانون هو دين الكون كله.", "Declares Islam as submission to the law is the religion of the entire universe.")),
            ("١٠. آية النور والظلمات (رمز الولاء والبراءة)", "﴿الْحَمْدُ لِلَّهِ الَّذِي خَلَقَ السَّمَاوَاتِ وَالْأَرْضَ وَجَعَلَ الظُّلُمَاتِ وَالنُّورَ﴾ [الأنعام: ١]", TXT("تقدم الثنائية الكونية (الظلمات والنور) رمزاً للولاء والبراءة.", "Presents cosmic duality (darkness and light) as a symbol of loyalty and disavowal.")),
            ("١١. آية تحول الحياة كلها إلى عبادة", "﴿قُلْ إِنَّ صَلَاتِي وَنُسُكِي وَمَحْيَايَ وَمَمَاتِي لِلَّهِ رَبِّ الْعَالَمِينَ * لَا شَرِيكَ لَهُ﴾ [الأنعام: ١٦٢-١٦٣]", TXT("تعلن أن الولاء لله ليس مقصوراً على العبادات الشعائرية، بل يشمل الحياة كلها.", "Declares loyalty to Allah is not limited to rituals but encompasses all of life.")),
            ("١٢. آية الغاية من الحياة والموت (الابتلاء)", "﴿الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا﴾ [الملك: ٢]", TXT("تبين أن الحياة والموت دار ابتلاء لاختبار معادلة الولاء والبراءة.", "Shows life and death as a trial to test the equation of loyalty and disavowal.")),
            ("١٣. آية حصر الجزاء في العمل", "﴿هَلْ تُجْزَوْنَ إِلَّا مَا كُنتُمْ تَعْمَلُونَ﴾ [النمل: ٩٠]", TXT("تقرر قانون السببية في الجزاء بأوضح عبارة.", "Establishes the law of causality in recompense in the clearest terms.")),
            ("١٤. آية قانون الذرة (دقة الجزاء)", "﴿فَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ * وَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ شَرًّا يَرَهُ﴾ [الزلزلة: ٧-٨]", TXT("تؤكد دقة قانون السببية: لا يضيع مثقال ذرة من خير أو شر.", "Affirms the precision of causality: not an atom's weight of good or evil is lost.")),
            ("١٥. آية الولاية الحق (نتيجة المعادلة)", "﴿هُنَالِكَ الْوَلَايَةُ لِلَّهِ الْحَقِّ ۚ هُوَ خَيْرٌ ثَوَابًا وَخَيْرٌ عُقْبًا﴾ [الكهف: ٤٤]", TXT("تعلن الثمرة النهائية لمعادلة الثبات: الولاية لله الحق.", "Declares the final fruit of the stability equation: true loyalty belongs to Allah.")),
            ("١٦. آية الخلق بالحق والجزاء بالعدل", "﴿وَخَلَقَ اللَّهُ السَّمَاوَاتِ وَالْأَرْضَ بِالْحَقِّ وَلِتُجْزَىٰ كُلُّ نَفْسٍ بِمَا كَسَبَتْ وَهُمْ لَا يُظْلَمُونَ﴾ [الجاثية: ٢٢]", TXT("تختم الإطار المرجعي: الخلق بالحق والجزاء بالعدل.", "Seals the reference frame: creation in truth and recompense in justice.")),
        ]
        for title, verse, meaning in verses:
            st.markdown(f"**{title}**")
            st.info(verse)
            st.caption(meaning)
            st.markdown("---")

    # =============================================
    # ٢. المفاتيح اللغوية والمشغلات
    # =============================================
    with ref_tab2:
        st.subheader(TXT("المفاتيح اللغوية والمشغلات – أدوات الهندسة القرآنية", "Linguistic Keys & Operators – Tools of Quranic Engineering"))
        st.markdown(TXT(
            "أهم الأدوات اللغوية التي تحول قراءة القرآن إلى قراءة معادلات كونية. "
            "الحروف في القرآن ليست مجرد أدوات نحوية، بل هي 'أوامر وجودية' تحدد طبيعة القوانين التي تحكمنا.",
            "The most important linguistic tools that transform Quran reading into cosmic equations. "
            "Letters in the Quran are not just grammatical tools, but 'existential commands' that determine the nature of the laws governing us."
        ))
        
        st.markdown("---")
        st.markdown(TXT("### ١. أدوات السببية والغائية", "### 1. Causality & Purpose Tools"))
        st.markdown(f"""
        | الأداة | الرمز | الوظيفة | مثال قرآني |
        |:---|:---|:---|:---|
        | **فاء السببية** | **فَـ** | علامة يساوي (=) في المعادلة الإلهية. تربط السبب بالنتيجة حتماً. | ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ **فَ** قَدِ اسْتَمْسَكَ﴾ |
        | **لام التعليل** | **لِـ** | سهم يوضح اتجاه الغاية (←). تبين العلة من الفعل. | ﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا **لِ** يَعْبُدُونِ﴾ |
        | **حتى الغائية** | **حَتَّىٰ** | استمرار السبب حتى تتحقق النتيجة. | ﴿حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ﴾ |
        | **لام الأمر** | **لِـ** | أداة التكليف المباشر. تجعل الفعل واجباً. | ﴿**لِ** يُنفِقْ ذُو سَعَةٍ﴾ |
        | **لعل للترجي** | **لَعَلَّ** | تعليق الرجاء بالحكمة. توقع حصول الثمرة. | ﴿**لَعَلَّ** كُمْ تَتَّقُونَ﴾ |
        """)
        
        st.markdown(TXT("### ٢. أدوات الشرط والاستقبال", "### 2. Condition & Future Tools"))
        st.markdown(f"""
        | الأداة | الرمز | الوظيفة | مثال قرآني |
        |:---|:---|:---|:---|
        | **إنْ الشرطية** | **إِنْ** | للاختيار وحرية الإنسان. تفيد الاحتمال. | ﴿**فَإِن** تَابُوا﴾ |
        | **إذا الشرطية** | **إِذَا** | للحتمية والسنن. تفيد التحقق. | ﴿**إِذَا** جَاءَ نَصْرُ اللَّهِ﴾ |
        | **فإن / فإذا** | **فَإِنْ / فَإِذَا** | الربط المذهل بين السببية والشرط (سلسلة سببية متصلة). | ﴿**فَإِن** تَابُوا... **فَ** إِخْوَانُكُمْ﴾ |
        | **لَوْ الشرطية** | **لَوْ** | للامتناع لامتناع (برهان عقلي). | ﴿**لَوْ** كَانَ فِيهِمَا آلِهَةٌ إِلَّا اللَّهُ لَفَسَدَتَا﴾ |
        """)
        
        st.markdown(TXT("### ٣. أدوات الحصر والتمييز", "### 3. Restriction & Distinction Tools"))
        st.markdown(f"""
        | الأداة | الرمز | الوظيفة | مثال قرآني |
        |:---|:---|:---|:---|
        | **إلا** | **إِلَّا** | سيف التمييز بين المعسكرين. حصر واستثناء. | ﴿لَا عَاصِمَ الْيَوْمَ مِنْ أَمْرِ اللَّهِ **إِلَّا** مَن رَّحِمَ﴾ |
        | **إنما** | **إِنَّمَا** | أداة حصر وقصر. | ﴿**إِنَّمَا** وَلِيُّكُمُ اللَّهُ﴾ |
        | **أدوات النفي** | **مَا، لَا، لَنْ، لَمْ** | لكل منها دلالة زمنية خاصة. | ﴿**لَا** انفِصَامَ لَهَا﴾ (نفي مطلق) |
        | **أدوات الاستفهام** | **هَلْ، الْهَمْزَة** | للتقرير والتوبيخ. | ﴿**هَلْ** تُجْزَوْنَ إِلَّا مَا كُنتُمْ تَعْمَلُونَ﴾ |
        """)

        st.markdown("---")
        st.subheader(TXT("⚡ المشغلات – الحروف كأوامر وجودية", "⚡ Operators – Letters as Existential Commands"))
        st.markdown(TXT(
            """
            ### فئة المشغلات (الفئة الخامسة في المعجم الهندسي)
            
            هذه الحروف الأربعة تمثل **أدوات المنطق والسببية** في كلام الله. إنها "أوامر برمجية" (Operators) 
            تخبرنا **ماذا نفعل** بالقيم الأخرى. الحرف لا يحمل قيمة في ذاته، بل يحدد **كيفية تفاعل** القيم الأخرى.
            
            | الحرف | القيمة | الرمز | الدور في المعادلة | شرح الوظيفة |
            |:---|:---|:---|:---|:---|
            | **ف** | 80 | **=** | **فاء السببية – علامة التساوي** | تجعل ما قبلها سبباً في حصول ما بعدها حتماً. هي مُشغّل القيمة السببية الذي يعلن أن ما بعدها هو قيمة سببية ثابتة في نظام الله. |
            | **و** | 6 | **× / +** | **واو العطف – الضرب أو الجمع** | تجمع بين طرفين. في آيات الجزاء تقسم الناس إلى فئتين وتضرب كل فئة في جزائها. |
            | **ب** | 2 | **بـ** | **باء الاستعانة – مفتاح التشغيل** | تربط الفعل بالوسيلة. "باسم الله" تعني تشغيل الفعل بقوة الله. |
            | **ل** | 30 | **→** | **لام التعليل – سهم الاتجاه** | تحدد الغاية والهدف. تخبرك لماذا تفعل الفعل. |
            
            ### سر "الفاء" – مُشغّل القيمة السببية
            
            في قوله تعالى: **﴿فَـ مَن يَكْفُرْ بِالطَّاغُوتِ﴾**، الفاء هنا ليست فقط للربط، بل هي **تعلن أن "الكفر بالطاغوت" قيمة سببية ثابتة** في نظام الله. إنها تجعل B (البراءة) ليس مجرد متغير، بل **ثابتاً معيارياً** في المعادلة.
            
            المعادلة تُقرأ هكذا:
            > **فَـ** (B × W) = S
            > **"فاء السببية"** تعلن أن حاصل ضرب قيمة البراءة في قيمة الولاء يساوي الثبات.
            """,
            """
            ### The Operators (Category 5 in the Geometric Lexicon)
            
            These four letters represent **tools of logic and causality** in Allah's speech. They are "programming commands" (Operators)
            that tell us **what to do** with other values. A letter does not carry a value in itself, but determines **how other values interact**.
            
            | Letter | Value | Symbol | Role in Equation | Function |
            |:---|:---|:---|:---|:---|
            | **F** | 80 | **=** | **Causative Fa – Equals Sign** | Makes what precedes it a cause for what follows it inevitably. It is the causal value operator declaring that what follows is a fixed causal value in Allah's system. |
            | **W** | 6 | **× / +** | **Conjunctive Waw – Multiplication or Addition** | Combines two terms. In verses of recompense, it divides people into two groups and multiplies each by its reward. |
            | **B** | 2 | **by** | **Instrumental Ba – Activation Key** | Links the action to its means. "In the name of Allah" means activating the action by Allah's power. |
            | **L** | 30 | **→** | **Purpose Lam – Direction Arrow** | Determines the goal and objective. Tells you why you do the action. |
            
            ### The Secret of "Fa" – The Causal Value Operator
            
            In Allah's words: **﴿So whoever disbelieves in Taghut...﴾**, the "Fa" here is not just for connection, but **declares that "disbelief in Taghut" is a fixed causal value** in Allah's system. It makes B (disavowal) not just a variable, but a **standard constant** in the equation.
            
            The equation reads:
            > **Fa** (B × W) = S
            > **The causative Fa** declares that the product of the value of disavowal and the value of loyalty equals stability.
            """
        ))

    # =============================================
    # ٣. الدورة الإلهية المحكمة
    # =============================================
    with ref_tab3:
        st.subheader(TXT("الدورة الإلهية المحكمة – خريطة المسار الكامل", "The Divine Cycle – Complete Path Map"))
        st.markdown(TXT(
            "ثماني مراحل تنتظم حياة الفرد والأمة من الخلق إلى الخلود. "
            "كل مرحلة تمهد للتي تليها، وتترتب عليها. من بدأ من أولها وواصل السير بصدق، وصل إلى غايتها المحمودة.",
            "Eight stages organizing the life of individuals and nations from creation to eternity. "
            "Each stage paves the way for the next. Whoever begins from the first and continues sincerely reaches its praiseworthy goal."
        ))
        st.markdown("---")
        stages = [
            ("١. التأسيس الكوني – الخلق والتكليف", 
             "خلق الإنسان على الفطرة السليمة، استخراج الميثاق الأزلي: ﴿أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾، منح الحرية والاختيار، التكليف بالعبودية.",
             TXT("الاستعداد الفطري الكامل لبدء الدورة.", "Full innate readiness to begin the cycle.")),
            ("٢. البيان النظري – الوحي والرسالة", 
             "إرسال الرسل تباعاً (نوح، إبراهيم، موسى، عيسى، محمد)، إنزال الكتب المتدرجة، بيان قانون: ﴿اعْبُدُوا اللَّهَ وَاجْتَنِبُوا الطَّاغُوتَ﴾، اكتمال البيان وارتفاع العذر.",
             TXT("اكتمال الحجة الإلهية على البشر.", "Completion of divine proof upon humans.")),
            ("٣. الامتحان العملي – التمحيص والتدافع", 
             "الابتلاء بالخير والشر، الغنى والفقر، الصحة والمرض. التمحيص: ﴿أَحَسِبَ النَّاسُ أَن يُتْرَكُوا أَن يَقُولُوا آمَنَّا وَهُمْ لَا يُفْتَنُونَ﴾. تمييز الصادق من الكاذب.",
             TXT("كشف المعدن الحقيقي للناس.", "Revealing the true mettle of people.")),
            ("٤. التطبيق المنهجي – التربية والبناء", 
             "بناء الفرد الرباني (العبادات)، بناء الأسرة المسلمة (القوامة والمودة)، بناء المجتمع المترابط (الأخوة والتعاون)، بناء الدولة العادلة (إقامة الشرع)، بناء الأمة الشاهدة (حمل الرسالة).",
             TXT("البناء المتدرج للمؤمنين الصادقين.", "Gradual building of the sincere believers.")),
            ("٥. النتائج الكونية – السنن الإلهية", 
             "ظهور النتائج الحتمية: سنن إيجابية للموالين (النصر، التمكين، الاستخلاف، الرحمة). سنن سلبية للمتخلفين (الذلة، الهوان، الهلاك).",
             TXT("لا تحابي أحداً. النتيجة حتمية.", "Favoring none. The result is inevitable.")),
            ("٦. تحقيق المقاصد الربانية", 
             "حفظ الضروريات الخمس (الدين، النفس، العقل، النسل، المال). تحقيق الكماليات (تحسين الحياة، نشر الخير، تحقيق العدل). إقامة الحضارة الربانية التي تشهد على الناس.",
             TXT("تحقيق الغايات التي من أجلها قامت الدورة.", "Achieving the goals for which the cycle was established.")),
            ("٧. الاستمرار والتجدد – آليات الحفظ", 
             "التجديد الدوري عبر العبادات (اليومية، الأسبوعية، السنوية). الحماية الإلهية للدين بحفظ القرآن والسنة. التكيف مع المتغيرات بثبات الأصول ومرونة الفروع.",
             TXT("الدورة مستمرة عبر الأجيال.", "The cycle continues across generations.")),
            ("٨. الخاتمة الكونية – يوم الفصل والجزاء", 
             "الموت، ثم يوم القيامة حيث الفصل النهائي بين الولاءات. نصب الموازين: ﴿وَنَضَعُ الْمَوَازِينَ الْقِسْطَ لِيَوْمِ الْقِيَامَةِ﴾. الجنة دار الولاية، النار دار البراءة.",
             TXT("العدل الإلهي المطلق.", "Absolute divine justice.")),
        ]
        for title, desc, meaning in stages:
            st.markdown(f"**{title}**")
            st.info(desc)
            st.caption(meaning)
            st.markdown("---")
        
        st.subheader(TXT("خصائص الدورة الإلهية", "Characteristics of the Divine Cycle"))
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(TXT("**الإحكام**\nالدقة المطلقة", "**Precision**\nAbsolute accuracy"))
        with col2:
            st.markdown(TXT("**الشمول**\nالعمومية الكاملة", "**Comprehensiveness**\nComplete universality"))
        with col3:
            st.markdown(TXT("**السننية**\nالقانونية الكونية", "**Lawfulness**\nCosmic legality"))
        with col4:
            st.markdown(TXT("**التكامل**\nالترابط العضوي", "**Integration**\nOrganic interconnection"))
        with col5:
            st.markdown(TXT("**التوازن**\nالاعتدال الشامل", "**Balance**\nComprehensive moderation"))

    # =============================================
    # ٤. الميزان الذهبي
    # =============================================
    with ref_tab4:
        st.subheader(TXT("الميزان الذهبي – ديناميكية الولاء والبراء في سورة التوبة", "The Golden Criterion – Dynamics in Surat At-Tawbah"))
        st.markdown(TXT(
            "تحليل الآية ١١ من سورة التوبة: ﴿فَإِن تَابُوا وَأَقَامُوا الصَّلَاةَ وَآتَوُا الزَّكَاةَ فَإِخْوَانُكُمْ فِي الدِّينِ﴾",
            "Analysis of verse 11 of At-Tawbah: ﴿But if they repent, establish prayer, and give zakah, then they are your brothers in religion.﴾"
        ))
        st.markdown("---")
        st.markdown(TXT(
            """
            ### المعادلة الكاملة
            
            إعلان البراءة (سياق السورة) ← **(فـ)** إن تابوا (سبب اختياري) ← **(فـ)** إخوانكم (نتيجة حتمية)
            
            ### تفصيل الشروط والنتيجة
            
            | المرتبة | العنصر | النوع | الدلالة |
            |:---|:---|:---|:---|
            | **الشرط الأول** | **التوبة** | تحول قلبي | البراءة من الشرك والطاغوت، والولاء لله وحده. التخلية قبل التحلية. |
            | **الشرط الثاني** | **إقامة الصلاة** | عبادة بدنية | الدليل العملي على صدق التوبة. رمز الولاء اليومي لله. |
            | **الشرط الثالث** | **إيتاء الزكاة** | عبادة مالية | الدليل المالي على صدق التوبة. رمز الولاء الاجتماعي للمؤمنين. |
            | **النتيجة** | **الأخوة في الدين** | ولاية كاملة | أعمق مراتب الولاء. لهم ما لنا، وعليهم ما علينا. |
            
            ### الدروس المستفادة
            
            ١. **الولاء والبراء ديناميكيان:** ليسا حالتين جامدتين، بل يتغيران بتغير الأحوال والأسباب.
            ٢. **باب التوبة مفتوح:** البراءة ليست عداوة أبدية، بل مرتبطة بسبب هو الكفر والعداوة.
            ٣. **الأخوة تُستحق بالعمل:** لا بالانتساب فقط. لا بد من التوبة القلبية والعمل الصالح.
            ٤. **التوازن بين العدل والرحمة:** السورة بدأت ببراءة قاطعة، وفي قلبها هذا الميزان الذهبي الذي يفتح باب الأخوة.
            """,
            """
            ### The Complete Equation
            
            Declaration of disavowal (context of the Surah) ← **(Fa)** If they repent (optional cause) ← **(Fa)** They are your brothers (inevitable result)
            
            ### Detailing Conditions and Result
            
            | Rank | Element | Type | Significance |
            |:---|:---|:---|:---|
            | **First Condition** | **Repentance** | Heart transformation | Disavowal of shirk and Taghut, loyalty to Allah alone. Evacuation before filling. |
            | **Second Condition** | **Establishing Prayer** | Physical worship | Practical proof of sincere repentance. Symbol of daily loyalty to Allah. |
            | **Third Condition** | **Giving Zakat** | Financial worship | Financial proof of sincere repentance. Symbol of social loyalty to believers. |
            | **Result** | **Brotherhood in Religion** | Complete loyalty | The deepest rank of loyalty. They have what we have, and upon them what is upon us. |
            
            ### Lessons Learned
            
            1. **Loyalty and Disavowal are Dynamic:** Not fixed states, but change with changing circumstances and causes.
            2. **The Door of Repentance is Open:** Disavowal is not eternal enmity, but linked to the cause of disbelief and hostility.
            3. **Brotherhood is Earned by Deeds:** Not by mere affiliation. Heartfelt repentance and righteous deeds are necessary.
            4. **Balance between Justice and Mercy:** The Surah began with decisive disavowal, and in its heart is this golden criterion opening the door of brotherhood.
            """
        ))

    # =============================================
    # ٥. المعجم الهندسي الكامل
    # =============================================
    with ref_tab5:
        st.subheader(TXT("المعجم الهندسي الكامل – الحروف وقيمها وأدوارها", "Complete Geometric Lexicon – Letters, Values & Roles"))
        st.markdown(TXT(
            "هذا المعجم يربط كل حرف من الحروف العربية الثمانية والعشرين بقيمته العددية (حساب الجمل) "
            "ودوره الوجودي في معادلة الميزان. التصنيف مبني على ست فئات وجودية.",
            "This lexicon links each of the twenty-eight Arabic letters to its numerical value (Abjad calculation) "
            "and its existential role in the Mizan equation. Classification is based on six existential categories."
        ))
        st.markdown("---")
        
        letters_data = {
            TXT('الفئة الأولى: الذات الإلهية – المصدر (حرفان)', 'Category 1: Divine Essence – Source (2 letters)'): {
                'ك': {'value': 20, 'role': TXT('ثابت الأمر والتكوين – كُن', 'Constant of command and formation – Be')},
                'ن': {'value': 50, 'role': TXT('ثابت النور الذاتي – ﴿اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ﴾', 'Constant of intrinsic light')},
            },
            TXT('الفئة الثانية: الازدواج – ثابت في الذات متجلي في الخلق (حرفان)', 'Category 2: Duality – Fixed in Essence, Manifested in Creation (2 letters)'): {
                'ق': {'value': 100, 'role': TXT('الثابت: الميزان – المتجلي: القسط والعدل والدِّينُ القَيِّم', 'Fixed: The Balance – Manifested: Justice and the Upright Religion')},
                'ص': {'value': 90, 'role': TXT('الثابت: الصمد – المتجلي: الصبر والصدق والاصطفاء', 'Fixed: The Eternal – Manifested: Patience, Truthfulness, and Selection')},
            },
            TXT('الفئة الثالثة: التجلي الإلهي – صفات متجلية في الخلق (٧ حروف)', 'Category 3: Divine Manifestation – Attributes Manifested in Creation (7 letters)'): {
                'أ': {'value': 1, 'role': TXT('الوحدانية – مُوَلِّد W', 'Oneness – W Generator')},
                'ل': {'value': 30, 'role': TXT('المُلك والعدل – مُوَلِّد B', 'Kingship and Justice – B Generator')},
                'م': {'value': 40, 'role': TXT('الجمع والتماسك – مُوَلِّد S', 'Gathering and Cohesion – S Generator')},
                'ر': {'value': 200, 'role': TXT('اليقظة والمراقبة – مُوَلِّد المقاومة', 'Wakefulness and Vigilance – Resistance Generator')},
                'س': {'value': 60, 'role': TXT('السمع والاستجابة', 'Hearing and Responsiveness')},
                'ح': {'value': 8, 'role': TXT('الحياة والاستدامة', 'Life and Sustainability')},
                'ط': {'value': 9, 'role': TXT('الطهارة والمناعة', 'Purity and Immunity')},
            },
            TXT('الفئة الرابعة: الاشتراك – الجسور بين الغيب والشهادة (٣ حروف)', 'Category 4: Connection – Bridges between Unseen and Seen (3 letters)'): {
                'ع': {'value': 70, 'role': TXT('جسر الإدراك والرؤية – ﴿يَرَوْنَهُ بَعِيدًا وَنَرَاهُ قَرِيبًا﴾', 'Bridge of perception and vision')},
                'ي': {'value': 10, 'role': TXT('جسر النداء والنسبة – ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا﴾', 'Bridge of call and belonging')},
                'هـ': {'value': 5, 'role': TXT('جسر الهوية والحضور – ﴿هُوَ اللَّهُ﴾', 'Bridge of identity and presence')},
            },
            TXT('الفئة الخامسة: المشغلات – أدوات المنطق والسببية (٤ حروف)', 'Category 5: Operators – Tools of Logic and Causality (4 letters)'): {
                'ف': {'value': 80, 'role': TXT('علامة التساوي (=) – فاء السببية', 'Equals sign (=) – Causative Fa')},
                'و': {'value': 6, 'role': TXT('الضرب (×) أو الجمع (+) – واو العطف', 'Multiplication (×) or Addition (+) – Conjunctive Waw')},
                'ب': {'value': 2, 'role': TXT('مفتاح الاستعانة (بـ) – باء الوسيلة', 'Activation key (by) – Instrumental Ba')},
                'ل': {'value': 30, 'role': TXT('سهم التعليل (→) – لام الغاية', 'Direction arrow (→) – Purpose Lam')},
            },
            TXT('الفئة السادسة: أعمال الخلق – إرادة حرة ± (١٠ حروف)', 'Category 6: Actions of Creation – Free Will ± (10 letters)'): {
                'ج': {'value': 3, 'role': TXT('الوجه الإيجابي: الجهاد، الجود | الوجه السلبي: الجهل، الجحود', 'Positive: Striving, Generosity | Negative: Ignorance, Denial')},
                'خ': {'value': 600, 'role': TXT('الوجه الإيجابي: الخير، الخشية | الوجه السلبي: الخيانة، الخذلان', 'Positive: Goodness, Awe | Negative: Betrayal, Letdown')},
                'ذ': {'value': 700, 'role': TXT('الوجه الإيجابي: الذكر | الوجه السلبي: الذل، الذنب', 'Positive: Remembrance | Negative: Humiliation, Sin')},
                'ز': {'value': 7, 'role': TXT('الوجه الإيجابي: الزكاة، الزهد | الوجه السلبي: الزور، الزيغ', 'Positive: Purification, Asceticism | Negative: Falsehood, Deviation')},
                'ش': {'value': 300, 'role': TXT('الوجه الإيجابي: الشكر، الشجاعة | الوجه السلبي: الشهوة، الشرك', 'Positive: Gratitude, Courage | Negative: Lust, Polytheism')},
                'ت': {'value': 400, 'role': TXT('الوجه الإيجابي: التوبة، التقوى | الوجه السلبي: التيه | حرف الاتخاذ والتبعية', 'Positive: Repentance, Godliness | Negative: Wandering | Letter of adoption and following')},
                'ث': {'value': 500, 'role': TXT('الوجه الإيجابي: الثبات، الثواب | الوجه السلبي: الثبور', 'Positive: Steadfastness, Reward | Negative: Destruction')},
                'ض': {'value': 800, 'role': TXT('الوجه الإيجابي: الضياء | الوجه السلبي: الضلال', 'Positive: Radiance | Negative: Misguidance')},
                'ظ': {'value': 900, 'role': TXT('الوجه الإيجابي: الظفر | الوجه السلبي: الظلم', 'Positive: Victory | Negative: Injustice')},
                'غ': {'value': 1000, 'role': TXT('الوجه الإيجابي: الغفران | الوجه السلبي: الغل', 'Positive: Forgiveness | Negative: Malice')},
            },
        }

        for cat, lets in letters_data.items():
            st.markdown(f"#### {cat}")
            for letter, info in lets.items():
                st.markdown(f"**{letter}** = {info['value']} | {info['role']}")
            st.markdown("---")
        
        st.info(TXT(
            "🔮 **المعادلة الأولى للوجود:** ك + ن = ع (20 + 50 = 70). الأمر (كُن) + النور = الإدراك (العلم).",
            "🔮 **The First Equation of Existence:** K + N = A (20 + 50 = 70). Command (Be) + Light = Perception (Knowledge)."
        ))
        
        st.info(TXT(
            "🔗 **المعادلات الوجودية للجسور:**\n"
            "• ك + ن = ع (المصدر ينتج أول جسر: الأمر + النور = الإدراك)\n"
            "• ع + ي = 80 (الإدراك + النداء = الاستجابة) — وقيمة 80 هي قيمة 'ف' (علامة التساوي)\n"
            "• ي + هـ = 15 (النداء + الحضور = تحديد الهوية)\n"
            "• الدائرة تعود: هـ → ك (الهوية تعود إلى المصدر: ﴿كُلٌّ إِلَيْنَا رَاجِعُونَ﴾)",
            "🔗 **Existential Equations of the Bridges:**\n"
            "• K + N = A (The source produces the first bridge: Command + Light = Perception)\n"
            "• A + Y = 80 (Perception + Call = Response) — Value 80 is the value of 'F' (the equals sign)\n"
            "• Y + H = 15 (Call + Presence = Identity Determination)\n"
            "• The circle returns: H → K (Identity returns to the source: ﴿And to Us all will return﴾)"
        ))

    # =============================================
    # ٦. أسرار الحروف
    # =============================================
    with ref_tab6:
        st.subheader(TXT("أسرار الحروف", "Secrets of the Letters"))
        
        # سر الألف
        st.markdown(TXT(
            """
            ### سر الألف (ا = 1) – الوحدانية في الكثرة
            
            **القيمة 1 = الوحدانية المطلقة.**
            **التكرار 13 مرة في فواتح السور = التجلي في عالم الكثرة (الخلق).**
            
            هذا ليس تناقضاً، بل هو السر الأعظم:
            - الله واحد في ذاته (قيمته 1)، ولكنه متجلي في خلقه (تكراره 13).
            - الـ 1 لا يتجزأ، ولكنه يظهر في كل مكان.
            - الألف هو الحرف الوحيد الذي لا ينطق بذاته (لا حركة له – فهو همزة أو مد)، ومع ذلك هو أساس كل كلمة.
            - إنه مثل "الله": لا تدركه الأبصار، ولكن كل شيء يدل عليه.
            
            **العلاقة مع الأسماء الحسنى:**
            الألف هو حرف "الأحد"، "الأول"، "الآخر"، "الظاهر"، "الباطن".
            قيمته 1، لأنه واحد في كل هذه الأسماء، لا شريك له.
            
            **الخلاصة الرياضية:**
            القيمة (1) = الذات الإلهية (ثابت لا يتغير).
            التكرار (13) = تجليات هذه الذات في الخلق (متغير حسب السياق).
            """,
            """
            ### The Secret of Alif (ا = 1) – Oneness in Multiplicity
            
            **Value 1 = Absolute Oneness.**
            **Frequency 13 in Quranic openings = Manifestation in the world of multiplicity.**
            
            This is not a contradiction, but the greatest secret:
            - Allah is One in His Essence (value 1), yet manifested in His creation (frequency 13).
            - Alif is the only letter that has no sound of its own, yet it is the basis of every word.
            - It is like "Allah": vision does not perceive Him, yet everything points to Him.
            
            **Relation to the Most Beautiful Names:**
            Alif is the letter of "The One", "The First", "The Last", "The Manifest", "The Hidden".
            
            **Mathematical Summary:**
            Value (1) = The Divine Essence (unchanging).
            Frequency (13) = Manifestations of this Essence in creation (variable by context).
            """
        ))

        st.markdown("---")

        # سر (الم)
        st.markdown(TXT(
            """
            ### منظومة (الم) – قاعدة الأسماء والصفات
            
            الحروف الثلاثة (ا، ل، م) هي "البصمة الصوتية" لأعظم اسم: **الله**.
            والقرآن يفتتح بها 6 سور (بعدد أيام الخلق)، لأنها "أم الكتاب" و"أم الأسماء".
            
            | الحرف | الرمز | أمثلة من أسماء الله التي تبدأ به | معانيها |
            |:---|:---|:---|:---|
            | **أ** | الوحدانية، البداية | الأحد، الأول، الآخر | هي أصل كل شيء. لا يشاركه فيها أحد. |
            | **ل** | المُلك، اللطف، العدل | الملك، اللطيف، العدل، الحليم | الله هو المَلِك، وأنت "عبد الله" (لام الملكية). |
            | **م** | الجمع، العطاء، المنع | المعطي، المانع، المحيي، المميت، المعز، المذل، المجيد، المتكبر، المتعال | هذه أسماء "الأفعال". الله يعطي ويمنع، يحيي ويميت، يعز ويذل. |
            
            عندما تقرأ "الم"، فأنت تستحضر كل هذه الأسماء. ولهذا كان النبي ﷺ يقول:
            "من قرأ حرفاً من كتاب الله فله به حسنة... لا أقول الم حرف، ولكن ألف حرف، ولام حرف، وميم حرف".
            لأن كل حرف منها كنز من الأسماء.
            """,
            """
            ### The (ALM) System – Foundation of Names and Attributes
            
            The three letters (A, L, M) are the "sound signature" of the greatest name: **Allah**.
            The Quran opens with them in 6 suras (the days of creation), because they are "the mother of the book" and "the mother of names".
            
            | Letter | Symbol | Examples of Allah's Names Starting with It | Meanings |
            |:---|:---|:---|:---|
            | **A** | Oneness, Beginning | The One, The First, The Last | They are the origin of everything. None shares in them. |
            | **L** | Kingship, Kindness, Justice | The King, The Subtle, The Just, The Forbearing | Allah is the King, and you are "Abdullah" (the L of ownership). |
            | **M** | Gathering, Giving, Withholding | The Giver, The Withholder, The Giver of Life, The Causer of Death, The Honorer, The Humiliator, The Glorious, The Supreme, The Exalted | These are names of "actions". Allah gives and withholds, gives life and causes death, honors and humiliates. |
            
            When you recite "ALM", you evoke all these names. Hence the Prophet ﷺ said:
            "Whoever recites a letter from the Book of Allah has a good deed... I do not say ALM is one letter, but Alif is a letter, Lam is a letter, and Meem is a letter."
            Because each letter is a treasure of names.
            """
        ))

        st.markdown("---")

        # سر القاف
        st.markdown(TXT(
            """
            ### سر حرف القاف (ق = 100) – حرف الميزان
            
            حرف **القاف** هو حرف "الحق" و"القيوم" و"القسط" و"الدِّينُ القَيِّم". قيمته 100 هي كمال العدد وأساس النسب.
            
            للقاف وجهان:
            - **وجه ثابت في الذات الإلهية:** ﴿الْحَقُّ﴾، ﴿الْقَيُّومُ﴾. وهذا ثابت لا يتغير.
            - **وجه متجلي في الخلق:** ﴿الْقِسْطُ﴾ (العدل)، ﴿الدِّينُ الْقَيِّمُ﴾ (القانون الإلهي الحق الثابت).
            
            و"الدِّينُ الْقَيِّمُ" هو القانون الإلهي الحق الثابت، ميزان الله الذي فطر الناس عليه، والذي لا تبديل فيه.
            وهذا هو سر كون "ق" هو حرف الميزان، وسر كون قيمته 100 تمثل تمام العدل وكمال الوزن.
            
            في فواتح السور، يظهر القاف في سورتين فقط (ق، والشورى التي فيها عسق). هذا الظهور المحدود يدل على أنه حرف الفصل والتمييز،
            حرف الميزان الذي يفرق بين الحق والباطل، بين الولاء والبراءة، بين الثبات والانهيار.
            """,
            """
            ### The Secret of Qaf (ق = 100) – The Letter of the Balance
            
            The letter **Qaf** is the letter of "The Truth", "The Self-Subsisting", "Justice", and "The Upright Religion". Its value 100 is numerical perfection and the basis of proportion.
            
            Qaf has two faces:
            - **A fixed face in the Divine Essence:** "The Truth", "The Self-Subsisting". This is unchanging.
            - **A manifested face in creation:** "Justice", "The Upright Religion" (the fixed divine law).
            
            And "The Upright Religion" is the divine law, the truth, the balance of Allah upon which people were created, in which there is no alteration.
            This is the secret of why Qaf is the letter of the Balance, and why its value 100 represents perfect justice and complete weight.
            """
        ))

        st.markdown("---")

        # سر التاء
        st.markdown(TXT(
            """
            ### سر حرف التاء (ت = 400) – حرف القرار والمصير
            
            حرف **التاء (ت)** قيمته ٤٠٠، وهو من حروف الخلق والمشغلات في آنٍ واحد.
            من أعظم دلالاته في القرآن الكريم: **الاتخاذ** و**التبعية**.
            
            الاتخاذ هو قرار القلب واختياره. وهو الذي يحدد موقعك على خريطة (W, B):
            
            **١. تاء الاتخاذ الإيجابي (الولاء):**
            > ﴿وَاتَّخَذَ اللَّهُ إِبْرَاهِيمَ خَلِيلًا﴾ [النساء: ١٢٥]
            > هذه ذروة الاتخاذ الإيجابي. الله يتخذ عبداً خليلاً. هذا هو W = 1.
            
            **٢. تاء الاتخاذ السلبي (الولاء للطاغوت):**
            > ﴿أَفَرَأَيْتَ مَنِ اتَّخَذَ إِلَٰهَهُ هَوَاهُ﴾ [الجاثية: ٢٣]
            > هذا هو W = 0 أو سالب. الولاء للهوى بدلاً من الله.
            
            > ﴿وَالَّذِينَ اتَّخَذُوا مِن دُونِهِ أَوْلِيَاءَ﴾ [الزمر: ٣]
            > هذا هو B = 0. البراءة منعدمة، والولاء موجه لغير الله.
            
            **٣. تاء التبعية (اتباع طريق):**
            > ﴿وَاتَّبِعْ مِلَّةَ إِبْرَاهِيمَ حَنِيفًا﴾ [النحل: ١٢٣]
            > اتباع ملة إبراهيم هو السير على الجيوديسي المستقيم (κ = 0).
            
            > ﴿قَالُوا بَلْ نَتَّبِعُ مَا وَجَدْنَا عَلَيْهِ آبَاءَنَا﴾ [البقرة: ١٧٠]
            > هذه هي التبعية العمياء التي تبعدك عن الصراط.
            
            **الخلاصة:**
            التاء هو حرف القرار. قيمته ٤٠٠ تشير إلى ثقل الاختيار.
            كل إنسان يقول: إما أن **أتخذ** الله ورسوله والمؤمنين أولياء، أو **أتخذ** الهوى والطاغوت.
            وكل إنسان يقول: إما **أتبع** ملة إبراهيم، أو **أتبع** ما وجد عليه آباءه.
            وهذا هو جوهر معادلة الميزان.
            """,
            """
            ### The Secret of Taa (ت = 400) – The Letter of Decision and Destiny
            
            The letter **Taa (ت)** with value 400 is both a creation letter and an operator.
            Its greatest significance in the Quran is **ittikhaadh (taking/adopting)** and **ittibaa' (following)**.
            
            Taking is the decision of the heart and its choice. It determines your position on the (W, B) map:
            
            **1. Positive Taking (Loyalty):**
            > ﴿And Allah took Abraham as a friend.﴾ [An-Nisa: 125]
            > This is the peak of positive taking. Allah takes a servant as a friend. This is W = 1.
            
            **2. Negative Taking (Loyalty to Taghut):**
            > ﴿Have you seen the one who takes his desire as his god?﴾ [Al-Jathiya: 23]
            > This is W = 0 or negative. Loyalty to desire instead of Allah.
            
            > ﴿And those who take allies besides Him...﴾ [Az-Zumar: 3]
            > This is B = 0. Disavowal is absent, and loyalty is directed to other than Allah.
            
            **3. Following (A Path):**
            > ﴿And follow the way of Abraham, inclining toward truth.﴾ [An-Nahl: 123]
            > Following the way of Abraham is walking the straight geodesic (κ = 0).
            
            > ﴿They said, "Rather, we will follow that which we found our fathers doing."﴾ [Al-Baqarah: 170]
            > This is blind following that distances you from the path.
            
            **Summary:**
            Taa is the letter of decision. Its value 400 indicates the weight of choice.
            Every person says: either I **take** Allah, His Messenger, and the believers as allies, or I **take** desire and Taghut.
            And every person says: either I **follow** the way of Abraham, or I **follow** what my fathers were upon.
            This is the essence of the Mizan equation.
            """
        ))
