import streamlit as st

st.set_page_config(page_title="كتاب الميزان", page_icon="📖", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); color: #ddd; }
    h1, h2, h3 { color: #FFD700; }
    hr { border-color: rgba(218,165,32,0.3); }
</style>
""", unsafe_allow_html=True)

st.title("📖 كتاب الميزان")
st.header("المختبر القرآني – من الثنائية الكونية إلى معادلة الوجود")
st.caption("تأليف: علي عادل العاطفي | © 2026")

st.divider()

# --- ملاحظة: يمكنك إضافة فصول الكتاب الكاملة هنا ---
# لقد قمنا بصياغة الكتاب في محادثتنا. يمكنك نسخ كل باب من الأبواب التي كتبناها معاً ولصقها في موسع `st.expander` خاص به.

st.info("⚠️ هذا القسم قيد الإنشاء. سنقوم بإضافة النص الكامل للكتاب هنا.")
