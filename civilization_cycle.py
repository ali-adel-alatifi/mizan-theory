# mizan/civilization_cycle.py
"""
محاكي الدورة الحضارية عبر الصلاة
من الفطرة إلى الاستخلاف والعكس
"""

import streamlit as st
import numpy as np
from config import TXT

# =============================================
# دالة إصلاح النصوص العربية
# =============================================
def fix_rtl_display():
    """إصلاح مشكلة عرض النصوص العربية في Streamlit"""
    st.markdown("""
    <style>
    /* إجبار كل النصوص على أن تكون من اليمين لليسار */
    div, p, h1, h2, h3, h4, h5, h6, span, strong, em, li, label, .stMarkdown, .stText {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: plaintext !important;
    }
    /* العناوين الرئيسية */
    .stTitle, .stHeader, .stSubheader {
        direction: rtl !important;
        text-align: right !important;
    }
    /* صناديق المعلومات */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        direction: rtl !important;
        text-align: right !important;
    }
    /* الأزرار والمنزلقات */
    button, .stSlider {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================
# 1. تعريف المراحل الخمس
# =============================================
CYCLE_STAGES = [
    {
        "id": "fitrah",
        "name": TXT("١. الفطرة السليمة", "1. Pure Innate Nature"),
        "icon": "🌱",
        "color": "#00FF88",
        "verse": TXT("﴿يَا بُنَيَّ أَقِمِ الصَّلَاةَ وَأْمُرْ بِالْمَعْرُوفِ وَانْهَ عَنِ الْمُنكَرِ﴾ [لقمان: 17]", "﴿O my son, establish prayer...﴾ [Luqman: 17]"),
        "desc": TXT("الصلاة هنا تحمي الفطرة من الانحراف. هي حارسة الولاء الأوّل.", "Prayer here protects innate nature from deviation. It is the guardian of first loyalty."),
        "threshold": 0.0
    },
    {
        "id": "wahi",
        "name": TXT("٢. تلقي الوحي", "2. Receiving Revelation"),
        "icon": "📖",
        "color": "#00BFFF",
        "verse": TXT("﴿وَأْمُرْ أَهْلَكَ بِالصَّلَاةِ وَاصْطَبِرْ عَلَيْهَا﴾ [طه: 132]", "﴿And enjoin prayer upon your family...﴾ [Taha: 132]"),
        "desc": TXT("الصلاة هنا قناة لتلقي المنهج وتوحيد الأسرة حوله.", "Prayer here is a channel for receiving the methodology and uniting the family around it."),
        "threshold": 0.2
    },
    {
        "id": "tasees",
        "name": TXT("٣. التأسيس الفردي", "3. Individual Foundation"),
        "icon": "🧍",
        "color": "#FFD700",
        "verse": TXT("﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾ [البقرة: 45]", "﴿And seek help through patience and prayer...﴾ [Al-Baqarah: 45]"),
        "desc": TXT("الصلاة هنا تثبت العروة الوثقى. هي معين على الصبر.", "Prayer here stabilizes the firm handhold. It is an aid for patience."),
        "threshold": 0.4
    },
    {
        "id": "jamaah",
        "name": TXT("٤. التكتل الجماعي", "4. Community Formation"),
        "icon": "🤝",
        "color": "#FFA500",
        "verse": TXT("﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾ [البقرة: 153]", "﴿O you who believe, seek help through patience and prayer...﴾ [Al-Baqarah: 153]"),
        "desc": TXT("الصلاة هنا توحد الجماعة وتربطها بحبل الله.", "Prayer here unites the community and binds it with Allah's rope."),
        "threshold": 0.6
    },
    {
        "id": "istikhlaf",
        "name": TXT("٥. الاستخلاف والتمكين", "5. Stewardship & Empowerment"),
        "icon": "🏛️",
        "color": "#FF4500",
        "verse": TXT("﴿حَافِظُوا عَلَى الصَّلَوَاتِ وَالصَّلَاةِ الْوُسْطَىٰ﴾ [البقرة: 238]", "﴿Guard strictly the prayers, and the middle prayer...﴾ [Al-Baqarah: 238]"),
        "desc": TXT("الصلاة هنا تحفظ التمكين من الزوال. هي ضمانة الاستمرار.", "Prayer here preserves empowerment from vanishing. It is the guarantee of continuity."),
        "threshold": 0.8
    },
]

def render_civilization_cycle():
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
    st.header(TXT("🔄 محاكي الدورة الحضارية", "🔄 Civilization Cycle Simulator"))
    st.caption(TXT(
        "حرّك منزلق الصلاة والزمن لترى كيف تنتقل الأمة عبر المراحل الخمس، وكيف تتراجع إذا أُهملت الصلاة.",
        "Move the prayer and time sliders to see how the nation transitions through the five stages, and how it regresses if prayer is neglected."
    ))

    # ─────────────────────────────────────────
    # متحكمات المحاكاة
    # ─────────────────────────────────────────
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        prayer_level = st.slider(
            TXT("حالة الصلاة في الأمة", "Nation's Prayer Status"),
            0.0, 1.0, 0.5, 0.05,
            key="cycle_prayer",
            help=TXT("0.0=الصلاة مهملة | 1.0=الصلاة قائمة بالكامل", "0.0=Abandoned | 1.0=Fully established")
        )
    with col_ctrl2:
        time_progress = st.slider(
            TXT("تقدّم الزمن", "Time Progression"),
            0.0, 1.0, 0.3, 0.01,
            key="cycle_time",
            help=TXT("0.0=البداية | 1.0=الذروة", "0.0=Beginning | 1.0=Peak")
        )

    # ─────────────────────────────────────────
    # حساب مرحلة الأمة الحالية
    # ─────────────────────────────────────────
    # الصلاة تسرّع التقدم، والزمن يدفع للأمام
    effective_progress = min(1.0, time_progress * (0.5 + 0.8 * prayer_level))
    # إذا انخفضت الصلاة كثيراً، تتراجع الأمة
    if prayer_level < 0.3 and time_progress > 0.5:
        effective_progress = max(0.0, effective_progress - 0.3)

    # تحديد المرحلة الحالية
    current_stage = CYCLE_STAGES[0]
    for stage in reversed(CYCLE_STAGES):
        if effective_progress >= stage["threshold"]:
            current_stage = stage
            break

    # ─────────────────────────────────────────
    # عرض المسار البصري للمراحل
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🗺️ مسار الدورة الحضارية", "🗺️ Civilization Cycle Path"))

    # شريط التقدم
    st.progress(effective_progress)

    # أيقونات المراحل
    cols = st.columns(len(CYCLE_STAGES))
    for i, (col, stage) in enumerate(zip(cols, CYCLE_STAGES)):
        with col:
            if effective_progress >= stage["threshold"]:
                st.markdown(f"<p style='text-align:center;font-size:2em;'>{stage['icon']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center;color:{stage['color']};font-size:0.7em;'>{stage['name']}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='text-align:center;font-size:2em;opacity:0.3;'>{stage['icon']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center;color:#888;font-size:0.7em;opacity:0.5;'>{stage['name']}</p>", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # تفاصيل المرحلة الحالية
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT(f"📍 المرحلة الحالية: {current_stage['name']}", f"📍 Current Stage: {current_stage['name']}"))
    st.markdown(f"<p style='text-align:center;font-size:3em;'>{current_stage['icon']}</p>", unsafe_allow_html=True)

    col_det1, col_det2 = st.columns([2, 1])
    with col_det1:
        st.info(current_stage["verse"])
        st.markdown(current_stage["desc"])
    with col_det2:
        # مؤشرات الأمة في هذه المرحلة
        W_nation = 0.3 + effective_progress * 0.7
        B_nation = 0.3 + effective_progress * 0.7
        S_nation = W_nation * B_nation
        st.metric(TXT("W (ولاء الأمة)", "W (Nation's Loyalty)"), f"{W_nation:.2f}")
        st.metric(TXT("B (براءة الأمة)", "B (Nation's Disavowal)"), f"{B_nation:.2f}")
        st.metric(TXT("S (ثبات الأمة)", "S (Nation's Stability)"), f"{S_nation:.2f}")

    # ─────────────────────────────────────────
    # تحذير الدورة العكسية
    # ─────────────────────────────────────────
    if prayer_level < 0.3 and effective_progress < 0.3:
        st.error(TXT(
            "🚨 **تحذير:** الأمة في خطر الضياع. الصلاة مهملة، والفطرة تفسد. ﴿فَخَلَفَ مِن بَعْدِهِمْ خَلْفٌ أَضَاعُوا الصَّلَاةَ وَاتَّبَعُوا الشَّهَوَاتِ﴾ [مريم: 59]",
            "🚨 **Warning:** The nation is in danger. Prayer is neglected, and innate nature corrupts. ﴿Then there succeeded them a generation who neglected prayer and pursued desires.﴾ [Maryam: 59]"
        ))
    elif prayer_level > 0.8 and effective_progress > 0.8:
        st.success(TXT(
            "🟢 **بشرى:** الأمة في مقام الاستخلاف. الصلاة قائمة، والتمكين مستمر. ﴿الَّذِينَ إِن مَّكَّنَّاهُمْ فِي الْأَرْضِ أَقَامُوا الصَّلَاةَ﴾ [الحج: 41]",
            "🟢 **Glad Tidings:** The nation is in the station of stewardship. Prayer is established, and empowerment continues. ﴿Those who, if We establish them in the land, establish prayer...﴾ [Al-Hajj: 41]"
        ))

    # ─────────────────────────────────────────
    # خلاصة الدرس
    # ─────────────────────────────────────────
    st.markdown("---")
    st.markdown(TXT(
        """
        ### 💡 الدرس المستفاد
        
        الصلاة هي **محور الدورة الإلهية**. في كل مرحلة، تتغير وظيفتها، لكنها تبقى الأداة المركزية لتحقيق الولاء والبراءة.
        - في **الضعف**: هي معين على الصبر.
        - في **القوة**: هي ضمانة للاستمرار.
        - في **القيادة**: هي حماية من الغرور.
        
        **أهمية الصلاة لا تتغير، ولكن طريقة الاستعانة بها تتغير حسب المرحلة.**
        """,
        """
        ### 💡 The Lesson
        
        Prayer is **the axis of the divine cycle**. In each stage, its function changes, but it remains the central tool for achieving loyalty and disavowal.
        - In **weakness**: It is an aid for patience.
        - In **strength**: It is a guarantee of continuity.
        - In **leadership**: It is protection from pride.
        
        **The importance of prayer does not change, but the way we seek help through it changes according to the stage.**
        """
    ))
