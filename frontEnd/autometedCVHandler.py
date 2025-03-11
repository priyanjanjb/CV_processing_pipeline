import streamlit as st 
from PyPDF2 import PdfReader
import docx
import re
import pandas as pd
import smtplib
import schedule
import time
import pytz
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from streamlit_gsheets import GSheetsConnection

# Google Sheets connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

# Set the spreadsheet ID and worksheet name
SPREADSHEET_ID = '1PtMEehypQHn4cNBALrN8XcgjQ5lwA91qWHq_DCGWb14'
WORKSHEET_NAME = "CVdata"

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
    education_pattern = r"(?i)(education|academic background|qualifications)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(education_pattern, text)
    return match.group().strip() if match else "❌ Education details not found."

# Function to extract Qualifications Section
def extract_qualifications_section(text):
    qualifications_pattern = r"(?i)(Qualifications|Skills|Certifications)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(qualifications_pattern, text)
    return match.group().strip() if match else "❌ Qualifications details not found."

# Function to extract Projects Section
def extract_projects_section(text):
    projects_pattern = r"(?i)(Projects|Internships)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(projects_pattern, text)
    return match.group().strip() if match else "❌ Projects details not found."

# Function to extract Personal Information Section
def extract_personal_information_section(text):
    personal_information_pattern = r"(?i)(Personal Information|Personal Details|About me)[\s\S]+?(?=\n\n|\n[A-Z])"
    match = re.search(personal_information_pattern, text)
    return match.group().strip() if match else "❌ Personal Information details not found."

# Function to extract name, email, and phone from the CV
def extract_contact_info(text):
    name_pattern = r"(?i)(name|full\sname|first\sname)\s*[:\-]?\s*(\w+\s\w+)"
    email_pattern = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
    phone_pattern = r"(\+?\d{1,2}[-\s]?)?(\(?\d{3}\)?[-\s]?)?[\d\s\-]{7,15}"
    
    name = re.search(name_pattern, text)
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)

    extracted_name = name.group(2) if name else "❌ Name not found"
    extracted_email = email.group(0) if email else "❌ Email not found"
    extracted_phone = phone.group(0) if phone else "❌ Phone not found"
    
    return extracted_name, extracted_email, extracted_phone

# Function to send email
def send_email(to_email, subject, body):
    from_email = "your_email@example.com"  # Your email
    password = "your_email_password"  # Your email password or app password

    # SMTP server configuration (for Gmail in this example)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach body to email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, password)

        # Send email
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to determine the appropriate time to send the email
def send_follow_up_email(email, name, timezone_str):
    # Convert applicant's time zone
    applicant_tz = pytz.timezone(timezone_str)
    current_time = datetime.now(applicant_tz)
    send_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)

    # Wait until the appropriate time to send the email
    while datetime.now(applicant_tz) < send_time:
        time.sleep(60)  # Sleep for a minute to check again

    # Email content
    subject = "Your CV is under review"
    body = f"Dear {name},\n\nThank you for submitting your CV. We would like to inform you that your application is currently under review. We will get back to you soon.\n\nBest regards,\nCompany Name"

    # Send email
    send_email(email, subject, body)

# Scheduling the follow-up email task (adjust this based on actual usage)
def schedule_follow_up(email, name, timezone_str):
    # Schedule the email to be sent the next day
    schedule.every().day.at("09:00").do(send_follow_up_email, email=email, name=name, timezone_str=timezone_str)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Streamlit app UI
st.title("Automated CV Handler")

# Upload CV for Extraction
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
        # Extract sections from CV
        education_section = extract_education_section(extracted_text)
        qualifications_section = extract_qualifications_section(extracted_text)
        projects_section = extract_projects_section(extracted_text)
        personal_information_section = extract_personal_information_section(extracted_text)

        # Extract Name, Email, Phone
        extracted_name, extracted_email, extracted_phone = extract_contact_info(extracted_text)

        # User Input Form for Google Sheets
        with st.form(key="cv_form"):
            name = st.text_input("Name", extracted_name)
            phone_number = st.text_input("Phone Number", extracted_phone)  # Ensuring it's stored as text
            email = st.text_input("Email", extracted_email)
            education = st.text_area("Education", education_section)
            qualifications = st.text_area("Qualifications", qualifications_section)
            projects = st.text_area("Projects", projects_section)
            personal_information = st.text_area("Personal Information", personal_information_section)

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                # Prepare data to be uploaded to Google Sheets
                new_entry = pd.DataFrame({
                    'Name': [name],
                    'Phone_number': [phone_number],  # Ensure it remains a string
                    'Email': [email],
                    'Education': [education],
                    'Qualifications': [qualifications],
                    'Projects': [projects]
                })

                try:
                    # Read existing data again to avoid overwriting
                    data = conn.read(
                        spreadsheet=SPREADSHEET_ID, 
                        usecols=['Name', 'Phone_number', 'Email', 'Education', 'Qualifications', 'Projects']
                    )

                    # Append new data
                    updated_data = pd.concat([data, new_entry], ignore_index=True)

                    # Update Google Sheets
                    conn.update(worksheet=WORKSHEET_NAME, data=updated_data)

                    st.success("New entry added successfully to Google Sheets! 🎉")
                except Exception as e:
                    st.error(f"Error updating Google Sheets: {e}")

                # Schedule follow-up email to be sent the next day
                schedule_follow_up(email, name, "Asia/Colombo")  # Set the applicant's time zone

    else:
        st.warning("⚠️ No readable text found in the CV. It may be scanned or image-based.")
