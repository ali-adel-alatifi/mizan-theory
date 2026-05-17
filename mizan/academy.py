# mizan/academy.py
"""
جامعة الميزان المفتوحة - دورات تفاعلية في نظرية الدين القيم
"""

import streamlit as st
from config import TXT
from utils import export_session_data, import_session_data

# =============================================
# 1. بيانات الدورات
# =============================================
COURSES = [
    {
        "id": "basics",
        "title": TXT("الدورة ١: ما هي نظرية الميزان؟", "Course 1: What is the Mizan Theory?"),
        "desc": TXT("تعرف على القانون الواحد الذي يحكم الذرة والحضارة.", "Learn the one law governing atom and civilization."),
        "lessons": [
            {"title": TXT("الدرس ١: أزمة الإنسان المعاصر", "Lesson 1: The Modern Human Crisis"), "content": TXT("لماذا نعيش القلق رغم التقدم؟ لأننا فقدنا 'الدين القيم'.", "Why anxiety despite progress? We lost 'Al-Deen Al-Qayyim'.")},
            {"title": TXT("الدرس ٢: معادلة الثبات S = W x B", "Lesson 2: The Stability Equation"), "content": TXT("W = الولاء لله. B = البراءة من الطاغوت. S = الثبات.", "W = Loyalty to Allah. B = Disavowal of Taghut. S = Stability.")},
            {"title": TXT("الدرس ٣: لماذا ضرب لا جمع؟", "Lesson 3: Why Multiply, Not Add?"), "content": TXT("لأن القلب لا يجتمع فيه ولاءان. إن نقص أحدهما انهار الثبات.", "A heart can't hold two loyalties. If one fails, stability collapses.")},
        ],
        "test_question": TXT("ما هي معادلة الثبات؟", "What is the stability equation?"),
        "test_options": ["S = W + B", "S = W - B", "S = W x B", "S = W / B"],
        "test_answer": 2,
    },
    {
        "id": "loyalty",
        "title": TXT("الدورة ٢: الولاء والبراء في حياتي", "Course 2: Loyalty & Disavowal in My Life"),
        "desc": TXT("كيف تطبق المعادلة في علاقاتك اليومية.", "Apply the equation in your daily life."),
        "lessons": [
            {"title": TXT("الدرس ١: من هو وليك؟", "Lesson 1: Who is Your Ally?"), "content": TXT("وليك هو من تنصره بمالك ولسانك وقلبك. المؤمنون أولياء بعض.", "Your ally is whom you support. Believers are allies of one another.")},
            {"title": TXT("الدرس ٢: ما هو الطاغوت؟", "Lesson 2: What is Taghut?"), "content": TXT("كل ما تجاوز حده من معبود أو متبوع أو مطاع في غير طاعة الله.", "Anything transgressing limits: worshipped, followed, obeyed besides Allah.")},
            {"title": TXT("الدرس ٣: البراءة العملية", "Lesson 3: Practical Disavowal"), "content": TXT("ليست كراهية قلبية فقط، بل موقف: لا أشاركهم شعائرهم، لا أتخذهم بطانة.", "Not just hatred, but a stance: don't share their rituals, don't take them as confidants.")},
        ],
        "test_question": TXT("من هو الطاغوت؟", "Who is Taghut?"),
        "test_options": [TXT("كل معبود من دون الله", "Any worshipped besides Allah"), TXT("فقط الأصنام", "Only idols"), TXT("فقط الحكام الظلمة", "Only unjust rulers"), TXT("لا يوجد طاغوت اليوم", "No Taghut today")],
        "test_answer": 0,
    },
    {
        "id": "change",
        "title": TXT("الدورة ٣: كيف أغير العالم بالميزان؟", "Course 3: How to Change the World with Mizan?"),
        "desc": TXT("من الفرد إلى الأمة: خارطة طريق النهضة.", "From individual to nation: a roadmap."),
        "lessons": [
            {"title": TXT("الدرس ١: ابدأ بنفسك", "Lesson 1: Start with Yourself"), "content": TXT("أصلح ما بينك وبين الله. أقم الصلاة، جدد التوبة، راقب قلبك.", "Fix your relationship with Allah. Pray, repent, watch your heart.")},
            {"title": TXT("الدرس ٢: ابنِ أسرتك", "Lesson 2: Build Your Family"), "content": TXT("الأسرة هي الخلية الأولى. اختر زوجك على الدين، ربِّ أبناءك.", "The family is the first cell. Choose a spouse for faith, raise your children.")},
            {"title": TXT("الدرس ٣: انهض بأمتك", "Lesson 3: Uplift Your Nation"), "content": TXT("بالعلم النافع، والاقتصاد العادل، والجهاد في سبيل الله.", "Through beneficial knowledge, just economy, and jihad for Allah.")},
        ],
        "test_question": TXT("أين تبدأ النهضة؟", "Where does revival start?"),
        "test_options": [TXT("من الحاكم", "From the ruler"), TXT("من الفرد", "From the individual"), TXT("من الاقتصاد", "From the economy"), TXT("من التعليم", "From education")],
        "test_answer": 1,
    },
]

