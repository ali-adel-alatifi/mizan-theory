# mizan/ahlulbayt.py
"""
مدرسة آل البيت - الثبات في الفتنة
النماذج العليا: الإمام علي، الحسن، الحسين رضي الله عنهم
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from config import TXT

# =============================================
# 1. قاعدة بيانات آل البيت
# =============================================
AHLULBAYT_DATA = [
    {
        "name": TXT("الإمام علي بن أبي طالب", "Imam Ali ibn Abi Talib"),
        "title": TXT("كرّم الله وجهه", "May Allah honor his face"),
        "emoji": "🦁",
        "color": "#FFD700",
        "quote": TXT(
            "«وَاللَّهِ لَوْ أُعْطِيتُ الْأَقَالِيمَ السَّبْعَةَ بِمَا تَحْتَ أَفْلَاكِهَا، عَلَى أَنْ أَعْصِيَ اللَّهَ فِي نَمْلَةٍ أَسْلُبُهَا جُلْبَ شَعِيرَةٍ، مَا فَعَلْتُهُ»",
            "«By Allah, if I were given the seven regions with all that is under their orbits, to disobey Allah by snatching a grain of barley from an ant, I would not do it.»"
        ),
        "W": 0.98, "B": 0.98, "S": 0.96,
        "lessons": TXT(
            "**الولاء الخالص:** لم يسجد لصنم قط (W=1). **البراءة العملية:** وقف في وجه الفتن والانحرافات بكل حزم (B=1). "
            "**الثبات:** ظل ثابتاً على الحق في السلم والحرب، في العسر واليسر.",
            "**Pure Loyalty:** Never prostrated to an idol (W=1). **Practical Disavowal:** Stood firm against strife and deviation (B=1). "
            "**Stability:** Remained steadfast in peace and war."
        ),
        "test": {
            "question": TXT("بماذا لقب الإمام علي؟", "What was Imam Ali's title?"),
            "options": [TXT("أسد الله", "Lion of Allah"), TXT("سيف الله", "Sword of Allah"), TXT("أبو تراب", "Abu Turab"), TXT("كل ما سبق", "All of the above")],
            "answer": 3
        }
    },
    {
        "name": TXT("الإمام الحسن بن علي", "Imam Hassan ibn Ali"),
        "title": TXT("رضي الله عنه", "May Allah be pleased with him"),
        "emoji": "🕊️",
        "color": "#00FF88",
        "quote": TXT(
            "«إِنِّي أَرَى اجْتِمَاعَ الْأُمَّةِ أَحَبَّ إِلَيَّ مِنْ طَلَبِ الْمُلْكِ»",
            "«I see the unity of the Ummah as more beloved to me than seeking kingship.»"
        ),
        "W": 0.95, "B": 0.85, "S": 0.81,
        "lessons": TXT(
            "**الولاء العالي:** حفيد رسول الله، نشأ في بيت النبوة (W عالٍ). **البراءة الحكيمة:** تنازل عن الخلافة حقناً لدماء المسلمين (براءة من الفتنة والفرقة). "
            "**الثبات:** ثبت على مبدأه في الحفاظ على وحدة الأمة.",
            "**High Loyalty:** Grandson of the Prophet, raised in the prophetic house. **Wise Disavowal:** Gave up the caliphate to spare Muslim blood (disavowal of discord). "
            "**Stability:** Remained steadfast in preserving the Ummah's unity."
        ),
        "test": {
            "question": TXT("ما أعظم ما فعله الحسن لوحدة الأمة؟", "What great act did Hassan do for unity?"),
            "options": [TXT("فتح مكة", "Conquered Mecca"), TXT("تنازل عن الخلافة", "Gave up the caliphate"), TXT("بنى مسجداً", "Built a mosque"), TXT("كتب مصحفاً", "Wrote a Mushaf")],
            "answer": 1
        }
    },
    {
        "name": TXT("الإمام الحسين بن علي", "Imam Hussein ibn Ali"),
        "title": TXT("رضي الله عنه", "May Allah be pleased with him"),
        "emoji": "⚔️",
        "color": "#FF4444",
        "quote": TXT(
            "«إِنِّي لَمْ أَخْرُجْ أَشِرًا وَلَا بَطِرًا وَلَا مُفْسِدًا وَلَا ظَالِمًا، إِنَّمَا خَرَجْتُ لِطَلَبِ الْإِصْلَاحِ فِي أُمَّةِ جَدِّي»",
            "«I did not come out as an insolent, nor an arrogant, nor a corrupter, nor an oppressor. I only came out seeking reform in the Ummah of my grandfather.»"
        ),
        "W": 1.0, "B": 1.0, "S": 1.0,
        "lessons": TXT(
            "**الولاء المطلق:** بذل نفسه وروحه وأهله في سبيل الله (W=1). **البراءة القصوى:** واجه الطاغوت بكل وضوح حتى الشهادة (B=1). "
            "**الثبات الأبدي:** أصبحت واقعة كربلاء رمزاً خالداً للثبات على الحق في وجه الظلم.",
            "**Absolute Loyalty:** Gave himself, his soul, and his family for Allah (W=1). **Ultimate Disavowal:** Confronted tyranny until martyrdom (B=1). "
            "**Eternal Stability:** Karbala became an eternal symbol of steadfastness."
        ),
        "test": {
            "question": TXT("ما هدف خروج الحسين كما قال؟", "What was Hussein's goal in his own words?"),
            "options": [TXT("طلب الملك", "Seeking kingship"), TXT("الإصلاح في أمة جده", "Reform in his grandfather's Ummah"), TXT("جمع المال", "Gathering wealth"), TXT("الانتقام", "Revenge")],
            "answer": 1
        }
    },
]

# =============================================
# 2. واجهة مدرسة آل البيت
# =============================================
def render_ahlulbayt():
    """عرض مدرسة آل البيت."""
    st.header(TXT("🏴 مدرسة آل البيت – الثبات في الفتنة", "🏴 School of Ahlul Bayt – Stability in Strife"))
    st.markdown(TXT(
        "### ﴿إِنَّمَا يُرِيدُ اللَّهُ لِيُذْهِبَ عَنكُمُ الرِّجْسَ أَهْلَ الْبَيْتِ وَيُطَهِّرَكُمْ تَطْهِيرًا﴾",
        "### Allah only intends to keep away impurity from you, O People of the Household."
    ))
    st.caption(TXT(
        "هؤلاء هم الذين جسّدوا معادلة الثبات (S = W x B) في أقسى الفتن وأصعب الامتحانات. انظر كيف توزعوا على فضاء القيم.",
        "These are those who embodied the stability equation in the harshest trials."
    ))

    # عرض النماذج الثلاثة
    cols = st.columns(3)

    for i, person in enumerate(AHLULBAYT_DATA):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:20px;background:rgba(20,30,60,0.8);border-radius:15px;border:2px solid {person['color']};margin:5px;">
                <p style="font-size:3em;margin:0;">{person['emoji']}</p>
                <h3 style="color:{person['color']};margin:5px 0;">{person['name']}</h3>
                <p style="color:#CCC;font-size:0.8em;">{person['title']}</p>
                <hr style="border-color:rgba(255,215,0,0.3);">
                <p style="color:#FFD700;">W={person['W']:.2f} | B={person['B']:.2f} | S={person['S']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

    # عرض مفصل لكل منهم
    st.markdown("---")
    selected_person = st.selectbox(
        TXT("اختر نموذجاً للتفصيل:", "Choose a model for details:"),
        [p["name"] for p in AHLULBAYT_DATA]
    )

    person = next(p for p in AHLULBAYT_DATA if p["name"] == selected_person)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"## {person['emoji']} {person['name']}")
        st.markdown(f"*{person['quote']}*")
        st.markdown(person["lessons"])

    with col2:
        # مخطط دائري لمؤشراته
        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        labels = ['W (الولاء)', 'B (البراءة)', 'S (الثبات)']
        values = [person['W'], person['B'], person['S']]
        colors = ['#FFD700', '#FF5252', '#00FF88']
        ax.bar(labels, values, color=colors, edgecolor='white', linewidth=2)
        ax.set_ylim(0, 1.1)
        ax.set_title(TXT("مؤشرات الثبات", "Stability Indicators"), color='white', fontsize=12)
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, axis='y')
        st.pyplot(fig)

    # اختبار سريع
    st.markdown("---")
    st.subheader(TXT("📝 اختبر فهمك", "📝 Test Your Understanding"))
    test = person["test"]
    ans = st.radio(test["question"], test["options"], key=f"test_{person['name']}")
    if st.button(TXT("تحقق", "Check"), key=f"btn_test_{person['name']}"):
        if test["options"].index(ans) == test["answer"]:
            st.success(TXT("✅ أحسنت! لقد فهمت الدرس.", "✅ Well done! You understood the lesson."))
        else:
            st.error(TXT("❌ حاول مرة أخرى.", "❌ Try again."))

    # خلاصة
    st.markdown("---")
    st.subheader(TXT("💡 الخلاصة", "💡 Summary"))
    st.markdown(TXT(
        "الولاء الخالص (W) والبراءة الصادقة (B) يولّدان ثباتاً لا يزعزعه شيء. "
        "الإمام علي جسّد الحكمة والعدل، والحسن جسّد الإيثار والوحدة، والحسين جسّد التضحية في سبيل الإصلاح. "
        "كلهم ثبتوا على الصراط المستقيم في أقسى الظروف. وهم الأسوة الحسنة بعد النبي صلى الله عليه وسلم.",
        "Pure loyalty (W) and sincere disavowal (B) generate unshakeable stability. "
        "Imam Ali embodied wisdom and justice, Hassan embodied sacrifice and unity, Hussein embodied sacrifice for reform. "
        "All remained steadfast on the straight path in the harshest conditions."
    ))
