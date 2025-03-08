#import the library
import streamlit as st
from PyPDF2 import PdfReader


 

st.title('Automated CV Handler')

name = st.text_input('Name')
email = st.text_input('Email')
phone_number = st.text_input('Phone Number')

# upload cv as pdf or docx format 
upload_cv  = st.file_uploader('Upload your CV', type=['pdf', 'docx'])

# check uploading process success or not 
if upload_cv:
    st.write('File uploaded successfully')
    st.write(upload_cv.name)
else: 
    st.write('File uploaded unsuccessfull {check the file type}')


# read the pdf file
if upload_cv is not None:
    pdf_reader = PdfReader(upload_cv) # read your PDF file
    # extract the text data from your PDF file after looping through its pages with the .extract_text() method
    text_data= ""
    for page in pdf_reader.pages: # for loop method
        text_data+= page.extract_text()
    
    st.write(text_data) # view the text data

submitButton = st.button('Submit')