# Automated CV Handler with Google Sheets Integration

This is a Streamlit app that allows users to upload their CV (in PDF or DOCX format), extract key information, and upload that information to a Google Sheets database. The app also provides the ability to view the data stored in Google Sheets.

## Features

- **Upload CV**: Users can upload CVs in PDF or DOCX formats.
- **Extract Data**: The app extracts relevant sections from the CV, such as:
  - Education
  - Qualifications
  - Projects
  - Personal Information
- **View Data**: The app fetches and displays the data stored in a connected Google Sheet.
- **Store Data in Google Sheets**: After extracting the information, users can submit the data to a Google Sheets database.

## Requirements

Make sure you have the following Python libraries installed:

- `streamlit`
- `pandas`
- `PyPDF2`
- `python-docx`
- `streamlit-gsheets`
- `pydrive`
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`

You can install them using the following command:

```bash
pip install -r requirements.txt


### Explanation of Sections:

- **Project Title and Description**: Briefly describe what your app does and its features.
- **Requirements**: List the Python libraries needed to run your app.
- **Authentication**: Instructions for setting up Google authentication and the `client_secret.json` file.
- **How to Run the App**: Provides steps for local installation and running the app.
- **Deployment**: Explains how to deploy the app to cloud platforms like Streamlit Cloud, Heroku, or PythonAnywhere.
- **Google Sheets Integration**: Explains how to configure the app to work with Google Sheets.
- **License**: Information about the license governing the project.
- **Acknowledgments**: Acknowledges any third-party libraries or services used in the project.

Feel free to modify the `README.md` to match your app’s specific needs and deployment details!



