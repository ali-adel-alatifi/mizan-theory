import streamlit as st

st.set_page_config(
    page_title="الدين القيم – متحف الميزان",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); }
    .big-title { font-size: 3em; font-weight: 900; color: #FFD700; text-align: center; margin: 30px 0 0 0; }
    .sub-title { font-size: 1.3em; color: #CCCCCC; text-align: center; margin: 0 0 5px 0; }
    .gold-text { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">⚖️ الدِّينُ الْقَيِّم</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">متحف الميزان – Al-Deen Al-Qayyim</p>', unsafe_allow_html=True)
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌌 المختبر الحي")
    st.markdown("المحاكاة التفاعلية لنظرية الميزان. شاهد النجوم والأمم وهي تتفاعل مع قوانين `S = W × B`.")
    st.page_link("pages/1_🌌_المختبر_الحي.py", label="🔬 ادخل إلى المختبر", use_container_width=True)

with col2:
    st.markdown("### 📖 كتاب الميزان")
    st.markdown("النظرية كاملة من الأزل إلى الخلود. الأبواب العشرة والشروحات الفلسفية والعلمية.")
    st.page_link("pages/2_📖_كتاب_الميزان.py", label="📜 افتح الكتاب", use_container_width=True)

with col3:
    st.markdown("### 📜 الدليل المرجعي")
    st.markdown("الوثائق الرسمية، المعجم الهندسي، وحقوق الملكية الفكرية للمشروع.")
    st.page_link("pages/3_📜_الدليل_المرجعي.py", label="🗂️ تصفح الوثائق", use_container_width=True)

st.divider()
st.info("جميع الحقوق محفوظة للمؤلف علي عادل العاطفي © 2026 | Al-Deen Al-Qayyim – The Cosmic Balance Law")
