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
    st.image("https://raw.githubusercontent.com/juliankkk/Project-Data-Analisis-/9332ece5d4c78f645627c348e9e9821eda09d65b/Picture1.png")
    st.sidebar.header("Filter:")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date Range',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Visit my Profile:")

st.sidebar.markdown("Julian Kurnianto")

col1, col2 = st.sidebar.columns(2)

with col1:
    st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](www.linkedin.com/in/julian-kurnianto-190096233)")
with col2:
    st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/juliankkk)")


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

# Membuat Dashboard 

# judul
st.header('Bike Rental Bike Bennish Dashboard')

# jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_user_casual = daily_casual_user['casual'].sum()
    st.metric('Casual User', value= daily_user_casual)

with col2:
    daily_user_registered = daily_registered_user['registered'].sum()
    st.metric('Registered User', value= daily_user_registered)
 
with col3:
    daily_user_total = daily_user['count'].sum()
    st.metric('Total User', value= daily_user_total)

# Membuat jumlah penyewaan bulanan
import matplotlib.pyplot as plt

st.subheader('Monthly Rentals Report')

# Membuat figure dan axes dengan ukuran yang diinginkan
fig, ax = plt.subplots(figsize=(26, 9))

# Mengubah warna garis dan elemen-elemen lainnya menjadi hitam dan putih
ax.plot(
    monthly_user.index,
    monthly_user['count'],
    marker='o', 
    linestyle='-',  # Garis solid untuk model
    linewidth=3,  # Ukuran ketebalan garis
    color='white',  # Mengganti warna garis menjadi hitam
    label='Rental Count'  # Label garis untuk legenda
)

# Menambahkan garis horizontal rata-rata dengan garis hitam-putih (dotted line)
average = monthly_user['count'].mean()
ax.axhline(average, color='gray', linestyle='--', linewidth=2, label=f'Average: {average:.2f}')

# Menambahkan teks angka pada setiap titik data, dengan warna hitam
for index, row in enumerate(monthly_user['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12, color='black')

# Menambahkan legenda
ax.legend(fontsize=20, facecolor='white', edgecolor='white')  # Warna legenda hitam putih

# Mengubah tema menjadi hitam-putih
ax.set_facecolor('black')  # Background putih
fig.patch.set_facecolor('black')  # Background luar putih

# Mengatur ukuran label untuk sumbu x dan y
ax.tick_params(axis='x', labelsize=25, rotation=45, colors='white')  # Label sumbu x hitam
ax.tick_params(axis='y', labelsize=20, colors='white')  # Label sumbu y hitam

# Mengubah warna grid menjadi abu-abu terang
ax.grid(True, color='lightgray')

# Menampilkan chart
st.pyplot(fig)

st.subheader('Seasonly Rentals')

import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(16, 8)) 

# Plot batang untuk "registered"
sns.barplot(
    x='season',
    y='registered',
    data=season_user,
    label='Registered',
    color='black',  # Ganti dengan warna yang lebih netral
    ax=ax
)

# Plot batang untuk "casual"
sns.barplot(
    x='season',
    y='casual',
    data=season_user,
    label='Casual',
    color='grey',  # Ganti dengan warna yang lebih kontras
    ax=ax
)

# Menambahkan nilai di atas masing-masing batang
for index, row in season_user.iterrows():
    ax.text(index, row['registered'] + 10, f"{int(row['registered'])}", ha='center', va='bottom', fontsize=14, color='black')  # Angka di atas "registered"
    ax.text(index, row['casual'] - 10, f"{int(row['casual'])}", ha='center', va='top', fontsize=14, color='white')  # Angka di atas "casual"

# Menambahkan judul
ax.set_title('Registered vs Casual Users by Season', fontsize=22, pad=20)

# Menambahkan label pada sumbu X dan Y
ax.set_xlabel('Season', fontsize=18)
ax.set_ylabel('Number of Users', fontsize=18)

# Memperbesar label sumbu X dan Y
ax.tick_params(axis='x', labelsize=16, rotation=0)
ax.tick_params(axis='y', labelsize=15)

# Menambahkan grid untuk mempermudah pembacaan
ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.7)

# Menambahkan legenda
ax.legend(fontsize=16)

# Menampilkan plot
st.pyplot(fig)

import seaborn as sns
import matplotlib.pyplot as plt

st.subheader('Rental Rate Based on Weather Conditions')

# Grouping the data by weather conditions
weather_cond_user = main_df.groupby(by='weather').agg({
    'count': 'sum'
})

# Creating the figure and axis
fig, ax = plt.subplots(figsize=(16, 8))

# Enhanced color palette
colors = sns.color_palette("Set2", n_colors=len(weather_cond_user))

# Creating a bar plot
sns.barplot(
    x=weather_cond_user.index,
    y=weather_cond_user['count'],
    palette=colors,
    ax=ax
)

# Adding count labels on top of the bars
for index, row in enumerate(weather_cond_user['count']):
    ax.text(index, row + 5, str(row), ha='center', va='bottom', fontsize=15, fontweight='bold')

# Setting titles and labels
ax.set_title('Total Rentals by Weather Conditions', fontsize=22, pad=20)
ax.set_xlabel('Weather Conditions', fontsize=18)
ax.set_ylabel('Total Rentals', fontsize=18)

# Adjusting tick parameters for better readability
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)

# Adding a grid for better readability
ax.yaxis.grid(True, linestyle='--', linewidth=0.7, color='gray')

# Displaying the plot
st.pyplot(fig)
