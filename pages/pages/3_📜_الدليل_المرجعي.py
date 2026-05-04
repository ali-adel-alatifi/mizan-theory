import streamlit as st

st.set_page_config(page_title="الدليل المرجعي", page_icon="📜", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); color: #ddd; }
    h1, h2, h3 { color: #FFD700; }
    hr { border-color: rgba(218,165,32,0.3); }
</style>
""", unsafe_allow_html=True)

st.title("📜 الدليل المرجعي الشامل")
st.header("نظرية الميزان – الوثائق الرسمية والهوية")
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi")

st.divider()

with st.expander("📜 الوثيقة الشاملة", expanded=True):
    st.markdown("""
    **المشروع:** نظرية الميزان – محاكاة تفاعلية
    **المؤلف:** علي عادل العاطفي (Ali Adel Alatifi)
    **الترخيص:** MIT License
    
    **ملخص تنفيذي**
    نظرية الميزان هي إطار رياضي وفلسفي متكامل يهدف إلى نمذجة صعود وسقوط الحضارات...
    """)

with st.expander("🔤 معجم 'نحو الميزان' – المشغلات القرآنية", expanded=False):
    st.markdown("""
    **المشغّلات الأساسية**
    - **الفاء (فَـ) =**: علامة التساوي. تربط السبب بالنتيجة ربطًا حتميًا.
    - **الواو (وَ) ×**: واو الضرب الشرطي. تجمع بين شرطين لا يتم الأمر إلا بهما.
    - **الواو (وَ) +**: واو الجمع التراكمي. تجمع بين قيمتين تتراكمان.
    """)

with st.expander("🛡️ حقوق الملكية والترخيص", expanded=False):
    st.markdown("""
    **© 2026 علي عادل العاطفي**
    هذا المشروع محمي بموجب ترخيص MIT License.
    يُسمح بالاستخدام والتعديل والنشر مع ذكر المصدر الأصلي والمؤلف.
    
    أي استخدام تجاري أو بحثي يجب أن يُنسب إلى:
    **علي عادل العاطفي – Ali Adel Alatifi**
    """)
