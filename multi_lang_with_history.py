#multi language llm with system message and history straming

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel(model_name="gemini-pro-vision")
chat_history = model.start_chat(history=[])

#get response from gemini-pro-vision
def get_response(input,image,prompt):
    response = chat_history.send_message([input,image,prompt],stream=True)
    return response


#streamlit setup
st.set_page_config(page_title="Gemini milti lang")
st.header("Gemnini App")

#initialze streamlit session-state
if 'history' not in st.session_state:
    st.session_state['history'] = []

input = st.text_input("Input Query", key='prompt')
uploaded_file = st.file_uploader("Upload the image")
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded image")

submit = st.button("Response")

system_message = """
        You are an export in Optical Character Recognition
        help with the uploaded image and answer some question based on that.
        """

if submit and uploaded_file:
    response = get_response(system_message,image,input)
    st.session_state['history'].append(("You",input))
    st.subheader("The response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['history'].append(("Bot",chunk.text))

    st.subheader("Convosation History")
    for role,text in st.session_state['history']:
        st.write(f"{role}: {text}")