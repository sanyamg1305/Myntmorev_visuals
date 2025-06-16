import streamlit as st
import pandas as pd
from io import BytesIO
from supabase import create_client, Client
import base64

# Supabase Configuration
SUPABASE_URL = "https://ecqhgzbcvzbpyrfytqtq.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjcWhnemJjdnpicHlyZnl0cXRxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDA1OTQ3NSwiZXhwIjoyMDY1NjM1NDc1fQ.t_LYs4coYrmGBPIwjfwpF_JxYh1SA5mg1POBQGBREkk"
BUCKET_NAME = "myntmetric-files"

# Supabase client
@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

supabase = get_supabase_client()

st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# Upload to Supabase
def upload_to_supabase(file_bytes, filename):
    try:
        res = supabase.storage.from_(BUCKET_NAME).upload(filename, file_bytes, {"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
        if res.get("error"):
            st.error(f"Upload failed: {res['error']['message']}")
            return False
        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

def list_supabase_files():
    try:
        res = supabase.storage.from_(BUCKET_NAME).list()
        if isinstance(res, list):
            return [f["name"] for f in res if f["name"].endswith(".xlsx")]
        else:
            st.error("Failed to list files.")
            return []
    except Exception as e:
        st.error(f"Failed to list files: {e}")
        return []

def read_excel_from_supabase(filename):
    try:
        res = supabase.storage.from_(BUCKET_NAME).download(filename)
        if isinstance(res, bytes):
            return pd.ExcelFile(BytesIO(res))
        else:
            st.error("Failed to download file from Supabase.")
            return None
    except Exception as e:
        st.error(f"Download failed: {e}")
        return None

# Clean number
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
        if st.button("Upload to Supabase"):
            filename = f"{month}_{year}.xlsx"
            success = upload_to_supabase(uploaded_file.getbuffer(), filename)
            if success:
                st.success(f"✅ Uploaded and saved as `{filename}` in Supabase.")

# Load & Compare
st.header("📂 Load & Compare Monthly Data")
month_options = [f.replace(".xlsx", "") for f in list_supabase_files()]
selected_months = st.multiselect("Select Month(s) to View", options=month_options, default=month_options)

# Load and process selected files
data_by_month = {}
for filename in month_options:
    if filename in selected_months:
        xls = read_excel_from_supabase(f"{filename}.xlsx")
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
