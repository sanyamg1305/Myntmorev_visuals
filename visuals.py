import streamlit as st
import pandas as pd
from io import BytesIO
import os
import boto3
from botocore.client import Config

# Cloudflare R2 Configuration
R2_ACCESS_KEY_ID = "sanyam@myntmore.com"
R2_SECRET_ACCESS_KEY = "941b182490142925d61487cd1509c54b677a3"
R2_BUCKET_NAME = "myntmetrics-files"
R2_ENDPOINT = "https://823b7248bb96f3485e0901c2e5da3802.r2.cloudflarestorage.com"

# Boto3 client for R2
s3 = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# Upload file to R2
@st.cache_resource(show_spinner=False)
def list_r2_files():
    try:
        response = s3.list_objects_v2(Bucket=R2_BUCKET_NAME)
        files = response.get('Contents', [])
        return [f['Key'] for f in files]
    except Exception as e:
        st.error(f"Failed to list R2 files: {e}")
        return []

def upload_to_r2(file_bytes, filename):
    try:
        s3.put_object(Bucket=R2_BUCKET_NAME, Key=filename, Body=file_bytes)
        return True
    except Exception as e:
        st.error(f"Upload to R2 failed: {e}")
        return False

def download_r2_file(key):
    try:
        response = s3.get_object(Bucket=R2_BUCKET_NAME, Key=key)
        return pd.ExcelFile(BytesIO(response['Body'].read()))
    except Exception as e:
        st.error(f"Failed to read file from R2: {e}")
        return None

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
        if st.button("Upload to Cloudflare R2"):
            filename = f"{month}_{year}.xlsx"
            success = upload_to_r2(uploaded_file.getbuffer(), filename)
            if success:
                st.success(f"Uploaded and saved as {filename} in R2 ✅")

# Show available files to load
st.header("📂 Load & Compare Monthly Data")
all_files = list_r2_files()
month_options = [f.replace(".xlsx", "") for f in all_files if f.endswith(".xlsx")]
selected_months = st.multiselect("Select Month(s) to View", options=month_options, default=month_options)

# Load and process selected files
data_by_month = {}
for file in all_files:
    label = file.replace(".xlsx", "")
    if label in selected_months:
        xls = download_r2_file(file)
        if not xls:
            continue
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

    def clean_number(x):
        if pd.isna(x):
            return 0
        x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
        try:
            return float(x)
        except:
            return 0

    chart_data['Monthly Actual'] = chart_data['Monthly Actual'].apply(clean_number)
    chart_data['Monthly Target'] = chart_data['Monthly Target'].apply(clean_number)

    st.bar_chart(chart_data.set_index('Month'))

    st.write("### Detailed Table")
    safe_display_df = display_df.reset_index(drop=True).astype(str)
    st.dataframe(safe_display_df)
