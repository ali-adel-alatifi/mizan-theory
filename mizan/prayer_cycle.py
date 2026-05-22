# mizan/prayer_cycle.py
"""
دورة الصلاة والميزان – الاستعانة بالصلاة في الدورة الإلهية
وسر سورة الماعون: اختبار صدق العبادة
"""

import streamlit as st
from config import TXT

# =============================================
# دالة إصلاح النصوص العربية
# =============================================
def fix_rtl_display():
    """إصلاح مشكلة عرض النصوص العربية في Streamlit"""
    st.markdown("""
    <style>
    /* إجبار كل النصوص على أن تكون من اليمين لليسار */
    div, p, h1, h2, h3, h4, h5, h6, span, strong, em, li, label, .stMarkdown, .stText {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: plaintext !important;
    }
    /* العناوين الرئيسية */
    .stTitle, .stHeader, .stSubheader {
        direction: rtl !important;
        text-align: right !important;
    }
    /* صناديق المعلومات */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        direction: rtl !important;
        text-align: right !important;
    }
    /* الأزرار والمنزلقات */
    button, .stSlider {
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_prayer_cycle():
    # === تطبيق الحل أولاً ===
    fix_rtl_display()
    
    st.header(TXT("🕌 دورة الصلاة والميزان", "🕌 The Prayer & Mizan Cycle"))
    
    # ─────────────────────────────────────────
    # ١. المحطات الخمس للاستعانة بالصلاة
    # ─────────────────────────────────────────
    st.subheader(TXT("محطات الاستعانة بالصلاة في القرآن", "Stations of Seeking Help through Prayer in the Quran"))
    
    st.markdown(TXT(
        """
        الصلاة ليست مجرد عبادة، بل هي **محور الدورة الإلهية** و**الناظم الذي يربط كل مراحلها**. 
        لقد وردت "الاستعانة بالصلاة" في خمسة مواضع قرآنية، كل واحد منها يمثل مرحلة من مراحل بناء الفرد والأمة.
        """,
        """
        Prayer is not just an act of worship, but the **axis of the divine cycle** and **the thread connecting all its stages**.
        "Seeking help through prayer" appears in five Quranic contexts, each representing a stage in building the individual and the nation.
        """
    ))
    
    stations = [
        {
            "verse": "لقمان: ١٧",
            "text": "﴿يَا بُنَيَّ أَقِمِ الصَّلَاةَ وَأْمُرْ بِالْمَعْرُوفِ وَانْهَ عَنِ الْمُنكَرِ وَاصْبِرْ عَلَىٰ مَا أَصَابَكَ﴾",
            "stage": TXT("المرحلة ١: الفطرة والتأسيس", "Stage 1: Innate Nature & Foundation"),
            "role": TXT("الصلاة هنا: **حارسة الفطرة**. تُزرع في النشء لتحمي الفطرة السليمة من الانحراف. "
                        "هذه مرحلة **بناء الفرد** قبل المواجهة المجتمعية.",
                        "Prayer here: **Guardian of innate nature**. Planted in the young to protect pure nature from deviation. "
                        "This is the stage of **individual building** before societal confrontation."),
            "w": 0.7, "b": 0.3, "s": 0.21,
        },
        {
            "verse": "طه: ١٣٢",
            "text": "﴿وَأْمُرْ أَهْلَكَ بِالصَّلَاةِ وَاصْطَبِرْ عَلَيْهَا لَا نَسْأَلُكَ رِزْقًا نَّحْنُ نَرْزُقُكَ﴾",
            "stage": TXT("المرحلة ٢: الوحي والبيان", "Stage 2: Revelation & Clarification"),
            "role": TXT("الصلاة هنا: **متلقية الوحي**. أمر للنبي ﷺ بتعليم أهله، إعداداً للدعوة والمواجهة. "
                        "هذه مرحلة **تأسيس الأسرة** ونواة الجماعة.",
                        "Prayer here: **Receiver of revelation**. A command to the Prophet ﷺ to teach his family, preparing for the call and confrontation. "
                        "This is the stage of **family foundation** and the nucleus of the community."),
            "w": 0.8, "b": 0.5, "s": 0.40,
        },
        {
            "verse": "البقرة: ٤٥",
            "text": "﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ وَإِنَّهَا لَكَبِيرَةٌ إِلَّا عَلَى الْخَاشِعِينَ﴾",
            "stage": TXT("المرحلة ٣: التأسيس الفردي", "Stage 3: Individual Foundation"),
            "role": TXT("الصلاة هنا: **مثبتة العروة الوثقى**. تأسيس للفرد المؤمن على الثبات في وجه الابتلاءات. "
                        "هذه مرحلة **بناء المناعة الفردية**.",
                        "Prayer here: **Establisher of the firm handhold**. Grounding the believing individual in steadfastness in the face of trials. "
                        "This is the stage of **building individual immunity**."),
            "w": 0.85, "b": 0.7, "s": 0.60,
        },
        {
            "verse": "البقرة: ١٥٣",
            "text": "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾",
            "stage": TXT("المرحلة ٤: التكتل الجماعي", "Stage 4: Collective Solidarity"),
            "role": TXT("الصلاة هنا: **موحدة الجماعة**. نداء جماعي للمؤمنين، في سياق الجهاد والتضحية. "
                        "هذه مرحلة **بناء حبل الله** والتماسك الجماعي.",
                        "Prayer here: **Unifier of the community**. A collective call to believers, in the context of jihad and sacrifice. "
                        "This is the stage of **building the rope of Allah** and collective cohesion."),
            "w": 0.9, "b": 0.9, "s": 0.81,
        },
        {
            "verse": "البقرة: ٢٣٨",
            "text": "﴿حَافِظُوا عَلَى الصَّلَوَاتِ وَالصَّلَاةِ الْوُسْطَىٰ وَقُومُوا لِلَّهِ قَانِتِينَ﴾",
            "stage": TXT("المرحلة ٥: الاستخلاف والتمكين", "Stage 5: Vicegerency & Empowerment"),
            "role": TXT("الصلاة هنا: **ضمانة الاستمرار**. بعد النصر والتمكين، يأتي الأمر بالمحافظة لئلا تفسد النعمة. "
                        "هذه مرحلة **بناء الدولة والحضارة**.",
                        "Prayer here: **Guarantee of continuity**. After victory and empowerment, the command to preserve comes so that the blessing is not corrupted. "
                        "This is the stage of **building the state and civilization**."),
            "w": 0.95, "b": 0.95, "s": 0.90,
        },
    ]
    
    for stn in stations:
        with st.expander(f"**{stn['stage']}** ({stn['verse']})"):
            st.markdown(stn["text"])
            st.info(stn["role"])
            c1, c2, c3 = st.columns(3)
            c1.metric("W (الولاء)", f"{stn['w']:.2f}")
            c2.metric("B (البراءة)", f"{stn['b']:.2f}")
            c3.metric("S (الثبات)", f"{stn['s']:.2f}")

    # ─────────────────────────────────────────
    # ٢. سر سورة الماعون – اختبار صدق العبادة
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("⚡ سر سورة الماعون – اختبار صدق العبادة", "⚡ The Secret of Surat Al-Ma'un – Testing Worship Sincerity"))
    
    st.markdown(TXT(
        """
        ### ﴿أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ﴾ [الماعون: ١]
        
        **"الدين"** هنا هو **قانون السببية** (الدين القيم) و**يوم الجزاء** (يوم الدين). 
        والتكذيب به يعني **إنكار أن للأعمال نتائج**. وهذا هو أصل كل فساد.
        
        ثم يكشف الله العلامة العملية لهذا التكذيب:
        
        > ﴿فَذَٰلِكَ الَّذِي يَدُعُّ الْيَتِيمَ * وَلَا يَحُضُّ عَلَىٰ طَعَامِ الْمِسْكِينِ﴾ [الماعون: ٢-٣]
        
        فهو **قاسٍ على الضعيف** (يدع اليتيم) و**بخيل على المحتاج** (لا يحض على طعام المسكين).
        لماذا؟ لأنه كذب بالدين، فلم يعد يخشى عاقبة ظلمه، ولم يعد يرجو ثواب إحسانه.
        
        ثم تأتي المفاجأة الكبرى:
        
        > ﴿فَوَيْلٌ لِّلْمُصَلِّينَ * الَّذِينَ هُمْ عَن صَلَاتِهِمْ سَاهُونَ * الَّذِينَ هُمْ يُرَاءُونَ * وَيَمْنَعُونَ الْمَاعُونَ﴾ [الماعون: ٤-٧]
        
        لم يقل "فويل للكافرين" أو "فويل لمن لا يصلي"، بل قال: **"فويل للمصلين"**!
        
        **السر:** صلاتهم لم تثمر. صلاتهم لم تولد طاقة كافية لتغيير سلوكهم. لماذا؟
        - لأنهم **ساهون** عن الصلاة: ضعف في **الولاء (W)**.
        - ولأنهم **يراؤون**: اختلال في **البراءة (B)** (فبدلاً من البراءة من طلب رضا الناس، صاروا يطلبون رضاهم بعبادتهم).
        
        **النتيجة الحتمية:** ﴿وَيَمْنَعُونَ الْمَاعُونَ﴾. الماعون هو الشيء اليسير الذي يتعاوره الناس. 
        ومنعه هو **العلامة النهائية** على أن المعادلة مختلة: **S = 0**.
        
        **المعادلة في سورة الماعون:**
        > **W (صلاة بلا سهو) × B (إخلاص بلا رياء) = S (رحمة وعطاء)**
        > **W (صلاة مع سهو) × B (رياء) = 0 (ويل ومنع للماعون)**
        
        وحتى لو سقطت فريضة الزكاة عن إنسان لعدم بلوغه النصاب، فإن الله لم يتوقف عند هذا الحد، 
        بل أشار إلى **"الماعون"** – أبسط ما يملكه الإنسان – ليكشف **النوايا الباطلة**. 
        فمن لم يبذل حتى هذا اليسير، فقد كذب بالدين حقاً.
        """,
        """
        ### ﴿Have you seen the one who denies the Recompense?﴾ [Al-Ma'un: 1]
        
        **"Ad-Deen"** here is **the law of causality** (Al-Deen Al-Qayyim) and **the Day of Judgment** (Yawm Ad-Deen).
        Denying it means **denying that deeds have consequences**. This is the root of all corruption.
        
        Then comes the great surprise:
        
        > ﴿So woe to those who pray * who are heedless of their prayer * who make show [of their deeds] * and withhold [simple] assistance.﴾ [Al-Ma'un: 4-7]
        
        He did not say "woe to the disbelievers" or "woe to those who don't pray", but **"woe to those who pray"**!
        
        **The secret:** Their prayer did not bear fruit. Why?
        - Because they are **heedless** of prayer: weakness in **loyalty (W)**.
        - And because they **show off**: imbalance in **disavowal (B)**.
        
        **The inevitable result:** They withhold **Al-Ma'un** – the simplest things people share.
        This is the final sign that the equation is broken: **S = 0**.
        
        **The equation in Surat Al-Ma'un:**
        > **W (prayer without heedlessness) × B (sincerity without showing off) = S (mercy and giving)**
        > **W (prayer with heedlessness) × B (showing off) = 0 (woe and withholding)**
        
        Even if Zakat is not obligatory on someone due to not reaching the threshold, Allah did not stop there,
        but pointed to **"Al-Ma'un"** – the simplest things one owns – to expose **false intentions**.
        Whoever does not even give this little, has truly denied the Deen.
        """
    ))

    # ─────────────────────────────────────────
    # ٣. خلاصة
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("💎 الخلاصة", "💎 Summary"))
    st.markdown(TXT(
        """
        الصلاة هي **محور الدورة الإلهية**:
        
        - **لقمان ١٧:** الصلاة حارسة الفطرة (بناء الفرد).
        - **طه ١٣٢:** الصلاة متلقية الوحي (بناء الأسرة).
        - **البقرة ٤٥:** الصلاة مثبتة العروة الوثقى (بناء المناعة).
        - **البقرة ١٥٣:** الصلاة موحدة الجماعة (بناء حبل الله).
        - **البقرة ٢٣٨:** الصلاة ضمانة الاستمرار (بناء الحضارة).
        
        و**سورة الماعون** هي المختبر: صلاتك = زكاتك + ماعونك. فإن لم تثمر الصلاة رحمةً وعطاءً، 
        فراجع معادلة ولائك وبراءتك.
        
        **S = W × B**
        """,
        """
        Prayer is the **axis of the divine cycle**:
        
        - **Luqman 17:** Prayer guards innate nature (building the individual).
        - **Ta-Ha 132:** Prayer receives revelation (building the family).
        - **Al-Baqarah 45:** Prayer establishes the firm handhold (building immunity).
        - **Al-Baqarah 153:** Prayer unites the community (building the rope of Allah).
        - **Al-Baqarah 238:** Prayer guarantees continuity (building civilization).
        
        And **Surat Al-Ma'un** is the test: Your prayer = your charity + your assistance. 
        If prayer does not bear fruit in mercy and giving, review your equation of loyalty and disavowal.
        
        **S = W × B**
        """
    ))
