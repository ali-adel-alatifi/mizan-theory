import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="مختبر الميزان – القانون الواحد", page_icon="⚖️", layout="wide")

if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri+Quran&display=swap');
.stApp { background: linear-gradient(180deg, #0a0f1e 0%, #0d1528 30%, #0f1a2e 100%); }
h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #FFD700; }
p, label, div { font-family: 'Cairo', sans-serif; color: #E0E0E0; }
.golden-title { font-size: 3.2em; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; }
.verse-text { text-align: center; color: #FFD700; font-size: 1.3em; margin: 15px 0; line-height: 2; }
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; width: 100%; transition: all 0.3s ease; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; box-shadow: 0 0 25px rgba(255,215,0,0.5); }
.stTabs [data-baseweb="tab-list"] { gap: 5px; background: rgba(13,21,40,0.8); border-radius: 15px; padding: 5px; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: bold; }
.message-box { background: rgba(20,30,60,0.7); border-radius: 15px; padding: 30px; margin: 20px 0; border: 1px solid rgba(255,215,0,0.3); line-height: 2.2; }
</style>
""", unsafe_allow_html=True)

def star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    return '#888888'

def classify(W, B):
    if W >= 0.5 and B >= 0.5: return (T("مؤمن","Believer"), '#FFD700')
    elif W < 0.5 and B >= 0.5: return (T("كافر","Disbeliever"), '#FF5252')
    elif W < 0.5 and B < 0.5: return (T("منافق","Hypocrite"), '#FFB6C1')
    return (T("مشرك","Polytheist"), '#FFA500')

def curvature(W, B):
    if len(W) < 3: return 0
    dW = np.gradient(list(W)); dB = np.gradient(list(B))
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return num / denom

# ═══════════════════════════════════════════════════════════════
# النظام النهائي – المنزلقات السبعة مع الحروف
# ═══════════════════════════════════════════════════════════════
ISLAMIC_SYSTEM_FINAL = {
    "faith": {
        "label": T("١. الإيمان", "1. Faith"),
        "desc": T("+ إيمان خالص بالله | − إيمان بغير الله", "+ Pure faith in Allah | − Faith in other than Allah"),
        "aya": "﴿آمَنَ الرَّسُولُ﴾",
        "effect_W": 0.30, "effect_B": 0.15,
        "letters": {"ar": "أ", "en": "A"},
    },
    "worship": {
        "label": T("٢. العبادات", "2. Worship"),
        "desc": T("+ إقامة العبادات | − تركها", "+ Performing worship | − Abandoning"),
        "aya": "﴿بُنِيَ الْإِسْلَامُ عَلَىٰ خَمْسٍ﴾",
        "effect_W": 0.20, "effect_B": 0.15,
        "letters": {"ar": "ط", "en": "T"},
    },
    "transactions": {
        "label": T("٣. المعاملات", "3. Transactions"),
        "desc": T("+ تحكيم شرع الله | − الحكم بغيره", "+ Sharia | − Other laws"),
        "aya": "﴿فَاحْكُم بَيْنَهُم بِمَا أَنزَلَ اللَّهُ﴾",
        "effect_W": 0.12, "effect_B": 0.18,
        "letters": {"ar": "س", "en": "S"},
    },
    "morals": {
        "label": T("٤. الأخلاق", "4. Morals"),
        "desc": T("+ موالاة المؤمنين | − موالاة الكفار", "+ Alliance | − Disavowal"),
        "aya": "﴿وَتَعَاوَنُوا عَلَى الْبِرِّ﴾",
        "effect_W": 0.15, "effect_B": 0.10,
        "letters": {"ar": "ي", "en": "Y"},
    },
    "enjoining": {
        "label": T("٥. الأمر والنهي", "5. Enjoining & Forbidding"),
        "desc": T("+ الدعوة للخير | − الأمر بالمنكر", "+ Calling to good | − Calling to evil"),
        "aya": "﴿وَلْتَكُن مِّنكُمْ أُمَّةٌ﴾",
        "effect_W": 0.10, "effect_B": 0.20,
        "letters": {"ar": "ع", "en": "A"},
    },
    "hudud": {
        "label": T("٦. إقامة الحدود", "6. Limits"),
        "desc": T("+ إقامة الحدود | − تعطيلها", "+ Establishing | − Abolishing"),
        "aya": "﴿تِلْكَ حُدُودُ اللَّهِ﴾",
        "effect_W": 0.05, "effect_B": 0.25,
        "letters": {"ar": "ح", "en": "H"},
    },
    "jihad": {
        "label": T("٧. الجهاد", "7. Jihad"),
        "desc": T("+ جهاد في سبيل الله | − قعود", "+ Jihad | − Sitting back"),
        "aya": "﴿وَجَاهِدُوا فِي اللَّهِ﴾",
        "effect_W": 0.15, "effect_B": 0.15,
        "letters": {"ar": "ج", "en": "J"},
    },
}

# ═══════════════════════════════════════════════════════════════
# قاعدة بيانات الشواهد التاريخية (مصححة)
# ═══════════════════════════════════════════════════════════════
HISTORICAL_DATA = {
    T("الخلافة الراشدة (٦٣٢-٦٦١م)", "Rashidun Caliphate (632-661 CE)"): {
        "W": 0.95, "B": 0.95, "E": 0.90,
        "desc": T("أعلى فترات التوازن في التاريخ الإسلامي. الثبات الذاتي.", "Highest balance period. Self-sustained stability.")
    },
    T("الدولة الأموية – أوج التوسع (٧٢٠م)", "Umayyad – Peak Expansion (720 CE)"): {
        "W": 0.50, "B": 0.40, "E": 0.95,
        "desc": T("التمكين امتداد لرصيد الخلافة الراشدة. بداية الاستدراج.", "Empowerment extended from Rashidun reserve. Beginning of Istidraj.")
    },
    T("الدولة الأموية – قبل السقوط (٧٤٠م)", "Umayyad – Before Fall (740 CE)"): {
        "W": 0.25, "B": 0.20, "E": 0.70,
        "desc": T("انهيار W و B مع استمرار التمكين ظاهرياً. استدراج متقدم.", "W and B collapsed while empowerment continued. Advanced Istidraj.")
    },
    T("الدولة العثمانية – أواخر (١٨٠٠م)", "Ottoman Empire – Late (1800 CE)"): {
        "W": 0.35, "B": 0.25, "E": 0.60,
        "desc": T("الرجل المريض: فجوة استدراج طويلة.", "The sick man: Long Istidraj gap.")
    },
    T("الاتحاد السوفيتي (١٩٢٢-١٩٩١م)", "Soviet Union (1922-1991 CE)"): {
        "W": 0.05, "B": 0.10, "E": 0.70,
        "desc": T("W = صفر تقريباً: انهيار مفاجئ.", "W ≈ 0: Sudden collapse.")
    },
}

# ═══════════════════════════════════════════════════════════════
# دالة الحساب
# ═══════════════════════════════════════════════════════════════
def compute_WB_final(values):
    W_total = 0.1; B_total = 0.1
    for key, val in values.items():
        if key in ISLAMIC_SYSTEM_FINAL:
            W_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_W"]
            B_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_B"]
    return np.clip(W_total, 0.01, 1.0), np.clip(B_total, 0.01, 1.0)

# ═══════════════════════════════════════════════════════════════
# أسئلة البوصلة – ١٩ سؤالاً (صياغة حيادية محكمة)
# ═══════════════════════════════════════════════════════════════
UNIFIED_QUESTIONS = [
    {"q": T("١. مركزية الله في الحياة: في خضم انشغال الناس بالوظيفة والمال والشهرة... أين الله في معادلة حياتك اليومية؟", "1. Where is Allah in your daily life?"), "answers": [
        (T("🌟 الله مركز حياتي وقراراتي", "🌟 Allah is the center of my life"), 0.8, 0.2),
        (T("⚠️ أعبد الله لكن الدنيا تطغى عليّ أحياناً", "⚠️ I worship but dunia overcomes me sometimes"), 0.3, -0.2),
        (T("🔴 لا أشعر بوجود الله في تفاصيل يومي", "🔴 I don't feel Allah's presence in my daily life"), -0.3, 0.1),
        (T("🩷 أتحدث عن الدين لكن قلبي مشغول بغيره", "🩷 I talk about religion but my heart is elsewhere"), -0.2, -0.3),
    ]},
    {"q": T("٢. الصلاة – مختبر الولاء اليومي: في زمن المشتتات... أين موقع الصلاة من يومك؟", "2. Prayer: Where is prayer in your daily routine?"), "answers": [
        (T("🌟 الصلاة راحتي وقرة عيني، لا أتركها", "🌟 Prayer is my comfort and I never miss it"), 0.7, 0.3),
        (T("⚠️ أصلي لكني أؤخرها أو أسرع فيها", "⚠️ I pray but sometimes delay or rush"), 0.3, -0.1),
        (T("🔴 لا أجد في نفسي دافعاً للصلاة", "🔴 I don't feel motivated to pray"), -0.3, 0.1),
        (T("🩷 أصلي أمام الناس وأتركها سراً", "🩷 I pray publicly and abandon it privately"), -0.1, -0.3),
    ]},
    {"q": T("٣. الزكاة والصيام – تطهير المال والنفس: هل تؤدي الزكاة وتصوم إيماناً واحتساباً؟", "3. Zakat & Fasting: Do you give Zakat and fast with faith?"), "answers": [
        (T("🌟 نعم، لله وحده، وأشعر بتطهير روحي", "🌟 Yes, for Allah alone, and I feel spiritual purification"), 0.5, 0.5),
        (T("⚠️ أفعلهما لكن بغير روحهما", "⚠️ I do them but without their true spirit"), 0.2, -0.1),
        (T("🔴 لا أزكي ولا أصوم", "🔴 I don't give Zakat nor fast"), -0.2, 0.2),
        (T("🩷 أفعلهما لأجل الناس لا لله", "🩷 I do them for people, not for Allah"), -0.1, -0.3),
    ]},
    {"q": T("٤. الحج – شوق إلى بيت الله: هل في قلبك شوق حقيقي لزيارة بيت الله؟", "4. Hajj: Is there real longing for the House of Allah?"), "answers": [
        (T("🌟 قلبي معلق بالبيت الحرام وأخطط لزيارته", "🌟 My heart is attached to the Sacred House and I plan to visit"), 0.6, 0.4),
        (T("⚠️ أتمناه لكني لا أخطط له", "⚠️ I wish but don't plan for it"), 0.2, -0.1),
        (T("🔴 لا شوق لي ولا اهتمام", "🔴 No longing or interest"), -0.2, 0.1),
        (T("🩷 أقول سأحج لأجل منظر اجتماعي", "🩷 I say I'll go for social appearance"), -0.1, -0.2),
    ]},
    {"q": T("٥. تحكيم الشريعة: في عصر حُصرت فيه الشريعة في الأحوال الشخصية... أين تقف؟", "5. Applying Sharia: Where do you stand?"), "answers": [
        (T("🌟 شرع الله هو الحكم في كل شيء", "🌟 Allah's law should govern everything"), 0.4, 0.6),
        (T("⚠️ الشريعة مثالية لكن يصعب تطبيقها كاملة اليوم", "⚠️ Sharia is ideal but hard to fully apply today"), 0.2, -0.1),
        (T("🔴 الشريعة لا تصلح لهذا العصر", "🔴 Sharia is unsuitable for this age"), -0.2, 0.2),
        (T("🩷 أطالب بها شعاراً لا تطبيقاً", "🩷 I call for it as a slogan, not for real"), -0.1, -0.3),
    ]},
    {"q": T("٦. الولاء والبراءة في زمن العولمة: هل انتماؤك للإسلام فوق كل انتماء؟", "6. Loyalty in globalization: Is your Islamic identity above all?"), "answers": [
        (T("🌟 الإسلام هويتي الأولى والأخيرة", "🌟 Islam is my primary and ultimate identity"), 0.7, 0.3),
        (T("⚠️ مسلم لكن الوطن أو القومية تطغى أحياناً", "⚠️ Muslim but nationality overrides sometimes"), 0.3, -0.2),
        (T("🔴 مواطن عالمي أولاً، والدين للتعبد فقط", "🔴 Global citizen first, religion is just for worship"), -0.2, 0.1),
        (T("🩷 مسلم ثقافياً فقط بدون التزام", "🩷 Culturally Muslim only, without commitment"), -0.1, -0.2),
    ]},
    {"q": T("٧. الصدق والوفاء: في عصر العلاقات العامة... هل أنت صادق في أقوالك وأفعالك؟", "7. Truthfulness: Are you truthful in words and deeds?"), "answers": [
        (T("🌟 الصدق ديني والوفاء طبعي", "🌟 Truthfulness is my religion"), 0.6, 0.4),
        (T("⚠️ أصدق غالباً لكني أكذب للمصلحة أحياناً", "⚠️ Mostly truthful but lie for benefit"), 0.3, -0.2),
        (T("🔴 الكذب أداة ضرورية للتعامل", "🔴 Lying is a necessary tool"), -0.2, 0.1),
        (T("🩷 أظهر الصدق وأخفي الكذب", "🩷 I show truth and hide lies"), -0.1, -0.3),
    ]},
    {"q": T("٨. الأمر بالمعروف والنهي عن المنكر: في زمن الخصوصية... هل تأمر وتنهى؟", "8. Enjoining & Forbidding: Do you enjoin good and forbid evil?"), "answers": [
        (T("🌟 نعم، بالحكمة والموعظة الحسنة", "🌟 Yes, with wisdom"), 0.3, 0.7),
        (T("⚠️ أحياناً لكني أخاف ردود الفعل", "⚠️ Sometimes but fear reactions"), 0.1, -0.1),
        (T("🔴 لا شأن لي بالناس، كلٌّ حر", "🔴 Not my business"), -0.1, 0.1),
        (T("🩷 آمر غيري ولا أفعل", "🩷 I enjoin others and don't do it"), -0.2, -0.2),
    ]},
    {"q": T("٩. البراءة من الطاغوت: في زمن شرعية الأنظمة... هل تبرأ من الطواغيت؟", "9. Disavowal of Taghut: Do you disavow false deities and tyrants?"), "answers": [
        (T("🌟 أكفر بالطاغوت وأتبرأ منه قلباً وقالباً", "🌟 I disbelieve in Taghut and disavow it completely"), 0.2, 0.8),
        (T("⚠️ أكرههم لكني أتعامل معهم مضطراً", "⚠️ I hate them but deal with them out of necessity"), 0.1, -0.2),
        (T("🔴 لا وجود للطواغيت اليوم", "🔴 Taghut doesn't exist today"), -0.2, 0.1),
        (T("🩷 أظهر البراءة وأبطن الموالاة", "🩷 I show disavowal and hide alliance"), -0.1, -0.3),
    ]},
    {"q": T("١٠. البراءة من الشرك: في زمن حوار الأديان... هل تبرأ من الشرك وأهله؟", "10. Disavowal of polytheism: Do you disavow it?"), "answers": [
        (T("🌟 أتبرأ من كل ما يعبد من دون الله", "🌟 I disavow all worshipped besides Allah"), 0.2, 0.8),
        (T("⚠️ أكره الشرك لكني لا أجاهر بعدائي لأهله", "⚠️ I hate it but don't declare enmity"), 0.1, -0.1),
        (T("🔴 لكل إنسان دينه، لا داعي للبراءة", "🔴 Everyone has their religion"), -0.2, 0.1),
        (T("🩷 أشاركهم أعيادهم وأقول إنه باطل", "🩷 I join their festivals but say it's false"), -0.1, -0.3),
    ]},
    {"q": T("١١. البراءة من الكفر والإلحاد: في زمن حرية الفكر... هل تبرأ من الكفر؟", "11. Disavowal of disbelief: Do you disavow atheism?"), "answers": [
        (T("🌟 أكفر بكل فكر إلحادي وأتبرأ منه", "🌟 I disbelieve in all atheist thought"), 0.2, 0.8),
        (T("⚠️ أكرهه لكني أتعامل مع أهله بحسن نية", "⚠️ I hate it but deal kindly"), 0.1, -0.1),
        (T("🔴 الإلحاد فكر يحترم كغيره", "🔴 Atheism is as respectable"), -0.2, 0.1),
        (T("🩷 أقول ضده وأعجب ببعض أفكاره سراً", "🩷 I oppose publicly, admire privately"), -0.1, -0.3),
    ]},
    {"q": T("١٢. البراءة من النفاق: في زمن المرونة والبراغماتية... هل تبرأ من النفاق؟", "12. Disavowal of hypocrisy: Do you disavow it?"), "answers": [
        (T("🌟 أمقت النفاق وأجاهد نفسي لأكون صادقاً", "🌟 I hate hypocrisy and struggle to be sincere"), 0.2, 0.8),
        (T("⚠️ أكرهه لكني أتلون للمصلحة أحياناً", "⚠️ I hate it but adapt for benefit"), 0.1, -0.2),
        (T("🔴 التلون ضرورة حياة، لا بأس به", "🔴 Adapting is a life necessity"), -0.2, 0.1),
        (T("🩷 أقول خلاف ما أفعل باستمرار", "🩷 I constantly say what I don't do"), -0.3, -0.3),
    ]},
    {"q": T("١٣. البراءة من الربا: في زمن النظام المالي العالمي... هل تبرأ من الربا؟", "13. Disavowal of usury: Do you disavow it?"), "answers": [
        (T("🌟 أتبرأ منه ولا أتعامل به مهما كلفني", "🌟 I disavow and avoid it"), 0.2, 0.8),
        (T("⚠️ أكرهه لكني مضطر للتعامل مع البنوك", "⚠️ I hate it but am forced"), 0.1, -0.2),
        (T("🔴 الربا ضرورة اقتصادية لا غنى عنها", "🔴 Usury is indispensable"), -0.2, 0.1),
        (T("🩷 أقول حرام وأتعامل به", "🩷 I say it's haram and deal with it"), -0.1, -0.3),
    ]},
    {"q": T("١٤. البراءة من الظلم: في زمن الأمر الواقع... هل تبرأ من الظلم والظالمين؟", "14. Disavowal of injustice: Do you disavow it?"), "answers": [
        (T("🌟 لا أرضى بالظلم وأنصر المظلوم", "🌟 I reject injustice and help the oppressed"), 0.3, 0.7),
        (T("⚠️ أكرهه لكني أسكت خوفاً على نفسي", "⚠️ I hate it but stay silent"), 0.1, -0.1),
        (T("🔴 القوي يأكل الضعيف، هذه طبيعة الحياة", "🔴 The strong eat the weak"), -0.3, 0.1),
        (T("🩷 أتحدث عن العدالة وأظلم غيري", "🩷 I speak of justice and oppress"), -0.2, -0.3),
    ]},
    {"q": T("١٥. البراءة من الفواحش: في زمن الحرية الشخصية... هل تبرأ من الفواحش؟", "15. Disavowal of immorality: Do you disavow it?"), "answers": [
        (T("🌟 أتبرأ منها وأحفظ نفسي وأهلي", "🌟 I disavow and guard myself"), 0.2, 0.8),
        (T("⚠️ أكرهها لكني لا أنكرها على غيري", "⚠️ I hate it but don't forbid others"), 0.1, -0.1),
        (T("🔴 حرية شخصية لا تُمنع", "🔴 Personal freedom can't be restricted"), -0.2, 0.1),
        (T("🩷 أتحدث عن الأخلاق وأفعلها سراً", "🩷 I speak of morals and do it secretly"), -0.2, -0.3),
    ]},
    {"q": T("١٦. إقامة الحدود: هل تقيم حدود الله ولا تتعداها؟", "16. Establishing limits: Do you establish Allah's limits?"), "answers": [
        (T("🌟 حدود الله هي الحاكمة في حياتي", "🌟 Allah's limits govern my life"), 0.3, 0.7),
        (T("⚠️ أراها صعبة التطبيق الكامل اليوم", "⚠️ Difficult to fully apply today"), 0.1, -0.1),
        (T("🔴 حدود متخلفة لا تناسب العصر", "🔴 Backward limits"), -0.2, 0.2),
        (T("🩷 أطالب بها شكلاً وأخالفها فعلاً", "🩷 I call for them in form, violate in practice"), -0.1, -0.2),
    ]},
    {"q": T("١٧. الجهاد الباطن: هل تحمل هم الإسلام والمسلمين في قلبك؟", "17. Inner Jihad: Do you carry the concerns of Islam?"), "answers": [
        (T("🌟 هم الأمة في قلبي وأعمل لنصرتها", "🌟 I carry the nation's concerns and act"), 0.5, 0.5),
        (T("⚠️ أهتم أحياناً لكني لا أفعل شيئاً", "⚠️ I care sometimes but do nothing"), 0.2, -0.1),
        (T("🔴 لا يهمني أمرهم، مشغول بنفسي", "🔴 I don't care"), -0.2, 0.1),
        (T("🩷 أظهر الاهتمام وأبطن اللامبالاة", "🩷 I show care and hide indifference"), -0.1, -0.2),
    ]},
    {"q": T("١٨. الجهاد بالمال والنفس: هل تنصر الحق وأهله والمستضعفين؟", "18. Jihad with wealth & self: Do you support truth?"), "answers": [
        (T("🌟 أبذل نفسي ومالي للحق ما استطعت", "🌟 I give myself and wealth for truth"), 0.4, 0.6),
        (T("⚠️ أساعد لكني لا أضحي كثيراً", "⚠️ I help but don't sacrifice much"), 0.2, -0.1),
        (T("🔴 لا أبذل شيئاً، هذه مشاكلهم", "🔴 I give nothing"), -0.2, 0.1),
        (T("🩷 أتحدث عن النصرة ولا أفعل", "🩷 I talk and don't act"), -0.1, -0.2),
    ]},
    {"q": T("١٩. الحب والبغض في الله – البوصلة النهائية: في زمن المصالح... هل تحب وتبغض في الله؟", "19. Love & Hate for Allah: Do you love and hate for Allah?"), "answers": [
        (T("🌟 أحب وأبغض في الله، لا تأخذني في الحق لومة لائم", "🌟 I love and hate for Allah"), 0.5, 0.5),
        (T("⚠️ أحب في الله لكني لا أبغض في الله", "⚠️ I love but don't hate for Allah"), 0.3, -0.2),
        (T("🔴 لا هذا ولا ذاك، علاقاتي بالمصالح", "🔴 Neither, based on interests"), -0.2, 0.1),
        (T("🩷 أوالي من ينفعني وأعادي من يضرني", "🩷 I ally with who benefits me"), -0.2, -0.3),
    ]},
]

# دالة رسم شجرة الإيمان (مختصرة)
def render_faith_tree(values_dict, W_val=None, B_val=None):
    if W_val is None or B_val is None:
        W_val, B_val = compute_WB_final(values_dict)
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    faith_y = 9
    ax.text(5, faith_y, f"{ISLAMIC_SYSTEM_FINAL['faith']['label']} [أ]\n{values_dict.get('faith', 0):.2f}", ha='center', fontsize=12, color='#FFD700', fontweight='bold', bbox=dict(facecolor='#0a0f1e', edgecolor='#FFD700', boxstyle='round,pad=0.5'))
    worship_y = 7
    ax.text(2.5, worship_y, f"{ISLAMIC_SYSTEM_FINAL['worship']['label']} [ط]\n{values_dict.get('worship', 0):.2f}", ha='center', fontsize=10, color='#FFD700', bbox=dict(facecolor='#0a0f1e', edgecolor='#FFA500', boxstyle='round,pad=0.3'))
    ax.text(7.5, worship_y, f"{ISLAMIC_SYSTEM_FINAL['enjoining']['label']} [ع]\n{values_dict.get('enjoining', 0):.2f}", ha='center', fontsize=10, color='#00BFFF', bbox=dict(facecolor='#0a0f1e', edgecolor='#00BFFF', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(2.5, worship_y+0.3), xytext=(5, faith_y-0.3), arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1.5))
    ax.annotate('', xy=(7.5, worship_y+0.3), xytext=(5, faith_y-0.3), arrowprops=dict(arrowstyle='->', color='#00BFFF', lw=1.5))
    trans_y = 5
    ax.text(5, trans_y, f"{ISLAMIC_SYSTEM_FINAL['transactions']['label']} [س]\n{values_dict.get('transactions', 0):.2f}", ha='center', fontsize=10, color='#FFD700', bbox=dict(facecolor='#0a0f1e', edgecolor='#00FF88', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(5, trans_y+0.3), xytext=(2.5, worship_y-0.3), arrowprops=dict(arrowstyle='->', color='#FFA500', lw=1.5))
    ax.annotate('', xy=(5, trans_y+0.3), xytext=(7.5, worship_y-0.3), arrowprops=dict(arrowstyle='->', color='#00BFFF', lw=1.5))
    morals_y = 3
    ax.text(5, morals_y, f"{ISLAMIC_SYSTEM_FINAL['morals']['label']} [ي]\n{values_dict.get('morals', 0):.2f}", ha='center', fontsize=10, color='#FFD700', bbox=dict(facecolor='#0a0f1e', edgecolor='#FF69B4', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(5, morals_y+0.3), xytext=(5, trans_y-0.3), arrowprops=dict(arrowstyle='->', color='#00FF88', lw=1.5))
    bottom_y = 1
    ax.text(2.5, bottom_y, f"{ISLAMIC_SYSTEM_FINAL['hudud']['label']} [ح]\n{values_dict.get('hudud', 0):.2f}", ha='center', fontsize=10, color='#FFD700', bbox=dict(facecolor='#0a0f1e', edgecolor='#FF6347', boxstyle='round,pad=0.3'))
    ax.text(7.5, bottom_y, f"{ISLAMIC_SYSTEM_FINAL['jihad']['label']} [ج]\n{values_dict.get('jihad', 0):.2f}", ha='center', fontsize=10, color='#FFD700', bbox=dict(facecolor='#0a0f1e', edgecolor='#FF4500', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(2.5, bottom_y+0.3), xytext=(5, morals_y-0.3), arrowprops=dict(arrowstyle='->', color='#FF69B4', lw=1.5))
    ax.annotate('', xy=(7.5, bottom_y+0.3), xytext=(5, morals_y-0.3), arrowprops=dict(arrowstyle='->', color='#FF69B4', lw=1.5))
    ax.text(5, -0.5, f"S = W × B = {W_val:.2f} × {B_val:.2f} = {W_val*B_val:.3f}", ha='center', fontsize=14, color='#FFD700', fontweight='bold')
    ax.set_title(T("🌳 شجرة الإيمان", "🌳 Faith Tree"), color='white', fontsize=14, fontweight='bold')
    st.pyplot(fig)

def create_final_sliders(prefix, defaults=None):
    if defaults is None: defaults = {k: 0.0 for k in ISLAMIC_SYSTEM_FINAL}
    values = {}
    for key, data in ISLAMIC_SYSTEM_FINAL.items():
        letters_str = data["letters"][L]
        label_with_letters = f"{data['label']}  [{letters_str}]"
        values[key] = st.slider(label_with_letters, -1.0, 1.0, defaults.get(key, 0.0), 0.05, key=f"{prefix}_{key}", help=f"{data['desc']}\n\n{data['aya']}")
    return values

# الجلسة العامة
if 'init' not in st.session_state:
    np.random.seed(42); random.seed(42)
    cx, cy = 14, 10.0; N = 150
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-13, cx+13, N)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, N)
    st.session_state.sw = np.random.uniform(0.1, 1, N)
    st.session_state.sb = np.random.uniform(0.1, 1, N)
    st.session_state.N = N
    st.session_state.W = 0.55; st.session_state.B = 0.52; st.session_state.E = 0.3
    st.session_state.S = 0.55 * 0.52
    st.session_state.pW = deque([0.55], maxlen=50); st.session_state.pB = deque([0.52], maxlen=50)
    st.session_state.hS = deque(maxlen=300); st.session_state.hE = deque(maxlen=300); st.session_state.hx = deque(maxlen=300)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0; st.session_state.frame = 0
    st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]; st.session_state.path_kappa = [0.0]
    for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
        setattr(st.session_state, f"path_{l}", [0.5])
    st.session_state.live_compass_W = 0.0; st.session_state.live_compass_B = 0.0
    st.session_state.live_compass_history_W = [0.0]; st.session_state.live_compass_history_B = [0.0]
    st.session_state.live_compass_answered = {}; st.session_state.live_compass_count = 0
    st.session_state.challenge = None; st.session_state.spiritual_nudge = None
    st.session_state.init = True

print("✅ المرحلة الأولى مكتملة.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثانية: رسالة الترحيب، دليل المستخدم، الميزان الحي، العنوان، التبويبات
# ═══════════════════════════════════════════════════════════════

# --- رسالة الترحيب – الصياغة المحكمة ---
with st.expander(T("📜 رسالة ترحيب", "📜 Welcome Message"), expanded=True):
    st.markdown(f"""
    <div class="message-box">
    <h2 style="text-align:center;color:#FFD700;">⚖️ {T('مختبر الميزان', 'The Mizan Lab')}</h2>
    <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;">
    "{T('هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟', 'Is there a single law governing the atom and civilization?')}"
    </p>
    <p>{T(
    'هذا ليس كتابًا، وليس تطبيقًا. هذا مختبر. مختبرٌ صغير، لعله يفتح لك بابًا كبيرًا. '
    'لا ندّعي الحقيقة المطلقة، بل ندعوك لرؤية شيءٍ قد يكون مرّ على قلبك ولم تلاحظه.',
    'This is not a book, nor an app. This is a lab. A small lab, perhaps it opens a big door for you. '
    'We do not claim absolute truth, but invite you to see something that may have passed your heart unnoticed.'
    )}</p>
    <p>{T(
    'تأمل معي: الذرةُ في داخلها قوتان: جاذبيةٌ تجمع، وتنافرٌ يمنع التصادم. لو اختلت إحداهما، لانهارت الذرة. '
    'والخليةُ في جسدك: جهاز مناعةٍ يحمي، وغذاءٌ يبني. لو نامت المناعة، لالتهم المرضُ الجسد.',
    'Reflect with me: the atom has two forces: attraction that gathers, and repulsion that prevents collision. '
    'If one fails, the atom collapses. And the cell in your body: an immune system that protects, and nutrition that builds. '
    'If immunity sleeps, disease devours the body.'
    )}</p>
    <p>{T(
    'وحتى في عالم الكيمياء، يتجلى القانون نفسه: الذرّات المتآلفة تتحد برابطةٍ قوية (هذا ولاؤها)، '
    'لكنها تحتاج إلى "طاقة تنشيط" لتنفصل عن ذراتٍ أخرى كانت مرتبطة بها (هذه براءتها). '
    'إن لم تملك هذه الطاقة، بقيت أسيرة تفاعلاتها القديمة، لا تتحد بالجديد. '
    'هذه "التوبة" الكيميائية: قوةٌ تدفعها لتكسر حاجزًا، فتنطلق إلى استقرارٍ أعظم. '
    'أليس هذا ما يحدث للمؤمن حين يتوب؟',
    'Even in chemistry, the same law manifests: compatible atoms unite with a strong bond (their loyalty), '
    'but they need "activation energy" to separate from other atoms they were bound to (their disavowal). '
    'Without this energy, they remain captive to old reactions, unable to unite with the new. '
    'This is chemical "repentance": a force that pushes them to break a barrier, launching them to greater stability. '
    'Is this not what happens to the believer when they repent?'
    )}</p>
    <p>{T(
    'والمجتمع: ولاءٌ يجمع أفراده، وبراءةٌ من الفساد تحمي تماسكه. لو غاب أحدهما، تفكك المجتمع.',
    'And society: loyalty that gathers its members, and disavowal of corruption that protects its cohesion. '
    'If either is absent, society disintegrates.'
    )}</p>
    <p style="color:#FFD700;font-weight:bold;">{T(
    'هل هذه مصادفة؟ أم أن هناك "قانونًا واحدًا" ينساب في نسيج الوجود كله، من الذرة إلى الحضارة؟',
    'Is this coincidence? Or is there a "single law" flowing through the fabric of existence, from atom to civilization?'
    )}</p>
    <p>{T(
    'نحن هنا لا نعظ. نحن نعرض. لا نفرض عليك جوابًا، بل نتركك تجرب بيدك. '
    'حرّك المنزلقات. أجب عن الأسئلة. شاهد كيف يتغير الثبات. واسأل نفسك: '
    'لماذا ينهار كل شيء عندما يختل أحد القطبين؟ '
    'لماذا تتكرر هذه الثنائية في كل ما حولنا؟ '
    'هل هناك "حق" و"باطل" موجودان في صلب الوجود، لا في كتب الأخلاق فقط؟',
    'We are not preaching. We are presenting. We do not impose an answer, but let you experiment with your own hands. '
    'Move the sliders. Answer the questions. Watch how stability changes. And ask yourself: '
    'Why does everything collapse when one pole fails? '
    'Why does this duality repeat everywhere around us? '
    'Is there "truth" and "falsehood" embedded in the core of existence, not just in books of ethics?'
    )}</p>
    <p style="text-align:center;color:#FFD700;font-size:1.2em;font-weight:bold;">S = W × B</p>
    <p>{T(
    'W: الولاء لله وأوليائه. B: البراءة من الطاغوت وأوليائه. S: الثبات الوجودي.',
    'W: Loyalty to Allah & His allies. B: Disavowal of Taghut & its allies. S: Existential Stability.'
    )}</p>
    <p>{T(
    'هذه معادلة، لا أكثر. ولكنها قد تكون أعمق مما تظن. إنها ليست اختراعًا، بل استنباطٌ من قوله تعالى: '
    '﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾.',
    'This is an equation, nothing more. But it may be deeper than you think. It is not an invention, '
    'but a derivation from His saying: ﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾.'
    )}</p>
    <p style="color:#FFD700;">{T(
    '"العروة الوثقى" هي الثبات الذي تبحث عنه. والطريق إليها مرسومٌ في هذه المنزلقات السبعة وهذه الأسئلة التسعة عشر.',
    '"The Firm Handhold" is the stability you seek. The path to it is drawn in these seven sliders and nineteen questions.'
    )}</p>
    <p style="text-align:center;font-style:italic;color:#AAA;">{T(
    'جرب. تأمل. واسأل. الباب مفتوح.',
    'Try. Reflect. Ask. The door is open.'
    )}</p>
    </div>
    """, unsafe_allow_html=True)

# --- دليل المستخدم – صياغة محكمة ---
with st.expander(T("📖 دليل المستخدم", "📖 User Guide"), expanded=False):
    st.markdown(T("""
    ### 🎯 كيف تستخدم هذا المختبر؟
    
    **١. المنزلقات السبعة:** كل منزلق يمثل بُعدًا من أبعاد الإسلام، ويحمل حرفه من المعجم الهندسي [بين قوسين].
    حركه **يمينًا** (قيم موجبة) لترى كيف يزيد الثبات، و**يسارًا** (قيم سالبة) لترى كيف ينهار.
    
    **٢. بوصلة الأسئلة (١٩ سؤالاً):** أجب عن الأسئلة لتعرف موقعك الدقيق.
    كل سؤال له ٤ إجابات تؤثر **كل واحدة منها على القطبين (W و B) معًا**.
    النقطة تتحرك فورًا مع كل إجابة.
    
    **٣. أصل النظرية:** تبويب كامل يشرح النظرية من جذورها: الفطرة، الإنسان، الدين القيم، الإسلام،
    العبادات كمختبرات تدريبية، السنن الإلهية، والحديثان النبويان المؤسِّسان.
    
    **٤. مختبر الأمة المتكاملة:** مجتمع + دولة + أمة في محاكاة واحدة.
    
    **٥. الشواهد التاريخية:** قارن بين الدول التاريخية لترى كيف تنطبق المعادلة على التاريخ الفعلي.
    
    **٦. هندسة الصراط:** النموذج الإبراهيمي، والتحفيز الروحي بالآيات والأحاديث مع كل خطوة.
    
    **٧. الميزان الأخروي الحي:** يظهر في الشريط الجانبي، يسجل حسناتك وسيئاتك في الوقت الحقيقي.
    
    **٨. تحدي اليوم:** تحدٍ جديد كل يوم لتقوية أحد جوانب ميزانك.
    
    **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
    """,
    """
    ### 🎯 How to Use This Lab
    
    **1. Seven Sliders:** Each slider represents a dimension of Islam and carries its letter from the Geometric Lexicon.
    Move **right** for positive values, **left** for negative.
    
    **2. 19-Question Compass:** Each question has 4 answers affecting **both poles simultaneously**.
    Your point moves immediately with each answer.
    
    **3. Theory Tab:** Explains the complete theory: fitrah, human, divine law, Islam, worship as training labs,
    divine laws in history, and the two founding hadiths.
    
    **4. Integrated Nation Lab:** Society + State + Nation in one simulation.
    
    **5. Historical Evidence:** Compare historical nations to see the equation in action.
    
    **6. Path Geometry:** The Abrahamic model and spiritual motivation with verses and hadiths at each step.
    
    **7. Live Scales:** Your deeds are tracked in real-time in the sidebar.
    
    **8. Daily Challenge:** A new challenge each day to strengthen one aspect of your balance.
    
    **Central Equation:** **S = W × B** (multiplication, not addition).
    """))

# --- الميزان الأخروي الحي ---
def render_live_scales():
    good = st.session_state.get('good', 0)
    bad = st.session_state.get('bad', 0)
    balance = good - bad
    if balance > 0: status, color = T("⚖️ راجحة", "⚖️ Winning"), '#FFD700'
    elif balance < 0: status, color = T("⚖️ خاسرة", "⚖️ Losing"), '#FF4444'
    else: status, color = T("⚖️ متوازنة", "⚖️ Balanced"), '#888'
    st.sidebar.markdown(f"""
    <div style="text-align:center;padding:10px;background:rgba(10,15,30,0.9);border-radius:10px;border:1px solid #FFD700;margin-top:10px;">
        <p style="color:#FFD700;font-size:0.8em;margin:0;">📜 {T('الميزان الحي', 'Live Scales')}</p>
        <p style="color:#FFD700;font-size:0.7em;margin:2px 0;">{T('حسنات', 'Good')}: {good:.0f} | {T('سيئات', 'Bad')}: {bad:.0f}</p>
        <p style="color:{color};font-size:0.9em;margin:0;font-weight:bold;">{status}</p>
    </div>
    """, unsafe_allow_html=True)

# --- العنوان الرئيسي ---
col_icon1, col_title, col_icon2 = st.columns([1, 6, 1])
with col_icon1:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{T('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
with col_icon2:
    st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='verse-text'>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    <br><span style='font-size:0.8em;'>S = W × B | ق = ١٠٠ = الحق = الميزان</span>
</div>
""", unsafe_allow_html=True)

# --- أزرار التحكم ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("English" if L == "ar" else "العربية", key="btn_lang", use_container_width=True):
        st.session_state.lang = "en" if L == "ar" else "ar"
        st.rerun()

st.markdown("---")

# --- التبويبات ---
tab_labels = [
    T("📖 أصل النظرية", "📖 Theory"),
    T("🌌 الكون", "🌌 Cosmos"),
    T("🧍 الفرد", "🧍 Individual"),
    T("🏛️ الأمة المتكاملة", "🏛️ Integrated Nation"),
    T("🏰 الحضارة", "🏰 Civilization"),
    T("📜 الشواهد", "📜 Evidence"),
    T("📐 الصراط", "📐 Path"),
]

tabs = st.tabs(tab_labels)

# --- شريط جانبي ---
with st.sidebar:
    st.markdown("### ⚙️ إعدادات عامة")
    lag = st.select_slider(T("فجوة الاستدراج", "Istidraj Gap"), options=[5,10,15,22,30,40,50], value=22, key="lag")
    st.markdown("---")
    render_live_scales()
    st.markdown("---")
    st.markdown(f"### 🎯 {T('تحدي اليوم', 'Daily Challenge')}")
    if st.session_state.get('challenge') is None:
        challenges = [
            T("اليوم: أجب عن أسئلة البوصلة الـ ١٩ لتكتشف موقعك بدقة.", "Today: Answer the 19 compass questions to discover your precise position."),
            T("اليوم: شاهد المشهد الكوني لمدة دقيقتين وتأمل في الاستدراج.", "Today: Watch the cosmic scene for 2 minutes and reflect on Istidraj."),
            T("اليوم: قارن بين حضارتين في تبويب 'الحضارة' ولاحظ أثر W و B.", "Today: Compare two civilizations and observe the effect of W and B."),
            T("اليوم: استعرض شاهداً تاريخياً وتأمل كيف تتحقق السنن الإلهية.", "Today: Review a historical case and reflect on the divine laws."),
        ]
        st.session_state.challenge = random.choice(challenges)
    st.info(st.session_state.challenge)
    st.markdown("---")
    if st.button("🔄 إعادة ضبط كل شيء", key="btn_reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

print("✅ المرحلة الثانية مكتملة: رسالة الترحيب، دليل المستخدم، الميزان الحي، العنوان، التبويبات.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الثالثة: أصل النظرية، الكون، الفرد
# ═══════════════════════════════════════════════════════════════

# --- تبويب ١: أصل النظرية – من الفاتحة إلى الناس ---
with tabs[0]:
    st.header(T("📖 أصل النظرية – نظرية الإسلام المتكاملة", "📖 Theory – The Integrated Islamic Theory"))
    
    st.markdown(T("""
    <div style="text-align:center;color:#AAA;font-size:1.1em;margin-bottom:30px;line-height:2.2;">
    هذه هي <b style="color:#FFD700;">الأسس القرآنية والنبوية</b> التي تثبت أن المعادلة <b style="color:#FFD700;">S = W × B</b> 
    ليست اختراعًا بشريًا، بل هي استنباط من كلام الله وسنة رسوله ﷺ،
    يؤيدها العقل، وتشهد لها الفطرة، وينطق بها الكون.
    </div>
    """, """
    <div style="text-align:center;color:#AAA;font-size:1.1em;margin-bottom:30px;line-height:2.2;">
    These are the <b style="color:#FFD700;">Quranic and Prophetic foundations</b> proving that the equation <b style="color:#FFD700;">S = W × B</b>
    is not a human invention, but a derivation from the Word of God and the Sunnah of His Messenger ﷺ,
    supported by reason, witnessed by fitrah, and declared by the cosmos.
    </div>
    """), unsafe_allow_html=True)

    # --- الفصل الأول: الدين القيم ---
    with st.expander(T("⚖️ ١. الدين القيم – قانون الوجود الحق", "⚖️ 1. Al-Deen Al-Qayyim – The True Law of Existence"), expanded=True):
        st.markdown(T("""
        ### ⚖️ الدين القيم – قانون الوجود الحق
        
        نبدأ رحلتنا من أم الكتاب، من الدعاء الذي لا تنقطع ألسنة المؤمنين عن ترداده في كل ركعة: **﴿اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ﴾**.
        ما هو هذا الصراط المستقيم الذي نسأل الله الهداية إليه سبع عشرة مرة في اليوم؟ إنه ليس مجرد طريق، بل هو **الدين القيم** نفسه،
        قانون الوجود الذي فطر الله عليه السماوات والأرض ومن فيهن.
        
        **تعريفه:** الدين القيم هو قانون السببية الكوني الثابت في أصله، المتجدد في تطبيقاته؛ الذي أرسل به الرسل، وأنزل به الكتب.
        وهو النظام الحتمي الذي يربط الأسباب بالنتائج في العوالم الفيزيائية والبيولوجية والأخلاقية والتاريخية، دون تبديل أو تحويل.
        
        **خصائصه:** الربانية (مصدره الله وحده)، الثبات (لا يتبدل ولا يتحول)، الشمول (يسري على كل العوالم)،
        الحتمية (النتيجة مرتبطة بالسبب)، والديناميكية (يتجدد في تطبيقاته مع ثبات أصله).
        
        > **﴿فَلَن تَجِدَ لِسُنَّتِ اللَّهِ تَبْدِيلًا وَلَن تَجِدَ لِسُنَّتِ اللَّهِ تَحْوِيلًا﴾**
        
        من عرف أن للوجود قانونًا محكمًا، فقد حصل على أعظم كنز: **اليقين**.
        """,
        """
        ### ⚖️ Al-Deen Al-Qayyim – The True Law of Existence
        
        We begin from the Mother of the Book, from the supplication that never ceases: **﴿Guide us to the Straight Path﴾**.
        This is Al-Deen Al-Qayyim itself: the cosmic law of causality, constant in origin, dynamic in application.
        
        **Its characteristics:** Divine origin, immutability, comprehensiveness, inevitability, and dynamism.
        
        Whoever knows that existence has a precise law has obtained the greatest treasure: **certainty**.
        """))

    # --- الفصل الثاني: الإسلام الحنيف ---
    with st.expander(T("🕌 ٢. الإسلام الحنيف – الاستجابة الديناميكية للقانون", "🕌 2. Al-Islam Al-Hanif – The Dynamic Response"), expanded=False):
        st.markdown(T("""
        ### 🕌 الإسلام الحنيف – الاستجابة الديناميكية للقانون
        
        إذا كان الدين القيم هو القانون، فما هو موقفنا منه؟ هنا يأتي **الإسلام الحنيف**: إنه الاستجابة الوحيدة الممكنة للدين القيم.
        فكل المخلوقات "مسلمة" لله قهرًا، أما الإنسان فقد مُنح شرف الاختيار.
        
        **تعريفه:** الإسلام الحنيف هو الاستجابة الطوعية الواعية والديناميكية من الإنسان المختار لقانون السببية الكوني،
        والمتمثلة في التوجه الكلي للطاقة الإيمانية نحو الله ورسوله والمؤمنين (الولاء)،
        وصرف هذه الطاقة عن الكفر والشرك والنفاق وأهله (البراءة).
        
        **معادلته:** `I = W × B` (العلاقة ضرب لا جمع).
        
        **لماذا إبراهيم هو النموذج الأكمل؟** لأنه جسّد الاستجابة الكاملة: والى الله، وتبرأ من الطاغوت،
        فاستحق أن يكون إمامًا للناس: **﴿إِنِّي جَاعِلُكَ لِلنَّاسِ إِمَامًا﴾**.
        """,
        """
        ### 🕌 Al-Islam Al-Hanif – The Dynamic Response
        
        If Al-Deen Al-Qayyim is the law, what is our stance? **Al-Islam Al-Hanif** is the only possible response.
        All creatures submit to Allah involuntarily; only humans were granted the honor of choice.
        
        **Its equation:** `I = W × B` (multiplication, not addition).
        
        **Why Abraham?** Because he embodied the complete response, earning the station of Imamate.
        """))

    # --- الفصل الثالث: الفطرة ---
    with st.expander(T("🌳 ٣. الفطرة – نظام التشغيل الأصلي", "🌳 3. The Fitrah – The Original Operating System"), expanded=False):
        st.markdown(T("""
        ### 🌳 الفطرة – نظام التشغيل الأصلي
        
        من أين للإنسان القدرة على هذه الاستجابة؟ الجواب في **الفطرة**: إنها البذرة الإلهية في أعماق كل إنسان،
        والبرنامج الأصلي الذي يجعل الإنسان قابلاً لمعرفة الحق ومائلاً إليه.
        
        **تعريفها:** الفطرة هي نظام التشغيل الأصلي الذي فطر الله الناس عليه. وهي الاستعداد الفطري
        والبنية النفسية والروحية التي تجعل الإنسان قابلاً لمعرفة الله، ومائلاً إلى الإسلام الحنيف.
        
        **أصلها:** الميثاق الأزلي: **﴿وَإِذْ أَخَذَ رَبُّكَ مِن بَنِي آدَمَ... أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾**.
        
        الفطرة لا تموت، ولكنها تُغطى. ومهمة الوحي إيقاظها إذا نامت، وتصحيحها إذا انحرفت.
        """,
        """
        ### 🌳 The Fitrah – The Original Operating System
        
        The answer lies in the **Fitrah**: the divine seed within every human, the original program enabling knowledge of truth.
        
        **Its origin:** The primordial covenant: **﴿Am I not your Lord? They said: Yes, we have testified.﴾**
        
        The fitrah never dies, but it can be covered. The role of revelation is to awaken it.
        """))

    # --- الفصل الرابع: الولاء (W) ---
    with st.expander(T("🤍 ٤. الولاء (W) – القطب الموجب في معادلة الإسلام الحنيف", "🤍 4. Al-Walaa (W) – The Positive Pole"), expanded=False):
        st.markdown(T("""
        ### 🤍 الولاء (W) – القطب الموجب في معادلة الإسلام الحنيف
        
        الولاء هو قانون الجذب الروحي. فكما أن للكون جاذبية تجذب الكتل، فللقلب جاذبية تجذبه إلى معبوده.
        والولاء هو توجيه هذه الجاذبية الفطرية نحو الله وحده.
        
        **تعريفه:** القطب الموجب في معادلة الإسلام الحنيف. وهو توجيه كامل الطاقة الإيمانية (حبًا، طاعة، ونصرة)
        نحو الله، ثم نحو رسوله والمؤمنين. ويمكن التعبير عنه بالرمز **W**.
        
        **مراتبه:** الله (الولي الأعلى) ← الرسول ﷺ ← المؤمنون. وهذا الترتيب يثبت أن كل ولاء لغير الله إنما هو فرع عنه وتابع له.
        
        **مكوناته:** الحب القلبي، والطاعة العملية، والنصرة.
        
        > **﴿إِنَّمَا وَلِيُّكُمُ اللَّهُ وَرَسُولُهُ وَالَّذِينَ آمَنُوا﴾**
        
        ومن ثمراته: ولاية الله للعبد، والطمأنينة، والنصر، والأخوة الإيمانية.
        """,
        """
        ### 🤍 Al-Walaa (W) – The Positive Pole
        
        Loyalty is the law of spiritual gravity. As the cosmos has gravity, the heart has attraction toward its object of worship.
        
        **Definition:** The positive pole in the equation. Directing full faith energy toward Allah, His Messenger, and the believers.
        
        **Levels:** Allah → Messenger ﷺ → Believers. Every loyalty to other than Allah is a branch of loyalty to Him.
        """))

    # --- الفصل الخامس: البراءة (B) ---
    with st.expander(T("❤️ ٥. البراءة (B) – القطب السالب وسياج الفطرة", "❤️ 5. Al-Baraa (B) – The Negative Pole & the Fence of Fitrah"), expanded=False):
        st.markdown(T("""
        ### ❤️ البراءة (B) – القطب السالب وسياج الفطرة
        
        لماذا يحتاج المؤمن إلى البراءة؟ لأن الولاء الخالص لله لا يمكن أن يستقر في قلبٍ لم يُفرّغ من ولاء الطاغوت. **فالتخلية قبل التحلية**.
        وكما أن الدائرة الكهربائية لا تعمل بقطب موجب فقط، فكذلك معادلة الإسلام الحنيف لا تستقيم إلا بالولاء والبراءة معًا.
        
        **تعريفها:** القطب السالب في معادلة الإسلام الحنيف. وهي صرف الطاقة السلبية (بغضًا، عداوة، ومفاصلة)
        عن الكفر والشرك والنفاق وأهله، مع الالتزام بالعدل والقسط مع غير المحاربين.
        
        **ليست تعصبًا أعمى، بل هي:** رباط الحب في الله، وحاجز يمنع الإخوة من التفرق، وفصل وتميز يضع حدًا فاصلاً بين الفريقين،
        وسياج يحمي الفطرة من الانحراف، والإيمان من الشوائب، والهوية من الاختلاط، والاستقامة من مسالك الضلال والهلاك.
        
        **مراتبها:** البراءة القلبية (بغض الكفر)، والقولية (إعلان البراءة)، والعملية (المفاصلة والجهاد عند الاستطاعة).
        
        **شروطها وحدودها:** البراءة ليست موجهة إلى الأشخاص لذواتهم، بل إلى ما هم عليه من الكفر والعداوة.
        وهي لا تمنع العدل والبر مع غير المحاربين: **﴿لَّا يَنْهَاكُمُ اللَّهُ عَنِ الَّذِينَ لَمْ يُقَاتِلُوكُمْ فِي الدِّينِ... أَن تَبَرُّوهُمْ وَتُقْسِطُوا إِلَيْهِمْ﴾**.
        
        **متى تنقلب البراءة إلى ولاية؟** عند حصول الإيمان: **﴿أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾**.
        فإذا آمنوا، انقلبت العداوة إلى أخوة: **﴿فَإِن تَابُوا وَأَقَامُوا الصَّلَاةَ وَآتَوُا الزَّكَاةَ فَإِخْوَانُكُمْ فِي الدِّينِ﴾**.
        
        **التمييز بين البراءة العقدية والمعاملة الأخلاقية:** البراءة العقدية من الكفر لا تمنع الإحسان إلى الجار الكافر،
        ولا صلة الرحم الكافرة، ولا التجارة مع الكافر غير المحارب. وكما قال تعالى: **﴿لَّا يَنْهَاكُمُ اللَّهُ﴾**، فالبراءة عقدية، والمعاملة أخلاقية.
        
        > **﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ وَالَّذِينَ مَعَهُ إِذْ قَالُوا لِقَوْمِهِمْ إِنَّا بُرَآءُ مِنكُمْ وَمِمَّا تَعْبُدُونَ مِن دُونِ اللَّهِ كَفَرْنَا بِكُمْ وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾**
        
        **معادلة الثبات:** `S = W × B`. فإذا كان أحدهما صفرًا، كان الثبات معدومًا.
        وهذا يفسر لماذا ينهار كثير من الناس رغم ادعائهم الإيمان، لأنهم لم يحققوا البراءة من الطاغوت.
        """,
        """
        ### ❤️ Al-Baraa (B) – The Negative Pole & the Fence of Fitrah
        
        Why does the believer need disavowal? Because pure loyalty to Allah cannot settle in a heart that has not been emptied of loyalty to Taghut.
        
        **It is not blind fanaticism, but rather:** the bond of love in Allah, a barrier preventing the separation of brothers, a fence protecting fitrah from deviation and faith from impurities.
        
        **Conditions:** Disavowal is directed at disbelief, not at persons. It does not prevent justice toward non-combatants.
        
        **When does disavowal turn to loyalty?** When faith occurs: **﴿Until you believe in Allah alone﴾**.
        
        **Stability equation:** `S = W × B`. If either is zero, stability is nonexistent.
        """))

    # --- الفصل السادس: الحنيفية ---
    with st.expander(T("🔀 ٦. الحنيفية – سر المرونة والصلاحية لكل زمان ومكان", "🔀 6. Al-Hanifiyyah – The Secret of Flexibility"), expanded=False):
        st.markdown(T("""
        ### 🔀 الحنيفية – سر المرونة والصلاحية لكل زمان ومكان
        
        كيف نطبق هذه المعادلة في واقع متغير؟ الجواب في **الحنيفية**: خاصية الديناميكية والمرونة في تطبيق الإسلام الحنيف.
        
        **تعريفها:** الميل الثابت عن الباطل إلى الحق، مع قابلية التكيف في الفروع والوسائل بما يحقق المقاصد الشرعية،
        دون المساس بثوابت الأصول.
        
        **إبراهيم هو الإمام في الحنيفية** لأنه جمع بين الثبات على الأصول (التوحيد، الولاء، البراءة) والمرونة في الوسائل
        (تنوع أساليب الدعوة، التدرج في التعامل مع الأب، بناء الكعبة مع دعاء للأمة).
        
        **ضوابطها:** ثبات الأصول، الالتزام بمقاصد الشريعة، أهلية الاجتهاد، عدم مخالفة الإجماع.
        
        **انحرافان عن الحنيفية:** الجمود (تقديس اجتهادات السلف وسد باب الاجتهاد)، والانحلال (التمرد على الثوابت وإسقاط النصوص).
        والسبيل الوسط هو الحنيفية.
        """,
        """
        ### 🔀 Al-Hanifiyyah – The Secret of Flexibility
        
        How do we apply this equation in a changing reality? The answer: **Hanifiyyah** – the property of dynamism in applying Islam.
        
        **Abraham is the Imam of Hanifiyyah**: combining firmness in principles with flexibility in means.
        
        **Two deviations:** Rigidity (freezing jurisprudence) and dissolution (rebelling against constants). The middle way is Hanifiyyah.
        """))

    # --- الفصل السابع: وحدة الخلق والأمر ---
    with st.expander(T("🌌 ٧. وحدة الخلق والأمر – التطابق بين الكتاب والكون", "🌌 7. Unity of Creation & Command"), expanded=False):
        st.markdown(T("""
        ### 🌌 وحدة الخلق والأمر – التطابق بين آيات الكتاب وآيات الكون
        
        هذا هو البرهان الأعظم: القانون الذي يحكم الذرة (الخلق) هو نفسه الذي شرعه الله للإنسان (الأمر).
        
        **في الفيزياء:** الجاذبية (W) والتنافر (B) يحفظان استقرار الذرة والمجرة. واختلال أحدهما يؤدي إلى الانهيار.
        **في الكيمياء:** التفاعل (W) والانفصال (B) يحكمان الذرات. والجزيء لا يتكون إلا بالتوازن بينهما.
        **في البيولوجيا:** جهاز المناعة يوالي الذات (W) ويهاجم اللاذات (B). واختلاله يسبب أمراض المناعة الذاتية أو السرطان.
        **في التاريخ:** الأمم تصعد بولائها للحق وبراءتها من الباطل، وتهوي باختلال أحد القطبين.
        
        > **﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ حَتَّىٰ يَتَبَيَّنَ لَهُمْ أَنَّهُ الْحَقُّ﴾**
        
        هذا المختبر هو تحقيق لهذا الوعد الإلهي: إراءة رقمية للآيات في الآفاق والأنفس.
        """,
        """
        ### 🌌 Unity of Creation & Command
        
        The law governing the atom is the same law legislated for humanity. One source, one law.
        
        This lab fulfills the divine promise: **﴿We will show them Our signs in the horizons and within themselves.﴾**
        """))

    # --- الفصل الثامن: الحديثان النبويان ---
    with st.expander(T("🕋 ٨. البرهان النبوي – الحديثان المؤسِّسان", "🕋 8. The Prophetic Proof"), expanded=False):
        st.markdown(T("""
        ### 🕋 البرهان النبوي – الحديثان المؤسِّسان
        
        **الحديث الأول:** «أَوْثَقُ عُرَى الْإِيمَانِ: الْحُبُّ فِي اللَّهِ، وَالْبُغْضُ فِي اللَّهِ»
        - الحب في الله = W. البغض في الله = B. أوثق عرى الإيمان = S.
        
        **الحديث الثاني:** «مَنْ أَحَبَّ لِلَّهِ، وَأَبْغَضَ لِلَّهِ، وَأَعْطَى لِلَّهِ، وَمَنَعَ لِلَّهِ، فَقَدِ اسْتَكْمَلَ الْإِيمَانَ»
        - استكمل الإيمان = S=1.
        
        **الواو هنا واو المعية (×) لا واو الجمع (+)**، لأن أوثق عرى الإيمان لا تتم إلا باجتماع الحب والبغض معًا.
        فمن أحب في الله ولم يبغض في الله، لم يستكمل الإيمان. ومن أبغض في الله ولم يحب في الله، لم يستكمل الإيمان.
        """,
        """
        ### 🕋 The Prophetic Proof
        
        Two hadiths proving S = W × B. The "and" is multiplication (×), not addition (+).
        Faith is only complete when both love and hatred for Allah are present.
        """))

    # --- خاتمة أصل النظرية ---
    st.markdown("---")
    st.markdown(T("""
    <div style="text-align:center;padding:30px;background:rgba(20,30,60,0.7);border-radius:15px;border:1px solid #FFD700;">
        <h3 style="color:#FFD700;">﴿سَنُرِيهِمْ آيَاتِنَا فِي الْآفَاقِ وَفِي أَنفُسِهِمْ حَتَّىٰ يَتَبَيَّنَ لَهُمْ أَنَّهُ الْحَقُّ﴾</h3>
        <p style="color:#FFD700;">﴿وَفِي الْأَرْضِ آيَاتٌ لِّلْمُوقِنِينَ • وَفِي أَنفُسِكُمْ ۚ أَفَلَا تُبْصِرُونَ﴾</p>
        <p style="color:#AAA;margin-top:15px;">هذا المختبر تحقيق متواضع لهذا الوعد الإلهي. فإن أصبنا فمن الله، وإن أخطأنا فمن أنفسنا.</p>
    </div>
    """, """
    <div style="text-align:center;padding:30px;background:rgba(20,30,60,0.7);border-radius:15px;border:1px solid #FFD700;">
        <h3 style="color:#FFD700;">﴿We will show them Our signs in the horizons and within themselves...﴾</h3>
        <p style="color:#AAA;margin-top:15px;">This lab is a humble fulfillment of this divine promise.</p>
    </div>
    """), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# تبويب ٢: الكون
# ═══════════════════════════════════════════════════════════════
with tabs[1]:
    st.header(T("🌌 المشهد الكوني – آيات الله في الآفاق", "🌌 The Cosmic Scene – Signs of Allah in the Horizons"))
    
    with st.expander(T("⚙️ المنزلقات السبعة", "⚙️ Seven Sliders"), expanded=True):
        cosmic_values = create_final_sliders("cosmic")
    
    with st.expander(T("🌳 شجرة الإيمان", "🌳 Faith Tree"), expanded=False):
        W_cur, B_cur = compute_WB_final(cosmic_values)
        render_faith_tree(cosmic_values, W_cur, B_cur)
    
    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        if st.button(T("▶️ تشغيل المشهد", "▶️ Run Scene"), key="btn_run_cosmic", use_container_width=True, type="primary"):
            st.session_state.run = True
    with col_btn2:
        if st.button(T("⏹️ إيقاف", "⏹️ Stop"), key="btn_stop_cosmic", use_container_width=True):
            st.session_state.run = False
    
    placeholder = st.empty()
    
    if st.session_state.get("run", False):
        W, B = compute_WB_final(cosmic_values)
        st.session_state.W = W; st.session_state.B = B
        
        while st.session_state.run:
            W = st.session_state.W; B = st.session_state.B; E = st.session_state.E
            S = st.session_state.S; phase = st.session_state.phase; ca = st.session_state.ca
            aW = st.session_state.aW; aB = st.session_state.aB
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx = st.session_state.cx; cy = st.session_state.cy; eb = st.session_state.eb
            hS = st.session_state.hS; hE = st.session_state.hE; hx = st.session_state.hx
            good = st.session_state.good; bad = st.session_state.bad
            pW = st.session_state.pW; pB = st.session_state.pB; frame = st.session_state.frame
            N = st.session_state.N

            ca += 0.008; sv = np.sin(ca)
            if sv > 0.5: phase = T('ذروة', 'Peak')
            elif sv > 0: phase = T('صعود', 'Rising')
            elif sv > -0.5: phase = T('انهيار', 'Collapse')
            else: phase = T('قاع', 'Bottom')
            if 0.3 < sv < 0.35: phase = T('>> استدراج <<', '>> Istidraj <<')
            target = 0.5 + 0.45 * sv

            for i in range(N):
                dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                nbr = np.where((dist < 2.0) & (np.arange(N) != i))[0]
                sw[i] += (target - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (target - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                if len(nbr) > 0:
                    sw[i] += (np.mean(sw[nbr]) - sw[i]) * 0.03
                    sb[i] += (np.mean(sb[nbr]) - sb[i]) * 0.03
                sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

            if random.random() < 0.005:
                aff = np.random.choice(N, size=int(N * 0.2), replace=False)
                sw[aff] *= random.uniform(0.5, 0.8); sb[aff] *= random.uniform(0.5, 0.8)

            W += (np.mean(sw) - W) * 0.04; B += (np.mean(sb) - B) * 0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            eb.append(S); past = list(eb)[-lag] if len(eb) >= lag else S
            E += 0.03 * (past - E)
            W = W - 0.015 * E + 0.03 / (S + 0.1) - 0.007 * (1 - B)
            B = B - 0.012 * E + 0.006 * (1 - B) * W * (1 - W)
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            pW.append(W); pB.append(B)
            frame += 1
            if frame % 2 == 0: hS.append(S); hE.append(E); hx.append(len(hx))

            aW += 0.02 + random.uniform(-0.02, 0.02) * (1 - W)**2
            aB += 0.02 + random.uniform(-0.02, 0.02) * (1 - B)**2
            wx = cx + (7 - 2.5 * W) * np.cos(aW); wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5 * B) * np.cos(aB); by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7

            instability = 1 - np.mean(sw * sb)
            sx += np.random.uniform(-0.07, 0.07, N) * instability
            sy += np.random.uniform(-0.07, 0.07, N) * instability
            sx = np.clip(sx, cx - 13, cx + 13); sy = np.clip(sy, cy - 9, cy + 9)

            good += W * 0.1; bad += (1 - B) * 0.1

            st.session_state.W = W; st.session_state.B = B; st.session_state.E = E; st.session_state.S = S
            st.session_state.phase = phase; st.session_state.ca = ca
            st.session_state.aW = aW; st.session_state.aB = aB; st.session_state.eb = eb
            st.session_state.sx = sx; st.session_state.sy = sy; st.session_state.sw = sw; st.session_state.sb = sb
            st.session_state.pW = pW; st.session_state.pB = pB
            st.session_state.hS = hS; st.session_state.hE = hE; st.session_state.hx = hx; st.session_state.frame = frame
            st.session_state.good = good; st.session_state.bad = bad

            fig, ax = plt.subplots(figsize=(16, 10), facecolor='#0a0f1e')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5, 0.98, '#FFF'), (1, 0.6, '#FFD700'), (1.8, 0.3, '#FFD700'), (2.8, 0.1, '#FFA500'), (4, 0.03, '#FF4500')]:
                ax.add_patch(Circle((cx, cy), r * (0.5 + 3 * S), color=c, alpha=a, zorder=15))
            ax.text(cx, cy, 'S', color='#000', fontsize=14, ha='center', va='center', fontweight='bold')
            ax.add_patch(Circle((cx, cy), 0.5 + 16 * E, color='#0FF', alpha=0.15, zorder=7))
            ax.add_patch(Circle((wx, wy), 0.2 + 0.6 * W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx, by), 0.2 + 0.6 * B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx, wy + 0.8, 'W', color='#FFF', fontsize=10, ha='center')
            ax.text(bx, by + 0.8, 'B', color='#F33', fontsize=10, ha='center')
            colors = [star_color(sw[i], sb[i]) for i in range(N)]
            ax.scatter(sx, sy, s=20, c=colors, alpha=0.9, edgecolors='white', linewidths=0.2, zorder=5)

            akh_x, akh_y, ms = 26.5, 18, 1.5
            ax.plot([akh_x, akh_x], [akh_y - 3, akh_y + 1.5], color='#FFD700', lw=1, alpha=0.4)
            ly = akh_y - 1.5 + ms * min(good / 50, 1.5); ry = akh_y - 1.5 - ms * min(bad / 50, 1.5)
            ax.add_patch(Circle((akh_x - 1, ly), 0.6, color='#FFD700', alpha=0.3, zorder=20))
            ax.text(akh_x - 1, ly - 1, T('حسنات', 'Good'), color='#FFD700', fontsize=5, ha='center')
            ax.add_patch(Circle((akh_x + 1, ry), 0.6, color='#FF4444', alpha=0.3, zorder=20))
            ax.text(akh_x + 1, ry - 1, T('سيئات', 'Bad'), color='#FF4444', fontsize=5, ha='center')
            diff = (bad - good) / 50 * ms
            ax.plot([akh_x - 1, akh_x + 1], [akh_y - diff, akh_y + diff], color='#FFD700', lw=1.5, alpha=0.6)

            pax = ax.inset_axes([0.5, 0.02, 0.46, 0.12])
            pax.set_xlim(0, 350); pax.set_ylim(0, 1.05)
            pax.set_title(T("S يقود E — الاستدراج", "S leads E — Istidraj"), color='white', fontsize=7)
            pax.tick_params(colors='white', labelsize=5); pax.grid(True, alpha=0.12)
            if hS: pax.plot(list(hx), list(hS), color='#FFD700', lw=2); pax.plot(list(hx), list(hE), color='#0FF', lw=1.5)

            ax.text(14, 1.2, f'{phase} | S={S:.2f} | E={E:.2f} | κ={curvature(pW, pB):.3f}', color='#CCC', fontsize=9, ha='center')
            plt.tight_layout(pad=0); placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.06)
    else:
        st.info(T("اضغط ▶️ تشغيل المشهد", "Press ▶️ Run Scene"))

    if not st.session_state.get("run", False) and len(st.session_state.hS) > 0:
        csv_data = "Time,S,E\n" + "\n".join([f"{i},{s:.4f},{e:.4f}" for i, (s, e) in enumerate(zip(st.session_state.hS, st.session_state.hE))])
        st.download_button(T("📥 تحميل البيانات", "📥 Download Data"), data=csv_data, file_name="mizan_cosmic.csv", mime="text/csv", key="dl_cosmic")

# ═══════════════════════════════════════════════════════════════
# تبويب ٣: الفرد – بوصلة الميزان الحية
# ═══════════════════════════════════════════════════════════════
with tabs[2]:
    st.header(T("🧍 مختبر الفرد – بوصلة الميزان الحية", "🧍 Individual Lab – The Living Mizan Compass"))
    st.markdown(T(
        "كل سؤال له **٤ إجابات**، تؤثر **كل واحدة منها على W و B معًا**. "
        "اختر بصدق، وستتحرك نقطتك فورًا بين الأرباع الأربعة. الأسئلة قابلة للطي.",
        "Each question has **4 answers**, **each affecting both W and B**. Choose honestly, and your point moves immediately."
    ))
    
    current_W = st.session_state.live_compass_W
    current_B = st.session_state.live_compass_B
    W_norm = (current_W + 1) / 2
    B_norm = (current_B + 1) / 2
    S_current = W_norm * B_norm
    q_name, q_color = classify(W_norm, B_norm)
    
    col_pos1, col_pos2, col_pos3, col_pos4 = st.columns(4)
    col_pos1.metric("W (الولاء)", f"{current_W:+.2f}")
    col_pos2.metric("B (البراءة)", f"{current_B:+.2f}")
    col_pos3.metric("S (الثبات)", f"{S_current:.3f}")
    col_pos4.markdown(f"<h3 style='color:{q_color};text-align:center;margin-top:15px;'>{q_name}</h3>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
    ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.2))
    ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF5252', alpha=0.2))
    ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.2))
    ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA500', alpha=0.2))
    ax.text(0.5, 0.5, "مؤمن", ha='center', color='#FFD700', fontsize=12, fontweight='bold')
    ax.text(-0.5, 0.5, "كافر", ha='center', color='#FF5252', fontsize=12, fontweight='bold')
    ax.text(-0.5, -0.5, "منافق", ha='center', color='#FFB6C1', fontsize=12, fontweight='bold')
    ax.text(0.5, -0.5, "مشرك", ha='center', color='#FFA500', fontsize=12, fontweight='bold')
    
    hist_W = st.session_state.live_compass_history_W
    hist_B = st.session_state.live_compass_history_B
    if len(hist_W) > 1:
        for i in range(1, len(hist_W)):
            alpha_val = 0.3 + 0.7 * (i / len(hist_W))
            ax.plot([hist_B[i-1], hist_B[i]], [hist_W[i-1], hist_W[i]], color='#00FFFF', lw=2, alpha=alpha_val)
        ax.scatter([hist_B[0]], [hist_W[0]], s=80, c='white', edgecolors='#00FFFF', linewidth=2, zorder=10)
    
    ax.scatter([current_B], [current_W], s=250, c=q_color, edgecolors='white', linewidth=3, zorder=15)
    ax.set_xlabel("B (البراءة)", color='white', fontsize=10)
    ax.set_ylabel("W (الولاء)", color='white', fontsize=10)
    ax.tick_params(colors='white')
    ax.set_title(T("رحلتك الحية في فضاء (W, B)", "Your Live Journey in (W, B) Space"), color='white', fontsize=13, fontweight='bold')
    ax.scatter([1.0], [1.0], s=100, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, marker='*')
    ax.text(1.0, 1.1, T("إبراهيم", "Abraham"), ha='center', color='#FFD700', fontsize=8)
    st.pyplot(fig)
    
    answered_count = st.session_state.live_compass_count
    progress_val = answered_count / 19
    st.markdown(f"""
    <div style="margin: 10px 0;">
        <p style="margin:0;color:#AAA;font-size:0.9em;">{T(f'الأسئلة المجاب عنها: {answered_count} / 19', f'Answered: {answered_count} / 19')}</p>
        <div style="background:rgba(255,255,255,0.1);border-radius:10px;height:12px;overflow:hidden;">
            <div style="width:{progress_val*100}%;height:100%;background:{q_color};border-radius:10px;transition:width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(T("### 📝 أجب عن الأسئلة – ستتحرك نقطتك فورًا", "### 📝 Answer – Your point moves immediately"))
    
    for i, q_data in enumerate(UNIFIED_QUESTIONS):
        q_key = f"Q{i+1}"
        if q_key in st.session_state.live_compass_answered:
            st.markdown(f"**{q_data['q']}** ✅ {st.session_state.live_compass_answered[q_key]}")
        else:
            with st.expander(q_data["q"], expanded=False):
                for ans_text, delta_W, delta_B in q_data["answers"]:
                    if st.button(f"→ {ans_text}", key=f"btn_{q_key}_{ans_text[:20]}", use_container_width=True):
                        st.session_state.live_compass_W += delta_W
                        st.session_state.live_compass_B += delta_B
                        st.session_state.live_compass_W = np.clip(st.session_state.live_compass_W, -1.0, 1.0)
                        st.session_state.live_compass_B = np.clip(st.session_state.live_compass_B, -1.0, 1.0)
                        st.session_state.live_compass_history_W.append(st.session_state.live_compass_W)
                        st.session_state.live_compass_history_B.append(st.session_state.live_compass_B)
                        short_ans = ans_text[:50] + "..." if len(ans_text) > 50 else ans_text
                        st.session_state.live_compass_answered[q_key] = short_ans
                        st.session_state.live_compass_count += 1
                        st.rerun()
    
    if st.session_state.live_compass_count == 19:
        st.divider()
        st.balloons()
        st.header(T("🎉 اكتملت رحلتك", "🎉 Your Journey is Complete"))
        
        final_W = st.session_state.live_compass_W
        final_B = st.session_state.live_compass_B
        W_norm_final = (final_W + 1) / 2
        B_norm_final = (final_B + 1) / 2
        S_final = W_norm_final * B_norm_final
        q_name_final, q_color_final = classify(W_norm_final, B_norm_final)
        
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;border:2px solid {q_color_final};text-align:center;margin:15px 0;'>
            <h2 style='color:{q_color_final};'>📍 {q_name_final}</h2>
            <p style='color:#CCC;'>W = {final_W:+.2f} | B = {final_B:+.2f}</p>
            <p style='color:#FFD700;font-size:1.3em;'>⚖️ S = W × B = {S_final:.3f}</p>
            <p style='color:#AAA;'>📏 المسافة إلى مقام إبراهيم: <b>{np.sqrt((1-W_norm_final)**2 + (1-B_norm_final)**2):.3f}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(T("🧠 تحليل مفصل من المستشار", "🧠 Detailed Analysis"), expanded=True):
            st.markdown(T("### 📊 تحليل نقاط القوة والضعف", "### 📊 Strengths & Weaknesses"))
            strengths = []
            weaknesses = []
            for i, q_data in enumerate(UNIFIED_QUESTIONS):
                q_key = f"Q{i+1}"
                selected_ans = st.session_state.live_compass_answered.get(q_key, "")
                for ans_text, delta_W, delta_B in q_data["answers"]:
                    short_ans = ans_text[:50] + "..." if len(ans_text) > 50 else ans_text
                    if short_ans == selected_ans:
                        if delta_W + delta_B >= 0.5: strengths.append(q_data["q"][:80])
                        elif delta_W + delta_B <= -0.5: weaknesses.append(q_data["q"][:80])
                        break
            if strengths:
                st.markdown(T("#### 🌟 نقاط قوتك", "#### 🌟 Your Strengths"))
                for s in strengths: st.markdown(f"- ✅ {s}")
            if weaknesses:
                st.markdown(T("#### ⚠️ مجالات للتحسين", "#### ⚠️ Areas for Improvement"))
                for w in weaknesses: st.markdown(f"- 🔧 {w}")
            if not strengths and not weaknesses:
                st.info(T("أنت في منطقة متوازنة. استمر في رحلتك نحو مقام إبراهيم عليه السلام.", "You are in a balanced zone. Continue toward the Station of Abraham."))
            st.markdown("---")
            st.markdown(T("**تذكر:** إبراهيم عليه السلام هو الأسوة الحسنة. كل خطوة تخطوها نحو (1,1) تقربك من مقامه. ﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ﴾", "**Remember:** Abraham is the excellent pattern. Every step toward (1,1) brings you closer to his station."))
        
        if st.button(T("🔄 أعد الرحلة", "🔄 Restart Journey"), key="btn_reset_compass", use_container_width=True):
            st.session_state.live_compass_W = 0.0
            st.session_state.live_compass_B = 0.0
            st.session_state.live_compass_history_W = [0.0]
            st.session_state.live_compass_history_B = [0.0]
            st.session_state.live_compass_answered = {}
            st.session_state.live_compass_count = 0
            st.rerun()

print("✅ المرحلة الثالثة مكتملة: أصل النظرية، الكون، الفرد.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الرابعة: الأمة المتكاملة، الحضارة، الشواهد
# ═══════════════════════════════════════════════════════════════

# --- تبويب ٤: الأمة المتكاملة ---
with tabs[3]:
    st.header(T("🏛️ مختبر الأمة المتكاملة – المجتمع والدولة في نسيج واحد", "🏛️ The Integrated Nation Lab – Society & State Woven Together"))
    st.markdown(T(
        "هذا المختبر يجمع **المجتمع والدولة والأمة** في محاكاة واحدة. "
        "ليس المجتمع بمعزل عن الحكم، ولا الدولة بمعزل عن القيم. الكل نسيج واحد، "
        "تحكمه المعادلة التي فطر الله عليها الوجود: **S = W × B**.",
        
        "This lab integrates **society, state, and nation** into one simulation. "
        "Society is not isolated from governance, nor is the state isolated from values. "
        "All are one fabric, governed by the equation upon which Allah created existence: **S = W × B**."
    ))
    
    with st.expander(T("⚙️ المنزلقات السبعة – أبعاد الحضارة", "⚙️ Seven Sliders – Dimensions of Civilization"), expanded=True):
        integrated_values = create_final_sliders("integrated")
    
    with st.expander(T("🌳 شجرة الإيمان – من الجذر إلى الثمرة", "🌳 Faith Tree – From Root to Fruit"), expanded=False):
        W_int_cur, B_int_cur = compute_WB_final(integrated_values)
        render_faith_tree(integrated_values, W_int_cur, B_int_cur)
    
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        pop_size = st.slider(T("عدد الأفراد (المجتمع)", "Population (Society)"), 50, 300, 150, 25, key="int_pop")
    with col_set2:
        sim_years = st.slider(T("سنوات المحاكاة", "Simulation Years"), 100, 500, 300, 25, key="int_years")
    with col_set3:
        influence_radius = st.slider(T("مدى التأثر بالجيران", "Neighbor Influence"), 0.5, 5.0, 2.0, 0.5, key="int_radius")
    
    if st.button(T("🚀 شغّل محاكاة الأمة المتكاملة", "🚀 Run Integrated Nation Simulation"), 
                key="btn_integrated", use_container_width=True, type="primary"):
        
        with st.spinner(T("المحاكاة المتكاملة تعمل...", "Integrated simulation running...")):
            W_base, B_base = compute_WB_final(integrated_values)
            
            pop = pop_size
            pW = np.random.uniform(W_base * 0.5, W_base * 1.2, pop)
            pB = np.random.uniform(B_base * 0.5, B_base * 1.2, pop)
            pW = np.clip(pW, 0.01, 1.0); pB = np.clip(pB, 0.01, 1.0)
            px = np.random.uniform(0, 30, pop); py = np.random.uniform(0, 30, pop)
            
            Y = sim_years
            W_nation = np.zeros(Y); B_nation = np.zeros(Y)
            S_nation = np.zeros(Y); E_nation = np.zeros(Y)
            believers_pct = np.zeros(Y)
            
            W_nation[0] = np.mean(pW); B_nation[0] = np.mean(pB)
            S_nation[0] = W_nation[0] * B_nation[0]; E_nation[0] = 0.1
            believers_pct[0] = np.sum((pW >= 0.5) & (pB >= 0.5)) / pop * 100
            
            for t in range(1, Y):
                nW = pW.copy(); nB = pB.copy()
                for i in range(pop):
                    dist = np.sqrt((px - px[i])**2 + (py - py[i])**2)
                    neighbors = np.where((dist < influence_radius) & (np.arange(pop) != i))[0]
                    if len(neighbors) > 0:
                        nW[i] += 0.03 * (np.mean(pW[neighbors]) - pW[i])
                        nB[i] += 0.03 * (np.mean(pB[neighbors]) - pB[i])
                    nW[i] += 0.02 * (W_base - pW[i]) - 0.008 * E_nation[t-1] * (1 - pB[i]) + 0.01 * (np.random.rand() - 0.5)
                    nB[i] += 0.02 * (B_base - pB[i]) - 0.006 * E_nation[t-1] * (1 - pW[i]) + 0.01 * (np.random.rand() - 0.5)
                    nW[i] = np.clip(nW[i], 0.01, 1.0); nB[i] = np.clip(nB[i], 0.01, 1.0)
                pW = nW; pB = nB
                px += np.random.randint(-1, 2, pop); py += np.random.randint(-1, 2, pop)
                px = np.clip(px, 0, 29); py = np.clip(py, 0, 29)
                
                W_nation[t] = np.mean(pW); B_nation[t] = np.mean(pB)
                S_nation[t] = W_nation[t] * B_nation[t]
                past_idx = max(0, t - lag)
                E_nation[t] = E_nation[t-1] + 0.03 * (S_nation[past_idx] - E_nation[t-1])
                E_nation[t] = np.clip(E_nation[t], 0.01, 1.0)
                believers_pct[t] = np.sum((pW >= 0.5) & (pB >= 0.5)) / pop * 100
            
            fig, axes = plt.subplots(2, 2, figsize=(18, 14), facecolor='#0a0f1e')
            
            ax1 = axes[0, 0]; ax1.set_facecolor('#0a0f1e')
            ax1.plot(S_nation, 'g-', lw=2.5, label='S (الثبات)')
            ax1.plot(E_nation, 'b--', lw=2.0, label='E (التمكين)')
            ax1.plot(W_nation, color='gold', lw=1.5, alpha=0.7, label='W')
            ax1.plot(B_nation, color='#FF5252', lw=1.5, alpha=0.7, label='B')
            idx_S_max = np.argmax(S_nation); idx_E_max = np.argmax(E_nation)
            if idx_S_max < idx_E_max:
                ax1.axvspan(idx_S_max, idx_E_max, alpha=0.2, color='red', label=T('فجوة الاستدراج', 'Istidraj Gap'))
            ax1.set_title(T("📈 دورة الأمة المتكاملة", "📈 Integrated Nation Cycle"), color='white', fontsize=14, fontweight='bold')
            ax1.set_xlabel(T("السنوات", "Years"), color='white'); ax1.set_ylabel(T("القيمة", "Value"), color='white')
            ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=9)
            ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white'); ax1.set_ylim(0, 1.05)
            
            ax2 = axes[0, 1]; ax2.set_facecolor('#0a0f1e')
            ax2.plot(B_nation, W_nation, 'w-', alpha=0.5, lw=1.2)
            ax2.scatter(B_nation[0], W_nation[0], s=150, c='green', edgecolors='white', linewidth=2, zorder=10, label=T('البداية', 'Start'))
            ax2.scatter(B_nation[-1], W_nation[-1], s=150, c='red', edgecolors='white', linewidth=2, zorder=10, label=T('النهاية', 'End'))
            ax2.axhline(0.5, color='grey', ls=':', lw=1); ax2.axvline(0.5, color='grey', ls=':', lw=1)
            ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
            ax2.set_xlabel('B', color='white'); ax2.set_ylabel('W', color='white')
            ax2.set_title(T("🗺️ مسار الأمة في فضاء (W, B)", "🗺️ Nation Path in (W, B)"), color='white', fontsize=14, fontweight='bold')
            ax2.fill_between([0.5, 1], 0.5, 1, alpha=0.1, color='green')
            ax2.fill_between([0, 0.5], 0.5, 1, alpha=0.1, color='orange')
            ax2.fill_between([0.5, 1], 0, 0.5, alpha=0.1, color='blue')
            ax2.fill_between([0, 0.5], 0, 0.5, alpha=0.1, color='red')
            ax2.text(0.75, 0.75, T("مؤمنة", "Believing"), color='green', fontsize=10, ha='center')
            ax2.text(0.25, 0.75, T("كافرة", "Disbelieving"), color='orange', fontsize=10, ha='center')
            ax2.text(0.25, 0.25, T("منافقة", "Hypocritical"), color='red', fontsize=10, ha='center')
            ax2.text(0.75, 0.25, T("مشركة", "Polytheistic"), color='blue', fontsize=10, ha='center')
            ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=9)
            ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
            
            ax3 = axes[1, 0]; ax3.set_facecolor('#0a0f1e')
            ax3.plot(believers_pct, color='#FFD700', lw=2, label=T('% المؤمنين', '% Believers'))
            ax3.set_xlabel(T("السنوات", "Years"), color='white'); ax3.set_ylabel('%', color='white')
            ax3.set_title(T("👥 صحة المجتمع – نسبة المؤمنين عبر الزمن", "👥 Society Health – Believers Percentage Over Time"), color='white', fontsize=14, fontweight='bold')
            ax3.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=9)
            ax3.grid(True, alpha=0.2); ax3.tick_params(colors='white'); ax3.set_ylim(0, 105)
            
            ax4 = axes[1, 1]; ax4.set_facecolor('#0a0f1e')
            gap = E_nation - S_nation
            ax4.fill_between(range(Y), 0, gap, where=(gap > 0), color='red', alpha=0.3, label=T('فجوة إيجابية (استدراج)', 'Positive Gap (Istidraj)'))
            ax4.fill_between(range(Y), 0, gap, where=(gap < 0), color='green', alpha=0.3, label=T('فجوة سلبية (تعافٍ)', 'Negative Gap (Recovery)'))
            ax4.axhline(y=0, color='white', lw=0.5)
            ax4.set_xlabel(T("السنوات", "Years"), color='white'); ax4.set_ylabel('E - S', color='white')
            ax4.set_title(T("⚠️ مؤشر الاستدراج (E - S) – متى يسبق التمكينُ الثباتَ؟", "⚠️ Istidraj Indicator (E - S) – When Does Empowerment Outrun Stability?"), color='white', fontsize=14, fontweight='bold')
            ax4.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=9)
            ax4.grid(True, alpha=0.2); ax4.tick_params(colors='white')
            
            plt.tight_layout(); st.pyplot(fig)
            
            st.divider(); st.subheader(T("📊 لوحة المؤشرات – حصاد الرحلة", "📊 Dashboard – Journey Harvest"))
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            c1.metric(T("W النهائي", "Final W"), f"{W_nation[-1]:.3f}")
            c2.metric(T("B النهائي", "Final B"), f"{B_nation[-1]:.3f}")
            c3.metric(T("S النهائي", "Final S"), f"{S_nation[-1]:.3f}")
            collapse_year = np.argmin(S_nation) if S_nation[np.argmin(S_nation)] < 0.2 else -1
            c4.metric(T("عام الانهيار", "Collapse Year"), f"{collapse_year}" if collapse_year >= 0 else T("مستقر", "Stable"))
            c5.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, np.argmax(E_nation) - np.argmax(S_nation))} {T('عام', 'yrs')}")
            c6.metric(T("% المؤمنين النهائي", "Final % Believers"), f"{believers_pct[-1]:.0f}%")
            
            csv_data = "Year,W,B,S,E,Believers%\n" + "\n".join(
                [f"{t},{W_nation[t]:.4f},{B_nation[t]:.4f},{S_nation[t]:.4f},{E_nation[t]:.4f},{believers_pct[t]:.1f}" for t in range(Y)])
            st.download_button(T("📥 تحميل بيانات المحاكاة", "📥 Download Data"), data=csv_data, file_name="mizan_integrated_nation.csv", mime="text/csv", key="dl_integrated")

# --- تبويب ٥: الحضارة – صراع القيم في ميدان الزمن ---
with tabs[4]:
    st.header(T("🏰 مختبر الحضارة – صراع القيم في ميدان الزمن", "🏰 Civilization Lab – The Clash of Values in the Arena of Time"))
    st.markdown(T(
        "قارن بين حضارتين تبدأ كل منهما بقيم مختلفة. شاهد كيف تزدهر الحضارة التي توازن بين W و B، "
        "وكيف تنهار التي تخل بهذا التوازن. البقاء للأصلح ميزانًا.",
        "Compare two civilizations starting with different values. Watch how the one that balances W and B flourishes, "
        "and how the one that disrupts this balance collapses. Survival is for the fittest in Mizan."
    ))
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"### 🟡 {T('الحضارة الأولى', 'Civilization A')}")
        civ_a_values = create_final_sliders("civ_a")
    with col_b:
        st.markdown(f"### 🔴 {T('الحضارة الثانية', 'Civilization B')}")
        civ_b_values = create_final_sliders("civ_b", defaults={k: -0.5 for k in ISLAMIC_SYSTEM_FINAL})
    
    if st.button(T("🚀 شغّل مقارنة الحضارات", "🚀 Run Civilization Comparison"), key="btn_civ", use_container_width=True, type="primary"):
        with st.spinner(T("المحاكاة تعمل...", "Simulation running...")):
            W_a, B_a = compute_WB_final(civ_a_values)
            W_b, B_b = compute_WB_final(civ_b_values)
            Y = 200
            Sh_a = np.zeros(Y); Eh_a = np.zeros(Y); Sh_b = np.zeros(Y); Eh_b = np.zeros(Y)
            Wh_a = np.zeros(Y); Bh_a = np.zeros(Y); Wh_b = np.zeros(Y); Bh_b = np.zeros(Y)
            Wh_a[0] = W_a * 0.8; Bh_a[0] = B_a * 0.8; Sh_a[0] = Wh_a[0] * Bh_a[0]; Eh_a[0] = 0.1
            Wh_b[0] = W_b * 0.8; Bh_b[0] = B_b * 0.8; Sh_b[0] = Wh_b[0] * Bh_b[0]; Eh_b[0] = 0.1
            for t in range(1, Y):
                Wh_a[t] = np.clip(Wh_a[t-1] + 0.02*(W_a - Wh_a[t-1]) - 0.01*Eh_a[t-1], 0.01, 1.0)
                Bh_a[t] = np.clip(Bh_a[t-1] + 0.02*(B_a - Bh_a[t-1]) - 0.008*Eh_a[t-1], 0.01, 1.0)
                Sh_a[t] = Wh_a[t] * Bh_a[t]; past_a = Sh_a[max(0, t-20)]
                Eh_a[t] = np.clip(Eh_a[t-1] + 0.04*(past_a - Eh_a[t-1]), 0.01, 1.0)
                Wh_b[t] = np.clip(Wh_b[t-1] + 0.02*(W_b - Wh_b[t-1]) - 0.01*Eh_b[t-1], 0.01, 1.0)
                Bh_b[t] = np.clip(Bh_b[t-1] + 0.02*(B_b - Bh_b[t-1]) - 0.008*Eh_b[t-1], 0.01, 1.0)
                Sh_b[t] = Wh_b[t] * Bh_b[t]; past_b = Sh_b[max(0, t-20)]
                Eh_b[t] = np.clip(Eh_b[t-1] + 0.04*(past_b - Eh_b[t-1]), 0.01, 1.0)
            
            fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
            ax1 = axes[0]; ax1.set_facecolor('#0a0f1e')
            ax1.plot(Sh_a, 'gold', lw=2, label=T('حضارة أ (S)', 'Civ A (S)'))
            ax1.plot(Eh_a, 'gold', lw=1.5, ls='--', alpha=0.6, label=T('حضارة أ (E)', 'Civ A (E)'))
            ax1.plot(Sh_b, '#FF5252', lw=2, label=T('حضارة ب (S)', 'Civ B (S)'))
            ax1.plot(Eh_b, '#FF5252', lw=1.5, ls='--', alpha=0.6, label=T('حضارة ب (E)', 'Civ B (E)'))
            ax1.set_title(T("مقارنة الحضارتين – دورة الحياة", "Civilization Comparison – Life Cycle"), color='white', fontsize=13)
            ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
            ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white'); ax1.set_ylim(0, 1.05)
            
            ax2 = axes[1]; ax2.set_facecolor('#0a0f1e')
            ax2.plot(Bh_a, Wh_a, 'gold', lw=1.5, alpha=0.7, label=T('حضارة أ', 'Civ A'))
            ax2.plot(Bh_b, Wh_b, '#FF5252', lw=1.5, alpha=0.7, label=T('حضارة ب', 'Civ B'))
            ax2.scatter(Bh_a[0], Wh_a[0], s=80, c='gold', edgecolors='white', linewidth=2, zorder=10)
            ax2.scatter(Bh_b[0], Wh_b[0], s=80, c='#FF5252', edgecolors='white', linewidth=2, zorder=10)
            ax2.axhline(0.5, color='grey', ls=':', lw=1); ax2.axvline(0.5, color='grey', ls=':', lw=1)
            ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
            ax2.set_xlabel('B', color='white'); ax2.set_ylabel('W', color='white')
            ax2.set_title(T("المسار في فضاء (W, B) – أين تذهب كل حضارة؟", "Path in (W, B) Space – Where Does Each Civilization Go?"), color='white', fontsize=13)
            ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
            ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
            plt.tight_layout(); st.pyplot(fig)
            
            c1, c2 = st.columns(2)
            c1.metric(T("S النهائي - حضارة أ", "Final S - Civ A"), f"{Sh_a[-1]:.3f}")
            c2.metric(T("S النهائي - حضارة ب", "Final S - Civ B"), f"{Sh_b[-1]:.3f}")
            
            csv_data = "Year,S_A,E_A,S_B,E_B\n" + "\n".join([f"{t},{Sh_a[t]:.4f},{Eh_a[t]:.4f},{Sh_b[t]:.4f},{Eh_b[t]:.4f}" for t in range(Y)])
            st.download_button(T("📥 تحميل بيانات المقارنة", "📥 Download Comparison"), data=csv_data, file_name="mizan_civilizations.csv", mime="text/csv", key="dl_civ")

# --- تبويب ٦: الشواهد التاريخية – حين ينطق التاريخ مصدقًا ---
with tabs[5]:
    st.header(T("📜 الشواهد التاريخية – حين ينطق التاريخ مصدقًا للمعادلة", "📜 Historical Evidence – When History Bears Witness"))
    st.markdown(T(
        "اختر دولة تاريخية لترى كيف تنطبق معادلة الميزان على التاريخ الفعلي. "
        "هذه تقديرات تقريبية، والهدف منها أن تريك كيف أن سنة الله في الأمم لا تتبدل ولا تتحول.",
        "Select a historical nation to see how the Mizan equation applies to actual history. "
        "These are approximate estimates, meant to show you that Allah's law in nations does not change or transform."
    ))
    
    selected_nation = st.selectbox(T("اختر دولة:", "Select a nation:"), list(HISTORICAL_DATA.keys()))
    
    if selected_nation:
        data = HISTORICAL_DATA[selected_nation]
        W_hist, B_hist, E_hist = data["W"], data["B"], data["E"]
        S_hist = W_hist * B_hist
        
        st.markdown(f"**{selected_nation}**"); st.markdown(data["desc"])
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("W", f"{W_hist:.2f}"); c2.metric("B", f"{B_hist:.2f}")
        c3.metric("S", f"{S_hist:.2f}"); c4.metric("E", f"{E_hist:.2f}")
        
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0a0f1e'); ax.set_facecolor('#0a0f1e')
        categories = ['W (الولاء)', 'B (البراءة)', 'S (الثبات)', 'E (التمكين)']
        values = [W_hist, B_hist, S_hist, E_hist]
        colors_bar = ['gold', '#FF5252', '#0F8', '#0FF']
        ax.bar(categories, values, color=colors_bar, edgecolor='white', linewidth=1.5)
        if E_hist > S_hist * 1.3:
            ax.annotate(T('فجوة الاستدراج', 'Istidraj Gap'), xy=(3, E_hist), xytext=(3.5, E_hist+0.1),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2), color='red', fontsize=10, fontweight='bold')
        ax.set_ylim(0, 1.1); ax.set_title(T("مؤشرات الدولة التاريخية", "Historical Nation Indicators"), color='white', fontsize=13)
        ax.tick_params(colors='white'); ax.grid(True, alpha=0.2); st.pyplot(fig)
        
        if E_hist > S_hist * 1.5:
            st.warning(T("⚠️ حالة استدراج واضحة: التمكين المادي يفوق الثبات الأخلاقي بكثير. الانهيار قادم لا محالة.", "⚠️ Clear Istidraj: material empowerment far exceeds moral stability. Collapse is inevitable."))
        elif S_hist > 0.7:
            st.success(T("✅ حالة توازن عالٍ: W و B متوازنتان، والتمكين يتبع الثبات بشكل صحي.", "✅ High balance: W and B are balanced, and empowerment follows stability healthily."))
        else:
            st.info(T("ℹ️ حالة متوسطة إلى منخفضة. هناك مؤشرات على بداية تراجع تحتاج إلى إصلاح.", "ℹ️ Moderate to low state. Signs of decline that need reform."))

print("✅ المرحلة الرابعة مكتملة: الأمة المتكاملة، الحضارة، الشواهد التاريخية.")

# ═══════════════════════════════════════════════════════════════
# المرحلة الخامسة: الصراط (البرهان النبوي + النموذج الإبراهيمي) والتذييل
# ═══════════════════════════════════════════════════════════════

# --- الثوابت الإبراهيمية ---
ABRAHAMIC_VERSE = T(
    '﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ وَالَّذِينَ مَعَهُ إِذْ قَالُوا لِقَوْمِهِمْ إِنَّا بُرَآءُ مِنكُمْ وَمِمَّا تَعْبُدُونَ مِن دُونِ اللَّهِ كَفَرْنَا بِكُمْ وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾',
    '﴿There has certainly been for you an excellent pattern in Abraham and those with him, when they said to their people, "Indeed, we are disassociated from you and from whatever you worship other than Allah. We have denied you, and there has appeared between us and you animosity and hatred forever until you believe in Allah alone."﴾'
)

def get_spiritual_nudge(situation):
    """توليد رسالة تحفيز روحي مبنية على الوحيين، بأسلوب يجمع بين الحكمة والتواضع."""
    if situation == "approaching":
        return T(
            f'🌟 لقد اقتربتَ من مقام إبراهيم عليه السلام!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'تأمل كيف جمع إبراهيم بين **الولاء لله** (W) و**البراءة من الطاغوت** (B) في آنٍ واحد. '
            f'هذا هو سر الأسوة الحسنة. هذا هو الثبات الكامل (S=1).\n\n'
            f'**سؤال للتأمل:** هل في حياتك "براءة" واضحة مما يعبد من دون الله؟ '
            f'أم أنك تجمع بين الولاء لله وولاءات أخرى؟ تذكر أن القلب لا يجتمع فيه ولاءان.',
            
            f'🌟 You are approaching the Station of Abraham!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'Reflect on how Abraham combined **loyalty to Allah** (W) and **disavowal of Taghut** (B) simultaneously. '
            f'This is the secret of the excellent pattern. This is complete stability (S=1).\n\n'
            f'**A question for reflection:** Is there clear "disavowal" in your life from what is worshipped besides Allah? '
            f'Or do you combine loyalty to Allah with other loyalties? Remember, a heart cannot contain two loyalties.'
        )
    elif situation == "progressing":
        return T(
            f'🚶 أنت في طريقك إلى مقام إبراهيم.\n\n'
            f'لاحظ كلمة **"أَبَدًا"** في الآية: ﴿وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾\n\n'
            f'البراءة من الطاغوت ليست مؤقتة، وليست مرحلة عابرة. إنها موقف دائم حتى يتحقق الإيمان. '
            f'والولاء لله **"وَحْدَهُ"**: لا شريك له في الولاء، ولا ندّ له في المحبة.\n\n'
            f'**سؤال للمراجعة:** هل هناك شيء تعطيه من ولائك لغير الله؟ راجع قلبك.',
            
            f'🚶 You are on your way to the Station of Abraham.\n\n'
            f'Note the word **"forever"**: animosity and hatred forever, until you believe in Allah alone.\n\n'
            f'Disavowal of Taghut is not temporary. Loyalty is to Allah **alone**.\n\n'
            f'**Review question:** Is there anything to which you give loyalty other than Allah? Examine your heart.'
        )
    elif situation == "sin":
        return T(
            f'⚠️ لقد ابتعدتَ عن الصراط قليلاً. لكن إبراهيم يعلمك كيف تعود.\n\n'
            f'﴿إِنَّا بُرَآءُ مِنكُمْ﴾ — أعلنها صريحة كما أعلنها إبراهيم. '
            f'جدد براءتك. جدد ولاءك. التوبة هي العودة إلى الأسوة الحسنة.\n\n'
            f'**خطوة عملية:** استحضر في قلبك الآن معنى "لا إله إلا الله". '
            f'انفِ كل طاغوت، وأثبتِ الله وحده. فهذا هو الطريق الوحيد للعودة إلى الصراط.',
            
            f'⚠️ You have strayed from the path. But Abraham teaches you how to return.\n\n'
            f'Declare it clearly as Abraham did: "We are disassociated from you." '
            f'Renew your disavowal. Renew your loyalty. Repentance is returning to the excellent pattern.\n\n'
            f'**Practical step:** Bring to your heart now the meaning of "There is no god but Allah." '
            f'Negate every false deity, and affirm Allah alone.'
        )
    elif situation == "repentance":
        return T(
            f'🕋 لقد تبتَ وعدتَ إلى الصراط!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'إبراهيم نفسه كان بشرًا. لم يكن ملكًا. لكنه **اختار** أن يكون في مقام (1,1). '
            f'وأنت أيضًا تختار. وكل مرة تختار فيها الله، تقترب من هذا المقام.\n\n'
            f'**﴿إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ وَيُحِبُّ الْمُتَطَهِّرِينَ﴾**\n'
            f'عدتَ إلى الطريق. فاثبت حتى تلقى الله.',
            
            f'🕋 You have repented and returned to the path!\n\n'
            f'{ABRAHAMIC_VERSE}\n\n'
            f'Abraham himself was human. But he **chose** to be at the Station of (1,1). '
            f'You too choose. And every time you choose Allah, you draw closer to this station.\n\n'
            f'**﴿Indeed, Allah loves those who are constantly repentant and loves those who purify themselves.﴾**\n'
            f'You have returned to the path. Now remain steadfast until you meet Allah.'
        )
    else:
        return ""

# ═══════════════════════════════════════════════════════════════
# تبويب ٧: الصراط – البرهان النبوي والنموذج الإبراهيمي
# ═══════════════════════════════════════════════════════════════
with tabs[6]:
    st.header(T("📐 هندسة الصراط – البرهان النبوي والنموذج الإبراهيمي", "📐 Path Geometry – Prophetic Proof & Abrahamic Model"))
    
    # --- البرهان النبوي – الحديثان المؤسِّسان ---
    st.markdown(T("""
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:25px;border:2px solid #FFD700;margin:20px 0;text-align:center;">
        <h3 style="color:#FFD700;margin-top:0;">🕋 {title}</h3>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;direction:rtl;">
            «أَوْثَقُ عُرَى الْإِيمَانِ: الْحُبُّ فِي اللَّهِ، وَالْبُغْضُ فِي اللَّهِ»
        </p>
        <p style="color:#AAA;font-size:0.85em;">رواه الإمام أحمد وأبو داود والطبراني، وصححه الألباني</p>
        <p style="color:#FFD700;font-size:1.2em;margin:15px 0;">⬇️</p>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;direction:rtl;">
            «مَنْ أَحَبَّ لِلَّهِ، وَأَبْغَضَ لِلَّهِ، وَأَعْطَى لِلَّهِ، وَمَنَعَ لِلَّهِ، فَقَدِ اسْتَكْمَلَ الْإِيمَانَ»
        </p>
        <p style="color:#AAA;font-size:0.85em;">رواه أبو داود، وصححه الألباني</p>
        <hr style="border-color:rgba(255,215,0,0.3);margin:20px 0;">
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W × B</p>
        <p style="color:#AAA;">
            الحب في الله = W (الولاء). البغض في الله = B (البراءة).<br>
            أوثق عرى الإيمان = S (الثبات). استكمل الإيمان = S=1.<br>
            الواو هنا واو المعية (×) لا واو الجمع (+)، لأن الإيمان لا يكتمل إلا باجتماعهما معًا.
        </p>
    </div>
    """,
    """
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:25px;border:2px solid #FFD700;margin:20px 0;text-align:center;">
        <h3 style="color:#FFD700;margin-top:0;">🕋 The Prophetic Proof</h3>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;">
            "The firmest handhold of faith is: love for the sake of Allah, and hatred for the sake of Allah."
        </p>
        <p style="color:#AAA;font-size:0.85em;">Narrated by Ahmad, Abu Dawud, At-Tabarani; authenticated by Al-Albani</p>
        <p style="color:#FFD700;font-size:1.2em;margin:15px 0;">⬇️</p>
        <p style="color:#CCC;font-size:1.1em;line-height:2.2;">
            "Whoever loves for the sake of Allah, hates for the sake of Allah, gives for the sake of Allah, and withholds for the sake of Allah, has completed faith."
        </p>
        <p style="color:#AAA;font-size:0.85em;">Narrated by Abu Dawud; authenticated by Al-Albani</p>
        <hr style="border-color:rgba(255,215,0,0.3);margin:20px 0;">
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W × B</p>
        <p style="color:#AAA;">
            Love for Allah = W. Hatred for Allah = B.<br>
            The firmest handhold = S. Completed faith = S=1.<br>
            The "and" is multiplication (×), because faith is only complete with both together.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # --- شرح النموذج الإبراهيمي ---
    st.markdown(T("""
    ### 🕋 النموذج الإبراهيمي: الجيوديسي المثالي
    
    إبراهيم عليه السلام هو "أبو الأنبياء" و"خليل الله". مساره في فضاء (W, B) هو **الجيوديسي المثالي**:
    الخط المستقيم الذي انحناؤه صفر (κ = 0). إنه أقصر طريق بين الفطرة ورضا الله.
    
    **لماذا إبراهيم؟** لأنه حقق الكمال في القطبين معًا:
    - **W = 1**: ﴿أَسْلَمْتُ لِرَبِّ الْعَالَمِينَ﴾
    - **B = 1**: ﴿إِنَّنِي بَرَاءٌ مِّمَّا تَعْبُدُونَ﴾
    - **S = 1**: ﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ﴾
    
    **الخط الذهبي** في الرسم البياني هو مسار إبراهيم. وكل إنسان مدعو لاتباع هذا المسار.
    وكل خطوة تخطوها نحو (1,1) تقربك من مقامه.
    """,
    """
    ### 🕋 The Abrahamic Model: The Ideal Geodesic
    
    Abraham (AS) is the "Father of Prophets" and the "Friend of Allah". His path in (W, B) space is the **ideal geodesic**:
    the straight line with zero curvature (κ = 0). It is the shortest path between fitrah and Allah's pleasure.
    
    **Why Abraham?** Because he achieved perfection in both poles:
    - **W = 1**, **B = 1**, **S = 1**.
    
    **The golden line** is Abraham's path. Every human is invited to follow it.
    Every step toward (1,1) brings you closer to his station.
    """))
    
    st.markdown("---")
    
    # --- أزرار التفاعل ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button(T("▶️ خطوة نحو الكمال", "▶️ Step Toward Perfection"), key="btn_path", use_container_width=True):
            levels = ["faith","worship","transactions","morals","enjoining","hudud","jihad"]
            chosen = random.choice(levels)
            current = getattr(st.session_state, f"path_{chosen}")[-1]
            new_val = min(1.0, current + 0.1)
            for l in levels:
                if l == chosen:
                    getattr(st.session_state, f"path_{l}").append(new_val)
                else:
                    getattr(st.session_state, f"path_{l}").append(getattr(st.session_state, f"path_{l}")[-1])
            final_vals = {l: getattr(st.session_state, f"path_{l}")[-1] for l in levels}
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            
            dist = np.sqrt((1 - W_new)**2 + (1 - B_new)**2)
            if dist < 0.3:
                st.session_state.spiritual_nudge = get_spiritual_nudge("approaching")
            elif dist < 0.5:
                st.session_state.spiritual_nudge = get_spiritual_nudge("progressing")
            else:
                st.session_state.spiritual_nudge = None
            
            st.rerun()
    
    with c2:
        sin_str = st.slider(T("⚡ شدة المعصية", "⚡ Sin Strength"), 0.01, 0.3, 0.1, 0.01, key="sin_path")
        if st.button(T("⚠️ معصية", "⚠️ Sin"), key="btn_sin", use_container_width=True):
            levels = ["faith","worship","transactions","morals","enjoining","hudud","jihad"]
            chosen = random.choice(levels)
            current = getattr(st.session_state, f"path_{chosen}")[-1]
            new_val = max(-1.0, current - sin_str * random.uniform(0.5, 1.0))
            for l in levels:
                if l == chosen:
                    getattr(st.session_state, f"path_{l}").append(new_val)
                else:
                    getattr(st.session_state, f"path_{l}").append(getattr(st.session_state, f"path_{l}")[-1])
            final_vals = {l: getattr(st.session_state, f"path_{l}")[-1] for l in levels}
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            
            st.session_state.spiritual_nudge = get_spiritual_nudge("sin")
            st.rerun()
    
    with c3:
        if st.button(T("🕌 توبة نصوح", "🕌 Sincere Repentance"), key="btn_rep", use_container_width=True):
            for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
                current = getattr(st.session_state, f"path_{l}")[-1]
                new_val = min(1.0, current + 0.8 * (1.0 - current))
                getattr(st.session_state, f"path_{l}").append(new_val)
            final_vals = {l: getattr(st.session_state, f"path_{l}")[-1] for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]}
            W_new, B_new = compute_WB_final(final_vals)
            st.session_state.path_W.append(W_new); st.session_state.path_B.append(B_new)
            st.session_state.path_kappa.append(0.0)
            
            st.session_state.spiritual_nudge = get_spiritual_nudge("repentance")
            st.rerun()
    
    # --- عرض رسالة التحفيز الروحي ---
    if hasattr(st.session_state, 'spiritual_nudge') and st.session_state.spiritual_nudge:
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.9);border-radius:12px;padding:20px;border:1px solid #FFD700;margin:15px 0;text-align:center;line-height:2.2;'>
            <p style='color:#FFD700;font-size:1.1em;margin:0;white-space:pre-line;'>{st.session_state.spiritual_nudge}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- زر إعادة ---
    if st.button(T("🔄 إعادة الرحلة", "🔄 Reset Path"), key="btn_reset_path", use_container_width=True):
        for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
            setattr(st.session_state, f"path_{l}", [0.0])
        st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
        st.session_state.path_kappa = [0.0]
        st.session_state.spiritual_nudge = None
        st.rerun()
    
    # --- رسم المسار ---
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
    
    ax1 = axes[0]
    ax1.set_facecolor('#0a0f1e')
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_xlabel("B (البراءة)", color='white'); ax1.set_ylabel("W (الولاء)", color='white')
    ax1.set_title(T("مسارك في فضاء (W, B) – النموذج الإبراهيمي", "Your Path in (W, B) Space – The Abrahamic Model"), color='white', fontsize=13)
    
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=3, alpha=0.8, 
             label=T("✦ مسار إبراهيم عليه السلام (الجيوديسي: κ = 0)", "✦ Abraham's Path (Geodesic: κ = 0)"))
    ax1.scatter([1], [1], s=200, c='#FFD700', edgecolors='white', linewidth=3, zorder=10, 
                label=T("⭐ مقام إبراهيم (الكمال: 1,1)", "⭐ Station of Abraham (Perfection: 1,1)"))
    
    pW = st.session_state.path_W; pB = st.session_state.path_B
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.path_kappa[i] if i < len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2 if kv < 0.05 else 3)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label=T("البداية", "Start"))
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label=T("الآن", "Now"))
    
    ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
    
    ax2 = axes[1]
    ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.path_kappa, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label=T("حد الخطر", "Danger"))
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label=T("الصراط – مسار إبراهيم", "Straight – Abraham's Path"))
    ax2.set_title(T("منحنى الانحناء (κ) – تاريخ انحرافاتك", "Curvature Over Time – Your Deviation History"), color='white', fontsize=13)
    ax2.set_xlabel(T("الخطوات", "Steps"), color='white'); ax2.set_ylabel("κ", color='white')
    ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
    max_kappa = max(st.session_state.path_kappa) if st.session_state.path_kappa else 0.1
    ax2.set_ylim(-0.01, max(0.2, max_kappa * 1.2))
    
    plt.tight_layout(); st.pyplot(fig)
    
    # --- مؤشرات المستويات ---
    st.divider()
    st.subheader(T("📊 المستويات الحية", "📊 Live Levels"))
    
    cols = st.columns(7)
    levels_labels = [
        ("faith", T("الإيمان", "Faith"), '#FFD700'),
        ("worship", T("العبادات", "Worship"), '#FFA500'),
        ("transactions", T("المعاملات", "Transactions"), '#00FF88'),
        ("morals", T("الأخلاق", "Morals"), '#FF69B4'),
        ("enjoining", T("الأمر والنهي", "Enjoining"), '#00BFFF'),
        ("hudud", T("الحدود", "Limits"), '#FF6347'),
        ("jihad", T("الجهاد", "Jihad"), '#FF4500'),
    ]
    
    for i, (key, label, color) in enumerate(levels_labels):
        val = getattr(st.session_state, f"path_{key}")[-1]
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:6px;background:rgba(20,30,60,0.8);border-radius:6px;border:1px solid {color};">
                <p style="color:{color};font-size:0.6em;margin:0;">{label}</p>
                <p style="color:white;font-size:0.9em;margin:0;font-weight:bold;">{val:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # --- مؤشرات المسار ---
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("W (الولاء)", f"{pW[-1]:.3f}")
    c2.metric("B (البراءة)", f"{pB[-1]:.3f}")
    current_kappa = st.session_state.path_kappa[-1] if st.session_state.path_kappa else 0.0
    c3.metric("κ (الانحناء)", f"{current_kappa:.4f}")
    on_path = current_kappa < 0.03
    c4.metric(T("الصراط؟", "On Path?"), T("✅ نعم", "✅ YES") if on_path else T("⚠️ لا", "⚠️ NO"))
    
    # --- المسافة إلى مقام إبراهيم ---
    st.divider()
    dist_to_abraham = np.sqrt((1 - pW[-1])**2 + (1 - pB[-1])**2)
    st.markdown(f"""
    <div style='text-align:center;padding:15px;background:rgba(20,30,60,0.8);border-radius:10px;border:1px solid #FFD700;'>
        <p style='color:#FFD700;font-size:1em;margin:0;'>
            {T(f'📏 المسافة إلى مقام إبراهيم (الكمال): {dist_to_abraham:.3f}', f'📏 Distance to Station of Abraham (Perfection): {dist_to_abraham:.3f}')}
        </p>
        <p style='color:#AAA;font-size:0.8em;margin:5px 0 0 0;'>
            {T('﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ﴾ [الممتحنة: ٤]', '﴿There has certainly been for you an excellent pattern in Abraham.﴾ [Al-Mumtahanah: 4]')}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🏁 التذييل – ختام المسك
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.5em;">⚖️ مختبر الميزان</p>
    <p style="font-size:1.1em;">{T('سفينة نوح الرقمية – القانون الواحد من الذرة إلى الحضارة', 'The Digital Ark – The One Law from Atom to Civilization')}</p>
    <p style="color:#FFD700;font-size:1.3em;">S = W × B</p>
    <p>ق = ١٠٠ = الحق = الميزان</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size:0.8em;margin-top:15px;">
        {T(
            'هذا المختبر ليس إلا محاولة متواضعة لفهم سنة من سنن الله في خلقه. '
            'إن أصبنا فمن الله، وإن أخطأنا فمن أنفسنا. '
            'والحمد لله الذي هدانا لهذا وما كنا لنهتدي لولا أن هدانا الله.',
            'This lab is but a humble attempt to understand one of Allah\'s laws in His creation. '
            'If we are right, it is from Allah; if we are wrong, it is from ourselves. '
            'And praise be to Allah who guided us to this, for we would not have been guided had Allah not guided us.'
        )}
    </p>
    <p style="color:#FFD700;font-size:1.2em;margin-top:15px;">﴿وَقُلِ الْحَمْدُ لِلَّهِ سَيُرِيكُمْ آيَاتِهِ فَتَعْرِفُونَهَا﴾</p>
</div>
""", unsafe_allow_html=True)

print("✅ المرحلة الخامسة والأخيرة مكتملة.")
print("✅✅✅ تم بناء مختبر الميزان – سفينة نوح الرقمية – النسخة النهائية المتكاملة.")
