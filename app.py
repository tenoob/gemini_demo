from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-pro")
#fun to get response from gemini-pro model
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

#streamlit setup
st.set_page_config(page_title="QA demo")
st.header("GEmini QA Demo")

input = st.text_input("Input: ",key="input")
submit = st.button("Response")

if submit:
    response = get_gemini_response(input)
    st.write(response)