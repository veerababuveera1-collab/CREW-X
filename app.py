import streamlit as st
import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from streamlit_lottie import st_lottie

# --- 1. System Environment Fixes ---
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sk-placeholder"

# --- 2. Advanced UI Styling ---
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
            font-weight: 800; font-size: 3.5rem; text-align: center; margin-bottom: 0px;
        }
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white; border-radius: 8px; border: none; padding: 12px 24px;
            font-weight: 600; width: 100%; transition: all 0.3s ease;
        }
        div.stButton > button:hover { transform: scale(1.01); box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3); }
        .output-box {
            background-color: #FFFFFF; padding: 25px; border-radius: 12px;
            border-left: 6px solid #2563EB; color: #1E293B; line-height: 1.8;
            box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)

def load_lottie(url):
    try: return requests.get(url).json()
    except: return None

# --- 3. App Initialization ---
st.set_page_config(page_title="CREW-X | Next-Gen AI", layout="wide", page_icon="⚡")
apply_ui_theme()

# Sidebar: Configuration
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    groq_api_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
    
    # NEW: Model Selection Dropdown
    selected_model = st.selectbox(
        "Intelligence Engine:",
        ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama-3.1-8b-instant"],
        help="70b is smarter for research; 8b is faster."
    )
    
    st.divider()
    st.markdown("### 🤖 Agent Status")
    st.success("Researcher Ready")
    st.success("Writer Ready")
    
    lottie_side = load_lottie("https://assets5.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
    if lottie_side: st_lottie(lottie_side, height=150)

# Main Header
st.markdown("<h1 class='title-text'>CREW-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 1.1rem;'>Autonomous Multi-Agent Intelligence Hub</p>", unsafe_allow_html=True)

# Layout
left_col, right_col = st.columns([1.5, 1], gap="large")

with left_col:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🎯 Research Parameters")
    topic = st.text_input("What would you like to research?", placeholder="e.g. The future of decentralized finance in 2030")
    
    c1, c2 = st.columns(2)
    with c1:
        tone = st.selectbox("Tone:", ["Professional", "Deep Technical", "Journalistic", "Concise"])
    with c2:
        length = st.select_slider("Target length:", options=[300, 500, 800, 1200])
    
    st.markdown('</div>', unsafe_allow_html=True)
    execute_btn = st.button("🚀 EXECUTE AGENTS")

with right_col:
    main_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_ai9m8yca.json")
    if main_anim: st_lottie(main_anim, height=350)

# --- 4. Logic Execution ---
if execute_btn:
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic:
        st.warning("Please provide a research topic.")
    else:
        try:
            with st.status(f"🧠 Powering up {selected_model}...", expanded=True) as status:
                
                # Initialize LLM with selected model
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name=selected_model,
                    temperature=0.3
                )

                # Agent Definitions
                researcher = Agent(
                    role='Lead Research Analyst',
                    goal=f'Conduct comprehensive data gathering on {topic}',
                    backstory="Expert at scanning vast information and finding hidden technical breakthroughs.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                writer = Agent(
                    role='Chief Editor',
                    goal=f'Synthesize research into a {tone} report of {length} words about {topic}',
                    backstory="Specialist in technical communication and high-impact writing.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # Task Definitions
                t1 = Task(
                    description=f"Research {topic}. Focus on 5 key trends and future implications.",
                    agent=researcher,
                    expected_output="A structured list of findings with data references."
                )

                t2 = Task(
                    description=f"Draft a {tone} article based on the research. Ensure it is roughly {length} words.",
                    agent=writer,
                    expected_output="A high-quality Markdown report ready for publishing."
                )

                # Crew Assembly
                crew = Crew(
                    agents=[researcher, writer],
                    tasks=[t1, t2],
                    process=Process.sequential,
                    memory=False, # Essential: Bypasses OpenAI Embeddings
                    verbose=True
                )

                st.write("📡 Agents are collaborating...")
                result = crew.kickoff()
                status.update(label="✅ Mission Accomplished!", state="complete", expanded=False)

            # Display Output
            st.markdown("### 📄 Intelligence Report")
            st.markdown(f'<div class="output-box">{result.raw}</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Markdown Report",
                data=result.raw,
                file_name=f"CREW_X_Report_{topic.replace(' ', '_')}.md"
            )

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
            st.info("Tip: If you see a 'Model Not Found' error, try switching the model in the sidebar.")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>CREW-X Intelligence Engine v2.0 | 2026 Edition</p>", unsafe_allow_html=True)
