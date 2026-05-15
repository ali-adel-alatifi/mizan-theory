import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import random, time
from collections import deque
from io import BytesIO
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
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; width: 100%; transition: all 0.3s ease; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; box-shadow: 0 0 25px rgba(255,215,0,0.5); }
.stTabs [data-baseweb="tab-list"] { gap: 5px; background: rgba(13,21,40,0.8); border-radius: 15px; padding: 5px; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: bold; }
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
    'و': 6, 'ب': 2
}

# =============================================
# الدوال المساعدة
# =============================================
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

# =============================================
# قاعدة بيانات البوصلة الكاملة (19 سؤالاً) مع القيم الحرفية
# =============================================
COMPASS_DATA = [
    {"id":1,"topic":T("القوانين الوضعية وتحكيم الشريعة","Man-Made Laws vs. Sharia"),"letter":"ق","value":100,
     "text":T("في زمن سيادة القوانين الوضعية، وشعار 'الدين لله والوطن للجميع'، كمسلم: ما هو موقفك من تحكيم شرع الله؟","In an age of man-made laws..."),
     "answers":[(T("تحكيم شرع الله هو الصحيح، وأبذل كل ما أستطيع لتطبيقه","Applying Sharia is correct..."),2),
                (T("أتمنى تطبيق الشريعة، لكني لا أعمل لأجلها","I wish for Sharia..."),1),
                (T("أرى أن بعض أحكام الشريعة صالحة وبعضها غير صالح","Some rulings are valid..."),-1),
                (T("الشريعة الإسلامية لم تعد تصلح لهذا العصر","Sharia is no longer suitable..."),-2)]},
    {"id":2,"topic":T("الولاء للعرق والحزب والطائفة","Loyalty to Race, Party, and Sect"),"letter":"أ","value":1,
     "text":T("في عصر أصبح فيه الولاء للعرق والحزب والطائفة والمذهب هو المعيار، كمسلم: ما هو موقفك؟","In an age where loyalty to race..."),
     "answers":[(T("ولائي لله ورسوله والمؤمنين فوق كل رابطة، وأتبرأ من العصبيات الجاهلية","My loyalty is to Allah..."),2),
                (T("أحاول أن أوازن بين ولائي للإسلام وانتمائي العرقي أو الحزبي","I try to balance..."),1),
                (T("ولائي لديني ضعيف، وأميل للفخر بعرقي أو حزبي أكثر","My religious loyalty is weak..."),-1),
                (T("لا أرى مشكلة في تقديم العرق أو الحزب على الدين، فهذا واقع العصر","I see no problem..."),-2)]},
    {"id":3,"topic":T("الاستهزاء بالمقدسات وحرية التعبير","Mockery of Sanctities & Free Speech"),"letter":"هـ","value":5,
     "text":T("في زمن تُباح فيه 'حرية التعبير' للاستهزاء بالدين والمقدسات، كمسلم: ما هو موقفك؟","In an age where 'free speech'..."),
     "answers":[(T("أبغض في الله المستهزئين، وأدين فعلهم بكل وضوح","I hate the mockers..."),2),
                (T("أستنكر الاستهزاء في قلبي، لكني لا أعلن موقفي جهارًا","I disapprove in my heart..."),1),
                (T("أرى أنها 'حرية رأي' ولا داعي للغضب","It's 'free speech'..."),-1),
                (T("أضحك معهم أحيانًا، ولا أرى في ذلك ضررًا كبيرًا","I sometimes laugh..."),-2)]},
    {"id":4,"topic":T("الربا والنظام المالي العالمي","Usury and the Global Financial System"),"letter":"ص","value":90,
     "text":T("في زمن يقوم فيه النظام المالي العالمي على الربا...","In an age where the global financial system..."),
     "answers":[(T("أتجنب الربا بكل صوره وأبحث عن البدائل الإسلامية ولو خسرت ربحًا","I avoid all usury..."),2),
                (T("أكره الربا، لكني مضطر للتعامل به أحيانًا بحكم الواقع","I hate usury, but am forced..."),1),
                (T("أتعامل بالربا كالجميع، ولا أرى مشكلة حقيقية في ذلك","I deal with usury like everyone else..."),-1),
                (T("الربا ضرورة اقتصادية، وتحريمه كان لزمن غير زمننا","Usury is an economic necessity..."),-2)]},
    {"id":5,"topic":T("العلمانية وفصل الدين عن الدولة","Secularism: Separating Religion from State"),"letter":"ك","value":20,
     "text":T("في زمن تسود فيه العلمانية، وتُرفع شعارات 'فصل الدين عن الدولة'...","In an age of secularism..."),
     "answers":[(T("أرفض العلمانية، وأؤمن أن الإسلام دين ودولة وشريعة تحكم كل الحياة","I reject secularism..."),2),
                (T("أرى أن العلمانية قد تكون حلاً مؤقتًا لحين استعداد المجتمع","Secularism may be a temporary solution..."),1),
                (T("لا أمانع فصل الدين عن السياسة، فالدين علاقة شخصية بالله","I don't mind separating..."),-1),
                (T("العلمانية هي الطريق الصحيح للتقدم، والدين يجب أن يبقى في المسجد فقط","Secularism is the right path..."),-2)]},
    {"id":6,"topic":T("إقامة الحدود الشرعية","Establishing Sharia Penalties"),"letter":"ح","value":8,
     "text":T("في زمن تُلغى فيه الحدود الشرعية (كقطع يد السارق ورجم الزاني)...","In an age where Sharia penalties..."),
     "answers":[(T("الحدود الشرعية رحمة وعدل، وأؤمن بضرورة إقامتها لحماية المجتمع","Sharia penalties are mercy..."),2),
                (T("الحدود حق، لكن الظروف الحالية لا تسمح بتطبيقها","Penalties are right, but current conditions..."),1),
                (T("أشعر بالحرج من بعض الحدود، وأراها قاسية","I feel embarrassed..."),-1),
                (T("الحدود الشرعية همجية ولا تصلح للعصر الحديث","Sharia penalties are barbaric..."),-2)]},
    {"id":7,"topic":T("الإلحاد وإنكار الخالق","Atheism: Denying the Creator"),"letter":"ن","value":50,
     "text":T("في زمن ينتشر فيه الإلحاد، ويُقدَّم العلم على أنه ينفي وجود الله...","In an age of spreading atheism..."),
     "answers":[(T("أؤمن بالله يقينًا لا يتزعزع، وأرى في العلم دليلاً على وجوده","I believe in Allah with unshakable certainty..."),2),
                (T("أؤمن بالله، لكني لا أملك حججًا للرد على شبهات الملحدين","I believe, but lack arguments..."),1),
                (T("تساورني أحيانًا شكوك، لكني أعود للإيمان","Doubts sometimes cross my mind..."),-1),
                (T("أعتقد أن الإلحاد طرح فكري يحترم، والدين مجرد أساطير","Atheism is a respectable thought..."),-2)]},
    {"id":8,"topic":T("الجهاد ونصرة المستضعفين","Jihad and Supporting the Oppressed"),"letter":"ر","value":200,
     "text":T("في زمن يُشوَّه فيه الجهاد ويوصم بـ 'الإرهاب'...","In an age where jihad is distorted..."),
     "answers":[(T("الجهاد ذروة سنام الإسلام، وأتمنى أن أكون في صفوف المجاهدين","Jihad is the peak of Islam..."),2),
                (T("الجهاد حق، وأدعمه بقلبي ومالي إن استطعت، لكني لا أقاتل الآن","Jihad is right; I support it..."),1),
                (T("أخشى من الجهاد، وأرى أنه يجلب المشاكل للمسلمين","I fear jihad..."),-1),
                (T("الجهاد أصبح إرهابًا، ولا مكان له في هذا العصر","Jihad has become terrorism..."),-2)]},
    {"id":9,"topic":T("حقوق المرأة بين الإسلام والتغريب","Women's Rights: Islam vs. Westernization"),"letter":"هـ","value":5,
     "text":T("في زمن تُطرح فيه 'حقوق المرأة' بصيغة غربية تنتزعها من فطرتها...","In an age where 'women's rights'..."),
     "answers":[(T("أؤمن أن الإسلام كرم المرأة ورفع شأنها، وأن أحكامه هي عين العدل","Islam honored woman..."),2),
                (T("أؤمن بالإسلام، لكني أرى ضرورة 'تحديث' بعض الأحكام لتواكب العصر","I believe, but some rulings need updating..."),1),
                (T("أشعر بالحرج من بعض أحكام الإسلام الخاصة بالمرأة","I feel embarrassed..."),-1),
                (T("أعتقد أن الإسلام ظلم المرأة، وأن تحريرها يكون بالعلمانية","Islam oppressed women..."),-2)]},
    {"id":10,"topic":T("العولمة، الذوبان الحضاري، الموضة، والاستهلاك","Globalization, Cultural Dissolution, Fashion & Consumerism"),"letter":"م","value":40,
     "text":T("في زمن العولمة التي تسعى لطمس الهويات، وجعل الثقافة الغربية هي المعيار...","In an age of globalization..."),
     "answers":[(T("أتمسك بهويتي الإسلامية، وأتبرأ من تقليد الكفار في ثقافتهم وأزيائهم، وأزهد في الدنيا...","I hold fast to my Islamic identity..."),2),
                (T("أحاول أن أوازن بين هويتي الإسلامية ومتطلبات العصر، وأوفق بين التمتع بالحلال والزهد","I try to balance..."),1),
                (T("أقلد الغرب في كثير من ثقافته وأزيائه واستهلاكه، ولا أرى بأساً في ذلك","I imitate the West..."),-1),
                (T("الثقافة الغربية هي ثقافة التقدم، ويجب أن نندمج فيها كلياً...","Western culture is progress..."),-2)]},
    {"id":11,"topic":T("الديمقراطية والتشريع","Democracy and Legislation"),"letter":"ل","value":30,
     "text":T("في زمن تُقدَّس فيه الديمقراطية وتُجعل الشعب هو مصدر التشريع...","In an age where democracy is sanctified..."),
     "answers":[(T("أرفض جعل الشعب مشرعًا، فالتشريع لله وحده، والشورى لا تعني الالتفاف على الشرع...","I reject making the people legislators..."),2),
                (T("أرى أن الديمقراطية وسيلة يمكن استخدامها لتحقيق بعض المصالح","Democracy is a tool..."),1),
                (T("أفضّل النظام الديمقراطي على الأنظمة الاستبدادية","I prefer democracy..."),-1),
                (T("الديمقراطية هي أفضل نظام حكم، والشريعة لا تصلح للتطبيق السياسي","Democracy is best..."),-2)]},
    {"id":12,"topic":T("التعددية الدينية","Religious Pluralism"),"letter":"ي","value":10,
     "text":T("في زمن تُطرح فيه 'التعددية الدينية' على أنها تعني أن كل الأديان طرق للخلاص...","In an age where 'religious pluralism'..."),
     "answers":[(T("الإسلام هو الدين الوحيد المقبول عند الله، ومن لم يؤمن به فهو خاسر في الآخرة","Islam is the only religion..."),2),
                (T("الإسلام هو الحق، لكني لا أحكم على أصحاب الديانات الأخرى","Islam is truth, but I don't judge..."),1),
                (T("أرى أن كل الأديان فيها جزء من الحق","I see every religion..."),-1),
                (T("كل الأديان سواء، ولا يحق لأحد أن يدعي امتلاك الحقيقة المطلقة","All religions are equal..."),-2)]},
    {"id":13,"topic":T("الحب في الله والبغض في الله","Love for Allah and Hatred for Allah"),"letter":"ق","value":100,
     "text":T("في زمن أصبحت فيه المصلحة هي المعيار الأساسي في العلاقات...","In an age where interests became the standard..."),
     "answers":[(T("أحب في الله أولياءه وأبغض في الله أعداءه، وهذا أوثق عرى إيماني، ولا أجعل مصلحتي الشخصية فوق هذا","I love for Allah His allies..."),2),
                (T("أحاول، لكن علاقاتي تغلب عليها المصالح والمنافع أحيانًا","I try, but my relationships..."),1),
                (T("أتعامل مع الجميع بالمثل، لا حب ولا بغض في الله، فالمصلحة هي الأساس","I deal with everyone equally..."),-1),
                (T("علاقاتي كلها تقوم على مصلحتي الشخصية، ولا دخل للدين فيها","All my relationships..."),-2)]},
    {"id":14,"topic":T("التحلي بالأخلاق الحميدة – الكذب والغش والخيانة","Embodying Noble Character"),"letter":"ط","value":9,
     "text":T("في زمن أصبح الخداع والكذب والغش ذكاءً، وخان الناس الأمانات والعهود...","In an age where deception..."),
     "answers":[(T("الصدق والأمانة والوفاء دين، وألتزم بها ولو خسرت دنيويًا، ولا أخون ولا أغش ولا أكذب","Truthfulness, honesty, and fidelity..."),2),
                (T("أحاول الالتزام بها، لكني قد أضطر للكذب أو التغاضي عن بعض الأمانات أحيانًا","I try to adhere..."),1),
                (T("أرى أن المبالغة في الصدق سذاجة، والواقع يفرض بعض 'المرونة' في الكذب والغش","Excessive honesty is naivety..."),-1),
                (T("الكذب والغش والخيانة أدوات ضرورية للنجاح في هذا العصر","Lying, fraud, and betrayal..."),-2)]},
    {"id":15,"topic":T("الغيرة على المحارم والأمر بالمعروف","Protective Jealousy & Enjoining Good"),"letter":"ب","value":2,
     "text":T("في زمن انتشرت فيه الفواحش، وصار إنكار المنكر 'تطرفًا'...","In an age of widespread indecency..."),
     "answers":[(T("آمر بالمعروف وأنهى عن المنكر بكل استطاعتي، فهذا واجبي","I enjoin good and forbid evil..."),2),
                (T("أنكر بقلبي، وأحيانًا بلساني إذا لم أخف ضررًا كبيرًا","I reject in my heart..."),1),
                (T("أسكت عن المنكر حفاظًا على علاقاتي ومصالحي","I remain silent..."),-1),
                (T("لا داعي للأمر والنهي، فكل إنسان حر في تصرفاته","No need for enjoining/forbidding..."),-2)]},
    {"id":16,"topic":T("الوطنية والحزبية والمذهبية","Patriotism, Partisanship, and Sectarianism"),"letter":"ف","value":80,
     "text":T("في زمن تُقدَّس فيه الوطنية والحزبية والمذهبية، ويُرفع شعار 'الوطن أو الحزب أو المذهب أولاً'...","In an age where patriotism..."),
     "answers":[(T("ولائي للإسلام فوق كل وطن وحزب ومذهب، وأتبرأ من كل دعوة جاهلية تفرق المسلمين","My loyalty to Islam is above every nation..."),2),
                (T("أحب وطني وحزبي ومذهبي، لكني أقدّم الإسلام عليها","I love my nation, party, and sect..."),1),
                (T("أشعر أن انتمائي لوطني أو حزبي أو مذهبي أهم من انتمائي للإسلام","My belonging to my nation..."),-1),
                (T("لا أرى مشكلة في تقديم الوطن أو الحزب أو المذهب على الدين، فهذا واقع العصر","No problem prioritizing nation..."),-2)]},
    {"id":17,"topic":T("الصلاة في زمن الانشغال","Prayer in an Age of Busyness"),"letter":"ن","value":50,
     "text":T("في زمن تزدحم فيه الحياة، وتتسارع فيه الأيام، وأصبحت الصلاة 'عبئًا' على البعض...","In an age of crowded life..."),
     "answers":[(T("الصلاة راحتي وقرة عيني، ولا أتركها مهما كنت مشغولاً","Prayer is my comfort..."),2),
                (T("أصلي لكني أؤخرها أو أستعجل فيها أحيانًا","I pray but sometimes delay or rush"),1),
                (T("أصلي أحيانًا وأتركها أحيانًا، حسب الظروف","I pray sometimes and leave it sometimes"),-1),
                (T("لا أجد وقتًا للصلاة، وأراها غير عملية في هذا العصر","I find no time for prayer..."),-2)]},
    {"id":18,"topic":T("الصوم في زمن الشهوات","Fasting in an Age of Desires"),"letter":"ط","value":9,
     "text":T("في زمن تحاصر فيه الشهوات الإنسان من كل جانب...","In an age where desires besiege man..."),
     "answers":[(T("أصوم الفرض والنفل، وأراه دورة تدريبية على تقوى الله","I fast obligatory and voluntary..."),2),
                (T("أصوم الفرض فقط، ولا أستطيع صيام النفل","I fast only the obligatory..."),1),
                (T("أصوم رمضان كعادة اجتماعية، ولا أشعر بروحانيته","I fast Ramadan as a social habit..."),-1),
                (T("لا أصوم، وأرى أن العصر لا يتناسب مع فكرة الصيام","I don't fast..."),-2)]},
    {"id":19,"topic":T("الزكاة والصدقة في زمن الأنانية","Zakat and Charity in an Age of Selfishness"),"letter":"ط","value":9,
     "text":T("في زمن طغت فيه الأنانية، وضعف فيه التكافل، وأصبح المال 'إلهًا'...","In an age of rampant selfishness..."),
     "answers":[(T("أؤدي الزكاة طيبة بها نفسي، وأعترف أن المال مال الله، وفيها طهارة لنفسي وعونًا لإخوتي","I pay Zakat willingly..."),2),
                (T("أؤدي الزكاة فقط، وأحيانًا أتصدق","I pay only Zakat..."),1),
                (T("أخرج الزكاة بخلاً، وأشعر أنها 'ضريبة'","I pay Zakat grudgingly..."),-1),
                (T("لا أزكي، فالمال مالي ولا دخل لأحد فيه","I don't pay Zakat..."),-2)]},
]

