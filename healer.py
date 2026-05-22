# mizan/healer.py
"""
طبيب القلوب – رحلة من السؤال إلى اليقين
من منظور: الدين القيم (قانون السببية الكوني) والإسلام الحنيف (الاستجابة الديناميكية)
"""

import streamlit as st
from config import TXT

# =============================================
# ١. الأسئلة – لحظات صدق مع النفس
# كل سؤال هنا يعكس جانباً من "الإسلام الحنيف" كاستجابة للقانون
# =============================================
HEALER_QUESTIONS = [
    {
        "id": "mood",
        "text": TXT(
            "في أعماقك، بعيداً عن الأقنعة... كيف تصف حال قلبك الآن؟ هذا هو مؤشر 'S' (الثبات) الأولي.",
            "Deep inside, beyond all masks... how do you describe your heart's state? This is your initial 'S' (stability) indicator."
        ),
        "options": [
            TXT("مطمئن بذكر الله – S مرتفع", "At peace with Allah's remembrance – High S"),
            TXT("متقلب بين اليقين والغفلة", "Fluctuating between certainty and heedlessness"),
            TXT("فيه قلق وضيق لا أعرف سببه", "Anxiety and tightness I can't explain"),
            TXT("قاسی کالحجارة أو أشد قسوة – S منخفض جداً", "Hard as stone, or even harder – Very low S")
        ]
    },
    {
        "id": "prayer",
        "text": TXT(
            "صلاتك... تلك الوقفة بين يدي الله، أعظم محطة شحن روحي. أين أنت منها؟",
            "Your Salah... that standing before Allah, the greatest spiritual charging station. Where are you with it?"
        ),
        "options": [
            TXT("أقيمها بخشوع وأجد فيها راحتي – W مرتفع", "I establish it with devotion and find my rest – High W"),
            TXT("أصليها في وقتها لكني مشغول القلب", "I pray on time but my heart is distracted"),
            TXT("أصليها متأخرة وأحياناً تفوتني", "I delay it and sometimes miss it"),
            TXT("ثقيلة عليّ... لا أجد لها طعماً – W منخفض", "It's heavy on me... I find no taste – Low W")
        ]
    },
    {
        "id": "sins",
        "text": TXT(
            "ما الذنب الذي إذا خلوت بنفسك... وجدته يعاودك ويُثقل روحك؟ هذا هو 'الطاغوت الداخلي' الذي يضعف B (البراءة).",
            "What sin, when you're alone with yourself, haunts you and burdens your soul? This is the 'inner Taghut' weakening your B (disavowal)."
        ),
        "options": [
            TXT("شهوة تحاصرني ولا أقوى على تركها", "A lust that besieges me and I can't leave it"),
            TXT("غضب يغلبني فأندم بعد فوات الأوان", "Anger that overcomes me, then I regret too late"),
            TXT("كبر أو عُجب أو حب للمديح", "Arrogance, vanity, or love of praise"),
            TXT("تعلّق قلبي بالدنيا وزينتها", "My heart is attached to this world and its glitter")
        ]
    },
    {
        "id": "company",
        "text": TXT(
            "من تصاحب؟ فالمرء على دين خليله. الرفقة إما أن ترفع W أو تخفضه. من هم رفقتك؟",
            "Who do you befriend? A person is on the religion of their friend. Company either raises W or lowers it. Who are your companions?"
        ),
        "options": [
            TXT("أصحاب يعينونني على ذكر الله وطاعته", "Friends who help me remember Allah"),
            TXT("أهلي وعائلتي... فيهم خير لكني أرغب في صحبة أصدق", "My family... they're good but I want truer company"),
            TXT("زملاء عمل أو دراسة، العلاقة سطحية", "Work or study colleagues, superficial"),
            TXT("وحيد... لا صاحب لي ولا رفيق", "Alone... I have no friend or companion")
        ]
    },
    {
        "id": "quran",
        "text": TXT(
            "وهذا القرآن... كلام ربك، دليل التشغيل. كم هو نصيبك منه؟",
            "And this Quran... the words of your Lord, the operating manual. What is your share of it?"
        ),
        "options": [
            TXT("أتلو منه كل يوم ولو قليلاً بتدبر", "I recite daily, even a little, with reflection"),
            TXT("أقرؤه في رمضان وأحياناً في غيره", "I read it in Ramadan and occasionally outside"),
            TXT("أسمعه فقط ولا أفتح المصحف", "I only listen, I don't open the Mushaf"),
            TXT("هجرته... يمر الشهر ولا أقرأ منه شيئاً", "I abandoned it... months pass without reading")
        ]
    },
]

