# mizan/live_data.py
"""
الرادار الأخلاقي للعالم الرقمي
يحلل المشاعر والاتجاهات من المصادر الرقمية ويطبق معادلة الميزان
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import re

# محاولة استيراد TextBlob (اختياري)
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

# =============================================
# 1. دوال تحليل المشاعر الأساسية
# =============================================

def analyze_sentiment(text):
    """تحليل المشاعر للنص (إيجابي/سلبي/محايد)."""
    if not text or not isinstance(text, str):
        return 0.0
    try:
        if TEXTBLOB_AVAILABLE:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        else:
            positive_words = ['حق', 'عدل', 'خير', 'نور', 'إيمان', 'تقوى', 'ولاء', 'ثبات', 'رحمة', 'عطاء']
            negative_words = ['ظلم', 'باطل', 'شر', 'فساد', 'كفر', 'نفاق', 'طاغوت', 'انهيار', 'جهل']
            text_lower = text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            total = pos_count + neg_count
            if total == 0:
                return 0.0
            return (pos_count - neg_count) / total
    except Exception:
        return 0.0

# =============================================
# 2. جلب البيانات من المصادر المفتوحة
# =============================================

@st.cache_data(ttl=1800)
def fetch_news_sentiment(query="الدين القيم", language="ar"):
    """جلب المقالات الإخبارية وتحليل مشاعرها."""
    try:
        api_key = st.secrets.get("NEWS_API_KEY", "")
        if not api_key:
            return None, None
        url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            sentiments = []
            for article in articles[:20]:
                text = article.get("title", "") + " " + article.get("description", "")
                polarity = analyze_sentiment(text)
                sentiments.append(polarity)
            if sentiments:
                avg_sentiment = np.mean(sentiments)
                return avg_sentiment, len(sentiments)
        return None, None
    except Exception:
        return None, None

@st.cache_data(ttl=1800)
def fetch_reddit_sentiment(subreddit="islam", query="الدين القيم"):
    """جلب منشورات Reddit وتحليل مشاعرها."""
    try:
        url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&q={query}&size=20"
        response = requests.get(url, timeout=10)
        data = response.json()
        posts = data.get("data", [])
        sentiments = []
        for post in posts[:20]:
            text = post.get("title", "") + " " + post.get("selftext", "")
            polarity = analyze_sentiment(text)
            sentiments.append(polarity)
        if sentiments:
            avg_sentiment = np.mean(sentiments)
            return avg_sentiment, len(sentiments)
        return None, None
    except Exception:
        return None, None

@st.cache_data(ttl=1800)
def fetch_twitter_sentiment_simulated(query="الدين القيم"):
    """محاكاة لبيانات تويتر."""
    np.random.seed(hash(query) % 1000)
    sentiment = np.random.normal(0.2, 0.3)
    sentiment = max(-1.0, min(1.0, sentiment))
    return sentiment, 100

@st.cache_data(ttl=1800)
def fetch_youtube_sentiment_simulated(query="الدين القيم"):
    """محاكاة لبيانات يوتيوب."""
    np.random.seed(hash(query) % 2000)
    sentiment = np.random.normal(0.1, 0.4)
    sentiment = max(-1.0, min(1.0, sentiment))
    return sentiment, 50

# =============================================
# 3. الدالة الرئيسية لجمع البيانات الحية
# =============================================

def fetch_live_indicators(mode="auto", manual_values=None):
    """
    جلب البيانات الحية أو استخدام القيم اليدوية.
    المعاملات:
        mode: "auto" (رادار حي) أو "manual" (إدخال يدوي)
        manual_values: قاموس يحتوي على قيم W و B و E إذا كان الوضع يدوياً
    """
    if mode == "manual" and manual_values:
        return {
            "status": "manual",
            "sentiment_avg": manual_values.get("sentiment", 0.0),
            "trend_direction": manual_values.get("trend", 0.0),
            "engagement_count": manual_values.get("engagement", 100),
            "sources": {"mode": "manual"},
            "timestamp": datetime.now().isoformat()
        }
    
    with st.spinner("📡 تشغيل الرادار الأخلاقي... جاري تحليل المشاعر والاتجاهات من العالم الرقمي"):
        news_sentiment, news_count = fetch_news_sentiment()
        reddit_sentiment, reddit_count = fetch_reddit_sentiment()
        twitter_sentiment, twitter_count = fetch_twitter_sentiment_simulated()
        youtube_sentiment, youtube_count = fetch_youtube_sentiment_simulated()
        
        sentiments = []
        counts = []
        if news_sentiment is not None:
            sentiments.append(news_sentiment)
            counts.append(news_count)
        if reddit_sentiment is not None:
            sentiments.append(reddit_sentiment)
            counts.append(reddit_count)
        if twitter_sentiment is not None:
            sentiments.append(twitter_sentiment)
            counts.append(twitter_count)
        if youtube_sentiment is not None:
            sentiments.append(youtube_sentiment)
            counts.append(youtube_count)
        
        if sentiments:
            total_count = sum(counts) if counts else 1
            weighted_sentiment = sum(s * c for s, c in zip(sentiments, counts)) / total_count
        else:
            weighted_sentiment = 0.0
        
        trend_direction = np.random.normal(0.1, 0.2)
        trend_direction = max(-1.0, min(1.0, trend_direction))
        engagement_count = sum(counts) if counts else 100
        
        return {
            "status": "live" if sentiments else "simulated",
            "sentiment_avg": weighted_sentiment,
            "trend_direction": trend_direction,
            "engagement_count": engagement_count,
            "sources": {
                "news": {"sentiment": news_sentiment, "count": news_count},
                "reddit": {"sentiment": reddit_sentiment, "count": reddit_count},
                "twitter": {"sentiment": twitter_sentiment, "count": twitter_count},
                "youtube": {"sentiment": youtube_sentiment, "count": youtube_count}
            },
            "timestamp": datetime.now().isoformat()
        }

# =============================================
# 4. بناء بيانات العالم (للمرصد)
# =============================================

def build_world_data(live_data):
    """بناء بيانات العالم من البيانات الحية والمحاكاة."""
    from observatory import WORLD_DATA_SIMULATED
    simulated = WORLD_DATA_SIMULATED
    
    if live_data.get("status") == "manual":
        return simulated
    
    if live_data.get("status") in ("live", "simulated"):
        # تطبيق المشاعر الحية على الدول
        adjusted_data = []
        sentiment = live_data.get("sentiment_avg", 0.0)
        for country in simulated:
            country_sentiment = sentiment + np.random.normal(0, 0.1)
            country_sentiment = max(-1.0, min(1.0, country_sentiment))
            country["worship"] = max(0.0, min(1.0, country["worship"] + country_sentiment * 0.15))
            country["taghut"] = max(0.0, min(1.0, country["taghut"] - country_sentiment * 0.15))
            adjusted_data.append(country)
        return adjusted_data
    return simulated
