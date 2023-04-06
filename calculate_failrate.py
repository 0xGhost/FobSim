import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy
import matplotlib
matplotlib.use('TkAgg')

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
