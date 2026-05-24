# mizan/lexicon.py
"""
المعجم الهندسي – الحروف وقيمها وأسرارها
متضمناً المشغلات القيمية (ف، و) ودورها في معادلة الجزاء
"""

import streamlit as st
import pandas as pd
from config import TXT, LETTERS_DB

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
    /* جداول البيانات */
    .stDataFrame {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_lexicon():
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
    st.header(TXT("📖 المعجم الهندسي – الحروف وقيمها وأسرارها", "📖 Geometric Lexicon – Letters, Values & Secrets"))

    # =============================================
    # ١. عرض الحروف وقيمها في فئات
    # =============================================
    st.subheader(TXT("الحروف العربية وقيمها العددية", "Arabic Letters and Their Numerical Values"))

    letters_data = {
        TXT('الفئة الأولى: الذات الإلهية (المصدر)', 'Category 1: Divine Essence (Source)'):
            {'ك': 20, 'ن': 50},
        TXT('الفئة الثانية: الازدواج', 'Category 2: Duality'):
            {'ق': 100, 'ص': 90},
        TXT('الفئة الثالثة: التجلي الإلهي', 'Category 3: Divine Manifestation'):
            {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        TXT('الفئة الرابعة: الاشتراك (الجسور)', 'Category 4: Connection (Bridges)'):
            {'ع': 70, 'ي': 10, 'هـ': 5},
        TXT('الفئة الخامسة: المشغلات', 'Category 5: Operators'):
            {'ف': 80, 'و': 6, 'ب': 2},
        TXT('الفئة السادسة: أعمال الخلق', 'Category 6: Actions of Creation'):
            {'ج': 3, 'خ': 600, 'ذ': 700, 'ش': 300, 'ز': 7,
             'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
    }

    for cat, lets in letters_data.items():
        st.markdown(f"**{cat}**")
        df = pd.DataFrame(list(lets.items()), columns=[TXT('الحرف', 'Letter'), TXT('القيمة', 'Value')])
        st.dataframe(df, hide_index=True, use_container_width=True)

    # المعادلة الأولى للوجود
    st.info(TXT(
        "🔮 **المعادلة الأولى للوجود:** ك + ن = ع (20 + 50 = 70). الأمر (كُن) + النور = الإدراك (العلم).",
        "🔮 **The First Equation of Existence:** K + N = A (20 + 50 = 70). Command (Be) + Light = Perception (Knowledge)."
    ))

    st.markdown("---")

    # =============================================
    # ٢. المشغلات القيمية – فك شفرة "ف" و "و"
    # =============================================
    st.subheader(TXT("⚡ المشغلات القيمية: فك شفرة 'ف' و 'و'", "⚡ Value Operators: Decoding 'F' and 'W'"))
    
    st.markdown(TXT(
        """
        في قلب "المعجم الهندسي"، توجد أحرف ليست مجرد قيم عددية، بل هي **أوامر تشغيل** (Operators) تخبرنا كيف نتعامل مع القيم الأخرى. 
        أعظم هذه المشغلات هما **"الفاء" (ف)** و **"الواو" (و)**. إنهما ليسا مجرد حروف عطف، بل هما "شفرة" إلهية تخبرنا بطبيعة القانون.
        """,
        """
        At the heart of the "Geometric Lexicon", there are letters that are not just numerical values, but **Operation Commands** (Operators) that tell us how to deal with other values. 
        The greatest of these operators are **"Fa" (ف)** and **"Waw" (و)**. They are not just conjunctions, but a divine "code" that tells us the nature of the law.
        """
    ))

    # شرح الفاء
    st.markdown(TXT(
        """
        ### 🅵 فاء السببية (=) – مُشغّل القيمة السببية
        
        الفاء في القرآن ليست فقط للربط بين السبب والنتيجة. إنها تعلن أن **ما قبلها قيمة سببية ثابتة** في قانون الله.
        
        > **﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256]**
        
        هنا "فَـ" تجعل من "الكفر بالطاغوت" و"الإيمان بالله" **قيمتين سببيتين ثابتتين**. إنها تقول: "هذان الركنان (B و W) هما أساس المعادلة، ولا يمكن الاستغناء عنهما أو تغيير قيمتهما الجوهرية".
        
        > **﴿فَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ﴾ [الزلزلة: 7]**
        
        هنا "فَـ" تجعل من "العمل بمثقال الذرة" قيمة سببية ثابتة. أي عمل، مهما صغر، له وزن محدد في نظام الجزاء. الفاء تعلن أن هذه هي "قاعدة النظام".
        
        **في نموذجنا:** الفاء تجعل B و W ثوابت (Constants) في معادلة الحياة، وليست مجرد متغيرات.
        """,
        """
        ### 🅵 The Causative Fa (=) – The Causal Value Operator
        
        The "Fa" in the Quran not only links cause and effect, it declares that **what precedes it is a fixed causal value** in Allah's law.
        
        > **﴿So whoever disbelieves in Taghut and believes in Allah has grasped the most trustworthy handhold.﴾**
        
        Here "Fa" makes "disbelief in Taghut" and "belief in Allah" **two fixed causal values**. It says: "These two pillars (B and W) are the foundation of the equation, and their essential value cannot be dispensed with or changed."
        
        > **﴿So whoever does an atom's weight of good will see it.﴾**
        
        Here "Fa" makes "doing an atom's weight of good" a fixed causal value. Any deed, no matter how small, has a specific weight in the system of recompense. Fa declares that this is the "system's rule".
        
        **In our model:** Fa makes B and W Constants in the equation of life, not mere variables.
        """
    ))

    # شرح الواو
    st.markdown(TXT(
        """
        ### 🅆 واو العطف (×) – مُشغّل الضرب والجمع
        
        الواو في القرآن، خاصة في سياق الجزاء، هي **مشغّل الفصل والضرب**. إنها تقسم الناس إلى فئات، وتضرب كل فئة في جزائها.
        
        > **﴿فَأَمَّا مَنْ أُوتِيَ كِتَابَهُ بِيَمِينِهِ... وَأَمَّا مَنْ أُوتِيَ كِتَابَهُ بِشِمَالِهِ...﴾ [الحاقة: 19-25]**
        
        هنا "الواو" في "وأما" تقسم البشر إلى فئتين: فئة W العالية (أهل اليمين)، وفئة W المنخفضة (أهل الشمال). وهي **تضرب** كل فئة في مصيرها:
        
        > `(أهل اليمين × نعيم) + (أهل الشمال × جحيم) = المشهد النهائي`
        
        الواو هنا هي التي تنفذ عملية الضرب هذه. إنها "المشغّل" الذي يوزع المصير بناءً على قيمة W.
        """,
        """
        ### 🅆 The Conjunctive Waw (×) – The Multiplication Operator
        
        The "Waw" in the Quran, especially in the context of recompense, is **the operator of separation and multiplication**. It divides people into categories and multiplies each category by its recompense.
        
        > **﴿Then as for he who is given his record in his right hand... But as for he who is given his record in his left hand...﴾**
        
        Here the "Waw" in "But as for" divides humanity into two groups: the high-W group (people of the right), and the low-W group (people of the left). It **multiplies** each group by its destiny:
        
        > `(People of the right × Bliss) + (People of the left × Hellfire) = The final scene`
        
        The Waw here is what executes this multiplication process. It is the "operator" that distributes destiny based on the value of W.
        """
    ))

    st.markdown("---")

    # =============================================
    # ٣. أسرار الحروف (الألف، الميم، القاف، التاء)
    # =============================================
    st.subheader(TXT("أسرار الحروف", "Secrets of the Letters"))
    
    # سر الألف
    st.markdown(TXT(
        """
        ### سر الألف (ا = 1)
        
        **القيمة 1 = الوحدانية المطلقة.**
        **التكرار 13 مرة في فواتح السور = التجلي في عالم الكثرة (الخلق).**
        
        هذا ليس تناقضًا، بل هو السر الأعظم:
        - الله واحد في ذاته (قيمته 1)، ولكنه متجلي في خلقه (تكراره 13).
        - الألف هو الحرف الوحيد الذي لا ينطق بذاته، ومع ذلك هو أساس كل كلمة.
        - إنه مثل "الله": لا تدركه الأبصار، ولكن كل شيء يدل عليه.
        
        **العلاقة مع الأسماء الحسنى:**
        الألف هو حرف "الأحد"، "الأول"، "الآخر"، "الظاهر"، "الباطن".
        """,
        """
        ### The Secret of Alif (ا = 1)
        
        **Value 1 = Absolute Oneness.**
        **Frequency 13 in Quranic openings = Manifestation in the world of multiplicity.**
        
        - Allah is One in His Essence (value 1), yet manifested in His creation (frequency 13).
        - Alif has no sound of its own, yet it is the basis of every word.
        - It is like "Allah": vision does not perceive Him, yet everything points to Him.
        
        **Relation to the Beautiful Names:**
        Alif is the letter of "Al-Ahad", "Al-Awwal", "Al-Akhir", "Al-Zahir", "Al-Batin".
        """
    ))

    # سر الميم
    st.markdown(TXT(
        """
        ### منظومة (الم) – قاعدة الأسماء
        
        الحروف الثلاثة (ا، ل، م) هي البصمة الصوتية لأعظم اسم: **الله**.
        والقرآن يفتتح بها 6 سور (بعدد أيام الخلق)، لأنها "أم الكتاب" و"أم الأسماء".
        
        | الحرف | الرمز | أمثلة من أسماء الله | معانيها |
        |:---|:---|:---|:---|
        | **أ** | الوحدانية | الأحد، الأول، الآخر | أصل كل شيء |
        | **ل** | المُلك والعدل | الملك، اللطيف، العدل | الله هو المَلِك |
        | **م** | الجمع والعطاء | المعطي، المانع، المحيي، المميت | أسماء الأفعال |
        
        عندما تقرأ "الم"، فأنت تستحضر كل هذه الأسماء. ولهذا قال النبي ﷺ:
        "لا أقول الم حرف، ولكن ألف حرف، ولام حرف، وميم حرف".
        """,
        """
        ### The (ALM) System – Foundation of Names
        
        The three letters (A, L, M) are the sound signature of the greatest name: **Allah**.
        The Quran opens with them in 6 suras.
        
        | Letter | Symbol | Examples of Allah's Names | Meanings |
        |:---|:---|:---|:---|
        | **A** | Oneness | Al-Ahad, Al-Awwal | Origin of all |
        | **L** | Kingship | Al-Malik, Al-Latif | Allah is the King |
        | **M** | Giving | Al-Mu'ti, Al-Mani' | Names of actions |
        
        When you recite "ALM", you evoke all these names.
        """
    ))

    # سر القاف
    st.markdown(TXT(
        """
        ### سر حرف القاف (ق = 100) – حرف الميزان
        
        حرف **القاف** هو حرف "الحق" و"القيوم" و"القسط" و"الدِّينُ القَيِّم". قيمته 100 هي كمال العدد وأساس النسب.
        
        للقاف وجهان:
        - **وجه ثابت في الذات الإلهية:** الحق، القيوم. وهذا ثابت لا يتغير.
        - **وجه متجلي في الخلق:** القسط (العدل)، الدِّينُ القَيِّم. وهذا ما أُمر الناس بإقامته.
        
        و"الدِّينُ القَيِّمُ" هو القانون الإلهي الحق الثابت، ميزان الله الذي فطر الناس عليه، والذي لا تبديل فيه.
        """,
        """
        ### The Secret of Qaf (ق = 100) – The Letter of the Balance
        
        The letter **Qaf** is the letter of "Al-Haqq", "Al-Qayyum", "Al-Qist", and "Ad-Deen Al-Qayyim".
        
        Qaf has two faces:
        - **Fixed in the Divine Essence:** Al-Haqq, Al-Qayyum. Unchanging.
        - **Manifested in creation:** Al-Qist (justice), Ad-Deen Al-Qayyim. Commanded to be established.
        
        "Ad-Deen Al-Qayyim" is the divine law, the balance of Allah upon which people were created.
        """
    ))

    # سر التاء
    st.markdown(TXT(
        """
        ### سر حرف التاء (ت = 400) – حرف القرار والمصير
        
        حرف **التاء** هو حرف **الاتخاذ** و**التبعية**.
        
        **الاتخاذ الإيجابي (الولاء):**
        > ﴿وَاتَّخَذَ اللَّهُ إِبْرَاهِيمَ خَلِيلًا﴾ [النساء: ١٢٥]
        
        **الاتخاذ السلبي (الولاء للطاغوت):**
        > ﴿أَفَرَأَيْتَ مَنِ اتَّخَذَ إِلَٰهَهُ هَوَاهُ﴾ [الجاثية: ٢٣]
        
        **التبعية:**
        > ﴿وَاتَّبِعْ مِلَّةَ إِبْرَاهِيمَ حَنِيفًا﴾ [النحل: ١٢٣]
        > ﴿قَالُوا بَلْ نَتَّبِعُ مَا وَجَدْنَا عَلَيْهِ آبَاءَنَا﴾ [البقرة: ١٧٠]
        
        التاء هو حرف القرار. إما أن تتخذ الله وأولياءه، وإما أن تتخذ الطاغوت. إما أن تتبع ملة إبراهيم، وإما أن تتبع الأهواء. وهذا هو جوهر S = W × B.
        """,
        """
        ### The Secret of Taa (ت = 400) – The Letter of Decision
        
        The letter **Taa** is the letter of **taking (ittikhaadh)** and **following (ittibaa')**.
        
        **Positive Taking (Loyalty):**
        > ﴿And Allah took Abraham as a friend.﴾ [An-Nisa: 125]
        
        **Negative Taking (Disavowal failure):**
        > ﴿Have you seen the one who takes his desire as his god?﴾ [Al-Jathiya: 23]
        
        **Following:**
        > ﴿And follow the way of Abraham, inclining toward truth.﴾ [An-Nahl: 123]
        > ﴿They said, "Rather, we will follow that which we found our fathers doing."﴾ [Al-Baqara: 170]
        
        Taa is the letter of decision. Either you take Allah and His allies, or you take Taghut. This is the essence of S = W × B.
        """
    ))

    # سر الفاء والواو كمشغلات
    st.markdown(TXT(
        """
        ### سر الفاء (ف = 80) والواو (و = 6) – المشغلات الإلهية
        
        **الفاء (ف = 80):** علامة التساوي (=) في المعادلة الإلهية، ومُشغّل القيمة السببية.
        > ﴿**فَـ** مَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ **فَـ** قَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256]
        الفاء الأولى تعلن أن ما بعدها سبب معياري ثابت في قانون الله. الفاء الثانية تربط السبب بالنتيجة حتماً.
        
        **الواو (و = 6):** أداة العطف (× أو +)، تجمع بين الطرفين في المعادلة.
        > «أَوْثَقُ عُرَى الْإِيمَانِ: الْحُبُّ فِي اللَّهِ، وَالْبُغْضُ فِي اللَّهِ»
        الواو هنا واو المعية (×)، لأن الإيمان لا يكتمل إلا باجتماعهما معًا.
        
        **المعادلة:** **فَـ** (B) × (W) = S
        حيث "فَـ" هي مُشغّل القيمة السببية الذي يعلن أن B و W قيمتان ثابتتان في نظام الله.
        """,
        """
        ### The Secret of Fa (ف = 80) and Waw (و = 6) – The Divine Operators
        
        **Fa (ف = 80):** The equals sign (=) in the divine equation, and the causal value operator.
        > ﴿**So** whoever disbelieves in Taghut and believes in Allah **has** grasped the firm handhold.﴾ [Al-Baqarah: 256]
        The first Fa declares that what follows is a standard cause in Allah's law. The second Fa links cause to result inevitably.
        
        **Waw (و = 6):** The conjunction operator (× or +), combining both sides of the equation.
        > "The firmest handhold of faith is: love for the sake of Allah, **and** hatred for the sake of Allah."
        The "and" here is multiplication (×), because faith is only complete with both together.
        
        **The equation:** **Fa** (B) × (W) = S
        Where "Fa" is the causal value operator declaring that B and W are fixed values in Allah's system.
        """
    ))
