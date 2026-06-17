"""
Jude Merritt
CSE 163, Section AI

This module defines the Visualizer class, which extends the
DataProcessor class to create a visual representation of
the watersports vehicle tracking data. The Visualizer class
loads the data, processes it to predict missing coordinates
and remove outliers, and then generates two interactive scatter
plots using Plotly Express. One plot displays the trajectory
of the vehicle over time, with hover information showing timestamps
and speeds at each point, while the other displays the speed of the
vehicle over time. The second plot is accessable via a tab at the top
of of the UI. The resulting visualization is saved as an HTML file.

This class encompasses my updated THA 2, THA 4, and THA 5 creative components.
"""

from DataProcessor import DataProcessor
import plotly.express as px
import os


class Visualizer(DataProcessor):
    """
    A class used to visualize watersports vehicle tracking data.

    Extends DataProcessor to handle data cleaning and then generates two
    interactive plots: one showing the path, timestamps, and speeds, and
    the other showing the speed of the vehicle over time.
    """

    def __init__(self, file_path: str):
        """
        Initializes the Visualizer, loads and processes data from a csv file
        by interpolating missing coordinates and removing speed outliers, and
        calculates the final speed values at each position point.

        Args:
            file_path (str): The path to the csv file containing tracking data.
        """
        super().__init__()
        self.load_data(file_path)
        self.predict_missing_coords()
        self.remove_outliers()
        self.data["speed"] = self.calculate_speeds()

    def create_visualization(self, file_name="historical_analysis.html"):
        """
        Generates an interactive scatter plot of the vehicle trajectory,
        and of vehicle speed over time. The plots are accessable via tabs
        in the final HTML output.
        """
        max_val = max(
            self.data["x_coord"].abs().max(),
            self.data["y_coord"].abs().max()
        )

        # Default trace: Rout map (THA 2)
        fig = px.scatter(
            self.data,
            x="x_coord",
            y="y_coord",
            title="Watersports Vehicle Tracker (Server Processed)",
            hover_data=["timestamp", "speed"]
        )
        fig.update_traces(mode="markers+lines", name="Route")

        # Hidden trace: Speed over time (THA 4)
        fig.add_scatter(
            x=self.data["timestamp"],
            y=self.data["speed"],
            mode="lines+markers",
            name="Speed",
            visible=False,
            hovertemplate="Time: %{x}<br>Speed: %{y:.2f} m/s"
        )

        # Tabs logic
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    x=0.5,
                    y=1,
                    xanchor="center",
                    yanchor="bottom",
                    showactive=True,
                    buttons=list([
                        dict(
                            label="Route Map",
                            method="update",
                            args=[
                                {"visible": [True, False]},
                                {
                                    "xaxis.title.text": "West/East (m)",
                                    "yaxis.title.text": "South/North (m)",
                                    "xaxis.type": "linear",
                                    "yaxis.type": "linear",
                                    "xaxis.range": [-max_val * 1.2, max_val * 1.2],
                                    "yaxis.range": [-max_val * 1.2, max_val * 1.2],
                                }
                            ],
                        ),
                        # Speed tab logic (THA 4)
                        dict(
                            label="Speed over Time",
                            method="update",
                            args=[
                                {"visible": [False, True]},
                                {
                                    "xaxis.title.text": "Timestamp",
                                    "yaxis.title.text": "Speed (m/s)",
                                    "xaxis.type": "date",
                                    "yaxis.type": "linear",
                                }
                            ],
                        ),
                    ]),
                ),
                # Font size toggle for accessibility (THA 5)
                dict(
                    type="buttons",
                    direction="right",
                    x=0,
                    y=1.3,
                    xanchor="left",
                    buttons=list([
                        dict(
                            label="Normal Text",
                            method="relayout",
                            args=[{"font.size": 12}],
                        ),
                        dict(
                            label="Large Text",
                            method="relayout",
                            args=[{"font.size": 18}],
                        ),
                    ]),
                )
            ]
        )

        # Default styling for route map
        fig.update_xaxes(
            title="West/East (m)",
            range=[-max_val * 1.2, max_val * 1.2],
            zeroline=True,
            zerolinecolor='black',
            gridcolor='lightgrey'
        )
        fig.update_yaxes(
            title="South/North (m)",
            range=[-max_val * 1.2, max_val * 1.2],
            zeroline=True,
            zerolinecolor='black',
            gridcolor='lightgrey',
        )

        fig.write_html(file_name)
        print(f"File successfully saved as {file_name}")
