import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
# Replace 'your_file.csv' with the actual file path of your CSV
data = pd.read_csv('results.csv')

# Extract bin numbers and P(success) values from the CSV
bins = data.iloc[:, 0]  # Left-most column for bin numbers
p_success = data.iloc[:, -1]  # Right-most column for P(success)

# Plot the histogram using the data
fig, ax = plt.subplots()
ax.bar(bins, p_success, width=0.8, color='blue', alpha=0.7)

# Set plot labels and title
ax.set_xlabel('Number of Successes')
ax.set_ylabel('P(Success)')
ax.set_title('Histogram of Successes vs Probability of Success')

# Set x-axis ticks to match bin numbers
ax.set_xticks(bins)
ax.minorticks_on()
min_y = min(p_success) - 0.01  # Add a small margin below the minimum
max_y = max(p_success) + 0.01  # Add a small margin above the maximum
ax.set_ylim(min_y, max_y)
# Display the plot
plt.show()
