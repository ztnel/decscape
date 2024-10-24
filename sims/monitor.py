import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

epoch_buf = []
p_s1_buf = []
p_s2_buf = []
p_s1_s2_buf = []
acc_s2_buf = []
acc_s1_buf = []

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_title("Event P(success)")
ax2.set_title("Event Accumulated Successes")
fig.suptitle("Monte Carlo Simulation")
fig.supxlabel('Simulation Epoch')

# Initialize two line objects (one in each axes)
l1, = ax1.plot([], [], label="P(S1)", color='blue')
l2, = ax1.plot([], [], label="P(S2)", color='green')
l3, = ax1.plot([], [], label="P(S1+S2)", color='red')
l4, = ax2.plot([], [], label="ACC(S1)", color='blue')
l5, = ax2.plot([], [], label="ACC(S2)", color='green')
line = [l1, l2, l3, l4, l5]

# Add annotations for each line
annot_p_s1 = ax1.text(0, 0, "", color='blue')
annot_p_s2 = ax1.text(0, 0, "", color='green')
annot_p_s1_s2 = ax1.text(0, 0, "", color='red')
annot_acc_s1 = ax2.text(0, 0, "", color='blue')
annot_acc_s2 = ax2.text(0, 0, "", color='green')

annotations = [annot_p_s1, annot_p_s2, annot_p_s1_s2, annot_acc_s1, annot_acc_s2]

# Set axis labels
ax1.set_ylabel("P(success)")
ax2.set_ylabel('Accumulated Successes')
ax1.minorticks_on()
ax2.minorticks_on()
# Add legends to the plots
ax1.legend()
ax2.legend()

# Initialize the limits for the axes
ax1.set_xlim(0, 10)
ax1.set_ylim(0.0, 1.2)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 1)

def init():
    """
    Initialization function for FuncAnimation.
    Sets the line objects with empty data.
    """
    for l in line:
        l.set_data([], [])
    for a in annotations:
        a.set_text("")
    return line + annotations

def read_data():
    """
    Reads data from stdin and yields it to be used in the animation.
    """
    while True:
        line = sys.stdin.readline()
        if line == "\n":
            ani.event_source.stop()
            break;
        if line and not line[0].isalpha():
            # Split the line and convert to appropriate types
            epoch, acc_s1, acc_s2, p_s1, p_s2, p_s1_s2 = line.strip().split(',')
            yield int(epoch), int(acc_s1), int(acc_s2), float(p_s1), float(p_s2), float(p_s1_s2)


def run(data):
    """
    Redraw the plot with the latest data.
    """
    epoch, acc_s1, acc_s2, p_s1, p_s2, p_s1_s2 = data
    epoch_buf.append(epoch)
    p_s1_buf.append(p_s1)
    p_s2_buf.append(p_s2)
    acc_s1_buf.append(acc_s1)
    acc_s2_buf.append(acc_s2)
    p_s1_s2_buf.append(p_s1_s2)
    
    # Dynamically adjust axis limits if needed
    xmin, xmax = ax1.get_xlim()
    if epoch >= xmax:
        ax1.set_xlim(xmin, 2 * xmax)
        ax2.set_xlim(xmin, 2 * xmax)
        ax1.figure.canvas.draw()
        ax2.figure.canvas.draw()
    
    ymin2, ymax2 = ax2.get_ylim()
    
    if min(acc_s1_buf + acc_s2_buf) <= ymin2 or max(acc_s1_buf + acc_s2_buf) >= ymax2:
        ax2.set_ylim(min(acc_s1_buf + acc_s2_buf) - 0.1, max(acc_s1_buf + acc_s2_buf) + 0.1 * max(acc_s1_buf + acc_s2_buf))

    # Update the data for each line
    line[0].set_data(epoch_buf, p_s1_buf)
    line[1].set_data(epoch_buf, p_s2_buf)
    line[2].set_data(epoch_buf, p_s1_s2_buf)
    line[3].set_data(epoch_buf, acc_s1_buf)
    line[4].set_data(epoch_buf, acc_s2_buf)

    # Update annotations with the latest y-values and position
    annotations[0].set_position((epoch_buf[-1], p_s1_buf[-1]))
    annotations[0].set_text(f'{p_s1_buf[-1]:.2f}')

    annotations[1].set_position((epoch_buf[-1], p_s2_buf[-1]))
    annotations[1].set_text(f'{p_s2_buf[-1]:.2f}')

    annotations[2].set_position((epoch_buf[-1], p_s1_s2_buf[-1]))
    annotations[2].set_text(f'{p_s1_s2_buf[-1]}')

    annotations[3].set_position((epoch_buf[-1], acc_s1_buf[-1]))
    annotations[3].set_text(f'{acc_s1_buf[-1]}')

    annotations[4].set_position((epoch_buf[-1], acc_s2_buf[-1]))
    annotations[4].set_text(f'{acc_s2_buf[-1]}')

    return line + annotations

if __name__ == '__main__':
    # Create the animation
    ani = animation.FuncAnimation(fig, run, read_data, init_func=init, interval=1, blit=True, repeat=False, cache_frame_data=False)
    plt.show()
