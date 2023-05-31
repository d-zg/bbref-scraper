import pandas as pd
import numpy as np
import math
import scipy.stats


# get the win percentage for each record
def get_win_percentage_dict():
    df = pd.read_csv('nba_playoff_results.csv')

    # Group the dataframe by 'Record' column and count the total number of rows for each group
    total_rows = df.groupby('Record').size()

    # Filter the dataframe to include only rows where 'Winner' is equal to 'This Team'
    filtered_df = df[df['Winner'] == df['This Team']]

    # Group the filtered dataframe by 'Record' column and count the number of rows for each group
    matching_rows = filtered_df.groupby('Record').size()

    # Combine the total rows and matching rows into a single dataframe
    result = pd.DataFrame({'Total Rows': total_rows, 'Matching Rows': matching_rows})

    # Calculate the ratio of matching rows to total rows
    result['Matching Ratio'] = result['Matching Rows'] / result['Total Rows']

    # Convert the dataframe into a dictionary
    result_dict = result['Matching Ratio'].to_dict()

    # def remove_values(dictionary):
    #     return {key: value for key, value in dictionary.items() if value != 1 and not math.isnan(value)}

    # result_dict = remove_values(result_dict)
    return result_dict

# for each record, group by Win Order and get the win percentage and number of games for each Win Order   
# Group by Win Order and calculate the counts
def observed_winrate_by_order():
    df = pd.read_csv('nba_playoff_results.csv')
    grouped = df.groupby('Win Order').agg(
        Record=('Record', 'first'),  # Get the first value of 'Record' for each group
        Same_Winner_Count=('Winner', lambda x: (x.eq(df['This Team'])).sum()),  # Count rows where 'Winner' == 'This Team'
        Total_Count=('Winner', 'count')  # Count total rows in each group
    ).reset_index()

    # Calculate win rate
    grouped['Winrate'] = grouped['Same_Winner_Count'] / grouped['Total_Count']

    # Reset index
    grouped = grouped.reset_index()

    # return the resulting DataFrame
    return grouped

# for each order, get the p value of the observed win percentage at Total_Count trials 
# from a binomial distribution with the win percentage of the record
def get_p_values():
    # Get the observed win rate by order
    observed_winrate_df = observed_winrate_by_order()

    # Get the win percentage dictionary
    win_percentage_dict = get_win_percentage_dict()

    # Calculate the p-value for each row
    observed_winrate_df['p-value'] = observed_winrate_df.apply(
        lambda row: 1 - scipy.stats.binom.cdf(row['Same_Winner_Count'], row['Total_Count'], win_percentage_dict[row['Record']]),
        axis=1)

    # Return the resulting dataframe
    return observed_winrate_df

pd.set_option('display.max_rows', None)
results = get_p_values()
# print(results)

# save results to csv
results.to_csv('p_values.csv', index=False)

mask = results['Record'].str.contains('4')

# Invert the mask to select rows that do not contain '4'
filtered_df = results[~mask]

filtered_df.reset_index(drop=True, inplace=True)
# Sort the dataframe by the length of the "Win Order" column
sorted_df = filtered_df.iloc[filtered_df['Win Order'].str.len().sort_values().index]

# save the sorted, filtered dataframe to csv
sorted_df.to_csv('cleaned_p_values.csv', index=False)