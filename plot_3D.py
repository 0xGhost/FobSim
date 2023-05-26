import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.metrics import r2_score
import sys



mode = 1 # 1 for failrate, 2 for avg_block_time
#handle console arguments
if len(sys.argv) >= 2:
    mode = int(sys.argv[1])

filename = ''
result_y = ''

if mode == 1:
    filename = '3D_max_injection_rate.xlsx'
    result_y = 'max injection rate(per sec)'
elif mode == 2:
    filename = '3D_avg_block_time.xlsx'
    result_y = 'avg block time(ms)'




# Define the function to plot
def func(x1, x2):
    if mode == 1:
        return func1(x1, x2)
    elif mode == 2:
        return func2(x1, x2)

def func1(x1, x2):
    return (0.1594*x2 + 8.699) + (0.2787*x2 - 2.352) * np.log(x1) + (-0.003334*x2 + 0.06600) * x1

def func2(x1, x2): # for avg_block_time
    return (413.2 * pow(x2, -0.96)) * x1 + 4687.7 * pow(x2, -1.002)

# Load the Excel file into a pandas dataframe
df = pd.read_excel(filename, index_col=0)
# print(df)

# Get the values of x1 and x2 from the dataframe
ox1 = df.index.values.astype(float)
ox2 = df.columns.values.astype(float)

# Create a 2D grid of x1 and x2 values
oX1, oX2 = np.meshgrid(ox1, ox2)

# print(ox1)
# print(ox2)
# print(oX1)
# print(oX2)

# Calculate the predicted values for each point in the grid
Y_pred = func(oX1, oX2)

# Switch the rows and columns of Y_pred
Y_pred = Y_pred.transpose()

# Flatten the dataframe and the predicted values into 1D arrays
Y_true = df.values.flatten()
Y_pred = Y_pred.flatten()
# print(Y_true)
# print(Y_pred)
# Calculate the R-squared score
r2 = r2_score(Y_true, Y_pred)

# Print the R-squared score
print('R-squared score:', r2)

# Generate the values for x1 and x2
# x1 = np.linspace(5, 95, 20)
x1 = np.linspace(5, 95, 100)
# x2 = np.linspace(100, 800, 8)
x2 = np.linspace(100, 800, 100)

# Create a 2D grid of x1 and x2 values
X1, X2 = np.meshgrid(x1, x2)

# Calculate the corresponding y values for each point in the grid
Y = func(X1, X2)

# Create a 3D plot of the function
fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X1, X2, Y, cmap='coolwarm')
ax.set_xlabel('tx per block')
ax.set_ylabel('network bandwidth')
ax.set_zlabel(result_y)
if mode == 1:
    plt.title("predict injection rate from block size and network bandwidth")
elif mode == 2:
    plt.title("predict average block time from block size and network bandwidth")

plt.savefig(result_y+'_fitting.png')

print("plot successfully generated")