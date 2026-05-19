# mizan/academy.py
"""
جامعة الميزان المفتوحة
دورات تفاعلية قصيرة في نظرية الدين القيم والإسلام الحنيف
"""

import streamlit as st
from config import TXT
from utils import export_session_data, import_session_data

# =============================================
# 1. بيانات الدورات الثلاث
# =============================================
COURSES = [
    {
        "id": "basics",
        "title": TXT("الدورة ١: ما هي نظرية الميزان؟", "Course 1: What is the Mizan Theory?"),
        "desc": TXT(
            "اكتشف القانون الواحد الذي يحكم الذرة والحضارة والقلب البشري.",
            "Discover the one law governing the atom, civilization, and the human heart."
        ),
        "lessons": [
            {
                "title": TXT("الدرس ١: أزمة الإنسان المعاصر", "Lesson 1: The Modern Human Crisis"),
                "content": TXT(
                    "لماذا نعيش القلق رغم التقدم؟ لأننا فقدنا 'الدين القيم'، ذلك القانون الذي فطر الله عليه الخلق. "
                    "كل شيء حولك يسير بنظام دقيق: الذرة، الخلية، المجرة... إلا الإنسان حين يختار أن يعيش خارج هذا النظام. "
                    "هذا المختبر هو محاولة لإعادة اكتشاف هذا النظام.",
                    "Why do we live in anxiety despite progress? Because we lost 'Al-Deen Al-Qayyim', "
                    "the law upon which Allah created everything. Everything around you runs by precise order: "
                    "the atom, the cell, the galaxy... except humans when they choose to live outside this system. "
                    "This lab is an attempt to rediscover this system."
                )
            },
            {
                "title": TXT("الدرس ٢: معادلة الثبات S = W × B", "Lesson 2: The Stability Equation"),
                "content": TXT(
                    "في قلب هذا النظام، توجد معادلة بسيطة في شكلها، عميقة في أثرها: **S = W × B**. "
                    "**W (الولاء لله وأوليائه):** قوة الجذب نحو الحق. **B (البراءة من الطاغوت وأوليائه):** قوة التنافر عن الباطل. "
                    "**S (الثبات الوجودي):** هو حاصل ضربهما معاً. إنها علاقة ضرب لا جمع، لأن القلب لا يجتمع فيه ولاءان.",
                    "At the heart of this system lies an equation simple in form, deep in impact: **S = W × B**. "
                    "**W (Loyalty to Allah and His allies):** The force of attraction to truth. "
                    "**B (Disavowal of Taghut and its allies):** The force of repulsion from falsehood. "
                    "**S (Existential Stability):** Their product. It's multiplication, not addition, because a heart cannot hold two loyalties."
                )
            },
            {
                "title": TXT("الدرس ٣: لماذا ضرب لا جمع؟", "Lesson 3: Why Multiply, Not Add?"),
                "content": TXT(
                    "تأمل قوله تعالى: ﴿مَا جَعَلَ اللَّهُ لِرَجُلٍ مِّنْ قَلْبَيْنِ فِي جَوْفِهِ﴾. "
                    "القلب لا يمكنه أن يكون مخلصاً لله ومطيعاً للشيطان في آن واحد. "
                    "إذا كان W=0 (لا ولاء) أو B=0 (لا براءة)، فإن S=0 (ينهار الثبات). "
                    "لهذا يسقط المنافق، ولهذا يفشل المتردد، ولهذا ينتصر المؤمن الصادق.",
                    "Reflect on Allah's words: ﴿Allah has not made for any man two hearts in his chest.﴾ "
                    "A heart cannot be sincere to Allah and obedient to Satan at the same time. "
                    "If W=0 (no loyalty) or B=0 (no disavowal), then S=0 (stability collapses). "
                    "This is why the hypocrite falls, the hesitant fails, and the sincere believer triumphs."
                )
            },
        ],
        "test_question": TXT("ما هي معادلة الثبات؟", "What is the stability equation?"),
        "test_options": ["S = W + B", "S = W - B", "S = W × B", "S = W / B"],
        "test_answer": 2,
    },
    {
        "id": "loyalty",
        "title": TXT("الدورة ٢: الولاء والبراء في حياتي", "Course 2: Loyalty & Disavowal in My Life"),
        "desc": TXT(
            "كيف تطبق المعادلة في علاقاتك اليومية واختياراتك المصيرية.",
            "How to apply the equation in your daily relationships and life choices."
        ),
        "lessons": [
            {
                "title": TXT("الدرس ١: من هو وليك؟", "Lesson 1: Who is Your Ally?"),
                "content": TXT(
                    "وليك هو من تنصره بمالك ولسانك وقلبك. هو من تفرح لفرحه وتحزن لحزنه. "
                    "قال تعالى: ﴿إِنَّمَا وَلِيُّكُمُ اللَّهُ وَرَسُولُهُ وَالَّذِينَ آمَنُوا﴾. "
                    "ولاؤك لله يظهر في طاعته، ولاؤك للرسول في اتباعه، ولاؤك للمؤمنين في حبهم ونصرتهم.",
                    "Your ally is whom you support with your wealth, tongue, and heart. "
                    "Allah says: ﴿Your ally is none but Allah, His Messenger, and the believers.﴾ "
                    "Your loyalty to Allah appears in obeying Him, to the Messenger in following him, "
                    "and to the believers in loving and supporting them."
                )
            },
            {
                "title": TXT("الدرس ٢: ما هو الطاغوت؟", "Lesson 2: What is Taghut?"),
                "content": TXT(
                    "الطاغوت هو كل ما تجاوز به العبد حده من معبود أو متبوع أو مطاع في غير طاعة الله. "
                    "قد يكون شيطاناً، أو حاكماً جائراً، أو عالماً محرفاً، أو كاهناً، أو حتى هوى نفسك إذا اتبعته في معصية الله. "
                    "قال تعالى: ﴿أَفَرَأَيْتَ مَنِ اتَّخَذَ إِلَٰهَهُ هَوَاهُ﴾.",
                    "Taghut is anything that transgresses its limits: worshipped, followed, or obeyed besides Allah. "
                    "It may be a devil, a tyrant ruler, a corrupt scholar, a fortune-teller, or even your own desire if you follow it in disobeying Allah. "
                    "Allah says: ﴿Have you seen the one who takes his own desire as his god?﴾"
                )
            },
            {
                "title": TXT("الدرس ٣: البراءة العملية", "Lesson 3: Practical Disavowal"),
                "content": TXT(
                    "البراءة ليست كراهية قلبية فقط. إنها موقف. لا أشاركهم شعائرهم. لا أتخذهم بطانة. "
                    "لا أستحسن ما هم عليه. ثم ترتقي إلى الجهاد باللسان واليد بحسب الاستطاعة. "
                    "قال إبراهيم: ﴿إِنَّنِي بَرَاءٌ مِّمَّا تَعْبُدُونَ﴾، وأعلنها جهاراً.",
                    "Disavowal is not just hatred in the heart. It's a stance. I don't share their rituals. I don't take them as confidants. "
                    "I don't approve of their ways. Then it rises to striving with tongue and hand according to ability. "
                    "Abraham said: ﴿I am disassociated from what you worship﴾, and he declared it openly."
                )
            },
        ],
        "test_question": TXT("من هو الطاغوت؟", "Who is Taghut?"),
        "test_options": [
            TXT("كل ما عُبد من دون الله", "Anything worshipped besides Allah"),
            TXT("فقط الأصنام", "Only idols"),
            TXT("فقط الحكام الظلمة", "Only unjust rulers"),
            TXT("لا يوجد طاغوت اليوم", "No Taghut today")
        ],
        "test_answer": 0,
    },
    {
        "id": "change",
        "title": TXT("الدورة ٣: كيف أغير العالم بالميزان؟", "Course 3: How to Change the World with Mizan?"),
        "desc": TXT(
            "من الفرد إلى الأمة: خارطة طريق النهضة.",
            "From the individual to the nation: a roadmap for revival."
        ),
        "lessons": [
            {
                "title": TXT("الدرس ١: ابدأ بنفسك", "Lesson 1: Start with Yourself"),
                "content": TXT(
                    "قال تعالى: ﴿إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ﴾. "
                    "النهضة لا تبدأ من الحاكم ولا من النظام. تبدأ من قلبك أنت. "
                    "أصلح ما بينك وبين الله. أقم الصلاة بخشوع. جدد التوبة كل يوم. راقب قلبك. "
                    "فإذا صلح الفرد، صلحت الأسرة، وصلح المجتمع، وصلحت الأمة.",
                    "Allah says: ﴿Indeed, Allah will not change the condition of a people until they change what is in themselves.﴾ "
                    "Revival does not start from the ruler or the system. It starts from your own heart. "
                    "Fix what is between you and Allah. Establish prayer with devotion. Renew repentance daily. Watch your heart. "
                    "When the individual is reformed, the family is reformed, society is reformed, and the nation is reformed."
                )
            },
            {
                "title": TXT("الدرس ٢: ابنِ أسرتك", "Lesson 2: Build Your Family"),
                "content": TXT(
                    "الأسرة هي الخلية الأولى في جسد الأمة. اختر زوجك على الدين والخلق. "
                    "ربِّ أبناءك على حب الله ورسوله. اجعل بيتك مدرسة للولاء والبراءة. "
                    "قال تعالى: ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا قُوا أَنفُسَكُمْ وَأَهْلِيكُمْ نَارًا﴾.",
                    "The family is the first cell in the body of the Ummah. Choose your spouse for faith and character. "
                    "Raise your children on the love of Allah and His Messenger. Make your home a school for loyalty and disavowal. "
                    "Allah says: ﴿O you who believe, protect yourselves and your families from a Fire.﴾"
                )
            },
            {
                "title": TXT("الدرس ٣: انهض بأمتك", "Lesson 3: Uplift Your Nation"),
                "content": TXT(
                    "بالعلم النافع، والاقتصاد العادل، والإعلام الهادف، والجهاد في سبيل الله. "
                    "كل واحد منا يستطيع أن يخدم أمته في مجال تخصصه. العالم بعلمه، والتاجر بماله، "
                    "والمهندس ببنائه، والطبيب بعلاجه. حين تتحد الجهود على أساس من الولاء لله، تنهض الأمة.",
                    "Through beneficial knowledge, a just economy, purposeful media, and striving in the path of Allah. "
                    "Each of us can serve the Ummah in their field. The scholar with their knowledge, the merchant with their wealth, "
                    "the engineer with their building, the doctor with their healing. When efforts unite on the basis of loyalty to Allah, the Ummah rises."
                )
            },
        ],
        "test_question": TXT("أين تبدأ النهضة الحقيقية؟", "Where does true revival begin?"),
        "test_options": [
            TXT("من الحاكم", "From the ruler"),
            TXT("من الفرد", "From the individual"),
            TXT("من الاقتصاد", "From the economy"),
            TXT("من التعليم", "From education")
        ],
        "test_answer": 1,
    },
]

