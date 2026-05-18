# mizan/healer.py
"""
طبيب القلوب - المختبر الشخصي الذكي
يحاور المستخدم، يشخص موقعه، ويعطيه روشتة علاجية
"""

import streamlit as st
from config import TXT

# =============================================
# 1. الأسئلة الذكية للمرشد الروحي
# =============================================
HEALER_QUESTIONS = [
    {"id": "mood", "text": TXT("كيف تشعر اليوم؟", "How do you feel today?"),
     "options": [TXT("مطمئن", "At peace"), TXT("قلق", "Anxious"), TXT("حزين", "Sad"), TXT("غاضب", "Angry")]},
    {"id": "prayer", "text": TXT("كيف هي صلاتك؟", "How is your prayer?"),
     "options": [TXT("أقيمها بخشوع", "I pray with devotion"), TXT("أصلي لكن بفتور", "I pray but weakly"), TXT("أصلي أحياناً", "I pray sometimes"), TXT("لا أصلي", "I don't pray")]},
    {"id": "sins", "text": TXT("ما أكثر ما يثقل قلبك؟", "What burdens your heart most?"),
     "options": [TXT("الشهوات", "Lusts"), TXT("الغضب", "Anger"), TXT("الحسد", "Envy"), TXT("حب الدنيا", "Love of world")]},
    {"id": "company", "text": TXT("من تصاحب أكثر وقتك؟", "Who do you spend most time with?"),
     "options": [TXT("الصالحين", "The righteous"), TXT("العائلة", "Family"), TXT("أصدقاء عاديون", "Ordinary friends"), TXT("وحيد", "Alone")]},
    {"id": "quran", "text": TXT("كم تقرأ القرآن؟", "How much Quran do you read?"),
     "options": [TXT("يومياً", "Daily"), TXT("أسبوعياً", "Weekly"), TXT("نادراً", "Rarely"), TXT("لا أقرأ", "Never")]},
]

# =============================================
# 2. روشتات علاجية (مكتبة الأدوية الروحية)
# =============================================
HEALING_PRESCRIPTIONS = {
    "الشهوات": {
        "diagnosis": TXT("ضعف في البراءة (B). الطاغوت الداخلي (الهوى) يسيطر.", "Weakness in B. Internal Taghut dominates."),
        "verses": ["﴿وَأَمَّا مَنْ خَافَ مَقَامَ رَبِّهِ وَنَهَى النَّفْسَ عَنِ الْهَوَىٰ﴾ [النازعات: ٤٠]", "﴿وَلَا تَتَّبِعِ الْهَوَىٰ فَيُضِلَّكَ عَن سَبِيلِ اللَّهِ﴾ [ص: ٢٦]"],
        "hadith": TXT("«حُفَّتِ الْجَنَّةُ بِالْمَكَارِهِ وَحُفَّتِ النَّارُ بِالشَّهَوَاتِ» [متفق عليه]", "Paradise is surrounded by hardships..."),
        "action": TXT("صم ٣ أيام هذا الأسبوع. كلما هاجتك شهوة، استعذ بالله وقل: 'اللهم إني أسألك حبك وحب من يحبك'.", "Fast 3 days this week."),
    },
    "الغضب": {
        "diagnosis": TXT("ضعف في الولاء (W). الغضب يطفئ نور الإيمان.", "Weakness in W. Anger extinguishes faith."),
        "verses": ["﴿وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ﴾ [آل عمران: ١٣٤]"],
        "hadith": TXT("«لَيْسَ الشَّدِيدُ بِالصُّرَعَةِ، إِنَّمَا الشَّدِيدُ الَّذِي يَمْلِكُ نَفْسَهُ عِنْدَ الْغَضَبِ» [متفق عليه]", "The strong is not the one who overcomes..."),
        "action": TXT("توضأ فوراً عند الغضب. قل: 'أعوذ بالله من الشيطان الرجيم'. اجلس إن كنت قائماً.", "Perform ablution when angry."),
    },
    "الحسد": {
        "diagnosis": TXT("ضعف في البراءة (B). الحسد اعتراض على قسمة الله.", "Weakness in B. Envy is objection to Allah's decree."),
        "verses": ["﴿أَمْ يَحْسُدُونَ النَّاسَ عَلَىٰ مَا آتَاهُمُ اللَّهُ مِن فَضْلِهِ﴾ [النساء: ٥٤]"],
        "hadith": TXT("«لَا تَحَاسَدُوا وَلَا تَقَاطَعُوا...» [مسلم]", "Do not envy one another..."),
        "action": TXT("ادعُ لمن تحسده كل يوم: 'اللهم بارك له وزده من فضلك'.", "Pray for the one you envy daily."),
    },
    "حب الدنيا": {
        "diagnosis": TXT("ضعف في الولاء (W). التعلق بالدنيا يضعف التعلق بالله.", "Weakness in W. Attachment to world weakens faith."),
        "verses": ["﴿وَمَا الْحَيَاةُ الدُّنْيَا إِلَّا مَتَاعُ الْغُرُورِ﴾ [آل عمران: ١٨٥]"],
        "hadith": TXT("«ازْهَدْ فِي الدُّنْيَا يُحِبَّكَ اللَّهُ» [ابن ماجه]", "Renounce the world and Allah will love you."),
        "action": TXT("تصدق كل يوم بشيء ولو يسير. قل: 'اللهم لا تجعل الدنيا أكبر همنا'.", "Give charity daily."),
    },
}

