import streamlit as st
import pandas as pd
import plotly.express as px

# Load the monthly and yearly data
@st.cache_resource
def load_data():
    file_path = '/home/florian/DocumentsStrom_3.xlsx'  # Update this path if needed

    # Load monthly data
    monthly_data = pd.read_excel(file_path, skiprows=1, sheet_name=0)
    monthly_data.columns = ['Date', 'Electricity Usage', 'Power to Grid', 'Heating Electricity 1', 'Heating Electricity 2', 'PV Production', 'Water Usage']
    monthly_data['Date'] = pd.to_datetime(monthly_data['Date'])

    # Calculate monthly changes
    monthly_data['Monthly Electricity Usage'] = monthly_data['Electricity Usage'].diff()
    monthly_data['Monthly Power to Grid'] = monthly_data['Power to Grid'].diff()
    monthly_data['Monthly PV Production'] = monthly_data['PV Production'].diff()
    monthly_data['Total Heating Electricity'] = monthly_data['Heating Electricity 1'] + monthly_data['Heating Electricity 2']
    monthly_data['Monthly Heating Usage'] = monthly_data['Total Heating Electricity'].diff()
    monthly_data['Monthly Water Usage'] = monthly_data['Water Usage'].diff()

    # Load and preprocess yearly data
    yearly_data = pd.read_excel(file_path, sheet_name=-1, usecols='A:E,H:L', skiprows=0)
    yearly_data.columns = ['Year', 'Electricity Consumption', 'Heating Electricity', 'Water Consumption', 'PV Generation', 
                           'Year_Costs', 'Electricity Cost', 'Heating Cost', 'Water Cost', 'PV Income']
    # Drop rows with NaN in 'Year' column and convert 'Year' to string
    yearly_data = yearly_data.dropna(subset=['Year'])
    yearly_data['Year'] = yearly_data['Year'].astype(str)

    return monthly_data, yearly_data

monthly_data, yearly_data = load_data()

# Streamlit app layout
st.title('Energy and Water Consumption Dashboard')

# Monthly data visualization
st.subheader('Monthly Data Overview')

# Monthly Electricity and Heating Usage
st.plotly_chart(px.line(monthly_data, x='Date', y=['Monthly Electricity Usage', 'Monthly Heating Usage'],
                        labels={'value': 'Usage (kWh)', 'variable': 'Type'},
                        title='Monthly Electricity and Heating Usage'))

# Monthly Water Usage
st.plotly_chart(px.line(monthly_data, x='Date', y='Monthly Water Usage',
                        labels={'value': 'Usage (m³)'},
                        title='Monthly Water Usage'))

# Monthly PV Production and Power to Grid
st.plotly_chart(px.bar(monthly_data, x='Date', y=['Monthly Power to Grid', 'Monthly PV Production'],
                       barmode='group',
                       labels={'value': 'Power (kWh) / Production (kWh)', 'variable': 'Type'},
                       title='Monthly PV Production and Power to Grid'))

# Yearly data visualization
st.subheader('Yearly Data Overview')

# Function to create a bar chart with custom x-axis
def create_yearly_bar_chart(df, x, y, title):
    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_xaxes(tickvals=df[x].unique())
    return fig

# Electricity and Heating Consumption
st.subheader('Yearly Electricity and Heating Consumption')
st.plotly_chart(create_yearly_bar_chart(yearly_data, 'Year', ['Electricity Consumption', 'Heating Electricity'], 'Yearly Electricity and Heating Consumption (kWh)'))

# Water Consumption
st.subheader('Yearly Water Consumption')
st.plotly_chart(create_yearly_bar_chart(yearly_data, 'Year', 'Water Consumption', 'Yearly Water Consumption (m³)'))

# PV Generation
st.subheader('Yearly PV Generation')
st.plotly_chart(create_yearly_bar_chart(yearly_data, 'Year', 'PV Generation', 'Yearly PV Generation (kWh)'))

# Costs vs Income
st.subheader('Yearly Costs vs. PV Income')
st.plotly_chart(create_yearly_bar_chart(yearly_data, 'Year', ['Electricity Cost', 'Heating Cost', 'Water Cost'], 'Yearly Energy and Water Costs (€)'))
st.plotly_chart(create_yearly_bar_chart(yearly_data, 'Year', 'PV Income', 'Yearly PV Income (€)'))
