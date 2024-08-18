from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini-pro model and get response
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Chatbot")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Input:", key="input")
submit = st.button("Submit")

if submit and user_input:
    response = get_gemini_response(user_input)

    # Add user query and response to chat history
    st.session_state['chat_history'].append(("you", user_input))
    st.subheader("The response is:")
    
    if response:
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Gemini", chunk.text))
    else:
        st.write("No response received. Please try again.")

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
