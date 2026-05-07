import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="المختبر المتكامل - نهائي", layout="wide")
st.title("🌌 المختبر المتكامل: محاكي الاستخلاف + نموذج العوامل + تشخيص الدولة")
st.markdown("هذا المختبر يجمع بين التلسكوب والميكروسكوب وأداة تشخيص الدول.")

mode = st.sidebar.radio("اختر المحاكاة:", ["📡 محاكي الاستخلاف (الأمة ككل)", "🔬 نموذج العوامل (الأفراد)", "🌐 المختبر المتكامل", "🏛️ مختبر تشخيص الدولة"])

# ==============================================
# دوال المحاكاة
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

@st.cache_data
def run_micro(pop_size, infection_rate, personal_deviation, laziness, sermon_effect, years):
    GRID = int(np.sqrt(pop_size) * 1.5)
    W = np.random.uniform(0.3, 0.9, pop_size)
    B = np.random.uniform(0.3, 0.9, pop_size)
    pos = np.random.randint(0, GRID, (pop_size, 2))
    hW, hB, hS = [], [], []
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
            if W[i] > 0.7 and B[i] > 0.7: dB[i] -= laziness
        W = np.clip(W + dW, 0.0, 1.0)
        B = np.clip(B + dB, 0.0, 1.0)
        pos = pos + np.random.randint(-1, 2, (pop_size, 2))
        pos = np.clip(pos, 0, GRID-1)
        if y % 10 == 0: W += sermon_effect * (1 - W)
        hW.append(np.mean(W)); hB.append(np.mean(B)); hS.append(np.mean(W*B))
    return W, B, pos, hW, hB, hS

def diagnose_country(rule_of_law, corruption, family_stability, debt_to_gdp, political_indep, military_indep):
    W = (rule_of_law + (1-corruption) + family_stability) / 3
    B = ((1-debt_to_gdp) + political_indep + military_indep) / 3
    S = W * B
    if S > 0.7: status, advice = "🟢 أمة في مرحلة الصعود والقوة", "حافظ على W وB مرتفعين. احذر من فتنة المال والترف."
    elif S > 0.4: status, advice = "🟡 أمة في مرحلة التوازن الهش", "أنت في مفترق طرق. قوِّ B فورًا بتقليل الديون وزيادة الاستقلال."
    elif S > 0.2: status, advice = "🟠 أمة في بداية منطقة الاستدراج", "خطر! التمكين المادي (E) قد يبدو مرتفعًا، لكن الانهيار قادم."
    else: status, advice = "🔴 أمة على حافة الهاوية", "الانهيار وشيك. لا يتبقى إلا التوبة النصوح والرجوع الكامل لله."
    return W, B, S, status, advice

# ==============================================
# واجهة كل وضع
# ==============================================
if mode == "📡 محاكي الاستخلاف (الأمة ككل)":
    st.sidebar.subheader("📊 إعدادات")
    years = st.sidebar.slider("سنوات المحاكاة", 50, 500, 200, 50)
    W0 = st.sidebar.slider("W الابتدائي", 0.0, 1.0, 0.9, 0.05)
    B0 = st.sidebar.slider("B الابتدائي", 0.0, 1.0, 0.9, 0.05)
    E0 = st.sidebar.slider("E الابتدائي", 0.0, 1.0, 0.1, 0.05)
    lag = st.sidebar.slider("فجوة الاستدراج", 0, 50, 20, 1)
    W, B, S, E = run_macro(W0, B0, E0, lag, years)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    time = np.arange(years)
    ax = axes[0,0]; ax.plot(time, S, 'g-', label='S'); ax.plot(time, E, 'b--', label='E')
    gs, ge = np.argmax(S), np.argmax(E)
    if gs < ge: ax.axvspan(gs, ge, alpha=0.2, color='red', label='الاستدراج')
    ax.set_title('دورة الحضارة'); ax.legend(); ax.grid(True, alpha=0.3)
    ax = axes[0,1]; ax.plot(time, W, 'darkgreen', label='W'); ax.plot(time, B, 'darkred', label='B')
    ax.set_title('مكونات المعادلة'); ax.legend(); ax.grid(True, alpha=0.3)
    ax = axes[1,0]; H = 10/(S+0.1); ax.plot(time, S, 'g-'); ax.plot(time, H, 'r-')
    ax.set_title('الثبات والهوان'); ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0,5)
    ax = axes[1,1]; ax.axhline(0.5, color='gray', ls=':'); ax.axvline(0.5, color='gray', ls=':')
    sc = ax.scatter(B, W, c=time, cmap='viridis', s=5)
    ax.plot(B[0], W[0], 'go', ms=8); ax.plot(B[-1], W[-1], 'ro', ms=8)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel('B'); ax.set_ylabel('W')
    ax.set_title('مسار الأمة في (W, B)'); plt.colorbar(sc, ax=ax, label='الزمن')
    plt.tight_layout(); st.pyplot(fig)

