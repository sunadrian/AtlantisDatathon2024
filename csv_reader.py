import pandas as pd
from pathlib import Path
from collections import namedtuple

def load_dataset(path) -> pd.DataFrame:
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

def abs_difference(a, b):
    return abs(a - b)

def difference(a, b):
    return a - b

Property_Info = namedtuple('Property_Info', ['address', 'rooms', 'fireplace', 'security', 'sprinklers'])
def fiveclosest(dataframe, budget, zipcode, budgetcheckbox = False):
    # storage = {}
    differences = []
    associated_info = []
    cur_df = dataframe[dataframe['ZipCode'] == zipcode]

    if budgetcheckbox:
        diff_func = abs_difference
    else:
        cur_df = cur_df[cur_df['TotalAssessedValue'] <= budget]
        diff_func = difference
        print(cur_df)

    for i, row in cur_df.iterrows():
        cost = row.iloc[15]
        new_info = Property_Info(row['PropertyAddress'], row['TotalNumberOfRooms'], row['HasFireplace'],
                                            row['HasSecurityAlarm'], row['HasSprinklers'])
        if len(differences) < 5:
            differences.append(diff_func(budget, cost))
            associated_info.append(new_info)
        else:
            if diff_func(budget, cost) < diff_func(budget, max(differences)):
                removed_index = differences.index(max(differences))
                differences.pop(removed_index)
                differences.append(diff_func(budget, cost))
                associated_info.pop(removed_index)
                associated_info.append(new_info)
    return associated_info

if __name__ == "__main__":
    df = load_dataset(Path("PropertyAssessmentData.csv"))
    zipcode_stats = calc_zipcode_stats(df)

    res = fiveclosest(df, 280000, 92706, True)
    for r in res:
        print(r)
