"""
==========================================================================
🌌 THE COSMIC COMMAND CENTER – THE MIZAN THEORY PLATFORM
==========================================================================
Author:     Ali Adel Alatifi
License:    MIT License
Platform:   Streamlit
Repository: https://github.com/your-repo/mizan-theory
==========================================================================
Description:
The complete platform for simulating the Divine Equation S = W × B.
Includes: Strategic Advisor, National Dashboard, Society Lab,
and Civilizations Clash Simulator.
==========================================================================
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
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
# Main Title
# =============================================
st.title("🌌 The Cosmic Command Center")
st.markdown("### The Mizan Theory Platform – S = W × B | Author: Ali Adel Alatifi")
st.markdown("---")

# =============================================
# Core Simulation Engine (Standard)
# =============================================
def run_standard_simulation(W0, B0, E0, years=200, lag=25):
    """
    Runs the standard civilization simulation.
    
    Parameters:
    W0 (float): Initial loyalty value (0-1)
    B0 (float): Initial disavowal value (0-1)
    E0 (float): Initial empowerment value (0-1)
    years (int): Number of simulation years
    
    Returns:
    tuple: (W, B, S, E) arrays
    """
    W = np.zeros(years)
    B = np.zeros(years)
    S = np.zeros(years)
    E = np.zeros(years)
    
    W[0], B[0], E[0] = W0, B0, E0
    S[0] = W0 * B0
    
    for t in range(1, years):
        # Calculate Hardship (H) from previous Stability (S)
        H = 10 / (S[t-1] + 0.1)
        
        # Update W (Loyalty): Struggle between awakening and laziness
        dW = (0.08 * H) - (0.05 * E[t-1]) - (0.04 * (1 - B[t-1]))
        W[t] = max(0.0, min(1.0, W[t-1] + dW))
        
        # Update B (Disavowal): Struggle between luxury and renewal
        dB = (-0.04 * E[t-1]) + (0.01 * (1 - B[t-1]) * W[t-1] * (1 - W[t-1]))
        B[t] = max(0.0, min(1.0, B[t-1] + dB))
        
        # Calculate Stability (S)
        S[t] = W[t] * B[t]
        
        # Update E (Empowerment) with Lag Effect (Istidraj)
        past_idx = t - lag
        S_past = S[past_idx] if past_idx >= 0 else S[t]
        dE = 0.05 * (S_past - E[t-1])
        E[t] = max(0.0, min(1.0, E[t-1] + dE))
    
    return W, B, S, E
    # =============================================
# Sidebar – Module Navigation
# =============================================
st.sidebar.title("🧭 Command Modules")
module = st.sidebar.radio(
    "Select Module:",
    [
        "🏠 Main Command Center",
        "🧠 The Strategic Advisor",
        "🌍 National Dashboard",
        "👥 Society Lab",
        "⚔️ Civilizations Clash"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("*Cosmic Platform v7.0 – Ali Adel Alatifi*")

# =============================================
# Module 0: Main Command Center (Overview)
# =============================================
if module == "🏠 Main Command Center":
    st.header("🏠 Welcome to the Cosmic Command Center")
    st.markdown("""
    ### 🌌 The Mizan Theory – The Equation of Everything
    
    This is the ultimate control room. From here, you can access all modules:
    
    1.  **🧠 The Strategic Advisor**: Ask any question and receive intelligent answers with live simulations.
    2.  **🌍 National Dashboard**: Enter real-world indicators for any nation to diagnose its position on the Istidraj Map.
    3.  **👥 Society Lab**: Watch 500 individuals interact in a virtual society governed by S = W × B.
    4.  **⚔️ Civilizations Clash**: A virtual world of 6 nations competing, allying, and clashing.
    
    ---
    ### 📊 The Core Equation: S = W × B
    
    **S** = Existential Stability (tranquility, honor, empowerment).
    **W** = Loyalty to God (faith, righteous deeds, justice).
    **B** = Disavowal of False Deities (struggle, chastity, independence).
    
    This is a **multiplicative** equation. If either factor is zero, stability is zero.
    It is derived from the Quran: {So whoever disbelieves in false deities and believes in Allah has grasped the most trustworthy handhold}.
    """)
    
    # Interactive Demo
    col1, col2, col3 = st.columns(3)
    with col1:
        W_demo = st.slider("W (Loyalty)", 0.0, 1.0, 0.8, 0.05, key="demo_W")
    with col2:
        B_demo = st.slider("B (Disavowal)", 0.0, 1.0, 0.8, 0.05, key="demo_B")
    with col3:
        S_demo = W_demo * B_demo
        st.metric("S (Stability)", f"{S_demo:.2f}")
    
    # Demonstration Simulation
    W_s, B_s, S_s, E_s = run_standard_simulation(W_demo, B_demo, 0.3, years=150)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(S_s, 'g-', linewidth=2, label='S (Stability)')
    ax.plot(E_s, 'b--', linewidth=2, label='E (Empowerment)')
    max_S = np.argmax(S_s)
    max_E = np.argmax(E_s)
    if max_S < max_E:
        ax.axvspan(max_S, max_E, alpha=0.2, color='red', label=f'Istidraj Gap ({max_E - max_S} years)')
    ax.set_title('Demonstration: The Civilization Cycle')
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    # =============================================
# Module 1: The Strategic Advisor (Smart Answer Engine)
# =============================================
elif module == "🧠 The Strategic Advisor":
    st.header("🧠 The Strategic Advisor – Smart Answer Engine")
    st.markdown("Ask any question in any field, and receive an intelligent, comprehensive answer.")

    # =============================================
    # 1. Encyclopedic Knowledge Base (Hundreds of Topics)
    # =============================================
    KNOWLEDGE_BASE = [
        # --- Religion & Spirituality ---
        ["Monotheism", ["monotheism", "tawhid", "god", "lord", "deity", "oneness", "one", "allahu", "ahad", "samad", "faith", "belief", "allah", "creator"],
         "Monotheism (Tawhid) is the foundation of Islam: declaring God's absolute Oneness in Lordship, Worship, and Names & Attributes. It is the belief that God is One, without partner, in His creation, dominion, and management. In the Mizan Theory, Monotheism is the letter 'Alif' (A=1), the origin of everything. Whoever truly unifies God (W=1) has grasped the Firm Handhold (Al-Urwah Al-Wuthqa). The Quran states: {Say, He is Allah, [who is] One}."],

        ["Prayer", ["prayer", "salat", "salah", "worship", "prostration", "ruku", "sujud", "rakah", "obligatory", "connection"],
         "Prayer (Salat) is the pillar of the faith, the daily connection between the servant and their Lord. In the Mizan Theory, prayer is the daily 'charging station' for Loyalty (W). Every rak'ah increases your Stability (S). The Prophet (PBUH) said: 'The coolness of my eyes is in prayer.' It is a practical application of the equation, combining physical submission with spiritual devotion."],

        ["Quran", ["quran", "koran", "book", "revelation", "scripture", "verses", "ayat", "surah", "divine", "recitation", "miracle"],
         "The Quran is the literal Word of God, revealed to Prophet Muhammad (PBUH) over 23 years. It is the eternal miracle. In the Mizan Theory, the Quran is the complete 'Operating Manual' for existence. Each letter has a numerical value (Abjad numerals), and every verse encapsulates an equation of the 'Deen Al-Qayyim' (The Upright Law). It is the ultimate guide for maximizing S (Stability)."],

        ["Repentance", ["repentance", "tawba", "forgiveness", "sin", "return", "regret", "astaghfirullah", "mercy", "turn back", "purification"],
         "Repentance (Tawba) in the Mizan Theory is a 'system reset'. When a person sins, their B (Disavowal) drops. Sincere repentance (regret + cessation + firm resolve) is a 'corrective leap' that restores the S trajectory. It is always available, as God states: {Except for those who repent, believe and do righteous work. For them Allah will replace their evil deeds with good.}"],

        # --- Science & Physics ---
        ["Gravity", ["gravity", "gravitation", "newton", "mass", "attraction", "force", "apple", "orbit", "planets"],
         "Gravity is the force of attraction between masses, famously formulated by Newton. In the Mizan Theory, Gravity is 'Loyalty' (W) in the material world. Just as masses 'loyally' attract each other, hearts are attracted by Loyalty to God. The equation F = G × (m1 × m2) / r² mirrors S = W × B; both describe a multiplicative attractive force that holds systems together."],

        ["Entropy", ["entropy", "chaos", "disorder", "thermodynamics", "energy", "heat", "second law", "randomness", "decay"],
         "Entropy is a measure of disorder in a closed system. In the Mizan Theory, entropy represents 'absent Disavowal' (B=0). When a nation loses its Disavowal (chastity, identity, independence), its entropy (chaos, moral decay) increases until it collapses. Maintaining high B is the only way to reverse entropy and maintain order."],

        ["Relativity", ["relativity", "einstein", "time", "space", "spacetime", "light speed", "e=mc2", "special", "general", "mass energy"],
         "Einstein's Theory of Relativity revolutionized our understanding of the universe. In the Mizan Theory, the equation E=mc² mirrors S=W×B. Energy (E) is latent within mass (m), just as Empowerment (E) is latent within Stability (S). The speed of light (c) is a constant, just as the Divine Constants (the 14 letters of the Quranic openings) govern the moral universe."],

        # --- Philosophy & Psychology ---
        ["Happiness", ["happiness", "joy", "pleasure", "contentment", "satisfaction", "bliss", "happy", "radiance", "delight", "rida", "sakinah"],
         "True happiness is not in wealth or fame, but in achieving 'Existential Stability' (S=W×B). When a person is loyal to God (W) and disavows their ego (B), they feel tranquility (Sakinah). God states: {Verily, in the remembrance of Allah do hearts find rest}. It is an internal state resulting from a balanced equation."],

        ["Anxiety", ["anxiety", "stress", "fear", "depression", "worry", "sadness", "mental", "peace", "tranquility", "mental health", "khawf"],
         "Anxiety is a state of 'low Stability' (S). In the Mizan Theory, anxiety occurs when W (Loyalty/Trust in God) is low, or when B (Disavowal from fearing creation) is low. The cure is to increase W through remembrance (Dhikr) and trust (Tawakkul), and to increase B by liberating oneself from the fear of created beings. God states: {Who have believed and whose hearts have rest in the remembrance of God.}"],

        ["Meaning of Life", ["meaning", "purpose", "goal", "life", "existence", "why are we here", "philosophy", "teleology", "aim", "reason"],
         "According to the Mizan Theory, the meaning of life is 'Ibadah' (worship), which is the practical application of the equation S=W×B. God states: {And I did not create the jinn and mankind except to worship Me.} Worship is not merely ritual; it is a comprehensive existential state: to be loyal to God (W) in everything, and to disavow all false deities (B)."],

        # --- History & Civilization ---
        ["Civilization Cycle", ["civilization", "cycle", "rise", "fall", "history", "empire", "decline", "collapse", "ibn khaldun", "pattern", "nation", "state"],
         "The Civilization Cycle passes through four phases: 1. Rise (High W & B), 2. Peak (Stability), 3. Istidraj (W & B collapse, but E remains high), 4. Collapse (E crashes). This cycle is governed by S = W × B. All civilizations founded on 'Loyalty to God' and 'Disavowal of Falsehood' endured. Those that neglected W or B collapsed. This is an immutable divine law."],

        ["Islamic Golden Age", ["islamic", "golden", "age", "abbasid", "umayyad", "science", "civilization", "golden age", "renaissance", "baghdad", "cordoba"],
         "The Islamic Golden Age (8th-13th centuries) was a model of the 'Mizan'. It had W=1 (justice, science, worship) and B=1 (independence, military strength, identity). When the equation became unbalanced (luxury, injustice, dependence on foreign elements), the decline began. This is a historical proof of the Mizan Theory."],

        ["Fall of Al-Andalus", ["andalus", "spain", "granada", "fall", "muslim", "europe", "reconquista", "decline", "last sigh"],
         "The Fall of Al-Andalus (1492 CE) is a historical case study in 'Istidraj'. Al-Andalus appeared powerful externally (high E), but W and B had collapsed (disunity, alliance with enemies, luxury). After decades of Istidraj, it fell suddenly. This is the law of the Mizan: {So when they forgot that by which they had been reminded, We opened to them the doors of every [good] thing... We seized them suddenly.}"],

        # --- Technology & Ethics ---
        ["Artificial Intelligence", ["artificial", "intelligence", "ai", "machine learning", "robot", "chatgpt", "deep learning", "neural", "algorithm", "automation"],
         "Artificial Intelligence (AI) is a double-edged sword. In the Mizan Theory, its value equals W(Programmer) × B(Programmer). If programmed for good (W=1) with ethical constraints (B=1), it is a blessing. If programmed for evil (W=-1), it becomes a force for tyranny (Dajjal). The current application you are using is a 'Smart Advisor' operating on this very Mizan Equation!"],

        # --- Health & Well-being ---
        ["Mental Health", ["mental", "health", "wellness", "balance", "therapy", "well-being", "psychological", "mind", "healthy", "brain"],
         "Mental Health in the Mizan Theory is 'S' (Stability). The higher W (faith, hope) and B (resilience, boundaries), the better the mental health. Therapy involves a 'recalibration' of the equation—increasing spiritual connection and psychological defenses. God states: {And whoever turns away from My remembrance – indeed, he will have a depressed [i.e., difficult] life.}"]
    ]

    # =============================================
    # 2. Intelligent Inference Engine
    # =============================================
    def smart_analyze(query, knowledge_base):
        """Analyzes the query and searches the knowledge base for the best match."""
        q = query.lower()
        best_match = None
        best_score = 0

        for entry in knowledge_base:
            score = 0
            for kw in entry[1]:
                if kw.lower() in q:
                    score += 3
                for qw in q.split():
                    if len(kw) > 3 and len(qw) > 2:
                        if kw.lower().startswith(qw.lower()) or qw.lower().startswith(kw.lower()):
                            score += 1
            if score > best_score:
                best_score = score
                best_match = entry

        return best_match, best_score

    # =============================================
    # 3. User Interface
    # =============================================
    user_q = st.text_input(
        "✍️ Ask any question:",
        placeholder="Example: What is monotheism? How do I overcome anxiety? What is gravity?"
    )

    if user_q:
        with st.spinner("🧠 The Strategic Advisor is analyzing your question..."):
            best_match, score = smart_analyze(user_q, KNOWLEDGE_BASE)

            if best_match and score > 1:
                st.success(f"💡 **Strategic Advisor's Answer:** {best_match[2]}")
            else:
                st.info("🤔 I couldn't find a specific answer in my knowledge base. Try asking about: religion, philosophy, physics, history, technology, or psychology.")

            # Extract scenario for demonstration simulation
            W0, B0, E0 = 0.5, 0.5, 0.3
            q_lower = user_q.lower()
            if any(w in q_lower for w in ["istidraj", "luxury", "rich", "affluent", "decadent", "decline"]):
                W0, B0, E0 = 0.3, 0.3, 0.9
            elif any(w in q_lower for w in ["rising", "strong", "faith", "early", "beginning", "startup", "rise"]):
                W0, B0, E0 = 0.9, 0.9, 0.1
            elif any(w in q_lower for w in ["individual", "self", "personal", "anxiety", "happy", "mental"]):
                W0, B0, E0 = 0.6, 0.5, 0.2
            elif any(w in q_lower for w in ["injustice", "tyranny", "oppression", "dictator", "corrupt"]):
                W0, B0, E0 = 0.2, 0.7, 0.8

            # Run simulation
            W_s, B_s, S_s, E_s = run_standard_simulation(W0, B0, E0)
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.plot(S_s, 'g-', label='S (Stability)')
            ax.plot(E_s, 'b--', label='E (Empowerment)')
            max_S = np.argmax(S_s)
            max_E = np.argmax(E_s)
            if max_S < max_E:
                ax.axvspan(max_S, max_E, alpha=0.2, color='red', label=f'Istidraj Gap ({max_E - max_S} years)')
            ax.set_title('Live Simulation: Civilization Cycle Based on Your Query')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 1.05)
            st.pyplot(fig)
            # =============================================
# Module 2: National Dashboard (Digital Twin)
# =============================================
elif module == "🌍 National Dashboard":
    st.header("🌍 National Dashboard – The Digital Twin")
    st.markdown("Enter real-world indicators for any nation to diagnose its position on the Istidraj Map and forecast its future.")

    # =============================================
    # 1. Indicator Input
    # =============================================
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("W Indicators (Loyalty / Justice)")
        rule_of_law = st.slider("Rule of Law", 0.0, 1.0, 0.5, 0.05, help="The extent to which agents have confidence in and abide by the rules of society.")
        education = st.slider("Education & Values", 0.0, 1.0, 0.5, 0.05, help="Quality of education and moral value transmission.")
        family_stability = st.slider("Family Stability", 0.0, 1.0, 0.5, 0.05, help="Strength of the family unit and divorce rates.")

    with col2:
        st.subheader("B Indicators (Disavowal / Independence)")
        corruption_control = st.slider("Control of Corruption", 0.0, 1.0, 0.5, 0.05, help="The extent to which public power is exercised for private gain.")
        justice_index = st.slider("Justice & Equality", 0.0, 1.0, 0.5, 0.05, help="Fairness and equality before the law.")
        economic_power = st.slider("Economic Strength", 0.0, 1.0, 0.6, 0.05, help="Overall economic output, innovation, and independence from foreign debt.")

    # =============================================
    # 2. Calculate W, B, S from indicators
    # =============================================
    W0 = (rule_of_law + education + family_stability) / 3
    B0 = (corruption_control + justice_index + (1 - (1 - rule_of_law))) / 3
    E0 = economic_power
    S0 = W0 * B0

    # Determine national status
    if S0 > 0.7:
        status = "🟢 Rising Power"
        advice = "The nation is in a strong position. Maintain high W and B. Beware of the fitnah of wealth and luxury."
    elif S0 > 0.4:
        status = "🟡 Precarious Balance"
        advice = "The nation is at a crossroads. Immediately strengthen B (independence) by reducing foreign dependency and corruption."
    elif S0 > 0.2:
        status = "🟠 Entering the Istidraj Zone"
        advice = "DANGER! Material empowerment (E) may appear high, but collapse is imminent. Immediately reform the judiciary (W) and fight corruption (B)."
    else:
        status = "🔴 On the Brink of Collapse"
        advice = "Collapse is near. Nothing remains but sincere repentance and a complete return to the divine equation."

    # =============================================
    # 3. Display Metrics
    # =============================================
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("W (Loyalty)", f"{W0:.2f}")
    col2.metric("B (Disavowal)", f"{B0:.2f}")
    col3.metric("S (Stability)", f"{S0:.2f}")
    col4.metric("E (Empowerment)", f"{E0:.2f}")

    st.markdown(f"### {status}")
    st.warning(advice)

    # =============================================
    # 4. Run Simulation & Forecast
    # =============================================
    if st.button("🚀 Run Simulation & Forecast Future", type="primary", use_container_width=True):
        W_s, B_s, S_s, E_s = run_standard_simulation(W0, B0, E0, years=100)

        # Find turning points
        max_S_idx = np.argmax(S_s)
        max_E_idx = np.argmax(E_s)
        collapse_year = None
        for t in range(max_S_idx, len(S_s)):
            if E_s[t] < 0.3:
                collapse_year = t
                break

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Chart 1: Civilization Cycle
        ax = axes[0]
        ax.plot(S_s, 'g-', label='S (Stability)', linewidth=2)
        ax.plot(E_s, 'b--', label='E (Empowerment)', linewidth=2)
        if max_S_idx < max_E_idx:
            ax.axvspan(max_S_idx, max_E_idx, alpha=0.2, color='red', label=f'Istidraj Zone ({max_E_idx - max_S_idx} years)')
        if collapse_year:
            ax.axvline(x=collapse_year, color='red', linestyle='--', linewidth=2, label=f'Collapse Forecast (Year {collapse_year})')
        ax.set_title('National Future Forecast')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.05)

        # Chart 2: Current Position on W-B Map
        ax = axes[1]
        ax.axhline(0.5, color='gray', ls=':')
        ax.axvline(0.5, color='gray', ls=':')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel('B (Disavowal)')
        ax.set_ylabel('W (Loyalty)')
        ax.set_title('Current National Position in (W, B) Space')
        ax.scatter(B0, W0, s=500, c='red', edgecolors='black', linewidth=2, zorder=10)
        ax.text(B0 + 0.05, W0 + 0.05, 'Current Position', fontsize=12)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)

        # Print analytical report
        gap = max_E_idx - max_S_idx if max_S_idx < max_E_idx else 0
        st.info(f"""
        📊 **National Forecast Report:**
        
        - **Current W (Loyalty):** {W0:.2f}
        - **Current B (Disavowal):** {B0:.2f}
        - **Current S (Stability):** {S0:.2f}
        - **Istidraj Gap:** {gap} years
        
        {"⚠️ Collapse forecast around year: " + str(collapse_year) if collapse_year else "✅ No collapse forecast in the near term."}
        
        🛠️ **Roadmap to Recovery:**
        1. To increase W: Reform the judiciary, support the family unit, uphold freedom of belief.
        2. To increase B: Fight corruption, achieve justice, and secure economic independence.
        """)
        # =============================================
# Module 3: Society Lab (Agent-Based Model)
# =============================================
elif module == "👥 Society Lab":
    st.header("👥 Society Lab – Agent-Based Model")
    st.markdown("Watch 500 agents interact in a virtual society governed by S = W × B. Observe how goodness and corruption spread.")

    # =============================================
    # 1. Simulation Controls
    # =============================================
    col1, col2, col3 = st.columns(3)
    with col1:
        pop_size = st.slider("Population Size", 100, 800, 400, 50, help="Number of agents in the virtual society.")
    with col2:
        influence_radius = st.slider("Influence Radius", 1.0, 5.0, 2.5, 0.5, help="Distance within which an agent influences their neighbors.")
    with col3:
        simulation_steps = st.slider("Simulation Years", 10, 100, 50, 10, help="Number of years to simulate.")

    # =============================================
    # 2. Helper Functions
    # =============================================
    def initialize_society(size):
        """Initialize a society with random W and B values."""
        np.random.seed(42)
        W = np.random.uniform(0.3, 0.9, size)
        B = np.random.uniform(0.3, 0.9, size)
        pos_x = np.random.randint(0, 30, size)
        pos_y = np.random.randint(0, 30, size)
        return W, B, pos_x, pos_y

    def classify_agent(w, b):
        """Classify an agent based on W and B values."""
        if w >= 0.6 and b >= 0.6:
            return "saint"
        elif w < 0.4 and b < 0.4:
            return "hypocrite"
        elif w >= 0.5 and b < 0.4:
            return "weak_disavowal"
        elif w < 0.4 and b >= 0.5:
            return "harsh"
        else:
            return "average"

    # =============================================
    # 3. Run Simulation
    # =============================================
    if st.button("▶️ Start Simulation", type="primary", use_container_width=True):
        W, B, pos_x, pos_y = initialize_society(pop_size)
        
        # Track history
        history_W = np.zeros(simulation_steps)
        history_B = np.zeros(simulation_steps)
        history_S = np.zeros(simulation_steps)
        history_saints = np.zeros(simulation_steps)
        history_hypocrites = np.zeros(simulation_steps)

        for step in range(simulation_steps):
            new_W = W.copy()
            new_B = B.copy()
            
            for i in range(pop_size):
                # Find neighbors within influence radius
                distances = np.sqrt((pos_x - pos_x[i])**2 + (pos_y - pos_y[i])**2)
                neighbors = np.where(distances < influence_radius)[0]
                neighbors = neighbors[neighbors != i]
                
                if len(neighbors) > 0:
                    local_W = np.mean(W[neighbors])
                    local_B = np.mean(B[neighbors])
                    # Faith contagion
                    new_W[i] += 0.02 * (local_W - W[i])
                    new_B[i] += 0.02 * (local_B - B[i])
                
                # Personal fluctuations
                new_W[i] += 0.01 * (np.random.rand() - 0.5)
                new_B[i] += 0.01 * (np.random.rand() - 0.5)
                
                # Laziness for the comfortable
                if W[i] > 0.7 and B[i] > 0.7:
                    new_B[i] -= 0.005 * np.random.rand()
                
                # Clamp values
                new_W[i] = max(0.05, min(1.0, new_W[i]))
                new_B[i] = max(0.05, min(1.0, new_B[i]))
            
            W = new_W
            B = new_B
            
            # Move agents slightly
            pos_x = pos_x + np.random.randint(-1, 2, pop_size)
            pos_y = pos_y + np.random.randint(-1, 2, pop_size)
            pos_x = np.clip(pos_x, 0, 29)
            pos_y = np.clip(pos_y, 0, 29)
            
            # Record history
            history_W[step] = np.mean(W)
            history_B[step] = np.mean(B)
            history_S[step] = np.mean(W * B)
            
            # Classify agents
            classifications = [classify_agent(W[i], B[i]) for i in range(pop_size)]
            history_saints[step] = sum(1 for c in classifications if c == "saint")
            history_hypocrites[step] = sum(1 for c in classifications if c == "hypocrite")

        # =============================================
        # 4. Visualize Results
        # =============================================
        final_classifications = [classify_agent(W[i], B[i]) for i in range(pop_size)]
        saints_mask = np.array([c == "saint" for c in final_classifications])
        hypocrites_mask = np.array([c == "hypocrite" for c in final_classifications])
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Map of the society
        ax = axes[0]
        ax.scatter(pos_x[saints_mask], pos_y[saints_mask], c='green', s=30, alpha=0.7, label='Saints')
        ax.scatter(pos_x[hypocrites_mask], pos_y[hypocrites_mask], c='red', s=30, alpha=0.7, label='Hypocrites')
        others_mask = ~(saints_mask | hypocrites_mask)
        ax.scatter(pos_x[others_mask], pos_y[others_mask], c='gray', s=15, alpha=0.5, label='Average')
        ax.set_xlim(0, 29)
        ax.set_ylim(0, 29)
        ax.set_title(f'Society Map (Year {simulation_steps})')
        ax.legend()
        ax.grid(False)
        
        # Evolution of averages
        ax = axes[1]
        time_axis = np.arange(simulation_steps)
        ax.plot(time_axis, history_W, 'g-', label='Avg W')
        ax.plot(time_axis, history_B, 'r-', label='Avg B')
        ax.plot(time_axis, history_S, 'gold', linewidth=2, label='Avg S')
        ax.set_title('Society Evolution Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        
        # Population counts
        ax = axes[2]
        ax.plot(time_axis, history_saints, 'g-', label='Saints')
        ax.plot(time_axis, history_hypocrites, 'r-', label='Hypocrites')
        ax.set_title('Population Counts Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)
        
        # Display final statistics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Saints", f"{int(history_saints[-1])}")
        col2.metric("Total Hypocrites", f"{int(history_hypocrites[-1])}")
        col3.metric("Average S", f"{history_S[-1]:.3f}")
        col4.metric("Years Passed", f"{simulation_steps}")
        # =============================================
# Module 4: Civilizations Clash Simulator
# =============================================
elif module == "⚔️ Civilizations Clash":
    st.header("⚔️ Civilizations Clash Simulator")
    st.markdown("A virtual world of 6 nations competing, allying, and clashing according to the Mizan Equation S = W × B.")

    # =============================================
    # 1. Initialize World
    # =============================================
    def initialize_world():
        """Initialize the world with 6 distinct civilizations."""
        return [
            {"name": "Nation of Faith", "W": 0.9, "B": 0.9, "E": 0.1, "color": "green", "hist_S": [], "hist_E": []},
            {"name": "Nation of Luxury", "W": 0.3, "B": 0.2, "E": 0.9, "color": "gold", "hist_S": [], "hist_E": []},
            {"name": "Nation of Hypocrisy", "W": 0.5, "B": 0.5, "E": 0.5, "color": "gray", "hist_S": [], "hist_E": []},
            {"name": "The Tyrant Empire", "W": 0.1, "B": 0.9, "E": 0.85, "color": "red", "hist_S": [], "hist_E": []},
            {"name": "Nation of Knowledge", "W": 0.8, "B": 0.6, "E": 0.4, "color": "cyan", "hist_S": [], "hist_E": []},
            {"name": "Nation of Dependency", "W": 0.6, "B": 0.15, "E": 0.3, "color": "orange", "hist_S": [], "hist_E": []},
        ]

    # =============================================
    # 2. Step Function (Update World)
    # =============================================
    def step_world(nations):
        """Advance the world by one year."""
        for c in nations:
            W, B, E = c['W'], c['B'], c['E']
            
            # Internal dynamics (Mizan Equation)
            S = W * B
            H = 10 / (S + 0.1)
            
            # Natural change
            dW = 0.08 * H - 0.05 * E - 0.04 * (1 - B)
            dB = -0.04 * E + 0.01 * (1 - B) * W * (1 - W)
            dE = 0.05 * (S - E)
            
            W = max(0.01, min(1.0, W + dW))
            B = max(0.01, min(1.0, B + dB))
            E = max(0.01, min(1.0, E + dE))
            
            # Interactions with other nations
            for o in nations:
                if o['name'] == c['name']:
                    continue
                
                oS = o['W'] * o['B']
                
                # 1. Natural alliance (similar W and B attract)
                similarity = 1 - abs(S - oS)
                if similarity > 0.7:
                    W += 0.01 * similarity
                    B += 0.01 * similarity
                
                # 2. War (high B nations attack low B nations)
                if o['B'] > 0.7 and B < 0.4:
                    E -= 0.05 * o['B'] * (1 - B)
                    B -= 0.03
                
                # 3. Cultural invasion (high E nations erode B of others)
                if o['E'] > 0.7 and B < 0.6:
                    B -= 0.02 * o['E'] * (1 - B)
                    W -= 0.01 * o['E'] * (1 - W)
            
            # Random fluctuations
            W = max(0.01, min(1.0, W + np.random.uniform(-0.02, 0.02)))
            B = max(0.01, min(1.0, B + np.random.uniform(-0.02, 0.02)))
            E = max(0.01, min(1.0, E + np.random.uniform(-0.02, 0.02)))
            
            c['W'], c['B'], c['E'] = W, B, E
            c['hist_S'].append(W * B)
            c['hist_E'].append(E)
        
        return nations

    # =============================================
    # 3. Simulation Controls
    # =============================================
    sim_years = st.slider("Simulation Years", 20, 200, 80, 10)

    # =============================================
    # 4. Run Simulation
    # =============================================
    if st.button("▶️ Start Simulation", type="primary", use_container_width=True):
        world = initialize_world()
        
        for y in range(sim_years):
            world = step_world(world)
        
        # =============================================
        # 5. Visualize Results
        # =============================================
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Chart 1: Stability (S) Curves
        ax = axes[0]
        for c in world:
            ax.plot(c['hist_S'], color=c['color'], linewidth=2, label=c['name'])
        ax.set_title('Stability Curves (S) for Each Nation')
        ax.set_xlabel('Years')
        ax.set_ylabel('S')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.05)
        
        # Chart 2: Empowerment (E) Curves
        ax = axes[1]
        for c in world:
            ax.plot(c['hist_E'], color=c['color'], linewidth=2, linestyle='--', label=c['name'])
        ax.set_title('Empowerment Curves (E) for Each Nation')
        ax.set_xlabel('Years')
        ax.set_ylabel('E')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.05)
        
        # Chart 3: Current Position in W-B Space
        ax = axes[2]
        ax.axhline(0.5, color='gray', ls=':')
        ax.axvline(0.5, color='gray', ls=':')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel('B (Disavowal)')
        ax.set_ylabel('W (Loyalty)')
        ax.set_title(f'Current Position in (W, B) Space – Year {sim_years}')
        
        for c in world:
            S_current = c['W'] * c['B']
            ax.scatter(c['B'], c['W'], s=200, color=c['color'], edgecolors='black', linewidth=1.5, label=c['name'])
            ax.text(c['B'] + 0.03, c['W'] + 0.03, c['name'][:8], fontsize=8)
        
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Display final metrics
        cols = st.columns(len(world))
        for i, c in enumerate(world):
            S_final = c['W'] * c['B']
            cols[i].metric(c['name'], f"S={S_final:.2f}", f"W={c['W']:.2f} / B={c['B']:.2f}")

# =============================================
# Footer
# =============================================
st.markdown("---")
st.markdown("*The Cosmic Command Center – Mizan Theory Platform v7.0 – Ali Adel Alatifi*")
