from typing import Optional

import pandas as pd


def average_speed(df: pd.DataFrame, speed_column: str = "SpeedMs") -> Optional[float]:
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


def apex(df: pd.DataFrame, x_column: str = "WorldPosition_x", y_column: str = "WorldPosition_y") -> Optional[dict]:
    """
    Find the apex of a curve in the track.

    Args:
        df (pd.DataFrame): The DataFrame containing the telemetry data.
        x_column (str): The name of the column containing x-coordinate data. Defaults to 'WorldPosition_x'.
        y_column (str): The name of the column containing y-coordinate data. Defaults to 'WorldPosition_y'.

    Returns:
        Optional[dict]: A dictionary containing the index and coordinates of the apex, or None if it can't be found.
    """
    if x_column not in df.columns or y_column not in df.columns:
        print(f"Warning: '{x_column}' or '{y_column}' column not found in the DataFrame.")
        return None

    # remove duplicates
    # df = df.drop_duplicates(subset=[x_column, y_column])

    # Calculate differences
    dx = df[x_column].diff()
    dy = df[y_column].diff()

    # Calculate second differences
    d2x = dx.diff()
    d2y = dy.diff()

    # Calculate curvature
    curvature = (dx * d2y - dy * d2x) / (dx**2 + dy**2) ** (3 / 2)

    # Find the index of the maximum absolute curvature
    apex_index = curvature.abs().idxmax()

    if pd.isna(apex_index):
        print("Warning: Could not determine the apex.")
        return None

    return {"index": apex_index, "x": df.loc[apex_index, x_column], "y": df.loc[apex_index, y_column], "curvature": curvature[apex_index]}
