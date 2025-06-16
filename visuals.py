import streamlit as st
import pandas as pd
from io import BytesIO
import os
import json
from google.oauth2 import service_account
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Constants
DRIVE_FOLDER_ID = "12qxuWIpFEAwgiVjY2AmjqT9nQ4vn8Og4"

st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# Authenticate Google Drive
@st.cache_resource(show_spinner=False)
def authenticate_drive():
    with open("myntmoremetrics-3099e8c12eed.json") as f:
        service_account_info = json.load(f)

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['https://www.googleapis.com/auth/drive']
    )

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
