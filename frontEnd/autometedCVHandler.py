import streamlit as st
from PyPDF2 import PdfReader
import docx
import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

# function to authenticate google drive
def authenticate():
    gauth.settings['client_config_file'] = 'client_secret.json'
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile('client_secret.json')


# Function to extract text from PDF
def extract_text_from_pdf(upload_cv):
    text = ""
    pdf_reader = PdfReader(upload_cv)
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:  # Ensure text is extracted
            text += extracted_text + "\n"
    return text.strip()



# Function to extract text from DOCX
def extract_text_from_docx(upload_cv):
    doc = docx.Document(upload_cv)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text.strip()

# Function to extract Education Section using regex
def extract_education_section(text):
    # Regex pattern to find the "Education" section
    education_pattern = r"(?i)(education|academic background|qualifications)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(education_pattern, text)

    return match.group().strip() if match else "❌ Education details not found."


# function to extract Qualifications section
def extract_qualifications_section(text):
    # Regex pattern to find the "Qualifications" section
    qualifications_pattern = r"(?i)(Qualifications|Skills|Certifications)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(qualifications_pattern, text)

    return match.group().strip() if match else "❌ Qualifications details not found."


# function to extract Projects section
def extract_projects_section(text):
    # Regex pattern to find the "Projects" section
    projects_pattern = r"(?i)(Projects|Internships)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(projects_pattern, text)

    return match.group().strip() if match else "❌ Projects details not found."

# function to extract personal_Information section
def extract_personal_information_section(text):
    # Regex pattern to find the "Personal Information" section
    personal_information_pattern = r"(?i)(Personal Information|Personal Details|About me)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(personal_information_pattern, text)

    return match.group().strip() if match else "❌ Personal Information details not found."

# Streamlit UI
st.title('Automated CV Handler')
name = st.text_input("Name")
emai  = st.text_input("Email")
Phone = st.text_input("Phone")



# Upload CV
upload_cv = st.file_uploader("Upload your CV", type=["pdf", "docx"])
if upload_cv is not None:
    file_type = upload_cv.type  # Get file type
    extracted_text = ""

    if file_type == "application/pdf":
        st.success("✅ Uploaded file is a PDF.")
        extracted_text = extract_text_from_pdf(upload_cv)

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        st.success("✅ Uploaded file is a DOCX.")
        extracted_text = extract_text_from_docx(upload_cv)

    if extracted_text.strip():
        # Extract Education Section
        education_section = extract_education_section(extracted_text)
        st.subheader("Education Section:")
        st.write(education_section)

        # Extract Qualifications Section
        qualifications_section = extract_qualifications_section(extracted_text)
        st.subheader("Qualifications Section:")
        st.write(qualifications_section)

        # Extract Projects Section
        projects_section = extract_projects_section(extracted_text)
        st.subheader("Projects Section:")

        # Extract Personal Information Section
        personal_information_section = extract_personal_information_section(extracted_text)
        st.subheader("Personal Information Section:")
        st.write(personal_information_section)

    else:
        st.warning("⚠️ No readable text found in the CV. It may be scanned or image-based.")

    authenticate()
    drive = GoogleDrive(gauth)

submit = st.button("Submit")
    # Upload to Google Drive
if upload_cv is not None:

    with open("upload_cv.pdf", "wb") as f:
        f.write(upload_cv.read())   
    # Upload to Google Drive
    file_metadata = {'title': 'uploaded_file.pdf', 'parents': ['1Z6MAytQ_0KN78gfyB_jZchjVAB2u19zA']}
    file = drive.CreateFile(file_metadata)
    file.SetContentFile("uploaded_file.pdf")  
    file.Upload()
    st.success("File uploaded successfully!")

# Run: streamlit run filename.py