def calc_compass(answers_dict):
    w_sum, b_sum = 0.0, 0.0
    total_weight = sum(q['value'] for q in COMPASS_DATA)
    for q in COMPASS_DATA:
        score = answers_dict.get(f"q_{q['id']}", 0)
        weight = q['value']
        if score > 0:
            w_sum += score * weight
            b_sum += score * weight * 0.7
        else:
            b_sum += score * weight
            w_sum += score * weight * 0.3
    max_possible = 2 * total_weight
    W_raw = max(-1.0, min(1.0, w_sum / max_possible))
    B_raw = max(-1.0, min(1.0, b_sum / max_possible))
    W_norm = (W_raw + 1) / 2
    B_norm = (B_raw + 1) / 2
    S_score = W_norm * B_norm
    return W_raw, B_raw, S_score

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
    st.session_state.hS = deque(maxlen=300); st.session_state.hE = deque(maxlen=300); st.session_state.hx = deque(maxlen=300)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0; st.session_state.frame = 0
    st.session_state.compass_answers = {}
    st.session_state.init = True

print("✅ المرحلة الأولى مكتملة: الأساسيات، الثوابت، الدوال، البوصلة الكاملة")

# =============================================
# المرحلة الثانية: الواجهة، التبويبات، البوصلة، المشهد الكوني
# =============================================

