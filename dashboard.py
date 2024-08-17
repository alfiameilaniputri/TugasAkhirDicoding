# Save this as dashboard.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

sns.set(style='dark')

# Load datasets
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Convert 'dteday' to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Define helper functions

def create_daily_df(df):
    daily_df = df.resample('D', on='dteday').agg({
        "cnt": "sum",
        "temp": "mean",
        "hum": "mean",
        "windspeed": "mean"
    }).reset_index()
    return daily_df

def create_hourly_df(df):
    hourly_df = df.resample('H', on='dteday').agg({
        "cnt": "sum",
        "temp": "mean",
        "hum": "mean",
        "windspeed": "mean"
    }).reset_index()
    return hourly_df

# Prepare data
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

# Streamlit app
st.header('Bike Sharing Dashboard :sparkles:')

with st.sidebar:
    st.image("https://i.pinimg.com/originals/7c/32/16/7c3216e13194cbaaa23d338ebf4f6d44.png")  # Update with your logo URL
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=min_date.date(),  # Convert to date object for comparison
        max_value=max_date.date(),  # Convert to date object for comparison
        value=[min_date.date(), max_date.date()]
    )

# Convert date inputs to datetime64
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data
filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
filtered_hour_df = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]

# Data preparation
daily_df = create_daily_df(filtered_day_df)
hourly_df = create_hourly_df(filtered_hour_df)

# Daily Orders
st.subheader('Daily Orders')
col1, col2 = st.columns(2)

with col1:
    total_orders = daily_df['cnt'].sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    average_temp = daily_df['temp'].mean()
    st.metric("Average Temperature (°C)", value=f"{average_temp:.2f}")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_df['dteday'], daily_df['cnt'], marker='o', linewidth=2, color="#90CAF9")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Orders")
ax.set_title("Daily Orders")
st.pyplot(fig)

# Hourly Orders
st.subheader('Hourly Orders')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(hourly_df['dteday'], hourly_df['cnt'], marker='o', linewidth=2, color="#90CAF9")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Orders")
ax.set_title("Hourly Orders")
st.pyplot(fig)

# Metrics for temperature, humidity, windspeed
st.subheader('Weather Metrics')
col1, col2, col3 = st.columns(3)

with col1:
    avg_temp = daily_df['temp'].mean()
    st.metric("Average Temperature (°C)", value=f"{avg_temp:.2f}")

with col2:
    avg_hum = daily_df['hum'].mean()
    st.metric("Average Humidity (%)", value=f"{avg_hum:.2f}")

with col3:
    avg_windspeed = daily_df['windspeed'].mean()
    st.metric("Average Windspeed (m/s)", value=f"{avg_windspeed:.2f}")

# Visualization of temperature, humidity, windspeed over time
st.subheader('Weather Over Time')
fig, ax = plt.subplots(nrows=3, figsize=(16, 15))

ax[0].plot(daily_df['dteday'], daily_df['temp'], color="#90CAF9")
ax[0].set_ylabel("Temperature (°C)")
ax[0].set_title("Temperature Over Time")

ax[1].plot(daily_df['dteday'], daily_df['hum'], color="#90CAF9")
ax[1].set_ylabel("Humidity (%)")
ax[1].set_title("Humidity Over Time")

ax[2].plot(daily_df['dteday'], daily_df['windspeed'], color="#90CAF9")
ax[2].set_ylabel("Windspeed (m/s)")
ax[2].set_title("Windspeed Over Time")

for axis in ax:
    axis.set_xlabel("Date")

st.pyplot(fig)

# Analysis Section
st.subheader('Analysis Insights')

# Insight 1: Weather Impact by Month
st.subheader('Impact of Weather on Bike Usage by Month')
weather_usage = day_df.groupby(['mnth', 'weathersit'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='mnth', y='cnt', hue='weathersit', data=weather_usage, ax=ax)
ax.set_title('Impact of Weather on Bike Usage by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Average Bike Usage')
st.pyplot(fig)

# Insight 2: Weekday vs Weekend Usage
st.subheader('Bike Usage on Weekdays vs Weekends')
day_df['is_weekend'] = day_df['weekday'].apply(lambda x: 1 if x == 0 or x == 6 else 0)
weekend_usage = day_df.groupby('is_weekend')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='is_weekend', y='cnt', data=weekend_usage, ax=ax)
ax.set_title('Bike Usage on Weekdays vs Weekends')
ax.set_xlabel('Weekend (1 = Yes, 0 = No)')
ax.set_ylabel('Average Bike Usage')
st.pyplot(fig)

# Footer
st.caption('Copyright (c) Your Name 2024')  # Update with your name
