import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import numpy
import math
import matplotlib
from sklearn.metrics import r2_score
# matplotlib.use('TkAgg')

filename = 'failrate_input.csv'
postfix = ''
failrate_limit1 = 0.00
failrate_limit2 = 0.05
failrate_limit3 = 0.10

log_fit_col = 1

#handle console arguments
if len(sys.argv) >= 2:
    filename = sys.argv[1]

if len(sys.argv) >= 3:
    postfix = sys.argv[2]

# if len(sys.argv) >= 5:
#     failrate_limit1 = sys.argv[2]
#     failrate_limit2 = sys.argv[3]
#     failrate_limit3 = sys.argv[4]

# read the CSV file into a pandas DataFrame
df = pd.read_csv(filename)



# Calculate the weighted average of "average block time(ms)" using "final No. block" as the weight
df['weighted_block_time'] = df['average block time(ms)'] * df['final No. block']
df_weighted_avg_block_time = df.groupby('tx per block').agg(
    {'weighted_block_time': 'sum', 'final No. block': 'sum'}).reset_index()
df_weighted_avg_block_time['avg_block_time'] = df_weighted_avg_block_time['weighted_block_time'] / df_weighted_avg_block_time['final No. block']

# Drop the intermediate columns and keep only the weighted average
df_weighted_avg_block_time = df_weighted_avg_block_time.drop(columns=['weighted_block_time', 'final No. block'])

# Write the result to an Excel file
df_weighted_avg_block_time.to_excel('avg_block_time'+postfix+'.xlsx', index=False)
print("Excel weighted average block time result file (tx per block only) generated")





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
df_rate.to_excel('failrate_result'+postfix+'.xlsx', index=False)
print("Excel result file generated")

################################################################################### show result curves
# Get unique values of 'tx per block'
tx_values = df_rate['tx per block'].unique()

fig = plt.figure()
fig.set_figwidth(60)
fig.set_figheight(10)


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

plt.xticks(numpy.arange(40,350,10))
plt.yticks(numpy.arange(0,1,0.05))
plt.grid(axis='y')

# Add legend to plot
plt.legend()

# Save plot to file
plt.subplots_adjust(left = 0.01, right = 0.99)
plt.savefig('failrate_plot'+postfix+'.png')
print("failrate plot file generated")

# Function to find the maximum injection rate for a given fail rate condition
def find_max_injection_rate(df, fail_rate_condition):
    df_filtered = df[df['fail_rate'] <= fail_rate_condition]
    df_not_filtered = df[df['fail_rate'] > fail_rate_condition]
    df_max_injection_list = []

    for tx in df['tx per block'].unique():
        filtered_values = df_filtered[df_filtered['tx per block'] == tx]['injection rate(per sec)']
        not_filtered_values = df_not_filtered[df_not_filtered['tx per block'] == tx]['injection rate(per sec)']

        if not_filtered_values.empty:
            max_injection_rate = filtered_values.max()
        else:
            min_not_filtered_value = not_filtered_values.min()
            max_injection_rate = filtered_values[filtered_values < min_not_filtered_value].max()

        df_max_injection_list.append({
            'tx per block': tx,
            f'fail_rate<={int(fail_rate_condition * 100)}%': max_injection_rate
        })

    df_max_injection = pd.DataFrame(df_max_injection_list)
    return df_max_injection

# Find the maximum injection rate for fail rate conditions <= 5% and <= 10%
df_max_injection_1 = find_max_injection_rate(df_rate, failrate_limit1)
df_max_injection_2 = find_max_injection_rate(df_rate, failrate_limit2)
df_max_injection_3 = find_max_injection_rate(df_rate, failrate_limit3)

# Merge the results into a single DataFrame
df_max_injection_merged_0_5 = pd.merge(df_max_injection_1, df_max_injection_2, on='tx per block', how='outer')
df_max_injection_merged = pd.merge(df_max_injection_merged_0_5, df_max_injection_3, on='tx per block', how='outer')


# Write the result to an Excel file
df_max_injection_merged.to_excel('max_injection_rate'+postfix+'.xlsx', index=False)
print("Excel max injection rate result file for multiple conditions generated")


xdata = df_max_injection_1['tx per block']
ydata = df_max_injection_1.iloc[:, log_fit_col]
# ydata = df_max_injection_1['fail_rate<=0%']
# ydata = df_max_injection_2['fail_rate<=5%']
# ydata = df_max_injection_3['fail_rate<=10%']


# Define the logarithmic function to fit to the data
def log_func(x, a, b, c):
    # return a + b * numpy.log(d * x) + c * x
    return a + b * numpy.log(x) + c * x
    # return a * numpy.log(x) + b + c

def exponential_func(x, a, b, c, d):
    return a + b * x + c * numpy.exp(d * x)

guess = [100, 0.1, -50, -0.1]
# Perform the curve fitting
popt1, pcov1 = curve_fit(log_func, xdata, ydata)
popt2, pcov2 = curve_fit(exponential_func, xdata, ydata, guess)
y1 = log_func(xdata, *popt1)
y2 = exponential_func(xdata, *popt2)
log_func_str = 'y = '+str(popt1[0])+' + '+str(popt1[1])+' * log(x) + '+str(popt1[2])+' * x'
exp_func_str = 'y = '+ str(popt2[0]) + ' + ' + str(popt2[1]) + ' * x + '+ str(popt2[2]) + ' * e ^ (' + str(popt2[3]) + ' * x )'
log_r2_score = str(r2_score(ydata, y1))
exp_r2_score = str(r2_score(ydata, y2))

print('--------------------------------------------------------------')
print('[log] R^2: ', log_r2_score)
print(log_func_str)
print(popt1)
print(pcov1)
print('--------------------------------------------------------------')

print('--------------------------------------------------------------')
print('[exp] R^2: ', r2_score(ydata, y2))
print('y =', popt2[0], '+', popt2[1], '* x +', popt2[2], '* e ^ (', popt2[3], '* x )')
print(popt2)
print(pcov2)
print('--------------------------------------------------------------')

# Plot the data and the fitted curve
fig = plt.figure()
fig.set_figwidth(30)
fig.set_figheight(10)
plt.plot(xdata, ydata, 'b-', label='data')

plt.plot(xdata, y1, 'r-', label='log_fit')
plt.plot(xdata, y2, 'g-', label='exp_fit')

plt.title(postfix+' curve fitting\nlog:'+log_func_str+'    R2:'+log_r2_score+'\nexp:'+exp_func_str+'    R2:'+exp_r2_score)
plt.xlabel('tx per block')
plt.ylabel('max injection rate')
plt.legend()
# plt.show()

# Save plot to file
# plt.subplots_adjust(left = 0.01, right = 0.99)
plt.savefig('logarithmic_fitting'+postfix+'.png')
print("curve fitting plot file generated")