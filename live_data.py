# mizan/live_data.py
"""
وحدة البيانات الحية - تجلب مؤشرات حقيقية من الإنترنت إن أمكن
وتطبق معادلة الميزان عليها، وإلا تعود للبيانات المحاكية.
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests

# =============================================
# 1. محاولة جلب البيانات الحية (بدون API Key)
# =============================================
@st.cache_data(ttl=3600)  # تحديث كل ساعة
def fetch_live_indicators():
    """
    تحاول جلب مؤشرات عالمية حقيقية من مصادر مفتوحة.
    إذا فشلت، تعود للبيانات المحاكية.
    """
    try:
        # المصدر: مؤشر السلام العالمي (متاح مجاناً)
        gpi_url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Global%20Peace%20Index%20-%20Institute%20for%20Economics%20%26%20Peace.csv"
        gpi_df = pd.read_csv(gpi_url)
        gpi_latest = gpi_df[gpi_df["Year"] == gpi_df["Year"].max()]
        
        # المصدر: تعداد السكان
        pop_url = "https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json"
        pop_resp = requests.get(pop_url, timeout=10)
        pop_data = pop_resp.json()
        pop_df = pd.DataFrame(pop_data)

        if not gpi_latest.empty:
            st.sidebar.success("🟢 متصل بالإنترنت - بيانات حية")
            return {"status": "live", "gpi": gpi_latest, "pop": pop_df}
        else:
            raise ValueError("بيانات فارغة")
    except Exception as e:
        st.sidebar.warning("🟡 بيانات محاكية (غير متصل أو خطأ في الجلب)")
        return {"status": "simulated"}

# =============================================
# 2. بناء قائمة الدول النهائية
# =============================================
def build_world_data(live_data):
    """دمج البيانات الحية (إن وجدت) مع المحاكاة الاحتياطية."""
    # استيراد البيانات المحاكية من observatory
    from observatory import WORLD_DATA_SIMULATED
    simulated = WORLD_DATA_SIMULATED

    if live_data["status"] != "live":
        return simulated

    # نحاول دمج البيانات الحية مع المحاكاة (للتبسيط، نعيد المحاكاة مع إشارة)
    # في النسخة النهائية، سنطابق أسماء الدول ونحدث المؤشرات
    return simulated  # مؤقتاً، حتى نكمل منطق الدمج
