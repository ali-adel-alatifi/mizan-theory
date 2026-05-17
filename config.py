# mizan/config.py
"""
الوحدة المركزية للثوابت والبيانات الأساسية
تحتوي: الثوابت الوجودية، المعجم الهندسي، المؤشرات الأخلاقية،
أسئلة البوصلة، الشواهد التاريخية، النصوص متعددة اللغات.
"""

import streamlit as st

# =============================================
# 1. النظام اللغوي
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

LANG = st.session_state.lang
TXT = lambda ar, en: ar if LANG == "ar" else en

# =============================================
# 2. الثوابت الوجودية – المعجم الهندسي (28 حرفاً)
# =============================================
LETTERS_DB = {
    'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60,
    'ح': 8, 'ط': 9, 'ق': 100, 'ك': 20, 'ص': 90,
    'ع': 70, 'ي': 10, 'هـ': 5, 'ن': 50, 'ف': 80,
    'و': 6, 'ب': 2, 'ظ': 900, 'ض': 800, 'غ': 1000,
    'ذ': 700, 'خ': 600, 'ش': 300, 'ز': 7, 'ج': 3,
    'ت': 400, 'ث': 500
}

# =============================================
# 3. المؤشرات الأخلاقية الأساسية (11 مؤشراً)
# =============================================
INDICATORS_META = [
    {"ar": "الصلاة (إقامة/تضييع)", "en": "Prayer", "letter": "ن", "val": 50},
    {"ar": "الزكاة والصدقات (إيتاء/منع)", "en": "Zakat & Charity", "letter": "ص", "val": 90},
    {"ar": "الولاء لله ورسوله والمؤمنين", "en": "Loyalty to Allah & Believers", "letter": "أ", "val": 1},
    {"ar": "تحكيم الشريعة (تحكيم/رفض)", "en": "Applying Sharia", "letter": "ل", "val": 30},
    {"ar": "العدل (عدل/ظلم)", "en": "Justice", "letter": "ق", "val": 100},
    {"ar": "الشورى (تشاور/استبداد)", "en": "Consultation", "letter": "م", "val": 40},
    {"ar": "البراءة من الطاغوت (براءة/موالاة)", "en": "Disavowal of Taghut", "letter": "هـ", "val": 5},
    {"ar": "الرحمة والعطاء – الماعون (رحمة/قسوة)", "en": "Mercy & Giving", "letter": "ح", "val": 8},
    {"ar": "الأمر بالمعروف (أمر/نهي)", "en": "Enjoining Good", "letter": "ف", "val": 80},
    {"ar": "النهي عن المنكر (نهي/أمر)", "en": "Forbidding Evil", "letter": "و", "val": 6},
    {"ar": "العفاف والتورع", "en": "Chastity & Godly Caution", "letter": "ط", "val": 9},
]
N_IND = len(INDICATORS_META)

def get_indicator_label(i):
    meta = INDICATORS_META[i]
    name = meta["ar"] if LANG == "ar" else meta["en"]
    return f"{name}  [{meta['letter']}={meta['val']}]"

