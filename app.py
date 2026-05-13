import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# =============================================
# إعداد الصفحة
# =============================================
st.set_page_config(page_title="⚖️ المنصة الذهبية", page_icon="⚖️", layout="wide")

# =============================================
# النظام اللغوي
# =============================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
LANG = st.session_state.lang
TXT = lambda ar, en: ar if LANG == "ar" else en

# =============================================
# قاعدة بيانات الحروف – الفئات الست
# =============================================
LETTERS = {
    "source": {
        "ك": {"val": 20, "label": TXT("الأمر (كُن)", "Command (Be)")},
        "ن": {"val": 50, "label": TXT("النور", "Light")},
    },
    "dual": {
        "ق": {"val": 100, "label": TXT("الميزان / القسط", "Balance / Equity")},
        "ص": {"val": 90, "label": TXT("الصمد / الصبر", "Eternal / Patience")},
    },
    "manifestation": {
        "أ": {"val": 1, "label": TXT("الوحدانية", "Oneness")},
        "ل": {"val": 30, "label": TXT("المُلك والعدل", "Sovereignty & Justice")},
        "م": {"val": 40, "label": TXT("الجمع والتماسك", "Gathering")},
        "ر": {"val": 200, "label": TXT("اليقظة", "Vigilance")},
        "س": {"val": 60, "label": TXT("السمع", "Hearing")},
        "ح": {"val": 8, "label": TXT("الحياة", "Life")},
        "ط": {"val": 9, "label": TXT("الطهارة", "Purity")},
    },
    "connection": {
        "ع": {"val": 70, "label": TXT("الإدراك", "Perception")},
        "ي": {"val": 10, "label": TXT("الهوية والنسبة", "Identity & Belonging")},
        "هـ": {"val": 5, "label": TXT("الوجود والحضور", "Existence & Presence")},
    },
    "operators": {
        "ف": {"val": 80, "role": "=", "label": TXT("فاء السببية", "Causative Fa")},
        "و": {"val": 6, "role": "×/+", "label": TXT("واو العطف", "Conjunctive Waw")},
        "ب": {"val": 2, "role": "بـ", "label": TXT("باء الاستعانة", "Instrumental Ba")},
        "ل": {"val": 30, "role": "→", "label": TXT("لام التعليل", "Purpose Lam")},
    },
    "actions": {
        "ج": {"val": 3, "pos": TXT("الجهاد", "Struggle"), "neg": TXT("الجهل", "Ignorance")},
        "خ": {"val": 600, "pos": TXT("الخير", "Goodness"), "neg": TXT("الخيانة", "Betrayal")},
        "د": {"val": 4, "pos": TXT("الدين", "Religion"), "neg": TXT("التدمير", "Destruction")},
        "ذ": {"val": 700, "pos": TXT("الذكر", "Remembrance"), "neg": TXT("الذل", "Humiliation")},
        "ز": {"val": 7, "pos": TXT("الزكاة", "Charity"), "neg": TXT("الزور", "Falsehood")},
        "ش": {"val": 300, "pos": TXT("الشكر", "Gratitude"), "neg": TXT("الشهوة", "Lust")},
        "ت": {"val": 400, "pos": TXT("التوبة", "Repentance"), "neg": TXT("التيه", "Wandering")},
        "ث": {"val": 500, "pos": TXT("الثبات", "Steadfastness"), "neg": TXT("الثبور", "Destruction")},
        "ض": {"val": 800, "pos": TXT("الضياء", "Radiance"), "neg": TXT("الضلال", "Misguidance")},
        "ظ": {"val": 900, "pos": TXT("الظفر", "Victory"), "neg": TXT("الظلم", "Injustice")},
        "غ": {"val": 1000, "pos": TXT("الغفران", "Forgiveness"), "neg": TXT("الغش", "Fraud")},
    },
}

