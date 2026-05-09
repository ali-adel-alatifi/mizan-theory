import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import random
import time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="المنصة الذهبية – The Golden Platform", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# ================================================================
# قاعدة بيانات الحروف الـ 28
# ================================================================
MIZAN_LETTERS = {
    "light": {
        "أ": {"value": 1,   "label": {"ar":"الوحدانية","en":"Oneness"},        "aya": "إِيَّاكَ نَعْبُدُ"},
        "ل": {"value": 30,  "label": {"ar":"المُلك","en":"Sovereignty"},       "aya": "إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ"},
        "م": {"value": 40,  "label": {"ar":"الجمع","en":"Gathering"},          "aya": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ"},
        "ر": {"value": 200, "label": {"ar":"اليقظة","en":"Vigilance"},         "aya": "فَإِذَا فَرَغْتَ فَانصَبْ"},
        "ك": {"value": 20,  "label": {"ar":"الأمر","en":"Command"},            "aya": "كُن فَيَكُونُ"},
        "هـ": {"value": 5,   "label": {"ar":"الهوية","en":"Identity"},          "aya": "وَاجْتَنِبُوا الطَّاغُوتَ"},
        "ي": {"value": 10,  "label": {"ar":"الاستجابة","en":"Response"},       "aya": "اسْتَجِيبُوا لِلَّهِ وَلِلرَّسُولِ"},
        "ع": {"value": 70,  "label": {"ar":"الإدراك","en":"Perception"},       "aya": "وَقُل رَّبِّ زِدْنِي عِلْمًا"},
        "ص": {"value": 90,  "label": {"ar":"الصمد","en":"The Eternal"},        "aya": "اللَّهُ الصَّمَدُ"},
        "ق": {"value": 100, "label": {"ar":"الميزان","en":"The Balance"},      "aya": "وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ"},
        "ن": {"value": 50,  "label": {"ar":"النور","en":"Light"},              "aya": "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ"},
        "س": {"value": 60,  "label": {"ar":"السمع","en":"Hearing"},            "aya": "سَمِعْنَا وَأَطَعْنَا"},
        "ح": {"value": 8,   "label": {"ar":"الحياة","en":"Life"},              "aya": "فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً"},
        "ط": {"value": 9,   "label": {"ar":"الطهارة","en":"Purity"},           "aya": "إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ"},
    },
    "neutral": {
        "ف": {"value": 80,  "label": {"ar":"فاء السببية","en":"Causative Fa"}, "role": "=",  "aya": "فَمَن يَكْفُرْ بِالطَّاغُوتِ..."},
        "و": {"value": 6,   "label": {"ar":"واو العطف","en":"Conjunctive Waw"},"role": "×/+","aya": "وَيُؤْمِن بِاللَّهِ"},
        "ب": {"value": 2,   "label": {"ar":"باء الاستعانة","en":"Instrumental Ba"},"role": "بـ","aya": "بِسْمِ اللَّهِ الرَّحْمَٰنِ"},
        "ل": {"value": 30,  "label": {"ar":"لام التعليل","en":"Purpose Lam"}, "role": "→",  "aya": "لِيَعْبُدُونِ"},
        "ت": {"value": 400, "label": {"ar":"تاء الفاعل","en":"Subject Ta"},   "role": "ف",  "aya": "قَالَتِ امْرَأَتُ فِرْعَوْنَ"},
        "ث": {"value": 500, "label": {"ar":"ثم العطف","en":"Then Tha"},       "role": "ت",  "aya": "ثُمَّ خَلَقْنَا النُّطْفَةَ"},
    },
    "dark": {
        "ظ": {"value": 900, "label": {"ar":"الظلم","en":"Injustice"},          "aya": "إِنَّ الظَّالِمِينَ لَهُمْ عَذَابٌ أَلِيمٌ"},
        "ض": {"value": 800, "label": {"ar":"الضلال","en":"Misguidance"},       "aya": "وَمَن يُضْلِلِ اللَّهُ فَمَا لَهُ مِنْ هَادٍ"},
        "غ": {"value": 1000,"label": {"ar":"الغش","en":"Fraud"},               "aya": "مَنْ غَشَّنَا فَلَيْسَ مِنَّا"},
        "ذ": {"value": 700, "label": {"ar":"الذل","en":"Humiliation"},         "aya": "أَذِلَّةٍ عَلَى الْمُؤْمِنِينَ"},
        "خ": {"value": 600, "label": {"ar":"الخيانة","en":"Betrayal"},         "aya": "لَا تَخُونُوا اللَّهَ وَالرَّسُولَ"},
        "ش": {"value": 300, "label": {"ar":"الشهوة","en":"Lust"},              "aya": "وَلَا تَتَّبِعِ الْهَوَىٰ"},
        "ز": {"value": 7,   "label": {"ar":"الزور","en":"Falsehood"},          "aya": "وَاجْتَنِبُوا قَوْلَ الزُّورِ"},
        "ج": {"value": 3,   "label": {"ar":"الجهل","en":"Ignorance"},          "aya": "بَلْ أَكْثَرُهُمْ يَجْهَلُونَ"},
    }
}

# ================================================================
# نظام اللغة
# ================================================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang

def t(ar, en):
    return ar if LANG == "ar" else en

def tl(letter_dict):
    """ترجمة حقل label في الحروف"""
    return letter_dict["label"][LANG]

st.set_option('deprecation.showPyplotGlobalUse', False)

# ================================================================
# الشريط الجانبي
# ================================================================
with st.sidebar:
    lang_choice = st.radio("اللغة / Language", ["العربية", "English"], index=0 if LANG == "ar" else 1)
    if (lang_choice == "English" and LANG == "ar") or (lang_choice == "العربية" and LANG == "en"):
        st.session_state.lang = "en" if lang_choice == "English" else "ar"
        st.rerun()

    st.markdown("---")
    st.header(t("⚙️ المعاملات", "⚙️ Parameters"))
    
    W_init = st.slider(t("W الابتدائي", "Initial W"), 0.0, 1.0, 0.55, 0.01)
    B_init = st.slider(t("B الابتدائي", "Initial B"), 0.0, 1.0, 0.52, 0.01)
    delay = st.slider(t("فجوة الاستدراج", "Istidraj Gap"), 5, 50, 22, 1)
    N_STARS = st.slider(t("عدد النجوم", "Number of Stars"), 100, 600, 300, 50)
    
    st.markdown("---")
    st.subheader(t("🔮 الثوابت الإلهية", "🔮 Divine Constants"))
    q_val = st.slider(t("ق (الميزان)", "Qaf (Balance)"), 10, 200, 100, 10)
    n_val = st.slider(t("ن (النور)", "Nun (Light)"), 5, 100, 50, 5)
    s_val = st.slider(t("ص (الصمد)", "Sad (Eternal)"), 10, 200, 90, 10)
    k_val = st.slider(t("ك (الأمر)", "Kaf (Command)"), 2, 50, 20, 2)
    
    st.markdown("---")
    st.subheader(t("🏛️ أسس الحكم", "🏛️ Governance"))
    amr_val = st.slider(t("الأمر بالمعروف", "Enjoining Good"), 0.0, 1.0, 0.5, 0.01)
    nahy_val = st.slider(t("النهي عن المنكر", "Forbidding Evil"), 0.0, 1.0, 0.5, 0.01)
    adl_val = st.slider(t("العدل", "Justice"), 0.0, 1.0, 0.6, 0.01)
    shura_val = st.slider(t("الشورى", "Consultation"), 0.0, 1.0, 0.5, 0.01)
    
    st.markdown("---")
    st.subheader(t("💀 قوى الضلال", "💀 Forces of Darkness"))
    riba_val = st.slider(t("الربا", "Usury"), 0.0, 1.0, 0.2, 0.01)
    zulm_val = st.slider(t("الظلم", "Injustice"), 0.0, 1.0, 0.2, 0.01)
    khianah_val = st.slider(t("الخيانة", "Betrayal"), 0.0, 1.0, 0.2, 0.01)
    
    st.markdown("---")
    if st.button(t("▶️ تشغيل المحاكاة", "▶️ Run Simulation"), use_container_width=True):
        st.session_state.run = True
    if st.button(t("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True):
        st.session_state.run = False
    if st.button(t("🔄 إعادة ضبط", "🔄 Reset"), use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",):
                del st.session_state[k]
        st.rerun()

# ================================================================
# العنوان الرئيسي
# ================================================================
st.markdown(f"""
<div style="text-align: center; padding: 20px 0 10px 0;">
    <h1 style="color: #FFD700; font-size: 2.5em; margin-bottom: 0;">⚖️ {t('المنصة الذهبية', 'The Golden Platform')}</h1>
    <h2 style="color: #FFD700; font-size: 1.3em; margin-top: 0;">{t('S = W × B | من الذرة إلى الحضارة', 'S = W × B | From Atom to Civilization')}</h2>
</div>
""", unsafe_allow_html=True)

# ================================================================
# التبويبات
# ================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t("🏛️ المختبر الجماعي", "🏛️ The Collective Lab"),
    t("🧍 البوصلة الشخصية", "🧍 Personal Compass"),
    t("📖 كتاب الميزان", "📖 The Book of Mizan"),
    t("🔤 المعجم الهندسي", "🔤 Geometric Lexicon"),
    t("📜 رسالة الترحيب", "📜 Welcome Message"),
])

# ================================================================
# دوال مساعدة
# ================================================================
def get_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    else: return '#888888'

def calc_S(W, B, E, q_val=100, n_val=50, s_val=90, k_val=20, amr_val=0.5, nahy_val=0.5, adl_val=0.6, shura_val=0.5, riba_val=0.2, zulm_val=0.2, khianah_val=0.2):
    S_base = W * B
    divine = (n_val/50.0) ** (k_val/20.0) * np.exp(q_val/100.0 - 1)
    S_base *= divine
    S_base *= (0.5 + 0.5 * (amr_val * nahy_val))
    S_base *= (0.8 + 0.4 * adl_val)
    S_base *= (0.85 + 0.3 * shura_val)
    S_base *= (1 - 0.3 * riba_val)
    S_base *= (1 - 0.25 * zulm_val)
    S_base *= (1 - 0.15 * khianah_val)
    return np.clip(S_base, 0.001, 1.0)

# ================================================================
# تبويب 1: المختبر الجماعي – المحاكاة الحية
# ================================================================
with tab1:
    st.header(t("🏛️ المختبر الجماعي", "🏛️ The Collective Lab"))
    st.markdown(t("شاهد كيف يتفاعل الولاء (W) والبراءة (B) في مجتمع حي.", "Watch how Loyalty (W) and Disavowal (B) interact in a living society."))
    
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init' not in st.session_state: st.session_state.init = False
    
    if not st.session_state.init:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        st.session_state.cx = cx; st.session_state.cy = cy
        st.session_state.sx = np.random.uniform(cx-13, cx+13, N_STARS)
        st.session_state.sy = np.random.uniform(cy-9, cy+9, N_STARS)
        st.session_state.sw = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.sb = np.random.uniform(0.1, 1.0, N_STARS)
        st.session_state.W = W_init; st.session_state.B = B_init
        st.session_state.E = 0.3; st.session_state.S = W_init * B_init
        st.session_state.ph = t("توازن", "Balance"); st.session_state.ca = 0.0
        st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
        st.session_state.eb = deque([W_init*B_init]*30, maxlen=30)
        st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
        st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
        st.session_state.init = True

    if st.session_state.get("run", False):
        placeholder = st.empty()
        while st.session_state.get("run", False):
            W = st.session_state.W; B = st.session_state.B; E = st.session_state.E
            S = st.session_state.S; ph = st.session_state.ph; ca = st.session_state.ca
            aW = st.session_state.aW; aB = st.session_state.aB
            sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
            sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
            cx = st.session_state.cx; cy = st.session_state.cy
            eb = st.session_state.eb
            pS = st.session_state.pS.copy(); pE = st.session_state.pE.copy()
            px = st.session_state.px.copy(); pc = st.session_state.pc

            ca += 0.008; sv = np.sin(ca)
            if sv > 0.5: ph = t('ذروة الاستقرار', 'Peak Stability')
            elif sv > 0: ph = t('صعود', 'Rising')
            elif sv > -0.5: ph = t('انهيار', 'Collapse')
            else: ph = t('القاع', 'Rock Bottom')
            if 0.3 < sv < 0.35: ph = t('>> استدراج <<', '>> Istidraj <<')
            target_S = 0.5 + 0.45*sv

            for i in range(N_STARS):
                dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
                close = (dist < 2.0) & (np.arange(N_STARS) != i)
                sw[i] += (target_S - sw[i])*0.02 + np.random.uniform(-0.02,0.02)
                sb[i] += (target_S - sb[i])*0.02 + np.random.uniform(-0.02,0.02)
                if np.any(close):
                    sw[i] += (np.mean(sw[close])-sw[i])*0.03
                    sb[i] += (np.mean(sb[close])-sb[i])*0.03
                sw[i] = np.clip(sw[i], 0.01, 1.0)
                sb[i] = np.clip(sb[i], 0.01, 1.0)

            if random.random() < 0.005:
                aff = np.random.choice(N_STARS, size=int(N_STARS*0.2), replace=False)
                sw[aff] *= np.random.uniform(0.5,0.8); sb[aff] *= np.random.uniform(0.5,0.8)

            avgW = np.mean(sw); avgB = np.mean(sb)
            W += (avgW-W)*0.04; B += (avgB-B)*0.04
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            
            S = calc_S(W, B, E, q_val, n_val, s_val, k_val, amr_val, nahy_val, adl_val, shura_val, riba_val, zulm_val, khianah_val)
            eb.append(S)
            E_target = list(eb)[-delay] if len(eb) >= delay else S
            E += 0.03*(E_target - E)
            
            W = W - 0.015*E + 0.03/(S+0.1) - 0.007*(1-B)
            B = B - 0.012*E + 0.006*(1-B)*W*(1-W)
            W = np.clip(W, 0.01, 1.0); B = np.clip(B, 0.01, 1.0)
            S = calc_S(W, B, E, q_val, n_val, s_val, k_val, amr_val, nahy_val, adl_val, shura_val, riba_val, zulm_val, khianah_val)
            
            pc += 1
            if pc % 2 == 0:
                pS.append(S); pE.append(E); px.append(len(px))
            
            aW += 0.02 + random.uniform(-0.025,0.025)*(1-W)**2
            aB += 0.02 + random.uniform(-0.025,0.025)*(1-B)**2
            wx = cx + (7-2.5*W)*np.cos(aW); wy = cy + (7-2.5*W)*np.sin(aW)*0.7
            bx = cx + (5-1.5*B)*np.cos(aB); by = cy + (5-1.5*B)*np.sin(aB)*0.7
            
            sx += np.random.uniform(-0.07,0.07,N_STARS)*(1-np.mean(sw*sb))
            sy += np.random.uniform(-0.07,0.07,N_STARS)*(1-np.mean(sw*sb))
            sx = np.clip(sx, cx-13, cx+13); sy = np.clip(sy, cy-9, cy+9)
            
            st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
            st.session_state.ph=ph; st.session_state.ca=ca
            st.session_state.aW=aW; st.session_state.aB=aB
            st.session_state.eb=eb
            st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
            st.session_state.pS=pS; st.session_state.pE=pE; st.session_state.px=px; st.session_state.pc=pc
            
            fig, ax = plt.subplots(figsize=(14,10), facecolor='#000010')
            ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
            
            for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                          (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
            ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
            
            ax.add_patch(Circle((cx,cy), 0.5+16*E, color='#0FF', alpha=0.25*(1-min(E,1))+0.04, zorder=7))
            ax.add_patch(Circle((cx,cy), 8.5, color='#0F8', alpha=0.15, fill=False, lw=2.5, zorder=2))
            
            ax.add_patch(Circle((wx,wy), 0.2+0.6*W, color='#FFF', alpha=1, zorder=13))
            ax.add_patch(Circle((bx,by), 0.2+0.6*B, color='#F33', alpha=0.8, zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            
            colors = [get_color(sw[i],sb[i]) for i in range(N_STARS)]
            ax.scatter(sx, sy, s=35, c=colors, alpha=0.9, edgecolors='white', linewidths=0.4, zorder=5)
            
            pax = ax.inset_axes([0.5,0.02,0.46,0.10])
            pax.set_xlim(0,400); pax.set_ylim(0,1.05)
            pax.set_title(t('S (الذهب) يقود E (السماوي) – الاستدراج', 'S (Gold) leads E (Cyan) – Istidraj'), color='white', fontsize=7)
            pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
            pSl=list(pS); pEl=list(pE); pxl=list(px)
            if pSl: pax.plot(pxl,pSl,color='#FFD700',lw=2); pax.plot(pxl,pEl,color='#0FF',lw=1.5)
            
            ax.text(14,1.2,f'{ph} | S={S:.2f} | E={E:.2f}',color='white',fontsize=12,ha='center')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.08)
        st.success(t("✅ تم إيقاف المحاكاة.", "✅ Simulation stopped."))

# ================================================================
# تبويب 2: البوصلة الشخصية (28 سؤالاً)
# ================================================================
with tab2:
    st.header(t("🧭 البوصلة الشخصية", "🧭 Personal Compass"))
    st.markdown(t("أجب عن 28 سؤالاً لتكتشف موقعك في فضاء الولاء والبراءة.", "Answer 28 questions to discover your position in loyalty-disavowal space."))
    
    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    questions = {
        "W": [
            ("هل تعيش لله وحده؟", "Do you live for Allah alone?"),
            ("هل تقيم الصلاة بخشوع؟", "Do you pray with devotion?"),
            ("هل تؤدي الزكاة وتتصدق؟", "Do you pay Zakat & give charity?"),
            ("هل تصوم رمضان وتطوعًا؟", "Do you fast Ramadan & voluntarily?"),
            ("هل تحج أو تسعى للحج؟", "Do you perform/seek Hajj?"),
            ("هل تحب الله ورسوله أكثر من كل شيء؟", "Do you love Allah & Messenger most?"),
            ("هل تصدق في أقوالك وأفعالك؟", "Are you truthful?"),
            ("هل تؤدي الأمانات؟", "Do you fulfill trusts?"),
            ("هل تتوكل على الله مع الأخذ بالأسباب؟", "Do you rely on Allah while using means?"),
            ("هل تشكر في الرخاء وتصبر في البلاء؟", "Are you grateful & patient?"),
            ("هل تحمل هم الإسلام والمسلمين؟", "Do you care for Islam & Muslims?"),
            ("هل تفي بالعهد؟", "Do you keep your promises?"),
            ("هل أنت راضٍ بما قسم الله لك؟", "Are you content with Allah's decree?"),
            ("هل تنصر المؤمن إذا ظُلم؟", "Do you help the oppressed believer?"),
        ],
        "B": [
            ("هل تأمر بالمعروف؟", "Do you enjoin good?"),
            ("هل تنهى عن المنكر؟", "Do you forbid evil?"),
            ("هل أنت مستعد لبذل النفس والمال في سبيل الله؟", "Ready to sacrifice for Allah?"),
            ("هل تتبرأ من الشرك وأهله؟", "Do you disavow polytheism?"),
            ("هل ترفض الكفر والإلحاد؟", "Do you reject disbelief/atheism?"),
            ("هل تكره النفاق والتلون؟", "Do you hate hypocrisy?"),
            ("هل تجاهد نفسك على ترك الكذب؟", "Do you struggle against lying?"),
            ("هل تتجنب الغش في معاملاتك؟", "Do you avoid fraud?"),
            ("هل تفي بعهودك ولا تخون؟", "Do you keep trusts, no betrayal?"),
            ("هل ترفض الظلم بكل صوره؟", "Do you reject all injustice?"),
            ("هل تجاهد نفسك على ترك الفواحش؟", "Do you struggle against immorality?"),
            ("هل تخلص عملك لله وتجتنب الرياء؟", "Is your work sincere, no showing off?"),
            ("هل تسلم لله في قسمته ولا تحسد؟", "Do you accept Allah's decree, no envy?"),
            ("هل تحب في الله وتبغض في الله؟", "Do you love & hate for Allah's sake?"),
        ]
    }

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("🤍 أسئلة الولاء (W)", "🤍 Loyalty Questions (W)"))
        for i, (q_ar, q_en) in enumerate(questions["W"]):
            q = q_ar if LANG == "ar" else q_en
            ans = st.radio(q, [t("نعم (10)", "Yes (10)"), t("أحيانًا (5)", "Sometimes (5)"), t("لا (0)", "No (0)")], key=f"w_{i}", index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"W{i}"] = 10
                elif t("أحيانًا","Sometimes") in ans: st.session_state.compass_answers[f"W{i}"] = 5
                else: st.session_state.compass_answers[f"W{i}"] = 0
    with col2:
        st.subheader(t("❤️ أسئلة البراءة (B)", "❤️ Disavowal Questions (B)"))
        for i, (q_ar, q_en) in enumerate(questions["B"]):
            q = q_ar if LANG == "ar" else q_en
            ans = st.radio(q, [t("نعم (10)", "Yes (10)"), t("أحيانًا (5)", "Sometimes (5)"), t("لا (0)", "No (0)")], key=f"b_{i}", index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"B{i}"] = 10
                elif t("أحيانًا","Sometimes") in ans: st.session_state.compass_answers[f"B{i}"] = 5
                else: st.session_state.compass_answers[f"B{i}"] = 0

    if len(st.session_state.compass_answers) == 28:
        W_score = sum(st.session_state.compass_answers[f"W{i}"] for i in range(14))
        B_score = sum(st.session_state.compass_answers[f"B{i}"] for i in range(14))
        W_val = W_score / 140.0; B_val = B_score / 140.0
        S_val = W_val * B_val
        
        if W_val >= 0.5 and B_val >= 0.5:
            q_name, q_color = t("مؤمن (الربع الأول)", "Believer (Q1)"), '#FFD700'
        elif W_val < 0.5 and B_val >= 0.5:
            q_name, q_color = t("كافر (الربع الثاني)", "Disbeliever (Q2)"), '#FF5252'
        elif W_val < 0.5 and B_val < 0.5:
            q_name, q_color = t("منافق (الربع الثالث)", "Hypocrite (Q3)"), '#FFB6C1'
        else:
            q_name, q_color = t("مشرك (الربع الرابع)", "Polytheist (Q4)"), '#FFA500'
        
        st.divider()
        st.subheader(t("📊 نتيجتك", "📊 Your Result"))
        c1, c2, c3 = st.columns(3)
        c1.metric("W", f"{W_val:.2f}"); c2.metric("B", f"{B_val:.2f}"); c3.metric("S", f"{S_val:.2f}")
        st.markdown(f"<h2 style='color:{q_color}; text-align:center;'>{q_name}</h2>", unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(6,6), facecolor='#0a0a2e')
        ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.set_xlabel("B", color='white'); ax.set_ylabel("W", color='white')
        L_map = W_val*2-1; D_map = B_val*2-1
        ax.scatter(D_map, L_map, c='cyan', s=250, edgecolors='white', linewidth=3, zorder=10)
        ax.fill_between([0,1],0,1,alpha=0.15,color='gold'); ax.fill_between([-1,0],0,1,alpha=0.15,color='red')
        ax.fill_between([-1,0],-1,0,alpha=0.15,color='pink'); ax.fill_between([0,1],-1,0,alpha=0.15,color='orange')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        if st.button(t("🔄 إعادة الاختبار", "🔄 Retake Test")):
            st.session_state.compass_answers = {}
            st.rerun()

# ================================================================
# تبويب 3: كتاب الميزان
# ================================================================
with tab3:
    st.header(t("📖 كتاب الميزان", "📖 The Book of Mizan"))
    
    with st.expander(t("📜 الإهداء والمقدمة", "📜 Dedication & Introduction")):
        st.markdown(t("""
        **الإهداء**: إلى كل باحث عن الحقيقة، يبحث عن الخيط الناظم الذي يربط شتات هذا الوجود.
        
        **مقدمة المؤلف**: هذا كتاب "الميزان". يقدم "الدين القيم" (قانون السببية الأعظم) و"الإسلام الحنيف" (الاستجابة المثلى لهذا القانون) كمنظومة متكاملة تفسر الوجود من الذرة إلى الحضارة، ومن الأزل إلى الخلود.
        
        المعادلة المركزية: **S = W × B**
        """,
        """
        **Dedication**: To every seeker of truth, searching for the thread that binds existence together.
        
        **Author's Introduction**: This is the Book of Mizan. It presents "Al-Deen Al-Qayyim" (the supreme law of causality) and "Al-Islam Al-Hanif" (the optimal response to this law) as an integrated system explaining existence from the atom to civilization, and from eternity to eternity.
        
        The central equation: **S = W × B**
        """))
    
    with st.expander(t("🔍 تمهيد: البحث عن القانون الأعظم", "🔍 Prologue: The Search for the Supreme Law")):
        st.markdown(t("""
        منذ فجر الوعي، والبشرية تبحث عن القانون الذي يحكم الوجود.
        في الفيزياء، قضى أينشتاين عقوده الأخيرة باحثًا عن "نظرية المجال الموحد". فشل. لماذا؟ لأنه كان يبحث في المكان الخطأ.
        
        هذا الكتاب يقدم الإجابة من عند خالق الكون نفسه: **S = W × B**.
        """,
        """
        Since the dawn of consciousness, humanity has searched for the law governing existence.
        In physics, Einstein spent his last decades searching for a "Unified Field Theory". He failed. Why? Because he was looking in the wrong place.
        
        This book presents the answer from the Creator of the universe Himself: **S = W × B**.
        """))
    
    with st.expander(t("⚖️ الفصل الثاني: معادلة الثبات", "⚖️ Chapter 2: The Stability Equation")):
        st.markdown(t("""
        **S = W × B**
        
        - **W (الولاء)**: طاقة الحب والطاعة والنصرة نحو الله ورسوله والمؤمنين.
        - **B (البراءة)**: طاقة البغض والمفاصلة والمناعة من الكفر والشرك والطاغوت.
        - **S (الثبات)**: العروة الوثقى – حالة الاستقرار الوجودي.
        
        لماذا الضرب وليس الجمع؟ لأن العلاقة شرطية: لا يصح إيمان بلا براءة.
        """,
        """
        **S = W × B**
        
        - **W (Loyalty)**: The energy of love, obedience, and support towards Allah, His Messenger, and the believers.
        - **B (Disavowal)**: The energy of hatred, disassociation, and immunity from disbelief, polytheism, and false deities.
        - **S (Stability)**: The Firm Handhold – the state of existential stability.
        
        Why multiplication and not addition? Because the relationship is conditional: faith without disavowal is invalid.
        """))

# ================================================================
# تبويب 4: المعجم الهندسي
# ================================================================
with tab4:
    st.header(t("🔤 المعجم الهندسي للقرآن", "🔤 Geometric Lexicon of the Quran"))
    st.markdown(t("اكتشف كيف تترجم أدوات القرآن إلى مشغلات رياضية.", "Discover how Quranic particles translate into mathematical operators."))
    
    tools = {
        "فاء السببية (فَـ)": ("=", {"ar":"علامة يساوي. تربط السبب بالنتيجة حتمًا.", "en":"Equals sign. Inevitably connects cause to effect."}),
        "واو المعية (الضرب)": ("×", {"ar":"ربط شرطي: لا يتم الأمر إلا باجتماعهما.", "en":"Conditional conjunction: only complete with both."}),
        "واو الاستئناف (الجمع)": ("+", {"ar":"جمع تراكمي في مقام الحساب.", "en":"Accumulative addition in the context of reckoning."}),
        "لام التعليل (لِـ)": ("→", {"ar":"سهم الغاية. يوضح اتجاه المقصد.", "en":"Arrow of purpose. Shows direction of intent."}),
        "حتى الغائية": ("...", {"ar":"استمرار السبب حتى تتحقق النتيجة.", "en":"Continuation of cause until result."}),
        "إن الشرطية": ("( )ᵒ", {"ar":"قوس الشرط الاختياري. يمثل حرية الإنسان.", "en":"Optional condition. Represents human free will."}),
        "إذا الشرطية": ("( )ᶜ", {"ar":"قوس الشرط المحقق. يمثل حتمية الجزاء.", "en":"Certain condition. Represents inevitability of recompense."}),
        "إلا": ("{}", {"ar":"حدود المجموعة. تحدد أهل الولاية.", "en":"Set boundaries. Defines the people of loyalty."}),
        "كلا": ("⛔", {"ar":"قطع الأسباب الباطلة والمعادلات الفاسدة.", "en":"Severing false causes and corrupt equations."}),
    }
    
    sel = st.selectbox(t("اختر أداة:", "Select a tool:"), list(tools.keys()))
    if sel:
        st.metric(t("الرمز", "Symbol"), tools[sel][0])
        st.info(tools[sel][1][LANG])

# ================================================================
# تبويب 5: رسالة الترحيب
# ================================================================
with tab5:
    st.header(t("📜 رسالة الترحيب", "📜 Welcome Message"))
    st.markdown(t("""
    <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">

    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
    > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"

    ---

    **الدين القيم** = قانون السببية الكوني، وهو الحق لأن واضعه الحق،
    وهو القيم لأنه من القيوم نفسه. هو القانون الأعظم، إنه "الدين القيم"
    الذي هو أصل الوجود وغايته.

    ---

    <b style="color: #FFD700;">
    ﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ
    لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ وَلَٰكِنَّ أَكْثَرَ النَّاسِ لَا يَعْلَمُونَ﴾
    <br>— الروم 30
    </b>

    ---

    > "أيها البشر، لستم في فوضى. هناك قانون. هناك نظام. هناك ميزان.<br>
    > استقراركم ليس صدفة. انهياركم ليس حظاً سيئاً.<br>
    > إنها معادلة. إنها <b style="color: #FFD700;">S = W × B</b>."

    ---

    <b style="color: #FFD700;">Ali Adel Alatifi | علي عادل العاطفي | 2026</b>
    </div>
    """,
    """
    <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">

    > "Is there a single law governing the atom and civilization?<br>
    > This is the Mizan Model that proves <b style="color: #FFD700;">S = W × B</b>"

    ---

    **Al-Deen Al-Qayyim** = The cosmic law of causality, true because its Originator is the Truth,
    upright because it comes from the Self-Subsisting. It is the supreme law, the Upright Religion
    that is the origin of existence and its ultimate purpose.

    ---

    <b style="color: #FFD700;">
    ﴿So direct your face toward the religion, inclining to truth. [Adhere to] the fitrah of Allah
    upon which He has created [all] people. No change should there be in the creation of Allah.
    That is the correct religion, but most people do not know.﴾
    <br>— Ar-Rum 30
    </b>

    ---

    > "O humanity, you are not in chaos. There is a law. There is a system. There is a balance.<br>
    > Your stability is not a coincidence. Your collapse is not bad luck.<br>
    > It is an equation. It is <b style="color: #FFD700;">S = W × B</b>."

    ---

    <b style="color: #FFD700;">Ali Adel Alatifi | علي عادل العاطفي | 2026</b>
    </div>
    """), unsafe_allow_html=True)

# ================================================================
# التذييل
# ================================================================
st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#888;'>{t('© 2026 علي عادل العاطفي | المنصة الذهبية', '© 2026 Ali Adel Alatifi | The Golden Platform')}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:#FFD700; font-size: 1.2em;'>⚖️ S = W × B</p>", unsafe_allow_html=True)
