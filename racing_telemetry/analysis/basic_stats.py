import pandas as pd
from typing import Optional

def average_speed(df: pd.DataFrame, speed_column: str = 'SpeedMs') -> Optional[float]:
    """
    Calculate the average speed from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the telemetry data.
        speed_column (str): The name of the column containing speed data. Defaults to 'Speed'.

    Returns:
        Optional[float]: The average speed, or None if the speed column is not found or contains no valid data.
    """
    if speed_column not in df.columns:
        print(f"Warning: '{speed_column}' column not found in the DataFrame.")
        return None

    average = df[speed_column].mean()
    if pd.isna(average):
        print(f"Warning: No valid data found in the '{speed_column}' column.")
        return None

    return average
