import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import random, time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="مختبر الميزان الحي", page_icon="⚖️", layout="wide")

# ═══════════════════════════════════════════════════════════════
# اللغة
# ═══════════════════════════════════════════════════════════════
if "lang" not in st.session_state: st.session_state.lang = "ar"
LANG = st.session_state.lang
def t(ar, en): return ar if LANG == "ar" else en

# ═══════════════════════════════════════════════════════════════
# دوال المحاكاة
# ═══════════════════════════════════════════════════════════════
def get_star_color(w, b):
    if w >= 0.55 and b >= 0.55: return '#FFD700'
    elif w >= 0.55 and b < 0.45: return '#E0E0E0'
    elif w < 0.45 and b >= 0.55: return '#FF5252'
    elif w < 0.45 and b < 0.45: return '#FFB6C1'
    else: return '#888888'

def classify_quadrant(W, B):
    if W >= 0.5 and B >= 0.5: return ("believer", '#FFD700')
    elif W < 0.5 and B >= 0.5: return ("disbeliever", '#FF5252')
    elif W < 0.5 and B < 0.5: return ("hypocrite", '#FFB6C1')
    else: return ("polytheist", '#FFA500')

def compute_curvature(W_hist, B_hist):
    if len(W_hist) < 3: return 0.0
    dW = np.gradient(W_hist); dB = np.gradient(B_hist)
    ddW = np.gradient(dW); ddB = np.gradient(dB)
    num = abs(dW[-1] * ddB[-1] - dB[-1] * ddW[-1])
    denom = (dW[-1]**2 + dB[-1]**2 + 1e-10)**(1.5)
    return num / denom

def calc_S(W, B, E, q_intensity=1.0):
    return np.clip(W * B * (1 + q_intensity * 0.5), 0.001, 1.0)

# ═══════════════════════════════════════════════════════════════
# الشريط الجانبي
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    lang_choice = st.radio("اللغة / Language", ["العربية", "English"], index=0 if LANG == "ar" else 1)
    if (lang_choice == "English" and LANG == "ar") or (lang_choice == "العربية" and LANG == "en"):
        st.session_state.lang = "en" if lang_choice == "English" else "ar"
        st.rerun()
    st.markdown("---")
    st.subheader(t("⚙️ معاملات المختبر", "⚙️ Lab Parameters"))
    W_init = st.slider(t("W الابتدائي", "Initial W"), 0.0, 1.0, 0.55, 0.01)
    B_init = st.slider(t("B الابتدائي", "Initial B"), 0.0, 1.0, 0.52, 0.01)
    lag_frames = st.slider(t("فجوة الاستدراج", "Istidraj Gap"), 5, 50, 22, 1)
    N_STARS = st.slider(t("عدد النجوم", "Stars"), 100, 600, 300, 50)
    q_intensity = st.slider(t("ق (الميزان)", "Q (Balance)"), 0.0, 1.0, 1.0, 0.01)
    st.markdown("---")
    if st.button(t("▶️ تشغيل المشهد", "▶️ Run Scene"), use_container_width=True):
        st.session_state.run = True
    if st.button(t("⏹️ إيقاف", "⏹️ Stop"), use_container_width=True):
        st.session_state.run = False

# ═══════════════════════════════════════════════════════════════
# العنوان
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="text-align:center;padding:20px 0 10px 0;">
    <h1 style="color:#FFD700;font-size:2.8em;margin-bottom:0;">⚖️ {t('مختبر الميزان الحي', 'The Living Mizan Lab')}</h1>
    <h2 style="color:#CCC;font-size:1.2em;margin-top:0;">{t('S = W × B | من الذرة إلى الحضارة', 'S = W × B | From Atom to Civilization')}</h2>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# التبويبات
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    t("🌌 المشهد الكوني", "🌌 The Cosmic Scene"),
    t("🧭 ميزانك", "🧭 Your Balance"),
    t("📐 هندسة الصراط", "📐 Path Geometry"),
])

