import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('preprocessing.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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
    

    def convert_to_float_to_int_if_possible(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert float columns to int if possible.
        """
        for column in df.select_dtypes(include='float'):
            if df[column].equals(df[column].round()):
                df[column] = df[column].astype(int)
                self.logger.info(f"Converted float column '{column}' to int")
        return df


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
        Imputes null values in a DataFrame using a specified strategy for numerical columns 
        and 'most_frequent' strategy for categorical columns.

        Args:
            df (pd.DataFrame): The DataFrame with missing values.
            strategy (str, optional): The imputation strategy for numerical columns. Defaults to "mean".
                Valid options are 'mean', 'median', 'mode', or 'constant'.

        Returns:
            pd.DataFrame: The DataFrame with imputed values.

        Raises:
            ValueError: If an invalid imputation strategy is provided.
        """

        if strategy not in ["mean", "median", "mode", "constant"]:
            raise ValueError(f"Invalid strategy: {strategy}. Valid options are 'mean', 'median', 'mode', or 'constant'.")

        # Separate categorical and numerical columns
        categorical_cols = df.select_dtypes(include='object').columns
        numerical_cols = df.select_dtypes(include='number').columns

        # Impute categorical columns with 'most_frequent' strategy
        if len(categorical_cols) > 0:
            imputer = SimpleImputer(strategy='most_frequent')
            df[categorical_cols] = imputer.fit_transform(df[categorical_cols])

        # Impute numerical columns with provided strategy
        if len(numerical_cols) > 0:
            imputer = SimpleImputer(strategy=strategy)
            df[numerical_cols] = imputer.fit_transform(df[numerical_cols])

        self.logger.info(f"Imputed null values using strategy: {strategy} for numerical columns and 'most_frequent' for categorical columns")
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


    def preprocess_date_col(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses the 'Start' and 'End' datetime columns in the DataFrame to create new columns 
        representing the duration components (day, hour, minute, and second).

        This function performs the following steps:

        1. Converts 'Start' and 'End' columns to datetime format (if necessary).
        2. Calculates the duration as the difference between 'End' and 'Start' (assuming 'End' is later).
        3. Extracts day, hour, minute, and second components from the calculated duration.
           - Attempts to use the efficient `dt` accessor (available in pandas >= 0.20.0).
           - Falls back to timedelta operations for compatibility with older pandas versions.
        4. Drops the original 'Start', 'End', 'Dur. (ms)', and 'Duration' columns.

        Args:
            df (pd.DataFrame): The DataFrame containing 'Start' and 'End' datetime columns.

        Returns:
            pd.DataFrame: The DataFrame with new columns for duration components ('Dur (day)', 
                          'Dur (hour)', 'Dur (min)', 'Dur (sec)').
        """

        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])

        df['Duration'] = df['End'] - df['Start']  # Calculate duration (assuming 'End' is later than 'Start')

        # Extract duration components using dt accessor (if available) or timedelta operations
        try:
            df['Dur (day)'] = df['Duration'].dt.day
            df['Dur (hour)'] = df['Duration'].dt.hour
            df['Dur (min)'] = df['Duration'].dt.minute
            df['Dur (sec)'] = df['Duration'].dt.seconds
        except AttributeError:
            df['Dur (day)'] = df['Duration'] // pd.Timedelta(days=1)
            df['Dur (hour)'] = (df['Duration'] % pd.Timedelta(days=1)) // pd.Timedelta(hours=1)
            df['Dur (min)'] = (df['Duration'] % pd.Timedelta(hours=1)) // pd.Timedelta(minutes=1)
            df['Dur (sec)'] = df['Duration'] % pd.Timedelta(minutes=1)

        # Drop original and potentially unnecessary columns
        dropped_columns = ['Start', 'End', 'Dur. (ms)', 'Duration']
        df.drop(columns=dropped_columns, inplace=True)
        self.logger.info(f"Dropped columns after preprocessing date columns: {dropped_columns}")

        return df



