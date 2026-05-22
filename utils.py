# mizan/utils.py
"""
وحدة الأدوات المساعدة
تحتوي: تحليل الذكاء الاصطناعي، رسم الخرائط، الرسائل التحفيزية، حفظ/تحميل البيانات، تصدير التقارير
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from config import TXT, LETTERS_DB

# =============================================
# 1. أدوات الذكاء الاصطناعي
# =============================================

def get_openai_client():
    """
    محاولة الحصول على عميل OpenAI API بشكل آمن.
    ترجع العميل إذا كان متاحاً، أو None إذا لم يكن.
    """
    try:
        import openai
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if api_key:
            openai.api_key = api_key
            return openai
        return None
    except ImportError:
        return None
    except Exception:
        return None


def ai_analyze_compass(description, compass_data):
    """
    تحليل وصف المستخدم عبر الذكاء الاصطناعي لملء إجابات البوصلة.
    
    المعاملات:
        description: النص الوصفي من المستخدم
        compass_data: قائمة أسئلة البوصلة من config
    
    الإرجاع:
        قائمة بـ 19 قيمة (0-3) تمثل إجابات الأسئلة، أو None عند الفشل
    """
    client = get_openai_client()
    if not client:
        return None
    
    try:
        questions_desc = "\n".join([f"{q['id']}. {q['topic']}" for q in compass_data])
        prompt = f"""You are an expert in the Mizan theory. Analyze this person and return JSON with answers.
Questions:
{questions_desc}
Return ONLY valid JSON with format: {{"answers": [0, 2, 1, ...]}} (19 values, each 0-3).
Description: {description}"""
        
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
        
        ai_result = json.loads(content)
        return ai_result.get("answers", [])[:19]
    
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None


def ai_fill_sliders(description, indicators_meta):
    """
    تحليل وصف دولة/مجتمع عبر الذكاء الاصطناعي لملء المنزلقات.
    
    المعاملات:
        description: النص الوصفي
        indicators_meta: قائمة المؤشرات من config
    
    الإرجاع:
        قاموس يحتوي على values, W_pure, E_val, analysis، أو None عند الفشل
    """
    client = get_openai_client()
    if not client:
        return None
    
    try:
        from config import get_indicator_label
        n_ind = len(indicators_meta)
        indicators_desc = "\n".join([f"{i+1}. {get_indicator_label(i)}" for i in range(n_ind)])
        
        prompt = f"""You are an expert in the Mizan theory. Analyze the entity below and return JSON.
