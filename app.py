import streamlit as st
import os
import requests
from crewai import Agent, Task, Crew, Process
from streamlit_lottie import st_lottie

# --- 1. UI & Theme Configuration ---
def apply_modern_theme():
    st.markdown("""
        <style>
        /* Main page background */
        .stApp {
            background-color: #F4F7F9;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #E6E8EB;
        }

        /* Card container for parameters */
        .param-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #E6E8EB;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        /* Branding Text */
        .brand-title {
            font-family: 'Inter', sans-serif;
            color: #1A202C;
            font-weight: 800;
            font-size: 3rem;
            text-align: center;
            margin-bottom: 0px;
        }
        
        .brand-subtitle {
            text-align: center;
            color: #718096;
            font-size: 1rem;
            margin-bottom: 30px;
        }

        /* Custom Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #3182CE 0%, #2B6CB0 100%);
            color: white;
            border-radius: 10px;
            border: none;
            padding: 12px 24px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(49, 130, 206, 0.4);
        }

        /* Result Area */
        .report-box {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            border-left: 6px solid #3182CE;
            line-height: 1.7;
            color: #2D3748;
        }
        </style>
    """, unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- 2. Initial Setup ---
st.set_page_config(page_title="CREW-X | Next-Gen AI", layout="wide", page_icon="⚡")
apply_modern_theme()

# --- 3. Sidebar: Settings & Status ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    api_key = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...")
    
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.markdown("---")
    st.markdown("### 🤖 Agents Active")
    st.success("✅ Researcher")
    st.success("✅ Writer")
    
    st.markdown("---")
    lottie_sidebar = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
    if lottie_sidebar:
        st_lottie(lottie_sidebar, height=150)

# --- 4. Main Content Area ---
st.markdown("<h1 class='brand-title'>CREW-X</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>Next-Gen Multi-Agent Research Framework</p>", unsafe_allow_html=True)

col_input, col_anim = st.columns([1.5, 1], gap="large")

with col_input:
    st.markdown('<div class="param-card">', unsafe_allow_html=True)
    st.subheader("🎯 Research Parameters")
    
    topic = st.text_input("టాపిక్ ఎంటర్ చేయండి:", placeholder="ఉదా: Future of Agentic AI")
    
    c1, c2 = st.columns(2)
    with c1:
        tone = st.selectbox("వ్యాసం యొక్క శైలి (Tone):", ["Professional", "Conversational", "Academic", "Creative"])
    with c2:
        language = st.radio("భాష (Language):", ["Tanglish (Mix)", "Pure Telugu", "English"], horizontal=False)
    
    st.markdown('</div>', unsafe_allow_html=True)
    run_btn = st.button("🚀 Start Intelligence Engine")

with col_anim:
    lottie_main = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_ai9m8yca.json")
    if lottie_main:
        st_lottie(lottie_main, height=300)

# --- 5. Execution Logic ---
if run_btn:
    if not api_key:
        st.error("🚨 దయచేసి సైడ్‌బార్‌లో OpenAI API Key ఎంటర్ చేయండి!")
    elif not topic:
        st.warning("⚠️ దయచేసి ఒక టాపిక్ ఇవ్వండి!")
    else:
        try:
            with st.status("🧠 ఏజెంట్లు విశ్లేషిస్తున్నారు...", expanded=True) as status:
                
                # Agent Definitions
                researcher = Agent(
                    role='Senior Research Analyst',
                    goal=f'{topic} గురించి లోతైన సమాచారాన్ని సేకరించడం',
                    backstory="మీరు ఒక నిపుణులైన పరిశోధకులు. ఇంటర్నెట్ నుండి ఖచ్చితమైన సమాచారాన్ని వెలికితీస్తారు.",
                    verbose=True,
                    allow_delegation=False
                )

                writer = Agent(
                    role='Tech Content Strategist',
                    goal=f'రీసెర్చ్ డేటా ఆధారంగా {topic} పై {tone} వ్యాసం రాయడం',
                    backstory="మీరు క్లిష్టమైన విషయాలను సామాన్యులకు అర్థమయ్యేలా, ఆకర్షణీయంగా రాయగలరు.",
                    verbose=True,
                    allow_delegation=False
                )

                # Task Definitions
                t1 = Task(
                    description=f"{topic} గురించి 5 ముఖ్యమైన అప్‌డేట్స్ మరియు ఫ్యాక్ట్స్ సేకరించు.",
                    agent=researcher,
                    expected_output="వివరణాత్మకమైన బుల్లెట్ పాయింట్స్."
                )

                t2 = Task(
                    description=f"సేకరించిన సమాచారాన్ని ఉపయోగించి {language} భాషలో ఒక ప్రొఫెషనల్ వ్యాసం రాయి. టోన్ {tone} గా ఉండాలి.",
                    agent=writer,
                    expected_output="300-500 పదాల వ్యాసం."
                )

                # Crew Formation
                crew = Crew(
                    agents=[researcher, writer],
                    tasks=[t1, t2],
                    process=Process.sequential
                )

                st.write("📡 Researcher డేటాను సేకరిస్తున్నాడు...")
                result = crew.kickoff()
                status.update(label="✅ రీసెర్చ్ పూర్తయింది!", state="complete", expanded=False)

            # --- Results Display ---
            st.markdown("### 📝 Intelligence Report")
            st.markdown(f'<div class="report-box">{result.raw}</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Report",
                data=result.raw,
                file_name=f"CREW_X_{topic}.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# --- 6. Footer ---
st.markdown("<br><hr><p style='text-align: center; color: #A0AEC0; font-size: 0.9rem;'>CREW-X Intelligence Engine © 2026</p>", unsafe_allow_html=True)
