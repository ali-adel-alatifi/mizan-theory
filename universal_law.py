# mizan/universal_law.py
"""
القانون الكوني الشامل: التناظر بين الخلق والأمر
من الذرة إلى المجرة، من الفيزياء إلى الأخلاق
"""

import streamlit as st
import numpy as np
from config import TXT, LETTERS_DB

def render_universal_law():
    st.header(TXT("🌌 القانون الكوني الشامل", "🌌 The Universal Cosmic Law"))
    st.markdown(TXT(
        "### ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ [الرحمن: ٧]",
        "### And the heaven He raised and imposed the balance."
    ))
    
    # ─────────────────────────────────────────
    # ١. التناظر بين أركان الإسلام والقوى الفيزيائية الأربع
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("⚛️ أركان الإسلام والقوى الأربع", "⚛️ Pillars of Islam & the Four Forces"))
    
    cosmic_table = [
        [
            TXT("الصلاة", "Prayer"),
            TXT("النووية القوية", "Strong Nuclear"),
            TXT("التخليق (Synthesis)", "Synthesis"),
            TXT("التنفس الخلوي – إنتاج الطاقة", "Cellular Respiration – Energy Production"),
            TXT("W (الولاء)", "W (Loyalty)"),
            TXT("تجديد العهد 5 مرات يومياً", "Renewing the covenant 5 times daily")
        ],
        [
            TXT("الزكاة", "Zakat"),
            TXT("الكهرومغناطيسية", "Electromagnetism"),
            TXT("التوازن (Equilibrium)", "Equilibrium"),
            TXT("الدورة الدموية – توزيع المغذيات", "Blood Circulation – Distributing Nutrients"),
            TXT("B (البراءة)", "B (Disavowal)"),
            TXT("تطهير المال من الشح", "Purifying wealth from stinginess")
        ],
        [
            TXT("الصوم", "Fasting"),
            TXT("النووية الضعيفة", "Weak Nuclear"),
            TXT("التفكك (Decomposition)", "Decomposition"),
            TXT("الالتهام الذاتي – تنظيف الخلية", "Autophagy – Cleaning the Cell"),
            TXT("B (البراءة)", "B (Disavowal)"),
            TXT("كبح الشهوات", "Restraining desires")
        ],
        [
            TXT("الحج", "Hajj"),
            TXT("الجاذبية", "Gravity"),
            TXT("الترسيب (Precipitation)", "Precipitation"),
            TXT("الهجرة الخلوية – التجمع نحو المركز", "Chemotaxis – Moving toward the Center"),
            TXT("W (الولاء)", "W (Loyalty)"),
            TXT("الوفادة إلى الله", "Delegation to Allah")
        ],
    ]
    
    cols = st.columns([1, 1.2, 1.2, 1.2, 0.8, 1.2])
    headers = [
        TXT("الركن", "Pillar"),
        TXT("الفيزياء", "Physics"),
        TXT("الكيمياء", "Chemistry"),
        TXT("البيولوجيا", "Biology"),
        TXT("القطب", "Pole"),
        TXT("التأثير", "Effect")
    ]
    for col, h in zip(cols, headers):
        col.markdown(f"**{h}**")
    for row in cosmic_table:
        cols = st.columns([1, 1.2, 1.2, 1.2, 0.8, 1.2])
        for col, val in zip(cols, row):
            col.markdown(val)

    # ─────────────────────────────────────────
    # ٢. جدول الحروف الكامل مع دلالات التاء والأمثلة القرآنية
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🔤 جدول الحروف الكامل – التصنيف الجديد", "🔤 Complete Letter Classification"))
    
    letters_classification = [
        ("ك", 20, TXT("ثابت المصدر", "Source Constant"), TXT("الأمر (كن)", "The Command (Be)"), 1, "﴿كُن فَيَكُونُ﴾"),
        ("ن", 50, TXT("ثابت المصدر", "Source Constant"), TXT("النور", "The Light"), 1, "﴿ن ۚ وَالْقَلَمِ﴾"),
        ("ق", 100, TXT("ثابت مزدوج (وجهان)", "Dual Constant (Two Faces)"), TXT("الثابت: الحق / القيوم — المتجلي: القسط / العدل / الدِّينُ القَيِّم", "Fixed: Al-Haqq / Al-Qayyum — Manifest: Al-Qist / Justice / Ad-Deen Al-Qayyim"), 2, "﴿ق ۚ وَالْقُرْآنِ الْمَجِيدِ﴾"),
        ("ص", 90, TXT("ثابت مزدوج", "Dual Constant"), TXT("الصمد / الصبر والصدق", "Al-Samad / Patience and Truthfulness"), 4, "﴿ص ۚ وَالْقُرْآنِ ذِي الذِّكْرِ﴾"),
        ("أ", 1, TXT("تجلي إلهي", "Divine Manifestation"), TXT("الوحدانية", "Oneness"), 13, "﴿اللَّهُ أَحَدٌ﴾"),
        ("ل", 30, TXT("تجلي إلهي", "Divine Manifestation"), TXT("المُلك والعدل", "Kingship and Justice"), 13, "﴿الْمُلْكُ يَوْمَئِذٍ لِّلَّهِ﴾"),
        ("م", 40, TXT("تجلي إلهي", "Divine Manifestation"), TXT("الجمع", "The Gathering"), 17, "﴿مَالِكِ يَوْمِ الدِّينِ﴾"),
        ("ر", 200, TXT("تجلي إلهي", "Divine Manifestation"), TXT("الطاقة المشتركة", "Shared Energy"), 6, "﴿الرَّحْمَٰنُ عَلَّمَ الْقُرْآنَ﴾"),
        ("ح", 8, TXT("تجلي إلهي", "Divine Manifestation"), TXT("الكمال والدوام", "Perfection and Permanence"), 7, "﴿حَم ۚ تَنزِيلُ الْكِتَابِ﴾"),
        ("س", 60, TXT("تجلي إلهي", "Divine Manifestation"), TXT("السمع", "Hearing"), 5, "﴿سَمِيعٌ بَصِيرٌ﴾"),
        ("ط", 9, TXT("تجلي إلهي", "Divine Manifestation"), TXT("الطهارة", "Purity"), 4, "﴿طه ۚ مَا أَنزَلْنَا عَلَيْكَ الْقُرْآنَ لِتَشْقَىٰ﴾"),
        ("ع", 70, TXT("صفة مشتركة", "Shared Attribute"), TXT("العلم والإدراك", "Knowledge and Perception"), 2, "﴿عَلَّمَ الْإِنسَانَ مَا لَمْ يَعْلَمْ﴾"),
        ("ي", 10, TXT("صفة مشتركة", "Shared Attribute"), TXT("الاستجابة والدعاء", "Response and Supplication"), 2, "﴿وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ﴾"),
        ("هـ", 5, TXT("صفة مشتركة", "Shared Attribute"), TXT("الهوية والهدى", "Identity and Guidance"), 2, "﴿هُوَ اللَّهُ الْخَالِقُ الْبَارِئُ﴾"),
        ("ف", 80, TXT("مشغّل", "Operator"), TXT("السببية (=)", "Causality (=)"), "-", "﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ﴾"),
        ("و", 6, TXT("مشغّل", "Operator"), TXT("العطف (× أو +)", "Conjunction (× or +)"), "-", "﴿وَالَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ﴾"),
        ("ب", 2, TXT("مشغّل", "Operator"), TXT("الاستعانة (بـ)", "Assistance (by)"), "-", "﴿بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ﴾"),
        ("ل (المشغّل)", 30, TXT("مشغّل", "Operator"), TXT("التعليل (→)", "Purpose (→)"), "-", "﴿وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ﴾"),
        ("ج", 3, TXT("خلق", "Creation"), TXT("الجهاد / الجهل", "Striving / Ignorance"), "-", "﴿وَجَاهِدُوا فِي اللَّهِ حَقَّ جِهَادِهِ﴾"),
        ("خ", 600, TXT("خلق", "Creation"), TXT("الخير / الخيانة", "Good / Betrayal"), "-", "﴿وَتَعَاوَنُوا عَلَى الْبِرِّ وَالتَّقْوَىٰ﴾"),
        ("ش", 300, TXT("خلق", "Creation"), TXT("الشكر / الشهوة", "Gratitude / Lust"), "-", "﴿لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ﴾"),
        ("ض", 800, TXT("خلق", "Creation"), TXT("الضبط / الضلال", "Precision / Misguidance"), "-", "﴿وَمَا يَضِلُّ بِهِ إِلَّا الْفَاسِقِينَ﴾"),
        ("ظ", 900, TXT("خلق", "Creation"), TXT("الظفر / الظلم", "Victory / Injustice"), "-", "﴿وَلَا تَحْسَبَنَّ اللَّهَ غَافِلًا عَمَّا يَعْمَلُ الظَّالِمُونَ﴾"),
        ("غ", 1000, TXT("خلق", "Creation"), TXT("الغفران / الغل", "Forgiveness / Malice"), "-", "﴿وَاللَّهُ يَعِدُكُم مَّغْفِرَةً مِّنْهُ﴾"),
        ("ت", 400, TXT("خلق / مشغّل", "Creation / Operator"), TXT("الاتخاذ والتبعية", "Adoption and Following"), "-", TXT("انظر الشرح أدناه", "See explanation below")),
    ]
    
    st.dataframe(
        letters_classification,
        column_config={
            0: TXT("الحرف", "Letter"),
            1: TXT("القيمة", "Value"),
            2: TXT("التصنيف", "Category"),
            3: TXT("الدلالة", "Meaning"),
            4: TXT("ظهور", "Frequency"),
            5: TXT("مثال", "Example"),
        },
        hide_index=True, use_container_width=True
    )

    # ─────────────────────────────────────────
    # ٣. تفصيل دلالات تاء التأنيث والاتخاذ والتبعية
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🅃 تاء التأنيث والاتخاذ والتبعية – حرف القرار والمصير", "🅃 The Letter Taa – The Letter of Decision and Destiny"))
    
    st.markdown(TXT(
        """
        حرف **التاء (ت)** قيمته ٤٠٠، وهو من حروف الخلق والمشغلات في آنٍ واحد. 
        من أعظم دلالاته في القرآن الكريم: **الاتخاذ** و**التبعية**.
        
        الاتخاذ هو قرار القلب واختياره. وهو الذي يحدد موقعك على خريطة (W, B). 
        وتظهر التاء في هذا السياق في موضعين عظيمين:
        
        ### ١. تاء الاتخاذ الإيجابي (الولاء)
        
        حين يتخذك الله ولياً:
        > ﴿وَاتَّخَذَ اللَّهُ إِبْرَاهِيمَ خَلِيلًا﴾ [النساء: ١٢٥]
        هذه ذروة الاتخاذ الإيجابي. الله يتخذ عبداً خليلاً. هذا هو W = 1.
        
        حين تتخذ إبراهيم أسوة:
        > ﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ﴾ [الممتحنة: ٤]
        أنت تتخذ النموذج الصحيح، فتسير على الصراط.
        
        ### ٢. تاء الاتخاذ السلبي (الولاء للطاغوت)
        
        حين يتخذ الإنسان إلهه هواه:
        > ﴿أَفَرَأَيْتَ مَنِ اتَّخَذَ إِلَٰهَهُ هَوَاهُ﴾ [الجاثية: ٢٣]
        هذا هو W = 0 أو سالب. الولاء للهوى بدلاً من الله.
        
        حين يتخذون من دون الله أولياء:
        > ﴿وَالَّذِينَ اتَّخَذُوا مِن دُونِهِ أَوْلِيَاءَ﴾ [الزمر: ٣]
        هذا هو B = 0. البراءة منعدمة، والولاء موجه لغير الله.
        
        ### ٣. تاء التبعية (اتباع طريق)
        
        > ﴿وَاتَّبِعْ مِلَّةَ إِبْرَاهِيمَ حَنِيفًا﴾ [النحل: ١٢٣]
        اتباع ملة إبراهيم هو السير على الجيوديسي المستقيم (κ = 0).
        
        > ﴿قَالُوا بَلْ نَتَّبِعُ مَا وَجَدْنَا عَلَيْهِ آبَاءَنَا﴾ [البقرة: ١٧٠]
        هذه هي التبعية العمياء التي تبعدك عن الصراط.
        
        **الخلاصة:**
        التاء هو حرف القرار. قيمته ٤٠٠ تشير إلى ثقل الاختيار. 
        كل إنسان يقول: إما أن **أتخذ** الله ورسوله والمؤمنين أولياء، أو **أتخذ** الهوى والطاغوت. 
        وكل إنسان يقول: إما **أتبع** ملة إبراهيم، أو **أتبع** ما وجد عليه آباءه.
        وهذا هو جوهر معادلة الميزان.
        """,
        """
        The letter **Taa (ت)** with value 400 is both a creation letter and an operator. 
        Its greatest significance in the Quran is **ittikhaadh (taking/adopting)** and **ittibaa' (following)**.
        
        **Positive Taking (Loyalty):** Allah took Abraham as a friend (W=1). You take Abraham as a model.
        **Negative Taking (Disavowal failure):** Taking one's desire as a god, or taking allies besides Allah.
        **Following:** Either follow the path of Abraham (κ=0) or blindly follow ancestors.
        
        **Summary:** Taa is the letter of decision. Its value 400 indicates the weight of choice. Every person says: either I **take** Allah, His Messenger, and the believers as allies, or I **take** desire and Taghut. And every person says: either I **follow** the path of Abraham, or I **follow** what my fathers were upon. This is the essence of the Mizan equation.
        """
    ))

    # ─────────────────────────────────────────
    # ٤. المعادلة الموسعة
    # ─────────────────────────────────────────
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
    pos_boost = sum(creation_positive.values()) / max(len(creation_positive), 1)
    S *= (1 + 0.2 * pos_boost)
    neg_effect = sum(creation_negative.values()) / max(len(creation_negative), 1)
    S *= (1 - 0.3 * neg_effect)
    op_factor = operators.get('ف', 0.5) * operators.get('و', 0.5) * operators.get('ت', 0.5)
    S *= (0.8 + 0.4 * op_factor)
    if E > S:
        S -= operators.get('غ', 0.2) * (E - S) * 0.3
    return np.clip(S, 0.001, 1.0)
    """, language="python")

    # ─────────────────────────────────────────
    # ٥. الخلاصة القاطعة
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("💎 الخلاصة القاطعة", "💎 The Definitive Conclusion"))
    st.markdown(TXT(
        """
        هناك تطابق محكم كامل بين نظام الخلق (الكون) ونظام الأمر (القرآن) في قانون الولاية والبراءة الديناميكي:
        
        ١. **التطابق في المبدأ:** الجذب (الولاية) والتنافر (البراءة).
        ٢. **التطابق في الهيكل:** أنظمة هرمية متكاملة.
        ٣. **التطابق في الوظيفة:** أدوار تكاملية متخصصة.
        ٤. **التطابق في الغاية:** تحقيق التوازن والنظام.
        ٥. **التطابق في الديناميكية:** ثبات في الثوابت، مرونة في المتغيرات.
        
        الفرق الوحيد هو آلية التطبيق:
        - **الكون:** تطبيق قسري (قصري).
        - **الكائنات الدنيا:** تطبيق غريزي طبيعي.
        - **الحيوانات:** تطبيق مختلط (غريزي + مكتسب).
        - **الإنسان:** تطبيق فطري + اختياري + تكليفي.
        
        والتاء (ت = ٤٠٠) هو حرف القرار: إما أن تتخذ الله وأولياءه، وإما أن تتخذ الطاغوت. إما أن تتبع ملة إبراهيم، وإما أن تتبع الأهواء. وهذا هو جوهر S = W × B.
        
        ﴿اللَّهُ الَّذِي خَلَقَ سَبْعَ سَمَاوَاتٍ وَمِنَ الْأَرْضِ مِثْلَهُنَّ يَتَنَزَّلُ الْأَمْرُ بَيْنَهُنَّ لِتَعْلَمُوا أَنَّ اللَّهَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ وَأَنَّ اللَّهَ قَدْ أَحَاطَ بِكُلِّ شَيْءٍ عِلْمًا﴾ [الطلاق: ١٢]
        
        فالذي خلق السماوات السبع والأرضين السبع، هو الذي أنزل الأمر بينهن. الكون كتاب منظور، والقرآن كتاب مسطور.
        كلاهما يشهدان بوحدانية الخالق، وكمال حكمته، وشمول نظامه.
        
        **S = W × B** — هذا هو قانون الوجود كله، من الذرة إلى المجرة.
        """,
        """
        There is a complete, precise correspondence between the system of creation (the universe) 
        and the system of command (the Quran) in the dynamic law of loyalty and disavowal.
        
        The only difference is the mechanism of application:
        - **Universe:** Coercive application.
        - **Lower beings:** Natural instinctive application.
        - **Animals:** Mixed (instinctive + learned).
        - **Human:** Innate + voluntary + commissioned.
        
        And the letter Taa (ت = 400) is the letter of decision: either you take Allah and His allies, or you take Taghut. Either you follow the path of Abraham, or you follow desires. This is the essence of S = W × B.
        
        ﴿It is Allah who has created seven heavens and of the earth, the like of them. The command descends among them so you may know that Allah is over all things competent and that Allah has encompassed all things in knowledge.﴾ [At-Talaq: 12]
        
        He who created the seven heavens and the seven earths is the One who sent down the command between them. The universe is an observed book, and the Quran is a written book. Both testify to the oneness of the Creator, the perfection of His wisdom, and the comprehensiveness of His system.
        
        **S = W × B** — This is the law of all existence, from the atom to the galaxy.
        """
    ))
