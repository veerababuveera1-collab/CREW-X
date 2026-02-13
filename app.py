import streamlit as st
import os
import requests
from crewai import Agent, Task, Crew, Process
from streamlit_lottie import st_lottie

# --- 1. Ultra-Modern CSS Styling ---
def apply_custom_design():
    st.markdown("""
        <style>
        /* Main Background */
        .stApp {
            background: radial-gradient(circle at top right, #1e1e2f, #11111d);
            color: #e0e0e0;
        }
        
        /* Glassmorphism Container */
        .main-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            margin-bottom: 25px;
        }

        /* Neon Branding */
        .neon-brand {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            letter-spacing: 5px;
            margin-bottom: 10px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.3);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            color: #000;
            border: none;
            padding: 15px 40px;
            border-radius: 12px;
            font-weight: 800;
            width: 100%;
            transition: all 0.4s;
            text-transform: uppercase;
        }
        
        div.stButton > button:hover {
            box-shadow: 0 0 25px rgba(0, 242, 254, 0.6);
            transform: scale(1.02);
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. Animations ---
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# --- UI Initial Settings ---
st.set_page_config(page_title="CREW-X | AI Intelligence", layout="wide", page_icon="⚡")
apply_custom_design()

# Branding
st.markdown("<h1 class='neon-brand'>CREW-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>Next-Gen Multi-Agent Research Framework</p>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=80)
    st.title("Settings")
    api_key = st.text_input("OpenAI API Key:", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.markdown("---")
    st.write("**Agents Active:**")
    st.success("✅ Researcher")
    st.success("✅ Writer")

# --- Main Layout ---
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🎯 Research Parameters")
    topic = st.text_input("టాపిక్ ఎంటర్ చేయండి:", placeholder="e.g. Impact of Quantum Computing")
    
    tone = st.selectbox("వ్యాసం యొక్క శైలి (Tone):", ["Professional", "Conversational", "Academic", "Creative"])
    
    language = st.radio("భాష (Language):", ["Tanglish (Telugu + English)", "Pure Telugu", "English"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    ai_anim = load_lottie("https://assets1.lottiefiles.com/packages/lf20_qpwb7taz.json")
    if ai_anim:
        st_lottie(ai_anim, height=250)
    
    start_engine = st.button("🚀 Execute Agents")

# --- Execution Logic ---
if start_engine:
    if not api_key:
        st.error("🚨 OpenAI API Key అవసరం!")
    elif not topic:
        st.warning("⚠️ దయచేసి ఒక టాపిక్ ఇవ్వండి.")
    else:
        try:
            with st.status("🏗️ CREW-X Engines Warming Up...", expanded=True) as status:
                
                # 1. Agents Definition
                researcher = Agent(
                    role='Lead Research Specialist',
                    goal=f'{topic} గురించి సమగ్రమైన డేటా సేకరించడం',
                    backstory="మీరు ఒక ప్రపంచ స్థాయి పరిశోధకులు. డేటాలో దాగి ఉన్న నిజాలను వెలికితీయడం మీ నైపుణ్యం.",
                    verbose=True
                )

                writer = Agent(
                    role='Senior Content Architect',
                    goal=f'రీసెర్చ్ డేటాను ఒక {tone} వ్యాసంగా మార్చడం',
                    backstory="మీరు సంక్లిష్టమైన విషయాలను చాలా ఆకర్షణీయంగా రాయగలరు.",
                    verbose=True
                )

                # 2. Task Definition
                task_research = Task(
                    description=f"{topic} మీద తాజా అప్‌డేట్స్ మరియు 5 ముఖ్యమైన ఫ్యాక్ట్స్ సేకరించు.",
                    agent=researcher,
                    expected_output="Detailed analysis with bullet points."
                )

                task_writing = Task(
                    description=f"రీసెర్చ్ ఆధారంగా {language} లో ఒక అద్భుతమైన వ్యాసం రాయి. టోన్ {tone} గా ఉండాలి.",
                    agent=writer,
                    expected_output="A structured 500-word article."
                )

                # 3. Crew Setup
                crew_x = Crew(
                    agents=[researcher, writer],
                    tasks=[task_research, task_writing],
                    process=Process.sequential
                )

                st.write("🔍 Researcher పని మొదలుపెట్టాడు...")
                result = crew_x.kickoff()
                
                status.update(label="✨ Analysis Complete!", state="complete", expanded=False)

            # --- Display Final Output ---
            st.markdown("### 📄 Intelligence Report")
            st.markdown(f'<div class="main-card">{result.raw}</div>', unsafe_allow_html=True)
            
            # Action Area
            st.download_button(
                label="📥 Download as Markdown",
                data=result.raw,
                file_name=f"CREW_X_{topic}.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Error encountered: {str(e)}")

# Footer
st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>CREW-X Intelligence Engine © 2026</p>", unsafe_allow_html=True)