elif mode == "🔬 نموذج العوامل (الأفراد)":
    st.sidebar.subheader("📊 إعدادات")
    years = st.sidebar.slider("سنوات المحاكاة", 50, 500, 200, 50)
    pop_size = st.sidebar.slider("عدد الأفراد", 100, 2000, 500, 100)
    infection_rate = st.sidebar.slider("العدوى الإيمانية", 0.0, 0.1, 0.02, 0.01)
    personal_deviation = st.sidebar.slider("التقلبات الشخصية", 0.0, 0.05, 0.01, 0.005)
    laziness = st.sidebar.slider("التراخي", 0.0, 0.02, 0.005, 0.001)
    sermon_effect = st.sidebar.slider("تأثير التذكير", 0.0, 0.1, 0.03, 0.01)
    W, B, pos, hW, hB, hS = run_micro(pop_size, infection_rate, personal_deviation, laziness, sermon_effect, years)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    saints = (W>0.7)&(B>0.7); hypos = (W<0.3)&(B<0.3); others = ~(saints|hypos)
    ax = axes[0]; ax.scatter(pos[saints,0], pos[saints,1], c='green', s=30, alpha=0.7, label='أتقياء')
    ax.scatter(pos[hypos,0], pos[hypos,1], c='red', s=30, alpha=0.7, label='منافقون')
    ax.scatter(pos[others,0], pos[others,1], c='gray', s=10, alpha=0.5, label='عامة')
    ax.set_title(f'خريطة المجتمع (العام {years})'); ax.legend(); ax.grid(False)
    ax = axes[1]; ax.plot(hW, 'g-', label='W'); ax.plot(hB, 'r-', label='B'); ax.plot(hS, 'b-', label='S')
    ax.set_title('تطور متوسطات المجتمع'); ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0,1)
    ax = axes[2]; sc = ax.scatter(B, W, c=W*B, cmap='RdYlGn', s=20, alpha=0.7)
    ax.axhline(0.5, color='gray', ls=':'); ax.axvline(0.5, color='gray', ls=':')
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel('B'); ax.set_ylabel('W')
    ax.set_title('توزيع الأفراد في (W, B)'); plt.colorbar(sc, ax=ax, label='S')
    plt.tight_layout(); st.pyplot(fig)
    st.info(f"نسبة الأتقياء: {np.sum(saints)/len(W)*100:.1f}% | نسبة المنافقين: {np.sum(hypos)/len(W)*100:.1f}% | متوسط S: {hS[-1]:.3f}")

