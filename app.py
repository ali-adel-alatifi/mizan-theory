import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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
st.set_page_config(page_title="⚖️ الدين القيم – المنارة العالمية", page_icon="⚖️", layout="wide")

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
    {"ar": "الولاء لله ورسوله والمؤمنين", "en": "Loyalty", "letter": "أ", "val": 1},
    {"ar": "تحكيم الشريعة (تحكيم/رفض)", "en": "Applying Sharia", "letter": "ل", "val": 30},
    {"ar": "العدل (عدل/ظلم)", "en": "Justice", "letter": "ق", "val": 100},
    {"ar": "الشورى (تشاور/استبداد)", "en": "Consultation", "letter": "م", "val": 40},
    {"ar": "البراءة من الطاغوت (براءة/موالاة)", "en": "Disavowal of Taghut", "letter": "هـ", "val": 5},
    {"ar": "الرحمة والعطاء – الماعون (رحمة/قسوة)", "en": "Mercy & Giving", "letter": "ح", "val": 8},
    {"ar": "الأمر بالمعروف (أمر/نهي)", "en": "Enjoining Good", "letter": "ف", "val": 80},
    {"ar": "النهي عن المنكر (نهي/أمر)", "en": "Forbidding Evil", "letter": "و", "val": 6},
    {"ar": "النزاهة ومكافحة الفساد", "en": "Integrity", "letter": "ب", "val": 2},
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
# بوصلة الإسلام الحنيف – الأسئلة الأصلية الكاملة (19 سؤالاً)
# =============================================
COMPASS_DATA = [
    {"id":1,"topic":T("القوانين الوضعية وتحكيم الشريعة","Man-Made Laws vs. Sharia"),"letter":"ق","value":100,
     "text":T("في زمن سيادة القوانين الوضعية، وشعار 'الدين لله والوطن للجميع'، كمسلم: ما هو موقفك من تحكيم شرع الله؟","In an age of man-made laws..."),
     "answers":[(T("تحكيم شرع الله هو الصحيح، وأبذل كل ما أستطيع لتطبيقه","I strive to apply Sharia"),0.4,0.6),
                (T("أتمنى تطبيق الشريعة، لكني لا أعمل لأجلها","I wish but don't act"),0.2,-0.1),
                (T("أرى أن بعض أحكام الشريعة صالحة وبعضها غير صالح","Some valid, some not"),-0.1,-0.2),
                (T("الشريعة الإسلامية لم تعد تصلح لهذا العصر","Sharia unsuitable"),-0.3,-0.4)]},
    {"id":2,"topic":T("الولاء للعرق والحزب والطائفة","Loyalty to Race, Party, Sect"),"letter":"أ","value":1,
     "text":T("في عصر أصبح فيه الولاء للعرق والحزب والطائفة والمذهب هو المعيار، كمسلم: ما هو موقفك؟","In an age of racial loyalty..."),
     "answers":[(T("ولائي لله ورسوله والمؤمنين فوق كل رابطة، وأتبرأ من العصبيات الجاهلية","My loyalty is to Allah"),0.7,0.3),
                (T("أحاول أن أوازن بين ولائي للإسلام وانتمائي العرقي أو الحزبي","I try to balance"),0.3,-0.2),
                (T("ولائي لديني ضعيف، وأميل للفخر بعرقي أو حزبي أكثر","Weak religious loyalty"),-0.2,0.1),
                (T("لا أرى مشكلة في تقديم العرق أو الحزب على الدين، فهذا واقع العصر","Race over religion"),-0.5,-0.3)]},
    {"id":3,"topic":T("الاستهزاء بالمقدسات وحرية التعبير","Mockery of Sanctities"),"letter":"هـ","value":5,
     "text":T("في زمن تُباح فيه 'حرية التعبير' للاستهزاء بالدين والمقدسات، كمسلم: ما هو موقفك؟","In an age of free speech..."),
     "answers":[(T("أبغض في الله المستهزئين، وأدين فعلهم بكل وضوح","I hate and condemn mockers"),0.3,0.7),
                (T("أستنكر الاستهزاء في قلبي، لكني لا أعلن موقفي جهارًا","I disapprove in heart"),0.1,-0.1),
                (T("أرى أنها 'حرية رأي' ولا داعي للغضب","Free speech, no anger"),-0.2,0.1),
                (T("أضحك معهم أحيانًا، ولا أرى في ذلك ضررًا كبيرًا","I laugh with them"),-0.3,-0.3)]},
    {"id":4,"topic":T("الربا والنظام المالي العالمي","Usury and Global Finance"),"letter":"ص","value":90,
     "text":T("في زمن يقوم فيه النظام المالي العالمي على الربا، وأصبح التعامل بالفوائد 'أمرًا طبيعيًا'، كمسلم: ما هو موقفك؟","In an age of usury..."),
     "answers":[(T("أتجنب الربا بكل صوره وأبحث عن البدائل الإسلامية ولو خسرت ربحًا","I avoid all usury"),0.3,0.7),
                (T("أكره الربا، لكني مضطر للتعامل به أحيانًا بحكم الواقع","I hate it but forced"),0.1,-0.2),
                (T("أتعامل بالربا كالجميع، ولا أرى مشكلة حقيقية في ذلك","I deal with it like everyone"),-0.2,0.1),
                (T("الربا ضرورة اقتصادية، وتحريمه كان لزمن غير زمننا","Usury is a necessity"),-0.3,-0.3)]},
    {"id":5,"topic":T("العلمانية وفصل الدين عن الدولة","Secularism"),"letter":"ك","value":20,
     "text":T("في زمن تسود فيه العلمانية، وتُرفع شعارات 'فصل الدين عن الدولة'، كمسلم: ما هو موقفك؟","In an age of secularism..."),
     "answers":[(T("أرفض العلمانية، وأؤمن أن الإسلام دين ودولة وشريعة تحكم كل الحياة","I reject secularism"),0.4,0.6),
                (T("أرى أن العلمانية قد تكون حلاً مؤقتًا لحين استعداد المجتمع","Temporary solution"),0.1,-0.1),
                (T("لا أمانع فصل الدين عن السياسة، فالدين علاقة شخصية بالله","I don't mind separation"),-0.2,0.1),
                (T("العلمانية هي الطريق الصحيح للتقدم، والدين يجب أن يبقى في المسجد فقط","Secularism is correct"),-0.3,-0.3)]},
    {"id":6,"topic":T("إقامة الحدود الشرعية","Sharia Penalties"),"letter":"ح","value":8,
     "text":T("في زمن تُلغى فيه الحدود الشرعية (كقطع يد السارق ورجم الزاني) بدعوى 'الهمجية' و'عدم الإنسانية'، كمسلم: ما هو موقفك؟","In an age of abolishing penalties..."),
     "answers":[(T("الحدود الشرعية رحمة وعدل، وأؤمن بضرورة إقامتها لحماية المجتمع","Penalties are mercy and justice"),0.3,0.7),
                (T("الحدود حق، لكن الظروف الحالية لا تسمح بتطبيقها","Right but conditions hard"),0.1,-0.1),
                (T("أشعر بالحرج من بعض الحدود، وأراها قاسية","I feel embarrassed"),-0.2,0.1),
                (T("الحدود الشرعية همجية ولا تصلح للعصر الحديث","Penalties are barbaric"),-0.3,-0.3)]},
    {"id":7,"topic":T("الإلحاد وإنكار الخالق","Atheism"),"letter":"ن","value":50,
     "text":T("في زمن ينتشر فيه الإلحاد، ويُقدَّم العلم على أنه ينفي وجود الله، كمسلم: ما هو موقفك؟","In an age of atheism..."),
     "answers":[(T("أؤمن بالله يقينًا لا يتزعزع، وأرى في العلم دليلاً على وجوده","I believe in Allah certainly"),0.4,0.6),
                (T("أؤمن بالله، لكني لا أملك حججًا للرد على شبهات الملحدين","I believe but lack arguments"),0.1,-0.1),
                (T("تساورني أحيانًا شكوك، لكني أعود للإيمان","Doubts sometimes cross my mind"),-0.2,0.1),
                (T("أعتقد أن الإلحاد طرح فكري يحترم، والدين مجرد أساطير","Atheism is respectable"),-0.3,-0.3)]},
    {"id":8,"topic":T("الجهاد ونصرة المستضعفين","Jihad"),"letter":"ر","value":200,
     "text":T("في زمن يُشوَّه فيه الجهاد ويوصم بـ 'الإرهاب'، ويُخذل فيه المستضعفون من المسلمين، كمسلم: ما هو موقفك؟","In an age of distorting jihad..."),
     "answers":[(T("الجهاد ذروة سنام الإسلام، وأتمنى أن أكون في صفوف المجاهدين لنصرة المستضعفين","Jihad is the peak"),0.3,0.7),
                (T("الجهاد حق، وأدعمه بقلبي ومالي إن استطعت، لكني لا أقاتل الآن","Jihad is right, I support"),0.1,-0.1),
                (T("أخشى من الجهاد، وأرى أنه يجلب المشاكل للمسلمين","I fear jihad"),-0.2,0.1),
                (T("الجهاد أصبح إرهابًا، ولا مكان له في هذا العصر","Jihad became terrorism"),-0.3,-0.3)]},
    {"id":9,"topic":T("حقوق المرأة بين الإسلام والتغريب","Women's Rights"),"letter":"هـ","value":5,
     "text":T("في زمن تُطرح فيه 'حقوق المرأة' بصيغة غربية تنتزعها من فطرتها، وتُتهم الشريعة بظلمها، كمسلم: ما هو موقفك؟","In an age of women's rights..."),
     "answers":[(T("أؤمن أن الإسلام كرم المرأة ورفع شأنها، وأن أحكامه هي عين العدل","Islam honored women"),0.4,0.6),
                (T("أؤمن بالإسلام، لكني أرى ضرورة 'تحديث' بعض الأحكام لتواكب العصر","I believe but need update"),0.1,-0.1),
                (T("أشعر بالحرج من بعض أحكام الإسلام الخاصة بالمرأة","Embarrassed by some rulings"),-0.2,0.1),
                (T("أعتقد أن الإسلام ظلم المرأة، وأن تحريرها يكون بالعلمانية","Islam oppressed women"),-0.3,-0.3)]},
    {"id":10,"topic":T("العولمة، الذوبان الحضاري، الموضة، والاستهلاك","Globalization & Fashion"),"letter":"م","value":40,
     "text":T("في زمن العولمة التي تسعى لطمس الهويات... وتحول فيه الاستهلاك إلى ثقافة... والموضة العالمية تفرض أزياء تخالف الفطرة... كمسلم: ما هو موقفك؟","In an age of globalization..."),
     "answers":[(T("أتمسك بهويتي الإسلامية، وأتبرأ من تقليد الكفار... وأزهد في الدنيا...","I hold fast to my Islamic identity..."),0.4,0.6),
                (T("أحاول أن أوازن... وأوفق بين التمتع بالحلال والزهد","I try to balance"),0.1,-0.1),
                (T("أقلد الغرب في كثير من ثقافته وأزيائه واستهلاكه...","I imitate the West..."),-0.2,0.1),
                (T("الثقافة الغربية هي ثقافة التقدم... والحياة فرصة للاستمتاع...","Western culture is progress..."),-0.3,-0.3)]},
    {"id":11,"topic":T("الديمقراطية والتشريع","Democracy"),"letter":"ل","value":30,
     "text":T("في زمن تُقدَّس فيه الديمقراطية وتُجعل الشعب هو مصدر التشريع، كمسلم: ما هو موقفك؟","In an age of democracy..."),
     "answers":[(T("أرفض جعل الشعب مشرعًا، فالتشريع لله وحده، والشورى لا تعني الالتفاف على الشرع...","I reject people as legislators..."),0.4,0.6),
                (T("أرى أن الديمقراطية وسيلة يمكن استخدامها لتحقيق بعض المصالح","Democracy is a tool"),0.1,-0.1),
                (T("أفضّل النظام الديمقراطي على الأنظمة الاستبدادية","I prefer democracy over dictatorship"),-0.2,0.1),
                (T("الديمقراطية هي أفضل نظام حكم، والشريعة لا تصلح للتطبيق السياسي","Democracy is best"),-0.3,-0.3)]},
    {"id":12,"topic":T("التعددية الدينية","Religious Pluralism"),"letter":"ي","value":10,
     "text":T("في زمن تُطرح فيه 'التعددية الدينية' على أنها تعني أن كل الأديان طرق للخلاص، كمسلم: ما هو موقفك؟","In an age of pluralism..."),
     "answers":[(T("الإسلام هو الدين الوحيد المقبول عند الله، ومن لم يؤمن به فهو خاسر في الآخرة","Islam is the only accepted religion"),0.4,0.6),
                (T("الإسلام هو الحق، لكني لا أحكم على أصحاب الديانات الأخرى","Islam is truth but I don't judge"),0.1,-0.1),
                (T("أرى أن كل الأديان فيها جزء من الحق","All religions have truth"),-0.2,0.1),
                (T("كل الأديان سواء، ولا يحق لأحد أن يدعي امتلاك الحقيقة المطلقة","All religions are equal"),-0.3,-0.3)]},
    {"id":13,"topic":T("الحب في الله والبغض في الله","Love & Hatred for Allah"),"letter":"ق","value":100,
     "text":T("في زمن أصبحت فيه المصلحة هي المعيار الأساسي في العلاقات، واختفى معنى 'الحب في الله والبغض في الله'، كمسلم: ما هو موقفك؟","In an age of interests..."),
     "answers":[(T("أحب في الله أولياءه وأبغض في الله أعداءه، وهذا أوثق عرى إيماني، ولا أجعل مصلحتي فوق هذا","I love and hate for Allah"),0.4,0.6),
                (T("أحاول، لكن علاقاتي تغلب عليها المصالح والمنافع أحيانًا","I try but interests dominate"),0.1,-0.1),
                (T("أتعامل مع الجميع بالمثل، لا حب ولا بغض في الله، فالمصلحة هي الأساس","I deal equally with all"),-0.2,0.1),
                (T("علاقاتي كلها تقوم على مصلحتي الشخصية، ولا دخل للدين فيها","My relationships are interests only"),-0.3,-0.3)]},
    {"id":14,"topic":T("التحلي بالأخلاق الحميدة – الكذب والغش والخيانة","Noble Character"),"letter":"ط","value":9,
     "text":T("في زمن أصبح الخداع والكذب والغش ذكاءً، وخان الناس الأمانات والعهود، كمسلم: ما هو موقفك من الصدق والأمانة والوفاء؟","In an age of deception..."),
     "answers":[(T("الصدق والأمانة والوفاء دين، وألتزم بها ولو خسرت دنيويًا، ولا أخون ولا أغش ولا أكذب","Truthfulness is my religion"),0.4,0.6),
                (T("أحاول الالتزام بها، لكني قد أضطر للكذب أو التغاضي عن بعض الأمانات أحيانًا","I try but may be forced"),0.1,-0.1),
                (T("أرى أن المبالغة في الصدق سذاجة، والواقع يفرض بعض 'المرونة' في الكذب والغش","Excessive honesty is naivety"),-0.2,0.1),
                (T("الكذب والغش والخيانة أدوات ضرورية للنجاح في هذا العصر","Lying and fraud are success tools"),-0.3,-0.3)]},
    {"id":15,"topic":T("الغيرة على المحارم والأمر بالمعروف","Protective Jealousy"),"letter":"ب","value":2,
     "text":T("في زمن انتشرت فيه الفواحش، وصار إنكار المنكر 'تطرفًا'، كمسلم: ما هو موقفك من الأمر بالمعروف والنهي عن المنكر؟","In an age of indecency..."),
     "answers":[(T("آمر بالمعروف وأنهى عن المنكر بكل استطاعتي، فهذا واجبي","I enjoin and forbid as much as I can"),0.3,0.7),
                (T("أنكر بقلبي، وأحيانًا بلساني إذا لم أخف ضررًا كبيرًا","I reject in my heart sometimes"),0.1,-0.1),
                (T("أسكت عن المنكر حفاظًا على علاقاتي ومصالحي","I remain silent for my interests"),-0.2,0.1),
                (T("لا داعي للأمر والنهي، فكل إنسان حر في تصرفاته","No need for enjoining/forbidding"),-0.3,-0.3)]},
    {"id":16,"topic":T("الوطنية والحزبية والمذهبية","Patriotism, Partisanship"),"letter":"ف","value":80,
     "text":T("في زمن تُقدَّس فيه الوطنية والحزبية والمذهبية، ويُرفع شعار 'الوطن أو الحزب أو المذهب أولاً'، كمسلم: ما هو موقفك؟","In an age of sanctifying patriotism..."),
     "answers":[(T("ولائي للإسلام فوق كل وطن وحزب ومذهب، وأتبرأ من كل دعوة جاهلية تفرق المسلمين","My loyalty to Islam above all"),0.4,0.6),
                (T("أحب وطني وحزبي ومذهبي، لكني أقدّم الإسلام عليها","I love my country but prioritize Islam"),0.1,-0.1),
                (T("أشعر أن انتمائي لوطني أو حزبي أو مذهبي أهم من انتمائي للإسلام","My national belonging is more important"),-0.2,0.1),
                (T("لا أرى مشكلة في تقديم الوطن أو الحزب أو المذهب على الدين، فهذا واقع العصر","No problem with nationalism"),-0.3,-0.3)]},
    {"id":17,"topic":T("الصلاة في زمن الانشغال","Prayer in an Age of Busyness"),"letter":"ن","value":50,
     "text":T("في زمن تزدحم فيه الحياة، وتتسارع فيه الأيام، وأصبحت الصلاة 'عبئًا' على البعض، كمسلم: ما هو موقفك؟","In an age of busyness..."),
     "answers":[(T("الصلاة راحتي وقرة عيني، ولا أتركها مهما كنت مشغولاً","Prayer is my comfort, I never leave it"),0.4,0.6),
                (T("أصلي لكني أؤخرها أو أستعجل فيها أحيانًا","I pray but sometimes delay"),0.1,-0.1),
                (T("أصلي أحيانًا وأتركها أحيانًا، حسب الظروف","I pray sometimes and leave sometimes"),-0.2,0.1),
                (T("لا أجد وقتًا للصلاة، وأراها غير عملية في هذا العصر","I find no time for prayer"),-0.3,-0.3)]},
    {"id":18,"topic":T("الصوم في زمن الشهوات","Fasting in an Age of Desires"),"letter":"ط","value":9,
     "text":T("في زمن تحاصر فيه الشهوات الإنسان من كل جانب، وأصبح الصوم 'تقييدًا للحرية'، كمسلم: ما هو موقفك؟","In an age of desires..."),
     "answers":[(T("أصوم الفرض والنفل، وأراه دورة تدريبية على تقوى الله","I fast obligatory and voluntary"),0.4,0.6),
                (T("أصوم الفرض فقط، ولا أستطيع صيام النفل","I fast only obligatory"),0.1,-0.1),
                (T("أصوم رمضان كعادة اجتماعية، ولا أشعر بروحانيته","I fast Ramadan as a habit"),-0.2,0.1),
                (T("لا أصوم، وأرى أن العصر لا يتناسب مع فكرة الصيام","I don't fast"),-0.3,-0.3)]},
    {"id":19,"topic":T("الزكاة والصدقة في زمن الأنانية","Zakat & Charity in Selfishness"),"letter":"ط","value":9,
     "text":T("في زمن طغت فيه الأنانية، وضعف فيه التكافل، وأصبح المال 'إلهًا'، كمسلم: ما هو موقفك من الزكاة والصدقة؟","In an age of selfishness..."),
     "answers":[(T("أؤدي الزكاة طيبة بها نفسي، وأعترف أن المال مال الله، وفيها طهارة لنفسي وعونًا لإخوتي","I pay Zakat willingly"),0.4,0.6),
                (T("أؤدي الزكاة فقط، وأحيانًا أتصدق","I pay only Zakat"),0.1,-0.1),
                (T("أخرج الزكاة بخلاً، وأشعر أنها 'ضريبة'","I pay Zakat grudgingly"),-0.2,0.1),
                (T("لا أزكي، فالمال مالي ولا دخل لأحد فيه","I don't pay Zakat"),-0.3,-0.3)]},
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

# =============================================
# الشريط الجانبي
# =============================================
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:8px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <p style='font-size:2em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:0;'>{T('الدِّينُ الْقَيِّم','Al-Deen Al-Qayyim')}</h2>
        <p style='color:#e0e0e0;font-size:10px;'>{T('المنارة العالمية','The Global Beacon')}</p>
        <p style='color:#FFD700;font-size:14px;font-weight:bold;'>S = W x B</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(T("🇬🇧 English","🇸🇦 العربية"), use_container_width=True):
        st.session_state.lang = "en" if L == "ar" else "ar"
        st.rerun()
    st.markdown("---")
    st.markdown(f"### {T('⚙️ إعدادات عامة','⚙️ General Settings')}")
    lag = st.select_slider(T("فجوة الاستدراج","Istidraj Gap"), options=[5,10,15,22,30,40,50], value=22, key="lag")
    st.markdown("---")
    good = st.session_state.get('good',0); bad = st.session_state.get('bad',0)
    balance = good - bad
    if balance > 0: status, color = T("⚖️ راجحة","⚖️ Winning"), '#FFD700'
    elif balance < 0: status, color = T("⚖️ خاسرة","⚖️ Losing"), '#FF4444'
    else: status, color = T("⚖️ متوازنة","⚖️ Balanced"), '#888'
    st.sidebar.markdown(f"""
    <div style="text-align:center;padding:10px;background:rgba(10,15,30,0.9);border-radius:10px;border:1px solid #FFD700;">
        <p style="color:#FFD700;font-size:0.8em;">📜 {T('الميزان الحي','Live Scales')}</p>
        <p style="color:#FFD700;font-size:0.7em;">{T('حسنات','Good')}: {good:.0f} | {T('سيئات','Bad')}: {bad:.0f}</p>
        <p style="color:{color};font-size:0.9em;font-weight:bold;">{status}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button(T("🔄 إعادة ضبط كل شيء","🔄 Full Reset"), use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

# =============================================
# رسالة الترحيب
# =============================================
with st.expander(T("📜 رسالة ترحيب","📜 Welcome Message"), expanded=True):
    st.markdown(f"""
    <div class="message-box">
    <h2 style="text-align:center;color:#FFD700;">⚖️ {T('مختبر الميزان','The Mizan Lab')}</h2>
    <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;">"{T('هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟','Is there a single law?')}"</p>
    <p>{T('هذا مختبر...','This is a lab...')}</p>
    <p>{T('تأمل معي: الذرةُ في داخلها قوتان...','Reflect with me...')}</p>
    <p>{T('وحتى في عالم الكيمياء...','Even in chemistry...')}</p>
    <p>{T('والمجتمع: ولاءٌ يجمع أفراده...','And society...')}</p>
    <p style="color:#FFD700;font-weight:bold;">{T('هل هذه مصادفة؟','Is this coincidence?')}</p>
    <p style="text-align:center;color:#FFD700;font-size:1.2em;">S = W x B</p>
    <p>{T('W: الولاء لله... B: البراءة...','W: Loyalty... B: Disavowal...')}</p>
    <p style="text-align:center;font-style:italic;color:#AAA;">{T('جرب. تأمل. واسأل.','Try. Reflect. Ask.')}</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# العنوان الرئيسي
# =============================================
col_icon1, col_title, col_icon2 = st.columns([1,6,1])
with col_icon1: st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#CCC;'>{T('القانون الواحد من الذرة إلى الحضارة','The One Law')}</p>", unsafe_allow_html=True)
with col_icon2: st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
st.markdown("<div class='verse-text'>﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾<br>S = W x B | ق = ١٠٠ = الحق = الميزان</div>", unsafe_allow_html=True)
c1,c2,c3 = st.columns([1,2,1])
with c2:
    if st.button("English" if L=="ar" else "العربية", use_container_width=True):
        st.session_state.lang = "en" if L=="ar" else "ar"
        st.rerun()
st.markdown("---")

# =============================================
# التبويبات
# =============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    T("🧍 بوصلة الإسلام الحنيف","🧍 Compass"),
    T("🏛️ مختبر الأمة","🏛️ Nation Lab"),
    T("🌌 المشهد الكوني","🌌 Cosmic Scene"),
    T("📖 المعجم الهندسي","📖 Lexicon"),
    T("📜 الشواهد","📜 Evidence"),
    T("📐 هندسة الصراط","📐 Path")
])

