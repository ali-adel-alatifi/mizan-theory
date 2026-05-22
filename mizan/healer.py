# mizan/healer.py
"""
طبيب القلوب – رحلة من السؤال إلى اليقين
من منظور الدين القيم (قانون السببية) والإسلام الحنيف (الاستجابة الديناميكية)
كل حركة وسكنة: مولد طاقة نحو الولاية أو البراءة
"""

import streamlit as st
from config import TXT

# =============================================
# ١. الأسئلة – محطات صدق مع قانون السببية
# =============================================
HEALER_QUESTIONS = [
    {
        "id": "mood",
        "text": TXT(
            "في أعماقك، بعيداً عن الأقنعة... كيف تصف حال قلبك الآن؟ ﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾",
            "Deep inside, beyond all masks... how do you describe your heart's state? ﴿Verily, in the remembrance of Allah do hearts find rest.﴾"
        ),
        "options": [
            TXT("مطمئن بذكر الله – قلبي في توازن", "At peace with Allah's remembrance – my heart is balanced"),
            TXT("متقلب بين اليقين والغفلة – أحياناً أسير على الصراط وأحياناً أنحرف", "Fluctuating between certainty and heedlessness"),
            TXT("فيه قلق وضيق لا أعرف سببه – ران يغشاه", "Anxiety and tightness – a covering over it"),
            TXT("قاسی کالحجارة أو أشد قسوة – لا يتأثر بآيات الله", "Hard as stone, or even harder – unmoved by Allah's signs")
        ]
    },
    {
        "id": "prayer",
        "text": TXT(
            "صلاتك... تلك الوقفة بين يدي الله. هي محطة الشحن اليومية لطاقة الولاء. كيف هي في ميزانك؟ ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾",
            "Your Salah... that standing before Allah. It is the daily charging station for loyalty energy. How is it in your scale? ﴿And seek help through patience and prayer.﴾"
        ),
        "options": [
            TXT("أقيمها بخشوع وأجد فيها راحتي وسكينتي – هي صلاتي حقاً", "I establish it with devotion and find rest – it is truly my connection"),
            TXT("أصليها في وقتها لكني مشغول القلب – الجسد حاضر والروح غائبة", "I pray on time but my heart is distracted – body present, soul absent"),
            TXT("أصليها متأخرة وأحياناً تفوتني – الطاقة تتسرب", "I delay it and sometimes miss it – energy is leaking"),
            TXT("ثقيلة عليّ... لا أجد لها طعماً – الصلاة مجرد حركات", "It's heavy on me... I find no taste – mere movements")
        ]
    },
    {
        "id": "sins",
        "text": TXT(
            "ما الذنب الذي إذا خلوت بنفسك... وجدته يعاودك ويُثقل روحك؟ هذه هي نقطة تسرب الطاقة. ﴿إِنَّ الْحَسَنَاتِ يُذْهِبْنَ السَّيِّئَاتِ﴾",
            "What sin, when you're alone with yourself, haunts you and burdens your soul? This is the point of energy leakage. ﴿Indeed, good deeds do away with misdeeds.﴾"
        ),
        "options": [
            TXT("شهوة تحاصرني ولا أقوى على تركها – براءتي (B) ضعيفة", "A lust that besieges me – my disavowal (B) is weak"),
            TXT("غضب يغلبني فأندم بعد فوات الأوان – طاقتي السلبية تتفلت", "Anger that overcomes me – my negative energy runs wild"),
            TXT("كبر أو عُجب أو حب للمديح – ولائي (W) ليس خالصاً لله", "Arrogance, vanity, or love of praise – my loyalty (W) is not pure"),
            TXT("تعلّق قلبي بالدنيا وزينتها – E يطغى على S", "My heart is attached to this world – E overwhelms S")
        ]
    },
    {
        "id": "company",
        "text": TXT(
            "من تصاحب؟ فالمرء على دين خليله. رفقتك في الطريق إما أن تشحنك أو تستنزفك. ﴿الْأَخِلَّاءُ يَوْمَئِذٍ بَعْضُهُمْ لِبَعْضٍ عَدُوٌّ إِلَّا الْمُتَّقِينَ﴾",
            "Who do you befriend? A person is on the religion of their friend. Your companions either charge or drain you. ﴿Friends on that Day will be enemies to one another, except the righteous.﴾"
        ),
        "options": [
            TXT("أصحاب يعينونني على ذكر الله وطاعته – رفقة تزيد ولائي", "Friends who help me remember Allah – companions who increase my loyalty"),
            TXT("أهلي وعائلتي... فيهم خير لكني أرغب في صحبة أصدق", "My family... they're good but I want truer company"),
            TXT("زملاء عمل أو دراسة، العلاقة سطحية – لا شحن ولا تفريغ", "Work or study colleagues, superficial – no charge, no drain"),
            TXT("وحيد... لا صاحب لي ولا رفيق – أعيش في عزلة روحية", "Alone... I have no friend – living in spiritual isolation")
        ]
    },
    {
        "id": "quran",
        "text": TXT(
            "وهذا القرآن... كلام ربك، حبل الله الممدود. كم هو نصيبك منه؟ ﴿وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ لِّلْمُؤْمِنِينَ﴾",
            "And this Quran... your Lord's words, Allah's extended rope. What is your share of it? ﴿And We send down of the Quran that which is healing and mercy for the believers.﴾"
        ),
        "options": [
            TXT("أتلو منه كل يوم ولو قليلاً بتدبر – القرآن يغذيني", "I recite daily, even a little, with reflection – the Quran nourishes me"),
            TXT("أقرؤه في رمضان وأحياناً في غيره – شحن موسمي", "I read it in Ramadan and occasionally – seasonal charging"),
            TXT("أسمعه فقط ولا أفتح المصحف – أتلقى دون أن أتفاعل", "I only listen, I don't open the Mushaf – receiving without engaging"),
            TXT("هجرته... يمر الشهر ولا أقرأ منه شيئاً – انقطع الحبل", "I abandoned it... months pass without reading – the rope is severed")
        ]
    },
]

