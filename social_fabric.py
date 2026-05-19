# mizan/social_fabric.py
"""
النسيج الاجتماعي – المجتمع كخلية حية
محاكاة بصرية للعلاقات بين الأفراد بناءً على توازن W و B
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
from config import TXT

def render_social_fabric():
    st.header(TXT("🤝 النسيج الاجتماعي – المجتمع كخلية حية", "🤝 Social Fabric – Society as a Living Cell"))
    st.caption(TXT(
        "شاهد كيف تتشكل العلاقات بين الأفراد (النجوم) بناءً على درجة توازنهم في W و B. "
        "المتقاربون يتجاذبون، والمتنافرون يتباعدون. ﴿إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ﴾",
        "Watch how relationships form between individuals (stars) based on their balance in W and B. "
        "Those close attract, and those opposed repel."
    ))

    # ─────────────────────────────────────────
    # إعدادات المحاكاة
    # ─────────────────────────────────────────
    st.subheader(TXT("🎛️ إعدادات النسيج", "🎛️ Fabric Settings"))
    c1, c2, c3 = st.columns(3)
    with c1:
        n_people = st.slider(TXT("عدد الأفراد", "Number of People"), 20, 100, 50, 5, key="sf_people")
    with c2:
        avg_W = st.slider(TXT("متوسط W (الولاء)", "Average W (Loyalty)"), 0.0, 1.0, 0.55, 0.05, key="sf_W")
    with c3:
        avg_B = st.slider(TXT("متوسط B (البراءة)", "Average B (Disavowal)"), 0.0, 1.0, 0.52, 0.05, key="sf_B")

    c4, c5 = st.columns(2)
    with c4:
        spread = st.slider(TXT("درجة التشتت", "Spread"), 0.01, 0.3, 0.1, 0.01, key="sf_spread")
    with c5:
        attraction_strength = st.slider(TXT("قوة التجاذب", "Attraction Strength"), 0.0, 0.1, 0.03, 0.01, key="sf_attract")

    # ─────────────────────────────────────────
    # توليد المجتمع
    # ─────────────────────────────────────────
    if st.button(TXT("▶️ توليد / تحديث المجتمع", "▶️ Generate / Update Society"), use_container_width=True, type="primary"):
        np.random.seed(42)
        random.seed(42)
        
        # توليد الأفراد
        W_vals = np.clip(np.random.normal(avg_W, spread, n_people), 0.01, 1.0)
        B_vals = np.clip(np.random.normal(avg_B, spread, n_people), 0.01, 1.0)
        S_vals = W_vals * B_vals
        
        # توليد مواقع عشوائية
        positions = np.random.uniform(0, 10, (n_people, 2))
        
        # محاكاة التجاذب والتنافر (خطوات قليلة للتوضيح)
        for _ in range(20):
            for i in range(n_people):
                for j in range(i+1, n_people):
                    diff = positions[j] - positions[i]
                    dist = np.linalg.norm(diff)
                    if dist < 0.01: dist = 0.01
                    
                    # حساب "التوافق" بين الشخصين
                    compatibility = 1 - abs(S_vals[i] - S_vals[j])
                    
                    # إذا كانا متوافقين (متقاربين في S): يتجاذبان
                    # إذا كانا غير متوافقين (متباعدين في S): يتنافران
                    force = attraction_strength * (compatibility - 0.5) * 2
                    
                    direction = diff / dist
                    positions[i] += direction * force
                    positions[j] -= direction * force
            
            # إبقاء الأفراد داخل الحدود
            positions = np.clip(positions, 0, 10)
        
        # تخزين النتائج
        st.session_state.sf_positions = positions
        st.session_state.sf_W_vals = W_vals
        st.session_state.sf_B_vals = B_vals
        st.session_state.sf_S_vals = S_vals
        st.session_state.sf_generated = True

    # ─────────────────────────────────────────
    # عرض النسيج
    # ─────────────────────────────────────────
    if st.session_state.get("sf_generated", False):
        positions = st.session_state.sf_positions
        W_vals = st.session_state.sf_W_vals
        B_vals = st.session_state.sf_B_vals
        S_vals = st.session_state.sf_S_vals
        
        # الألوان حسب الثبات
        def get_social_color(S):
            if S >= 0.7: return '#FFD700'      # ثبات عالي – ذهبي
            elif S >= 0.5: return '#00FF88'    # ثبات متوسط – أخضر
            elif S >= 0.3: return '#FFA500'    # ضعيف – برتقالي
            else: return '#FF4444'             # منهار – أحمر

        colors = [get_social_color(s) for s in S_vals]
        sizes = 50 + S_vals * 300  # حجم النجمة يعكس S

        # رسم النسيج
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.set_xlim(0, 10); ax.set_ylim(0, 10)
        ax.axis('off')

        # رسم خطوط الوصل (العلاقات) بين المتقاربين
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                dist = np.linalg.norm(positions[j] - positions[i])
                compatibility = 1 - abs(S_vals[i] - S_vals[j])
                if compatibility > 0.7 and dist < 2.0:
                    alpha = 0.1 + 0.5 * compatibility
                    ax.plot([positions[i,0], positions[j,0]], [positions[i,1], positions[j,1]],
                           color='#FFD700', alpha=alpha, lw=0.5)

        # رسم الأفراد (النجوم)
        ax.scatter(positions[:,0], positions[:,1], s=sizes, c=colors, alpha=0.9,
                  edgecolors='white', linewidths=0.5, zorder=5)

        ax.set_title(TXT("النسيج الاجتماعي – العلاقات بين الأفراد",
                        "Social Fabric – Relationships Between Individuals"),
                    color='white', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

        # ─────────────────────────────────────────
        # إحصائيات المجتمع
        # ─────────────────────────────────────────
        st.markdown("---")
        st.subheader(TXT("📊 إحصائيات المجتمع", "📊 Community Statistics"))
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric(TXT("متوسط W", "Avg W"), f"{np.mean(W_vals):.2f}")
        col_s2.metric(TXT("متوسط B", "Avg B"), f"{np.mean(B_vals):.2f}")
        col_s3.metric(TXT("متوسط S", "Avg S"), f"{np.mean(S_vals):.2f}")
        col_s4.metric(TXT("عدد الأفراد", "Individuals"), n_people)

        # توزيع الأفراد على الفئات
        high_S = np.sum(S_vals >= 0.7)
        mid_S = np.sum((S_vals >= 0.5) & (S_vals < 0.7))
        low_S = np.sum((S_vals >= 0.3) & (S_vals < 0.5))
        col_S = np.sum(S_vals < 0.3)

        st.markdown(f"""
        <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;margin:10px 0;">
            <p>🟡 <b>{TXT('ثبات عالي', 'High Stability')} (S ≥ 0.7):</b> {high_S} {TXT('فرداً', 'individuals')} ({100*high_S/n_people:.0f}%)</p>
            <p>🟢 <b>{TXT('ثبات متوسط', 'Medium Stability')} (0.5 ≤ S < 0.7):</b> {mid_S} {TXT('فرداً', 'individuals')} ({100*mid_S/n_people:.0f}%)</p>
            <p>🟠 <b>{TXT('ثبات ضعيف', 'Low Stability')} (0.3 ≤ S < 0.5):</b> {low_S} {TXT('فرداً', 'individuals')} ({100*low_S/n_people:.0f}%)</p>
            <p>🔴 <b>{TXT('منهار', 'Collapsed')} (S < 0.3):</b> {col_S} {TXT('فرداً', 'individuals')} ({100*col_S/n_people:.0f}%)</p>
        </div>
        """, unsafe_allow_html=True)

        # خلاصة تحليلية
        if np.mean(S_vals) > 0.7:
            st.success(TXT("✅ مجتمع متماسك. الثبات عالٍ، والعلاقات قوية بين الأفراد.", "✅ Cohesive society. High stability, strong relationships."))
        elif np.mean(S_vals) > 0.5:
            st.info(TXT("ℹ️ مجتمع متوسط التماسك. توجد بؤر ضعف تحتاج إلى تقوية.", "ℹ️ Moderately cohesive society. Some weak spots need strengthening."))
        elif np.mean(S_vals) > 0.3:
            st.warning(TXT("⚠️ مجتمع متفكك. فجوة الاستدراج واضحة. العلاقات ضعيفة.", "⚠️ Fragmented society. Clear Istidraj gap. Weak relationships."))
        else:
            st.error(TXT("🚨 مجتمع منهار. الثبات شبه معدوم. لا توجد روابط تذكر.", "🚨 Collapsed society. Stability nearly nonexistent. No significant bonds."))
