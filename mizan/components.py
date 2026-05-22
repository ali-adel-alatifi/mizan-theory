# mizan/components.py
"""
وحدة مكونات الواجهة
تحتوي: دوال عرض جميع التبويبات (١٥ تبويباً)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random, time
from matplotlib.patches import Circle, Rectangle

from config import (TXT, LETTERS_DB, INDICATORS_META, N_IND, COMPASS_DATA,
                    HISTORICAL_DATA, get_indicator_label)
from logic import (calculate_S, simulate_future, compute_compass, curvature, star_color)
from utils import (ai_analyze_compass, ai_fill_sliders, plot_quadrant_map, get_spiritual_nudge,
                   export_session_data, import_session_data)

# استيراد الملفات المنفصلة
from observatory import render_observatory
from healer import render_healer
from network import render_network
from academy import render_academy
from ahlulbayt import render_ahlulbayt
from appendices import render_appendices
from lexicon import render_lexicon
from the_one_law import render_the_one_law
from spiritual_energy import render_spiritual_energy
from prayer_cycle import render_prayer_cycle
from social_fabric import render_social_fabric


# =============================================
# رسالة الترحيب ودليل المستخدم
# =============================================
def render_welcome():
    with st.expander(TXT("📜 رسالة ترحيب", "📜 Welcome Message"), expanded=True):
        st.markdown(f"""
        <div class="message-box">
        <h2 style="text-align:center;color:#FFD700;">⚖️ {TXT('مختبر الميزان', 'The Mizan Lab')}</h2>
        <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;">
        "{TXT('وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ * أَلَّا تَطْغَوْا فِي الْمِيزَانِ', 'And the heaven He raised and imposed the balance. That you not transgress within the balance.')}"
        </p>
        
        <p style="text-align:center;color:#FFD700;font-style:italic;font-size:1.1em;margin:10px 0;">
        ﴿وَمَا أُوتِيتُم مِّنَ الْعِلْمِ إِلَّا قَلِيلًا﴾ [الإسراء: ٨٥]
        </p>
        
        <p style="text-align:center;color:#FFD700;font-style:italic;font-size:1.1em;margin:10px 0;">
        ﴿وَفِي الْأَرْضِ آيَاتٌ لِّلْمُوقِنِينَ * وَفِي أَنفُسِكُمْ ۚ أَفَلَا تُبْصِرُونَ﴾ [الذاريات: ٢٠-٢١]
        </p>
        
        <p>{TXT(
        'أنت تقف الآن على عتبة مختبر فريد. ليس كمختبرات الكيمياء والفيزياء، بل مختبرٌ ينظر إلى الذرة والمجرة، وإلى القلب والضمير، عبر عدسةٍ واحدة. عدسةٌ تزعم أن للوجود قانوناً واحداً، يسري في نسيج الخلق كما يسري في نسيج الوحي. هذا القانون هو <b>"الميزان"</b>.',
        'You are standing at the threshold of a unique lab. Not one of chemistry or physics, but a lab that looks at the atom and the galaxy, at the heart and the conscience, through a single lens. A lens that claims existence has one law, flowing through the fabric of creation as it flows through the fabric of revelation. This law is <b>"Al-Mizan"</b>.'
        )}</p>
        <p>{TXT(
        'من الذرة التي تتآلف بقوة الجذب وتستقر بقوة التنافر، إلى الخلية التي تحمي ذاتها وتهاجم غريبها، إلى الكيمياء التي تتحد فيها الذرات وتحتاج إلى "طاقة تنشيط" لتكسر روابطها القديمة (توبتها!)، إلى المجتمعات التي تجمعها القيم وتحميها من الفساد... كل شيء يصرخ بقانونٍ واحد: <b>S = W × B</b>.',
        'From the atom that unites by attraction and stabilizes by repulsion, to the cell that protects itself and attacks intruders, to chemistry where atoms unite and need "activation energy" to break old bonds (its repentance!), to societies gathered by values and protected from corruption... everything screams one law: <b>S = W x B</b>.'
        )}</p>
        <p>{TXT(
        '<b>W (الولاء لله وأوليائه):</b> قوة الجذب نحو الحق. <b>B (البراءة من الطاغوت وأوليائه):</b> قوة التنافر عن الباطل. <b>S (الثبات الوجودي):</b> حاصل ضربهما. إنها معادلة ضرب لا جمع، لأن القلب لا يجتمع فيه ولاءان، ولأن الثبات لا يقوم إلا على ركنين. هذا هو "الدين القيم" الذي فطر الله الناس عليه، وهذا هو "الإسلام الحنيف" الذي هو الاستجابة الديناميكية لهذا القانون.',
        '<b>W (Loyalty to Allah & His allies):</b> The force of attraction to truth. <b>B (Disavowal of Taghut & its allies):</b> The force of repulsion from falsehood. <b>S (Existential Stability):</b> Their product. It is multiplication, not addition, because a heart cannot hold two loyalties, and stability only rests on two pillars. This is "Al-Deen Al-Qayyim" upon which Allah created people, and this is "Al-Islam Al-Hanif", the dynamic response to this law.'
        )}</p>
        <p>{TXT(
        'لم تكن هذه المعادلة مجرد نظرية بشرية. لقد جسّدها بشرٌ صدقوا ما عاهدوا الله عليه، رجالاً ونساءً، في كل الظروف والأحوال. <b>محمد</b> صلى الله عليه وعلى آله وسلم، خاتم النبيين وسيد المرسلين، الأسوة العظمى والقدوة المثلى، الذي قال: "أوثق عرى الإيمان: الحب في الله، والبغض في الله". ثم <b>إبراهيم</b> خليل الله، الذي أعلنها في وجه أبيه وقومه: "إنني براء مما تعبدون". و<b>موسى</b> كليم الله، الذي وقف في وجه الطاغوت السياسي. و<b>يوسف</b> الصديق، الذي اختار السجن على المعصية. و<b>أصحاب الكهف</b> الفتية، الذين اعتزلوا مجتمعهم الفاسد. و<b>علي والحسن والحسين</b>، الذين جسّدوا قمم الثبات في أقسى الفتن. و<b>أم موسى</b> التي ألقت بولدها في اليم ثقةً بوعد الله: "إنا رادوه إليك". و<b>آسيا امرأة فرعون</b> التي قالت تحت التعذيب: "رب ابن لي عندك بيتاً في الجنة"، متبرئةً من مُلك الطاغوت. هؤلاء ليسوا من عالم الملائكة. هم بشرٌ مثلنا، أكلوا الطعام ومشوا في الأسواق. ولكنهم عرفوا ما فضلهم الله به، وما أكرمهم به كبشر، فعملوا بهذا القانون، فارتقوا إلى أعلى عليين. وهذه المنصة تدعوك أن تسير على آثارهم.',
        'This equation was not merely a human theory. It was embodied by humans who were true to their covenant with Allah, men and women, in all circumstances. <b>Muhammad</b> ﷺ, the Seal of the Prophets and Master of the Messengers, the supreme example, who said: "The firmest handhold of faith is: love for the sake of Allah, and hatred for the sake of Allah." Then <b>Abraham</b>, the Friend of Allah, who declared to his father and people: "I am disassociated from what you worship". <b>Moses</b>, the one who spoke with Allah, who stood against the political tyrant. <b>Joseph</b>, the truthful, who chose prison over sin. <b>The People of the Cave</b>, the youths, who isolated themselves from their corrupt society. <b>Ali, Hassan, and Hussein</b>, who embodied the peaks of stability in the harshest trials. And <b>the mother of Moses</b>, who cast her child into the river, trusting Allah\'s promise: "We will return him to you". And <b>Asiya, the wife of Pharaoh</b>, who said under torture: "My Lord, build for me a house in Paradise", disavowing the tyrant\'s kingdom. These were not angels. They were humans like us, who ate food and walked in the markets. But they recognized what Allah had favored them with, and what He honored them with as humans, so they acted upon this law, and thereby ascended to the highest of heights. This platform invites you to walk in their footsteps.'
        )}</p>

        <p style="color:#FFD700;font-weight:bold;font-size:1.1em;text-align:center;margin:20px 0;">{TXT(
        'هذه المنصة ليست كتاباً فصلاً ولا تطبيقاً مكتملاً. إنها مختبر مفتوح، متواضع، يخطو خطواته الأولى على طريق طويل من التأمل والبحث. لقد جمعنا فيه ما وهبنا الله من فهم متواضع لسنة من سننه في خلقه، نرجو أن يكون باباً لقلبك لا سجناً لعقلك، ونافذةً على نور لا حاجزاً في وجه الظلمة. وإذا وجدت فيه خيراً، فاعلم أن الله هو الذي ألهم وأعان، وإذا وجدت فيه نقصاً، فاعلم أنه من صنع البشر، وأنه لا يضير الحق نقص في التعبير عنه.',
        'This platform is neither a definitive book nor a completed app. It is an open, humble lab, taking its first steps on a long path of reflection and inquiry. We have gathered in it what Allah has granted us of a humble understanding of one of His laws in creation, hoping it will be a door for your heart, not a cage for your mind, and a window to light, not a barrier against darkness. If you find good in it, know that Allah inspired and assisted; and if you find deficiency, know that it is from human craft, and the truth is not harmed by deficiency in its expression.'
        )}</p>

        <p style="text-align:center;color:#FFD700;font-size:1.2em;font-weight:bold;">S = W × B</p>
        <p style="text-align:center;font-style:italic;color:#AAA;font-size:1.1em;line-height:2.2;">{TXT(
        'هذا المختبر ليس بديلاً عن الوحي، بل هو شاهد من عالم الشهادة على صدق عالم الغيب. ﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ تَبَارَكَ اللَّهُ رَبُّ الْعَالَمِينَ﴾. إنه تحقيق لقوله تعالى: ﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ حَتَّىٰ يَتَبَيَّنَ لَهُمْ أَنَّهُ الْحَقُّ﴾. إنه محاولة متواضعة لنريك كيف يلتقي كتاب الله المسطور بكتابه المنظور، على ميزان واحد. فإن رأيت الحق فيه، فاحمد الله الذي هداك. وإن وجدت فيه نقصاً، فاعلم أنه من صنع البشر، ولا يضير الحق نقص في التعبير عنه.',
        'This lab is not a substitute for revelation, but a witness from the seen world to the truth of the unseen. ﴿Unquestionably, to Him belongs the creation and the command; blessed is Allah, Lord of the worlds.﴾ It is a fulfillment of His promise: ﴿We will show them Our signs in the horizons and within themselves until it becomes clear to them that it is the truth.﴾ It is a humble attempt to show you how Allah\'s written Book meets His observed Book, on a single balance. If you see truth in it, praise Allah who guided you. If you find deficiency, know that it is human craft, and the truth is not harmed by deficiency in its expression.'
        )}</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander(TXT("📖 دليل المستخدم", "📖 User Guide"), expanded=False):
        st.markdown(TXT("""
        ### 🎯 كيف تستخدم هذا المختبر؟

        **١. بوصلة الإسلام الحنيف:** أجب عن ١٩ سؤالاً لتعرف موقعك الدقيق.
        **٢. مختبر الأمة المتكاملة:** استخدم المنزلقات أو الذكاء الاصطناعي.
        **٣. المشهد الكوني الحي:** شاهد تفاعل النجوم مع قطبي الميزان.
        **٤. النسيج الاجتماعي:** شاهد كيف يترابط الأفراد المتوازنون وينفرط عقد غير المتوازنين.
        **٥. المرصد العالمي:** شاهد تطبيق المعادلة على دول العالم.
        **٦. هندسة الصراط:** تتبع مسارك نحو مقام إبراهيم.
        **٧. طبيب القلوب:** احصل على تشخيص وروشتة علاجية.
        **٨. شبكة الناجين:** تواصل مع المؤمنين الثابتين.
        **٩. جامعة الميزان:** تعلم النظرية عبر دورات تفاعلية.
        **١٠. مدرسة آل البيت:** نماذج الثبات في الفتنة.
        **١١. المعجم الهندسي:** تعرف على الحروف وقيمها وأسرارها.
        **١٢. القانون الواحد:** تجليات القانون من الذرة إلى المجرة.
        **١٣. دورة الصلاة:** الاستعانة بالصلاة في الدورة الإلهية.
        **١٤. الطاقة الروحية:** محاكاة قوانين الطاقة الروحية.
        **١٥. الدليل المرجعي:** مراجع متخصصة.

        **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
        """,
        """
        ### 🎯 How to Use This Lab

        **1. Compass:** Answer 19 questions.
        **2. Nation Lab:** Use sliders or AI.
        **3. Cosmic Scene:** Watch stars interact.
        **4. Social Fabric:** See how balanced individuals link up.
        **5. Observatory:** Apply the equation to world nations.
        **6. Path Geometry:** Track your path.
        **7. Healer:** Get diagnosis and prescription.
        **8. Network:** Connect with steadfast believers.
        **9. Academy:** Learn the theory via courses.
        **10. Ahlul Bayt:** Models of stability in strife.
        **11. Geometric Lexicon:** Explore letters, values, and secrets.
        **12. The One Law:** Manifestations from atom to galaxy.
        **13. Prayer Cycle:** Seeking help through prayer.
        **14. Spiritual Energy:** Simulate spiritual energy laws.
        **15. Reference Guide:** Specialized references.

        **Central Equation:** **S = W x B** (multiplication, not addition).
        """))
