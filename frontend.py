import streamlit as st
import requests
import json
import os

# File to store history
HISTORY_FILE = "chat_history.json"

# Function to load history from JSON file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Function to save history to JSON file
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Load history into session_state on app start
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_history()

# System prompt input
st.set_page_config(page_title="AI Agent", layout="centered")
st.title("My AI Agents")
st.write("Interact with the AI Agent!")

system_prompt = st.text_area(
    "Define your AI Agent:",
    height=71,
    placeholder="Type your system prompt here..."
)

# Only one Groq model
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile"]
selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)

allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="Ask Anything!"
)

API_URL = "http://127.0.0.1:9999/chat"

# Delete a single history item
if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

# Clear all history
def clear_all_history():
    st.session_state.chat_history = []
    save_history(st.session_state.chat_history)

# Show chat history in sidebar
st.sidebar.title("Chat History")
if st.session_state.chat_history:
    for idx, item in enumerate(reversed(st.session_state.chat_history)):
        history_index = len(st.session_state.chat_history) - 1 - idx  # Actual index
        with st.sidebar.expander(f"History #{history_index + 1}"):
            st.markdown(f"**System Prompt:** {item['system_prompt']}")
            st.markdown(f"**Query:** {item['query']}")
            st.markdown(f"**Response:** {item['response']}")

            # Delete button for this history
            if st.button(f"🗑️ Delete History #{history_index + 1}", key=f"delete_{history_index}"):
                st.session_state.delete_index = history_index

    # Button to clear all history
    if st.sidebar.button("🗑️ Clear All History"):
        clear_all_history()
        st.rerun()
else:
    st.sidebar.info("No history yet.")

# Actually delete the selected history outside of the loop
if st.session_state.delete_index is not None:
    del st.session_state.chat_history[st.session_state.delete_index]
    save_history(st.session_state.chat_history)
    st.session_state.delete_index = None
    st.rerun()

# Ask agent and save query/response/system_prompt
if st.button("Ask Agent"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": "Groq",  # Fixed provider as Groq
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                if "response" in response_data:
                    ai_response = response_data['response']

                    # Save to chat history
                    st.session_state.chat_history.append({
                        "system_prompt": system_prompt,
                        "query": user_query,
                        "response": ai_response
                    })
                    save_history(st.session_state.chat_history)

                    # Display the response
                    st.subheader("Agent Response")
                    st.markdown(f"**Final Response:** {ai_response}")
                else:
                    st.warning("No 'response' field found in the backend reply.")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a query before submitting.")
