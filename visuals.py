import streamlit as st
import pandas as pd
from io import BytesIO
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Constants
DRIVE_FOLDER_ID = "12qxuWIpFEAwgiVjY2AmjqT9nQ4vn8Og4"

# Secret JSON credentials
SERVICE_ACCOUNT_CREDS = {
  "type": "service_account",
  "project_id": "myntmoremetrics",
  "private_key_id": "3099e8c12eed41bc49374f1c0751499069905787",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChcqnDA9xFqgDB\n91BlD1wqOz/PmljnDDDtQbnkSELob2RpVAvyGHtX4lGJoZIQ2ErUJVxOUbR5gzdO\neMQt/UHS9IimvJAQ+xne5FCF0Rn3tQkVIi+t89EPOE5TNv+P0RQl1uLPYq7hJ+a7\nrJSk/d2At17SRU6LQ8ulYiMTytv472JmvFa3Sr0kSEUUn6VzwX1dxs/tHFzSqz66\ny/nJtGsQbBpFfUKFyTZTM/UX2gHUhUsNFewt/QYvcUPlCccH3BMj8gJXNQKiHlm2\n0XQEakJxqIlym+FtuK9L3rG+RTW/ClsUaZ0/Z4y8Njl/m3FscL9qvNg2pU7dYeB7\nF1/NiRYHAgMBAAECggEAGIzPbxMwNKZe9R/UFCSwzCSJqy+k+IVXD0z2T9YD2UUk\nYgvgwSX4jkBLoSp2LqTlRBCQ/RaEOLy7n+18pM2lFnIO3DlCOFgmnUk0oWn5kTxF\n2aEthOiAJYNXYw9dmeieMAmBddhjZWOO54JHxuBqWqoHpjaEdL2Qwwutmn3iKJ6S\nwUjRd2t5Fyf9AO4SjLYa66HG4OzqIngFT0yRZg+7ur4al+2B2XqEfcwNJhgHXM7l\n+3Lu40ZqsxPxb5DgyatDWdvgr8qtPO/rTBjwTqo1thIJL6PVt2dp9BxIyaGBqJrT\nYVN38BkiihrbMCb5pQNcuLyczCMS8rNNMynBX2GLCQKBgQDguSkR+bTVzz8hwzfk\nLPSMIAhLAvRE//ZFx/+KdEpho+hTzQDxmyGcwtid0MSlHwfOlfBGuB7o/1WXNHZm\nIvQrhNZg2hXK4+8wmilhJ4pE+Konux9ppDFH6Dtalt7A2cPKTt4v6nP7YviRqmOs\nGxZzy4geXqq6filTkedRwKDigwKBgQC36wPouleC0uOCW5wwfH9swbzp1YjIKaYf\nLm69nXdZQlbJX2K6UM6ljVzvW0uljmlnRbVAd1mHgdk7UI3Ak8OdiszBCKagxlT3\ntF1uNi32FZhtXtGOITvPutFTLtedP7hLzbNDP6MNmtRrsCMUckAkn+qpZq4YVogp\nJKPRXOKXLQKBgQCYFLb2s0bua5MOBk+M29+j9QmnuhgVmiPQlckaqhise4B/Nf2t\nhI76x+JQ6zgphxaBeHdjZLeGd0Y1TgvSk1UrHnr2kKCu7hKxkaLvXRL2GlMNEFXx\n6GxxfXitleyqFrWp9DXpt4FGX3RZIDbUAoDvXI6B/w8LptXQ+KzTZsl6gQKBgB2P\nGwi7cjcnd8NKv/aW+8/Z72fRlvM8pmNajhfRiA4DeHlS6EYzmJLI/ofFr4nDMrOT\nY4ch53S87NH4p1+tIAJg/XmEz2sFlUBeb6m38XkcjWv+kkV6l+dSCjSJUcQHKrKc\nM9R6FNWp7bwFCg5OMnrwbMGfLBnjRmz+Y4nRmOVdAoGAAQRja94E8QjCe8KXtD9l\nWBNVQI4amowXyGY9sLQCPT0qDBcsVELqg0XKGixv3Q3gecZYPdaBjVOTGcN2HYtv\nY5OyIss03Xcj6TUHJphZjZD4shJk38D6qDOCyf2Pbh1/ium47zBedmX6+z7+Llsd\naWjQvXHGDQEA+qFwjD3W5eU=\n-----END PRIVATE KEY-----\n",
  "client_email": "metrics@myntmoremetrics.iam.gserviceaccount.com",
  "client_id": "110536428410191620844",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/metrics%40myntmoremetrics.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# Authenticate Google Drive
@st.cache_resource(show_spinner=False)
def authenticate_drive():
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(SERVICE_ACCOUNT_CREDS, scopes=scope)
    gauth = GoogleAuth()
    gauth.credentials = credentials
    return GoogleDrive(gauth)

drive = authenticate_drive()

# Upload file to Google Drive
def upload_to_drive(file_bytes, filename):
    file_drive = drive.CreateFile({'title': filename, 'parents': [{'id': DRIVE_FOLDER_ID}]})
    with open("temp_upload.xlsx", "wb") as f:
        f.write(file_bytes)
    file_drive.SetContentFile("temp_upload.xlsx")
    file_drive.Upload()
    try:
        os.remove("temp_upload.xlsx")
    except PermissionError:
        pass
    return file_drive['id']

# Load all files from Google Drive folder
def list_drive_files():
    return drive.ListFile({'q': f"'{DRIVE_FOLDER_ID}' in parents and trashed=false"}).GetList()

# Read Excel file from Drive by file ID
def read_excel_from_drive(file):
    file.GetContentFile(file['title'])
    return pd.ExcelFile(file['title'])

# Utility: Clean currency/numeric values
def clean_number(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(x)
    except:
        return 0

# File upload section
st.header("📤 Upload Monthly Data")
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        month = st.selectbox("Select Month", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
    with col2:
        year = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2025, step=1)
    with col3:
        if st.button("Upload to Drive"):
            filename = f"{month}_{year}.xlsx"
            upload_to_drive(uploaded_file.getbuffer(), filename)
            st.success(f"Uploaded and saved as {filename} in Google Drive ✅")

# Show available files to load
st.header("📂 Load & Compare Monthly Data")
all_files = list_drive_files()
month_options = [f['title'].replace(".xlsx", "") for f in all_files if f['title'].endswith(".xlsx")]
selected_months = st.multiselect("Select Month(s) to View", options=month_options, default=month_options)

# Load and process selected files
data_by_month = {}
for file in all_files:
    if file['title'].replace(".xlsx", "") in selected_months:
        label = file['title'].replace(".xlsx", "")
        xls = read_excel_from_drive(file)
        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            if 'Metrics' not in df.columns:
                continue
            df['Category'] = df['Metrics'].where(
                df['Status'].isna() & df['Week 1'].isna() & df['Monthly Actual'].isna()
            ).ffill()
            df = df[~((df['Status'].isna()) & (df['Week 1'].isna()) & (df['Monthly Actual'].isna()))]
            df = df[df['Metrics'].notna()]
            df['Month'] = label
            data_by_month[label] = df

if data_by_month:
    combined_df = pd.concat(data_by_month.values(), ignore_index=True)

    st.sidebar.header("🔎 Filter Metrics")
    categories = combined_df['Category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Select Category", options=categories)

    filtered = combined_df[combined_df['Category'] == selected_category]
    metrics = filtered['Metrics'].dropna().unique()
    selected_metric = st.sidebar.selectbox("Select Metric", options=metrics)

    display_df = filtered[filtered['Metrics'] == selected_metric]

    st.subheader(f"📈 {selected_metric} across months")
    chart_data = display_df[['Month', 'Monthly Actual', 'Monthly Target']].copy()
    chart_data['Monthly Actual'] = chart_data['Monthly Actual'].apply(clean_number)
    chart_data['Monthly Target'] = chart_data['Monthly Target'].apply(clean_number)

    st.bar_chart(chart_data.set_index('Month'))

    st.write("### Detailed Table")
    safe_display_df = display_df.reset_index(drop=True).astype(str)
    st.dataframe(safe_display_df)
