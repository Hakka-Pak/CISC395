import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

st.set_page_config(
    page_title="Trip Notes AI",
    page_icon="✈️",
    layout="wide"
)

from src.storage import load_trips
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, client

# Initialize Session State
if "trips" not in st.session_state:
    st.session_state["trips"] = load_trips()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "search_history" not in st.session_state:
    st.session_state["search_history"] = []

if "agent_history" not in st.session_state:
    st.session_state["agent_history"] = []

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
    st.info("Coming soon — Exercise 2")

with tab2:
    st.info("Coming soon — Exercise 3")

with tab3:
    st.info("Coming soon — Exercise 4")
