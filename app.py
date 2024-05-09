import pandas as pd # type: ignore
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

# Displays the data
st.header('Crimes in Los Angeles between 2020 - Present', divider='red')
st.write('Visual Report by Angeneris Cifuentes')

# Creates a break with space
st.markdown("\n---")


# Section 1 of SDA
st.header('Crime Reports in Los Angeles from 2020 - 2024')
# Here you would write a summary of what the chart is 



# Creates a multiselection box for filtering the dataframe
# Creates multiselect dropdowns for selecting columns
selected_columns = st.multiselect('Select columns to display', crime.columns)

# Filters the DataFrame based on selected columns
filtered_data = crime[selected_columns]

# Displays the filtered DataFrame
st.write(filtered_data)

# Show the latest reported crime date
max_crime = crime['date_reported'].max()
st.write(f'The latest reported crime in this dataset occurred on: {max_crime}')
st.markdown("\n---")

# Group by year to see trends over time
yearly_trends = crime.groupby(crime['date_reported']).size().reset_index(name='total_crimes')
st.write(yearly_trends)

# Filter records by neighborhood
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
