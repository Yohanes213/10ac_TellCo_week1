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

    def drop_columns_with_null(self, df: pd.DataFrame, threshold: float = 0.3) -> pd.DataFrame:
        """
        Drop columns with a high percentage of missing values.
        """
        null_info = df.isnull().sum() / len(df)
        drop_columns = null_info[null_info > threshold].index
        self.logger.info(f"Dropped columns with high null values: {drop_columns}")
        return df.drop(columns=drop_columns)

    def convert_to_datetime(self, df: pd.DataFrame, columns) -> pd.DataFrame:
        """
        Convert a column to datetime format.
        """
        if isinstance(columns, str):
            columns = [columns]
        for column in columns:
            df[column] = pd.to_datetime(df[column])
            self.logger.info(f"Converted column '{column}' to datetime format")
        return df

    def convert_to_float_to_int_if_possible(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert float columns to int if possible.
        """
        for column in df.select_dtypes(include='float'):
            if df[column].equals(df[column].round()):
                df[column] = df[column].astype(int)
                self.logger.info(f"Converted float column '{column}' to int")
        return df

    def remove_outliers(self, df: pd.DataFrame, column: str, num_std: int = 3) -> pd.DataFrame:
        """
        Remove outliers from a column based on the specified number of standard deviations from the mean.
        """
        mean = df[column].mean()
        std = df[column].std()
        lower_bound = mean - num_std * std
        upper_bound = mean + num_std * std
        filtered_df = df[df[column].between(lower_bound, upper_bound)]
        outliers_count = len(df) - len(filtered_df)
        self.logger.info(f"Removed {outliers_count} outliers from column '{column}'")
        return filtered_df

    def encode_categorical_data(self, df: pd.DataFrame, categorical_columns=None) -> pd.DataFrame:
        """
        Encode categorical columns using LabelEncoder.
        """
        if categorical_columns is None:
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        encoder = LabelEncoder()
        encoded_df = df.copy()
        for col in categorical_columns:
            encoded_df[col] = encoder.fit_transform(df[col])
        self.logger.info(f"Encoded categorical columns: {categorical_columns}")
        return encoded_df

    def scale_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scale the entire DataFrame using Min-Max scaling.
        """
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_data, columns=df.columns)
        self.logger.info("Scaled the data using Min-Max scaling")
        return scaled_df

    def impute_nulls(self, df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
        """
        Imputes null values in all columns of the DataFrame using a specified strategy.
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

    def remove_outliers_from_dataframe(self, df: pd.DataFrame, column_names) -> pd.DataFrame:
        """
        Remove outliers from specified columns of a DataFrame using the interquartile range (IQR) method.
        """
        if isinstance(column_names, str):
            column_names = [column_names]

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