# =============================================
# ٢. روشتات علاجية – من الكتاب والسنة إلى خطة عملية
# =============================================
HEALING_PRESCRIPTIONS = {
    TXT("شهوة تحاصرني – براءتي (B) ضعيفة", "A lust that besieges me – my disavowal (B) is weak"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في البراءة (B). الطاغوت الداخلي (الهوى) يستعبدك. "
            "الولاء (W) موجود، لكن البراءة (B) ضعيفة جداً، مما يجعل ثباتك (S) منخفضاً. "
            "أنت في الربع الثاني (W مرتفع، B منخفض): تحب الله لكنك لا تتبرأ من الباطل. "
            "﴿وَأَمَّا مَنْ خَافَ مَقَامَ رَبِّهِ وَنَهَى النَّفْسَ عَنِ الْهَوَىٰ * فَإِنَّ الْجَنَّةَ هِيَ الْمَأْوَىٰ﴾",
            "**Mizan Diagnosis:** Weakness in Disavowal (B). The inner Taghut (desire) enslaves you. "
            "Loyalty (W) exists, but Disavowal (B) is very weak, making your Stability (S) low. "
            "You are in the second quadrant (W high, B low): you love Allah but don't disavow falsehood."
        ),
        "verses": [
            "﴿وَلَا تَقْرَبُوا الزِّنَىٰ ۖ إِنَّهُ كَانَ فَاحِشَةً وَسَاءَ سَبِيلًا﴾ [الإسراء: ٣٢]",
            "﴿قُل لِّلْمُؤْمِنِينَ يَغُضُّوا مِنْ أَبْصَارِهِمْ وَيَحْفَظُوا فُرُوجَهُمْ﴾ [النور: ٣٠]",
            "﴿إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ﴾ [العنكبوت: ٤٥]",
        ],
        "hadith": TXT(
            "«حُفَّتِ الْجَنَّةُ بِالْمَكَارِهِ وَحُفَّتِ النَّارُ بِالشَّهَوَاتِ» [متفق عليه]",
            "«Paradise is surrounded by hardships, and Hell by desires.» [Agreed upon]"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع B):**\n\n"
            "١. **الصيام:** صم يومين هذا الأسبوع (الإثنين والخميس). الصيام هو تدريب على البراءة من الشهوات.\n"
            "٢. **الصلاة:** إذا هاجتك شهوة، قم وتوضأ وصلِّ ركعتين. ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾.\n"
            "٣. **الذكر:** قل كل صباح: 'اللهم إني أسألك حبك وحب من يحبك وحب عمل يقربني إلى حبك'.\n"
            "٤. **البراءة العملية:** احذف أي تطبيق أو حساب يثير شهوتك. هذه براءة عملية ترفع B فوراً.\n"
            "٥. **المعادلة:** كلما ارتفع B، ارتفع S تلقائياً. ابدأ اليوم.",
            "**Your plan to restore balance (raising B):**\n\n"
            "1. **Fasting:** Fast two days this week (Mon & Thu). Fasting trains disavowal of desires.\n"
            "2. **Prayer:** If desire strikes, make wudu and pray two rak'ahs.\n"
            "3. **Remembrance:** Say each morning: 'O Allah, I ask for Your love...'\n"
            "4. **Practical Disavowal:** Delete any app or account that stirs your desire.\n"
            "5. **The Equation:** As B rises, S automatically rises. Start today."
        ),
    },
    TXT("غضب يغلبني – طاقتي السلبية تتفلت", "Anger that overcomes me – my negative energy runs wild"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الولاء (W). الغضب نار تحرق الإيمان وتستنزف الطاقة الروحية. "
            "عندما يغضب الإنسان، ينقطع عن ذكر الله، فينخفض W فوراً، ويهبط S. "
            "﴿وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ ۗ وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ﴾",
            "**Mizan Diagnosis:** Weakness in Loyalty (W). Anger is a fire that burns faith and drains spiritual energy. "
            "When angry, one disconnects from Allah's remembrance, W drops immediately, and S plummets."
        ),
        "verses": [
            "﴿وَلَا تَسْتَوِي الْحَسَنَةُ وَلَا السَّيِّئَةُ ۚ ادْفَعْ بِالَّتِي هِيَ أَحْسَنُ﴾ [فصلت: ٣٤]",
            "﴿وَإِمَّا يَنزَغَنَّكَ مِنَ الشَّيْطَانِ نَزْغٌ فَاسْتَعِذْ بِاللَّهِ﴾ [الأعراف: ٢٠٠]",
        ],
        "hadith": TXT(
            "«لَيْسَ الشَّدِيدُ بِالصُّرَعَةِ، إِنَّمَا الشَّدِيدُ الَّذِي يَمْلِكُ نَفْسَهُ عِنْدَ الْغَضَبِ» [متفق عليه]",
            "«The strong is not the one who overcomes people, but the one who controls himself when angry.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع W):**\n\n"
            "١. **تغيير الوضع:** إذا غضبت وأنت قائم فاجلس، وإن كنت جالساً فاضطجع.\n"
            "٢. **الاستعاذة:** قل: 'أعوذ بالله من الشيطان الرجيم'.\n"
            "٣. **الوضوء:** توضأ فوراً، فإن الغضب من الشيطان، والماء يطفئه.\n"
            "٤. **الصبر والصلاة:** ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾. صلِّ ركعتين.\n"
            "٥. **العفو قبل النوم:** سامح من أغضبك وادعُ له. هذا يرفع W ويقوي S.",
            "**Your plan to restore balance (raising W):**\n\n"
            "1. **Change position:** If angry while standing, sit; if sitting, lie down.\n"
            "2. **Seek refuge:** Say: 'I seek refuge in Allah from the accursed Satan'.\n"
            "3. **Ablution:** Make wudu immediately; anger is from Satan, water extinguishes it.\n"
            "4. **Patience and Prayer:** ﴿Seek help through patience and prayer.﴾ Pray two rak'ahs.\n"
            "5. **Forgive before sleep:** Forgive the one who angered you and pray for them."
        ),
    },
    TXT("كبر أو عُجب – ولائي (W) ليس خالصاً لله", "Arrogance – my loyalty (W) is not pure"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في البراءة (B) من الكبر والعجب. الكبر أول معصية عُصي الله بها. "
            "المتكبر يرى نفسه فوق القانون، فيرفض الخضوع (W) ويستكبر عن الحق (B). "
            "﴿إِلَّا إِبْلِيسَ أَبَىٰ وَاسْتَكْبَرَ وَكَانَ مِنَ الْكَافِرِينَ﴾",
            "**Mizan Diagnosis:** Weakness in Disavowal (B) from arrogance. Arrogance was the first sin. "
            "The arrogant sees himself above the law, refusing submission (W) and rejecting truth (B)."
        ),
        "verses": [
            "﴿وَلَا تَمْشِ فِي الْأَرْضِ مَرَحًا﴾ [الإسراء: ٣٧]",
            "﴿تِلْكَ الدَّارُ الْآخِرَةُ نَجْعَلُهَا لِلَّذِينَ لَا يُرِيدُونَ عُلُوًّا فِي الْأَرْضِ وَلَا فَسَادًا﴾ [القصص: ٨٣]",
        ],
        "hadith": TXT(
            "«لَا يَدْخُلُ الْجَنَّةَ مَنْ كَانَ فِي قَلْبِهِ مِثْقَالُ ذَرَّةٍ مِنْ كِبْرٍ» [مسلم]",
            "«Whoever has an atom's weight of arrogance in his heart will not enter Paradise.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع B):**\n\n"
            "١. **التواضع العملي:** انظر في المرآة وقل: 'اللهم كما حسنت خلقي فحسن خلقي'.\n"
            "٢. **خدمة الآخرين:** اخدم أهلك بنفسك هذا الأسبوع (نظف، اطبخ، ساعد).\n"
            "٣. **الثناء على الغير:** امدح ثلاثة أشخاص كل يوم بصدق.\n"
            "٤. **تذكر الأصل:** تذكر أنك من تراب وستعود إليه. ﴿مِنْهَا خَلَقْنَاكُمْ وَفِيهَا نُعِيدُكُمْ﴾.\n"
            "٥. **سجدة التواضع:** أطل السجود في صلاتك، فهو موضع الذل والخضوع لله.",
            "**Your plan to restore balance (raising B):**\n\n"
            "1. **Practical humility:** Look in the mirror and say: 'O Allah, as You beautified my form, beautify my character.'\n"
            "2. **Serve others:** Serve your family yourself this week.\n"
            "3. **Praise others:** Sincerely praise three people daily.\n"
            "4. **Remember origin:** You are from dust and to dust you shall return.\n"
            "5. **Prostration of humility:** Lengthen your prostration in prayer, the position of submission."
        ),
    },
    TXT("تعلّق قلبي بالدنيا – E يطغى على S", "My heart is attached to this world – E overwhelms S"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الولاء (W). حب الدنيا رأس كل خطيئة. "
            "عندما يطغى التمكين المادي (E) على الثبات الروحي (S)، يدخل الإنسان في حالة 'الاستدراج'. "
            "يظن أنه في نعمة، بينما هو في الحقيقة في انحدار. ﴿وَمَا الْحَيَاةُ الدُّنْيَا إِلَّا مَتَاعُ الْغُرُورِ﴾",
            "**Mizan Diagnosis:** Weakness in Loyalty (W). Love of this world is the root of all sin. "
            "When material empowerment (E) overwhelms spiritual stability (S), one enters 'Istidraj'. "
            "They think they are blessed, but are actually declining."
        ),
        "verses": [
            "﴿بَلْ تُؤْثِرُونَ الْحَيَاةَ الدُّنْيَا * وَالْآخِرَةُ خَيْرٌ وَأَبْقَىٰ﴾ [الأعلى: ١٦-١٧]",
            "﴿اعْلَمُوا أَنَّمَا الْحَيَاةُ الدُّنْيَا لَعِبٌ وَلَهْوٌ وَزِينَةٌ﴾ [الحديد: ٢٠]",
        ],
        "hadith": TXT(
            "«ازْهَدْ فِي الدُّنْيَا يُحِبَّكَ اللَّهُ، وَازْهَدْ فِيمَا فِي أَيْدِي النَّاسِ يُحِبُّوكَ» [ابن ماجه]",
            "«Renounce the world and Allah will love you; renounce what people possess and they will love you.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع W):**\n\n"
            "١. **الصدقة اليومية:** تصدق كل يوم بشيء تحبه (مال، طعام، وقت). هذا يحررك من عبودية المال.\n"
            "٢. **زيارة القبور:** زر المقبرة هذا الأسبوع. تذكر الموت يعيد ضبط بوصلة W.\n"
            "٣. **الدعاء:** قل كل ليلة: 'اللهم لا تجعل الدنيا أكبر همنا ولا مبلغ علمنا'.\n"
            "٤. **تدبر القرآن:** اقرأ سورة التكاثر كل يوم وتدبر معناها.\n"
            "٥. **تذكر:** ستموت وحدك، ولن ينفعك إلا عملك. S هو ما يبقى، E هو ما يفنى.",
            "**Your plan to restore balance (raising W):**\n\n"
            "1. **Daily charity:** Give charity daily from what you love. This frees you from money's slavery.\n"
            "2. **Visit graves:** Visit the graveyard this week. Remembering death resets the W compass.\n"
            "3. **Supplication:** Say each night: 'O Allah, do not make this world our greatest concern.'\n"
            "4. **Reflect on Quran:** Read Surat At-Takathur daily and reflect on its meaning.\n"
            "5. **Remember:** You will die alone, and only your deeds will benefit you. S remains, E perishes."
        ),
    },
}

