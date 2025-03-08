#import the framework
import streamlit as st
 

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


submitButton = st.button('Submit')