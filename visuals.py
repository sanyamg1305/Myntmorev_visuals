import streamlit as st
import pandas as pd
from io import BytesIO
from supabase import create_client
import altair as alt

# Must be the first Streamlit command
st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")

# Supabase config (service role, dummy key OK)
SUPABASE_URL = "https://ecqhgzbcvzbpyrfytqtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjcWhnemJjdnpicHlyZnl0cXRxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDA1OTQ3NSwiZXhwIjoyMDY1NjM1NDc1fQ.t_LYs4coYrmGBPIwjfwpF_JxYh1SA5mg1POBQGBREkk"
BUCKET = "myntmetrics-files"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Utils
def clean_number(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(x)
    except:
        return 0

def month_key(month_str):
    month_order = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    try:
        parts = month_str.split("_")
        month = parts[0]
        year = int(parts[1]) if len(parts) > 1 else 0
        return (year, month_order.get(month, 13))
    except:
        return (9999, 13)

def upload_to_supabase(file, filename):
    try:
        supabase.storage.from_(BUCKET).upload(file=filename, file_options={"content": file.getvalue()})
        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

def list_supabase_files():
    try:
        files = supabase.storage.from_(BUCKET).list()
        return [f['name'] for f in files if f['name'].endswith('.xlsx')]
    except Exception as e:
        st.error(f"Failed to list files: {e}")
        return []

def read_excel_from_supabase(filename):
    try:
        res = supabase.storage.from_(BUCKET).download(filename)
        return pd.ExcelFile(BytesIO(res))
    except Exception as e:
        st.error(f"Failed to read {filename}: {e}")
        return None

# UI: Upload
st.title("📊 MyntMetrics: Multi-Month Dashboard")

st.header("📤 Upload Monthly Data")
uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])
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
        if st.button("Upload"):
            filename = f"{month}_{year}.xlsx"
            success = upload_to_supabase(uploaded_file, filename)
            if success:
                st.success(f"✅ Uploaded as `{filename}`")

# List + Load files
st.header("📂 Load & Compare Monthly Data")
all_files = list_supabase_files()
month_options = sorted([f.replace(".xlsx", "") for f in all_files], key=month_key)
selected_months = st.multiselect("Select months to view", options=month_options, default=month_options)

# Load selected files
data_by_month = {}
for month in selected_months:
    xls = read_excel_from_supabase(f"{month}.xlsx")
    if not xls:
        continue
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        if "Metrics" not in df.columns:
            continue
        df['Category'] = df['Metrics'].where(
            df['Status'].isna() & df['Week 1'].isna() & df['Monthly Actual'].isna()
        ).ffill()
        df = df[~((df['Status'].isna()) & (df['Week 1'].isna()) & (df['Monthly Actual'].isna()))]
        df = df[df['Metrics'].notna()]
        df['Month'] = month
        data_by_month[month] = df

if not data_by_month:
    st.warning("No valid data found.")
    st.stop()

# Merge & clean
combined_df = pd.concat(data_by_month.values(), ignore_index=True)
combined_df['Monthly Actual'] = combined_df['Monthly Actual'].apply(clean_number)
combined_df['Monthly Target'] = combined_df['Monthly Target'].apply(clean_number)

# Sidebar filters
st.sidebar.header("🔎 Filter Metrics")
categories = combined_df['Category'].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", categories)

filtered = combined_df[combined_df['Category'] == selected_category]
metrics = filtered['Metrics'].dropna().unique()
selected_metric = st.sidebar.selectbox("Select Metric", metrics)

display_df = filtered[filtered['Metrics'] == selected_metric]

# Prepare bar chart
chart_df = display_df[['Month', 'Monthly Actual', 'Monthly Target']].copy()
chart_df['SortKey'] = chart_df['Month'].apply(month_key)
chart_df = chart_df.sort_values('SortKey')

# Melt for Altair
melted_df = chart_df.melt(id_vars='Month', value_vars=['Monthly Actual', 'Monthly Target'], var_name='Type', value_name='Value')
melted_df['Month'] = pd.Categorical(melted_df['Month'], categories=chart_df['Month'], ordered=True)

# Show chart
st.subheader(f"📈 {selected_metric} – Month-over-Month Comparison")
chart = alt.Chart(melted_df).mark_bar().encode(
    x=alt.X("Month:N", title="Month"),
    y=alt.Y("Value:Q", title="Value"),
    color=alt.Color("Type:N", title=""),
    column=alt.Column("Type:N", title=None)
).properties(width=200)

st.altair_chart(chart, use_container_width=True)

# Show table
st.write("### 📋 Detailed Table")
st.dataframe(display_df.reset_index(drop=True))