# ═══════════════════════════════════════════════════════════════
# تبويب ١: المشهد الكوني (المحاكاة الحية)
# ═══════════════════════════════════════════════════════════════
with tab1:
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init_cosmic' not in st.session_state: st.session_state.init_cosmic = False

    if not st.session_state.init_cosmic:
        np.random.seed(42); random.seed(42)
        cx, cy = 14, 10.0
        sx = np.random.uniform(cx-13, cx+13, N_STARS)
        sy = np.random.uniform(cy-9, cy+9, N_STARS)
        sw = np.random.uniform(0.1, 1.0, N_STARS)
        sb = np.random.uniform(0.1, 1.0, N_STARS)
        star_W_hist = [deque([sw[i]], maxlen=50) for i in range(N_STARS)]
        star_B_hist = [deque([sb[i]], maxlen=50) for i in range(N_STARS)]
        W, B, E = W_init, B_init, 0.3
        S = calc_S(W, B, E, q_intensity)
        planet_W_hist = deque([W], maxlen=50)
        planet_B_hist = deque([B], maxlen=50)
        phase = t("توازن", "Balance")
        cycle_angle, angle_W, angle_B = 0.0, 0.0, np.pi*0.5
        eb = deque([S]*30, maxlen=30)
        pS, pE, px = deque(maxlen=400), deque(maxlen=400), deque(maxlen=400)
        frame_count = 0
        good_deeds, bad_deeds = 10.0, 5.0
        st.session_state.update({
            'cx':cx,'cy':cy,'sx':sx,'sy':sy,'sw':sw,'sb':sb,
            'star_W_hist':star_W_hist,'star_B_hist':star_B_hist,
            'W':W,'B':B,'E':E,'S':S,'phase':phase,'cycle_angle':cycle_angle,
            'angle_W':angle_W,'angle_B':angle_B,'empowerment_buffer':eb,
            'history_S':pS,'history_E':pE,'history_x':px,'frame_count':frame_count,
            'planet_W_hist':planet_W_hist,'planet_B_hist':planet_B_hist,
            'good_deeds':good_deeds,'bad_deeds':bad_deeds,'init_cosmic':True
        })

    if st.session_state.get("run", False):
        placeholder = st.empty()
        while st.session_state.get("run", False):
            W=st.session_state.W; B=st.session_state.B; E=st.session_state.E; S=st.session_state.S
            phase=st.session_state.phase; cycle_angle=st.session_state.cycle_angle
            angle_W=st.session_state.angle_W; angle_B=st.session_state.angle_B
            sx=st.session_state.sx.copy(); sy=st.session_state.sy.copy()
            sw=st.session_state.sw.copy(); sb=st.session_state.sb.copy()
            star_W_hist=st.session_state.star_W_hist; star_B_hist=st.session_state.star_B_hist
            cx=st.session_state.cx; cy=st.session_state.cy; eb=st.session_state.empowerment_buffer
            pS=st.session_state.history_S; pE=st.session_state.history_E; px=st.session_state.history_x
            frame_count=st.session_state.frame_count
            planet_W_hist=st.session_state.planet_W_hist; planet_B_hist=st.session_state.planet_B_hist
            good_deeds=st.session_state.good_deeds; bad_deeds=st.session_state.bad_deeds

            cycle_angle += 0.008; sv = np.sin(cycle_angle)
            if sv>0.5: phase=t('ذروة الاستقرار','Peak')
            elif sv>0: phase=t('صعود','Rising')
            elif sv>-0.5: phase=t('انهيار','Collapse')
            else: phase=t('القاع','Bottom')
            if 0.3<sv<0.35: phase=t('>> استدراج <<','>> Istidraj <<')
            target_S = 0.5+0.45*sv

            for i in range(N_STARS):
                dist=np.sqrt((sx[i]-sx)**2+(sy[i]-sy)**2)
                close_cond = (dist<2.0)&(np.arange(N_STARS)!=i)
                close = np.where(close_cond)[0]
                sw[i]+=(target_S-sw[i])*0.02+np.random.uniform(-0.02,0.02)
                sb[i]+=(target_S-sb[i])*0.02+np.random.uniform(-0.02,0.02)
                if len(close)>0:
                    sw[i]+=(np.mean(sw[close])-sw[i])*0.03
                    sb[i]+=(np.mean(sb[close])-sb[i])*0.03
                sw[i]=np.clip(sw[i],0.01,1.0); sb[i]=np.clip(sb[i],0.01,1.0)
                star_W_hist[i].append(sw[i]); star_B_hist[i].append(sb[i])

            if random.random()<0.005:
                aff=np.random.choice(N_STARS,size=int(N_STARS*0.2),replace=False)
                sw[aff]*=np.random.uniform(0.5,0.8); sb[aff]*=np.random.uniform(0.5,0.8)

            avgW=np.mean(sw); avgB=np.mean(sb)
            W+=(avgW-W)*0.04; B+=(avgB-B)*0.04
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

            S = calc_S(W,B,E,q_intensity)
            eb.append(S)
            E_target = list(eb)[-lag_frames] if len(eb)>=lag_frames else S
            E += 0.03*(E_target-E)
            W = W-0.015*E+0.03/(S+0.1)-0.007*(1-B)
            B = B-0.012*E+0.006*(1-B)*W*(1-W)
            W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
            S = calc_S(W,B,E,q_intensity)

            planet_W_hist.append(W); planet_B_hist.append(B)
            frame_count+=1
            if frame_count%2==0: pS.append(S); pE.append(E); px.append(len(px))

            angle_W+=0.02+random.uniform(-0.025,0.025)*(1-W)**2
            angle_B+=0.02+random.uniform(-0.025,0.025)*(1-B)**2
            wx=cx+(7-2.5*W)*np.cos(angle_W); wy=cy+(7-2.5*W)*np.sin(angle_W)*0.7
            bx=cx+(5-1.5*B)*np.cos(angle_B); by=cy+(5-1.5*B)*np.sin(angle_B)*0.7

            instability=1-np.mean(sw*sb)
            sx+=np.random.uniform(-0.07,0.07,N_STARS)*instability
            sy+=np.random.uniform(-0.07,0.07,N_STARS)*instability
            sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)

            good_deeds+=W*0.1; bad_deeds+=(1-B)*0.1

            st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
            st.session_state.phase=phase; st.session_state.cycle_angle=cycle_angle
            st.session_state.angle_W=angle_W; st.session_state.angle_B=angle_B
            st.session_state.empowerment_buffer=eb
            st.session_state.sx=sx; st.session_state.sy=sy; st.session_state.sw=sw; st.session_state.sb=sb
            st.session_state.star_W_hist=star_W_hist; st.session_state.star_B_hist=star_B_hist
            st.session_state.planet_W_hist=planet_W_hist; st.session_state.planet_B_hist=planet_B_hist
            st.session_state.history_S=pS; st.session_state.history_E=pE; st.session_state.history_x=px
            st.session_state.frame_count=frame_count
            st.session_state.good_deeds=good_deeds; st.session_state.bad_deeds=bad_deeds

            fig,ax=plt.subplots(figsize=(14,10),facecolor='#000010')
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
            colors=[get_star_color(sw[i],sb[i]) for i in range(N_STARS)]
            ax.scatter(sx,sy,s=30,c=colors,alpha=0.9,edgecolors='white',linewidths=0.3,zorder=5)

            # كفتا الميزان
            akh_x,akh_y,ms=26.5,18,1.5
            ax.plot([akh_x,akh_x],[akh_y-3,akh_y+1.5],color='#FFD700',lw=1,alpha=0.4)
            ly=akh_y-1.5+ms*min(good_deeds/50,1.5); ry=akh_y-1.5-ms*min(bad_deeds/50,1.5)
            ax.add_patch(Circle((akh_x-1,ly),0.6,color='#FFD700',alpha=0.3,zorder=20))
            ax.text(akh_x-1,ly-1,f'ح {good_deeds:.0f}',color='#FFD700',fontsize=7,ha='center')
            ax.add_patch(Circle((akh_x+1,ry),0.6,color='#FF4444',alpha=0.3,zorder=20))
            ax.text(akh_x+1,ry-1,f'س {bad_deeds:.0f}',color='#FF4444',fontsize=7,ha='center')
            diff=(bad_deeds-good_deeds)/50*ms
            ax.plot([akh_x-1,akh_x+1],[akh_y-diff,akh_y+diff],color='#FFD700',lw=1.5,alpha=0.6)

            # منحنى الاستدراج
            pax=ax.inset_axes([0.5,0.02,0.46,0.12])
            pax.set_xlim(0,400); pax.set_ylim(0,1.05)
            pax.set_title(t('S يقود E – الاستدراج','S leads E – Istidraj'),color='white',fontsize=7)
            pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
            if pS: pax.plot(list(px),list(pS),color='#FFD700',lw=2); pax.plot(list(px),list(pE),color='#0FF',lw=1.5)

            ax.text(14,1.2,f'{phase} | S={S:.2f} | E={E:.2f}',color='white',fontsize=11,ha='center')
            plt.tight_layout(pad=0)
            placeholder.pyplot(fig); plt.close(fig)
            time.sleep(0.08)
        st.success(t("✅ توقفت المحاكاة", "✅ Simulation stopped"))
    else:
        st.info(t("اضغط ▶️ تشغيل المشهد", "Press ▶️ Run Scene"))

