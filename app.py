import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =============================================
# الإعدادات العامة
# =============================================
st.set_page_config(page_title="⚖️ مختبر الميزان – النظام المتكامل", page_icon="⚖️", layout="wide")
st.markdown("<h1 style='text-align:center;color:#FFD700'>⚖️ مختبر الميزان – النظام المتكامل</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#CCC'>﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>", unsafe_allow_html=True)

# =============================================
# الثوابت الوجودية
# =============================================
ح = {'أ':1,'ل':30,'م':40,'ر':200,'س':60,'ح':8,'ط':9}
W_LABELS = ["الصلاة", "الزكاة والصدقات", "الولاء لله ورسوله والمؤمنين", "تحكيم الشريعة", "العدل", "الشورى"]
B_LABELS = ["البراءة من الطاغوت", "الرحمة والعطاء (الماعون)", "الأمر بالمعروف", "النهي عن المنكر", "النزاهة ومكافحة الفساد"]

# =============================================
# الشريط الجانبي الذكي
# =============================================
with st.sidebar:
    st.header("🎛️ لوحة التحكم")
    mode = st.radio("اختر وضع الإدخال:", ["🧑‍⚖️ التقدير اليدوي (المنزلقات)", "🤖 مساعد الذكاء الاصطناعي"])

    if mode == "🧑‍⚖️ التقدير اليدوي (المنزلقات)":
        st.subheader("🤍 الولاء (W)")
        W1 = st.slider(W_LABELS[0], -1.0, 1.0, 0.0, 0.1)
        W2 = st.slider(W_LABELS[1], -1.0, 1.0, 0.0, 0.1)
        W3 = st.slider(W_LABELS[2], -1.0, 1.0, 0.0, 0.1)
        W4 = st.slider(W_LABELS[3], -1.0, 1.0, 0.0, 0.1)
        W5 = st.slider(W_LABELS[4], -1.0, 1.0, 0.0, 0.1)
        W6 = st.slider(W_LABELS[5], -1.0, 1.0, 0.0, 0.1)

        st.subheader("❤️ البراءة (B)")
        B1 = st.slider(B_LABELS[0], -1.0, 1.0, 0.0, 0.1)
        B2 = st.slider(B_LABELS[1], -1.0, 1.0, 0.0, 0.1, help="﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾")
        B3 = st.slider(B_LABELS[2], -1.0, 1.0, 0.0, 0.1)
        B4 = st.slider(B_LABELS[3], -1.0, 1.0, 0.0, 0.1)
        B5 = st.slider(B_LABELS[4], -1.0, 1.0, 0.0, 0.1)

        st.subheader("🌐 التمكين المادي (E)")
        E_val = st.slider("مستوى التمكين", 0.0, 1.0, 0.5, 0.05)

    else:  # وضع الذكاء الاصطناعي
        st.info("أدخل وصفًا نصيًا للكيان (دولة، مجتمع، فرد). سيقوم الذكاء الاصطناعي بتقدير القيم.")
        ai_text = st.text_area("الوصف النصي:", height=250)
        ai_mode = st.radio("نوع الكيان:", ["دولة", "مجتمع", "فرد"])
        if st.button("تحليل بالذكاء الاصطناعي"):
            with st.spinner("جاري التحليل..."):
                # هنا سيتم استدعاء API الذكاء الاصطناعي لتحويل النص إلى أرقام
                # ai_result = call_ai_api(ai_text)
                # حاليًا: محاكاة للنتيجة
                ai_result = {
                    "W": [0.5, 0.4, 0.5, 0.6, 0.4, 0.3],
                    "B": [0.6, 0.5, 0.4, 0.3, 0.4],
                    "E": 0.6
                }
                W1, W2, W3, W4, W5, W6 = ai_result["W"]
                B1, B2, B3, B4, B5 = ai_result["B"]
                E_val = ai_result["E"]
                st.success("تم التحليل!")
        else:
            W1, W2, W3, W4, W5, W6 = [0.0]*6
            B1, B2, B3, B4, B5 = [0.0]*5
            E_val = 0.5

# =============================================
# المحرك الوجودي
# =============================================
W_raw = np.mean([W1, W2, W3, W4, W5, W6])
B_raw = np.mean([B1, B2, B3, B4, B5])

# تطبيع
W = (W_raw + 1) / 2
B = (B_raw + 1) / 2

# تضخيم الحروف
W_boost = 1 + (ح['أ'] + ح['ر'] + ح['س'] + ح['ط']) / 1000
B_boost = 1 + (ح['ل'] + ح['ح'] + ح['ط']) / 1000
W_eff = W * W_boost
B_eff = B * B_boost
S_raw = W_eff * B_eff * (1 + ح['م'] / 1000)

# البوابات المنطقية
gate_name, gate_msg, gate_color = "", "", ""
if B2 <= 0:
    S_final = -1
    gate_name = "بوابة الماعون"
    gate_msg = "⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾"
    gate_color = "🔴"
elif W1 > 0 and B1 <= 0:
    S_final = 0
    gate_name = "بوابة الإخلاص"
    gate_msg = "⚠️ باطل: ﴿يَعْبُدُونَنِي وَلَا يُشْرِكُونَ بِي شَيْئًا﴾"
    gate_color = "🟡"
