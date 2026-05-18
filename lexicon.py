# mizan/lexicon.py
"""
المعجم الهندسي – الحروف وقيمها وأسرارها
"""

import streamlit as st
import pandas as pd
from config import TXT, LETTERS_DB

def render_lexicon():
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
    # ٢. أسرار الحروف
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
