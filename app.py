import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image

# ==============================================
# إعداد عنوان الصفحة والمقدمة
# ==============================================
st.set_page_config(page_title="محاكي الاستخلاف", layout="wide")
st.title("🌍 مختبر السنن الإلهية التفاعلي")
st.markdown("""
هذه الأداة تحاكي **دورة الحضارة** بناءً على معادلة الثبات القرآني: **S = W × B**.
استخدم المنزلقات في الشريط الجانبي لتغيير قيم المجتمع الابتدائية، وشاهد كيف تتغير منحنيات الصعود والسقوط!
""")

# ==============================================
# الشريط الجانبي (Sidebar) للتحكم بالمعاملات
# ==============================================
st.sidebar.header("⚙️ إعدادات المحاكاة")
W0 = st.sidebar.slider("W (الولاء لله) - القيمة الابتدائية", 0.0, 1.0, 0.9, 0.05)
B0 = st.sidebar.slider("B (البراءة من الطاغوت) - القيمة الابتدائية", 0.0, 1.0, 0.9, 0.05)
E0 = st.sidebar.slider("E (التمكين المادي) - القيمة الابتدائية", 0.0, 1.0, 0.1, 0.05)
lag = st.sidebar.slider("⏳ فجوة الاستدراج (تأخر الأثر بالسنوات)", 0, 40, 20, 1)
years = 200

st.sidebar.markdown("---")
st.sidebar.markdown("📊 **السيناريوهات الجاهزة:**")
scenario = st.sidebar.radio("اختر سيناريو:", ["مخصص", "أمة صاعدة (قوة إيمانية)", "أمة على حافة الهاوية (تيه وترف)"])

if scenario == "أمة صاعدة (قوة إيمانية)":
    W0, B0, E0, lag = 0.9, 0.9, 0.1, 25
elif scenario == "أمة على حافة الهاوية (تيه وترف)":
    W0, B0, E0, lag = 0.3, 0.2, 0.9, 15

# ==============================================
# محرك المحاكاة (Simulation Engine)
# ==============================================
@st.cache_data
def run_simulation(W0, B0, E0, lag, years):
    W = np.zeros(years)
    B = np.zeros(years)
    S = np.zeros(years)
    E = np.zeros(years)
    W[0], B[0], E[0] = W0, B0, E0
    S[0] = W[0] * B[0]
    
    for t in range(1, years):
        H = 10 / (S[t-1] + 0.1)
        dW = (0.08 * H) - (0.03 * E[t-1]) - (0.04 * (1 - B[t-1]))
        W[t] = max(0.0, min(1.0, W[t-1] + dW))
        dB = (-0.02 * E[t-1]) + (0.01 * (1 - B[t-1]) * W[t-1] * (1 - W[t-1]))
        B[t] = max(0.0, min(1.0, B[t-1] + dB))
        S[t] = W[t] * B[t]
        past_t = t - lag
        if past_t >= 0:
            dE = 0.05 * (S[past_t] - E[t-1])
        else:
            dE = 0.05 * (S[t] - E[t-1])
        E[t] = max(0.0, min(1.0, E[t-1] + dE))
    return W, B, S, E

W, B, S, E = run_simulation(W0, B0, E0, lag, years)

# ==============================================
# عرض النتائج (الرسوم البيانية)
# ==============================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
time = np.arange(years)

# الرسم 1: S و E
ax1 = axes[0, 0]
ax1.plot(time, S, label='S (الثبات)', color='green', linewidth=2)
ax1.plot(time, E, label='E (التمكين)', color='blue', linewidth=2, linestyle='--')
if np.argmax(S) < np.argmax(E):
    ax1.axvspan(np.argmax(S), np.argmax(E), alpha=0.2, color='red', label='منطقة الاستدراج')
ax1.set_title('دورة الحضارة: الثبات (S) مقابل التمكين (E)')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 1.1)

# الرسم 2: W و B
ax2 = axes[0, 1]
ax2.plot(time, W, label='W (الولاء)', color='darkgreen')
ax2.plot(time, B, label='B (البراءة)', color='darkred')
ax2.set_title('مكونات المعادلة: الولاء (W) والبراءة (B)')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.1)

# الرسم 3: S و H
ax3 = axes[1, 0]
H_series = 10 / (S + 0.1)
ax3.plot(time, S, label='S (الثبات)', color='green')
ax3.plot(time, H_series, label='H (الهوان)', color='red')
ax3.set_title('علاقة الثبات (S) بالهوان (H)')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_ylim(0, 5)

# الرسم 4: نص تحليلي
ax4 = axes[1, 1]
max_S_idx = np.argmax(S)
max_E_idx = np.argmax(E)
if max_S_idx < max_E_idx:
    gap_analysis = f"""
    ✅ **تم رصد "الاستدراج" الإلهي!**
    
    - **ذروة الثبات (S):** العام {max_S_idx}
    - **ذروة التمكين (E):** العام {max_E_idx}
    - **مدة الاستدراج:** {max_E_idx - max_S_idx} سنة
    
    ⚠️ لاحظت أن انهيار الإيمان (W) يسبق انهيار الحضارة (E) بعقود.
    """
else:
    gap_analysis = f"""
    📈 **المجتمع في حالة صعود.**
    
    - **ذروة الثبات (S):** العام {max_S_idx}
    - لم يصل E إلى ذروته بعد (أو مستقر).
    """
ax4.text(0.1, 0.5, gap_analysis, fontsize=14, verticalalignment='center')
ax4.axis('off')

st.pyplot(fig)

# ==============================================
# تذييل
# ==============================================
st.markdown("---")
st.markdown("🛠️ **كيف تقرأ هذه النتائج؟** إذا انهار S بينما E ما زال مرتفعاً، فاعلم أنك دخلت في **الاستدراج الإلهي**.")
