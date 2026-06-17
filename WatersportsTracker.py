"""
Jude Merritt
CSE 163, Section AI

This module defines the WatersportsTracker class, which serves
as the main integration point for processing and visualizing the
watersports vehicle tracking data. The WatersportsTracker class
integrates the functionality of the DataProcessor and Visualizer
classes to load the data, predict missing coordinates, remove
outliers, calculate speeds, and create an interactive visualization
of the vehicle's trajectory. 

This class integrates my updated THA 1 - 5 creative components.
"""

from Visualizer import Visualizer


def main(Visualizer):
    # Ensure this matches the name of the static CSV you push to your repo
    file_path = "location_data.csv"
    visualizer = Visualizer(file_path)
    visualizer.create_visualization()


if __name__ == "__main__":
    main(Visualizer)
