# mizan/healer.py
"""
طبيب القلوب – رحلة من السؤال إلى اليقين
من منظور الدين القيم (قانون السببية) والإسلام الحنيف (الاستجابة الديناميكية)
كل حركة وسكنة: مولد طاقة نحو الولاية أو البراءة
"""

import streamlit as st
from config import TXT

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
    /* الأزرار */
    button {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
        "id": "wealth",
        "text": TXT(
            "الغنى والفقر... نعمتان متضادتان يبتلى بهما العبد. كيف تتعامل مع المال في ميزانك؟ ﴿وَمَا أَمْوَالُكُمْ وَلَا أَوْلَادُكُمْ بِالَّتِي تُقَرِّبُكُمْ عِنْدَنَا زُلْفَىٰ﴾",
            "Wealth and poverty... two opposite blessings with which a servant is tested. How do you handle money in your scale?"
        ),
        "options": [
            TXT("أزكي مالي وأتصدق وأرى أنه مال الله، والله هو الرزاق. (B مرتفع)", "I pay Zakat and give charity, seeing it as Allah's wealth. (High B)"),
            TXT("أجمع المال وأبخل به، وأشعر أنني أملكه. (B منخفض)", "I hoard wealth and act as if I own it. (Low B)"),
            TXT("أغضب على فقري وأسخط على قدر الله. (B منخفض)", "I resent poverty and am angry at Allah's decree. (Low B)"),
            TXT("أتعب في طلب الرزق لكني أتكل على الله. (W مرتفع)", "I work hard for provision but trust in Allah. (High W)")
        ]
    },
    {
        "id": "health",
        "text": TXT(
            "الصحة والمرض... ساقيان من كأس الحياة. كيف تتعامل مع جسدك في طريقك إلى الله؟ ﴿وَبَشِّرِ الصَّابِرِينَ﴾",
            "Health and illness... two cups from the same life. How do you treat your body on the path to Allah?"
        ),
        "options": [
            TXT("أصبر على المرض وأحتسب الأجر، وأشكر الله على الصحة. (S مرتفع)", "I am patient with illness and grateful for health. (High S)"),
            TXT("أجزع عند المرض وأغفل شكر الله عند الصحة. (S منخفض)", "I complain in illness and neglect gratitude in health. (Low S)"),
            TXT("أتخذ من صحتي قوة للعبادة والجهاد. (W مرتفع)", "I use my health for worship and striving. (High W)"),
            TXT("أدعو الله بالعافية وأرضى بقضائه. (B مرتفع)", "I pray for well-being and am content with His decree. (High B)")
        ]
    },
    {
        "id": "discernment",
        "text": TXT(
            "الفرقان والالتباس... نور الحق وظلمة الشبهة. هل ترى بوضوح بين الحق والباطل؟ ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ وَآمَنُوا بِرَسُولِهِ يُؤْتِكُمْ كِفْلَيْنِ مِنْ رَحْمَتِهِ وَيَجْعَلْ لَكُمْ نُورًا تَمْشُونَ بِهِ﴾",
            "Discernment and confusion... the light of truth and the darkness of doubt. Do you see clearly between right and wrong?"
        ),
        "options": [
            TXT("أرى الحق واضحاً وأتبعه، وأرى الباطل واضحاً وأجتنبه. (W و B مرتفعان)", "I see truth clearly and follow it, and see falsehood clearly and avoid it. (High W & B)"),
            TXT("تختلط عليّ الأمور وأحتار بين الخيارات. (S منخفض)", "I get confused and hesitate between options. (Low S)"),
            TXT("أتخذ القرارات بناءً على الهوى لا على الهدى. (W منخفض)", "I make decisions based on desire, not guidance. (Low W)"),
            TXT("أستخير الله في كل أمر وأسأله التوفيق. (W مرتفع)", "I pray for guidance in every matter. (High W)")
        ]
    },
    {
        "id": "patience",
        "text": TXT(
            "الصبر والجزع... ميزان الثبات في المحن. كيف تتعامل مع الشدائد؟ ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾",
            "Patience and panic... the scale of stability in trials. How do you deal with hardships?"
        ),
        "options": [
            TXT("أصبر على البلاء وأستعين بالله، وأعلم أن مع العسر يسراً. (S مرتفع)", "I am patient and seek Allah's help, knowing that hardship follows ease. (High S)"),
            TXT("أجزع وأضجر وأغضب على قدر الله. (S منخفض)", "I panic, complain, and get angry at Allah's decree. (Low S)"),
            TXT("أصبر ولا أجزع، ولكن مع شيء من التسخط. (B منخفض)", "I am patient but with some inner resentment. (Low B)"),
            TXT("أعلم أن البلاء كفارة للذنوب. (W مرتفع)", "I know that trial is an expiation for sins. (High W)")
        ]
    },
    {
        "id": "strength",
        "text": TXT(
            "القوة والوهن... سلاح المؤمن وسلاح المنافق. كيف تستخدم قوتك؟ ﴿وَأَعِدُّوا لَهُمْ مَا اسْتَطَعْتُمْ مِنْ قُوَّةٍ﴾",
            "Strength and weakness... the weapon of the believer and the hypocrite. How do you use your strength?"
        ),
        "options": [
            TXT("أستعمل قوتي في طاعة الله ونصرة المظلوم. (W و B مرتفعان)", "I use my strength for Allah's obedience and supporting the oppressed. (High W & B)"),
            TXT("أستعمل قوتي في طلب الدنيا وعبادة الهوى. (W منخفض)", "I use my strength for worldly gain and following desire. (Low W)"),
            TXT("أشعر بالوهن والعجز أمام المسؤوليات. (S منخفض)", "I feel weak and incapable before responsibilities. (Low S)"),
            TXT("أتوكل على الله وأجتهد فيما يرضيه. (W مرتفع)", "I trust in Allah and strive for His pleasure. (High W)")
        ]
    },
    {
        "id": "company",
        "text": TXT(
            "من تصاحب؟ فالمرء على دين خليله. رفقتك في الطريق إما أن تشحنك أو تستنزفك. ﴿الْأَخِلَّاءُ يَوْمَئِذٍ بَعْضُهُمْ لِبَعْضٍ عَدُوٌّ إِلَّا الْمُتَّقِينَ﴾",
            "Who do you befriend? A person is on the religion of their friend. Your companions either charge or drain you."
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
            "And this Quran... your Lord's words, Allah's extended rope. What is your share of it?"
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
            "أنت في الربع الثاني (W مرتفع، B منخفض): تحب الله لكنك لا تتبرأ من الباطل.",
            "**Mizan Diagnosis:** Weakness in Disavowal (B). The inner Taghut (desire) enslaves you. "
            "You are in the second quadrant (W high, B low): you love Allah but don't disavow falsehood."
        ),
        "verses": [
            "﴿وَلَا تَقْرَبُوا الزِّنَىٰ ۖ إِنَّهُ كَانَ فَاحِشَةً وَسَاءَ سَبِيلًا﴾",
            "﴿قُل لِّلْمُؤْمِنِينَ يَغُضُّوا مِنْ أَبْصَارِهِمْ﴾",
            "﴿إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ﴾",
        ],
        "hadith": TXT(
            "«حُفَّتِ الْجَنَّةُ بِالْمَكَارِهِ وَحُفَّتِ النَّارُ بِالشَّهَوَاتِ»",
            "«Paradise is surrounded by hardships, and Hell by desires.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع B):**\n"
            "١. **الصيام:** صم يومين هذا الأسبوع (الإثنين والخميس).\n"
            "٢. **الصلاة:** إذا هاجتك شهوة، قم وتوضأ وصلِّ ركعتين.\n"
            "٣. **الذكر:** قل كل صباح: 'اللهم إني أسألك حبك وحب من يحبك وحب عمل يقربني إلى حبك'.\n"
            "٤. **البراءة العملية:** احذف أي تطبيق أو حساب يثير شهوتك.\n\n"
            "**إرشاد من الإمام علي (ع):** 'أوثق عرى الإيمان: الحب في الله والبغض في الله.'",
            "**Your plan to restore balance (raising B):**\n"
            "1. **Fasting:** Fast two days this week.\n"
            "2. **Prayer:** If desire strikes, make wudu and pray two rak'ahs.\n"
            "3. **Remembrance:** Say each morning: 'O Allah, I ask for Your love...'\n"
            "4. **Practical Disavowal:** Delete any app or account that stirs your desire.\n\n"
            "**Guidance from Imam Ali (AS):** 'The firmest handhold of faith is love for the sake of Allah and hatred for the sake of Allah.'"
        ),
    },
    TXT("غضب يغلبني – طاقتي السلبية تتفلت", "Anger that overcomes me – my negative energy runs wild"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الولاء (W). الغضب نار تحرق الإيمان وتستنزف الطاقة الروحية. "
            "عندما يغضب الإنسان، ينقطع عن ذكر الله، فينخفض W فوراً، ويهبط S.",
            "**Mizan Diagnosis:** Weakness in Loyalty (W). Anger is a fire that burns faith and drains spiritual energy."
        ),
        "verses": [
            "﴿وَلَا تَسْتَوِي الْحَسَنَةُ وَلَا السَّيِّئَةُ ۚ ادْفَعْ بِالَّتِي هِيَ أَحْسَنُ﴾",
            "﴿وَإِمَّا يَنزَغَنَّكَ مِنَ الشَّيْطَانِ نَزْغٌ فَاسْتَعِذْ بِاللَّهِ﴾",
        ],
        "hadith": TXT(
            "«لَيْسَ الشَّدِيدُ بِالصُّرَعَةِ، إِنَّمَا الشَّدِيدُ الَّذِي يَمْلِكُ نَفْسَهُ عِنْدَ الْغَضَبِ»",
            "«The strong is not the one who overcomes people, but the one who controls himself when angry.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع W):**\n"
            "١. **تغيير الوضع:** إذا غضبت وأنت قائم فاجلس، وإن كنت جالساً فاضطجع.\n"
            "٢. **الاستعاذة:** قل: 'أعوذ بالله من الشيطان الرجيم'.\n"
            "٣. **الوضوء:** توضأ فوراً.\n"
            "٤. **الصبر والصلاة:** ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾. صلِّ ركعتين.\n"
            "٥. **العفو قبل النوم:** سامح من أغضبك وادعُ له.\n\n"
            "**إرشاد من الإمام الحسن (ع):** 'خير العمل ما صلح به الدين والدنيا.'",
            "**Your plan to restore balance (raising W):**\n"
            "1. **Change position:** If angry while standing, sit; if sitting, lie down.\n"
            "2. **Seek refuge:** Say: 'I seek refuge in Allah from the accursed Satan'.\n"
            "3. **Ablution:** Make wudu immediately.\n"
            "4. **Patience and Prayer:** ﴿Seek help through patience and prayer.﴾ Pray two rak'ahs.\n"
            "5. **Forgive before sleep:** Forgive the one who angered you and pray for them.\n\n"
            "**Guidance from Imam Hassan (AS):** 'The best deed is that which rectifies religion and the world.'"
        ),
    },
    TXT("كبر أو عُجب – ولائي (W) ليس خالصاً لله", "Arrogance – my loyalty (W) is not pure"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في البراءة (B) من الكبر والعجب. الكبر أول معصية عُصي الله بها. "
            "المتكبر يرى نفسه فوق القانون، فيرفض الخضوع (W) ويستكبر عن الحق (B).",
            "**Mizan Diagnosis:** Weakness in Disavowal (B) from arrogance. Arrogance was the first sin."
        ),
        "verses": [
            "﴿وَلَا تَمْشِ فِي الْأَرْضِ مَرَحًا﴾",
            "﴿تِلْكَ الدَّارُ الْآخِرَةُ نَجْعَلُهَا لِلَّذِينَ لَا يُرِيدُونَ عُلُوًّا فِي الْأَرْضِ وَلَا فَسَادًا﴾",
        ],
        "hadith": TXT(
            "«لَا يَدْخُلُ الْجَنَّةَ مَنْ كَانَ فِي قَلْبِهِ مِثْقَالُ ذَرَّةٍ مِنْ كِبْرٍ»",
            "«Whoever has an atom's weight of arrogance in his heart will not enter Paradise.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع B):**\n"
            "١. **التواضع العملي:** انظر في المرآة وقل: 'اللهم كما حسنت خلقي فحسن خلقي'.\n"
            "٢. **خدمة الآخرين:** اخدم أهلك بنفسك هذا الأسبوع.\n"
            "٣. **الثناء على الغير:** امدح ثلاثة أشخاص كل يوم بصدق.\n"
            "٤. **تذكر الأصل:** تذكر أنك من تراب وستعود إليه.\n"
            "٥. **سجدة التواضع:** أطل السجود في صلاتك.\n\n"
            "**إرشاد من الإمام الحسين (ع):** 'إن الله يحب العبد المتواضع.'",
            "**Your plan to restore balance (raising B):**\n"
            "1. **Practical humility:** Look in the mirror and say: 'O Allah, as You beautified my form, beautify my character.'\n"
            "2. **Serve others:** Serve your family yourself this week.\n"
            "3. **Praise others:** Sincerely praise three people daily.\n"
            "4. **Remember origin:** You are from dust and to dust you shall return.\n"
            "5. **Prostration of humility:** Lengthen your prostration in prayer.\n\n"
            "**Guidance from Imam Hussain (AS):** 'Allah loves the humble servant.'"
        ),
    },
    TXT("تعلّق قلبي بالدنيا – E يطغى على S", "My heart is attached to this world – E overwhelms S"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الولاء (W). حب الدنيا رأس كل خطيئة. "
            "عندما يطغى التمكين المادي (E) على الثبات الروحي (S)، يدخل الإنسان في حالة 'الاستدراج'.",
            "**Mizan Diagnosis:** Weakness in Loyalty (W). Love of this world is the root of all sin."
        ),
        "verses": [
            "﴿بَلْ تُؤْثِرُونَ الْحَيَاةَ الدُّنْيَا * وَالْآخِرَةُ خَيْرٌ وَأَبْقَىٰ﴾",
            "﴿اعْلَمُوا أَنَّمَا الْحَيَاةُ الدُّنْيَا لَعِبٌ وَلَهْوٌ وَزِينَةٌ﴾",
        ],
        "hadith": TXT(
            "«ازْهَدْ فِي الدُّنْيَا يُحِبَّكَ اللَّهُ، وَازْهَدْ فِيمَا فِي أَيْدِي النَّاسِ يُحِبُّوكَ»",
            "«Renounce the world and Allah will love you; renounce what people possess and they will love you.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن (رفع W):**\n"
            "١. **الصدقة اليومية:** تصدق كل يوم بشيء تحبه.\n"
            "٢. **زيارة القبور:** زر المقبرة هذا الأسبوع.\n"
            "٣. **الدعاء:** قل كل ليلة: 'اللهم لا تجعل الدنيا أكبر همنا ولا مبلغ علمنا'.\n"
            "٤. **تدبر القرآن:** اقرأ سورة التكاثر كل يوم وتدبر معناها.\n"
            "٥. **تذكر:** ستموت وحدك، ولن ينفعك إلا عملك.\n\n"
            "**إرشاد من الإمام الحسين (ع):** 'إن الله خلق الدنيا للآخرة.'",
            "**Your plan to restore balance (raising W):**\n"
            "1. **Daily charity:** Give charity daily from what you love.\n"
            "2. **Visit graves:** Visit the graveyard this week.\n"
            "3. **Supplication:** Say each night: 'O Allah, do not make this world our greatest concern.'\n"
            "4. **Reflect on Quran:** Read Surat At-Takathur daily and reflect on its meaning.\n"
            "5. **Remember:** You will die alone, and only your deeds will benefit you.\n\n"
            "**Guidance from Imam Hussain (AS):** 'Allah created this world for the Hereafter.'"
        ),
    },
    TXT("الغنى والفقر – ميزان شكري ورضائي", "Wealth and Poverty – The Scale of Gratitude and Contentment"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في البراءة (B) أو الولاء (W). "
            "المال فتنة، والفقر فتنة. الأنبياء والأولياء ابتلوا بهما معاً. "
            "الغنى قد يجر إلى الطغيان، والفقر قد يجر إلى السخط.",
            "**Mizan Diagnosis:** Weakness in Disavowal (B) or Loyalty (W). "
            "Wealth and poverty are both trials. The prophets and saints were tested with both."
        ),
        "verses": [
            "﴿كُلُّ نَفْسٍ ذَائِقَةُ الْمَوْتِ ۗ وَإِنَّمَا تُؤْجَرُونَ يَوْمَ الْقِيَامَةِ ۚ فَمَنْ زُحْزِحَ عَنِ النَّارِ وَأُدْخِلَ الْجَنَّةَ فَقَدْ فَازَ ۚ وَمَا الْحَيَاةُ الدُّنْيَا إِلَّا مَتَاعُ الْغُرُورِ﴾",
            "﴿وَلَا تَجْعَلْ يَدَكَ مَغْلُولَةً إِلَىٰ عُنُقِكَ وَلَا تَبْسُطْهَا كُلَّ الْبَسْطِ فَتَقْعَدَ مَلُومًا مَحْسُورًا﴾",
        ],
        "hadith": TXT(
            "«لَوْ كَانَتِ الدُّنْيَا تَعْدِلُ عِنْدَ اللَّهِ جَنَاحَ بَعُوضَةٍ مَا سَقَى كَافِرًا مِنْهَا شَرْبَةَ مَاءٍ»",
            "«If this world were worth a mosquito's wing to Allah, He would not give a disbeliever a drink of water from it.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن:**\n"
            "١. **الزكاة والصدقة:** تصدق من مالك، ولو بالقليل.\n"
            "٢. **رضا بالقدر:** تعلم الرضا بما قسم الله لك.\n"
            "٣. **لا للمال الحرام:** تذكر أن الحرام لا يبارك فيه.\n"
            "٤. **الإرشاد من الإمام علي (ع):** 'من أصلح آخرته أصلح الله دنياه.'",
            "**Your plan to restore balance:**\n"
            "1. **Zakat and Charity:** Give charity from your wealth, even a little.\n"
            "2. **Contentment:** Learn to be content with what Allah has given you.\n"
            "3. **No forbidden wealth:** Remember that unlawful wealth brings no blessing.\n"
            "4. **Guidance from Imam Ali (AS):** 'Whoever rectifies his Hereafter, Allah rectifies his world.'"
        ),
    },
    TXT("الصحة والمرض – ميزان الصبر والشكر", "Health and Illness – The Scale of Patience and Gratitude"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الثبات (S). الصحة نعمة، والمرض ابتلاء. "
            "المؤمن الصادق يشكر على الصحة ويصبر على المرض.",
            "**Mizan Diagnosis:** Weakness in Stability (S). Health is a blessing, illness is a trial. "
            "The true believer is grateful for health and patient in illness."
        ),
        "verses": [
            "﴿وَإِنْ يَمْسَسْكَ اللَّهُ بِضُرٍّ فَلَا كَاشِفَ لَهُ إِلَّا هُوَ ۖ وَإِنْ يَمْسَسْكَ بِخَيْرٍ فَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ﴾",
            "﴿وَلَئِنْ أَذَقْنَاهُ رَحْمَةً مِنَّا مِنْ بَعْدِ ضَرَّاءَ مَسَّتْهُ لَيَقُولَنَّ هَذَا لِي وَمَا أَظُنُّ السَّاعَةَ قَائِمَةً﴾",
        ],
        "hadith": TXT(
            "«مَا يُصِيبُ الْمُؤْمِنَ مِنْ وَصَبٍ وَلَا نَصَبٍ إِلَّا كُفِّرَ عَنْهُ»",
            "«No believer is afflicted with illness or fatigue except that it expiates his sins.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن:**\n"
            "١. **شكر الله على الصحة:** قل 'الحمد لله على نعمة الصحة' كل يوم.\n"
            "٢. **احتساب الأجر في المرض:** تذكر أن المرض يكفر الذنوب ويرفع الدرجات.\n"
            "٣. **الصبر والاستعانة بالله:** ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾.\n"
            "٤. **الإرشاد من الإمام علي (ع):** 'من صبر على البلاء فاز.'",
            "**Your plan to restore balance:**\n"
            "1. **Thank Allah for health:** Say 'Praise be to Allah for the blessing of health' daily.\n"
            "2. **Seek reward in illness:** Remember that illness expiates sins and raises ranks.\n"
            "3. **Patience and seeking help from Allah:** ﴿Seek help through patience and prayer.﴾\n"
            "4. **Guidance from Imam Ali (AS):** 'Whoever is patient in trial succeeds.'"
        ),
    },
    TXT("الفرقان والالتباس – ميزان الهدى والضلال", "Discernment and Confusion – The Scale of Guidance and Misguidance"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الولاء (W). الفراشات في القلب تمنع رؤية الحق. "
            "القرآن فرقان. من تمسك به نجا، ومن أعرض عنه ضل.",
            "**Mizan Diagnosis:** Weakness in Loyalty (W). Doubts in the heart prevent seeing the truth."
        ),
        "verses": [
            "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ وَآمَنُوا بِرَسُولِهِ يُؤْتِكُمْ كِفْلَيْنِ مِنْ رَحْمَتِهِ وَيَجْعَلْ لَكُمْ نُورًا تَمْشُونَ بِهِ﴾",
            "﴿فَمَنِ اتَّبَعَ هُدَايَ فَلَا يَضِلُّ وَلَا يَشْقَىٰ﴾",
        ],
        "hadith": TXT(
            "«تَرَكْتُ فِيكُمْ أَمْرَيْنِ لَنْ تَضِلُّوا مَا تَمَسَّكْتُمْ بِهِمَا: كِتَابَ اللَّهِ وَسُنَّةَ نَبِيِّهِ»",
            "«I have left among you two things that you will never go astray as long as you hold fast to them: the Book of Allah and the Sunnah of His Prophet.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن:**\n"
            "١. **التمسك بالقرآن والسنة:** اجعل منهما مصدر نورك.\n"
            "٢. **التفكر والتدبر:** تدبر آيات الله في الآفاق والأنفس.\n"
            "٣. **الاستخارة:** استخر الله في كل أمر.\n"
            "٤. **الإرشاد من الإمام الحسين (ع):** 'القرآن فرقان بين الحق والباطل.'",
            "**Your plan to restore balance:**\n"
            "1. **Hold fast to Quran and Sunnah:** Make them your source of light.\n"
            "2. **Contemplation:** Reflect on Allah's signs in the horizons and within yourselves.\n"
            "3. **Pray for guidance:** Seek Allah's guidance in every matter.\n"
            "4. **Guidance from Imam Hussain (AS):** 'The Quran is the criterion between truth and falsehood.'"
        ),
    },
    TXT("الصبر والجزع – ميزان الثبات في المحن", "Patience and Panic – The Scale of Stability in Trials"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الثبات (S). الصبر زينة المؤمن، والجزع طريق الشيطان.",
            "**Mizan Diagnosis:** Weakness in Stability (S). Patience is the adornment of the believer."
        ),
        "verses": [
            "﴿وَبَشِّرِ الصَّابِرِينَ﴾",
            "﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾",
        ],
        "hadith": TXT(
            "«الصَّبْرُ نِصْفُ الْإِيمَانِ»",
            "«Patience is half of faith.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن:**\n"
            "١. **تذكر الأجر:** الصبر على البلاء يرفع الدرجات.\n"
            "٢. **الاستعانة بالصلاة:** الصلاة هي وسيلة الشحن الروحي.\n"
            "٣. **الدعاء:** ادع الله أن يثبتك عند الشدائد.\n"
            "٤. **الإرشاد من الإمام علي (ع):** 'الصبر صبران: صبر على ما تكره، وصبر على ما تحب.'",
            "**Your plan to restore balance:**\n"
            "1. **Remember the reward:** Patience in trial raises ranks.\n"
            "2. **Seek help through prayer:** Prayer is the spiritual charging station.\n"
            "3. **Supplication:** Pray to Allah to keep you steadfast in hardships.\n"
            "4. **Guidance from Imam Ali (AS):** 'Patience is of two kinds: patience over what you dislike, and patience over what you like.'"
        ),
    },
    TXT("القوة والوهن – ميزان العزة والذلة", "Strength and Weakness – The Scale of Honor and Humiliation"): {
        "diagnosis": TXT(
            "**التشخيص بالميزان:** ضعف في الولاء (W). القوة ليست عضلية، بل قوة إيمان وثبات.",
            "**Mizan Diagnosis:** Weakness in Loyalty (W). Strength is not physical, but faith and steadfastness."
        ),
        "verses": [
            "﴿وَأَعِدُّوا لَهُمْ مَا اسْتَطَعْتُمْ مِنْ قُوَّةٍ﴾",
            "﴿اللَّهُ وَلِيُّ الَّذِينَ آمَنُوا يُخْرِجُهُمْ مِنَ الظُّلُمَاتِ إِلَى النُّورِ﴾",
        ],
        "hadith": TXT(
            "«الْمُؤْمِنُ الْقَوِيُّ خَيْرٌ وَأَحَبُّ إِلَى اللَّهِ مِنَ الْمُؤْمِنِ الضَّعِيفِ»",
            "«The strong believer is better and more beloved to Allah than the weak believer.»"
        ),
        "action": TXT(
            "**خطتك لاستعادة التوازن:**\n"
            "١. **الاستعانة بالله:** ﴿إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ﴾.\n"
            "٢. **طلب العزة من الله:** قل 'اللهم أعزني بطاعتك'.\n"
            "٣. **عدم الركون إلى الدنيا:** القوة الحقيقية في تقوى الله.\n"
            "٤. **الإرشاد من الإمام علي (ع):** 'من عرف نفسه عرف ربه.'",
            "**Your plan to restore balance:**\n"
            "1. **Seek help from Allah:** ﴿You alone we worship and You alone we ask for help.﴾\n"
            "2. **Seek honor from Allah:** Say 'O Allah, honor me through obedience to You.'\n"
            "3. **Do not rely on the world:** True strength is in piety.\n"
            "4. **Guidance from Imam Ali (AS):** 'Whoever knows himself knows his Lord.'"
        ),
    },
}

# =============================================
# ٣. المحلل الشخصي الذكي – رحلة من السؤال إلى اليقين
# =============================================
def render_healer():
    """عرض طبيب القلوب التفاعلي."""
    
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
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
