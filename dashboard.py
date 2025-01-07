import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# PREPARING REQUIRED DATA
def fetch_and_merge_data():
    # CSV files
    files = [
        'PRSA_Data_Aotizhongxin_20130301-20170228.csv',
        'PRSA_Data_Changping_20130301-20170228.csv',
        'PRSA_Data_Dingling_20130301-20170228.csv',
        'PRSA_Data_Dongsi_20130301-20170228.csv',
        'PRSA_Data_Guanyuan_20130301-20170228.csv',
        'PRSA_Data_Gucheng_20130301-20170228.csv',
        'PRSA_Data_Huairou_20130301-20170228.csv',
        'PRSA_Data_Nongzhanguan_20130301-20170228.csv',
        'PRSA_Data_Shunyi_20130301-20170228.csv',
        'PRSA_Data_Tiantan_20130301-20170228.csv',
        'PRSA_Data_Wanliu_20130301-20170228.csv',
        'PRSA_Data_Wanshouxigong_20130301-20170228.csv'
    ]

    # Base URL prefix
    base_url = './PRSA_Data_20130301-20170228/'

    # Initialize an empty list to store DataFrames
    df_list = []

    # Loop through each file, fetch and read into DataFrame
    for file in files:
        file_url = base_url + file
        df = pd.read_csv(file_url)
        df_list.append(df)

    # Merge all DataFrames into one
    merged_df = pd.concat(df_list, ignore_index=True)

    return merged_df

def fill_na(df):
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:  # Check if numeric column and fill with mean
            df[column] = df[column].fillna(df[column].mean())
        else:  # If non-numeric column, fill with mode
            df[column] = df[column].fillna(df[column].mode()[0])

df = fetch_and_merge_data()
fill_na(df)


# CREATE DASHBOARD
# Sidebar filters
st.sidebar.header('Filters')
selected_station = st.sidebar.selectbox('Select Station', options=['All Stations'] + list(df['station'].unique()))
selected_year = st.sidebar.selectbox('Select Year', options=['All Years'] + list(df['year'].unique()))
selected_pollutant = st.sidebar.selectbox('Select Pollutant', options=['All Pollutants'] + ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])

# Filtered data
if selected_station != 'All Stations':
    filtered_df = df[df['station'] == selected_station]
else:
    filtered_df = df

if selected_year != 'All Years':
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

st.title('Air Quality Dashboard')

# Yearly Trend Visualization (with pollutant filter)
st.header('Yearly Trend of Pollutants')

# If 'All Pollutants' is selected, plot all pollutants
if selected_pollutant == 'All Pollutants':
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
else:
    pollutants = [selected_pollutant]

# Calculate monthly averages for the selected pollutants
monthly_avg = filtered_df.groupby('month')[pollutants].mean()

fig, ax = plt.subplots(figsize=(10, 6))
monthly_avg.plot(kind='line', ax=ax)
ax.set_title(f'Monthly Average {', '.join(pollutants)} Levels')
ax.set_xlabel('Month')
ax.set_ylabel('Concentration (µg/m³)')
ax.grid(True)

st.pyplot(fig)

# Scatter Plot Visualization (Temperature vs. Pollutant)
st.header(f'Scatter Plot: TEMP vs {selected_pollutant}')

fig, ax = plt.subplots(figsize=(6, 4))
if selected_pollutant == 'All Pollutants':
    for pollutant in pollutants:
        sns.scatterplot(x=filtered_df['TEMP'], y=filtered_df[pollutant], label=pollutant, ax=ax)
    ax.set_title('Correlation between TEMP and All Pollutants')
else:
    sns.scatterplot(x=filtered_df['TEMP'], y=filtered_df[selected_pollutant], ax=ax)
    ax.set_title(f'Correlation between TEMP and {selected_pollutant}')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel(f'Concentration (µg/m³)')

st.pyplot(fig)