# =============================================
# 2. واجهة الجامعة
# =============================================
def render_academy():
    """عرض جامعة الميزان المفتوحة."""
    
    st.header(TXT("🎓 جامعة الميزان المفتوحة", "🎓 Mizan Open University"))
    st.markdown(TXT(
        """
        ### ﴿فَاعْلَمْ أَنَّهُ لَا إِلَٰهَ إِلَّا اللَّهُ وَاسْتَغْفِرْ لِذَنبِكَ﴾
        هذه دورات قصيرة لتعلم نظرية الدين القيم. لا تحتاج إلى شهادة، بل إلى قلب مفتوح. 
        اختر دورة، وأكمل دروسها، واختبر نفسك. كل خطوة تخطوها تقربك من النور.
        """,
        """
        ### ﴿Know that there is no deity except Allah and ask forgiveness for your sin.﴾
        These are short courses to learn the theory of Al-Deen Al-Qayyim. You need no certificate, only an open heart. 
        Choose a course, complete its lessons, and test yourself. Every step you take brings you closer to the light.
        """
    ))

    # تهيئة الجلسة
    if "academy_progress" not in st.session_state:
        st.session_state.academy_progress = {}
    if "academy_certificates" not in st.session_state:
        st.session_state.academy_certificates = []

    if "selected_course" not in st.session_state:
        st.session_state.selected_course = None

    # عرض قائمة الدورات
    if not st.session_state.selected_course:
        st.subheader(TXT("📚 الدورات المتاحة", "📚 Available Courses"))
        for i, course in enumerate(COURSES):
            with st.expander(f"**{course['title']}**"):
                st.markdown(course["desc"])
                progress = st.session_state.academy_progress.get(course["id"], {})
                completed = progress.get("completed", False)
                if completed:
                    st.success(TXT("✅ مكتملة", "✅ Completed"))
                if st.button(TXT("▶️ ابدأ الدورة", "▶️ Start Course"), key=f"start_{course['id']}"):
                    st.session_state.selected_course = course["id"]
                    if course["id"] not in st.session_state.academy_progress:
                        st.session_state.academy_progress[course["id"]] = {"current_lesson": 0, "completed": False, "score": 0}
                    st.rerun()

    # عرض محتوى الدورة المختارة
    else:
        course_id = st.session_state.selected_course
        course = next(c for c in COURSES if c["id"] == course_id)
        progress = st.session_state.academy_progress.get(course_id, {"current_lesson": 0, "completed": False, "score": 0})

        if st.button(TXT("🔙 العودة للدورات", "🔙 Back to Courses"), key="btn_back_to_courses"):
            st.session_state.selected_course = None
            st.rerun()

        st.subheader(course["title"])

        if not progress.get("completed", False):
            lesson_idx = progress.get("current_lesson", 0)
            if lesson_idx < len(course["lessons"]):
                lesson = course["lessons"][lesson_idx]
                st.markdown(f"### {lesson['title']}")
                st.info(lesson["content"])

                col1, col2 = st.columns(2)
                with col1:
                    if lesson_idx > 0:
                        if st.button(TXT("⬅️ الدرس السابق", "⬅️ Previous"), key="btn_prev_lesson"):
                            progress["current_lesson"] -= 1
                            st.session_state.academy_progress[course_id] = progress
                            st.rerun()
                with col2:
                    if st.button(TXT("➡️ الدرس التالي", "➡️ Next"), key="btn_next_lesson"):
                        progress["current_lesson"] += 1
                        st.session_state.academy_progress[course_id] = progress
                        st.rerun()
            else:
                st.markdown("---")
                st.subheader(TXT("📝 اختبار الدورة", "📝 Course Test"))
                st.markdown(course["test_question"])
                ans = st.radio(TXT("اختر الإجابة:", "Choose:"), course["test_options"], key=f"test_{course_id}")
                if st.button(TXT("✅ تحقق من الإجابة", "✅ Check Answer"), key="btn_check_answer", type="primary"):
                    if course["test_options"].index(ans) == course["test_answer"]:
                        st.success(TXT("🎉 إجابة صحيحة! أحسنت.", "🎉 Correct! Well done."))
                        st.balloons()
                        progress["completed"] = True
                        progress["score"] = 1
                        st.session_state.academy_progress[course_id] = progress
                        st.session_state.academy_certificates.append(course["title"])
                        st.rerun()
                    else:
                        st.error(TXT("❌ إجابة خاطئة. حاول مرة أخرى.", "❌ Wrong. Try again."))

        else:
            st.success(TXT("🎓 لقد أكملت هذه الدورة بنجاح!", "🎓 You have completed this course!"))
            st.markdown(TXT("### 📜 شهادتك:", "### 📜 Your Certificate:"))
            st.markdown(f"**{course['title']}**")
            st.caption(TXT("مقدم من جامعة الميزان المفتوحة", "Awarded by Mizan Open University"))

    # عرض الشهادات
    if st.session_state.academy_certificates:
        st.markdown("---")
        st.subheader(TXT("🏆 شهاداتك", "🏆 Your Certificates"))
        for cert in st.session_state.academy_certificates:
            st.markdown(f"- ✅ {cert}")

    # أزرار الحفظ والتحميل (مع مفاتيح فريدة)
    st.markdown("---")
    st.subheader(TXT("💾 حفظ/استعادة تقدمك", "💾 Save/Restore Your Progress"))
    col_save, col_load = st.columns(2)
    with col_save:
        export_session_data(
            {
                "academy_progress": st.session_state.get("academy_progress", {}),
                "academy_certificates": st.session_state.get("academy_certificates", [])
            },
            "mizan_academy"
        )
    with col_load:
        import_session_data(["academy_progress", "academy_certificates"])

    # مكتبة المصادر
    st.markdown("---")
    st.subheader(TXT("📚 مكتبة المصادر", "📚 Resource Library"))
    st.markdown(f"""
    - {TXT("📖 الملحق (أ): الآيات الجامعات للنظرية", "📖 Appendix A: Key Verses")}
    - {TXT("📖 الملحق (ب): المفاتيح اللغوية", "📖 Appendix B: Linguistic Keys")}
    - {TXT("📖 الملحق (ج): الدورة الإلهية المحكمة", "📖 Appendix C: Divine Cycle")}
    - {TXT("📖 الملحق (د): الميزان الذهبي", "📖 Appendix D: Golden Criterion")}
    """)
