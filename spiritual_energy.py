# mizan/spiritual_energy.py
"""
محاكاة قوانين الطاقة الروحية
حفظ، تضاعف، مقاومة، تحول + بوصلة الصلاة + اختبار الماعون
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
# 1. مؤشرات الطاقة الروحية
# =============================================
if "spiritual_noor" not in st.session_state:
    st.session_state.spiritual_noor = 0.6
if "spiritual_raan" not in st.session_state:
    st.session_state.spiritual_raan = 0.2
if "spiritual_conductivity" not in st.session_state:
    st.session_state.spiritual_conductivity = 0.7
if "spiritual_multiplier" not in st.session_state:
    st.session_state.spiritual_multiplier = 1.0
if "prayer_status" not in st.session_state:
    st.session_state.prayer_status = 0.5
if "patience_tank" not in st.session_state:
    st.session_state.patience_tank = 0.5
if "maun_today" not in st.session_state:
    st.session_state.maun_today = False
if "maun_streak" not in st.session_state:
    st.session_state.maun_streak = 0

def render_spiritual_energy():
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
    st.header(TXT("⚡ قوانين الطاقة الروحية", "⚡ Laws of Spiritual Energy"))
    st.caption(TXT(
        "هذه المحاكاة تجسد القوانين السبعة للطاقة الروحية، مع بوصلة الصلاة واختبار الماعون.",
        "This simulation embodies the seven laws of spiritual energy, with the Prayer Compass and the Ma'un Test."
    ))

    # ─────────────────────────────────────────
    # 🕌 بوصلة الصلاة – مراقب الامتثال
    # ─────────────────────────────────────────
    st.subheader(TXT("🕌 بوصلة الصلاة – مراقب الامتثال", "🕌 Prayer Compass – Compliance Monitor"))
    st.caption(TXT(
        "حرّك المنزلق لترى كيف تؤثر حالة صلاتك على طاقتك الروحية وموقعك من مقام إبراهيم.",
        "Move the slider to see how your prayer status affects your spiritual energy."
    ))

    prayer_status = st.slider(
        TXT("حالة الصلاة", "Prayer Status"),
        0.0, 1.0, st.session_state.prayer_status, 0.05,
        key="prayer_slider",
        help=TXT(
            "0.0=تارك | 0.3=متكاسل | 0.6=محافظ بلا خشوع | 0.9=محافظ بخشوع | 1.0=قائم قانت",
            "0.0=Abandoned | 0.3=Lazy | 0.6=Regular without focus | 0.9=Devout | 1.0=Standing in devotion"
        )
    )
    st.session_state.prayer_status = prayer_status

    W_from_prayer = -0.5 + prayer_status * 1.2
    B_from_prayer = -0.3 + prayer_status * 1.0
    S_from_prayer = max(0, ((W_from_prayer + 1) / 2) * ((B_from_prayer + 1) / 2))

    if prayer_status < 0.2:
        prayer_phase = TXT(
            "⚠️ **مرحلة الخطر:** أنت في مرحلة ضياع العروة الوثقى. الصلاة هي حارسة الفطرة. بدونها، يفسد القلب ويذوب الولاء. (لقمان 17)",
            "⚠️ **Danger Zone:** You are losing the firm handhold. Prayer is the guardian of innate nature."
        )
    elif prayer_status < 0.5:
        prayer_phase = TXT(
            "🟡 **مرحلة التأسيس:** أنت تبني شخصيتك الإيمانية. الصلاة هنا تثبت العروة الوثقى. استعن بها على الصبر. (البقرة 45)",
            "🟡 **Foundation Phase:** You are building your faith character. Prayer stabilizes the firm handhold."
        )
    elif prayer_status < 0.8:
        prayer_phase = TXT(
            "🟢 **مرحلة الجماعة:** صلاتك توحدك مع المؤمنين. أنت الآن جزء من حبل الله. استعن بها على الجهاد والتضحية. (البقرة 153)",
            "🟢 **Community Phase:** Your prayer unites you with the believers."
        )
    else:
        prayer_phase = TXT(
            "🟣 **مرحلة الاستخلاف:** أنت في مقام القيادة. الصلاة هنا تحميك من فتنة الغنى والغرور. حافظ عليها ليستمر التمكين. (البقرة 238)",
            "🟣 **Stewardship Phase:** Prayer protects you from the trials of wealth and pride."
        )

    st.info(prayer_phase)

    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric(TXT("W (من الصلاة)", "W (from prayer)"), f"{W_from_prayer:+.2f}")
    col_p2.metric(TXT("B (من الصلاة)", "B (from prayer)"), f"{B_from_prayer:+.2f}")
    col_p3.metric(TXT("S (من الصلاة)", "S (from prayer)"), f"{S_from_prayer:.2f}")

    # ─────────────────────────────────────────
    # 🧴 اختبار الماعون اليومي
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🧴 اختبار الماعون اليومي", "🧴 The Daily Ma'un Test"))
    st.caption(TXT(
        "﴿وَيَمْنَعُونَ الْمَاعُونَ﴾ [الماعون: 7]. الماعون هو الشيء اليسير الذي يتعاوره الناس. "
        "من منعه كشف عن خلل في براءته (B)، حتى لو كان يصلي. أجب بصدق:",
        "﴿And they withhold the Ma'un (small kindnesses).﴾ [Al-Ma'un: 7]. Answer honestly:"
    ))

    col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
    with col_m1:
        st.markdown(TXT(
            "**اليوم، هل أعطيت شيئاً يسيراً (ماعوناً) لأحد؟** (مساعدة، كلمة طيبة، شيئاً تافهاً)",
            "**Today, did you give something small (Ma'un) to anyone?** (Help, kind word, a trivial thing)"
        ))
    with col_m2:
        if st.button(TXT("✅ نعم", "✅ Yes"), use_container_width=True, key="btn_maun_yes"):
            if not st.session_state.maun_today:
                st.session_state.maun_today = True
                st.session_state.maun_streak += 1
                st.session_state.spiritual_raan = max(0, st.session_state.spiritual_raan - 0.03)
                st.session_state.spiritual_noor = min(1, st.session_state.spiritual_noor + 0.02)
                st.session_state.spiritual_conductivity = min(1, st.session_state.spiritual_conductivity + 0.02)
            st.rerun()
    with col_m3:
        if st.button(TXT("❌ لا", "❌ No"), use_container_width=True, key="btn_maun_no"):
            if not st.session_state.maun_today:
                st.session_state.maun_today = True
                st.session_state.maun_streak = 0
                st.session_state.spiritual_raan = min(1, st.session_state.spiritual_raan + 0.04)
            st.rerun()

    if st.session_state.maun_today:
        if st.session_state.maun_streak > 0:
            st.success(TXT(
                f"✅ أحسنت! لقد أعطيت الماعون اليوم. سلسلة العطاء: {st.session_state.maun_streak} يوم.",
                f"✅ Well done! You gave Ma'un today. Streak: {st.session_state.maun_streak} days."
            ))
        else:
            st.warning(TXT(
                "⚠️ لقد منعت الماعون اليوم. تذكر قوله تعالى: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ... وَيَمْنَعُونَ الْمَاعُونَ﴾. "
                "حتى أبسط ما تملك، إذا منعته، كان علامة خلل في براءتك.",
                "⚠️ You withheld Ma'un today. Remember: ﴿Woe to those who pray... and withhold Ma'un.﴾"
            ))

    if st.button(TXT("🔄 يوم جديد (إعادة تعيين الماعون)", "🔄 New Day (Reset Ma'un)"), use_container_width=True):
        st.session_state.maun_today = False
        st.rerun()

    # ─────────────────────────────────────────
    # لوحة المؤشرات العامة
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("📊 مؤشرات الطاقة", "📊 Energy Indicators"))
    c1, c2, c3, c4, c5 = st.columns(5)

    noor = st.session_state.spiritual_noor
    raan = st.session_state.spiritual_raan
    cond = st.session_state.spiritual_conductivity
    mult = st.session_state.spiritual_multiplier
    patience = st.session_state.patience_tank

    c1.metric(TXT("النور", "Light"), f"{noor:.2f}")
    c2.metric(TXT("الران", "Darkness"), f"{raan:.2f}")
    c3.metric(TXT("التوصيلية", "Conductivity"), f"{cond:.2f}")
    c4.metric(TXT("المضاعف", "Multiplier"), f"{mult:.1f}x")
    c5.metric(TXT("خزان الصبر", "Patience"), f"{patience:.2f}")

    # ─────────────────────────────────────────
    # أزرار التفاعل (الأعمال)
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🎮 محاكاة الأعمال", "🎮 Deed Simulation"))

    col_a, col_b, col_c, col_d, col_e = st.columns(5)

    with col_a:
        if st.button(TXT("🤲 استغفار", "🤲 Seek Forgiveness"), use_container_width=True):
            st.session_state.spiritual_raan = max(0, raan - 0.08)
            st.session_state.spiritual_conductivity = min(1, cond + 0.06)
            st.session_state.spiritual_noor = min(1, noor + 0.03)
            st.session_state.patience_tank = min(1, patience + 0.05)
            st.rerun()

    with col_b:
        if st.button(TXT("🕌 توبة نصوح", "🕌 Sincere Repentance"), use_container_width=True):
            st.session_state.spiritual_raan = max(0, raan - 0.2)
            st.session_state.spiritual_conductivity = min(1, cond + 0.15)
            st.session_state.spiritual_noor = min(1, noor + 0.1)
            st.session_state.patience_tank = min(1, patience + 0.15)
            st.rerun()

    with col_c:
        if st.button(TXT("💵 صدقة", "💵 Charity"), use_container_width=True):
            st.session_state.spiritual_multiplier = min(10, mult + 0.5)
            st.session_state.spiritual_noor = min(1, noor + 0.04)
            st.rerun()

    with col_d:
        if st.button(TXT("🕌 صلاة بخشوع", "🕌 Devout Prayer"), use_container_width=True):
            st.session_state.spiritual_noor = min(1, noor + 0.08)
            st.session_state.spiritual_conductivity = min(1, cond + 0.04)
            st.session_state.patience_tank = min(1, patience + 0.1)
            st.session_state.prayer_status = min(1, st.session_state.prayer_status + 0.05)
            st.rerun()

    with col_e:
        if st.button(TXT("⚔️ مواجهة ابتلاء", "⚔️ Face Trial"), use_container_width=True):
            if patience > 0.3:
                st.session_state.patience_tank = max(0, patience - 0.25)
                st.session_state.spiritual_noor = min(1, noor + 0.02)
                st.success(TXT("✅ تجاوزت الابتلاء بالصبر!", "✅ You overcame the trial with patience!"))
            else:
                st.session_state.spiritual_raan = min(1, raan + 0.1)
                st.session_state.spiritual_noor = max(0, noor - 0.05)
                st.error(TXT("❌ سقطت في الذنب. خزان الصبر فارغ.", "❌ You fell into sin. Patience tank empty."))
            st.rerun()

    # ─────────────────────────────────────────
    # مؤثرات عكسية (ذنوب)
    # ─────────────────────────────────────────
    st.markdown("---")
    st.caption(TXT("محاكاة أثر الذنوب", "Simulating the effect of sins"))
    col_f, col_g = st.columns(2)
    with col_f:
        if st.button(TXT("😠 غضب / غيبة", "😠 Anger / Backbiting"), use_container_width=True):
            st.session_state.spiritual_raan = min(1, raan + 0.06)
            st.session_state.spiritual_conductivity = max(0, cond - 0.04)
            st.rerun()
    with col_g:
        if st.button(TXT("📱 نظر محرم", "📱 Forbidden Glance"), use_container_width=True):
            st.session_state.spiritual_raan = min(1, raan + 0.04)
            st.session_state.spiritual_noor = max(0, noor - 0.03)
            st.rerun()

    # ─────────────────────────────────────────
    # تطبيق القوانين السبعة (تلقائي)
    # ─────────────────────────────────────────
    st.session_state.spiritual_raan = max(0, st.session_state.spiritual_raan - 0.005 * st.session_state.spiritual_noor)
    st.session_state.spiritual_conductivity = min(1, max(0.1, st.session_state.spiritual_conductivity - 0.01 * st.session_state.spiritual_raan))
    st.session_state.spiritual_multiplier = max(1, st.session_state.spiritual_multiplier - 0.01)
    target_noor = (1 - st.session_state.spiritual_raan) * st.session_state.spiritual_conductivity
    st.session_state.spiritual_noor = st.session_state.spiritual_noor * 0.9 + target_noor * 0.1
    st.session_state.patience_tank = min(1, st.session_state.patience_tank + 0.02 * st.session_state.prayer_status)

    # ─────────────────────────────────────────
    # عرض القوانين السبعة
    # ─────────────────────────────────────────
    st.markdown("---")
    with st.expander(TXT("📜 القوانين السبعة للطاقة الروحية", "📜 The Seven Laws of Spiritual Energy")):
        st.markdown(TXT("""
        1. **قانون حفظ الطاقة:** الحسنة تتحول إلى نور، والسيئة تتحول إلى ظلمة. (الأنعام: 160)
        2. **قانون التناسب:** النتيجة تتناسب مع جودة العمل وإخلاصه. (النجم: 39-40)
        3. **قانون المقاومة والتوصيلية:** الذنوب تزيد "الران"، والتوبة تزيد "التوصيلية". (المطففين: 14)
        4. **قانون التجاذب والتنافر:** المتقون يتجاذبون، والكفار والمؤمنون يتنافرون. (الزخرف: 67)
        5. **قانون التضاعف الأسي:** الحسنة تتضاعف أضعافاً كثيرة. (البقرة: 261)
        6. **قانون التدافع الطاقي:** كلما زادت الطاقة الإيجابية، زادت مقاومة الطاقة السلبية. (البقرة: 251)
        7. **قانون التحول الطاقي:** الحسنات يذهبن السيئات. (هود: 114)
        """,
        """
        1. **Law of Energy Conservation:** Good deeds turn into light, sins into darkness. (Al-An'am: 160)
        2. **Law of Proportionality:** The result is proportional to the quality and sincerity of the deed. (An-Najm: 39-40)
        3. **Law of Resistance and Conductivity:** Sins increase "raan", repentance increases "conductivity". (Al-Mutaffifin: 14)
        4. **Law of Attraction and Repulsion:** The righteous attract each other, believers and disbelievers repel. (Az-Zukhruf: 67)
        5. **Law of Exponential Multiplication:** A good deed is multiplied many times. (Al-Baqarah: 261)
        6. **Law of Energetic Struggle:** As positive energy increases, negative energy resistance increases. (Al-Baqarah: 251)
        7. **Law of Energy Transformation:** Good deeds erase bad deeds. (Hud: 114)
        """))

    # ─────────────────────────────────────────
    # إعادة الضبط
    # ─────────────────────────────────────────
    st.markdown("---")
    if st.button(TXT("🔄 إعادة ضبط المؤشرات", "🔄 Reset Indicators")):
        st.session_state.spiritual_noor = 0.6
        st.session_state.spiritual_raan = 0.2
        st.session_state.spiritual_conductivity = 0.7
        st.session_state.spiritual_multiplier = 1.0
        st.session_state.prayer_status = 0.5
        st.session_state.patience_tank = 0.5
        st.session_state.maun_today = False
        st.session_state.maun_streak = 0
        st.rerun()