Indicators (each between -1 and +1):
{indicators_desc}
Also include: W_pure (bool), E_val (0-1), analysis (brief text).
Return ONLY valid JSON. Example: {{"values": [0.5, 0.4, ...], "W_pure": true, "E_val": 0.6, "analysis": "..."}}
Description: {description}"""
        
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
        
        return json.loads(content)
    
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None


# =============================================
# 2. دوال الرسم البياني
# =============================================

def plot_quadrant_map(B_raw, W_raw, istidraj_gap=0.0):
    """
    رسم خريطة الوجود الرباعية وموقع النقطة الحالية.
    """
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0a0f1e')
    ax.set_facecolor('#0a0f1e')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='grey', lw=0.5)
    ax.axvline(0, color='grey', lw=0.5)
    ax.set_xlabel(TXT("B (البراءة)", "B (Disavowal)"), color='white')
    ax.set_ylabel(TXT("W (الولاء)", "W (Faith)"), color='white')

    ax.fill_between([0, 1.2], 0, 1.2, color='#FFD700', alpha=0.3, label=TXT('المؤمنون', 'Believers'))
    ax.fill_between([-1.2, 0], 0, 1.2, color='#FF5252', alpha=0.2, label=TXT('المغضوب عليهم', 'Wrath'))
    ax.fill_between([-1.2, 0], -1.2, 0, color='#FFB6C1', alpha=0.2, label=TXT('المنافقون', 'Hypocrites'))
    ax.fill_between([0, 1.2], -1.2, 0, color='#FFA500', alpha=0.2, label=TXT('الضالون', 'Astray'))

    ax.scatter(B_raw, W_raw, s=300, c='cyan', edgecolors='white', linewidth=2, zorder=10)
    ax.scatter(1, 1, s=100, c='#FFD700', edgecolors='white', linewidth=2, zorder=10, marker='*')
    ax.text(1, 1.15, TXT('مقام إبراهيم', 'Abraham'), color='#FFD700', fontsize=8, ha='center')

    if istidraj_gap > 0:
        ax.text(0.5, -0.9, TXT(f"فجوة:{istidraj_gap:.2f}", f"Gap:{istidraj_gap:.2f}"),
                color='red', fontsize=9, ha='center', fontweight='bold')

    ax.legend(facecolor='#0a0f1e', edgecolor='white', labelcolor='white', fontsize=7, loc='lower left')
    ax.tick_params(colors='white')
    plt.tight_layout()
    return fig


# =============================================
# 3. الرسائل التحفيزية الروحية
# =============================================

ABRAHAMIC_VERSE = TXT(
    '﴿قَدْ كَانَتْ لَكُمْ أُسْوَةٌ حَسَنَةٌ فِي إِبْرَاهِيمَ وَالَّذِينَ مَعَهُ إِذْ قَالُوا لِقَوْمِهِمْ إِنَّا بُرَآءُ مِنكُمْ وَمِمَّا تَعْبُدُونَ مِن دُونِ اللَّهِ كَفَرْنَا بِكُمْ وَبَدَا بَيْنَنَا وَبَيْنَكُمُ الْعَدَاوَةُ وَالْبَغْضَاءُ أَبَدًا حَتَّىٰ تُؤْمِنُوا بِاللَّهِ وَحْدَهُ﴾',
    '﴿There has certainly been for you an excellent pattern in Abraham and those with him...﴾'
)

def get_spiritual_nudge(situation):
    """إرجاع رسالة تحفيزية حسب موقف المستخدم من مقام إبراهيم."""
    if situation == "approaching":
        return TXT(
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
        return TXT(
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
        return TXT(
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
        return TXT(
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
    return ""


# =============================================
# 4. تصدير التقارير
# =============================================

def generate_report(W_raw, B_raw, S_final, E_val, istidraj_gap, gate_name, gate_msg,
                    compass_data=None, answers_dict=None, slider_vals=None):
    """توليد تقرير نصي منسق بنتائج التحليل."""
    lines = []
    lines.append("=" * 60)
    lines.append(TXT("تقرير مختبر الميزان", "Mizan Lab Report"))
    lines.append("=" * 60)
    lines.append(f"W (الولاء): {W_raw:+.2f}")
    lines.append(f"B (البراءة): {B_raw:+.2f}")
    lines.append(f"S (الثبات): {S_final:.2f}")
    lines.append(f"E (التمكين): {E_val:.2f}")
    lines.append(f"فجوة الاستدراج: {istidraj_gap:.2f}")
    if gate_name:
        lines.append(f"البوابة: {gate_name}")
        lines.append(f"الحكم: {gate_msg}")
    
    if slider_vals:
        lines.append("-" * 40)
        lines.append("قيم المؤشرات:")
        from config import INDICATORS_META, get_indicator_label
        for i, val in enumerate(slider_vals):
            lines.append(f"  {get_indicator_label(i)}: {val:+.2f}")
    
    lines.append("-" * 40)
    lines.append(TXT("تم التوليد بواسطة مختبر الميزان", "Generated by Mizan Lab"))
    
    return "\n".join(lines)


# =============================================
# 5. حفظ وتحميل بيانات الجلسة (JSON)
# =============================================
def export_session_data(data_dict, filename_prefix="mizan_data"):
    """تحويل بيانات الجلسة إلى JSON وتوفير رابط تحميل."""
    json_str = json.dumps(data_dict, ensure_ascii=False, indent=2)
    st.download_button(
        label=TXT("💾 حفظ بياناتي", "💾 Save My Data"),
        data=json_str,
        file_name=f"{filename_prefix}.json",
        mime="application/json",
        use_container_width=True
    )

def import_session_data(keys_to_update):
    """رفع ملف JSON وتحديث مفاتيح الجلسة المحددة."""
    uploaded_file = st.file_uploader(
        TXT("اختر ملف JSON لاستعادة بياناتك", "Choose a JSON file to restore your data"),
        type=["json"]
    )
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            for key in keys_to_update:
                if key in data:
                    st.session_state[key] = data[key]
            st.success(TXT("✅ تم استعادة البيانات بنجاح!", "✅ Data restored successfully!"))
            st.rerun()
        except Exception as e:
            st.error(f"⚠️ خطأ في قراءة الملف: {e}")
