import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the function to plot
def func(x1, x2):
    return (0.1594*x2 + 8.699) + (0.2787*x2 - 2.352) * np.log(x1) + (-0.003334*x2 + 0.06600) * x1

# Generate the values for x1 and x2
x1 = np.linspace(5, 95, 100)
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
ax.set_zlabel('max injection rate')
plt.title("predict injection rate from block size and network bandwidth")

plt.savefig('3D_fitting.png')

print("plot successfully generated")