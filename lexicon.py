# mizan/geometric_lexicon.py
"""
المعجم الهندسي الشامل للقرآن الكريم
النسخة النهائية – صرح واحد يلتقي فيه الوحي بالعلم والفلسفة والتاريخ
"""

import streamlit as st
import pandas as pd
from config import TXT

def render_geometric_lexicon():
    st.header(TXT("📖 المعجم الهندسي للقرآن", "📖 The Geometric Lexicon of the Quran"))
    
    # =============================================
    # المقدمة: لماذا المعجم الهندسي؟
    # =============================================
    with st.expander(TXT("📜 مقدمة: لماذا المعجم الهندسي؟", "📜 Introduction: Why a Geometric Lexicon?"), expanded=True):
        st.markdown(TXT(
            """
            <div style="background:rgba(20,30,60,0.7); border-radius:15px; padding:25px; margin:15px 0; border:1px solid #FFD700; line-height:2.2;">
            <p>الحمد لله الذي جعل في كل حرف من كتابه آية، وفي كل كلمة معجزة، وفي كل آية نظامًا محكمًا.</p>
            
            <p>هذا المعجم ليس كغيره من المعاجم. إنه ليس مجرد جدول للحروف العربية بقيمها العددية. بل هو <b>محاولة متواضعة</b> – نعم، متواضعة – لفك شفرة من شفرات القرآن الكريم، لعلنا نقترب خطوة من فهم قوله تعالى: ﴿وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِّكُلِّ شَيْءٍ﴾.</p>
            
            <p>إنه يقوم على فرضية جريئة، ولكنها تستند إلى أدلة متراكمة: <b>أن الحروف العربية ليست مجرد أصوات، بل هي بصمات وجودية، تحمل قيمًا عددية ثابتة (حساب الجمل)، وأدوارًا رياضية في معادلة "الميزان" التي تحكم الوجود كله.</b></p>
            
            <p>في هذا المعجم، سنرى كيف يتجلى:</p>
            <ul>
                <li>🧬 <b>قدسية الوحي:</b> في استناد كل تصنيف إلى آيات الكتاب الحكيم وفواتح السور.</li>
                <li>⚛️ <b>دقة العلم:</b> في استخدام حساب الجمل (نظام أبجد هوز) وقيم الحروف الثابتة عبر التاريخ.</li>
                <li>💭 <b>عمق الفلسفة:</b> في التأمل في معاني الحروف الوجودية: المصدر، التجلي، الاشتراك.</li>
                <li>📜 <b>حكمة التاريخ:</b> في النظر إلى تكرار الحروف في فواتح السور، وربطها بأحداث الوجود الكبرى (أيام الخلق، السماوات السبع).</li>
                <li>🕋 <b>تواضع العارفين:</b> في الإقرار بأن هذا كله ليس إلا قطرة من بحر علم الله الذي لا قاع له، وأننا إن أصبنا فمن الله، وإن أخطأنا فمن أنفسنا، لقوله تعالى: ﴿وَمَا أُوتِيتُم مِّنَ الْعِلْمِ إِلَّا قَلِيلًا﴾.</li>
            </ul>
            </div>
            """,
            """
            <div style="background:rgba(20,30,60,0.7); border-radius:15px; padding:25px; margin:15px 0; border:1px solid #FFD700; line-height:2.2;">
            <p>This lexicon is unlike any other. It is a humble attempt to decode one of the codes of the Noble Quran.</p>
            
            <p>It rests on a bold hypothesis: that Arabic letters are not mere sounds, but existential fingerprints, carrying fixed numerical values (Abjad numerals) and mathematical roles in the equation of "Al-Mizan" that governs all existence.</p>
            
            <p>In this lexicon, we witness the convergence of:</p>
            <ul>
                <li>🧬 <b>The Sanctity of Revelation</b></li>
                <li>⚛️ <b>The Precision of Science</b></li>
                <li>💭 <b>The Depth of Philosophy</b></li>
                <li>📜 <b>The Wisdom of History</b></li>
                <li>🕋 <b>The Humility of the Knowers</b></li>
            </ul>
            </div>
            """
        ))

    # =============================================
    # ١. الأساس: نظام أبجد هوز (حساب الجمل)
    # =============================================
    with st.expander(TXT("١. الأساس: نظام أبجد هوز (حساب الجمل)", "1. Foundation: The Abjad Hawaz System"), expanded=False):
        st.markdown(TXT(
            """
            قبل الإسلام، كان العرب يستخدمون نظامًا عدديًا يعتمد على الحروف الأبجدية. لكل حرف قيمة عددية ثابتة. هذا النظام يُعرف بـ **"حساب الجمل"** أو **"أبجد هوز"**. وهو نظام دقيق وموثق، استخدمه العلماء المسلمون الأوائل في التأريخ للأحداث، وفي علوم الحرف والعدد.
            
            هذا الجدول ليس "اختراعًا" شخصيًا. إنه جزء من التراث اللغوي العربي. ونحن نستخدم هذه القيم كمُدخلات ثابتة (Constants) في نظام حاسوبي حي، يحاكي المعادلة الكونية.
            """,
            """
            Before Islam, Arabs used a numerical system based on the alphabet. Each letter has a fixed numerical value. This system is known as **"Abjad numerals"** or **"Abjad Hawaz"**. It is a precise and documented system, used by early Muslim scholars for dating events and in the sciences of letters and numbers.
            
            This table is not a personal "invention". It is part of the Arabic linguistic heritage. We use these values as fixed inputs (Constants) in a living computer system that simulates the cosmic equation.
            """
        ))
        
        # جدول أساسي
        abjad_table = [
            ["الآحاد", "أ", "ب", "ج", "د", "هـ", "و", "ز", "ح", "ط"],
            ["", 1, 2, 3, 4, 5, 6, 7, 8, 9],
            ["العشرات", "ي", "ك", "ل", "م", "ن", "س", "ع", "ف", "ص"],
            ["", 10, 20, 30, 40, 50, 60, 70, 80, 90],
            ["المئات", "ق", "ر", "ش", "ت", "ث", "خ", "ذ", "ض", "ظ"],
            ["", 100, 200, 300, 400, 500, 600, 700, 800, 900],
            ["الألف", "غ", "", "", "", "", "", "", "", ""],
            ["", 1000, "", "", "", "", "", "", "", ""],
        ]
        df_abjad = pd.DataFrame(abjad_table)
        st.table(df_abjad)

    # =============================================
    # ٢. التصنيف الوجودي للحروف – الفئات الست
    # =============================================
    with st.expander(TXT("٢. التصنيف الوجودي للحروف – الفئات الست", "2. Existential Classification – The Six Categories"), expanded=True):
        st.markdown(TXT(
            """
            هذا هو قلب المعجم. لقد قمنا بتصنيف الحروف الثمانية والعشرين إلى **ست فئات وجودية**، بناءً على خصائصها الصفاتية، وتكرارها في فواتح السور، وسياقاتها القرآنية. كل فئة تمثل مرتبة من مراتب الوجود، ولها دور رياضي محدد في معادلة الميزان.
            """,
            """
            This is the heart of the lexicon. We have classified the twenty-eight letters into **six existential categories**, based on their qualitative properties, frequency in Quranic openings, and Quranic contexts. Each category represents a level of existence and has a specific mathematical role in the Mizan equation.
            """
        ))
        
        # عرض الفئات الست
        categories = {
            TXT("الفئة الأولى: حروف الذات الإلهية (المصدر)", "Cat 1: Divine Essence (Source)"): {
                'letters': {'ك': 20, 'ن': 50},
                'desc': TXT(
                    "حرفان فقط يمثلان صفات الله الخاصة التي لا يشاركه فيها أحد. هما المصدر الذي تنبثق منه كل الصفات. ظهورهما في فواتح السور مرة واحدة فقط (في سورتي مريم والقلم) يدل على التفرد والوحدانية.",
                    "Only two letters represent Allah's exclusive attributes. They are the source from which all other attributes emanate. Their single appearance in Quranic openings indicates uniqueness and oneness."
                )
            },
            TXT("الفئة الثانية: حروف الازدواج (ثابت ومتجلي)", "Cat 2: Duality (Fixed & Manifested)"): {
                'letters': {'ق': 100, 'ص': 90},
                'desc': TXT(
                    "حرفان لهما وجهان: وجه ثابت في الذات الإلهية (الحق، الصمد)، ووجه متجلي في الخلق (القسط، الصبر). يظهران منفردين (سورتا ق وص) ومع غيرهما (سورتا الشورى ومريم)، للدلالة على جمعهما بين الثبات والتغير.",
                    "Two letters with two faces: one fixed in the Divine Essence (The Truth, The Eternal), and one manifested in creation (Justice, Patience). They appear alone and with others, indicating their combination of constancy and change."
                )
            },
            TXT("الفئة الثالثة: حروف التجلي الإلهي", "Cat 3: Divine Manifestation"): {
                'letters': {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
                'desc': TXT(
                    "سبعة حروف تمثل صفات الله المتجلية في خلقه. تكرارها الكبير في فواتح السور (أ=13، ل=13، م=17...) يدل على تعدد التجليات مع وحدة المصدر. وهي تعمل 'كمُوَلِّدات' ترفع قيمتي W و B في المعادلة.",
                    "Seven letters representing Allah's attributes manifested in His creation. Their frequent repetition in Quranic openings indicates the multiplicity of manifestations with the unity of the source. They act as 'generators' raising the values of W and B in the equation."
                )
            },
            TXT("الفئة الرابعة: حروف الاشتراك (الجسور)", "Cat 4: Connection (Bridges)"): {
                'letters': {'ع': 70, 'ي': 10, 'هـ': 5},
                'desc': TXT(
                    "ثلاثة حروف تمثل القنوات التي تربط عالم الغيب بعالم الشهادة. هي الجسور التي يعبر عليها الإدراك (ع)، والنداء (ي)، والهوية (هـ). وهي تمثل 'عوامل الاتزان' التي تضبط العلاقة بين W و B.",
                    "Three letters representing the channels connecting the Unseen world with the Seen world. They are the bridges for perception ('A), calling (Y), and identity (H). They act as 'balance factors' regulating the relationship between W and B."
                )
            },
            TXT("الفئة الخامسة: المشغلات المفتاحية", "Cat 5: Key Operators"): {
                'letters': {'ف': 80, 'و': 6, 'ب': 2, 'ل': 30},
                'desc': TXT(
                    "أربعة حروف تمثل أدوات المنطق والسببية في كلام الله. هي التي تحدد كيفية تفاعل الأسباب مع النتائج. فالفاء (=) للسببية، والواو (×) للضرب، والباء (بـ) للاستعانة، واللام (→) للتعليل.",
                    "Four letters representing the tools of logic and causality in Allah's speech. They determine how causes interact with results. Fa (=) for causality, Waw (×) for multiplication, Ba (by) for assistance, Lam (→) for purpose."
                )
            },
            TXT("الفئة السادسة: حروف أعمال الخلق", "Cat 6: Actions of Creation"): {
                'letters': {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
                'desc': TXT(
                    "أحد عشر حرفًا تمثل صفات وأفعال خاصة بالخلق. كل حرف منها له وجهان: إيجابي (إذا استُخدم في طاعة الله) وسلبي (إذا استُخدم في معصيته). وهي تمثل 'الإرادة الحرة' للإنسان، وتحدد قيمتها حسب توجيهه لها.",
                    "Eleven letters representing qualities and actions specific to creation. Each has two faces: positive (when used in obeying Allah) and negative (when used in disobeying Him). They represent human 'free will', and their values are determined by their direction."
                )
            },
        }
        
        for cat, data in categories.items():
            st.markdown(f"### {cat}")
            st.info(data['desc'])
            df = pd.DataFrame(list(data['letters'].items()), columns=[TXT('الحرف', 'Letter'), TXT('القيمة', 'Value')])
            st.dataframe(df, hide_index=True, use_container_width=True)
            st.markdown("---")

    # =============================================
    # ٣. جدول الحروف الكامل (28 حرفًا)
    # =============================================
    with st.expander(TXT("٣. جدول الحروف الكامل (28 حرفًا)", "3. Complete Letter Table (28 Letters)"), expanded=False):
        full_table = [
            ("ك", 20, TXT("الذات الإلهية", "Divine Essence"), TXT("ثابت الأمر والتكوين", "Constant of Command"), TXT("—", "—"), TXT("—", "—")),
            ("ن", 50, TXT("الذات الإلهية", "Divine Essence"), TXT("ثابت النور الذاتي", "Constant of Intrinsic Light"), TXT("—", "—"), TXT("—", "—")),
            ("ق", 100, TXT("الازدواج", "Duality"), TXT("ثابت الميزان / متغير القسط", "Fixed Balance / Variable Justice"), TXT("—", "—"), TXT("—", "—")),
            ("ص", 90, TXT("الازدواج", "Duality"), TXT("ثابت الصمد / متغير الصبر والصدق", "Fixed Eternal / Variable Patience"), TXT("—", "—"), TXT("—", "—")),
            ("أ", 1, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("مُوَلِّد W", "W Generator"), TXT("الوحدانية", "Oneness"), TXT("—", "—")),
            ("ل", 30, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("مُوَلِّد B", "B Generator"), TXT("المُلك والعدل", "Kingship & Justice"), TXT("—", "—")),
            ("م", 40, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("مُوَلِّد S", "S Generator"), TXT("الجمع والتماسك", "Gathering & Cohesion"), TXT("—", "—")),
            ("ر", 200, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("مُوَلِّد المقاومة", "Resistance Generator"), TXT("اليقظة والمراقبة", "Awakening & Watching"), TXT("—", "—")),
            ("س", 60, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("مُوَلِّد الاستجابة", "Response Generator"), TXT("السمع", "Hearing"), TXT("—", "—")),
            ("ح", 8, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("مُوَلِّد الاستدامة", "Sustainability Generator"), TXT("الحياة", "Life"), TXT("—", "—")),
            ("ط", 9, TXT("التجلي الإلهي", "Divine Manifestation"), TXT("مُوَلِّد المناعة", "Immunity Generator"), TXT("الطهارة", "Purity"), TXT("—", "—")),
            ("ع", 70, TXT("الاشتراك (الجسور)", "Connection (Bridges)"), TXT("جسر الإدراك والرؤية", "Bridge of Perception"), TXT("—", "—"), TXT("—", "—")),
            ("ي", 10, TXT("الاشتراك (الجسور)", "Connection (Bridges)"), TXT("جسر النداء والنسبة", "Bridge of Calling"), TXT("—", "—"), TXT("—", "—")),
            ("هـ", 5, TXT("الاشتراك (الجسور)", "Connection (Bridges)"), TXT("جسر الهوية والحضور", "Bridge of Identity"), TXT("—", "—"), TXT("—", "—")),
            ("ف", 80, TXT("المشغلات", "Operators"), TXT("علامة التساوي (=)", "Equality Sign (=)"), TXT("—", "—"), TXT("—", "—")),
            ("و", 6, TXT("المشغلات", "Operators"), TXT("الضرب (×) أو الجمع (+)", "Multiplication (×) or Addition (+)"), TXT("—", "—"), TXT("—", "—")),
            ("ب", 2, TXT("المشغلات", "Operators"), TXT("مفتاح الاستعانة (بـ)", "Key of Assistance (by)"), TXT("—", "—"), TXT("—", "—")),
            ("ل", 30, TXT("المشغلات", "Operators"), TXT("سهم التعليل (→)", "Arrow of Purpose (→)"), TXT("—", "—"), TXT("—", "—")),
            ("ج", 3, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الجهاد، الجود", "Striving, Generosity"), TXT("الجهل، الجحود", "Ignorance, Denial")),
            ("خ", 600, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الخير، الخشية", "Good, Awe"), TXT("الخيانة، الخذلان", "Betrayal, Abandonment")),
            ("د", 4, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الدين، الدعوة", "Religion, Calling"), TXT("التدمير", "Destruction")),
            ("ذ", 700, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الذكر", "Remembrance"), TXT("الذل، الذنب", "Humiliation, Sin")),
            ("ز", 7, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الزكاة، الزهد", "Purification, Asceticism"), TXT("الزور، الزيغ", "Falsehood, Deviation")),
            ("ش", 300, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الشكر، الشجاعة", "Gratitude, Courage"), TXT("الشهوة، الشرك", "Lust, Polytheism")),
            ("ت", 400, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("التوبة، التقوى", "Repentance, Piety"), TXT("التيه", "Wandering")),
            ("ث", 500, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الثبات، الثواب", "Steadfastness, Reward"), TXT("الثبور", "Destruction")),
            ("ض", 800, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الضياء", "Radiance"), TXT("الضلال", "Misguidance")),
            ("ظ", 900, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الظفر", "Victory"), TXT("الظلم", "Injustice")),
            ("غ", 1000, TXT("أعمال الخلق", "Actions of Creation"), TXT("إرادة حرة (±)", "Free Will (±)"), TXT("الغفران", "Forgiveness"), TXT("الغل", "Malice")),
        ]
        
        df_full = pd.DataFrame(full_table, columns=[
            TXT("الحرف", "Letter"), TXT("القيمة", "Value"), TXT("الفئة", "Category"),
            TXT("الدور في المعادلة", "Role in Equation"), TXT("الوجه الإيجابي", "Positive Face"), TXT("الوجه السلبي", "Negative Face")
        ])
        st.dataframe(df_full, hide_index=True, use_container_width=True)

    # =============================================
    # ٤. أسرار الحروف: الألف، الميم، القاف، التاء
    # =============================================
    with st.expander(TXT("٤. أسرار الحروف: الألف، الميم، القاف، التاء", "4. Letter Secrets: Alif, Meem, Qaf, Taa"), expanded=False):
        st.markdown(TXT(
            """
            ### سر الألف (ا = 1): الوحدانية في الكثرة
            **القيمة 1 = الوحدانية المطلقة.** **التكرار 13 مرة في فواتح السور = التجلي في عالم الكثرة.**
            الألف هو الحرف الوحيد الذي لا ينطق بذاته، ومع ذلك هو أساس كل كلمة. إنه مثل "الله": لا تدركه الأبصار، ولكن كل شيء يدل عليه.
            """,
            """
            ### The Secret of Alif (ا = 1): Oneness in Multiplicity
            **Value 1 = Absolute Oneness.** **Frequency 13 in openings = Manifestation in multiplicity.**
            Alif has no sound of its own, yet is the basis of every word. It is like "Allah": vision does not perceive Him, yet everything points to Him.
            """
        ))
        st.markdown(TXT(
            """
            ### منظومة (الم): قاعدة الأسماء الحسنى
            الحروف الثلاثة (ا، ل، م) هي البصمة الصوتية لأعظم اسم: **الله**. القرآن يفتتح بها 6 سور (بعدد أيام الخلق).
            | الحرف | الرمز | أمثلة من أسماء الله |
            |:---|:---|:---|
            | **أ** | الوحدانية | الأحد، الأول، الآخر |
            | **ل** | المُلك والعدل | الملك، اللطيف، العدل |
            | **م** | الجمع والعطاء | المعطي، المانع، المحيي، المميت |
            """,
            """
            ### The (ALM) System: Foundation of the Beautiful Names
            The three letters (A, L, M) are the sound signature of the greatest name: **Allah**. The Quran opens with them in 6 suras (the days of creation).
            | Letter | Symbol | Examples of Allah's Names |
            |:---|:---|:---|
            | **A** | Oneness | The One, The First, The Last |
            | **L** | Kingship | The King, The Subtle, The Just |
            | **M** | Giving | The Giver, The Withholder, The Giver of Life |
            """
        ))
        st.markdown(TXT(
            """
            ### سر حرف القاف (ق = 100): حرف الميزان
            حرف **القاف** هو حرف "الحق" و"القيوم" و"القسط" و"الدِّينُ القَيِّم". قيمته 100 هي كمال العدد وأساس النسب.
            **وجهه الثابت:** الحق، القيوم. **وجهه المتجلي:** القسط (العدل)، الدِّينُ القَيِّم.
            """,
            """
            ### The Secret of Qaf (ق = 100): The Letter of the Balance
            The letter **Qaf** is the letter of "The Truth", "The Self-Subsisting", "Justice", and "The Upright Religion". Its value 100 is numerical perfection.
            **Its fixed face:** The Truth, The Self-Subsisting. **Its manifested face:** Justice, The Upright Religion.
            """
        ))
        st.markdown(TXT(
            """
            ### سر حرف التاء (ت = 400): حرف القرار والمصير
            حرف **التاء** هو حرف **الاتخاذ** و**التبعية**. إما أن تتخذ الله وأولياءه، وإما أن تتخذ الطاغوت. إما أن تتبع ملة إبراهيم، وإما أن تتبع الأهواء.
            > ﴿وَاتَّخَذَ اللَّهُ إِبْرَاهِيمَ خَلِيلًا﴾ (ولاء)
            > ﴿أَفَرَأَيْتَ مَنِ اتَّخَذَ إِلَٰهَهُ هَوَاهُ﴾ (طاغوت)
            """,
            """
            ### The Secret of Taa (ت = 400): The Letter of Decision
            The letter **Taa** is the letter of **taking** and **following**. Either you take Allah and His allies, or you take Taghut. Either you follow the way of Abraham, or you follow desires.
            > ﴿And Allah took Abraham as a friend.﴾ (Loyalty)
            > ﴿Have you seen the one who takes his desire as his god?﴾ (Taghut)
            """
        ))

    # =============================================
    # ٥. المعادلات الوجودية: من "كُن" إلى "هو"
    # =============================================
    with st.expander(TXT("٥. المعادلات الوجودية: من 'كُن' إلى 'هو'", "5. Existential Equations: From 'Be' to 'He'"), expanded=False):
        st.markdown(TXT(
            """
            الحروف ليست مجرد قيم ثابتة، بل هي مترابطة في سلسلة من المعادلات الوجودية التي تروي قصة الخلق من الأمر (كُن) إلى المعرفة (هو):
            
            **١. المعادلة الأولى للوجود:**
            ```
            ك + ن = ع
            20 + 50 = 70
            ```
            الأمر الإلهي (كُن) + النور الذاتي = الإدراك. الوجود لا يُدرك إلا بالنور.
            
            **٢. المعادلات الوجودية للجسور:**
            ```
            ع + ي = الاستجابة (الإدراك + النداء)
            70 + 10 = 80 (قيمة الفاء = بداية السببية)
            
            ي + هـ = الهوية (النداء + الحضور)
            10 + 5 = 15
            
            هـ → ك (الهوية تعود إلى المصدر: "كلٌ إلينا راجعون")
            5 → 20
            ```
            
            **٣. الدائرة المغلقة:**
            من ك (كن) → إلى ن (النور) → إلى ع (الإدراك) → إلى ي (النداء) → إلى هـ (الهوية) → إلى ك (العودة إلى المصدر).
            
            هذه هي دورة الوجود من الأزل إلى الخلود، مختزلة في حروف وكلمات.
            """,
            """
            Letters are not just fixed values, but are interconnected in a series of existential equations that narrate the story of creation from the command (Be) to knowledge (He):
            
            **1. The First Equation of Existence:**
            K + N = A (Command + Light = Perception)
            
            **2. The Existential Equations of the Bridges:**
            A + Y = Response (Perception + Calling)
            Y + H = Identity (Calling + Presence)
            H → K (Identity returns to the Source)
            
            **3. The Closed Circle:**
            From K (Be) → to N (Light) → to A (Perception) → to Y (Calling) → to H (Identity) → back to K (Return to Source).
            
            This is the cycle of existence from eternity to eternity, condensed into letters and words.
            """
        ))

    # =============================================
    # ٦. دالة الميزان النهائية
    # =============================================
    with st.expander(TXT("٦. دالة الميزان النهائية (Python)", "6. The Final Mizan Function (Python)"), expanded=False):
        st.markdown(TXT(
            "بعد أن حددنا قيم كل حرف ودوره في المعادلة، نقدم الآن دالة الميزان النهائية التي تدمج كل هذه الحروف في معادلة واحدة لحساب الثبات (S).",
            "After defining the values and roles of each letter, we now present the final Mizan function that integrates all these letters into a single equation to calculate Stability (S)."
        ))
        st.code("""
import numpy as np

def calc_S(W, B, E,
          source_constants,      # ك، ن
          dual_constants,        # ق، ص
          manifestation_vars,    # أ، ل، م، ر، س، ح، ط
          connection_vars,       # ع، ي، هـ
          operator_vars,         # ف، و، ب، ل
          action_vars):          # ج، خ، د، ذ، ز، ش، ت، ث، ض، ظ، غ
    """
    المعادلة النهائية لنظرية الميزان – التصنيف الوجودي السداسي.
    S = [W × B] × [المصدر / المثبطات] × المشغلات
    """
    S = W * B
    
    # ١. ثوابت الذات الإلهية (ك، ن) – المصدر
    source_factor = (source_constants.get('ك', 0.5) * 20 + 
                     source_constants.get('ن', 0.5) * 50) / 2
    S *= (0.3 + 0.7 * source_factor / 100)
    
    # ٢. ثوابت الازدواج (ق، ص)
    dual_factor = (dual_constants.get('ق', 0.5) * 100 + 
                   dual_constants.get('ص', 0.5) * 90) / 2
    S *= (0.5 + 0.5 * dual_factor / 100)
    
    # ٣. حروف التجلي – ترفع W و B
    man_boost = sum(manifestation_vars.values()) / max(len(manifestation_vars), 1)
    S *= (0.4 + 0.6 * man_boost)
    
    # ٤. حروف الاشتراك (الجسور) – تضبط التوازن
    conn_balance = sum(connection_vars.values()) / max(len(connection_vars), 1)
    S *= (0.7 + 0.6 * conn_balance)
    
    # ٥. المشغلات – تحدد منطق التفاعل
    ف = operator_vars.get('ف', 0.5)
    و = operator_vars.get('و', 0.5)
    ب = operator_vars.get('ب', 0.5)
    ل_op = operator_vars.get('ل', 0.5)
    op_factor = (ف * 80 + و * 6 + ب * 2 + ل_op * 30) / 118
    S *= (0.7 + 0.6 * op_factor)
    
    # ٦. أعمال الخلق – إرادة حرة (±)
    pos_sum = sum(v for k, v in action_vars.items() if v > 0)
    neg_sum = sum(abs(v) for k, v in action_vars.items() if v < 0)
    S *= (1.0 + 0.2 * pos_sum / max(len(action_vars), 1))
    S *= (1.0 - 0.3 * neg_sum / max(len(action_vars), 1))
    
    # ٧. الاستدراج
    if E > S:
        S -= 0.1 * (E - S)
    
    return np.clip(S, 0.001, 1.0)
    """, language="python")

    # =============================================
    # ٧. الخاتمة: تواضع العارفين
    # =============================================
    with st.expander(TXT("٧. الخاتمة: تواضع العارفين", "7. Conclusion: The Humility of the Knowers"), expanded=False):
        st.markdown(TXT(
            """
            <div style="background:rgba(20,30,60,0.7); border-radius:15px; padding:25px; margin:15px 0; border:1px solid #FFD700; line-height:2.2; text-align:center;">
            <h3 style="color:#FFD700;">﴿وَمَا أُوتِيتُم مِّنَ الْعِلْمِ إِلَّا قَلِيلًا﴾ [الإسراء: ٨٥]</h3>
            
            <p>هذا ما انتهينا إليه. وهذا ما وفقنا الله إليه. وهو – بلا شك – ليس كل شيء، بل هو أقل القليل من بحر علم الله الذي لا قاع له.</p>
            
            <p>ما قدمناه هنا ليس "الحقيقة المطلقة"، بل هو محاولة متواضعة لفهم سنة من سنن الله في خلقه، ولفك شفرة من شفرات كتابه العزيز. إنه جهد بشري، يحتمل الصواب ويحتمل الخطأ.</p>
            
            <p>فما كان فيه من صواب، فمن الله وحده، وله الحمد والمنة. وما كان فيه من خطأ، فمن أنفسنا، ونسأل الله أن يغفره لنا. وحسبنا أنا حاولنا، وأننا فتحنا بابًا لعل غيرنا يكمل المسيرة، ويصحح المسار.</p>
            
            <p>والله أسأل أن ينفع بهذا العمل كاتبه وقارئه، وأن يجعله خالصًا لوجهه الكريم، وأن يكتب له القبول في الأرض والثواب في السماء.</p>
            
            <p style="font-size:1.2em; font-weight:bold;">S = W × B</p>
            <p style="font-size:0.8em; color:#AAA;">ق = ١٠٠ = الحق = الميزان</p>
            </div>
            """,
            """
            <div style="background:rgba(20,30,60,0.7); border-radius:15px; padding:25px; margin:15px 0; border:1px solid #FFD700; line-height:2.2; text-align:center;">
            <h3 style="color:#FFD700;">﴿And you have not been given of knowledge except a little.﴾ [Al-Isra: 85]</h3>
            
            <p>This is what we have reached. It is, without doubt, not everything, but the smallest of drops from the endless ocean of Allah's knowledge.</p>
            
            <p>What we have presented here is not "the absolute truth", but a humble attempt to understand one of Allah's laws in His creation, and to decode one of the codes of His Mighty Book. It is a human effort, liable to error.</p>
            
            <p>Whatever is correct in it is from Allah alone, and to Him belongs all praise. Whatever is wrong is from ourselves, and we ask Allah for His forgiveness. We have tried, and we have opened a door for others to continue the journey.</p>
            
            <p style="font-size:1.2em; font-weight:bold;">S = W × B</p>
            <p style="font-size:0.8em; color:#AAA;">Q = 100 = The Truth = The Balance</p>
            </div>
            """
        ))

def render_new_geometric_lexicon():
    render_geometric_lexicon()
