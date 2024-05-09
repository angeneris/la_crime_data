import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load crime data
crime = pd.read_csv('crime_data_2020_to_present.csv', parse_dates=['date_reported', 'crime_date'], index_col=False)

# Sample the data to reduce size
crime = crime.sample(n=50000, random_state=42)

# Data preprocessing
crime['year'] = crime['date_reported'].dt.strftime('%Y')

# Displays header and an introduction 
st.header('Crimes in Los Angeles between 2020 - Present')
st.write('Visual Report by Angeneris Cifuentes')

# New Section
st.markdown("---")

# Summary for the dataframe
st.write('This data belongs to the public and is taken from the public LAPD database detailing crimes that have been reported between the years 2020-2024 in Los Angeles County')

# Displays the dataframe, including a message with the most up-to-date crime reported
st.write('The latest reported crime in this dataset occurred on:', crime['date_reported'].max())
st.write(crime)

# New Section
st.markdown("\n---")
st.subheader('Overall Crime Trends')
# Group by crime type and count occurrences, select top 10 crime types
top_crime_types = crime['crime'].value_counts().head(10).index.tolist()

# Filter data for top 10 crime types
filtered_top_crimes = crime[crime['crime'].isin(top_crime_types)]

# Creates a scatter plot
scatter = px.scatter(filtered_top_crimes, x='date_reported', y='crime', 
                          title='Crime Scatter Plot: Crime and Report Date', 
                          labels={'date_reported': 'Date Reported', 'crime': 'Crime Type'})

# Display the scatter plot
st.plotly_chart(scatter)

# Filtering data by any columns 
st.subheader('Filter Dataframe by Any Column Grouping')
st.write('Use the multiselect tool below to filter. \nExample: Select "Crime" and "Status". '
         'Do you see any patterns between crime committed and the status of their investigation?')
# Creates multiselect dropdowns for selecting columns
selected_columns = st.multiselect('Select columns to display', crime.columns)
# Filters the DataFrame based on selected columns
filtered_data = crime[selected_columns]

# Displays the filtered DataFrame
st.write(filtered_data)

# New Section
st.markdown("\n---")
st.subheader('Yearly Crime Trends')

# Create a slider for selecting years
start_year = 2020
end_year = 2024
selected_years = st.slider('Select a range of years (2020-2024):', start_year, end_year, (start_year, end_year))

# Filter data based on selected years
filtered_crime = crime[(crime['year'] >= str(selected_years[0])) & (crime['year'] <= str(selected_years[1]))]

# Group data by year and neighborhood
yearly_neighborhood_crimes = filtered_crime.groupby(['year', 'crime_area']).size().reset_index(name='total_crimes')

# Plot the data using Plotly Express
st.subheader('Yearly Crime Trends by Neighborhood')
fig = px.line(yearly_neighborhood_crimes, x='year', y='total_crimes', color='crime_area',
              labels={'year': 'Year', 'total_crimes': 'Total Crimes', 'crime_area': 'Neighborhood'},
              title='Total Crimes per Year by Neighborhood')
st.plotly_chart(fig)

# Display the DataFrame
st.write(yearly_neighborhood_crimes)

# New Section
st.markdown("\n---")
st.subheader('Top 10 Neighborhoods with Reported Crimes')
st.write('Below you can view a bar chart with the Top 10 Neighborhoods with reported crimes between the years 2020-2024')

# Plots top 10 neighborhoods with reported crimes
crime_counts = crime['crime_area'].value_counts().head(10)
fig = px.bar(crime_counts, x=crime_counts.values, y=crime_counts.index, orientation='h',
             labels={'y': 'Los Angeles Neighborhood', 'x': 'Number of Crimes Committed'},
             title='Top 10 Neighborhoods with Crimes Reported in LA')
st.plotly_chart(fig)

# New Section
st.markdown("\n---")
st.subheader('Histogram of Days Between Crimes and Reporting of Crimes')
st.write('Shows the distribution of the number of days between when crimes occur and when they are reported.')

# Show histogram of days between crimes and reporting
reported_crime = crime[crime['days_between_report'] < 8]
fig = px.histogram(reported_crime, x='days_between_report', title='Histogram of Days Between Crimes and Reporting of Crimes',
                   labels={'days_between_report': 'Days Between Crimes and Reporting of Crimes'}, histfunc='count', nbins=5)
st.write(fig)