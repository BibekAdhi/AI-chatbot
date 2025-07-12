#step1: setup ui with streamlit (model provider, model, system prompt, web search, query)

import streamlit as st

st.set_page_config(page_title="AI Agent", layout="centered")
st.title("My AI Agents")
st.write("Interact with the AI Agents!")

system_prompt=st.text_area("Define your AI Agent: ", height=71, placeholder="Type your system prompt here....")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]


provider=st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search=st.checkbox("Allow Web Search")

user_query=st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

API_URL= "http://127.0.0.1:9999/chat"

if st.button("Ask Agent"):
    if user_query.strip():
        import requests

        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                if "response" in response_data:
                    st.subheader("Agent Response")
                    st.markdown(f"**Final Response:** {response_data['response']}")
                else:
                    st.warning("No 'response' field found in the backend reply.")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a query before submitting.")






