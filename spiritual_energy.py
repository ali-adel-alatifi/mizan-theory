# mizan/spiritual_energy.py
"""
محاكاة قوانين الطاقة الروحية
حفظ، تضاعف، مقاومة، تحول
"""

import streamlit as st
import numpy as np
from config import TXT

# =============================================
# 1. مؤشرات الطاقة الروحية
# =============================================
if "spiritual_noor" not in st.session_state:
    st.session_state.spiritual_noor = 0.6       # النور (0 إلى 1)
if "spiritual_raan" not in st.session_state:
    st.session_state.spiritual_raan = 0.2       # الران (0 إلى 1)
if "spiritual_conductivity" not in st.session_state:
    st.session_state.spiritual_conductivity = 0.7  # التوصيلية (0 إلى 1)
if "spiritual_multiplier" not in st.session_state:
    st.session_state.spiritual_multiplier = 1.0    # المضاعف (≥1)

def render_spiritual_energy():
    st.header(TXT("⚡ قوانين الطاقة الروحية", "⚡ Laws of Spiritual Energy"))
    st.caption(TXT(
        "هذه المحاكاة تجسد القوانين السبعة للطاقة الروحية: الحفظ، التناسب، المقاومة، التجاذب، التضاعف، التدافع، والتحول.",
        "This simulation embodies the seven laws of spiritual energy."
    ))

    # ─────────────────────────────────────────
    # لوحة المؤشرات
    # ─────────────────────────────────────────
    st.subheader(TXT("📊 مؤشرات الطاقة", "📊 Energy Indicators"))
    c1, c2, c3, c4 = st.columns(4)
    
    noor = st.session_state.spiritual_noor
    raan = st.session_state.spiritual_raan
    cond = st.session_state.spiritual_conductivity
    mult = st.session_state.spiritual_multiplier

    c1.metric(TXT("النور", "Light"), f"{noor:.2f}")
    c2.metric(TXT("الران", "Darkness"), f"{raan:.2f}")
    c3.metric(TXT("التوصيلية", "Conductivity"), f"{cond:.2f}")
    c4.metric(TXT("المضاعف", "Multiplier"), f"{mult:.1f}x")

    # ─────────────────────────────────────────
    # أزرار التفاعل (الأعمال)
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("🎮 محاكاة الأعمال", "🎮 Deed Simulation"))
    st.caption(TXT("اضغط على الأزرار لتشاهد كيف تتغير مؤشرات الطاقة الروحية.", "Press the buttons to watch spiritual energy indicators change."))

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        if st.button(TXT("🤲 استغفار", "🤲 Seek Forgiveness"), use_container_width=True):
            st.session_state.spiritual_raan = max(0, raan - 0.08)
            st.session_state.spiritual_conductivity = min(1, cond + 0.06)
            st.session_state.spiritual_noor = min(1, noor + 0.03)
            st.rerun()

    with col_b:
        if st.button(TXT("🕌 توبة نصوح", "🕌 Sincere Repentance"), use_container_width=True):
            st.session_state.spiritual_raan = max(0, raan - 0.2)
            st.session_state.spiritual_conductivity = min(1, cond + 0.15)
            st.session_state.spiritual_noor = min(1, noor + 0.1)
            st.rerun()

    with col_c:
        if st.button(TXT("💵 صدقة", "💵 Charity"), use_container_width=True):
            st.session_state.spiritual_multiplier = min(10, mult + 0.5)
            st.session_state.spiritual_noor = min(1, noor + 0.04)
            st.rerun()

    with col_d:
        if st.button(TXT("🕋 صلاة بخشوع", "🕋 Devout Prayer"), use_container_width=True):
            st.session_state.spiritual_noor = min(1, noor + 0.08)
            st.session_state.spiritual_conductivity = min(1, cond + 0.04)
            st.rerun()

    # ─────────────────────────────────────────
    # مؤثرات عكسية (ذنوب)
    # ─────────────────────────────────────────
    st.markdown("---")
    st.caption(TXT("محاكاة أثر الذنوب", "Simulating the effect of sins"))
    col_e, col_f = st.columns(2)
    with col_e:
        if st.button(TXT("😠 غضب / غيبة", "😠 Anger / Backbiting"), use_container_width=True):
            st.session_state.spiritual_raan = min(1, raan + 0.06)
            st.session_state.spiritual_conductivity = max(0, cond - 0.04)
            st.rerun()
    with col_f:
        if st.button(TXT("📱 نظر محرم", "📱 Forbidden Glance"), use_container_width=True):
            st.session_state.spiritual_raan = min(1, raan + 0.04)
            st.session_state.spiritual_noor = max(0, noor - 0.03)
            st.rerun()

    # ─────────────────────────────────────────
    # تطبيق القوانين السبعة (تلقائي)
    # ─────────────────────────────────────────
    # قانون التحول: النور يذيب الران تدريجياً
    st.session_state.spiritual_raan = max(0, st.session_state.spiritual_raan - 0.005 * st.session_state.spiritual_noor)
    # قانون المقاومة: الران يقلل التوصيلية
    st.session_state.spiritual_conductivity = min(1, max(0.1, st.session_state.spiritual_conductivity - 0.01 * st.session_state.spiritual_raan))
    # قانون التضاعف: المضاعف يزيد أثر الأعمال، لكنه يضمحل ببطء
    st.session_state.spiritual_multiplier = max(1, st.session_state.spiritual_multiplier - 0.01)
    # قانون حفظ الطاقة: النور = (1 - الران) × التوصيلية
    target_noor = (1 - st.session_state.spiritual_raan) * st.session_state.spiritual_conductivity
    st.session_state.spiritual_noor = st.session_state.spiritual_noor * 0.9 + target_noor * 0.1

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
        3. **Law of Resistance and Conductivity:** Sins increase "raan" (darkness), repentance increases "conductivity". (Al-Mutaffifin: 14)
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
        st.rerun()
