import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_processing import load_and_process_data
from model.forecasting import forecast_fertilizer_usage

# Load data
@st.cache_data
def load_data():
    file_path = 'data/country_fertilizer_trend.csv'
    country_df, global_df = load_and_process_data(file_path)
    return country_df, global_df

country_df, global_df = load_data()

# Sidebar
st.sidebar.title("Fertilizer Usage Dashboard")
countries = sorted(country_df['Country'].unique())
selected_country = st.sidebar.selectbox("Select a Country", countries)
st.sidebar.write(f"Selected Country: {selected_country}")

# Main layout
st.title("Country-wise Fertilizer Usage Trend Analysis and 5-Year Forecasting Dashboard")

# Filter data for selected country
country_data = country_df[country_df['Country'] == selected_country].copy()
country_data = country_data.sort_values('Year')

# 1. Country-wise Fertilizer Usage Trend
st.header("Country-wise Fertilizer Usage Trend")
if not country_data.empty:
    fig_country = go.Figure()
    fig_country.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Total_Fertilizer_Usage'],
                                     mode='lines+markers', name=selected_country))
    fig_country.update_layout(title=f"Fertilizer Usage Trend for {selected_country}",
                              xaxis_title="Year", yaxis_title="Total Fertilizer Usage (k_t)")
    st.plotly_chart(fig_country)
else:
    st.write("No data available for the selected country.")

# 2. Global Fertilizer Usage Trend
st.header("Global Fertilizer Usage Trend")
fig_global = go.Figure()
fig_global.add_trace(go.Scatter(x=global_df['Year'], y=global_df['Total_Fertilizer_Usage'],
                                mode='lines+markers', name="Global"))
fig_global.update_layout(title="Global Fertilizer Usage Trend",
                         xaxis_title="Year", yaxis_title="Total Fertilizer Usage (k_t)")
st.plotly_chart(fig_global)

# 3. Country vs Global Comparison
st.header("Country vs Global Comparison")
fig_comparison = go.Figure()
# Global
fig_comparison.add_trace(go.Scatter(x=global_df['Year'], y=global_df['Total_Fertilizer_Usage'],
                                    mode='lines+markers', name="Global"))
# Country
if not country_data.empty:
    fig_comparison.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Total_Fertilizer_Usage'],
                                        mode='lines+markers', name=selected_country))
fig_comparison.update_layout(title=f"{selected_country} vs Global Fertilizer Usage",
                             xaxis_title="Year", yaxis_title="Total Fertilizer Usage (k_t)")
st.plotly_chart(fig_comparison)

# 4. 5-Year Fertilizer Usage Forecast
st.header("5-Year Fertilizer Usage Forecast")

# Forecast for country
if not country_data.empty and len(country_data) >= 5:
    country_ts = country_data.set_index('Year')['Total_Fertilizer_Usage']
    country_forecast = forecast_fertilizer_usage(country_ts, periods=5)
    st.subheader(f"Forecast for {selected_country}")
    fig_country_forecast = go.Figure()
    # Historical
    hist = country_forecast[country_forecast['Type'] == 'Historical']
    fig_country_forecast.add_trace(go.Scatter(x=hist['Year'], y=hist['Total_Fertilizer_Usage'],
                                              mode='lines', name='Historical', line=dict(color='blue')))
    # Forecast
    fore = country_forecast[country_forecast['Type'] == 'Forecast']
    fig_country_forecast.add_trace(go.Scatter(x=fore['Year'], y=fore['Total_Fertilizer_Usage'],
                                              mode='lines', name='Forecast', line=dict(dash='dash', color='red')))
    fig_country_forecast.update_layout(title=f"5-Year Forecast for {selected_country}",
                                       xaxis_title="Year", yaxis_title="Total Fertilizer Usage (k_t)")
    st.plotly_chart(fig_country_forecast)
else:
    st.write(f"Not enough data for forecasting {selected_country}.")

# Forecast for global
global_ts = global_df.set_index('Year')['Total_Fertilizer_Usage']
global_forecast = forecast_fertilizer_usage(global_ts, periods=5)
st.subheader("Global Forecast")
fig_global_forecast = go.Figure()
# Historical
hist_global = global_forecast[global_forecast['Type'] == 'Historical']
fig_global_forecast.add_trace(go.Scatter(x=hist_global['Year'], y=hist_global['Total_Fertilizer_Usage'],
                                         mode='lines', name='Historical', line=dict(color='blue')))
# Forecast
fore_global = global_forecast[global_forecast['Type'] == 'Forecast']
fig_global_forecast.add_trace(go.Scatter(x=fore_global['Year'], y=fore_global['Total_Fertilizer_Usage'],
                                         mode='lines', name='Forecast', line=dict(dash='dash', color='red')))
fig_global_forecast.update_layout(title="5-Year Global Forecast",
                                  xaxis_title="Year", yaxis_title="Total Fertilizer Usage (k_t)")
st.plotly_chart(fig_global_forecast)