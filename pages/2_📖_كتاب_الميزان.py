import streamlit as st

st.set_page_config(page_title="كتاب الميزان", page_icon="📖", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); color: #ddd; }
    h1, h2, h3 { color: #FFD700; }
</style>
""", unsafe_allow_html=True)

st.title("📖 كتاب الميزان")
st.header("المختبر القرآني – من الثنائية الكونية إلى معادلة الوجود")
st.caption("تأليف: علي عادل العاطفي | © 2026")

st.divider()

with st.expander("📜 الإهداء والمقدمة", expanded=False):
    st.markdown("""
    **الإهداء**
    إلى كل باحث عن الحقيقة...
    
    **مقدمة المؤلف**
    الحمد لله الذي رفع السماء ووضع الميزان...
    """)

with st.expander("🔍 تمهيد: البحث عن نظرية كل شيء", expanded=False):
    st.markdown("""
    منذ فجر الوعي، والبشرية تبحث عن إجابة لسؤال واحد...
    `S = W × B`
    """)

with st.expander("الباب الأول: الأصول – من أين بدأنا؟", expanded=False):
    st.markdown("""
    **الفصل الأول: ﴿اقْرَأْ بِاسْمِ رَبِّكَ﴾**
    ...
    """)

with st.expander("الباب الثاني: التعريفات المركزية", expanded=False):
    st.markdown("""
    **الدين القيم – قانون السببية الكوني الثابت**
    ...
    """)

with st.expander("الباب الثالث: الثنائية الكونية", expanded=False):
    st.markdown("""
    **٣.١ الكون يتكلم بلغة الثنائيات**
    ...
    """)

with st.expander("الباب الرابع: وحدة الخلق والأمر", expanded=False):
    st.markdown("""
    **﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ﴾**
    ...
    """)

with st.expander("الباب الخامس: المختبر – تشغيل المحاكاة", expanded=False):
    st.markdown("""
    **الحالات الأربع للكائن البشري: الذهبي، الأبيض، الأحمر، الوردي**
    ...
    """)

with st.expander("الباب السادس: نحو الأمة الذهبية", expanded=False):
    st.markdown("""
    **من الفرد إلى الأمة – هندسة المجتمع الذهبي**
    ...
    """)

with st.expander("الباب السابع: الفطرة – نظام التشغيل الأصلي", expanded=False):
    st.markdown("""
    **الميثاق الغليظ – يوم قالوا بلى**
    ...
    """)

with st.expander("الباب الثامن: التشخيص – واقع الأمة", expanded=False):
    st.markdown("""
    **حال الميزان اليوم**
    ...
    """)

with st.expander("الباب التاسع: سبل العودة إلى القانون", expanded=False):
    st.markdown("""
    **الإصلاح الفردي، الأسري، المجتمعي**
    ...
    """)

with st.expander("الباب العاشر: اكتمال الدائرة", expanded=False):
    st.markdown("""
    **من الأزل إلى الخلود**
    ...
    """)

st.caption("© 2026 علي عادل العاطفي | Al-Deen Al-Qayyim")
