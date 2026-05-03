import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, RegularPolygon
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="نظرية الميزان", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# قاموس الحروف
MIZAN_LETTERS = {
    "light": {
        "أ": {"value": 1, "label": "الوحدانية", "aya": "إِيَّاكَ نَعْبُدُ"},
        "ل": {"value": 30, "label": "المُلك", "aya": "إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ"},
        "م": {"value": 40, "label": "الجمع", "aya": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ"},
        "ر": {"value": 200, "label": "اليقظة", "aya": "فَإِذَا فَرَغْتَ فَانصَبْ"},
        "ك": {"value": 20, "label": "الأمر", "aya": "كُن فَيَكُونُ"},
        "هـ": {"value": 5, "label": "الهوية", "aya": "وَاجْتَنِبُوا الطَّاغُوتَ"},
        "ي": {"value": 10, "label": "الاستجابة", "aya": "اسْتَجِيبُوا لِلَّهِ وَلِلرَّسُولِ"},
        "ع": {"value": 70, "label": "الإدراك", "aya": "وَقُل رَّبِّ زِدْنِي عِلْمًا"},
        "ص": {"value": 90, "label": "الصمد", "aya": "اللَّهُ الصَّمَدُ"},
        "ق": {"value": 100, "label": "الميزان", "aya": "وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ"},
        "ن": {"value": 50, "label": "النور", "aya": "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ"},
        "س": {"value": 60, "label": "السمع", "aya": "سَمِعْنَا وَأَطَعْنَا"},
        "ح": {"value": 8, "label": "الحياة", "aya": "فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً"},
        "ط": {"value": 9, "label": "الطهارة", "aya": "إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ"},
    },
    "neutral": {
        "ف": {"value": 80, "label": "فاء السببية", "role": "=", "aya": "فَمَن يَكْفُرْ بِالطَّاغُوتِ..."},
        "و": {"value": 6, "label": "واو العطف", "role": "×/+", "aya": "وَيُؤْمِن بِاللَّهِ"},
        "ب": {"value": 2, "label": "باء الاستعانة", "role": "بـ", "aya": "بِسْمِ اللَّهِ الرَّحْمَٰنِ"},
        "ل": {"value": 30, "label": "لام التعليل", "role": "→", "aya": "لِيَعْبُدُونِ"},
        "ت": {"value": 400, "label": "تاء الفاعل", "role": "ف", "aya": "قَالَتِ امْرَأَتُ فِرْعَوْنَ"},
        "ث": {"value": 500, "label": "ثم العطف", "role": "ت", "aya": "ثُمَّ خَلَقْنَا النُّطْفَةَ"},
    },
    "dark": {
        "ظ": {"value": 900, "label": "الظلم", "aya": "إِنَّ الظَّالِمِينَ لَهُمْ عَذَابٌ أَلِيمٌ"},
        "ض": {"value": 800, "label": "الضلال", "aya": "وَمَن يُضْلِلِ اللَّهُ فَمَا لَهُ مِنْ هَادٍ"},
        "غ": {"value": 1000, "label": "الغش", "aya": "مَنْ غَشَّنَا فَلَيْسَ مِنَّا"},
        "ذ": {"value": 700, "label": "الذل", "aya": "أَذِلَّةٍ عَلَى الْمُؤْمِنِينَ"},
        "خ": {"value": 600, "label": "الخيانة", "aya": "لَا تَخُونُوا اللَّهَ وَالرَّسُولَ"},
        "ش": {"value": 300, "label": "الشهوة", "aya": "وَلَا تَتَّبِعِ الْهَوَىٰ"},
        "ز": {"value": 7, "label": "الزور", "aya": "وَاجْتَنِبُوا قَوْلَ الزُّورِ"},
        "ج": {"value": 3, "label": "الجهل", "aya": "بَلْ أَكْثَرُهُمْ يَجْهَلُونَ"},
    }
}

if "lang" not in st.session_state: st.session_state.lang = "ar"
lang = st.session_state.lang
T = {
    "ar": {
        "title": "نظرية الميزان",
        "subtitle": "S = W × B | 28 حرفاً | الفيزياء والكيمياء والبيولوجيا والأخلاق",
        "quote": "الاستقرار الحقيقي (S) ينبع من الداخل (W × B)، أما الانهيار فيبدأ من الخارج (E). ليست النعم دليل رضا، بل اختبار استدراج.",
        "author": "علي عادل العاطفي",
        "run": "▶️ تشغيل", "stop": "⏹️ إيقاف", "reset": "🔄 إعادة ضبط", "download": "📥 تحميل",
        "footer": "2026 | علي عادل العاطفي",
        "balance_good": "✅ توازن تام", "simulation_stopped": "⏸️ تم الإيقاف",
        "help_title": "📖 دليل الحروف", "help_content": "تأليف: علي عادل العاطفي"
    },
    "en": {
        "title": "The Mizan Principle",
        "subtitle": "S = W × B | 28 Letters | Physics, Chemistry, Biology & Ethics",
        "quote": "True stability (S) comes from within (W × B). When you see people collapsing morally yet flooded with blessings, know it is Istidraj.",
        "author": "Ali Adel Alatifi",
        "run": "▶️ Run", "stop": "⏹️ Stop", "reset": "🔄 Reset", "download": "📥 Download",
        "footer": "2026 | Ali Adel Alatifi",
        "balance_good": "✅ Perfect Balance", "simulation_stopped": "⏸️ Stopped",
        "help_title": "📖 Guide", "help_content": "By Ali Adel Alatifi"
    }
}
T = T.get(lang, T["ar"])

# --- اختيار اللغة ---
col_lang, col_title = st.columns([1, 4])
with col_lang:
    lang_options = {"ar": "🇸🇦 العربية", "en": "🇬🇧 English"}
    selected_lang = st.selectbox("اللغة", options=list(lang_options.keys()), format_func=lambda x: lang_options[x], index=list(lang_options.keys()).index(lang), key="lang_selector")
    if selected_lang != lang: st.session_state.lang = selected_lang; st.rerun()

# --- تصميم الواجهة الفاخرة ---
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%); padding: 40px 20px; border-radius: 20px; margin-bottom: 30px; border: 1px solid #FFD700; box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);">
    <div style="text-align: center; margin-bottom: 30px;">
        <span style="font-size: 48px;">⚖️</span>
        <h1 style="color: #FFD700; font-size: 42px; margin: 10px 0; font-weight: 900; letter-spacing: 3px; text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);">
            {T['title']}
        </h1>
        <span style="font-size: 48px;">⚖️</span>
    </div>
    
    <div style="background: rgba(255, 215, 0, 0.05); border-right: 3px solid #FFD700; border-left: 3px solid #FFD700; padding: 20px 30px; margin: 20px 0; border-radius: 10px;">
        <p style="color: #e0e0e0; font-size: 18px; line-height: 1.8; text-align: center; font-style: italic;">
            "{T['quote']}"
        </p>
    </div>
    
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #FFD700; font-size: 22px; margin: 0; font-weight: bold;">{T['author']}</p>
        <p style="color: #aaaaaa; font-size: 14px; margin: 5px 0 15px 0;">{T['subtitle']}</p>
        <div style="width: 100px; height: 2px; background: linear-gradient(90deg, transparent, #FFD700, transparent); margin: 15px auto;"></div>
        <p style="color: #666; font-size: 12px;">{T['footer']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- الشريط الجانبي ---
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:15px;background:linear-gradient(135deg,#0a0a0a,#1a1a2e);border-radius:10px;margin-bottom:10px;border:1px solid #FFD700;'>
        <h2 style='color:#FFD700;margin:0;'>⚖️ الميزان</h2>
        <p style='color:#e0e0e0;font-size:12px;'>S = W × B</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🕌 أركان الإسلام")
    prayer = st.slider("🟣 الصلاة", 0.0, 1.0, 0.8, 0.01, key="p")
    zakat = st.slider("🟡 الزكاة", 0.0, 1.0, 0.6, 0.01, key="z")
    fasting = st.slider("🟠 الصوم", 0.0, 1.0, 0.7, 0.01, key="f")
    hajj = st.slider("🔵 الحج", 0.0, 1.0, 0.5, 0.01, key="h")
    st.subheader("🏛️ أسس الحكم")
    amr = st.slider("📢 الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01, key="am")
    nahy = st.slider("🚫 النهي عن المنكر", 0.0, 1.0, 0.5, 0.01, key="na")
    adl = st.slider("⚖️ العدل", 0.0, 1.0, 0.6, 0.01, key="ad")
    shura = st.slider("🤝 الشورى", 0.0, 1.0, 0.5, 0.01, key="sh")
    
    st.header("🔤 الحروف العربية الـ 28")
    with st.expander("🔆 النورانية (14)", expanded=False):
        light_vals = {}
        for letter, data in MIZAN_LETTERS["light"].items():
            light_vals[letter] = st.slider(f"{letter} ({data['label']})", 0.0, 1.0, 0.7, 0.01, help=data['aya'], key=f"l_{letter}")
    with st.expander("⚙️ المحايدة (6)", expanded=False):
        neutral_vals = {}
        for letter, data in MIZAN_LETTERS["neutral"].items():
            neutral_vals[letter] = st.slider(f"{letter} ({data['label']})", 0.0, 1.0, 0.5, 0.01, help=data['aya'], key=f"n_{letter}")
    with st.expander("🌑 الظلامية (8)", expanded=False):
        dark_vals = {}
        for letter, data in MIZAN_LETTERS["dark"].items():
            dark_vals[letter] = st.slider(f"{letter} ({data['label']})", 0.0, 1.0, 0.2, 0.01, help=data['aya'], key=f"d_{letter}")
            
    st.subheader("⚙️ معاملات")
    W_init = st.slider("W الابتدائي", 0.0, 1.0, 0.55, 0.01, key="wi")
    B_init = st.slider("B الابتدائي", 0.0, 1.0, 0.52, 0.01, key="bi")
    N_STARS = st.slider("النجوم", 100, 600, 300, 50, key="ns")
    cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001, key="cs")
    delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1, key="df")
    
    c1, c2, c3 = st.columns(3)
    if c1.button(T["run"], use_container_width=True): st.session_state.run = True
    if c2.button(T["stop"], use_container_width=True): st.session_state.run = False
    if c3.button(T["reset"], use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

# --- الدوال المساعدة ---
def get_color(w, b):
    try:
        w=float(w); b=float(b)
        if w>=0.7 and b>=0.7: return '#FFD700'
        elif w>=0.55 and b<0.45: return '#E0E0E0'
        elif w<0.45 and b>=0.55: return '#FF5252'
        elif w<0.45 and b<0.45: return '#FF8A80'
        elif w>b: return '#FFF9C4'
        else: return '#FFCCBC'
    except: return '#888888'

def calc_S(W, B, E, prayer, zakat, fasting, hajj, amr, nahy, adl, shura, light_vals, dark_vals):
    ق=light_vals.get('ق',0.7)*100; ن=light_vals.get('ن',0.7)*50; ص=light_vals.get('ص',0.7)*90; ط=light_vals.get('ط',0.7)*9; ح=light_vals.get('ح',0.7)*8; أ=light_vals.get('أ',0.7)*1; ل=light_vals.get('ل',0.7)*30; م=light_vals.get('م',0.7)*40; ر=light_vals.get('ر',0.7)*200; ي=light_vals.get('ي',0.7)*10; ع=light_vals.get('ع',0.7)*70; س=light_vals.get('س',0.7)*60; هـ=light_vals.get('هـ',0.7)*5
    ظ=dark_vals.get('ظ',0.2)*900; ض=dark_vals.get('ض',0.2)*800; ش=dark_vals.get('ش',0.2)*300; ج=dark_vals.get('ج',0.2)*3; غ=dark_vals.get('غ',0.2)*1000; ذ=dark_vals.get('ذ',0.2)*700; خ=dark_vals.get('خ',0.2)*600
    Sb=W*B
    pb=(prayer*(0.5+0.5*min(1,ن/50))+zakat*(0.5+0.5*min(1,ص/90))+fasting*(0.5+0.5*min(1,ط/9))+hajj*(0.5+0.5*min(1,ح/8)))/4
    Sb*=(0.5+0.5*pb)
    pr=(amr*W*(0.5+0.5*min(1,ل/30))+nahy*B*(0.5+0.5*min(1,ق/100)))/2
    Sb*=(0.8+0.4*pr)
    Sb*=(0.9+0.2*adl*(0.5+0.5*min(1,ل/30)))
    Sb*=(0.85+0.3*shura*(0.5+0.5*min(1,م/40)))
    Sb*=(1+0.05*min(1,أ/1))*(1+0.02*min(1,ر/200))*(1+0.03*min(1,ي/10))*(1+0.04*min(1,ع/70))*(1+0.01*min(1,س/60))*(1+0.01*min(1,هـ/5))
    df=1.0-0.05*min(1,ظ/900)-0.03*min(1,ض/800)-0.04*min(1,ش/300)-0.02*min(1,ج/3)
    df=max(0.1,df); Sb*=df
    if E>Sb: Sb-=0.3*(1+0.5*min(1,غ/1000))*(E-Sb)
    Ww=W*(1-0.15*min(1,خ/600)); Bw=B*(1-0.15*min(1,ذ/700))
    Sf=Ww*Bw
    Sf*=(0.5+0.5*pb)*(0.8+0.4*pr)*(0.9+0.2*adl*(0.5+0.5*min(1,ل/30)))*(0.85+0.3*shura*(0.5+0.5*min(1,م/40)))*df
    return np.clip(Sf,0.001,1.0)

def check_warnings(W,B,S,E,ph):
    w=[]
    if E>S*1.5: w.append("⚠️ فجوة استدراج")
    elif E>S*1.2: w.append("⚡ بداية استدراج")
    if abs(W-B)>0.3: w.append("⚖️ اختلال كبير")
    elif abs(W-B)>0.2: w.append("📊 ميلان")
    if S<0.2: w.append("🔴 انهيار")
    elif S<0.3: w.append("🟠 خطر")
    if 'ISTIDRAJ' in ph: w.append("💀 استدراج")
    elif 'RECOVERY' in ph: w.append("🌱 تعافي")
    return w

def create_heatmap(sw,sb):
    fig,ax=plt.subplots(figsize=(3,2.5),facecolor='#000010')
    wr=np.linspace(0,1,20); br=np.linspace(0,1,20)
    Wg,Bg=np.meshgrid(wr,br); Sg=Wg*Bg
    ax.pcolormesh(Wg,Bg,Sg,cmap='RdYlGn',shading='auto',vmin=0,vmax=1)
    ax.scatter(sw,sb,c='white',s=2,alpha=0.6)
    ax.set_xlabel('W',color='white',fontsize=6); ax.set_ylabel('B',color='white',fontsize=6)
    ax.set_title('S = W × B',color='white',fontsize=7)
    ax.tick_params(colors='white',labelsize=4)
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    plt.tight_layout(pad=0.5)
    return fig

if 'run' not in st.session_state: st.session_state.run=False
if 'init' not in st.session_state: st.session_state.init=False

if not st.session_state.init:
    try:
        seed=42; np.random.seed(seed); random.seed(seed)
        cx,cy=14,10.0
        st.session_state.cx=cx; st.session_state.cy=cy
        st.session_state.sx=np.random.uniform(cx-13,cx+13,N_STARS)
        st.session_state.sy=np.random.uniform(cy-9,cy+9,N_STARS)
        st.session_state.sw=np.random.uniform(0.1,1.0,N_STARS)
        st.session_state.sb=np.random.uniform(0.1,1.0,N_STARS)
        st.session_state.W=W_init; st.session_state.B=B_init
        st.session_state.E=0.3; st.session_state.S=W_init*B_init
        st.session_state.ph="Balance"; st.session_state.ca=0.0
        st.session_state.aW=0.0; st.session_state.aB=np.pi*0.5; st.session_state.aa=0.0
        st.session_state.eb=deque([W_init*B_init]*30,maxlen=30)
        st.session_state.pS=deque(maxlen=400); st.session_state.pE=deque(maxlen=400)
        st.session_state.px=deque(maxlen=400); st.session_state.pc=0
        st.session_state.init=True
    except Exception as e:
        st.error(f"خطأ: {str(e)}")
        st.session_state.init=False

if st.session_state.init:
    c1,c2,c3=st.columns(3)
    with c1: st.metric("⚖️ S",f"{st.session_state.S:.3f}"); st.metric("🤍 W",f"{st.session_state.W:.3f}")
    with c2: st.metric("💫 E",f"{st.session_state.E:.3f}"); st.metric("❤️ B",f"{st.session_state.B:.3f}")
    with c3: st.metric("📊 المرحلة",st.session_state.ph); st.metric("⭐ متوسط S*",f"{np.mean(st.session_state.sw*st.session_state.sb):.3f}")
    warns=check_warnings(st.session_state.W,st.session_state.B,st.session_state.S,st.session_state.E,st.session_state.ph)
    if warns: st.warning(" | ".join(warns))
    else: st.success(T["balance_good"])

if st.session_state.get("run",False):
    placeholder=st.empty(); progress_text=st.empty(); warn_placeholder=st.empty()
    while st.session_state.get("run",False):
        try:
            W=st.session_state.W; B=st.session_state.B; E=st.session_state.E
            S=st.session_state.S; ph=st.session_state.ph; ca=st.session_state.ca
            aW=st.session_state.aW; aB=st.session_state.aB; aa=st.session_state.aa
            sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
            sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
            cx=st.session_state.cx; cy=st.session_state.cy
            eb=st.session_state.eb
            pS=st.session_state.pS.copy(); pE=st.session_state.pE.copy()
            px=st.session_state.px.copy(); pc=st.session_state.pc

            ca+=cycle_speed; sv=np.sin(ca)
            if sv>0.5: ph='Peak Stability'
            elif sv>0: ph='Rising'
            elif sv>-0.5: ph='Collapsing'
            else: ph='Rock Bottom'
            if 0.3<sv<0.35: ph='>> ISTIDRAJ <<'
            if -0.35<sv<-0.3: ph='>> RECOVERY <<'
            target_S=0.5+0.45*sv

            n_stars=len(sw)
            for i in range(n_stars):
                wb=prayer*0.01*(0.5+0.5*light_vals.get('ن',0.7))
                bb=fasting*0.01*(0.5+0.5*light_vals.get('ط',0.7))
                dist=np.sqrt((sx[i]-sx)**2+(sy[i]-sy)**2)
                close=(dist<2.0)&(np.arange(n_stars)!=i)
                sw[i]+=amr*0.015; sb[i]+=nahy*0.015
                sw[i]+=(target_S-sw[i])*0.02+np.random.uniform(-0.02,0.02)+wb
                sb[i]+=(target_S-sb[i])*0.02+np.random.uniform(-0.02,0.02)+bb
                if np.any(close):
                    sw[i]+=(np.mean(sw[close])-sw[i])*0.03*(0.5+0.5*shura)
                    sb[i]+=(np.mean(sb[close])-sb[i])*0.03*(0.5+0.5*shura)
                sw[i]*=(1-dark_vals.get('خ',0.2)*0.02); sb[i]*=(1-dark_vals.get('ذ',0.2)*0.02)
                sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)

            shock_p=0.005*(1-adl*0.8)*(1-light_vals.get('ر',0.7)*0.5)
            if random.random()<shock_p:
                aff=np.random.choice(n_stars,size=int(n_stars*0.3),replace=False)
                sw[aff]*=np.random.uniform(0.5,0.8); sb[aff]*=np.random.uniform(0.5,0.8)
            if random.random()<shock_p:
                aff=np.random.choice(n_stars,size=int(n_stars*0.2),replace=False)
                sw[aff]=np.minimum(1.0,sw[aff]*1.3); sb[aff]=np.minimum(1.0,sb[aff]*1.2)

            avgW=np.mean(sw); avgB=np.mean(sb)
            W+=(avgW-W)*0.04; B+=(avgB-B)*0.04
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
            S=calc_S(W,B,E,prayer,zakat,fasting,hajj,amr,nahy,adl,shura,light_vals,dark_vals)
            eb.append(S)
            eff_delay=int(delay_frames*(1+dark_vals.get('غ',0.2)*0.5))
            eb_list=list(eb)
            E_target=eb_list[-min(eff_delay,len(eb_list))] if len(eb_list)>=eff_delay else S
            E+=0.03*(E_target-E)
            zf=1+0.1*dark_vals.get('ظ',0.2)
            W=W-0.015*E*zf+0.03/(S+0.1)-0.007*(1-B)
            B=B-0.012*E*zf+0.006*(1-B)*W*(1-W)
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
            S=calc_S(W,B,E,prayer,zakat,fasting,hajj,amr,nahy,adl,shura,light_vals,dark_vals)
            pc+=1
            if pc%2==0: pS.append(S); pE.append(E); px.append(len(px))
            aW+=0.02+random.uniform(-0.025,0.025)*(1-W)**2
            aB+=0.02+random.uniform(-0.025,0.025)*(1-B)**2
            wx=cx+(7-2.5*W)*np.cos(aW); wy=cy+(7-2.5*W)*np.sin(aW)*0.7
            bx=cx+(5-1.5*B)*np.cos(aB); by=cy+(5-1.5*B)*np.sin(aB)*0.7
            ins=1-np.mean(sw*sb)
            sx+=np.random.uniform(-0.07,0.07,n_stars)*ins
            sy+=np.random.uniform(-0.07,0.07,n_stars)*ins
            sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)

            st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
            st.session_state.ph=ph; st.session_state.ca=ca
            st.session_state.aW=aW; st.session_state.aB=aB; st.session_state.aa=aa+0.12
            st.session_state.eb=eb
            st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
            st.session_state.pS=pS; st.session_state.pE=pE; st.session_state.px=px; st.session_state.pc=pc

            fig,ax=plt.subplots(figsize=(16,12),facecolor='#000010')
            ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
            for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),(2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy),r*(0.5+2.8*S),color=c,alpha=a,zorder=15))
            ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
            ax.text(cx,cy-2.5,f'S={S:.2f}',color='#FFD700',fontsize=10,ha='center')
            ax.add_patch(Circle((cx,cy),0.5+16*E,color='#00FFFF',alpha=0.25*(1-min(E,1))+0.04,zorder=7))
            ax.add_patch(Circle((cx,cy),8.5,color='#00FF88',alpha=0.15,fill=False,lw=2.5,zorder=2))
            for r in [10.0,11.5,13.0]: ax.add_patch(Circle((cx,cy),r,color='#FFD700',alpha=0.03,fill=False,lw=0.6,ls=':'))
            for i in range(6):
                an=-np.pi/4+i*(np.pi/2)/5
                ax.add_patch(Circle((cx+8.5*np.cos(an),cy+8.5*np.sin(an)),0.4,color='#FFF',alpha=0.3+0.5*avgW,zorder=8))
            for i in range(6):
                an=np.pi-np.pi/4+i*(np.pi/2)/5
                ax.add_patch(Circle((cx+8.5*np.cos(an),cy+8.5*np.sin(an)),0.4,color='#F33',alpha=0.25+0.35*avgB,zorder=8))
            ax.add_patch(Circle((wx,wy),0.2+0.6*W,color='#FFF',alpha=1,zorder=13))
            ax.add_patch(Circle((bx,by),0.2+0.6*B,color='#F33',alpha=0.8,zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            colors=[get_color(sw[i],sb[i]) for i in range(n_stars)]
            ax.scatter(sx,sy,s=35,c=colors,alpha=0.9,edgecolors='white',linewidths=0.4,zorder=5)
            aa+=0.12; er=0.5+0.4*S
            ax.add_patch(Circle((3.5,4.0),0.15+0.25*S,color='#4488FF',alpha=0.8,zorder=7))
            ax.add_patch(Circle((3.5+er*np.cos(aa),4.0+er*np.sin(aa)),0.04,color='white',alpha=0.95,zorder=8))
            ax.text(3.5,2.7,'ذرة',color='#4488FF',fontsize=6,ha='center')
            cx2,cy2=9.5,4.0
            ax.add_patch(RegularPolygon((cx2,cy2),numVertices=6,radius=0.35+0.25*S,orientation=np.pi/6,facecolor='#FFA500',alpha=0.7,zorder=7))
            ax.text(cx2,cy2-0.9,'جزيء',color='#FFA500',fontsize=6,ha='center')
            ax.add_patch(Circle((24.5,4.0),0.35+0.45*S,color='#00FF88',alpha=0.35,zorder=7,ec='#00FF88',lw=1))
            ax.add_patch(Circle((24.5,4.0),0.1+0.15*S,color='white',alpha=0.8,zorder=8))
            ax.text(24.5,2.7,'خلية',color='#00FF88',fontsize=6,ha='center')
            mx,my=0.5,16.5; bw=3.0; bh=0.4
            ax.add_patch(FancyBboxPatch((mx,my),bw,bh,boxstyle="round,pad=0.15",facecolor='#1a1a2e',alpha=0.8,zorder=20))
            if W>0: ax.add_patch(FancyBboxPatch((mx,my),W*bw/2,bh,boxstyle="round,pad=0.1",facecolor='#FFF',alpha=0.9,zorder=21))
            if B>0: ax.add_patch(FancyBboxPatch((mx+bw/2,my),B*bw/2,bh,boxstyle="round,pad=0.1",facecolor='#F33',alpha=0.9,zorder=21))
            if W+B>0: ax.plot(mx+(W/(W+B))*bw,my+bh/2,'v',color='#FFD700',markersize=12,markeredgecolor='white',zorder=22)
            ax.text(mx,my-0.6,f'W={W:.2f}',color='white',fontsize=8,ha='center')
            ax.text(mx+bw,my-0.6,f'B={B:.2f}',color='#F33',fontsize=8,ha='center')
            ax.text(mx+bw/2,my+bh+0.6,'الميزان',color='#FFD700',fontsize=9,ha='center',fontweight='bold')
            pSl=list(pS); pEl=list(pE); pxl=list(px)
            if pSl:
                pax=ax.inset_axes([0.50,0.02,0.46,0.10])
                pax.set_xlim(0,max(400,len(pxl))); pax.set_ylim(0,1.05)
                pax.set_title('S يقود E – الاستدراج',color='white',fontsize=7)
                pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
                pax.plot(pxl,pSl,color='#FFD700',lw=2,label='S'); pax.plot(pxl,pEl,color='#00FFFF',lw=1.5,label='E')
                pax.legend(facecolor='#000',edgecolor='white',labelcolor='white',fontsize=5)
            hfig=create_heatmap(sw,sb)
            hbuf=BytesIO(); hfig.savefig(hbuf,format='png',dpi=80,facecolor='#000010'); hbuf.seek(0)
            heat_ax=ax.inset_axes([0.02,0.02,0.20,0.18])
            heat_ax.imshow(plt.imread(hbuf)); heat_ax.axis('off'); plt.close(hfig)
            ax.text(14,1.2,f'{ph} | S={S:.2f} | E={E:.2f}',color='white',fontsize=12,ha='center',fontweight='bold')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig)
            buf=BytesIO(); fig.savefig(buf,format='png',dpi=100,facecolor='#000010'); buf.seek(0)
            st.session_state.latest_image=buf; plt.close(fig)
            progress_text.text(f"قيد التشغيل... | {ph} | S={S:.2f} | E={E:.2f}")
            warns=check_warnings(W,B,S,E,ph)
            if warns: warn_placeholder.warning(" | ".join(warns))
            else: warn_placeholder.success(T["balance_good"])
            time.sleep(0.08)
        except Exception as e:
            st.error(f"خطأ: {str(e)}")
            st.session_state.run=False
            break
    st.success(T["simulation_stopped"])

elif st.session_state.init and 'latest_image' in st.session_state:
    st.image(st.session_state.latest_image,caption="آخر حالة",use_column_width=True)

if 'latest_image' in st.session_state:
    st.sidebar.download_button(T["download"],st.session_state.latest_image,"mizan.png","image/png")

st.markdown("---")
with st.expander(T["help_title"]): st.markdown(T["help_content"])
st.markdown(f"<p style='text-align:center;color:#666;'>🧪 مختبر الميزان v5.0 – من الذرة إلى المجرة 🌌</p>", unsafe_allow_html=True)
