"""
==========================================================================
🌌 قمرة القيادة المركزية – المنصة الكونية الكاملة (الإصدار النهائي)
==========================================================================
تجمع كل المراحل: المستشار، لوحة القيادة، مختبر المجتمع، وصراع الحضارات.
تم تعديل دالة المحاكاة لتوضيح "فجوة الاستدراج" بشكل أسرع.
==========================================================================
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# =============================================
# إعداد الصفحة
# =============================================
st.set_page_config(page_title="قمرة القيادة المركزية", page_icon="🌌", layout="wide")
st.title("🌌 قمرة القيادة المركزية – المنصة الكونية الكاملة")
st.markdown("### تجمع كل وحدات المنصة في مكان واحد: المستشار، لوحة القيادة، مختبر المجتمع، وصراع الحضارات")

# =============================================
# دالة المحاكاة المعدلة (لتسريع الاستدراج)
# =============================================
def run_standard_simulation(W0, B0, E0, years=200, lag=25):
    W = np.zeros(years); B = np.zeros(years); S = np.zeros(years); E = np.zeros(years)
    W[0], B[0], E[0] = W0, B0, E0; S[0] = W0 * B0
    for t in range(1, years):
        H = 10 / (S[t-1] + 0.1)
        # تم زيادة معامل الكسل (E) لتسريع انهيار W
        dW = (0.08 * H) - (0.05 * E[t-1]) - (0.04 * (1 - B[t-1]))
        # تم زيادة معامل الترف (E) لتسريع انهيار B
        dB = (-0.04 * E[t-1]) + (0.01 * (1 - B[t-1]) * W[t-1] * (1 - W[t-1]))
        W[t] = max(0.0, min(1.0, W[t-1] + dW))
        B[t] = max(0.0, min(1.0, B[t-1] + dB))
        S[t] = W[t] * B[t]
        past_idx = t - lag
        S_past = S[past_idx] if past_idx >= 0 else S[t]
        dE = 0.05 * (S_past - E[t-1])
        E[t] = max(0.0, min(1.0, E[t-1] + dE))
    return W, B, S, E

# =============================================
# الشريط الجانبي – قائمة الوحدات
# =============================================
st.sidebar.title("🧭 قائمة الوحدات")
module = st.sidebar.radio(
    "اختر الوحدة:",
    ["🏠 القمرة الرئيسية", "🧠 المستشار الدلالي", "🌍 لوحة القيادة الوطنية", "👥 مختبر المجتمع", "⚔️ صراع الحضارات"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("*المنصة الكونية الكاملة – v6.1*")

# =============================================
# الوحدة 0: القمرة الرئيسية (نظرة عامة)
# =============================================
if module == "🏠 القمرة الرئيسية":
    st.header("🏠 مرحبًا بك في قمرة القيادة المركزية")
    st.markdown("""
    ### 🌌 المنصة الكونية الكاملة – نظرية الميزان
    
    هذه هي "غرفة التحكم" النهائية. من هنا، يمكنك الوصول إلى كل وحدات المنصة:
    
    1.  **🧠 المستشار الدلالي**: اسأل أي سؤال عن الحضارة والتاريخ والنفس، وستحصل على إجابة مع محاكاة حية.
    2.  **🌍 لوحة القيادة الوطنية**: أدخل بيانات أي دولة، لترى موقعها على خريطة الاستدراج وتوقعات مستقبلها.
    3.  **👥 مختبر المجتمع**: شاهد كيف يتفاعل 500 فرد في مجتمع واحد، وكيف ينتشر الخير والشر.
    4.  **⚔️ صراع الحضارات**: عالم افتراضي يضم 6 دول، تتحارب وتتحالف وتغزو بعضها ثقافيًا.
    
    ---
    ### 📊 معادلة اليوم: S = W × B
    
    **S** = الثبات الوجودي (الطمأنينة والعزة والتمكين).
    **W** = الولاء لله (الإيمان والعمل الصالح والعدل).
    **B** = البراءة من الطاغوت (الجهاد والعفة والاستقلال).
    
    إنها معادلة **ضربية**. إذا كان أحد طرفيها صفرًا، كان الثبات معدومًا.
    """)
    
    # رسم توضيحي سريع للمعادلة
    col1, col2, col3 = st.columns(3)
    with col1:
        W_demo = st.slider("W (الولاء)", 0.0, 1.0, 0.8, 0.05, key="demo_W")
    with col2:
        B_demo = st.slider("B (البراءة)", 0.0, 1.0, 0.8, 0.05, key="demo_B")
    with col3:
        S_demo = W_demo * B_demo
        st.metric("S (الثبات)", f"{S_demo:.2f}")
    
    W_s, B_s, S_s, E_s = run_standard_simulation(W_demo, B_demo, 0.3, years=150)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(S_s, 'g-', linewidth=2, label='S (الثبات)')
    ax.plot(E_s, 'b--', linewidth=2, label='E (التمكين)')
    ax.set_title('منحنى توضيحي: دورة الحضارة')
    ax.legend(); ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# =============================================
# الوحدة 1: المستشار الدلالي
# =============================================
elif module == "🧠 المستشار الدلالي":
    st.header("🧠 المستشار الدلالي")
    
    QA_DB = {
        "معادلة": "معادلة الثبات الوجودي هي S = W × B. حيث S هو الثبات، W هو الولاء لله، و B هو البراءة من الطاغوت. إنها معادلة ضربية: إذا كان أحد طرفيها صفرًا، كان الثبات معدومًا.",
        "استدراج": "الاستدراج هو أن يُملي الله للظالمين، فيمدهم في طغيانهم، ثم يأخذهم بغتة. في النموذج: ينهار S بينما E ما زال مرتفعًا. هذا يفسر لماذا تنهار الحضارات فجأة بعد قرون من القوة.",
        "حضارة": "دورة الحضارة: صعود (ارتفاع W وB)، ذروة، استدراج (انهيار S مع بقاء E)، انهيار (سقوط E). كل الحضارات التي قامت على 'الولاء لله' و'البراءة من الطاغوت' صمدت وتمكنت. وكل الحضارات التي فرطت في W أو B انهارت.",
    }
    
    user_q = st.text_input("✍️ اسأل المستشار:", placeholder="مثال: ما هو الاستدراج؟")
    
    if user_q:
        found = False
        for key, ans in QA_DB.items():
            if key in user_q:
                st.info(f"💡 {ans}")
                found = True
                if "استدراج" in user_q:
                    W0, B0, E0 = 0.3, 0.3, 0.9
                elif "صاعد" in user_q or "قوة" in user_q:
                    W0, B0, E0 = 0.9, 0.9, 0.1
                else:
                    W0, B0, E0 = 0.5, 0.5, 0.3
                
                W_s, B_s, S_s, E_s = run_standard_simulation(W0, B0, E0)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(S_s, 'g-', label='S'); ax.plot(E_s, 'b--', label='E')
                ax.set_title('محاكاة حية'); ax.legend(); ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                break
        if not found:
            st.warning("لم أجد إجابة محددة. جرب كلمات مثل: معادلة، استدراج، حضارة.")

# =============================================
# الوحدة 2: لوحة القيادة الوطنية
# =============================================
elif module == "🌍 لوحة القيادة الوطنية":
    st.header("🌍 لوحة القيادة الوطنية – التوأم الرقمي")
    
    col1, col2 = st.columns(2)
    with col1:
        rule_of_law = st.slider("سيادة القانون", 0.0, 1.0, 0.5, 0.05)
        education = st.slider("التعليم والقيم", 0.0, 1.0, 0.5, 0.05)
        family = st.slider("الاستقرار الأسري", 0.0, 1.0, 0.5, 0.05)
    with col2:
        corruption = st.slider("مكافحة الفساد", 0.0, 1.0, 0.5, 0.05)
        justice = st.slider("العدل والمساواة", 0.0, 1.0, 0.5, 0.05)
        economic = st.slider("القوة الاقتصادية", 0.0, 1.0, 0.6, 0.05)
    
    W0 = (rule_of_law + education + family) / 3
    B0 = (corruption + justice + rule_of_law) / 3
    E0 = economic
    S0 = W0 * B0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("W", f"{W0:.2f}"); col2.metric("B", f"{B0:.2f}"); col3.metric("S", f"{S0:.2f}")
    
    if st.button("شغّل المحاكاة", type="primary"):
        W_s, B_s, S_s, E_s = run_standard_simulation(W0, B0, E0, years=100)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes[0].plot(S_s, 'g-', label='S'); axes[0].plot(E_s, 'b--', label='E')
        axes[0].set_title('توقعات المستقبل'); axes[0].legend(); axes[0].grid(True, alpha=0.3)
        axes[1].scatter(B0, W0, s=400, c='red', edgecolors='black')
        axes[1].axhline(0.5, color='gray', ls=':'); axes[1].axvline(0.5, color='gray', ls=':')
        axes[1].set_xlim(0, 1); axes[1].set_ylim(0, 1)
        axes[1].set_xlabel('B'); axes[1].set_ylabel('W')
        axes[1].set_title('موقع الدولة الآن')
        plt.tight_layout(); st.pyplot(fig)

# =============================================
# الوحدة 3: مختبر المجتمع
# =============================================
elif module == "👥 مختبر المجتمع":
    st.header("👥 مختبر المجتمع – نموذج العوامل")
    
    pop_size = st.slider("عدد الأفراد", 100, 500, 300, 50)
    influence = st.slider("نصف قطر التأثير", 1.0, 4.0, 2.5, 0.5)
    
    if st.button("▶️ شغّل", type="primary"):
        W = np.random.uniform(0.3, 0.9, pop_size)
        B = np.random.uniform(0.3, 0.9, pop_size)
        px = np.random.randint(0, 30, pop_size)
        py = np.random.randint(0, 30, pop_size)
        
        for step in range(50):
            for i in range(pop_size):
                dist = np.sqrt((px - px[i])**2 + (py - py[i])**2)
                neighbors = np.where(dist < influence)[0]
                neighbors = neighbors[neighbors != i]
                if len(neighbors) > 0:
                    W[i] += 0.02 * (np.mean(W[neighbors]) - W[i])
                    B[i] += 0.02 * (np.mean(B[neighbors]) - B[i])
                W[i] = max(0.05, min(1.0, W[i] + 0.01*(np.random.rand()-0.5)))
                B[i] = max(0.05, min(1.0, B[i] + 0.01*(np.random.rand()-0.5)))
            px = np.clip(px + np.random.randint(-1, 2, pop_size), 0, 29)
            py = np.clip(py + np.random.randint(-1, 2, pop_size), 0, 29)
        
        saints = (W > 0.6) & (B > 0.6)
        hypos = (W < 0.4) & (B < 0.4)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.scatter(px[saints], py[saints], c='green', s=30, alpha=0.7, label='أتقياء')
        ax.scatter(px[hypos], py[hypos], c='red', s=30, alpha=0.7, label='منافقون')
        ax.scatter(px[~(saints|hypos)], py[~(saints|hypos)], c='gray', s=15, alpha=0.5)
        ax.set_title(f'خريطة المجتمع (بعد 50 سنة) – أتقياء: {np.sum(saints)} | منافقون: {np.sum(hypos)}')
        ax.legend(); ax.set_xlim(0, 29); ax.set_ylim(0, 29)
        st.pyplot(fig)

# =============================================
# الوحدة 4: صراع الحضارات
# =============================================
elif module == "⚔️ صراع الحضارات":
    st.header("⚔️ محاكاة صراع الحضارات")
    
    countries = [
        {"name": "دولة الإيمان", "W": 0.9, "B": 0.9, "E": 0.1, "color": "green", "hist_S": [], "hist_E": []},
        {"name": "دولة الترف", "W": 0.3, "B": 0.2, "E": 0.9, "color": "gold", "hist_S": [], "hist_E": []},
        {"name": "دولة النفاق", "W": 0.5, "B": 0.5, "E": 0.5, "color": "gray", "hist_S": [], "hist_E": []},
        {"name": "الإمبراطورية", "W": 0.1, "B": 0.9, "E": 0.85, "color": "red", "hist_S": [], "hist_E": []},
        {"name": "دولة العلم", "W": 0.8, "B": 0.6, "E": 0.4, "color": "cyan", "hist_S": [], "hist_E": []},
        {"name": "دولة التبعية", "W": 0.6, "B": 0.15, "E": 0.3, "color": "orange", "hist_S": [], "hist_E": []},
    ]
    
    if st.button("▶️ شغّل", type="primary"):
        years = 80
        for y in range(years):
            for c in countries:
                W, B, E = c['W'], c['B'], c['E']
                S = W * B; H = 10/(S+0.1)
                dW = 0.08*H - 0.05*E - 0.04*(1-B)
                dB = -0.04*E + 0.01*(1-B)*W*(1-W)
                W = max(0.01, min(1.0, W + dW))
                B = max(0.01, min(1.0, B + dB))
                E = max(0.01, min(1.0, E + 0.05*(S - E)))
                
                for o in countries:
                    if o['name'] == c['name']: continue
                    oS = o['W'] * o['B']
                    if abs(S - oS) > 0.5 and o['B'] > 0.7 and B < 0.4:
                        E -= 0.05; B -= 0.03
                    if o['E'] > 0.7 and B < 0.6:
                        B -= 0.02; W -= 0.01
                
                c['W'], c['B'], c['E'] = W, B, E
                c['hist_S'].append(W*B); c['hist_E'].append(E)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        for c in countries:
            axes[0].plot(c['hist_S'], color=c['color'], linewidth=2, label=c['name'])
            axes[1].plot(c['hist_E'], color=c['color'], linewidth=2, linestyle='--', label=c['name'])
        axes[0].set_title('منحنيات الثبات (S)'); axes[0].legend(fontsize=7); axes[0].grid(True, alpha=0.3)
        axes[1].set_title('منحنيات التمكين (E)'); axes[1].legend(fontsize=7); axes[1].grid(True, alpha=0.3)
        plt.tight_layout(); st.pyplot(fig)

st.markdown("---")
st.markdown("*قمرة القيادة المركزية – المنصة الكونية الكاملة v6.1*")
