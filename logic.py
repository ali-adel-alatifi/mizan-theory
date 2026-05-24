# mizan/logic.py
"""
وحدة المنطق الرياضي والمحاكاة
تحتوي: المحكمة العليا، حساب S (الأساسية والموسعة)، المحاكاة الزمنية، حساب البوصلة، الانحناء
"""

import numpy as np
import random
from config import LETTERS_DB, TXT

# =============================================
# 1. المحكمة العليا (4 بوابات)
# =============================================
def supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal):
    """
    تقييم الحالة عبر البوابات الأربع وإرجاع الحكم.
    المعاملات:
        W_raw, B_raw: قيمتا الولاء والبراءة الخام (من -1 إلى 1)
        W_pure: هل الولاء خالص لله (عدم الشرك)
        B_compassion: مؤشر الرحمة والعطاء (من B_vals)
        B_disavowal: مؤشر البراءة من الطاغوت (من B_vals)
    الإرجاع:
        S_gate: قيمة الثبات بعد الحكم (0, -1, 1, أو None للمرور للمعادلة العامة)
        gate_name, gate_msg, gate_color: تفاصيل البوابة
    """
    # البوابة 1: الشرك
    if not W_pure:
        return (0, TXT("بوابة الشرك","Shirk Gate"),
                TXT("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾","⚠️ Unforgivable"),
                "🔴")
    
    # البوابة 2: الماعون (انهيار الرحمة)
    if B_compassion <= 0:
        return (-1, TXT("بوابة الماعون","Al-Ma'un Gate"),
                TXT("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ...﴾","⚠️ Collapse"),
                "🔴")
    
    # البوابة 3: الإخلاص (عبادة باطلة)
    if W_raw > 0 and B_disavowal <= 0:
        return (0, TXT("بوابة الإخلاص","Sincerity Gate"),
                TXT("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي...﴾","⚠️ Void"),
                "🟡")
    
    # البوابة 4: الوعد (ثبات)
    if W_raw > 0 and B_raw > 0:
        return (1, TXT("بوابة الوعد","Promise Gate"),
                TXT("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾","🟢 Stability"),
                "🟢")
    
    # لا ينطبق أي شرط → المرور للمعادلة العامة
    return None, None, None, None


# =============================================
# 2. حساب S (المعادلة العامة الأساسية)
# =============================================
def calculate_S(W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal):
    """
    حساب الثبات S والتمكين E والفجوة، مع المرور أولاً على المحكمة العليا.
    """
    # المرور على البوابات
    S_gate, gate_name, gate_msg, gate_color = supreme_court(
        W_raw, B_raw, W_pure, B_compassion, B_disavowal
    )
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0
    
    # المعادلة العامة
    W = (W_raw + 1) / 2  # تطبيع من [-1,1] إلى [0,1]
    B = (B_raw + 1) / 2
    E = E_raw  # E يأتي من [0,1] مباشرة في الواجهة
    
    # معاملات التعزيز من الحروف
    W_boost = 1 + (LETTERS_DB['أ'] + LETTERS_DB['ر'] + LETTERS_DB['س'] + LETTERS_DB['ط']) / 1000
    B_boost = 1 + (LETTERS_DB['ل'] + LETTERS_DB['ح'] + LETTERS_DB['ط']) / 1000
    
    S_raw = (W * W_boost) * (B * B_boost) * (1 + LETTERS_DB['م'] / 1000)
    
    # فجوة الاستدراج
    istidraj_gap = max(0, E - S_raw)
    
    return min(1.0, S_raw), E, TXT("المعادلة العامة","General"), "", "⚪", istidraj_gap


