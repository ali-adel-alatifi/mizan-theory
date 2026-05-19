# mizan/live_data.py
"""
وحدة البيانات الحية - تجلب مؤشرات حقيقية من الإنترنت إن أمكن
وتطبق معادلة الميزان عليها، وإلا تعود للبيانات المحاكية.
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# =============================================
# 1. دوال جلب البيانات من مصادر متعددة
# =============================================

@st.cache_data(ttl=86400)
def fetch_gpi_data():
    """جلب مؤشر السلام العالمي (Global Peace Index)"""
    try:
        url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Global%20Peace%20Index%20-%20Institute%20for%20Economics%20%26%20Peace.csv"
        df = pd.read_csv(url)
        latest_year = df["Year"].max()
        df_latest = df[df["Year"] == latest_year]
        return df_latest.to_dict('records')
    except Exception as e:
        st.warning(f"⚠️ تعذر جلب GPI: {e}")
        return []

@st.cache_data(ttl=86400)
def fetch_cpi_data():
    """جلب مؤشر مدركات الفساد (Corruption Perceptions Index)"""
    try:
        url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Corruption%20Perceptions%20Index%20-%20Transparency%20International.csv"
        df = pd.read_csv(url)
        latest_year = df["Year"].max()
        df_latest = df[df["Year"] == latest_year]
        return df_latest.to_dict('records')
    except Exception as e:
        st.warning(f"⚠️ تعذر جلب CPI: {e}")
        return []

@st.cache_data(ttl=86400)
def fetch_hdi_data():
    """جلب مؤشر التنمية البشرية (Human Development Index)"""
    try:
        url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Human%20Development%20Index%20-%20UNDP.csv"
        df = pd.read_csv(url)
        latest_year = df["Year"].max()
        df_latest = df[df["Year"] == latest_year]
        return df_latest.to_dict('records')
    except Exception as e:
        st.warning(f"⚠️ تعذر جلب HDI: {e}")
        return []

@st.cache_data(ttl=86400)
def fetch_world_bank_data():
    """جلب بيانات GDP per capita و Population من البنك الدولي"""
    try:
        gdp_url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/GDP%20per%20capita%20-%20World%20Bank.csv"
        gdp_df = pd.read_csv(gdp_url)
        latest_year = gdp_df["Year"].max()
        gdp_latest = gdp_df[gdp_df["Year"] == latest_year]
        
        pop_url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Population%20-%20World%20Bank.csv"
        pop_df = pd.read_csv(pop_url)
        pop_latest = pop_df[pop_df["Year"] == latest_year]
        
        return {
            "gdp": gdp_latest.to_dict('records'),
            "pop": pop_latest.to_dict('records')
        }
    except Exception as e:
        st.warning(f"⚠️ تعذر جلب بيانات البنك الدولي: {e}")
        return {"gdp": [], "pop": []}

# =============================================
# 2. الدالة الرئيسية لجلب جميع البيانات الحية
# =============================================

def fetch_live_indicators():
    """جلب جميع البيانات الحية المتاحة من المصادر المفتوحة."""
    with st.spinner("جاري جلب البيانات الحية من المصادر العالمية..."):
        gpi = fetch_gpi_data()
        cpi = fetch_cpi_data()
        hdi = fetch_hdi_data()
        wb = fetch_world_bank_data()
        
        return {
            "status": "live" if gpi or cpi or hdi or wb["gdp"] else "simulated",
            "gpi": gpi,
            "cpi": cpi,
            "hdi": hdi,
            "gdp": wb["gdp"],
            "pop": wb["pop"],
            "timestamp": datetime.now().isoformat()
        }

# =============================================
# 3. دمج البيانات الحية مع البيانات المحاكية
# =============================================

def merge_live_data_with_simulated(live_data, simulated_countries):
    """دمج البيانات الحية مع البيانات المحاكية وتحديث القيم الفعلية."""
    live_dict = {}
    
    for row in live_data.get("gpi", []):
        country = row.get("Entity", "")
        if country:
            if country not in live_dict:
                live_dict[country] = {}
            gpi_score = row.get("GPI score", 2.5)
            live_dict[country]["crime"] = min(0.9, max(0.1, (gpi_score - 1) / 4 * 0.8 + 0.1))
            live_dict[country]["peace"] = 1 - live_dict[country]["crime"]
    
    for row in live_data.get("cpi", []):
        country = row.get("Entity", "")
        if country:
            if country not in live_dict:
                live_dict[country] = {}
            cpi_score = row.get("CPI score", 50)
            live_dict[country]["justice"] = min(0.9, max(0.1, cpi_score / 100 * 0.8 + 0.1))
            live_dict[country]["consult"] = live_dict[country]["justice"] * 0.7
    
    for row in live_data.get("hdi", []):
        country = row.get("Entity", "")
        if country:
            if country not in live_dict:
                live_dict[country] = {}
            hdi_score = row.get("HDI", 0.7)
            live_dict[country]["development"] = min(0.9, max(0.1, hdi_score * 0.9))
            live_dict[country]["empowerment"] = live_dict[country]["development"] * 0.8
    
    for row in live_data.get("gdp", []):
        country = row.get("Entity", "")
        if country:
            if country not in live_dict:
                live_dict[country] = {}
            gdp_val = row.get("GDP per capita (current US$)", 10000)
            live_dict[country]["gdp_real"] = gdp_val
    
    for row in live_data.get("pop", []):
        country = row.get("Entity", "")
        if country:
            if country not in live_dict:
                live_dict[country] = {}
            pop_val = row.get("Population (historical estimates)", 10000000)
            live_dict[country]["pop_real"] = pop_val
    
    merged = []
    for sim in simulated_countries:
        country_name = sim["country"]
        live = live_dict.get(country_name, {})
        
        sim["gdp"] = round(live.get("gdp_real", sim["gdp"]) / 1000) * 1000
        sim["pop"] = round(live.get("pop_real", sim["pop"]) * 1000000) / 1000000
        
        if "crime" in live:
            sim["crime"] = round(live["crime"], 2)
        if "justice" in live:
            sim["justice"] = round(live["justice"], 2)
        if "empowerment" in live:
            sim["consult"] = round((sim["consult"] + live["empowerment"]) / 2, 2)
        
        merged.append(sim)
    
    return merged

# =============================================
# 4. الدالة الرئيسية لبناء بيانات العالم
# =============================================

def build_world_data(live_data):
    """دمج البيانات الحية مع المحاكاة وإرجاع القائمة النهائية للدول."""
    from observatory import WORLD_DATA_SIMULATED
    simulated = WORLD_DATA_SIMULATED
    
    if live_data["status"] == "live":
        return merge_live_data_with_simulated(live_data, simulated)
    else:
        return simulated
