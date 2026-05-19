# mizan/civilization_cycle.py
"""
محاكي الدورة الحضارية
من الفطرة إلى الخلود: صعود، استدراج، انهيار
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from config import TXT

# =============================================
# مراحل الدورة
# =============================================
CYCLE_STAGES = [
    {"name": TXT("الفطرة", "Fitrah"), "range": (0.9, 1.0), "color": "#FFD700",
     "desc": TXT("الأمة في أصلها الفطري. W وB في ذروتهما. الثبات تام.", "The nation at its pure origin. W and B at peak. Perfect stability.")},
    {"name": TXT("الصعود", "Rise"), "range": (0.7, 0.9), "color": "#00FF88",
     "desc": TXT("الأمة تصعد بقوة الإيمان والعمل الصالح. التمكين يتبع الثبات.", "The nation rises with faith and righteous deeds. Empowerment follows stability.")},
    {"name": TXT("الذروة", "Peak"), "range": (0.5, 0.7), "color": "#00BFFF",
     "desc": TXT("ذروة القوة المادية. لكن الفجوة بين E وS تبدأ بالظهور.", "Peak of material power. But the gap between E and S begins to appear.")},
    {"name": TXT("الاستدراج", "Istidraj"), "range": (0.3, 0.5), "color": "#FFA500",
     "desc": TXT("التمكين المادي يتجاوز الثبات الأخلاقي. فجوة خطيرة. ﴿سَنَسْتَدْرِجُهُم مِّنْ حَيْثُ لَا يَعْلَمُونَ﴾", "Material empowerment exceeds moral stability. Dangerous gap.")},
    {"name": TXT("الانهيار", "Collapse"), "range": (0.0, 0.3), "color": "#FF4444",
     "desc": TXT("انهيار الثبات الأخلاقي يؤدي إلى انهيار الحضارة. ﴿فَكُلًّا أَخَذْنَا بِذَنبِهِ﴾", "Collapse of moral stability leads to civilizational collapse.")},
]

def get_stage(S):
    for stage in CYCLE_STAGES:
        low, high = stage["range"]
        if low <= S < high or (S == 1.0 and low == 0.9):
            return stage
    return CYCLE_STAGES[-1]

def render_civilization_cycle():
    st.header(TXT("🔄 محاكي الدورة الحضارية", "🔄 Civilization Cycle Simulator"))
    st.caption(TXT(
        "شاهد كيف تمر الأمة بمراحل الصعود والذروة والاستدراج والانهيار بناءً على تغير W و B. ﴿وَتِلْكَ الْأَيَّامُ نُدَاوِلُهَا بَيْنَ النَّاسِ﴾",
        "Watch how a nation passes through stages of rise, peak, istidraj, and collapse based on changes in W and B."
    ))

    # ─────────────────────────────────────────
    # منزلقات التحكم
    # ─────────────────────────────────────────
    st.subheader(TXT("🎛️ إعدادات الأمة", "🎛️ Nation Settings"))
    c1, c2, c3 = st.columns(3)
    with c1:
        W_init = st.slider(TXT("W الابتدائي (الولاء)", "Initial W (Loyalty)"), 0.0, 1.0, 0.95, 0.05, key="cc_W")
    with c2:
        B_init = st.slider(TXT("B الابتدائي (البراءة)", "Initial B (Disavowal)"), 0.0, 1.0, 0.95, 0.05, key="cc_B")
    with c3:
        E_init = st.slider(TXT("E الابتدائي (التمكين)", "Initial E (Empowerment)"), 0.0, 1.0, 0.3, 0.05, key="cc_E")

    c4, c5 = st.columns(2)
    with c4:
        decay_rate = st.slider(TXT("معدل الانحلال (ضعف W وB)", "Decay Rate (weakening of W & B)"), 0.0, 0.05, 0.01, 0.005, key="cc_decay")
    with c5:
        years = st.slider(TXT("عدد السنوات للمحاكاة", "Years to Simulate"), 50, 500, 200, 50, key="cc_years")

    # ─────────────────────────────────────────
    # أزرار التحكم
    # ─────────────────────────────────────────
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        run_sim = st.button(TXT("▶️ تشغيل المحاكاة", "▶️ Run Simulation"), use_container_width=True, type="primary")
    with c_btn2:
        if st.button(TXT("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
            st.rerun()

    # ─────────────────────────────────────────
    # تشغيل المحاكاة
    # ─────────────────────────────────────────
    if run_sim:
        W_vals = [W_init]
        B_vals = [B_init]
        E_vals = [E_init]
        S_vals = [W_init * B_init]
        stages_history = [get_stage(S_vals[0])["name"]]

        for t in range(1, years):
            # تآكل W وB بسبب الترف والفساد (إذا كان E مرتفعاً)
            if E_vals[-1] > S_vals[-1] + 0.2:  # فجوة استدراج
                W_vals.append(max(0.01, W_vals[-1] - decay_rate * 1.5))
                B_vals.append(max(0.01, B_vals[-1] - decay_rate * 1.5))
            elif E_vals[-1] > S_vals[-1] + 0.1:
                W_vals.append(max(0.01, W_vals[-1] - decay_rate))
                B_vals.append(max(0.01, B_vals[-1] - decay_rate))
            else:
                W_vals.append(max(0.01, W_vals[-1] - decay_rate * 0.3))
                B_vals.append(max(0.01, B_vals[-1] - decay_rate * 0.3))

            nS = W_vals[-1] * B_vals[-1]
            S_vals.append(nS)
            # التمكين يتأخر عن الثبات
            nE = E_vals[-1] + 0.05 * (S_vals[-2] - E_vals[-1])
            E_vals.append(max(0.01, nE))
            stages_history.append(get_stage(nS)["name"])

        # ─────────────────────────────────────────
        # الرسم البياني
        # ─────────────────────────────────────────
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), facecolor='#0a0f1e')

        # المخطط 1: S وE عبر الزمن
        ax1.set_facecolor('#0a0f1e')
        ax1.plot(S_vals, label='S (الثبات)', color='#FFD700', lw=2)
        ax1.plot(E_vals, label='E (التمكين)', color='#0FF', lw=1.5, ls='--')
        ax1.fill_between(range(years), S_vals, E_vals,
                        where=(np.array(E_vals) > np.array(S_vals)),
                        color='red', alpha=0.2, label=TXT('فجوة الاستدراج', 'Istidraj Gap'))
        ax1.set_xlabel(TXT('السنوات', 'Years'), color='white')
        ax1.set_ylabel(TXT('القيمة', 'Value'), color='white')
        ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
        ax1.tick_params(colors='white')
        ax1.grid(True, alpha=0.2)
        ax1.set_title(TXT('مسار الأمة عبر الزمن', 'Nation Path Over Time'), color='white', fontsize=13)

        # المخطط 2: خريطة المراحل (ملونة)
        ax2.set_facecolor('#0a0f1e')
        stage_colors = {'الفطرة': '#FFD700', 'Fitrah': '#FFD700',
                       'الصعود': '#00FF88', 'Rise': '#00FF88',
                       'الذروة': '#00BFFF', 'Peak': '#00BFFF',
                       'الاستدراج': '#FFA500', 'Istidraj': '#FFA500',
                       'الانهيار': '#FF4444', 'Collapse': '#FF4444'}
        unique_stages = list(dict.fromkeys(stages_history))
        for stg in unique_stages:
            indices = [i for i, s in enumerate(stages_history) if s == stg]
            if indices:
                ax2.axvspan(indices[0], indices[-1], alpha=0.3, color=stage_colors.get(stg, '#888'), label=stg)
        ax2.plot(S_vals, color='#FFD700', lw=2)
        ax2.set_xlabel(TXT('السنوات', 'Years'), color='white')
        ax2.set_ylabel('S (الثبات)', color='white')
        ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.2)
        ax2.set_title(TXT('مراحل الدورة', 'Cycle Stages'), color='white', fontsize=13)

        plt.tight_layout()
        st.pyplot(fig)

        # ─────────────────────────────────────────
        # بطاقة المرحلة الحالية
        # ─────────────────────────────────────────
        final_S = S_vals[-1]
        final_E = E_vals[-1]
        current_stage = get_stage(final_S)
        gap = final_E - final_S

        st.markdown("---")
        st.subheader(TXT("📊 الحالة النهائية للأمة", "📊 Final State of the Nation"))
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("W (الولاء)", f"{W_vals[-1]:.2f}")
        col_m2.metric("B (البراءة)", f"{B_vals[-1]:.2f}")
        col_m3.metric("S (الثبات)", f"{final_S:.2f}")
        col_m4.metric(TXT("فجوة الاستدراج", "Istidraj Gap"), f"{gap:.2f}")

        st.markdown(f"""
        <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;border:2px solid {current_stage['color']};margin:15px 0;text-align:center;">
            <h2 style="color:{current_stage['color']};">📍 {current_stage['name']}</h2>
            <p style="color:#CCC;font-size:1.1em;">{current_stage['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        # تحذير إذا كان في مرحلة خطر
        if final_S < 0.3:
            st.error(TXT("🚨 الأمة في مرحلة الانهيار! مطلوب إحياء فوري للولاء (W) والبراءة (B).", "🚨 Nation in collapse! Immediate revival of W and B required."))
        elif gap > 0.3:
            st.error(TXT("⚠️ فجوة استدراج خطيرة! التمكين المادي يفوق الثبات الأخلاقي بكثير.", "⚠️ Dangerous Istidraj gap! Material empowerment far exceeds moral stability."))
        elif gap > 0.1:
            st.warning(TXT("⚡ فجوة استدراج متوسطة. راقب المؤشرات.", "⚡ Moderate Istidraj gap. Watch the indicators."))
        else:
            st.success(TXT("✅ الأمة في حالة توازن جيد.", "✅ Nation in good balance."))

        # خلاصة الدورة
        st.markdown("---")
        st.subheader(TXT("💡 الدورة الإلهية – المراحل الثماني", "💡 The Divine Cycle – Eight Stages"))
        stages_list = [
            ("١. التأسيس الكوني", TXT("الخلق على الفطرة، الميثاق الأزلي، التكليف بالعبودية.", "Creation on fitrah, the covenant, commissioning.")),
            ("٢. البيان النظري", TXT("إرسال الرسل وإنزال الكتب لبيان القانون.", "Sending messengers and revealing books to explain the law.")),
            ("٣. الامتحان العملي", TXT("الابتلاء بالخير والشر، التمحيص بين الصادق والكاذب.", "Trial with good and evil, distinguishing truthful from false.")),
            ("٤. التطبيق المنهجي", TXT("بناء الفرد، الأسرة، المجتمع، الدولة، الأمة.", "Building the individual, family, society, state, nation.")),
            ("٥. النتائج الكونية", TXT("ظهور السنن: النصر والتمكين أو الذلة والهلاك.", "Manifestation of laws: victory and empowerment or humiliation and destruction.")),
            ("٦. تحقيق المقاصد", TXT("حفظ الضروريات، تحقيق الكماليات، إقامة الحضارة.", "Preserving necessities, achieving complements, establishing civilization.")),
            ("٧. الاستمرار والتجدد", TXT("التجديد الدوري، التكيف مع المتغيرات.", "Periodic renewal, adapting to changes.")),
            ("٨. الخاتمة الكونية", TXT("الموت، يوم الفصل، الميزان، الجنة أو النار.", "Death, Day of Judgment, the Balance, Paradise or Hell.")),
        ]
        for title, desc in stages_list:
            st.markdown(f"**{title}**")
            st.info(desc)
