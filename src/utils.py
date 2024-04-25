import numpy as np
import pandas as pd
from sklearn.metrics import euclidean_distances
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('utils.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Utils:
    def __init__(self):
        self.logger = self.logger()

    def calculate_score(self, metrics, cluster_labels):
        """
        Calculate the score for each user based on their metrics and cluster labels.

        Parameters:
        - metrics: DataFrame, contains user metrics (rows) and corresponding columns
        - cluster_labels: array-like, cluster labels assigned to each user

        Returns:
        - scores: array, engagement or experience scores for each user
        """
        try:
            # Identify the least engaged cluster
            less_engaged_cluster = np.argmin(np.sum(metrics[cluster_labels == less_engaged_cluster], axis=0))

            # Get the data points of users belonging to the least engaged cluster
            less_engaged_data_points = metrics[cluster_labels == less_engaged_cluster]

            # Compute the score for each user
            scores = []
            for index, row in metrics.iterrows():
                # Get the cluster label for the user
                user_cluster = row['Cluster']
                # Check if the user belongs to the least engaged cluster
                if user_cluster == less_engaged_cluster:
                    # If user belongs to the least engaged cluster, distance is 0
                    distance = 0
                else:
                    # Get the data point of the user
                    data_point = row.drop('Cluster').values.reshape(1, -1)  # Remove 'Cluster' column and reshape as a row
                    # Calculate Euclidean distance between user's data point and data points of users in least engaged cluster
                    distances = euclidean_distances(data_point, less_engaged_data_points)
                    distance = np.min(distances)
                scores.append(distance)
            return scores
        except Exception as e:
            self.logger.error(f"An error occurred while calculating scores: {str(e)}")
