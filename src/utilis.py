import matplotlib.pyplot as plt
import pandas as pd

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


