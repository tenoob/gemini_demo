#v2 of application tracking system using gemini and prompt engineering 

import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

from PIL import Image
import PyPDF2
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_bot_response(prompt):
    model = genai.GenerativeModel(model_name='gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def pdf_setup(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text


#streamlit app
st.set_page_config("ATS helper bot")
st.header("GEMini app")

input_text = st.text_area("Job description" , key="input")
uploaded_file = st.file_uploader("Upload resume(PDF)",type=["pdf"])
submit = st.button("submit")

prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{input_text}

I want the response in one single string having the structure
{{"JD Match":"%",\n\n
"MissingKeywords:[]",\n\n
"Profile Summary":""}}
"""

if submit and uploaded_file is not None:
    text = pdf_setup(uploaded_file)
    response = get_bot_response(prompt=prompt)
    st.subheader("Response")
    st.write(response)
    st.subheader("Resume")
    st.write(text)