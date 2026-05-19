# mizan/academy.py
"""
جامعة الميزان المفتوحة
دورات تفاعلية قصيرة في نظرية الدين القيم والإسلام الحنيف
"""

import streamlit as st
from config import TXT
from utils import export_session_data, import_session_data

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
# 1. بيانات الدورات الثلاث
# =============================================
COURSES = [
    # ... (نفس البيانات الموجودة في ملفك الأصلي)
]

# =============================================
# 2. واجهة الجامعة
# =============================================
def render_academy():
    """عرض جامعة الميزان المفتوحة."""
    
    # === تطبيق الحل أولاً ===
    fix_rtl_display()

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

        if st.button(TXT("🔙 العودة للدورات", "🔙 Back to Courses")):
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
                st.markdown("---")
                st.subheader(TXT("📝 اختبار الدورة", "📝 Course Test"))
                st.markdown(course["test_question"])
                ans = st.radio(TXT("اختر الإجابة:", "Choose:"), course["test_options"], key=f"test_{course_id}")
                if st.button(TXT("✅ تحقق من الإجابة", "✅ Check Answer"), type="primary"):
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