# =============================================
# دالة الميزان – المعادلة النهائية
# =============================================
def calc_S(W, B, E, source_v, dual_v, manif_v, conn_v, op_v, act_v,
          amr=0.5, nahy=0.5, adl=0.6, shura=0.5, riba=0.2, zulm=0.2, khi=0.2):
    S = W * B

    # 1. المصدر (ك، ن)
    sf = (source_v.get('ك',0.5)*20 + source_v.get('ن',0.5)*50) / 2
    S *= (0.3 + 0.7*sf/100)

    # 2. الازدواج (ق، ص)
    df = (dual_v.get('ق',0.5)*100 + dual_v.get('ص',0.5)*90) / 2
    S *= (0.5 + 0.5*df/100)

    # 3. التجلي
    mb = sum(manif_v.values()) / max(len(manif_v), 1)
    S *= (0.4 + 0.6*mb)

    # 4. الجسور
    cb = sum(conn_v.values()) / max(len(conn_v), 1)
    S *= (0.7 + 0.6*cb)

    # 5. المشغلات
    ف = op_v.get('ف',0.5); و = op_v.get('و',0.5)
    ب = op_v.get('ب',0.5); ل = op_v.get('ل',0.5)
    of = (ف*80 + و*6 + ب*2 + ل*30) / 118
    S *= (0.7 + 0.6*of)

    # 6. الأعمال
    pos = sum(v for v in act_v.values() if v > 0)
    neg = sum(abs(v) for v in act_v.values() if v < 0)
    S *= (1.0 + 0.2*pos/max(len(act_v),1))
    S *= (1.0 - 0.3*neg/max(len(act_v),1))

    # 7. الحكم
    S *= (0.5 + 0.5*amr*nahy)
    S *= (0.8 + 0.4*adl)
    S *= (0.85 + 0.3*shura)
    S *= (1 - 0.3*riba)
    S *= (1 - 0.25*zulm)
    S *= (1 - 0.15*khi)

    # 8. الاستدراج
    if E > S:
        S -= 0.1 * (E - S)

    return np.clip(S, 0.001, 1.0)