elif mode == "🌐 المختبر المتكامل":
    st.sidebar.subheader("📊 إعدادات")
    years = st.sidebar.slider("سنوات المحاكاة", 50, 500, 200, 50)
    W0 = st.sidebar.slider("W الابتدائي", 0.0, 1.0, 0.9, 0.05)
    B0 = st.sidebar.slider("B الابتدائي", 0.0, 1.0, 0.9, 0.05)
    E0 = st.sidebar.slider("E الابتدائي", 0.0, 1.0, 0.1, 0.05)
    lag = st.sidebar.slider("فجوة الاستدراج", 0, 50, 20, 1)
    pop_size = st.sidebar.slider("عدد الأفراد", 100, 1000, 500, 100)
    W_m, B_m, S_m, E_m = run_macro(W0, B0, E0, lag, years)
    W_f, B_f, pos_f, hW, hB, hS = run_micro(pop_size, 0.02, 0.01, 0.005, 0.03, years)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📡 التلسكوب")
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(S_m, 'g-', label='S'); ax.plot(E_m, 'b--', label='E')
        gs, ge = np.argmax(S_m), np.argmax(E_m)
        if gs < ge: ax.axvspan(gs, ge, alpha=0.2, color='red')
        ax.set_title('دورة الحضارة'); ax.legend(); ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    with col2:
        st.subheader("🔬 الميكروسكوب")
        fig, ax = plt.subplots(figsize=(6,4))
        saints = (W_f>0.7)&(B_f>0.7); hypos = (W_f<0.3)&(B_f<0.3); others = ~(saints|hypos)
        ax.scatter(pos_f[saints,0], pos_f[saints,1], c='green', s=20, alpha=0.7)
        ax.scatter(pos_f[hypos,0], pos_f[hypos,1], c='red', s=20, alpha=0.7)
        ax.scatter(pos_f[others,0], pos_f[others,1], c='gray', s=5, alpha=0.5)
        ax.set_title(f'خريطة المجتمع'); ax.grid(False)
        st.pyplot(fig)
    st.info(f"نسبة الأتقياء: {np.sum(saints)/len(W_f)*100:.1f}% | نسبة المنافقين: {np.sum(hypos)/len(W_f)*100:.1f}% | متوسط S الكلي: {hS[-1]:.3f}")

elif mode == "🏛️ مختبر تشخيص الدولة":
    st.header("🏛️ مختبر تشخيص الدولة")
    st.markdown("أدخل بيانات تقريبية عن أي دولة لترى أين تقع على خريطة الاستدراج.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("مؤشرات W (الولاء)")
        rule_of_law = st.slider("سيادة القانون (1=قوي)", 0.0, 1.0, 0.5, 0.05)
        corruption = st.slider("مؤشر الفساد (1=فاسد)", 0.0, 1.0, 0.5, 0.05)
        family_stability = st.slider("التماسك الأسري (1=قوي)", 0.0, 1.0, 0.5, 0.05)
    with col2:
        st.subheader("مؤشرات B (البراءة)")
        debt_to_gdp = st.slider("نسبة الدين (1=مديون بالكامل)", 0.0, 1.0, 0.5, 0.05)
        political_indep = st.slider("الاستقلال السياسي (1=مستقل)", 0.0, 1.0, 0.5, 0.05)
        military_indep = st.slider("الاستقلال العسكري (1=مستقل)", 0.0, 1.0, 0.5, 0.05)
    if st.button("شخّص الدولة", type="primary"):
        W, B, S, status, advice = diagnose_country(rule_of_law, corruption, family_stability, debt_to_gdp, political_indep, military_indep)
        col1, col2, col3 = st.columns(3)
        col1.metric("W (الولاء)", f"{W:.2f}")
        col2.metric("B (البراءة)", f"{B:.2f}")
        col3.metric("S (الثبات)", f"{S:.2f}")
        st.info(status)
        st.warning(advice)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.axhline(0.5, color='gray', ls=':'); ax.axvline(0.5, color='gray', ls=':')
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel('B (البراءة)'); ax.set_ylabel('W (الولاء)')
        ax.scatter(B, W, s=500, c='red', edgecolors='black', linewidth=2, zorder=5)
        ax.text(B+0.05, W+0.05, 'موقع الدولة', fontsize=12)
        ax.set_title('موقع الدولة في فضاء (W, B)')
        st.pyplot(fig)