# =============================================
# 3. المحلل الشخصي الذكي
# =============================================
def render_healer():
    """عرض طبيب القلوب التفاعلي."""
    st.header("🩺 طبيب القلوب – المختبر الشخصي الذكي")
    st.markdown(TXT(
        "### مرحباً بك. أنا مرشدك الروحي. دعني أسألك بعض الأسئلة لأفهم حالك، ثم أصف لك الدواء.",
        "### Welcome. I am your spiritual guide. Let me ask you a few questions."
    ))

    # تهيئة الجلسة
    if "healer_answers" not in st.session_state:
        st.session_state.healer_answers = {}
    if "healer_done" not in st.session_state:
        st.session_state.healer_done = False

    # إذا لم يكتمل التشخيص
    if not st.session_state.healer_done:
        for q in HEALER_QUESTIONS:
            ans = st.radio(
                f"**{q['text']}**",
                q["options"],
                key=q["id"],
                index=None
            )
            if ans:
                st.session_state.healer_answers[q["id"]] = ans

        if len(st.session_state.healer_answers) == len(HEALER_QUESTIONS):
            if st.button(TXT("🔍 شخّص حالتي", "🔍 Diagnose Me"), type="primary"):
                st.session_state.healer_done = True
                st.rerun()

    # بعد اكتمال التشخيص
    else:
        # تحديد المشكلة الرئيسية
        main_issue = st.session_state.healer_answers.get("sins", "الشهوات")
        if main_issue not in HEALING_PRESCRIPTIONS:
            main_issue = "الشهوات"

        pres = HEALING_PRESCRIPTIONS[main_issue]

        # عرض التشخيص
        st.markdown("---")
        st.subheader(TXT("📋 التشخيص", "📋 Diagnosis"))
        st.warning(pres["diagnosis"])

        # محاكاة حساب الموقع (تبسيطي)
        mood_map = {"مطمئن": 0.8, "At peace": 0.8, "قلق": 0.3, "Anxious": 0.3, "حزين": 0.2, "Sad": 0.2, "غاضب": 0.1, "Angry": 0.1}
        prayer_map = {"أقيمها بخشوع": 1.0, "I pray with devotion": 1.0, "أصلي لكن بفتور": 0.5, "I pray but weakly": 0.5, "أصلي أحياناً": 0.2, "I pray sometimes": 0.2, "لا أصلي": -0.8, "I don't pray": -0.8}
        company_map = {"الصالحين": 0.8, "The righteous": 0.8, "العائلة": 0.5, "Family": 0.5, "أصدقاء عاديون": 0.0, "Ordinary friends": 0.0, "وحيد": -0.3, "Alone": -0.3}
        quran_map = {"يومياً": 1.0, "Daily": 1.0, "أسبوعياً": 0.5, "Weekly": 0.5, "نادراً": 0.1, "Rarely": 0.1, "لا أقرأ": -0.5, "Never": -0.5}

        w_raw = (mood_map.get(st.session_state.healer_answers.get("mood", ""), 0.3) +
                 prayer_map.get(st.session_state.healer_answers.get("prayer", ""), 0.3) +
                 company_map.get(st.session_state.healer_answers.get("company", ""), 0.3) +
                 quran_map.get(st.session_state.healer_answers.get("quran", ""), 0.3)) / 4
        w_raw = max(-1.0, min(1.0, w_raw * 2 - 1))

        b_raw = 0.5  # تقدير متوسط
        S_score = ((w_raw + 1) / 2) * ((b_raw + 1) / 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("W (الولاء)", f"{w_raw:+.2f}")
        col2.metric("B (البراءة)", f"{b_raw:+.2f}")
        col3.metric("S (الثبات)", f"{S_score:.2f}")

        # عرض الروشتة العلاجية
        st.markdown("---")
        st.subheader("💊 الروشتة العلاجية")
        st.markdown("### 📖 آيات للتدبر:")
        for v in pres["verses"]:
            st.markdown(f"- {v}")
        st.markdown(f"### 🕋 حديث شريف:\n{pres['hadith']}")
        st.markdown(f"### 🏃 خطة عملية:\n{pres['action']}")

        # زر إعادة
        if st.button(TXT("🔄 إعادة التشخيص", "🔄 Re-diagnose")):
            st.session_state.healer_answers = {}
            st.session_state.healer_done = False
            st.rerun()
