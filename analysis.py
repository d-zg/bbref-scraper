import pandas as pd
import numpy as np

df = pd.read_csv('nba_playoff_results.csv')


# Group the dataframe by 'Record' column and count the total number of rows for each group
total_rows = df.groupby('Record').size()

# Filter the dataframe to include only rows where 'Winner' is equal to 'This Team'
filtered_df = df[df['Winner'] == df['This Team']]

# Group the filtered dataframe by 'Record' column and count the number of rows for each group
matching_rows = filtered_df.groupby('Record').size()

# Combine the total rows and matching rows into a single dataframe
result = pd.DataFrame({'Total Rows': total_rows, 'Matching Rows': matching_rows})

print(result)

rows_with_01 = df[df['Record'] == '1-0']
print(rows_with_01)