# =============================================
# الشريط الجانبي
# =============================================
with st.sidebar:
    st.markdown("## ⚖️ المنصة الذهبية")
    st.markdown("### S = W × B")
    lang_btn = st.button("English" if LANG=="ar" else "العربية")
    if lang_btn:
        st.session_state.lang = "en" if LANG=="ar" else "ar"
        st.rerun()
    st.divider()

    # إعدادات أساسية
    st.subheader(TXT("⚙️ إعدادات أساسية","⚙️ Basic Settings"))
    W_init = st.slider("W", 0.0,1.0,0.55,0.01)
    B_init = st.slider("B", 0.0,1.0,0.52,0.01)
    N = st.slider(TXT("عدد النجوم","Stars"), 100,500,300,50)
    delay = st.slider(TXT("تأخير الاستدراج","Istidraj Lag"), 5,50,22,1)
    st.divider()

    # الفئات الست – في أقسام قابلة للطي
    source_v, dual_v, manif_v, conn_v, op_v, act_v = {}, {}, {}, {}, {}, {}

    with st.expander(TXT("🔮 المصدر (ك، ن)","🔮 Source (K, N)")):
        for l, d in LETTERS["source"].items():
            source_v[l] = st.slider(f"{l} – {d['label']}", 0.0,1.0,0.8,0.01, key=f"src_{l}")

    with st.expander(TXT("⚖️ الازدواج (ق، ص)","⚖️ Dual (Q, S)")):
        for l, d in LETTERS["dual"].items():
            dual_v[l] = st.slider(f"{l} – {d['label']}", 0.0,1.0,0.7,0.01, key=f"dual_{l}")

    with st.expander(TXT("🔆 التجلي (7 حروف)","🔆 Manifestation (7)")):
        for l, d in LETTERS["manifestation"].items():
            manif_v[l] = st.slider(f"{l} – {d['label']}", 0.0,1.0,0.7,0.01, key=f"man_{l}")

    with st.expander(TXT("🔄 الجسور (ع، ي، هـ)","🔄 Bridges (A, Y, H)")):
        for l, d in LETTERS["connection"].items():
            conn_v[l] = st.slider(f"{l} – {d['label']}", 0.0,1.0,0.7,0.01, key=f"conn_{l}")

    with st.expander(TXT("⚡ المشغلات (ف، و، ب، ل)","⚡ Operators (F, W, B, L)")):
        for l, d in LETTERS["operators"].items():
            op_v[l] = st.slider(f"{l} ({d['role']}) – {d['label']}", 0.0,1.0,0.5,0.01, key=f"op_{l}")

    with st.expander(TXT("💚 الأعمال (11 حرفاً)","💚 Actions (11 letters)")):
        for l, d in LETTERS["actions"].items():
            act_v[l] = st.slider(f"{l} – {d['pos']} / {d['neg']}", -1.0,1.0,0.0,0.1, key=f"act_{l}")

    st.divider()
    c1, c2, c3 = st.columns(3)
    if c1.button("▶️", use_container_width=True): st.session_state.run = True
    if c2.button("⏹️", use_container_width=True): st.session_state.run = False
    if c3.button("🔄", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("lang",): del st.session_state[k]
        st.rerun()

# =============================================
# العنوان
# =============================================
st.markdown(f"""
<div style="text-align:center">
    <h1 style="color:#FFD700">⚖️ {TXT('المنصة الذهبية','The Golden Platform')}</h1>
    <p style="color:#CCC">S = W × B | {TXT('من الذرة إلى الحضارة','From Atom to Civilization')}</p>
</div>
""", unsafe_allow_html=True)

# =============================================
# التهيئة
# =============================================
if 'init' not in st.session_state:
    np.random.seed(42); random.seed(42)
    cx, cy = 14.0, 10.0
    st.session_state.cx = cx; st.session_state.cy = cy
    st.session_state.sx = np.random.uniform(cx-11, cx+11, N)
    st.session_state.sy = np.random.uniform(cy-7, cy+7, N)
    st.session_state.sw = np.random.uniform(0.1,1.0,N)
    st.session_state.sb = np.random.uniform(0.1,1.0,N)
    st.session_state.W = W_init; st.session_state.B = B_init
    st.session_state.E = 0.3; st.session_state.S = W_init*B_init
    st.session_state.ph = TXT("توازن","Balance"); st.session_state.ca = 0.0
    st.session_state.aW = 0.0; st.session_state.aB = np.pi*0.5
    st.session_state.eb = deque([W_init*B_init]*30, maxlen=30)
    st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
    st.session_state.px = deque(maxlen=400)
    st.session_state.init = True

# =============================================
# حلقة المحاكاة (بدون while – باستخدام st.rerun)
# =============================================
def run_one_frame():
    W = st.session_state.W; B = st.session_state.B; E = st.session_state.E
    S = st.session_state.S; ph = st.session_state.ph; ca = st.session_state.ca
    aW = st.session_state.aW; aB = st.session_state.aB
    sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
    sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
    cx = st.session_state.cx; cy = st.session_state.cy
    eb = st.session_state.eb; pS = st.session_state.pS; pE = st.session_state.pE; px = st.session_state.px

    ca += 0.008; sv = np.sin(ca)
    if sv>0.5: ph = TXT('ذروة','Peak')
    elif sv>0: ph = TXT('صعود','Rising')
    elif sv>-0.5: ph = TXT('انهيار','Collapse')
    else: ph = TXT('قاع','Bottom')
    if 0.3<sv<0.35: ph = TXT('>> استدراج <<','>> Istidraj <<')
    target = 0.5 + 0.45*sv

    # تأثير المشغلات "ف" و"و" على النجوم
    ف_effect = op_v.get('ف', 0.5)  # قيمة السببية: تحدد قوة تأثير الأسباب
    و_effect = op_v.get('و', 0.5)  # واو العطف: تحدد قوة التجاذب بين النجوم

    for i in range(N):
        sw[i] += (target-sw[i])*0.02*ف_effect + np.random.uniform(-0.02,0.02)
        sb[i] += (target-sb[i])*0.02*ف_effect + np.random.uniform(-0.02,0.02)
        dist = np.sqrt((sx[i]-sx)**2 + (sy[i]-sy)**2)
        close = (dist<2.0) & (np.arange(N)!=i)
        if np.any(close):
            sw[i] += (np.mean(sw[close])-sw[i])*0.03*و_effect
            sb[i] += (np.mean(sb[close])-sb[i])*0.03*و_effect
        sw[i] = np.clip(sw[i],0.01,1.0); sb[i] = np.clip(sb[i],0.01,1.0)

    if random.random()<0.005:
        aff = np.random.choice(N,size=int(N*0.2),replace=False)
        sw[aff]*=random.uniform(0.5,0.8); sb[aff]*=random.uniform(0.5,0.8)

    W += (np.mean(sw)-W)*0.04; B += (np.mean(sb)-B)*0.04
    W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)

    S = calc_S(W,B,E,source_v,dual_v,manif_v,conn_v,op_v,act_v)
    eb.append(S)
    Et = list(eb)[-delay] if len(eb)>=delay else S
    E += 0.03*(Et-E)

    W = W - 0.015*E + 0.03/(S+0.1) - 0.007*(1-B)
    B = B - 0.012*E + 0.006*(1-B)*W*(1-W)
    W=np.clip(W,0.01,1.0); B=np.clip(B,0.01,1.0)
    S = calc_S(W,B,E,source_v,dual_v,manif_v,conn_v,op_v,act_v)

    if len(px)%2==0:
        pS.append(S); pE.append(E); px.append(len(px))

    aW += 0.02+random.uniform(-0.025,0.025)*(1-W)**2
    aB += 0.02+random.uniform(-0.025,0.025)*(1-B)**2
    wx=cx+(7-2.5*W)*np.cos(aW); wy=cy+(7-2.5*W)*np.sin(aW)*0.7
    bx=cx+(5-1.5*B)*np.cos(aB); by=cy+(5-1.5*B)*np.sin(aB)*0.7

    ins = 1-np.mean(sw*sb)
    sx+=np.random.uniform(-0.07,0.07,N)*ins; sy+=np.random.uniform(-0.07,0.07,N)*ins
    sx=np.clip(sx,cx-13,cx+13); sy=np.clip(sy,cy-9,cy+9)

    st.session_state.W=W; st.session_state.B=B; st.session_state.E=E; st.session_state.S=S
    st.session_state.ph=ph; st.session_state.ca=ca; st.session_state.aW=aW; st.session_state.aB=aB
    st.session_state.eb=eb; st.session_state.sx=sx; st.session_state.sy=sy
    st.session_state.sw=sw; st.session_state.sb=sb; st.session_state.pS=pS; st.session_state.pE=pE; st.session_state.px=px

    # رسم
    fig,ax=plt.subplots(figsize=(14,10),facecolor='#000010')
    ax.set_xlim(0,28); ax.set_ylim(0,20); ax.axis('off')
    for r,a,c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),(2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
        ax.add_patch(Circle((cx,cy),r*(0.5+2.8*S),color=c,alpha=a,zorder=15))
    ax.text(cx,cy,'S',color='#1a1000',fontsize=16,ha='center',va='center',fontweight='bold')
    ax.add_patch(Circle((cx,cy),0.5+16*E,color='#0FF',alpha=0.25*(1-min(E,1))+0.04,zorder=7))
    ax.add_patch(Circle((cx,cy),8.5,color='#0F8',alpha=0.15,fill=False,lw=2.5,zorder=2))
    ax.add_patch(Circle((wx,wy),0.2+0.6*W,color='#FFF',alpha=1,zorder=13))
    ax.add_patch(Circle((bx,by),0.2+0.6*B,color='#F33',alpha=0.8,zorder=13))
    ax.text(wx,wy+0.8,'W',color='#FFF',fontsize=10,ha='center')
    ax.text(bx,by+0.8,'B',color='#F33',fontsize=10,ha='center')
    cols=[]
    for i in range(N):
        w,bv=sw[i],sb[i]
        if w>=0.55 and bv>=0.55: cols.append('#FFD700')
        elif w>=0.55 and bv<0.45: cols.append('#E0E0E0')
        elif w<0.45 and bv>=0.55: cols.append('#FF5252')
        elif w<0.45 and bv<0.45: cols.append('#FFB6C1')
        else: cols.append('#888888')
    ax.scatter(sx,sy,s=35,c=cols,alpha=0.9,edgecolors='white',linewidths=0.4,zorder=5)
    pax=ax.inset_axes([0.5,0.02,0.46,0.10])
    pax.set_xlim(0,400); pax.set_ylim(0,1.05)
    pax.set_title('S → E (Istidraj)',color='white',fontsize=7)
    pax.tick_params(colors='white',labelsize=4); pax.grid(True,alpha=0.12)
    if list(pS): pax.plot(list(px),list(pS),color='#FFD700',lw=2); pax.plot(list(px),list(pE),color='#0FF',lw=1.5)
    ax.text(14,1.2,f'{ph} | S={S:.2f} | E={E:.2f}',color='white',fontsize=12,ha='center',fontweight='bold')
    plt.tight_layout(pad=0)
    buf=BytesIO(); fig.savefig(buf,format='png',dpi=100,facecolor='#000010'); buf.seek(0)
    st.session_state.latest_image=buf
    plt.close(fig)

# =============================================
# التشغيل
# =============================================
if st.session_state.get("run", False):
    placeholder = st.empty()
    run_one_frame()
    if 'latest_image' in st.session_state:
        placeholder.image(st.session_state.latest_image, use_column_width=True)
    st.caption(f"{st.session_state.ph} | S={st.session_state.S:.2f} | E={st.session_state.E:.2f}")
    time.sleep(0.08)
    st.rerun()
elif st.session_state.init and 'latest_image' in st.session_state:
    st.image(st.session_state.latest_image, caption=TXT("آخر حالة","Last state"), use_column_width=True)

# =============================================
# تحميل
# =============================================
if 'latest_image' in st.session_state:
    st.sidebar.download_button(TXT("📥 تحميل الصورة","📥 Download Image"),
                               st.session_state.latest_image, "mizan.png", "image/png")

st.markdown("---")
st.markdown(f"*{TXT('المنصة الذهبية – الإصدار النهائي','The Golden Platform – Final Edition')} | علي عادل العاطفي | 2026*")
