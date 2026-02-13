import streamlit as st
import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from streamlit_lottie import st_lottie

# --- 1. Modern UI Configuration ---
def apply_ui_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #F8FAFC; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
        .main-container {
            background-color: #FFFFFF;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .title-text {
            font-family: 'Inter', sans-serif;
            color: #1E293B;
            font-weight: 800;
            font-size: 3rem;
            text-align: center;
            letter-spacing: -1px;
        }
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 12px 24px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        }
        .output-box {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 12px;
            border-left: 5px solid #2563EB;
            color: #334155;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

def load_lottie(url):
    try:
        return requests.get(url).json()
    except:
        return None

# --- 2. App Initialization ---
st.set_page_config(page_title="CREW-X | AI Hub", layout="wide", page_icon="⚡")
apply_ui_theme()

# --- 3. Sidebar (Control Panel) ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    groq_api_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
    st.caption("Get your free key at [console.groq.com](https://console.groq.com)")
    
    st.divider()
    st.markdown("### 🤖 Engine Status")
    st.success("Researcher Active")
    st.success("Writer Active")
    
    lottie_side = load_lottie("https://assets5.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
    if lottie_side:
        st_lottie(lottie_side, height=150)

# --- 4. Main Layout ---
st.markdown("<h1 class='title-text'>CREW-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; margin-top: -10px;'>High-Performance Multi-Agent Research Framework</p>", unsafe_allow_html=True)

left_col, right_col = st.columns([1.4, 1], gap="large")

with left_col:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🎯 Research Parameters")
    
    topic = st.text_input("Enter Topic:", placeholder="e.g. Next-gen solid-state batteries")
    
    c1, c2 = st.columns(2)
    with c1:
        tone = st.selectbox("Content Tone:", ["Professional", "Technical", "Creative", "Concise"])
    with c2:
        length = st.select_slider("Length (Words):", options=[300, 500, 800, 1000])
    
    st.markdown('</div>', unsafe_allow_html=True)
    execute_btn = st.button("🚀 Run Intelligence Engine")

with right_col:
    main_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_ai9m8yca.json")
    if main_anim:
        st_lottie(main_anim, height=300)

# --- 5. Logic Execution ---
if execute_btn:
    if not groq_api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a research topic.")
    else:
        try:
            # FIX: Set dummy OpenAI key and disable telemetry to prevent the error
            os.environ["OTEL_SDK_DISABLED"] = "true"
            if "OPENAI_API_KEY" not in os.environ:
                os.environ["OPENAI_API_KEY"] = "NA"

            with st.status("🧠 Agents are thinking...", expanded=True) as status:
                
                # LLM Setup - Explicitly define Groq
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="llama3-70b-8192",
                    temperature=0.5
                )

                # Agent Definitions
                researcher = Agent(
                    role='Senior Research Analyst',
                    goal=f'Conduct in-depth research about {topic}',
                    backstory="You are an expert researcher with access to complex data patterns.",
                    llm=llm, # Pass LLM explicitly
                    verbose=True,
                    allow_delegation=False
                )

                writer = Agent(
                    role='Technical Content Strategist',
                    goal=f'Write a {tone} report about {topic} based on research',
                    backstory="You specialize in translating complex research into engaging articles.",
                    llm=llm, # Pass LLM explicitly
                    verbose=True,
                    allow_delegation=False
                )

                # Task Definitions
                task1 = Task(
                    description=f"Analyze {topic} and provide 5 key breakthrough facts.",
                    agent=researcher,
                    expected_output="Bullet points of high-quality research data."
                )

                task2 = Task(
                    description=f"Using the research, write a {length}-word article in a {tone} tone.",
                    agent=writer,
                    expected_output="A professionally formatted Markdown article."
                )

                # Crew Assembly
                crew = Crew(
                    agents=[researcher, writer],
                    tasks=[task1, task2],
                    process=Process.sequential,
                    verbose=True
                )

                st.write("📡 Analyst gathering intelligence...")
                result = crew.kickoff()
                status.update(label="✅ Research Complete!", state="complete", expanded=False)

            # Display Results
            st.markdown("### 📄 Final Intelligence Report")
            st.markdown(f'<div class="output-box">{result.raw}</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Report (.md)",
                data=result.raw,
                file_name=f"CREW_X_{topic.replace(' ', '_')}.md"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# --- 6. Footer ---
st.markdown("<br><hr><p style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>CREW-X Intelligence Engine © 2026 | Powered by Groq</p>", unsafe_allow_html=True)
