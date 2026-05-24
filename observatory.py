# mizan/observatory.py
"""
الرادار الأخلاقي للعالم الرقمي
يطبق معادلة الميزان على المشاعر والاتجاهات من العالم الرقمي
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from logic import calculate_S
from live_data import fetch_live_indicators, build_world_data
from config import TXT

# =============================================
# دالة إصلاح النصوص العربية
# =============================================
def fix_rtl_display():
    st.markdown("""
    <style>
    div, p, h1, h2, h3, h4, h5, h6, span, strong, em, li, label, .stMarkdown, .stText {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: plaintext !important;
    }
    .stTitle, .stHeader, .stSubheader { direction: rtl !important; text-align: right !important; }
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError { direction: rtl !important; text-align: right !important; }
    .stDataFrame { direction: rtl !important; }
    </style>
    """, unsafe_allow_html=True)

WORLD_DATA_SIMULATED = [
    {"country": "السعودية", "iso": "SAU", "pop": 36, "gdp": 23000, "worship": 0.9, "charity": 0.7, "justice": 0.7, "consult": 0.6, "loyalty": 0.8, "prayer": 0.8, "crime": 0.2, "divorce": 0.3, "suicide": 0.1, "alcohol": 0.05, "riba": 0.4, "taghut": 0.3},
    {"country": "الإمارات", "iso": "ARE", "pop": 10, "gdp": 50000, "worship": 0.7, "charity": 0.8, "justice": 0.6, "consult": 0.4, "loyalty": 0.7, "prayer": 0.7, "crime": 0.2, "divorce": 0.3, "suicide": 0.1, "alcohol": 0.3, "riba": 0.7, "taghut": 0.3},
    {"country": "قطر", "iso": "QAT", "pop": 3, "gdp": 70000, "worship": 0.8, "charity": 0.7, "justice": 0.6, "consult": 0.3, "loyalty": 0.7, "prayer": 0.7, "crime": 0.1, "divorce": 0.3, "suicide": 0.1, "alcohol": 0.2, "riba": 0.8, "taghut": 0.3},
    {"country": "البحرين", "iso": "BHR", "pop": 2, "gdp": 28000, "worship": 0.7, "charity": 0.6, "justice": 0.5, "consult": 0.3, "loyalty": 0.7, "prayer": 0.6, "crime": 0.2, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.4, "riba": 0.7, "taghut": 0.4},
    {"country": "الكويت", "iso": "KWT", "pop": 4, "gdp": 33000, "worship": 0.7, "charity": 0.6, "justice": 0.5, "consult": 0.3, "loyalty": 0.7, "prayer": 0.6, "crime": 0.2, "divorce": 0.4, "suicide": 0.1, "alcohol": 0.2, "riba": 0.7, "taghut": 0.3},
    {"country": "سلطنة عمان", "iso": "OMN", "pop": 5, "gdp": 20000, "worship": 0.8, "charity": 0.5, "justice": 0.5, "consult": 0.3, "loyalty": 0.7, "prayer": 0.7, "crime": 0.1, "divorce": 0.2, "suicide": 0.1, "alcohol": 0.1, "riba": 0.5, "taghut": 0.3},
    {"country": "اليمن", "iso": "YEM", "pop": 34, "gdp": 700, "worship": 0.8, "charity": 0.6, "justice": 0.1, "consult": 0.1, "loyalty": 0.7, "prayer": 0.7, "crime": 0.5, "divorce": 0.4, "suicide": 0.3, "alcohol": 0.05, "riba": 0.3, "taghut": 0.6},
    {"country": "العراق", "iso": "IRQ", "pop": 45, "gdp": 5000, "worship": 0.7, "charity": 0.5, "justice": 0.2, "consult": 0.2, "loyalty": 0.6, "prayer": 0.6, "crime": 0.6, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.1, "riba": 0.4, "taghut": 0.6},
    {"country": "سوريا", "iso": "SYR", "pop": 22, "gdp": 800, "worship": 0.7, "charity": 0.6, "justice": 0.1, "consult": 0.1, "loyalty": 0.6, "prayer": 0.6, "crime": 0.5, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.1, "riba": 0.3, "taghut": 0.6},
    {"country": "الأردن", "iso": "JOR", "pop": 11, "gdp": 4500, "worship": 0.7, "charity": 0.6, "justice": 0.5, "consult": 0.3, "loyalty": 0.7, "prayer": 0.6, "crime": 0.2, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.1, "riba": 0.5, "taghut": 0.4},
    {"country": "لبنان", "iso": "LBN", "pop": 6, "gdp": 4000, "worship": 0.5, "charity": 0.4, "justice": 0.2, "consult": 0.2, "loyalty": 0.5, "prayer": 0.5, "crime": 0.4, "divorce": 0.3, "suicide": 0.3, "alcohol": 0.5, "riba": 0.7, "taghut": 0.6},
    {"country": "فلسطين", "iso": "PSE", "pop": 5, "gdp": 3500, "worship": 0.9, "charity": 0.7, "justice": 0.1, "consult": 0.2, "loyalty": 0.9, "prayer": 0.8, "crime": 0.3, "divorce": 0.2, "suicide": 0.2, "alcohol": 0.05, "riba": 0.3, "taghut": 0.2},
    {"country": "مصر", "iso": "EGY", "pop": 110, "gdp": 4000, "worship": 0.7, "charity": 0.8, "justice": 0.3, "consult": 0.2, "loyalty": 0.7, "prayer": 0.6, "crime": 0.4, "divorce": 0.4, "suicide": 0.2, "alcohol": 0.1, "riba": 0.6, "taghut": 0.6},
    {"country": "ليبيا", "iso": "LBY", "pop": 7, "gdp": 6000, "worship": 0.7, "charity": 0.5, "justice": 0.1, "consult": 0.1, "loyalty": 0.6, "prayer": 0.6, "crime": 0.6, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.05, "riba": 0.4, "taghut": 0.6},
    {"country": "تونس", "iso": "TUN", "pop": 12, "gdp": 4000, "worship": 0.6, "charity": 0.5, "justice": 0.4, "consult": 0.4, "loyalty": 0.6, "prayer": 0.5, "crime": 0.3, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.6, "taghut": 0.5},
    {"country": "الجزائر", "iso": "DZA", "pop": 45, "gdp": 4500, "worship": 0.7, "charity": 0.5, "justice": 0.3, "consult": 0.2, "loyalty": 0.7, "prayer": 0.6, "crime": 0.3, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.1, "riba": 0.5, "taghut": 0.5},
    {"country": "المغرب", "iso": "MAR", "pop": 38, "gdp": 3500, "worship": 0.7, "charity": 0.5, "justice": 0.4, "consult": 0.3, "loyalty": 0.7, "prayer": 0.6, "crime": 0.3, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.5, "taghut": 0.5},
    {"country": "موريتانيا", "iso": "MRT", "pop": 5, "gdp": 2000, "worship": 0.8, "charity": 0.5, "justice": 0.2, "consult": 0.2, "loyalty": 0.7, "prayer": 0.7, "crime": 0.4, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.05, "riba": 0.3, "taghut": 0.5},
    {"country": "السودان", "iso": "SDN", "pop": 48, "gdp": 1000, "worship": 0.7, "charity": 0.6, "justice": 0.1, "consult": 0.1, "loyalty": 0.6, "prayer": 0.6, "crime": 0.6, "divorce": 0.4, "suicide": 0.3, "alcohol": 0.05, "riba": 0.4, "taghut": 0.7},
    {"country": "نيجيريا", "iso": "NGA", "pop": 223, "gdp": 2000, "worship": 0.7, "charity": 0.4, "justice": 0.2, "consult": 0.2, "loyalty": 0.6, "prayer": 0.5, "crime": 0.7, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.5, "taghut": 0.7},
    {"country": "جنوب أفريقيا", "iso": "ZAF", "pop": 60, "gdp": 6000, "worship": 0.5, "charity": 0.3, "justice": 0.3, "consult": 0.5, "loyalty": 0.4, "prayer": 0.4, "crime": 0.8, "divorce": 0.5, "suicide": 0.4, "alcohol": 0.6, "riba": 0.7, "taghut": 0.7},
    {"country": "كينيا", "iso": "KEN", "pop": 55, "gdp": 2000, "worship": 0.6, "charity": 0.4, "justice": 0.3, "consult": 0.4, "loyalty": 0.5, "prayer": 0.5, "crime": 0.6, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.3, "riba": 0.5, "taghut": 0.6},
    {"country": "إثيوبيا", "iso": "ETH", "pop": 126, "gdp": 1000, "worship": 0.6, "charity": 0.4, "justice": 0.2, "consult": 0.3, "loyalty": 0.5, "prayer": 0.5, "crime": 0.5, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.3, "taghut": 0.6},
    {"country": "تنزانيا", "iso": "TZA", "pop": 67, "gdp": 1200, "worship": 0.5, "charity": 0.4, "justice": 0.3, "consult": 0.3, "loyalty": 0.4, "prayer": 0.4, "crime": 0.5, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.3, "taghut": 0.6},
    {"country": "السنغال", "iso": "SEN", "pop": 18, "gdp": 1700, "worship": 0.8, "charity": 0.6, "justice": 0.3, "consult": 0.3, "loyalty": 0.7, "prayer": 0.7, "crime": 0.3, "divorce": 0.3, "suicide": 0.1, "alcohol": 0.05, "riba": 0.3, "taghut": 0.4},
    {"country": "مالي", "iso": "MLI", "pop": 23, "gdp": 900, "worship": 0.8, "charity": 0.5, "justice": 0.1, "consult": 0.1, "loyalty": 0.7, "prayer": 0.7, "crime": 0.5, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.05, "riba": 0.2, "taghut": 0.5},
    {"country": "غانا", "iso": "GHA", "pop": 33, "gdp": 2500, "worship": 0.6, "charity": 0.4, "justice": 0.4, "consult": 0.5, "loyalty": 0.5, "prayer": 0.5, "crime": 0.4, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.3, "riba": 0.5, "taghut": 0.5},
    {"country": "تركيا", "iso": "TUR", "pop": 85, "gdp": 12000, "worship": 0.6, "charity": 0.5, "justice": 0.5, "consult": 0.4, "loyalty": 0.6, "prayer": 0.5, "crime": 0.3, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.3, "riba": 0.7, "taghut": 0.5},
    {"country": "ألبانيا", "iso": "ALB", "pop": 3, "gdp": 7000, "worship": 0.4, "charity": 0.3, "justice": 0.3, "consult": 0.4, "loyalty": 0.4, "prayer": 0.3, "crime": 0.3, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.4, "riba": 0.5, "taghut": 0.5},
    {"country": "البوسنة", "iso": "BIH", "pop": 3, "gdp": 7000, "worship": 0.5, "charity": 0.4, "justice": 0.3, "consult": 0.3, "loyalty": 0.5, "prayer": 0.4, "crime": 0.3, "divorce": 0.2, "suicide": 0.3, "alcohol": 0.3, "riba": 0.5, "taghut": 0.5},
    {"country": "كوسوفو", "iso": "XKX", "pop": 2, "gdp": 5000, "worship": 0.6, "charity": 0.4, "justice": 0.3, "consult": 0.3, "loyalty": 0.6, "prayer": 0.5, "crime": 0.3, "divorce": 0.2, "suicide": 0.2, "alcohol": 0.2, "riba": 0.5, "taghut": 0.4},
    {"country": "أمريكا", "iso": "USA", "pop": 335, "gdp": 76000, "worship": 0.3, "charity": 0.5, "justice": 0.6, "consult": 0.8, "loyalty": 0.2, "prayer": 0.2, "crime": 0.5, "divorce": 0.6, "suicide": 0.5, "alcohol": 0.7, "riba": 0.9, "taghut": 0.3},
    {"country": "بريطانيا", "iso": "GBR", "pop": 68, "gdp": 47000, "worship": 0.2, "charity": 0.5, "justice": 0.7, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.5, "divorce": 0.5, "suicide": 0.4, "alcohol": 0.8, "riba": 0.9, "taghut": 0.2},
    {"country": "فرنسا", "iso": "FRA", "pop": 66, "gdp": 44000, "worship": 0.2, "charity": 0.4, "justice": 0.6, "consult": 0.8, "loyalty": 0.1, "prayer": 0.1, "crime": 0.5, "divorce": 0.5, "suicide": 0.5, "alcohol": 0.7, "riba": 0.9, "taghut": 0.3},
    {"country": "ألمانيا", "iso": "DEU", "pop": 84, "gdp": 51000, "worship": 0.2, "charity": 0.5, "justice": 0.7, "consult": 0.8, "loyalty": 0.1, "prayer": 0.1, "crime": 0.4, "divorce": 0.4, "suicide": 0.4, "alcohol": 0.8, "riba": 0.9, "taghut": 0.2},
    {"country": "إيطاليا", "iso": "ITA", "pop": 59, "gdp": 38000, "worship": 0.3, "charity": 0.4, "justice": 0.5, "consult": 0.7, "loyalty": 0.2, "prayer": 0.2, "crime": 0.4, "divorce": 0.4, "suicide": 0.3, "alcohol": 0.6, "riba": 0.8, "taghut": 0.3},
    {"country": "إسبانيا", "iso": "ESP", "pop": 48, "gdp": 31000, "worship": 0.3, "charity": 0.4, "justice": 0.6, "consult": 0.7, "loyalty": 0.2, "prayer": 0.2, "crime": 0.4, "divorce": 0.5, "suicide": 0.3, "alcohol": 0.6, "riba": 0.8, "taghut": 0.3},
    {"country": "هولندا", "iso": "NLD", "pop": 18, "gdp": 62000, "worship": 0.2, "charity": 0.5, "justice": 0.8, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.4, "suicide": 0.4, "alcohol": 0.7, "riba": 0.9, "taghut": 0.2},
    {"country": "بلجيكا", "iso": "BEL", "pop": 12, "gdp": 54000, "worship": 0.2, "charity": 0.4, "justice": 0.7, "consult": 0.8, "loyalty": 0.1, "prayer": 0.1, "crime": 0.4, "divorce": 0.5, "suicide": 0.5, "alcohol": 0.7, "riba": 0.9, "taghut": 0.3},
    {"country": "سويسرا", "iso": "CHE", "pop": 9, "gdp": 94000, "worship": 0.2, "charity": 0.5, "justice": 0.9, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.2, "divorce": 0.4, "suicide": 0.4, "alcohol": 0.6, "riba": 0.9, "taghut": 0.1},
    {"country": "السويد", "iso": "SWE", "pop": 11, "gdp": 56000, "worship": 0.1, "charity": 0.5, "justice": 0.8, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.5, "suicide": 0.4, "alcohol": 0.6, "riba": 0.9, "taghut": 0.2},
    {"country": "النرويج", "iso": "NOR", "pop": 6, "gdp": 89000, "worship": 0.1, "charity": 0.6, "justice": 0.9, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.2, "divorce": 0.4, "suicide": 0.3, "alcohol": 0.5, "riba": 0.9, "taghut": 0.1},
    {"country": "الدنمارك", "iso": "DNK", "pop": 6, "gdp": 68000, "worship": 0.1, "charity": 0.6, "justice": 0.9, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.2, "divorce": 0.5, "suicide": 0.3, "alcohol": 0.7, "riba": 0.9, "taghut": 0.1},
    {"country": "فنلندا", "iso": "FIN", "pop": 6, "gdp": 54000, "worship": 0.1, "charity": 0.5, "justice": 0.9, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.2, "divorce": 0.4, "suicide": 0.4, "alcohol": 0.6, "riba": 0.9, "taghut": 0.2},
    {"country": "بولندا", "iso": "POL", "pop": 38, "gdp": 21000, "worship": 0.4, "charity": 0.4, "justice": 0.5, "consult": 0.6, "loyalty": 0.3, "prayer": 0.3, "crime": 0.2, "divorce": 0.3, "suicide": 0.3, "alcohol": 0.7, "riba": 0.7, "taghut": 0.3},
    {"country": "أوكرانيا", "iso": "UKR", "pop": 38, "gdp": 4000, "worship": 0.4, "charity": 0.3, "justice": 0.3, "consult": 0.4, "loyalty": 0.3, "prayer": 0.3, "crime": 0.4, "divorce": 0.5, "suicide": 0.5, "alcohol": 0.7, "riba": 0.6, "taghut": 0.5},
    {"country": "روسيا", "iso": "RUS", "pop": 144, "gdp": 13000, "worship": 0.3, "charity": 0.3, "justice": 0.3, "consult": 0.2, "loyalty": 0.2, "prayer": 0.2, "crime": 0.6, "divorce": 0.6, "suicide": 0.6, "alcohol": 0.8, "riba": 0.7, "taghut": 0.7},
    {"country": "اليونان", "iso": "GRC", "pop": 10, "gdp": 23000, "worship": 0.3, "charity": 0.3, "justice": 0.5, "consult": 0.6, "loyalty": 0.2, "prayer": 0.2, "crime": 0.4, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.5, "riba": 0.8, "taghut": 0.4},
    {"country": "إيران", "iso": "IRN", "pop": 89, "gdp": 5000, "worship": 0.8, "charity": 0.6, "justice": 0.4, "consult": 0.3, "loyalty": 0.7, "prayer": 0.7, "crime": 0.3, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.05, "riba": 0.4, "taghut": 0.5},
    {"country": "باكستان", "iso": "PAK", "pop": 240, "gdp": 1500, "worship": 0.7, "charity": 0.6, "justice": 0.2, "consult": 0.3, "loyalty": 0.7, "prayer": 0.6, "crime": 0.5, "divorce": 0.3, "suicide": 0.3, "alcohol": 0.05, "riba": 0.5, "taghut": 0.6},
    {"country": "أفغانستان", "iso": "AFG", "pop": 42, "gdp": 400, "worship": 0.9, "charity": 0.5, "justice": 0.1, "consult": 0.1, "loyalty": 0.8, "prayer": 0.8, "crime": 0.5, "divorce": 0.2, "suicide": 0.3, "alcohol": 0.01, "riba": 0.2, "taghut": 0.4},
    {"country": "الهند", "iso": "IND", "pop": 1440, "gdp": 2500, "worship": 0.3, "charity": 0.4, "justice": 0.3, "consult": 0.5, "loyalty": 0.2, "prayer": 0.3, "crime": 0.4, "divorce": 0.2, "suicide": 0.5, "alcohol": 0.2, "riba": 0.5, "taghut": 0.5},
    {"country": "بنجلاديش", "iso": "BGD", "pop": 173, "gdp": 2800, "worship": 0.7, "charity": 0.5, "justice": 0.2, "consult": 0.3, "loyalty": 0.7, "prayer": 0.7, "crime": 0.3, "divorce": 0.2, "suicide": 0.2, "alcohol": 0.02, "riba": 0.4, "taghut": 0.5},
    {"country": "إندونيسيا", "iso": "IDN", "pop": 277, "gdp": 4500, "worship": 0.8, "charity": 0.7, "justice": 0.5, "consult": 0.5, "loyalty": 0.7, "prayer": 0.7, "crime": 0.3, "divorce": 0.4, "suicide": 0.2, "alcohol": 0.1, "riba": 0.5, "taghut": 0.4},
    {"country": "ماليزيا", "iso": "MYS", "pop": 34, "gdp": 12000, "worship": 0.8, "charity": 0.6, "justice": 0.5, "consult": 0.4, "loyalty": 0.7, "prayer": 0.7, "crime": 0.3, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.1, "riba": 0.6, "taghut": 0.4},
    {"country": "بروناي", "iso": "BRN", "pop": 1, "gdp": 35000, "worship": 0.9, "charity": 0.7, "justice": 0.6, "consult": 0.3, "loyalty": 0.8, "prayer": 0.8, "crime": 0.1, "divorce": 0.2, "suicide": 0.1, "alcohol": 0.05, "riba": 0.5, "taghut": 0.2},
    {"country": "الصين", "iso": "CHN", "pop": 1425, "gdp": 13000, "worship": 0.1, "charity": 0.3, "justice": 0.3, "consult": 0.1, "loyalty": 0.1, "prayer": 0.1, "crime": 0.2, "divorce": 0.4, "suicide": 0.4, "alcohol": 0.4, "riba": 0.6, "taghut": 0.8},
    {"country": "اليابان", "iso": "JPN", "pop": 124, "gdp": 35000, "worship": 0.1, "charity": 0.4, "justice": 0.7, "consult": 0.7, "loyalty": 0.1, "prayer": 0.1, "crime": 0.1, "divorce": 0.3, "suicide": 0.7, "alcohol": 0.6, "riba": 0.9, "taghut": 0.2},
    {"country": "كوريا الجنوبية", "iso": "KOR", "pop": 52, "gdp": 34000, "worship": 0.2, "charity": 0.4, "justice": 0.6, "consult": 0.7, "loyalty": 0.2, "prayer": 0.2, "crime": 0.2, "divorce": 0.3, "suicide": 0.7, "alcohol": 0.7, "riba": 0.8, "taghut": 0.3},
    {"country": "أستراليا", "iso": "AUS", "pop": 26, "gdp": 63000, "worship": 0.2, "charity": 0.5, "justice": 0.7, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.5, "suicide": 0.4, "alcohol": 0.7, "riba": 0.9, "taghut": 0.2},
    {"country": "كندا", "iso": "CAN", "pop": 40, "gdp": 54000, "worship": 0.2, "charity": 0.6, "justice": 0.8, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.4, "suicide": 0.4, "alcohol": 0.6, "riba": 0.9, "taghut": 0.2},
    {"country": "المكسيك", "iso": "MEX", "pop": 128, "gdp": 11000, "worship": 0.4, "charity": 0.3, "justice": 0.3, "consult": 0.5, "loyalty": 0.3, "prayer": 0.3, "crime": 0.7, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.4, "riba": 0.7, "taghut": 0.6},
    {"country": "البرازيل", "iso": "BRA", "pop": 216, "gdp": 9000, "worship": 0.4, "charity": 0.4, "justice": 0.3, "consult": 0.5, "loyalty": 0.3, "prayer": 0.3, "crime": 0.7, "divorce": 0.5, "suicide": 0.3, "alcohol": 0.5, "riba": 0.8, "taghut": 0.6},
    {"country": "الأرجنتين", "iso": "ARG", "pop": 46, "gdp": 13000, "worship": 0.4, "charity": 0.3, "justice": 0.4, "consult": 0.6, "loyalty": 0.3, "prayer": 0.3, "crime": 0.5, "divorce": 0.4, "suicide": 0.3, "alcohol": 0.5, "riba": 0.8, "taghut": 0.5},
    {"country": "فنزويلا", "iso": "VEN", "pop": 28, "gdp": 4000, "worship": 0.4, "charity": 0.2, "justice": 0.1, "consult": 0.2, "loyalty": 0.3, "prayer": 0.3, "crime": 0.8, "divorce": 0.4, "suicide": 0.2, "alcohol": 0.4, "riba": 0.6, "taghut": 0.8},
    {"country": "كازاخستان", "iso": "KAZ", "pop": 20, "gdp": 12000, "worship": 0.4, "charity": 0.4, "justice": 0.3, "consult": 0.2, "loyalty": 0.4, "prayer": 0.3, "crime": 0.4, "divorce": 0.3, "suicide": 0.4, "alcohol": 0.4, "riba": 0.5, "taghut": 0.6},
    {"country": "أوزبكستان", "iso": "UZB", "pop": 36, "gdp": 2500, "worship": 0.6, "charity": 0.5, "justice": 0.2, "consult": 0.2, "loyalty": 0.6, "prayer": 0.5, "crime": 0.3, "divorce": 0.2, "suicide": 0.2, "alcohol": 0.2, "riba": 0.4, "taghut": 0.5},
    {"country": "أذربيجان", "iso": "AZE", "pop": 10, "gdp": 6000, "worship": 0.5, "charity": 0.4, "justice": 0.3, "consult": 0.2, "loyalty": 0.5, "prayer": 0.4, "crime": 0.3, "divorce": 0.2, "suicide": 0.2, "alcohol": 0.3, "riba": 0.5, "taghut": 0.5},
    {"country": "تايلاند", "iso": "THA", "pop": 72, "gdp": 7000, "worship": 0.1, "charity": 0.4, "justice": 0.4, "consult": 0.4, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.3, "suicide": 0.3, "alcohol": 0.5, "riba": 0.6, "taghut": 0.4},
    {"country": "فيتنام", "iso": "VNM", "pop": 99, "gdp": 4000, "worship": 0.1, "charity": 0.3, "justice": 0.4, "consult": 0.2, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.2, "suicide": 0.3, "alcohol": 0.5, "riba": 0.5, "taghut": 0.7},
    {"country": "الفلبين", "iso": "PHL", "pop": 117, "gdp": 4000, "worship": 0.4, "charity": 0.5, "justice": 0.3, "consult": 0.5, "loyalty": 0.4, "prayer": 0.4, "crime": 0.5, "divorce": 0.1, "suicide": 0.2, "alcohol": 0.4, "riba": 0.5, "taghut": 0.5},
]

def compute_world_mizan():
    live_data = fetch_live_indicators()
    world_list = build_world_data(live_data)
    results = []
    for d in world_list:
        W_vals = [d["worship"], d["charity"], d["justice"], d["consult"], d["loyalty"], d["prayer"]]
        B_vals = [1 - d["crime"], 1 - d["divorce"], 1 - d["suicide"], 1 - d["alcohol"], 1 - d["riba"], 1 - d["taghut"]]
        W_raw = np.mean(W_vals) * 2 - 1
        B_raw = np.mean(B_vals) * 2 - 1
        W_pure = True
        B_compassion = (1 - d["divorce"]) * 2 - 1
        B_disavowal = (1 - d["taghut"]) * 2 - 1
        gdp_normalized = min(1.0, d["gdp"] / 100000)
        S_final, E_val, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
            W_raw, B_raw, gdp_normalized, W_pure, B_compassion, B_disavowal
        )
        results.append({
            "الدولة": d["country"],
            "ISO": d["iso"],
            "السكان (مليون)": d["pop"],
            "الناتج (GDP)": d["gdp"],
            "W": round(W_raw, 3),
            "B": round(B_raw, 3),
            "S (الثبات)": round(S_final, 3),
            "فجوة الاستدراج": round(istidraj_gap, 3),
            "الحكم": gate_name
        })
    return pd.DataFrame(results)

def render_observatory():
    fix_rtl_display()
    
    st.header("🌍 الرادار الأخلاقي للعالم الرقمي")
    st.markdown("### 📡 محطة الرصد الأخلاقية – القانون الكوني الحي")
    st.caption(TXT(
        "يقيس هذا الرادار نبض العالم الرقمي في الزمن الحقيقي، ويطبق معادلة الميزان على المشاعر والاتجاهات.",
        "This radar measures the pulse of the digital world in real-time, applying the Mizan equation to sentiment and trends."
    ))
    
    # ─────────────────────────────────────────
    # اختيار وضع التشغيل
    # ─────────────────────────────────────────
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        mode = st.radio(
            TXT("وضع الرادار", "Radar Mode"),
            [TXT("🖐️ يدوي (تحليل ثابت)", "🖐️ Manual (Static)"), TXT("📡 رادار أخلاقي حي", "📡 Live Ethical Radar")],
            key="observatory_mode"
        )
    
    # ─────────────────────────────────────────
    # جلب البيانات حسب الوضع
    # ─────────────────────────────────────────
    if mode == TXT("🖐️ يدوي (تحليل ثابت)", "🖐️ Manual (Static)"):
        st.caption(TXT("استخدم المنزلقات للتحكم في قيم W و B و E يدويًا.", "Use sliders to control W, B, and E manually."))
        col_w, col_b, col_e = st.columns(3)
        with col_w:
            manual_w = st.slider("W (الولاء)", -1.0, 1.0, 0.5, 0.1, key="manual_w")
        with col_b:
            manual_b = st.slider("B (البراءة)", -1.0, 1.0, 0.5, 0.1, key="manual_b")
        with col_e:
            manual_e = st.slider("E (التمكين)", 0.0, 1.0, 0.5, 0.1, key="manual_e")
        
        live_data = fetch_live_indicators(
            mode="manual",
            manual_values={"sentiment": manual_w, "trend": manual_b, "engagement": manual_e * 1000}
        )
    else:
        st.caption(TXT(
            "📡 الرادار الأخلاقي الحي يستخدم الذكاء الاصطناعي لتحليل المشاعر والاتجاهات من المصادر الحية.",
            "📡 Live Ethical Radar uses AI to analyze sentiment and trends from live sources."
        ))
        live_data = fetch_live_indicators(mode="auto")
    
    # ─────────────────────────────────────────
    # عرض بيانات الرادار
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader(TXT("📊 بيانات الرادار الأخلاقي", "📊 Ethical Radar Data"))
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    col_s1.metric(TXT("متوسط المشاعر", "Avg Sentiment"), f"{live_data.get('sentiment_avg', 0.0):.2f}")
    col_s2.metric(TXT("اتجاه الاتجاه", "Trend Direction"), f"{live_data.get('trend_direction', 0.0):.2f}")
    col_s3.metric(TXT("التفاعلات", "Engagement"), f"{live_data.get('engagement_count', 0)}")
    col_s4.metric(TXT("حالة الرادار", "Radar Status"), 
                 TXT("🟢 حي", "🟢 Live") if live_data.get("status") == "live" else 
                 TXT("🟡 محاكاة", "🟡 Simulated"))
    
    # عرض نبض العالم الرقمي (مؤشر بصري)
    st.markdown("---")
    st.subheader(TXT("📡 نبض العالم الرقمي", "📡 Digital World Pulse"))
    
    pulse_value = (live_data.get('sentiment_avg', 0.0) + 1) / 2 * 100
    st.progress(int(pulse_value), text=TXT(f"نبض العالم الرقمي: {pulse_value:.1f}%", f"Digital World Pulse: {pulse_value:.1f}%"))
    
    if pulse_value > 70:
        st.success(TXT("🟢 العالم الرقمي في حالة ثبات عالٍ.", "🟢 The digital world is in high stability."))
    elif pulse_value > 50:
        st.info(TXT("🟡 العالم الرقمي في حالة متوسطة.", "🟡 The digital world is in moderate stability."))
    elif pulse_value > 30:
        st.warning(TXT("🟠 العالم الرقمي في حالة انحدار.", "🟠 The digital world is declining."))
    else:
        st.error(TXT("🔴 العالم الرقمي في حالة انهيار.", "🔴 The digital world is collapsing."))
    
    # عرض الخريطة والجدول
    world_list = build_world_data(live_data)
    df = pd.DataFrame(world_list)
    
    fig = px.scatter_geo(
        df,
        locations="iso",
        locationmode="ISO-3",
        size="pop",
        color="worship",
        hover_name="country",
        hover_data={"worship": True, "taghut": True},
        color_continuous_scale="RdYlGn",
        projection="natural earth",
        title=TXT("خريطة الميزان العالمية (تحديث حي)", "Global Mizan Map (Live Update)")
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader(TXT("📊 جدول الأمم – الميزان التفصيلي", "📊 Nations Table – Detailed Mizan"))
    display_cols = ["country", "worship", "taghut", "pop", "gdp"]
    st.dataframe(df[display_cols], hide_index=True, use_container_width=True)
