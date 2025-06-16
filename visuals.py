import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from supabase import create_client, Client
import base64

# Make sure this is the first Streamlit command
st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")

# Supabase configuration
SUPABASE_URL = "https://ecqhgzbcvzbpyrfytqtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjcWhnemJjdnpicHlyZnl0cXRxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDA1OTQ3NSwiZXhwIjoyMDY1NjM1NDc1fQ.t_LYs4coYrmGBPIwjfwpF_JxYh1SA5mg1POBQGBREkk"
SUPABASE_BUCKET = "myntmetrics-files"

@st.cache_resource(show_spinner=False)
def load_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = load_supabase()

def upload_to_supabase(file_bytes, filename):
    try:
        supabase.storage.from_(SUPABASE_BUCKET).upload(filename, file_bytes, file_options={"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

def list_supabase_files():
    try:
        response = supabase.storage.from_(SUPABASE_BUCKET).list()
        return [f['name'] for f in response if f['name'].endswith('.xlsx')]
    except Exception as e:
        st.error(f"Failed to list files: {e}")
        return []

def read_excel_from_supabase(filename):
    try:
        file_data = supabase.storage.from_(SUPABASE_BUCKET).download(filename)
        return pd.ExcelFile(BytesIO(file_data))
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None

# Utility: Clean currency/numeric values
def clean_number(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(x)
    except:
        return 0

# Upload section
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")
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
        if st.button("Upload to Cloud"):
            filename = f"{month}_{year}.xlsx"
            success = upload_to_supabase(uploaded_file.getvalue(), filename)
            if success:
                st.success(f"Uploaded and saved as {filename} in Supabase ✅")

# Show available files to load
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

    display_df = filtered[filtered['Metrics'] == selected_metric].copy()

    # Clean numeric values
    display_df['Monthly Actual'] = display_df['Monthly Actual'].apply(clean_number)
    display_df['Monthly Target'] = display_df['Monthly Target'].apply(clean_number)

    if display_df.empty:
        st.warning("No data available for this metric across selected months.")
    else:
        # Group and reshape for dual bar comparison
        chart_df = display_df[['Month', 'Monthly Actual', 'Monthly Target']]
        chart_df = chart_df.groupby("Month").sum().reset_index()

        melted_df = chart_df.melt(id_vars='Month', var_name='Type', value_name='Value')

        # Sort months correctly
        def month_key(m):
            month_order = {name: i for i, name in enumerate([
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ])}
            base, _, year = m.partition("_")
            return (int(year), month_order.get(base, 13))

        chart_df['SortKey'] = chart_df['Month'].apply(month_key)
        chart_df = chart_df.sort_values('SortKey')
        melted_df['Month'] = pd.Categorical(
            melted_df['Month'],
            categories=chart_df['Month'],
            ordered=True
        )

        # Seaborn barplot for grouped bar chart
        st.subheader(f"📊 {selected_metric} - Monthly Actual vs Target")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=melted_df, x='Month', y='Value', hue='Type', ax=ax)
        ax.set_ylabel("Value")
        ax.set_xlabel("Month")
        ax.legend(title="Metric Type")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        # Optional: line chart for trend (Actual Only)
        st.subheader("📉 Monthly Trend (Actual)")
        trend_df = chart_df[['Month', 'Monthly Actual']].copy()
        trend_df.set_index('Month', inplace=True)
        st.line_chart(trend_df)

        # Display table
        st.subheader("🧾 Detailed Data")
        st.dataframe(display_df[['Month', 'Metrics', 'Monthly Actual', 'Monthly Target']].reset_index(drop=True).style.format({
            'Monthly Actual': "{:,.0f}",
            'Monthly Target': "{:,.0f}"
        }))
