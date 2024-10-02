import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Menyiapkan data 
day_df = pd.read_csv("day.csv")
day_df.head()

# Menghapus variabel instant
drop_col = ['instatnt']

for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)

# Mengubah nama variabel
day_df.rename(columns={
    'dteday': 'date',
    'mnth': 'month',
    'yr': 'year',
    'weathersit': 'weather',
    'hr': 'hour',
    'workingday': 'workday',
    'cnt': 'count',
    'hum': 'humidity',
    'temp': 'temperature',
    'atemp': 'feeling_temperature'
    }, inplace=True)

# Mengubah keterangan data 
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
day_df['weather'] = day_df['weather'].map({
    1: 'Cerah',
    2: 'Berawan',
    3: 'Hujan',
    4: 'Cuaca Buruk'})

def create_daily_user(df):
    daily_user = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily_user

def create_daily_casual_user(df):
    create_daily_casual_user = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return create_daily_casual_user

def create_daily_registered_user(df):
    daily_registered_user = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_user   

def create_season_user(df):
    season_user = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_user

def create_monthly_user(df):
    monthly_user = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_user = monthly_user.reindex(ordered_months, fill_value=0)
    return monthly_user

def create_weekday_user(df):
    weekday_user = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_user

def create_workday_user(df):
    workday_user = df.groupby(by='workday').agg({
        'count': 'sum'
    }).reset_index()
    return workday_user

def create_holiday_user(df):
    holiday_user = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_user

def create_weather_cond_user(df):
    weather_cond_user = df.groupby(by='weather').agg({
        'count': 'sum'
    })
    return weather_cond_user


# Membuat komponen filter
min_date = pd.to_datetime(day_df['date']).dt.date.min()
max_date = pd.to_datetime(day_df['date']).dt.date.max()
 
with st.sidebar:
    st.image("https://github.com/juliankkk/Project-Data-Analisis-/blob/main/Picture1.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['date'] >= str(start_date)) & 
                (day_df['date'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_user = create_daily_user(main_df)
daily_casual_user = create_daily_casual_user(main_df)
daily_registered_user = create_daily_registered_user(main_df)
season_user = create_season_user(main_df)
monthly_user = create_monthly_user(main_df)
weekday_user= create_weekday_user(main_df)
workday_user = create_workday_user(main_df)
holiday_user = create_holiday_user(main_df)
weather_cond_user = create_weather_cond_user(main_df)
