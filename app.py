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


# Displays the formatted date
st.write(f'The latest crime reported occurred on: {max_crime_formatted}')

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

