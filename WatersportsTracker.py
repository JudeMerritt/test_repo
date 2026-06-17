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
import os


def main(Visualizer):
    file_path = "location_data.csv"
    
    # Check if the file exists before trying to process it
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Generating placeholder HTML.")
        
        # Create a placeholder page so the UI button doesn't lead to a broken link (404 Error)
        placeholder_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Server Analysis</title>
            <style>
                body { background-color: #111; color: white; font-family: sans-serif; text-align: center; padding-top: 20%; }
                a { color: #3498db; text-decoration: none; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>No Server-Side Data Available</h2>
            <p>No static CSV file was found in the repository during the last deployment.</p>
            <p>Please return to the <a href="index.html">Main Tracker</a> and use the "Upload Local CSV" button.</p>
        </body>
        </html>
        """
        with open("historical_analysis.html", "w") as f:
            f.write(placeholder_html)
        return

    # If the file does exist (e.g., if you run this locally), proceed as normal
    visualizer = Visualizer(file_path)
    visualizer.create_visualization()


if __name__ == "__main__":
    main(Visualizer)
