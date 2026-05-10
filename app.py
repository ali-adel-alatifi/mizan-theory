import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="مختبر الميزان الحي", page_icon="⚖️", layout="wide")
if "lang" not in st.session_state: st.session_state.lang = "ar"
L = st.session_state.lang
def T(ar, en): return ar if L == "ar" else en

def star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    else: return '#888888'

def quadrant(W, B):
    if W >= 0.5 and B >= 0.5: return ("believer", '#FFD700')
    elif W < 0.5 and B >= 0.5: return ("disbeliever", '#FF5252')
    elif W < 0.5 and B < 0.5: return ("hypocrite", '#FFB6C1')
    else: return ("polytheist", '#FFA500')

def curvature(Wh, Bh):
    if len(Wh) < 3: return 0.0
    dW = np.gradient(Wh); dB = np.gradient(Bh)
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    n = abs(dW[-1]*ddB[-1] - dB[-1]*ddW[-1])
    d = (dW[-1]**2 + dB[-1]**2 + 1e-10)**1.5
    return n / d

def S_calc(W, B, q=1.0):
    return np.clip(W * B * (1 + q * 0.5), 0.001, 1.0)

# ═══════════════════════════════════════════════
# الشريط الجانبي
# ═══════════════════════════════════════════════
with st.sidebar:
    lang_choice = st.radio("🌐 اللغة / Language", ["العربية", "English"], index=0 if L=="ar" else 1)
    if (lang_choice=="English" and L=="ar") or (lang_choice=="العربية" and L=="en"):
        st.session_state.lang = "en" if lang_choice=="English" else "ar"
        st.rerun()
    st.markdown("---")
    st.subheader(T("⚙️ إعدادات المحاكاة", "⚙️ Simulation Settings"))
    W0 = st.slider(T("W الابتدائي", "Initial W"), 0.0, 1.0, 0.55, 0.01)
    B0 = st.slider(T("B الابتدائي", "Initial B"), 0.0, 1.0, 0.52, 0.01)
    lag = st.slider(T("فجوة الاستدراج", "Istidraj Gap"), 5, 50, 22, 1)
    N = st.slider(T("عدد النجوم", "Stars"), 100, 600, 300, 50)
    Q = st.slider(T("⚖️ ق (الميزان)", "⚖️ Q (Balance)"), 0.0, 1.0, 1.0, 0.01)
    st.markdown("---")
    c1, c2 = st.columns(2)
    if c1.button(T("▶️ تشغيل", "▶️ Run"), use_container_width=True): st.session_state.run = True
    if c2.button(T("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True): st.session_state.run = False

# ═══════════════════════════════════════════════
# العنوان
# ═══════════════════════════════════════════════
st.markdown(f"""
<div style="text-align:center;padding:20px 0 10px 0;">
    <h1 style="color:#FFD700;font-size:2.8em;margin-bottom:0;">⚖️ {T('المختبر الإلهي للميزان', 'The Divine Mizan Lab')}</h1>
    <h2 style="color:#CCC;font-size:1.2em;margin-top:0;">{T('S = W × B | قانون واحد من الذرة إلى الحضارة', 'S = W × B | One Law from Atom to Civilization')}</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    T("🌌 الكون", "🌌 Cosmos"),
    T("🌍 الأمم", "🌍 Nations"),
    T("🧭 النفس", "🧭 Self"),
    T("📐 الصراط", "📐 Path"),
    T("📜 الرسالة", "📜 Message"),
])

# ═══════════════════════════════════════════════
# ١. الكون
# ═══════════════════════════════════════════════
with tab1:
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init' not in st.session_state: st.session_state.init = False
    if not st.session_state.init:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        sx = np.random.uniform(cx-13, cx+13, N)
        sy = np.random.uniform(cy-9, cy+9, N)
        sw = np.random.uniform(0.1, 1.0, N)
        sb = np.random.uniform(0.1, 1.0, N)
        Wh = [deque([sw[i]], maxlen=50) for i in range(N)]
        Bh = [deque([sb[i]], maxlen=50) for i in range(N)]
        W, B, E = W0, B0, 0.3
        S = S_calc(W, B, Q)
        pWh = deque([W], maxlen=50); pBh = deque([B], maxlen=50)
        ph = T("توازن", "Balance")
        ca, aW, aB = 0.0, 0.0, np.pi*0.5
        eb = deque([S]*30, maxlen=30)
        pS, pE, px = deque(maxlen=400), deque(maxlen=400), deque(maxlen=400)
        fc, gd, bd = 0, 10.0, 5.0
        st.session_state.update({
            'cx':cx,'cy':cy,'sx':sx,'sy':sy,'sw':sw,'sb':sb,'Wh':Wh,'Bh':Bh,
            'W':W,'B':B,'E':E,'S':S,'ph':ph,'ca':ca,'aW':aW,'aB':aB,'eb':eb,
            'pS':pS,'pE':pE,'px':px,'fc':fc,'pWh':pWh,'pBh':pBh,'gd':gd,'bd':bd,'init':True
        })
    if st.session_state.get("run", False):
        placeholder = st.empty()
        while st.session_state.get("run", False):
            W=st.session_state.W; B=st.session_state.B; E=st.session_state.E; S=st.session_state.S
            ph=st.session_state.ph; ca=st.session_state.ca; aW=st.session_state.aW; aB=st.session_state.aB
            sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
            sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
            Wh=st.session_state.Wh; Bh=st.session_state.Bh
            cx=st.session_state.cx; cy=st.session_state.cy; eb=st.session_state.eb
            pS=st.session_state.pS; pE=st.session_state.pE; px=st.session_state.px
            fc=st.session_state.fc; pWh=st.session_state.pWh; pBh=st.session_state.pBh
            gd=st.session_state.gd; bd=st.session_state.bd

            ca += 0.008; sv = np.sin(ca)
            if sv>0.5: ph=T('ذروة','Peak')
            elif sv>0: ph=T('صعود','Rising')
            elif sv>-0.5: ph=T('انهيار','Collapse')
            else: ph=T('قاع','Bottom')
            if 0.3<sv<0.35: ph=T('>> استدراج <<','>> Istidraj <<')
            tgt = 0.5+0.45*sv

            for i in range(N):
                dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
                close = np.where((dist < 2.0) & (np.arange(N) != i))[0]
                sw[i] += (tgt - sw[i])*0.02 + np.random.uniform(-0.02,0.02)
                sb[i] += (tgt - sb[i])*0.02 + np.random.uniform(-0.02,0.02)
                if len(close) > 0:
                    sw[i] += (np.mean(sw[close])-sw[i])*0.03
                    sb[i] += (np.mean(sb[close])-sb[i])*0.03
                sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)
                Wh[i].append(sw[i]); Bh[i].append(sb[i])

            if random.random()<0.005:
                aff = np.random.choice(N, size=int(N*0.2), replace=False)
                sw[aff]*=np.random.uniform(0.5,0.8); sb[aff]*=np.random.uniform(0.5,0.8)

            avgW=np.mean(sw); avgB=np.mean(sb)
            W+=(avgW-W)*0.04; B+=(avgB-B)*0.04
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

            S = S_calc(W,B,Q)
            eb.append(S)
            E_target = list(eb)[-lag] if len(eb)>=lag else S
            E += 0.03*(E_target-E)

            W = W - 0.015*E + 0.03/(S+0.1) - 0.007*(1-B)
            B = B - 0.012*E + 0.006*(1-B)*W*(1-W)
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
            S = S_calc(W,B,Q)

            pWh.append(W); pBh.append(B)
            fc+=1
            if fc%2==0: pS.append(S); pE.append(E); px.append(len(px))

            aW+=0.02+random.uniform(-0.025,0.025)*(1-W)**2
            aB+=0.02+random.uniform(-0.025,0.025)*(1-B)**2
            wx=cx+(7-2.5*W)*np.cos(aW); wy=cy+(7-2.5*W)*np.sin(aW)*0.7
            bx=cx+(5-1.5*B)*np.cos(aB); by=cy+(5-1.5*B)*np.sin(aB)*0.7

            instability = 1-np.mean(sw*sb)
            sx+=np.random.uniform(-0.07,0.07,N)*instability
            sy+=np.random.uniform(-0.07,0.07,N)*instability
            sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)
            gd += W*0.1; bd += (1-B)*0.1

            st.session_state.update({
                'W':W,'B':B,'E':E,'S':S,'ph':ph,'ca':ca,'aW':aW,'aB':aB,'eb':eb,
                'sx':sx,'sy':sy,'sw':sw,'sb':sb,'Wh':Wh,'Bh':Bh,
                'pWh':pWh,'pBh':pBh,'pS':pS,'pE':pE,'px':px,'fc':fc,'gd':gd,'bd':bd
            })

            fig, ax = plt.subplots(figsize=(14,10),facecolor='#000010')
            ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
            for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),
                          (2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                ax.add_patch(Circle((cx,cy),r*(0.5+2.8*S),color=c,alpha=a,zorder=15))
            ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
            ax.add_patch(Circle((cx,cy),0.5+17*E,color='#0FF',alpha=0.25*(1-min(E,1))+0.04,zorder=7))
            ax.add_patch(Circle((cx,cy),8.5,color='#0F8',alpha=0.15,fill=False,lw=2.5,zorder=2))
            ax.add_patch(Circle((wx,wy),0.2+0.6*W,color='#FFF',alpha=1,zorder=13))
            ax.add_patch(Circle((bx,by),0.2+0.6*B,color='#F33',alpha=0.8,zorder=13))
            ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
            ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
            colors = [star_color(sw[i],sb[i]) for i in range(N)]
            ax.scatter(sx,sy,s=30,c=colors,alpha=0.9,edgecolors='white',linewidths=0.3,zorder=5)

            # كفتا الميزان
            akh_x,akh_y,ms=26.5,18,1.5
            ax.plot([akh_x,akh_x],[akh_y-3,akh_y+1.5],color='#FFD700',lw=1,alpha=0.4)
            ly=akh_y-1.5+ms*min(gd/50,1.5); ry=akh_y-1.5-ms*min(bd/50,1.5)
            ax.add_patch(Circle((akh_x-1,ly),0.6,color='#FFD700',alpha=0.3,zorder=20))
            ax.add_patch(Circle((akh_x+1,ry),0.6,color='#FF4444',alpha=0.3,zorder=20))
            ax.text(akh_x-1,ly-1,f'ح {gd:.0f}',color='#FFD700',fontsize=7,ha='center')
            ax.text(akh_x+1,ry-1,f'س {bd:.0f}',color='#FF4444',fontsize=7,ha='center')
            diff = (bd-gd)/50*ms
            ax.plot([akh_x-1,akh_x+1],[akh_y-diff,akh_y+diff],color='#FFD700',lw=1.5,alpha=0.6)

            pax = ax.inset_axes([0.5,0.02,0.46,0.12])
            pax.set_xlim(0,400); pax.set_ylim(0,1.05)
            pax.set_title(T('S يقود E – الاستدراج','S leads E – Istidraj'),color='white',fontsize=7)
            pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
            if pS: pax.plot(list(px),list(pS),color='#FFD700',lw=2); pax.plot(list(px),list(pE),color='#0FF',lw=1.5)

            ax.text(14,1.2,f'{ph} | S={S:.2f} | E={E:.2f}',color='white',fontsize=11,ha='center')
            plt.tight_layout(pad=0); placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.08)
        st.success(T("✅ توقفت المحاكاة", "✅ Simulation stopped"))
    else:
        st.info(T("اضغط ▶️ تشغيل في الشريط الجانبي", "Press ▶️ Run in the sidebar"))
    if not st.session_state.get("run", False) and 'pS' in st.session_state:
        csv_data = "Time,S,E\n" + "\n".join([f"{i},{s:.4f},{e:.4f}" for i,(s,e) in enumerate(zip(st.session_state.pS, st.session_state.pE))])
        st.download_button(T("📥 تحميل بيانات المحاكاة", "📥 Download Data"), data=csv_data, file_name="mizan_cosmic.csv", mime="text/csv")

# ═══════════════════════════════════════════════
# ٢. الأمم
# ═══════════════════════════════════════════════
with tab2:
    st.header(T("🌍 مختبر الأمم والحضارات", "🌍 Nations & Civilizations Lab"))
    st.markdown(T("اضبط مولدات الطاقة وحدود البراءة، وشاهد كيف تنهض الحضارة أو تنهار.", "Adjust energy generators and disavowal boundaries, and watch civilization rise or fall."))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🕌 مولدات الطاقة")
        civ_p = st.slider(T("الصلاة (W)", "Prayer (W)"), 0.0, 1.0, 0.7, 0.01, key="cp")
        civ_f = st.slider(T("الصوم (B)", "Fasting (B)"), 0.0, 1.0, 0.6, 0.01, key="cf")
        civ_z = st.slider(T("الزكاة (B)", "Zakat (B)"), 0.0, 1.0, 0.5, 0.01, key="cz")
        civ_h = st.slider(T("الحج (W)", "Hajj (W)"), 0.0, 1.0, 0.4, 0.01, key="ch")
    with col2:
        st.markdown("### 🛡️ البراءة والجهاد")
        civ_js = st.slider(T("جهاد النفس (B)", "Jihad Self (B)"), 0.0, 1.0, 0.8, 0.01, key="cjs")
        civ_jw = st.slider(T("جهاد المال (B)", "Jihad Wealth (B)"), 0.0, 1.0, 0.5, 0.01, key="cjw")
        civ_d = st.slider(T("البراءة من الطاغوت (B)", "Disavowal (B)"), 0.0, 1.0, 0.9, 0.01, key="cd")
        civ_a = st.slider(T("موالاة المؤمنين (W)", "Alliance (W)"), 0.0, 1.0, 0.8, 0.01, key="ca")
    with col3:
        st.markdown("### ⚖️ أسس الحكم")
        civ_j = st.slider(T("العدل", "Justice"), 0.0, 1.0, 0.6, 0.01, key="cj")
        civ_s = st.slider(T("الشورى", "Consultation"), 0.0, 1.0, 0.5, 0.01, key="cs")
        civ_sh = st.slider(T("تحكيم الشرع", "Sharia"), 0.0, 1.0, 0.5, 0.01, key="csh")
    st.markdown("---")
    st.markdown(T("### 📜 سيناريوهات", "### 📜 Presets"))
    pcol = st.columns(4)
    if pcol[0].button(T("🏴 الراشدة", "🏴 Rashidun"), use_container_width=True):
        civ_p=civ_f=civ_z=civ_h=0.9; civ_js=civ_jw=civ_d=civ_a=0.9; civ_j=civ_s=civ_sh=0.9; st.rerun()
    if pcol[1].button(T("🏳️ العثمانيون", "🏳️ Ottomans"), use_container_width=True):
        civ_p=0.5; civ_f=0.4; civ_z=0.3; civ_h=0.3; civ_js=0.4; civ_jw=0.2; civ_d=0.3; civ_a=0.5; civ_j=0.4; civ_s=0.3; civ_sh=0.4; st.rerun()
    if pcol[2].button(T("🔻 السوفيت", "🔻 Soviets"), use_container_width=True):
        civ_p=civ_f=civ_z=civ_h=0.0; civ_js=civ_jw=civ_d=civ_a=0.0; civ_j=civ_s=civ_sh=0.0; st.rerun()
    if pcol[3].button(T("🕌 الأندلس", "🕌 Andalusia"), use_container_width=True):
        civ_p=0.4; civ_f=0.3; civ_z=0.2; civ_h=0.2; civ_js=0.2; civ_jw=0.1; civ_d=0.2; civ_a=0.3; civ_j=0.3; civ_s=0.2; civ_sh=0.3; st.rerun()
    st.markdown("---")
    if st.button(T("🚀 أطلق", "🚀 Launch"), use_container_width=True, type="primary"):
        Wc = (civ_p + civ_h + civ_a + civ_sh + civ_j*0.5)/4.5
        Bc = (civ_f + civ_z + civ_js + civ_jw + civ_d + civ_j*0.5)/5.5
        Wc=np.clip(Wc,0.01,1.0); Bc=np.clip(Bc,0.01,1.0)
        years=300; Wh=np.zeros(years); Bh=np.zeros(years); Sh=np.zeros(years); Eh=np.zeros(years)
        Wh[0]=Wc; Bh[0]=Bc; Sh[0]=Wc*Bc; Eh[0]=0.1
        for t in range(1,years):
            Wh[t]=Wh[t-1]-0.01*Eh[t-1]+0.01*civ_p*civ_a
            Bh[t]=Bh[t-1]-0.008*Eh[t-1]+0.01*civ_d*civ_js
            Wh[t]+=0.005*civ_sh; Bh[t]+=0.005*civ_sh
            Wh[t]=np.clip(Wh[t],0.01,1.0); Bh[t]=np.clip(Bh[t],0.01,1.0)
            Sh[t]=Wh[t]*Bh[t]
            Et=Sh[max(0,t-lag)]
            Eh[t]=Eh[t-1]+0.03*(Et-Eh[t-1]); Eh[t]=np.clip(Eh[t],0.01,1.0)
        fig,axes=plt.subplots(1,2,figsize=(16,7),facecolor='#000010')
        ax1=axes[0]; ax1.set_facecolor('#0a0a2e')
        ax1.plot(Sh,'g-',lw=2.5,label=T('S (الثبات)','S (Stability)'))
        ax1.plot(Eh,'b--',lw=2.0,label=T('E (التمكين)','E (Empowerment)'))
        ax1.plot(Wh,'gold',lw=1.5,alpha=0.7,label=T('W (الولاء)','W (Loyalty)'))
        ax1.plot(Bh,'#FF5252',lw=1.5,alpha=0.7,label=T('B (البراءة)','B (Disavowal)'))
        ax1.axvspan(np.argmax(Sh),np.argmax(Eh),alpha=0.2,color='red',label=T('فجوة الاستدراج','Istidraj Gap'))
        ax1.set_title(T('دورة الحضارة عبر ٣٠٠ عام','Civilization Cycle 300 Years'),color='white',fontsize=14,fontweight='bold')
        ax1.set_xlabel(T('السنوات','Years'),color='white'); ax1.set_ylabel(T('القيمة','Value'),color='white')
        ax1.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=9)
        ax1.grid(True,alpha=0.2); ax1.tick_params(colors='white'); ax1.set_ylim(0,1.05)
        ax2=axes[1]; ax2.set_facecolor('#0a0a2e')
        ax2.plot(Bh,Wh,'w-',alpha=0.4,lw=0.8)
        ax2.scatter([Bh[0]],[Wh[0]],s=150,c='green',edgecolors='white',linewidth=2,zorder=10,label=T('البداية','Start'))
        ax2.scatter([Bh[-1]],[Wh[-1]],s=150,c='red',edgecolors='white',linewidth=2,zorder=10,label=T('النهاية','End'))
        ax2.axhline(0.5,color='grey',ls=':',lw=1); ax2.axvline(0.5,color='grey',ls=':',lw=1)
        ax2.set_xlim(0,1); ax2.set_ylim(0,1)
        ax2.set_xlabel('B (البراءة)',color='white'); ax2.set_ylabel('W (الولاء)',color='white')
        ax2.set_title(T('مسار الحضارة في فضاء (W,B)','Path in (W,B)'),color='white',fontsize=14,fontweight='bold')
        ax2.fill_between([0.5,1],0.5,1,alpha=0.1,color='green'); ax2.fill_between([0,0.5],0.5,1,alpha=0.1,color='orange')
        ax2.fill_between([0.5,1],0,0.5,alpha=0.1,color='blue'); ax2.fill_between([0,0.5],0,0.5,alpha=0.1,color='red')
        ax2.text(0.75,0.75,T('مؤمن','Believer'),color='green',fontsize=10,ha='center')
        ax2.text(0.25,0.75,T('كافر','Disbeliever'),color='orange',fontsize=10,ha='center')
        ax2.text(0.25,0.25,T('منافق','Hypocrite'),color='red',fontsize=10,ha='center')
        ax2.text(0.75,0.25,T('مشرك','Polytheist'),color='blue',fontsize=10,ha='center')
        ax2.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=9)
        ax2.grid(True,alpha=0.2); ax2.tick_params(colors='white')
        plt.tight_layout(); st.pyplot(fig)
        st.divider()
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric(T("W النهائي","Final W"),f"{Wh[-1]:.3f}")
        c2.metric(T("B النهائي","Final B"),f"{Bh[-1]:.3f}")
        c3.metric(T("S النهائي","Final S"),f"{Sh[-1]:.3f}")
        c4.metric(T("عام الانهيار","Collapse Year"),f"{np.argmin(Sh)}" if Sh[np.argmin(Sh)]<0.2 else T("مستقر","Stable"))
        c5.metric(T("فجوة الاستدراج","Istidraj Gap"),f"{max(0,np.argmax(Eh)-np.argmax(Sh))} {T('عام','yrs')}")

# ═══════════════════════════════════════════════
# ٣. النفس
# ═══════════════════════════════════════════════
with tab3:
    st.header(T("🧭 ميزانك", "🧭 Your Balance"))
    if 'ans' not in st.session_state: st.session_state.ans={}
    qs = {
        "W":[(T("حياتي لله وحده","My life is for Allah alone"),3),
             (T("أقيم الصلاة بخشوع","I pray with devotion"),3),
             (T("أحب الله ورسوله أكثر من كل شيء","I love Allah & Messenger most"),3),
             (T("أتوكل على الله مع الأخذ بالأسباب","I rely on Allah with means"),3),
             (T("أشكر وأصبر","I thank and am patient"),3),
             (T("أحمل هم الإسلام","I carry concerns of Islam"),3)],
        "B":[(T("آمر بالمعروف","I enjoin good"),3),
             (T("أنكر المنكر","I forbid evil"),3),
             (T("أتبرأ من الشرك","I disavow polytheism"),3),
             (T("أجاهد نفسي عن الكذب والغيبة والظلم","I struggle against sins"),3),
             (T("أرفض الظلم","I reject injustice"),3),
             (T("أحب وأبغض في الله","I love & hate for Allah"),3)]
    }
    ca,cb=st.columns(2)
    with ca:
        st.subheader(T("🤍 الولاء (W)","🤍 Loyalty (W)"))
        for i,(q,v) in enumerate(qs["W"]):
            ans=st.radio(q,[T(f"نعم (+{v})",f"Yes (+{v})"),T("أحياناً (+1)","Sometimes (+1)"),T("لا (0)","No (0)"),T("العكس (-1)","Opposite (-1)")],key=f"cw_{i}",index=None)
            if ans:
                if T("نعم","Yes") in ans: st.session_state.ans[f"W{i}"]=v
                elif T("أحياناً","Sometimes") in ans: st.session_state.ans[f"W{i}"]=1
                elif "لا" in ans: st.session_state.ans[f"W{i}"]=0
                else: st.session_state.ans[f"W{i}"]=-1
    with cb:
        st.subheader(T("❤️ البراءة (B)","❤️ Disavowal (B)"))
        for i,(q,v) in enumerate(qs["B"]):
            ans=st.radio(q,[T(f"نعم (+{v})",f"Yes (+{v})"),T("أحياناً (+1)","Sometimes (+1)"),T("لا (0)","No (0)"),T("العكس (-1)","Opposite (-1)")],key=f"cb_{i}",index=None)
            if ans:
                if T("نعم","Yes") in ans: st.session_state.ans[f"B{i}"]=v
                elif T("أحياناً","Sometimes") in ans: st.session_state.ans[f"B{i}"]=1
                elif "لا" in ans: st.session_state.ans[f"B{i}"]=0
                else: st.session_state.ans[f"B{i}"]=-1
    if len(st.session_state.ans)==12:
        Wr=sum(st.session_state.ans[f"W{i}"] for i in range(6))
        Br=sum(st.session_state.ans[f"B{i}"] for i in range(6))
        Wv=np.clip(Wr/18.0,-1,1); Bv=np.clip(Br/18.0,-1,1)
        Wn=(Wv+1)/2; Bn=(Bv+1)/2; Sv=Wn*Bn
        qn,qc=quadrant(Wn,Bn)
        names={"believer":T("المؤمن","Believer"),"disbeliever":T("الكافر","Disbeliever"),"hypocrite":T("المنافق","Hypocrite"),"polytheist":T("المشرك","Polytheist")}
        st.divider(); st.header(T("📊 نتيجتك","📊 Your Result"))
        c1,c2,c3=st.columns(3); c1.metric("W",f"{Wv:.2f}"); c2.metric("B",f"{Bv:.2f}"); c3.metric("S",f"{Sv:.2f}")
        st.markdown(f"<h2 style='color:{qc};text-align:center;'>{names.get(qn,qn)}</h2>",unsafe_allow_html=True)
        fig,ax=plt.subplots(figsize=(6,6),facecolor='#0a0a2e'); ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
        ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
        ax.add_patch(Rectangle((0,0),1,1,color='#FFD700',alpha=0.15))
        ax.add_patch(Rectangle((-1,0),1,1,color='#FF5252',alpha=0.15))
        ax.add_patch(Rectangle((-1,-1),1,1,color='#FFB6C1',alpha=0.15))
        ax.add_patch(Rectangle((0,-1),1,1,color='#FFA500',alpha=0.15))
        ax.scatter(Bv,Wv,s=250,c='#00FFFF',edgecolors='white',linewidth=3,zorder=10)
        ax.set_xlabel("B",color='white'); ax.set_ylabel("W",color='white'); ax.tick_params(colors='white')
        st.pyplot(fig)
        if st.button(T("🔄 أعد","🔄 Retake"),use_container_width=True): st.session_state.ans={}; st.rerun()

# ═══════════════════════════════════════════════
# ٤. الصراط
# ═══════════════════════════════════════════════
with tab4:
    st.header(T("📐 مختبر هندسة الصراط", "📐 Path Geometry Lab"))
    if 'pW' not in st.session_state: st.session_state.pW=[0.5]; st.session_state.pB=[0.5]; st.session_state.pk=[0.0]
    c1,c2,c3=st.columns([1,1,1])
    with c1: sin_s=st.slider(T("⚡ المعصية","⚡ Sin"),0.0,0.1,0.02,0.005,key="sin")
    with c2: rep_s=st.slider(T("💧 التوبة","💧 Sincerity"),0.0,1.0,0.8,0.05,key="rep")
    with c3:
        if st.button(T("🕌 توبة","🕌 Repent"),use_container_width=True):
            cW=st.session_state.pW[-1]; cB=st.session_state.pB[-1]
            st.session_state.pW.append(np.clip(cW+(1.0-cW)*rep_s,0.0,1.0))
            st.session_state.pB.append(np.clip(cB+(1.0-cB)*rep_s,0.0,1.0))
            st.session_state.pk.append(0.0)
            st.rerun()
    b1,b2=st.columns(2)
    if b1.button(T("▶️ خطوة","▶️ Step"),use_container_width=True):
        cW=st.session_state.pW[-1]; cB=st.session_state.pB[-1]
        nW=np.clip(cW-sin_s*(cW-0.2)+np.random.uniform(-0.01,0.01),0.05,1.0)
        nB=np.clip(cB-sin_s*(cB-0.2)+np.random.uniform(-0.01,0.01),0.05,1.0)
        st.session_state.pW.append(nW); st.session_state.pB.append(nB)
        st.session_state.pk.append(curvature(st.session_state.pW,st.session_state.pB) if len(st.session_state.pW)>=3 else 0.0)
        st.rerun()
    if b2.button(T("🔄 إعادة","🔄 Reset"),use_container_width=True):
        st.session_state.pW=[0.5]; st.session_state.pB=[0.5]; st.session_state.pk=[0.0]; st.rerun()
    fig,axes=plt.subplots(1,2,figsize=(16,7),facecolor='#000010')
    ax1=axes[0]; ax1.set_facecolor('#0a0a2e'); ax1.set_xlim(0,1); ax1.set_ylim(0,1)
    ax1.set_xlabel("B",color='white'); ax1.set_ylabel("W",color='white')
    ax1.set_title(T("مسارك","Your Path"),color='white',fontsize=13)
    ax1.plot([0.5,1],[0.5,1],'--',color='#FFD700',lw=2.5,alpha=0.7,label=T("الصراط","Straight"))
    ax1.scatter([1],[1],s=150,c='#FFD700',edgecolors='white',linewidth=2,zorder=10)
    pW=st.session_state.pW; pB=st.session_state.pB
    if len(pW)>1:
        for i in range(1,len(pW)):
            kv=st.session_state.pk[i] if i<len(st.session_state.pk) else 0
            ax1.plot(pB[i-1:i+1],pW[i-1:i+1],color='#00FFFF' if kv<0.05 else '#FF4444',lw=2 if kv<0.05 else 3)
        ax1.scatter([pB[0]],[pW[0]],s=80,c='white',edgecolors='cyan',linewidth=2,zorder=10)
        ax1.scatter([pB[-1]],[pW[-1]],s=120,c='#00FFFF',edgecolors='white',linewidth=3,zorder=10)
    ax1.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=8,loc='lower right')
    ax1.grid(True,alpha=0.2); ax1.tick_params(colors='white')
    ax2=axes[1]; ax2.set_facecolor('#0a0a2e')
    ax2.plot(st.session_state.pk,color='#FFD700',lw=2,marker='o',markersize=3)
    ax2.axhline(y=0.05,color='#FF4444',linestyle='--',alpha=0.6,label=T("حد الخطر","Danger"))
    ax2.axhline(y=0.0,color='#00FF88',linestyle='--',alpha=0.4,label=T("الصراط","Straight"))
    ax2.set_xlabel(T("الخطوات","Steps"),color='white'); ax2.set_ylabel("κ",color='white')
    ax2.set_title(T("الانحناء","Curvature"),color='white',fontsize=13)
    ax2.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=8)
    ax2.grid(True,alpha=0.2); ax2.tick_params(colors='white')
    ax2.set_ylim(-0.01,max(0.2,max(st.session_state.pk)*1.2 if st.session_state.pk else 0.1))
    plt.tight_layout(); st.pyplot(fig)
    st.divider(); c1,c2,c3,c4=st.columns(4)
    c1.metric("W",f"{pW[-1]:.3f}"); c2.metric("B",f"{pB[-1]:.3f}")
    c3.metric("κ",f"{st.session_state.pk[-1]:.4f}")
    c4.metric(T("الصراط؟","On Path?"),T("✅ نعم" if st.session_state.pk[-1]<0.03 else "⚠️ لا","✅ YES" if st.session_state.pk[-1]<0.03 else "⚠️ NO"))

# ═══════════════════════════════════════════════
# ٥. الرسالة
# ═══════════════════════════════════════════════
with tab5:
    st.header(T("📜 رسالة إلى البشرية", "📜 Message to Humanity"))
    st.markdown(T("""
    <div style="text-align:center;font-size:1.1em;line-height:2.2;color:#CCC;">
    > "هَلْ يُوجَد قَانُون وَاحِد يَحْكُم الذَّرَّة وَالْحَضَارَة؟"<br>
    > هَذَا نَمُوذَج الْمِيزَان الَّذِي يُثْبِت أَنَّ <b style="color:#FFD700;">S = W × B</b>
    <br><br>
    <b>هَذَا الْمُخْتَبَر</b> يَجْمَع بَيْن الْكِتَاب الْمَسْطُور وَالْكِتَاب الْمَنْظُور، وَيُثْبِت أَنَّ لِهَذَا الْوُجُود قَانُونًا وَاحِدًا، وَأَنَّ الْجَزَاء مِن جِنْس الْعَمَل.
    <br><br>
    <b style="color:#FFD700;">
    ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾<br>
    ﴿فَمَن يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِن بِاللَّهِ فَقَدِ اسْتَمْسَكَ بِالْعُرْوَةِ الْوُثْقَىٰ﴾
    </b>
    </div>
    ""","""
    <div style="text-align:center;font-size:1.1em;line-height:2.2;color:#CCC;">
    > "Is there a single law governing the atom and civilization?"<br>
    > This Mizan model proves <b style="color:#FFD700;">S = W × B</b>
    <br><br>
    <b>This lab</b> unites the written and observed Books, proving one law governs existence, and recompense mirrors the deed.
    <br><br>
    <b style="color:#FFD700;">
    ﴿And the heaven He raised and imposed the balance﴾<br>
    ﴿Whoever disbelieves in Taghut and believes in Allah has grasped the firm handhold﴾
    </b>
    </div>
    """), unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#888;'>⚖️ S = W × B | ق = الحق = الميزان | © 2026 علي عادل العاطفي</p>", unsafe_allow_html=True)
