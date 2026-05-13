import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =============================================
# الإعدادات
# =============================================
st.set_page_config(page_title="⚖️ المحرك الوجودي", page_icon="⚖️", layout="wide")
st.markdown("<h1 style='text-align:center;color:#FFD700'>⚖️ المحرك الوجودي – قانون العروة الوثقى</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#CCC'>﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>", unsafe_allow_html=True)

# =============================================
# الشريط الجانبي – 11 منزلقًا وجوديًا
# =============================================
with st.sidebar:
    st.header("🎛️ مؤشرات الوجود")

    st.subheader("🤍 الولاء (W) – الإيمان بالله")
    W1 = st.slider("الصلاة", -1.0, 1.0, 0.0, 0.1)
    W2 = st.slider("الزكاة والصدقات", -1.0, 1.0, 0.0, 0.1)
    W3 = st.slider("الولاء لله ورسوله والمؤمنين", -1.0, 1.0, 0.0, 0.1)
    W4 = st.slider("تحكيم الشريعة", -1.0, 1.0, 0.0, 0.1)
    W5 = st.slider("العدل", -1.0, 1.0, 0.0, 0.1)
    W6 = st.slider("الشورى", -1.0, 1.0, 0.0, 0.1)

    st.subheader("❤️ البراءة (B) – الكفر بالطاغوت")
    B1 = st.slider("البراءة من الطاغوت", -1.0, 1.0, 0.0, 0.1)
    B2 = st.slider("الرحمة والعطاء (الماعون)", -1.0, 1.0, 0.0, 0.1, help="﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾")
    B3 = st.slider("الأمر بالمعروف", -1.0, 1.0, 0.0, 0.1)
    B4 = st.slider("النهي عن المنكر", -1.0, 1.0, 0.0, 0.1)
    B5 = st.slider("النزاهة ومكافحة الفساد", -1.0, 1.0, 0.0, 0.1)

# =============================================
# المحرك الوجودي – حيث تتحول الآية إلى معادلة
# =============================================

# ١. القيم الخام
W_raw = np.mean([W1, W2, W3, W4, W5, W6])
B_raw = np.mean([B1, B2, B3, B4, B5])

# ٢. القيم العددية للحروف (حساب الجمل)
ح = {'أ':1,'ل':30,'م':40,'ر':200,'س':60,'ح':8,'ط':9}

# ٣. تطبيع W و B إلى 0-1
W = (W_raw + 1) / 2
B = (B_raw + 1) / 2

# ٤. تطبيق مُوَلِّدَات الحروف (تضخيم الطاقة الوجودية)
W_boost = 1 + (ح['أ'] + ح['ر'] + ح['س'] + ح['ط']) / 1000
B_boost = 1 + (ح['ل'] + ح['ح'] + ح['ط']) / 1000
W_eff = W * W_boost
B_eff = B * B_boost

# ٥. حساب الثبات S
S_raw = W_eff * B_eff * (1 + ح['م'] / 1000)

# =============================================
# البوابات المنطقية الثلاث – المستمدة من القرآن
# =============================================
gate_name, gate_msg = "", ""

if B2 <= 0:  # بوابة الماعون
    S_final = -1
    gate_name = "بوابة الماعون"
    gate_msg = "⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾"
elif W1 > 0 and B1 <= 0:  # بوابة الإخلاص
    S_final = 0
    gate_name = "بوابة الإخلاص"
    gate_msg = "⚠️ باطل: ﴿يَعْبُدُونَنِي وَلَا يُشْرِكُونَ بِي شَيْئًا﴾"
elif W_raw > 0 and B_raw > 0:  # بوابة الوعد
    S_final = min(1.0, S_raw)
    gate_name = "بوابة الوعد"
    gate_msg = "🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾"
else:
    S_final = max(0.0, S_raw)
    gate_name = "المعادلة العامة"

# =============================================
# عرض النتائج
# =============================================
col1, col2, col3 = st.columns(3)
col1.metric("W (الولاء)", f"{W_raw:+.2f}")
col2.metric("B (البراءة)", f"{B_raw:+.2f}")
col3.metric("S (الثبات)", f"{S_final:.2f}")

if gate_msg:
    if "انهيار" in gate_msg: st.error(gate_msg)
    elif "باطل" in gate_msg: st.warning(gate_msg)
    else: st.success(gate_msg)

# =============================================
# خريطة الوجود (فضاء القيم)
# =============================================
fig, ax = plt.subplots(figsize=(6,6), facecolor='#0a0a2e')
ax.set_facecolor('#0a0a2e')
ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
ax.set_xlabel("B (الكفر بالطاغوت)", color='white'); ax.set_ylabel("W (الإيمان بالله)", color='white')

# الأرباع
ax.fill_between([0,1.2], 0, 1.2, color='#FFD700', alpha=0.2)
ax.fill_between([-1.2,0], 0, 1.2, color='#FF5252', alpha=0.2)
ax.fill_between([-1.2,0], -1.2, 0, color='#FFB6C1', alpha=0.2)
ax.fill_between([0,1.2], -1.2, 0, color='#FFA500', alpha=0.2)

ax.text(0.6,0.6,'المؤمنون',color='#FFD700',fontsize=10,ha='center',fontweight='bold')
ax.text(-0.6,0.6,'المغضوب عليهم',color='#FF5252',fontsize=10,ha='center',fontweight='bold')
ax.text(-0.6,-0.6,'المنافقون',color='#FFB6C1',fontsize=10,ha='center',fontweight='bold')
ax.text(0.6,-0.6,'الضالون',color='#FFA500',fontsize=10,ha='center',fontweight='bold')

# نقطة الكيان
ax.scatter(B_raw, W_raw, s=300, c='cyan', edgecolors='white', linewidth=3, zorder=10)
# مقام إبراهيم
ax.scatter(1, 1, s=100, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, marker='*')
ax.text(1, 1.15, 'إبراهيم', color='#FFD700', fontsize=8, ha='center')

ax.tick_params(colors='white')
st.pyplot(fig)

st.markdown("---")
st.caption("⚖️ المحرك الوجودي – المرحلة الأولى | علي عادل العاطفي | 2026")
