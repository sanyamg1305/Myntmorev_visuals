import streamlit as st
import pandas as pd
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError

# ✅ Backblaze B2 S3-Compatible Configuration
B2_KEY_ID = "00548633c258da10000000002"
B2_APPLICATION_KEY = "K005AIX1EbwPPMnSNgRk7Ai+u1fnmQo"
B2_BUCKET_NAME = "myntmetrics-files"
B2_ENDPOINT = "https://s3.us-west-004.backblazeb2.com"

# Streamlit UI config
st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# Initialize B2 client
@st.cache_resource(show_spinner=False)
def get_b2_client():
    session = boto3.session.Session()
    return session.client(
        service_name='s3',
        aws_access_key_id=B2_KEY_ID,
        aws_secret_access_key=B2_APPLICATION_KEY,
        endpoint_url=B2_ENDPOINT,
    )

b2_client = get_b2_client()

# Upload to B2
def upload_to_b2(file_bytes, filename):
    try:
        b2_client.upload_fileobj(BytesIO(file_bytes), B2_BUCKET_NAME, filename)
        return True
    except NoCredentialsError:
        st.error("B2 credentials not available.")
        return False
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

# List B2 files
def list_b2_files():
    try:
        response = b2_client.list_objects_v2(Bucket=B2_BUCKET_NAME)
        return [content['Key'] for content in response.get('Contents', [])]
    except Exception as e:
        st.error(f"Failed to list files: {e}")
        return []

# Read Excel from B2
def read_excel_from_b2(filename):
    buffer = BytesIO()
    try:
        b2_client.download_fileobj(B2_BUCKET_NAME, filename, buffer)
        buffer.seek(0)
        return pd.ExcelFile(buffer)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None

# Utility to clean numbers
def clean_number(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(x)
    except:
        return 0

# Upload section
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
        if st.button("Upload to B2"):
            filename = f"{month}_{year}.xlsx"
            success = upload_to_b2(uploaded_file.getbuffer(), filename)
            if success:
                st.success(f"Uploaded and saved as `{filename}` in Backblaze B2 ✅")

# Load and compare section
st.header("📂 Load & Compare Monthly Data")
month_options = [f.replace(".xlsx", "") for f in list_b2_files() if f.endswith(".xlsx")]
selected_months = st.multiselect("Select Month(s) to View", options=month_options, default=month_options)

# Process data
data_by_month = {}
for filename in month_options:
    if filename in selected_months:
        xls = read_excel_from_b2(f"{filename}.xlsx")
        if xls is None:
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
            df['Month'] = filename
            data_by_month[filename] = df

# Display comparison
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
    st.dataframe(display_df.reset_index(drop=True).astype(str))
