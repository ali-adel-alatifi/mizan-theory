# mizan/network.py
"""
شبكة الناجين - حبل الله الرقمي
يجمع المؤمنين على البر والتقوى، ويتيح التواصل والتآخي
"""

import streamlit as st
import pandas as pd
from config import TXT

def render_network():
    """عرض شبكة الناجين."""

    # --- تهيئة البيانات داخل الدالة (حل آمن من الاختفاء بعد إعادة الضبط) ---
    if "survivors_db" not in st.session_state:
        st.session_state.survivors_db = [
            {"name": "أبو عبد الله", "city": "مكة المكرمة", "country": "السعودية", "W": 0.85, "B": 0.80, "status": "مؤمن قوي"},
            {"name": "أم محمد", "city": "المدينة المنورة", "country": "السعودية", "W": 0.90, "B": 0.75, "status": "مؤمن قوي"},
            {"name": "عبد الرحمن", "city": "إسطنبول", "country": "تركيا", "W": 0.65, "B": 0.60, "status": "مؤمن"},
            {"name": "فاطمة الزهراء", "city": "القاهرة", "country": "مصر", "W": 0.70, "B": 0.55, "status": "مؤمن"},
            {"name": "أبو بكر", "city": "جاكرتا", "country": "إندونيسيا", "W": 0.80, "B": 0.70, "status": "مؤمن قوي"},
            {"name": "خالد", "city": "لندن", "country": "بريطانيا", "W": 0.55, "B": 0.65, "status": "مؤمن"},
            {"name": "عائشة", "city": "دبي", "country": "الإمارات", "W": 0.75, "B": 0.70, "status": "مؤمن قوي"},
            {"name": "محمد", "city": "نيويورك", "country": "أمريكا", "W": 0.45, "B": 0.60, "status": "مؤمن ضعيف"},
        ]

    if "forum_messages" not in st.session_state:
        st.session_state.forum_messages = [
            {"from": "أبو عبد الله", "msg": "السلام عليكم ورحمة الله وبركاته. ثبتنا الله وإياكم على الصراط المستقيم."},
            {"from": "أم محمد", "msg": "وعليكم السلام. من كان له ورد قرآن هذا الأسبوع؟"},
        ]

    st.header("🤝 شبكة الناجين – حبل الله الرقمي")
    st.markdown(TXT(
        "### ﴿وَاعْتَصِمُوا بِحَبْلِ اللَّهِ جَمِيعًا وَلَا تَفَرَّقُوا﴾",
        "### Hold firmly to the rope of Allah all together and do not become divided."
    ))
    st.caption(TXT(
        "هذه الشبكة تجمع أهل الثبات (S > 0.6). انضم إليهم، واجعل لك رفيقًا في طريق الصراط.",
        "This network gathers people of stability. Join them and find a companion on the path."
    ))

    net_tab1, net_tab2, net_tab3 = st.tabs([
        TXT("🗺️ خريطة الناجين", "🗺️ Survivors Map"),
        TXT("💬 المنتدى", "💬 Forum"),
        TXT("🔍 ابحث عن رفيق", "🔍 Find a Companion"),
    ])

    with net_tab1:
        st.subheader(TXT("🗺️ خريطة الناجين حول العالم", "🗺️ Survivors Map Worldwide"))
        df = pd.DataFrame(st.session_state.survivors_db)
        city_coords = {
            "مكة المكرمة": (21.42, 39.83), "المدينة المنورة": (24.47, 39.61),
            "إسطنبول": (41.01, 28.98), "القاهرة": (30.04, 31.24),
            "جاكرتا": (-6.21, 106.85), "لندن": (51.51, -0.13),
            "دبي": (25.20, 55.27), "نيويورك": (40.71, -74.01),
        }
        df["lat"] = df["city"].map(lambda c: city_coords.get(c, (0,0))[0])
        df["lon"] = df["city"].map(lambda c: city_coords.get(c, (0,0))[1])
        st.map(df[df["lat"] != 0], latitude="lat", longitude="lon", size=10)

        st.markdown("---")
        st.subheader(TXT("📋 سجل الناجين", "📋 Survivors Registry"))
        st.dataframe(
            df[["name", "city", "country", "status"]].rename(columns={
                "name": TXT("الاسم", "Name"), "city": TXT("المدينة", "City"),
                "country": TXT("البلد", "Country"), "status": TXT("الحالة", "Status")
            }),
            hide_index=True, use_container_width=True
        )

    with net_tab2:
        st.subheader(TXT("💬 منتدى الناجين", "💬 Survivors Forum"))
        st.caption(TXT("اكتب رسالة قصيرة لإخوانك في الشبكة.", "Write a short message to your brothers in the network."))
        for msg in st.session_state.forum_messages[-10:]:
            st.markdown(f"**{msg['from']}**: {msg['msg']}")
        with st.form("new_message", clear_on_submit=True):
            user_name = st.text_input(TXT("اسمك:", "Your name:"), placeholder=TXT("أبو فلان", "Abu Fulan"))
            user_msg = st.text_area(TXT("رسالتك:", "Your message:"), placeholder=TXT("اكتب رسالة...", "Write a message..."))
            if st.form_submit_button(TXT("📨 أرسل", "📨 Send")):
                if user_name and user_msg:
                    st.session_state.forum_messages.append({"from": user_name, "msg": user_msg})
                    st.rerun()

    with net_tab3:
        st.subheader(TXT("🔍 ابحث عن رفيق الصراط", "🔍 Find a Path Companion"))
        st.caption(TXT("أدخل مدينتك أو بلدك لتجد أقرب الناجين إليك.", "Enter your city or country to find survivors near you."))
        search_city = st.text_input(TXT("المدينة:", "City:"), placeholder=TXT("مثال: إسطنبول", "Example: Istanbul"))
        if search_city:
            df = pd.DataFrame(st.session_state.survivors_db)
            matches = df[df["city"].str.contains(search_city, case=False)]
            if not matches.empty:
                st.success(TXT(f"✅ وجدنا {len(matches)} من الناجين في {search_city}", f"✅ Found {len(matches)} survivors in {search_city}"))
                for _, row in matches.iterrows():
                    st.markdown(f"- **{row['name']}** ({row['status']})")
            else:
                st.warning(TXT("لم نجد ناجين في هذه المدينة بعد. كن أنت الأول!", "No survivors found yet. Be the first!"))

    st.markdown("---")
    st.subheader(TXT("🕋 انضم إلى الشبكة", "🕋 Join the Network"))
    with st.form("join_network", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input(TXT("اسمك:", "Your name:"), placeholder=TXT("أبو فلان", "Abu Fulan"))
        with col2:
            new_city = st.text_input(TXT("المدينة:", "City:"), placeholder=TXT("مكة المكرمة", "Mecca"))
        new_country = st.text_input(TXT("البلد:", "Country:"), placeholder=TXT("السعودية", "Saudi Arabia"))
        if st.form_submit_button(TXT("✅ انضم", "✅ Join")):
            if new_name and new_city and new_country:
                st.session_state.survivors_db.append({
                    "name": new_name, "city": new_city, "country": new_country,
                    "W": 0.6, "B": 0.6, "status": TXT("مؤمن جديد", "New Believer")
                })
                st.success(TXT("🎉 مرحباً بك في شبكة الناجين! أنت الآن جزء من حبل الله.", "🎉 Welcome to the Survivors Network! You are now part of Allah's rope."))
                st.rerun()
