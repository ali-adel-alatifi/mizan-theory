import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =============================================
# الإعدادات
# =============================================
st.set_page_config(page_title="⚖️ الدين القيم – المنارة العالمية", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang
TXT = lambda ar, en: ar if LANG == "ar" else en

# =============================================
# الثوابت الوجودية – المعجم الهندسي
# =============================================
LETTERS_DB = {
    'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60,
    'ح': 8, 'ط': 9, 'ق': 100, 'ك': 20, 'ص': 90,
    'ع': 70, 'ي': 10, 'هـ': 5, 'ن': 50, 'ف': 80,
    'و': 6, 'ب': 2
}

# =============================================
# البوصلة – 19 سؤالاً مع القيم الحرفية
# =============================================
COMPASS_DATA = [
    {"id": 1, "topic_ar": "القوانين الوضعية وتحكيم الشريعة", "topic_en": "Man-Made Laws vs. Sharia", "letter": "ق", "value": 100,
     "answers": [("تحكيم شرع الله هو الصحيح، وأبذل كل ما أستطيع لتطبيقه", 2), ("أتمنى تطبيق الشريعة، لكني لا أعمل لأجلها", 1), ("أرى أن بعض أحكام الشريعة صالحة وبعضها غير صالح", -1), ("الشريعة الإسلامية لم تعد تصلح لهذا العصر", -2)]},
    {"id": 2, "topic_ar": "الولاء للعرق والحزب والطائفة", "topic_en": "Loyalty to Race, Party, and Sect", "letter": "أ", "value": 1,
     "answers": [("ولائي لله ورسوله والمؤمنين فوق كل رابطة، وأتبرأ من العصبيات الجاهلية", 2), ("أحاول أن أوازن بين ولائي للإسلام وانتمائي العرقي أو الحزبي", 1), ("ولائي لديني ضعيف، وأميل للفخر بعرقي أو حزبي أكثر", -1), ("لا أرى مشكلة في تقديم العرق أو الحزب على الدين، فهذا واقع العصر", -2)]},
    {"id": 3, "topic_ar": "الاستهزاء بالمقدسات وحرية التعبير", "topic_en": "Mockery of Sanctities & Free Speech", "letter": "هـ", "value": 5,
     "answers": [("أبغض في الله المستهزئين، وأدين فعلهم بكل وضوح", 2), ("أستنكر الاستهزاء في قلبي، لكني لا أعلن موقفي جهارًا", 1), ("أرى أنها 'حرية رأي' ولا داعي للغضب", -1), ("أضحك معهم أحيانًا، ولا أرى في ذلك ضررًا كبيرًا", -2)]},
    {"id": 4, "topic_ar": "الربا والنظام المالي العالمي", "topic_en": "Usury and the Global Financial System", "letter": "ص", "value": 90,
     "answers": [("أتجنب الربا بكل صوره وأبحث عن البدائل الإسلامية ولو خسرت ربحًا", 2), ("أكره الربا، لكني مضطر للتعامل به أحيانًا بحكم الواقع", 1), ("أتعامل بالربا كالجميع، ولا أرى مشكلة حقيقية في ذلك", -1), ("الربا ضرورة اقتصادية، وتحريمه كان لزمن غير زمننا", -2)]},
    {"id": 5, "topic_ar": "العلمانية وفصل الدين عن الدولة", "topic_en": "Secularism: Separating Religion from State", "letter": "ك", "value": 20,
     "answers": [("أرفض العلمانية، وأؤمن أن الإسلام دين ودولة وشريعة تحكم كل الحياة", 2), ("أرى أن العلمانية قد تكون حلاً مؤقتًا لحين استعداد المجتمع", 1), ("لا أمانع فصل الدين عن السياسة، فالدين علاقة شخصية بالله", -1), ("العلمانية هي الطريق الصحيح للتقدم، والدين يجب أن يبقى في المسجد فقط", -2)]},
    {"id": 6, "topic_ar": "إقامة الحدود الشرعية", "topic_en": "Establishing Sharia Penalties", "letter": "ح", "value": 8,
     "answers": [("الحدود الشرعية رحمة وعدل، وأؤمن بضرورة إقامتها لحماية المجتمع", 2), ("الحدود حق، لكن الظروف الحالية لا تسمح بتطبيقها", 1), ("أشعر بالحرج من بعض الحدود، وأراها قاسية", -1), ("الحدود الشرعية همجية ولا تصلح للعصر الحديث", -2)]},
    {"id": 7, "topic_ar": "الإلحاد وإنكار الخالق", "topic_en": "Atheism: Denying the Creator", "letter": "ن", "value": 50,
     "answers": [("أؤمن بالله يقينًا لا يتزعزع، وأرى في العلم دليلاً على وجوده", 2), ("أؤمن بالله، لكني لا أملك حججًا للرد على شبهات الملحدين", 1), ("تساورني أحيانًا شكوك، لكني أعود للإيمان", -1), ("أعتقد أن الإلحاد طرح فكري يحترم، والدين مجرد أساطير", -2)]},
    {"id": 8, "topic_ar": "الجهاد ونصرة المستضعفين", "topic_en": "Jihad and Supporting the Oppressed", "letter": "ر", "value": 200,
     "answers": [("الجهاد ذروة سنام الإسلام، وأتمنى أن أكون في صفوف المجاهدين لنصرة المستضعفين", 2), ("الجهاد حق، وأدعمه بقلبي ومالي إن استطعت، لكني لا أقاتل الآن", 1), ("أخشى من الجهاد، وأرى أنه يجلب المشاكل للمسلمين", -1), ("الجهاد أصبح إرهابًا، ولا مكان له في هذا العصر", -2)]},
    {"id": 9, "topic_ar": "حقوق المرأة بين الإسلام والتغريب", "topic_en": "Women's Rights: Islam vs. Westernization", "letter": "هـ", "value": 5,
     "answers": [("أؤمن أن الإسلام كرم المرأة ورفع شأنها، وأن أحكامه هي عين العدل", 2), ("أؤمن بالإسلام، لكني أرى ضرورة 'تحديث' بعض الأحكام لتواكب العصر", 1), ("أشعر بالحرج من بعض أحكام الإسلام الخاصة بالمرأة", -1), ("أعتقد أن الإسلام ظلم المرأة، وأن تحريرها يكون بالعلمانية", -2)]},
    {"id": 10, "topic_ar": "العولمة والذوبان الحضاري", "topic_en": "Globalization and Cultural Dissolution", "letter": "م", "value": 40,
     "answers": [("أتمسك بهويتي الإسلامية، وأتبرأ من تقليد الكفار في ثقافتهم وأزيائهم", 2), ("أحاول أن أوازن بين هويتي الإسلامية ومتطلبات العصر", 1), ("أقلد الغرب في كثير من ثقافته، ولا أرى بأسًا في ذلك", -1), ("الثقافة الغربية هي ثقافة التقدم، ويجب أن نندمج فيها كليًا", -2)]},
    {"id": 11, "topic_ar": "الديمقراطية والتشريع", "topic_en": "Democracy and Legislation", "letter": "ل", "value": 30,
     "answers": [("أرفض جعل الشعب مشرعًا، فالتشريع لله وحده، والشورى لا تعني الالتفاف على الشرع، بل هي طاعة لله في تطبيق ما شرع", 2), ("أرى أن الديمقراطية وسيلة يمكن استخدامها لتحقيق بعض المصالح", 1), ("أفضّل النظام الديمقراطي على الأنظمة الاستبدادية", -1), ("الديمقراطية هي أفضل نظام حكم، والشريعة لا تصلح للتطبيق السياسي", -2)]},
    {"id": 12, "topic_ar": "التعددية الدينية", "topic_en": "Religious Pluralism", "letter": "ي", "value": 10,
     "answers": [("الإسلام هو الدين الوحيد المقبول عند الله، ومن لم يؤمن به فهو خاسر في الآخرة", 2), ("الإسلام هو الحق، لكني لا أحكم على أصحاب الديانات الأخرى", 1), ("أرى أن كل الأديان فيها جزء من الحق", -1), ("كل الأديان سواء، ولا يحق لأحد أن يدعي امتلاك الحقيقة المطلقة", -2)]},
    {"id": 13, "topic_ar": "الحب في الله والبغض في الله", "topic_en": "Love for Allah and Hatred for Allah", "letter": "ق", "value": 100,
     "answers": [("أحب في الله أولياءه وأبغض في الله أعداءه، وهذا أوثق عرى إيماني، ولا أجعل مصلحتي الشخصية فوق هذا", 2), ("أحاول، لكن علاقاتي تغلب عليها المصالح والمنافع أحيانًا", 1), ("أتعامل مع الجميع بالمثل، لا حب ولا بغض في الله، فالمصلحة هي الأساس", -1), ("علاقاتي كلها تقوم على مصلحتي الشخصية، ولا دخل للدين فيها", -2)]},
    {"id": 14, "topic_ar": "التحلي بالأخلاق الحميدة", "topic_en": "Embodying Noble Character", "letter": "ط", "value": 9,
     "answers": [("الصدق والأمانة والوفاء دين، وألتزم بها ولو خسرت دنيويًا", 2), ("أحاول الالتزام بها، لكني قد أضطر للكذب أحيانًا", 1), ("أرى أن المبالغة في الصدق سذاجة، والواقع يفرض بعض 'المرونة'", -1), ("الكذب والغش أدوات ضرورية للنجاح في هذا العصر", -2)]},
    {"id": 15, "topic_ar": "الغيرة على المحارم والأمر بالمعروف", "topic_en": "Protective Jealousy & Enjoining Good", "letter": "ب", "value": 2,
     "answers": [("آمر بالمعروف وأنهى عن المنكر بكل استطاعتي، فهذا واجبي", 2), ("أنكر بقلبي، وأحيانًا بلساني إذا لم أخف ضررًا كبيرًا", 1), ("أسكت عن المنكر حفاظًا على علاقاتي ومصالحي", -1), ("لا داعي للأمر والنهي، فكل إنسان حر في تصرفاته", -2)]},
    {"id": 16, "topic_ar": "الوطنية والقومية", "topic_en": "Patriotism and Nationalism", "letter": "ف", "value": 80,
     "answers": [("ولائي للإسلام فوق كل وطن وقومية، وأتبرأ من كل دعوة جاهلية تفرق المسلمين", 2), ("أحب وطني، لكني أقدّم الإسلام عليه", 1), ("أشعر أن انتمائي لوطني أهم من انتمائي للإسلام", -1), ("لا أرى مشكلة في القومية، فالإسلام لا يتعارض مع حب الوطن", -2)]},
    {"id": 17, "topic_ar": "الصلاة في زمن الانشغال", "topic_en": "Prayer in an Age of Busyness", "letter": "ن", "value": 50,
     "answers": [("الصلاة راحتي وقرة عيني، ولا أتركها مهما كنت مشغولاً", 2), ("أصلي لكني أؤخرها أو أستعجل فيها أحيانًا", 1), ("أصلي أحيانًا وأتركها أحيانًا، حسب الظروف", -1), ("لا أجد وقتًا للصلاة، وأراها غير عملية في هذا العصر", -2)]},
    {"id": 18, "topic_ar": "الصوم في زمن الشهوات", "topic_en": "Fasting in an Age of Desires", "letter": "ط", "value": 9,
     "answers": [("أصوم الفرض والنفل، وأراه دورة تدريبية على تقوى الله", 2), ("أصوم الفرض فقط، ولا أستطيع صيام النفل", 1), ("أصوم رمضان كعادة اجتماعية، ولا أشعر بروحانيته", -1), ("لا أصوم، وأرى أن العصر لا يتناسب مع فكرة الصيام", -2)]},
    {"id": 19, "topic_ar": "الزكاة والصدقة في زمن الأنانية", "topic_en": "Zakat and Charity in an Age of Selfishness", "letter": "ط", "value": 9,
     "answers": [("أؤدي الزكاة طيبة بها نفسي، وأعترف أن المال مال الله، وفيها طهارة لنفسي وعونًا لإخوتي", 2), ("أؤدي الزكاة فقط، وأحيانًا أتصدق", 1), ("أخرج الزكاة بخلاً، وأشعر أنها 'ضريبة'", -1), ("لا أزكي، فالمال مالي ولا دخل لأحد فيه", -2)]},
]

# =============================================
# المحرك الوجودي
# =============================================
def calculate_compass(answers_dict):
    """حساب W و B من إجابات البوصلة باستخدام القيم الحرفية"""
    w_weighted_sum = 0.0
    b_weighted_sum = 0.0
    total_weight = sum(q['value'] for q in COMPASS_DATA)

    for q in COMPASS_DATA:
        key = f"q_{q['id']}"
        score = answers_dict.get(key, 0)
        weight = q['value']
        # الطاقة الإيجابية تذهب للولاء، والسالبة تذهب للبراءة
        if score > 0:
            w_weighted_sum += score * weight
            b_weighted_sum += score * weight * 0.7  # البراءة تتأثر أيضاً
        else:
            b_weighted_sum += score * weight
            w_weighted_sum += score * weight * 0.3  # الولاء يتأثر سلباً

    max_possible = 2 * total_weight
    W_raw = max(-1.0, min(1.0, w_weighted_sum / max_possible))
    B_raw = max(-1.0, min(1.0, b_weighted_sum / max_possible))

    W_norm = (W_raw + 1) / 2
    B_norm = (B_raw + 1) / 2
    S_score = W_norm * B_norm

    return W_raw, B_raw, S_score

print("✅ المرحلة الأولى مكتملة: الأساسيات، الثوابت، البوصلة، المحرك الوجودي")

# =============================================
# المرحلة الثانية: الواجهة، التبويبات، النتائج
# =============================================

# الشريط الجانبي
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:8px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <p style='font-size:2em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:0;'>{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h2>
        <p style='color:#e0e0e0;font-size:10px;margin:2px 0;'>{TXT('المنارة العالمية', 'The Global Beacon')}</p>
        <p style='color:#FFD700;font-size:14px;margin:2px 0;font-weight:bold;'>S = W × B</p>
        <p style='font-size:2em;margin:0;'>⚖️</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(TXT("🇬🇧 English", "🇸🇦 العربية"), use_container_width=True):
        st.session_state.lang = "en" if LANG == "ar" else "ar"
        st.rerun()

# العنوان الرئيسي
st.markdown(f"""
<div style="text-align:center;padding:25px 0 15px 0;">
    <p style="font-size:2.8em;margin:0;">⚖️</p>
    <h1 style="color:#FFD700;font-size:2.8em;margin:5px 0;font-weight:900;letter-spacing:3px;">{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h1>
    <h2 style="color:#FFD700;font-size:1.3em;margin-top:0;font-weight:400;">{TXT('المنارة العالمية – بوصلة التائهين وحبل نجاة الغارقين', 'The Global Beacon – Compass for the Lost, Lifeline for the Drowning')}</h2>
    <p style="font-size:2.2em;color:#FFD700;margin:15px 0;font-weight:bold;">S = W × B</p>
    <p style="color:#CCC;font-size:1.1em;line-height:2;">﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انفِصَامَ لَهَا﴾</p>
    <p style="font-size:2.8em;margin:0;">⚖️</p>
</div>
""", unsafe_allow_html=True)

# التبويبات
tab1, tab2, tab3, tab4 = st.tabs([
    TXT("🧭 بوصلة الإسلام الحنيف", "🧭 Al-Islam Al-Hanif Compass"),
    TXT("📐 هندسة الصراط", "📐 Path Geometry"),
    TXT("📖 المعجم الهندسي", "📖 Geometric Lexicon"),
    TXT("📜 رسالة الترحيب", "📜 Welcome Message")
])

# =============================================
# تبويب 1: بوصلة الإسلام الحنيف
# =============================================
with tab1:
    st.subheader(TXT("🧭 بوصلة الإسلام الحنيف", "🧭 Al-Islam Al-Hanif Compass"))
    st.markdown(TXT(
        "19 سؤالاً، كل سؤال يستحضر مفهوماً معاصراً مغلوطاً ويطرح موقفاً يلامس واقع الأمة. أجب بصدق لتعرف موقعك الحقيقي. المعادلة: S = W × B.",
        "19 questions, each recalling a distorted modern concept and posing a stance that touches the Ummah's reality. Answer honestly to discover your true position. Equation: S = W × B."
    ))

    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    # عرض الأسئلة
    for q in COMPASS_DATA:
        topic = q['topic_ar'] if LANG == "ar" else q['topic_en']
        with st.expander(f"**{q['id']}. {topic}**  [{q['letter']}={q['value']}]"):
            text = q.get('text_ar', q.get('text', '')) if LANG == "ar" else q.get('text_en', q.get('text', ''))
            if not text:
                # استخدام النص الافتراضي من الإجابات
                text = q['answers'][0][0] if q['answers'] else ""
            st.markdown(f"*{text}*")
            key = f"q_{q['id']}"
            # الحصول على نصوص الإجابات
            ans_texts = [a[0] for a in q['answers']]
            ans = st.radio(
                TXT("اختر موقعك:", "Choose your position:"),
                ans_texts,
                key=key, index=None
            )
            if ans is not None:
                for a_text, a_val in q['answers']:
                    if ans == a_text:
                        st.session_state.compass_answers[key] = a_val
                        break

    # الحساب والعرض
    if len(st.session_state.compass_answers) == 19:
        W_raw, B_raw, S_score = calculate_compass(st.session_state.compass_answers)

        # تحديد الربع
        if W_raw > 0 and B_raw > 0:
            q_name, q_color = TXT("مؤمن حنيف (متوازن)", "Hanif Believer (Balanced)"), '#FFD700'
        elif W_raw > 0 and B_raw <= 0:
            q_name, q_color = TXT("مؤمن مستضعف (يحتاج للمناعة)", "Weak Believer"), '#FF5252'
        elif W_raw <= 0 and B_raw <= 0:
            q_name, q_color = TXT("غافل أو منافق", "Heedless or Hypocrite"), '#FFB6C1'
        else:
            q_name, q_color = TXT("متطرف (براءة بلا ولاء)", "Extremist"), '#FFA500'

        st.divider()
        st.subheader("📊 نتيجة البوصلة")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("W (الولاء)", f"{W_raw:+.2f}")
        c2.metric("B (البراءة)", f"{B_raw:+.2f}")
        c3.metric("S (الثبات)", f"{S_score:.2f}")
        c4.metric(TXT("موقعك", "Position"), q_name)
        st.markdown(f"<h2 style='color:{q_color};text-align:center;'>{q_name}</h2>", unsafe_allow_html=True)

        # خريطة رباعية
        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.set_xlabel("B", color='white'); ax.set_ylabel("W", color='white')
        ax.fill_between([0, 1.2], 0, 1.2, color='#FFD700', alpha=0.3, label=TXT('حنيف', 'Hanif'))
        ax.fill_between([-1.2, 0], 0, 1.2, color='#FF5252', alpha=0.2, label=TXT('ضعيف', 'Weak'))
        ax.fill_between([-1.2, 0], -1.2, 0, color='#FFB6C1', alpha=0.2, label=TXT('غافل', 'Heedless'))
        ax.fill_between([0, 1.2], -1.2, 0, color='#FFA500', alpha=0.2, label=TXT('متطرف', 'Extremist'))
        ax.scatter(B_raw, W_raw, s=200, c='cyan', edgecolors='white', linewidth=2, zorder=10)
        ax.scatter(1, 1, s=80, c='#FFD700', marker='*', zorder=10)
        ax.text(1, 1.1, TXT('إبراهيم', 'Abraham'), color='#FFD700', fontsize=7, ha='center')
        ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=6, loc='lower left')
        ax.tick_params(colors='white')
        st.pyplot(fig)

        # تحليل
        if q_name == TXT("مؤمن حنيف (متوازن)", "Hanif Believer (Balanced)"):
            st.success(TXT("أنت في حالة توازن ديناميكي. استمر في الاستجابة المثلى للقانون الإلهي.", "You are in dynamic balance. Continue."))
        elif q_name == TXT("مؤمن مستضعف (يحتاج للمناعة)", "Weak Believer"):
            st.warning(TXT("لديك إيمان لكن براءتك ضعيفة. قوِّ مناعتك وتعلم أن تقول 'لا' في وجه الباطل.", "You have faith but weak immunity. Strengthen it."))
        elif q_name == TXT("غافل أو منافق", "Heedless or Hypocrite"):
            st.error(TXT("خطر! لا ولاء قوي ولا براءة. عد إلى الله وجدد إيمانك.", "Danger! Return to Allah and renew your faith."))
        else:
            st.warning(TXT("لديك حماس ومناعة لكنك تفتقر لأساس الإيمان. ازرع حب الله في قلبك.", "You have zeal but lack the foundation of faith."))

        if st.button(TXT("🔄 إعادة البوصلة", "🔄 Retake Compass"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

# =============================================
# تبويب 2: هندسة الصراط
# =============================================
with tab2:
    st.subheader(TXT("هندسة الصراط – انحناء المسار", "Path Geometry – Curvature"))
    st.markdown(TXT(
        "الصراط المستقيم هو المسار الذي انحناؤه صفر (κ=0). أي انحراف عن هذا المسار هو معصية أو فتنة. الهدف هو الوصول إلى مقام إبراهيم (1,1).",
        "The straight path has zero curvature (κ=0). Any deviation is sin or trial. The goal is Abraham's Station (1,1)."
    ))

    if 'path_W' not in st.session_state:
        st.session_state.path_W = [0.5]  # قيمة افتراضية
    if 'path_B' not in st.session_state:
        st.session_state.path_B = [0.5]

    # زر لتسجيل الحالة الحالية
    col_path_btn, _ = st.columns([1, 3])
    with col_path_btn:
        if st.button(TXT("➕ سجل حالتك", "➕ Record State"), use_container_width=True):
            # استخدام آخر نتيجة للبوصلة إذا كانت متاحة
            if len(st.session_state.compass_answers) == 19:
                W_raw, B_raw, _ = calculate_compass(st.session_state.compass_answers)
            else:
                W_raw, B_raw = 0.0, 0.0
            st.session_state.path_W.append(W_raw)
            st.session_state.path_B.append(B_raw)
            st.rerun()

    pW = st.session_state.path_W
    pB = st.session_state.path_B

    if len(pW) > 1:
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.plot([pB[0], 1], [pW[0], 1], '--', color='#FFD700', lw=1.5, alpha=0.6, label=TXT('الصراط المستقيم (κ=0)', 'Straight Path'))
        ax.plot(pB, pW, 'o-', color='#0FF', lw=2, markersize=4, label=TXT('مسارك', 'Your Path'))
        ax.scatter(pB[-1], pW[-1], s=100, c='cyan', edgecolors='white', linewidth=2, zorder=10)
        ax.scatter(1, 1, s=100, c='#FFD700', marker='*', zorder=10, label=TXT('مقام إبراهيم', 'Abraham'))
        ax.set_xlabel("B", color='white'); ax.set_ylabel("W", color='white')
        ax.legend(facecolor='#0a0a2e', edgecolor='white', labelcolor='white', fontsize=7)
        ax.tick_params(colors='white')
        st.pyplot(fig)

        try:
            dW = np.gradient(pW); dB = np.gradient(pB)
            ddW = np.gradient(dW); ddB = np.gradient(dB)
            num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
            denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
            kappa = num / denom
            st.metric(TXT("انحناء المسار (κ)", "Curvature"), f"{kappa:.4f}")
            if kappa < 0.03:
                st.success(TXT("✅ على الصراط المستقيم", "✅ On straight path"))
            elif kappa < 0.1:
                st.warning(TXT("⚠️ انحراف طفيف", "⚠️ Slight deviation"))
            else:
                st.error(TXT("🚨 انحراف خطير", "🚨 Dangerous deviation"))
        except:
            st.info(TXT("تحتاج إلى 3 نقاط لحساب الانحناء", "Need 3 points to calculate curvature"))
    else:
        st.info(TXT("سجل حالتك لتتبع مسارك نحو مقام إبراهيم. يمكنك استخدام نتيجة البوصلة كأول نقطة.", "Record your state to track your path."))

# =============================================
# تبويب 3: المعجم الهندسي
# =============================================
with tab3:
    st.subheader(TXT("📖 المعجم الهندسي – الحروف وقيمها", "📖 Geometric Lexicon"))
    st.markdown(TXT(
        "هذا المعجم يربط كل حرف بقيمته العددية (حساب الجمل) ودوره الوجودي في معادلة الميزان.",
        "This lexicon links each letter to its numerical value and existential role in the Mizan equation."
    ))

    letters_data = {
        TXT('الفئة الأولى: الذات الإلهية (المصدر)', 'Cat 1: Divine Essence'): {'ك': 20, 'ن': 50},
        TXT('الفئة الثانية: الازدواج', 'Cat 2: Duality'): {'ق': 100, 'ص': 90},
        TXT('الفئة الثالثة: التجلي الإلهي', 'Cat 3: Manifestation'): {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        TXT('الفئة الرابعة: الاشتراك (الجسور)', 'Cat 4: Bridges'): {'ع': 70, 'ي': 10, 'هـ': 5},
        TXT('الفئة الخامسة: المشغلات', 'Cat 5: Operators'): {'ف': 80, 'و': 6, 'ب': 2},
        TXT('الفئة السادسة: أعمال الخلق', 'Cat 6: Actions'): {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
    }
    for cat, lets in letters_data.items():
        st.markdown(f"**{cat}**")
        st.dataframe(pd.DataFrame(list(lets.items()), columns=[TXT('الحرف', 'Letter'), TXT('القيمة', 'Value')]), hide_index=True)

# =============================================
# تبويب 4: رسالة الترحيب
# =============================================
with tab4:
    st.subheader(TXT("📜 رسالة الترحيب", "📜 Welcome Message"))
    st.markdown(f"""
    <div style="text-align:center;color:#CCC;line-height:2.2;font-size:1.1em;">
    > "{TXT('هل يوجد قانون واحد يحكم الذرة والحضارة؟', 'Is there a single law?')}"<br>
    > {TXT('نعم. إنه', 'Yes. It is')} <b style="color:#FFD700;">S = W × B</b>.
    <br><br>
    <b style="color:#FFD700;">﴿أَفَغَيْرَ دِينِ اللَّهِ يَبْغُونَ...﴾</b>
    <br><br>
    {TXT('هذه المنصة هي منارة للعالمين، وبوصلة للتائهين، وحبل نجاة للغارقين، ومشفى لكل ضر، ومحكمة عادلة لا تستأنف.', 
    'This platform is a beacon for the world, a compass for the lost, and a just court.')}
    <br><br>
    > "{TXT('أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.', 'O humanity, you are not in chaos.')}"
    </div>
    """, unsafe_allow_html=True)

# =============================================
# التذييل
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:20px;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="font-size:2em;margin:0;">⚖️</p>
    <p style="color:#FFD700;font-size:1.5em;font-weight:bold;">{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</p>
    <p style="color:#FFD700;font-size:1.2em;">S = W × B</p>
    <p>{TXT('المنارة العالمية – بوصلة التائهين وحبل نجاة الغارقين', 'The Global Beacon – Compass for the Lost, Lifeline for the Drowning')}</p>
    <p>﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
    <p>{TXT('علي عادل العاطفي', 'Ali Adel Alatifi')} | 2026</p>
    <p style="font-size:0.8em;margin-top:10px;">MIT License | {TXT('المنصة الذهبية v5.0', 'Golden Platform v5.0')}</p>
    <p style="font-size:2em;margin:0;">⚖️</p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الثانية مكتملة: الواجهة، التبويبات، النتائج، المعجم، التذييل")
print("✅✅✅ تم بناء منصة الدين القيم – المنارة العالمية بنجاح!")
