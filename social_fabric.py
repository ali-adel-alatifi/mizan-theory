# mizan/social_fabric.py
"""
محاكي المجتمع كخلية حية
النسيج الاجتماعي: تفاعل الأفراد بناءً على W و B
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
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
    /* نصوص المخططات */
    .matplotlib-text {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_social_fabric():
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
    st.header(TXT("🧬 محاكي المجتمع كخلية حية", "🧬 Social Fabric Simulator"))
    st.caption(TXT(
        "هذا المشهد يحاكي المجتمع كنسيج حي. كل نقطة تمثل فرداً. الألوان تعكس درجة توازنه (S = W × B). "
        "الأفراد المتوازنون يتجاذبون ويشكلون نسيجاً متماسكاً. غير المتوازنين يتباعدون أو يتنافرون.",
        "This scene simulates society as a living fabric. Each dot represents an individual. Colors reflect stability (S = W × B). "
        "Balanced individuals attract each other and form a cohesive fabric. Unbalanced ones drift apart or repel."
    ))

    # إعدادات المحاكاة
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        n_individuals = st.slider(TXT("عدد الأفراد", "Number of Individuals"), 20, 100, 50, 5, key="fab_n")
    with col_set2:
        avg_W = st.slider(TXT("متوسط W (الولاء)", "Average W (Loyalty)"), 0.0, 1.0, 0.5, 0.05, key="fab_W")
    with col_set3:
        avg_B = st.slider(TXT("متوسط B (البراءة)", "Average B (Disavowal)"), 0.0, 1.0, 0.5, 0.05, key="fab_B")

    # زر توليد مجتمع جديد
    if "fab_individuals" not in st.session_state:
        st.session_state.fab_individuals = None

    if st.button(TXT("🔄 توليد مجتمع جديد", "🔄 Generate New Society"), use_container_width=True):
        st.session_state.fab_individuals = None
        st.rerun()

    # تهيئة المجتمع
    if st.session_state.fab_individuals is None:
        np.random.seed(random.randint(0, 9999))
        n = n_individuals
        Ws = np.random.normal(avg_W, 0.15, n).clip(0, 1)
        Bs = np.random.normal(avg_B, 0.15, n).clip(0, 1)
        xs = np.random.uniform(0, 10, n)
        ys = np.random.uniform(0, 10, n)
        st.session_state.fab_individuals = {
            "W": Ws, "B": Bs, "x": xs, "y": ys, "iterations": 0
        }

    # تحديث المواقع (تفاعل الأفراد)
    data = st.session_state.fab_individuals
    Ws = data["W"]
    Bs = data["B"]
    xs = data["x"].copy()
    ys = data["y"].copy()
    n = len(Ws)
    Ss = Ws * Bs

    for i in range(n):
        fx, fy = 0.0, 0.0
        for j in range(n):
            if i == j:
                continue
            dx = xs[j] - xs[i]
            dy = ys[j] - ys[i]
            dist = max(np.sqrt(dx**2 + dy**2), 0.1)
            S_diff = 1 - abs(Ss[i] - Ss[j])
            # الأفراد المتشابهون يتجاذبون
            if S_diff > 0.5:
                force = S_diff * 0.02
                fx += dx / dist * force
                fy += dy / dist * force
            # الأفراد المختلفون يتنافرون
            else:
                force = (1 - S_diff) * 0.01
                fx -= dx / dist * force
                fy -= dy / dist * force
        xs[i] = np.clip(xs[i] + fx, 0, 10)
        ys[i] = np.clip(ys[i] + fy, 0, 10)

    data["x"] = xs
    data["y"] = ys
    data["iterations"] += 1
    st.session_state.fab_individuals = data

    # رسم المجتمع
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title(TXT("النسيج الاجتماعي – المجتمع كخلية حية", "Social Fabric – Society as a Living Cell"),
                 color='white', fontsize=13)

    # تحديد الألوان حسب S (مع التصنيف الجديد)
    colors = []
    for i in range(n):
        w = Ws[i]
        b = Bs[i]
        if w >= 0.5 and b >= 0.5:
            colors.append('#FFD700')      # مؤمن (ذهبي)
        elif w < 0.5 and b >= 0.5:
            colors.append('#FF5252')      # كافر (أحمر)
        elif w < 0.5 and b < 0.5:
            colors.append('#FFB6C1')      # منافق (وردي)
        else:  # w >= 0.5 and b < 0.5
            colors.append('#FFA500')      # مشرك (برتقالي)

    # رسم الأفراد
    ax.scatter(xs, ys, s=80, c=colors, alpha=0.8, edgecolors='white', linewidths=0.5, zorder=5)

    # رسم روابط بين الأفراد المتشابهين
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt((xs[j] - xs[i])**2 + (ys[j] - ys[i])**2)
            S_diff = 1 - abs(Ss[i] - Ss[j])
            if S_diff > 0.7 and dist < 3:
                ax.plot([xs[i], xs[j]], [ys[i], ys[j]],
                        color='#FFD700', alpha=S_diff * 0.3, lw=0.5, zorder=1)

    st.pyplot(fig)

    # إحصائيات المجتمع
    st.markdown("---")
    st.subheader(TXT("📊 إحصائيات المجتمع", "📊 Community Statistics"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(TXT("متوسط W", "Avg W"), f"{np.mean(Ws):.2f}")
    c2.metric(TXT("متوسط B", "Avg B"), f"{np.mean(Bs):.2f}")
    c3.metric(TXT("متوسط S", "Avg S"), f"{np.mean(Ss):.2f}")
    c4.metric(TXT("عدد المتوازنين (S>0.7)", "Balanced (S>0.7)"), f"{np.sum(Ss > 0.7)}")

    # تفسير النتائج
    st.markdown("---")
    st.subheader(TXT("💡 تفسير المشهد", "💡 Scene Interpretation"))
    st.markdown(TXT(
        """
        - **النقاط الذهبية (S > 0.7):** أفراد متوازنون، يحبون في الله ويبغضون في الله. هم نواة المجتمع المتماسك.
        - **النقاط البرتقالية (S > 0.4):** أفراد في بداية الطريق، لديهم ولاء لكن براءتهم ضعيفة، أو العكس.
        - **النقاط الحمراء والرمادية (S < 0.4):** أفراد يعانون من خلل في المعادلة. إما منغمسون في الباطل، أو متطرفون بلا ولاء.
        - **الروابط الذهبية:** تمثل أواصر الأخوة الإيمانية التي تنشأ بين المتقين. كلما زاد عدد المتوازنين، زادت الروابط.
        
        **الدرس:** المجتمع المتماسك لا يُبنى بالشعارات، بل بتوازن الولاء والبراءة في قلوب أفراده. S = W × B.
        """,
        """
        - **Golden dots (S > 0.7):** Balanced individuals, loving and hating for Allah's sake. They are the nucleus of a cohesive society.
        - **Orange dots (S > 0.4):** Individuals at the start of the path, having loyalty but weak disavowal, or vice versa.
        - **Red and gray dots (S < 0.4):** Individuals suffering from an imbalance in the equation. Either immersed in falsehood or extremists without loyalty.
        - **Golden links:** Represent the bonds of faith-brotherhood arising between the righteous. The more balanced individuals, the more links.
        
        **The lesson:** A cohesive society is not built by slogans, but by balancing loyalty and disavowal in the hearts of its members. S = W × B.
        """
    ))

    # زر إعادة الضبط
    if st.button(TXT("🔄 إعادة ضبط المحاكاة", "🔄 Reset Simulation"), use_container_width=True):
        st.session_state.fab_individuals = None
        st.rerun()
