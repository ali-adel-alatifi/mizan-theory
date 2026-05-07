import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# إعداد الصفحة
# ==============================================
st.set_page_config(page_title="المختبر المتكامل", layout="wide")
st.title("🌌 المختبر المتكامل: محاكي الاستخلاف + نموذج العوامل")
st.markdown("""
هذا المختبر يجمع بين **"التلسكوب"** (رؤية الأمة ككل) و**"الميكروسكوب"** (رؤية الأفراد وتفاعلاتهم).
""")

# ==============================================
# الشريط الجانبي للتحكم الكامل
# ==============================================
st.sidebar.header("⚙️ إعدادات المحاكاة")

# اختيار وضع المحاكاة
mode = st.sidebar.radio(
    "اختر المحاكاة:",
    ["📡 محاكي الاستخلاف (الأمة ككل)", "🔬 نموذج العوامل (الأفراد)", "🌐 المختبر المتكامل"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 إعدادات عامة")
years = st.sidebar.slider("سنوات المحاكاة", 50, 500, 200, 50)

# إعدادات المحاكاة الكلية
st.sidebar.markdown("---")
st.sidebar.subheader("📡 إعدادات المحاكاة الكلية (الأمة)")
W0 = st.sidebar.slider("W (الولاء) - القيمة الابتدائية", 0.0, 1.0, 0.9, 0.05)
B0 = st.sidebar.slider("B (البراءة) - القيمة الابتدائية", 0.0, 1.0, 0.9, 0.05)
E0 = st.sidebar.slider("E (التمكين) - القيمة الابتدائية", 0.0, 1.0, 0.1, 0.05)
lag = st.sidebar.slider("⏳ فجوة الاستدراج (تأخر الأثر)", 0, 50, 20, 1)

st.sidebar.markdown("---")
st.sidebar.subheader("🔬 إعدادات نموذج العوامل (الأفراد)")
pop_size = st.sidebar.slider("عدد الأفراد", 100, 2000, 500, 100)
infection_rate = st.sidebar.slider("قوة التأثر بالبيئة (العدوى الإيمانية)", 0.0, 0.1, 0.02, 0.01)
personal_deviation = st.sidebar.slider("قوة التقلبات الشخصية", 0.0, 0.05, 0.01, 0.005)
laziness = st.sidebar.slider("قوة التراخي (التأثير السلبي للراحة)", 0.0, 0.02, 0.005, 0.001)
sermon_effect = st.sidebar.slider("تأثير خطبة الجمعة (كل 10 سنوات)", 0.0, 0.1, 0.03, 0.01)

# سيناريوهات جاهزة
st.sidebar.markdown("---")
st.sidebar.subheader("🎭 سيناريوهات جاهزة")
scenario = st.sidebar.selectbox(
    "اختر سيناريو:",
    ["مخصص", "أمة صاعدة (قوة إيمانية)", "أمة على حافة الهاوية (تيه وترف)", "مجتمع منقسم (أتقياء ومنافقون)"]
)

if scenario == "أمة صاعدة (قوة إيمانية)":
    W0, B0, E0, lag = 0.9, 0.9, 0.1, 25
elif scenario == "أمة على حافة الهاوية (تيه وترف)":
    W0, B0, E0, lag = 0.3, 0.2, 0.9, 15
elif scenario == "مجتمع منقسم (أتقياء ومنافقون)":
    W0, B0, E0, lag = 0.5, 0.5, 0.5, 10

# ==============================================
# المحاكاة الكلية (محاكي الاستخلاف)
# ==============================================
@st.cache_data
def run_macro(W0, B0, E0, lag, years):
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

# ==============================================
# المحاكاة الجزئية (نموذج العوامل)
# ==============================================
@st.cache_data
def run_micro(pop_size, infection_rate, personal_deviation, laziness, sermon_effect, years):
    GRID = int(np.sqrt(pop_size) * 1.5)
    W = np.random.uniform(0.3, 0.9, pop_size)
    B = np.random.uniform(0.3, 0.9, pop_size)
    pos = np.random.randint(0, GRID, (pop_size, 2))
    history_W, history_B, history_S = [], [], []
    
    for y in range(years):
        dW, dB = np.zeros(pop_size), np.zeros(pop_size)
        for i in range(pop_size):
            dist = np.sqrt(np.sum((pos - pos[i])**2, axis=1))
            neighbors = np.where(dist < 3)[0]
            neighbors = neighbors[neighbors != i]
            local_W = np.mean(W[neighbors]) if len(neighbors) > 0 else W[i]
            local_B = np.mean(B[neighbors]) if len(neighbors) > 0 else B[i]
            dW[i] += infection_rate * (local_W - W[i])
            dB[i] += infection_rate * (local_B - B[i])
            dW[i] += personal_deviation * (np.random.rand() - 0.5)
            if W[i] > 0.7 and B[i] > 0.7:
                dB[i] -= laziness
        W = np.clip(W + dW, 0.0, 1.0)
        B = np.clip(B + dB, 0.0, 1.0)
        pos = pos + np.random.randint(-1, 2, (pop_size, 2))
        pos = np.clip(pos, 0, GRID-1)
        if y % 10 == 0:
            W += sermon_effect * (1 - W)
        history_W.append(np.mean(W))
        history_B.append(np.mean(B))
        history_S.append(np.mean(W * B))
    
    return W, B, pos, history_W, history_B, history_S

# ==============================================
# عرض النتائج حسب الاختيار
# ==============================================
if mode == "📡 محاكي الاستخلاف (الأمة ككل)":
    st.subheader("📡 التلسكوب: رؤية الأمة ككل")
    W, B, S, E = run_macro(W0, B0, E0, lag, years)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    time = np.arange(years)
    
    ax = axes[0,0]
    ax.plot(time, S, 'g-', label='S (الثبات)'); ax.plot(time, E, 'b--', label='E (التمكين)')
    gs = np.argmax(S); ge = np.argmax(E)
    if gs < ge: ax.axvspan(gs, ge, alpha=0.2, color='red', label='منطقة الاستدراج')
    ax.set_title('دورة الحضارة'); ax.legend(); ax.grid(True, alpha=0.3)
    
    ax = axes[0,1]
    ax.plot(time, W, 'darkgreen', label='W (الولاء)'); ax.plot(time, B, 'darkred', label='B (البراءة)')
    ax.set_title('مكونات المعادلة'); ax.legend(); ax.grid(True, alpha=0.3)
    
    ax = axes[1,0]
    H = 10/(S+0.1)
    ax.plot(time, S, 'g-', label='S (الثبات)'); ax.plot(time, H, 'r-', label='H (الهوان)')
    ax.set_title('الثبات والهوان'); ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0,5)
    
    ax = axes[1,1]
    ax.axhline(0.5, color='gray', ls=':'); ax.axvline(0.5, color='gray', ls=':')
    sc = ax.scatter(B, W, c=time, cmap='viridis', s=5)
    ax.plot(B[0], W[0], 'go', ms=8, label='البداية'); ax.plot(B[-1], W[-1], 'ro', ms=8, label='النهاية')
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel('B'); ax.set_ylabel('W')
    ax.set_title('مسار الأمة في (W, B)'); plt.colorbar(sc, ax=ax, label='الزمن')
    ax.legend()
    
    plt.tight_layout(); st.pyplot(fig)

elif mode == "🔬 نموذج العوامل (الأفراد)":
    st.subheader("🔬 الميكروسكوب: رؤية الأفراد وتفاعلاتهم")
    W, B, pos, hW, hB, hS = run_micro(pop_size, infection_rate, personal_deviation, laziness, sermon_effect, years)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    saints = (W>0.7)&(B>0.7)
    hypos = (W<0.3)&(B<0.3)
    others = ~(saints|hypos)
    
    ax = axes[0]
    ax.scatter(pos[saints,0], pos[saints,1], c='green', s=30, alpha=0.7, label='أتقياء')
    ax.scatter(pos[hypos,0], pos[hypos,1], c='red', s=30, alpha=0.7, label='منافقون')
    ax.scatter(pos[others,0], pos[others,1], c='gray', s=10, alpha=0.5, label='عامة')
    ax.set_title(f'خريطة المجتمع (العام {years})'); ax.legend(); ax.grid(False)
    
    ax = axes[1]
    ax.plot(hW, 'g-', label='W'); ax.plot(hB, 'r-', label='B'); ax.plot(hS, 'b-', label='S')
    ax.set_title('تطور متوسطات المجتمع'); ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0,1)
    
    ax = axes[2]
    sc = ax.scatter(B, W, c=W*B, cmap='RdYlGn', s=20, alpha=0.7)
    ax.axhline(0.5, color='gray', ls=':'); ax.axvline(0.5, color='gray', ls=':')
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel('B'); ax.set_ylabel('W')
    ax.set_title('توزيع الأفراد في (W, B)'); plt.colorbar(sc, ax=ax, label='S')
    
    plt.tight_layout(); st.pyplot(fig)
    st.info(f"📊 نسبة الأتقياء: {np.sum(saints)/len(W)*100:.1f}% | نسبة المنافقين: {np.sum(hypos)/len(W)*100:.1f}% | متوسط S: {hS[-1]:.3f}")

