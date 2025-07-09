import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# loading .env file 
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function For Calling the llm and returning the response
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-2.5-pro')
    response=model.generate_content(input)
    return response.text

# Function For converting the provided resume into text using PyPDF2
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
input_prompt="""
# Instructions 
Hey, act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, generative ai engineer, machine learning, 
data science , data analyst and big data engineer. 

# Task is
Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on Job description and the missing keywords with high accuracy

# Input is
resume:{text}
description:{jd}

# Outcomes
I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Streamlit app code
st.title("Smart ATS Resume Checker")
st.text("Improve Your Resume")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")
submit = st.button("Submit")

# Code when user click on the submit button
if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)