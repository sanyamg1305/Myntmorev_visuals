import streamlit as st
import pandas as pd
from io import BytesIO
from supabase import create_client, Client

# 🧩 Page config
st.set_page_config(page_title="MyntMetrics Dashboard", layout="wide")
st.title("📊 MyntMetrics: Multi-Month Metrics Dashboard")

# 🔐 Supabase config
SUPABASE_URL = "https://ecqhgzbcvzbpyrfytqtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjcWhnemJjdnpicHlyZnl0cXRxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDA1OTQ3NSwiZXhwIjoyMDY1NjM1NDc1fQ.t_LYs4coYrmGBPIwjfwpF_JxYh1SA5mg1POBQGBREkk"
BUCKET_NAME = "myntmetrics-files"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Define allowed metrics
defined_metrics = {
    "SALES": [
        "Jahnvi Sales connection requests", "Jahnvi Sales Inmail messages",
        "Accepted connection requests", "Connection requests acceptance rate",
        "Meetings booked", "Meetings completed", "Conversions"
    ],
    "TEJAS JHAVERI": [
        "No of posts posted", "Impressions", "Profile viewers (Bi-Monthly)",
        "Engagement", "Search Appearances", "New followers", "Total follower count",
        "Happiness Index (0-10) | Week 4"
    ],
    "SHIRIN DHABHAR": [
        "No of text + image posts posted", "No of carousels posted", "Impressions",
        "Profile viewers (Bi-Monthly)", "Followers", "Total Follower Count",
        "Happiness Index (0-10) | Week 4"
    ],
    "HEMAL JHAVERI": [
        "No of posts posted", "Sent Invitations", "Accepted Invitations", "Acceptance Rate",
        "Hot Leads", "Meetings Booked", "Profile Viewers (Bi-monthly)", "Impressions",
        "Followers", "Total Follower Count", "Happiness Index (0-10) | Week 4"
    ],
    "SITANSHU": [
        "No of text + image posts posted", "Carousels posted", "Impressions", "Engagements",
        "Profile viewers (Bi-Monthly)", "Followers", "Total Follower Count",
        "Connection Requests Sent", "Accepted Invitations", "Acceptance Rate", "Hot Leads",
        "Meetings Booked", "Happiness Index (0-10) | Week 4"
    ],
    "HOZEFA": [
        "No of text + image posts posted", "No of carousels posted", "Total posts posted",
        "EOM Report", "Impressions", "Engagement", "Profile viewers (Bi-Monthly)",
        "Followers", "Total Follower Count", "InMails Requests Sent", "Connection Requests Sent",
        "Accepted Invitations", "Acceptance Rate", "Hot Leads", "Meetings Booked",
        "Happiness Index (0-10) | Week 4"
    ],
    "SANDEEP KHEMKA": [
        "No of text + image posts posted", "No of carousels posted", "Total posts posted",
        "Impressions", "Engagement", "Profile viewers (Bi-Monthly)", "New Followers",
        "Total Follower Count", "InMails Requests Sent", "Connection Requests Sent",
        "Accepted Invitations", "Acceptance Rate", "Hot Leads", "Meetings Booked",
        "Happiness Index (0-10) | Week 4"
    ],
    "MOHIT JHAVERI": [
        "No of text + image posts posted", "No of carousels posted", "Total posts posted",
        "Impressions", "Engagement", "Profile viewers (Bi-Monthly)", "Followers",
        "Total Follower Count", "InMails Requests Sent", "Connection Requests Sent",
        "Accepted Invitations", "Acceptance Rate", "Hot Leads", "Meetings Booked",
        "Happiness Index (0-10) | Week 4"
    ],
    "Linkedin Newsletter": [
        "LinkedIn Newsletter Subscriber count", "New subscribers", "Members Reached",
        "Email sends", "Email open rate", "Impressions", "Article Views"
    ],
    "Email Newsletter": [
        "Subscriber count", "Unsubscribed", "Sent", "Delivered", "Open", "Open Rate", "Clicked",
        "Soft Bounce", "Hard Bounce", "Total Bounce Rate", "Replies",
        "Website Newsletter (footer) Converstions", "Website Newsletter (footer) Interactions",
        "Website Newsletter (page) Coversions", "Website Newsletter (page) Interactions"
    ],
    "Myntmore Marketing": [
        "Instagram Posts", "LinkedIn Posts", "Facebook Posts", "Instagram Follower Count",
        "Instagram New Followers", "Facebook follower Count", "Linkedin Follower Count",
        "Linkedin New Followers", "Impressions", "Clicks", "Reactions", "Comments",
        "Engagement Rate", "Total page views", "Total unique visitors",
        "Website traffic - Active users", "Average session duration", "Bounce rate",
        "Website traffic - New Users"
    ],
    "ATHARVA VIDEO EDITOR": [
        "Videos sent to atharva", "Videos edited", "Videos posted", "Videos shot", "TJ Approvals"
    ]
}