# =============================================
# 4. قاعدة بيانات البوصلة الكاملة (19 سؤالاً)
# =============================================
COMPASS_DATA = [
    {"id":1,"topic":TXT("تحكيم الشريعة في زمن القوانين الوضعية","Sharia vs Man-Made Laws"),"letter":"ق","value":100,
     "text":TXT("في زمن سيادة القوانين الوضعية، وشعار 'الدين لله والوطن للجميع'، كمسلم: ما هو موقفك من تحكيم شرع الله؟","In an age of man-made laws..."),
     "answers":[(TXT("أجاهد لتطبيق شرع الله في كل مناحي الحياة","I strive to apply Sharia"),0.5,0.5),(TXT("أتمنى تطبيقها لكني لا أعمل لأجلها","I wish but don't act"),0.3,-0.2),(TXT("بعض أحكامها صالح والآخر لا","Some valid, some not"),-0.2,-0.2),(TXT("الشريعة لا تصلح لهذا العصر","Sharia is unsuitable"),-0.4,-0.5)]},
    {"id":2,"topic":TXT("الولاء للعرق والحزب والطائفة","Loyalty to Race, Party, Sect"),"letter":"أ","value":1,
     "text":TXT("في عصر أصبح فيه الولاء للعرق والحزب والطائفة والمذهب هو المعيار، كمسلم: ما هو موقفك؟","In an age of racial loyalty..."),
     "answers":[(TXT("ولائي لله ورسوله والمؤمنين فوق كل رابطة","My loyalty to Allah above all"),0.7,0.2),(TXT("أوازن بين ولائي للإسلام وانتمائي العرقي","I try to balance"),0.3,-0.2),(TXT("ولائي لديني ضعيف وأميل للفخر بعرقي","Weak religious loyalty"),-0.2,0.1),(TXT("لا أرى مشكلة في تقديم العرق على الدين","Race over religion"),-0.5,-0.3)]},
    {"id":3,"topic":TXT("الاستهزاء بالمقدسات وحرية التعبير","Mockery of Sanctities & Free Speech"),"letter":"هـ","value":5,
     "text":TXT("في زمن تُباح فيه 'حرية التعبير' للاستهزاء بالدين والمقدسات، كمسلم: ما هو موقفك؟","In an age of free speech..."),
     "answers":[(TXT("أبغض في الله المستهزئين وأدين فعلهم","I hate and condemn mockers"),0.3,0.7),(TXT("أستنكر الاستهزاء بقلبي لكن لا أعلن","I disapprove in heart"),0.1,-0.1),(TXT("أرى أنها حرية رأي ولا داعي للغضب","Free speech, no anger"),-0.2,0.1),(TXT("أضحك معهم أحياناً ولا أرى ضرراً","I laugh with them"),-0.3,-0.3)]},
    {"id":4,"topic":TXT("الربا والنظام المالي العالمي","Usury and Global Finance"),"letter":"ص","value":90,
     "text":TXT("في زمن يقوم فيه النظام المالي العالمي على الربا، وأصبح التعامل بالفوائد 'أمراً طبيعياً'، كمسلم: ما هو موقفك؟","In an age of usurious finance..."),
     "answers":[(TXT("أتجنب الربا بكل صوره وأبحث عن بدائل إسلامية","I avoid all usury"),0.3,0.7),(TXT("أكره الربا لكني مضطر للتعامل به أحياناً","I hate it but am forced"),0.1,-0.2),(TXT("أتعامل بالربا كالجميع ولا أرى مشكلة","I deal with it like everyone"),-0.2,0.1),(TXT("الربا ضرورة اقتصادية وتحريمه كان لزمن غير زمننا","Usury is a necessity"),-0.3,-0.3)]},
    {"id":5,"topic":TXT("العلمانية وفصل الدين عن الدولة","Secularism & Separation"),"letter":"ك","value":20,
     "text":TXT("في زمن تسود فيه العلمانية، وتُرفع شعارات 'فصل الدين عن الدولة'، كمسلم: ما هو موقفك؟","In an age of secularism..."),
     "answers":[(TXT("أرفض العلمانية وأؤمن أن الإسلام دين ودولة","I reject secularism"),0.5,0.5),(TXT("العلمانية قد تكون حلاً مؤقتاً","Temporary solution"),0.1,-0.1),(TXT("لا أمانع فصل الدين عن السياسة","I don't mind separation"),-0.2,0.1),(TXT("العلمانية هي الطريق الصحيح للتقدم","Secularism is correct"),-0.4,-0.5)]},
    {"id":6,"topic":TXT("إقامة الحدود الشرعية","Establishing Sharia Penalties"),"letter":"ح","value":8,
     "text":TXT("في زمن تُلغى فيه الحدود الشرعية (كقطع يد السارق) بدعوى 'الهمجية' و'عدم الإنسانية'، كمسلم: ما هو موقفك؟","In an age of abolishing penalties..."),
     "answers":[(TXT("الحدود الشرعية رحمة وعدل وأؤمن بضرورة إقامتها","Penalties are mercy"),0.3,0.7),(TXT("الحدود حق لكن الظروف الحالية لا تسمح","Right but conditions hard"),0.1,-0.1),(TXT("أشعر بالحرج من بعض الحدود وأراها قاسية","I feel embarrassed"),-0.2,0.1),(TXT("الحدود الشرعية همجية ولا تصلح للعصر الحديث","Penalties are barbaric"),-0.3,-0.3)]},
    {"id":7,"topic":TXT("الإلحاد وإنكار الخالق","Atheism & Denying the Creator"),"letter":"ن","value":50,
     "text":TXT("في زمن ينتشر فيه الإلحاد، ويُقدَّم العلم على أنه ينفي وجود الله، كمسلم: ما هو موقفك؟","In an age of atheism..."),
     "answers":[(TXT("أؤمن بالله يقيناً لا يتزعزع وأرى في العلم دليلاً عليه","I believe certainly"),0.5,0.5),(TXT("أؤمن بالله لكني لا أملك حججاً للرد على الشبهات","I believe but lack arguments"),0.1,-0.1),(TXT("تساورني أحياناً شكوك لكني أعود للإيمان","Doubts cross my mind"),-0.2,0.1),(TXT("الإلحاد طرح فكري يحترم والدين مجرد أساطير","Atheism is respectable"),-0.4,-0.5)]},
    {"id":8,"topic":TXT("الجهاد ونصرة المستضعفين","Jihad & Supporting the Oppressed"),"letter":"ر","value":200,
     "text":TXT("في زمن يُشوَّه فيه الجهاد ويوصم بـ 'الإرهاب'، ويُخذل فيه المستضعفون من المسلمين، كمسلم: ما هو موقفك؟","In an age of distorting jihad..."),
     "answers":[(TXT("الجهاد ذروة سنام الإسلام وأتمنى أن أكون في صفوف المجاهدين","Jihad is peak of Islam"),0.3,0.7),(TXT("الجهاد حق وأدعمه بقلبي ومالي إن استطعت","Jihad is right, I support"),0.1,-0.1),(TXT("أخشى من الجهاد وأرى أنه يجلب المشاكل","I fear jihad"),-0.2,0.1),(TXT("الجهاد أصبح إرهاباً ولا مكان له في هذا العصر","Jihad became terrorism"),-0.3,-0.3)]},
    {"id":9,"topic":TXT("حقوق المرأة بين الإسلام والتغريب","Women's Rights: Islam vs. West"),"letter":"هـ","value":5,
     "text":TXT("في زمن تُطرح فيه 'حقوق المرأة' بصيغة غربية تنتزعها من فطرتها، وتُتهم الشريعة بظلمها، كمسلم: ما هو موقفك؟","In an age of women's rights..."),
     "answers":[(TXT("أؤمن أن الإسلام كرم المرأة ورفع شأنها وأن أحكامه عين العدل","Islam honored women"),0.5,0.5),(TXT("أؤمن بالإسلام لكني أرى ضرورة تحديث بعض الأحكام","Need update"),0.1,-0.1),(TXT("أشعر بالحرج من بعض أحكام الإسلام الخاصة بالمرأة","I feel embarrassed"),-0.2,0.1),(TXT("الإسلام ظلم المرأة وتحريرها يكون بالعلمانية","Islam oppressed women"),-0.4,-0.5)]},
    {"id":10,"topic":TXT("العولمة والذوبان الحضاري والموضة والاستهلاك","Globalization & Fashion"),"letter":"م","value":40,
     "text":TXT("في زمن العولمة التي تسعى لطمس الهويات، وتحول الاستهلاك إلى ثقافة، وأصبح الترف هدفاً، والموضة تفرض أزياء تخالف الفطرة... ما هو موقفك؟","In an age of globalization..."),
     "answers":[(TXT("أتمسك بهويتي الإسلامية وأتبرأ من تقليد الكفار وأزهد في الدنيا","I hold fast to my Islamic identity"),0.5,0.5),(TXT("أحاول أوازن بين هويتي ومتطلبات العصر","I try to balance"),0.1,-0.1),(TXT("أقلد الغرب في ثقافته وأزيائه واستهلاكه","I imitate the West"),-0.2,0.1),(TXT("الثقافة الغربية هي التقدم ويجب الاندماج","Western culture is progress"),-0.4,-0.5)]},
    {"id":11,"topic":TXT("الديمقراطية والتشريع","Democracy & Legislation"),"letter":"ل","value":30,
     "text":TXT("في زمن تُقدَّس فيه الديمقراطية وتُجعل الشعب هو مصدر التشريع، كمسلم: ما هو موقفك؟","In an age of democracy..."),
     "answers":[(TXT("التشريع لله وحده والشورى طاعة لله في تطبيق ما شرع","Legislation for Allah"),0.5,0.5),(TXT("الديمقراطية وسيلة يمكن استخدامها لتحقيق مصالح","Democracy is a tool"),0.1,-0.1),(TXT("أفضّل الديمقراطية على الاستبداد","I prefer democracy"),-0.2,0.1),(TXT("الديمقراطية أفضل نظام والشريعة لا تصلح سياسياً","Democracy is best"),-0.4,-0.5)]},
    {"id":12,"topic":TXT("التعددية الدينية","Religious Pluralism"),"letter":"ي","value":10,
     "text":TXT("في زمن تُطرح فيه 'التعددية الدينية' على أنها تعني أن كل الأديان طرق للخلاص، كمسلم: ما هو موقفك؟","In an age of pluralism..."),
     "answers":[(TXT("الإسلام هو الدين الوحيد المقبول عند الله","Islam is the only accepted religion"),0.5,0.5),(TXT("الإسلام هو الحق لكني لا أحكم على الآخرين","Islam is truth but I don't judge"),0.1,-0.1),(TXT("أرى أن كل الأديان فيها جزء من الحق","All religions have truth"),-0.2,0.1),(TXT("كل الأديان سواء ولا يحق لأحد ادعاء الحقيقة","All religions are equal"),-0.4,-0.5)]},
    {"id":13,"topic":TXT("الحب في الله والبغض في الله","Love & Hatred for Allah"),"letter":"ق","value":100,
     "text":TXT("في زمن أصبحت فيه المصلحة هي المعيار الأساسي في العلاقات، واختفى معنى 'الحب في الله والبغض في الله'، كمسلم: ما هو موقفك؟","In an age of interests..."),
     "answers":[(TXT("أحب في الله أولياءه وأبغض في الله أعداءه","I love and hate for Allah"),0.5,0.5),(TXT("أحاول لكن علاقاتي تغلب عليها المصالح","I try but interests dominate"),0.1,-0.1),(TXT("أتعامل مع الجميع بالمثل لا حب ولا بغض","I deal equally with all"),-0.2,0.1),(TXT("علاقاتي كلها تقوم على مصلحتي الشخصية","My relationships are interests only"),-0.4,-0.5)]},
    {"id":14,"topic":TXT("الصدق والأمانة والوفاء في زمن الكذب والغش","Truthfulness in an Age of Lying"),"letter":"ط","value":9,
     "text":TXT("في زمن أصبح الخداع والكذب والغش ذكاءً، وخان الناس الأمانات والعهود، كمسلم: ما هو موقفك من الصدق والأمانة والوفاء؟","In an age of deception..."),
     "answers":[(TXT("الصدق والأمانة والوفاء دين وألتزم بها ولو خسرت","Truthfulness is my religion"),0.5,0.5),(TXT("أحاول الالتزام لكني قد أضطر للكذب أحياناً","I try but may be forced"),0.1,-0.1),(TXT("المبالغة في الصدق سذاجة والواقع يفرض المرونة","Excessive honesty is naivety"),-0.2,0.1),(TXT("الكذب والغش والخيانة أدوات ضرورية للنجاح","Lying is necessary for success"),-0.4,-0.5)]},
    {"id":15,"topic":TXT("الأمر بالمعروف والنهي عن المنكر في زمن الفواحش","Enjoining Good in an Age of Indecency"),"letter":"ب","value":2,
     "text":TXT("في زمن انتشرت فيه الفواحش، وصار إنكار المنكر 'تطرفاً'، كمسلم: ما هو موقفك من الأمر بالمعروف والنهي عن المنكر؟","In an age of indecency..."),
     "answers":[(TXT("آمر بالمعروف وأنهى عن المنكر بكل استطاعتي","I enjoin and forbid as much as I can"),0.3,0.7),(TXT("أنكر بقلبي وأحياناً بلساني إذا لم أخف ضرراً","I reject in my heart"),0.1,-0.1),(TXT("أسكت عن المنكر حفاظاً على علاقاتي ومصالحي","I remain silent"),-0.2,0.1),(TXT("لا داعي للأمر والنهي فكل إنسان حر","No need for enjoining"),-0.3,-0.3)]},
    {"id":16,"topic":TXT("الوطنية والحزبية والمذهبية","Patriotism, Partisanship, Sectarianism"),"letter":"ف","value":80,
     "text":TXT("في زمن تُقدَّس فيه الوطنية والحزبية والمذهبية، ويُرفع شعار 'الوطن أو الحزب أو المذهب أولاً'، كمسلم: ما هو موقفك؟","In an age of patriotism..."),
     "answers":[(TXT("ولائي للإسلام فوق كل وطن وحزب ومذهب","My loyalty to Islam above all"),0.5,0.5),(TXT("أحب وطني وحزبي ومذهبي لكني أقدّم الإسلام","I love my country but prioritize Islam"),0.1,-0.1),(TXT("انتمائي لوطني أو حزبي أهم من انتمائي للإسلام","National belonging is more important"),-0.2,0.1),(TXT("لا أرى مشكلة في تقديم الوطن أو الحزب على الدين","No problem with nationalism"),-0.4,-0.5)]},
    {"id":17,"topic":TXT("الصلاة في زمن الانشغال","Prayer in an Age of Busyness"),"letter":"ن","value":50,
     "text":TXT("في زمن تزدحم فيه الحياة، وتتسارع فيه الأيام، وأصبحت الصلاة 'عبئاً' على البعض، كمسلم: ما هو موقفك؟","In an age of busyness..."),
     "answers":[(TXT("الصلاة راحتي وقرة عيني ولا أتركها مهما كنت مشغولاً","Prayer is my comfort"),0.5,0.5),(TXT("أصلي لكني أؤخرها أو أستعجل فيها أحياناً","I pray but sometimes delay"),0.1,-0.1),(TXT("أصلي أحياناً وأتركها أحياناً حسب الظروف","I pray sometimes and leave sometimes"),-0.2,0.1),(TXT("لا أجد وقتاً للصلاة وأراها غير عملية","I find no time for prayer"),-0.4,-0.5)]},
    {"id":18,"topic":TXT("الصوم في زمن الشهوات","Fasting in an Age of Desires"),"letter":"ط","value":9,
     "text":TXT("في زمن تحاصر فيه الشهوات الإنسان من كل جانب، وأصبح الصوم 'تقييداً للحرية'، كمسلم: ما هو موقفك؟","In an age of desires..."),
     "answers":[(TXT("أصوم الفرض والنفل وأراه دورة تدريبية على تقوى الله","I fast obligatory and voluntary"),0.5,0.5),(TXT("أصوم الفرض فقط ولا أستطيع صيام النفل","I fast only obligatory"),0.1,-0.1),(TXT("أصوم رمضان كعادة اجتماعية ولا أشعر بروحانيته","I fast Ramadan as a habit"),-0.2,0.1),(TXT("لا أصوم وأرى أن العصر لا يتناسب مع فكرة الصيام","I don't fast"),-0.4,-0.5)]},
    {"id":19,"topic":TXT("الزكاة والصدقة في زمن الأنانية","Zakat & Charity in an Age of Selfishness"),"letter":"ط","value":9,
     "text":TXT("في زمن طغت فيه الأنانية، وضعف فيه التكافل، وأصبح المال 'إلهاً'، كمسلم: ما هو موقفك من الزكاة والصدقة؟","In an age of selfishness..."),
     "answers":[(TXT("أؤدي الزكاة طيبة بها نفسي وأعترف أن المال مال الله","I pay Zakat willingly"),0.5,0.5),(TXT("أؤدي الزكاة فقط وأحياناً أتصدق","I pay only Zakat"),0.1,-0.1),(TXT("أخرج الزكاة بخلاً وأشعر أنها ضريبة","I pay Zakat grudgingly"),-0.2,0.1),(TXT("لا أزكي فالمال مالي ولا دخل لأحد فيه","I don't pay Zakat"),-0.4,-0.5)]},
]