# =============================================
# ٢. روشتات – من الكتاب والسنة إلى خطة عملية
# كل روشتة تربط الداء بـ "الدين القيم" وتقدم العلاج عبر "الإسلام الحنيف"
# =============================================
HEALING_PRESCRIPTIONS = {
    TXT("شهوة تحاصرني", "A lust that besieges me"): {
        "diagnosis": TXT(
            "ضعف في البراءة (B). الطاغوت الداخلي (الهوى) يستعبدك. قانون السببية يقول: من والى شهوته فقد أخل بالميزان. "
            "﴿وَأَمَّا مَنْ خَافَ مَقَامَ رَبِّهِ وَنَهَى النَّفْسَ عَنِ الْهَوَىٰ * فَإِنَّ الْجَنَّةَ هِيَ الْمَأْوَىٰ﴾ [النازعات: ٤٠-٤١]",
            "Weakness in Disavowal (B). The inner Taghut (desire) enslaves you. The law of causality says: whoever allies with desire has disrupted the balance. "
            "﴿But as for he who feared the position of his Lord and prevented the soul from [unlawful] inclination, then indeed, Paradise will be [his] refuge.﴾"
        ),
        "verses": [
            "﴿وَلَا تَقْرَبُوا الزِّنَىٰ ۖ إِنَّهُ كَانَ فَاحِشَةً وَسَاءَ سَبِيلًا﴾ [الإسراء: ٣٢]",
            "﴿قُل لِّلْمُؤْمِنِينَ يَغُضُّوا مِنْ أَبْصَارِهِمْ وَيَحْفَظُوا فُرُوجَهُمْ﴾ [النور: ٣٠]",
            "﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾ [البقرة: ٤٥] — استعن بهما على كسر طاغوت الشهوة.",
        ],
        "hadith": TXT(
            "«حُفَّتِ الْجَنَّةُ بِالْمَكَارِهِ وَحُفَّتِ النَّارُ بِالشَّهَوَاتِ» [متفق عليه]\n"
            "«يَا مَعْشَرَ الشَّبَابِ، مَنِ اسْتَطَاعَ مِنْكُمُ الْبَاءَةَ فَلْيَتَزَوَّجْ، فَإِنَّهُ أَغَضُّ لِلْبَصَرِ وَأَحْصَنُ لِلْفَرْجِ، وَمَنْ لَمْ يَسْتَطِعْ فَعَلَيْهِ بِالصَّوْمِ فَإِنَّهُ لَهُ وِجَاءٌ» [متفق عليه]",
            "«Paradise is surrounded by hardships, and Hell by desires.»\n"
            "«O young men, whoever among you can afford marriage, let him marry, for it is more effective in lowering the gaze and guarding chastity. And whoever cannot, let him fast, for it is a shield for him.»"
        ),
        "action": TXT(
            "**خطتك هذا الأسبوع (طاقة روحية = B + W):**\n"
            "١. صم يومين (الإثنين والخميس) – الصوم يزيد B (البراءة من الشهوة).\n"
            "٢. إذا هاجتك شهوة، قم وتوضأ وصلِّ ركعتين – الصلاة ترفع W (الولاء).\n"
            "٣. قل كل صباح: 'اللهم إني أسألك حبك وحب من يحبك وحب عمل يقربني إلى حبك'.\n"
            "٤. احذف أي تطبيق أو حساب يثير شهوتك. هذه براءة عملية.",
            "**Your plan this week (Spiritual Energy = B + W):**\n"
            "1. Fast two days (Mon & Thu) – fasting increases B (disavowal of lust).\n"
            "2. If desire strikes, make wudu and pray two rak'ahs – prayer raises W (loyalty).\n"
            "3. Say each morning: 'O Allah, I ask for Your love...'\n"
            "4. Delete any app or account that stirs your desire. This is practical disavowal."
        ),
    },
    TXT("غضب يغلبني", "Anger that overcomes me"): {
        "diagnosis": TXT(
            "ضعف في الولاء (W). الغضب نار تحرق الإيمان وتخل بالميزان. "
            "﴿وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ ۗ وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ﴾ [آل عمران: ١٣٤]",
            "Weakness in Loyalty (W). Anger is a fire that burns faith and disrupts the balance. "
            "﴿Who restrain anger and pardon people – and Allah loves the doers of good.﴾"
        ),
        "verses": [
            "﴿وَلَا تَسْتَوِي الْحَسَنَةُ وَلَا السَّيِّئَةُ ۚ ادْفَعْ بِالَّتِي هِيَ أَحْسَنُ﴾ [فصلت: ٣٤]",
            "﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾ [البقرة: ٤٥] — استعن بهما على كظم الغيظ.",
        ],
        "hadith": TXT(
            "«لَيْسَ الشَّدِيدُ بِالصُّرَعَةِ، إِنَّمَا الشَّدِيدُ الَّذِي يَمْلِكُ نَفْسَهُ عِنْدَ الْغَضَبِ» [متفق عليه]\n"
            "«إِذَا غَضِبَ أَحَدُكُمْ وَهُوَ قَائِمٌ فَلْيَجْلِسْ، فَإِنْ ذَهَبَ عَنْهُ الْغَضَبُ وَإِلَّا فَلْيَضْطَجِعْ» [أبو داود]",
            "«The strong is not the one who overcomes people, but the one who controls himself when angry.»\n"
            "«If one of you becomes angry while standing, let him sit. If it leaves him, [good]; otherwise, let him lie down.»"
        ),
        "action": TXT(
            "**خطتك:**\n"
            "١. إذا غضبت وأنت قائم فاجلس، وإن كنت جالساً فاضطجع – تحويل الطاقة الحركية.\n"
            "٢. قل: 'أعوذ بالله من الشيطان الرجيم' – قطع ولاية الشيطان.\n"
            "٣. توضأ فوراً – الماء يطفئ نار الغضب كما يطفئ نار الدنيا.\n"
            "٤. قبل أن تنام، سامح من أغضبك وادعُ له – هذا يرفع W ويقوي S.",
            "**Your plan:**\n"
            "1. If angry while standing, sit; if sitting, lie down – redirecting kinetic energy.\n"
            "2. Say: 'A'udhu billahi min ash-shaytan ir-rajim' – cutting the alliance of Satan.\n"
            "3. Make wudu immediately – water extinguishes the fire of anger.\n"
            "4. Before sleeping, forgive the one who angered you and pray for them – this raises W and strengthens S."
        ),
    },
    TXT("كبر أو عُجب", "Arrogance or vanity"): {
        "diagnosis": TXT(
            "ضعف في البراءة (B). الكبر أول معصية عُصي الله بها، وهو يناقض 'الإسلام' (الاستسلام لله). "
            "﴿إِلَّا إِبْلِيسَ أَبَىٰ وَاسْتَكْبَرَ وَكَانَ مِنَ الْكَافِرِينَ﴾ [البقرة: ٣٤]",
            "Weakness in Disavowal (B). Arrogance was the first sin against Allah, contradicting 'Islam' (submission to Allah). "
            "﴿Except Iblis; he refused and was arrogant and became of the disbelievers.﴾"
        ),
        "verses": [
            "﴿وَلَا تَمْشِ فِي الْأَرْضِ مَرَحًا إِنَّكَ لَن تَخْرِقَ الْأَرْضَ وَلَن تَبْلُغَ الْجِبَالَ طُولًا﴾ [الإسراء: ٣٧]",
        ],
        "hadith": TXT(
            "«لَا يَدْخُلُ الْجَنَّةَ مَنْ كَانَ فِي قَلْبِهِ مِثْقَالُ ذَرَّةٍ مِنْ كِبْرٍ» [مسلم]\n"
            "قَالَ رَجُلٌ: يَا رَسُولَ اللَّهِ، إِنَّ الرَّجُلَ يُحِبُّ أَنْ يَكُونَ ثَوْبُهُ حَسَنًا وَنَعْلُهُ حَسَنَةً. قَالَ: «إِنَّ اللَّهَ جَمِيلٌ يُحِبُّ الْجَمَالَ، الْكِبْرُ بَطَرُ الْحَقِّ وَغَمْطُ النَّاسِ» [مسلم]",
            "«Whoever has an atom's weight of arrogance in his heart will not enter Paradise.»\n"
            "A man said: 'O Messenger of Allah, a man likes his clothes to be nice and his shoes to be nice.' He said: 'Allah is Beautiful and loves beauty. Arrogance is rejecting truth and looking down on people.'"
        ),
        "action": TXT(
            "**خطتك:**\n"
            "١. انظر في المرآة وقل: 'اللهم كما حسنت خلقي فحسن خلقي' – تذكير بالنعمة.\n"
            "٢. اخدم أهلك بنفسك هذا الأسبوع (نظف، اطبخ، ساعد) – تواضع عملي.\n"
            "٣. امدح ثلاثة أشخاص كل يوم بصدق – كسر للكبر.\n"
            "٤. تذكر أنك من تراب وستعود إليه – أصل التواضع.",
            "**Your plan:**\n"
            "1. Look in the mirror and say: 'O Allah, as You beautified my form, beautify my character.'\n"
            "2. Serve your family yourself this week – practical humility.\n"
            "3. Sincerely praise three people daily – breaking arrogance.\n"
            "4. Remember you are from dust and to dust you shall return – the root of humility."
        ),
    },
    TXT("تعلّق قلبي بالدنيا", "My heart is attached to this world"): {
        "diagnosis": TXT(
            "ضعف في الولاء (W). حب الدنيا رأس كل خطيئة، وهو يخل بالميزان لأن E (التمكين المادي) يطغى على S (الثبات). "
            "﴿وَمَا الْحَيَاةُ الدُّنْيَا إِلَّا مَتَاعُ الْغُرُورِ﴾ [آل عمران: ١٨٥]",
            "Weakness in Loyalty (W). Love of this world is the root of all sin, disrupting the balance because E (material gain) overpowers S (stability). "
            "﴿And what is the worldly life except the enjoyment of delusion.﴾"
        ),
        "verses": [
            "﴿بَلْ تُؤْثِرُونَ الْحَيَاةَ الدُّنْيَا * وَالْآخِرَةُ خَيْرٌ وَأَبْقَىٰ﴾ [الأعلى: ١٦-١٧]",
        ],
        "hadith": TXT(
            "«ازْهَدْ فِي الدُّنْيَا يُحِبَّكَ اللَّهُ، وَازْهَدْ فِيمَا فِي أَيْدِي النَّاسِ يُحِبُّوكَ» [ابن ماجه]\n"
            "«لَوْ كَانَتِ الدُّنْيَا تَعْدِلُ عِنْدَ اللَّهِ جَنَاحَ بَعُوضَةٍ مَا سَقَى كَافِرًا مِنْهَا شَرْبَةَ مَاءٍ» [الترمذي]",
            "«Renounce the world and Allah will love you; renounce what people possess and they will love you.»\n"
            "«If this world were worth a mosquito's wing to Allah, He would not give a disbeliever a drink of water from it.»"
        ),
        "action": TXT(
            "**خطتك:**\n"
            "١. تصدق كل يوم بشيء تحبه (مال، طعام، وقت) – ترجمة B إلى عمل.\n"
            "٢. زر المقبرة هذا الأسبوع – تذكير بالآخرة.\n"
            "٣. قل كل ليلة: 'اللهم لا تجعل الدنيا أكبر همنا ولا مبلغ علمنا'.\n"
            "٤. تذكر أنك ستموت وحدك، ولن ينفعك إلا عملك – هذه هي المعادلة S = W × B.",
            "**Your plan:**\n"
            "1. Give charity daily from what you love – translating B into action.\n"
            "2. Visit the graveyard this week – a reminder of the Hereafter.\n"
            "3. Say each night: 'O Allah, do not make this world our greatest concern.'\n"
            "4. Remember you will die alone, and only your deeds will benefit you – this is the equation S = W × B."
        ),
    },
}

