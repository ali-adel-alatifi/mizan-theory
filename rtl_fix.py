# mizan/rtl_fix.py
"""
ملف إصلاح RTL بديل - يستخدم إذا لم يعمل كود CSS في ui_enhancements.py
"""

import streamlit as st

def apply_rtl_fix():
    """تطبيق إصلاح RTL القسري على الصفحة"""
    st.markdown("""
    <style>
    /* إجبار الصفحة بأكملها على العرض من اليمين لليسار */
    .stApp, body {
        direction: rtl !important;
        unicode-bidi: plaintext !important;
    }
    
    /* إجبار كل النصوص والعناصر على الاتجاه الصحيح */
    div, p, h1, h2, h3, h4, h5, h6, span, strong, em, li, label, .stMarkdown, .stText {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: plaintext !important;
    }
    
    /* إصلاح تخطيط الشاشة لملء العرض بالكامل */
    [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        margin-left: 0 !important;
        padding-right: 0 !important;
    }
    
    [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
    """, unsafe_allow_html=True)