# =============================================
# 5. الشواهد التاريخية
# =============================================
HISTORICAL_DATA = {
    TXT("الخلافة الراشدة (٦٣٢-٦٦١م)", "Rashidun Caliphate (632-661 CE)"): {
        "W": 0.95, "B": 0.95, "E": 0.90,
        "era": TXT("عصر النبوة والراشدين", "Era of Prophethood & Rashidun"),
        "desc": TXT(
            "أعلى فترات التوازن في التاريخ الإسلامي. W و B في ذروتهما. الثبات الذاتي (S ≈ 0.90). "
            "التمكين (E) نتاج طبيعي للثبات، لا فجوة استدراج تُذكر.",
            "Highest balance period in Islamic history. W and B at their peak. Self-sustained stability (S ≈ 0.90). "
            "Empowerment (E) a natural product of stability, no significant Istidraj gap."
        ),
        "lessons": TXT(
            "• الإيمان والبراءة متلازمان في النموذج الراشدي.\n• التمكين يتبع الثبات دون تأخير يُذكر.\n• هذا هو 'العصر الذهبي' الذي يُقاس به.",
            "• Faith and disavowal are intertwined in the Rashidun model.\n• Empowerment follows stability without significant delay.\n• This is the 'golden age' by which others are measured."
        )
    },
    TXT("الدولة الأموية – أوج التوسع (٧٢٠م)", "Umayyad – Peak Expansion (720 CE)"): {
        "W": 0.50, "B": 0.40, "E": 0.95,
        "era": TXT("عصر الفتوحات", "Era of Conquests"),
        "desc": TXT(
            "التمكين (E) في ذروته: الامتداد من الصين إلى فرنسا. لكن W و B بدآ في الانخفاض (ضعف الورع، ظهور العصبية). "
            "فجوة استدراج واضحة: E = 0.95 بينما S = 0.20 فقط. الثبات لم يعد ذاتيًا، بل ممتدًا من رصيد الراشدة.",
            "Empowerment (E) at its peak: stretching from China to France. But W and B began declining (weakening piety, tribal partisanship). "
            "Clear Istidraj gap: E = 0.95 while S = 0.20 only. Stability no longer self-sustained, but extended from Rashidun reserves."
        ),
        "lessons": TXT(
            "• التمكين المادي يمكن أن يستمر لعقود بعد انهيار الثبات.\n• هذه هي 'فجوة الاستدراج' بعينها.\n• الاعتماد على 'رصيد السابقين' دون تجديد يؤدي إلى الانهيار.",
            "• Material empowerment can persist for decades after stability collapses.\n• This is the 'Istidraj gap' in action.\n• Relying on 'predecessor reserves' without renewal leads to collapse."
        )
    },
    TXT("الدولة الأموية – قبل السقوط (٧٤٠م)", "Umayyad – Before Fall (740 CE)"): {
        "W": 0.25, "B": 0.20, "E": 0.70,
        "era": TXT("عصر الفتن والانهيار", "Era of Strife & Collapse"),
        "desc": TXT(
            "انهيار شبه كامل في W (ضعف الإيمان، الظلم، الترف) و B (الانغماس في الدنيا، ترك الجهاد). "
            "E ما زال مرتفعًا نسبيًا (0.70) لكنه آخذ في الانهيار. 'استدراج متقدم' ينذر بالسقوط الوشيك.",
            "Near-total collapse in W (weak faith, injustice, luxury) and B (worldly indulgence, abandoning jihad). "
            "E still relatively high (0.70) but beginning to crumble. 'Advanced Istidraj' warning of imminent fall."
        ),
        "lessons": TXT(
            "• عندما يصل S إلى 0.05، يصبح الانهيار مسألة وقت.\n• E ينهار متأخرًا، لكنه ينهار بعنف.\n• هذا هو قانون 'الاستدراج' الإلهي.",
            "• When S reaches 0.05, collapse is only a matter of time.\n• E collapses late, but violently.\n• This is the divine law of 'Istidraj'."
        )
    },
    TXT("الدولة العباسية – العصر الذهبي (٨٠٠م)", "Abbasid – Golden Age (800 CE)"): {
        "W": 0.80, "B": 0.70, "E": 0.85,
        "era": TXT("عصر العلم والحضارة", "Era of Science & Civilization"),
        "desc": TXT(
            "نهضة علمية وحضارية هائلة (W مرتفع بسبب العلم، B مرتفع بسبب القوة). "
            "S = 0.56، و E = 0.85. فجوة استدراج طفيفة، لكنها تحت السيطرة بسبب تجدد W عبر العلم.",
            "Massive scientific and civilizational renaissance (W high due to knowledge, B high due to power). "
            "S = 0.56, E = 0.85. Slight Istidraj gap, but under control due to W renewal through knowledge."
        ),
        "lessons": TXT(
            "• العلم (ع) يجدد W ويؤخر الانهيار.\n• الحضارة تحتاج إلى 'تجديد مستمر' للإيمان.\n• العصر الذهبي ليس 'استقرارًا' بل 'حركة دائمة'.",
            "• Knowledge renews W and delays collapse.\n• Civilization needs 'continuous renewal' of faith.\n• The golden age is not 'stability' but 'constant motion'."
        )
    },
    TXT("الدولة العثمانية – الذروة (١٥٠٠م)", "Ottoman – Peak (1500 CE)"): {
        "W": 0.75, "B": 0.80, "E": 0.90,
        "era": TXT("عصر القوة والعدل", "Era of Power & Justice"),
        "desc": TXT(
            "ذروة القوة العثمانية: فتح القسطنطينية، نظام العدل (W)، الجيش الإنكشاري (B). "
            "توازن جيد بين W و B. E = 0.90 نتاج طبيعي لـ S = 0.60.",
            "Peak Ottoman power: Conquest of Constantinople, justice system (W), Janissary army (B). "
            "Good balance between W and B. E = 0.90 natural product of S = 0.60."
        ),
        "lessons": TXT(
            "• التوازن بين W و B هو سر القوة.\n• 'القانون العثماني' كان محاولة لتطبيق الشريعة (W).\n• الجيش القوي (B) يحمي هذا التوازن.",
            "• Balance between W and B is the secret of power.\n• 'Ottoman law' was an attempt to apply Sharia (W).\n• A strong army (B) protects this balance."
        )
    },
    TXT("الدولة العثمانية – أواخر (١٨٠٠م)", "Ottoman – Late (1800 CE)"): {
        "W": 0.35, "B": 0.25, "E": 0.60,
        "era": TXT("عصر 'الرجل المريض'", "Era of 'The Sick Man'"),
        "desc": TXT(
            "انهيار W (الفساد، الانفصال عن الشريعة) و B (التبعية للغرب، ضعف الجهاد). "
            "E ما زال 0.60 بسبب 'رصيد' الماضي، لكن الدولة تُعرف بـ 'رجل أوروبا المريض'. فجوة استدراج طويلة.",
            "Collapse of W (corruption, separation from Sharia) and B (dependency on the West, weak jihad). "
            "E still 0.60 due to past 'reserves', but the empire is known as 'The Sick Man of Europe'. Long Istidraj gap."
        ),
        "lessons": TXT(
            "• 'الرجل المريض' هو وصف دقيق لحالة الاستدراج.\n• E يبقى مرتفعًا بسبب 'التراكم' لا بسبب 'الصحة'.\n• الانهيار النهائي (1924) كان حتميًا.",
            "• 'The Sick Man' is an accurate description of the Istidraj state.\n• E remains high due to 'accumulation', not 'health'.\n• The final collapse (1924) was inevitable."
        )
    },
    TXT("الاتحاد السوفيتي (١٩٢٢-١٩٩١م)", "Soviet Union (1922-1991 CE)"): {
        "W": 0.05, "B": 0.10, "E": 0.70,
        "era": TXT("عصر الإلحاد الشيوعي", "Era of Communist Atheism"),
        "desc": TXT(
            "W = صفر تقريبًا (إلحاد رسمي). B ضعيف (جيش قوي لكن بلا روح). "
            "E = 0.70 (قوة عظمى ظاهريًا). انهيار مفاجئ وغير متوقع 'كالصاعقة' عام 1991. "
            "أعظم مثال على 'الاستدراج' في التاريخ الحديث.",
            "W ≈ 0 (official atheism). B weak (strong army but soulless). "
            "E = 0.70 (superpower on the surface). Sudden, unexpected collapse 'like lightning' in 1991. "
            "The greatest modern example of 'Istidraj'."
        ),
        "lessons": TXT(
            "• دولة بلا W تنهار فجأة مهما بلغت قوتها.\n• 'الاستدراج' الإلهي يسري على المسلم والكافر.\n• ﴿فَلَمَّا نَسُوا مَا ذُكِّرُوا بِهِ فَتَحْنَا عَلَيْهِمْ أَبْوَابَ كُلِّ شَيْءٍ﴾",
            "• A state without W collapses suddenly, however powerful.\n• Divine 'Istidraj' applies to believer and disbeliever alike.\n• ﴿So when they forgot that by which they had been reminded, We opened to them the doors of every thing.﴾"
        )
    },
}