# ═══════════════════════════════════════════════════════════════
# تبويب ٢: ميزانك (البوصلة)
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.header(t("🧭 ميزانك", "🧭 Your Balance"))
    if 'compass_answers' not in st.session_state: st.session_state.compass_answers = {}
    questions = {
        "W": [
            (t("حياتي كلها لله، لا أبتغي بها إلا وجهه", "My whole life is for Allah alone"), 3),
            (t("أقيم الصلاة بخشوع، أستشعر الوقوف بين يدي الله", "I pray with devotion"), 3),
            (t("أحب الله ورسوله أكثر من كل شيء", "I love Allah & Messenger most"), 3),
            (t("أتوكل على الله مع الأخذ بالأسباب", "I rely on Allah with means"), 3),
            (t("أشكر الله في الرخاء وأصبر في البلاء", "I thank and am patient"), 3),
            (t("أحمل هم الإسلام والمسلمين، وأسعى لنصرتهم", "I carry concerns of Islam"), 3),
        ],
        "B": [
            (t("آمر بالمعروف بالحكمة والموعظة الحسنة", "I enjoin good wisely"), 3),
            (t("أنكر المنكر بلساني أو قلبي", "I forbid evil"), 3),
            (t("أتبرأ من الشرك وأهله، وأعلن براءتي منهم", "I disavow polytheism"), 3),
            (t("أجاهد نفسي على ترك الكذب والغيبة والظلم", "I struggle against sins"), 3),
            (t("أرفض الظلم بكل صوره، ولا أرضاه لأحد", "I reject all injustice"), 3),
            (t("أحب في الله وأبغض في الله، أوالي أولياءه وأعادي أعداءه", "I love & hate for Allah"), 3),
        ]
    }
    colA, colB = st.columns(2)
    with colA:
        st.subheader(t("🤍 الولاء (W)", "🤍 Loyalty (W)"))
        for i, (q, v) in enumerate(questions["W"]):
            ans = st.radio(q, [t(f"نعم (+{v})", f"Yes (+{v})"), t(f"أحياناً (+1)", "Sometimes (+1)"), t("لا (0)", "No (0)"), t(f"العكس (-1)", "Opposite (-1)")], key=f"cw_{i}", index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"W{i}"] = v
                elif t("أحياناً","Sometimes") in ans: st.session_state.compass_answers[f"W{i}"] = 1
                elif "لا" in ans and "0" in ans: st.session_state.compass_answers[f"W{i}"] = 0
                else: st.session_state.compass_answers[f"W{i}"] = -1
    with colB:
        st.subheader(t("❤️ البراءة (B)", "❤️ Disavowal (B)"))
        for i, (q, v) in enumerate(questions["B"]):
            ans = st.radio(q, [t(f"نعم (+{v})", f"Yes (+{v})"), t(f"أحياناً (+1)", "Sometimes (+1)"), t("لا (0)", "No (0)"), t(f"العكس (-1)", "Opposite (-1)")], key=f"cb_{i}", index=None)
            if ans:
                if t("نعم","Yes") in ans: st.session_state.compass_answers[f"B{i}"] = v
                elif t("أحياناً","Sometimes") in ans: st.session_state.compass_answers[f"B{i}"] = 1
                elif "لا" in ans and "0" in ans: st.session_state.compass_answers[f"B{i}"] = 0
                else: st.session_state.compass_answers[f"B{i}"] = -1

    if len(st.session_state.compass_answers) == 12:
        W_raw = sum(st.session_state.compass_answers[f"W{i}"] for i in range(6))
        B_raw = sum(st.session_state.compass_answers[f"B{i}"] for i in range(6))
        W_val = W_raw / 18.0; B_val = B_raw / 18.0
        W_val = np.clip(W_val, -1, 1); B_val = np.clip(B_val, -1, 1)
        qn, qc = classify_quadrant((W_val+1)/2, (B_val+1)/2)
        names = {"believer":t("المؤمن ♧","Believer"),"disbeliever":t("الكافر","Disbeliever"),
                 "hypocrite":t("المنافق","Hypocrite"),"polytheist":t("المشرك","Polytheist")}
        st.divider(); st.header(t("📊 نتيجتك", "📊 Your Result"))
        c1,c2,c3=st.columns(3); c1.metric("W",f"{W_val:.2f}"); c2.metric("B",f"{B_val:.2f}"); c3.metric("S",f"{abs((W_val+1)/2*(B_val+1)/2):.2f}")
        st.markdown(f"<h2 style='color:{qc};text-align:center;'>{names.get(qn,qn)}</h2>",unsafe_allow_html=True)
        fig,ax=plt.subplots(figsize=(6,6),facecolor='#0a0a2e'); ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
        ax.axhline(0,color='grey',lw=0.5); ax.axvline(0,color='grey',lw=0.5)
        ax.add_patch(Rectangle((0,0),1,1,color='#FFD700',alpha=0.15))
        ax.add_patch(Rectangle((-1,0),1,1,color='#FF5252',alpha=0.15))
        ax.add_patch(Rectangle((-1,-1),1,1,color='#FFB6C1',alpha=0.15))
        ax.add_patch(Rectangle((0,-1),1,1,color='#FFA500',alpha=0.15))
        ax.text(0.5,0.5,t("مؤمن","Believer"),ha='center',color='white',alpha=0.6)
        ax.text(-0.5,0.5,t("كافر","Disbeliever"),ha='center',color='white',alpha=0.6)
        ax.text(-0.5,-0.5,t("منافق","Hypocrite"),ha='center',color='white',alpha=0.6)
        ax.text(0.5,-0.5,t("مشرك","Polytheist"),ha='center',color='white',alpha=0.6)
        ax.scatter(B_val,W_val,s=250,c='#00FFFF',edgecolors='white',linewidth=3,zorder=10)
        ax.set_xlabel("B",color='white'); ax.set_ylabel("W",color='white'); ax.tick_params(colors='white')
        st.pyplot(fig)
        if st.button(t("🔄 أعد الميزان", "🔄 Retake"), use_container_width=True):
            st.session_state.compass_answers = {}; st.rerun()

