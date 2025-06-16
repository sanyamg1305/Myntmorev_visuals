import streamlit as st
import pandas as pd
from io import BytesIO
from supabase import create_client

# 🔧 Config must be first
st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")

# 🔐 Supabase credentials
SUPABASE_URL = "https://ecqhgzbcvzbpyrfytqtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjcWhnemJjdnpicHlyZnl0cXRxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDA1OTQ3NSwiZXhwIjoyMDY1NjM1NDc1fQ.t_LYs4coYrmGBPIwjfwpF_JxYh1SA5mg1POBQGBREkk"
BUCKET_NAME = "myntmetrics-files"

# 🔌 Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 📤 Upload file to Supabase Storage
def upload_to_supabase(file_bytes, filename):
    try:
        # Convert to bytes if needed
        if isinstance(file_bytes, BytesIO):
            file_bytes = file_bytes.getvalue()
        supabase.storage.from_(BUCKET_NAME).upload(
            filename,
            file_bytes,
            {"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
            upsert=True
        )
        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

# 📄 List all files in Supabase Storage
def list_supabase_files():
    try:
        return [
            f["name"]
            for f in supabase.storage.from_(BUCKET_NAME).list()
            if f["name"].endswith(".xlsx")
        ]
    except Exception as e:
        st.error(f"Failed to list files: {e}")
        return []

# 📥 Read file from Supabase
def read_excel_from_supabase(filename):
    try:
        file_data = supabase.storage.from_(BUCKET_NAME).download(filename)
        return pd.ExcelFile(BytesIO(file_data))
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None

# 🧹 Clean numeric data
def clean_number(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(x)
    except:
        return 0

# ---------------- UI ----------------

st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# Upload UI
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
        year = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2025)
    with col3:
        if st.button("Upload to Supabase"):
            filename = f"{month}_{year}.xlsx"
            success = upload_to_supabase(uploaded_file, filename)
            if success:
                st.success(f"✅ Uploaded as `{filename}`")

# Load and select files
st.header("📂 Load & Compare Monthly Data")
available_files = list_supabase_files()
month_options = [f.replace(".xlsx", "") for f in available_files]
selected_months = st.multiselect("Select Month(s)", options=month_options, default=month_options)

# Process files
data_by_month = {}
for month in selected_months:
    xls = read_excel_from_supabase(f"{month}.xlsx")
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
        df['Month'] = month
        data_by_month[month] = df

# Display chart
if data_by_month:
    combined_df = pd.concat(data_by_month.values(), ignore_index=True)

    st.sidebar.header("🔎 Filter Metrics")
    categories = combined_df['Category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Select Category", options=categories)

    filtered_df = combined_df[combined_df['Category'] == selected_category]
    metric_options = filtered_df['Metrics'].dropna().unique()
    selected_metric = st.sidebar.selectbox("Select Metric", options=metric_options)

    display_df = filtered_df[filtered_df['Metrics'] == selected_metric]

    st.subheader(f"📈 {selected_metric} Across Months")
    chart_data = display_df[['Month', 'Monthly Actual', 'Monthly Target']].copy()
    chart_data['Monthly Actual'] = chart_data['Monthly Actual'].apply(clean_number)
    chart_data['Monthly Target'] = chart_data['Monthly Target'].apply(clean_number)

    st.bar_chart(chart_data.set_index('Month'))

    st.write("### 📋 Detailed Table")
    st.dataframe(display_df.reset_index(drop=True).astype(str))
