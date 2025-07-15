
import streamlit as st
import pandas as pd
import re
from pandas.api.types import CategoricalDtype
import calendar

# ---------------------------
# 📊 Embedded data
# ---------------------------

data_records = [
    {'Month': 'December2024', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales connection requests', 'Monthly Actual': 428},
    {'Month': 'December2024', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales Inmail messages', 'Monthly Actual': 6},
    {'Month': 'December2024', 'Main Category': 'SALES', 'Sub Category': 'Accepted connection requests', 'Monthly Actual': 104},
    {'Month': 'December2024', 'Main Category': 'SALES', 'Sub Category': 'Connection requests acceptance rate', 'Monthly Actual': 0.1402},
    {'Month': 'December2024', 'Main Category': 'SALES', 'Sub Category': 'Meetings booked', 'Monthly Actual': 14},
    {'Month': 'December2024', 'Main Category': 'SALES', 'Sub Category': 'Meetings completed', 'Monthly Actual': 13},
    {'Month': 'December2024', 'Main Category': 'SALES', 'Sub Category': 'Conversions', 'Monthly Actual': 1},
    {'Month': 'December2024', 'Main Category': 'NEWSLETTER', 'Sub Category': 'LinkedIn Newsletter Subscriber count', 'Monthly Actual': 1000},
    {'Month': 'December2024', 'Main Category': 'NEWSLETTER', 'Sub Category': 'Unsubscribed', 'Monthly Actual': 32},
    {'Month': 'December2024', 'Main Category': 'NEWSLETTER', 'Sub Category': 'Clicked', 'Monthly Actual': '14+8+7+4'},
    {'Month': 'December2024', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram follower count', 'Monthly Actual': 21},
    {'Month': 'December2024', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn follower count', 'Monthly Actual': 1344},
    {'Month': 'December2024', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook follower count', 'Monthly Actual': 0},
    {'Month': 'December2024', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Posts', 'Monthly Actual': 10},
    {'Month': 'December2024', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn Posts', 'Monthly Actual': 10},
    {'Month': 'December2024', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook Posts', 'Monthly Actual': 10},
    {'Month': 'December2024', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 16},
    {'Month': 'December2024', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 20532},
    {'Month': 'December2024', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 377},
    {'Month': 'December2024', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Engagement', 'Monthly Actual': 459},
    {'Month': 'December2024', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 301},
    {'Month': 'December2024', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 14},
    {'Month': 'December2024', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Impressions', 'Monthly Actual': 5715},
    {'Month': 'December2024', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 304},
    {'Month': 'December2024', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 17},
    {'Month': 'December2024', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'New Followers', 'Monthly Actual': 21},
    {'Month': 'December2024', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 9},
    {'Month': 'December2024', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 4152},
    {'Month': 'December2024', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 159},
    {'Month': 'December2024', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 74},
    {'Month': 'December2024', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 69},
    {'Month': 'January2025', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales connection requests', 'Monthly Actual': 305.0},
    {'Month': 'January2025', 'Main Category': 'SALES', 'Sub Category': 'Accepted connection requests', 'Monthly Actual': 43.0},
    {'Month': 'January2025', 'Main Category': 'SALES', 'Sub Category': 'Connection requests acceptance rate', 'Monthly Actual': 0.2782},
    {'Month': 'January2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings booked', 'Monthly Actual': 5.0},
    {'Month': 'January2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings completed', 'Monthly Actual': 5.0},
    {'Month': 'January2025', 'Main Category': 'SALES', 'Sub Category': 'Conversions', 'Monthly Actual': 1.0},
    {'Month': 'January2025', 'Main Category': 'NEWSLETTER', 'Sub Category': 'LinkedIn Newsletter Subscriber count', 'Monthly Actual': 1148.0},
    {'Month': 'January2025', 'Main Category': 'NEWSLETTER', 'Sub Category': 'New subscribers', 'Monthly Actual': 148.0},
    {'Month': 'January2025', 'Main Category': 'NEWSLETTER', 'Sub Category': 'Impressions', 'Monthly Actual': 2446.0},
    {'Month': 'January2025', 'Main Category': 'NEWSLETTER', 'Sub Category': 'Soft Bounce', 'Monthly Actual': 283.0},
    {'Month': 'January2025', 'Main Category': 'NEWSLETTER', 'Sub Category': 'Hard Bounce', 'Monthly Actual': 131.0},
    {'Month': 'January2025', 'Main Category': 'NEWSLETTER', 'Sub Category': 'Total Bounce Rate', 'Monthly Actual': 0.15},
    {'Month': 'January2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Posts', 'Monthly Actual': 3.0},
    {'Month': 'January2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn Posts', 'Monthly Actual': 3.0},
    {'Month': 'January2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook Posts', 'Monthly Actual': 3.0},
    {'Month': 'January2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Follower Count', 'Monthly Actual': 6.0},
    {'Month': 'January2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Linkedin Follower Count', 'Monthly Actual': 403.0},
    {'Month': 'January2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook follower Count', 'Monthly Actual': 0.0},
    {'Month': 'January2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 12.0},
    {'Month': 'January2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 13327.0},
    {'Month': 'January2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 258.0},
    {'Month': 'January2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Engagement', 'Monthly Actual': 428.0},
    {'Month': 'January2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 272.0},
    {'Month': 'January2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 18.0},
    {'Month': 'January2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Impressions', 'Monthly Actual': 8104.0},
    {'Month': 'January2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 393.0},
    {'Month': 'January2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 45.0},
    {'Month': 'January2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 393.0},
    {'Month': 'January2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'New Followers', 'Monthly Actual': 66.0},
    {'Month': 'January2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 4.0},
    {'Month': 'January2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 2459.0},
    {'Month': 'January2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 142.0},
    {'Month': 'January2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 35.0},
    {'Month': 'January2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 142.0},
    {'Month': 'January2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 63.0},
    {'Month': 'February2025', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales connection requests', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'SALES', 'Sub Category': 'Connection requests acceptance rate', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings booked', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings completed', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'SALES', 'Sub Category': 'Conversions', 'Monthly Actual': 1.0},
    {'Month': 'February2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'LinkedIn Newsletter Subscriber count', 'Monthly Actual': 4823.0},
    {'Month': 'February2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'New subscribers', 'Monthly Actual': 80.0},
    {'Month': 'February2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'Impressions', 'Monthly Actual': 2726.0},
    {'Month': 'February2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Subscriber count', 'Monthly Actual': 2662.0},
    {'Month': 'February2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Unsubscribed', 'Monthly Actual': 22.0},
    {'Month': 'February2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Sent', 'Monthly Actual': 10695.0},
    {'Month': 'February2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Soft Bounce', 'Monthly Actual': 155.0},
    {'Month': 'February2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Hard Bounce', 'Monthly Actual': 18.0},
    {'Month': 'February2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Posts', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn Posts', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook Posts', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Follower Count', 'Monthly Actual': 6.0},
    {'Month': 'February2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Linkedin Follower Count', 'Monthly Actual': 1688.0},
    {'Month': 'February2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook follower Count', 'Monthly Actual': 0.0},
    {'Month': 'February2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 13.0},
    {'Month': 'February2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 9549.0},
    {'Month': 'February2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 127.0},
    {'Month': 'February2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 135.0},
    {'Month': 'February2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 15.0},
    {'Month': 'February2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Impressions', 'Monthly Actual': 9453.0},
    {'Month': 'February2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 448.0},
    {'Month': 'February2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 92.0},
    {'Month': 'February2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'New Followers', 'Monthly Actual': 57.0},
    {'Month': 'February2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 4.0},
    {'Month': 'February2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 5373.0},
    {'Month': 'February2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 196.0},
    {'Month': 'February2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 83.0},
    {'Month': 'February2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 86.0},
    {'Month': 'February2025', 'Main Category': 'SITANSHU', 'Sub Category': 'No of posts posted', 'Monthly Actual': 6.0},
    {'Month': 'February2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Impressions', 'Monthly Actual': 3302.0},
    {'Month': 'February2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 100.0},
    {'Month': 'February2025', 'Main Category': 'SITANSHU', 'Sub Category': 'New Followers', 'Monthly Actual': 36.0},
    {'Month': 'March2025', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales connection requests', 'Monthly Actual': 783.0},
    {'Month': 'March2025', 'Main Category': 'SALES', 'Sub Category': 'Accepted connection requests', 'Monthly Actual': 174.0},
    {'Month': 'March2025', 'Main Category': 'SALES', 'Sub Category': 'Connection requests acceptance rate', 'Monthly Actual': 0.244},
    {'Month': 'March2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings booked', 'Monthly Actual': 18.0},
    {'Month': 'March2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings completed', 'Monthly Actual': 13.0},
    {'Month': 'March2025', 'Main Category': 'SALES', 'Sub Category': 'Conversions', 'Monthly Actual': 1.0},
    {'Month': 'March2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'LinkedIn Newsletter Subscriber count', 'Monthly Actual': 1296.0},
    {'Month': 'March2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'New subscribers', 'Monthly Actual': 68.0},
    {'Month': 'March2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'Impressions', 'Monthly Actual': 2048.0},
    {'Month': 'March2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Subscriber count', 'Monthly Actual': 2646.0},
    {'Month': 'March2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Unsubscribed', 'Monthly Actual': 20.0},
    {'Month': 'March2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Soft Bounce', 'Monthly Actual': 168.0},
    {'Month': 'March2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Hard Bounce', 'Monthly Actual': 15.0},
    {'Month': 'March2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Posts', 'Monthly Actual': 4.0},
    {'Month': 'March2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn Posts', 'Monthly Actual': 4.0},
    {'Month': 'March2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook Posts', 'Monthly Actual': 4.0},
    {'Month': 'March2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Follower Count', 'Monthly Actual': 15.0},
    {'Month': 'March2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Linkedin Follower Count', 'Monthly Actual': 546.0},
    {'Month': 'March2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook follower Count', 'Monthly Actual': 1.0},
    {'Month': 'March2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 15.0},
    {'Month': 'March2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 10131.0},
    {'Month': 'March2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 207.0},
    {'Month': 'March2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Engagement', 'Monthly Actual': 395.0},
    {'Month': 'March2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 428.0},
    {'Month': 'March2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 16.0},
    {'Month': 'March2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Impressions', 'Monthly Actual': 23625.0},
    {'Month': 'March2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 969.0},
    {'Month': 'March2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 130.0},
    {'Month': 'March2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'New Followers', 'Monthly Actual': 232.0},
    {'Month': 'March2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 4.0},
    {'Month': 'March2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 1573.0},
    {'Month': 'March2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 79.0},
    {'Month': 'March2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 45.0},
    {'Month': 'March2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 28.0},
    {'Month': 'March2025', 'Main Category': 'SITANSHU', 'Sub Category': 'No of posts posted', 'Monthly Actual': 14.0},
    {'Month': 'March2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Impressions', 'Monthly Actual': 5227.0},
    {'Month': 'March2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 111.0},
    {'Month': 'March2025', 'Main Category': 'SITANSHU', 'Sub Category': 'New Followers', 'Monthly Actual': 33.0},
    {'Month': 'April2025', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales connection requests', 'Monthly Actual': 170.0},
    {'Month': 'April2025', 'Main Category': 'SALES', 'Sub Category': 'Accepted connection requests', 'Monthly Actual': 54.0},
    {'Month': 'April2025', 'Main Category': 'SALES', 'Sub Category': 'Connection requests acceptance rate', 'Monthly Actual': 0.6434},
    {'Month': 'April2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings booked', 'Monthly Actual': 30.0},
    {'Month': 'April2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings completed', 'Monthly Actual': 23.0},
    {'Month': 'April2025', 'Main Category': 'SALES', 'Sub Category': 'Conversions', 'Monthly Actual': 0.0},
    {'Month': 'April2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'LinkedIn Newsletter Subscriber count', 'Monthly Actual': 1361.0},
    {'Month': 'April2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'New subscribers', 'Monthly Actual': 65.0},
    {'Month': 'April2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'Impressions', 'Monthly Actual': 5706.0},
    {'Month': 'April2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Subscriber count', 'Monthly Actual': 2630.0},
    {'Month': 'April2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Unsubscribed', 'Monthly Actual': 16.0},
    {'Month': 'April2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Soft Bounce', 'Monthly Actual': 123.0},
    {'Month': 'April2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Hard Bounce', 'Monthly Actual': 28.0},
    {'Month': 'April2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Posts', 'Monthly Actual': 10.0},
    {'Month': 'April2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn Posts', 'Monthly Actual': 10.0},
    {'Month': 'April2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook Posts', 'Monthly Actual': 10.0},
    {'Month': 'April2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Follower Count', 'Monthly Actual': 8.0},
    {'Month': 'April2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Linkedin Follower Count', 'Monthly Actual': 604.0},
    {'Month': 'April2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook follower Count', 'Monthly Actual': 5.0},
    {'Month': 'April2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 16.0},
    {'Month': 'April2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 13849.0},
    {'Month': 'April2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 290.0},
    {'Month': 'April2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Engagement', 'Monthly Actual': 273.0},
    {'Month': 'April2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 520.0},
    {'Month': 'April2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Total follower count', 'Monthly Actual': 10395.0},
    {'Month': 'April2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 10.0},
    {'Month': 'April2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Impressions', 'Monthly Actual': 29424.0},
    {'Month': 'April2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 1080.0},
    {'Month': 'April2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 102.0},
    {'Month': 'April2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'New Followers', 'Monthly Actual': 270.0},
    {'Month': 'April2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 1131.0},
    {'Month': 'April2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 4.0},
    {'Month': 'April2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 2077.0},
    {'Month': 'April2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 106.0},
    {'Month': 'April2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 23.0},
    {'Month': 'April2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 83.0},
    {'Month': 'April2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 673.0},
    {'Month': 'April2025', 'Main Category': 'SITANSHU', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 12.0},
    {'Month': 'April2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Impressions', 'Monthly Actual': 6539.0},
    {'Month': 'April2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 219.0},
    {'Month': 'April2025', 'Main Category': 'SITANSHU', 'Sub Category': 'New Followers', 'Monthly Actual': 185.0},
    {'Month': 'April2025', 'Main Category': 'HOZEFA', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 0.0},
    {'Month': 'April2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Impressions', 'Monthly Actual': 2177.0},
    {'Month': 'April2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 45.0},
    {'Month': 'April2025', 'Main Category': 'HOZEFA', 'Sub Category': 'New Followers', 'Monthly Actual': 34.0},
    {'Month': 'April2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 2319.0},
    {'Month': 'May2025', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales connection requests', 'Monthly Actual': 391.0},
    {'Month': 'May2025', 'Main Category': 'SALES', 'Sub Category': 'Accepted connection requests', 'Monthly Actual': 82.0},
    {'Month': 'May2025', 'Main Category': 'SALES', 'Sub Category': 'Connection requests acceptance rate', 'Monthly Actual': 0.156371964},
    {'Month': 'May2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings booked', 'Monthly Actual': 42.0},
    {'Month': 'May2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings completed', 'Monthly Actual': 33.0},
    {'Month': 'May2025', 'Main Category': 'SALES', 'Sub Category': 'Conversions', 'Monthly Actual': 2.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 15.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 12424.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 197.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Engagement', 'Monthly Actual': 344.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 294.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Total follower count', 'Monthly Actual': 10743.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'All Appearances', 'Monthly Actual': 26895.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Comments', 'Monthly Actual': 131.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Posts', 'Monthly Actual': 165.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Network Recommendations', 'Monthly Actual': 90.0},
    {'Month': 'May2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Search', 'Monthly Actual': 16.0},
    {'Month': 'May2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 10.0},
    {'Month': 'May2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Impressions', 'Monthly Actual': 12383.0},
    {'Month': 'May2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 498.0},
    {'Month': 'May2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 171.0},
    {'Month': 'May2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'New Followers', 'Monthly Actual': 107.0},
    {'Month': 'May2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 4.0},
    {'Month': 'May2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 1730.0},
    {'Month': 'May2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 57.0},
    {'Month': 'May2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 205.0},
    {'Month': 'May2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 301.0},
    {'Month': 'May2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 1029.0},
    {'Month': 'May2025', 'Main Category': 'SITANSHU', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 7.0},
    {'Month': 'May2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Impressions', 'Monthly Actual': 6032.0},
    {'Month': 'May2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 196.0},
    {'Month': 'May2025', 'Main Category': 'SITANSHU', 'Sub Category': 'New Followers', 'Monthly Actual': 197.0},
    {'Month': 'May2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 817.0},
    {'Month': 'May2025', 'Main Category': 'HOZEFA', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 5.0},
    {'Month': 'May2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Impressions', 'Monthly Actual': 4058.0},
    {'Month': 'May2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 110.0},
    {'Month': 'May2025', 'Main Category': 'HOZEFA', 'Sub Category': 'New Followers', 'Monthly Actual': 149.0},
    {'Month': 'May2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 2477.0},
    {'Month': 'May2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'LinkedIn Newsletter Subscriber count', 'Monthly Actual': 1403.0},
    {'Month': 'May2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'New subscribers', 'Monthly Actual': 42.0},
    {'Month': 'May2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'Impressions', 'Monthly Actual': 2192.0},
    {'Month': 'May2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Subscriber count', 'Monthly Actual': 2631.0},
    {'Month': 'May2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Unsubscribed', 'Monthly Actual': 6.0},
    {'Month': 'May2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Soft Bounce', 'Monthly Actual': 187.0},
    {'Month': 'May2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Hard Bounce', 'Monthly Actual': 26.0},
    {'Month': 'May2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Posts', 'Monthly Actual': 8.0},
    {'Month': 'May2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn Posts', 'Monthly Actual': 8.0},
    {'Month': 'May2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook Posts', 'Monthly Actual': 8.0},
    {'Month': 'May2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Follower Count', 'Monthly Actual': 12.0},
    {'Month': 'May2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Linkedin Follower Count', 'Monthly Actual': 604.0},
    {'Month': 'May2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Linkedin New Followers', 'Monthly Actual': 40.0},
    {'Month': 'May2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook follower Count', 'Monthly Actual': 4.0},
    {'Month': 'May2025', 'Main Category': 'LINKEDIN COMPANY PAGE', 'Sub Category': 'Impressions', 'Monthly Actual': 672.0},
    {'Month': 'May2025', 'Main Category': 'LINKEDIN COMPANY PAGE', 'Sub Category': 'Reactions', 'Monthly Actual': 26.0},
    {'Month': 'May2025', 'Main Category': 'LINKEDIN COMPANY PAGE', 'Sub Category': 'Total unique visitors', 'Monthly Actual': 193.0},
    {'Month': 'May2025', 'Main Category': 'ATHARVA VIDEO EDITOR', 'Sub Category': 'Videos edited', 'Monthly Actual': 9.0},
    {'Month': 'May2025', 'Main Category': 'ATHARVA VIDEO EDITOR', 'Sub Category': 'Videos posted', 'Monthly Actual': 0.0},
    {'Month': 'June2025', 'Main Category': 'SALES', 'Sub Category': 'Jahnvi Sales connection requests', 'Monthly Actual': 605.0},
    {'Month': 'June2025', 'Main Category': 'SALES', 'Sub Category': 'Accepted connection requests', 'Monthly Actual': 193.0},
    {'Month': 'June2025', 'Main Category': 'SALES', 'Sub Category': 'Connection requests acceptance rate', 'Monthly Actual': 0.3323},
    {'Month': 'June2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings booked', 'Monthly Actual': 29.0},
    {'Month': 'June2025', 'Main Category': 'SALES', 'Sub Category': 'Meetings completed', 'Monthly Actual': 25.0},
    {'Month': 'June2025', 'Main Category': 'SALES', 'Sub Category': 'Conversions', 'Monthly Actual': 2.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 12.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 10802.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 189.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Engagement', 'Monthly Actual': 393.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 370.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'All Appearances', 'Monthly Actual': 23447.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Comments', 'Monthly Actual': 162.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Posts', 'Monthly Actual': 172.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Network Recommendations', 'Monthly Actual': 57.0},
    {'Month': 'June2025', 'Main Category': 'TEJAS JHAVERI', 'Sub Category': 'Search', 'Monthly Actual': 16.0},
    {'Month': 'June2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 8.0},
    {'Month': 'June2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Impressions', 'Monthly Actual': 10429.0},
    {'Month': 'June2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 409.0},
    {'Month': 'June2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 66.0},
    {'Month': 'June2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'New Followers', 'Monthly Actual': 72.0},
    {'Month': 'June2025', 'Main Category': 'SHIRIN DHABHAR', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 1270.0},
    {'Month': 'June2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'No of posts posted', 'Monthly Actual': 2.0},
    {'Month': 'June2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Profile Viewers (Bi-monthly)', 'Monthly Actual': 328.0},
    {'Month': 'June2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Engagement metrics', 'Monthly Actual': 46.0},
    {'Month': 'June2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 1713.0},
    {'Month': 'June2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 323.0},
    {'Month': 'June2025', 'Main Category': 'HEMAL JHAVERI', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 1353.0},
    {'Month': 'June2025', 'Main Category': 'SITANSHU', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 11.0},
    {'Month': 'June2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Impressions', 'Monthly Actual': 8117.0},
    {'Month': 'June2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 112.0},
    {'Month': 'June2025', 'Main Category': 'SITANSHU', 'Sub Category': 'New Followers', 'Monthly Actual': 106.0},
    {'Month': 'June2025', 'Main Category': 'SITANSHU', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 911.0},
    {'Month': 'June2025', 'Main Category': 'HOZEFA', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 3.0},
    {'Month': 'June2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Impressions', 'Monthly Actual': 5443.0},
    {'Month': 'June2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 180.0},
    {'Month': 'June2025', 'Main Category': 'HOZEFA', 'Sub Category': 'New Followers', 'Monthly Actual': 161.0},
    {'Month': 'June2025', 'Main Category': 'HOZEFA', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 2632.0},
    {'Month': 'June2025', 'Main Category': 'SANDEEP KHEMKA', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 3.0},
    {'Month': 'June2025', 'Main Category': 'SANDEEP KHEMKA', 'Sub Category': 'Impressions', 'Monthly Actual': 1816.0},
    {'Month': 'June2025', 'Main Category': 'SANDEEP KHEMKA', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 79.0},
    {'Month': 'June2025', 'Main Category': 'SANDEEP KHEMKA', 'Sub Category': 'New Followers', 'Monthly Actual': 18.0},
    {'Month': 'June2025', 'Main Category': 'SANDEEP KHEMKA', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 2610.0},
    {'Month': 'June2025', 'Main Category': 'MOHIT JHAVERI', 'Sub Category': 'No of text + image posts posted', 'Monthly Actual': 1.0},
    {'Month': 'June2025', 'Main Category': 'MOHIT JHAVERI', 'Sub Category': 'Impressions', 'Monthly Actual': 0.0},
    {'Month': 'June2025', 'Main Category': 'MOHIT JHAVERI', 'Sub Category': 'Profile viewers (Bi-Monthly)', 'Monthly Actual': 0.0},
    {'Month': 'June2025', 'Main Category': 'MOHIT JHAVERI', 'Sub Category': 'New Followers', 'Monthly Actual': 17.0},
    {'Month': 'June2025', 'Main Category': 'MOHIT JHAVERI', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 56.0},
    {'Month': 'June2025', 'Main Category': 'ARPIT AGGARWAL', 'Sub Category': 'Total Follower Count', 'Monthly Actual': 448.0},
    {'Month': 'June2025', 'Main Category': 'LINKEDIN NEWSLETTER', 'Sub Category': 'New subscribers', 'Monthly Actual': 25.0},
    {'Month': 'June2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Unsubscribed', 'Monthly Actual': 27.0},
    {'Month': 'June2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Soft Bounce', 'Monthly Actual': 83.0},
    {'Month': 'June2025', 'Main Category': 'EMAIL NEWSLETTER', 'Sub Category': 'Hard Bounce', 'Monthly Actual': 10.0},
    {'Month': 'June2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Instagram Posts', 'Monthly Actual': 8.0},
    {'Month': 'June2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'LinkedIn Posts', 'Monthly Actual': 8.0},
    {'Month': 'June2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook Posts', 'Monthly Actual': 8.0},
    {'Month': 'June2025', 'Main Category': 'MYNTMORE MARKETING', 'Sub Category': 'Facebook follower Count', 'Monthly Actual': 4.0},
    {'Month': 'June2025', 'Main Category': 'ATHARVA VIDEO EDITOR', 'Sub Category': 'Videos edited', 'Monthly Actual': 5.0},
    {'Month': 'June2025', 'Main Category': 'ATHARVA VIDEO EDITOR', 'Sub Category': 'Videos posted', 'Monthly Actual': 5.0},
]


# ---------------------------
# 🚀 Convert to DataFrame
# ---------------------------
data = pd.DataFrame(data_records)

# Ensure correct numeric types
data["Monthly Actual"] = pd.to_numeric(data["Monthly Actual"], errors="coerce")

# Drop rows with missing Main Category or Sub Category
data = data.dropna(subset=["Main Category", "Sub Category"])

# Drop rows where Monthly Actual is NaN (prevents KeyError in groupby)
data = data.dropna(subset=["Monthly Actual"])

# ---------------------------
# 🔍 Compute high & low per (Main + Sub Category)
# ---------------------------
high_low = data.groupby(["Main Category", "Sub Category"]).apply(
    lambda x: pd.Series({
        "High Score": x["Monthly Actual"].max(),
        "High Month": x.loc[x["Monthly Actual"].idxmax(), "Month"],
        "Low Score": x["Monthly Actual"].min(),
        "Low Month": x.loc[x["Monthly Actual"].idxmin(), "Month"]
    })
).reset_index()

# ---------------------------
# 🎨 Streamlit UI
# ---------------------------
st.title("📊 Monthly Data Visualisation Across Categories")

def parse_month_year(month_str):
    # e.g., 'December2024'
    for i, name in enumerate(calendar.month_name):
        if name and month_str.startswith(name):
            year = int(month_str[len(name):])
            return year, i
    return (0, 0)

unique_months = sorted(data["Month"].dropna().unique(), key=parse_month_year)
month_cat_type = CategoricalDtype(categories=unique_months, ordered=True)
data["Month"] = data["Month"].astype(month_cat_type)

selected_category = st.selectbox("Pick a main category", data["Main Category"].dropna().unique())
filtered_data = data[data["Main Category"] == selected_category]

selected_subcategory = st.selectbox("Pick a sub category", filtered_data["Sub Category"].unique())
chart_data = filtered_data[filtered_data["Sub Category"] == selected_subcategory]

# Ensure chart_data is sorted by Month for correct plotting
chart_data = chart_data.sort_values("Month")

# Chart
st.line_chart(chart_data.set_index("Month")["Monthly Actual"])

# High/Low summary
hl_row = high_low[(high_low["Main Category"] == selected_category) & (high_low["Sub Category"] == selected_subcategory)]
if not hl_row.empty:
    st.success(f"Highest: {hl_row['High Score'].values[0]} in {hl_row['High Month'].values[0]}")
    st.error(f"Lowest: {hl_row['Low Score'].values[0]} in {hl_row['Low Month'].values[0]}")

# ---------------------------
# 📝 Notes
# ---------------------------
st.caption("All data embedded. High & Low computed per Main+Sub category. Ready for Streamlit Cloud deployment.")
