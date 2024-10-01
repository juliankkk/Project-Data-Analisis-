import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV files (Update the path to your actual CSV files)
hour_data = pd.read_csv('hour.csv')
day_data = pd.read_csv('day.csv')

# Set up Streamlit layout
st.title("Advanced Bike Rentals Dashboard with Filters")

st.write("""
## Explore bike rental trends with advanced techniques like RFM Analysis and Clustering. 
Use the filters to customize the data.
""")

# Filter: Select Season (for daily data)
season_filter = st.selectbox(
    'Select Season for RFM Analysis',
    options=[1, 2, 3, 4],
    format_func=lambda x: {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}[x],
    help="Filter bike rentals by season."
)

# Filter: Select Weather Situation (for hourly data)
weather_filter = st.selectbox(
    'Select Weather Condition for Clustering by Time of Day',
    options=[1, 2, 3, 4],
    format_func=lambda x: {
        1: 'Clear, Few clouds', 2: 'Mist + Cloudy', 3: 'Light Snow or Rain', 4: 'Heavy Rain or Snow'
    }[x],
    help="Filter bike rentals by weather condition."
)

# Filter: Select Hour of the Day (for hourly data)
hour_filter = st.slider(
    'Select Hour Range for Clustering by Time of Day',
    min_value=0, max_value=23, value=(0, 23),
    help="Filter bike rentals between specific hours of the day."
)

# --- RFM Analysis ---
st.write("### RFM Analysis (Filtered by Season)")

# Filter daily data by season
filtered_day_data = day_data[day_data['season'] == season_filter]

# Recency: Menghitung berapa hari sejak terakhir kali pengguna menyewa sepeda
filtered_day_data['dteday'] = pd.to_datetime(filtered_day_data['dteday'])
most_recent_date = filtered_day_data['dteday'].max()

# Recency
filtered_day_data['recency'] = (most_recent_date - filtered_day_data['dteday']).dt.days

# Frequency and Monetary (using 'cnt' as a proxy)
filtered_day_data['frequency'] = filtered_day_data['cnt']
filtered_day_data['monetary'] = filtered_day_data['cnt']

# Membuat dataframe RFM
rfm_data = filtered_day_data[['recency', 'frequency', 'monetary']].copy()

# Mengelompokkan RFM berdasarkan kuartil
rfm_data['R'] = pd.qcut(rfm_data['recency'], 4, labels=[4, 3, 2, 1])
rfm_data['F'] = pd.qcut(rfm_data['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm_data['M'] = pd.qcut(rfm_data['monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4])

# Skor RFM
rfm_data['RFM_Score'] = rfm_data[['R', 'F', 'M']].sum(axis=1)

st.write(rfm_data[['recency', 'frequency', 'monetary', 'RFM_Score']].head())

# --- Clustering (Binning) Based on Time of Day ---
st.write("### Clustering by Time of Day (Filtered by Weather and Hour Range)")

# Filter hourly data by weather and hour range
filtered_hour_data = hour_data[
    (hour_data['hr'] >= hour_filter[0]) &
    (hour_data['hr'] <= hour_filter[1]) &
    (hour_data['weathersit'] == weather_filter)
].copy()  # Make a copy to avoid modification on the original dataframe

# Membuat bins (klasifikasi manual) berdasarkan jam
bins = [0, 6, 12, 18, 24]
labels = ['Night', 'Morning', 'Afternoon', 'Evening']

# Membuat kolom baru 'time_of_day' menggunakan .loc untuk menghindari masalah "SettingWithCopyWarning"
filtered_hour_data.loc[:, 'time_of_day'] = pd.cut(filtered_hour_data['hr'], bins=bins, labels=labels, right=False)

# Mengelompokkan jumlah rental berdasarkan waktu
grouped_data = filtered_hour_data.groupby('time_of_day')['cnt'].sum().reset_index()

# Visualisasi cluster berdasarkan waktu
fig_time_of_day = px.bar(grouped_data, x='time_of_day', y='cnt', title='Bike Rentals by Time of Day')
st.plotly_chart(fig_time_of_day)

# --- Additional visualizations ---
st.write("### Additional Visualizations")
# Hourly bike rentals trend
fig_hourly = px.line(filtered_hour_data, x='hr', y='cnt', title='Hourly Bike Rentals Trend')
st.plotly_chart(fig_hourly)

# Daily bike rentals trend (with season filter)
fig_daily = px.line(filtered_day_data, x='dteday', y='cnt', title='Daily Bike Rentals Trend')
st.plotly_chart(fig_daily)
