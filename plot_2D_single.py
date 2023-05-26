import numpy as np
import matplotlib.pyplot as plt

def plot_function():
# Define the functions to plot
    def x2(x1):
        return (8.699 - 2.352 * np.log(x1) + 0.066 * x1 - 129.032)/ -(0.1594 + 0.2787 * np.log(x1) -0.003334 * x1)

    def f(x1):
        return (100 - 4687.7 * pow(x2(x1), -1.002))/(413.2 * pow(x2(x1), -0.96)) - x1

    # Generate x values from -2*pi to 2*pi
    x1 = np.linspace(1, 99, 1000)


    # Generate y values for the two functions
    y = f(x1)


    # Create the plot
    fig, ax = plt.subplots()
    fig.set_figwidth(15)
    fig.set_figheight(10)
    # Plot the first function and fill upper area with red color
    ax.plot(x1, y, 'r-', linewidth=2)
    # ax.fill_between(x1, y, 800, where=(y_x2 >= 0), interpolate=True, color='red', alpha=0.3)

    # Plot the second function and fill upper area with blue color
    # ax.plot(y_x1, x2, 'b-', linewidth=2, label='block time constraint')
    # ax.fill_between(y_x1, x2, 800, where=(y_x1 >= 0), interpolate=True, color='blue', alpha=0.3)

    # Fill the area where the two functions overlap with green color
    # ax.fill_between(x, np.minimum(y1, y2), 1, where=(y1 >= 0) & (y2 >= 0), interpolate=True, color='green', alpha=0.3)


    # Enable horizontal grid lines
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Set labels and title
    ax.set_xlabel('transaction per block')
    ax.set_ylabel('network bandwidth')
    ax.set_title('tpb vs bandwidth under block time and injection rate constraints')
    
    # Add legend
    # ax.legend()
    
    # Display the plot
    # plt.show()
    plt.savefig('function_plot.png')
    
# Call the function to plot the function and fill the upper area
plot_function()