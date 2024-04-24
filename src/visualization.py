import matplotlib.pyplot as plt
import pandas as pd
import logging


class VisualizationUtils:
    """
    A collection of utility functions for data visualization.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('visualization.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def plot_bar(self, data, xlabel, ylabel, title, rotation=45):
        """
        Plot a bar chart.

        Parameters:
            data (pandas Series): Data to plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Title of the plot.
            rotation (int, optional): Rotation angle for x-axis labels. Defaults to 45.
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.bar(data.index, data.values, color='skyblue')
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.xticks(rotation=rotation, ha='right')
            plt.show()
            self.logger.info(f"Bar plot created for '{title}'")
        except Exception as e:
            self.logger.error(f"Error occurred while plotting bar chart: {e}")

    def plot_hist(self, df, column, ax=None):
        """
        Plot a histogram.

        Parameters:
            df (pandas DataFrame): DataFrame containing the data.
            column (str): Name of the column for which histogram is plotted.
            ax (matplotlib Axes, optional): The Axes object to plot on. If None, create a new figure and axis.
        """
        try:
            if ax is None:
                fig, ax = plt.subplots()
            df[column] = pd.to_numeric(df[column])
            df[column].hist(bins=10, edgecolor='black', ax=ax)
            ax.set_title(f"Histogram of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Count")
            if ax is None:
                plt.show()
            self.logger.info(f"Histogram plot created for '{column}'")
        except ValueError:
            self.logger.warning(f"Column '{column}' is not numerical. Histogram cannot be created")

    def plot_boxplot(self, df, column, ax=None):
        """
        Plot a boxplot.

        Parameters:
            df (pandas DataFrame): DataFrame containing the data.
            column (str): Name of the column for which boxplot is plotted.
            ax (matplotlib Axes, optional): The Axes object to plot on. If None, create a new figure and axis.
        """
        try:
            if ax is None:
                fig, ax = plt.subplots()
            df[column] = pd.to_numeric(df[column])
            df[column].plot(kind='box', ax=ax, vert=False, patch_artist=True, notch=True, showmeans=True)
            ax.set_title(f"Boxplot of {column}")
            ax.grid(True)
            if ax is None:
                plt.show()
            self.logger.info(f"Boxplot created for '{column}'")
        except ValueError:
            self.logger.warning(f"Column '{column}' is not numerical. Boxplot cannot be created")
