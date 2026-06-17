"""
Jude Merritt
CSE 163, Section AI

This module defines the DataProcessor class, which serves as a base
class for processing the watersports vehicle tracking data. The
DataProcessor class includes methods for loading the data from a
csv file, predicting missing coordinates using interpolation, removing
incomplete rows, calculating speeds based on coordinate changes and
timestamps, and removing outliers based on speed thresholds. This class
provides the foundational data processing functionality that can be
extended by other classes, such as the Visualizer class, to create
visual representations of the data.

This class encompasses my updated THA 1 and THA 3 creative components.
"""

import pandas as pd


class DataProcessor:
    """
    A class used to process watersports vehicle tracking data.

    This class provides functionality for loading, cleaning, and analyzing
    tracking data, including interpolation of missing coordinates and
    speed-based outlier removal.
    """

    def __init__(self):
        """
        Initializes the DataProcessor with no data loaded.
        """
        self.data = None

    def load_data(self, file_path: str):
        """
        Loads tracking data from a csv file into a pandas DataFrame.

        Args:
            file_path (str): The path to the csv file to be loaded.
        """
        self.data = pd.read_csv(file_path)

    def get_data(self) -> pd.DataFrame:
        """
        Returns the current state of the processed tracking data.

        Returns:
            pd.DataFrame: The internal tracking data.
        """
        return self.data

    def calculate_speeds(self) -> pd.Series:
        """
        Calculates the speed between consecutive tracking points.

        Uses the Pythagorean theorem to determine distance and divides by
        the time difference between timestamps.

        Returns:
            pd.Series: A series representing the calculated speeds.
        """
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        dx = self.data["x_coord"].diff()
        dy = self.data["y_coord"].diff()
        distances = (dx**2 + dy**2)**0.5
        time_diff = self.data['timestamp'].diff().dt.total_seconds()
        speeds = distances / time_diff
        return speeds

    def predict_missing_coords(self) -> pd.DataFrame:
        """
        Fills missing x and y coordinate values using linear interpolation.

        Returns:
            pd.DataFrame: The updated DataFrame with interpolated coordinates.
        """
        self.data[["x_coord", "y_coord"]] = \
            self.data[["x_coord", "y_coord"]].interpolate()
        return self.data

    def remove_incomplete_rows(self) -> pd.DataFrame:
        """
        Removes all rows containing missing (NaN) values from the dataset.

        Returns:
            pd.DataFrame: The DataFrame after dropping incomplete rows.
        """
        self.data = self.data.dropna()
        return self.data

    def remove_outliers(self, max_speed: int = 50) -> pd.DataFrame:
        """
        Filters the dataset to remove rows where the speed exceeds a threshold.

        Calculates speeds between points and retains only rows within the
        acceptable range or rows where speed cannot be calculated
        (e.g., the first row).

        Args:
            max_speed (int, optional): The maximum allowable speed.
            Defaults to 50.

        Returns:
            pd.DataFrame: The filtered DataFrame with outliers removed.
        """
        speeds = self.calculate_speeds()
        self.data = self.data[(speeds <= max_speed) | (speeds.isna())]
        return self.data
