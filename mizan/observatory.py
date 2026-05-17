# mizan/observatory.py
"""
المرصد الحضاري العالمي - يطبق معادلة الميزان على جميع دول العالم
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from logic import calculate_S
from live_data import fetch_live_indicators, build_world_data

# =============================================
# 1. البيانات المحاكية الاحتياطية - جميع دول العالم
# =============================================
WORLD_DATA_SIMULATED = [
    # الشرق الأوسط وشمال أفريقيا
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
    # أفريقيا جنوب الصحراء
    {"country": "نيجيريا", "iso": "NGA", "pop": 223, "gdp": 2000, "worship": 0.7, "charity": 0.4, "justice": 0.2, "consult": 0.2, "loyalty": 0.6, "prayer": 0.5, "crime": 0.7, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.5, "taghut": 0.7},
    {"country": "جنوب أفريقيا", "iso": "ZAF", "pop": 60, "gdp": 6000, "worship": 0.5, "charity": 0.3, "justice": 0.3, "consult": 0.5, "loyalty": 0.4, "prayer": 0.4, "crime": 0.8, "divorce": 0.5, "suicide": 0.4, "alcohol": 0.6, "riba": 0.7, "taghut": 0.7},
    {"country": "كينيا", "iso": "KEN", "pop": 55, "gdp": 2000, "worship": 0.6, "charity": 0.4, "justice": 0.3, "consult": 0.4, "loyalty": 0.5, "prayer": 0.5, "crime": 0.6, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.3, "riba": 0.5, "taghut": 0.6},
    {"country": "إثيوبيا", "iso": "ETH", "pop": 126, "gdp": 1000, "worship": 0.6, "charity": 0.4, "justice": 0.2, "consult": 0.3, "loyalty": 0.5, "prayer": 0.5, "crime": 0.5, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.3, "taghut": 0.6},
    {"country": "تنزانيا", "iso": "TZA", "pop": 67, "gdp": 1200, "worship": 0.5, "charity": 0.4, "justice": 0.3, "consult": 0.3, "loyalty": 0.4, "prayer": 0.4, "crime": 0.5, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.2, "riba": 0.3, "taghut": 0.6},
    {"country": "السنغال", "iso": "SEN", "pop": 18, "gdp": 1700, "worship": 0.8, "charity": 0.6, "justice": 0.3, "consult": 0.3, "loyalty": 0.7, "prayer": 0.7, "crime": 0.3, "divorce": 0.3, "suicide": 0.1, "alcohol": 0.05, "riba": 0.3, "taghut": 0.4},
    {"country": "مالي", "iso": "MLI", "pop": 23, "gdp": 900, "worship": 0.8, "charity": 0.5, "justice": 0.1, "consult": 0.1, "loyalty": 0.7, "prayer": 0.7, "crime": 0.5, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.05, "riba": 0.2, "taghut": 0.5},
    {"country": "غانا", "iso": "GHA", "pop": 33, "gdp": 2500, "worship": 0.6, "charity": 0.4, "justice": 0.4, "consult": 0.5, "loyalty": 0.5, "prayer": 0.5, "crime": 0.4, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.3, "riba": 0.5, "taghut": 0.5},
    # أوروبا
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
    # آسيا والمحيط الهادئ
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
    # الأمريكتان
    {"country": "كندا", "iso": "CAN", "pop": 40, "gdp": 54000, "worship": 0.2, "charity": 0.6, "justice": 0.8, "consult": 0.9, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.4, "suicide": 0.4, "alcohol": 0.6, "riba": 0.9, "taghut": 0.2},
    {"country": "المكسيك", "iso": "MEX", "pop": 128, "gdp": 11000, "worship": 0.4, "charity": 0.3, "justice": 0.3, "consult": 0.5, "loyalty": 0.3, "prayer": 0.3, "crime": 0.7, "divorce": 0.3, "suicide": 0.2, "alcohol": 0.4, "riba": 0.7, "taghut": 0.6},
    {"country": "البرازيل", "iso": "BRA", "pop": 216, "gdp": 9000, "worship": 0.4, "charity": 0.4, "justice": 0.3, "consult": 0.5, "loyalty": 0.3, "prayer": 0.3, "crime": 0.7, "divorce": 0.5, "suicide": 0.3, "alcohol": 0.5, "riba": 0.8, "taghut": 0.6},
    {"country": "الأرجنتين", "iso": "ARG", "pop": 46, "gdp": 13000, "worship": 0.4, "charity": 0.3, "justice": 0.4, "consult": 0.6, "loyalty": 0.3, "prayer": 0.3, "crime": 0.5, "divorce": 0.4, "suicide": 0.3, "alcohol": 0.5, "riba": 0.8, "taghut": 0.5},
    {"country": "فنزويلا", "iso": "VEN", "pop": 28, "gdp": 4000, "worship": 0.4, "charity": 0.2, "justice": 0.1, "consult": 0.2, "loyalty": 0.3, "prayer": 0.3, "crime": 0.8, "divorce": 0.4, "suicide": 0.2, "alcohol": 0.4, "riba": 0.6, "taghut": 0.8},
    # آسيا الوسطى والقوقاز
    {"country": "كازاخستان", "iso": "KAZ", "pop": 20, "gdp": 12000, "worship": 0.4, "charity": 0.4, "justice": 0.3, "consult": 0.2, "loyalty": 0.4, "prayer": 0.3, "crime": 0.4, "divorce": 0.3, "suicide": 0.4, "alcohol": 0.4, "riba": 0.5, "taghut": 0.6},
    {"country": "أوزبكستان", "iso": "UZB", "pop": 36, "gdp": 2500, "worship": 0.6, "charity": 0.5, "justice": 0.2, "consult": 0.2, "loyalty": 0.6, "prayer": 0.5, "crime": 0.3, "divorce": 0.2, "suicide": 0.2, "alcohol": 0.2, "riba": 0.4, "taghut": 0.5},
    {"country": "أذربيجان", "iso": "AZE", "pop": 10, "gdp": 6000, "worship": 0.5, "charity": 0.4, "justice": 0.3, "consult": 0.2, "loyalty": 0.5, "prayer": 0.4, "crime": 0.3, "divorce": 0.2, "suicide": 0.2, "alcohol": 0.3, "riba": 0.5, "taghut": 0.5},
    # شرق آسيا إضافي
    {"country": "تايلاند", "iso": "THA", "pop": 72, "gdp": 7000, "worship": 0.1, "charity": 0.4, "justice": 0.4, "consult": 0.4, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.3, "suicide": 0.3, "alcohol": 0.5, "riba": 0.6, "taghut": 0.4},
    {"country": "فيتنام", "iso": "VNM", "pop": 99, "gdp": 4000, "worship": 0.1, "charity": 0.3, "justice": 0.4, "consult": 0.2, "loyalty": 0.1, "prayer": 0.1, "crime": 0.3, "divorce": 0.2, "suicide": 0.3, "alcohol": 0.5, "riba": 0.5, "taghut": 0.7},
    {"country": "الفلبين", "iso": "PHL", "pop": 117, "gdp": 4000, "worship": 0.4, "charity": 0.5, "justice": 0.3, "consult": 0.5, "loyalty": 0.4, "prayer": 0.4, "crime": 0.5, "divorce": 0.1, "suicide": 0.2, "alcohol": 0.4, "riba": 0.5, "taghut": 0.5},
]

# =============================================
# 2. تحويل البيانات الخام إلى W_raw و B_raw
# =============================================
def compute_world_mizan():
    """حساب معادلة الميزان لجميع دول العالم وإرجاع DataFrame."""
    live_data = fetch_live_indicators()
    world_list = build_world_data(live_data)
    
    results = []
    for d in world_list:
        W_vals = [d["worship"], d["charity"], d["justice"], d["consult"], d["loyalty"], d["prayer"]]
        B_vals = [1 - d["crime"], 1 - d["divorce"], 1 - d["suicide"],
                  1 - d["alcohol"], 1 - d["riba"], 1 - d["taghut"]]

        W_raw = np.mean(W_vals) * 2 - 1
        B_raw = np.mean(B_vals) * 2 - 1

        W_pure = True
        B_compassion = (1 - d["divorce"]) * 2 - 1
        B_disavowal = (1 - d["taghut"]) * 2 - 1

        S_final, E_val, gate_name, gate_msg, gate_color, istidraj_gap = calculate_S(
            W_raw, B_raw, d["gdp"] / 100000, W_pure, B_compassion, B_disavowal
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
            "الحكم": gate_name,
        })
    return pd.DataFrame(results)

# =============================================
# 3. عرض المرصد على الخريطة
# =============================================
def render_observatory():
    """عرض المرصد الحضاري العالمي."""
    st.header("🌍 المرصد الحضاري العالمي")
    st.markdown("### 📡 محطة الأرصاد الحضارية – القانون الكوني الحي")
    st.caption("النقاط الذهبية = ثبات | النقاط البرتقالية = استدراج | النقاط الحمراء = انهيار")

    df = compute_world_mizan()

    # تحديد اللون بناء على فجوة الاستدراج
    def get_color(row):
        if row["فجوة الاستدراج"] > 0.3: return "#ff4444"
        elif row["فجوة الاستدراج"] > 0.1: return "#ffaa00"
        elif row["S (الثبات)"] > 0.6: return "#FFD700"
        elif row["S (الثبات)"] > 0.3: return "#ffdd57"
        else: return "#888888"

    df["اللون"] = df.apply(get_color, axis=1)

    fig = px.scatter_geo(
        df,
        locations="ISO",
        locationmode="ISO-3",
        size="السكان (مليون)",
        color="فجوة الاستدراج",
        hover_name="الدولة",
        hover_data={
            "W": True, "B": True, "S (الثبات)": True,
            "فجوة الاستدراج": True, "الحكم": True,
            "السكان (مليون)": True, "الناتج (GDP)": True
        },
        color_continuous_scale=["#ff4444", "#ffaa00", "#ffdd57", "#FFD700"],
        range_color=[0, 0.5],
        projection="natural earth",
        title="خريطة الميزان العالمية – S = W x B"
    )
    fig.update_geos(showcoastlines=True, coastlinecolor="white", showland=True, landcolor="#0a0f1e")
    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 جدول الأمم – الميزان التفصيلي")
    display_cols = ["الدولة", "W", "B", "S (الثبات)", "فجوة الاستدراج", "الحكم"]
    st.dataframe(
        df[display_cols].sort_values("S (الثبات)", ascending=False)
        .style.background_gradient(subset=["S (الثبات)"], cmap="YlOrRd")
        .background_gradient(subset=["فجوة الاستدراج"], cmap="RdYlGn_r")
        .format({"W": "{:.3f}", "B": "{:.3f}", "S (الثبات)": "{:.3f}", "فجوة الاستدراج": "{:.3f}"}),
        hide_index=True, use_container_width=True
    )

    st.markdown("---")
    high_S = df[df["S (الثبات)"] > 0.6]
    high_gap = df[df["فجوة الاستدراج"] > 0.3]
    st.markdown(f"🟢 **دول ذات ثبات عالٍ (S > 0.6):** {len(high_S)} دولة")
    st.markdown(f"🔴 **دول في حالة استدراج (فجوة > 0.3):** {len(high_gap)} دولة")
