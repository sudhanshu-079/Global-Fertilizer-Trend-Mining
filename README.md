# Country-wise Fertilizer Usage Trend Analysis and 5-Year Forecasting Dashboard

This project provides an interactive web application for analyzing and forecasting fertilizer usage trends by country and globally using Streamlit.

## Project Structure

```
fertilizer-trend-project/
│
├── app.py                 # Streamlit app
├── data/
│   └── country_fertilizer_trend.csv
├── model/
│   └── forecasting.py
├── utils/
│   └── data_processing.py
├── requirements.txt
└── README.md
```

## Features

- Select a country from the sidebar
- View historical fertilizer usage trends for the selected country
- View global fertilizer usage trends
- Compare country-level usage with global trends
- Predict fertilizer usage for the next 5 years using ARIMA models

## Installation

1. Clone or download the project.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Locally

1. Navigate to the project directory.
2. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

3. Open the provided URL in your browser.

### On Google Colab

1. Upload the project files to Google Colab.
2. Install dependencies:

   ```python
   !pip install -r requirements.txt
   ```

3. Run the app:

   ```python
   !streamlit run app.py & npx localtunnel --port 8501
   ```

   Follow the localtunnel link to access the app.

## Data

The dataset `country_fertilizer_trend.csv` contains fertilizer consumption data by country, year, and crop. The app aggregates this data to provide country-wise and global totals.

## Forecasting

The forecasting uses ARIMA (AutoRegressive Integrated Moving Average) models fitted to the historical data. For countries with insufficient data (<5 years), no forecast is provided.

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Statsmodels
- Pmdarima