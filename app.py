import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import random
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════
st.set_page_config(page_title="هندسة الصراط", page_icon="📐", layout="wide")

if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

# ═══════════════════════════════════
# تنسيق
# ═══════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Cairo:wght@400;700;900&display=swap');
    .stApp { background: radial-gradient(ellipse at 50% 50%, #0a0a1a 0%, #020108 100%); }
    h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #FFD700; }
    .golden-title { font-size: 3em; font-weight: 900; text-align: center; 
                    background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 40%, #B8860B 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
    .stButton > button { background: none; border: 2px solid #FFD700; color: #FFD700; border-radius: 50px;
                        padding: 15px 30px; font-size: 1.1em; font-weight: bold; transition: all 0.5s; }
    .stButton > button:hover { background: #FFD700; color: #000; box-shadow: 0 0 30px gold; }
    .arabic { font-family: 'Cairo', sans-serif; direction: rtl; }
    .metric-box { background: rgba(10,10,46,0.8); border-radius: 15px; padding: 15px; border: 1px solid #FFD700; text-align: center; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════
# دوال
# ═══════════════════════════════════
def get_curvature(W, B):
    if len(W) < 3: return 0.0
    dW = np.gradient(list(W)); dB = np.gradient(list(B))
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return num / denom

def classify(W, B):
    if W >= 0.5 and B >= 0.5: return ("مؤمن", '#FFD700')
    elif W < 0.5 and B >= 0.5: return ("كافر", '#FF5252')
    elif W < 0.5 and B < 0.5: return ("منافق", '#FFB6C1')
    else: return ("مشرك", '#FFA500')

# ═══════════════════════════════════
# العنوان
# ═══════════════════════════════════
st.markdown('<h1 class="golden-title">📐 هندسة الصراط</h1>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:#AAA;font-size:1.1em;margin-top:-20px;'>κ(t) = |W'B'' - B'W''| / (W'² + B'²)^{3/2}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:#888;font-size:0.9em;'>κ = 0 → الصراط المستقيم | κ > 0 → انحراف | التوبة → قوة تصحيحية</p>", unsafe_allow_html=True)
st.divider()

# ═══════════════════════════════════
# تهيئة الجلسة
# ═══════════════════════════════════
if 'path_W' not in st.session_state:
    st.session_state.path_W = [0.5]
    st.session_state.path_B = [0.5]
    st.session_state.kappa_vals = [0.0]
    st.session_state.score = 0
    st.session_state.steps = 0
    st.session_state.best_score = 0

# ═══════════════════════════════════
# ١. رحلة المسار
# ═══════════════════════════════════
st.subheader("🧭 رحلة المسار")
st.markdown("**أزرار التحكم:** 'خطوة' تحركك نحو الهدف، 'معصية' تنحرف بك، 'توبة' تعيدك للاستقامة.")

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("▶️ خطوة", use_container_width=True):
        Wc, Bc = st.session_state.path_W[-1], st.session_state.path_B[-1]
        nW = Wc + (1.0 - Wc)*0.15 + random.uniform(-0.03, 0.03)
        nB = Bc + (1.0 - Bc)*0.15 + random.uniform(-0.03, 0.03)
        nW = np.clip(nW, 0.01, 1.0); nB = np.clip(nB, 0.01, 1.0)
        st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
        k = get_curvature(st.session_state.path_W, st.session_state.path_B)
        st.session_state.kappa_vals.append(k)
        st.session_state.steps += 1
        st.session_state.score += int((nW + nB) * 10)
        st.rerun()

with c2:
    sin_strength = st.slider("⚡ شدة المعصية", 0.01, 0.2, 0.05, 0.01, key="sin_str")
with c3:
    if st.button("⚠️ معصية", use_container_width=True):
        Wc, Bc = st.session_state.path_W[-1], st.session_state.path_B[-1]
        nW = Wc - sin_strength*(Wc - 0.1) + random.uniform(-0.05, 0.05)
        nB = Bc - sin_strength*(Bc - 0.1) + random.uniform(-0.05, 0.05)
        nW = np.clip(nW, 0.01, 1.0); nB = np.clip(nB, 0.01, 1.0)
        st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
        k = get_curvature(st.session_state.path_W, st.session_state.path_B)
        st.session_state.kappa_vals.append(k)
        st.session_state.steps += 1
        st.session_state.score -= 5
        st.rerun()

with c4:
    if st.button("🕌 توبة", use_container_width=True, type="primary"):
        Wc, Bc = st.session_state.path_W[-1], st.session_state.path_B[-1]
        nW = Wc + (1.0 - Wc)*0.8; nB = Bc + (1.0 - Bc)*0.8
        nW = np.clip(nW, 0.01, 1.0); nB = np.clip(nB, 0.01, 1.0)
        st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
        st.session_state.kappa_vals.append(0.0)
        st.session_state.score += 20
        st.rerun()

if st.button("🔄 إعادة الرحلة", use_container_width=True):
    if st.session_state.score > st.session_state.best_score:
        st.session_state.best_score = st.session_state.score
    st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
    st.session_state.kappa_vals = [0.0]; st.session_state.score = 0; st.session_state.steps = 0
    st.rerun()

# رسم المسار
fig1, axes1 = plt.subplots(1, 2, figsize=(14, 6), facecolor='#030310')
ax1 = axes1[0]; ax1.set_facecolor('#0a0a1a'); ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
ax1.set_xlabel("B (البراءة)", color='white'); ax1.set_ylabel("W (الولاء)", color='white')
ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=2.5, alpha=0.7, label=T("الصراط (إبراهيم)", "Straight Path"))
ax1.scatter([1], [1], s=120, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, label=T("الكمال", "Perfection"))
pW = st.session_state.path_W; pB = st.session_state.path_B
if len(pW) > 1:
    for i in range(1, len(pW)):
        kv = st.session_state.kappa_vals[i] if i < len(st.session_state.kappa_vals) else 0
        cl = '#00FFFF' if kv < 0.05 else '#FF4444'
        ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2 if kv < 0.05 else 3)
    ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label=T("البداية", "Start"))
    ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label=T("الآن", "Now"))
ax1.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')

ax2 = axes1[1]; ax2.set_facecolor('#0a0a1a')
ax2.plot(st.session_state.kappa_vals, color='#FFD700', lw=2, marker='o', markersize=3)
ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label=T("حد الخطر", "Danger"))
ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label=T("الصراط", "Straight"))
ax2.set_title(T("منحنى الانحناء", "Curvature Curve"), color='white', fontsize=12)
ax2.legend(facecolor='#0a0a1a', edgecolor='white', labelcolor='white', fontsize=8)
ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
ax2.set_ylim(-0.01, max(0.2, max(st.session_state.kappa_vals)*1.2 if st.session_state.kappa_vals else 0.1))
plt.tight_layout(); st.pyplot(fig1)

