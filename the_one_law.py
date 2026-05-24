# mizan/the_one_law.py
"""
القانون الواحد – من الذرة إلى المجرة
يجمع تجليات القانون في مستويات الوجود + التناظر مع القوى الأربع + المعادلة الموسعة
"""

import streamlit as st
import numpy as np
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
    /* الأعمدة */
    .stColumn {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_the_one_law():
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
    st.header(TXT("⚛️ القانون الواحد", "⚛️ The One Law"))
    st.markdown(TXT(
        "### ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ [الرحمن: ٧]",
        "### And the heaven He raised and imposed the balance."
    ))
    
    # =============================================
    # ١. تجليات القانون في ستة مستويات
    # =============================================
    st.markdown("---")
    st.subheader(TXT("🔬 تجليات القانون في مستويات الوجود", "🔬 Manifestations of the Law in Levels of Existence"))
    
    # المستوى 1: الفيزياء
    st.markdown(TXT(
        """
        ### ١. قانون فيزيائي: الجذب والتنافر
        
        في قلب كل ذرة، تدور الإلكترونات حول النواة بقوة جذب كهرومغناطيسية. 
        ولولا قوة التنافر بين الإلكترونات لانهارت الذرة. 
        
        **الولاء = قوة الجذب.** **البراءة = قوة التنافر.**
        
        > F = G (m₁ × m₂) / r²  ← قانون الجذب (الولاء الكوني)
        > F = k (q₁ × q₂) / r²  ← قانون التنافر (البراءة الكونية)
        """,
        """
        ### 1. Physical Law: Attraction and Repulsion
        
        In every atom, electrons orbit the nucleus by electromagnetic attraction.
        Without repulsion between electrons, the atom would collapse.
        
        **Loyalty = Attraction.** **Disavowal = Repulsion.**
        
        > F = G (m₁ × m₂) / r²  ← Law of attraction (cosmic loyalty)
        > F = k (q₁ × q₂) / r²  ← Law of repulsion (cosmic disavowal)
        """
    ))
    
    # المستوى 2: الكيمياء
    st.markdown(TXT(
        """
        ### ٢. قانون كيميائي: الروابط وطاقة التنشيط والتوبة الجزيئية
        
        الذرّات المتآلفة تتحد بروابط كيميائية قوية (هذا **ولاؤها**). 
        ولكنها تحتاج أولاً إلى **طاقة تنشيط** لتكسر روابطها القديمة (هذه **براءتها**).
        
        **الولاء الكيميائي:** تفاعلات التخليق (Synthesis).
        **البراءة الكيميائية:** تفاعلات التفكك (Decomposition).
        **التوبة الكيميائية:** طاقة التنشيط التي تدفع الذرة لتكسر حاجزها القديم وتنطلق إلى استقرار أعظم.
        
        أليس هذا ما يحدث للمؤمن حين يتوب؟
        """,
        """
        ### 2. Chemical Law: Bonds, Activation Energy, and Molecular Repentance
        
        Compatible atoms unite with strong bonds (their **loyalty**).
        But they first need **Activation Energy** to break old bonds (their **disavowal**).
        
        **Chemical Loyalty:** Synthesis.
        **Chemical Disavowal:** Decomposition.
        **Chemical Repentance:** Activation energy breaking old barriers for greater stability.
        
        Is this not what happens to the believer when they repent?
        """
    ))

    # المستوى 3: البيولوجيا
    st.markdown(TXT(
        """
        ### ٣. قانون بيولوجي: المناعة والحماية
        
        جهاز المناعة يميز بين **الذات** و**اللا ذات**. 
        هو **يوالي** خلايا الجسم ويحميها، و**يتبرأ** من الأجسام الغريبة فيهاجمها.
        
        **الجسد السليم = ولاية صحيحة + براءة صحيحة.**
        """,
        """
        ### 3. Biological Law: Immunity and Protection
        
        The immune system distinguishes **self** from **non-self**.
        It **is loyal** to body cells and **disavows** foreign bodies.
        
        **A healthy body = correct loyalty + correct disavowal.**
        """
    ))
    
    # المستوى 4: الفطرة
    st.markdown(TXT(
        """
        ### ٤. قانون فطري: ميل النفس ونفورها
        
        كل إنسان يولد مفطوراً على حب الحق والخير والعدل (ولاء)، وبغض الظلم والشر والكذب (براءة).
        
        **الولاء والبراء ليسا تلقيناً خارجياً، بل هما استيقاظ للفطرة الأصلية.**
        """,
        """
        ### 4. Innate Law: The Soul's Inclination and Aversion
        
        Every human is born inclined to love truth and justice (loyalty) and hate oppression and falsehood (disavowal).
        
        **Loyalty and disavowal are an awakening of original nature.**
        """
    ))
    
    # المستوى 5: التاريخ
    st.markdown(TXT(
        """
        ### ٥. قانون تاريخي: صعود الأمم وسقوطها
        
        الأمم التي قامت على الحق والعدل (ولاء) ونبذت الظلم (براءة) صعدت وتمكنت.
        والأمم التي انغمست في الظلم والترف سقطت واندثرت.
        
        **قانون الولاء والبراء يفسر التاريخ كما يفسر الذرة.**
        """,
        """
        ### 5. Historical Law: Rise and Fall of Nations
        
        Nations standing on truth and justice (loyalty) and rejecting oppression (disavowal) rose.
        Nations indulging in injustice and luxury fell.
        
        **The law of loyalty and disavowal explains history as it explains the atom.**
        """
    ))
    
    # المستوى 6: الشرع
    st.markdown(TXT(
        """
        ### ٦. قانون شرعي: التطبيق الواعي
        
        بعد أن تجلى القانون في الكون والكيمياء والجسد والفطرة والتاريخ، جاء الشرع **ليُوقِظ** الإنسان إلى هذا القانون، 
        و**ليُرشده** إلى كيفية تطبيقه بوعي واختيار.
        
        الإنسان هو الكائن الوحيد المخيَّر في تطبيق هذا القانون، وهذا هو سر تكريمه وسر ابتلائه.
        """,
        """
        ### 6. Legal Law: Conscious Application
        
        After the law manifested in the cosmos, chemistry, body, nature, and history, the Sharia came **to awaken** humans to this law
        and **guide** them on how to apply it consciously.
        
        The human is the only being with choice in applying this law – the secret of honor and trial.
        """
    ))

    # =============================================
    # ٢. التناظر بين أركان الإسلام والقوى الأربع
    # =============================================
    st.markdown("---")
    st.subheader(TXT("⚛️ أركان الإسلام والقوى الأربع", "⚛️ Pillars of Islam & the Four Forces"))
    
    cosmic_table = [
        [
            TXT("الصلاة", "Prayer"),
            TXT("النووية القوية", "Strong Nuclear"),
            TXT("التخليق (Synthesis)", "Synthesis"),
            TXT("التنفس الخلوي", "Cellular Respiration"),
            TXT("W (الولاء)", "W (Loyalty)"),
        ],
        [
            TXT("الزكاة", "Zakat"),
            TXT("الكهرومغناطيسية", "Electromagnetism"),
            TXT("التوازن (Equilibrium)", "Equilibrium"),
            TXT("الدورة الدموية", "Blood Circulation"),
            TXT("B (البراءة)", "B (Disavowal)"),
        ],
        [
            TXT("الصوم", "Fasting"),
            TXT("النووية الضعيفة", "Weak Nuclear"),
            TXT("التفكك (Decomposition)", "Decomposition"),
            TXT("الالتهام الذاتي", "Autophagy"),
            TXT("B (البراءة)", "B (Disavowal)"),
        ],
        [
            TXT("الحج", "Hajj"),
            TXT("الجاذبية", "Gravity"),
            TXT("الترسيب (Precipitation)", "Precipitation"),
            TXT("الهجرة الخلوية", "Chemotaxis"),
            TXT("W (الولاء)", "W (Loyalty)"),
        ],
    ]
    
    cols = st.columns([1, 1.2, 1.2, 1.2, 0.8])
    headers = [
        TXT("الركن", "Pillar"),
        TXT("الفيزياء", "Physics"),
        TXT("الكيمياء", "Chemistry"),
        TXT("البيولوجيا", "Biology"),
        TXT("القطب", "Pole"),
    ]
    for col, h in zip(cols, headers):
        col.markdown(f"**{h}**")
    for row in cosmic_table:
        cols = st.columns([1, 1.2, 1.2, 1.2, 0.8])
        for col, val in zip(cols, row):
            col.markdown(val)

    # =============================================
    # ٣. المعادلة الموسعة
    # =============================================
    st.markdown("---")
    st.subheader(TXT("🧮 المعادلة الموسعة", "🧮 The Expanded Equation"))
    st.code("""
def calc_S_final(W, B, E, source_constants, dual_constants, manifestation_vars,
                 connection_vars, creation_positive, creation_negative, operators):
    S = W * B
    source_factor = (source_constants['ك'] * 20 + source_constants['ن'] * 50) / 2
    S *= (0.5 + 0.5 * source_factor / 100)
    dual_factor = (dual_constants['ق'] * 100 + dual_constants['ص'] * 90) / 2
    S *= (0.6 + 0.4 * dual_factor / 100)
    manifestation_boost = sum(manifestation_vars.values()) / len(manifestation_vars)
    S *= (0.5 + 0.5 * manifestation_boost)
    connection_balance = sum(connection_vars.values()) / len(connection_vars)
    S *= (0.8 + 0.4 * connection_balance)
    pos_boost = sum(creation_positive.values()) / len(creation_positive)
    S *= (1 + 0.2 * pos_boost)
    neg_effect = sum(creation_negative.values()) / len(creation_negative)
    S *= (1 - 0.3 * neg_effect)
    op_factor = operators.get('ف', 0.5) * operators.get('و', 0.5) * operators.get('ت', 0.5)
    S *= (0.8 + 0.4 * op_factor)
    if E > S:
        S -= operators.get('غ', 0.2) * (E - S) * 0.3
    return np.clip(S, 0.001, 1.0)
    """, language="python")

    # =============================================
    # ٤. الخلاصة
    # =============================================
    st.markdown("---")
    st.markdown(TXT(
        """
        ## 💎 الخلاصة: الميزان هو قانون الوجود
        
        **الولاء والبراء** هو قانون الوجود كله:
        
        - من **الذرة** (جذب وتنافر) إلى **المجرة** (جاذبية وطاقة مظلمة).
        - من **التفاعل الكيميائي** (تخليق وتفكك) إلى **التوبة** (طاقة تنشيط وانطلاق).
        - من **الخلية** (مناعة وحماية) إلى **المجتمع** (ولاء وبراءة).
        - من **الفرد** (فطرة وضمير) إلى **الأمة** (صعود وسقوط).
        - من **الدنيا** (سنن وأسباب) إلى **الآخرة** (جنة ونار).
        
        وهذا هو **الدين القيم**، وهذا هو **الإسلام الحنيف**.
        
        **S = W × B**
        """,
        """
        ## 💎 Summary: Al-Mizan is the Law of Existence
        
        **Loyalty and Disavowal** is the law of all existence:
        
        - From the **atom** to the **galaxy**.
        - From the **chemical reaction** to **repentance**.
        - From the **cell** to **society**.
        - From the **individual** to the **nation**.
        - From the **world** to the **hereafter**.
        
        This is **Al-Deen Al-Qayyim**, and this is **Al-Islam Al-Hanif**.
        
        **S = W × B**
        """
    ))