# 🔧 Clean currency-like fields
def clean_number(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("₹", "").replace("?", "").strip()
    try:
        return float(x)
    except:
        return 0

# 🧩 Supabase functions
def upload_to_supabase(file_bytes, filename):
    try:
        res = supabase.storage.from_(BUCKET_NAME).upload(
            path=filename,
            file=file_bytes,
            file_options={"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "upsert": "true"}
        )
        return res is not None
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

def list_supabase_files():
    try:
        return [f["name"] for f in supabase.storage.from_(BUCKET_NAME).list() if f["name"].endswith(".xlsx")]
    except Exception as e:
        st.error(f"Failed to list files: {e}")
        return []

def read_excel_from_supabase(filename):
    try:
        res = supabase.storage.from_(BUCKET_NAME).download(filename)
        return pd.ExcelFile(BytesIO(res))
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None

# 📤 Upload Interface
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
            success = upload_to_supabase(uploaded_file.getbuffer().tobytes(), filename)
            if success:
                st.success(f"✅ Uploaded and saved as `{filename}` in Supabase Storage!")

# 📂 Load & Compare Section
st.header("📂 Load & Compare Monthly Data")
month_options = [f.replace(".xlsx", "") for f in list_supabase_files()]
selected_months = st.multiselect("Select Month(s) to View", options=month_options, default=month_options)

data_by_month = {}
for month in selected_months:
    xls = read_excel_from_supabase(f"{month}.xlsx")
    if xls is None:
        continue
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        if 'Metrics' not in df.columns:
            continue

        valid_rows = []
        for cat, metrics in defined_metrics.items():
            for metric in metrics:
                match = df[df['Metrics'].astype(str).str.strip().str.lower() == metric.lower()]
                if not match.empty:
                    match = match.copy()
                    match['Category'] = cat
                    valid_rows.append(match)

        if valid_rows:
            filtered_df = pd.concat(valid_rows, ignore_index=True)
            filtered_df['Month'] = month
            data_by_month[month] = filtered_df

# 📊 Dashboard View
if data_by_month:
    combined_df = pd.concat(data_by_month.values(), ignore_index=True)
    # Drop duplicates to ensure each metric is unique per month and category
    combined_df = combined_df.drop_duplicates(subset=['Month', 'Metrics', 'Category'], keep='first')

    # Add a datetime column for sorting
    def parse_month_year(row):
        import calendar
        try:
            month_name, year = row['Month'].split('_')
            month_num = list(calendar.month_name).index(month_name)
            return pd.Timestamp(year=int(year), month=month_num, day=1)
        except Exception:
            return pd.NaT
    combined_df['Month_Year'] = combined_df.apply(parse_month_year, axis=1)
    combined_df = combined_df.sort_values('Month_Year')

    st.sidebar.header("🔎 Filter Metrics")
    categories = list(defined_metrics.keys())
    selected_category = st.sidebar.selectbox("Select Category", options=categories)

    filtered = combined_df[combined_df['Category'] == selected_category]
    metrics = defined_metrics[selected_category]
    selected_metric = st.sidebar.selectbox("Select Metric", options=metrics)

    display_df = filtered[filtered['Metrics'].str.lower() == selected_metric.lower()]
    chart_data = display_df[['Month', 'Monthly Actual', 'Month_Year']].copy()
    chart_data['Monthly Actual'] = chart_data['Monthly Actual'].apply(clean_number)
    chart_data = chart_data.sort_values('Month_Year')

    # Sort display_df and chart_data by Month_Year for correct order
    display_df = display_df.sort_values('Month_Year')
    chart_data = chart_data.sort_values('Month_Year')

    st.subheader(f"📈 {selected_metric} across months")
    # Create ordered categories from unique sorted months
    unique_months = chart_data['Month'].unique()
    chart_data['Month'] = pd.Categorical(
        chart_data['Month'],
        categories=unique_months,
        ordered=True
    )
    
    st.bar_chart(chart_data.set_index('Month')['Monthly Actual'])

    # High and low score with month/year
    max_val = chart_data['Monthly Actual'].max()
    min_val = chart_data['Monthly Actual'].min()
    max_row = chart_data[chart_data['Monthly Actual'] == max_val].iloc[0] if not chart_data[chart_data['Monthly Actual'] == max_val].empty else None
    min_row = chart_data[chart_data['Monthly Actual'] == min_val].iloc[0] if not chart_data[chart_data['Monthly Actual'] == min_val].empty else None
    max_month = max_row['Month'] if max_row is not None else "-"
    min_month = min_row['Month'] if min_row is not None else "-"

    st.metric("📈 High Score", f"{max_val:,.0f}", help=f"Month: {max_month}")
    st.metric("📉 Low Score", f"{min_val:,.0f}", help=f"Month: {min_month}")

    st.write("### 📋 Detailed Table")
    st.dataframe(display_df.reset_index(drop=True).astype(str))