# =============================================
# 3. حساب S (المعادلة الموسعة - للنمذجة المتقدمة)
# =============================================
def calc_S_final(W, B, E, source_constants, dual_constants, manifestation_vars,
                 connection_vars, creation_positive, creation_negative, operators):
    """
    المعادلة الموسعة لنظرية الميزان - تأخذ بالاعتبار جميع فئات الحروف.
    """
    S = W * B
    
    # ثوابت المصدر (ك، ن)
    source_factor = (source_constants.get('ك', 20) * 20 + source_constants.get('ن', 50) * 50) / 2
    S *= (0.5 + 0.5 * source_factor / 100)
    
    # الثوابت المزدوجة (ق، ص)
    dual_factor = (dual_constants.get('ق', 100) * 100 + dual_constants.get('ص', 90) * 90) / 2
    S *= (0.6 + 0.4 * dual_factor / 100)
    
    # حروف التجلي
    if manifestation_vars:
        manifestation_boost = sum(manifestation_vars.values()) / len(manifestation_vars)
        S *= (0.5 + 0.5 * manifestation_boost)
    
    # حروف الوصل
    if connection_vars:
        connection_balance = sum(connection_vars.values()) / len(connection_vars)
        S *= (0.8 + 0.4 * connection_balance)
    
    # الأسباب الإيجابية
    if creation_positive:
        pos_boost = sum(creation_positive.values()) / len(creation_positive)
        S *= (1 + 0.2 * pos_boost)
    
    # الأسباب السلبية
    if creation_negative:
        neg_effect = sum(creation_negative.values()) / len(creation_negative)
        S *= (1 - 0.3 * neg_effect)
    
    # المشغلات
    op_factor = operators.get('ف', 0.5) * operators.get('و', 0.5) * operators.get('ت', 0.5)
    S *= (0.8 + 0.4 * op_factor)
    
    # تأثير الاستدراج
    if E > S:
        S -= operators.get('غ', 0.2) * (E - S) * 0.3
    
    return np.clip(S, 0.001, 1.0)


# =============================================
# 4. المحاكاة الزمنية
# =============================================
def simulate_future(S, E, W_raw, B_raw, years=50):
    """
    محاكاة تطور S و E عبر الزمن.
    """
    Sh, Eh = [S], [E]
    
    for _ in range(years):
        nE = Eh[-1] + 0.02 * (Sh[-1] - Eh[-1])
        nB = B_raw
        
        # تأثير فجوة الاستدراج على البراءة
        if nE > Sh[-1] + 0.2:
            nB -= 0.03
        elif nE < Sh[-1]:
            nB += 0.01
        
        # إعادة حساب S
        W_norm = (W_raw + 1) / 2
        B_norm = (nB + 1) / 2
        nS = W_norm * B_norm * (1 + sum(LETTERS_DB.values()) / 1000)
        
        Sh.append(nS)
        Eh.append(nE)
    
    return Sh, Eh


# =============================================
# 5. حساب البوصلة من الإجابات
# =============================================
def compute_compass(answers_dict, compass_data):
    """
    حساب W_raw, B_raw, S_score من إجابات المستخدم.
    """
    w_raw, b_raw = 0.0, 0.0
    total_weight = sum(q['value'] for q in compass_data)
    
    for q in compass_data:
        key = f"q_{q['id']}"
        ans_idx = answers_dict.get(key, 0)
        if ans_idx < len(q['answers']):
            delta_w, delta_b = q['answers'][ans_idx][1], q['answers'][ans_idx][2]
            weight = q['value'] / 100.0
            w_raw += delta_w * weight
            b_raw += delta_b * weight
    
    w_raw = max(-1.0, min(1.0, w_raw))
    b_raw = max(-1.0, min(1.0, b_raw))
    S_score = ((w_raw + 1) / 2) * ((b_raw + 1) / 2)
    
    return w_raw, b_raw, S_score


# =============================================
# 6. حساب الانحناء (κ)
# =============================================
def curvature(W_list, B_list):
    """
    حساب انحناء المسار في فضاء (W, B).
    κ = |W'B'' - B'W''| / (W'² + B'²)^(3/2)
    """
    if len(W_list) < 3:
        return 0.0
    
    W = np.array(W_list)
    B = np.array(B_list)
    
    dW = np.gradient(W)
    dB = np.gradient(B)
    ddW = np.gradient(dW)
    ddB = np.gradient(dB)
    
    num = abs(dW[-1] * ddB[-1] - dB[-1] * ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    
    return num / denom


# =============================================
# 7. لون النجمة في المشهد الكوني (الألوان المعدلة)
# =============================================
def star_color(w, b):
    """
    تحديد لون النجمة بناءً على موقعها في فضاء (W, B).
    
    الألوان الجديدة:
    - المؤمن (w ≥ 0.5 و b ≥ 0.5): ذهبي (#FFD700)
    - الكافر (w < 0.5 و b ≥ 0.5): أحمر (#FF5252)
    - المنافق (w < 0.5 و b < 0.5): وردي (#FFB6C1)
    - المشرك (w ≥ 0.5 و b < 0.5): برتقالي (#FFA500)
    """
    if w >= 0.5 and b >= 0.5:
        return '#FFD700'      # مؤمن (ذهبي)
    elif w < 0.5 and b >= 0.5:
        return '#FF5252'      # كافر (أحمر)
    elif w < 0.5 and b < 0.5:
        return '#FFB6C1'      # منافق (وردي)
    else:  # w >= 0.5 and b < 0.5
        return '#FFA500'      # مشرك (برتقالي)
