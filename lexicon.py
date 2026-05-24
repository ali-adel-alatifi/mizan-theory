# mizan/lexicon.py
"""
المعجم الهندسي والدليل المرجعي المتقدم
يجمع: سورة الفاتحة (دستور الثبات)، سورة الماعون (مختبر صدق العبادة)، شجرة قرارات نحو الميزان،
شجرة الإيمان والميزان، القواعد النحوية، أسرار الحروف، المفاتيح اللغوية، الآيات الجامعات،
وتحليل علاقة الحروف بقيمها ومحطات الثبات والدورة الإلهية المحكمة.
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
    
    st.header(TXT("📖 المعجم الهندسي والدليل المرجعي المتقدم", "📖 Advanced Geometric Lexicon & Reference Guide"))
    st.caption(TXT(
        "هذا المعجم هو المرجع الشامل لـ 'نحو الميزان'. يضم جميع الحروف والأدوات والمفاتيح اللغوية في القرآن الكريم، مع بيان قواعدها النحوية، ورموزها الهندسية، ومعانيها الرياضية، ووظائفها في قانون السببية الإلهي.",
        "This lexicon is the comprehensive reference for 'Nahw Al-Mizan'. It includes all letters, tools, and linguistic keys in the Quran, with their grammatical rules, geometric symbols, mathematical meanings, and functions in the divine law of causality."
    ))

    # =============================================
    # ١. سورة الفاتحة – دستور الثبات
    # =============================================
    st.markdown("---")
    st.subheader(TXT("١. سورة الفاتحة – دستور الثبات", "1. Surat Al-Fatiha – The Constitution of Stability"))
    
    st.markdown(TXT(
        """
        ### ﴿بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ﴾
        
        **الفاتحة هي دستور الثبات (S).** فيها تتجلى معادلة **S = W × B** في أنقى صورها.
        
        - **الآية ١ (بسم الله الرحمن الرحيم):** افتتاح بذكر الله (ولاء - W).
        - **الآية ٢ (الحمد لله رب العالمين):** ثناء على الله (ولاء - W).
        - **الآية ٣ (الرحمن الرحيم):** صفات الرحمة (براءة من القسوة - B).
        - **الآية ٤ (مالك يوم الدين):** الإيمان بيوم الجزاء (ثبات - S).
        - **الآية ٥ (إياك نعبد وإياك نستعين):** الولاء الخالص لله (W) والبراءة من العبادة لغير الله (B).
        - **الآية ٦ (اهدنا الصراط المستقيم):** طلب الهداية (ثبات - S).
        - **الآية ٧ (صراط الذين أنعمت عليهم غير المغضوب عليهم ولا الضالين):** التبرأ من طريق المغضوب عليهم (براءة - B) والضالين (ولاء - W).
        
        **التحليل بالميزان:**
        > **الفاتحة = W × B = S**
        > **الولاء (W) = الحمد، العبادة، الاستعانة.**
        > **البراءة (B) = التبرأ من طريق المغضوب عليهم والضالين.**
        > **الثبات (S) = الصراط المستقيم، الهداية، مالك يوم الدين.**
        """,
        """
        ### ﴿In the name of Allah, the Most Gracious, the Most Merciful.﴾
        
        **Al-Fatiha is the constitution of stability (S).** The equation **S = W × B** manifests in its purest form.
        
        - **Verse 1 (In the name of Allah...):** Opening with Allah's name (Loyalty - W).
        - **Verse 2 (Praise be to Allah...):** Praising Allah (Loyalty - W).
        - **Verse 3 (The Most Gracious, the Most Merciful):** Attributes of mercy (Disavowal of cruelty - B).
        - **Verse 4 (Master of the Day of Judgment):** Faith in the Day of Recompense (Stability - S).
        - **Verse 5 (You alone we worship...):** Pure loyalty to Allah (W) and disavowal of worshiping others (B).
        - **Verse 6 (Guide us to the straight path):** Seeking guidance (Stability - S).
        - **Verse 7 (The path of those upon whom You have bestowed favor...):** Disavowal of the path of the wrathful (B) and the astray (W).
        
        **Mizan Analysis:**
        > **Al-Fatiha = W × B = S**
        > **Loyalty (W) = Praise, worship, seeking help.**
        > **Disavowal (B) = Disavowal of the path of the wrathful and the astray.**
        > **Stability (S) = The straight path, guidance, Master of the Day of Judgment.**
        """
    ))

    # =============================================
    # ٢. سورة الماعون – مختبر صدق العبادة
    # =============================================
    st.markdown("---")
    st.subheader(TXT("٢. سورة الماعون – مختبر صدق العبادة", "2. Surat Al-Ma'un – The Laboratory of Worship Sincerity"))
    
    st.markdown(TXT(
        """
        ### ﴿أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ﴾ [الماعون: ١]
        
        **"الدين"** هنا هو **قانون السببية** (الدين القيم) و**يوم الجزاء** (يوم الدين). 
        والتكذيب به يعني **إنكار أن للأعمال نتائج**. وهذا هو أصل كل فساد.
        
        ثم يكشف الله العلامة العملية لهذا التكذيب:
        
        > ﴿فَذَٰلِكَ الَّذِي يَدُعُّ الْيَتِيمَ * وَلَا يَحُضُّ عَلَىٰ طَعَامِ الْمِسْكِينِ﴾ [الماعون: ٢-٣]
        
        فهو **قاسٍ على الضعيف** (يدع اليتيم) و**بخيل على المحتاج** (لا يحض على طعام المسكين).
        لماذا؟ لأنه كذب بالدين، فلم يعد يخشى عاقبة ظلمه، ولم يعد يرجو ثواب إحسانه.
        
        ثم تأتي المفاجأة الكبرى:
        
        > ﴿فَوَيْلٌ لِّلْمُصَلِّينَ * الَّذِينَ هُمْ عَن صَلَاتِهِمْ سَاهُونَ * الَّذِينَ هُمْ يُرَاءُونَ * وَيَمْنَعُونَ الْمَاعُونَ﴾ [الماعون: ٤-٧]
        
        لم يقل "فويل للكافرين" أو "فويل لمن لا يصلي"، بل قال: **"فويل للمصلين"**!
        
        **السر:** صلاتهم لم تثمر. صلاتهم لم تولد طاقة كافية لتغيير سلوكهم. لماذا؟
        - لأنهم **ساهون** عن الصلاة: ضعف في **الولاء (W)**.
        - ولأنهم **يراؤون**: اختلال في **البراءة (B)** (فبدلاً من البراءة من طلب رضا الناس، صاروا يطلبون رضاهم بعبادتهم).
        
        **النتيجة الحتمية:** ﴿وَيَمْنَعُونَ الْمَاعُونَ﴾. الماعون هو الشيء اليسير الذي يتعاوره الناس. 
        ومنعه هو **العلامة النهائية** على أن المعادلة مختلة: **S = 0**.
        
        **المعادلة في سورة الماعون:**
        > **W (صلاة بلا سهو) × B (إخلاص بلا رياء) = S (رحمة وعطاء)**
        > **W (صلاة مع سهو) × B (رياء) = 0 (ويل ومنع للماعون)**
        
        وحتى لو سقطت فريضة الزكاة عن إنسان لعدم بلوغه النصاب، فإن الله لم يتوقف عند هذا الحد، 
        بل أشار إلى **"الماعون"** – أبسط ما يملكه الإنسان – ليكشف **النوايا الباطلة**. 
        فمن لم يبذل حتى هذا اليسير، فقد كذب بالدين حقاً.
        """,
        """
        ### ﴿Have you seen the one who denies the Recompense?﴾ [Al-Ma'un: 1]
        
        **"Ad-Deen"** here is **the law of causality** (Al-Deen Al-Qayyim) and **the Day of Judgment** (Yawm Ad-Deen).
        Denying it means **denying that deeds have consequences**. This is the root of all corruption.
        
        Then comes the great surprise:
        
        > ﴿So woe to those who pray * who are heedless of their prayer * who make show [of their deeds] * and withhold [simple] assistance.﴾ [Al-Ma'un: 4-7]
        
        He did not say "woe to the disbelievers" or "woe to those who don't pray", but **"woe to those who pray"**!
        
        **The secret:** Their prayer did not bear fruit. Why?
        - Because they are **heedless** of prayer: weakness in **loyalty (W)**.
        - And because they **show off**: imbalance in **disavowal (B)**.
        
        **The inevitable result:** They withhold **Al-Ma'un** – the simplest things people share.
        This is the final sign that the equation is broken: **S = 0**.
        
        **The equation in Surat Al-Ma'un:**
        > **W (prayer without heedlessness) × B (sincerity without showing off) = S (mercy and giving)**
        > **W (prayer with heedlessness) × B (showing off) = 0 (woe and withholding)**
        
        Even if Zakat is not obligatory on someone due to not reaching the threshold, Allah did not stop there,
        but pointed to **"Al-Ma'un"** – the simplest things one owns – to expose **false intentions**.
        Whoever does not even give this little, has truly denied the Deen.
        """
    ))

    # =============================================
    # ٣. القواعد النحوية الأساسية
    # =============================================
    st.markdown("---")
    st.subheader(TXT("٣. القواعد النحوية الأساسية", "3. Basic Grammatical Rules"))
    
    st.markdown(TXT(
        """
        ### القاعدة ١: الفاعل هو المصدر
        في لغة الميزان، **الفاعل** هو الذي يولد الطاقة (السبب). **المصدر** هو النتيجة (الجزاء).
        
        > ﴿مَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ﴾ [الزلزلة: ٧]
        > الفاعل (مَن) = العامل (بإرادته). المصدر (خير) = نتيجة العمل (الطاقة المولدة).
        
        **القاعدة ٢: الفعل يحدد القدرة**
        نوع الفعل (ماضٍ، مضارع، أمر) يحدد نوع الطاقة المتولدة.
        - **الماضي:** طاقة ثابتة (تاريخية).
        - **المضارع:** طاقة متجددة (مستمرة).
        - **الأمر:** طاقة مكلفة (واجبة).
        
        **القاعدة ٣: الحروف هي المشغلات**
        كل حرف في القرآن هو "مشغّل" هندسي يحدد العلاقة بين الطاقة المولدة والنتيجة.
        """,
        """
        ### Rule 1: The Subject is the Source
        In the language of Mizan, the **subject** is the generator of energy (cause). The **source** is the result (recompense).
        
        > ﴿Whoever does an atom's weight of good will see it.﴾
        > The subject (whoever) = the doer. The source (good) = the result (generated energy).
        
        **Rule 2: The Verb Determines the Power**
        The type of verb (past, present, imperative) determines the type of energy generated.
        - **Past:** Fixed energy (historical).
        - **Present:** Renewable energy (continuous).
        - **Imperative:** Obligatory energy (required).
        
        **Rule 3: Letters are Operators**
        Every letter in the Quran is a geometric "operator" that determines the relationship between generated energy and result.
        """
    ))

    # =============================================
    # ٤. شجرة الإيمان والميزان
    # =============================================
    st.markdown("---")
    st.subheader(TXT("٤. شجرة الإيمان والميزان", "4. The Tree of Faith and Mizan"))
    
    st.markdown(TXT(
        """
        **شجرة الإيمان** هي تمثيل بصري لمعادلة **S = W × B**:
        
        - **الجذر:** التوحيد (W).
        - **الساق:** العبادة (W + B).
        - **الأغصان:** الولاء والبراءة (W × B).
        - **الثمرة:** الثبات (S).
        
        > ﴿كَلِمَةٌ طَيِّبَةٌ كَشَجَرَةٍ طَيِّبَةٍ أَصْلُهَا ثَابِتٌ وَفَرْعُهَا فِي السَّمَاءِ﴾ [إبراهيم: ٢٤]
        
        **التطبيق:** كلما زادت جذور الإيمان (W) وامتدت الأغصان (B)، زاد الثمر (S).
        """,
        """
        **The Tree of Faith** is a visual representation of the equation **S = W × B**:
        
        - **The Root:** Tawheed (W).
        - **The Trunk:** Worship (W + B).
        - **The Branches:** Loyalty and Disavowal (W × B).
        - **The Fruit:** Stability (S).
        
        > ﴿A good word is like a good tree, its root is firm and its branch is in the sky.﴾ [Ibrahim: 24]
        
        **Application:** The more the roots of faith (W) grow and the branches (B) extend, the greater the fruit (S).
        """
    ))

    # =============================================
    # ٥. شجرة القرارات نحو الميزان
    # =============================================
    st.markdown("---")
    st.subheader(TXT("٥. شجرة القرارات نحو الميزان", "5. The Decision Tree Towards Mizan"))
    
    st.markdown(TXT(
        """
        **شجرة القرارات** هي خريطة الطريق لتحليل أي آية أو حدث:
        
        **الخطوة ١: تحديد الأداة** (هل هي حرف، أداة شرط، أداة نفي؟)
        **الخطوة ٢: تصنيف الأداة** (أي باب من أبواب المعجم؟)
        **الخطوة ٣: تحديد الرمز الهندسي** (مثل =، →، +، ×، ⛔)
        **الخطوة ٤: استخراج المعادلة** (ما هو السبب؟ ما هي النتيجة؟)
        **الخطوة ٥: كتابة المعادلة** (باستخدام الرموز الهندسية)
        **الخطوة ٦: الربط بقانون الميزان** (S = W × B)
        """,
        """
        **The Decision Tree** is a roadmap for analyzing any verse or event:
        
        **Step 1:** Identify the tool (letter, conditional, negation?)
        **Step 2:** Classify the tool (which chapter?)
        **Step 3:** Determine the geometric symbol (=, →, +, ×, ⛔)
        **Step 4:** Extract the equation (cause? result?)
        **Step 5:** Write the equation (using geometric symbols)
        **Step 6:** Link to Mizan Law (S = W × B)
        """
    ))

    # =============================================
    # ٦. المفاتيح اللغوية – أدوات الهندسة القرآنية
    # =============================================
    st.markdown("---")
    st.subheader(TXT("٦. المفاتيح اللغوية – أدوات الهندسة القرآنية", "6. Linguistic Keys – Tools of Quranic Engineering"))
    
    st.markdown(TXT("### ١. أدوات السببية والغائية", "### 1. Causality & Purpose Tools"))
    st.markdown(f"""
    - **فاء السببية (فَـ):** علامة التساوي (=) في المعادلة الإلهية. مثال: ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ **فَ** قَدِ اسْتَمْسَكَ﴾
    - **لام التعليل (لِـ):** سهم الغاية (→). مثال: ﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا **لِ** يَعْبُدُونِ﴾
    - **حتى (حَتَّىٰ):** استمرار السبب (...) حتى تتحقق النتيجة. مثال: ﴿حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ﴾
    - **لام الأمر (لِـ):** المولد (!). مثال: ﴿**لِ** يُنفِقْ ذُو سَعَةٍ﴾
    - **لعل (لَعَلَّ):** توقع النتيجة (≈). مثال: ﴿**لَعَلَّ** كُمْ تَتَّقُونَ﴾
    """)
    
    st.markdown(TXT("### ٢. أدوات الشرط والجزاء", "### 2. Condition & Result Tools"))
    st.markdown(f"""
    - **إنْ (إِنْ):** الشرط الاختياري ( )ᵒ. مثال: ﴿**فَإِن** تَابُوا وَأَقَامُوا الصَّلَاةَ﴾
    - **إذا (إِذَا):** الشرط المحقق ( )ᶜ. مثال: ﴿**إِذَا** جَاءَ نَصْرُ اللَّهِ﴾
    - **لولا (لَوْلَا):** كشف المانع (⛔). مثال: ﴿**لَوْلَا** أَن رَّأَىٰ بُرْهَانَ رَبِّهِ﴾
    """)

    # =============================================
    # ٧. أسرار الحروف – تحليل متقدم
    # =============================================
    st.markdown("---")
    st.subheader(TXT("٧. أسرار الحروف – التحليل المتقدم", "7. Letter Secrets – Advanced Analysis"))
    
    # سر الألف
    st.markdown(TXT(
        """
        ### سر الألف (ا = 1)
        **القيمة 1 = الوحدانية المطلقة.** **التكرار 13 مرة = التجلي في عالم الكثرة.**
        
        الألف هو حرف "الأحد"، "الأول"، "الآخر"، "الظاهر"، "الباطن". وهو الحرف الوحيد الذي لا ينطق بذاته، ومع ذلك هو أساس كل كلمة.
        
        **علاقته بمحطات الثبات:** الألف هو **ولاء (W)** مطلق. هو أصل التوحيد.
        """,
        """
        ### The Secret of Alif (ا = 1)
        **Value 1 = Absolute Oneness.**
        
        Alif is the letter of "Al-Ahad", "Al-Awwal", "Al-Akhir", "Al-Zahir", "Al-Batin".
        
        **Relation to stability stations:** Alif is absolute **Loyalty (W)**. It is the origin of Tawheed.
        """
    ))
    
    # سر الميم
    st.markdown(TXT(
        """
        ### سر الميم (م = 40)
        **القيمة 40 = جمع وتماسك.** 
        
        الميم هو حرف "محمد" و "المؤمنون" و "الميزان".
        الميم في "الميزان" تشير إلى **الجمع بين W و B** للحصول على S.
        
        **علاقته بمحطات الثبات:** الميم هو **ثبات (S)**. يجمع بين الولاء والبراءة ليعطي الثبات الوجودي.
        """,
        """
        ### The Secret of Meem (م = 40)
        **Value 40 = Gathering and Cohesion.**
        
        Meem is the letter of "Muhammad", "Al-Mu'minun", and "Al-Mizan".
        Meem in "Al-Mizan" indicates **the combination of W and B** to obtain S.
        
        **Relation to stability stations:** Meem is **Stability (S)**. It combines loyalty and disavowal to give existential stability.
        """
    ))
    
    # سر القاف
    st.markdown(TXT(
        """
        ### سر القاف (ق = 100)
        **القيمة 100 = كمال العدد وأساس النسب.**
        
        القاف هو حرف "الحق"، "القيوم"، "القسط"، "الدِّينُ القَيِّم". قيمته 100 هي كمال العدد.
        
        **علاقته بمحطات الثبات:** القاف هو **البراءة (B)**. هو ميزان الحق الذي يوزن به الباطل.
        """,
        """
        ### The Secret of Qaf (ق = 100)
        **Value 100 = Completeness of number and basis of ratios.**
        
        Qaf is the letter of "Al-Haqq", "Al-Qayyum", "Al-Qist", "Ad-Deen Al-Qayyim".
        
        **Relation to stability stations:** Qaf is **Disavowal (B)**. It is the balance of truth that weighs falsehood.
        """
    ))
    
    # سر اللام
    st.markdown(TXT(
        """
        ### سر اللام (ل = 30)
        **القيمة 30 = المُلك والعدل.**
        
        اللام هو حرف "الملك"، "اللطيف"، "العدل". وهو سهم الغاية (→) الذي يحدد اتجاه المقصد.
        
        **تحليل علاقة اللام بالدورة الإلهية المحكمة:**
        - **لِـ يَعْبُدُونِ (الذاريات: ٥٦):** سهم الغاية. "اللام" هنا تحدد أن العبادة هي الغاية من الخلق. وهذا هو **ولاء (W)**.
        - **لِـ يُنفِقْ (الطلاق: ٧):** لام الأمر. "اللام" هنا تأمر بالإنفاق. وهذا هو **براءة (B)** من البخل.
        - **لِـ هُمْ الْبُشْرَىٰ (يونس: ١٦):** لام العاقبة. "اللام" تشير إلى المصير الحتمي. وهذا هو **ثبات (S)**.
        - **لِـ يَمْكَنَّهُمْ (النور: ٥٥):** لام التعليل. "اللام" تشير إلى أن التمكين هو نتيجة الثبات.
        
        **اللام في كل مرحلة من الدورة الإلهية:**
        - **التأسيس الكوني:** لِـ يَعْبُدُونِ (الغاية).
        - **البيان النظري:** لِـ يُبَيِّنَ (الوحي).
        - **الامتحان العملي:** لِـ يَبْلُوَكُمْ (الابتلاء).
        - **التطبيق المنهجي:** لِـ تُقَامَ (الشريعة).
        - **النتائج الكونية:** لِـ هُمْ الْبُشْرَىٰ (الجزاء).
        
        **اللام دليل على الحضور والتدخل الإلهي** وسريان قوانينه في كل مرحلة.
        """,
        """
        ### The Secret of Lam (ل = 30)
        **Value 30 = Kingship and Justice.**
        
        Lam is the letter of "Al-Malik", "Al-Latif", "Al-'Adl". It is the arrow of purpose (→).
        
        **Analysis of Lam in the Divine Cycle:**
        - **لِـ يَعْبُدُونِ (Adh-Dhariyat: 56):** Arrow of purpose. "Lam" specifies worship as the purpose of creation. This is **Loyalty (W)**.
        - **لِـ يُنْفِقْ (At-Talaq: 7):** Imperative Lam. "Lam" commands spending. This is **Disavowal (B)** of stinginess.
        - **لِـ هُمْ الْبُشْرَىٰ (Yunus: 16):** Result Lam. "Lam" indicates the final destiny. This is **Stability (S)**.
        - **لِـ يَمْكَنَّهُمْ (An-Nur: 55):** Causal Lam. "Lam" indicates that empowerment is the result of stability.
        
        **Lam in every stage of the Divine Cycle:**
        - **Cosmic Foundation:** لِـ يَعْبُدُونِ (Purpose).
        - **Theoretical Clarification:** لِـ يُبَيِّنَ (Revelation).
        - **Practical Trial:** لِـ يَبْلُوَكُمْ (Test).
        - **Methodological Application:** لِـ تُقَامَ (Sharia).
        - **Cosmic Results:** لِـ هُمْ الْبُشْرَىٰ (Recompense).
        
        **Lam is evidence of Divine presence and intervention** and the flow of His laws at every stage.
        """
    ))
    
    # سر التاء
    st.markdown(TXT(
        """
        ### سر التاء (ت = 400)
        **القيمة 400 = القرار والمصير.**
        
        التاء هو حرف **الاتخاذ** و **التبعية**.
        
        **تحليل علاقة التاء بالدورة الإلهية:**
        - **تَـ اتَّخَذَ اللَّهُ إِبْرَاهِيمَ خَلِيلًا (النساء: ١٢٥):** اتخاذ إيجابي (ولاء).
        - **تَـ اتَّخَذَ إِلَٰهَهُ هَوَاهُ (الجاثية: ٢٣):** اتخاذ سلبي (براءة).
        - **تَـ اتَّبِعْ مِلَّةَ إِبْرَاهِيمَ (النحل: ١٢٣):** تبعية الحق (ولاء).
        - **تَـ نَتَّبِعُ مَا وَجَدْنَا عَلَيْهِ آبَاءَنَا (البقرة: ١٧٠):** تبعية الباطل (براءة).
        
        **التاء هو حرف القرار:** إما أن تتخذ الله وأولياءه، وإما أن تتخذ الطاغوت.
        """,
        """
        ### The Secret of Taa (ت = 400)
        **Value 400 = Decision and Destiny.**
        
        Taa is the letter of **taking (ittikhaadh)** and **following (ittibaa')**.
        
        **Analysis of Taa in the Divine Cycle:**
        - **تَـ اتَّخَذَ اللَّهُ إِبْرَاهِيمَ خَلِيلًا (An-Nisa: 125):** Positive taking (Loyalty).
        - **تَـ اتَّخَذَ إِلَٰهَهُ هَوَاهُ (Al-Jathiya: 23):** Negative taking (Disavowal).
        - **تَـ اتَّبِعْ مِلَّةَ إِبْرَاهِيمَ (An-Nahl: 123):** Following truth (Loyalty).
        - **تَـ نَتَّبِعُ مَا وَجَدْنَا عَلَيْهِ آبَاءَنَا (Al-Baqara: 170):** Following falsehood (Disavowal).
        
        **Taa is the letter of decision:** Either you take Allah and His allies, or you take Taghut.
        """
    ))

    # =============================================
    # ٨. الآيات الجامعات – الإطار المرجعي النهائي
    # =============================================
    st.markdown("---")
    st.subheader(TXT("٨. الآيات الجامعات – الإطار المرجعي النهائي", "8. Key Verses – Final Reference Frame"))
    
    verses = [
        ("١. آية الفطرة والدين القيم", "﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ﴾ [الروم: ٣٠]"),
        ("٢. آية العروة الوثقى (معادلة الثبات)", "﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾ [البقرة: ٢٥٦]"),
        ("٣. آية الولاء والبراءة (دعوة كل الرسل)", "﴿وَلَقَدْ بَعَثْنَا فِي كُلِّ أُمَّةٍ رَّسُولًا أَنِ اعْبُدُوا اللَّهَ وَاجْتَنِبُوا الطَّاغُوتَ﴾ [النحل: ٣٦]"),
        ("٤. آية الميزان (قانون السببية)", "﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ﴾ [الرحمن: ٧-٨]"),
        ("٥. آية الغاية من الخلق (العبادة)", "﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ﴾ [الذاريات: ٥٦]"),
    ]
    for title, verse in verses:
        st.markdown(f"**{title}**")
        st.info(verse)

# =============================================
# ٩. تحليل الحروف وعلاقتها بمحطات الثبات (تكملة)
# =============================================
    st.markdown("---")
    st.subheader(TXT("٩. تحليل الحروف وعلاقتها بمحطات الثبات", "9. Letter Analysis & Relation to Stability Stations"))
    
    # سر الصاد
    st.markdown(TXT(
        """
        ### سر الصاد (ص = 90)
        **القيمة 90 = الصمد، الصبر، الصدق، الصلاة.**
        
        الصاد هو حرف **الصمد** (الثابت في ذاته) و **الصبر** (الثبات على الحق) و **الصدق** (الإخلاص في القول والعمل) و **الصلاة** (محطة الشحن اليومية).
        
        **تحليل علاقة الصاد بمحطات الثبات:**
        - **صـ بشر الصابرين (البقرة: ١٥٥):** الصبر هو محطة الثبات في المحن. الصاد هنا يربط بين الصبر والثبات (S). "وبشر الصابرين" تعني: بشر الذين يثبتون عند الابتلاء.
        - **صـ اركعوا مع الراكعين (البقرة: ٤٣):** الركوع هو علامة الخضوع لله. الصاد هنا يربط بين الصلاة (W) والجماعة (B). "اركعوا مع الراكعين" تعني: اتحدوا في العبادة (ولاء) وتبرأوا من الانفراد (براءة).
        - **صـ كونوا مع الصادقين (التوبة: ١١٩):** الصدق هو الإخلاص في الولاء والبراءة. "كونوا مع الصادقين" تعني: اصحبوا أهل الثبات (S).
        
        **الصاد في الدورة الإلهية:**
        - **التأسيس الكوني:** صمد (الثبات الذاتي لله).
        - **البيان النظري:** صدق (صدق الوحي).
        - **الامتحان العملي:** صبر (صبر على الابتلاء).
        - **التطبيق المنهجي:** صلاة (الصلاة محطة الشحن).
        - **النتائج الكونية:** صلاح (صلاح الأحوال).
        
        **الخلاصة:** الصاد هو **ثبات (S)**. هو حرف الصبر والصدق والصلاة، وهي كلها محطات توليد الثبات الوجودي.
        """,
        """
        ### The Secret of Sad (ص = 90)
        **Value 90 = As-Samad, Sabr, Sidq, Salah.**
        
        Sad is the letter of **As-Samad** (The Eternal), **Sabr** (Patience), **Sidq** (Truthfulness), and **Salah** (Prayer).
        
        **Analysis of Sad in the Divine Cycle:**
        - **صـ And give good news to the patient (Al-Baqarah: 155):** Patience is the station of stability in trials. Sad connects patience with stability (S).
        - **صـ Bow with those who bow (Al-Baqarah: 43):** Bowing is a sign of submission to Allah. Sad connects prayer (W) with community (B).
        - **صـ Be with the truthful (At-Tawbah: 119):** Truthfulness is sincerity in loyalty and disavowal. Sad connects truthfulness with stability (S).
        
        **Conclusion:** Sad is **Stability (S)**. It is the letter of patience, truthfulness, and prayer.
        """
    ))
    
    # سر الحاء
    st.markdown(TXT(
        """
        ### سر الحاء (ح = 8)
        **القيمة 8 = الحياة، الحفظ، الحرية، الحسنات.**
        
        الحاء هو حرف **الحياة** (الطاقة الروحية)، **الحفظ** (المناعة)، **الحرية** (الاختيار)، **الحسنات** (الأعمال الصالحة).
        
        **تحليل علاقة الحاء بمحطات الثبات:**
        - **حـ الله يحب المحسنين (آل عمران: ١٣٤):** الإحسان هو قمة الثبات. "يحب المحسنين" تعني: الله يحب الذين حققوا التوازن بين W و B.
        - **حـ ويل للمصلين (الماعون: ٤):** الويل للمصلين الذين يمنعون الماعون. الحاء هنا تشير إلى أن الحياة (W) بدون عمل صالح (B) تؤدي إلى الهلاك.
        - **حـ وحفظناها (الحجر: ٩):** حفظ الله للقرآن هو حفظ للقانون. الحاء تشير إلى أن الثبات (S) لا يتحقق إلا بحفظ القانون.
        
        **الحاء في الدورة الإلهية:**
        - **التأسيس الكوني:** حياة (الخلق).
        - **البيان النظري:** حفظ (حفظ الوحي).
        - **الامتحان العملي:** حرارة (الابتلاء يحرق الشوائب).
        - **التطبيق المنهجي:** حرية (الاختيار بين الحق والباطل).
        - **النتائج الكونية:** حسنات (الجزاء على الأعمال).
        
        **الخلاصة:** الحاء هو **الولاء (W)**. هو حرف الحياة والحفظ والحرية، وهي كلها محطات توليد الولاء لله.
        """,
        """
        ### The Secret of Ha (ح = 8)
        **Value 8 = Hayah (Life), Hifz (Protection), Hurriyyah (Freedom), Hasanat (Good Deeds).**
        
        Ha is the letter of **Life**, **Protection**, **Freedom**, and **Good Deeds**.
        
        **Analysis of Ha in the Divine Cycle:**
        - **حـ Allah loves those who do good (Al-Imran: 134):** Ihsan is the peak of stability. Ha connects goodness with stability (S).
        - **حـ Woe to those who pray (Al-Ma'un: 4):** Woe to those who pray but withhold Ma'un. Ha indicates that life (W) without good deeds (B) leads to destruction.
        - **حـ And We preserved it (Al-Hijr: 9):** Allah's preservation of the Quran is preservation of the law. Ha connects stability (S) with preserving the law.
        
        **Conclusion:** Ha is **Loyalty (W)**. It is the letter of life, protection, and freedom.
        """
    ))
    
    # سر الراء
    st.markdown(TXT(
        """
        ### سر الراء (ر = 200)
        **القيمة 200 = الرؤية، الرباط، الرجاء، الراحة.**
        
        الراء هو حرف **الرؤية** (البصيرة)، **الرباط** (الصلة بالله)، **الرجاء** (الأمل)، **الراحة** (السكينة).
        
        **تحليل علاقة الراء بمحطات الثبات:**
        - **رـ رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً (البقرة: ٢٠١):** الراء هنا تطلب الحسنة (الولاء) في الدنيا.
        - **رـ رَضِيَ اللَّهُ عَنْهُمْ وَرَضُوا عَنْهُ (المائدة: ١١٩):** الرضا هو قمة الثبات. الراء تشير إلى الرضا بين W و B.
        
        **الخلاصة:** الراء هو **الولاء (W)**. هو حرف الرؤية والرجاء والراحة.
        """,
        """
        ### The Secret of Ra (ر = 200)
        **Value 200 = Ru'yah (Vision), Ribat (Connection), Raja' (Hope), Raha (Tranquility).**
        
        Ra is the letter of **Vision**, **Connection**, **Hope**, and **Tranquility**.
        
        **Conclusion:** Ra is **Loyalty (W)**. It is the letter of vision, hope, and tranquility.
        """
    ))
    
    # سر السين
    st.markdown(TXT(
        """
        ### سر السين (س = 60)
        **القيمة 60 = السمع، السكون، السرعة، السعادة.**
        
        السين هو حرف **السمع** (الاستجابة)، **السكون** (الطمأنينة)، **السرعة** (التجاوب)، **السعادة** (الفلاح).
        
        **تحليل علاقة السين بمحطات الثبات:**
        - **سـ سَمِعْنَا وَأَطَعْنَا (البقرة: ٢٨٥):** السمع والطاعة هما أساس الولاء (W).
        - **سـ سَكِينَةٌ مِنْ رَبِّهِمْ (الفتح: ٤):** السكينة هي ثبات القلب (S).
        - **سـ سَرَعُوا إِلَىٰ مَغْفِرَةٍ (آل عمران: ١٣٣):** السرعة في التوبة هي البراءة (B).
        
        **الخلاصة:** السين هو **الولاء (W)**. هو حرف السمع والطاعة والسكينة.
        """,
        """
        ### The Secret of Seen (س = 60)
        **Value 60 = Sam' (Hearing), Sukun (Tranquility), Sur'ah (Speed), Sa'adah (Happiness).**
        
        Seen is the letter of **Hearing**, **Tranquility**, **Speed**, and **Happiness**.
        
        **Conclusion:** Seen is **Loyalty (W)**. It is the letter of hearing, obedience, and tranquility.
        """
    ))
    
    # سر الطاء
    st.markdown(TXT(
        """
        ### سر الطاء (ط = 9)
        **القيمة 9 = الطهارة، الطمأنينة، الطاعة، التطوع.**
        
        الطاء هو حرف **الطهارة** (النقاء)، **الطمأنينة** (السكينة)، **الطاعة** (الامتثال)، **التطوع** (البذل الاختياري).
        
        **تحليل علاقة الطاء بمحطات الثبات:**
        - **طـ طَهِّرْ بَيْتِيَ (الحج: ٢٦):** الطهارة هي شرط الولاء (W).
        - **طـ طَمْأَنَّتْ قُلُوبُهُمْ (الرعد: ٢٨):** الطمأنينة هي نتيجة الثبات (S).
        - **طـ طَاعَةٌ وَقَوْلٌ مَعْرُوفٌ (محمد: ٢١):** الطاعة هي لب البراءة (B).
        
        **الخلاصة:** الطاء هو **الثبات (S)**. هو حرف الطهارة والطمأنينة والطاعة.
        """,
        """
        ### The Secret of Ta (ط = 9)
        **Value 9 = Taharah (Purity), Tuma'ninah (Tranquility), Ta'ah (Obedience), Taww' (Voluntary Giving).**
        
        Ta is the letter of **Purity**, **Tranquility**, **Obedience**, and **Voluntary Giving**.
        
        **Conclusion:** Ta is **Stability (S)**. It is the letter of purity, tranquility, and obedience.
        """
    ))

# =============================================
# ١٠. جدول العلاقات بين الحروف ومحطات الثبات
# =============================================
    st.markdown("---")
    st.subheader(TXT("١٠. جدول العلاقات بين الحروف ومحطات الثبات", "10. Table of Letter Relations with Stability Stations"))
    
    letter_stability_data = [
        ("أ (1)", "الولاء (W)", "الوحدانية، التوحيد، الأحد"),
        ("ل (30)", "البراءة (B)", "المُلك، العدل، سهم الغاية (→)"),
        ("م (40)", "الثبات (S)", "الجمع، التماسك، الميزان"),
        ("ق (100)", "البراءة (B)", "الحق، القسط، الدِّينُ القَيِّم"),
        ("ص (90)", "الثبات (S)", "الصبر، الصدق، الصلاة، الصمد"),
        ("ح (8)", "الولاء (W)", "الحياة، الحفظ، الحرية، الحسنات"),
        ("ر (200)", "الولاء (W)", "الرؤية، الرباط، الرجاء، الراحة"),
        ("س (60)", "الولاء (W)", "السمع، السكون، السرعة، السعادة"),
        ("ط (9)", "الثبات (S)", "الطهارة، الطمأنينة، الطاعة، التطوع"),
        ("ف (80)", "المشغل (السببية)", "فاء السببية (=)"),
        ("و (6)", "المشغل (الضرب)", "واو المعية (×)"),
        ("ت (400)", "القرار (المصير)", "الاتخاذ، التبعية، التوبة، التيه"),
    ]
    
    df_letters = pd.DataFrame(letter_stability_data, columns=[
        TXT("الحرف", "Letter"),
        TXT("القطب", "Pole"),
        TXT("المعاني", "Meanings")
    ])
    st.dataframe(df_letters, hide_index=True, use_container_width=True)

# =============================================
# ١١. الخاتمة
# =============================================
    st.markdown("---")
    st.markdown(TXT(
        """
        ### 💎 خاتمة المعجم الهندسي والدليل المرجعي
        
        هذا المعجم هو المرجع الشامل لـ "نحو الميزان". يضم تحليلًا متقدمًا للحروف والأدوات والمفاتيح اللغوية في القرآن الكريم، مع بيان قواعدها النحوية، ورموزها الهندسية، ومعانيها الرياضية، ووظائفها في قانون السببية الإلهي.
        
        بهذا المعجم، يصبح القرآن أمامك مخططًا هندسيًا مفتوحًا. كل حرف فيه هو ترس في آلة الكون. كل أداة هي مشغل في نظام المعادلات الإلهية.
        
        **من أتقن هذه الرموز، استطاع أن يقرأ القرآن كما يقرأ المهندس المخططات، وكما يقرأ المبرمج الكود المصدري للوجود.**
        
        ﴿كِتَابٌ أَنزَلْنَاهُ إِلَيْكَ مُبَارَكٌ لِّيَدَّبَّرُوا آيَاتِهِ وَلِيَتَذَكَّرَ أُولُو الْأَلْبَابِ﴾ [ص: 29].
        """,
        """
        ### 💎 Conclusion of the Geometric Lexicon and Reference Guide
        
        This lexicon is the comprehensive reference for "Nahw Al-Mizan". It includes advanced analysis of letters, tools, and linguistic keys in the Quran, with their grammatical rules, geometric symbols, mathematical meanings, and functions in the divine law of causality.
        
        With this lexicon, the Quran becomes an open geometric blueprint before you. Every letter is a gear in the cosmic machine. Every tool is an operator in the divine equation system.
        
        **Whoever masters these symbols can read the Quran as an engineer reads blueprints, and as a programmer reads the source code of existence.**
        
        ﴿This is a blessed Book which We have sent down to you, that they may reflect upon its verses and that those of understanding may be reminded.﴾ [Sad: 29].
        """
    ))