elif W_raw > 0 and B_raw > 0:
    S_final = min(1.0, S_raw)
    gate_name = "بوابة الوعد"
    gate_msg = "🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾"
    gate_color = "🟢"
else:
    S_final = max(0.0, S_raw)
    gate_name = "المعادلة العامة"
    gate_color = "⚪"

# فجوة الاستدراج
istidraj_gap = max(0, E_val - S_final) if S_final > -1 else 1.0
istidraj_warning = ""
if istidraj_gap > 0.3:
    istidraj_warning = f"🚨 إنذار استدراج: التمكين المادي (E={E_val:.2f}) يتجاوز الثبات (S={S_final:.2f}) بفجوة {istidraj_gap:.2f}!"
elif istidraj_gap > 0.1:
    istidraj_warning = f"⚡ تحذير: فجوة استدراج متوسطة ({istidraj_gap:.2f})."

# =============================================
# عرض النتائج الحالية
# =============================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("W (الولاء)", f"{W_raw:+.2f}")
col2.metric("B (البراءة)", f"{B_raw:+.2f}")
col3.metric("S (الثبات)", f"{S_final:.2f}")
col4.metric("E (التمكين)", f"{E_val:.2f}")

st.markdown(f"### {gate_color} {gate_name}")
if gate_msg:
    if "انهيار" in gate_msg: st.error(gate_msg)
    elif "باطل" in gate_msg: st.warning(gate_msg)
    else: st.success(gate_msg)
if istidraj_warning:
    st.error(istidraj_warning) if "إنذار" in istidraj_warning else st.warning(istidraj_warning)

# =============================================
# المحاكي الزمني – حتمية المصير
# =============================================
st.divider()
st.header("⏳ المحاكي الزمني – حتمية المصير")
st.markdown("هذه المحاكاة تظهر كيف ستتغير S وE عبر 50 سنة افتراضية بناءً على القيم الحالية.")

years = 50
S_history, E_history = [S_final], [E_val]
for _ in range(years):
    new_E = E_history[-1] + 0.02 * (S_history[-1] - E_history[-1])
    new_W = W_raw
    new_B = B_raw
    # تأثير طويل المدى: إذا كانت الفجوة كبيرة، تنهار S تدريجيًا
    if new_E > S_history[-1] + 0.2:
        new_B -= 0.03
    elif new_E < S_history[-1]:
        new_B += 0.01
    new_S = ((new_W+1)/2) * ((new_B+1)/2) * (1 + sum(ح.values())/1000)
    S_history.append(new_S)
    E_history.append(new_E)

fig, ax = plt.subplots(figsize=(10, 4), facecolor='#0a0a2e')
ax.set_facecolor('#0a0a2e')
ax.plot(S_history, label='S (الثبات)', color='#FFD700', linewidth=2)
ax.plot(E_history, label='E (التمكين)', color='#00FFFF', linewidth=2, linestyle='--')
ax.fill_between(range(years+1), S_history, E_history, where=(np.array(E_history) > np.array(S_history)), color='red', alpha=0.2, label='منطقة الاستدراج')
ax.axhline(y=0, color='red', linestyle=':')
ax.set_xlabel('السنوات', color='white')
ax.set_ylabel('القيمة', color='white')
ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.2)
st.pyplot(fig)

# =============================================
# المستشفى – وصفة علاجية
# =============================================
st.divider()
st.header("🏥 المستشفى – وصفة علاجية")
W_vals, B_vals = [W1,W2,W3,W4,W5,W6], [B1,B2,B3,B4,B5]
weakest_W_idx, weakest_B_idx = np.argmin(W_vals), np.argmin(B_vals)
if gate_name == "بوابة الماعون":
    st.error(f"🎯 الأولوية القصوى: إصلاح '{B_LABELS[weakest_B_idx]}'. بدون رحمة وعطاء، لا تنفع أي عبادة.")
elif gate_name == "بوابة الإخلاص":
    st.warning(f"🎯 الأولوية: تنقية '{W_LABELS[weakest_W_idx]}' من شوائب الشرك والرياء.")
elif istidraj_gap > 0.3:
    st.error(f"🎯 سد فجوة الاستدراج ({istidraj_gap:.2f}) عبر رفع '{B_LABELS[weakest_B_idx]}' أو '{W_LABELS[weakest_W_idx]}'.")
else:
    st.info(f"🎯 للتقدم نحو مقام إبراهيم: عزز '{W_LABELS[weakest_W_idx]}' و'{B_LABELS[weakest_B_idx]}'.")
st.markdown(f"- أضعف مؤشر ولاء (W): **{W_LABELS[weakest_W_idx]}** ({W_vals[weakest_W_idx]:+.2f})\n- أضعف مؤشر براءة (B): **{B_LABELS[weakest_B_idx]}** ({B_vals[weakest_B_idx]:+.2f})")

st.markdown("---")
st.caption("⚖️ مختبر الميزان – النظام المتكامل | علي عادل العاطفي | 2026")
