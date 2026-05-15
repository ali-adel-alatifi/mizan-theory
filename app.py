import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
from io import BytesIO
import json
import warnings
warnings.filterwarnings('ignore')

# =============================================
# إعدادات الصفحة
# =============================================
st.set_page_config(page_title="⚖️ الدين القيم – المنارة العالمية", page_icon="⚖️", layout="wide")

# =============================================
# اللغة
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

# =============================================
# الأنماط CSS
# =============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri+Quran&display=swap');
.stApp { background: linear-gradient(180deg, #0a0f1e 0%, #0d1528 30%, #0f1a2e 100%); }
h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #FFD700; }
p, label, div { font-family: 'Cairo', sans-serif; color: #E0E0E0; }
.golden-title { font-size: 3.2em; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; }
.verse-text { text-align: center; color: #FFD700; font-size: 1.3em; margin: 15px 0; line-height: 2; }
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; width: 100%; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; }
.message-box { background: rgba(20,30,60,0.7); border-radius: 15px; padding: 30px; margin: 20px 0; border: 1px solid rgba(255,215,0,0.3); line-height: 2.2; }
</style>
""", unsafe_allow_html=True)

# =============================================
# الثوابت الوجودية – المعجم الهندسي
# =============================================
LETTERS_DB = {
    'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60,
    'ح': 8, 'ط': 9, 'ق': 100, 'ك': 20, 'ص': 90,
    'ع': 70, 'ي': 10, 'هـ': 5, 'ن': 50, 'ف': 80,
    'و': 6, 'ب': 2, 'ظ': 900, 'ض': 800, 'غ': 1000,
    'ذ': 700, 'خ': 600, 'ش': 300, 'ز': 7, 'ج': 3,
    'ت': 400, 'ث': 500
}

# =============================================
# المؤشرات الأخلاقية الأساسية
# =============================================
INDICATORS_META = [
    {"ar": "الصلاة (إقامة/تضييع)", "en": "Prayer", "letter": "ن", "val": 50},
    {"ar": "الزكاة والصدقات (إيتاء/منع)", "en": "Zakat & Charity", "letter": "ص", "val": 90},
    {"ar": "الولاء لله ورسوله والمؤمنين", "en": "Loyalty to Allah & Believers", "letter": "أ", "val": 1},
    {"ar": "تحكيم الشريعة (تحكيم/رفض)", "en": "Applying Sharia", "letter": "ل", "val": 30},
    {"ar": "العدل (عدل/ظلم)", "en": "Justice", "letter": "ق", "val": 100},
    {"ar": "الشورى (تشاور/استبداد)", "en": "Consultation", "letter": "م", "val": 40},
    {"ar": "البراءة من الطاغوت (براءة/موالاة)", "en": "Disavowal of Taghut", "letter": "هـ", "val": 5},
    {"ar": "الرحمة والعطاء (رحمة/قسوة)", "en": "Mercy & Giving", "letter": "ح", "val": 8},
    {"ar": "الأمر بالمعروف (أمر/نهي)", "en": "Enjoining Good", "letter": "ف", "val": 80},
    {"ar": "النهي عن المنكر (نهي/أمر)", "en": "Forbidding Evil", "letter": "و", "val": 6},
    {"ar": "النزاهة ومكافحة الفساد", "en": "Integrity & Anti-Corruption", "letter": "ب", "val": 2},
]
N_IND = len(INDICATORS_META)

def get_indicator_label(i):
    meta = INDICATORS_META[i]
    name = meta["ar"] if L == "ar" else meta["en"]
    return f"{name}  [{meta['letter']}={meta['val']}]"

# =============================================
# المحكمة العليا
# =============================================
def supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal):
    if not W_pure:
        return (0, T("بوابة الشرك","Shirk Gate"), T("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾","⚠️ Unforgivable"), "🔴")
    if B_compassion <= 0:
        return (-1, T("بوابة الماعون","Al-Ma'un Gate"), T("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ...﴾","⚠️ Collapse"), "🔴")
    if W_raw > 0 and B_disavowal <= 0:
        return (0, T("بوابة الإخلاص","Sincerity Gate"), T("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي...﴾","⚠️ Void"), "🟡")
    if W_raw > 0 and B_raw > 0:
        return (1, T("بوابة الوعد","Promise Gate"), T("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾","🟢 Stability"), "🟢")
    return None, None, None, None

def calculate_S(W_raw, B_raw, E_raw, W_pure, B_compassion, B_disavowal):
    S_gate, gate_name, gate_msg, gate_color = supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal)
    if S_gate is not None:
        return S_gate, 0, gate_name, gate_msg, gate_color, 0
    W = (W_raw + 1) / 2; B = (B_raw + 1) / 2; E = (E_raw + 1) / 2
    W_boost = 1 + (LETTERS_DB['أ'] + LETTERS_DB['ر'] + LETTERS_DB['س'] + LETTERS_DB['ط']) / 1000
    B_boost = 1 + (LETTERS_DB['ل'] + LETTERS_DB['ح'] + LETTERS_DB['ط']) / 1000
    S_raw = (W * W_boost) * (B * B_boost) * (1 + LETTERS_DB['م'] / 1000)
    istidraj_gap = max(0, E - S_raw)
    return min(1.0, S_raw), E, T("المعادلة العامة","General"), "", "⚪", istidraj_gap

def simulate_future(S, E, W_raw, B_raw, years=50):
    Sh, Eh = [S], [E]
    for _ in range(years):
        nE = Eh[-1] + 0.02 * (Sh[-1] - Eh[-1]); nB = B_raw
        if nE > Sh[-1] + 0.2: nB -= 0.03
        elif nE < Sh[-1]: nB += 0.01
        Sh.append(((W_raw+1)/2) * ((nB+1)/2) * (1 + sum(LETTERS_DB.values())/1000))
        Eh.append(nE)
    return Sh, Eh

def plot_quadrant_map(B_raw, W_raw, istidraj_gap):
    fig, ax = plt.subplots(figsize=(6,6), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e'); ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
    ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
    ax.set_xlabel(T("B (الكفر بالطاغوت)","B (Disavowal)"), color='white')
    ax.set_ylabel(T("W (الإيمان بالله)","W (Faith)"), color='white')
    ax.fill_between([0,1.2],0,1.2,color='#FFD700',alpha=0.3,label=T('المؤمنون','Believers'))
    ax.fill_between([-1.2,0],0,1.2,color='#FF5252',alpha=0.2,label=T('المغضوب عليهم','Wrath'))
    ax.fill_between([-1.2,0],-1.2,0,color='#FFB6C1',alpha=0.2,label=T('المنافقون','Hypocrites'))
    ax.fill_between([0,1.2],-1.2,0,color='#FFA500',alpha=0.2,label=T('الضالون','Astray'))
    ax.scatter(B_raw,W_raw,s=300,c='cyan',edgecolors='white',linewidth=2,zorder=10)
    ax.scatter(1,1,s=100,c='#FFD700',edgecolors='white',linewidth=2,zorder=10,marker='*')
    ax.text(1,1.15,T('مقام إبراهيم','Abraham'),color='#FFD700',fontsize=8,ha='center')
    if istidraj_gap>0: ax.text(0.5,-0.9,T(f"فجوة:{istidraj_gap:.2f}",f"Gap:{istidraj_gap:.2f}"),color='red',fontsize=9,ha='center',fontweight='bold')
    ax.legend(facecolor='#0a0f1e',edgecolor='white',labelcolor='white',fontsize=7,loc='lower left')
    ax.tick_params(colors='white')
    return fig

# =============================================
# قاعدة بيانات البوصلة الكاملة (19 سؤالاً)
# =============================================
COMPASS_DATA = [
    {"id":1,"topic":T("القوانين الوضعية وتحكيم الشريعة","Man-Made Laws vs. Sharia"),"letter":"ق","value":100,
     "text":T("في زمن سيادة القوانين الوضعية... ما هو موقفك من تحكيم شرع الله؟","In an age of man-made laws..."),
     "answers":[(T("أجاهد لتطبيق شرع الله","I strive to apply Sharia"),0.4,0.6),(T("أتمنى لكن لا أعمل","I wish but don't act"),0.2,-0.1),(T("بعضها صالح والآخر لا","Some valid, some not"),-0.1,-0.2),(T("الشريعة لا تصلح للعصر","Sharia unsuitable"),-0.3,-0.4)]},
    {"id":2,"topic":T("الولاء للعرق والحزب والطائفة","Loyalty to Race, Party, Sect"),"letter":"أ","value":1,
     "text":T("في عصر الولاء للعرق... ما هو موقفك؟","In an age of loyalty to race..."),
     "answers":[(T("ولائي لله فوق كل رابطة","My loyalty is to Allah"),0.7,0.3),(T("أوازن بين الدين والعرق","I balance"),0.3,-0.2),(T("ولائي لديني ضعيف","Weak religious loyalty"),-0.2,0.1),(T("العرق أهم من الدين","Race over religion"),-0.5,-0.3)]},
    {"id":3,"topic":T("الاستهزاء بالمقدسات وحرية التعبير","Mockery of Sanctities & Free Speech"),"letter":"هـ","value":5,
     "text":T("في زمن حرية التعبير... ما موقفك من الاستهزاء بالدين؟","In an age of free speech..."),
     "answers":[(T("أبغض المستهزئين وأدينهم","I hate and condemn mockers"),0.3,0.7),(T("أستنكر بقلبي","I disapprove in heart"),0.1,-0.1),(T("حرية رأي ولا داعي للغضب","Free speech, no anger"),-0.2,0.1),(T("أضحك معهم أحياناً","I laugh with them"),-0.3,-0.3)]},
    {"id":4,"topic":T("الربا والنظام المالي العالمي","Usury and Global Finance"),"letter":"ص","value":90,
     "text":T("في زمن النظام المالي الربوي... ما موقفك؟","In an age of usurious finance..."),
     "answers":[(T("أتجنب الربا وأبحث عن بدائل","I avoid usury and seek alternatives"),0.3,0.7),(T("أكرهه لكني مضطر","I hate it but am forced"),0.1,-0.2),(T("أتعامل به كالجميع","I deal with it like everyone"),-0.2,0.1),(T("الربا ضرورة اقتصادية","Usury is a necessity"),-0.3,-0.3)]},
    {"id":5,"topic":T("العلمانية وفصل الدين عن الدولة","Secularism & Separation"),"letter":"ك","value":20,
     "text":T("في زمن العلمانية... ما موقفك من فصل الدين عن الدولة؟","In an age of secularism..."),
     "answers":[(T("أرفض العلمانية والدين لله","I reject secularism"),0.4,0.6),(T("حل مؤقت لحين الاستعداد","Temporary solution"),0.1,-0.1),(T("لا أمانع الفصل","I don't mind separation"),-0.2,0.1),(T("العلمانية هي الصحيح","Secularism is correct"),-0.3,-0.3)]},
    {"id":6,"topic":T("إقامة الحدود الشرعية","Establishing Sharia Penalties"),"letter":"ح","value":8,
     "text":T("في زمن إلغاء الحدود... ما موقفك؟","In an age of abolishing penalties..."),
     "answers":[(T("الحدود رحمة وعدل","Penalties are mercy and justice"),0.3,0.7),(T("الحدود حق لكن الظروف صعبة","Right but conditions hard"),0.1,-0.1),(T("أشعر بالحرج منها","I feel embarrassed"),-0.2,0.1),(T("الحدود همجية","Penalties are barbaric"),-0.3,-0.3)]},
    {"id":7,"topic":T("الإلحاد وإنكار الخالق","Atheism & Denying the Creator"),"letter":"ن","value":50,
     "text":T("في زمن الإلحاد... ما موقفك؟","In an age of atheism..."),
     "answers":[(T("أؤمن بالله يقيناً","I believe in Allah certainly"),0.4,0.6),(T("أؤمن لكني لا أملك حججاً","I believe but lack arguments"),0.1,-0.1),(T("تساورني شكوك أحياناً","Doubts sometimes cross my mind"),-0.2,0.1),(T("الإلحاد فكر يحترم","Atheism is respectable"),-0.3,-0.3)]},
    {"id":8,"topic":T("الجهاد ونصرة المستضعفين","Jihad & Supporting the Oppressed"),"letter":"ر","value":200,
     "text":T("في زمن تشويه الجهاد... ما موقفك؟","In an age of distorting jihad..."),
     "answers":[(T("الجهاد ذروة سنام الإسلام","Jihad is the peak of Islam"),0.3,0.7),(T("الجهاد حق وأدعمه بقلبي","Jihad is right, I support"),0.1,-0.1),(T("أخشى من الجهاد","I fear jihad"),-0.2,0.1),(T("الجهاد أصبح إرهاباً","Jihad became terrorism"),-0.3,-0.3)]},
    {"id":9,"topic":T("حقوق المرأة بين الإسلام والتغريب","Women's Rights: Islam vs. West"),"letter":"هـ","value":5,
     "text":T("في زمن طرح حقوق المرأة... ما موقفك؟","In an age of women's rights..."),
     "answers":[(T("الإسلام كرم المرأة","Islam honored women"),0.4,0.6),(T("أؤمن لكن نحتاج تحديثاً","I believe but need update"),0.1,-0.1),(T("أشعر بالحرج من بعض الأحكام","Embarrassed by some rulings"),-0.2,0.1),(T("الإسلام ظلم المرأة","Islam oppressed women"),-0.3,-0.3)]},
    {"id":10,"topic":T("العولمة والذوبان الحضاري","Globalization & Dissolution"),"letter":"م","value":40,
     "text":T("في زمن العولمة... ما موقفك؟","In an age of globalization..."),
     "answers":[(T("أتمسك بهويتي الإسلامية","I hold fast to my Islamic identity"),0.4,0.6),(T("أوازن بين الهوية والعصر","I balance identity and modernity"),0.1,-0.1),(T("أقلد الغرب في ثقافته","I imitate Western culture"),-0.2,0.1),(T("الثقافة الغربية هي التقدم","Western culture is progress"),-0.3,-0.3)]},
    {"id":11,"topic":T("الديمقراطية والتشريع","Democracy & Legislation"),"letter":"ل","value":30,
     "text":T("في زمن تقديس الديمقراطية... ما موقفك؟","In an age of sanctifying democracy..."),
     "answers":[(T("التشريع لله والشورى طاعة","Legislation for Allah, Shura obedience"),0.4,0.6),(T("الديمقراطية وسيلة","Democracy is a tool"),0.1,-0.1),(T("أفضلها على الاستبداد","I prefer it over dictatorship"),-0.2,0.1),(T("الديمقراطية أفضل نظام","Democracy is the best"),-0.3,-0.3)]},
    {"id":12,"topic":T("التعددية الدينية","Religious Pluralism"),"letter":"ي","value":10,
     "text":T("في زمن التعددية... ما موقفك؟","In an age of pluralism..."),
     "answers":[(T("الإسلام هو الدين الوحيد المقبول","Islam is the only accepted religion"),0.4,0.6),(T("الإسلام حق لكن لا أحكم","Islam is truth but I don't judge"),0.1,-0.1),(T("كل الأديان فيها حق","All religions have truth"),-0.2,0.1),(T("كل الأديان سواء","All religions are equal"),-0.3,-0.3)]},
    {"id":13,"topic":T("الحب في الله والبغض في الله","Love & Hatred for Allah"),"letter":"ق","value":100,
     "text":T("في زمن المصالح... ما موقفك من الحب والبغض في الله؟","In an age of interests..."),
     "answers":[(T("أحب في الله وأبغض في الله","I love and hate for Allah"),0.4,0.6),(T("أحاول لكن المصالح تغلب","I try but interests dominate"),0.1,-0.1),(T("أتعامل بالمثل","I deal equally with all"),-0.2,0.1),(T("علاقاتي بالمصالح فقط","My relationships are interests only"),-0.3,-0.3)]},
    {"id":14,"topic":T("التحلي بالأخلاق الحميدة","Embodying Noble Character"),"letter":"ط","value":9,
     "text":T("في زمن الكذب والغش... ما موقفك من الصدق والأمانة؟","In an age of lying and fraud..."),
     "answers":[(T("الصدق والأمانة دين","Truthfulness is my religion"),0.4,0.6),(T("أحاول لكني قد أضطر","I try but may be forced"),0.1,-0.1),(T("المبالغة في الصدق سذاجة","Excessive honesty is naivety"),-0.2,0.1),(T("الكذب والغش أدوات نجاح","Lying and fraud are success tools"),-0.3,-0.3)]},
    {"id":15,"topic":T("الغيرة على المحارم والأمر بالمعروف","Protective Jealousy & Enjoining Good"),"letter":"ب","value":2,
     "text":T("في زمن انتشار الفواحش... ما موقفك من الأمر والنهي؟","In an age of indecency..."),
     "answers":[(T("آمر وأنهى بكل استطاعتي","I enjoin and forbid as much as I can"),0.3,0.7),(T("أنكر بقلبي أحياناً","I reject in my heart sometimes"),0.1,-0.1),(T("أسكت حفاظاً على مصالحي","I remain silent for my interests"),-0.2,0.1),(T("لا داعي للأمر والنهي","No need for enjoining/forbidding"),-0.3,-0.3)]},
    {"id":16,"topic":T("الوطنية والحزبية والمذهبية","Patriotism, Partisanship, Sectarianism"),"letter":"ف","value":80,
     "text":T("في زمن تقديس الوطنية والحزبية... ما موقفك؟","In an age of sanctifying patriotism..."),
     "answers":[(T("ولائي للإسلام فوق الكل","My loyalty to Islam above all"),0.4,0.6),(T("أحب وطني وأقدم الإسلام","I love my country but prioritize Islam"),0.1,-0.1),(T("انتمائي لوطني أهم","My national belonging is more important"),-0.2,0.1),(T("لا مشكلة في القومية","No problem with nationalism"),-0.3,-0.3)]},
    {"id":17,"topic":T("الصلاة في زمن الانشغال","Prayer in an Age of Busyness"),"letter":"ن","value":50,
     "text":T("في زمن الانشغال... ما موقفك من الصلاة؟","In an age of busyness..."),
     "answers":[(T("الصلاة راحتي ولا أتركها","Prayer is my comfort, I never leave it"),0.4,0.6),(T("أصلي لكني أؤخرها أحياناً","I pray but sometimes delay"),0.1,-0.1),(T("أصلي أحياناً وأترك أحياناً","I pray sometimes and leave sometimes"),-0.2,0.1),(T("لا أجد وقتاً للصلاة","I find no time for prayer"),-0.3,-0.3)]},
    {"id":18,"topic":T("الصوم في زمن الشهوات","Fasting in an Age of Desires"),"letter":"ط","value":9,
     "text":T("في زمن الشهوات... ما موقفك من الصوم؟","In an age of desires..."),
     "answers":[(T("أصوم الفرض والنفل","I fast obligatory and voluntary"),0.4,0.6),(T("أصوم الفرض فقط","I fast only obligatory"),0.1,-0.1),(T("أصوم رمضان كعادة","I fast Ramadan as a habit"),-0.2,0.1),(T("لا أصوم","I don't fast"),-0.3,-0.3)]},
    {"id":19,"topic":T("الزكاة والصدقة في زمن الأنانية","Zakat & Charity in an Age of Selfishness"),"letter":"ط","value":9,
     "text":T("في زمن الأنانية... ما موقفك من الزكاة والصدقة؟","In an age of selfishness..."),
     "answers":[(T("أؤدي الزكاة طيبة بها نفسي","I pay Zakat willingly"),0.4,0.6),(T("أؤدي الزكاة فقط","I pay only Zakat"),0.1,-0.1),(T("أخرج الزكاة بخلاً","I pay Zakat grudgingly"),-0.2,0.1),(T("لا أزكي","I don't pay Zakat"),-0.3,-0.3)]},
]

def compute_compass(answers_dict):
    w_raw, b_raw = 0.0, 0.0
    total_weight = sum(q['value'] for q in COMPASS_DATA)
    for q in COMPASS_DATA:
        key = f"q_{q['id']}"
        ans_idx = answers_dict.get(key, 0)
        if ans_idx < len(q['answers']):
            delta_w, delta_b = q['answers'][ans_idx][1], q['answers'][ans_idx][2]
            weight = q['value'] / 100.0
            w_raw += delta_w * weight
            b_raw += delta_b * weight
    w_raw = max(-1.0, min(1.0, w_raw))
    b_raw = max(-1.0, min(1.0, b_raw))
    return w_raw, b_raw, ((w_raw + 1) / 2) * ((b_raw + 1) / 2)

# =============================================
# التهيئة العامة للجلسة
# =============================================
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
    st.session_state.hS = deque(maxlen=300); st.session_state.hE = deque(maxlen=300)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0; st.session_state.frame = 0
    st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]; st.session_state.path_kappa = [0.0]
    st.session_state.compass_answers = {}
    st.session_state.slider_values = {f"V{i}": 0.0 for i in range(N_IND)}
    st.session_state.slider_values["W_pure"] = True
    st.session_state.slider_values["E_val"] = 0.5
    st.session_state.init = True

print("✅ المرحلة الأولى مكتملة: الأساسيات، الثوابت، الدوال، البوصلة الكاملة")

# =============================================
# المرحلة الثانية: الواجهة الرئيسية والتبويبات الأولى
# =============================================

# --- الشريط الجانبي ---
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:8px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <p style='font-size:2em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:0;'>{T('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h2>
        <p style='color:#e0e0e0;font-size:10px;margin:2px 0;'>{T('المنارة العالمية', 'The Global Beacon')}</p>
        <p style='color:#FFD700;font-size:14px;margin:2px 0;font-weight:bold;'>S = W x B</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(T("🇬🇧 English", "🇸🇦 العربية"), use_container_width=True):
        st.session_state.lang = "en" if L == "ar" else "ar"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown(f"### {T('⚙️ إعدادات عامة', '⚙️ General Settings')}")
    lag = st.select_slider(
        T("فجوة الاستدراج", "Istidraj Gap"),
        options=[5, 10, 15, 22, 30, 40, 50],
        value=22, key="lag"
    )
    
    st.markdown("---")
    
    # --- الميزان الأخروي الحي ---
    good = st.session_state.get('good', 0)
    bad = st.session_state.get('bad', 0)
    balance = good - bad
    if balance > 0:
        status, color = T("⚖️ راجحة", "⚖️ Winning"), '#FFD700'
    elif balance < 0:
        status, color = T("⚖️ خاسرة", "⚖️ Losing"), '#FF4444'
    else:
        status, color = T("⚖️ متوازنة", "⚖️ Balanced"), '#888'
    st.sidebar.markdown(f"""
    <div style="text-align:center;padding:10px;background:rgba(10,15,30,0.9);border-radius:10px;border:1px solid #FFD700;margin-top:10px;">
        <p style="color:#FFD700;font-size:0.8em;margin:0;">📜 {T('الميزان الحي', 'Live Scales')}</p>
        <p style="color:#FFD700;font-size:0.7em;margin:2px 0;">{T('حسنات', 'Good')}: {good:.0f} | {T('سيئات', 'Bad')}: {bad:.0f}</p>
        <p style="color:{color};font-size:0.9em;margin:0;font-weight:bold;">{status}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button(T("🔄 إعادة ضبط كل شيء", "🔄 Full Reset"), key="btn_reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

# --- رسالة الترحيب ---
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
    <p style="text-align:center;color:#FFD700;font-size:1.2em;font-weight:bold;">S = W x B</p>
    <p>{T(
    'W: الولاء لله وأوليائه. B: البراءة من الطاغوت وأوليائه. S: الثبات الوجودي.',
    'W: Loyalty to Allah & His allies. B: Disavowal of Taghut & its allies. S: Existential Stability.'
    )}</p>
    <p style="text-align:center;font-style:italic;color:#AAA;">{T(
    'جرب. تأمل. واسأل. الباب مفتوح.',
    'Try. Reflect. Ask. The door is open.'
    )}</p>
    </div>
    """, unsafe_allow_html=True)

# --- دليل المستخدم ---
with st.expander(T("📖 دليل المستخدم", "📖 User Guide"), expanded=False):
    st.markdown(T("""
    ### 🎯 كيف تستخدم هذا المختبر؟
    
    **١. بوصلة الإسلام الحنيف:** أجب عن ١٩ سؤالاً لتعرف موقعك الدقيق في فضاء القيم. كل سؤال له ٤ إجابات تؤثر على القطبين (W و B) معًا.
    
    **٢. مختبر الأمة المتكاملة:** استخدم المنزلقات أو الذكاء الاصطناعي لملء القيم، وشاهد المحاكاة الحية.
    
    **٣. المشهد الكوني الحي:** شاهد تفاعل النجوم (الأفراد) مع قطبي الميزان في الزمن الحقيقي.
    
    **٤. المعجم الهندسي:** تعرف على الحروف العربية وقيمها العددية ودورها الوجودي في المعادلة.
    
    **٥. الشواهد التاريخية:** قارن بين الدول التاريخية لترى كيف تنطبق المعادلة على التاريخ الفعلي.
    
    **٦. هندسة الصراط:** تتبع مسارك نحو مقام إبراهيم عليه السلام.
    
    **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
    """,
    """
    ### 🎯 How to Use This Lab
    
    **1. Compass:** Answer 19 questions to discover your precise position.
    
    **2. Nation Lab:** Use sliders or AI to fill values and watch the live simulation.
    
    **3. Cosmic Scene:** Watch stars interact with the Mizan poles in real-time.
    
    **4. Lexicon:** Explore Arabic letters and their numerical values.
    
    **5. Evidence:** Compare historical nations to see the equation in action.
    
    **6. Path Geometry:** Track your path toward Abraham's Station.
    
    **Central Equation:** **S = W x B** (multiplication, not addition).
    """))

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
    <br><span style='font-size:0.8em;'>S = W x B | ق = ١٠٠ = الحق = الميزان</span>
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    T("🧍 بوصلة الإسلام الحنيف", "🧍 Compass"),
    T("🏛️ مختبر الأمة", "🏛️ Nation Lab"),
    T("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    T("📖 المعجم الهندسي", "📖 Lexicon"),
    T("📜 الشواهد", "📜 Evidence"),
    T("📐 هندسة الصراط", "📐 Path")
])

# =============================================
# تبويب ١: بوصلة الإسلام الحنيف
# =============================================
with tab1:
    st.header(T("🧍 بوصلة الإسلام الحنيف – اكتشف موقعك بدقة", "🧍 Compass – Discover Your Precise Position"))
    
    # إعدادات البوصلة
    col_set1, col_set2 = st.columns([3, 1])
    with col_set1:
        st.markdown(T("أجب عن الأسئلة الـ 19. كل إجابة تؤثر على W و B معًا. المعادلة: S = W x B", "Answer the 19 questions. Each answer affects both W and B."))
    with col_set2:
        use_ai = st.checkbox(T("🤖 استخدام الذكاء الاصطناعي", "🤖 Use AI"))
    
    if use_ai:
        st.info(T("اكتب وصفًا لحالتك ليقوم الذكاء الاصطناعي بتقدير إجاباتك.", "Describe your condition for AI to estimate."))
        ai_text = st.text_area(T("الوصف:", "Description:"), height=100, key="ai_compass")
        if st.button(T("تحليل بالذكاء الاصطناعي", "Analyze with AI"), key="btn_ai_compass"):
            with st.spinner(T("جاري التحليل...", "Analyzing...")):
                try:
                    import openai
                    openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
                    if openai.api_key:
                        questions_desc = "\n".join([f"{q['id']}. {q['topic']}" for q in COMPASS_DATA])
                        prompt = f"""You are an expert in the Mizan theory. Analyze this person and return JSON with answers (0-3, representing the choice index for each of the 19 questions).
Questions:
{questions_desc}
Return ONLY valid JSON with format: {{"answers": [0, 2, 1, ...]}} (19 values, each 0-3).
Description: {ai_text}"""
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role":"system","content":"Return ONLY valid JSON."}, {"role":"user","content":prompt}],
                            temperature=0.3, max_tokens=400
                        )
                        content = response.choices[0].message.content.strip()
                        if content.startswith("```"): content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
                        ai_result = json.loads(content)
                        for i, val in enumerate(ai_result.get("answers", [])[:19]):
                            st.session_state.compass_answers[f"q_{i+1}"] = val
                        st.success(T("✅ تم التحليل!", "✅ Analysis complete!"))
                        st.rerun()
                    else:
                        st.error(T("يرجى إضافة مفتاح OpenAI API", "Please add OpenAI API key"))
                except Exception as e:
                    st.error(f"AI Error: {e}")
    
    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}
    
    for q in COMPASS_DATA:
        with st.expander(f"**{q['id']}. {q['topic']}**  [{q['letter']}={q['value']}]"):
            st.markdown(f"*{q['text']}*")
            key = f"q_{q['id']}"
            ans = st.radio(
                T("اختر:", "Choose:"),
                [a[0] for a in q['answers']],
                key=key, index=None
            )
            if ans is not None:
                idx = [a[0] for a in q['answers']].index(ans)
                st.session_state.compass_answers[key] = idx
    
    if len(st.session_state.compass_answers) == 19:
        W_raw, B_raw, S_score = compute_compass(st.session_state.compass_answers)
        
        if W_raw >= 0.5 and B_raw >= 0.5:
            q_name, q_color = T("مؤمن", "Believer"), '#FFD700'
        elif W_raw < 0.5 and B_raw >= 0.5:
            q_name, q_color = T("كافر", "Disbeliever"), '#FF5252'
        elif W_raw < 0.5 and B_raw < 0.5:
            q_name, q_color = T("منافق", "Hypocrite"), '#FFB6C1'
        else:
            q_name, q_color = T("مشرك", "Polytheist"), '#FFA500'
        
        st.divider()
        st.subheader(T("📊 موقعك", "📊 Your Position"))
        c1, c2, c3 = st.columns(3)
        c1.metric("W (الولاء)", f"{W_raw:+.2f}")
        c2.metric("B (البراءة)", f"{B_raw:+.2f}")
        c3.metric("S (الثبات)", f"{S_score:.2f}")
        st.markdown(f"<h2 style='color:{q_color};text-align:center;'>{q_name}</h2>", unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(5,5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.fill_between([0,1.2], 0, 1.2, color='#FFD700', alpha=0.3)
        ax.fill_between([-1.2,0], 0, 1.2, color='#FF5252', alpha=0.2)
        ax.fill_between([-1.2,0], -1.2, 0, color='#FFB6C1', alpha=0.2)
        ax.fill_between([0,1.2], -1.2, 0, color='#FFA500', alpha=0.2)
        ax.scatter(B_raw, W_raw, s=200, c='cyan', edgecolors='white', linewidth=2, zorder=10)
        ax.scatter(1, 1, s=80, c='#FFD700', marker='*', zorder=10)
        ax.text(1, 1.1, T('إبراهيم', 'Abraham'), color='#FFD700', fontsize=7, ha='center')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        if st.button(T("🔄 إعادة", "🔄 Retake"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

print("✅ المرحلة الثانية مكتملة: الواجهة، رسالة الترحيب، دليل المستخدم، الشريط الجانبي، البوصلة")

# =============================================
# المرحلة الثالثة: مختبر الأمة والمشهد الكوني
# =============================================

# =============================================
# تبويب ٢: مختبر الأمة المتكامل
# =============================================
with tab2:
    st.header(T("🏛️ مختبر الأمة – المنزلقات والذكاء الاصطناعي", "🏛️ Nation Lab – Sliders & AI"))
    
    # --- إعدادات المنزلقات ---
    with st.expander(T("🎛️ مؤشرات الطاقة الروحية", "🎛️ Spiritual Energy Indicators"), expanded=True):
        st.caption(T(
            "كل حركة وسكنة مولد طاقة نحو الولاية والبراءة. [الحرف=القيمة]",
            "Every movement generates energy. [Letter=Value]"
        ))
        
        slider_vals = []
        for i in range(0, N_IND, 2):
            col_a, col_b = st.columns(2)
            with col_a:
                if i < N_IND:
                    val = st.slider(get_indicator_label(i), -1.0, 1.0,
                                   st.session_state.slider_values.get(f"V{i}", 0.0), 0.1,
                                   key=f"lab_V{i}")
                    slider_vals.append(val)
                    st.session_state.slider_values[f"V{i}"] = val
            with col_b:
                if i + 1 < N_IND:
                    val = st.slider(get_indicator_label(i+1), -1.0, 1.0,
                                   st.session_state.slider_values.get(f"V{i+1}", 0.0), 0.1,
                                   key=f"lab_V{i+1}")
                    slider_vals.append(val)
                    st.session_state.slider_values[f"V{i+1}"] = val
        
        st.markdown("---")
        col_pure, col_E = st.columns(2)
        with col_pure:
            W_pure = st.checkbox(
                T("الإخلاص لله (عدم الشرك) [أ=1]", "Sincerity [A=1]"),
                value=st.session_state.slider_values.get("W_pure", True)
            )
            st.session_state.slider_values["W_pure"] = W_pure
        with col_E:
            E_val = st.slider(
                T("التمكين (E) [ق=100]", "Empowerment [Q=100]"),
                0.0, 1.0, st.session_state.slider_values.get("E_val", 0.5), 0.05, key="lab_E"
            )
            st.session_state.slider_values["E_val"] = E_val
    
    # --- الذكاء الاصطناعي الفائق ---
    st.markdown("---")
    st.subheader(T("🤖 مساعد الذكاء الاصطناعي", "🤖 AI Assistant"))
    st.markdown(T(
        "اكتب وصفًا لأي دولة أو مجتمع أو فرد، وسيقوم الذكاء الاصطناعي بتحليله وملء المنزلقات تلقائيًا. المعادلة هي الحكم.",
        "Describe any nation, community, or individual, and AI will analyze it and fill the sliders automatically. The equation is the judge."
    ))
    
    ai_text = st.text_area(
        T("الوصف النصي:", "Description:"),
        height=100,
        placeholder=T("مثال: دولة إسلامية ذات أغلبية شابة، تعاني من فساد إداري لكنها تملك جيشًا قويًا واقتصادًا زراعيًا...",
                     "Example: An Islamic country with a young majority, suffering from corruption but with a strong military...")
    )
    
    if st.button(T("تحليل بالذكاء الاصطناعي وملء المنزلقات", "Analyze with AI & Fill Sliders"), type="primary", use_container_width=True):
        if not ai_text.strip():
            st.warning(T("يرجى إدخال وصف نصي أولاً.", "Please enter a description first."))
        else:
            with st.spinner(T("جاري التحليل بالذكاء الاصطناعي...", "Analyzing with AI...")):
                try:
                    import openai
                    openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
                    if not openai.api_key:
                        st.error(T("يرجى إضافة مفتاح OpenAI API", "Please add OpenAI API key"))
                    else:
                        indicators_desc = "\n".join([f"{i+1}. {get_indicator_label(i)}" for i in range(N_IND)])
                        prompt = f"""You are an expert in the Mizan theory. Analyze the entity described below and return numerical estimates in JSON format only.
Indicators (each between -1 and +1):
{indicators_desc}
Also include:
- W_pure: true or false
- E_val: value between 0 and 1
- analysis: brief analysis in Arabic
Return ONLY valid JSON. Example: {{"values": [0.5, 0.4, 0.7, 0.3, 0.6, 0.2, 0.6, 0.5, 0.4, 0.3, 0.4], "W_pure": true, "E_val": 0.6, "analysis": "تحليل موجز"}}
Description: {ai_text}"""
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role":"system","content":"Return ONLY valid JSON."}, {"role":"user","content":prompt}],
                            temperature=0.3, max_tokens=500
                        )
                        content = response.choices[0].message.content.strip()
                        if content.startswith("```"): content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
                        ai_result = json.loads(content)
                        
                        vals = ai_result.get("values", [0.0] * N_IND)[:N_IND]
                        for i in range(N_IND):
                            st.session_state.slider_values[f"V{i}"] = vals[i]
                        st.session_state.slider_values["W_pure"] = ai_result.get("W_pure", True)
                        st.session_state.slider_values["E_val"] = ai_result.get("E_val", 0.5)
                        
                        st.success(T("✅ تم التحليل وملء المنزلقات!", "✅ Analysis complete! Sliders filled."))
                        if "analysis" in ai_result:
                            st.info(ai_result["analysis"])
                        st.rerun()
                except Exception as e:
                    st.error(f"خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}")
    
    # --- عرض النتائج ---
    st.markdown("---")
    vals = [st.session_state.slider_values.get(f"V{i}", 0.0) for i in range(N_IND)]
    W_pure = st.session_state.slider_values.get("W_pure", True)
    E_val = st.session_state.slider_values.get("E_val", 0.5)
    W_vals = vals[0:6]; B_vals = vals[6:11]
    W_raw = np.mean(W_vals); B_raw = np.mean(B_vals)
    B_compassion = B_vals[1]; B_disavowal = B_vals[0]
    S_final, E_norm, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
        W_raw, B_raw, E_val, W_pure, B_compassion, B_disavowal
    )
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("W", f"{W_raw:+.2f}"); col2.metric("B", f"{B_raw:+.2f}")
    col3.metric("S", f"{S_final:.2f}"); col4.metric("E", f"{E_val:.2f}")
    col5.metric(T("فجوة", "Gap"), f"{istidraj_gap:.2f}")
    
    if gate_msg:
        st.markdown(f"### {gate_color} {gate_name}")
        if TXT("انهيار", "Collapse") in gate_msg or TXT("لا يغفر", "Unforgivable") in gate_msg:
            st.error(gate_msg)
        elif TXT("باطلة", "Void") in gate_msg:
            st.warning(gate_msg)
        else:
            st.success(gate_msg)
    
    if istidraj_gap > 0.3: st.error(f"🚨 {TXT('إنذار استدراج', 'Istidraj Alert')}")
    elif istidraj_gap > 0.1: st.warning(f"⚡ {TXT('فجوة متوسطة', 'Moderate Gap')}")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(T("### 🗺️ خريطة الوجود", "### 🗺️ Existence Map"))
        fig = plot_quadrant_map(B_raw, W_raw, istidraj_gap)
        st.pyplot(fig)
    with col_b:
        st.markdown(T("### ⏳ المحاكي الزمني", "### ⏳ Time Simulator"))
        years = st.slider(T("سنوات", "Years"), 10, 100, 50, 10, key="yrs_lab")
        S_hist, E_hist = simulate_future(S_final, E_val, W_raw, B_raw, years)
        fig, ax = plt.subplots(figsize=(5,3), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(S_hist, label='S', color='#FFD700', lw=2)
        ax.plot(E_hist, label='E', color='#0FF', lw=1.5, ls='--')
        ax.fill_between(range(years+1), S_hist, E_hist, where=(np.array(E_hist)>np.array(S_hist)), color='red', alpha=0.2)
        ax.set_xlabel(T('سنوات', 'Years'), color='white')
        ax.set_ylabel(T('قيمة', 'Value'), color='white')
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=6)
        ax.tick_params(colors='white', labelsize=6); ax.grid(True, alpha=0.2)
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown(T("### 🏥 المستشفى", "### 🏥 Hospital"))
    wW, wB = np.argmin(W_vals), np.argmin(B_vals)
    W_L = [get_indicator_label(i) for i in range(6)]
    B_L = [get_indicator_label(i+6) for i in range(5)]
    if gate_name == T("بوابة الشرك", "Shirk Gate"):
        st.error(T("العلاج: تجديد التوحيد.", "Renew Tawheed."))
    elif gate_name == T("بوابة الماعون", "Al-Ma'un Gate"):
        st.error(f"🎯 أصلح '{B_L[wB]}' أولاً.")
    elif gate_name == T("بوابة الإخلاص", "Sincerity Gate"):
        st.warning(f"🎯 نقِّ '{W_L[wW]}' من الشرك.")
    elif istidraj_gap > 0.3:
        st.error(f"🎯 سد الفجوة عبر '{W_L[wW]}' أو '{B_L[wB]}'.")
    else:
        st.info(f"🎯 عزز '{W_L[wW]}' و'{B_L[wB]}'.")

# =============================================
# تبويب ٣: المشهد الكوني الحي
# =============================================
with tab3:
    st.header(T("🌌 المشهد الكوني الحي", "🌌 Live Cosmic Scene"))
    
    with st.expander(T("⚙️ إعدادات المشهد", "⚙️ Scene Settings"), expanded=False):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            live_speed = st.slider(T("السرعة", "Speed"), 0.01, 0.2, 0.06, 0.01, key="live_speed")
        with col_s2:
            live_stars = st.slider(T("عدد النجوم", "Stars"), 50, 300, 150, 25, key="live_stars")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button(T("▶️ تشغيل", "▶️ Run"), use_container_width=True, type="primary"):
            st.session_state.run = True
    with col_btn2:
        if st.button(T("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True):
            st.session_state.run = False
    with col_btn3:
        if st.button(T("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
            for k in list(st.session_state.keys()):
                if k.startswith("live_"): del st.session_state[k]
            st.rerun()
    
    placeholder = st.empty()
    
    if st.session_state.get("run", False):
        if not st.session_state.get("live_init", False):
            N = live_stars
            cx, cy = st.session_state.cx, st.session_state.cy
            st.session_state.live_sx = np.random.uniform(cx-13, cx+13, N)
            st.session_state.live_sy = np.random.uniform(cy-9, cy+9, N)
            st.session_state.live_sw = np.random.uniform(0.1, 1.0, N)
            st.session_state.live_sb = np.random.uniform(0.1, 1.0, N)
            st.session_state.live_W = st.session_state.W
            st.session_state.live_B = st.session_state.B
            st.session_state.live_E = st.session_state.E
            st.session_state.live_S = st.session_state.S
            st.session_state.live_aW = st.session_state.aW
            st.session_state.live_aB = st.session_state.aB
            st.session_state.live_frame = 0
            st.session_state.live_init = True
        
        try:
            cx = st.session_state.cx; cy = st.session_state.cy
            sx = st.session_state.live_sx.copy(); sy = st.session_state.live_sy.copy()
            sw = st.session_state.live_sw.copy(); sb = st.session_state.live_sb.copy()
            W = st.session_state.live_W; B = st.session_state.live_B
            E = st.session_state.live_E; S = st.session_state.live_S
            aW = st.session_state.live_aW; aB = st.session_state.live_aB
            frame = st.session_state.live_frame
            N = len(sx)
            
            for i in range(N):
                sw[i] += (W - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                sb[i] += (B - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02)
                dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                close = (dist < 2.0) & (np.arange(N) != i)
                if np.any(close):
                    sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03
                    sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03
                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)
            
            if random.random() < 0.005:
                aff = np.random.choice(N, size=int(N*0.2), replace=False)
                sw[aff] *= random.uniform(0.5, 0.8)
                sb[aff] *= random.uniform(0.5, 0.8)
            
            avgW = np.mean(sw); avgB = np.mean(sb)
            W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = W * B
            E += 0.03 * (S - E)
            
            aW += 0.02 + random.uniform(-0.02, 0.02) * (1-W)**2
            aB += 0.02 + random.uniform(-0.02, 0.02) * (1-B)**2
            wx = cx + (7 - 2.5*W) * np.cos(aW)
            wy = cy + (7 - 2.5*W) * np.sin(aW) * 0.7
            bx = cx + (5 - 1.5*B) * np.cos(aB)
            by = cy + (5 - 1.5*B) * np.sin(aB) * 0.7
            
            instability = 1 - np.mean(sw*sb)
            sx += np.random.uniform(-0.07, 0.07, N) * instability
            sy += np.random.uniform(-0.07, 0.07, N) * instability
            sx = np.clip(sx, cx-13, cx+13); sy = np.clip(sy, cy-9, cy+9)
            
            frame += 1
            
            st.session_state.live_sx = sx; st.session_state.live_sy = sy
            st.session_state.live_sw = sw; st.session_state.live_sb = sb
            st.session_state.live_W = W; st.session_state.live_B = B
            st.session_state.live_E = E; st.session_state.live_S = S
            st.session_state.live_aW = aW; st.session_state.live_aB = aB
            st.session_state.live_frame = frame
            
            fig, ax = plt.subplots(figsize=(14, 10), facecolor='#0a0f1e')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            for r, a, c in [(0.5,0.98,'#FFF'),(1,0.6,'#FFD700'),(1.8,0.3,'#FFD700'),(2.8,0.1,'#FFA500'),(4,0.03,'#FF4500')]:
                ax.add_patch(Circle((cx,cy), r*(0.5+3*S), color=c, alpha=a, zorder=15))
            ax.text(cx,cy,'S',color='#000',fontsize=14,ha='center',va='center',fontweight='bold')
            ax.add_patch(Circle((cx,cy), 0.5+16*E, color='#0FF', alpha=0.15, zorder=7))
            ax.add_patch(Circle((wx,wy), 0.2+0.6*W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx,by), 0.2+0.6*B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            colors = []
            for i in range(N):
                w, b = sw[i], sb[i]
                if w >= 0.55 and b >= 0.55: colors.append('#FFD700')
                elif w >= 0.55 and b < 0.45: colors.append('#E0E0E0')
                elif w < 0.45 and b >= 0.55: colors.append('#FF5252')
                elif w < 0.45 and b < 0.45: colors.append('#FFB6C1')
                else: colors.append('#888888')
            ax.scatter(sx,sy,s=20,c=colors,alpha=0.9,edgecolors='white',linewidths=0.2,zorder=5)
            ax.text(14,1.2,f'S={S:.2f} | E={E:.2f}',color='#CCC',fontsize=9,ha='center')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(live_speed)
            st.rerun()
        except Exception as e:
            st.error(f"Simulation error: {e}")
            st.session_state.run = False
    else:
        st.info(T("اضغط ▶️ تشغيل", "Press ▶️ Run"))

print("✅ المرحلة الثالثة مكتملة: مختبر الأمة، الذكاء الاصطناعي، المشهد الكوني الحي")

# =============================================
# المرحلة الرابعة: المعجم الهندسي، الشواهد، الصراط، التذييل
# =============================================

# =============================================
# تبويب ٤: المعجم الهندسي
# =============================================
with tab4:
    st.header(T("📖 المعجم الهندسي – الحروف وقيمها", "📖 Geometric Lexicon – Letters & Values"))
    st.markdown(T(
        "هذا المعجم يربط كل حرف بقيمته العددية (حساب الجمل) ودوره الوجودي في معادلة الميزان.",
        "This lexicon links each letter to its numerical value (Abjad) and its existential role in the Mizan equation."
    ))
    
    letters_data = {
        T('الفئة الأولى: الذات الإلهية (المصدر)', 'Cat 1: Divine Essence (Source)'): {'ك': 20, 'ن': 50},
        T('الفئة الثانية: الازدواج', 'Cat 2: Duality'): {'ق': 100, 'ص': 90},
        T('الفئة الثالثة: التجلي الإلهي', 'Cat 3: Divine Manifestation'): {'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9},
        T('الفئة الرابعة: الاشتراك (الجسور)', 'Cat 4: Connection (Bridges)'): {'ع': 70, 'ي': 10, 'هـ': 5},
        T('الفئة الخامسة: المشغلات', 'Cat 5: Operators'): {'ف': 80, 'و': 6, 'ب': 2},
        T('الفئة السادسة: أعمال الخلق', 'Cat 6: Actions of Creation'): {'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300, 'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000},
    }
    
    for cat, lets in letters_data.items():
        st.markdown(f"**{cat}**")
        df = pd.DataFrame(list(lets.items()), columns=[T('الحرف', 'Letter'), T('القيمة', 'Value')])
        st.dataframe(df, hide_index=True)

# =============================================
# قاعدة بيانات الشواهد التاريخية
# =============================================
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

# =============================================
# تبويب ٥: الشواهد التاريخية
# =============================================
with tab5:
    st.header(T("📜 الشواهد التاريخية – حين ينطق التاريخ مصدقًا للمعادلة", "📜 Historical Evidence"))
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
            st.warning(T("⚠️ حالة استدراج واضحة: التمكين المادي يفوق الثبات الأخلاقي بكثير.", "⚠️ Clear Istidraj state."))
        elif S_hist > 0.7:
            st.success(T("✅ حالة توازن عالٍ: W و B متوازنتان، والتمكين يتبع الثبات بشكل صحي.", "✅ High balance state."))
        else:
            st.info(T("ℹ️ حالة متوسطة إلى منخفضة.", "ℹ️ Moderate to low state."))

# =============================================
# الثوابت الإبراهيمية
# =============================================
ABRAHAMIC_VERSE = T(
    '﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ وَالَّذِينَ مَعَهُ إِذْ قَالُوا لِقَوْمِهِمْ إِنَّا بُرَآءُ مِنكُمْ وَمِمَّا تَعْبُدُونَ مِن دُونِ اللَّهِ كَفَرْنَا بِكُمْ وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾',
    '﴿There has certainly been for you an excellent pattern in Abraham and those with him, when they said to their people, "Indeed, we are disassociated from you and from whatever you worship other than Allah. We have denied you, and there has appeared between us and you animosity and hatred forever until you believe in Allah alone."﴾'
)

def get_spiritual_nudge(situation):
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

# =============================================
# تبويب ٦: هندسة الصراط
# =============================================
with tab6:
    st.header(T("📐 هندسة الصراط – البرهان النبوي والنموذج الإبراهيمي", "📐 Path Geometry – Prophetic Proof & Abrahamic Model"))
    
    st.markdown(T("""
    <div style="background:rgba(20,30,60,0.8);border-radius:15px;padding:25px;border:2px solid #FFD700;margin:20px 0;text-align:center;">
        <h3 style="color:#FFD700;margin-top:0;">🕋 البرهان النبوي</h3>
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
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W x B</p>
        <p style="color:#AAA;">
            الحب في الله = W (الولاء). البغض في الله = B (البراءة).<br>
            أوثق عرى الإيمان = S (الثبات). استكمل الإيمان = S=1.<br>
            الواو هنا واو المعية (x) لا واو الجمع (+)، لأن الإيمان لا يكتمل إلا باجتماعهما معًا.
        </p>
    </div>
    """, """
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
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W x B</p>
        <p style="color:#AAA;">
            Love for Allah = W. Hatred for Allah = B.<br>
            The firmest handhold = S. Completed faith = S=1.<br>
            The "and" is multiplication (x), because faith is only complete with both together.
        </p>
    </div>
    """), unsafe_allow_html=True)
    
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
    
    # التأكد من تهيئة متغيرات المسار
    if 'path_W' not in st.session_state:
        st.session_state.path_W = [0.5]
    if 'path_B' not in st.session_state:
        st.session_state.path_B = [0.5]
    if 'path_kappa' not in st.session_state:
        st.session_state.path_kappa = [0.0]
    
    # --- أزرار التفاعل ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button(T("▶️ خطوة نحو الكمال", "▶️ Step Toward Perfection"), key="btn_path", use_container_width=True):
            current_W = st.session_state.path_W[-1]
            current_B = st.session_state.path_B[-1]
            new_W = min(1.0, current_W + 0.05)
            new_B = min(1.0, current_B + 0.05)
            st.session_state.path_W.append(new_W)
            st.session_state.path_B.append(new_B)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            
            dist = np.sqrt((1 - new_W)**2 + (1 - new_B)**2)
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
            current_W = st.session_state.path_W[-1]
            current_B = st.session_state.path_B[-1]
            new_W = max(0.0, current_W - sin_str * random.uniform(0.5, 1.5))
            new_B = max(0.0, current_B - sin_str * random.uniform(0.5, 1.5))
            st.session_state.path_W.append(new_W)
            st.session_state.path_B.append(new_B)
            st.session_state.path_kappa.append(curvature(st.session_state.path_W, st.session_state.path_B))
            st.session_state.spiritual_nudge = get_spiritual_nudge("sin")
            st.rerun()
    
    with c3:
        if st.button(T("🕌 توبة نصوح", "🕌 Sincere Repentance"), key="btn_rep", use_container_width=True):
            current_W = st.session_state.path_W[-1]
            current_B = st.session_state.path_B[-1]
            new_W = min(1.0, current_W + 0.8 * (1.0 - current_W))
            new_B = min(1.0, current_B + 0.8 * (1.0 - current_B))
            st.session_state.path_W.append(new_W)
            st.session_state.path_B.append(new_B)
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
        st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
        st.session_state.path_kappa = [0.0]
        st.session_state.spiritual_nudge = None
        st.rerun()
    
    # --- رسم المسار ---
    pW = st.session_state.path_W
    pB = st.session_state.path_B
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0f1e')
    
    ax1 = axes[0]
    ax1.set_facecolor('#0a0f1e')
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_xlabel("B (البراءة)", color='white'); ax1.set_ylabel("W (الولاء)", color='white')
    ax1.set_title(T("مسارك في فضاء (W, B) – النموذج الإبراهيمي", "Your Path in (W, B) Space"), color='white', fontsize=13)
    
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=3, alpha=0.8, 
             label=T("✦ مسار إبراهيم (κ = 0)", "✦ Abraham's Path"))
    ax1.scatter([1], [1], s=200, c='#FFD700', edgecolors='white', linewidth=3, zorder=10, 
                label=T("⭐ مقام إبراهيم (1,1)", "⭐ Station of Abraham"))
    
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.path_kappa[i] if i < len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label=T("البداية", "Start"))
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label=T("الآن", "Now"))
    
    ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
    
    ax2 = axes[1]
    ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.path_kappa, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label=T("حد الخطر", "Danger"))
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label=T("الصراط (κ=0)", "Straight Path"))
    ax2.set_title(T("منحنى الانحناء (κ)", "Curvature Over Time"), color='white', fontsize=13)
    ax2.set_xlabel(T("الخطوات", "Steps"), color='white'); ax2.set_ylabel("κ", color='white')
    ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
    max_kappa = max(st.session_state.path_kappa) if st.session_state.path_kappa else 0.1
    ax2.set_ylim(-0.01, max(0.2, max_kappa * 1.2))
    
    plt.tight_layout(); st.pyplot(fig)
    
    # --- مؤشرات ---
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("W (الولاء)", f"{pW[-1]:.3f}")
    c2.metric("B (البراءة)", f"{pB[-1]:.3f}")
    current_kappa = st.session_state.path_kappa[-1] if st.session_state.path_kappa else 0.0
    c3.metric("κ (الانحناء)", f"{current_kappa:.4f}")
    on_path = current_kappa < 0.03
    c4.metric(T("الصراط؟", "On Path?"), T("✅ نعم", "✅ YES") if on_path else T("⚠️ لا", "⚠️ NO"))
    
    dist_to_abraham = np.sqrt((1 - pW[-1])**2 + (1 - pB[-1])**2)
    st.markdown(f"""
    <div style='text-align:center;padding:15px;background:rgba(20,30,60,0.8);border-radius:10px;border:1px solid #FFD700;'>
        <p style='color:#FFD700;font-size:1em;margin:0;'>
            {T(f'📏 المسافة إلى مقام إبراهيم: {dist_to_abraham:.3f}', f'📏 Distance to Station of Abraham: {dist_to_abraham:.3f}')}
        </p>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# 🏁 التذييل – ختام المسك
# =============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.5em;">⚖️ مختبر الميزان</p>
    <p style="font-size:1.1em;">{T('سفينة نوح الرقمية – القانون الواحد من الذرة إلى الحضارة', 'The Digital Ark – The One Law from Atom to Civilization')}</p>
    <p style="color:#FFD700;font-size:1.3em;">S = W x B</p>
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

print("✅ المرحلة الرابعة مكتملة: المعجم الهندسي، الشواهد، الصراط، التذييل")
print("✅✅✅ تم بناء المنصة الذهبية – الدين القيم – المنارة العالمية بنجاح!")
