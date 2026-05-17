# mizan/logic.py
"""
وحدة المنطق الرياضي والمحاكاة
تحتوي: المحكمة العليا، حساب S، المحاكاة الزمنية، حساب البوصلة، الانحناء
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
# 2. حساب S (المعادلة العامة)
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
# 3. المحاكاة الزمنية
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
# 4. حساب البوصلة من الإجابات
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
# 5. حساب الانحناء (κ)
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
# 6. لون النجمة في المشهد الكوني
# =============================================
def star_color(w, b):
    """
    تحديد لون النجمة بناءً على موقعها في فضاء (W, B).
    """
    if w >= 0.55 and b >= 0.55:
        return '#FFD700'      # مؤمن (ذهبي)
    elif w >= 0.55 and b < 0.45:
        return '#E0E0E0'      # ضال (أبيض)
    elif w < 0.45 and b >= 0.55:
        return '#FF5252'      # مغضوب عليه (أحمر)
    elif w < 0.45 and b < 0.45:
        return '#FFB6C1'      # منافق (وردي)
    return '#888888'          # منطقة انتقالية (رمادي)
