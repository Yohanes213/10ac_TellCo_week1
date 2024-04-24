import matplotlib.pyplot as plt
import pandas as pd
import logging
import seaborn as sns


class VisualizationUtils:
    """A collection of utility functions for data visualization.

    This class configures a logger for visualization-related messages.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler("visualization.log")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def plot_bar(self, data: pd.Series, xlabel: str, ylabel: str, title: str, rotation=45) -> None:
        """
        Plot a bar chart.

        Parameters:
            data (pandas.Series): Data to plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Title of the plot.
            rotation (int, optional): Rotation angle for x-axis labels. Defaults to 45.
        """

        try:
            plt.figure(figsize=(10, 6))
            plt.bar(data.index, data.values, color="skyblue")
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.xticks(rotation=rotation, ha="right")
            plt.show()
            self.logger.info(f"Bar plot created for '{title}'")
        except Exception as e:
            self.logger.error(f"Error occurred while plotting bar chart: {e}")

    def plot_hist(self, df: pd.DataFrame, column: str, ax=None) -> None:
        """
        Plot a histogram.

        Parameters:
            df (pandas.DataFrame): DataFrame containing the data.
            column (str): Name of the column for which histogram is plotted.
            ax (matplotlib.Axes, optional): The Axes object to plot on. If None, create a new figure and axis.
        """

        try:
            if ax is None:
                fig, ax = plt.subplots()
            # Handle non-numeric values (optional)
            df[column] = pd.to_numeric(df[column], errors="coerce")
            df[column].hist(bins=10, edgecolor="black", ax=ax)
            ax.set_title(f"Histogram of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Count")
            if ax is None:
                plt.show()
            self.logger.info(f"Histogram plot created for '{column}'")
        except ValueError:
            self.logger.warning(f"Column '{column}' is not numerical. Histogram cannot be created")

    def plot_boxplot(self, df: pd.DataFrame, column: str, ax=None) -> None:
        """
        Plot a boxplot.

        Parameters:
            df (pandas.DataFrame): DataFrame containing the data.
            column (str): Name of the column for which boxplot is plotted.
            ax (matplotlib.Axes, optional): The Axes object to plot on. If None, create a new figure and axis.
        """

        try:
            if ax is None:
                fig, ax = plt.subplots()
            # Handle non-numeric values (optional)
            df[column] = pd.to_numeric(df[column], errors="coerce")
            df[column].plot(kind="box", ax=ax, vert=False, patch_artist=True, notch=True, showmeans=True)
            ax.set_title(f"Boxplot of {column}")
            ax.grid(True)
            if ax is None:
                plt.show()
            self.logger.info(f"Boxplot created for '{column}'")
        except ValueError:
            self.logger.warning(f"Column '{column}' is not numerical. Boxplot cannot be created")

        
    def plot_heatmap_correlation(self, df: pd.DataFrame, title: str = None, cmap="coolwarm") -> None:
        """
        Plot a heatmap representing the correlation matrix of the DataFrame.

        Parameters:
            df (pandas.DataFrame): DataFrame containing the data for calculating correlations.
            title (str, optional): Title for the heatmap. Defaults to None.
            cmap (str, optional): Colormap to use for visualization. Defaults to "coolwarm".
        """

        try:
            correlation_matrix = df.corr()  # Calculate correlation matrix
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(correlation_matrix, annot=True, ax=ax, cmap=cmap)  # Use seaborn for heatmap

            if title:
                plt.title(title)
            plt.xlabel("Features")
            plt.ylabel("Features")
            plt.show()
            self.logger.info(f"Correlation heatmap generated for '{title if title else 'data'}'")
        except Exception as e:
            self.logger.error(f"Error occurred while plotting correlation heatmap: {e}")
