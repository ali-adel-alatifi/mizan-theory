# mizan/smart_guide.py
"""
المرشد الشخصي الذكي
يقدم ملخص حالة فوري، تذكيرات، واقتراحات مخصصة بناءً على موقع المستخدم
"""

import streamlit as st
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
    /* الأعمدة */
    .stColumn {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_user_phase(W_raw, B_raw):
    """تحديد مرحلة المستخدم بناءً على W و B"""
    if W_raw is None or B_raw is None:
        return "unknown"
    if W_raw >= 0.5 and B_raw >= 0.5:
        return "believer"
    elif W_raw >= 0.5 and B_raw < 0.1:
        return "wrath"
    elif W_raw < 0.1 and B_raw >= 0.5:
        return "astray"
    elif W_raw < 0.1 and B_raw < 0.1:
        return "hypocrite"
    else:
        return "transition"

def get_personalized_recommendation(phase, prayer_status):
    """توليد توصية مخصصة بناءً على المرحلة"""
    recommendations = {
        "believer": TXT(
            "🟢 أنت في منطقة الثبات. حافظ على الصلاة والبراءة. جرب تبويب 'القانون الواحد' لتعمق فهمك للنظام الكوني.",
            "🟢 You are in the stability zone. Maintain prayer and disavowal. Try 'The One Law' tab to deepen your understanding."
        ),
        "wrath": TXT(
            "🟡 أنت تصلي لكن براءتك ضعيفة. أنت في منطقة الخطر. ابدأ بقراءة سورة الممتحنة. جرب تبويب 'طبيب القلوب' لتشخيص مشكلتك.",
            "🟡 You pray but your disavowal is weak. You are in the danger zone. Start reading Surat Al-Mumtahina. Try the 'Healer' tab."
        ),
        "astray": TXT(
            "🟠 براءتك قوية لكن ولاءك ضعيف. لا تكتفِ بمحاربة الباطل، بل قوِّ إيمانك. جرب تبويب 'البوصلة' لاكتشاف موقعك بدقة.",
            "🟠 Your disavowal is strong but your loyalty is weak. Don't just fight falsehood, strengthen your faith. Try the 'Compass' tab."
        ),
        "hypocrite": TXT(
            "🔴 أنت في حالة انهيار. لا ولاء ولا براءة. ابدأ فوراً بالتوبة. جرب زر 'توبة نصوح' في تبويب 'الطاقة الروحية'.",
            "🔴 You are in a state of collapse. No loyalty, no disavowal. Start immediately with repentance. Try 'Sincere Repentance' in the 'Spiritual Energy' tab."
        ),
        "transition": TXT(
            "🟡 أنت في منطقة انتقالية. في طريقك إلى الثبات. استمر في تحسين صلاتك وبراءتك.",
            "🟡 You are in a transitional zone. On your way to stability. Keep improving your prayer and disavowal."
        ),
    }
    return recommendations.get(phase, recommendations["transition"])

def get_daily_reminders():
    """توليد تذكيرات يومية بناءً على نشاط المستخدم"""
    reminders = []
    
    if not st.session_state.get("maun_today", False):
        reminders.append(TXT("⚠️ لم تجب على اختبار الماعون اليوم. اذهب إلى تبويب 'الطاقة الروحية'.", "⚠️ You haven't done the Ma'un test today."))
    
    if st.session_state.get("prayer_status", 0.5) < 0.5:
        reminders.append(TXT("🕌 صلاتك تحتاج إلى تقوية. حرّك منزلق الصلاة في تبويب 'الطاقة الروحية'.", "🕌 Your prayer needs strengthening."))
    
    if st.session_state.get("spiritual_raan", 0.2) > 0.5:
        reminders.append(TXT("🖤 الران على قلبك مرتفع. جرب زر 'توبة نصوح' لتنظيفه.", "🖤 The darkness on your heart is high. Try 'Sincere Repentance'."))
    
    if not reminders:
        reminders.append(TXT("✅ أحسنت! لقد اعتنيت بنفسك اليوم. استمر.", "✅ Well done! You took care of yourself today."))
    
    return reminders

def render_smart_guide():
    """عرض المرشد الشخصي الذكي في الشريط الجانبي"""
    fix_rtl_display()
    
    W_raw = None
    B_raw = None
    
    if len(st.session_state.get("compass_answers", {})) == 19:
        from logic import compute_compass
        from config import COMPASS_DATA
        W_raw, B_raw, _ = compute_compass(st.session_state.compass_answers, COMPASS_DATA)
    
    if W_raw is None:
        vals = [st.session_state.slider_values.get(f"V{i}", 0.0) for i in range(11)] if "slider_values" in st.session_state else None
        if vals:
            import numpy as np
            W_vals = vals[0:6]
            B_vals = vals[6:11]
            W_raw = np.mean(W_vals)
            B_raw = np.mean(B_vals)
    
    phase = get_user_phase(W_raw, B_raw)
    prayer_status = st.session_state.get("prayer_status", 0.5)
    
    st.markdown(f"### 🧭 {TXT('مرشدك الشخصي', 'Your Personal Guide')}")
    st.info(get_personalized_recommendation(phase, prayer_status))
    
    st.markdown(f"**{TXT('📋 تذكيرات اليوم', '📋 Today\'s Reminders')}**")
    for reminder in get_daily_reminders():
        st.markdown(f"- {reminder}")
    
    st.markdown(f"**{TXT('📊 مؤشراتك السريعة', '📊 Your Quick Indicators')}**")
    c1, c2, c3 = st.columns(3)
    c1.metric("W", f"{W_raw:+.2f}" if W_raw is not None else "؟")
    c2.metric("B", f"{B_raw:+.2f}" if B_raw is not None else "؟")
    c3.metric(TXT("صلاة", "Prayer"), f"{prayer_status:.2f}")
