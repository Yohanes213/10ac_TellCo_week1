import numpy as np
import pandas as pd
from sklearn.metrics import euclidean_distances
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('utils.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Utils:
    def __init__(self):
        self.logger = logger

    def calculate_score(self, metrics: pd.DataFrame, less_cluster: int) -> list:
        """
        Calculate the score for each user based on their metrics and cluster labels.

        Parameters:
        - metrics: DataFrame, contains user metrics (rows) and corresponding columns
        - less_cluster: int, least engaged cluster label

        Returns:
        - scores: list, engagement or experience scores for each user
        """
        try:
            # Get the data points of users belonging to the least engaged cluster
            less_engaged_data_points = metrics[metrics['cluster'] == less_cluster]

            # Compute the score for each user
            scores = []
            for index, row in metrics.iterrows():
                # Get the cluster label for the user
                user_cluster = row['cluster']
                # Check if the user belongs to the least engaged cluster
                if user_cluster == less_cluster:
                    # If user belongs to the least engaged cluster, distance is 0
                    distance = 0
                else:
                    # Get the data point of the user
                    data_point = row.drop('cluster').values.reshape(1, -1)  # Remove 'Cluster' column and reshape as a row
                    # Calculate Euclidean distance between user's data point and data points of users in least engaged cluster
                    distances = euclidean_distances(data_point, less_engaged_data_points.drop(columns=['cluster']))
                    distance = np.min(distances)
                scores.append(distance)
            return scores
        except Exception as e:
            self.logger.error(f"An error occurred while calculating scores: {str(e)}")
