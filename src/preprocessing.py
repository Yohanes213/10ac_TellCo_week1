import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class PreprocessingUtils:
    """
    A collection of utility functions for data preprocessing.
    """

    def __init__(self):
        self.logger = logger

    def drop_columns_with_null(self, df, threshold=0.3):
        """
        Drop columns with a high percentage of missing values.

        Parameters:
            df (pandas DataFrame): Input DataFrame.
            threshold (float, optional): Threshold for dropping columns based on missing value percentage.
                Defaults to 0.3.

        Returns:
            pandas DataFrame: DataFrame with columns dropped.
        """
        null_info = df.isnull().sum() / len(df)
        drop_columns = null_info[null_info > threshold].index
        self.logger.info(f"Dropped columns with high null values: {drop_columns}")
        return df.drop(columns=drop_columns)

    def convert_to_datetime(self, df, columns):
        """
        Convert a column to datetime format.

        Parameters:
            df (pandas DataFrame): Input DataFrame.
            column (str): Name of the column to convert.

        Returns:
            pandas DataFrame: DataFrame with column converted to datetime.
        """
        for column in columns:
            df[column] = pd.to_datetime(df[column])
            self.logger.info(f"Converted column '{column}' to datetime format")
        return df

    def convert_to_float_to_int_if_possible(self, df):
        """
        Convert float columns to int if possible.

        Parameters:
            df (pandas DataFrame): Input DataFrame.

        Returns:
            pandas DataFrame: DataFrame with float columns converted to int if possible.
        """
        for column in df.select_dtypes(include='float'):
            if df[column].equals(df[column].round()):
                df[column] = df[column].astype(int)
                self.logger.info(f"Converted float column '{column}' to int")
        return df

    def remove_outliers(self, df, column, num_std=3):
        """
        Remove outliers from a column based on the specified number of standard deviations from the mean.

        Parameters:
            df (pandas DataFrame): Input DataFrame.
            column (str): Name of the column to remove outliers from.
            num_std (int, optional): Number of standard deviations from the mean to consider as outlier. Defaults to 3.

        Returns:
            pandas DataFrame: DataFrame with outliers removed.
        """
        mean = df[column].mean()
        std = df[column].std()
        lower_bound = mean - num_std * std
        upper_bound = mean + num_std * std
        filtered_df = df[df[column].between(lower_bound, upper_bound)]
        outliers_count = len(df) - len(filtered_df)
        self.logger.info(f"Removed {outliers_count} outliers from column '{column}'")
        return filtered_df

    def encode_categorical_data(self, df, categorical_columns=None):
        """
        Encode categorical columns using LabelEncoder.

        Parameters:
            df (pandas DataFrame): Input DataFrame.
            categorical_columns (list of str): The names of the categorical columns. If None, all object-type columns will be considered categorical.

        Returns:
            pandas DataFrame: DataFrame with encoded categorical columns.
        """
        if categorical_columns is None:
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        encoder = LabelEncoder()
        encoded_df = df.copy()
        for col in categorical_columns:
            encoded_df[col] = encoder.fit_transform(df[col])
        self.logger.info(f"Encoded categorical columns: {categorical_columns}")
        return encoded_df

    def scale_data(self, df):
        """
        Scale the entire DataFrame using Min-Max scaling.

        Parameters:
            df (pandas DataFrame): Input DataFrame.

        Returns:
            pandas DataFrame: DataFrame with scaled data.
        """
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_data, columns=df.columns)
        self.logger.info("Scaled the data using Min-Max scaling")
        return scaled_df

    def impute_nulls(self, df, strategy="mean"):
        """
        Imputes null values in all columns of the DataFrame using a specified strategy.

        Parameters:
            df (pandas DataFrame): Input DataFrame.
            strategy (str, optional): The imputation strategy to use. Defaults to "mean".
                Can be "mean", "median", "mode", or "constant".

        Returns:
            pandas DataFrame: DataFrame with imputed null values.
        """
        if strategy not in ["mean", "median", "mode", "constant"]:
            raise ValueError(f"Invalid strategy: {strategy}. Valid options are 'mean', 'median', 'mode', or 'constant'.")

        if df.dtypes.eq('object').any():
            categorical_cols = df.select_dtypes(include='object').columns
            imputer = SimpleImputer(strategy='most_frequent')
            df[categorical_cols] = imputer.fit_transform(df[categorical_cols])

        numerical_cols = df.select_dtypes(include='number').columns
        imputer = SimpleImputer(strategy=strategy)
        df[numerical_cols] = imputer.fit_transform(df[numerical_cols])

        self.logger.info(f"Imputed null values using strategy: {strategy}")
        return df

    def remove_outliers_from_dataframe(self, df, column_names):
        """
        Remove outliers from specified columns of a DataFrame using the interquartile range (IQR) method.

        Parameters:
            df (pandas DataFrame): Input DataFrame.
            column_names (list of str): Names of the columns containing the data.

        Returns:
            pandas DataFrame: DataFrame with outliers removed from the specified columns.
        """
        filtered_df = df.copy()
        for column_name in column_names:
            Q1 = df[column_name].quantile(0.25)
            Q3 = df[column_name].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            filtered_df = filtered_df[(filtered_df[column_name] >= lower_bound) & (filtered_df[column_name] <= upper_bound)]
        self.logger.info(f"Removed outliers from columns: {column_names}")
        return filtered_df