# =============================================
# ٣. المحلل الشخصي الذكي – رحلة من السؤال إلى اليقين
# =============================================
def render_healer():
    """عرض طبيب القلوب التفاعلي."""
    
    # --- الغلاف الافتتاحي ---
    st.header(TXT("🩺 طبيب القلوب", "🩺 Heart Healer"))
    st.markdown(TXT(
        """
        ### ﴿أَلَمْ يَأْنِ لِلَّذِينَ آمَنُوا أَن تَخْشَعَ قُلُوبُهُمْ لِذِكْرِ اللَّهِ﴾ [الحديد: ١٦]
        
        هذه ليست استشارة باردة. هذا وقفة مع النفس، في ضوء **الدين القيم** (قانون السببية الكوني) 
        و**الإسلام الحنيف** (الاستجابة الديناميكية لهذا القانون). 
        
        كل سؤال هنا يكشف جانباً من معادلة **S = W × B** في حياتك. 
        أجب عن هذه الأسئلة كما أنت، لا كما تتمنى أن تكون. 
        فالصدق مع النفس هو أول خطوة على طريق **الولاية لله والبراءة من الطاغوت**.
        """,
        """
        ### ﴿Has the time not come for those who believe that their hearts should become humbly submissive at the remembrance of Allah?﴾ [Al-Hadid: 16]
        
        This is not a cold consultation. This is a pause with yourself, in light of **Al-Deen Al-Qayyim** (the cosmic law of causality) 
        and **Al-Islam Al-Hanif** (the dynamic response to this law). 
        
        Each question reveals an aspect of the **S = W × B** equation in your life. 
        Answer as you are, not as you wish to be. 
        Honesty with oneself is the first step on the path of **loyalty to Allah and disavowal of Taghut**.
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
            if st.button(TXT("🔍 شخّص حالي... أريد أن أعرف", "🔍 Diagnose me... I want to know"), type="primary"):
                st.session_state.healer_done = True
                st.rerun()

    # بعد اكتمال التشخيص
    else:
        # تحديد المشكلة الرئيسية من إجابة السؤال الثالث (الذنب)
        main_issue = st.session_state.healer_answers.get("sins", TXT("شهوة تحاصرني", "A lust that besieges me"))
        # البحث عن الكلمة المفتاحية في إجابته
        issue_key = None
        for key in HEALING_PRESCRIPTIONS:
            if key in main_issue:
                issue_key = key
                break
        if not issue_key:
            issue_key = TXT("شهوة تحاصرني", "A lust that besieges me")

        pres = HEALING_PRESCRIPTIONS[issue_key]

        # --- عرض التشخيص (النور) ---
        st.markdown("---")
        st.subheader(TXT("📋 التشخيص", "📋 Diagnosis"))
        st.warning(pres["diagnosis"])

        # --- محاكاة حساب الموقع (W, B) ---
        mood_map = {
            TXT("مطمئن بذكر الله – S مرتفع", "At peace with Allah's remembrance – High S"): 0.9,
            TXT("متقلب بين اليقين والغفلة", "Fluctuating between certainty and heedlessness"): 0.4,
            TXT("فيه قلق وضيق لا أعرف سببه", "Anxiety and tightness I can't explain"): 0.1,
            TXT("قاسی کالحجارة أو أشد قسوة – S منخفض جداً", "Hard as stone, or even harder – Very low S"): -0.6
        }
        prayer_map = {
            TXT("أقيمها بخشوع وأجد فيها راحتي – W مرتفع", "I establish it with devotion and find my rest – High W"): 1.0,
            TXT("أصليها في وقتها لكني مشغول القلب", "I pray on time but my heart is distracted"): 0.4,
            TXT("أصليها متأخرة وأحياناً تفوتني", "I delay it and sometimes miss it"): -0.2,
            TXT("ثقيلة عليّ... لا أجد لها طعماً – W منخفض", "It's heavy on me... I find no taste – Low W"): -0.7
        }
        company_map = {
            TXT("أصحاب يعينونني على ذكر الله وطاعته", "Friends who help me remember Allah"): 0.8,
            TXT("أهلي وعائلتي... فيهم خير لكني أرغب في صحبة أصدق", "My family... they're good but I want truer company"): 0.3,
            TXT("زملاء عمل أو دراسة، العلاقة سطحية", "Work or study colleagues, superficial"): 0.0,
            TXT("وحيد... لا صاحب لي ولا رفيق", "Alone... I have no friend or companion"): -0.4
        }
        quran_map = {
            TXT("أتلو منه كل يوم ولو قليلاً بتدبر", "I recite daily, even a little, with reflection"): 1.0,
            TXT("أقرؤه في رمضان وأحياناً في غيره", "I read it in Ramadan and occasionally outside"): 0.3,
            TXT("أسمعه فقط ولا أفتح المصحف", "I only listen, I don't open the Mushaf"): -0.1,
            TXT("هجرته... يمر الشهر ولا أقرأ منه شيئاً", "I abandoned it... months pass without reading"): -0.6
        }

        w_raw = (
            mood_map.get(st.session_state.healer_answers.get("mood", ""), 0.1) +
            prayer_map.get(st.session_state.healer_answers.get("prayer", ""), 0.1) +
            company_map.get(st.session_state.healer_answers.get("company", ""), 0.1) +
            quran_map.get(st.session_state.healer_answers.get("quran", ""), 0.1)
        ) / 4
        w_raw = max(-1.0, min(1.0, w_raw * 2 - 1))

        b_raw = 0.5  # تقدير متوسط للبراءة بناءً على الإجابات
        S_score = ((w_raw + 1) / 2) * ((b_raw + 1) / 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("W (الولاء)", f"{w_raw:+.2f}")
        col2.metric("B (البراءة)", f"{b_raw:+.2f}")
        col3.metric("S (الثبات)", f"{S_score:.2f}")

        # --- الروشتة العلاجية ---
        st.markdown("---")
        st.subheader(TXT("💊 الروشتة العلاجية", "💊 The Prescription"))
        st.markdown(TXT("#### 📖 آيات تتدبرها:", "#### 📖 Verses to reflect on:"))
        for v in pres["verses"]:
            st.info(v)
        st.markdown(TXT(f"#### 🕋 حديث شريف:\n{pres['hadith']}", f"#### 🕋 Hadith:\n{pres['hadith']}"))
        st.markdown(TXT(f"#### 🏃 خطة عملية:\n{pres['action']}", f"#### 🏃 Action Plan:\n{pres['action']}"))

        # --- رسالة أمل – من الشك إلى اليقين ---
        st.markdown("---")
        st.markdown(TXT(
            """
            ### 🌅 من الظلمات إلى النور... من العبث إلى المعنى
            
            ﴿قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ ۚ إِنَّ اللَّهَ يَغْفِرُ الذُّنُوبَ جَمِيعًا﴾ [الزمر: ٥٣]
            
            **تذكر:** هذه المعادلة **S = W × B** ليست قدراً محتوماً. إنها قانون السببية الذي فطر الله الكون عليه. 
            ولكن الله – برحمته – فتح لك باب **التوبة**، الذي هو أعظم من أي معادلة. 
            التوبة تعيد ضبط المعادلة. التوبة تجعل W = 1 و B = 1. التوبة تولد طاقة روحية هائلة تمحو أثر كل سالب.
            
            **كل حركة وسكنة في حياتك** هي مولد طاقة. 
            صلاتك، صيامك، صدقتك، ذكرك... كلها ترفع W. 
            استغفارك، توبتك، مجاهدتك لهواك... كلها ترفع B. 
            وكلما ارتفع W و B، ارتفع S (الثبات)، فارتفعت معه الطمأنينة في الدنيا، والدرجات في الآخرة.
            
            أنت الآن في أول الطريق. ليس مطلوباً أن تصل إلى مقام إبراهيم (W=1, B=1) دفعة واحدة. 
            ولكن أن تخطو الخطوة الأولى. **كل يوم، جاهد نفسك قليلاً، وسترى كيف تتبدل الظلمات نوراً.**
            
            ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾ [البقرة: ٤٥]
            """,
            """
            ### 🌅 From darkness to light... from absurdity to meaning
            
            ﴿Say, O My servants who have transgressed against themselves, do not despair of the mercy of Allah. Indeed, Allah forgives all sins.﴾ [Az-Zumar: 53]
            
            **Remember:** This equation **S = W × B** is not an immutable fate. It is the law of causality upon which Allah created the universe. 
            But Allah – in His mercy – opened for you the door of **repentance**, which is greater than any equation. 
            Repentance resets the equation. Repentance makes W = 1 and B = 1. Repentance generates tremendous spiritual energy that erases every negative trace.
            
            **Every movement and stillness in your life** is an energy generator. 
            Your prayer, fasting, charity, remembrance... all raise W. 
            Your seeking forgiveness, repentance, striving against desire... all raise B. 
            And as W and B rise, S (stability) rises, bringing tranquility in this life and elevated ranks in the Hereafter.
            
            You are now at the beginning of the path. You are not required to reach Abraham's station (W=1, B=1) in one leap. 
            But take the first step. **Strive a little each day, and you will see how darkness turns to light.**
            
            ﴿And seek help through patience and prayer.﴾ [Al-Baqarah: 45]
            """
        ))

        # زر إعادة
        if st.button(TXT("🔄 أريد أن أبدأ من جديد", "🔄 I want to start over")):
            st.session_state.healer_answers = {}
            st.session_state.healer_done = False
            st.rerun()
