import pandas as pd
from pathlib import Path

def filereader(path) -> pd.DataFrame:
    return pd.read_csv(path)


def calc_zipcode_stats(df: pd.DataFrame) -> dict:
    """
    Calculates the min, max, average property cost
    for each zipcode in the pandas dataframe.
    """
    grouped_df = df.groupby('ZipCode')
    zipcode_stats = {}

    for zipcode, group in grouped_df:
        max_value = group['TotalAssessedValue'].max()
        min_value = group['TotalAssessedValue'].min()
        avg_value = group['TotalAssessedValue'].mean()
        avg_latitude = group['Latitude'].mean()
        avg_longitude = group['Longitude'].mean()
        zipcode_stats[zipcode] = [max_value, min_value, avg_value, avg_latitude, avg_longitude]
    return zipcode_stats




if __name__ == "__main__":
    df = filereader(Path("PropertyAssessmentData.csv"))
    zipcode_stats = calc_zipcode_stats(df)