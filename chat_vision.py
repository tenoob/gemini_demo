#using gemini-pro-vision llm model 
#input: text and image

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-pro-vision")
#fun to get response from gemini-pro model
def get_gemini_response(query,image):
    if input !="":
        response = model.generate_content([query,image])
    else:
        response = model.generate_content(image)
    return response.text

#streamlit setup
st.set_page_config(page_title="Gemini text-image demo")
st.header("GEmini Vision Demo")

input = st.text_input("Input: ",key="input")
uploaded_image = st.file_uploader("Choose image:")

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image")

submit = st.button("Describe the image")

if submit:
    response = get_gemini_response(input,image)
    st.write(response)