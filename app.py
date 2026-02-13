import streamlit as st
import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from streamlit_lottie import st_lottie

# --- 1. System Environment Fixes ---
# These MUST stay at the top to prevent OpenAI errors
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sk-placeholder" 

# --- 2. Professional UI Styling ---
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
            font-weight: 800; font-size: 3rem; text-align: center;
        }
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white; border-radius: 8px; border: none; padding: 12px 24px;
            font-weight: 600; width: 100%;
        }
        .output-box {
            background-color: #F1F5F9; padding: 25px; border-radius: 12px;
            border-left: 5px solid #2563EB; color: #1E293B; line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

def load_lottie(url):
    try:
        return requests.get(url).json()
    except:
        return None

# --- 3. App Setup ---
st.set_page_config(page_title="CREW-X | AI Intelligence", layout="wide", page_icon="⚡")
apply_ui_theme()

# Sidebar Control Panel
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    groq_api_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
    st.caption("Get your free key at [console.groq.com](https://console.groq.com)")
    
    st.divider()
    st.markdown("### 🤖 Agent Status")
    st.success("Researcher Active")
    st.success("Writer Active")
    
    lottie_side = load_lottie("https://assets5.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
    if lottie_side:
        st_lottie(lottie_side, height=150)

# Main Branding
st.markdown("<h1 class='title-text'>CREW-X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>High-Performance Multi-Agent Research Framework</p>", unsafe_allow_html=True)

# UI Layout
left_col, right_col = st.columns([1.4, 1], gap="large")

with left_col:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🎯 Research Parameters")
    topic = st.text_input("Enter Research Topic:", placeholder="e.g. Advancements in Fusion Energy")
    
    c1, c2 = st.columns(2)
    with c1:
        tone = st.selectbox("Content Tone:", ["Professional", "Technical", "Conversational"])
    with c2:
        length = st.select_slider("Word Count:", options=[300, 500, 800])
    
    st.markdown('</div>', unsafe_allow_html=True)
    execute_btn = st.button("🚀 Execute Intelligence Engine")

with right_col:
    main_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_ai9m8yca.json")
    if main_anim:
        st_lottie(main_anim, height=300)

# --- 4. Logic Execution ---
if execute_btn:
    if not groq_api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a research topic.")
    else:
        try:
            with st.status("🧠 Agents are initializing...", expanded=True) as status:
                
                # Initialize LLM
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="llama3-70b-8192",
                    temperature=0.4
                )

                # Define Agents
                researcher = Agent(
                    role='Senior Research Analyst',
                    goal=f'Gather comprehensive insights on {topic}',
                    backstory="You are a meticulous researcher capable of distilling complex data.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                writer = Agent(
                    role='Content Strategist',
                    goal=f'Write a {tone} article based on the research for {topic}',
                    backstory="You are a professional writer who crafts engaging, factual content.",
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # Define Tasks
                task1 = Task(
                    description=f"Identify 5 critical breakthroughs and facts regarding {topic}.",
                    agent=researcher,
                    expected_output="A structured list of 5 major research findings."
                )

                task2 = Task(
                    description=f"Draft a {length}-word {tone} article based on the research findings.",
                    agent=writer,
                    expected_output="A polished Markdown article."
                )

                # Assemble Crew
                crew = Crew(
                    agents=[researcher, writer],
                    tasks=[task1, task2],
                    process=Process.sequential,
                    memory=False, # Disable memory to avoid OpenAI embedding calls
                    verbose=True
                )

                st.write("📡 Researcher is scanning for intelligence...")
                result = crew.kickoff()
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

            # Display Output
            st.markdown("### 📄 Generated Report")
            st.markdown(f'<div class="output-box">{result.raw}</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Report",
                data=result.raw,
                file_name=f"CREW_X_{topic.replace(' ', '_')}.md"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>CREW-X Intelligence Engine © 2026 | Powered by Groq Llama-3</p>", unsafe_allow_html=True)
