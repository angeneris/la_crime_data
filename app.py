import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
import streamlit as st


crime = pd.read_csv('/Users/angeneris/la_crime_data/la_crime_data-1/crime_data_2020_to_present.csv', parse_dates=['date_reported', 'crime_date'])

# Sort the data by 'date_reported' for ease of analysis
crime = crime.sort_values(by='date_reported')


st.header('Crimes in Los Angeles between 2020 - Present', divider='blue')
st.write('Visual Report by Angeneris Cifuentes')

st.write(crime)

# Creates an update message
max_crime = crime['date_reported'].max()

# Displays the message
st.write(f'The latest crime reported occurred on: {max_crime}')


# Extracts year, month, and date from the 'crime_date' column
crime['year'] = crime['crime_date'].dt.year
crime['month'] = crime['crime_date'].dt.month
crime['day'] = crime['crime_date'].dt.day

# Group by year to see trends over time
yearly_trends = crime.groupby('year').size().reset_index(name='total_crimes')
st.write(yearly_trends)


# Group and count occurrences of each combination of year and status
crime_data_grouped = crime_data.groupby(['year', 'status']).size().reset_index(name='count')

# Sort the grouped data by 'year' and 'count' in descending order
crime_data_grouped_sorted = crime_data_grouped.sort_values(by=['year', 'count'], ascending=[True, False])

# Create scatterplot using Streamlit
st.title('Count of Crimes by Year and Status')
selected_status = st.multiselect('Select Status:', crime_data_grouped_sorted['status'].unique())

filtered_data = crime_data_grouped_sorted[crime_data_grouped_sorted['status'].isin(selected_status)]

fig, ax = plt.subplots(figsize=(12, 8))
for status in selected_status:
    data = filtered_data[filtered_data['status'] == status]
    ax.scatter(data['year'], data['count'], label=status, alpha=0.8)

ax.set_xlabel('Year')
ax.set_ylabel('Count of Crimes')
ax.legend()
ax.grid(True)


# Count the occurrence of each crime type 
crime_counts = crime['crime_area'].value_counts()



# Display a search box to filter records by neighborhood
neighborhood = st.text_input('Enter a neighborhood:', '')
filtered_data = crime_data[crime_data['crime_area'].str.contains(neighborhood, case=False)]
st.write(filtered_data)

# Plot the Crimes in the Top 10 Neighborhoods with Crimes Reported in LA'
top_10 = plt.figure(figsize=(8,6))
sns.barplot(x=crime_counts.head(10).values, y=crime_counts.head(10).index)
plt.xlabel('Number of Crimes Committed')
plt.ylabel('Los Angeles Neighborhood')
plt.title('Top 10 Neighborhoods with Crimes Reported in LA')
st.pyplot(top_10)


# Count the occurrence of each crime type 
crime_counts = crime['crime'].value_counts()


# Creates a histogram viewing only the days between when crimes occur and their reporting are a week or less

reported_crime = crime[crime['days_between_report'] < 8]

fig = px.histogram(reported_crime, x='days_between_report', title='Histogram of Days Between Crimes and Reporting of Crimes',
                   labels={'days_between_report': 'Days Between Crimes and Reporting of Crimes'}, histfunc= 'count', nbins=5)

# Show the plot
st.write(fig)

