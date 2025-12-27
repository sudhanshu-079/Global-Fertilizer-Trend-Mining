import pandas as pd
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

def forecast_fertilizer_usage(data, periods=5):
    """
    Forecast fertilizer usage for the next 'periods' years using ARIMA.

    Args:
        data (pd.Series): Time series data with Year as index.
        periods (int): Number of years to forecast.

    Returns:
        pd.DataFrame: Historical and forecasted data.
    """
    if len(data) < 5:  # Not enough data for forecasting
        # Return the data as is, no forecast
        forecast_df = data.reset_index()
        forecast_df['Type'] = 'Historical'
        return forecast_df

    # Fit auto ARIMA
    model = auto_arima(data, seasonal=False, trace=False, error_action='ignore', suppress_warnings=True)
    model_fit = model.fit(data)

    # Forecast
    forecast = model_fit.predict(n_periods=periods)

    # Create forecast index
    last_year = data.index[-1]
    forecast_years = range(last_year + 1, last_year + 1 + periods)

    # Combine historical and forecast
    historical_df = data.reset_index()
    historical_df['Type'] = 'Historical'

    forecast_df = pd.DataFrame({
        'Year': forecast_years,
        'Total_Fertilizer_Usage': forecast,
        'Type': 'Forecast'
    })

    combined = pd.concat([historical_df, forecast_df], ignore_index=True)

    return combined