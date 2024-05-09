import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load crime data
crime = pd.read_csv('crime_data_2020_to_present.csv', parse_dates=['date_reported', 'crime_date'], index_col=False)

# Data preprocessing
crime['date_reported'] = pd.to_datetime(crime['date_reported']).dt.date
crime['crime_date'] = pd.to_datetime(crime['crime_date']).dt.date
crime = crime.sort_values(by='date_reported')

# Displays header and an introduction 
st.header('Crimes in Los Angeles between 2020 - Present')
st.write('Visual Report by Angeneris Cifuentes')

# New Section
st.markdown("---")

# Dataframe Header and summary for the dataframe
st.subheader('Crime Reports in Los Angeles from 2020 - 2024')
st.write('This data belongs to the public and is taken from the public LAPD database detailing crimes that have been reported between the years 2020-2024 in Los Angeles County')

# Displays the dataframe, including a message with the most up-to-date crime reported
st.write(crime)
st.write('The latest reported crime in this dataset occurred on:', crime['date_reported'].max())

# New Section
st.markdown("---")

# Filtering data by any columns 
st.subheader('Filter Dataframe by Any Column Grouping')
st.write('Use the multiselect tool below to filter. Example: Select "Crime" and "Status". '
         'Do you see any patterns between crime committed and the status of their investigation?')
# Creates multiselect dropdowns for selecting columns
selected_columns = st.multiselect('Select columns to display', crime.columns)
# Filters the DataFrame based on selected columns
filtered_data = crime[selected_columns]

# Displays the filtered DataFrame
st.write(filtered_data)

# New Section
st.markdown("\n---")

# Group by year to see trends over time
yearly_trends = crime.groupby(crime['date_reported']).size().reset_index(name='total_crimes')
st.write(yearly_trends)

# Filter records by neighborhood
st.subheader('Filter Crimes by Neighborhood')
st.write('Use the search tool below to filter crimes by neighborhood.')
neighborhood = st.text_input('Enter a neighborhood:', '')
filtered_data = crime[crime['crime_area'].str.contains(neighborhood, case=False)]
st.write(filtered_data)

# Plot top 10 neighborhoods with reported crimes
crime_counts = crime['crime_area'].value_counts()
top_10 = plt.figure(figsize=(8, 6))
sns.barplot(x=crime_counts.head(10).values, y=crime_counts.head(10).index)
plt.xlabel('Number of Crimes Committed')
plt.ylabel('Los Angeles Neighborhood')
plt.title('Top 10 Neighborhoods with Crimes Reported in LA')
st.pyplot(top_10)

# Show histogram of days between crimes and reporting
reported_crime = crime[crime['days_between_report'] < 8]
fig = px.histogram(reported_crime, x='days_between_report', title='Histogram of Days Between Crimes and Reporting of Crimes',
                   labels={'days_between_report': 'Days Between Crimes and Reporting of Crimes'}, histfunc='count', nbins=5)
st.write(fig)
