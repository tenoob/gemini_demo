#gemini chat bot with history streaming

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-pro")
chat_history = model.start_chat(history=[])

#gemini model call and return response
def get_llm_response(query):
    response = chat_history.send_message(query,stream=True)
    return response


#streamit build
st.set_page_config(page_title="Gemini chatbot")
st.header("GEmini LLM chatbot with respose stream")

#initialize streamlit session-state for convosation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

input = st.text_input("Query: ", key='input')
submit = st.button("ASK query")

if input and submit:
    response = get_llm_response(input)

    #adding input to session-state
    st.session_state['history'].append(("Que",input))
    st.subheader("Response: ")
    for chunk in response:
        st.write(chunk.text)
        #adding response to session-state
        st.session_state['history'].append(("Ans",chunk.text))
    
    st.subheader("Convosation History:")
    for role, text in st.session_state['history']:
        st.write(f"{role}: {text}")
        

