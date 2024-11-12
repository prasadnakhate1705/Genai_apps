from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load gemini pro vision

model=genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, image, prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        byte_data = uploaded_file.getvalue()
        
        image_parts= [
            {
                'mime_type': uploaded_file.type,
                'data': byte_data
                
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    


st.set_page_config(page_title="Multi-Language Invoice Extracter")
st.header("MultiLanguage Invoice Extracter")
input=st.text_input("INput Prompt: ", key='Input')
uploaded_file= st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])

image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")  


input_prompt= '''
You are an expert in understanding invoices. we will upload an image of invoice and you will
have to answer any questions based on the uploaded invoice image
''' 

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response) 


    
 