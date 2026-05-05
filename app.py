import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import random, time
from io import BytesIO
from collections import deque
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="الدين القيم – المختبر القرآني", page_icon="⚖️", layout="wide", initial_sidebar_state="auto")

# =============================================
# 🎨 CSS
# =============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(160deg, #0a0a2e 0%, #0d0d28 30%, #0f0f1a 100%); }
    .big-title { font-size: 2.5em; font-weight: 900; color: #FFD700; text-align: center; margin: 10px 0 0 0; }
    .sub-title { font-size: 1.1em; color: #CCCCCC; text-align: center; margin: 0 0 20px 0; }
    .stButton > button { border: 1px solid #FFD700; color: #FFD700; background: #1a1a3e; border-radius: 8px; height: 2.5em; }
    .metric-box { background: rgba(10,10,46,0.8); border-radius: 10px; padding: 8px 5px; text-align: center; border: 1px solid rgba(218,165,32,0.3); }
    .metric-val { font-size: 1.6em; font-weight: bold; margin: 0; }
    .metric-lbl { font-size: 0.7em; color: #aaa; margin: 0; }
    [data-testid="stExpander"] details { background: rgba(10,10,40,0.5); border: 1px solid rgba(218,165,32,0.3); border-radius: 8px; }
    [data-testid="stExpander"] summary { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================
# 🏛️ العنوان الرئيسي
# =============================================
st.markdown('<p class="big-title">⚖️ الدِّينُ الْقَيِّم ⚖️</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">المختبر القرآني – نظرية الميزان | S = W × B</p>', unsafe_allow_html=True)
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi")

# =============================================
# 📑 ألسنة التبويب الرئيسية
# =============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌌 المختبر الحي", 
    "🧭 البوصلة الكونية",
    "📖 كتاب الميزان", 
    "📜 رسالة الترحيب", 
    "📋 الدليل المرجعي"
])

# =============================================
# 🌌 تبويب المختبر الحي
# =============================================
with tab1:
    # --- دوال المحاكاة ---
    def get_color(w, b):
        if w >= 0.6 and b >= 0.6: return '#FFD700'
        elif w >= 0.6 and b < 0.4: return '#FFFFFF'
        elif w < 0.4 and b >= 0.6: return '#FF3333'
        elif w < 0.4 and b < 0.4: return '#FFB6C1'
        else:
            if w > b: return '#FFF8DC'
            elif b > w: return '#FFA07A'
            else: return '#FFBF00'

    def calc_S(W, B, E, p, z, f, h, amr, nahy, adl, shura, riba, ghish, kadhib):
        Sb = W * B
        pillars = (p + z + f + h) / 4
        Sb *= (0.5 + 0.5 * pillars)
        prot = (amr * W + nahy * B) / 2
        Sb *= (0.8 + 0.4 * prot) * (0.9 + 0.2 * adl) * (0.85 + 0.3 * shura)
        if E > Sb: Sb -= riba * (E - Sb) * 0.3
        return np.clip(Sb, 0.001, 1.0)

    # --- الشريط الجانبي للإعدادات ---
    with st.sidebar:
        st.header("🎛️ لوحة التحكم")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("▶️", use_container_width=True): st.session_state.run = True
        with c2:
            if st.button("⏹️", use_container_width=True): st.session_state.run = False
        with c3:
            if st.button("🔄", use_container_width=True):
                for k in list(st.session_state.keys()): del st.session_state[k]
                st.rerun()
        with c4:
            if st.button("🧹", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                for k in list(st.session_state.keys()): del st.session_state[k]
                st.rerun()

        st.divider()

        with st.expander("🕌 أركان الإسلام", expanded=False):
            prayer = st.slider("الصلاة", 0.0, 1.0, 0.8, 0.01, key="p")
            zakat = st.slider("الزكاة", 0.0, 1.0, 0.6, 0.01, key="z")
            fasting = st.slider("الصوم", 0.0, 1.0, 0.7, 0.01, key="f")
            hajj = st.slider("الحج", 0.0, 1.0, 0.5, 0.01, key="h")

        with st.expander("🏛️ أسس الحكم (بناء الدولة)", expanded=False):
            taalim = st.slider("تعليم يجمع بين العلم والدين", 0.0, 1.0, 0.5, 0.01, key="taalim")
            iqtisad = st.slider("اقتصاد إسلامي", 0.0, 1.0, 0.5, 0.01, key="iqtisad")
            iilam = st.slider("إعلام هادف", 0.0, 1.0, 0.5, 0.01, key="iilam")
            iktifaa = st.slider("اكتفاء ذاتي", 0.0, 1.0, 0.5, 0.01, key="iktifaa")
            musharaka = st.slider("إشراك المجتمع في المسؤولية", 0.0, 1.0, 0.5, 0.01, key="musharaka")
            adl = st.slider("العدل", 0.0, 1.0, 0.6, 0.01, key="adl")
            shura = st.slider("الشورى", 0.0, 1.0, 0.5, 0.01, key="shura")

        with st.expander("🛡️ آليات الإصلاح (حماية المجتمع)", expanded=False):
            amr_marouf = st.slider("الأمر بالمعروف", 0.0, 1.0, 0.5, 0.01, key="amr")
            nahy_munkar = st.slider("النهي عن المنكر", 0.0, 1.0, 0.5, 0.01, key="nahy")
            taawun_birr = st.slider("التعاون على البر", 0.0, 1.0, 0.5, 0.01, key="tb")
            taawun_taqwa = st.slider("التعاون على التقوى", 0.0, 1.0, 0.5, 0.01, key="tt")
            tawasi_haqq = st.slider("التواصي بالحق", 0.0, 1.0, 0.5, 0.01, key="th")
            tawasi_sabr = st.slider("التواصي بالصبر", 0.0, 1.0, 0.5, 0.01, key="ts")
            infaq = st.slider("الإنفاق في سبيل الله", 0.0, 1.0, 0.5, 0.01, key="infaq")
            jihad = st.slider("الجهاد بكل أشكاله", 0.0, 1.0, 0.5, 0.01, key="jihad")

        with st.expander("💀 آليات الإفساد (أدوات الهدم)", expanded=False):
            nahy_marouf_e = st.slider("النهي عن المعروف", 0.0, 1.0, 0.2, 0.01, key="nm")
            amr_munkar_e = st.slider("الأمر بالمنكر", 0.0, 1.0, 0.2, 0.01, key="amr_e")
            taawun_ithm = st.slider("التعاون على الإثم", 0.0, 1.0, 0.2, 0.01, key="ti")
            taawun_udwan = st.slider("التعاون على العدوان", 0.0, 1.0, 0.2, 0.01, key="tu")
            tawasi_batil = st.slider("التواصي بالباطل", 0.0, 1.0, 0.2, 0.01, key="tbat")
            adam_sabr = st.slider("التواكل وعدم الصبر", 0.0, 1.0, 0.2, 0.01, key="as")
            bukhl = st.slider("البخل والشح", 0.0, 1.0, 0.2, 0.01, key="bukhl")

        with st.expander("⚠️ الأمراض الأخلاقية", expanded=False):
            riba = st.slider("الربا", 0.0, 1.0, 0.2, 0.01, key="riba")
            ghish = st.slider("الغش", 0.0, 1.0, 0.2, 0.01, key="ghish")
            kadhib = st.slider("الكذب", 0.0, 1.0, 0.2, 0.01, key="kadhib")

        with st.expander("⚙️ إعدادات المحاكاة", expanded=True):
            cycle_speed = st.slider("سرعة الدورة", 0.001, 0.05, 0.008, 0.001, key="spd")
            delay_frames = st.slider("تأخير التمكين", 5, 50, 22, 1, key="dly")
            N_STARS = st.slider("عدد النجوم", 50, 300, 150, 10, key="nst")

    # --- تهيئة المحاكاة ---
    if 'run' not in st.session_state: st.session_state.run = False
    if 'init' not in st.session_state: st.session_state.init = False

    if not st.session_state.init:
        np.random.seed(42); random.seed(42)
        n = N_STARS if 'N_STARS' in locals() else 150
        cx, cy = 14, 10.0
        st.session_state.cx = cx; st.session_state.cy = cy
        st.session_state.sx = np.random.uniform(cx-13, cx+13, n)
        st.session_state.sy = np.random.uniform(cy-9, cy+9, n)
        st.session_state.sw = np.random.uniform(0.1, 1.0, n)
        st.session_state.sb = np.random.uniform(0.1, 1.0, n)
        st.session_state.W = 0.55; st.session_state.B = 0.52
        st.session_state.E = 0.3; st.session_state.S = 0.286
        st.session_state.ph = "استقرار"; st.session_state.ca = 0.0
        st.session_state.aW = 0.0; st.session_state.aB = np.pi * 0.5; st.session_state.aa = 0.0
        st.session_state.eb = deque([0.286]*30, maxlen=30)
        st.session_state.pS = deque(maxlen=400); st.session_state.pE = deque(maxlen=400)
        st.session_state.px = deque(maxlen=400); st.session_state.pc = 0
        st.session_state.hasanat = 10.0; st.session_state.sayyiat = 5.0
        st.session_state.init = True

    # --- مؤشرات ---
    if st.session_state.init:
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFD700;">{st.session_state.S:.3f}</p><p class="metric-lbl">⚖️ S</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FFF;">{st.session_state.W:.3f}</p><p class="metric-lbl">🤍 W</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#FF5252;">{st.session_state.B:.3f}</p><p class="metric-lbl">❤️ B</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:#00FFFF;">{st.session_state.E:.3f}</p><p class="metric-lbl">💫 E</p></div>', unsafe_allow_html=True)
        with m5:
            mizan_akhira = st.session_state.hasanat - st.session_state.sayyiat
            color = "#FFD700" if mizan_akhira >= 0 else "#FF3333"
            st.markdown(f'<div class="metric-box"><p class="metric-val" style="color:{color};">{mizan_akhira:.3f}</p><p class="metric-lbl">📜 الميزان الأخروي</p></div>', unsafe_allow_html=True)

    plot_placeholder = st.empty()

    # --- المحاكاة الحية ---
    if st.session_state.get("run", False):
        while st.session_state.run:
            try:
                W = st.session_state.W; B = st.session_state.B; E = st.session_state.E; S = st.session_state.S
                ph = st.session_state.ph; ca = st.session_state.ca
                aW = st.session_state.aW; aB = st.session_state.aB; aa = st.session_state.aa
                sx = st.session_state.sx.copy(); sy = st.session_state.sy.copy()
                sw = st.session_state.sw.copy(); sb = st.session_state.sb.copy()
                cx, cy = st.session_state.cx, st.session_state.cy
                eb = st.session_state.eb; pS = st.session_state.pS; pE = st.session_state.pE; px = st.session_state.px

                ca += cycle_speed; sv = np.sin(ca)
                target_S = 0.5 + 0.45 * sv
                if sv > 0.5: ph = 'Peak Stability'
                elif sv > 0: ph = 'Rising'
                elif sv > -0.5: ph = 'Collapsing'
                else: ph = 'Rock Bottom'
                if 0.3 < sv < 0.35: ph = '>> Istidraj <<'

                n = len(sw)
                for i in range(n):
                    wb = prayer * 0.01; bb = fasting * 0.01
                    dist = np.sqrt((sx[i] - sx)**2 + (sy[i] - sy)**2)
                    close = (dist < 2.0) & (np.arange(n) != i)
                    
                    w_gov = (taalim + iqtisad + iilam + iktifaa + musharaka + adl + shura) / 7
                    sw[i] += w_gov * 0.02
                    
                    b_ref = (amr_marouf + nahy_munkar + taawun_birr + taawun_taqwa + tawasi_haqq + tawasi_sabr + infaq + jihad) / 8
                    sb[i] += b_ref * 0.02
                    
                    e_fasad = (nahy_marouf_e + amr_munkar_e + taawun_ithm + taawun_udwan + tawasi_batil + adam_sabr + bukhl) / 7
                    sw[i] -= e_fasad * 0.015
                    sb[i] -= e_fasad * 0.015
                    
                    sw[i] += (target_S - sw[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + wb
                    sb[i] += (target_S - sb[i]) * 0.02 + np.random.uniform(-0.02, 0.02) + bb
                    
                    if np.any(close):
                        sw[i] += (np.mean(sw[close]) - sw[i]) * 0.03 * (0.5 + 0.5 * shura)
                        sb[i] += (np.mean(sb[close]) - sb[i]) * 0.03 * (0.5 + 0.5 * shura)
                    
                    sw[i] = np.clip(sw[i], 0.01, 1.0); sb[i] = np.clip(sb[i], 0.01, 1.0)

                shock_p = 0.005 * (1 - adl * 0.8)
                if random.random() < shock_p:
                    aff = np.random.choice(n, size=int(n * 0.3), replace=False)
                    sw[aff] *= np.random.uniform(0.5, 0.8); sb[aff] *= np.random.uniform(0.5, 0.8)

                avgW = np.mean(sw); avgB = np.mean(sb)
                W += (avgW - W) * 0.04; B += (avgB - B) * 0.04
                W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
                S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr_marouf, nahy_munkar, adl, shura, riba, ghish, kadhib)
                eb.append(S)
                if len(eb) > 30: eb.pop(0)
                E_target = eb[-delay_frames] if len(eb) >= delay_frames else S
                E += 0.03 * (E_target - E)
                W = W - 0.01 * E + 0.02 / (S + 0.1)
                B = B - 0.008 * E + 0.005 * (1 - B) * W * (1 - W)
                W, B = np.clip(W, 0.01, 1.0), np.clip(B, 0.01, 1.0)
                S = calc_S(W, B, E, prayer, zakat, fasting, hajj, amr_marouf, nahy_munkar, adl, shura, riba, ghish, kadhib)
                pS.append(S); pE.append(E); px.append(len(px))
                if len(px) > 400: pS.popleft(); pE.popleft(); px.popleft()

                st.session_state.hasanat += np.mean(sw) * 0.1
                st.session_state.sayyiat += (1 - np.mean(sb)) * 0.1

                aW += 0.02 + random.uniform(-0.025, 0.025) * (1 - W)**2
                aB += 0.02 + random.uniform(-0.025, 0.025) * (1 - B)**2
                wx = cx + (7 - 2.5 * W) * np.cos(aW); wy = cy + (7 - 2.5 * W) * np.sin(aW) * 0.7
                bx = cx + (5 - 1.5 * B) * np.cos(aB); by = cy + (5 - 1.5 * B) * np.sin(aB) * 0.7
                ins = 1 - np.mean(sw * sb)
                sx += np.random.uniform(-0.07, 0.07, n) * ins; sy += np.random.uniform(-0.07, 0.07, n) * ins
                sx, sy = np.clip(sx, cx-13, cx+13), np.clip(sy, cy-9, cy+9)

                st.session_state.W, st.session_state.B = W, B
                st.session_state.E, st.session_state.S = E, S
                st.session_state.ph, st.session_state.ca = ph, ca
                st.session_state.aW, st.session_state.aB, st.session_state.aa = aW, aB, aa + 0.12
                st.session_state.eb = eb
                st.session_state.sx, st.session_state.sy = sx, sy
                st.session_state.sw, st.session_state.sb = sw, sb
                st.session_state.pS, st.session_state.pE, st.session_state.px = pS, pE, px

                fig, ax = plt.subplots(figsize=(12, 9), facecolor='#000010')
                ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
                for r, a, c in [(0.5,0.98,'#FFF'),(1,0.65,'#FFD700'),(1.7,0.3,'#FFD700'),(2.6,0.12,'#FFA500'),(3.8,0.05,'#FF6347'),(5.5,0.02,'#FF4500')]:
                    ax.add_patch(Circle((cx,cy), r*(0.5+2.8*S), color=c, alpha=a, zorder=15))
                ax.text(cx, cy, 'S', color='#1a1000', fontsize=18, ha='center', va='center', fontweight='bold')
                ax.add_patch(Circle((cx,cy), 0.5+14*E, color='#00FFFF', alpha=0.15, zorder=7))
                ax.add_patch(Circle((cx,cy), 8.5, color='#00FF88', alpha=0.15, fill=False, lw=2, zorder=2))
                colors = [get_color(sw[i], sb[i]) for i in range(n)]
                ax.scatter(sx, sy, s=40, c=colors, alpha=0.9, edgecolors='white', linewidths=0.3, zorder=5)
                ax.add_patch(Circle((wx,wy), 0.2+0.5*W, color='#FFF', alpha=1, zorder=13))
                ax.add_patch(Circle((bx,by), 0.2+0.5*B, color='#F33', alpha=0.8, zorder=13))
                ax.text(wx, wy-1.2, 'W', color='#FFF', fontsize=12, ha='center')
                ax.text(bx, by-1.2, 'B', color='#F33', fontsize=12, ha='center')
                pSl, pEl, pxl = list(pS), list(pE), list(px)
                if pSl:
                    pax = ax.inset_axes([0.3, 0.02, 0.65, 0.18])
                    pax.set_xlim(0, 400); pax.set_ylim(0, 1.05)
                    pax.set_title('📈 S (الذهب) يقود E (السماوي) — الاستدراج', color='white', fontsize=10, fontweight='bold')
                    pax.tick_params(colors='white', labelsize=7); pax.grid(True, alpha=0.3)
                    pax.plot(pxl, pSl, color='#FFD700', lw=2.5, label='S')
                    pax.plot(pxl, pEl, color='#00FFFF', lw=2, label='E')
                    pax.legend(facecolor='#000', edgecolor='white', labelcolor='white', fontsize=8)
                ax.text(14, 1.2, f'{ph} | S={S:.2f} | E={E:.2f}', color='white', fontsize=14, ha='center', fontweight='bold')
                plt.tight_layout(pad=0)
                plot_placeholder.pyplot(fig)
                buf = BytesIO()
                fig.savefig(buf, format='png', dpi=100, facecolor='#000010')
                buf.seek(0)
                st.session_state.latest_image = buf
                plt.close(fig)
                time.sleep(0.08)
            except Exception as e:
                st.error(str(e))
                st.session_state.run = False
                break
        st.success("⏸️ تم إيقاف المحاكاة")
    else:
        if st.session_state.init:
            fig, ax = plt.subplots(figsize=(6, 4), facecolor='#000010')
            ax.set_xlim(0, 28); ax.set_ylim(0, 20); ax.axis('off')
            colors = [get_color(st.session_state.sw[i], st.session_state.sb[i]) for i in range(len(st.session_state.sw))]
            ax.scatter(st.session_state.sx, st.session_state.sy, s=20, c=colors, alpha=0.9)
            ax.text(14, 10, '⚖️', fontsize=30, ha='center', va='center', color='#FFD700')
            plot_placeholder.pyplot(fig)
            plt.close(fig)

    if 'latest_image' in st.session_state:
        st.download_button("📥 تحميل صورة المشهد", st.session_state.latest_image, "mizan_scene.png", "image/png")

# =============================================
# 🧭 تبويب البوصلة الكونية
# =============================================
with tab2:
    st.header("🧭 البوصلة الكونية")
    st.subheader("اختبار الإحداثيات الوجودية – اكتشف موقعك في فضاء الولاء والبراء")

    if 'compass_answers' not in st.session_state:
        st.session_state.compass_answers = {}

    questions = {
        "L": [
            {"id": "L1", "q": "عندما أكون وحيداً، أفكاري تتجه نحو:", "a": [("الله وذكره", 3), ("أمور الدنيا والمستقبل المادي", 1), ("لا أفكر في شيء محدد", 0), ("أفكار سلبية ومتشائمة", -1)]},
            {"id": "L2", "q": "شعوري تجاه الله هو:", "a": [("محبة وخوف ورجاء", 3), ("خوف من العقاب فقط", 1), ("لا أشعر بشيء خاص", 0), ("مشاعر سلبية أو رفض", -1)]},
            {"id": "L3", "q": "قراراتي الكبرى في الحياة تتخذ بناءً على:", "a": [("ما يرضي الله أولاً", 3), ("ما ينفعني مادياً", 1), ("حسب الموقف", 0), ("ما يشبع رغباتي", -1)]},
            {"id": "L4", "q": "أولويتي عند تعارض المصالح:", "a": [("رضا الله فوق كل شيء", 3), ("مصلحتي الشخصية", 1), ("أبحث عن حل وسط", 0), ("مصلحتي أولاً ولو بمعصية", -1)]},
            {"id": "L5", "q": "علاقاتي مع الآخرين تقوم على:", "a": [("مرضاة الله وخدمة الخلق", 3), ("المصالح المتبادلة", 1), ("العاطفة والمزاج", 0), ("الاستغلال والمنفعة", -1)]},
            {"id": "L6", "q": "انتمائي الحقيقي هو لـ:", "a": [("الله ودينه وأمته", 3), ("بلدي وعائلتي فقط", 1), ("نفسي ومصالحي", 0), ("لا أنتمي لأحد", -1)]},
        ],
        "D": [
            {"id": "D1", "q": "مشاعري تجاه المعاصي:", "a": [("كراهية وبغض", 3), ("خوف من العواقب فقط", 1), ("لا مشاعر خاصة", 0), ("رغبة وميل", -1)]},
            {"id": "D2", "q": "عند رؤية المنكر أشعر بـ:", "a": [("حزن ورغبة في التغيير", 3), ("ازعاج فقط", 1), ("لا شيء", 0), ("متعة أو تقبل", -1)]},
            {"id": "D3", "q": "تعاملي مع المحرمات:", "a": [("أتجنبها تماماً", 3), ("أتجنب الكبائر فقط", 1), ("أحياناً أقع فيها", 0), ("أمارسها عمداً", -1)]},
            {"id": "D4", "q": "عندما أخطئ:", "a": [("أتوب فوراً وأتدارك", 3), ("أتوب إذا تذكرت", 1), ("لا أبالي", 0), ("أستمتع وأكرر", -1)]},
            {"id": "D5", "q": "في تعاملي مع الظالمين:", "a": [("أبرأ منهم ولا أعاونهم", 3), ("أتعامل لمصلحتي فقط", 1), ("أتعامل طالما لم يضروني", 0), ("أتعاون معهم", -1)]},
            {"id": "D6", "q": "موقفي من الأفكار المخالفة للدين:", "a": [("أرفضها وأحذر منها", 3), ("أتجاهلها", 1), ("أستمع لها بلا موقف", 0), ("أتقبلها وأعتنقها", -1)]},
        ]
    }

    st.markdown("### 📝 أجب عن الأسئلة التالية بصدق")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🤍 أسئلة الولاء (L)")
        for q in questions["L"]:
            ans = st.radio(f"**{q['q']}**", [a[0] for a in q['a']], key=q['id'], index=None)
            if ans:
                st.session_state.compass_answers[q['id']] = [a[1] for a in q['a'] if a[0] == ans][0]

    with col2:
        st.markdown("#### ❤️ أسئلة البراء (D)")
        for q in questions["D"]:
            ans = st.radio(f"**{q['q']}**", [a[0] for a in q['a']], key=q['id'], index=None)
            if ans:
                st.session_state.compass_answers[q['id']] = [a[1] for a in q['a'] if a[0] == ans][0]

    if len(st.session_state.compass_answers) == 12:
        L_score = sum([st.session_state.compass_answers[f"L{i}"] for i in range(1, 7)])
        D_score = sum([st.session_state.compass_answers[f"D{i}"] for i in range(1, 7)])
        
        L = L_score / 18
        D = D_score / 18

        if L > 0 and D > 0: quadrant = "Q1"
        elif L < 0 and D > 0: quadrant = "Q2"
        elif L < 0 and D < 0: quadrant = "Q3"
        elif L > 0 and D < 0: quadrant = "Q4"
        else: quadrant = "محايد"

        q_names = {"Q1": "المؤمن (الربع الأول)", "Q2": "الكافر (الربع الثاني)", "Q3": "المنافق (الربع الثالث)", "Q4": "المشرك (الربع الرابع)", "محايد": "منطقة محايدة"}
        q_colors = {"Q1": "#FFD700", "Q2": "#FF3333", "Q3": "#FFB6C1", "Q4": "#FFA07A", "محايد": "#888888"}
        q_advice = {
            "Q1": "أنت في الطريق الصحيح. حافظ على ثباتك، واستمر في النمو نحو (1,1).",
            "Q2": "ولاؤك لغير الله. أنت بحاجة إلى توبة جذرية وتحويل بوصلتك نحو الخالق.",
            "Q3": "أنت في حالة تذبذب خطيرة. أنت بحاجة إلى الصدق مع نفسك واتخاذ قرار حاسم.",
            "Q4": "لديك إيمان بالله لكنك تخلطه بشرك. أنت بحاجة إلى توحيد خالص لله."
        }

        st.divider()
        st.header("📊 نتائج اختبار البوصلة الكونية")

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f"""
            <div style="background: rgba(10,10,46,0.8); border-radius: 15px; padding: 20px; border: 2px solid {q_colors[quadrant]}; margin: 10px 0; text-align: center;">
                <p style="font-size: 2em; font-weight: bold; color: {q_colors[quadrant]};">{q_names[quadrant]}</p>
                <p>إحداثياتك: <b>L = {L:.2f}</b> | <b>D = {D:.2f}</b></p>
                <p>{q_advice[quadrant]}</p>
            </div>
            """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0a2e')
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axhline(0, color='grey', lw=0.5)
        ax.axvline(0, color='grey', lw=0.5)
        ax.set_xlabel("البراء (D)", color='white')
        ax.set_ylabel("الولاء (L)", color='white')

        ax.add_patch(Rectangle((0, 0), 1, 1, color='#FFD700', alpha=0.15))
        ax.add_patch(Rectangle((-1, 0), 1, 1, color='#FF3333', alpha=0.15))
        ax.add_patch(Rectangle((-1, -1), 1, 1, color='#FFB6C1', alpha=0.15))
        ax.add_patch(Rectangle((0, -1), 1, 1, color='#FFA07A', alpha=0.15))

        ax.text(0.5, 0.5, "مؤمن", color='white', ha='center', alpha=0.5)
        ax.text(-0.5, 0.5, "كافر", color='white', ha='center', alpha=0.5)
        ax.text(-0.5, -0.5, "منافق", color='white', ha='center', alpha=0.5)
        ax.text(0.5, -0.5, "مشرك", color='white', ha='center', alpha=0.5)
        
        ax.scatter(D, L, c='#00FFFF', s=200, edgecolors='white', linewidth=2, zorder=5)
        ax.tick_params(colors='white')
        st.pyplot(fig)

        if st.button("🔄 إعادة الاختبار"):
            st.session_state.compass_answers = {}
            st.rerun()

# =============================================
# 📖 تبويب كتاب الميزان
# =============================================
with tab3:
    st.header("📖 كتاب الميزان")
    st.subheader("المختبر القرآني – من الثنائية الكونية إلى معادلة الوجود")
    st.caption("تأليف: علي عادل العاطفي | © 2026")
    st.divider()

    with st.expander("📜 الإهداء والمقدمة", expanded=False):
        st.markdown("""
        ### الإهداء
        إلى كل باحث عن الحقيقة، يبحث عن الخيط الناظم الذي يربط شتات هذا الوجود.
        إلى كل قلب حائر، يبحث عن الطمأنينة في زمن القلق.
        وإلى كل عقل متعطش، يريد أن يرى كيف يلتقي الوحي بالعلم.
        
        هذا الكتاب هو محاولة متواضعة لإعادة الأمور إلى نصابها، ولإثبات أن "الدين" ليس مجرد طقوس،
        بل هو "نظام التشغيل" الذي صممه الخالق لهذا الكون. إنه "الميزان" الذي وضعه الله.
        
        ### مقدمة المؤلف
        الحمد لله الذي رفع السماء ووضع الميزان...
        
        هذا كتاب "الميزان". يقدم "الدين القيم" (قانون السببية الأعظم) و"الإسلام الحنيف"
        (الاستجابة المثلى لهذا القانون) كمنظومة متكاملة تفسر الوجود من الذرة إلى الحضارة.
        
        المعادلة: **S = W × B**
        """)

    with st.expander("🔍 تمهيد: البحث عن نظرية كل شيء", expanded=False):
        st.markdown("منذ فجر الوعي، والبشرية تبحث عن إجابة لسؤال واحد... **S = W × B**.")

    with st.expander("الباب الأول: الأصول – من أين بدأنا؟", expanded=False):
        st.markdown("""
        **الفصل الأول:** ﴿اقْرَأْ بِاسْمِ رَبِّكَ﴾ – المنهج الإلهي.
        **الفصل الثاني:** ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾.
        **الفصل الثالث:** ﴿سَنُرِيهِمْ آيَاتِنَا﴾ – المنهج التجريبي.
        """)

    with st.expander("الباب الثاني: التعريفات المركزية", expanded=False):
        st.markdown("**الدين القيم** = قانون السببية الأعظم. **الإسلام الحنيف** = الاستجابة المثلى للقانون.")

    with st.expander("الباب الثالث: الثنائية الكونية", expanded=False):
        st.markdown("النور والظلام. الجذب والتنافر. النظام والفوضى.")

    with st.expander("الباب الرابع: وحدة الخلق والأمر", expanded=False):
        st.markdown("**﴿أَلَا لَهُ الْخَلْقُ وَالْأَمْرُ﴾** – القانون واحد في الذرة والخلية والتاريخ.")

    with st.expander("الباب الخامس: المختبر – تشغيل المحاكاة", expanded=False):
        st.markdown("**الحالات الأربع:** 🟡 ذهبي = مؤمن | ⚪ أبيض = راهب | 🔴 أحمر = كافر | 🩷 وردي = منافق.")

    with st.expander("الباب السادس: نحو الأمة الذهبية", expanded=False):
        st.markdown("بناء الفرد الذهبي. بناء الأسرة. بناء الجماعة. بناء المؤسسات.")

    with st.expander("الباب السابع: الفطرة – نظام التشغيل الأصلي", expanded=False):
        st.markdown("﴿أَلَسْتُ بِرَبِّكُمْ قَالُوا بَلَىٰ﴾ – أصل W.")

    with st.expander("الباب الثامن: التشخيص – واقع الأمة", expanded=False):
        st.markdown("W ضعيفة، B منهارة، S تقترب من الصفر. الانفصام الخماسي.")

    with st.expander("الباب التاسع: سبل العودة إلى القانون", expanded=False):
        st.markdown("الإصلاح الفردي (معرفي، قلبي، سلوكي). الإصلاح الأسري. الإصلاح المجتمعي.")

    with st.expander("الباب العاشر: اكتمال الدائرة", expanded=False):
        st.markdown("من الأزل إلى الخلود. الميثاق، الخلق، الشهادة، الميزان، دار القرار.")

# =============================================
# 📜 تبويب رسالة الترحيب
# =============================================
with tab4:
    st.header("📜 رسالة الترحيب")
    st.markdown("""
    <div style="text-align: center; font-size: 1.1em; line-height: 2; color: #CCCCCC;">
    > "هل يوجد قانون واحد يحكم الذرة والحضارة؟<br>
    > هذا هو نموذج الميزان الذي يثبت أن <b style="color: #FFD700;">S = W × B</b>"
    
    ---
    
    <b>الدين القيم</b> = قانون السببية الكوني، وهو الحق لأن واضعه الحق،
    وهو القيم لأنه من القيوم نفسه. هو القانون الأعظم، إنه "الدين القيم"
    الذي هو أصل الوجود وغايته.
    
    إنه <b>"الميزان"</b> الذي قامت به السماوات والأرض،
    والذي يدور حوله كل شيء، من الأزل إلى الخلود.
    
    ---
    
    ﴿وَالسَّمَاءَ رَفَعَهَا وَوَضَعَ الْمِيزَانَ﴾ — الرحمن 7
    
    ---
    
    <b>© 2026 علي عادل العاطفي | Ali Adel Alatifi</b>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# 📋 تبويب الدليل المرجعي
# =============================================
with tab5:
    st.header("📋 الدليل المرجعي")
    st.markdown("""
    **المشروع:** نظرية الميزان – المختبر القرآني
    **المؤلف:** علي عادل العاطفي (Ali Adel Alatifi)
    **الترخيص:** MIT License
    
    ---
    
    ### 📚 المكتبة الرسمية
    الكتب والوثائق الكاملة متوفرة في مستودع المكتبة:
    [github.com/ali-adel-alatifi/mizan-library](https://github.com/ali-adel-alatifi/mizan-library)
    """)

# =============================================
# 📥 تذييل
# =============================================
st.divider()
st.caption("© 2026 علي عادل العاطفي | Ali Adel Alatifi | Al-Deen Al-Qayyim – The Cosmic Balance Law")
