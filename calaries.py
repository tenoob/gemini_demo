#gemini lim app to get total calaries from image of the food passed to it

import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(prompt,image):
    model = genai.GenerativeModel(model_name="gemini-pro-vision")
    response = model.generate_content([prompt,image[0]])
    return response.text

def image_setup(file):
    if file is not None:
        # Read the file into bytes
        bytes_data = file.getvalue()

        image_parts = [
            {
                "mime_type": file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

#streamlit app
st.set_page_config("Calaries Counter bot")
st.header("GEMini app")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

        Also tell about whether the food is healthy or not, also mention the
        percentage split of the ration of carbohydrates, fats, fibers, suger and other important things related to diet

"""

## If submit button is clicked

if submit:
    image_data=image_setup(uploaded_file)
    response=get_response(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)

