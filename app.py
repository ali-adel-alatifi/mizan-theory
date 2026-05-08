"""
==========================================================================
🌌 THE COSMIC COMMAND CENTER – THE MIZAN THEORY PLATFORM
==========================================================================
Author:     Ali Adel Alatifi
License:    MIT License
Platform:   Streamlit
Description: The complete platform for simulating the Divine Equation S = W × B.
Includes: Strategic Advisor, National Dashboard, Society Lab, and Civilizations Clash.
==========================================================================
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# =============================================
# Page Configuration
# =============================================
st.set_page_config(
    page_title="The Cosmic Command Center – Ali Adel Alatifi",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# 🧠 THE UNIFIED COSMIC ENGINE
# =============================================
def cosmic_engine(W0, B0, E0, years=200, lag=25):
    """
    The single, unified engine for all modules.
    It runs the standard Mizan simulation S = W × B.
    """
    W = np.zeros(years)
    B = np.zeros(years)
    S = np.zeros(years)
    E = np.zeros(years)
    
    W[0], B[0], E[0] = W0, B0, E0
    S[0] = W0 * B0
    
    for t in range(1, years):
        H = 10 / (S[t-1] + 0.1)
        
        dW = (0.08 * H) - (0.05 * E[t-1]) - (0.04 * (1 - B[t-1]))
        W[t] = np.clip(W[t-1] + dW, 0.01, 1.0)
        
        dB = (-0.04 * E[t-1]) + (0.01 * (1 - B[t-1]) * W[t-1] * (1 - W[t-1]))
        B[t] = np.clip(B[t-1] + dB, 0.01, 1.0)
        
        S[t] = W[t] * B[t]
        
        past_idx = t - lag
        S_past = S[past_idx] if past_idx >= 0 else S[t]
        dE = 0.05 * (S_past - E[t-1])
        E[t] = np.clip(E[t-1] + dE, 0.01, 1.0)
    
    return W, B, S, E

# =============================================
# 🧭 SIDEBAR – Command Modules
# =============================================
st.sidebar.title("🧭 Command Modules")
module = st.sidebar.radio(
    "Select Module:",
    [
        "🏠 Main Command Center",
        "🧠 The Strategic Advisor",
        "🌍 National Dashboard",
        "👥 Society Lab",
        "⚔️ Civilizations Clash",
        "🧭 The Existential Compass",
        "📜 The Akhirah Balance",
        "⚛️ Physics & Biology Lab",
        "🔥 The Battle Heatmap"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("*Cosmic Platform v8.0 – Ali Adel Alatifi*")

# =============================================
# MODULE 0: THE COSMIC OVERVIEW
# =============================================
if module == "🏠 Main Command Center":
    st.header("🏠 The Cosmic Overview")
    st.markdown("""
    ### 🌌 The Mizan Theory – The Equation of Everything
    
    This is the ultimate control room. From here, you can access all modules:
    
    1.  **🧠 The Strategic Advisor**: Ask any question and receive intelligent answers.
    2.  **🌍 National Dashboard**: Diagnose any nation's position on the Istidraj Map.
    3.  **👥 Society Lab**: Watch 500 individuals interact in a virtual society.
    4.  **⚔️ Civilizations Clash**: A virtual world of 6 nations competing.
    
    ---
    ### 📊 The Core Equation: S = W × B
    **S** = Existential Stability. **W** = Loyalty to God. **B** = Disavowal of False Deities.
    """)
    
    # Interactive Demo
    col1, col2, col3 = st.columns(3)
    with col1: W_demo = st.slider("W (Loyalty)", 0.0, 1.0, 0.8, 0.05, key="demo_W")
    with col2: B_demo = st.slider("B (Disavowal)", 0.0, 1.0, 0.8, 0.05, key="demo_B")
    with col3: st.metric("S (Stability)", f"{W_demo * B_demo:.2f}")

    if st.button("🚀 Run Quick Simulation", use_container_width=True):
        W_s, B_s, S_s, E_s = cosmic_engine(W_demo, B_demo, 0.3, 150)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(S_s, 'g-', label='S (Stability)')
        ax.plot(E_s, 'b--', label='E (Empowerment)')
        max_S = np.argmax(S_s); max_E = np.argmax(E_s)
        if max_S < max_E:
            ax.axvspan(max_S, max_E, alpha=0.2, color='red', label=f'Istidraj Gap ({max_E - max_S} years)')
        ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0, 1.05)
        st.pyplot(fig)

# =============================================
# MODULE 1: THE STRATEGIC ADVISOR
# =============================================
elif module == "🧠 The Strategic Advisor":
    st.header("🧠 The Strategic Advisor")
    st.markdown("Ask any question and receive an intelligent answer with a live simulation.")
    
    user_q = st.text_input("✍️ Ask any question:", placeholder="Example: What is monotheism? How to overcome anxiety?")

    # Simple Knowledge Base
    knowledge = {
        "monotheism": "Monotheism (Tawhid) is the foundation of Islam. In the Mizan Theory, it is the 'Alif' (A=1), the origin of everything.",
        "prayer": "Prayer (Salat) is the daily 'charging station' for Loyalty (W). It is the pillar of the faith.",
        "anxiety": "Anxiety is a state of 'low Stability' (S). The cure is to increase W (Trust in God) and B (Disavowal from fearing creation).",
        "civilization": "All civilizations follow the Mizan cycle: Rise (High W&B), Peak, Istidraj (W&B collapse), and Collapse.",
    }
    
    if user_q:
        response = "I couldn't find a specific answer, but I can run a simulation based on your query."
        W0, B0 = 0.5, 0.5
        q = user_q.lower()
        for kw, ans in knowledge.items():
            if kw in q:
                response = ans
                break
        if "istidraj" in q or "collapse" in q: W0, B0 = 0.3, 0.3
        if "rise" in q or "faith" in q: W0, B0 = 0.9, 0.9
        
        st.success(response)
        W_s, B_s, S_s, E_s = cosmic_engine(W0, B0, 0.3, 100)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(S_s, 'g-', label='S'); ax.plot(E_s, 'b--', label='E')
        ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0, 1.05)
        st.pyplot(fig)

# =============================================
# MODULE 2: NATIONAL DASHBOARD
# =============================================
elif module == "🌍 National Dashboard":
    st.header("🌍 National Dashboard – The Digital Twin")
    st.markdown("Diagnose any nation's position on the Istidraj Map.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("W (Loyalty)")
        rule_of_law = st.slider("Rule of Law", 0.0, 1.0, 0.5)
        education = st.slider("Education & Values", 0.0, 1.0, 0.5)
    with col2:
        st.subheader("B (Disavowal)")
        corruption = st.slider("Control of Corruption", 0.0, 1.0, 0.5)
        justice = st.slider("Justice & Equality", 0.0, 1.0, 0.5)
    
    W0 = (rule_of_law + education) / 2
    B0 = (corruption + justice) / 2
    S0 = W0 * B0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("W", f"{W0:.2f}"); col2.metric("B", f"{B0:.2f}"); col3.metric("S", f"{S0:.2f}")
    
    if st.button("🚀 Forecast Future", use_container_width=True):
        W_s, B_s, S_s, E_s = cosmic_engine(W0, B0, 0.5, 100)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(S_s, 'g-', label='S'); ax.plot(E_s, 'b--', label='E')
        ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0, 1.05)
        st.pyplot(fig)

# =============================================
# MODULE 3: SOCIETY LAB
# =============================================
elif module == "👥 Society Lab":
    st.header("👥 Society Lab – Agent-Based Model")
    st.markdown("Watch agents interact in a virtual society governed by S = W × B.")
    
    pop_size = st.slider("Population", 50, 300, 150)
    if st.button("▶️ Start Society Simulation", use_container_width=True):
        # Simple agent model
        W = np.random.uniform(0.3, 0.9, pop_size)
        B = np.random.uniform(0.3, 0.9, pop_size)
        
        for step in range(50):
            for i in range(pop_size):
                # Influence random neighbor
                j = random.randint(0, pop_size-1)
                W[i] += 0.02 * (W[j] - W[i])
                B[i] += 0.02 * (B[j] - B[i])
                W[i], B[i] = np.clip(W[i], 0.01, 1.0), np.clip(B[i], 0.01, 1.0)
        
        colors = []
        for i in range(pop_size):
            if W[i] > 0.6 and B[i] > 0.6: colors.append('gold')
            elif W[i] < 0.4 and B[i] < 0.4: colors.append('red')
            else: colors.append('gray')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(np.random.uniform(0, 30, pop_size), np.random.uniform(0, 30, pop_size), c=colors, s=40)
        ax.set_title('Society After 50 Years'); st.pyplot(fig)

# =============================================
# MODULE 4: CIVILIZATIONS CLASH
# =============================================
elif module == "⚔️ Civilizations Clash":
    st.header("⚔️ Civilizations Clash Simulator")
    st.markdown("6 nations competing according to S = W × B.")
    
    nations = [
        {"name": "Faith", "W": 0.9, "B": 0.9, "E": 0.1, "color": "green"},
        {"name": "Luxury", "W": 0.3, "B": 0.2, "E": 0.9, "color": "gold"},
        {"name": "Tyrant", "W": 0.1, "B": 0.9, "E": 0.85, "color": "red"},
        {"name": "Knowledge", "W": 0.8, "B": 0.6, "E": 0.4, "color": "cyan"},
    ]
    
    years = st.slider("Simulation Years", 20, 150, 60)
    
    if st.button("▶️ Start Clash Simulation", use_container_width=True):
        fig, ax = plt.subplots(figsize=(10, 6))
        for n in nations:
            W_s, B_s, S_s, E_s = cosmic_engine(n['W'], n['B'], n['E'], years)
            ax.plot(S_s, color=n['color'], label=n['name'])
        ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(0, 1.05)
        st.pyplot(fig)

# =============================================
# MODULES 5-8: SIMPLIFIED PLACEHOLDERS
# =============================================
elif module == "🧭 The Existential Compass":
    st.header("🧭 The Existential Compass")
    st.markdown("Discover your position in the W-B space.")
    W_val = st.slider("Your W Score", 0.0, 1.0, 0.5)
    B_val = st.slider("Your B Score", 0.0, 1.0, 0.5)
    st.metric("Your S (Stability)", f"{W_val * B_val:.2f}")

elif module == "📜 The Akhirah Balance":
    st.header("📜 The Akhirah Balance")
    hasanat = st.number_input("Total Hasanat", 0, 10000, 500)
    sayyiat = st.number_input("Total Sayyiat", 0, 10000, 300)
    balance = hasanat - sayyiat
    st.metric("Net Balance", balance, delta="Positive" if balance > 0 else "Negative")

elif module == "⚛️ Physics & Biology Lab":
    st.header("⚛️ Physics & Biology Lab")
    st.markdown("Explore the Mizan in physics, chemistry, and biology.")

elif module == "🔥 The Battle Heatmap":
    st.header("🔥 The Battle Heatmap")
    if st.button("Generate Heatmap", use_container_width=True):
        W_s, B_s, S_s, E_s = cosmic_engine(0.5, 0.5, 0.3, 100)
        heat_data = np.array([W_s, B_s, S_s, E_s])
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.imshow(heat_data, aspect='auto', cmap='RdYlGn', vmin=0, vmax=1)
        ax.set_yticks([0,1,2,3]); ax.set_yticklabels(['W','B','S','E'])
        st.pyplot(fig)

# =============================================
# Footer
# =============================================
st.markdown("---")
st.markdown("*The Cosmic Command Center – Mizan Theory Platform v8.0 – Ali Adel Alatifi*")