# =============================================
# 2. واجهة الجامعة
# =============================================
def render_academy():
    """عرض جامعة الميزان المفتوحة."""
    st.header("🎓 جامعة الميزان المفتوحة")
    st.markdown(TXT(
        "### ﴿فَاعْلَمْ أَنَّهُ لَا إِلَٰهَ إِلَّا اللَّهُ وَاسْتَغْفِرْ لِذَنبِكَ﴾",
        "### Know that there is no deity except Allah and ask forgiveness for your sin."
    ))
    st.caption(TXT(
        "دورات قصيرة لتعلم نظرية الدين القيم. اختر دورة، وأكمل دروسها، واختبر نفسك.",
        "Short courses to learn the theory. Choose, complete lessons, and test yourself."
    ))

    # تهيئة الجلسة
    if "academy_progress" not in st.session_state:
        st.session_state.academy_progress = {}
    if "academy_certificates" not in st.session_state:
        st.session_state.academy_certificates = []

    # اختيار دورة
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

        # زر العودة
        if st.button(TXT("🔙 العودة للدورات", "🔙 Back to Courses")):
            st.session_state.selected_course = None
            st.rerun()

        st.subheader(course["title"])

        # إذا لم يكمل الدورة
        if not progress.get("completed", False):
            lesson_idx = progress.get("current_lesson", 0)
            if lesson_idx < len(course["lessons"]):
                lesson = course["lessons"][lesson_idx]
                st.markdown(f"### {lesson['title']}")
                st.info(lesson["content"])

                col1, col2 = st.columns(2)
                with col1:
                    if lesson_idx > 0:
                        if st.button(TXT("⬅️ الدرس السابق", "⬅️ Previous")):
                            progress["current_lesson"] -= 1
                            st.session_state.academy_progress[course_id] = progress
                            st.rerun()
                with col2:
                    if st.button(TXT("➡️ الدرس التالي", "➡️ Next")):
                        progress["current_lesson"] += 1
                        st.session_state.academy_progress[course_id] = progress
                        st.rerun()
            else:
                # انتهت الدروس، نعرض الاختبار
                st.markdown("---")
                st.subheader(TXT("📝 اختبار الدورة", "📝 Course Test"))
                st.markdown(course["test_question"])
                ans = st.radio(TXT("اختر الإجابة:", "Choose:"), course["test_options"], key=f"test_{course_id}")
                if st.button(TXT("✅ تحقق من الإجابة", "✅ Check Answer"), type="primary"):
                    if course["test_options"].index(ans) == course["test_answer"]:
                        st.success(TXT("🎉 إجابة صحيحة! أحسنت.", "🎉 Correct! Well done."))
                        progress["completed"] = True
                        progress["score"] = 1
                        st.session_state.academy_progress[course_id] = progress
                        st.session_state.academy_certificates.append(course["title"])
                        st.rerun()
                    else:
                        st.error(TXT("❌ إجابة خاطئة. حاول مرة أخرى.", "❌ Wrong. Try again."))

        # إذا أكمل الدورة
        else:
            st.success(TXT("🎓 لقد أكملت هذه الدورة بنجاح!", "🎓 You have completed this course!"))
            st.balloons()
            st.markdown(TXT("### 📜 شهادتك:", "### 📜 Your Certificate:"))
            st.markdown(f"**{course['title']}**")
            st.caption(TXT("مقدم من جامعة الميزان المفتوحة", "Awarded by Mizan Open University"))

    # عرض الشهادات
    if st.session_state.academy_certificates:
        st.markdown("---")
        st.subheader(TXT("🏆 شهاداتك", "🏆 Your Certificates"))
        for cert in st.session_state.academy_certificates:
            st.markdown(f"- ✅ {cert}")

    # أزرار الحفظ والتحميل
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
