import numpy as np

def run_standard_simulation(W0, B0, E0, years=200, lag=20):
    W = np.zeros(years); B = np.zeros(years); S = np.zeros(years); E = np.zeros(years)
    W[0], B[0], E[0] = W0, B0, E0; S[0] = W0 * B0
    for t in range(1, years):
        H = 10 / (S[t-1] + 0.1)
        dW = (0.08 * H) - (0.03 * E[t-1]) - (0.04 * (1 - B[t-1]))
        W[t] = max(0.0, min(1.0, W[t-1] + dW))
        dB = (-0.02 * E[t-1]) + (0.01 * (1 - B[t-1]) * W[t-1] * (1 - W[t-1]))
        B[t] = max(0.0, min(1.0, B[t-1] + dB))
        S[t] = W[t] * B[t]
        past_idx = t - lag
        S_past = S[past_idx] if past_idx >= 0 else S[t]
        dE = 0.05 * (S_past - E[t-1])
        E[t] = max(0.0, min(1.0, E[t-1] + dE))
    return W, B, S, E

# =============================================
# الاختبارات
# =============================================
print("="*50)
print("بدء اختبارات الوحدة...")
print("="*50)

# اختبار 1: الحالة المثالية (W=0.9, B=0.9)
W, B, S, E = run_standard_simulation(0.9, 0.9, 0.1)
assert len(W) == 200, "خطأ: عدد السنوات غير صحيح"
assert 0 <= np.mean(S) <= 1, "خطأ: S خارج المدى [0, 1]"
assert 0 <= np.mean(E) <= 1, "خطأ: E خارج المدى [0, 1]"
print("✅ اختبار 1 (الحالة المثالية): ناجح")

# اختبار 2: الحالة الصفرية (W=0.0, B=0.0)
W, B, S, E = run_standard_simulation(0.0, 0.0, 0.0)
assert np.mean(S) < 0.1, "خطأ: S يجب أن يكون قريبًا من الصفر"
print("✅ اختبار 2 (الحالة الصفرية): ناجح")

# اختبار 3: الاستدراج (W=0.3, B=0.3, E=0.9)
W, B, S, E = run_standard_simulation(0.3, 0.3, 0.9)
max_S = np.argmax(S)
max_E = np.argmax(E)
assert max_S < max_E, "خطأ: لم يتم رصد الاستدراج"
print(f"✅ اختبار 3 (الاستدراج): ناجح – فجوة الاستدراج = {max_E - max_S} سنة")

# اختبار 4: الحالة المتطرفة (W=1.0, B=1.0)
W, B, S, E = run_standard_simulation(1.0, 1.0, 1.0)
assert all(0 <= val <= 1 for val in W), "خطأ: W خارج المدى"
assert all(0 <= val <= 1 for val in B), "خطأ: B خارج المدى"
print("✅ اختبار 4 (الحالة المتطرفة): ناجح")

print("="*50)
print("🎉 جميع اختبارات الوحدة ناجحة!")
print("="*50)
