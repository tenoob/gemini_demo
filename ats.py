#application tracking system using gemini and prompt engineering

import base64
import io
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_bot_response(input,pdf,prompt):
    model = genai.GenerativeModel(model_name='gemini-pro-vision')
    response = model.generate_content([input,pdf[0],prompt])
    return response.text

def pdf_setup(file):
    #convert pdf to image
    if file is not None:
        image = pdf2image.convert_from_bytes(file.read())
        print(image)
        first_page = image[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


#streamlit app
st.set_page_config("ATS helper bot")
st.header("GEMini app")

input_text = st.text_area("Job description" , key="input")
uploaded_file = st.file_uploader("Upload resume(PDF)",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

if submit1:
    if uploaded_file is not None:
        pdf_content=pdf_setup(uploaded_file)
        response=get_bot_response(input_text,pdf_content,input_prompt1)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=pdf_setup(uploaded_file)
        response=get_bot_response(input_text,pdf_content,input_prompt3)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")