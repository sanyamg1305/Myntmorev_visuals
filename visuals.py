import streamlit as st
import pandas as pd
from io import BytesIO
from supabase import create_client, Client
import re

# ───── Supabase Config ─────
SUPABASE_URL = "https://ecqhgzbcvzbpyrfytqtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjcWhnemJjdnpicHlyZnl0cXRxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDA1OTQ3NSwiZXhwIjoyMDY1NjM1NDc1fQ.t_LYs4coYrmGBPIwjfwpF_JxYh1SA5mg1POBQGBREkk"
BUCKET = "myntmetrics-files"

# ───── Must be first Streamlit command ─────
st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# ───── Supabase Client Init ─────
@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = get_supabase_client()

# ───── Upload Excel File to Supabase ─────
def upload_to_supabase(file, filename):
    try:
        supabase.storage.from_(BUCKET).upload(
            path=filename,
            file=file.getvalue(),
            file_options={"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
        )
        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

# ───── List Excel Files from Supabase ─────
def list_supabase_files():
    try:
        files = supabase.storage.from_(BUCKET).list()
        return [f["name"] for f in files if f["name"].endswith(".xlsx")]
    except Exception as e:
        st.error(f"Failed to list files: {e}")
        return []

# ───── Read Excel File from Supabase ─────
def read_excel_from_supabase(filename):
    try:
        file = supabase.storage.from_(BUCKET).download(filename)
        return pd.ExcelFile(BytesIO(file))
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None

# ───── Clean numeric values ─────
def clean_number(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(x)
    except:
        return 0

# ───── Upload Section ─────
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
            success = upload_to_supabase(uploaded_file, filename)
            if success:
                st.success(f"✅ Uploaded and saved as `{filename}`")

# ───── Load and Compare Monthly Data ─────
st.header("📂 Load & Compare Monthly Data")
file_list = list_supabase_files()
month_options = [f.replace(".xlsx", "") for f in file_list]
selected_months = st.multiselect("Select Month(s) to View", options=month_options, default=month_options)

data_by_month = {}

for month_label in selected_months:
    xls = read_excel_from_supabase(f"{month_label}.xlsx")
    if xls is None:
        continue
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        if 'Metrics' not in df.columns or 'Monthly Actual' not in df.columns:
            continue
        df['Category'] = df['Metrics'].where(
            df['Status'].isna() & df['Week 1'].isna() & df['Monthly Actual'].isna()
        ).ffill()
        df = df[~((df['Status'].isna()) & (df['Week 1'].isna()) & (df['Monthly Actual'].isna()))]
        df = df[df['Metrics'].notna()]
        df['MonthLabel'] = month_label
        df['Month'], df['Year'] = re.findall(r'([A-Za-z]+)_([0-9]+)', month_label)[0]
        df['MonthNum'] = pd.to_datetime(df['Month'], format='%B').dt.month
        df['Year'] = df['Year'].astype(int)
        data_by_month[month_label] = df

if data_by_month:
    combined_df = pd.concat(data_by_month.values(), ignore_index=True)

    # Sort data
    combined_df.sort_values(by=["Year", "MonthNum"], inplace=True)

    # ───── Sidebar Filters ─────
    st.sidebar.header("🔎 Filter Metrics")
    categories = combined_df['Category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Select Category", options=categories)

    filtered_df = combined_df[combined_df['Category'] == selected_category]
    metrics = filtered_df['Metrics'].dropna().unique()
    selected_metric = st.sidebar.selectbox("Select Metric", options=metrics)

    display_df = filtered_df[filtered_df['Metrics'] == selected_metric].copy()
    display_df['Monthly Actual'] = display_df['Monthly Actual'].apply(clean_number)
    display_df['Monthly Target'] = display_df['Monthly Target'].apply(clean_number)

    # ───── Chart ─────
    st.subheader(f"📈 {selected_metric} Over Time")
    chart_df = display_df[['MonthLabel', 'Monthly Actual', 'Monthly Target']]
    chart_df.set_index('MonthLabel', inplace=True)

    st.bar_chart(chart_df)

    # ───── Table ─────
    st.write("### 📋 Detailed Table")
    st.dataframe(display_df[['MonthLabel', 'Metrics', 'Monthly Actual', 'Monthly Target', 'Category']].reset_index(drop=True))

else:
    st.info("Upload or select monthly data to see visualizations.")
