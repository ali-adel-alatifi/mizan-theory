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
    if not W_pure:
        return (0, TXT("بوابة الشرك","Shirk Gate"),
                TXT("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾","⚠️ Unforgivable"), "🔴")
    if B_compassion <= 0:
        return (-1, TXT("بوابة الماعون","Al-Ma'un Gate"),
                TXT("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ...﴾","⚠️ Collapse"), "🔴")
    if W_raw > 0 and B_disavowal <= 0:
        return (0, TXT("بوابة الإخلاص","Sincerity Gate"),
                TXT("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي...﴾","⚠️ Void"), "🟡")
    if W_raw > 0 and B_raw > 0:
        return (1, TXT("بوابة الوعد","Promise Gate"),
                TXT("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾","🟢 Stability"), "🟢")
    return None, None, None, None

# =============================================
# 2. حساب S (المعادلة العامة الأساسية)
# =============================================
def calculate_S(W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal):
    S_gate, gate_name, gate_msg, gate_color = supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal)
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0
    W = (W_raw + 1) / 2
    B = (B_raw + 1) / 2
    E = E_raw
    W_boost = 1 + (LETTERS_DB['أ'] + LETTERS_DB['ر'] + LETTERS_DB['س'] + LETTERS_DB['ط']) / 1000
    B_boost = 1 + (LETTERS_DB['ل'] + LETTERS_DB['ح'] + LETTERS_DB['ط']) / 1000
    S_raw = (W * W_boost) * (B * B_boost) * (1 + LETTERS_DB['م'] / 1000)
    istidraj_gap = max(0, E - S_raw)
    return min(1.0, S_raw), E, TXT("المعادلة العامة","General"), "", "⚪", istidraj_gap

# =============================================
# 3. حساب S (المعادلة الموسعة)
# =============================================
def calc_S_final(W, B, E, source_constants, dual_constants, manifestation_vars,
                 connection_vars, creation_positive, creation_negative, operators):
    S = W * B
    source_factor = (source_constants.get('ك', 20) * 20 + source_constants.get('ن', 50) * 50) / 2
    S *= (0.5 + 0.5 * source_factor / 100)
    dual_factor = (dual_constants.get('ق', 100) * 100 + dual_constants.get('ص', 90) * 90) / 2
    S *= (0.6 + 0.4 * dual_factor / 100)
    if manifestation_vars:
        manifestation_boost = sum(manifestation_vars.values()) / len(manifestation_vars)
        S *= (0.5 + 0.5 * manifestation_boost)
    if connection_vars:
        connection_balance = sum(connection_vars.values()) / len(connection_vars)
        S *= (0.8 + 0.4 * connection_balance)
    if creation_positive:
        pos_boost = sum(creation_positive.values()) / len(creation_positive)
        S *= (1 + 0.2 * pos_boost)
    if creation_negative:
        neg_effect = sum(creation_negative.values()) / len(creation_negative)
        S *= (1 - 0.3 * neg_effect)
    op_factor = operators.get('ف', 0.5) * operators.get('و', 0.5)
    S *= (0.8 + 0.4 * op_factor)
    if E > S:
        S -= operators.get('غ', 0.2) * (E - S) * 0.3
    return np.clip(S, 0.001, 1.0)

# =============================================
# 4. المحاكاة الزمنية
# =============================================
def simulate_future(S, E, W_raw, B_raw, years=50):
    Sh, Eh = [S], [E]
    for _ in range(years):
        nE = Eh[-1] + 0.02 * (Sh[-1] - Eh[-1])
        nB = B_raw
        if nE > Sh[-1] + 0.2:
            nB -= 0.03
        elif nE < Sh[-1]:
            nB += 0.01
        W_norm = (W_raw + 1) / 2
        B_norm = (nB + 1) / 2
        nS = W_norm * B_norm * (1 + sum(LETTERS_DB.values()) / 1000)
        Sh.append(nS)
        Eh.append(nE)
    return Sh, Eh

# =============================================
# 5. حساب البوصلة من الإجابات
# =============================================
def compute_comp
