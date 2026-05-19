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
    # ... (باقي شرح أسرار الحروف كما هو في ملفك الأصلي)
