import pandas as pd
import sys


filename = ' '

#handle console arguments
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = 'failrate_input.csv'

# read the CSV file into a pandas DataFrame
df = pd.read_csv(filename)

# filter the DataFrame to include only the rows where "Fail time(secs)" < 0
df_filtered = df[df['fail time(secs)'] < 0]

# group the filtered DataFrame by "tx per block" and "injection rate(per sec)" and calculate the rate of successful transactions
df_rate = df_filtered.groupby(['tx per block', 'injection rate(per sec)']).size().reset_index(name='success_count')
df_total = df.groupby(['tx per block', 'injection rate(per sec)']).size().reset_index(name='total_count')
df_rate = pd.merge(df_rate, df_total, on=['tx per block', 'injection rate(per sec)'], how='outer')
df_rate.fillna(0, inplace=True)
df_rate['success_rate'] = df_rate['success_count'] / df_rate['total_count']
df_rate['fail_rate'] = 1.0 - df_rate['success_rate']

# write the result to an Excel file
df_rate.to_excel('failrate_result.xlsx', index=False)