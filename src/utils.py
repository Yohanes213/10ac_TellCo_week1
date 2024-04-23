import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer  # Import from scikit-learn


def top_n(df, column, n):
    top_n_column = df[column].value_counts().head(n)
    
    plt.figure(figsize=(10,6))
    top_n_column.plot(kind="bar")
    plt.title(f"Top {n} {column} (Distrubtion)")
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def visualize_top_handsets(top_5_handset_per_manufacturer, choosen_manufacturer):
    
    choosen_top_5_handsets = top_5_handset_per_manufacturer.get(choosen_manufacturer, pd.Series())
    plt.figure(figsize=(10,6))

    plt.bar(choosen_top_5_handsets.index, choosen_top_5_handsets.values, color='skyblue')

    plt.xlabel("Handset")
    plt.ylabel("Count")
    plt.title(f"Top 5 Handsets for {choosen_manufacturer} Manufacturer")
    plt.xticks(rotation=45, ha='right')


class Preprocess:

    def __init__(self, df):
        self.df = df.copy()


    def drop_columns_with_null(self, threshold = 0.3):
        null_info = self.df.isnull().sum() / len(self.df)

        drop_columns = null_info[null_info > threshold].index

        self.df.drop(columns = drop_columns, inplace = True)

        return self.df
    
    def convert_to_datetime(self, column):

        self.df[column] = self.df[column].apply(pd.to_datetime)

    
    def convert_to_float_to_int_if_possible(self):

        for column in self.df.select_dtypes(include='float'):
            if all(elements % 1 == 0 for elements in self.df[column]):
                self.df[column] = self.df[column].astype(int)
        
        return self.df
    
    def remove_outliers(self, column, num_std=3):
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            print("Warning: Column '{column}' is not numerical. Outlier removal cannot be done")
        
        mean = self.df[column].mean()
        std = self.df[column].std()

        lower_bound = mean - num_std * std
        upper_bound = mean + num_std * std
    
        self.df =  self.df[self.df[column].between(lower_bound, upper_bound)]

        return self.df
        #return filtered_df
    


    def impute_nulls(self, strategy="mean"):
        """
        Imputes null values in all columns of the DataFrame using a specified strategy.

        Args:
            strategy (str, optional): The imputation strategy to use. Defaults to "mean".
                Can be "mean", "median", "mode", or "constant".

        Returns:
            pd.DataFrame: A new DataFrame with imputed null values.
        """

        # Validate strategy (consider adding 'most_frequent' for categorical data)
        if strategy not in ["mean", "median", "mode", "constant"]:
            raise ValueError(f"Invalid strategy: {strategy}. Valid options are 'mean', 'median', 'mode', or 'constant'.")


        if self.df.dtypes.eq('object').any():  # Check for any categorical columns
            categorical_cols = self.df.select_dtypes(include='object').columns
            imputer = SimpleImputer(strategy='most_frequent')  # Use 'most_frequent' for categorical
            self.df[categorical_cols] = imputer.fit_transform(self.df[categorical_cols])

        numerical_cols = self.df.select_dtypes(include='number').columns  # Get numerical columns
        imputer = SimpleImputer(strategy=strategy)
        self.df[numerical_cols] = imputer.fit_transform(self.df[numerical_cols])

        return self.df
def visualize_distributions(df, column):

    try:
        plt.figure(figsize=(10,6))
        df[column] = pd.to_numeric(df[column])
        df[column].hist(bins=10, edgecolor='black')
        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
    except:
        print(f"Warning: Column '{column}' ud not numerical. Histogram cannot be created")

    plt.show()

def plt_boxplot(df, column):
    try:
        plt.figure(figsize=(10,6))
        df[column] = pd.to_numeric(df[column])
        plt.boxplot(df[column])
        plt.title(f"Boxplot of {column}")
        plt.xlabel(column)
        plt.ylabel("Value")
        plt.grid(True)
    except:
        print(f"Warning: Column '{column}' is not numerical. Boxplot cannot be created")

    plt.show()
