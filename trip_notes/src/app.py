import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

st.set_page_config(
    page_title="Trip Notes AI",
    page_icon="✈️",
    layout="wide"
)

from src.storage import load_trips
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, client, MODEL, rag_ask
from src.rag import ensure_index
from src.tools import run_agent, TOOL_DEFINITIONS

# Initialize Session State
if "trips" not in st.session_state:
    st.session_state["trips"] = load_trips()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "search_history" not in st.session_state:
    st.session_state["search_history"] = []

if "agent_history" not in st.session_state:
    st.session_state["agent_history"] = []

ensure_index()

# Sidebar
st.sidebar.title("✈️ Trip Notes AI")
st.sidebar.caption("Powered by Atlas, your travel AI")

trip_collection = st.session_state["trips"]
trips_list = trip_collection.get_all()

if not trips_list:
    trip_names = ["(no trips yet)"]
    selected_trip_name = st.sidebar.selectbox("📍 Current trip", trip_names)
    selected_trip = None
else:
    trip_names = [trip.name for trip in trips_list]
    selected_trip_name = st.sidebar.selectbox("📍 Current trip", trip_names)
    selected_trip = next((t for t in trips_list if t.name == selected_trip_name), None)

if selected_trip:
    if selected_trip.notes:
        with st.sidebar.expander(f"📋 Notes ({len(selected_trip.notes)})"):
            for note in selected_trip.notes:
                st.markdown(f"• {note}")
        
        if st.sidebar.button("Generate Briefing"):
            with st.sidebar:
                with st.spinner("Generating briefing..."):
                    notes_text = "\n".join([f"- {note}" for note in selected_trip.notes])
                    prompt = f"Please provide a quick travel briefing for {selected_trip.name} based on the following notes:\n{notes_text}"
                    response = ask(prompt, system_instruction=TRAVEL_SYSTEM_PROMPT)
                st.markdown(response)
    else:
        st.sidebar.caption("No notes yet for this trip.")
        
        if st.sidebar.button("Generate Briefing"):
            st.sidebar.warning("Add some notes first.")

# Main area
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🔍 Search", "🤖 Agent"])

with tab1:
    st.subheader("Atlas — Your Travel AI")
    st.caption("Ask me anything about travel.")

    if st.button("Clear chat", key="clear_chat"):
        st.session_state["chat_history"] = []
        st.rerun()

    # Display chat history
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Atlas anything..."):
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        MAX_TURNS = 8
        messages = [{"role": "system", "content": TRAVEL_SYSTEM_PROMPT}]
        messages.extend(st.session_state["chat_history"][-(MAX_TURNS * 2):])

        with st.chat_message("assistant"):
            with st.spinner("Atlas is thinking..."):
                response = client.chat.completions.create(model=MODEL, messages=messages)
                content = response.choices[0].message.content
                st.markdown(content)
        
        st.session_state["chat_history"].append({"role": "assistant", "content": content})

with tab2:
    st.subheader("Search My Guides")
    st.caption("Answers grounded in your guides/ documents.")

    if st.button("Clear search", key="clear_search"):
        st.session_state["search_history"] = []
        st.rerun()

    # Display search history
    for message in st.session_state["search_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if search_input := st.chat_input("Search your guides...", key="search_input"):
        st.session_state["search_history"].append({"role": "user", "content": search_input})
        with st.chat_message("user"):
            st.markdown(search_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching guides..."):
                response = rag_ask(search_input)
                st.markdown(response)
        
        st.session_state["search_history"].append({"role": "assistant", "content": response})

with tab3:
    st.subheader("AI Travel Agent")
    st.caption("The agent uses tools: budget calculation, live weather, and guide search.")

    agent_input = st.text_area(
        "Your question:",
        placeholder="e.g. I have $1200 for 8 days in Tokyo. Check the weather and break down my budget."
    )

    if st.button("Ask the Agent"):
        if agent_input.strip():
            with st.spinner("Agent is working..."):
                agent_answer = run_agent(agent_input)
            
            st.markdown(agent_answer)
            
            with st.expander("▶ Tools available to this agent"):
                for tool in TOOL_DEFINITIONS:
                    st.markdown(f"• `{tool['function']['name']}`")
                    
            st.session_state["agent_history"].append({
                "question": agent_input,
                "answer": agent_answer
            })
        else:
            st.warning("Please enter a question for the agent.")

    if st.session_state["agent_history"]:
        st.markdown("---")
        st.markdown("Previous queries this session:")
        for idx, entry in enumerate(reversed(st.session_state["agent_history"])):
            short_q = entry["question"][:60] + ("..." if len(entry["question"]) > 60 else "")
            with st.expander(f"▶ Q: {short_q}"):
                st.markdown(entry["answer"])
