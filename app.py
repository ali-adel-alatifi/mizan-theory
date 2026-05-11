import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="مختبر الميزان", page_icon="⚖️", layout="wide")

if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
T = lambda ar, en: ar if L == "ar" else en

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri+Quran&display=swap');
.stApp { background: linear-gradient(180deg, #0a0f1e 0%, #0d1528 30%, #0f1a2e 100%); }
h1, h2, h3 { font-family: 'Cairo', sans-serif; color: #FFD700; }
p, label, div { font-family: 'Cairo', sans-serif; color: #E0E0E0; }
.golden-title { font-size: 3.5em; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; }
.verse-text { text-align: center; color: #FFD700; font-family: 'Amiri Quran', 'Cairo', serif; font-size: 1.3em; margin: 15px 0; line-height: 2; }
.stButton > button { background: linear-gradient(135deg, rgba(20,30,60,0.9), rgba(30,40,70,0.9)); border: 2px solid #FFD700; color: #FFD700; border-radius: 12px; padding: 12px 25px; font-weight: bold; font-size: 1em; width: 100%; transition: all 0.3s ease; font-family: 'Cairo', sans-serif; }
.stButton > button:hover { background: #FFD700; color: #0a0f1e; box-shadow: 0 0 25px rgba(255,215,0,0.5); transform: scale(1.02); }
.stTabs [data-baseweb="tab-list"] { gap: 5px; background: rgba(13,21,40,0.8); border-radius: 15px; padding: 5px; }
.stTabs [data-baseweb="tab"] { background: transparent; border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; color: #CCC; font-family: 'Cairo', sans-serif; padding: 10px 18px; }
.stTabs [aria-selected="true"] { background: rgba(255,215,0,0.15) !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    return '#888888'

def classify(W, B):
    if W >= 0.5 and B >= 0.5: return ("مؤمن", '#FFD700')
    elif W < 0.5 and B >= 0.5: return ("كافر", '#FF5252')
    elif W < 0.5 and B < 0.5: return ("منافق", '#FFB6C1')
    return ("مشرك", '#FFA500')

def curvature(W, B):
    if len(W) < 3: return 0
    dW = np.gradient(list(W)); dB = np.gradient(list(B))
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return num / denom

def calc_S(W, B, E, q=1.0):
    return np.clip(W * B * (1 + q * 0.5), 0.001, 1.0)

# ═══════════════════════════════════════
# الجلسة
# ═══════════════════════════════════════
if 'init' not in st.session_state:
    np.random.seed(42); random.seed(42)
    cx, cy = 14, 10.0; N = 200
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-13, cx+13, N)
    st.session_state.sy = np.random.uniform(cy-9, cy+9, N)
    st.session_state.sw = np.random.uniform(0.1, 1, N)
    st.session_state.sb = np.random.uniform(0.1, 1, N)
    st.session_state.N = N
    st.session_state.W = 0.55; st.session_state.B = 0.52; st.session_state.E = 0.3
    st.session_state.S = 0.55 * 0.52
    st.session_state.pW = deque([0.55], maxlen=50)
    st.session_state.pB = deque([0.52], maxlen=50)
    st.session_state.hS = deque(maxlen=300)
    st.session_state.hE = deque(maxlen=300)
    st.session_state.hx = deque(maxlen=300)
    st.session_state.eb = deque([0.55*0.52]*30, maxlen=30)
    st.session_state.phase = "توازن"; st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.good = 10.0; st.session_state.bad = 5.0
    st.session_state.frame = 0
    st.session_state.path_W = [0.5]; st.session_state.path_B = [0.5]
    st.session_state.kappa_vals = [0.0]
    st.session_state.run = False
    st.session_state.init = True

# ═══════════════════════════════════════
# العنوان
# ═══════════════════════════════════════
col_icon1, col_title, col_icon2 = st.columns([1, 6, 1])
with col_icon1: st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 class='golden-title'>مختبر الميزان</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#CCC;font-size:1.2em;'>{T('القانون الواحد من الذرة إلى الحضارة', 'The One Law from Atom to Civilization')}</p>", unsafe_allow_html=True)
with col_icon2: st.markdown("<p style='text-align:center;font-size:4em;'>⚖️</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='verse-text'>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    <br><span style='font-size:0.8em;'>S = W × B | ق = ١٠٠ = الحق = الميزان</span>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# أزرار التحكم + اللغة
# ═══════════════════════════════════════
c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
with c1:
    if st.button("▶️ تشغيل", use_container_width=True): st.session_state.run = True
with c2:
    if st.button("⏹️ إيقاف", use_container_width=True): st.session_state.run = False
with c3:
    if st.button("English" if L == "ar" else "العربية", use_container_width=True):
        st.session_state.lang = "en" if L == "ar" else "ar"
        st.rerun()
with c4:
    lag = st.select_slider(T("فجوة الاستدراج", "Istidraj Gap"), options=[5, 10, 15, 22, 30, 40, 50], value=22)
with c5:
    if st.button("🔄 إعادة", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

st.markdown("---")

# ═══════════════════════════════════════
# التبويبات
# ═══════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    T("🌌 المشهد الكوني", "🌌 Cosmic Scene"),
    T("🧍 ميزانك الشخصي", "🧍 Personal Balance"),
    T("👥 المجتمع", "👥 Society"),
    T("🏛️ الدولة", "🏛️ State"),
    T("🌍 الأمة", "🌍 Nation"),
    T("📐 هندسة الصراط", "📐 Path Geometry"),
])

# ═══════════════════════════════════════
# تبويب ١: الكون
# ═══════════════════════════════════════
with tab1:
    placeholder = st.empty()
    with st.expander(T("⚙️ إعدادات المشهد", "⚙️ Settings"), expanded=False):
        W0 = st.slider(T("W (الولاء لله)", "W (Loyalty to Allah)"), 0.0, 1.0, 0.55, 0.01)
        B0 = st.slider(T("B (البراءة من الطاغوت)", "B (Disavowal of Taghut)"), 0.0, 1.0, 0.52, 0.01)
        q_val = st.slider(T("⚖️ ق (الميزان)", "⚖️ Q (Balance)"), 0.0, 1.0, 1.0, 0.01)
    
    if st.session_state.get("run", False):
        st.session_state.W = W0; st.session_state.B = B0
        while st.session_state.run:
            W=st.session_state.W; B=st.session_state.B; E=st.session_state.E
            S=st.session_state.S; phase=st.session_state.phase; ca=st.session_state.ca
            aW=st.session_state.aW; aB=st.session_state.aB
            sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
            sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
            cx=st.session_state.cx; cy=st.session_state.cy; eb=st.session_state.eb
            hS=st.session_state.hS; hE=st.session_state.hE; hx=st.session_state.hx
            good=st.session_state.good; bad=st.session_state.bad
            pW=st.session_state.pW; pB=st.session_state.pB; frame=st.session_state.frame
            N=st.session_state.N

            ca+=0.008; sv=np.sin(ca)
            if sv>0.5: phase=T('ذروة','Peak')
            elif sv>0: phase=T('صعود','Rising')
            elif sv>-0.5: phase=T('انهيار','Collapse')
            else: phase=T('قاع','Bottom')
            if 0.3<sv<0.35: phase=T('>> استدراج <<','>> Istidraj <<')
            target=0.5+0.45*sv

            for i in range(N):
                dist=np.sqrt((sx[i]-sx)**2+(sy[i]-sy)**2)
                nbr=np.where((dist<2.0)&(np.arange(N)!=i))[0]
                sw[i]+=(target-sw[i])*0.02+np.random.uniform(-0.02,0.02)
                sb[i]+=(target-sb[i])*0.02+np.random.uniform(-0.02,0.02)
                if len(nbr)>0:
                    sw[i]+=(np.mean(sw[nbr])-sw[i])*0.03; sb[i]+=(np.mean(sb[nbr])-sb[i])*0.03
                sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)
            if random.random()<0.005:
                aff=np.random.choice(N,size=int(N*0.2),replace=False)
                sw[aff]*=random.uniform(0.5,0.8); sb[aff]*=random.uniform(0.5,0.8)

            W+=(np.mean(sw)-W)*0.04; B+=(np.mean(sb)-B)*0.04
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
            S=calc_S(W,B,E,q_val)
            eb.append(S)
            past=list(eb)[-lag] if len(eb)>=lag else S
            E+=0.03*(past-E)
            W=W-0.015*E+0.03/(S+0.1)-0.007*(1-B)
            B=B-0.012*E+0.006*(1-B)*W*(1-W)
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
            S=calc_S(W,B,E,q_val)
            pW.append(W); pB.append(B)
            frame+=1
            if frame%2==0: hS.append(S); hE.append(E); hx.append(len(hx))
            aW+=0.02+random.uniform(-0.02,0.02)*(1-W)**2
            aB+=0.02+random.uniform(-0.02,0.02)*(1-B)**2
            wx=cx+(7-2.5*W)*np.cos(aW); wy=cy+(7-2.5*W)*np.sin(aW)*0.7
            bx=cx+(5-1.5*B)*np.cos(aB); by=cy+(5-1.5*B)*np.sin(aB)*0.7
            instability=1-np.mean(sw*sb)
            sx+=np.random.uniform(-0.07,0.07,N)*instability; sy+=np.random.uniform(-0.07,0.07,N)*instability
            sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)
            good+=W*0.1; bad+=(1-B)*0.1

            st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
            st.session_state.phase=phase; st.session_state.ca=ca
            st.session_state.aW=aW; st.session_state.aB=aB; st.session_state.eb=eb
            st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
            st.session_state.pW=pW; st.session_state.pB=pB
            st.session_state.hS=hS; st.session_state.hE=hE; st.session_state.hx=hx; st.session_state.frame=frame
            st.session_state.good=good; st.session_state.bad=bad

            fig,ax=plt.subplots(figsize=(16,10),facecolor='#0a0f1e')
            ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
            for r,a,c in [(0.5,0.98,'#FFF'),(1,0.6,'#FFD700'),(1.8,0.3,'#FFD700'),(2.8,0.1,'#FFA500'),(4,0.03,'#FF4500')]:
                ax.add_patch(Circle((cx,cy),r*(0.5+3*S),color=c,alpha=a,zorder=15))
            ax.text(cx,cy,'S',color='#000',fontsize=14,ha='center',va='center',fontweight='bold')
            ax.add_patch(Circle((cx,cy),0.5+16*E,color='#0FF',alpha=0.15,zorder=7))
            ax.add_patch(Circle((wx,wy),0.2+0.6*W,color='#FFF',alpha=1,zorder=13))
            ax.add_patch(Circle((bx,by),0.2+0.6*B,color='#F33',alpha=0.8,zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            colors=[star_color(sw[i],sb[i]) for i in range(N)]
            ax.scatter(sx,sy,s=20,c=colors,alpha=0.9,edgecolors='white',linewidths=0.2,zorder=5)
            
            # الميزان الأخروي
            akh_x, akh_y, ms = 26.5, 18, 1.5
            ax.plot([akh_x, akh_x], [akh_y-3, akh_y+1.5], color='#FFD700', lw=1, alpha=0.4)
            ly = akh_y-1.5 + ms*min(good/50, 1.5)
            ry = akh_y-1.5 - ms*min(bad/50, 1.5)
            ax.add_patch(Circle((akh_x-1, ly), 0.6, color='#FFD700', alpha=0.3, zorder=20))
            ax.text(akh_x-1, ly-1, T('حسنات','Good'), color='#FFD700', fontsize=6, ha='center')
            ax.add_patch(Circle((akh_x+1, ry), 0.6, color='#FF4444', alpha=0.3, zorder=20))
            ax.text(akh_x+1, ry-1, T('سيئات','Bad'), color='#FF4444', fontsize=6, ha='center')
            diff = (bad-good)/50*ms
            ax.plot([akh_x-1, akh_x+1], [akh_y-diff, akh_y+diff], color='#FFD700', lw=1.5, alpha=0.6)

            pax=ax.inset_axes([0.5,0.02,0.46,0.12])
            pax.set_xlim(0,350); pax.set_ylim(0,1.05)
            pax.set_title(T("S يَقُود E — الِاسْتِدْرَاج","S leads E — Istidraj"),color='white',fontsize=7)
            pax.tick_params(colors='white',labelsize=5); pax.grid(True,alpha=0.12)
            if hS: pax.plot(list(hx),list(hS),color='#FFD700',lw=2); pax.plot(list(hx),list(hE),color='#0FF',lw=1.5)
            ax.text(14,1.2,f'{phase} | S={S:.2f} | E={E:.2f} | κ={curvature(pW,pB):.3f}',color='#CCC',fontsize=9,ha='center')
            plt.tight_layout(pad=0); placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.06)
    else:
        st.info(T("اضغط ▶️ تشغيل", "Press ▶️ Run"))
    
    # زر التحميل
    if not st.session_state.get("run", False) and len(st.session_state.hS) > 0:
        csv_data = "Time,S,E\n" + "\n".join([f"{i},{s:.4f},{e:.4f}" for i,(s,e) in enumerate(zip(st.session_state.hS, st.session_state.hE))])
        st.download_button(T("📥 تحميل بيانات المحاكاة", "📥 Download Simulation Data"), data=csv_data, file_name="mizan_cosmic.csv", mime="text/csv")

# ═══════════════════════════════════════
# تبويب ٢: ميزانك الشخصي
# ═══════════════════════════════════════
with tab2:
    st.header(T("🧍 ميزانك الشخصي", "🧍 Your Personal Balance"))
    st.markdown(T("أجب عن ١٢ سؤالاً بصدق لتكتشف موقعك في فضاء الولاء والبراءة.", "Answer 12 questions honestly."))
    
    compass = {}
    qs = {
        "W": [
            (T("حياتي كلها لله، لا أبتغي بها إلا وجهه", "My whole life is for Allah alone"), 3),
            (T("أقيم الصلاة بخشوع، أستشعر الوقوف بين يدي الله", "I pray with devotion"), 3),
            (T("أحب الله ورسوله أكثر من كل شيء", "I love Allah & Messenger most"), 3),
            (T("أتوكل على الله مع الأخذ بالأسباب", "I rely on Allah with means"), 3),
            (T("أشكر الله في الرخاء وأصبر في البلاء", "I thank and am patient"), 3),
            (T("أحمل هم الإسلام والمسلمين، وأسعى لنصرتهم", "I carry concerns of Islam"), 3),
        ],
        "B": [
            (T("آمر بالمعروف بالحكمة والموعظة الحسنة", "I enjoin good wisely"), 3),
            (T("أنكر المنكر بيدي ولساني وقلبي حسب استطاعتي", "I forbid evil with hand, tongue, and heart"), 3),
            (T("أتبرأ من الشرك وأهله، وأعلن براءتي منهم", "I disavow polytheism"), 3),
            (T("أجاهد نفسي على ترك الكذب والغيبة والظلم", "I struggle against sins"), 3),
            (T("أرفض الظلم بكل صوره، ولا أرضاه لأحد", "I reject all injustice"), 3),
            (T("أحب في الله وأبغض في الله، أوالي أولياءه وأعادي أعداءه", "I love & hate for Allah's sake"), 3),
        ]
    }
    
    ca, cb = st.columns(2)
    with ca:
        st.subheader(T("🤍 الولاء (W)", "🤍 Loyalty (W)"))
        for i, (q, v) in enumerate(qs["W"]):
            ans = st.radio(q, [T("نعم (+3)","Yes (+3)"), T("أحياناً (+1)","Sometimes (+1)"), T("لا (0)","No (0)"), T("العكس (-1)","Opposite (-1)")], key=f"w_{i}")
            if ans: compass[f"W{i}"] = 3 if T("نعم","Yes") in ans else 1 if T("أحياناً","Sometimes") in ans else 0 if "لا" in ans else -1
    with cb:
        st.subheader(T("❤️ البراءة (B)", "❤️ Disavowal (B)"))
        for i, (q, v) in enumerate(qs["B"]):
            ans = st.radio(q, [T("نعم (+3)","Yes (+3)"), T("أحياناً (+1)","Sometimes (+1)"), T("لا (0)","No (0)"), T("العكس (-1)","Opposite (-1)")], key=f"b_{i}")
            if ans: compass[f"B{i}"] = 3 if T("نعم","Yes") in ans else 1 if T("أحياناً","Sometimes") in ans else 0 if "لا" in ans else -1
    
    if len(compass) == 12:
        Ws = np.clip(sum(compass[f"W{i}"] for i in range(6)) / 18.0, -1, 1)
        Bs = np.clip(sum(compass[f"B{i}"] for i in range(6)) / 18.0, -1, 1)
        Wn = (Ws + 1) / 2; Bn = (Bs + 1) / 2
        name, color = classify(Wn, Bn)
        
        st.markdown(f"""
        <div style='background:rgba(20,30,60,0.8);border-radius:15px;padding:20px;border:2px solid {color};text-align:center;margin:15px 0;'>
            <h2 style='color:{color};'>{name}</h2>
            <p style='color:#CCC;'>W = {Ws:.2f} | B = {Bs:.2f}</p>
            <p style='color:#FFD700;font-size:1.3em;'>⚖️ S = W × B = {Wn*Bn:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5); ax.axvline(0, color='grey', lw=0.5)
        ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.15))
        ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF5252', alpha=0.15))
        ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.15))
        ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA500', alpha=0.15))
        ax.text(0.5, 0.5, T("مؤمن","Believer"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, 0.5, T("كافر","Disbeliever"), ha='center', color='white', alpha=0.6)
        ax.text(-0.5, -0.5, T("منافق","Hypocrite"), ha='center', color='white', alpha=0.6)
        ax.text(0.5, -0.5, T("مشرك","Polytheist"), ha='center', color='white', alpha=0.6)
        ax.scatter(Bs, Ws, s=200, c='#00FFFF', edgecolors='white', linewidth=3, zorder=10)
        ax.set_xlabel(T("B (البراءة)","B (Disavowal)"), color='white')
        ax.set_ylabel(T("W (الولاء)","W (Loyalty)"), color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)

# ═══════════════════════════════════════
# تبويب ٣: المجتمع
# ═══════════════════════════════════════
with tab3:
    st.header(T("👥 مختبر المجتمع", "👥 Society Lab"))
    pop = st.slider(T("عدد الأفراد", "Population"), 50, 300, 150, 25, key="pop")
    amr = st.slider(T("الأمر بالمعروف", "Enjoining Good"), 0.0, 1.0, 0.5, 0.05, key="amr")
    nahy = st.slider(T("النهي عن المنكر", "Forbidding Evil"), 0.0, 1.0, 0.5, 0.05, key="nahy")
    
    if st.button(T("شغّل محاكاة المجتمع", "Run Society Simulation"), use_container_width=True):
        pW = np.random.uniform(0.2, 0.9, pop); pB = np.random.uniform(0.2, 0.9, pop)
        px = np.random.uniform(0, 30, pop); py = np.random.uniform(0, 30, pop)
        for _ in range(80):
            nW = pW.copy(); nB = pB.copy()
            for i in range(pop):
                d = np.sqrt((px - px[i])**2 + (py - py[i])**2)
                nbr = np.where((d < 2.5) & (np.arange(pop) != i))[0]
                if len(nbr) > 0:
                    nW[i] += 0.03 * (np.mean(pW[nbr]) - pW[i])
                    nB[i] += 0.03 * (np.mean(pB[nbr]) - pB[i])
                nW[i] += 0.02 * amr * (1 - pW[i]) + 0.01 * (np.random.rand() - 0.5)
                nB[i] += 0.02 * nahy * (1 - pB[i]) + 0.01 * (np.random.rand() - 0.5)
                nW[i] = np.clip(nW[i], 0.01, 1.0); nB[i] = np.clip(nB[i], 0.01, 1.0)
            pW = nW; pB = nB
            px += np.random.randint(-1, 2, pop); py += np.random.randint(-1, 2, pop)
            px = np.clip(px, 0, 29); py = np.clip(py, 0, 29)
        
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        colors = [star_color(pW[i], pB[i]) for i in range(pop)]
        ax.scatter(px, py, c=colors, s=30, alpha=0.8, edgecolors='white', linewidths=0.2)
        ax.set_xlim(0, 30); ax.set_ylim(0, 30)
        ax.set_title(T("خريطة المجتمع", "Society Map"), color='white', fontsize=13)
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white')
        st.pyplot(fig)
        
        bel = np.sum((pW >= 0.5) & (pB >= 0.5))
        c1, c2 = st.columns(2)
        c1.metric(T("🟡 المؤمنون", "🟡 Believers"), f"{bel} ({bel/pop*100:.0f}%)")
        c2.metric("⚖️ S", f"{np.mean(pW * pB):.3f}")

# ═══════════════════════════════════════
# تبويب ٤: الدولة
# ═══════════════════════════════════════
with tab4:
    st.header(T("🏛️ مختبر الدولة", "🏛️ State Lab"))
    c1, c2, c3 = st.columns(3)
    with c1: j = st.slider(T("العدل", "Justice"), 0.0, 1.0, 0.6, 0.05, key="j")
    with c2: s = st.slider(T("الشورى", "Consultation"), 0.0, 1.0, 0.5, 0.05, key="s")
    with c3: sh = st.slider(T("تحكيم شرع الله", "Applying Sharia"), 0.0, 1.0, 0.5, 0.05, key="sh")
    
    if st.button(T("شغّل محاكاة الدولة", "Run State Simulation"), use_container_width=True):
        Y = 120; Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
        Wh[0] = np.clip(sh*j, 0.01, 1.0); Bh[0] = np.clip(sh*(1-0.2), 0.01, 1.0)
        Sh[0] = Wh[0]*Bh[0]; Eh[0] = 0.1
        for t in range(1, Y):
            Wh[t] = np.clip(Wh[t-1] + j*0.015 + sh*0.02 + s*0.01 - 0.01*Eh[t-1], 0.01, 1.0)
            Bh[t] = np.clip(Bh[t-1] + sh*0.025 + j*0.01 - 0.008*Eh[t-1], 0.01, 1.0)
            Sh[t] = Wh[t]*Bh[t]
            past = Sh[max(0, t-15)]; Eh[t] = np.clip(Eh[t-1] + 0.04*(past-Eh[t-1]), 0.01, 1.0)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(Sh, 'g-', lw=2, label='S'); ax.plot(Eh, 'b--', lw=2, label='E')
        ax.plot(Wh, color='gold', lw=1, alpha=0.6, label='W'); ax.plot(Bh, '#FF5252', lw=1, alpha=0.6, label='B')
        ax.set_title(T("دورة الدولة", "State Cycle"), color='white', fontsize=13)
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
        st.pyplot(fig)
        st.metric(T("S النهائي", "Final S"), f"{Sh[-1]:.3f}")

# ═══════════════════════════════════════
# تبويب ٥: الأمة
# ═══════════════════════════════════════
with tab5:
    st.header(T("🌍 مختبر الأمة", "🌍 Nation Lab"))
    c1, c2 = st.columns(2)
    with c1: np_ = st.slider(T("الصلاة (تقوي W)", "Prayer (W)"), 0.0, 1.0, 0.7, 0.01, key="np")
    with c2: nd = st.slider(T("البراءة من الطاغوت (تقوي B)", "Disavowal of Taghut (B)"), 0.0, 1.0, 0.7, 0.01, key="nd")
    
    if st.button(T("شغّل محاكاة الأمة", "Run Nation Simulation"), use_container_width=True):
        Y = 250; Wh = np.zeros(Y); Bh = np.zeros(Y); Sh = np.zeros(Y); Eh = np.zeros(Y)
        Wh[0] = np_*0.8; Bh[0] = nd*0.8; Sh[0] = Wh[0]*Bh[0]; Eh[0] = 0.1
        for t in range(1, Y):
            Wh[t] = np.clip(Wh[t-1] - 0.01*Eh[t-1] + 0.01*np_, 0.01, 1.0)
            Bh[t] = np.clip(Bh[t-1] - 0.008*Eh[t-1] + 0.01*nd, 0.01, 1.0)
            Sh[t] = Wh[t]*Bh[t]
            past = Sh[max(0, t-lag)]; Eh[t] = np.clip(Eh[t-1] + 0.03*(past-Eh[t-1]), 0.01, 1.0)
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0f1e')
        ax.set_facecolor('#0a0f1e')
        ax.plot(Sh, 'g-', lw=2, label='S'); ax.plot(Eh, 'b--', lw=2, label='E')
        ax.set_title(T("دورة الأمة", "Nation Cycle"), color='white', fontsize=13)
        ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2); ax.tick_params(colors='white'); ax.set_ylim(0, 1.05)
        st.pyplot(fig)
        
        idxS = np.argmax(Sh); idxE = np.argmax(Eh)
        st.metric(T("فجوة الاستدراج", "Istidraj Gap"), f"{max(0, idxE-idxS)} {T('عام','yrs')}")

# ═══════════════════════════════════════
# تبويب ٦: هندسة الصراط
# ═══════════════════════════════════════
with tab6:
    st.header(T("📐 هندسة الصراط", "📐 Path Geometry"))
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(T("▶️ خطوة", "▶️ Step"), use_container_width=True):
            Wc=st.session_state.path_W[-1]; Bc=st.session_state.path_B[-1]
            nW=np.clip(Wc+(1-Wc)*0.15+random.uniform(-0.03,0.03),0.01,1.0)
            nB=np.clip(Bc+(1-Bc)*0.15+random.uniform(-0.03,0.03),0.01,1.0)
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.kappa_vals.append(curvature(st.session_state.path_W,st.session_state.path_B))
            st.rerun()
    with c2:
        sin_str=st.slider(T("شدة المعصية","Sin Strength"),0.01,0.2,0.05,0.01)
        if st.button(T("⚠️ معصية","⚠️ Sin"),use_container_width=True):
            Wc=st.session_state.path_W[-1]; Bc=st.session_state.path_B[-1]
            nW=np.clip(Wc-sin_str*(Wc-0.1)+random.uniform(-0.05,0.05),0.01,1.0)
            nB=np.clip(Bc-sin_str*(Bc-0.1)+random.uniform(-0.05,0.05),0.01,1.0)
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.kappa_vals.append(curvature(st.session_state.path_W,st.session_state.path_B))
            st.rerun()
    with c3:
        if st.button(T("🕌 توبة","🕌 Repent"),use_container_width=True):
            Wc=st.session_state.path_W[-1]; Bc=st.session_state.path_B[-1]
            nW=np.clip(Wc+(1-Wc)*0.8,0.01,1.0); nB=np.clip(Bc+(1-Bc)*0.8,0.01,1.0)
            st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
            st.session_state.kappa_vals.append(0.0); st.rerun()
    
    if st.button(T("🔄 إعادة","🔄 Reset"),use_container_width=True):
        st.session_state.path_W=[0.5]; st.session_state.path_B=[0.5]; st.session_state.kappa_vals=[0.0]; st.rerun()
    
    fig,axes=plt.subplots(1,2,figsize=(14,6),facecolor='#0a0f1e')
    ax1=axes[0]; ax1.set_facecolor('#0a0f1e'); ax1.set_xlim(0,1); ax1.set_ylim(0,1)
    ax1.set_xlabel("B",color='white'); ax1.set_ylabel("W",color='white')
    ax1.plot([0.5,1],[0.5,1],'--',color='#FFD700',lw=2.5,alpha=0.7,label=T("الصراط","Straight Path"))
    ax1.scatter([1],[1],s=120,c='#FFD700',edgecolors='white',linewidth=2,zorder=10,label=T("الكمال","Perfection"))
    pW=st.session_state.path_W; pB=st.session_state.path_B
    if len(pW)>1:
        for i in range(1,len(pW)):
            kv=st.session_state.kappa_vals[i] if i<len(st.session_state.kappa_vals) else 0
            cl='#00FFFF' if kv<0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1],pW[i-1:i+1],color=cl,lw=2)
        ax1.scatter([pB[0]],[pW[0]],s=80,c='white',edgecolors='cyan',linewidth=2,zorder=10,label=T("البداية","Start"))
        ax1.scatter([pB[-1]],[pW[-1]],s=120,c='#00FFFF',edgecolors='white',linewidth=3,zorder=10,label=T("الآن","Now"))
    ax1.legend(facecolor='#0a0f1e',edgecolor='white',labelcolor='white',fontsize=8,loc='lower right')
    ax1.grid(True,alpha=0.2); ax1.tick_params(colors='white')
    
    ax2=axes[1]; ax2.set_facecolor('#0a0f1e')
    ax2.plot(st.session_state.kappa_vals,color='#FFD700',lw=2,marker='o',markersize=3)
    ax2.axhline(y=0.05,color='#FF4444',ls='--',alpha=0.6,label=T("حد الخطر","Danger"))
    ax2.axhline(y=0.0,color='#00FF88',ls='--',alpha=0.4,label=T("الصراط","Straight"))
    ax2.set_title(T("منحنى الانحناء","Curvature"),color='white',fontsize=12)
    ax2.set_xlabel(T("الخطوات","Steps"),color='white'); ax2.set_ylabel("κ",color='white')
    ax2.legend(facecolor='#0a0f1e',edgecolor='white',labelcolor='white',fontsize=8)
    ax2.grid(True,alpha=0.2); ax2.tick_params(colors='white')
    ax2.set_ylim(-0.01,max(0.2,max(st.session_state.kappa_vals)*1.2 if st.session_state.kappa_vals else 0.1))
    plt.tight_layout(); st.pyplot(fig)
    
    c1,c2,c3,c4=st.columns(4)
    c1.metric("W",f"{pW[-1]:.3f}"); c2.metric("B",f"{pB[-1]:.3f}")
    c3.metric("κ",f"{st.session_state.kappa_vals[-1]:.4f}")
    c4.metric(T("الصراط؟","On Path?"), T("✅ نعم","✅ YES") if st.session_state.kappa_vals[-1]<0.03 else T("⚠️ لا","⚠️ NO"))

# ═══════════════════════════════════════
# التذييل
# ═══════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#888;font-size:0.9em;line-height:1.8;">
    <p style="color:#FFD700;font-size:1.3em;">⚖️ مختبر الميزان</p>
    <p>S = W × B | ق = ١٠٠ = الحق = الميزان</p>
    <p>© 2026 علي عادل العاطفي | Ali Adel Alatifi</p>
</div>
""", unsafe_allow_html=True)
