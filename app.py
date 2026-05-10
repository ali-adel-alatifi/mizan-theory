import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random
import time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ================================================================
# إعداد الصفحة – اسم المنصة الجديد: نظام الإثبات
# ================================================================
st.set_page_config(
    page_title="نظام الإثبات – نظرية الميزان",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# حقوق المؤلف والترخيص
# ================================================================
__AUTHOR__ = "علي عادل العاطفي | Ali Adel Alatifi"
__YEAR__ = 2026
__LICENSE__ = "MIT License"
__VERSION__ = "4.0.0 – نظام الإثبات الرقمي"
__SIGNATURE__ = "⚖️ S = W × B | ق = الحق = الميزان"

# ================================================================
# النظام اللغوي
# ================================================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(ar_text, en_text):
    return ar_text if LANG == "ar" else en_text

# ================================================================
# 🌟 الأساس الأول: الكتاب المسطور (القرآن)
# المصدر: ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ [البقرة: 256]
# الاستنباط: B (يكفر بالطاغوت) × W (يؤمن بالله) → S (استمسك بالعروة الوثقى)
# القيمة الثابتة: ق = 100 (من حساب الجمل القرآني، رمز الحق والميزان)
# ================================================================
QAF_TRUTH = 100  # ق = الحق = الميزان = الجزاء = العدل (مصدر قرآني)

# ================================================================
# 🌌 الأساس الثاني: الكتاب المنظور (الكون والفطرة)
# المصدر: قانون الجذب والتنافر في الذرة، جهاز المناعة في الخلية
# الاستنباط: الثبات (S) = الجذب (W) × التنافر (B)
# هذه المعادلة مركوزة في الفطرة، ومشهودة في الآفاق والأنفس
# ================================================================
# الدليل الفِطري: كل إنسان يبحث عمَّن يحبه (W) وعمَّا يحميه منه (B)
# الدليل الكوني: الذرة لا تستقر إلا بتوازن القوتين

# ================================================================
# 🧠 الأساس الثالث: العقل والرياضيات
# المصدر: الهندسة التفاضلية، نظرية النظم الديناميكية
# الاستنباط: 
#   - المسار: γ(t) = (B(t), W(t))
#   - الانحناء: κ = |W'B'' - B'W''| / (W'² + B'²)^(3/2)
#   - الصراط المستقيم: κ = 0
#   - التوبة: F_correction = -α × ∇κ
# ================================================================

# ================================================================
# ⚖️ الأساس الرابع: السنن الإلهية (التاريخ والاستقراء)
# المصدر: سنة الاستدراج، سنة التداول، سنة الجزاء من جنس العمل
# الاستنباط: 
#   - الاستدراج: E(t) = E(t-1) + γ × (S(t-lag) - E(t-1))
#   - الجزاء من جنس العمل: الثبات (S) ينهار بانهيار (W) أو (B)
#   - التمكين (E) يتأخر عن الثبات (S) ثم ينهار فجأة
# ================================================================
ISTIDRAJ_LAG = 22  # من استقراء التاريخ القرآني والبشري

print("✅ المرحلة الأولى من نظام الإثبات اكتملت: تم توثيق مصادر النظرية الأربعة.")

# ================================================================
# 🧮 المرحلة الثانية: دوال المعادلة والهندسة التفاضلية
# ================================================================

# ================================================================
# الدالة ١: حساب الثبات S (المصدر: القرآن والكون والفطرة)
# ----------------------------------------------------------
# القرآن: ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
# الاستنباط: B (يكفر بالطاغوت) × W (يؤمن بالله) = S (العروة الوثقى)
# الكون: استقرار الذرة = الجذب النووي × التنافر الكهرومغناطيسي
# الفطرة: استقرار النفس = الحب لله × البغض في الله
# ================================================================
def calculate_stability(W, B, E, 
                       q_intensity=1.0,      # ق: من القرآن – الحق والميزان
                       k_val=20, n_val=50,   # ك، ن: من الحروف المقطعة – الأمر والنور
                       amr_val=0.5, nahy_val=0.5,  # أسس الحكم: من السنة والتشريع
                       adl_val=0.6, shura_val=0.5, # العدل والشورى: من القرآن
                       riba_val=0.2, zulm_val=0.2, khianah_val=0.2): # الحدود: من الشريعة
    """
    تحسب الثبات الوجودي (S) بناءً على:
    - الكتاب المسطور: S = W × B (استنباط من آية البقرة 256)
    - الكتاب المنظور: W (جذب) × B (تنافر) = استقرار (في الذرة والمجتمع)
    - العقل والرياضيات: تطبيق دالة أسية للتمييز بين التوازن والاختلال
    - السنن الإلهية: الجزاء من جنس العمل (S تنهار بانهيار أحد القطبين)
    """
    # الأساس: الضرب لا الجمع (من القرآن: "فَمَن يَكْفُرْ... وَيُؤْمِن...")
    # الضرب يعني الشرطية: لا ثبات بلا قطبين معًا
    S_base = W * B
    
    # ============================================================
    # تطبيق معامل الحق (ق) – من القرآن: "وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ"
    # ق = 100 = رمز الحق والميزان (حساب الجمل)
    # دور ق: يجعل الثبات يعتمد على توازن W و B، ويعاقب الاختلال
    # ============================================================
    imbalance = abs(W - B)  # مقدار الاختلال بين القطبين
    # كلما زادت q_intensity، زادت عقوبة الاختلال (الجزاء من جنس العمل)
    q_penalty = (q_intensity * QAF_TRUTH) / (q_intensity * QAF_TRUTH + imbalance * 50)
    S_base *= q_penalty
    
    # ============================================================
    # تطبيق المصدر (ك × ن) – من الحروف المقطعة في فواتح السور
    # ك = 20 (الأمر: كُن) – ن = 50 (النور: الهداية)
    # المصدر هو القوة المحركة للوجود، وبدونه لا ثبات
    # ============================================================
    source_factor = (k_val * n_val) / 1000.0
    S_base *= (1 + source_factor)
    
    # ============================================================
    # تطبيق أسس الحكم (من القرآن والسنة)
    # العدل: ﴿إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالْإِحْسَانِ﴾
    # الشورى: ﴿وَأَمْرُهُمْ شُورَىٰ بَيْنَهُمْ﴾
    # الأمر بالمعروف والنهي عن المنكر: آلية حفظ التوازن
    # ============================================================
    governance_factor = (0.5 + 0.5 * (amr_val * nahy_val))
    governance_factor *= (0.8 + 0.4 * adl_val)
    governance_factor *= (0.85 + 0.3 * shura_val)
    S_base *= governance_factor
    
    # ============================================================
    # تطبيق الحدود (من الشريعة)
    # الربا: ﴿فَأْذَنُوا بِحَرْبٍ مِّنَ اللَّهِ وَرَسُولِهِ﴾ – يمحق البركة
    # الظلم: ﴿إِنَّ الظَّالِمِينَ لَهُمْ عَذَابٌ أَلِيمٌ﴾ – أسرع مهلك
    # الخيانة: ﴿لَا تَخُونُوا اللَّهَ وَالرَّسُولَ﴾ – تنخر الثقة
    # ============================================================
    S_base *= (1 - 0.3 * riba_val)
    S_base *= (1 - 0.25 * zulm_val)
    S_base *= (1 - 0.15 * khianah_val)
    
    return np.clip(S_base, 0.001, 1.0)

# ================================================================
# الدالة ٢: حساب انحناء المسار (المصدر: الهندسة التفاضلية + القرآن)
# ----------------------------------------------------------
# القرآن: ﴿اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ﴾ – الصراط المستقيم: κ = 0
# العقل: الانحناء (Curvature) = مقياس الانحراف عن الاستقامة
# الفطرة: كل إنسان يشعر بالانحراف (الذنب) كانحناء عن الطريق
# ================================================================
def compute_path_curvature(W_history, B_history):
    """
    يحسب انحناء (Curvature) المسار في فضاء (W, B).
    المصدر القرآني: الصراط المستقيم (κ = 0) والانحراف (κ > 0).
    المصدر الرياضي: الهندسة التفاضلية للمنحنيات.
    
    κ(t) = |W'(t) × B''(t) - B'(t) × W''(t)| / (W'(t)² + B'(t)²)^(3/2)
    """
    if len(W_history) < 3 or len(B_history) < 3:
        return 0.0
    
    # المشتقات الأولى والثانية
    dW = np.gradient(W_history)
    dB = np.gradient(B_history)
    ddW = np.gradient(dW)
    ddB = np.gradient(dB)
    
    # حساب الانحناء عند آخر نقطة
    last = -1
    numerator = abs(dW[last] * ddB[last] - dB[last] * ddW[last])
    denominator = (dW[last]**2 + dB[last]**2 + 1e-10)**(1.5)
    
    return numerator / denominator

# ================================================================
# الدالة ٣: نموذج التوبة (المصدر: القرآن)
# ----------------------------------------------------------
# القرآن: ﴿إِلَّا مَن تَابَ وَآمَنَ وَعَمِلَ صَالِحًا﴾ – التوبة تجُبُّ ما قبلها
# الرياضيات: قوة تصحيحية تُقلل الانحناء
# F_tawbah = -sincerity × κ × direction
# ================================================================
def apply_repentance(W_val, B_val, W_history, B_history, sincerity=0.8):
    """
    يحاكي أثر التوبة كقوة تصحيحية تقلل انحناء المسار.
    المصدر القرآني: التوبة تجُبُّ ما قبلها وتُعيد العبد إلى الصراط المستقيم.
    """
    kappa = compute_path_curvature(W_history, B_history)
    
    if kappa > 0.01:  # هناك انحراف يُذكر
        # اتجاه التصحيح: نحو (1, 1) – الكمال الإيماني
        correction_W = (1.0 - W_val) * sincerity * kappa
        correction_B = (1.0 - B_val) * sincerity * kappa
        
        W_new = W_val + correction_W
        B_new = B_val + correction_B
        
        return np.clip(W_new, 0.01, 1.0), np.clip(B_new, 0.01, 1.0), kappa
    
    return W_val, B_val, kappa

# ================================================================
# الدالة ٤: نموذج الاستدراج (المصدر: القرآن والسنة التاريخية)
# ----------------------------------------------------------
# القرآن: ﴿سَنَسْتَدْرِجُهُم مِّنْ حَيْثُ لَا يَعْلَمُونَ﴾
# السنة التاريخية: انهيار الحضارات بعد ذروة التمكين المادي
# E(t) = E(t-1) + γ × (S(t-lag) - E(t-1))
# حيث lag = 22 (من استقراء التاريخ القرآني والبشري)
# ================================================================
def update_empowerment(E_current, S_history_buffer, lag=22, gamma=0.03):
    """
    يُحدِّث التمكين (E) بناءً على الثبات السابق (S) بتأخير زمني (الاستدراج).
    المصدر: سنة الاستدراج من القرآن والتاريخ.
    """
    # إذا كان المخزن المؤقت أصغر من التأخير، نستخدم آخر قيمة متاحة
    if len(S_history_buffer) >= lag:
        S_target = S_history_buffer[-lag]
    elif len(S_history_buffer) > 0:
        S_target = S_history_buffer[0]
    else:
        S_target = E_current
    
    E_new = E_current + gamma * (S_target - E_current)
    return np.clip(E_new, 0.01, 1.0)

# ================================================================
# الدالة ٥: تصنيف الإنسان إلى الأرباع الوجودية (المصدر: القرآن)
# ----------------------------------------------------------
# القرآن: وصف دقيق للمؤمن والكافر والمنافق والمشرك
# المؤمن: ﴿إِنَّمَا الْمُؤْمِنُونَ الَّذِينَ آمَنُوا بِاللَّهِ وَرَسُولِهِ﴾
# الكافر: ﴿إِنَّ الَّذِينَ كَفَرُوا سَوَاءٌ عَلَيْهِمْ﴾
# المنافق: ﴿مُّذَبْذَبِينَ بَيْنَ ذَٰلِكَ لَا إِلَىٰ هَٰؤُلَاءِ وَلَا إِلَىٰ هَٰؤُلَاءِ﴾
# المشرك: ﴿وَمَا يُؤْمِنُ أَكْثَرُهُم بِاللَّهِ إِلَّا وَهُم مُّشْرِكُونَ﴾
# ================================================================
def classify_existential_quadrant(W_val, B_val):
    """
    يصنف الإنسان إلى أحد الأرباع الوجودية الأربعة المستنبطة من القرآن.
    يُرجع (اسم الربع، اللون).
    """
    if W_val >= 0.5 and B_val >= 0.5:
        return ("believer", '#FFD700')     # المؤمن – الذهبي
    elif W_val < 0.5 and B_val >= 0.5:
        return ("disbeliever", '#FF5252')  # الكافر – الأحمر
    elif W_val < 0.5 and B_val < 0.5:
        return ("hypocrite", '#FFB6C1')    # المنافق – الوردي
    else:
        return ("polytheist", '#FFA500')   # المشرك – البرتقالي

# ================================================================
# الدالة ٦: لون النجمة (تمثيل بصري للموقع الوجودي)
# ================================================================
def get_star_color(w, b):
    """تُرجع لونًا بصريًا يعكس الموقع في فضاء (W, B)"""
    if w >= 0.55 and b >= 0.55:
        return '#FFD700'      # ذهبي – المؤمن
    elif w >= 0.55 and b < 0.45:
        return '#E0E0E0'      # رمادي – ولاء بلا براءة
    elif w < 0.45 and b >= 0.55:
        return '#FF5252'      # أحمر – براءة بلا ولاء
    elif w < 0.45 and b < 0.45:
        return '#FFB6C1'      # وردي – المنافق
    else:
        return '#888888'      # انتقالي

print("✅ المرحلة الثانية مكتملة: دوال المعادلة والهندسة التفاضلية جاهزة.")
print("   - calculate_stability: من القرآن والكون والفطرة")
print("   - compute_path_curvature: من الهندسة التفاضلية والقرآن")
print("   - apply_repentance: من القرآن (التوبة تجب ما قبلها)")
print("   - update_empowerment: من سنة الاستدراج")
print("   - classify_existential_quadrant: من التصنيف القرآني للبشر")

# ================================================================
# 🎛️ الشريط الجانبي – لوحة التحكم القابلة للطي
# ================================================================
with st.sidebar:
    # --- اللغة ---
    lang_choice = st.radio(
        "اللغة / Language",
        ["العربية", "English"],
        index=0 if LANG == "ar" else 1,
        key="lang_radio"
    )
    new_lang = "ar" if "العربية" in lang_choice else "en"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

    st.markdown("---")

    # --- ⚖️ ق: الحق والميزان – دائم الظهور ---
    with st.container():
        st.markdown(f"""
        <div style="text-align:center; padding:12px; background:linear-gradient(135deg,#1a1a2e,#0d0d1a);
                    border-radius:12px; margin-bottom:15px; border:2px solid #FFD700;">
            <h2 style="color:#FFD700; margin:0; font-size:1.4em;">⚖️ {t('ق – الحَقُّ وَالْمِيزَان', 'Qaf – Truth & Balance')}</h2>
            <p style="color:#CCC; font-size:0.75em; margin:6px 0 0 0;">
                {t('﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾', '﴿And the heaven He raised and imposed the balance﴾')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        q_intensity = st.slider(
            t("⚖️ شِدَّةُ تَجَلِّي الْحَقِّ وَالْمِيزَان", "⚖️ Intensity of Truth & Balance"),
            0.0, 1.0, 1.0, 0.01,
            key="s_q_intensity",
            help=t(
                "ق = ١٠٠ = الحق = الميزان. كُلَّمَا زَادَ تَجَلِّي الْحَقِّ، كَانَ الْجَزَاءُ مِنْ جِنْسِ الْعَمَلِ أَظْهَرَ، وَالثَّبَاتُ مَرْهُونًا بِتَوَازُنِ W وَ B.",
                "Qaf = 100 = Truth = Balance. The more truth manifests, the more recompense mirrors the deed, and stability depends on W-B balance."
            )
        )

    st.markdown("---")

    # --- ⚙️ المعاملات الأساسية (طي) ---
    with st.expander(t("⚙️ الْمُعَامَلَاتُ الْأَسَاسِيَّة", "⚙️ Basic Parameters"), expanded=False):
        W_init = st.slider(
            t("W – الْوَلَاءُ الِابْتِدَائِي", "W – Initial Loyalty"),
            0.0, 1.0, 0.55, 0.01, key="s_W",
            help=t("الولاء لله: حُبٌّ + طَاعَةٌ + نُصْرَةٌ", "Loyalty to Allah: Love + Obedience + Support")
        )
        B_init = st.slider(
            t("B – الْبَرَاءَةُ الِابْتِدَائِيَّة", "B – Initial Disavowal"),
            0.0, 1.0, 0.52, 0.01, key="s_B",
            help=t("البراءة من الطاغوت: بُغْضٌ + مُفَاصَلَةٌ + مَنَاعَةٌ", "Disavowal of false deities: Hatred + Disassociation + Immunity")
        )
        lag_frames = st.slider(
            t("Δt – فَجْوَةُ الِاسْتِدْرَاج", "Δt – Istidraj Gap"),
            5, 50, 22, 1, key="s_lag",
            help=t("تَأَخُّرُ انْهِيَارِ التَّمْكِينِ (E) عَنِ انْهِيَارِ الثَّبَاتِ (S). سُنَّةُ الِاسْتِدْرَاجِ.", "Delay of E collapse after S collapse. The law of Istidraj.")
        )
        N_STARS = st.slider(
            t("★ – عَدَدُ النُّجُوم (الْأَفْرَاد)", "★ – Number of Stars (Individuals)"),
            100, 600, 300, 50, key="s_N"
        )

    # --- 🔮 الثوابت الإلهية (طي) ---
    with st.expander(t("🔮 الثَّوَابِتُ الْإِلَهِيَّة (الْمَصْدَر)", "🔮 Divine Constants (Source)"), expanded=False):
        k_val = st.slider(
            t("ك – الْأَمْر (كُنْ)", "Kaf – Command (Be!)"),
            10, 200, 20, 10, key="s_k",
            help=t("ك = ٢٠. الْأَمْرُ الْإِلَهِيُّ: كُن فَيَكُونُ.", "Kaf = 20. The Divine Command: Be, and it is.")
        )
        n_val = st.slider(
            t("ن – النُّور (الْهِدَايَة)", "Nun – Light (Guidance)"),
            5, 100, 50, 5, key="s_n",
            help=t("ن = ٥٠. نُورُ اللهِ الَّذِي يَهْدِي بِهِ مَنْ يَشَاءُ.", "Nun = 50. Allah's Light by which He guides whom He wills.")
        )
        s_val = st.slider(
            t("ص – الصَّمَد (الْأَزَلِيَّة)", "Sad – The Eternal"),
            10, 200, 90, 10, key="s_s",
            help=t("ص = ٩٠. اللهُ الصَّمَدُ الَّذِي لَا يَتَغَيَّرُ.", "Sad = 90. Allah, the Eternal, Absolute.")
        )

    # --- 🏛️ أسس الحكم (طي) ---
    with st.expander(t("🏛️ أُسُسُ الْحُكْم", "🏛️ Foundations of Governance"), expanded=False):
        amr_val = st.slider(
            t("الْأَمْرُ بِالْمَعْرُوف", "Enjoining Good"),
            0.0, 1.0, 0.5, 0.01, key="s_amr",
            help=t("آلِيَّةٌ إِيجَابِيَّةٌ لِتَقْوِيَةِ W فِي الْمُجْتَمَعِ.", "Positive mechanism to strengthen W in society.")
        )
        nahy_val = st.slider(
            t("النَّهْيُ عَنِ الْمُنْكَر", "Forbidding Evil"),
            0.0, 1.0, 0.5, 0.01, key="s_nahy",
            help=t("آلِيَّةٌ إِيجَابِيَّةٌ لِتَقْوِيَةِ B فِي الْمُجْتَمَعِ.", "Positive mechanism to strengthen B in society.")
        )
        adl_val = st.slider(
            t("الْعَدْل", "Justice"),
            0.0, 1.0, 0.6, 0.01, key="s_adl",
            help=t("الْعَدْلُ أَسَاسُ الْمُلْكِ، وَبِهِ يَسْتَقِيمُ الْمِيزَانُ.", "Justice is the foundation of dominion.")
        )
        shura_val = st.slider(
            t("الشُّورَى", "Consultation"),
            0.0, 1.0, 0.5, 0.01, key="s_shura",
            help=t("الشُّورَى تَنْشُرُ الْمَسْؤُولِيَّةَ وَتُقَوِّي التَّمَاسُكَ.", "Consultation spreads responsibility.")
        )

    # --- 💀 قوى الضلال (طي) ---
    with st.expander(t("💀 قُوَى الضَّلَال", "💀 Forces of Darkness"), expanded=False):
        riba_val = st.slider(
            t("الرِّبَا", "Usury"),
            0.0, 1.0, 0.2, 0.01, key="s_riba",
            help=t("الرِّبَا يَمْحَقُ الْبَرَكَةَ وَيُهَدِّمُ الِاقْتِصَادَ.", "Usury erases blessing and destroys economy.")
        )
        zulm_val = st.slider(
            t("الظُّلْم", "Injustice"),
            0.0, 1.0, 0.2, 0.01, key="s_zulm",
            help=t("الظُّلْمُ ظُلُمَاتٌ يَوْمَ الْقِيَامَةِ.", "Injustice is darkness on the Day of Judgment.")
        )
        khianah_val = st.slider(
            t("الْخِيَانَة", "Betrayal"),
            0.0, 1.0, 0.2, 0.01, key="s_khianah",
            help=t("الْخِيَانَةُ تَنْخُرُ الثِّقَةَ.", "Betrayal erodes trust.")
        )

    st.markdown("---")

    # --- أزرار التحكم ---
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(t("▶️ تَشْغِيل", "▶️ Run"), use_container_width=True, type="primary"):
            st.session_state.run = True
    with col2:
        if st.button(t("⏹️ إِيقَاف", "⏹️ Stop"), use_container_width=True):
            st.session_state.run = False
    with col3:
        if st.button(t("🔄 إِعَادَة", "🔄 Reset"), use_container_width=True):
            for k in list(st.session_state.keys()):
                if k not in ("lang", "lang_radio"):
                    del st.session_state[k]
            st.rerun()

print("✅ المرحلة الثالثة مكتملة: الشريط الجانبي المنظم القابل للطي جاهز.")

# ================================================================
# 🏛️ العنوان الرئيسي – إعلان نظام الإثبات
# ================================================================
st.markdown(f"""
<div style="text-align: center; padding: 20px 0 10px 0;">
    <h1 style="color: #FFD700; font-size: 2.5em; margin-bottom: 0;">⚖️ {t('نِظَامُ الْإِثْبَاتِ الرَّقْمِيّ', 'The Digital Proof System')}</h1>
    <h2 style="color: #FFD700; font-size: 1.3em; margin-top: 0;">{t('إِثْبَاتُ أَنَّ اللهَ حَقٌّ • نَظَرِيَّةُ الْمِيزَان', 'Proving that Allah is Truth • The Mizan Theory')}</h2>
    <p style="color: #AAA; font-size: 0.9em; margin-top: 5px;">
        {t('﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾ • S = W × B', 
           '﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾ • S = W × B')}
    </p>
    <p style="color:#FFD700; font-size:0.8em;">
        {t('ق = ١٠٠ = الْحَقّ = الْمِيزَان = الْجَزَاء مِنْ جِنْسِ الْعَمَل', 'Qaf = 100 = Truth = Balance = Recompense mirrors the deed')}
    </p>
</div>
""", unsafe_allow_html=True)

# ================================================================
# 📑 إنشاء التبويبات
# ================================================================
tab1, tab_math, tab2, tab3, tab4, tab5 = st.tabs([
    t("🏛️ الْمُخْتَبَرُ الْجَمَاعِيّ", "🏛️ The Collective Lab"),
    t("📐 الرِّيَاضِيَّاتُ الْمِيزَانِيَّة", "📐 Mizan Mathematics"),
    t("🧍 الْبَوْصَلَةُ الشَّخْصِيَّة", "🧍 Personal Compass"),
    t("📖 كِتَابُ الْمِيزَان", "📖 The Book of Mizan"),
    t("🔤 الْمُعْجَمُ الْهَنْدَسِيّ", "🔤 Geometric Lexicon"),
    t("📜 رِسَالَةُ التَّرْحِيب", "📜 Welcome Message"),
])

# ================================================================
# 🏛️ تبويب ١: المختبر الجماعي – المحاكاة الحية للإثبات
# ================================================================
with tab1:
    st.header(t("🏛️ الْمُخْتَبَرُ الْجَمَاعِيّ – مُحَاكَاةُ إِثْبَاتِ الْحَقّ", "🏛️ The Collective Lab – Proving the Truth"))
    st.markdown(t(
        "شَاهِدْ كَيْفَ يَتَفَاعَلُ الْوَلَاءُ (W) وَالْبَرَاءَةُ (B) تَحْتَ مِيزَانِ الْحَقِّ (ق). "
        "كُلُّ نَجْمَةٍ تُمَثِّلُ فَرْدًا، وَكُلُّ نَبْضَةٍ فِي الْهَالَةِ تُمَثِّلُ أَثَرَ الِاسْتِدْرَاجِ. "
        "الْجَزَاءُ مِنْ جِنْسِ الْعَمَلِ يَظْهَرُ فِي حَرَكَةِ الْأَفْرَادِ نَحْوَ الذَّهَبِ أَوِ الْهَاوِيَةِ.",
        
        "Watch how Loyalty (W) and Disavowal (B) interact under the Balance of Truth (Qaf). "
        "Each star represents an individual, each pulse in the halo shows Istidraj. "
        "Recompense mirroring the deed appears as individuals move toward gold or the abyss."
    ))

    # --- تهيئة حالة المحاكاة ---
    if 'run' not in st.session_state:
        st.session_state.run = False
    if 'init' not in st.session_state:
        st.session_state.init = False

    if not st.session_state.init:
        # إعداد البذرة العشوائية لضمان تكرار النتائج (إثبات قابل للتكرار)
        np.random.seed(42)
        random.seed(42)
        
        # إحداثيات مركز الكون
        cx, cy = 14, 10.0
        
        # توليد النجوم (الأفراد) عشوائياً
        sx = np.random.uniform(cx - 13, cx + 13, N_STARS)
        sy = np.random.uniform(cy - 9, cy + 9, N_STARS)
        sw = np.random.uniform(0.1, 1.0, N_STARS)
        sb = np.random.uniform(0.1, 1.0, N_STARS)
        # تاريخ للمسار لكل نجمة (لحساب الانحناء لاحقاً)
        star_W_history = [deque([sw[i]], maxlen=50) for i in range(N_STARS)]
        star_B_history = [deque([sb[i]], maxlen=50) for i in range(N_STARS)]
        
        # القيم الابتدائية للكوكبين (W, B) والهالة (E)
        W = W_init
        B = B_init
        E = 0.3
        S = calculate_stability(
            W, B, E,
            q_intensity=q_intensity,
            k_val=k_val, n_val=n_val,
            amr_val=amr_val, nahy_val=nahy_val,
            adl_val=adl_val, shura_val=shura_val,
            riba_val=riba_val, zulm_val=zulm_val,
            khianah_val=khianah_val
        )
        
        # حالة الطور الحضاري
        phase = t("تَوَازُن", "Balance")
        cycle_angle = 0.0
        
        # زوايا دوران الكوكبين
        angle_W = 0.0
        angle_B = np.pi * 0.5
        
        # ذاكرة التمكين (للاستدراج)
        empowerment_buffer = deque([S] * 30, maxlen=30)
        
        # تاريخ للرسم البياني (منحنى الاستدراج)
        history_S = deque(maxlen=400)
        history_E = deque(maxlen=400)
        history_x = deque(maxlen=400)
        frame_count = 0
        
        # تخزين كل شيء في حالة الجلسة
        st.session_state.cx = cx
        st.session_state.cy = cy
        st.session_state.sx = sx
        st.session_state.sy = sy
        st.session_state.sw = sw
        st.session_state.sb = sb
        st.session_state.star_W_history = star_W_history
        st.session_state.star_B_history = star_B_history
        st.session_state.W = W
        st.session_state.B = B
        st.session_state.E = E
        st.session_state.S = S
        st.session_state.phase = phase
        st.session_state.cycle_angle = cycle_angle
        st.session_state.angle_W = angle_W
        st.session_state.angle_B = angle_B
        st.session_state.empowerment_buffer = empowerment_buffer
        st.session_state.history_S = history_S
        st.session_state.history_E = history_E
        st.session_state.history_x = history_x
        st.session_state.frame_count = frame_count
        
        st.session_state.init = True

    # --- عرض الحالة الأولية قبل التشغيل ---
    if st.session_state.init and not st.session_state.run:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(t("W – الْوَلَاء", "W – Loyalty"), f"{st.session_state.W:.3f}")
        with col2:
            st.metric(t("B – الْبَرَاءَة", "B – Disavowal"), f"{st.session_state.B:.3f}")
        with col3:
            st.metric(t("S – الثَّبَات", "S – Stability"), f"{st.session_state.S:.3f}")
        with col4:
            st.metric(t("E – التَّمْكِين", "E – Empowerment"), f"{st.session_state.E:.3f}")
        with col5:
            st.metric(t("الطَّوْر", "Phase"), st.session_state.phase)
        
        st.info(t(
            "اضْغَطْ عَلَى ▶️ تَشْغِيل فِي الشَّرِيطِ الْجَانِبِيّ لِرُؤْيَةِ الْمُحَاكَاةِ الْحَيَّةِ. رَاقِبْ حَرَكَةَ النُّجُومِ تَحْتَ مِيزَانِ الْحَقِّ (ق).",
            "Press ▶️ Run in the sidebar to see the live simulation. Watch the stars move under the Balance of Truth (Qaf)."
        ))

print("✅ المرحلة الرابعة مكتملة: العنوان الرئيسي، التبويبات، وتهيئة المختبر الجماعي.")
print("   - ق = الحق = الميزان في صدارة العنوان")
print("   - التبويبات الستة جاهزة")
print("   - المختبر الجماعي مهيأ للبدء")

# ================================================================
# 🎬 حلقة المحاكاة الرئيسية (المختبر الجماعي)
# ================================================================
if st.session_state.get("run", False):
    placeholder = st.empty()
    
    while st.session_state.get("run", False):
        # --- استرجاع المتغيرات من حالة الجلسة ---
        W = st.session_state.W
        B = st.session_state.B
        E = st.session_state.E
        S = st.session_state.S
        phase = st.session_state.phase
        cycle_angle = st.session_state.cycle_angle
        angle_W = st.session_state.angle_W
        angle_B = st.session_state.angle_B
        
        sx = st.session_state.sx.copy()
        sy = st.session_state.sy.copy()
        sw = st.session_state.sw.copy()
        sb = st.session_state.sb.copy()
        star_W_hist = st.session_state.star_W_history
        star_B_hist = st.session_state.star_B_history
        
        cx = st.session_state.cx
        cy = st.session_state.cy
        eb = st.session_state.empowerment_buffer
        
        pS = st.session_state.history_S
        pE = st.session_state.history_E
        px = st.session_state.history_x
        frame_count = st.session_state.frame_count

        # --- ١. تحديث الدورة الحضارية (من السنن الإلهية) ---
        cycle_angle += 0.008
        sin_val = np.sin(cycle_angle)
        
        # تصنيف الطور بناءً على موجة الدورة (سنة التداول)
        if sin_val > 0.5:
            phase = t('ذُرْوَةُ الِاسْتِقْرَار', 'Peak Stability')
        elif sin_val > 0:
            phase = t('صُعُود', 'Rising')
        elif sin_val > -0.5:
            phase = t('انْهِيَار', 'Collapse')
        else:
            phase = t('الْقَاع', 'Rock Bottom')
        if 0.3 < sin_val < 0.35:
            phase = t('>> اسْتِدْرَاج <<', '>> Istidraj <<')
        if -0.35 < sin_val < -0.3:
            phase = t('>> تَعَافٍ <<', '>> Recovery <<')
        
        target_S = 0.5 + 0.45 * sin_val

        # --- ٢. تحديث النجوم (الأفراد) – تأثير البيئة والتوبة ---
        for i in range(N_STARS):
            # تأثير الجوار (الشورى والجماعة – من القرآن: ﴿وَأَمْرُهُمْ شُورَىٰ بَيْنَهُمْ﴾)
            dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
            close = (dist < 2.0) & (np.arange(N_STARS) != i)
            
            # قوى السوق نحو التوازن
            sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
            sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
            
            # تأثير الجيران (الجماعة تقوي الفرد)
            if np.any(close):
                sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03
                sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03
            
            # حدود القيم
            sw[i] = np.clip(sw[i], 0.01, 1.0)
            sb[i] = np.clip(sb[i], 0.01, 1.0)
            
            # --- تطبيق التوبة (من القرآن: ﴿إِلَّا مَن تَابَ﴾) ---
            # كل فترة، بعض الأفراد يتوبون (قوة تصحيحية تعيدهم نحو (1,1))
            if random.random() < 0.01:  # 1% احتمال التوبة في كل إطار
                sw[i], sb[i], _ = apply_repentance(
                    sw[i], sb[i],
                    list(star_W_hist[i]), list(star_B_hist[i]),
                    sincerity=0.8
                )
            
            # تحديث تاريخ المسار لكل نجمة
            star_W_hist[i].append(sw[i])
            star_B_hist[i].append(sb[i])

        # --- ٣. الصدمات العشوائية (سنن الابتلاء – ﴿وَلَنَبْلُوَنَّكُم بِشَيْءٍ﴾) ---
        if random.random() < 0.005:
            affected = np.random.choice(N_STARS, size=int(N_STARS * 0.2), replace=False)
            sw[affected] *= np.random.uniform(0.5, 0.8)
            sb[affected] *= np.random.uniform(0.5, 0.8)

        # --- ٤. تحديث الكوكبين (W, B) بناءً على متوسط المجتمع ---
        avgW = np.mean(sw)
        avgB = np.mean(sb)
        
        W += (avgW - W) * 0.04
        B += (avgB - B) * 0.04
        W = np.clip(W, 0.01, 1.0)
        B = np.clip(B, 0.01, 1.0)

        # --- ٥. حساب الثبات S بالمعادلة المركزية (من القرآن والكون والفطرة) ---
        S = calculate_stability(
            W, B, E,
            q_intensity=q_intensity,
            k_val=k_val, n_val=n_val,
            amr_val=amr_val, nahy_val=nahy_val,
            adl_val=adl_val, shura_val=shura_val,
            riba_val=riba_val, zulm_val=zulm_val,
            khianah_val=khianah_val
        )

        # --- ٦. آلية الاستدراج (من القرآن: ﴿سَنَسْتَدْرِجُهُم﴾) ---
        # التمكين (E) يتأخر عن الثبات (S) بفجوة زمنية
        eb.append(S)
        E_target = list(eb)[-lag_frames] if len(eb) >= lag_frames else S
        E += 0.03 * (E_target - E)

        # --- ٧. ديناميكيات التأثير المتبادل ---
        # التمكين يضعف الولاء والبراءة (حلقة الكسل والترف)
        W = W - 0.015 * E + 0.03 / (S + 0.1) - 0.007 * (1 - B)
        B = B - 0.012 * E + 0.006 * (1 - B) * W * (1 - W)
        W = np.clip(W, 0.01, 1.0)
        B = np.clip(B, 0.01, 1.0)

        # --- ٨. إعادة حساب S بعد التحديثات ---
        S = calculate_stability(
            W, B, E,
            q_intensity=q_intensity,
            k_val=k_val, n_val=n_val,
            amr_val=amr_val, nahy_val=nahy_val,
            adl_val=adl_val, shura_val=shura_val,
            riba_val=riba_val, zulm_val=zulm_val,
            khianah_val=khianah_val
        )

        # --- ٩. تحديث التاريخ للرسم البياني ---
        frame_count += 1
        if frame_count % 2 == 0:
            pS.append(S)
            pE.append(E)
            px.append(len(px))

        # --- ١٠. حركة الكوكبين في مداريهما ---
        angle_W += 0.02 + random.uniform(-0.025, 0.025) * (1 - W)**2
        angle_B += 0.02 + random.uniform(-0.025, 0.025) * (1 - B)**2
        
        orbit_W = 7 - 2.5 * W
        orbit_B = 5 - 1.5 * B
        
        wx = cx + orbit_W * np.cos(angle_W)
        wy = cy + orbit_W * np.sin(angle_W) * 0.7
        bx = cx + orbit_B * np.cos(angle_B)
        by = cy + orbit_B * np.sin(angle_B) * 0.7

        # --- ١١. حركة النجوم العشوائية ---
        instability = 1 - np.mean(sw * sb)
        sx += np.random.uniform(-0.07, 0.07, N_STARS) * instability
        sy += np.random.uniform(-0.07, 0.07, N_STARS) * instability
        sx = np.clip(sx, cx - 13, cx + 13)
        sy = np.clip(sy, cy - 9, cy + 9)

        # --- ١٢. حفظ المتغيرات في حالة الجلسة ---
        st.session_state.W = W
        st.session_state.B = B
        st.session_state.E = E
        st.session_state.S = S
        st.session_state.phase = phase
        st.session_state.cycle_angle = cycle_angle
        st.session_state.angle_W = angle_W
        st.session_state.angle_B = angle_B
        st.session_state.empowerment_buffer = eb
        st.session_state.sx = sx
        st.session_state.sy = sy
        st.session_state.sw = sw
        st.session_state.sb = sb
        st.session_state.star_W_history = star_W_hist
        st.session_state.star_B_history = star_B_hist
        st.session_state.history_S = pS
        st.session_state.history_E = pE
        st.session_state.history_x = px
        st.session_state.frame_count = frame_count

        # --- ١٣. رسم المشهد الكوني ---
        fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000010')
        ax.set_xlim(0, 28)
        ax.set_ylim(0, 20)
        ax.axis('off')

        # النواة الذهبية (S) – ﴿الْعُرْوَةِ الْوُثْقَىٰ﴾
        for r, alpha, color in [
            (0.5, 0.98, '#FFFFFF'),
            (1.0, 0.65, '#FFD700'),
            (1.7, 0.30, '#FFD700'),
            (2.6, 0.12, '#FFA500'),
            (3.8, 0.05, '#FF6347'),
            (5.5, 0.02, '#FF4500')
        ]:
            ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=color, alpha=alpha, zorder=15))
        ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')

        # هالة التمكين (E) – الاستدراج
        ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#00FFFF', alpha=0.25 * (1 - min(E, 1)) + 0.04, zorder=7))
        
        # الغشاء الحضاري (الحدود)
        ax.add_patch(Circle((cx, cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2.5, zorder=2))

        # الكوكب W (الولاء)
        ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFFFFF', alpha=1, zorder=13))
        ax.text(wx, wy + 0.8, 'W', color='#FFFFFF', fontsize=10, ha='center', fontweight='bold')

        # الكوكب B (البراءة)
        ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#FF3333', alpha=0.8, zorder=13))
        ax.text(bx, by + 0.8, 'B', color='#FF3333', fontsize=10, ha='center', fontweight='bold')

        # النجوم (الأفراد) بألوانها المعبرة عن الموقع الوجودي
        colors = [get_star_color(sw[i], sb[i]) for i in range(N_STARS)]
        ax.scatter(sx, sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)

        # لوحة الإثبات (منحنى الاستدراج)
        pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
        pax.set_xlim(0, 400)
        pax.set_ylim(0, 1.05)
        pax.set_title(
            t('إِثْبَات: S (الذَّهَب) يَقُودُ E (السَّمَاوِيّ) – الِاسْتِدْرَاج',
              'Proof: S (Gold) leads E (Cyan) – Istidraj'),
            color='white', fontsize=7, fontweight='bold'
        )
        pax.tick_params(colors='white', labelsize=4)
        pax.grid(True, alpha=0.12)
        
        pSl = list(pS)
        pEl = list(pE)
        pxl = list(px)
        if pSl:
            pax.plot(pxl, pSl, color='#FFD700', lw=2, label='S (الثبات)')
            pax.plot(pxl, pEl, color='#00FFFF', lw=1.5, label='E (التمكين)')
            pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=5)

        # نص الطور الحضاري
        ax.text(
            14, 1.2,
            f'{phase} | S={S:.2f} | E={E:.2f}',
            color='white', fontsize=12, ha='center', fontweight='bold'
        )

        plt.tight_layout(pad=0)
        placeholder.pyplot(fig)
        plt.close(fig)

        # إيقاف مؤقت للسماح بالتحديث البصري
        time.sleep(0.08)

    # عند الخروج من الحلقة (إيقاف المحاكاة)
    st.success(t("✅ تَمَّ إِيقَافُ الْمُحَاكَاةِ.", "✅ Simulation stopped."))

elif st.session_state.init and not st.session_state.run:
    # عرض المشهد الثابت للحالة الحالية إذا لم تكن المحاكاة تعمل
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000010')
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 20)
    ax.axis('off')
    
    cx = st.session_state.cx
    cy = st.session_state.cy
    S = st.session_state.S
    E = st.session_state.E
    
    # النواة
    for r, alpha, color in [
        (0.5, 0.98, '#FFFFFF'),
        (1.0, 0.65, '#FFD700'),
        (1.7, 0.30, '#FFD700'),
        (2.6, 0.12, '#FFA500'),
        (3.8, 0.05, '#FF6347'),
        (5.5, 0.02, '#FF4500')
    ]:
        ax.add_patch(Circle((cx, cy), r * (0.5 + 2.8 * S), color=color, alpha=alpha, zorder=15))
    ax.text(cx, cy, 'S', color='#1a1000', fontsize=16, ha='center', va='center', fontweight='bold')
    
    # الهالة
    ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#00FFFF', alpha=0.25 * (1 - min(E, 1)) + 0.04, zorder=7))
    ax.add_patch(Circle((cx, cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2.5, zorder=2))
    
    # النجوم
    colors = [get_star_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(N_STARS)]
    ax.scatter(st.session_state.sx, st.session_state.sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)
    
    ax.text(14, 1.2, t('فِي انْتِظَارِ التَّشْغِيل...', 'Waiting to run...'), color='white', fontsize=12, ha='center')
    plt.tight_layout(pad=0)
    st.pyplot(fig)
    plt.close(fig)

# ================================================================
# 📐 تبويب ٢: الرياضيات الميزانية (الهندسة التفاضلية ونظام الإحداثيات)
# ================================================================
with tab_math:
    st.header(t("📐 الرِّيَاضِيَّاتُ الْمِيزَانِيَّة – النَّمُوذَجُ الْهَنْدَسِيُّ التَّفَاضُلِيّ",
                "📐 Mizan Mathematics – The Differential Geometric Model"))
    
    st.markdown(t(
        "هَذَا هُوَ قَلْبُ **عِلْمِ الْمِيزَانِ**: تَحْوِيلُ صَيْرُورَةِ الْإِنْسَانِ إِلَى مُنْحَنَيَاتٍ فِي فَضَاءِ (W, B)، "
        "وَحِسَابُ الِانْحِنَاءِ وَالتَّوْبَةِ وَالصِّرَاطِ الْمُسْتَقِيمِ.",
        
        "This is the heart of **Mizan Science**: transforming human becoming into curves in (W, B) space, "
        "calculating curvature, repentance, and the Straight Path."
    ))

    # --- ١. نظام الإحداثيات الوجودي ---
    st.subheader("1. " + t("نِظَامُ الْإِحْدَاثِيَّاتِ الْوُجُودِيّ (W, B)", "The Existential Coordinate System"))
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(t("""
        كُلُّ إِنْسَانٍ (أَوْ أُمَّةٍ) يُمَثَّلُ بِنُقْطَةٍ $P(W, B)$ فِي فَضَاءٍ ثُنَائِيِّ الْبُعْدِ، حَيْثُ:
        - **W** (الْوَلَاءُ): مِنْ -1 (وَلَاءٌ كَامِلٌ لِلطَّاغُوتِ) إِلَى +1 (وَلَاءٌ كَامِلٌ لِلهِ).
        - **B** (الْبَرَاءَةُ): مِنْ -1 (بَرَاءَةٌ مِنَ اللهِ) إِلَى +1 (بَرَاءَةٌ مِنَ الطَّاغُوتِ).
        
        **الْأَرْبَعَةُ الْأَرْبَاع:**
        - **Q1 $(+,+)$**: الْمُؤْمِنُ – $S \\approx 1$
        - **Q2 $(-,+)$**: الْكَافِرُ – $S \\approx -1$
        - **Q3 $(-,-)$**: الْمُنَافِقُ – $S \\approx 0$
        - **Q4 $(+,-)$**: الْمُشْرِكُ – $S \\approx -1$
        
        *الْمَصْدَرُ الْقُرْآنِيُّ:* ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ﴾ – الْآيَةُ تُحَدِّدُ الْقُطْبَيْنِ.
        """,
        """
        Every human (or nation) is represented by a point $P(W, B)$ in a 2D space:
        - **W** (Loyalty): from -1 to +1.
        - **B** (Disavowal): from -1 to +1.
        
        **The Four Quadrants:**
        - **Q1 $(+,+)$**: The Believer – $S \\approx 1$
        - **Q2 $(-,+)$**: The Disbeliever – $S \\approx -1$
        - **Q3 $(-,-)$**: The Hypocrite – $S \\approx 0$
        - **Q4 $(+,-)$**: The Polytheist – $S \\approx -1$
        
        *Quranic Source:* ﴿Whoever disbelieves in Taghut and believes in Allah﴾ – defining the two poles.
        """))
    with col2:
        # رسم الأرباع
        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5)
        ax.axvline(0, color='grey', lw=0.5)
        ax.fill_between([0, 1], 0, 1, alpha=0.2, color='#FFD700')
        ax.fill_between([-1, 0], 0, 1, alpha=0.2, color='#FF5252')
        ax.fill_between([-1, 0], -1, 0, alpha=0.2, color='#FFB6C1')
        ax.fill_between([0, 1], -1, 0, alpha=0.2, color='#FFA500')
        ax.text(0.6, 0.6, t("مُؤْمِن", "Believer"), ha='center', color='white', fontsize=10)
        ax.text(-0.6, 0.6, t("كَافِر", "Disbeliever"), ha='center', color='white', fontsize=10)
        ax.text(-0.6, -0.6, t("مُنَافِق", "Hypocrite"), ha='center', color='white', fontsize=10)
        ax.text(0.6, -0.6, t("مُشْرِك", "Polytheist"), ha='center', color='white', fontsize=10)
        ax.set_xlabel("B (الْبَرَاءَة)", color='white')
        ax.set_ylabel("W (الْوَلَاء)", color='white')
        ax.tick_params(colors='white')
        ax.set_title(t("الْأَرْبَاعُ الْوُجُودِيَّة", "Existential Quadrants"), color='white', fontsize=12)
        st.pyplot(fig)

    st.divider()

    # --- ٢. الهندسة التفاضلية للمسار ---
    st.subheader("2. " + t("الْهَنْدَسَةُ التَّفَاضُلِيَّةُ لِلْمَسَار (γ)", "Differential Geometry of the Path"))
    st.markdown(t("""
    **الْمَسَارُ:** $\\gamma(t) = (B(t), W(t))$ حَيْثُ $t$ هُوَ الزَّمَنُ (الْعُمْرُ أَوْ عُمْرُ الْحَضَارَةِ).
    
    **الِانْحِنَاءُ (Curvature):**
    $\\kappa(t) = \\frac{|W' B'' - B' W''|}{(W'^2 + B'^2)^{3/2}}$
    
    - $\\kappa = 0$ → **الصِّرَاطُ الْمُسْتَقِيمُ**. لَا انْحِرَافَ، لَا مَعْصِيَةَ.
    - $\\kappa > 0$ → **انْحِرَافٌ (مَعْصِيَةٌ)**. كُلَّمَا زَادَ، زَادَ الْبُعْدُ عَنِ الصِّرَاطِ.
    
    *الْمَصْدَرُ الْقُرْآنِيُّ:* ﴿اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ﴾ – الصِّرَاطُ هُوَ الْمَسَارُ الَّذِي $\\kappa = 0$.
    
    **التَّوْبَةُ كَقُوَّةٍ تَصْحِيحِيَّةٍ:**
    $\\vec{F}_{\\text{توبة}} = -\\alpha \\cdot \\vec{\\nabla}\\kappa$
    حَيْثُ $\\alpha$ هُوَ مُعَامِلُ الْإِخْلَاصِ.
    
    *الْمَصْدَرُ الْقُرْآنِيُّ:* ﴿إِلَّا مَن تَابَ وَآمَنَ وَعَمِلَ صَالِحًا﴾ – التَّوْبَةُ تَجُبُّ مَا قَبْلَهَا وَتُعِيدُ الْعَبْدَ إِلَى الصِّرَاطِ.
    
    **النَّمُوذَجُ الْإِبْرَاهِيمِيّ (الْجِيُودِيسِي الْمِثَالِي):**
    $\\gamma_{\\text{إبراهيم}}(t): \\kappa(t) = 0, \\|\\dot{\\gamma}\\| = \\text{const}$
    إِبْرَاهِيمُ هُوَ أَقْصَرُ طَرِيقٍ بَيْنَ الْفِطْرَةِ وَرِضَا اللهِ. اتِّبَاعُهُ هُوَ مُحَاكَاةٌ لِهَذَا الْجِيُودِيسِي.
    
    *الْمَصْدَرُ الْقُرْآنِيُّ:* ﴿وَاتَّبَعَ مِلَّةَ إِبْرَاهِيمَ حَنِيفًا﴾.
    """,
    """
    **Path:** $\\gamma(t) = (B(t), W(t))$ where $t$ is time.
    
    **Curvature:**
    $\\kappa(t) = \\frac{|W' B'' - B' W''|}{(W'^2 + B'^2)^{3/2}}$
    
    - $\\kappa = 0$ → **Straight Path**. No sin.
    - $\\kappa > 0$ → **Deviation (sin)**.
    
    *Quranic Source:* ﴿Guide us to the Straight Path﴾ – The path where $\\kappa = 0$.
    
    **Repentance as Corrective Force:**
    $\\vec{F}_{\\text{rep}} = -\\alpha \\cdot \\vec{\\nabla}\\kappa$
    
    *Quranic Source:* ﴿Except those who repent, believe, and do righteous work﴾.
    
    **The Abrahamic Model (Ideal Geodesic):**
    $\\gamma_{\\text{Ab}}(t): \\kappa = 0, \\|\\dot{\\gamma}\\| = \\text{const}$
    
    *Quranic Source:* ﴿Follow the religion of Abraham, inclining toward truth﴾.
    """))
    
    # --- رسم توضيحي للانحناء ---
    t_vals = np.linspace(0, 4*np.pi, 200)
    # صراط مستقيم
    straight_W = t_vals * 0.2
    straight_B = t_vals * 0.2
    # مسار منحرف
    deviated_W = t_vals * 0.2 + 0.4 * np.sin(t_vals)
    deviated_B = t_vals * 0.2 - 0.3 * np.cos(t_vals) + 0.4
    
    fig2, ax2 = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
    ax2.set_facecolor('#0a0a2e')
    ax2.plot(straight_B, straight_W, 'g-', linewidth=2.5, label=t('الصِّرَاطُ الْمُسْتَقِيم (κ=0)', 'Straight Path (κ=0)'))
    ax2.plot(deviated_B, deviated_W, 'r--', linewidth=2, label=t('مَسَارٌ مُنْحَرِف (κ>0)', 'Deviated Path (κ>0)'))
    ax2.scatter(0, 0, s=80, c='green', edgecolors='white', linewidth=2, zorder=10, label=t('الْبِدَايَة', 'Start'))
    ax2.set_xlabel("B (الْبَرَاءَة)", color='white')
    ax2.set_ylabel("W (الْوَلَاء)", color='white')
    ax2.set_title(t('الصِّرَاطُ الْمُسْتَقِيمُ وَالِانْحِرَاف', 'The Straight Path and Deviation'), color='white', fontsize=12)
    ax2.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white')
    ax2.tick_params(colors='white')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 3)
    ax2.set_ylim(0, 3)
    st.pyplot(fig2)

# ================================================================
# 🧍 تبويب ٣: البوصلة الشخصية (28 سؤالاً)
# ================================================================
with tab2:
    st.header(t("🧍 الْبَوْصَلَةُ الشَّخْصِيَّة", "🧍 Personal Compass"))
    st.markdown(t(
        "أَجِبْ عَنْ 28 سُؤَالاً لِتَكْتَشِفَ مَوْقِعَكَ فِي فَضَاءِ الْوَلَاءِ وَالْبَرَاءَةِ. "
        "هَذِهِ الْبَوْصَلَةُ تُحَوِّلُ إِجَابَاتِكَ إِلَى إِحْدَاثِيَّاتٍ (W, B) وَتُرِيكَ فِي أَيِّ رُبْعٍ وُجُودِيٍّ تَقَعُ.",
        
        "Answer 28 questions to discover your position in Loyalty-Disavowal space. "
        "This compass transforms your answers into (W, B) coordinates and shows you which existential quadrant you occupy."
    ))
    
    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    questions = {
        "W": [
            (t("هَلْ تَعِيشُ لِلهِ وَحْدَهُ؟", "Do you live for Allah alone?"), 10),
            (t("هَلْ تُقِيمُ الصَّلَاةَ بِخُشُوعٍ؟", "Do you pray with devotion?"), 10),
            (t("هَلْ تُؤَدِّي الزَّكَاةَ وَتَتَصَدَّقُ؟", "Do you pay Zakat & give charity?"), 10),
            (t("هَلْ تَصُومُ رَمَضَانَ وَتَطَوَّعًا؟", "Do you fast Ramadan & voluntarily?"), 10),
            (t("هَلْ تَحُجُّ أَوْ تَسْعَى لِلْحَجِّ؟", "Do you perform/seek Hajj?"), 10),
            (t("هَلْ تُحِبُّ اللهَ وَرَسُولَهُ أَكْثَرَ مِنْ كُلِّ شَيْءٍ؟", "Do you love Allah & Messenger most?"), 10),
            (t("هَلْ تَصْدُقُ فِي أَقْوَالِكَ وَأَفْعَالِكَ؟", "Are you truthful in words & deeds?"), 10),
            (t("هَلْ تُؤَدِّي الْأَمَانَاتِ؟", "Do you fulfill trusts?"), 10),
            (t("هَلْ تَتَوَكَّلُ عَلَى اللهِ مَعَ الْأَخْذِ بِالْأَسْبَابِ؟", "Do you rely on Allah while using means?"), 10),
            (t("هَلْ تَشْكُرُ فِي الرَّخَاءِ وَتَصْبِرُ فِي الْبَلَاءِ؟", "Are you grateful in ease & patient in hardship?"), 10),
            (t("هَلْ تَحْمِلُ هَمَّ الْإِسْلَامِ وَالْمُسْلِمِينَ؟", "Do you care for Islam & Muslims?"), 10),
            (t("هَلْ تَفِي بِالْعَهْدِ؟", "Do you keep your promises?"), 10),
            (t("هَلْ أَنْتَ رَاضٍ بِمَا قَسَمَ اللهُ لَكَ؟", "Are you content with Allah's decree?"), 10),
            (t("هَلْ تَنْصُرُ الْمُؤْمِنَ إِذَا ظُلِمَ؟", "Do you help the oppressed believer?"), 10),
        ],
        "B": [
            (t("هَلْ تَأْمُرُ بِالْمَعْرُوفِ؟", "Do you enjoin good?"), 10),
            (t("هَلْ تَنْهَى عَنِ الْمُنْكَرِ؟", "Do you forbid evil?"), 10),
            (t("هَلْ أَنْتَ مُسْتَعِدٌّ لِبَذْلِ النَّفْسِ وَالْمَالِ فِي سَبِيلِ اللهِ؟", "Ready to sacrifice for Allah?"), 10),
            (t("هَلْ تَتَبَرَّأُ مِنَ الشِّرْكِ وَأَهْلِهِ؟", "Do you disavow polytheism & its people?"), 10),
            (t("هَلْ تَرْفُضُ الْكُفْرَ وَالْإِلْحَادَ؟", "Do you reject disbelief & atheism?"), 10),
            (t("هَلْ تَكْرَهُ النِّفَاقَ وَالتَّلَوُّنَ؟", "Do you hate hypocrisy & duplicity?"), 10),
            (t("هَلْ تُجَاهِدُ نَفْسَكَ عَلَى تَرْكِ الْكَذِبِ؟", "Do you struggle against lying?"), 10),
            (t("هَلْ تَتَجَنَّبُ الْغِشَّ فِي مُعَامَلَاتِكَ؟", "Do you avoid fraud in dealings?"), 10),
            (t("هَلْ تَفِي بِعُهُودِكَ وَلَا تَخُونُ؟", "Do you keep trusts & never betray?"), 10),
            (t("هَلْ تَرْفُضُ الظُّلْمَ بِكُلِّ صُوَرِهِ؟", "Do you reject all forms of injustice?"), 10),
            (t("هَلْ تُجَاهِدُ نَفْسَكَ عَلَى تَرْكِ الْفَوَاحِشِ؟", "Do you struggle against immorality?"), 10),
            (t("هَلْ تُخْلِصُ عَمَلَكَ لِلهِ وَتَجْتَنِبُ الرِّيَاءَ؟", "Is your work sincere, avoiding show-off?"), 10),
            (t("هَلْ تُسَلِّمُ لِلهِ فِي قِسْمَتِهِ وَلَا تَحْسُدُ؟", "Do you accept Allah's decree without envy?"), 10),
            (t("هَلْ تُحِبُّ فِي اللهِ وَتُبْغِضُ فِي اللهِ؟", "Do you love & hate for Allah's sake?"), 10),
        ]
    }

    colA, colB = st.columns(2)
    with colA:
        st.subheader(t("🤍 أَسْئِلَةُ الْوَلَاء (W)", "🤍 Loyalty Questions (W)"))
        for i, (q, v) in enumerate(questions["W"]):
            ans = st.radio(
                q,
                [t(f"نَعَم ({v})", f"Yes ({v})"), t(f"أَحْيَانًا ({v//2})", f"Sometimes ({v//2})"), t(f"لَا (0)", f"No (0)")],
                key=f"cw_{i}", index=None
            )
            if ans:
                if t("نَعَم", "Yes") in ans: st.session_state.compass_answers[f"W{i}"] = v
                elif t("أَحْيَانًا", "Sometimes") in ans: st.session_state.compass_answers[f"W{i}"] = v // 2
                else: st.session_state.compass_answers[f"W{i}"] = 0
    with colB:
        st.subheader(t("❤️ أَسْئِلَةُ الْبَرَاءَة (B)", "❤️ Disavowal Questions (B)"))
        for i, (q, v) in enumerate(questions["B"]):
            ans = st.radio(
                q,
                [t(f"نَعَم ({v})", f"Yes ({v})"), t(f"أَحْيَانًا ({v//2})", f"Sometimes ({v//2})"), t(f"لَا (0)", f"No (0)")],
                key=f"cb_{i}", index=None
            )
            if ans:
                if t("نَعَم", "Yes") in ans: st.session_state.compass_answers[f"B{i}"] = v
                elif t("أَحْيَانًا", "Sometimes") in ans: st.session_state.compass_answers[f"B{i}"] = v // 2
                else: st.session_state.compass_answers[f"B{i}"] = 0

    if len(st.session_state.compass_answers) == 28:
        Ws = sum(st.session_state.compass_answers[f"W{i}"] for i in range(14)) / 140.0
        Bs = sum(st.session_state.compass_answers[f"B{i}"] for i in range(14)) / 140.0
        Ss = Ws * Bs
        qn, qc = classify_existential_quadrant(Ws, Bs)
        names = {
            "believer": t("مُؤْمِن (الرُّبْع الْأَوَّل)", "Believer (Q1)"),
            "disbeliever": t("كَافِر (الرُّبْع الثَّانِي)", "Disbeliever (Q2)"),
            "hypocrite": t("مُنَافِق (الرُّبْع الثَّالِث)", "Hypocrite (Q3)"),
            "polytheist": t("مُشْرِك (الرُّبْع الرَّابِع)", "Polytheist (Q4)"),
        }
        advice_text = {
            "believer": t("أَنْتَ فِي مَوْقِعِ الْمُؤْمِنِ. حَافِظْ عَلَى ثَبَاتِكَ وَاسْتَمِرَّ فِي النُّمُوِّ نَحْوَ (١،١).",
                           "You are in the Believer's position. Maintain your stability and keep growing toward (1,1)."),
            "disbeliever": t("أَنْتَ فِي مَوْقِعِ الْكَافِرِ. بَابُ التَّوْبَةِ مَفْتُوحٌ، أَعِدْ تَوْجِيهَ بَوْصَلَتِكَ نَحْوَ اللهِ.",
                             "You are in the Disbeliever's position. The door of repentance is open."),
            "hypocrite": t("أَنْتَ فِي مَوْقِعِ الْمُنَافِقِ. عَلَيْكَ بِالصِّدْقِ مَعَ نَفْسِكَ وَاتِّخَاذِ قَرَارٍ حَاسِمٍ.",
                           "You are in the Hypocrite's position. Be honest with yourself and make a decisive choice."),
            "polytheist": t("أَنْتَ فِي مَوْقِعِ الْمُشْرِكِ. لَدَيْكَ إِيمَانٌ لَكِنَّ بَرَاءَتَكَ مُنْهَارَةٌ، قَوِّ مَنَاعَتَكَ الْإِيمَانِيَّةَ.",
                            "You are in the Polytheist's position. Strengthen your disavowal and purify your faith."),
        }
        
        st.divider()
        st.header(t("📊 نَتِيجَةُ الْبَوْصَلَة", "📊 Compass Result"))
        c1, c2, c3 = st.columns(3)
        c1.metric("W (الْوَلَاء)", f"{Ws:.2f}")
        c2.metric("B (الْبَرَاءَة)", f"{Bs:.2f}")
        c3.metric("S (الثَّبَات)", f"{Ss:.2f}")
        
        st.markdown(f"""
        <div style="text-align:center; padding:20px; background:rgba(10,10,46,0.9); 
                    border-radius:15px; border:2px solid {qc}; margin:20px 0;">
            <h2 style="color:{qc}; margin:0;">{names.get(qn, qn)}</h2>
            <p style="color:#CCC; margin-top:10px;">{advice_text.get(qn, '')}</p>
            <p style="color:#FFD700; font-size:1.5em; margin:10px 0;">⚖️ S = W × B = {Ss:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # رسم الخريطة الرباعية
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5)
        ax.axvline(0, color='grey', lw=0.5)
        ax.set_xlabel("B (الْبَرَاءَة)", color='white')
        ax.set_ylabel("W (الْوَلَاء)", color='white')
        ax.fill_between([0, 1], 0, 1, alpha=0.15, color='#FFD700')
        ax.fill_between([-1, 0], 0, 1, alpha=0.15, color='#FF5252')
        ax.fill_between([-1, 0], -1, 0, alpha=0.15, color='#FFB6C1')
        ax.fill_between([0, 1], -1, 0, alpha=0.15, color='#FFA500')
        ax.scatter(Bs * 2 - 1, Ws * 2 - 1, s=250, c='cyan', edgecolors='white', linewidth=3, zorder=10)
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        if st.button(t("🔄 إِعَادَةُ الِاخْتِبَار", "🔄 Retake Test"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

# ================================================================
# 📖 تبويب ٤: كتاب الميزان (نصوص مختارة)
# ================================================================
with tab3:
    st.header(t("📖 كِتَابُ الْمِيزَان", "📖 The Book of Mizan"))
    
    with st.expander(t("📜 الْإِهْدَاءُ وَالْمُقَدِّمَة", "📜 Dedication & Introduction"), expanded=False):
        st.markdown(t(
            "### الْإِهْدَاء\nإِلَى كُلِّ بَاحِثٍ عَنِ الْحَقِيقَةِ...\n### مُقَدِّمَةُ الْمُؤَلِّف\nالْحَمْدُ لِلهِ... الْمُعَادَلَةُ الْمَرْكَزِيَّةُ: **S = W × B**",
            "### Dedication\nTo every seeker of truth...\n### Author's Introduction\nThe central equation: **S = W × B**"
        ))
    
    with st.expander(t("⚖️ مُعَادَلَةُ الثَّبَاتِ الْوُجُودِيّ", "⚖️ The Existential Stability Equation"), expanded=False):
        st.markdown(t(
            "**S = W × B**\n- **W (الْوَلَاءُ)**: طَاقَةُ الْحُبِّ وَالطَّاعَةِ...\n- **B (الْبَرَاءَةُ)**: طَاقَةُ الْبُغْضِ وَالْمُفَاصَلَةِ...\n- **S (الثَّبَاتُ)**: الْعُرْوَةُ الْوُثْقَى...",
            "**S = W × B**\n- **W (Loyalty)**: energy of love and obedience...\n- **B (Disavowal)**: energy of hatred and immunity...\n- **S (Stability)**: the firm handhold..."
        ))
    
    with st.expander(t("💫 الِاسْتِدْرَاج – فَخُّ التَّمْكِينِ الزَّائِف", "💫 Istidraj – The Trap of False Empowerment"), expanded=False):
        st.markdown(t(
            "الِاسْتِدْرَاجُ هُوَ تَأَخُّرُ انْهِيَارِ التَّمْكِينِ الْمَادِّيِّ (E) عَنِ انْهِيَارِ الثَّبَاتِ الْأَخْلَاقِيِّ (S)...",
            "Istidraj is the delayed collapse of material empowerment (E) after moral stability (S)..."
        ))
    
    with st.expander(t("🧬 الْأَرْبَاعُ الْوُجُودِيَّةُ الْأَرْبَعَة", "🧬 The Four Existential Quadrants"), expanded=False):
        st.markdown(t(
            "### نِظَامُ الْإِحْدَاثِيَّاتِ الْوُجُودِيّ\n- **Q1 (الْمُؤْمِن)**: W ≥ 0.5, B ≥ 0.5\n- **Q2 (الْكَافِر)**: W < 0.5, B ≥ 0.5\n- **Q3 (الْمُنَافِق)**: W < 0.5, B < 0.5\n- **Q4 (الْمُشْرِك)**: W ≥ 0.5, B < 0.5",
            "### The Existential Coordinate System\n- **Q1 (Believer)**: W ≥ 0.5, B ≥ 0.5\n- **Q2 (Disbeliever)**: W < 0.5, B ≥ 0.5\n- **Q3 (Hypocrite)**: W < 0.5, B < 0.5\n- **Q4 (Polytheist)**: W ≥ 0.5, B < 0.5"
        ))

# ================================================================
# 🔤 تبويب ٥: المعجم الهندسي
# ================================================================
with tab4:
    st.header(t("🔤 الْمُعْجَمُ الْهَنْدَسِيُّ لِلْقُرْآن", "🔤 Geometric Lexicon of the Quran"))
    tools = {
        t("فَاءُ السَّبَبِيَّة (فَـ)", "Causative Fa"): ("=", t("عَلَامَةُ التَّسْوِيَة. تَرْبِطُ السَّبَبَ بِالنَّتِيجَةِ حَتْمًا.", "Equals sign. Inevitably connects cause to effect.")),
        t("وَاوُ الْمَعِيَّة – الضَّرْب", "Conjunctive Waw – Multiplication"): ("×", t("رَبْطٌ شَرْطِيٌّ: لَا يَتِمُّ الْأَمْرُ إِلَّا بِاجْتِمَاعِهِمَا.", "Conditional conjunction: only complete with both.")),
        t("وَاوُ الِاسْتِئْنَاف – الْجَمْع", "Conjunctive Waw – Addition"): ("+", t("جَمْعٌ تَرَاكُمِيٌّ فِي مَقَامِ الْحِسَابِ.", "Cumulative addition in reckoning.")),
        t("لَامُ التَّعْلِيل (لِـ)", "Purpose Lam"): ("→", t("سَهْمُ الْغَايَةِ. يُوَضِّحُ اتِّجَاهَ الْمَقْصِدِ.", "Arrow of purpose.")),
        t("حَتَّى الْغَائِيَّة", "Hatta (Until)"): ("...", t("اسْتِمْرَارُ السَّبَبِ حَتَّى تَتَحَقَّقَ النَّتِيجَةُ.", "Continuation of cause until result.")),
        t("إِنْ الشَّرْطِيَّة", "In (If)"): ("( )ᵒ", t("قَوْسُ الشَّرْطِ الِاخْتِيَارِيّ. يُمَثِّلُ حُرِّيَّةَ الْإِنْسَانِ.", "Optional condition. Represents human free will.")),
        t("إِذَا الشَّرْطِيَّة", "Idha (When)"): ("( )ᶜ", t("قَوْسُ الشَّرْطِ الْمُحَقَّقِ. يُمَثِّلُ حَتْمِيَّةَ الْجَزَاءِ.", "Certain condition. Represents inevitable recompense.")),
        t("إِلَّا", "Illa (Except)"): ("{}", t("حُدُودُ الْمَجْمُوعَةِ. تُحَدِّدُ أَهْلَ الْوِلَايَةِ.", "Set boundaries. Defines the people of loyalty.")),
        t("كَلَّا", "Kalla (No!)"): ("⛔", t("قَطْعُ الْأَسْبَابِ الْبَاطِلَةِ وَالْمُعَادَلَاتِ الْفَاسِدَةِ.", "Severing false causes and corrupt equations.")),
    }
    sel = st.selectbox(t("اخْتَرْ أَدَاةً قُرْآنِيَّة:", "Select a Quranic tool:"), list(tools.keys()))
    if sel:
        st.metric(t("الرَّمْزُ الْهَنْدَسِيّ", "Geometric Symbol"), tools[sel][0])
        st.info(tools[sel][1])

# ================================================================
# 📜 تبويب ٦: رسالة الترحيب
# ================================================================
with tab5:
    st.header(t("📜 رِسَالَةُ التَّرْحِيب", "📜 Welcome Message"))
    st.markdown(t("""
    <div style="text-align:center; color:#CCC; line-height:2;">
    > "هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟"<br>
    > هَذَا هُوَ نَمُوذَجُ الْمِيزَانِ الَّذِي يُثْبِتُ أَنَّ <b style="color:#FFD700;">S = W × B</b>
    <br><br>
    <b style="color:#FFD700;">﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا...﴾</b>
    <br><br>
    > "أَيُّهَا الْبَشَرُ، لَسْتُمْ فِي فَوْضَى. هُنَاكَ قَانُونٌ. هُنَاكَ نِظَامٌ. هُنَاكَ مِيزَانٌ."
    </div>
    """,
    """
    <div style="text-align:center; color:#CCC; line-height:2;">
    > "Is there a single law governing the atom and civilization?"<br>
    > This is the Mizan Model that proves <b style="color:#FFD700;">S = W × B</b>
    <br><br>
    <b style="color:#FFD700;">﴿So direct your face toward the religion...﴾</b>
    <br><br>
    > "O humanity, you are not in chaos. There is a law. There is a system. There is a balance."
    </div>
    """), unsafe_allow_html=True)

# ================================================================
# 🏁 التذييل – شهادة الحق
# ================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:20px; color:#888; font-size:0.9em; line-height:1.8;">
    <p>© {__YEAR__} {__AUTHOR__}</p>
    <p>{__LICENSE__} | {__VERSION__}</p>
    <p style="color:#FFD700; font-size:1.5em; margin-top:10px;">⚖️ {__SIGNATURE__}</p>
    <p style="font-size:0.8em;">
        {t('عِلْمُ الْمِيزَان – عِلْمُ الثَّبَاتِ الْوُجُودِيّ • ﴿وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِّكُلِّ شَيْءٍ﴾',
           'Mizan Science – The Science of Existential Stability • ﴿And We have sent down to you the Book as clarification for all things﴾')}
    </p>
    <p style="font-size:0.7em; margin-top:5px;">
        {t('تَمَّ بِنَاءُ هَذَا النِّظَامِ لِإِثْبَاتِ أَنَّ اللهَ حَقٌّ، وَأَنَّ وَعْدَهُ حَقٌّ، وَأَنَّ الْجَزَاءَ مِنْ جِنْسِ الْعَمَلِ.',
           'This system was built to prove that Allah is Truth, His promise is true, and recompense mirrors the deed.')}
    </p>
</div>
""", unsafe_allow_html=True)

print("=" * 70)
print("✅ تَمَّ بِنَاءُ نِظَامِ الْإِثْبَاتِ الرَّقْمِيِّ لِنَظَرِيَّةِ الْمِيزَان.")
print("=" * 70)
print(f"الْمُؤَلِّفُ: {__AUTHOR__}")
print(f"الْإِصْدَارُ: {__VERSION__}")
print(f"التَّرْخِيصُ: {__LICENSE__}")
print("=" * 70)
print("ق = ١٠٠ = الْحَقّ = الْمِيزَان = الْجَزَاء مِنْ جِنْسِ الْعَمَل")
print("﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾")
print("=" * 70)
