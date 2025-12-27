import pandas as pd
import numpy as np

def load_and_process_data(file_path):
    """
    Load the fertilizer dataset, clean it, and aggregate by country and year.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        tuple: (country_df, global_df)
            country_df: DataFrame with columns ['Country', 'Year', 'Total_Fertilizer_Usage']
            global_df: DataFrame with columns ['Year', 'Total_Fertilizer_Usage']
    """
    # Load the data
    df = pd.read_csv(file_path)

    # Convert Year to int, handling formats like '1991/92'
    df['Year'] = df['Year'].astype(str).str[:4].astype(int)

    # Replace 'NA' with NaN
    df.replace('NA', np.nan, inplace=True)

    # Convert numeric columns to float
    numeric_cols = ['N_k_t', 'P2O5_k_t', 'K2O_k_t', 'N_P2O5_K2O_k_t']
    df[numeric_cols] = df[numeric_cols].astype(float)

    # Create total fertilizer usage: if N_P2O5_K2O_k_t is available, use it, else sum the components
    df['Total_Fertilizer_Usage'] = df['N_P2O5_K2O_k_t'].fillna(
        df['N_k_t'].fillna(0) + df['P2O5_k_t'].fillna(0) + df['K2O_k_t'].fillna(0)
    )

    # Aggregate by Country and Year
    country_df = df.groupby(['Country', 'Year'])['Total_Fertilizer_Usage'].sum().reset_index()

    # Sort by Country and Year
    country_df = country_df.sort_values(['Country', 'Year'])

    # Aggregate for global
    global_df = df.groupby('Year')['Total_Fertilizer_Usage'].sum().reset_index()

    # Sort by Year
    global_df = global_df.sort_values('Year')

    return country_df, global_df