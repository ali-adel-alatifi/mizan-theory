# mizan/healer.py
"""
طبيب القلوب – رحلة من السؤال إلى اليقين
لا يشخص فقط، بل يأخذ بيدك إلى أول الطريق
"""

import streamlit as st
from config import TXT

# =============================================
# 1. الأسئلة – لحظات صدق مع النفس
# =============================================
HEALER_QUESTIONS = [
    {
        "id": "mood",
        "text": TXT(
            "في أعماقك، بعيداً عن الأقنعة... كيف تصف حال قلبك الآن؟",
            "Deep inside, beyond all masks... how do you describe your heart's state?"
        ),
        "options": [
            TXT("مطمئن بذكر الله", "At peace with Allah's remembrance"),
            TXT("متقلب بين اليقين والغفلة", "Fluctuating between certainty and heedlessness"),
            TXT("فيه قلق وضيق لا أعرف سببه", "Anxiety and tightness I can't explain"),
            TXT("قاسی کالحجارة أو أشد قسوة", "Hard as stone, or even harder")
        ]
    },
    {
        "id": "prayer",
        "text": TXT(
            "صلاتك... تلك الوقفة بين يدي الله. كيف هي في ميزانك؟",
            "Your Salah... that standing before Allah. How is it in your scale?"
        ),
        "options": [
            TXT("أقيمها وأجد فيها راحتي وسكينتي", "I establish it and find my rest in it"),
            TXT("أصليها في وقتها لكني مشغول القلب", "I pray on time but my heart is distracted"),
            TXT("أصليها متأخرة وأحياناً تفوتني", "I delay it and sometimes miss it"),
            TXT("ثقيلة عليّ... لا أجد لها طعماً", "It's heavy on me... I find no taste in it")
        ]
    },
    {
        "id": "sins",
        "text": TXT(
            "ما الذنب الذي إذا خلوت بنفسك... وجدته يعاودك ويُثقل روحك؟",
            "What sin, when you're alone with yourself, haunts you and burdens your soul?"
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
            "من تصاحب؟ فالم رء على دين خليله. من هم رفقتك في الطريق؟",
            "Who do you befriend? A person is on the religion of their friend. Who are your companions?"
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
            "وهذا القرآن... كلام ربك. كم هو نصيبك منه؟",
            "And this Quran... the words of your Lord. What is your share of it?"
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
# 2. روشتات – من الكتاب والسنة إلى خطة عملية
# =============================================
HEALING_PRESCRIPTIONS = {
    "شهوة تحاصرني": {
        "diagnosis": TXT(
            "ضعف في البراءة (B). الطاغوت الداخلي (الهوى) يستعبدك. "
            "أنت في الربع الثاني أو الرابع... تريد الخير لكنك لا تقوى على الشر. "
            "﴿وَأَمَّا مَنْ خَافَ مَقَامَ رَبِّهِ وَنَهَى النَّفْسَ عَنِ الْهَوَىٰ * فَإِنَّ الْجَنَّةَ هِيَ الْمَأْوَىٰ﴾",
            "Weakness in Disavowal (B). The inner Taghut (desire) enslaves you. "
            "You want good but can't resist evil."
        ),
        "verses": [
            "﴿وَلَا تَقْرَبُوا الزِّنَىٰ ۖ إِنَّهُ كَانَ فَاحِشَةً وَسَاءَ سَبِيلًا﴾ [الإسراء: ٣٢]",
            "﴿قُل لِّلْمُؤْمِنِينَ يَغُضُّوا مِنْ أَبْصَارِهِمْ﴾ [النور: ٣٠]",
        ],
        "hadith": TXT(
            "«حُفَّتِ الْجَنَّةُ بِالْمَكَارِهِ وَحُفَّتِ النَّارُ بِالشَّهَوَاتِ» [متفق عليه]",
            "«Paradise is surrounded by hardships, and Hell by desires.»"
        ),
        "action": TXT(
            "**خطتك هذا الأسبوع:** ١. صم يومين (الإثنين والخميس). ٢. إذا هاجتك شهوة، قم وتوضأ وصلِّ ركعتين. "
            "٣. قل كل صباح: 'اللهم إني أسألك حبك وحب من يحبك وحب عمل يقربني إلى حبك'. "
            "٤. احذف أي تطبيق أو حساب يثير شهوتك. هذه براءة عملية.",
            "**Your plan this week:** 1. Fast two days (Mon & Thu). 2. If desire strikes, make wudu and pray two rak'ahs. "
            "3. Say each morning: 'O Allah, I ask for Your love...' 4. Delete any app or account that stirs your desire."
        ),
    },
    "غضب يغلبني": {
        "diagnosis": TXT(
            "ضعف في الولاء (W). الغضب نار تحرق الإيمان. "
            "﴿وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ ۗ وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ﴾",
            "Weakness in Loyalty (W). Anger is a fire that burns faith."
        ),
        "verses": [
            "﴿وَلَا تَسْتَوِي الْحَسَنَةُ وَلَا السَّيِّئَةُ ۚ ادْفَعْ بِالَّتِي هِيَ أَحْسَنُ﴾ [فصلت: ٣٤]",
        ],
        "hadith": TXT(
            "«لَيْسَ الشَّدِيدُ بِالصُّرَعَةِ، إِنَّمَا الشَّدِيدُ الَّذِي يَمْلِكُ نَفْسَهُ عِنْدَ الْغَضَبِ» [متفق عليه]",
            "«The strong is not the one who overcomes people, but the one who controls himself when angry.»"
        ),
        "action": TXT(
            "**خطتك:** ١. إذا غضبت وأنت قائم فاجلس، وإن كنت جالساً فاضطجع. ٢. قل: 'أعوذ بالله من الشيطان الرجيم'. "
            "٣. توضأ فوراً. ٤. قبل أن تنام، سامح من أغضبك وادعُ له.",
            "**Your plan:** 1. If angry while standing, sit; if sitting, lie down. 2. Say: 'A'udhu billahi min ash-shaytan ir-rajim'. "
            "3. Make wudu immediately. 4. Before sleeping, forgive the one who angered you and pray for them."
        ),
    },
    "كبر أو عُجب": {
        "diagnosis": TXT(
            "ضعف في البراءة (B). الكبر أول معصية عُصي الله بها. "
            "﴿إِلَّا إِبْلِيسَ أَبَىٰ وَاسْتَكْبَرَ وَكَانَ مِنَ الْكَافِرِينَ﴾",
            "Weakness in Disavowal (B). Arrogance was the first sin against Allah."
        ),
        "verses": [
            "﴿وَلَا تَمْشِ فِي الْأَرْضِ مَرَحًا﴾ [الإسراء: ٣٧]",
        ],
        "hadith": TXT(
            "«لَا يَدْخُلُ الْجَنَّةَ مَنْ كَانَ فِي قَلْبِهِ مِثْقَالُ ذَرَّةٍ مِنْ كِبْرٍ» [مسلم]",
            "«Whoever has an atom's weight of arrogance in his heart will not enter Paradise.»"
        ),
        "action": TXT(
            "**خطتك:** ١. انظر في المرآة وقل: 'اللهم كما حسنت خلقي فحسن خلقي'. "
            "٢. اخدم أهلك بنفسك هذا الأسبوع (نظف، اطبخ، ساعد). ٣. امدح ثلاثة أشخاص كل يوم بصدق. "
            "٤. تذكر أنك من تراب وستعود إليه.",
            "**Your plan:** 1. Look in the mirror and say: 'O Allah, as You beautified my form, beautify my character.' "
            "2. Serve your family yourself this week. 3. Sincerely praise three people daily. "
            "4. Remember you are from dust and to dust you shall return."
        ),
    },
    "تعلّق قلبي بالدنيا": {
        "diagnosis": TXT(
            "ضعف في الولاء (W). حب الدنيا رأس كل خطيئة. "
            "﴿وَمَا الْحَيَاةُ الدُّنْيَا إِلَّا مَتَاعُ الْغُرُورِ﴾",
            "Weakness in Loyalty (W). Love of this world is the root of all sin."
        ),
        "verses": [
            "﴿بَلْ تُؤْثِرُونَ الْحَيَاةَ الدُّنْيَا * وَالْآخِرَةُ خَيْرٌ وَأَبْقَىٰ﴾ [الأعلى: ١٦-١٧]",
        ],
        "hadith": TXT(
            "«ازْهَدْ فِي الدُّنْيَا يُحِبَّكَ اللَّهُ، وَازْهَدْ فِيمَا فِي أَيْدِي النَّاسِ يُحِبُّوكَ» [ابن ماجه]",
            "«Renounce the world and Allah will love you; renounce what people possess and they will love you.»"
        ),
        "action": TXT(
            "**خطتك:** ١. تصدق كل يوم بشيء تحبه (مال، طعام، وقت). ٢. زر المقبرة هذا الأسبوع. "
            "٣. قل كل ليلة: 'اللهم لا تجعل الدنيا أكبر همنا ولا مبلغ علمنا'. "
            "٤. تذكر أنك ستموت وحدك، ولن ينفعك إلا عملك.",
            "**Your plan:** 1. Give charity daily from what you love. 2. Visit the graveyard this week. "
            "3. Say each night: 'O Allah, do not make this world our greatest concern.' "
            "4. Remember you will die alone, and only your deeds will benefit you."
        ),
    },
}

# =============================================
# 3. المحلل الشخصي الذكي – رحلة من السؤال إلى اليقين
# =============================================
def render_healer():
    """عرض طبيب القلوب التفاعلي."""
    
    # --- الغلاف الافتتاحي ---
    st.header("🩺 طبيب القلوب")
    st.markdown(TXT(
        """
        ### ﴿أَلَمْ يَأْنِ لِلَّذِينَ آمَنُوا أَن تَخْشَعَ قُلُوبُهُمْ لِذِكْرِ اللَّهِ﴾
        هذه ليست استشارة باردة. هذا وقفة مع النفس. أنا هنا فقط لأرافقك في لحظات صدق،
        لتكتشف بنفسك أين تقف، وإلى أين تسير. أجب عن هذه الأسئلة كما أنت، لا كما تتمنى أن تكون.
        """,
        """
        ### ﴿Has the time not come for those who believe that their hearts should become humbly submissive at the remembrance of Allah?﴾
        This is not a cold consultation. This is a pause with yourself. I am only here to accompany you in moments of truth,
        so you may discover for yourself where you stand and where you are heading.
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
        main_issue = st.session_state.healer_answers.get("sins", "شهوة تحاصرني")
        # نبحث عن الكلمة المفتاحية في إجابته
        issue_key = None
        for key in HEALING_PRESCRIPTIONS:
            if key in main_issue:
                issue_key = key
                break
        if not issue_key:
            issue_key = "شهوة تحاصرني"  # افتراضي

        pres = HEALING_PRESCRIPTIONS[issue_key]

        # --- عرض التشخيص (النور) ---
        st.markdown("---")
        st.subheader(TXT("📋 التشخيص", "📋 Diagnosis"))
        st.warning(pres["diagnosis"])

        # --- محاكاة حساب الموقع (W, B) ---
        mood_map = {
            "مطمئن بذكر الله": 0.9, "متقلب بين اليقين والغفلة": 0.4,
            "فيه قلق وضيق لا أعرف سببه": 0.1, "قاسی کالحجارة أو أشد قسوة": -0.6
        }
        prayer_map = {
            "أقيمها وأجد فيها راحتي وسكينتي": 1.0, "أصليها في وقتها لكني مشغول القلب": 0.4,
            "أصليها متأخرة وأحياناً تفوتني": -0.2, "ثقيلة عليّ... لا أجد لها طعماً": -0.7
        }
        company_map = {
            "أصحاب يعينونني على ذكر الله وطاعته": 0.8, "أهلي وعائلتي...": 0.3,
            "زملاء عمل أو دراسة": 0.0, "وحيد... لا صاحب لي ولا رفيق": -0.4
        }
        quran_map = {
            "أتلو منه كل يوم ولو قليلاً بتدبر": 1.0, "أقرؤه في رمضان وأحياناً في غيره": 0.3,
            "أسمعه فقط ولا أفتح المصحف": -0.1, "هجرته... يمر الشهر ولا أقرأ منه شيئاً": -0.6
        }

        w_raw = (
            mood_map.get(st.session_state.healer_answers.get("mood", ""), 0.1) +
            prayer_map.get(st.session_state.healer_answers.get("prayer", ""), 0.1) +
            company_map.get(st.session_state.healer_answers.get("company", ""), 0.1) +
            quran_map.get(st.session_state.healer_answers.get("quran", ""), 0.1)
        ) / 4
        w_raw = max(-1.0, min(1.0, w_raw * 2 - 1))

        b_raw = 0.5  # تقدير متوسط
        S_score = ((w_raw + 1) / 2) * ((b_raw + 1) / 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("W (الولاء)", f"{w_raw:+.2f}")
        col2.metric("B (البراءة)", f"{b_raw:+.2f}")
        col3.metric("S (الثبات)", f"{S_score:.2f}")

        # --- الروشتة العلاجية ---
        st.markdown("---")
        st.subheader("💊 الروشتة العلاجية")
        st.markdown("#### 📖 آيات تتدبرها:")
        for v in pres["verses"]:
            st.info(v)
        st.markdown(f"#### 🕋 حديث شريف:\n{pres['hadith']}")
        st.markdown(f"#### 🏃 خطة عملية:\n{pres['action']}")

        # --- رسالة أمل ---
        st.markdown("---")
        st.markdown(TXT(
            """
            ### 🌅 تذكر...
            ﴿قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ ۚ إِنَّ اللَّهَ يَغْفِرُ الذُّنُوبَ جَمِيعًا﴾
            أنت الآن في أول الطريق. ليس مطلوباً أن تصل إلى القمة دفعة واحدة، ولكن أن تخطو الخطوة الأولى. كل يوم، جاهد نفسك قليلاً، وسترى كيف تتبدل الظلمات نوراً.
            """,
            """
            ### 🌅 Remember...
            ﴿Say, O My servants who have transgressed against themselves, do not despair of the mercy of Allah.﴾
            You are now at the beginning of the path. You are not required to reach the top in one leap, but to take the first step. Strive a little each day, and you will see how darkness turns to light.
            """
        ))

        # زر إعادة
        if st.button(TXT("🔄 أريد أن أبدأ من جديد", "🔄 I want to start over")):
            st.session_state.healer_answers = {}
            st.session_state.healer_done = False
            st.rerun()
