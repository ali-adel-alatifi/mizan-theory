import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="البوصلة الكونية", page_icon="🧭", layout="wide")

# =============================================
# 🎨 CSS
# =============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); color: #ddd; }
    h1, h2, h3 { color: #FFD700; }
    .result-box { background: rgba(10,10,46,0.8); border-radius: 15px; padding: 20px; border: 1px solid #FFD700; margin: 10px 0; }
    .big-number { font-size: 3em; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🧭 البوصلة الكونية")
st.header("اختبار الإحداثيات الوجودية – اكتشف موقعك في فضاء الولاء والبراء")
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi")

st.divider()

# =============================================
# 📋 جلسة الاختبار
# =============================================
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# تعريف الأسئلة
questions = {
    "L": [
        {"id": "L1", "q": "عندما أكون وحيداً، أفكاري تتجه نحو:", "a": [("الله وذكره", 3), ("أمور الدنيا والمستقبل المادي", 1), ("لا أفكر في شيء محدد", 0), ("أفكار سلبية ومتشائمة", -1)]},
        {"id": "L2", "q": "شعوري تجاه الله هو:", "a": [("محبة وخوف ورجاء", 3), ("خوف من العقاب فقط", 1), ("لا أشعر بشيء خاص", 0), ("مشاعر سلبية أو رفض", -1)]},
        {"id": "L3", "q": "قراراتي الكبرى في الحياة تتخذ بناءً على:", "a": [("ما يرضي الله أولاً", 3), ("ما ينفعني مادياً", 1), ("حسب الموقف", 0), ("ما يشبع رغباتي", -1)]},
        {"id": "L4", "q": "أولويتي عند تعارض المصالح:", "a": [("رضا الله فوق كل شيء", 3), ("مصلحتي الشخصية", 1), ("أبحث عن حل وسط", 0), ("مصلحتي أولاً ولو بمعصية", -1)]},
        {"id": "L5", "q": "علاقاتي مع الآخرين تقوم على:", "a": [("مرضاة الله وخدمة الخلق", 3), ("المصالح المتبادلة", 1), ("العاطفة والمزاج", 0), ("الاستغلال والمنفعة", -1)]},
        {"id": "L6", "q": "انتمائي الحقيقي هو لـ:", "a": [("الله ودينه وأمته", 3), ("بلدي وعائلتي فقط", 1), ("نفسي ومصالحي", 0), ("لا أنتمي لأحد", -1)]},
    ],
    "D": [
        {"id": "D1", "q": "مشاعري تجاه المعاصي:", "a": [("كراهية وبغض", 3), ("خوف من العواقب فقط", 1), ("لا مشاعر خاصة", 0), ("رغبة وميل", -1)]},
        {"id": "D2", "q": "عند رؤية المنكر أشعر بـ:", "a": [("حزن ورغبة في التغيير", 3), ("ازعاج فقط", 1), ("لا شيء", 0), ("متعة أو تقبل", -1)]},
        {"id": "D3", "q": "تعاملي مع المحرمات:", "a": [("أتجنبها تماماً", 3), ("أتجنب الكبائر فقط", 1), ("أحياناً أقع فيها", 0), ("أمارسها عمداً", -1)]},
        {"id": "D4", "q": "عندما أخطئ:", "a": [("أتوب فوراً وأتدارك", 3), ("أتوب إذا تذكرت", 1), ("لا أبالي", 0), ("أستمتع وأكرر", -1)]},
        {"id": "D5", "q": "في تعاملي مع الظالمين:", "a": [("أبرأ منهم ولا أعاونهم", 3), ("أتعامل لمصلحتي فقط", 1), ("أتعامل طالما لم يضروني", 0), ("أتعاون معهم", -1)]},
        {"id": "D6", "q": "موقفي من الأفكار المخالفة للدين:", "a": [("أرفضها وأحذر منها", 3), ("أتجاهلها", 1), ("أستمع لها بلا موقف", 0), ("أتقبلها وأعتنقها", -1)]},
    ]
}

st.subheader("📝 أجب عن الأسئلة التالية بصدق")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🤍 أسئلة الولاء (L)")
    for q in questions["L"]:
        ans = st.radio(f"**{q['q']}**", [a[0] for a in q['a']], key=q['id'], index=None)
        if ans:
            st.session_state.answers[q['id']] = [a[1] for a in q['a'] if a[0] == ans][0]

with col2:
    st.markdown("### ❤️ أسئلة البراء (D)")
    for q in questions["D"]:
        ans = st.radio(f"**{q['q']}**", [a[0] for a in q['a']], key=q['id'], index=None)
        if ans:
            st.session_state.answers[q['id']] = [a[1] for a in q['a'] if a[0] == ans][0]

# =============================================
# 🧮 حساب النتيجة
# =============================================
if len(st.session_state.answers) == 12:
    L_score = sum([st.session_state.answers[f"L{i}"] for i in range(1, 7)])
    D_score = sum([st.session_state.answers[f"D{i}"] for i in range(1, 7)])
    
    L = L_score / 12  # L ∈ [-1, 1]
    D = D_score / 12  # D ∈ [-1, 1]

    # تحديد الربع
    if L > 0 and D > 0: quadrant = "Q1"
    elif L < 0 and D > 0: quadrant = "Q2"
    elif L < 0 and D < 0: quadrant = "Q3"
    elif L > 0 and D < 0: quadrant = "Q4"
    else: quadrant = "محايد"

    # أسماء الأرباع
    q_names = {"Q1": "المؤمن (الربع الأول)", "Q2": "الكافر (الربع الثاني)", "Q3": "المنافق (الربع الثالث)", "Q4": "المشرك (الربع الرابع)", "محايد": "منطقة محايدة"}
    q_advice = {
        "Q1": "أنت في الطريق الصحيح. حافظ على ثباتك، واستمر في النمو نحو (1,1).",
        "Q2": "ولاؤك لغير الله. أنت بحاجة إلى توبة جذرية وتحويل بوصلتك نحو الخالق. ابدأ بالتعرف على الله حق المعرفة.",
        "Q3": "أنت في حالة تذبذب خطيرة. أنت بحاجة إلى الصدق مع نفسك واتخاذ قرار حاسم بالولاء لله وحده.",
        "Q4": "لديك إيمان بالله لكنك تخلطه بشرك. أنت بحاجة إلى توحيد خالص لله، والبراءة من كل ما سواه."
    }

    st.divider()
    st.header("📊 نتائج اختبار البوصلة الكونية")

    # عرض النتيجة
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"""
        <div class="result-box">
            <p class="big-number" style="color:#FFD700;">{q_names[quadrant]}</p>
            <p style="text-align:center;">إحداثياتك: <b>L = {L:.2f}</b> | <b>D = {D:.2f}</b></p>
            <p style="text-align:center;">{q_advice[quadrant]}</p>
        </div>
        """, unsafe_allow_html=True)

    # رسم الخريطة
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
    ax.set_facecolor('#0a0a2e')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='grey', lw=0.5)
    ax.axvline(0, color='grey', lw=0.5)
    ax.set_xlabel("البراء (D)", color='white')
    ax.set_ylabel("الولاء (L)", color='white')

    # تلوين الأرباع
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.15))
    ax.add_patch(patches.Rectangle((-1, 0), 1, 1, color='#FF3333', alpha=0.15))
    ax.add_patch(patches.Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.15))
    ax.add_patch(patches.Rectangle((0, -1), 1, 1, color='#FFA07A', alpha=0.15))

    ax.text(0.5, 0.5, "مؤمن", color='white', ha='center', alpha=0.5)
    ax.text(-0.5, 0.5, "كافر", color='white', ha='center', alpha=0.5)
    ax.text(-0.5, -0.5, "منافق", color='white', ha='center', alpha=0.5)
    ax.text(0.5, -0.5, "مشرك", color='white', ha='center', alpha=0.5)
    
    # نقطة المستخدم
    ax.scatter(D, L, c='#00FFFF', s=200, edgecolors='white', linewidth=2, zorder=5)
    ax.tick_params(colors='white')
    st.pyplot(fig)

    # زر إعادة الاختبار
    if st.button("🔄 إعادة الاختبار"):
        st.session_state.answers = {}
        st.rerun()

st.caption("© 2026 علي عادل العاطفي | Al-Deen Al-Qayyim – البوصلة الكونية")
