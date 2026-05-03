import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random, time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="الدين القيم", page_icon="⚖️", layout="wide")

# --------------------------- CSS ---------------------------
st.markdown("""
<style>
    .stApp { background: #0a0a1a; }
    .big-title { font-size: 1.8em; font-weight: 900; color: #FFD700; text-align: center; margin: 5px 0 0 0; }
    .sub-title { font-size: 0.85em; color: #CCCCCC; text-align: center; margin: 0 0 12px 0; }
    .stButton > button {
        border-radius: 12px; font-weight: bold; height: 3em; width: 100%;
        background: #1a1a2e; color: white; border: 2px solid #FFD700; font-size: 1em;
    }
    .metric-box { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 8px 2px; text-align: center; border: 1px solid rgba(255,215,0,0.2); }
    .metric-val { font-size: 1.3em; font-weight: bold; margin: 0; }
    .metric-lbl { font-size: 0.6em; color: #aaa; margin: 0; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# علامة تأكيد فريدة
st.success("✅ V20 FINAL – جميع الخيارات ظاهرة تحت هذا السطر مباشرة")

st.markdown('<p class="big-title">⚖️ الدِّينُ الْقَيِّم ⚖️</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">S = W × B | قانون التوازن الكوني</p>', unsafe_allow_html=True)

# أزرار التحكم
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("▶️ تشغيل", use_container_width=True): st.session_state.run = True; st.rerun()
with c2:
    if st.button("⏹️ إيقاف", use_container_width=True): st.session_state.run = False; st.rerun()
with c3:
    if st.button("🔄 إعادة ضبط", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.cache_data.clear(); st.cache_resource.clear()
        st.rerun()

# مؤشرات
if 'init' in st.session_state and st.session_state.init:
    m1,m2,m3,m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFD700;">{st.session_state.S:.2f}</p><p class="metric-lbl">⚖️ S</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFF;">{st.session_state.W:.2f}</p><p class="metric-lbl">🤍 W</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FF5252;">{st.session_state.B:.2f}</p><p class="metric-lbl">❤️ B</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#00FFFF;">{st.session_state.E:.2f}</p><p class="metric-lbl">💫 E</p></div>', unsafe_allow_html=True)

# =========== جميع الخيارات التي في الدائرة الحمراء ===========
st.markdown("---")
st.markdown("## 🎛️ جميع الخيارات (اسحب للأسفل إن لزم)")

# كل شريط تمرير في سطر خاص به، ظاهر مباشرة
prayer = st.slider("الصلاة 🟣", 0.0, 1.0, 0.8, 0.05, key="p")
zakat = st.slider("الزكاة 🟡", 0.0, 1.0, 0.6, 0.05, key="z")
fasting = st.slider("الصوم 🟠", 0.0, 1.0, 0.7, 0.05, key="f")
hajj = st.slider("الحج 🔵", 0.0, 1.0, 0.5, 0.05, key="h")

amr = st.slider("الأمر بالمعروف 📢", 0.0, 1.0, 0.5, 0.05, key="amr")
nahy = st.slider("النهي عن المنكر 🚫", 0.0, 1.0, 0.5, 0.05, key="nahy")
adl = st.slider("العدل ⚖️", 0.0, 1.0, 0.6, 0.05, key="adl")
shura = st.slider("الشورى 🤝", 0.0, 1.0, 0.5, 0.05, key="shura")

taawun_birr = st.slider("التعاون على البر", 0.0, 1.0, 0.5, 0.05, key="tb")
taawun_taqwa = st.slider("التعاون على التقوى", 0.0, 1.0, 0.5, 0.05, key="tt")
tawasi_haqq = st.slider("التواصي بالحق", 0.0, 1.0, 0.5, 0.05, key="th")
tawasi_sabr = st.slider("التواصي بالصبر", 0.0, 1.0, 0.5, 0.05, key="ts")

nahy_marouf_e = st.slider("النهي عن المعروف (إفساد)", 0.0, 1.0, 0.2, 0.05, key="nm")
amr_munkar_e = st.slider("الأمر بالمنكر (إفساد)", 0.0, 1.0, 0.2, 0.05, key="amr_e")
taawun_ithm = st.slider("التعاون على الإثم", 0.0, 1.0, 0.2, 0.05, key="ti")
taawun_udwan = st.slider("التعاون على العدوان", 0.0, 1.0, 0.2, 0.05, key="tu")
tawasi_batil = st.slider("التواصي بالباطل", 0.0, 1.0, 0.2, 0.05, key="tbat")
adam_sabr = st.slider("عدم الصبر", 0.0, 1.0, 0.2, 0.05, key="as")

riba = st.slider("الربا 💸", 0.0, 1.0, 0.2, 0.05, key="riba")
ghish = st.slider("الغش 🎭", 0.0, 1.0, 0.2, 0.05, key="ghish")
kadhib = st.slider("الكذب 🤥", 0.0, 1.0, 0.2, 0.05, key="kadhib")

cycle_speed = st.slider("سرعة الدورة", 0.02, 0.3, 0.12, 0.01, key="spd")
delay_frames = st.slider("تأخير التمكين", 5, 40, 22, 1, key="dly")
N_STARS = st.slider("عدد النجوم", 40, 150, 60, 10, key="nst")

# --------------------------- الدوال ---------------------------
def get_color(w, b):
    if w>=0.55 and b>=0.55: return '#FFD700'
    elif w>=0.55 and b<0.45: return '#FFFFFF'
    elif w<0.45 and b>=0.55: return '#FF3333'
    elif w<0.45 and b<0.45: return '#FFB6C1'
    return '#FFF8DC' if w>b else '#FFA07A'

def calc_S(W, B, E, p, z, f, h, amr, nahy, adl, shura, riba, ghish, kadhib):
    S_base = W * B
    pillars = (p+z+f+h)/4
    S_base *= (0.5 + 0.5*pillars)
    protection = (amr*W + nahy*B)/2
    S_base *= (0.8 + 0.4*protection)*(0.9 + 0.2*adl)*(0.85 + 0.3*shura)
    if E > S_base: S_base -= riba*(E - S_base)*0.3
    W_weak = W*(1 - kadhib*0.2)
    S_final = W_weak * B
    S_final *= (0.5 + 0.5*pillars)*(0.8 + 0.4*protection)*(0.9 + 0.2*adl)*(0.85 + 0.3*shura)
    return np.clip(S_final, 0.001, 1.0)

# --------------------------- التهيئة ---------------------------
if 'init' not in st.session_state: st.session_state.init = False
if 'run' not in st.session_state: st.session_state.run = False

if not st.session_state.init:
    np.random.seed(42); random.seed(42)
    n = N_STARS
    cx, cy = 5, 5
    st.session_state.cx=cx; st.session_state.cy=cy
    st.session_state.sx=np.random.uniform(0,10,n); st.session_state.sy=np.random.uniform(0,10,n)
    st.session_state.sw=np.random.uniform(0.1,1.0,n); st.session_state.sb=np.random.uniform(0.1,1.0,n)
    st.session_state.W=0.55; st.session_state.B=0.52; st.session_state.E=0.3; st.session_state.S=0.55*0.52
    st.session_state.ph="استقرار"; st.session_state.ca=0.0
    st.session_state.eb=deque([0.55*0.52]*30, maxlen=30)
    st.session_state.pS=deque(maxlen=150); st.session_state.pE=deque(maxlen=150); st.session_state.px=deque(maxlen=150)
    st.session_state.init=True

# تحذيرات
if st.session_state.init:
    S=st.session_state.S; E=st.session_state.E
    if E > S * 1.5: st.error("⚠️ فجوة استدراج خطيرة!")
    elif E > S * 1.2: st.warning("⚡ بداية استدراج")
    elif S < 0.2: st.error("🔴 خطر الانهيار")

plot_placeholder = st.empty()

# --------------------------- المحاكاة ---------------------------
if st.session_state.get("run", False):
    while st.session_state.get("run", False):
        try:
            W=st.session_state.W; B=st.session_state.B; E=st.session_state.E; S=st.session_state.S
            ph=st.session_state.ph; ca=st.session_state.ca
            sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
            sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
            eb=st.session_state.eb; pS=st.session_state.pS; pE=st.session_state.pE; px=st.session_state.px
            cx,cy=5,5

            ca+=0.1; sv=np.sin(ca); target_S=0.5+0.45*sv
            if sv>0.5: ph='استقرار تام'
            elif sv>0: ph='صعود'
            elif sv>-0.5: ph='انهيار'
            else: ph='قاع'
            if 0.3<sv<0.35: ph='>> استدراج <<'
            if -0.35<sv<-0.3: ph='>> تعافي <<'

            n=len(sw)
            for i in range(n):
                sw[i]+=prayer*0.01+hajj*0.005; sb[i]+=fasting*0.01+zakat*0.005
                sw[i]+=amr*0.008; sb[i]+=nahy*0.008
                dist=np.sqrt((sx[i]-sx)**2+(sy[i]-sy)**2)
                close=(dist<1.5)&(np.arange(n)!=i)
                if np.any(close):
                    sw[i]+=(np.mean(sw[close])-sw[i])*shura*0.03
                    sb[i]+=(np.mean(sb[close])-sb[i])*shura*0.03
                sw[i]+=(target_S-sw[i])*0.02+np.random.uniform(-0.02,0.02)
                sb[i]+=(target_S-sb[i])*0.02+np.random.uniform(-0.02,0.02)
                sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)

            if random.random()<0.005*(1-adl*0.8):
                aff=np.random.choice(n,size=int(n*0.2),replace=False)
                sw[aff]*=np.random.uniform(0.5,0.8); sb[aff]*=np.random.uniform(0.5,0.8)

            avgW=np.mean(sw); avgB=np.mean(sb)
            W+=(avgW-W)*0.04; B+=(avgB-B)*0.04
            W,B=np.clip(W,0.01,1.0),np.clip(B,0.01,1.0)

            S=calc_S(W,B,E,prayer,zakat,fasting,hajj,amr,nahy,adl,shura,riba,ghish,kadhib)
            eb.append(S)
            Et=list(eb)[-delay_frames] if len(eb)>delay_frames else S
            E+=0.03*(Et-E)
            W=W-0.01*E+0.02/(S+0.1); B=B-0.008*E+0.005*(1-B)*W*(1-W)
            W,B=np.clip(W,0.01,1.0),np.clip(B,0.01,1.0)
            S=calc_S(W,B,E,prayer,zakat,fasting,hajj,amr,nahy,adl,shura,riba,ghish,kadhib)

            pS.append(S); pE.append(E); px.append(len(px))
            ins=1-np.mean(sw*sb)
            sx+=np.random.uniform(-0.06,0.06,n)*ins; sy+=np.random.uniform(-0.06,0.06,n)*ins
            sx,sy=np.clip(sx,0,10),np.clip(sy,0,10)

            st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
            st.session_state.ph=ph; st.session_state.ca=ca
            st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
            st.session_state.pS=pS; st.session_state.pE=pE; st.session_state.px=px

            fig,ax=plt.subplots(figsize=(6,5),facecolor='#0a0a1a')
            ax.set_facecolor('#0a0a1a')
            colors=[get_color(sw[i],sb[i]) for i in range(n)]
            ax.scatter(sx,sy,s=45,c=colors,alpha=0.9,edgecolors='white',linewidth=0.3)
            ax.add_patch(Circle((cx,cy),2*S,color='#FFD700',alpha=0.2))
            ax.add_patch(Circle((cx,cy),1.5*E,color='#00FFFF',alpha=0.12))
            ax.text(cx,cy,'⚖️',fontsize=22,ha='center',va='center',color='#FFD700')
            ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
            ax.set_title(f'{ph}  |  S={S:.2f}  |  E={E:.2f}',color='white',fontsize=12)
            plt.tight_layout(pad=0)
            plot_placeholder.pyplot(fig); plt.close(fig)
            time.sleep(max(0.08,cycle_speed))
        except Exception as e:
            st.error(str(e)); st.session_state.run=False; break
    st.success("⏸️ تم إيقاف المحاكاة")
else:
    if st.session_state.init:
        fig,ax=plt.subplots(figsize=(3,2),facecolor='#0a0a1a')
        ax.set_facecolor('#0a0a1a')
        colors=[get_color(st.session_state.sw[i],st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
        ax.scatter(st.session_state.sx,st.session_state.sy,s=20,c=colors,alpha=0.9,edgecolors='white',linewidth=0.2)
        ax.add_patch(Circle((5,5),2*st.session_state.S,color='#FFD700',alpha=0.2))
        ax.text(5,5,'⚖️',fontsize=14,ha='center',va='center',color='#FFD700')
        ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
        ax.set_title('اضغط ▶️ تشغيل',color='white',fontsize=8)
        plt.tight_layout(pad=0)
        plot_placeholder.pyplot(fig); plt.close(fig)

st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;'>© 2026 علي عادل العاطفي | V20</p>", unsafe_allow_html=True)
