
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
day_df = pd.read_csv('day.csv')

# Convert the 'dteday' column to a datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Plot total users over time
st.title('Bike Sharing Data Dashboard')

st.subheader('Total Bike Rentals Over Time')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(day_df['dteday'], day_df['cnt'], label='Total Users (cnt)', color='blue')
ax.set_xlabel('Date')
ax.set_ylabel('Total Users')
ax.set_title('Total Bike Sharing Users Over Time (Daily)')
ax.grid(True)
st.pyplot(fig)

# High usage days (based on the 75th percentile)
high_usage_threshold = day_df['cnt'].quantile(0.75)
day_df['high_usage'] = (day_df['cnt'] > high_usage_threshold).astype(int)

# Monthly RFM-like analysis
monthly_high_usage_freq = day_df.groupby(['yr', 'mnth'])['high_usage'].sum().reset_index()
monthly_high_usage_freq.columns = ['Year', 'Month', 'High Usage Days']

monthly_monetary = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
monthly_monetary.columns = ['Year', 'Month', 'Total Rentals']

rfm_df = pd.merge(monthly_high_usage_freq, monthly_monetary, on=['Year', 'Month'])

# Display RFM-like analysis
st.subheader('Monthly High Usage Days and Total Rentals')
st.dataframe(rfm_df)

streamlit run dashboard.py