import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


crime = pd.read_csv('/Users/angeneris/la_crime_data/la_crime_data-1/crime_data_2020_to_present.csv', parse_dates=['date_reported', 'crime_date'])


# Display header and basic statistics
st.header('Crimes in Los Angeles between 2020 - Present', divider='blue')
st.write('Visual Report by Angeneris Cifuentes')
st.write(crime)

# Show the latest reported crime date
max_crime = crime['date_reported'].max()
st.write(f'The latest crime reported occurred on: {max_crime}')

# Group by year to see trends over time
yearly_trends = crime.groupby('year').size().reset_index(name='total_crimes')
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