elif mode == "🌐 المختبر المتكامل":
    st.subheader("🌐 المختبر المتكامل: رؤية شاملة للأمة والأفراد معًا")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📡 التلسكوب: الأمة ككل")
        W_m, B_m, S_m, E_m = run_macro(W0, B0, E0, lag, years)
        fig, ax = plt.subplots(figsize=(6,4))
        time = np.arange(years)
        ax.plot(time, S_m, 'g-', label='S'); ax.plot(time, E_m, 'b--', label='E')
        gs = np.argmax(S_m); ge = np.argmax(E_m)
        if gs < ge: ax.axvspan(gs, ge, alpha=0.2, color='red')
        ax.set_title('دورة الحضارة'); ax.legend(); ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("### 📈 تطور المكونات")
        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(time, W_m, 'darkgreen', label='W'); ax.plot(time, B_m, 'darkred', label='B')
        ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0,1)
        st.pyplot(fig)
    
    with col2:
        st.markdown("### 🔬 الميكروسكوب: الأفراد")
        W_f, B_f, pos_f, hW, hB, hS = run_micro(pop_size, infection_rate, personal_deviation, laziness, sermon_effect, years)
        fig, ax = plt.subplots(figsize=(6,4))
        saints = (W_f>0.7)&(B_f>0.7)
        hypos = (W_f<0.3)&(B_f<0.3)
        others = ~(saints|hypos)
        ax.scatter(pos_f[saints,0], pos_f[saints,1], c='green', s=20, alpha=0.7, label='أتقياء')
        ax.scatter(pos_f[hypos,0], pos_f[hypos,1], c='red', s=20, alpha=0.7, label='منافقون')
        ax.scatter(pos_f[others,0], pos_f[others,1], c='gray', s=5, alpha=0.5)
        ax.set_title(f'خريطة المجتمع'); ax.legend(); ax.grid(False)
        st.pyplot(fig)
        
        st.markdown("### 📊 توزيع الأفراد في فضاء (W, B)")
        fig, ax = plt.subplots(figsize=(6,4))
        sc = ax.scatter(B_f, W_f, c=W_f*B_f, cmap='RdYlGn', s=20, alpha=0.7)
        ax.axhline(0.5, color='gray', ls=':'); ax.axvline(0.5, color='gray', ls=':')
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel('B'); ax.set_ylabel('W')
        plt.colorbar(sc, ax=ax, label='S')
        st.pyplot(fig)
    
    st.info(f"📊 نسبة الأتقياء: {np.sum(saints)/len(W_f)*100:.1f}% | نسبة المنافقين: {np.sum(hypos)/len(W_f)*100:.1f}% | متوسط S الكلي: {hS[-1]:.3f}")