# --- تبويب ١: البوصلة ---
with tab1:
    st.header(T("🧍 بوصلة الإسلام الحنيف – اكتشف موقعك بدقة","🧍 Compass"))
    if 'compass_answers' not in st.session_state: st.session_state.compass_answers = {}
    for q in COMPASS_DATA:
        with st.expander(f"**{q['id']}. {q['topic']}**  [{q['letter']}={q['value']}]"):
            st.markdown(f"*{q['text']}*")
            key = f"q_{q['id']}"
            ans = st.radio(T("اختر:","Choose:"), [a[0] for a in q['answers']], key=key, index=None)
            if ans is not None:
                idx = [a[0] for a in q['answers']].index(ans)
                st.session_state.compass_answers[key] = idx
    if len(st.session_state.compass_answers) == 19:
        W_raw, B_raw, S_score = compute_compass(st.session_state.compass_answers)
        if W_raw>=0.5 and B_raw>=0.5: q_name, q_color = T("مؤمن","Believer"), '#FFD700'
        elif W_raw<0.5 and B_raw>=0.5: q_name, q_color = T("كافر","Disbeliever"), '#FF5252'
        elif W_raw<0.5 and B_raw<0.5: q_name, q_color = T("منافق","Hypocrite"), '#FFB6C1'
        else: q_name, q_color = T("مشرك","Polytheist"), '#FFA500'
        st.divider()
        c1,c2,c3=st.columns(3)
        c1.metric("W",f"{W_raw:+.2f}"); c2.metric("B",f"{B_raw:+.2f}"); c3.metric("S",f"{S_score:.2f}")
        st.markdown(f"<h2 style='color:{q_color};text-align:center;'>{q_name}</h2>", unsafe_allow_html=True)
        fig,ax=plt.subplots(figsize=(5,5),facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e'); ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
        ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
        ax.fill_between([0,1.2],0,1.2,color='#FFD700',alpha=0.3); ax.fill_between([-1.2,0],0,1.2,color='#FF5252',alpha=0.2)
        ax.fill_between([-1.2,0],-1.2,0,color='#FFB6C1',alpha=0.2); ax.fill_between([0,1.2],-1.2,0,color='#FFA500',alpha=0.2)
        ax.scatter(B_raw,W_raw,s=200,c='cyan',edgecolors='white',linewidth=2,zorder=10)
        ax.scatter(1,1,s=80,c='#FFD700',marker='*',zorder=10)
        ax.text(1,1.1,T('إبراهيم','Abraham'),color='#FFD700',fontsize=7,ha='center')
        ax.tick_params(colors='white'); st.pyplot(fig)
        if st.button(T("🔄 إعادة","🔄 Retake")): st.session_state.compass_answers={}; st.rerun()

# --- تبويب ٢: مختبر الأمة (مع الذكاء الاصطناعي) ---
with tab2:
    st.header(T("🏛️ مختبر الأمة","🏛️ Nation Lab"))
    with st.expander(T("🎛️ مؤشرات الطاقة الروحية","🎛️ Indicators"), expanded=True):
        for i in range(0,N_IND,2):
            ca,cb=st.columns(2)
            with ca:
                if i<N_IND:
                    val=st.slider(get_indicator_label(i),-1.0,1.0,st.session_state.slider_values.get(f"V{i}",0.0),0.1,key=f"lab_{i}")
                    st.session_state.slider_values[f"V{i}"]=val
            with cb:
                if i+1<N_IND:
                    val=st.slider(get_indicator_label(i+1),-1.0,1.0,st.session_state.slider_values.get(f"V{i+1}",0.0),0.1,key=f"lab_{i+1}")
                    st.session_state.slider_values[f"V{i+1}"]=val
        col_pure,col_E=st.columns(2)
        with col_pure:
            W_pure=st.checkbox(T("الإخلاص لله [أ=1]","Sincerity [A=1]"),value=st.session_state.slider_values.get("W_pure",True))
            st.session_state.slider_values["W_pure"]=W_pure
        with col_E:
            E_val=st.slider(T("التمكين [ق=100]","Empowerment [Q=100]"),0.0,1.0,st.session_state.slider_values.get("E_val",0.5),0.05,key="lab_E")
            st.session_state.slider_values["E_val"]=E_val
    st.markdown("---"); st.subheader(T("🤖 مساعد الذكاء الاصطناعي","🤖 AI Assistant"))
    ai_text=st.text_area(T("الوصف:","Description:"),height=80,placeholder=T("مثال: دولة إسلامية...","Example..."))
    if st.button(T("تحليل بالذكاء الاصطناعي","Analyze with AI"),use_container_width=True):
        if not ai_text.strip(): st.warning(T("أدخل وصفاً","Enter description"))
        else:
            with st.spinner(T("جاري التحليل...","Analyzing...")):
                try:
                    import openai
                    openai.api_key=st.secrets.get("OPENAI_API_KEY","")
                    if openai.api_key:
                        inds="\n".join([f"{i+1}. {get_indicator_label(i)}" for i in range(N_IND)])
                        prompt=f"""You are an expert in the Mizan theory. Analyze this entity and return JSON with values (between -1 and 1) for these indicators:\n{inds}\nAlso include "W_pure": true/false, "E_val": 0-1, "analysis": brief in Arabic. Return ONLY JSON.\nDescription: {ai_text}"""
                        response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"system","content":"Return ONLY JSON."},{"role":"user","content":prompt}],temperature=0.3,max_tokens=500)
                        content=response.choices[0].message.content.strip()
                        if content.startswith("```"): content=content.split("\n",1)[1].rsplit("\n",1)[0]
                        ai_result=json.loads(content)
                        vals=ai_result.get("values",[0.0]*N_IND)[:N_IND]
                        for i in range(N_IND): st.session_state.slider_values[f"V{i}"]=vals[i]
                        st.session_state.slider_values["W_pure"]=ai_result.get("W_pure",True)
                        st.session_state.slider_values["E_val"]=ai_result.get("E_val",0.5)
                        st.success(T("✅ تم التحليل!","✅ Analysis complete!"))
                        if "analysis" in ai_result: st.info(ai_result["analysis"])
                        st.rerun()
                except Exception as e: st.error(f"AI Error: {e}")
    vals=[st.session_state.slider_values.get(f"V{i}",0.0) for i in range(N_IND)]
    W_raw=np.mean(vals[0:6]); B_raw=np.mean(vals[6:11])
    S_final,E_norm,gate_name,gate_msg,gate_color,istidraj_gap=calculate_S(W_raw,B_raw,st.session_state.slider_values.get("E_val",0.5),st.session_state.slider_values.get("W_pure",True),vals[7],vals[6])
    col1,col2,col3,col4,col5=st.columns(5)
    col1.metric("W",f"{W_raw:+.2f}"); col2.metric("B",f"{B_raw:+.2f}"); col3.metric("S",f"{S_final:.2f}"); col4.metric("E",f"{E_val:.2f}"); col5.metric(T("فجوة","Gap"),f"{istidraj_gap:.2f}")
    if gate_msg:
        st.markdown(f"### {gate_color} {gate_name}")
        if T("انهيار","Collapse") in gate_msg or T("لا يغفر","Unforgivable") in gate_msg: st.error(gate_msg)
        elif T("باطلة","Void") in gate_msg: st.warning(gate_msg)
        else: st.success(gate_msg)
    if istidraj_gap>0.3: st.error(f"🚨 {T('إنذار استدراج','Istidraj Alert')}")
    elif istidraj_gap>0.1: st.warning(f"⚡ {T('فجوة متوسطة','Moderate Gap')}")
    col_a,col_b=st.columns(2)
    with col_a:
        fig=plot_quadrant_map(B_raw,W_raw,istidraj_gap); st.pyplot(fig)
    with col_b:
        years=st.slider(T("سنوات","Years"),10,100,50,10)
        Sh,Eh=simulate_future(S_final,E_val,W_raw,B_raw,years)
        fig,ax=plt.subplots(figsize=(5,3),facecolor='#0a0f1e'); ax.set_facecolor('#0a0f1e')
        ax.plot(Sh,label='S',color='#FFD700',lw=2); ax.plot(Eh,label='E',color='#0FF',lw=1.5,ls='--')
        ax.fill_between(range(years+1),Sh,Eh,where=(np.array(Eh)>np.array(Sh)),color='red',alpha=0.2)
        ax.set_xlabel(T('سنوات','Years'),color='white'); ax.legend(facecolor='#0a0f1e',edgecolor='white',labelcolor='white',fontsize=6)
        ax.tick_params(colors='white',labelsize=6); ax.grid(True,alpha=0.2); st.pyplot(fig)
    st.markdown("---"); st.markdown(T("### 🏥 المستشفى","### 🏥 Hospital"))
    wW,wB=np.argmin(vals[0:6]),np.argmin(vals[6:11])
    W_L=[get_indicator_label(i) for i in range(6)]; B_L=[get_indicator_label(i+6) for i in range(5)]
    if gate_name==T("بوابة الشرك","Shirk Gate"): st.error(T("جدد التوحيد","Renew Tawheed"))
    elif gate_name==T("بوابة الماعون","Al-Ma'un Gate"): st.error(f"🎯 أصلح '{B_L[wB]}'.")
    elif gate_name==T("بوابة الإخلاص","Sincerity Gate"): st.warning(f"🎯 نقِّ '{W_L[wW]}' من الشرك.")
    elif istidraj_gap>0.3: st.error(f"🎯 سد الفجوة عبر '{W_L[wW]}' أو '{B_L[wB]}'.")
    else: st.info(f"🎯 عزز '{W_L[wW]}' و'{B_L[wB]}'.")

# --- تبويب ٣: المشهد الكوني (موجود في المرحلة السابقة) ---
# (نفس كود المشهد الكوني السابق)

# --- تبويب ٤: المعجم الهندسي (موجود في المرحلة السابقة) ---
# (نفس كود المعجم السابق)

# --- تبويب ٥: الشواهد (موجود في المرحلة السابقة) ---
# (نفس كود الشواهد السابق)

# --- تبويب ٦: هندسة الصراط (موجود في المرحلة السابقة) ---
# (نفس كود الصراط السابق)

# --- التذييل ---
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.5em;">⚖️ مختبر الميزان</p>
    <p style="color:#FFD700;font-size:1.3em;">S = W x B</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
    <p style="font-size:0.8em;">{T('هذا المختبر ليس إلا محاولة متواضعة...','This lab is but a humble attempt...')}</p>
</div>
""", unsafe_allow_html=True)