# =============================================
# ٣. المحلل الشخصي الذكي – رحلة من السؤال إلى اليقين
# =============================================
def render_healer():
    """عرض طبيب القلوب التفاعلي."""
    
    # --- الغلاف الافتتاحي ---
    st.header("🩺 طبيب القلوب")
    st.markdown(TXT(
        """
        ### ﴿أَلَمْ يَأْنِ لِلَّذِينَ آمَنُوا أَن تَخْشَعَ قُلُوبُهُمْ لِذِكْرِ اللَّهِ﴾
        كل حركة وسكنة في حياتك هي مولد طاقة روحية، إما تدفعك نحو الولاء لله (W) فترتفع، 
        وإما تدفعك نحو الغفلة والمعصية (B) فتنخفض. ومعادلة الثبات (S = W × B) تحكم قلبك 
        كما تحكم الذرة والمجرة. هذه الأسئلة ليست استشارة باردة، بل هي لحظات صدق مع قانون السببية 
        الذي فطر الله عليه الكون. أجب كما أنت، لا كما تتمنى أن تكون.
        """,
        """
        ### ﴿Has the time not come for those who believe that their hearts should become humbly submissive at the remembrance of Allah?﴾
        Every movement and stillness in your life is a generator of spiritual energy, either pushing you toward loyalty to Allah (W) so it rises,
        or pushing you toward heedlessness and sin (B) so it falls. The stability equation (S = W × B) governs your heart
        as it governs the atom and the galaxy. These are not cold consultations, but moments of truth with the law of causality
        upon which Allah created the universe. Answer as you are, not as you wish to be.
        """
    ))

    # تهيئة الجلسة
    if "healer_answers" not in st.session_state:
        st.session_state.healer_answers = {}
    if "healer_done" not in st.session_state:
        st.session_state.healer_done = False

    # إذا لم يكتمل التشخيص
    if not st.session_state.healer_done:
        for q in HEALER_QUESTIONS:
            st.markdown("---")
            st.markdown(f"### {q['text']}")
            ans = st.radio(
                TXT("اختر إجابتك:", "Choose your answer:"),
                q["options"],
                key=q["id"],
                index=None
            )
            if ans:
                st.session_state.healer_answers[q["id"]] = ans

        if len(st.session_state.healer_answers) == len(HEALER_QUESTIONS):
            st.markdown("---")
            if st.button(TXT("🔍 شخّص حالي... أريد أن أعرف موقعي في الميزان", "🔍 Diagnose me... I want to know my position in the Mizan"), type="primary"):
                st.session_state.healer_done = True
                st.rerun()

    # بعد اكتمال التشخيص
    else:
        # تحديد المشكلة الرئيسية من إجابة السؤال الثالث (الذنب)
        main_issue = st.session_state.healer_answers.get("sins", TXT("شهوة تحاصرني – براءتي (B) ضعيفة", "A lust that besieges me"))
        # نبحث عن الكلمة المفتاحية في إجابته
        issue_key = None
        for key in HEALING_PRESCRIPTIONS:
            if key in main_issue:
                issue_key = key
                break
        if not issue_key:
            issue_key = TXT("شهوة تحاصرني – براءتي (B) ضعيفة", "A lust that besieges me")

        pres = HEALING_PRESCRIPTIONS[issue_key]

        # --- عرض التشخيص (النور) ---
        st.markdown("---")
        st.subheader(TXT("📋 التشخيص بالميزان", "📋 Mizan Diagnosis"))
        st.warning(pres["diagnosis"])

        # --- محاكاة حساب الموقع (W, B) ---
        mood_map = {
            TXT("مطمئن بذكر الله – قلبي في توازن", "At peace with Allah's remembrance"): 0.9,
            TXT("متقلب بين اليقين والغفلة", "Fluctuating between certainty and heedlessness"): 0.4,
            TXT("فيه قلق وضيق لا أعرف سببه", "Anxiety and tightness"): 0.1,
            TXT("قاسی کالحجارة أو أشد قسوة", "Hard as stone"): -0.6
        }
        prayer_map = {
            TXT("أقيمها بخشوع وأجد فيها راحتي", "I establish it with devotion"): 1.0,
            TXT("أصليها في وقتها لكني مشغول القلب", "I pray on time but my heart is distracted"): 0.4,
            TXT("أصليها متأخرة وأحياناً تفوتني", "I delay it and sometimes miss it"): -0.2,
            TXT("ثقيلة عليّ... لا أجد لها طعماً", "It's heavy on me"): -0.7
        }
        company_map = {
            TXT("أصحاب يعينونني على ذكر الله وطاعته", "Friends who help me remember Allah"): 0.8,
            TXT("أهلي وعائلتي...", "My family..."): 0.3,
            TXT("زملاء عمل أو دراسة", "Work or study colleagues"): 0.0,
            TXT("وحيد... لا صاحب لي ولا رفيق", "Alone..."): -0.4
        }
        quran_map = {
            TXT("أتلو منه كل يوم ولو قليلاً بتدبر", "I recite daily"): 1.0,
            TXT("أقرؤه في رمضان وأحياناً في غيره", "I read it in Ramadan"): 0.3,
            TXT("أسمعه فقط ولا أفتح المصحف", "I only listen"): -0.1,
            TXT("هجرته... يمر الشهر ولا أقرأ منه شيئاً", "I abandoned it"): -0.6
        }

        w_raw = (
            mood_map.get(st.session_state.healer_answers.get("mood", ""), 0.1) +
            prayer_map.get(st.session_state.healer_answers.get("prayer", ""), 0.1) +
            company_map.get(st.session_state.healer_answers.get("company", ""), 0.1) +
            quran_map.get(st.session_state.healer_answers.get("quran", ""), 0.1)
        ) / 4
        w_raw = max(-1.0, min(1.0, w_raw * 2 - 1))

        # B يُقدر بناءً على نوع الذنب
        if "شهوة" in main_issue or "lust" in main_issue.lower():
            b_raw = 0.2
        elif "غضب" in main_issue or "anger" in main_issue.lower():
            b_raw = 0.3
        elif "كبر" in main_issue or "arrogance" in main_issue.lower():
            b_raw = 0.1
        elif "دنيا" in main_issue or "world" in main_issue.lower():
            b_raw = 0.4
        else:
            b_raw = 0.5

        S_score = ((w_raw + 1) / 2) * ((b_raw + 1) / 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("W (الولاء)", f"{w_raw:+.2f}")
        col2.metric("B (البراءة)", f"{b_raw:+.2f}")
        col3.metric("S (الثبات)", f"{S_score:.2f}")

        # --- تفسير المعادلة للمستخدم ---
        st.markdown("---")
        st.subheader(TXT("🧮 معادلتك الآن", "🧮 Your Equation Now"))
        st.markdown(TXT(
            f"""
            **S = W × B**
            **{S_score:.2f} = {w_raw:+.2f} × {b_raw:+.2f}**
            
            كل حركة وسكنة في حياتك تولد طاقة. صلاتك، ذكرك، صدقتك، صحبتك... كلها ترفع W أو B.
            وكل غفلة، شهوة، كبر، حب دنيا... كلها تخفض W أو B. وحاصل ضربهما هو ثباتك.
            
            ﴿قُلْ إِنَّ صَلَاتِي وَنُسُكِي وَمَحْيَايَ وَمَمَاتِي لِلَّهِ رَبِّ الْعَالَمِينَ * لَا شَرِيكَ لَهُ﴾
            """,
            f"""
            **S = W × B**
            **{S_score:.2f} = {w_raw:+.2f} × {b_raw:+.2f}**
            
            Every movement and stillness in your life generates energy. Your prayer, remembrance, charity, company... all raise W or B.
            And every heedlessness, lust, arrogance, love of world... all lower W or B. Their product is your stability.
            
            ﴿Say, indeed my prayer, my rites of sacrifice, my living and my dying are for Allah, Lord of the worlds. No partner has He.﴾
            """
        ))

        # --- الروشتة العلاجية ---
        st.markdown("---")
        st.subheader(TXT("💊 الروشتة العلاجية", "💊 The Prescription"))
        st.markdown(TXT("#### 📖 آيات تتدبرها:", "#### 📖 Verses to reflect on:"))
        for v in pres["verses"]:
            st.info(v)
        st.markdown(TXT(f"#### 🕋 حديث شريف:\n{pres['hadith']}", f"#### 🕋 Hadith:\n{pres['hadith']}"))
        st.markdown(TXT(f"#### 🏃 خطة عملية:\n{pres['action']}", f"#### 🏃 Action Plan:\n{pres['action']}"))

        # --- رسالة أمل ---
        st.markdown("---")
        st.markdown(TXT(
            """
            ### 🌅 تذكر...
            ﴿قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ ۚ إِنَّ اللَّهَ يَغْفِرُ الذُّنُوبَ جَمِيعًا﴾
            
            قانون السببية دقيق، لكن رحمة الله أوسع. كل لحظة هي فرصة لتغيير المعادلة. 
            كل توبة ترفع B، وكل ذكر يرفع W. وحاصل ضربهما (S) هو ثباتك الذي تعيش به في الدنيا، 
            وتلقى الله به في الآخرة.
            
            أنت الآن في أول الطريق. ليس مطلوباً أن تصل إلى القمة دفعة واحدة، 
            ولكن أن تخطو الخطوة الأولى. كل يوم، جاهد نفسك قليلاً، وسترى كيف تتبدل الظلمات نوراً.
            """,
            """
            ### 🌅 Remember...
            ﴿Say, O My servants who have transgressed against themselves, do not despair of the mercy of Allah.﴾
            
            The law of causality is precise, but Allah's mercy is wider. Every moment is a chance to change the equation.
            Every repentance raises B, and every remembrance raises W. Their product (S) is your stability in this world,
            and the state in which you will meet Allah in the Hereafter.
            
            You are now at the beginning of the path. Strive a little each day, and you will see how darkness turns to light.
            """
        ))

        # زر إعادة
        if st.button(TXT("🔄 أريد أن أبدأ من جديد", "🔄 I want to start over")):
            st.session_state.healer_answers = {}
            st.session_state.healer_done = False
            st.rerun()