# ═══════════════════════════════════════════════════════════════
# تبويب ٣: هندسة الصراط (مختبر تفاعلي)
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.header(t("📐 مختبر هندسة الصراط", "📐 Path Geometry Lab"))
    if 'path_W' not in st.session_state:
        st.session_state.path_W = [0.5]
        st.session_state.path_B = [0.5]
        st.session_state.path_kappa = [0.0]

    c1,c2,c3 = st.columns([1,1,1])
    with c1:
        sin_strength = st.slider(t("⚡ شدة المعصية", "⚡ Sin Strength"), 0.0, 0.1, 0.02, 0.005)
    with c2:
        repentance_sincerity = st.slider(t("💧 صدق التوبة", "💧 Sincerity"), 0.0, 1.0, 0.8, 0.05)
    with c3:
        if st.button(t("🕌 توبة", "🕌 Repent"), use_container_width=True, type="primary"):
            cW = st.session_state.path_W[-1]; cB = st.session_state.path_B[-1]
            st.session_state.path_W.append(np.clip(cW + (1.0-cW)*repentance_sincerity, 0.0, 1.0))
            st.session_state.path_B.append(np.clip(cB + (1.0-cB)*repentance_sincerity, 0.0, 1.0))
            st.session_state.path_kappa.append(0.0)
            st.rerun()

    if st.button(t("▶️ خطوة", "▶️ Step"), use_container_width=True):
        cW = st.session_state.path_W[-1]; cB = st.session_state.path_B[-1]
        nW = cW - sin_strength*(cW-0.2) + np.random.uniform(-0.01,0.01)
        nB = cB - sin_strength*(cB-0.2) + np.random.uniform(-0.01,0.01)
        nW=np.clip(nW,0.05,1.0); nB=np.clip(nB,0.05,1.0)
        st.session_state.path_W.append(nW); st.session_state.path_B.append(nB)
        kappa = compute_curvature(st.session_state.path_W, st.session_state.path_B) if len(st.session_state.path_W)>=3 else 0.0
        st.session_state.path_kappa.append(kappa)
        st.rerun()

    if st.button(t("🔄 إعادة", "🔄 Reset Path"), use_container_width=True):
        st.session_state.path_W=[0.5]; st.session_state.path_B=[0.5]; st.session_state.path_kappa=[0.0]; st.rerun()

    fig,axes = plt.subplots(1,2,figsize=(16,7),facecolor='#000010')
    ax1=axes[0]; ax1.set_facecolor('#0a0a2e'); ax1.set_xlim(0,1); ax1.set_ylim(0,1)
    ax1.set_xlabel("B",color='white'); ax1.set_ylabel("W",color='white')
    ax1.set_title(t("مسارك في فضاء (W,B)", "Your Path in (W,B)"),color='white',fontsize=13)
    ax1.plot([0.5,1],[0.5,1],'--',color='#FFD700',lw=2.5,alpha=0.7,label=t("الصراط (إبراهيم)", "Straight Path"))
    ax1.scatter([1],[1],s=150,c='#FFD700',edgecolors='white',linewidth=2,zorder=10,label=t("الكمال", "Perfection"))
    pW=st.session_state.path_W; pB=st.session_state.path_B
    if len(pW)>1:
        for i in range(1,len(pW)):
            kv = st.session_state.path_kappa[i] if i<len(st.session_state.path_kappa) else 0
            cl = '#00FFFF' if kv<0.05 else '#FF4444'
            ax1.plot(pB[i-1:i+1],pW[i-1:i+1],color=cl,lw=2 if kv<0.05 else 3)
        ax1.scatter([pB[0]],[pW[0]],s=80,c='white',edgecolors='cyan',linewidth=2,zorder=10,label=t("البداية","Start"))
        ax1.scatter([pB[-1]],[pW[-1]],s=120,c='#00FFFF',edgecolors='white',linewidth=3,zorder=10,label=t("الآن","Now"))
    ax1.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=8,loc='lower right')
    ax1.grid(True,alpha=0.2); ax1.tick_params(colors='white')

    ax2=axes[1]; ax2.set_facecolor('#0a0a2e')
    ax2.plot(st.session_state.path_kappa,color='#FFD700',lw=2,marker='o',markersize=3)
    ax2.axhline(y=0.05,color='#FF4444',linestyle='--',alpha=0.6,label=t("حد الخطر","Danger"))
    ax2.axhline(y=0.0,color='#00FF88',linestyle='--',alpha=0.4,label=t("الصراط","Straight"))
    ax2.set_xlabel(t("الخطوات","Steps"),color='white'); ax2.set_ylabel("κ",color='white')
    ax2.set_title(t("منحنى الانحناء", "Curvature Curve"),color='white',fontsize=13)
    ax2.legend(facecolor='#0a0a2e',edgecolor='white',labelcolor='white',fontsize=8)
    ax2.grid(True,alpha=0.2); ax2.tick_params(colors='white')
    ax2.set_ylim(-0.01,max(0.2,max(st.session_state.path_kappa)*1.2 if st.session_state.path_kappa else 0.1))
    plt.tight_layout(); st.pyplot(fig)

    st.divider()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("W",f"{pW[-1]:.3f}"); c2.metric("B",f"{pB[-1]:.3f}")
    c3.metric("κ",f"{st.session_state.path_kappa[-1]:.4f}")
    c4.metric(t("الصراط؟","On Path?"),t("✅ نعم" if st.session_state.path_kappa[-1]<0.03 else "⚠️ لا","✅ YES" if st.session_state.path_kappa[-1]<0.03 else "⚠️ NO"))

# ═══════════════════════════════════════════════════════════════
# التذييل
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#888;'>⚖️ S = W × B | ق = الحق = الميزان | © 2026 علي عادل العاطفي</p>", unsafe_allow_html=True)
