import streamlit as st

st.set_page_config(page_title="الدين القيم", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

st.title("⚖️ الدِّينُ الْقَيِّم ⚖️")
st.header("قَانُونُ التَّوَازُنِ الْكَوْنِيّ")
st.caption("S = W × B | © 2026 Ali Adel Alatifi")

with st.sidebar:
    st.header("🎛️ لوحة التحكم")
    prayer = st.slider("الصلاة", 0.0, 1.0, 0.8, 0.01)
    zakat = st.slider("الزكاة", 0.0, 1.0, 0.6, 0.01)
    fasting = st.slider("الصوم", 0.0, 1.0, 0.7, 0.01)
    hajj = st.slider("الحج", 0.0, 1.0, 0.5, 0.01)

st.success("التطبيق يعمل بنجاح ✅")
st.info("© 2026 Ali Adel Alatifi | Al-Deen Al-Qayyim")
