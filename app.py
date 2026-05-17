import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import random, time
from collections import deque
from io import BytesIO
import json
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# =============================================
# إعدادات الصفحة
# =============================================
st.set_page_config(
    page_title="⚖️ الدين القيم – المنارة العالمية",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# النظام اللغوي
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang
TXT = lambda ar, en: ar if LANG == "ar" else en

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
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; width: 100%; transition: all 0.3s ease; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; box-shadow: 0 0 25px rgba(255,215,0,0.5); }
.stTabs [data-baseweb="tab-list"] { gap: 5px; background: rgba(13,21,40,0.8); border-radius: 15px; padding: 5px; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: bold; }
.message-box { background: rgba(20,30,60,0.7); border-radius: 15px; padding: 30px; margin: 20px 0; border: 1px solid rgba(255,215,0,0.3); line-height: 2.2; }
</style>
""", unsafe_allow_html=True)

# =============================================
# الثوابت الوجودية – المعجم الهندسي (28 حرفاً)
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
# المؤشرات الأخلاقية الأساسية (11 مؤشراً)
# =============================================
INDICATORS_META = [
    {"ar": "الصلاة (إقامة/تضييع)", "en": "Prayer", "letter": "ن", "val": 50},
    {"ar": "الزكاة والصدقات (إيتاء/منع)", "en": "Zakat & Charity", "letter": "ص", "val": 90},
    {"ar": "الولاء لله ورسوله والمؤمنين", "en": "Loyalty to Allah & Believers", "letter": "أ", "val": 1},
    {"ar": "تحكيم الشريعة (تحكيم/رفض)", "en": "Applying Sharia", "letter": "ل", "val": 30},
    {"ar": "العدل (عدل/ظلم)", "en": "Justice", "letter": "ق", "val": 100},
    {"ar": "الشورى (تشاور/استبداد)", "en": "Consultation", "letter": "م", "val": 40},
    {"ar": "البراءة من الطاغوت (براءة/موالاة)", "en": "Disavowal of Taghut", "letter": "هـ", "val": 5},
    {"ar": "الرحمة والعطاء – الماعون (رحمة/قسوة)", "en": "Mercy & Giving", "letter": "ح", "val": 8},
    {"ar": "الأمر بالمعروف (أمر/نهي)", "en": "Enjoining Good", "letter": "ف", "val": 80},
    {"ar": "النهي عن المنكر (نهي/أمر)", "en": "Forbidding Evil", "letter": "و", "val": 6},
    {"ar": "العفاف والتورع", "en": "Chastity & Godly Caution", "letter": "ط", "val": 9},
]
N_IND = len(INDICATORS_META)

def get_indicator_label(i):
    meta = INDICATORS_META[i]
    name = meta["ar"] if LANG == "ar" else meta["en"]
    return f"{name}  [{meta['letter']}={meta['val']}]"

# =============================================
# المحكمة العليا (4 بوابات)
# =============================================
def supreme_court(W_raw, B_raw, W_pure, B_compassion, B_disavowal):
    if not W_pure:
        return (0, TXT("بوابة الشرك","Shirk Gate"), TXT("⚠️ لا يغفر: ﴿إِنَّ اللَّهَ لَا يَغْفِرُ أَن يُشْرَكَ بِهِ﴾","⚠️ Unforgivable"), "🔴")
    if B_compassion <= 0:
        return (-1, TXT("بوابة الماعون","Al-Ma'un Gate"), TXT("⚠️ انهيار: ﴿فَوَيْلٌ لِّلْمُصَلِّينَ...﴾","⚠️ Collapse"), "🔴")
    if W_raw > 0 and B_disavowal <= 0:
        return (0, TXT("بوابة الإخلاص","Sincerity Gate"), TXT("⚠️ عبادة باطلة: ﴿يَعْبُدُونَنِي...﴾","⚠️ Void"), "🟡")
    if W_raw > 0 and B_raw > 0:
        return (1, TXT("بوابة الوعد","Promise Gate"), TXT("🟢 ثبات: ﴿فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ﴾","🟢 Stability"), "🟢")
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
    return min(1.0, S_raw), E, TXT("المعادلة العامة","General"), "", "⚪", istidraj_gap

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
    ax.set_xlabel(TXT("B (البراءة)","B (Disavowal)"), color='white')
    ax.set_ylabel(TXT("W (الولاء)","W (Faith)"), color='white')
    ax.fill_between([0,1.2],0,1.2,color='#FFD700',alpha=0.3,label=TXT('المؤمنون','Believers'))
    ax.fill_between([-1.2,0],0,1.2,color='#FF5252',alpha=0.2,label=TXT('المغضوب عليهم','Wrath'))
    ax.fill_between([-1.2,0],-1.2,0,color='#FFB6C1',alpha=0.2,label=TXT('المنافقون','Hypocrites'))
    ax.fill_between([0,1.2],-1.2,0,color='#FFA500',alpha=0.2,label=TXT('الضالون','Astray'))
    ax.scatter(B_raw,W_raw,s=300,c='cyan',edgecolors='white',linewidth=2,zorder=10)
    ax.scatter(1,1,s=100,c='#FFD700',edgecolors='white',linewidth=2,zorder=10,marker='*')
    ax.text(1,1.15,TXT('مقام إبراهيم','Abraham'),color='#FFD700',fontsize=8,ha='center')
    if istidraj_gap>0: ax.text(0.5,-0.9,TXT(f"فجوة:{istidraj_gap:.2f}",f"Gap:{istidraj_gap:.2f}"),color='red',fontsize=9,ha='center',fontweight='bold')
    ax.legend(facecolor='#0a0f1e',edgecolor='white',labelcolor='white',fontsize=7,loc='lower left')
    ax.tick_params(colors='white')
    return fig

def star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    return '#888888'

def curvature(W, B):
    if len(W) < 3: return 0
    dW = np.gradient(list(W)); dB = np.gradient(list(B))
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return num / denom

# =============================================
# قاعدة بيانات البوصلة الكاملة (19 سؤالاً)
# =============================================
COMPASS_DATA = [
    {"id":1,"topic":TXT("تحكيم الشريعة في زمن القوانين الوضعية","Sharia vs Man-Made Laws"),"letter":"ق","value":100,
     "text":TXT("في زمن سيادة القوانين الوضعية، وشعار 'الدين لله والوطن للجميع'، كمسلم: ما هو موقفك من تحكيم شرع الله؟","In an age of man-made laws..."),
     "answers":[(TXT("أجاهد لتطبيق شرع الله في كل مناحي الحياة","I strive to apply Sharia"),0.5,0.5),(TXT("أتمنى تطبيقها لكني لا أعمل لأجلها","I wish but don't act"),0.3,-0.2),(TXT("بعض أحكامها صالح والآخر لا","Some valid, some not"),-0.2,-0.2),(TXT("الشريعة لا تصلح لهذا العصر","Sharia is unsuitable"),-0.4,-0.5)]},
    {"id":2,"topic":TXT("الولاء للعرق والحزب والطائفة","Loyalty to Race, Party, Sect"),"letter":"أ","value":1,
     "text":TXT("في عصر أصبح فيه الولاء للعرق والحزب والطائفة والمذهب هو المعيار، كمسلم: ما هو موقفك؟","In an age of racial loyalty..."),
     "answers":[(TXT("ولائي لله ورسوله والمؤمنين فوق كل رابطة","My loyalty to Allah above all"),0.7,0.2),(TXT("أوازن بين ولائي للإسلام وانتمائي العرقي","I try to balance"),0.3,-0.2),(TXT("ولائي لديني ضعيف وأميل للفخر بعرقي","Weak religious loyalty"),-0.2,0.1),(TXT("لا أرى مشكلة في تقديم العرق على الدين","Race over religion"),-0.5,-0.3)]},
    {"id":3,"topic":TXT("الاستهزاء بالمقدسات وحرية التعبير","Mockery of Sanctities & Free Speech"),"letter":"هـ","value":5,
     "text":TXT("في زمن تُباح فيه 'حرية التعبير' للاستهزاء بالدين والمقدسات، كمسلم: ما هو موقفك؟","In an age of free speech..."),
     "answers":[(TXT("أبغض في الله المستهزئين وأدين فعلهم","I hate and condemn mockers"),0.3,0.7),(TXT("أستنكر الاستهزاء بقلبي لكن لا أعلن","I disapprove in heart"),0.1,-0.1),(TXT("أرى أنها حرية رأي ولا داعي للغضب","Free speech, no anger"),-0.2,0.1),(TXT("أضحك معهم أحياناً ولا أرى ضرراً","I laugh with them"),-0.3,-0.3)]},
    {"id":4,"topic":TXT("الربا والنظام المالي العالمي","Usury and Global Finance"),"letter":"ص","value":90,
     "text":TXT("في زمن يقوم فيه النظام المالي العالمي على الربا، وأصبح التعامل بالفوائد 'أمراً طبيعياً'، كمسلم: ما هو موقفك؟","In an age of usurious finance..."),
     "answers":[(TXT("أتجنب الربا بكل صوره وأبحث عن بدائل إسلامية","I avoid all usury"),0.3,0.7),(TXT("أكره الربا لكني مضطر للتعامل به أحياناً","I hate it but am forced"),0.1,-0.2),(TXT("أتعامل بالربا كالجميع ولا أرى مشكلة","I deal with it like everyone"),-0.2,0.1),(TXT("الربا ضرورة اقتصادية وتحريمه كان لزمن غير زمننا","Usury is a necessity"),-0.3,-0.3)]},
    {"id":5,"topic":TXT("العلمانية وفصل الدين عن الدولة","Secularism & Separation"),"letter":"ك","value":20,
     "text":TXT("في زمن تسود فيه العلمانية، وتُرفع شعارات 'فصل الدين عن الدولة'، كمسلم: ما هو موقفك؟","In an age of secularism..."),
     "answers":[(TXT("أرفض العلمانية وأؤمن أن الإسلام دين ودولة","I reject secularism"),0.5,0.5),(TXT("العلمانية قد تكون حلاً مؤقتاً","Temporary solution"),0.1,-0.1),(TXT("لا أمانع فصل الدين عن السياسة","I don't mind separation"),-0.2,0.1),(TXT("العلمانية هي الطريق الصحيح للتقدم","Secularism is correct"),-0.4,-0.5)]},
    {"id":6,"topic":TXT("إقامة الحدود الشرعية","Establishing Sharia Penalties"),"letter":"ح","value":8,
     "text":TXT("في زمن تُلغى فيه الحدود الشرعية (كقطع يد السارق) بدعوى 'الهمجية' و'عدم الإنسانية'، كمسلم: ما هو موقفك؟","In an age of abolishing penalties..."),
     "answers":[(TXT("الحدود الشرعية رحمة وعدل وأؤمن بضرورة إقامتها","Penalties are mercy"),0.3,0.7),(TXT("الحدود حق لكن الظروف الحالية لا تسمح","Right but conditions hard"),0.1,-0.1),(TXT("أشعر بالحرج من بعض الحدود وأراها قاسية","I feel embarrassed"),-0.2,0.1),(TXT("الحدود الشرعية همجية ولا تصلح للعصر الحديث","Penalties are barbaric"),-0.3,-0.3)]},
    {"id":7,"topic":TXT("الإلحاد وإنكار الخالق","Atheism & Denying the Creator"),"letter":"ن","value":50,
     "text":TXT("في زمن ينتشر فيه الإلحاد، ويُقدَّم العلم على أنه ينفي وجود الله، كمسلم: ما هو موقفك؟","In an age of atheism..."),
     "answers":[(TXT("أؤمن بالله يقيناً لا يتزعزع وأرى في العلم دليلاً عليه","I believe certainly"),0.5,0.5),(TXT("أؤمن بالله لكني لا أملك حججاً للرد على الشبهات","I believe but lack arguments"),0.1,-0.1),(TXT("تساورني أحياناً شكوك لكني أعود للإيمان","Doubts cross my mind"),-0.2,0.1),(TXT("الإلحاد طرح فكري يحترم والدين مجرد أساطير","Atheism is respectable"),-0.4,-0.5)]},
    {"id":8,"topic":TXT("الجهاد ونصرة المستضعفين","Jihad & Supporting the Oppressed"),"letter":"ر","value":200,
     "text":TXT("في زمن يُشوَّه فيه الجهاد ويوصم بـ 'الإرهاب'، ويُخذل فيه المستضعفون من المسلمين، كمسلم: ما هو موقفك؟","In an age of distorting jihad..."),
     "answers":[(TXT("الجهاد ذروة سنام الإسلام وأتمنى أن أكون في صفوف المجاهدين","Jihad is peak of Islam"),0.3,0.7),(TXT("الجهاد حق وأدعمه بقلبي ومالي إن استطعت","Jihad is right, I support"),0.1,-0.1),(TXT("أخشى من الجهاد وأرى أنه يجلب المشاكل","I fear jihad"),-0.2,0.1),(TXT("الجهاد أصبح إرهاباً ولا مكان له في هذا العصر","Jihad became terrorism"),-0.3,-0.3)]},
    {"id":9,"topic":TXT("حقوق المرأة بين الإسلام والتغريب","Women's Rights: Islam vs. West"),"letter":"هـ","value":5,
     "text":TXT("في زمن تُطرح فيه 'حقوق المرأة' بصيغة غربية تنتزعها من فطرتها، وتُتهم الشريعة بظلمها، كمسلم: ما هو موقفك؟","In an age of women's rights..."),
     "answers":[(TXT("أؤمن أن الإسلام كرم المرأة ورفع شأنها وأن أحكامه عين العدل","Islam honored women"),0.5,0.5),(TXT("أؤمن بالإسلام لكني أرى ضرورة تحديث بعض الأحكام","Need update"),0.1,-0.1),(TXT("أشعر بالحرج من بعض أحكام الإسلام الخاصة بالمرأة","I feel embarrassed"),-0.2,0.1),(TXT("الإسلام ظلم المرأة وتحريرها يكون بالعلمانية","Islam oppressed women"),-0.4,-0.5)]},
    {"id":10,"topic":TXT("العولمة والذوبان الحضاري والموضة والاستهلاك","Globalization & Fashion"),"letter":"م","value":40,
     "text":TXT("في زمن العولمة التي تسعى لطمس الهويات، وتحول الاستهلاك إلى ثقافة، وأصبح الترف هدفاً، والموضة تفرض أزياء تخالف الفطرة... ما هو موقفك؟","In an age of globalization..."),
     "answers":[(TXT("أتمسك بهويتي الإسلامية وأتبرأ من تقليد الكفار وأزهد في الدنيا","I hold fast to my Islamic identity"),0.5,0.5),(TXT("أحاول أوازن بين هويتي ومتطلبات العصر","I try to balance"),0.1,-0.1),(TXT("أقلد الغرب في ثقافته وأزيائه واستهلاكه","I imitate the West"),-0.2,0.1),(TXT("الثقافة الغربية هي التقدم ويجب الاندماج","Western culture is progress"),-0.4,-0.5)]},
    {"id":11,"topic":TXT("الديمقراطية والتشريع","Democracy & Legislation"),"letter":"ل","value":30,
     "text":TXT("في زمن تُقدَّس فيه الديمقراطية وتُجعل الشعب هو مصدر التشريع، كمسلم: ما هو موقفك؟","In an age of democracy..."),
     "answers":[(TXT("التشريع لله وحده والشورى طاعة لله في تطبيق ما شرع","Legislation for Allah"),0.5,0.5),(TXT("الديمقراطية وسيلة يمكن استخدامها لتحقيق مصالح","Democracy is a tool"),0.1,-0.1),(TXT("أفضّل الديمقراطية على الاستبداد","I prefer democracy"),-0.2,0.1),(TXT("الديمقراطية أفضل نظام والشريعة لا تصلح سياسياً","Democracy is best"),-0.4,-0.5)]},
    {"id":12,"topic":TXT("التعددية الدينية","Religious Pluralism"),"letter":"ي","value":10,
     "text":TXT("في زمن تُطرح فيه 'التعددية الدينية' على أنها تعني أن كل الأديان طرق للخلاص، كمسلم: ما هو موقفك؟","In an age of pluralism..."),
     "answers":[(TXT("الإسلام هو الدين الوحيد المقبول عند الله","Islam is the only accepted religion"),0.5,0.5),(TXT("الإسلام هو الحق لكني لا أحكم على الآخرين","Islam is truth but I don't judge"),0.1,-0.1),(TXT("أرى أن كل الأديان فيها جزء من الحق","All religions have truth"),-0.2,0.1),(TXT("كل الأديان سواء ولا يحق لأحد ادعاء الحقيقة","All religions are equal"),-0.4,-0.5)]},
    {"id":13,"topic":TXT("الحب في الله والبغض في الله","Love & Hatred for Allah"),"letter":"ق","value":100,
     "text":TXT("في زمن أصبحت فيه المصلحة هي المعيار الأساسي في العلاقات، واختفى معنى 'الحب في الله والبغض في الله'، كمسلم: ما هو موقفك؟","In an age of interests..."),
     "answers":[(TXT("أحب في الله أولياءه وأبغض في الله أعداءه","I love and hate for Allah"),0.5,0.5),(TXT("أحاول لكن علاقاتي تغلب عليها المصالح","I try but interests dominate"),0.1,-0.1),(TXT("أتعامل مع الجميع بالمثل لا حب ولا بغض","I deal equally with all"),-0.2,0.1),(TXT("علاقاتي كلها تقوم على مصلحتي الشخصية","My relationships are interests only"),-0.4,-0.5)]},
    {"id":14,"topic":TXT("الصدق والأمانة والوفاء في زمن الكذب والغش","Truthfulness in an Age of Lying"),"letter":"ط","value":9,
     "text":TXT("في زمن أصبح الخداع والكذب والغش ذكاءً، وخان الناس الأمانات والعهود، كمسلم: ما هو موقفك من الصدق والأمانة والوفاء؟","In an age of deception..."),
     "answers":[(TXT("الصدق والأمانة والوفاء دين وألتزم بها ولو خسرت","Truthfulness is my religion"),0.5,0.5),(TXT("أحاول الالتزام لكني قد أضطر للكذب أحياناً","I try but may be forced"),0.1,-0.1),(TXT("المبالغة في الصدق سذاجة والواقع يفرض المرونة","Excessive honesty is naivety"),-0.2,0.1),(TXT("الكذب والغش والخيانة أدوات ضرورية للنجاح","Lying is necessary for success"),-0.4,-0.5)]},
    {"id":15,"topic":TXT("الأمر بالمعروف والنهي عن المنكر في زمن الفواحش","Enjoining Good in an Age of Indecency"),"letter":"ب","value":2,
     "text":TXT("في زمن انتشرت فيه الفواحش، وصار إنكار المنكر 'تطرفاً'، كمسلم: ما هو موقفك من الأمر بالمعروف والنهي عن المنكر؟","In an age of indecency..."),
     "answers":[(TXT("آمر بالمعروف وأنهى عن المنكر بكل استطاعتي","I enjoin and forbid as much as I can"),0.3,0.7),(TXT("أنكر بقلبي وأحياناً بلساني إذا لم أخف ضرراً","I reject in my heart"),0.1,-0.1),(TXT("أسكت عن المنكر حفاظاً على علاقاتي ومصالحي","I remain silent"),-0.2,0.1),(TXT("لا داعي للأمر والنهي فكل إنسان حر","No need for enjoining"),-0.3,-0.3)]},
    {"id":16,"topic":TXT("الوطنية والحزبية والمذهبية","Patriotism, Partisanship, Sectarianism"),"letter":"ف","value":80,
     "text":TXT("في زمن تُقدَّس فيه الوطنية والحزبية والمذهبية، ويُرفع شعار 'الوطن أو الحزب أو المذهب أولاً'، كمسلم: ما هو موقفك؟","In an age of patriotism..."),
     "answers":[(TXT("ولائي للإسلام فوق كل وطن وحزب ومذهب","My loyalty to Islam above all"),0.5,0.5),(TXT("أحب وطني وحزبي ومذهبي لكني أقدّم الإسلام","I love my country but prioritize Islam"),0.1,-0.1),(TXT("انتمائي لوطني أو حزبي أهم من انتمائي للإسلام","National belonging is more important"),-0.2,0.1),(TXT("لا أرى مشكلة في تقديم الوطن أو الحزب على الدين","No problem with nationalism"),-0.4,-0.5)]},
    {"id":17,"topic":TXT("الصلاة في زمن الانشغال","Prayer in an Age of Busyness"),"letter":"ن","value":50,
     "text":TXT("في زمن تزدحم فيه الحياة، وتتسارع فيه الأيام، وأصبحت الصلاة 'عبئاً' على البعض، كمسلم: ما هو موقفك؟","In an age of busyness..."),
     "answers":[(TXT("الصلاة راحتي وقرة عيني ولا أتركها مهما كنت مشغولاً","Prayer is my comfort"),0.5,0.5),(TXT("أصلي لكني أؤخرها أو أستعجل فيها أحياناً","I pray but sometimes delay"),0.1,-0.1),(TXT("أصلي أحياناً وأتركها أحياناً حسب الظروف","I pray sometimes and leave sometimes"),-0.2,0.1),(TXT("لا أجد وقتاً للصلاة وأراها غير عملية","I find no time for prayer"),-0.4,-0.5)]},
    {"id":18,"topic":TXT("الصوم في زمن الشهوات","Fasting in an Age of Desires"),"letter":"ط","value":9,
     "text":TXT("في زمن تحاصر فيه الشهوات الإنسان من كل جانب، وأصبح الصوم 'تقييداً للحرية'، كمسلم: ما هو موقفك؟","In an age of desires..."),
     "answers":[(TXT("أصوم الفرض والنفل وأراه دورة تدريبية على تقوى الله","I fast obligatory and voluntary"),0.5,0.5),(TXT("أصوم الفرض فقط ولا أستطيع صيام النفل","I fast only obligatory"),0.1,-0.1),(TXT("أصوم رمضان كعادة اجتماعية ولا أشعر بروحانيته","I fast Ramadan as a habit"),-0.2,0.1),(TXT("لا أصوم وأرى أن العصر لا يتناسب مع فكرة الصيام","I don't fast"),-0.4,-0.5)]},
    {"id":19,"topic":TXT("الزكاة والصدقة في زمن الأنانية","Zakat & Charity in an Age of Selfishness"),"letter":"ط","value":9,
     "text":TXT("في زمن طغت فيه الأنانية، وضعف فيه التكافل، وأصبح المال 'إلهاً'، كمسلم: ما هو موقفك من الزكاة والصدقة؟","In an age of selfishness..."),
     "answers":[(TXT("أؤدي الزكاة طيبة بها نفسي وأعترف أن المال مال الله","I pay Zakat willingly"),0.5,0.5),(TXT("أؤدي الزكاة فقط وأحياناً أتصدق","I pay only Zakat"),0.1,-0.1),(TXT("أخرج الزكاة بخلاً وأشعر أنها ضريبة","I pay Zakat grudgingly"),-0.2,0.1),(TXT("لا أزكي فالمال مالي ولا دخل لأحد فيه","I don't pay Zakat"),-0.4,-0.5)]},
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
# المرحلة الثانية: الواجهة الكاملة + تبويب البوصلة
# =============================================

# --- الشريط الجانبي ---
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:8px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <p style='font-size:2em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:0;'>{TXT('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h2>
        <p style='color:#e0e0e0;font-size:10px;margin:2px 0;'>{TXT('المنارة العالمية', 'The Global Beacon')}</p>
        <p style='color:#FFD700;font-size:14px;margin:2px 0;font-weight:bold;'>S = W x B</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(TXT("🇬🇧 English", "🇸🇦 العربية"), use_container_width=True):
        st.session_state.lang = "en" if LANG == "ar" else "ar"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown(f"### {TXT('⚙️ إعدادات عامة', '⚙️ General Settings')}")
    lag = st.select_slider(
        TXT("فجوة الاستدراج", "Istidraj Gap"),
        options=[5, 10, 15, 22, 30, 40, 50],
        value=22, key="lag"
    )
    
    st.markdown("---")
    
    # --- الميزان الأخروي الحي ---
    good = st.session_state.get('good', 0)
    bad = st.session_state.get('bad', 0)
    balance = good - bad
    if balance > 0:
        status, color = TXT("⚖️ راجحة", "⚖️ Winning"), '#FFD700'
    elif balance < 0:
        status, color = TXT("⚖️ خاسرة", "⚖️ Losing"), '#FF4444'
    else:
        status, color = TXT("⚖️ متوازنة", "⚖️ Balanced"), '#888'
    st.sidebar.markdown(f"""
    <div style="text-align:center;padding:10px;background:rgba(10,15,30,0.9);border-radius:10px;border:1px solid #FFD700;margin-top:10px;">
        <p style="color:#FFD700;font-size:0.8em;margin:0;">📜 {TXT('الميزان الحي', 'Live Scales')}</p>
        <p style="color:#FFD700;font-size:0.7em;margin:2px 0;">{TXT('حسنات', 'Good')}: {good:.0f} | {TXT('سيئات', 'Bad')}: {bad:.0f}</p>
        <p style="color:{color};font-size:0.9em;margin:0;font-weight:bold;">{status}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button(TXT("🔄 إعادة ضبط كل شيء", "🔄 Full Reset"), key="btn_reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

# --- رسالة الترحيب ---
with st.expander(TXT("📜 رسالة ترحيب", "📜 Welcome Message"), expanded=True):
    st.markdown(f"""
    <div class="message-box">
    <h2 style="text-align:center;color:#FFD700;">⚖️ {TXT('مختبر الميزان', 'The Mizan Lab')}</h2>
    <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;">
    "{TXT('هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟', 'Is there a single law governing the atom and civilization?')}"
    </p>
    <p>{TXT(
    'هذا ليس كتابًا، وليس تطبيقًا. هذا مختبر. مختبرٌ صغير، لعله يفتح لك بابًا كبيرًا. '
    'لا ندّعي الحقيقة المطلقة، بل ندعوك لرؤية شيءٍ قد يكون مرّ على قلبك ولم تلاحظه.',
    'This is not a book, nor an app. This is a lab. A small lab, perhaps it opens a big door for you. '
    'We do not claim absolute truth, but invite you to see something that may have passed your heart unnoticed.'
    )}</p>
    <p>{TXT(
    'تأمل معي: الذرةُ في داخلها قوتان: جاذبيةٌ تجمع، وتنافرٌ يمنع التصادم. لو اختلت إحداهما، لانهارت الذرة. '
    'والخليةُ في جسدك: جهاز مناعةٍ يحمي، وغذاءٌ يبني. لو نامت المناعة، لالتهم المرضُ الجسد.',
    'Reflect with me: the atom has two forces: attraction that gathers, and repulsion that prevents collision. '
    'If one fails, the atom collapses. And the cell in your body: an immune system that protects, and nutrition that builds. '
    'If immunity sleeps, disease devours the body.'
    )}</p>
    <p>{TXT(
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
    <p>{TXT(
    'والمجتمع: ولاءٌ يجمع أفراده، وبراءةٌ من الفساد تحمي تماسكه. لو غاب أحدهما، تفكك المجتمع.',
    'And society: loyalty that gathers its members, and disavowal of corruption that protects its cohesion. '
    'If either is absent, society disintegrates.'
    )}</p>
    <p style="color:#FFD700;font-weight:bold;">{TXT(
    'هل هذه مصادفة؟ أم أن هناك "قانونًا واحدًا" ينساب في نسيج الوجود كله، من الذرة إلى الحضارة؟',
    'Is this coincidence? Or is there a "single law" flowing through the fabric of existence, from atom to civilization?'
    )}</p>
    <p>{TXT(
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
    <p>{TXT(
    'W: الولاء لله وأوليائه. B: البراءة من الطاغوت وأوليائه. S: الثبات الوجودي.',
    'W: Loyalty to Allah & His allies. B: Disavowal of Taghut & its allies. S: Existential Stability.'
    )}</p>
    <p style="text-align:center;font-style:italic;color:#AAA;">{TXT(
    'جرب. تأمل. واسأل. الباب مفتوح.',
    'Try. Reflect. Ask. The door is open.'
    )}</p>
    </div>
    """, unsafe_allow_html=True)

# --- دليل المستخدم ---
with st.expander(TXT("📖 دليل المستخدم", "📖 User Guide"), expanded=False):
    st.markdown(TXT("""
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
    st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{TXT('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
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
    if st.button("English" if LANG == "ar" else "العربية", key="btn_lang", use_container_width=True):
        st.session_state.lang = "en" if LANG == "ar" else "ar"
        st.rerun()

st.markdown("---")

# --- التبويبات ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    TXT("🧍 بوصلة الإسلام الحنيف", "🧍 Compass"),
    TXT("🏛️ مختبر الأمة", "🏛️ Nation Lab"),
    TXT("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    TXT("📖 المعجم الهندسي", "📖 Lexicon"),
    TXT("📜 الشواهد", "📜 Evidence"),
    TXT("📐 هندسة الصراط", "📐 Path")
])

# =============================================
# تبويب ١: بوصلة الإسلام الحنيف
# =============================================
with tab1:
    st.header(TXT("🧍 بوصلة الإسلام الحنيف – اكتشف موقعك بدقة", "🧍 Compass – Discover Your Precise Position"))
    
    # إعدادات البوصلة
    col_set1, col_set2 = st.columns([3, 1])
    with col_set1:
        st.markdown(TXT("أجب عن الأسئلة الـ 19. كل إجابة تؤثر على W و B معًا. المعادلة: S = W x B", "Answer the 19 questions. Each answer affects both W and B."))
    with col_set2:
        use_ai = st.checkbox(TXT("🤖 استخدام الذكاء الاصطناعي", "🤖 Use AI"))
    
    if use_ai:
        st.info(TXT("اكتب وصفًا لحالتك ليقوم الذكاء الاصطناعي بتقدير إجاباتك.", "Describe your condition for AI to estimate."))
        ai_text = st.text_area(TXT("الوصف:", "Description:"), height=100, key="ai_compass")
        if st.button(TXT("تحليل بالذكاء الاصطناعي", "Analyze with AI"), key="btn_ai_compass"):
            with st.spinner(TXT("جاري التحليل...", "Analyzing...")):
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
                        st.success(TXT("✅ تم التحليل!", "✅ Analysis complete!"))
                        st.rerun()
                    else:
                        st.error(TXT("يرجى إضافة مفتاح OpenAI API", "Please add OpenAI API key"))
                except Exception as e:
                    st.error(f"AI Error: {e}")
    
    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}
    
    for q in COMPASS_DATA:
        with st.expander(f"**{q['id']}. {q['topic']}**  [{q['letter']}={q['value']}]"):
            st.markdown(f"*{q['text']}*")
            key = f"q_{q['id']}"
            ans = st.radio(
                TXT("اختر:", "Choose:"),
                [a[0] for a in q['answers']],
                key=key, index=None
            )
            if ans is not None:
                idx = [a[0] for a in q['answers']].index(ans)
                st.session_state.compass_answers[key] = idx
    
    if len(st.session_state.compass_answers) == 19:
        W_raw, B_raw, S_score = compute_compass(st.session_state.compass_answers)
        
        if W_raw >= 0.5 and B_raw >= 0.5:
            q_name, q_color = TXT("مؤمن", "Believer"), '#FFD700'
        elif W_raw < 0.5 and B_raw >= 0.5:
            q_name, q_color = TXT("كافر", "Disbeliever"), '#FF5252'
        elif W_raw < 0.5 and B_raw < 0.5:
            q_name, q_color = TXT("منافق", "Hypocrite"), '#FFB6C1'
        else:
            q_name, q_color = TXT("مشرك", "Polytheist"), '#FFA500'
        
        st.divider()
        st.subheader(TXT("📊 موقعك", "📊 Your Position"))
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
        ax.text(1, 1.1, TXT('إبراهيم', 'Abraham'), color='#FFD700', fontsize=7, ha='center')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        if st.button(TXT("🔄 إعادة", "🔄 Retake"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

print("✅ المرحلة الثانية مكتملة: الواجهة، رسالة الترحيب، البوصلة الكاملة")

# =============================================
# المرحلة الثالثة: مختبر الأمة والمشهد الكوني الحي
# =============================================

# =============================================
# تبويب ٢: مختبر الأمة المتكامل
# =============================================
with tab2:
    st.header(TXT("🏛️ مختبر الأمة – المنزلقات والذكاء الاصطناعي", "🏛️ Nation Lab – Sliders & AI"))
    
    # --- إعدادات المنزلقات ---
    with st.expander(TXT("🎛️ مؤشرات الطاقة الروحية", "🎛️ Spiritual Energy Indicators"), expanded=True):
        st.caption(TXT(
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
                TXT("الإخلاص لله (عدم الشرك) [أ=1]", "Sincerity [A=1]"),
                value=st.session_state.slider_values.get("W_pure", True)
            )
            st.session_state.slider_values["W_pure"] = W_pure
        with col_E:
            E_val = st.slider(
                TXT("التمكين (E) [ق=100]", "Empowerment [Q=100]"),
                0.0, 1.0, st.session_state.slider_values.get("E_val", 0.5), 0.05, key="lab_E"
            )
            st.session_state.slider_values["E_val"] = E_val
    
    # --- الذكاء الاصطناعي الفائق ---
    st.markdown("---")
    st.subheader(TXT("🤖 مساعد الذكاء الاصطناعي", "🤖 AI Assistant"))
    st.markdown(TXT(
        "اكتب وصفًا لأي دولة أو مجتمع أو فرد، وسيقوم الذكاء الاصطناعي بتحليله وملء المنزلقات تلقائيًا. المعادلة هي الحكم.",
        "Describe any nation, community, or individual, and AI will analyze it and fill the sliders automatically. The equation is the judge."
    ))
    
    ai_text = st.text_area(
        TXT("الوصف النصي:", "Description:"),
        height=100,
        placeholder=TXT("مثال: دولة إسلامية ذات أغلبية شابة، تعاني من فساد إداري لكنها تملك جيشًا قويًا واقتصادًا زراعيًا...",
                     "Example: An Islamic country with a young majority, suffering from corruption but with a strong military...")
    )
    
    if st.button(TXT("تحليل بالذكاء الاصطناعي وملء المنزلقات", "Analyze with AI & Fill Sliders"), type="primary", use_container_width=True):
        if not ai_text.strip():
            st.warning(TXT("يرجى إدخال وصف نصي أولاً.", "Please enter a description first."))
        else:
            with st.spinner(TXT("جاري التحليل بالذكاء الاصطناعي...", "Analyzing with AI...")):
                try:
                    import openai
                    openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
                    if not openai.api_key:
                        st.error(TXT("يرجى إضافة مفتاح OpenAI API", "Please add OpenAI API key"))
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
                        
                        st.success(TXT("✅ تم التحليل وملء المنزلقات!", "✅ Analysis complete! Sliders filled."))
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
    col5.metric(TXT("فجوة", "Gap"), f"{istidraj_gap:.2f}")
    
    if gate_msg:
        st.markdown(f"### {gate_color} {gate_name}")
        if "انهيار" in gate_msg or "Collapse" in gate_msg or "لا يغفر" in gate_msg or "Unforgivable" in gate_msg:
            st.error(gate_msg)
        elif "باطلة" in gate_msg or "Void" in gate_msg:
            st.warning(gate_msg)
        else:
            st.success(gate_msg)
    
    if istidraj_gap > 0.3: st.error(f"🚨 {TXT('إنذار استدراج', 'Istidraj Alert')}")
    elif istidraj_gap > 0.1: st.warning(f"⚡ {TXT('فجوة متوسطة', 'Moderate Gap')}")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(TXT("### 🗺️ خريطة الوجود", "### 🗺️ Existence Map"))
        fig = plot_quadrant_map(B_raw, W_raw, istidraj_gap)
        st.pyplot(fig)
    with col_b:
        st.markdown(TXT("### ⏳ المحاكي الزمني", "### ⏳ Time Simulator"))
        years = st.slider(TXT("سنوات", "Years"), 10, 100, 50, 10, key="yrs_lab")
        S_hist, E_hist = simulate_future(S_final, E_val, W_raw, B_raw, years)
        fig, ax = plt.subplots(figsize=(5,3), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(S_hist, label='S', color='#FFD700', lw=2)
        ax.plot(E_hist, label='E', color='#0FF', lw=1.5, ls='--')
        ax.fill_between(range(years+1), S_hist, E_hist, where=(np.array(E_hist)>np.array(S_hist)), color='red', alpha=0.2)
        ax.set_xlabel(TXT('سنوات', 'Years'), color='white')
        ax.set_ylabel(TXT('قيمة', 'Value'), color='white')
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=6)
        ax.tick_params(colors='white', labelsize=6); ax.grid(True, alpha=0.2)
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown(TXT("### 🏥 المستشفى", "### 🏥 Hospital"))
    wW, wB = np.argmin(W_vals), np.argmin(B_vals)
    W_L = [get_indicator_label(i) for i in range(6)]
    B_L = [get_indicator_label(i+6) for i in range(5)]
    if gate_name == TXT("بوابة الشرك", "Shirk Gate"):
        st.error(TXT("العلاج: تجديد التوحيد.", "Renew Tawheed."))
    elif gate_name == TXT("بوابة الماعون", "Al-Ma'un Gate"):
        st.error(f"🎯 أصلح '{B_L[wB]}' أولاً.")
    elif gate_name == TXT("بوابة الإخلاص", "Sincerity Gate"):
        st.warning(f"🎯 نقِّ '{W_L[wW]}' من الشرك.")
    elif istidraj_gap > 0.3:
        st.error(f"🎯 سد الفجوة عبر '{W_L[wW]}' أو '{B_L[wB]}'.")
    else:
        st.info(f"🎯 عزز '{W_L[wW]}' و'{B_L[wB]}'.")

# =============================================
# تبويب ٣: المشهد الكوني الحي
# =============================================
with tab3:
    st.header(TXT("🌌 المشهد الكوني الحي", "🌌 Live Cosmic Scene"))
    
    with st.expander(TXT("⚙️ إعدادات المشهد", "⚙️ Scene Settings"), expanded=False):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            live_speed = st.slider(TXT("السرعة", "Speed"), 0.01, 0.2, 0.06, 0.01, key="live_speed")
        with col_s2:
            live_stars = st.slider(TXT("عدد النجوم", "Stars"), 50, 300, 150, 25, key="live_stars")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button(TXT("▶️ تشغيل", "▶️ Run"), use_container_width=True, type="primary"):
            st.session_state.run = True
    with col_btn2:
        if st.button(TXT("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True):
            st.session_state.run = False
    with col_btn3:
        if st.button(TXT("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
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
        st.info(TXT("اضغط ▶️ تشغيل", "Press ▶️ Run"))

print("✅ المرحلة الثالثة مكتملة: مختبر الأمة، الذكاء الاصطناعي، المشهد الكوني الحي")

# =============================================
# المرحلة الرابعة: المعجم الهندسي والشواهد التاريخية
# =============================================

# =============================================
# تبويب ٤: المعجم الهندسي
# =============================================
with tab4:
    st.header(TXT("📖 المعجم الهندسي – الحروف وقيمها", "📖 Geometric Lexicon – Letters & Values"))
    st.markdown(TXT(
        "هذا المعجم يربط كل حرف بقيمته العددية (حساب الجمل) ودوره الوجودي في معادلة الميزان. "
        "التصنيف مبني على ست فئات وجودية، تم استنباطها من مواقع الحروف في فواتح السور وخصائصها.",
        "This lexicon links each letter to its numerical value (Abjad) and existential role in the Mizan equation. "
        "The classification is based on six existential categories, derived from the positions of letters in Quranic openings and their properties."
    ))
    
    letters_data = {
        TXT('الفئة الأولى: الذات الإلهية (المصدر)', 'Cat 1: Divine Essence (Source)'): {
            'ك': 20, 'ن': 50
        },
        TXT('الفئة الثانية: الازدواج (ثابت في الذات، متجلي في الخلق)', 'Cat 2: Duality (Fixed in Essence, Manifested in Creation)'): {
            'ق': 100, 'ص': 90
        },
        TXT('الفئة الثالثة: التجلي الإلهي (صفات متجلية في الخلق)', 'Cat 3: Divine Manifestation (Attributes Manifested in Creation)'): {
            'أ': 1, 'ل': 30, 'م': 40, 'ر': 200, 'س': 60, 'ح': 8, 'ط': 9
        },
        TXT('الفئة الرابعة: الاشتراك (الجسور بين الغيب والشهادة)', 'Cat 4: Connection (Bridges between Unseen and Seen)'): {
            'ع': 70, 'ي': 10, 'هـ': 5
        },
        TXT('الفئة الخامسة: المشغلات (أدوات المنطق والسببية)', 'Cat 5: Operators (Tools of Logic and Causality)'): {
            'ف': 80, 'و': 6, 'ب': 2
        },
        TXT('الفئة السادسة: أعمال الخلق (إرادة حرة – إيجاباً وسلباً)', 'Cat 6: Actions of Creation (Free Will – Positive and Negative)'): {
            'ج': 3, 'خ': 600, 'د': 4, 'ذ': 700, 'ز': 7, 'ش': 300,
            'ت': 400, 'ث': 500, 'ض': 800, 'ظ': 900, 'غ': 1000
        },
    }
    
    # عرض كل فئة في عمودين لتوفير المساحة
    for cat, lets in letters_data.items():
        st.markdown(f"**{cat}**")
        df = pd.DataFrame(list(lets.items()), columns=[TXT('الحرف', 'Letter'), TXT('القيمة', 'Value')])
        st.dataframe(df, hide_index=True, use_container_width=True)
    
    # --- شرح إضافي للمعجم ---
    with st.expander(TXT("📖 شرح الفئات الست", "📖 Explanation of the Six Categories"), expanded=False):
        st.markdown(TXT("""
        ### 🔮 الفئة الأولى: الذات الإلهية (المصدر)
        حرفان فقط: **ك** (الأمر – كُن) و **ن** (النور الذاتي). هما المصدر الذي تنبثق منه كل الصفات.
        ظهورهما في فواتح السور مرة واحدة فقط يدل على التفرد والوحدانية.
        **المعادلة الأولى للوجود:** ك + ن = ع (20 + 50 = 70). الأمر + النور = الإدراك.
        
        ### ⚖️ الفئة الثانية: الازدواج
        حرفان: **ق** (الميزان/القسط) و **ص** (الصمد/الصبر والصدق). لهما وجهان: وجه ثابت في الذات الإلهية، ووجه متجلي في الخلق.
        يظهران منفردين في سور (ق، ص)، ويجتمعان مع غيرهما في سور أخرى (عسق في الشورى، كهيعص في مريم).
        
        ### 🔆 الفئة الثالثة: التجلي الإلهي
        سبعة حروف: **أ، ل، م، ر، س، ح، ط**. تمثل صفات الله المتجلية في خلقه. تكرارها في فواتح السور كثير (أ=13، ل=13، م=17...)
        للدلالة على تعدد التجليات مع وحدة المصدر. هي "مُوَلِّدَات" ترفع قيمتي W و B في المعادلة.
        
        ### 🔄 الفئة الرابعة: الاشتراك (الجسور)
        ثلاثة حروف: **ع** (جسر الإدراك والعلم)، **ي** (جسر النداء والنسبة)، **هـ** (جسر الهوية والحضور).
        هي القنوات التي تربط عالم الغيب بعالم الشهادة. بدونها، لا يتواصل الخالق مع خلقه.
        
        ### ⚡ الفئة الخامسة: المشغلات
        أربعة حروف: **ف** (= فاء السببية)، **و** (×/+ واو العطف)، **ب** (بـ باء الاستعانة)، **ل** (← لام التعليل).
        هي أدوات المنطق والسببية في كلام الله. تحدد كيف تتفاعل القوى السابقة.
        
        ### 💚 الفئة السادسة: أعمال الخلق
        أحد عشر حرفاً: **ج، خ، د، ذ، ز، ش، ت، ث، ض، ظ، غ**. تمثل صفات وأفعال خاصة بالخلق.
        تحمل وجهين: إيجابي (إذا استُخدمت في الحق) وسلبي (إذا استُخدمت في الباطل).
        قيمها تحددها الإرادة البشرية الحرة.
        """,
        """
        ### 🔮 Category 1: Divine Essence (Source)
        Two letters only: **K** (Command – Be) and **N** (Intrinsic Light). They are the source from which all attributes emanate.
        Their single appearance in Quranic openings indicates uniqueness and oneness.
        **The first equation of existence:** K + N = A (20 + 50 = 70). Command + Light = Perception.
        
        ### ⚖️ Category 2: Duality
        Two letters: **Q** (Balance/Equity) and **S** (Eternal/Patience and Truthfulness). They have two faces: one fixed in the Divine Essence, and one manifested in creation.
        
        ### 🔆 Category 3: Divine Manifestation
        Seven letters: **A, L, M, R, S, H, T**. They represent Allah's attributes manifested in His creation. Their frequent repetition in Quranic openings indicates the multiplicity of manifestations with the unity of the source.
        
        ### 🔄 Category 4: Connection (Bridges)
        Three letters: **A** (Bridge of Perception), **Y** (Bridge of Calling and Belonging), **H** (Bridge of Identity and Presence). They are the channels connecting the Unseen world with the Seen world.
        
        ### ⚡ Category 5: Operators
        Four letters: **F** (= causative Fa), **W** (×/+ conjunctive Waw), **B** (instrumental Ba), **L** (← purpose Lam). They are the tools of logic and causality in Allah's speech.
        
        ### 💚 Category 6: Actions of Creation
        Eleven letters: **J, Kh, D, Dh, Z, Sh, T, Th, D, Dh, Gh**. They represent qualities and actions specific to creation. They carry two faces: positive (when used in truth) and negative (when used in falsehood). Their values are determined by free human will.
        """))

# =============================================
# قاعدة بيانات الشواهد التاريخية الموسعة
# =============================================
HISTORICAL_DATA = {
    TXT("الخلافة الراشدة (٦٣٢-٦٦١م)", "Rashidun Caliphate (632-661 CE)"): {
        "W": 0.95, "B": 0.95, "E": 0.90,
        "era": TXT("عصر النبوة والراشدين", "Era of Prophethood & Rashidun"),
        "desc": TXT(
            "أعلى فترات التوازن في التاريخ الإسلامي. W و B في ذروتهما. الثبات الذاتي (S ≈ 0.90). "
            "التمكين (E) نتاج طبيعي للثبات، لا فجوة استدراج تُذكر.",
            "Highest balance period in Islamic history. W and B at their peak. Self-sustained stability (S ≈ 0.90). "
            "Empowerment (E) a natural product of stability, no significant Istidraj gap."
        ),
        "lessons": TXT(
            "• الإيمان والبراءة متلازمان في النموذج الراشدي.\n• التمكين يتبع الثبات دون تأخير يُذكر.\n• هذا هو 'العصر الذهبي' الذي يُقاس به.",
            "• Faith and disavowal are intertwined in the Rashidun model.\n• Empowerment follows stability without significant delay.\n• This is the 'golden age' by which others are measured."
        )
    },
    TXT("الدولة الأموية – أوج التوسع (٧٢٠م)", "Umayyad – Peak Expansion (720 CE)"): {
        "W": 0.50, "B": 0.40, "E": 0.95,
        "era": TXT("عصر الفتوحات", "Era of Conquests"),
        "desc": TXT(
            "التمكين (E) في ذروته: الامتداد من الصين إلى فرنسا. لكن W و B بدآ في الانخفاض (ضعف الورع، ظهور العصبية). "
            "فجوة استدراج واضحة: E = 0.95 بينما S = 0.20 فقط. الثبات لم يعد ذاتيًا، بل ممتدًا من رصيد الراشدة.",
            "Empowerment (E) at its peak: stretching from China to France. But W and B began declining (weakening piety, tribal partisanship). "
            "Clear Istidraj gap: E = 0.95 while S = 0.20 only. Stability no longer self-sustained, but extended from Rashidun reserves."
        ),
        "lessons": TXT(
            "• التمكين المادي يمكن أن يستمر لعقود بعد انهيار الثبات.\n• هذه هي 'فجوة الاستدراج' بعينها.\n• الاعتماد على 'رصيد السابقين' دون تجديد يؤدي إلى الانهيار.",
            "• Material empowerment can persist for decades after stability collapses.\n• This is the 'Istidraj gap' in action.\n• Relying on 'predecessor reserves' without renewal leads to collapse."
        )
    },
    TXT("الدولة الأموية – قبل السقوط (٧٤٠م)", "Umayyad – Before Fall (740 CE)"): {
        "W": 0.25, "B": 0.20, "E": 0.70,
        "era": TXT("عصر الفتن والانهيار", "Era of Strife & Collapse"),
        "desc": TXT(
            "انهيار شبه كامل في W (ضعف الإيمان، الظلم، الترف) و B (الانغماس في الدنيا، ترك الجهاد). "
            "E ما زال مرتفعًا نسبيًا (0.70) لكنه آخذ في الانهيار. 'استدراج متقدم' ينذر بالسقوط الوشيك.",
            "Near-total collapse in W (weak faith, injustice, luxury) and B (worldly indulgence, abandoning jihad). "
            "E still relatively high (0.70) but beginning to crumble. 'Advanced Istidraj' warning of imminent fall."
        ),
        "lessons": TXT(
            "• عندما يصل S إلى 0.05، يصبح الانهيار مسألة وقت.\n• E ينهار متأخرًا، لكنه ينهار بعنف.\n• هذا هو قانون 'الاستدراج' الإلهي.",
            "• When S reaches 0.05, collapse is only a matter of time.\n• E collapses late, but violently.\n• This is the divine law of 'Istidraj'."
        )
    },
    TXT("الدولة العباسية – العصر الذهبي (٨٠٠م)", "Abbasid – Golden Age (800 CE)"): {
        "W": 0.80, "B": 0.70, "E": 0.85,
        "era": TXT("عصر العلم والحضارة", "Era of Science & Civilization"),
        "desc": TXT(
            "نهضة علمية وحضارية هائلة (W مرتفع بسبب العلم، B مرتفع بسبب القوة). "
            "S = 0.56، و E = 0.85. فجوة استدراج طفيفة، لكنها تحت السيطرة بسبب تجدد W عبر العلم.",
            "Massive scientific and civilizational renaissance (W high due to knowledge, B high due to power). "
            "S = 0.56, E = 0.85. Slight Istidraj gap, but under control due to W renewal through knowledge."
        ),
        "lessons": TXT(
            "• العلم (ع) يجدد W ويؤخر الانهيار.\n• الحضارة تحتاج إلى 'تجديد مستمر' للإيمان.\n• العصر الذهبي ليس 'استقرارًا' بل 'حركة دائمة'.",
            "• Knowledge renews W and delays collapse.\n• Civilization needs 'continuous renewal' of faith.\n• The golden age is not 'stability' but 'constant motion'."
        )
    },
    TXT("الدولة العثمانية – الذروة (١٥٠٠م)", "Ottoman – Peak (1500 CE)"): {
        "W": 0.75, "B": 0.80, "E": 0.90,
        "era": TXT("عصر القوة والعدل", "Era of Power & Justice"),
        "desc": TXT(
            "ذروة القوة العثمانية: فتح القسطنطينية، نظام العدل (W)، الجيش الإنكشاري (B). "
            "توازن جيد بين W و B. E = 0.90 نتاج طبيعي لـ S = 0.60.",
            "Peak Ottoman power: Conquest of Constantinople, justice system (W), Janissary army (B). "
            "Good balance between W and B. E = 0.90 natural product of S = 0.60."
        ),
        "lessons": TXT(
            "• التوازن بين W و B هو سر القوة.\n• 'القانون العثماني' كان محاولة لتطبيق الشريعة (W).\n• الجيش القوي (B) يحمي هذا التوازن.",
            "• Balance between W and B is the secret of power.\n• 'Ottoman law' was an attempt to apply Sharia (W).\n• A strong army (B) protects this balance."
        )
    },
    TXT("الدولة العثمانية – أواخر (١٨٠٠م)", "Ottoman – Late (1800 CE)"): {
        "W": 0.35, "B": 0.25, "E": 0.60,
        "era": TXT("عصر 'الرجل المريض'", "Era of 'The Sick Man'"),
        "desc": TXT(
            "انهيار W (الفساد، الانفصال عن الشريعة) و B (التبعية للغرب، ضعف الجهاد). "
            "E ما زال 0.60 بسبب 'رصيد' الماضي، لكن الدولة تُعرف بـ 'رجل أوروبا المريض'. فجوة استدراج طويلة.",
            "Collapse of W (corruption, separation from Sharia) and B (dependency on the West, weak jihad). "
            "E still 0.60 due to past 'reserves', but the empire is known as 'The Sick Man of Europe'. Long Istidraj gap."
        ),
        "lessons": TXT(
            "• 'الرجل المريض' هو وصف دقيق لحالة الاستدراج.\n• E يبقى مرتفعًا بسبب 'التراكم' لا بسبب 'الصحة'.\n• الانهيار النهائي (1924) كان حتميًا.",
            "• 'The Sick Man' is an accurate description of the Istidraj state.\n• E remains high due to 'accumulation', not 'health'.\n• The final collapse (1924) was inevitable."
        )
    },
    TXT("الاتحاد السوفيتي (١٩٢٢-١٩٩١م)", "Soviet Union (1922-1991 CE)"): {
        "W": 0.05, "B": 0.10, "E": 0.70,
        "era": TXT("عصر الإلحاد الشيوعي", "Era of Communist Atheism"),
        "desc": TXT(
            "W = صفر تقريبًا (إلحاد رسمي). B ضعيف (جيش قوي لكن بلا روح). "
            "E = 0.70 (قوة عظمى ظاهريًا). انهيار مفاجئ وغير متوقع 'كالصاعقة' عام 1991. "
            "أعظم مثال على 'الاستدراج' في التاريخ الحديث.",
            "W ≈ 0 (official atheism). B weak (strong army but soulless). "
            "E = 0.70 (superpower on the surface). Sudden, unexpected collapse 'like lightning' in 1991. "
            "The greatest modern example of 'Istidraj'."
        ),
        "lessons": TXT(
            "• دولة بلا W تنهار فجأة مهما بلغت قوتها.\n• 'الاستدراج' الإلهي يسري على المسلم والكافر.\n• ﴿فَلَمَّا نَسُوا مَا ذُكِّرُوا بِهِ فَتَحْنَا عَلَيْهِمْ أَبْوَابَ كُلِّ شَيْءٍ﴾",
            "• A state without W collapses suddenly, however powerful.\n• Divine 'Istidraj' applies to believer and disbeliever alike.\n• ﴿So when they forgot that by which they had been reminded, We opened to them the doors of every thing.﴾"
        )
    },
}

# =============================================
# تبويب ٥: الشواهد التاريخية
# =============================================
with tab5:
    st.header(TXT("📜 الشواهد التاريخية – حين ينطق التاريخ مصدقًا للمعادلة", "📜 Historical Evidence – When History Bears Witness"))
    st.markdown(TXT(
        "اختر دولة تاريخية لترى كيف تنطبق معادلة الميزان على التاريخ الفعلي. "
        "هذه تقديرات تقريبية مبنية على تحليل historians، والهدف منها أن تريك كيف أن سنة الله في الأمم لا تتبدل ولا تتحول.",
        "Select a historical nation to see how the Mizan equation applies to actual history. "
        "These are approximate estimates based on historical analysis, meant to show you that Allah's law in nations does not change or transform."
    ))
    
    # --- عرض شاهد واحد ---
    selected_nation = st.selectbox(
        TXT("اختر دولة:", "Select a nation:"),
        list(HISTORICAL_DATA.keys())
    )
    
    if selected_nation:
        data = HISTORICAL_DATA[selected_nation]
        W_hist, B_hist, E_hist = data["W"], data["B"], data["E"]
        S_hist = W_hist * B_hist
        gap = E_hist - S_hist
        
        st.markdown(f"### {selected_nation}")
        st.markdown(f"**{data['era']}**")
        st.markdown(data["desc"])
        
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        col_m1.metric("W (الولاء)", f"{W_hist:.2f}")
        col_m2.metric("B (البراءة)", f"{B_hist:.2f}")
        col_m3.metric("S (الثبات)", f"{S_hist:.2f}")
        col_m4.metric("E (التمكين)", f"{E_hist:.2f}")
        col_m5.metric(TXT("فجوة الاستدراج", "Istidraj Gap"), f"{gap:.2f}")
        
        # رسم بياني
        fig_hist, (ax_bar, ax_gauge) = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0a0f1e')
        
        ax_bar.set_facecolor('#0a0f1e')
        categories = ['W (الولاء)', 'B (البراءة)', 'S (الثبات)', 'E (التمكين)']
        values = [W_hist, B_hist, S_hist, E_hist]
        colors_bar = ['#FFD700', '#FF5252', '#00FF88', '#00FFFF']
        bars = ax_bar.bar(categories, values, color=colors_bar, edgecolor='white', linewidth=1.5)
        for bar, val in zip(bars, values):
            ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                       f'{val:.2f}', ha='center', color='white', fontsize=11, fontweight='bold')
        if gap > 0.3:
            ax_bar.annotate(TXT('⚠️ فجوة استدراج خطيرة', '⚠️ Dangerous Istidraj Gap'),
                          xy=(3, E_hist), xytext=(3.5, E_hist + 0.15),
                          arrowprops=dict(arrowstyle='->', color='red', lw=2),
                          color='red', fontsize=11, fontweight='bold')
        ax_bar.set_ylim(0, 1.15)
        ax_bar.set_title(TXT("مؤشرات الدولة", "State Indicators"), color='white', fontsize=13, fontweight='bold')
        ax_bar.tick_params(colors='white')
        ax_bar.grid(True, alpha=0.2, axis='y')
        
        ax_gauge.set_facecolor('#0a0f1e')
        ax_gauge.set_xlim(-1.5, 1.5); ax_gauge.set_ylim(-1.5, 1.5)
        ax_gauge.set_aspect('equal'); ax_gauge.axis('off')
        ax_gauge.add_patch(Rectangle((0, 0), 1.4, 1.4, color='#FFD700', alpha=0.2))
        ax_gauge.add_patch(Rectangle((-1.4, 0), 1.4, 1.4, color='#FF5252', alpha=0.2))
        ax_gauge.add_patch(Rectangle((-1.4, -1.4), 1.4, 1.4, color='#FFB6C1', alpha=0.2))
        ax_gauge.add_patch(Rectangle((0, -1.4), 1.4, 1.4, color='#FFA500', alpha=0.2))
        ax_gauge.axhline(0, color='white', lw=0.5, alpha=0.5)
        ax_gauge.axvline(0, color='white', lw=0.5, alpha=0.5)
        b_pos = (B_hist * 2 - 1) * 1.3
        w_pos = (W_hist * 2 - 1) * 1.3
        ax_gauge.scatter([b_pos], [w_pos], s=400, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
        ax_gauge.scatter([1.3], [1.3], s=150, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, marker='*')
        ax_gauge.text(1.3, 1.4, TXT("إبراهيم", "Abraham"), ha='center', color='#FFD700', fontsize=8)
        ax_gauge.set_title(TXT("الموقع في فضاء (W, B)", "Position in (W, B) Space"), color='white', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig_hist)
        
        # تحليل
        if gap > 0.4:
            st.error(TXT(
                f"⚠️ **حالة استدراج واضحة:** فجوة الاستدراج = {gap:.2f}. "
                "التمكين المادي (E) يفوق الثبات الأخلاقي (S) بكثير. هذا 'الاستدراج' الإلهي الذي حذر منه القرآن.",
                f"⚠️ **Clear Istidraj State:** Istidraj gap = {gap:.2f}. "
                "Material empowerment (E) far exceeds moral stability (S). This is the divine 'Istidraj' warned of in the Quran."
            ))
        elif gap > 0.15:
            st.warning(TXT(
                f"⚡ **فجوة استدراج معتدلة:** فجوة الاستدراج = {gap:.2f}. "
                "هناك تفاوت بين الثبات والتمكين. يُنصح بمراجعة W (الإيمان) و B (البراءة).",
                f"⚡ **Moderate Istidraj Gap:** Istidraj gap = {gap:.2f}. "
                "There is a disparity between stability and empowerment. Reviewing W and B is advised."
            ))
        elif S_hist > 0.7:
            st.success(TXT(
                f"✅ **حالة توازن عالٍ:** S = {S_hist:.2f}. "
                "W و B متوازنتان، والتمكين يتبع الثبات بشكل صحي. هذه علامة أمة 'آمنت واتقت'.",
                f"✅ **High Balance State:** S = {S_hist:.2f}. "
                "W and B are balanced, empowerment follows stability healthily."
            ))
        else:
            st.info(TXT(
                f"ℹ️ **حالة متوسطة:** S = {S_hist:.2f}. "
                "هناك مؤشرات على بداية تراجع. الإصلاح ممكن إذا بُدئ به فورًا.",
                f"ℹ️ **Moderate State:** S = {S_hist:.2f}. "
                "There are signs of beginning decline. Reform is possible if started immediately."
            ))
        
        # الدروس المستفادة
        st.markdown("---")
        st.subheader(TXT("💡 الدروس المستفادة", "💡 Lessons Learned"))
        st.markdown(data["lessons"])
    
    # --- مقارنة بين دولتين ---
    st.markdown("---")
    st.subheader(TXT("🔍 مقارنة بين دولتين", "🔍 Compare Two Nations"))
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        nation_a = st.selectbox(TXT("الدولة الأولى:", "First nation:"), list(HISTORICAL_DATA.keys()), key="nation_a")
    with col_c2:
        nation_b = st.selectbox(TXT("الدولة الثانية:", "Second nation:"), list(HISTORICAL_DATA.keys()), index=min(1, len(HISTORICAL_DATA)-1), key="nation_b")
    
    if nation_a and nation_b:
        data_a = HISTORICAL_DATA[nation_a]
        data_b = HISTORICAL_DATA[nation_b]
        
        fig_comp, ax_comp = plt.subplots(figsize=(10, 6), facecolor='#0a0f1e')
        ax_comp.set_facecolor('#0a0f1e')
        x = np.arange(4); width = 0.35
        labels = ['W', 'B', 'S', 'E']
        values_a = [data_a["W"], data_a["B"], data_a["W"]*data_a["B"], data_a["E"]]
        values_b = [data_b["W"], data_b["B"], data_b["W"]*data_b["B"], data_b["E"]]
        
        bars_a = ax_comp.bar(x - width/2, values_a, width, color='#FFD700', edgecolor='white', linewidth=1.5, label=nation_a[:40])
        bars_b = ax_comp.bar(x + width/2, values_b, width, color='#00BFFF', edgecolor='white', linewidth=1.5, label=nation_b[:40])
        
        for bar in bars_a:
            ax_comp.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', ha='center', color='#FFD700', fontsize=9)
        for bar in bars_b:
            ax_comp.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', ha='center', color='#00BFFF', fontsize=9)
        
        ax_comp.set_xticks(x); ax_comp.set_xticklabels(labels, color='white', fontsize=12)
        ax_comp.set_ylim(0, 1.15)
        ax_comp.set_title(TXT("مقارنة المؤشرات", "Indicator Comparison"), color='white', fontsize=13, fontweight='bold')
        ax_comp.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=10)
        ax_comp.tick_params(colors='white')
        ax_comp.grid(True, alpha=0.2, axis='y')
        plt.tight_layout()
        st.pyplot(fig_comp)
        
        S_a = data_a["W"] * data_a["B"]
        S_b = data_b["W"] * data_b["B"]
        gap_a = data_a["E"] - S_a
        gap_b = data_b["E"] - S_b
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"**{nation_a[:50]}**")
            st.markdown(f"- S = {S_a:.2f}")
            st.markdown(f"- {TXT('فجوة الاستدراج', 'Istidraj gap')}: {gap_a:.2f}")
            if gap_a > 0.3: st.warning(TXT("حالة استدراج", "Istidraj state"))
            else: st.success(TXT("حالة متوازنة", "Balanced state"))
        with col_r2:
            st.markdown(f"**{nation_b[:50]}**")
            st.markdown(f"- S = {S_b:.2f}")
            st.markdown(f"- {TXT('فجوة الاستدراج', 'Istidraj gap')}: {gap_b:.2f}")
            if gap_b > 0.3: st.warning(TXT("حالة استدراج", "Istidraj state"))
            else: st.success(TXT("حالة متوازنة", "Balanced state"))
    
    st.markdown("---")
    st.markdown(TXT("""
    <div style="text-align:center;padding:20px;background:rgba(20,30,60,0.7);border-radius:15px;border:1px solid #FFD700;">
        <p style="color:#FFD700;font-size:1.1em;">﴿وَتِلْكَ الْأَيَّامُ نُدَاوِلُهَا بَيْنَ النَّاسِ﴾</p>
        <p style="color:#AAA;">هذه التقديرات اجتهادية، والهدف منها التدبر في السنن الإلهية، لا الإحاطة بالغيب.</p>
    </div>
    """, """
    <div style="text-align:center;padding:20px;background:rgba(20,30,60,0.7);border-radius:15px;border:1px solid #FFD700;">
        <p style="color:#FFD700;font-size:1.1em;">﴿And these days We alternate among the people.﴾</p>
        <p style="color:#AAA;">These estimates are interpretive, aimed at reflecting on divine laws, not claiming certainty.</p>
    </div>
    """), unsafe_allow_html=True)

print("✅ المرحلة الرابعة مكتملة: المعجم الهندسي الكامل، الشواهد التاريخية الموسعة")

# =============================================
# المرحلة الخامسة: هندسة الصراط والتذييل
# =============================================

# --- الثوابت الإبراهيمية ---
ABRAHAMIC_VERSE = TXT(
    '﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ وَالَّذِينَ مَعَهُ إِذْ قَالُوا لِقَوْمِهِمْ إِنَّا بُرَآءُ مِنكُمْ وَمِمَّا تَعْبُدُونَ مِن دُونِ اللَّهِ كَفَرْنَا بِكُمْ وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾',
    '﴿There has certainly been for you an excellent pattern in Abraham and those with him, when they said to their people, "Indeed, we are disassociated from you and from whatever you worship other than Allah. We have denied you, and there has appeared between us and you animosity and hatred forever until you believe in Allah alone."﴾'
)

def get_spiritual_nudge(situation):
    if situation == "approaching":
        return TXT(
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
        return TXT(
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
        return TXT(
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
        return TXT(
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
    st.header(TXT("📐 هندسة الصراط – البرهان النبوي والنموذج الإبراهيمي", "📐 Path Geometry – Prophetic Proof & Abrahamic Model"))
    
    # --- البرهان النبوي ---
    st.markdown(TXT("""
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
        <p style="color:#FFD700;font-size:1.3em;font-weight:bold;">S = W x B</p>
        <p style="color:#AAA;">
            Love for Allah = W. Hatred for Allah = B.<br>
            The firmest handhold = S. Completed faith = S=1.<br>
            The "and" is multiplication (x), because faith is only complete with both together.
        </p>
    </div>
    """), unsafe_allow_html=True)
    
    # --- شرح النموذج الإبراهيمي ---
    st.markdown(TXT("""
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
    
    # --- التأكد من تهيئة متغيرات المسار ---
    if 'path_W' not in st.session_state:
        st.session_state.path_W = [0.5]
    if 'path_B' not in st.session_state:
        st.session_state.path_B = [0.5]
    if 'path_kappa' not in st.session_state:
        st.session_state.path_kappa = [0.0]
    if 'spiritual_nudge' not in st.session_state:
        st.session_state.spiritual_nudge = None
    
    # --- أزرار التفاعل ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button(TXT("▶️ خطوة نحو الكمال", "▶️ Step Toward Perfection"), key="btn_path", use_container_width=True):
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
        sin_str = st.slider(TXT("⚡ شدة المعصية", "⚡ Sin Strength"), 0.01, 0.3, 0.1, 0.01, key="sin_path")
        if st.button(TXT("⚠️ معصية", "⚠️ Sin"), key="btn_sin", use_container_width=True):
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
        if st.button(TXT("🕌 توبة نصوح", "🕌 Sincere Repentance"), key="btn_rep", use_container_width=True):
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
    if st.session_state.spiritual_nudge:
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.9);border-radius:12px;padding:20px;border:1px solid #FFD700;margin:15px 0;text-align:center;line-height:2.2;'>
            <p style='color:#FFD700;font-size:1.1em;margin:0;white-space:pre-line;'>{st.session_state.spiritual_nudge}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- زر إعادة ---
    if st.button(TXT("🔄 إعادة الرحلة", "🔄 Reset Path"), key="btn_reset_path", use_container_width=True):
        st.session_state.path_W = [0.5]
        st.session_state.path_B = [0.5]
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
    ax1.set_title(TXT("مسارك في فضاء (W, B) – النموذج الإبراهيمي", "Your Path in (W, B) Space"), color='white', fontsize=13)
    
    ax1.plot([0.5, 1], [0.5, 1], '--', color='#FFD700', lw=3, alpha=0.8, 
             label=TXT("✦ مسار إبراهيم (κ = 0)", "✦ Abraham's Path"))
    ax1.scatter([1], [1], s=200, c='#FFD700', edgecolors='white', linewidth=3, zorder=10, 
                label=TXT("⭐ مقام إبراهيم (1,1)", "⭐ Station of Abraham"))
    
    if len(pW) > 1:
        for i in range(1, len(pW)):
            kv = st.session_state.path_kappa[i] if i < len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv < 0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1], pW[i-1:i+1], color=cl, lw=2)
        ax1.scatter([pB[0]], [pW[0]], s=80, c='white', edgecolors='cyan', linewidth=2, zorder=10, label=TXT("البداية", "Start"))
        ax1.scatter([pB[-1]], [pW[-1]], s=120, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10, label=TXT("الآن", "Now"))
    
    ax1.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8, loc='lower right')
    ax1.grid(True, alpha=0.2); ax1.tick_params(colors='white')
    
    ax2 = axes[1]
    ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.path_kappa, color='#FFD700', lw=2, marker='o', markersize=3)
    ax2.axhline(y=0.05, color='#FF4444', linestyle='--', alpha=0.6, label=TXT("حد الخطر", "Danger"))
    ax2.axhline(y=0.0, color='#00FF88', linestyle='--', alpha=0.4, label=TXT("الصراط (κ=0)", "Straight Path"))
    ax2.set_title(TXT("منحنى الانحناء (κ)", "Curvature Over Time"), color='white', fontsize=13)
    ax2.set_xlabel(TXT("الخطوات", "Steps"), color='white'); ax2.set_ylabel("κ", color='white')
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
    c4.metric(TXT("الصراط؟", "On Path?"), TXT("✅ نعم", "✅ YES") if on_path else TXT("⚠️ لا", "⚠️ NO"))
    
    dist_to_abraham = np.sqrt((1 - pW[-1])**2 + (1 - pB[-1])**2)
    st.markdown(f"""
    <div style='text-align:center;padding:15px;background:rgba(20,30,60,0.8);border-radius:10px;border:1px solid #FFD700;'>
        <p style='color:#FFD700;font-size:1em;margin:0;'>
            {TXT(f'📏 المسافة إلى مقام إبراهيم: {dist_to_abraham:.3f}', f'📏 Distance to Station of Abraham: {dist_to_abraham:.3f}')}
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
    <p style="font-size:1.1em;">{TXT('سفينة نوح الرقمية – القانون الواحد من الذرة إلى الحضارة', 'The Digital Ark – The One Law from Atom to Civilization')}</p>
    <p style="color:#FFD700;font-size:1.3em;">S = W x B</p>
    <p>ق = ١٠٠ = الحق = الميزان</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size:0.8em;margin-top:15px;">
        {TXT(
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

print("✅ المرحلة الخامسة مكتملة: هندسة الصراط الكاملة والتذييل")
print("✅✅✅ تم بناء المنصة الذهبية – الدين القيم – المنارة العالمية بنجاح!")
