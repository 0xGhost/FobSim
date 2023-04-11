import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy
import matplotlib
# matplotlib.use('TkAgg')

filename = 'failrate_input.csv'
failrate_limit1 = 0.00
failrate_limit2 = 0.05
failrate_limit3 = 0.10

#handle console arguments
if len(sys.argv) >= 2:
    filename = sys.argv[1]

if len(sys.argv) >= 5:
    failrate_limit1 = sys.argv[2]
    failrate_limit2 = sys.argv[3]
    failrate_limit3 = sys.argv[4]
    


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
print("Excel result file generated")

################################################################################### show result curves
# Get unique values of 'tx per block'
tx_values = df_rate['tx per block'].unique()

fig = plt.figure()
fig.set_figwidth(200)


# Loop over tx_values and plot a curve for each one
for i, tx in enumerate(tx_values):
    # Select data for this tx value
    data = df_rate[df_rate['tx per block'] == tx]

    # Plot curve with injection rate on y-axis and fail rate on x-axis
    plt.plot(data['injection rate(per sec)'], data['fail_rate'], label=f'Tx per Block={tx}', linestyle='solid')

# Add title and labels to plot
plt.title('Injection Rate vs. Fail Rate')
plt.ylabel('Fail Rate')
plt.xlabel('Injection Rate')

plt.xticks(numpy.arange(150,2100,10))
plt.yticks(numpy.arange(0,0.5,0.05))
plt.grid(axis='y')

# Add legend to plot
plt.legend()

# Save plot to file
plt.subplots_adjust(left = 0.01, right = 0.99)
plt.savefig("failrate_plot.png")
print("Plot file generated")

# Function to find the maximum injection rate for a given fail rate condition
def find_max_injection_rate(df, fail_rate_condition):
    df_filtered = df[df['fail_rate'] <= fail_rate_condition]
    df_not_filtered = df[df['fail_rate'] > fail_rate_condition]
    df_max_injection = pd.DataFrame()

    for tx in df['tx per block'].unique():
        filtered_values = df_filtered[df_filtered['tx per block'] == tx]['injection rate(per sec)']
        not_filtered_values = df_not_filtered[df_not_filtered['tx per block'] == tx]['injection rate(per sec)']

        if not_filtered_values.empty:
            max_injection_rate = filtered_values.max()
        else:
            min_not_filtered_value = not_filtered_values.min()
            max_injection_rate = filtered_values[filtered_values < min_not_filtered_value].max()

        df_max_injection = df_max_injection.append({
            'tx per block': tx,
            f'max_injection_rate_{int(fail_rate_condition * 100)}': max_injection_rate
        }, ignore_index=True)

    return df_max_injection

# Find the maximum injection rate for fail rate conditions <= 5% and <= 10%
df_max_injection_1 = find_max_injection_rate(df_rate, failrate_limit1)
df_max_injection_2 = find_max_injection_rate(df_rate, failrate_limit2)
df_max_injection_3 = find_max_injection_rate(df_rate, failrate_limit3)

# Merge the results into a single DataFrame
df_max_injection_merged_0_5 = pd.merge(df_max_injection_1, df_max_injection_2, on='tx per block', how='outer')
df_max_injection_merged = pd.merge(df_max_injection_merged_0_5, df_max_injection_3, on='tx per block', how='outer')


# Write the result to an Excel file
df_max_injection_merged.to_excel('max_injection_rate.xlsx', index=False)
print("Excel max injection rate result file for multiple conditions generated")