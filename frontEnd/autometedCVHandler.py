#import the library
import streamlit as st
import docx
from PyPDF2 import PdfReader


 

st.title('Automated CV Handler')

name = st.text_input('Name')
email = st.text_input('Email')
phone_number = st.text_input('Phone Number')

# upload cv as pdf or docx format 
upload_cv  = st.file_uploader('Upload your CV', type=['pdf', 'docx'])

if upload_cv is not None:
    #get file type
    file_type = upload_cv.type
    st.write(file_type)


 # Check if the file is a PDF or DOCX
    if file_type == "application/pdf":
        st.success("✅ Uploaded file is a PDF.")
        if upload_cv:
            st.write('File uploaded successfully')
            st.write(upload_cv.name)

            if upload_cv is not None:
                pdf_reader = PdfReader(upload_cv) # read your PDF file
                # extract the text data from your PDF file after looping through its pages with the .extract_text() method
                text_data= ""
                for page in pdf_reader.pages: # for loop method
                    text_data+= page.extract_text()
                    st.write(text_data) # view the text data
        else: 
            st.write('File uploaded unsuccessfull {check the file type}')

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        st.success("✅ Uploaded file is a DOCX.")

        doc = docx.Document(upload_cv) # read your DOCX file
        text_data = ""
        for paragraph in doc.paragraphs:
            text_data += paragraph.text
            st.write(text_data)


    else:
        st.error("❌ Unsupported file type. Please upload a PDF or DOCX.")
# check uploading process success or not 



submitButton = st.button('Submit')