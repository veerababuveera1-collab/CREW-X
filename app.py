import streamlit as st
import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from streamlit_lottie import st_lottie

# --- 1. STRICT ENVIRONMENT OVERRIDES ---
# Disables CrewAI telemetry and bypasses OpenAI key requirements
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sk-placeholder"

# --- 2. UI DESIGN SYSTEM ---
def apply_ui_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #F8FAFC; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
        .main-container {
            background-color: #FFFFFF; padding: 30px; border-radius: 12px;
            border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .title-text {
            font-family: 'Inter', sans-serif; color: #1E293B;
            font-weight: 800; font-size: 3.5rem; text-align: center;
        }
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white; border-radius: 8px; border: none; padding: 12px 24px;
            font-weight: 600; width: 100%; transition: 0.3s;
        }
        div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px rgba(37, 99, 235, 0.3); }
        .output-box {
            background-color: #FFFFFF; padding: 25px; border-radius: 12px;
            border-left: 6px solid #2563EB; color: #1E293B; line-height: 1.8;
            white-space: pre-wrap;
        }
        </style>
    """, unsafe_allow_html=True)

def load_lottie(url):
    try: return requests.get(url).json()
    except: return None

# --- 3. APP INITIALIZATION ---
st.set_page_config(page_title="CREW-X | AI Hub", layout="wide", page_icon="⚡")
apply_ui_theme()

# Sidebar: Control Panel
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    groq_api_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
    
    # 2026 Verified Stable Model Strings
    model_options = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama3-70b-8192",
        "llama3-8b-8192"
    ]
    selected_model = st.selectbox("Intelligence Engine:", model_options)
    st.caption("Note: If you get a 404 error, switch to 'llama3-70b-8192'.")
    
    st.divider()
    st.markdown("### 🤖 Agent Status")
    st.success("Researcher Online")
    st.success("Writer Online")
    
    lottie_sidebar = load_lottie("https://assets5.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
    if lottie_sidebar: st_lottie(lottie_sidebar, height=150)

# Branding
st.markdown("<h1 class='title-text'>CREW-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>Autonomous Multi-Agent Intelligence Hub</p>", unsafe_allow_html=True)

# Main Interface Layout
col_left, col_right = st.columns([1.5, 1], gap="large")

with col_left:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🎯 Research Parameters")
    topic = st.text_input("Define your research topic:", placeholder="e.g. Scalability of Layer 2 Blockchain Solutions")
    
    c1, c2 = st.columns(2)
    with c1:
        tone = st.selectbox("Content Tone:", ["Professional", "Technical", "Academic", "Journalistic"])
    with c2:
        length = st.select_slider("Target Length (Words):", options=[300, 500, 800, 1200])
    
    st.markdown('</div>', unsafe_allow_html=True)
    execute_btn = st.button("🚀 EXECUTE CREW")

with col_right:
    main_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_ai9m8yca.json")
    if main_anim: st_lottie(main_anim, height=350)

# --- 4. EXECUTION LOGIC ---
if execute_btn:
    if not groq_api_key:
        st.error("Please provide a valid Groq API Key.")
    elif not topic:
        st.warning("Please enter a research topic to proceed.")
    else:
        try:
            with st.status(f"🧠 Synchronizing with {selected_model}...", expanded=True) as status:
                
                # LLM Initialization
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name=selected_model,
                    temperature=0.3
                )

                # Agent: Researcher
                researcher = Agent(
                    role='Senior Data Scientist',
                    goal=f'Conduct deep-dive research into {topic}',
                    backstory="You are a world-class researcher. You synthesize complex information into actionable insights.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # Agent: Writer
                writer = Agent(
                    role='Technical Editor',
                    goal=f'Create a {tone} article about {topic} based on the researcher\'s findings',
                    backstory="You are a master of technical communication, capable of explaining anything to any audience.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # Task 1: Research
                research_task = Task(
                    description=f"Analyze {topic} and identify 5 groundbreaking trends or facts.",
                    agent=researcher,
                    expected_output="A list of 5 structured research findings with brief explanations."
                )

                # Task 2: Writing
                writing_task = Task(
                    description=f"Using the findings, write a {length}-word article in a {tone} tone.",
                    agent=writer,
                    expected_output="A professionally formatted Markdown report."
                )

                # Crew Assembly
                crew_x = Crew(
                    agents=[researcher, writer],
                    tasks=[research_task, writing_task],
                    process=Process.sequential,
                    memory=False, # Essential for Groq-only apps
                    verbose=True
                )

                st.write("📡 Crew members are collaborating in sequence...")
                result = crew_x.kickoff()
                status.update(label="✅ Mission Accomplished!", state="complete", expanded=False)

            # --- Display Final Output ---
            st.markdown("### 📄 Final Intelligence Report")
            st.markdown(f'<div class="output-box">{result.raw}</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Report (.md)",
                data=result.raw,
                file_name=f"CREW_X_{topic.replace(' ', '_')}.md"
            )

        except Exception as e:
            st.error(f"System Error: {str(e)}")
            st.info("💡 **Model Tip:** If you see a '404' or 'Not Found', try choosing **'llama3-70b-8192'** from the sidebar Settings.")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>CREW-X Intelligence Engine © 2026 | Powered by Groq</p>", unsafe_allow_html=True)
