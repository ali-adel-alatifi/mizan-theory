import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# إعداد الصفحة
# ==============================================
st.set_page_config(page_title="المختبر القرآني المتكامل", layout="wide")
st.title("🌌 المختبر القرآني: محاكي الاستخلاف المتكامل")
st.markdown("""
هذه اللوحة تدمج **نظام الإحداثيات** و**الهندسة التفاضلية** في أداة واحدة.
راقب حركة المجتمع في فضاء (W, B)، وشاهد ديناميكية التوبة الفردية.
""")

# ==============================================
# الشريط الجانبي
# ==============================================
st.sidebar.header("⚙️ إعدادات المحاكاة")
W0 = st.sidebar.slider("W (الولاء) - ابتدائي", 0.0, 1.0, 0.9, 0.05)
B0 = st.sidebar.slider("B (البراءة) - ابتدائي", 0.0, 1.0, 0.9, 0.05)
E0 = st.sidebar.slider("E (التمكين) - ابتدائي", 0.0, 1.0, 0.1, 0.05)
lag = st.sidebar.slider("⏳ فجوة الاستدراج (تأخر الأثر)", 0, 40, 20, 1)
years = st.sidebar.slider("📅 عدد سنوات المحاكاة", 100, 1000, 300, 50)

scenario = st.sidebar.selectbox("🎭 سيناريو جاهز", ["مخصص", "أمة صاعدة", "أمة على حافة الهاوية"])
if scenario == "أمة صاعدة":
    W0, B0, E0, lag = 0.9, 0.9, 0.1, 25
elif scenario == "أمة على حافة الهاوية":
    W0, B0, E0, lag = 0.3, 0.2, 0.9, 15

# ==============================================
# محرك المحاكاة
# ==============================================
@st.cache_data
def run_sim(W0, B0, E0, lag, years):
    W = np.zeros(years); B = np.zeros(years); S = np.zeros(years); E = np.zeros(years)
    W[0], B[0], E[0] = W0, B0, E0; S[0] = W[0] * B[0]
    for t in range(1, years):
        H = 10 / (S[t-1] + 0.1)
        dW = (0.08 * H) - (0.03 * E[t-1]) - (0.04 * (1 - B[t-1]))
        W[t] = max(0.0, min(1.0, W[t-1] + dW))
        dB = (-0.02 * E[t-1]) + (0.01 * (1 - B[t-1]) * W[t-1] * (1 - W[t-1]))
        B[t] = max(0.0, min(1.0, B[t-1] + dB))
        S[t] = W[t] * B[t]
        past_idx = t - lag
        S_past = S[past_idx] if past_idx >= 0 else S[t]
        dE = 0.05 * (S_past - E[t-1])
        E[t] = max(0.0, min(1.0, E[t-1] + dE))
    return W, B, S, E

W, B, S, E = run_sim(W0, B0, E0, lag, years)

# ==============================================
# رسم النتائج الستة
# ==============================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
time = np.arange(years)

# 1. دورة الحضارة
ax = axes[0, 0]
ax.plot(time, S, label='S (الثبات)', color='green')
ax.plot(time, E, label='E (التمكين)', color='blue', linestyle='--')
gap_s = np.argmax(S); gap_e = np.argmax(E)
if gap_s < gap_e: ax.axvspan(gap_s, gap_e, alpha=0.2, color='red', label='الاستدراج')
ax.set_title('1. دورة الحضارة: S مقابل E'); ax.legend(); ax.grid(True, alpha=0.3)

# 2. مكونات
ax = axes[0, 1]
ax.plot(time, W, label='W (الولاء)', color='darkgreen')
ax.plot(time, B, label='B (البراءة)', color='darkred')
ax.set_title('2. مكونات المعادلة'); ax.legend(); ax.grid(True, alpha=0.3)

# 3. S و H
ax = axes[0, 2]
H_series = 10 / (S + 0.1)
ax.plot(time, S, label='S', color='green')
ax.plot(time, H_series, label='H (الهوان)', color='red')
ax.set_title('3. الثبات والهوان'); ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0, 5)

# 4. مسار المجتمع
ax = axes[1, 0]
ax.axhline(0.5, color='gray', ls=':'); ax.axvline(0.5, color='gray', ls=':')
sc = ax.scatter(B, W, c=time, cmap='viridis', s=5)
ax.plot(B[0], W[0], 'go', ms=8, label='البداية')
ax.plot(B[-1], W[-1], 'ro', ms=8, label='النهاية')
ax.set_xlabel('B'); ax.set_ylabel('W'); ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.set_title('4. مسار المجتمع في (W, B)'); ax.legend(); ax.grid(True, alpha=0.3)
plt.colorbar(sc, ax=ax, label='الزمن')

# 5. مسار الفرد والتوبة
ax = axes[1, 1]
# محاكاة فرد
W_i, B_i = [0.9], [0.9]
for _ in range(40):
    W_i.append(W_i[-1] - 0.005*np.random.randn())
    B_i.append(B_i[-1] - 0.01*np.random.randn())
W_i.append(W_i[-1]+0.3); B_i.append(B_i[-1]+0.3)
for _ in range(30):
    W_i.append(W_i[-1] + 0.005*np.random.randn())
    B_i.append(B_i[-1] + 0.005*np.random.randn())
W_i = np.clip(W_i, 0, 1); B_i = np.clip(B_i, 0, 1)
ax.plot(B_i, W_i, 'b-', lw=1.5)
ax.plot(B_i[39], W_i[39], 'mo', ms=10, label='التوبة')
ax.set_xlabel('B'); ax.set_ylabel('W'); ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.set_title('5. مسار الفرد: قفزة التوبة'); ax.legend(); ax.grid(True, alpha=0.3)

# 6. نص
ax = axes[1, 2]
gap_s, gap_e = np.argmax(S), np.argmax(E)
txt = f"✅ تم رصد 'الاستدراج'!\n\nذروة S: عام {gap_s}\nذروة E: عام {gap_e}\nفجوة: {gap_e - gap_s} سنة" if gap_s < gap_e else "📈 المجتمع في صعود."
ax.text(0.1, 0.5, txt, fontsize=14, va='center'); ax.axis('off')

plt.tight_layout()
st.pyplot(fig)
st.markdown("---\n🛠️ **كيف تقرأ النتائج؟** إذا انهار S بينما E ما زال مرتفعاً، فأنت في **الاستدراج الإلهي**.")