# مؤشرات
mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
    st.markdown(f"<div class='metric-box'><p style='color:#AAA;'>W</p><p style='color:#FFD700;font-size:1.5em;'>{pW[-1]:.3f}</p></div>", unsafe_allow_html=True)
with mc2:
    st.markdown(f"<div class='metric-box'><p style='color:#AAA;'>B</p><p style='color:#FFD700;font-size:1.5em;'>{pB[-1]:.3f}</p></div>", unsafe_allow_html=True)
with mc3:
    k_val = st.session_state.kappa_vals[-1]
    st.markdown(f"<div class='metric-box'><p style='color:#AAA;'>κ</p><p style='color:{'#00FFFF' if k_val<0.05 else '#FF4444'};font-size:1.5em;'>{k_val:.4f}</p></div>", unsafe_allow_html=True)
with mc4:
    st.markdown(f"<div class='metric-box'><p style='color:#AAA;'>النتيجة</p><p style='color:#FFD700;font-size:1.5em;'>{st.session_state.score}</p><p style='color:#888;'>الأفضل: {st.session_state.best_score}</p></div>", unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════
# ٢. بوصلة القيم
# ═══════════════════════════════════
st.subheader("🧭 بوصلة القيم")
st.markdown("حرك نقطتك لتكتشف في أي ربع تقع.")

cA, cB = st.columns(2)
with cA:
    myW = st.slider("W (الولاء)", 0.0, 1.0, 0.5, 0.01, key="compassW")
with cB:
    myB = st.slider("B (البراءة)", 0.0, 1.0, 0.5, 0.01, key="compassB")

name, color = classify(myW, myB)
S_val = myW * myB
st.markdown(f"<div style='text-align:center;padding:15px;border:2px solid {color};border-radius:15px;margin:10px 0;'><h2 style='color:{color};'>{name}</h2><p style='color:#CCC;'>S = W × B = {S_val:.3f}</p></div>", unsafe_allow_html=True)

fig2, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0a1a')
ax.set_facecolor('#0a0a1a'); ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.15))
ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF5252', alpha=0.15))
ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.15))
ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA500', alpha=0.15))
ax.text(0.5, 0.5, "مؤمن", ha='center', color='white', alpha=0.6)
ax.text(-0.5, 0.5, "كافر", ha='center', color='white', alpha=0.6)
ax.text(-0.5, -0.5, "منافق", ha='center', color='white', alpha=0.6)
ax.text(0.5, -0.5, "مشرك", ha='center', color='white', alpha=0.6)
ax.scatter(myB*2-1, myW*2-1, s=200, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
ax.set_xlabel("B", color='white'); ax.set_ylabel("W", color='white'); ax.tick_params(colors='white')
st.pyplot(fig2)

st.divider()

# ═══════════════════════════════════
# ٣. تحدي الصراط
# ═══════════════════════════════════
st.subheader("🎯 تحدي الصراط")
st.markdown(f"الهدف: الوصول إلى (1,1) بأقل عدد من الخطوات. **أفضل نتيجة: {st.session_state.best_score}**")

colT1, colT2 = st.columns(2)
with colT1:
    st.metric("الموقع الحالي", f"({pW[-1]:.2f}, {pB[-1]:.2f})")
with colT2:
    dist = np.sqrt((1-pW[-1])**2 + (1-pB[-1])**2)
    st.metric("المسافة إلى الكمال", f"{dist:.3f}")

st.progress(1 - dist/1.5)

st.divider()
st.markdown(f"<p style='text-align:center;color:#555;'>⚖️ S = W × B | ق = الحق = الميزان | علي عادل العاطفي | ٢٠٢٦</p>", unsafe_allow_html=True)
