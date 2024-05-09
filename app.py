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

# Top 10 crimes list
top_10_crimes = ['VEHICLE - STOLEN', 'BATTERY - SIMPLE ASSAULT', 'THEFT OF IDENTITY',
       'BURGLARY FROM VEHICLE', 'BURGLARY',
       'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)',
       'ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT',
       'THEFT PLAIN - PETTY ($950 & UNDER)',
       'INTIMATE PARTNER - SIMPLE ASSAULT',
       'THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)']


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
st.write('Below you can view the total amount of crimes reported between in LA County between the years of 2020-2024. ')
# Group data by year and calculate total crimes per year
yearly_total_crimes = crime.groupby('year').size()

# Display a blurb showing the total crimes per year
st.write(f"Total Crimes per Year: {yearly_total_crimes.to_dict()}")


# Group data by reporting date and count number of crimes reported on each date
daily_crime_counts = crime.groupby('date_reported').size().reset_index(name='crime_count')

# Create scatter plot for overall crime trends
fig = px.scatter(daily_crime_counts, 
                 x='date_reported', 
                 y='crime_count', 
                 title='Overall Crime Trends',
                 labels={'date_reported': 'Date Reported', 'crime_count': 'Number of Crimes'},
                 hover_name='date_reported',  # Show date on hover
                 hover_data={'crime_count': True},  # Show crime count on hover
                 )

# Customize the layout (optional)
fig.update_layout(xaxis=dict(title='Date Reported'),
                  yaxis=dict(title='Number of Crimes'),
                  )

# Display the plot
st.plotly_chart(fig)


st.markdown("\n")
st.subheader('Top 10 Neighborhoods with Reported Crimes')
st.write('Below you can view a bar chart with the Top 10 Neighborhoods with reported crimes between the years 2020-2024')

# Plots top 10 neighborhoods with reported crimes
crime_counts = crime['crime_area'].value_counts().head(10).sort_values(ascending=False)  # Sort in descending order
fig = px.bar(crime_counts, x=crime_counts.values, y=crime_counts.index, orientation='h',
             labels={'y': 'Los Angeles Neighborhood', 'x': 'Number of Crimes Committed'},
             title='Top 10 Neighborhoods with Crimes Reported in LA')
st.plotly_chart(fig)

# New Section
st.markdown("\n---")
st.subheader('Yearly Crime Trends')
st.write('Below you can view the yearly trends of crime by neighborhood between years 2020-2024')


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
st.write('Below you can view a line graph with the histroical data of crimes reported by neighborhood. The neighborhood with the most crimes reported are at the top, but you can change the view by hovering down the list of neighborhoods.')
fig = px.line(yearly_neighborhood_crimes, x='year', y='total_crimes', color='crime_area',
              labels={'year': 'Year', 'total_crimes': 'Total Crimes', 'crime_area': 'Neighborhood'},
              title='Total Crimes per Year by Neighborhood')
st.plotly_chart(fig)

# New Section
st.markdown("\n---")
st.subheader('Most Crimes are Reported Right Away')
st.subheader('Histogram of Days Between Crimes and Reporting of Crimes')
st.write('Shows the distribution of the number of days between when crimes occur and when they are reported.')

# Show histogram of days between crimes and reporting
reported_crime = crime[crime['days_between_report'] < 8]
fig = px.histogram(reported_crime, x='days_between_report', title='Histogram of Days Between Crimes and Reporting of Crimes',
                   labels={'days_between_report': 'Days Between Crimes and Reporting of Crimes'}, histfunc='count', nbins=5)
st.write(fig)

st.markdown("\n---")
st.subheader('Try Your Own Analysis')
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