# --- رسالة الترحيب ---
with st.expander(T("📜 رسالة ترحيب", "📜 Welcome Message"), expanded=True):
    st.markdown(f"""
    <div class="message-box">
    <h2 style="text-align:center;color:#FFD700;">⚖️ {T('الدِّينُ الْقَيِّم – المنارة العالمية', 'Al-Deen Al-Qayyim – The Global Beacon')}</h2>
    <p style="text-align:center;font-style:italic;color:#CCC;font-size:1.1em;">
    "{T('هَلْ يُوجَدُ قَانُونٌ وَاحِدٌ يَحْكُمُ الذَّرَّةَ وَالْحَضَارَةَ؟', 'Is there a single law governing the atom and civilization?')}"
    </p>
    <p>{T(
    'هذا مختبر. مختبرٌ صغير، لعله يفتح لك بابًا كبيرًا. '
    'لا ندّعي الحقيقة المطلقة، بل ندعوك لرؤية شيءٍ قد يكون مرّ على قلبك ولم تلاحظه.',
    'This is a lab. A small lab, perhaps it opens a big door for you. '
    'We do not claim absolute truth, but invite you to see something that may have passed your heart unnoticed.'
    )}</p>
    <p>{T(
    'تأمل معي: الذرةُ في داخلها قوتان: جاذبيةٌ تجمع، وتنافرٌ يمنع التصادم. لو اختلت إحداهما، لانهارت الذرة. '
    'والخليةُ في جسدك: جهاز مناعةٍ يحمي، وغذاءٌ يبني. لو نامت المناعة، لالتهم المرضُ الجسد.',
    'Reflect with me: the atom has two forces: attraction that gathers, and repulsion that prevents collision. '
    'If one fails, the atom collapses. And the cell in your body: an immune system that protects, and nutrition that builds. '
    'If immunity sleeps, disease devours the body.'
    )}</p>
    <p style="color:#FFD700;font-weight:bold;">{T(
    'هل هذه مصادفة؟ أم أن هناك "قانونًا واحدًا" ينساب في نسيج الوجود كله، من الذرة إلى الحضارة؟',
    'Is this coincidence? Or is there a "single law" flowing through the fabric of existence, from atom to civilization?'
    )}</p>
    <p style="text-align:center;color:#FFD700;font-size:1.2em;font-weight:bold;">S = W × B</p>
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
    
    **٢. المشهد الكوني الحي:** شاهد تفاعل النجوم (الأفراد) مع قطبي الميزان في الزمن الحقيقي.
    
    **٣. مختبر الأمة المتكاملة:** محاكاة تجمع المجتمع والدولة والأمة في نسيج واحد.
    
    **٤. مقارنة الحضارات:** قارن بين حضارتين تبدأ كل منهما بقيم مختلفة.
    
    **٥. الشواهد التاريخية:** قارن بين الدول التاريخية لترى كيف تنطبق المعادلة على التاريخ الفعلي.
    
    **٦. أصل النظرية:** الأسس القرآنية والنبوية التي تثبت أن المعادلة S = W × B ليست اختراعًا بشريًا.
    
    **٧. هندسة الصراط:** النموذج الإبراهيمي، وتتبع مسارك نحو مقام إبراهيم عليه السلام.
    
    **المعادلة المركزية:** **S = W × B** (العلاقة **ضرب لا جمع**).
    """,
    """
    ### 🎯 How to Use This Lab
    
    **1. Al-Islam Al-Hanif Compass:** Answer 19 questions to discover your position in the Value Space.
    
    **2. Live Cosmic Scene:** Watch stars (individuals) interact with the Mizan poles in real-time.
    
    **3. Integrated Nation Lab:** Simulation combining society, state, and nation.
    
    **4. Civilization Comparison:** Compare two civilizations starting with different values.
    
    **5. Historical Evidence:** Compare historical nations to see the equation in action.
    
    **6. Theory:** The Quranic and Prophetic foundations proving S = W × B.
    
    **7. Path Geometry:** The Abrahamic model and tracking your path toward Abraham's Station.
    
    **Central Equation:** **S = W × B** (multiplication, not addition).
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

# --- الشريط الجانبي ---
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:10px;background:linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:10px;margin-bottom:15px;border:1px solid #FFD700'>
        <p style='font-size:2em;margin:0;'>⚖️</p>
        <h2 style='color:#FFD700;margin:0;'>{T('الدِّينُ الْقَيِّم', 'Al-Deen Al-Qayyim')}</h2>
        <p style='color:#e0e0e0;font-size:10px;margin:2px 0;'>{T('المنارة العالمية', 'The Global Beacon')}</p>
        <p style='color:#FFD700;font-size:14px;margin:2px 0;font-weight:bold;'>S = W × B</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ إعدادات عامة")
    lag = st.select_slider(T("فجوة الاستدراج", "Istidraj Gap"), options=[5,10,15,22,30,40,50], value=22, key="lag")
    st.markdown("---")
    
    # --- الميزان الأخروي الحي ---
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
    
    st.markdown("---")
    if st.button("🔄 إعادة ضبط كل شيء", key="btn_reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

# --- التبويبات ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    T("📖 أصل النظرية", "📖 Theory"),
    T("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    T("🧍 بوصلة الإسلام الحنيف", "🧍 Compass"),
    T("🏛️ مختبر الأمة", "🏛️ Nation Lab"),
    T("🏰 مقارنة الحضارات", "🏰 Civilizations"),
    T("📜 الشواهد", "📜 Evidence"),
    T("📐 هندسة الصراط", "📐 Path")
])

# =============================================
# تبويب ١: أصل النظرية
# =============================================
with tab1:
    st.header(T("📖 أصل النظرية – نظرية الإسلام المتكاملة", "📖 Theory – The Integrated Islamic Theory"))
    with st.expander(T("⚖️ ١. الدين القيم – قانون الوجود الحق", "⚖️ 1. Al-Deen Al-Qayyim"), expanded=True):
        st.markdown(T("""
        ### ⚖️ الدين القيم – قانون الوجود الحق
        نبدأ رحلتنا من أم الكتاب، من الدعاء الذي لا تنقطع ألسنة المؤمنين عن ترداده في كل ركعة: **﴿اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ﴾**.
        ما هو هذا الصراط المستقيم؟ إنه ليس مجرد طريق، بل هو **الدين القيم** نفسه، قانون الوجود الذي فطر الله عليه السماوات والأرض ومن فيهن.
        **تعريفه:** الدين القيم هو قانون السببية الكوني الثابت في أصله، المتجدد في تطبيقاته.
        **خصائصه:** الربانية، الثبات، الشمول، الحتمية، والديناميكية (الحنيفية).
        """,
        """
        ### ⚖️ Al-Deen Al-Qayyim – The True Law of Existence
        We begin from the Mother of the Book: **﴿Guide us to the Straight Path﴾**.
        This is Al-Deen Al-Qayyim itself: the cosmic law of causality, constant in origin, dynamic in application.
        **Its characteristics:** Divine origin, immutability, comprehensiveness, inevitability, and dynamism.
        """))
    with st.expander(T("🕌 ٢. الإسلام الحنيف", "🕌 2. Al-Islam Al-Hanif"), expanded=False):
        st.markdown(T("""
        ### 🕌 الإسلام الحنيف – الاستجابة الديناميكية للقانون
        إذا كان الدين القيم هو القانون، فإن **الإسلام الحنيف** هو الاستجابة الوحيدة الممكنة لهذا القانون.
        **معادلته:** `I = W × B` (العلاقة ضرب لا جمع).
        **لماذا إبراهيم هو النموذج الأكمل؟** لأنه جسّد الاستجابة الكاملة.
        """,
        """
        ### 🕌 Al-Islam Al-Hanif – The Dynamic Response
        If Al-Deen Al-Qayyim is the law, **Al-Islam Al-Hanif** is the only possible response.
        **Its equation:** `I = W × B` (multiplication, not addition).
        **Why Abraham?** Because he embodied the complete response.
        """))

# =============================================
# تبويب ٢: المشهد الكوني الحي
# =============================================
with tab2:
    st.header(T("🌌 المشهد الكوني الحي", "🌌 Live Cosmic Scene"))
    
    # إعدادات المشهد
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
        # تهيئة المشهد إذا لم يكن مهيأ
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
        
        # تنفيذ إطار واحد
        try:
            cx = st.session_state.cx; cy = st.session_state.cy
            sx = st.session_state.live_sx.copy(); sy = st.session_state.live_sy.copy()
            sw = st.session_state.live_sw.copy(); sb = st.session_state.live_sb.copy()
            W = st.session_state.live_W; B = st.session_state.live_B
            E = st.session_state.live_E; S = st.session_state.live_S
            aW = st.session_state.live_aW; aB = st.session_state.live_aB
            frame = st.session_state.live_frame
            N = len(sx)
            
            # تحديث النجوم
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
            sx = np.clip(sx, cx-13, cx+13)
            sy = np.clip(sy, cy-9, cy+9)
            
            frame += 1
            
            # حفظ الحالة
            st.session_state.live_sx = sx; st.session_state.live_sy = sy
            st.session_state.live_sw = sw; st.session_state.live_sb = sb
            st.session_state.live_W = W; st.session_state.live_B = B
            st.session_state.live_E = E; st.session_state.live_S = S
            st.session_state.live_aW = aW; st.session_state.live_aB = aB
            st.session_state.live_frame = frame
            
            # رسم المشهد
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
            colors = [star_color(sw[i],sb[i]) for i in range(N)]
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

# =============================================
# تبويب ٣: بوصلة الإسلام الحنيف
# =============================================
with tab3:
    st.header(T("🧍 بوصلة الإسلام الحنيف", "🧍 Al-Islam Al-Hanif Compass"))
    st.markdown(T(
        "١٩ سؤالاً، كل سؤال يستحضر مفهوماً معاصراً مغلوطاً ويطرح موقفاً يلامس واقع الأمة. أجب بصدق لتعرف موقعك الحقيقي. المعادلة: S = W × B.",
        "19 questions, each recalling a distorted modern concept. Answer honestly to discover your true position."
    ))
    
    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}
    
    # عرض الأسئلة
    for q in COMPASS_DATA:
        with st.expander(f"**{q['id']}. {q['topic']}**  [{q['letter']}={q['value']}]"):
            st.markdown(f"*{q['text']}*")
            key = f"q_{q['id']}"
            ans = st.radio(
                T("اختر موقعك:", "Choose your position:"),
                [a[0] for a in q['answers']],
                key=key, index=None
            )
            if ans:
                for a_text, a_val in q['answers']:
                    if ans == a_text:
                        st.session_state.compass_answers[key] = a_val
                        break
    
    # الحساب والعرض
    if len(st.session_state.compass_answers) == 19:
        W_raw, B_raw, S_score = calc_compass(st.session_state.compass_answers)
        
        if W_raw > 0 and B_raw > 0:
            q_name, q_color = T("مؤمن حنيف (متوازن)","Hanif Believer"), '#FFD700'
        elif W_raw > 0 and B_raw <= 0:
            q_name, q_color = T("مؤمن مستضعف","Weak Believer"), '#FF5252'
        elif W_raw <= 0 and B_raw <= 0:
            q_name, q_color = T("غافل أو منافق","Heedless"), '#FFB6C1'
        else:
            q_name, q_color = T("متطرف","Extremist"), '#FFA500'
        
        st.divider()
        st.subheader("📊 نتيجة البوصلة")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("W", f"{W_raw:+.2f}")
        c2.metric("B", f"{B_raw:+.2f}")
        c3.metric("S", f"{S_score:.2f}")
        c4.metric(T("موقعك","Position"), q_name)
        st.markdown(f"<h2 style='color:{q_color};text-align:center;'>{q_name}</h2>", unsafe_allow_html=True)
        
        # خريطة رباعية
        fig, ax = plt.subplots(figsize=(5,5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
        ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
        ax.fill_between([0,1.2],0,1.2,color='#FFD700',alpha=0.3)
        ax.fill_between([-1.2,0],0,1.2,color='#FF5252',alpha=0.2)
        ax.fill_between([-1.2,0],-1.2,0,color='#FFB6C1',alpha=0.2)
        ax.fill_between([0,1.2],-1.2,0,color='#FFA500',alpha=0.2)
        ax.scatter(B_raw,W_raw,s=200,c='cyan',edgecolors='white',linewidth=2,zorder=10)
        ax.scatter(1,1,s=80,c='#FFD700',marker='*',zorder=10)
        ax.text(1,1.1,T('إبراهيم','Abraham'),color='#FFD700',fontsize=7,ha='center')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        if st.button(T("🔄 إعادة البوصلة", "🔄 Retake Compass"), use_container_width=True):
            st.session_state.compass_answers = {}
            st.rerun()

print("✅ المرحلة الثانية مكتملة: الواجهة، التبويبات، البوصلة، المشهد الكوني")

# =============================================
# المرحلة الثالثة: مختبر الأمة، مقارنة الحضارات، الشواهد
# =============================================

# =============================================
# النظام النهائي – المنزلقات السبعة مع الحروف
# =============================================
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
# دوال الحساب للمنزلقات السبعة
# =============================================
def compute_WB_final(values):
    W_total = 0.1; B_total = 0.1
    for key, val in values.items():
        if key in ISLAMIC_SYSTEM_FINAL:
            W_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_W"]
            B_total += val * ISLAMIC_SYSTEM_FINAL[key]["effect_B"]
    return np.clip(W_total, 0.01, 1.0), np.clip(B_total, 0.01, 1.0)

def create_final_sliders(prefix, defaults=None):
    if defaults is None: defaults = {k: 0.0 for k in ISLAMIC_SYSTEM_FINAL}
    values = {}
    for key, data in ISLAMIC_SYSTEM_FINAL.items():
        letters_str = data["letters"][L]
        label_with_letters = f"{data['label']}  [{letters_str}]"
        values[key] = st.slider(
            label_with_letters, -1.0, 1.0, defaults.get(key, 0.0), 0.05,
            key=f"{prefix}_{key}",
            help=f"{data['desc']}\n\n{data['aya']}"
        )
    return values

# =============================================
# دالة رسم شجرة الإيمان
# =============================================
def render_faith_tree(values_dict, W_val=None, B_val=None):
    if W_val is None or B_val is None:
        W_val, B_val = compute_WB_final(values_dict)
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    
    faith_y = 9
    ax.text(5, faith_y, f"{ISLAMIC_SYSTEM_FINAL['faith']['label']} [أ]\n{values_dict.get('faith', 0):.2f}",
            ha='center', fontsize=12, color='#FFD700', fontweight='bold',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FFD700', boxstyle='round,pad=0.5'))
    
    worship_y = 7
    ax.text(2.5, worship_y, f"{ISLAMIC_SYSTEM_FINAL['worship']['label']} [ط]\n{values_dict.get('worship', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FFA500', boxstyle='round,pad=0.3'))
    ax.text(7.5, worship_y, f"{ISLAMIC_SYSTEM_FINAL['enjoining']['label']} [ع]\n{values_dict.get('enjoining', 0):.2f}",
            ha='center', fontsize=10, color='#00BFFF',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#00BFFF', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(2.5, worship_y+0.3), xytext=(5, faith_y-0.3),
                arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1.5))
    ax.annotate('', xy=(7.5, worship_y+0.3), xytext=(5, faith_y-0.3),
                arrowprops=dict(arrowstyle='->', color='#00BFFF', lw=1.5))
    
    trans_y = 5
    ax.text(5, trans_y, f"{ISLAMIC_SYSTEM_FINAL['transactions']['label']} [س]\n{values_dict.get('transactions', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#00FF88', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(5, trans_y+0.3), xytext=(2.5, worship_y-0.3),
                arrowprops=dict(arrowstyle='->', color='#FFA500', lw=1.5))
    ax.annotate('', xy=(5, trans_y+0.3), xytext=(7.5, worship_y-0.3),
                arrowprops=dict(arrowstyle='->', color='#00BFFF', lw=1.5))
    
    morals_y = 3
    ax.text(5, morals_y, f"{ISLAMIC_SYSTEM_FINAL['morals']['label']} [ي]\n{values_dict.get('morals', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FF69B4', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(5, morals_y+0.3), xytext=(5, trans_y-0.3),
                arrowprops=dict(arrowstyle='->', color='#00FF88', lw=1.5))
    
    bottom_y = 1
    ax.text(2.5, bottom_y, f"{ISLAMIC_SYSTEM_FINAL['hudud']['label']} [ح]\n{values_dict.get('hudud', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FF6347', boxstyle='round,pad=0.3'))
    ax.text(7.5, bottom_y, f"{ISLAMIC_SYSTEM_FINAL['jihad']['label']} [ج]\n{values_dict.get('jihad', 0):.2f}",
            ha='center', fontsize=10, color='#FFD700',
            bbox=dict(facecolor='#0a0f1e', edgecolor='#FF4500', boxstyle='round,pad=0.3'))
    ax.annotate('', xy=(2.5, bottom_y+0.3), xytext=(5, morals_y-0.3),
                arrowprops=dict(arrowstyle='->', color='#FF69B4', lw=1.5))
    ax.annotate('', xy=(7.5, bottom_y+0.3), xytext=(5, morals_y-0.3),
                arrowprops=dict(arrowstyle='->', color='#FF69B4', lw=1.5))
    
    ax.text(5, -0.5, f"S = W × B = {W_val:.2f} × {B_val:.2f} = {W_val*B_val:.3f}",
            ha='center', fontsize=14, color='#FFD700', fontweight='bold')
    ax.set_title(T("🌳 شجرة الإيمان", "🌳 Faith Tree"), color='white', fontsize=14, fontweight='bold')
    st.pyplot(fig)

# =============================================
# تبويب ٤: مختبر الأمة المتكاملة
# =============================================
with tab4:
    st.header(T("🏛️ مختبر الأمة المتكاملة – المجتمع والدولة في نسيج واحد", "🏛️ The Integrated Nation Lab"))
    st.markdown(T(
        "هذا المختبر يجمع **المجتمع والدولة والأمة** في محاكاة واحدة. "
        "ليس المجتمع بمعزل عن الحكم، ولا الدولة بمعزل عن القيم. الكل نسيج واحد، "
        "تحكمه المعادلة التي فطر الله عليها الوجود: **S = W × B**.",
        "This lab integrates **society, state, and nation** into one simulation. "
        "All are one fabric, governed by the equation: **S = W × B**."
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
            ax3.set_title(T("👥 صحة المجتمع – نسبة المؤمنين عبر الزمن", "👥 Society Health"), color='white', fontsize=14, fontweight='bold')
            ax3.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=9)
            ax3.grid(True, alpha=0.2); ax3.tick_params(colors='white'); ax3.set_ylim(0, 105)
            
            ax4 = axes[1, 1]; ax4.set_facecolor('#0a0f1e')
            gap = E_nation - S_nation
            ax4.fill_between(range(Y), 0, gap, where=(gap > 0), color='red', alpha=0.3, label=T('فجوة إيجابية (استدراج)', 'Positive Gap (Istidraj)'))
            ax4.fill_between(range(Y), 0, gap, where=(gap < 0), color='green', alpha=0.3, label=T('فجوة سلبية (تعافٍ)', 'Negative Gap (Recovery)'))
            ax4.axhline(y=0, color='white', lw=0.5)
            ax4.set_xlabel(T("السنوات", "Years"), color='white'); ax4.set_ylabel('E - S', color='white')
            ax4.set_title(T("⚠️ مؤشر الاستدراج (E - S)", "⚠️ Istidraj Indicator (E - S)"), color='white', fontsize=14, fontweight='bold')
            ax4.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=9)
            ax4.grid(True, alpha=0.2); ax4.tick_params(colors='white')
            
            plt.tight_layout(); st.pyplot(fig)
            
            st.divider(); st.subheader(T("📊 لوحة المؤشرات", "📊 Dashboard"))
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

# =============================================
# تبويب ٥: مقارنة الحضارات
# =============================================
with tab5:
    st.header(T("🏰 مقارنة الحضارات – صراع القيم في ميدان الزمن", "🏰 Civilization Comparison"))
    st.markdown(T(
        "قارن بين حضارتين تبدأ كل منهما بقيم مختلفة. شاهد كيف تزدهر الحضارة التي توازن بين W و B، "
        "وكيف تنهار التي تخل بهذا التوازن.",
        "Compare two civilizations starting with different values. Watch how the balanced one flourishes."
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
            ax2.set_title(T("المسار في فضاء (W, B)", "Path in (W, B) Space"), color='white', fontsize=13)
            ax2.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=8)
            ax2.grid(True, alpha=0.2); ax2.tick_params(colors='white')
            plt.tight_layout(); st.pyplot(fig)
            
            c1, c2 = st.columns(2)
            c1.metric(T("S النهائي - حضارة أ", "Final S - Civ A"), f"{Sh_a[-1]:.3f}")
            c2.metric(T("S النهائي - حضارة ب", "Final S - Civ B"), f"{Sh_b[-1]:.3f}")
            
            csv_data = "Year,S_A,E_A,S_B,E_B\n" + "\n".join([f"{t},{Sh_a[t]:.4f},{Eh_a[t]:.4f},{Sh_b[t]:.4f},{Eh_b[t]:.4f}" for t in range(Y)])
            st.download_button(T("📥 تحميل بيانات المقارنة", "📥 Download Comparison"), data=csv_data, file_name="mizan_civilizations.csv", mime="text/csv", key="dl_civ")

# =============================================
# تبويب ٦: الشواهد التاريخية
# =============================================
with tab6:
    st.header(T("📜 الشواهد التاريخية – حين ينطق التاريخ مصدقًا للمعادلة", "📜 Historical Evidence"))
    st.markdown(T(
        "اختر دولة تاريخية لترى كيف تنطبق معادلة الميزان على التاريخ الفعلي. "
        "هذه تقديرات تقريبية، والهدف منها أن تريك كيف أن سنة الله في الأمم لا تتبدل ولا تتحول.",
        "Select a historical nation to see how the Mizan equation applies to actual history."
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

print("✅ المرحلة الثالثة مكتملة: مختبر الأمة، مقارنة الحضارات، الشواهد التاريخية")

# =============================================
# المرحلة الرابعة (معدلة): هندسة الصراط والتذييل
# =============================================

# --- الثوابت الإبراهيمية ---
ABRAHAMIC_VERSE = T(
    '﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ وَالَّذِينَ مَعَهُ إِذْ قَالُوا لِقَوْمِهِمْ إِنَّا بُرَآءُ مِنكُمْ وَمِمَّا تَعْبُدُونَ مِن دُونِ اللَّهِ كَفَرْنَا بِكُمْ وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾',
    '﴿There has certainly been for you an excellent pattern in Abraham and those with him, when they said to their people, "Indeed, we are disassociated from you and from whatever you worship other than Allah. We have denied you, and there has appeared between us and you animosity and hatred forever until you believe in Allah alone."﴾'
)

def get_spiritual_nudge(situation):
    """توليد رسالة تحفيز روحي مبنية على الوحيين."""
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
# تبويب ٧: هندسة الصراط – البرهان النبوي والنموذج الإبراهيمي
# =============================================
with tab7:
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
    
    # --- التأكد من تهيئة متغيرات المسار ---
    if 'path_W' not in st.session_state:
        st.session_state.path_W = [0.5]
    if 'path_B' not in st.session_state:
        st.session_state.path_B = [0.5]
    if 'path_kappa' not in st.session_state:
        st.session_state.path_kappa = [0.0]
    for l in ["faith","worship","transactions","morals","enjoining","hudud","jihad"]:
        if f"path_{l}" not in st.session_state:
            setattr(st.session_state, f"path_{l}", [0.5])
    
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
    pW = st.session_state.path_W
    pB = st.session_state.path_B
    
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
        if hasattr(st.session_state, f"path_{key}") and len(getattr(st.session_state, f"path_{key}")) > 0:
            val = getattr(st.session_state, f"path_{key}")[-1]
        else:
            val = 0.0
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

print("✅ المرحلة الرابعة (معدلة) مكتملة: هندسة الصراط مع تهيئة آمنة للمتغيرات والتذييل")
print("✅✅✅ تم بناء مختبر الميزان – المنصة الذهبية – النسخة النهائية المتكاملة بنجاح!")
