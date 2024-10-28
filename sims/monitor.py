import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

CHANNELS = 7
epoch_buf = []
p_bufs = [list() for _ in range(CHANNELS)]
acc_bufs = [list() for _ in range(CHANNELS)]

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_title("Event P(success)")
ax2.set_title("Event Accumulated Successes")
fig.suptitle("Monte Carlo Simulation")
fig.supxlabel('Simulation Epoch')

# Initialize two line objects (one in each axes)
# Add annotations for each line
line_p = []
line_acc= []
ann_p = []
ann_acc = []
colors = ['blue', 'green', 'red', 'orange', 'purple', 'pink', 'gold']
for i in range(CHANNELS):
    l1, = ax1.plot([],[],label=f"P(E{i})", color=colors[i])
    l2, = ax2.plot([],[],label=f"ACC(E{i})", color=colors[i])
    line_p.append(l1)
    line_acc.append(l2)
    ann_p.append(ax1.text(0, 0, "", color=colors[i]))
    ann_acc.append(ax2.text(0, 0, "", color=colors[i]))

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
    for l in line_p:
        l.set_data([], [])
    for l in line_acc:
        l.set_data([], [])
    for a in ann_p:
        a.set_text("")
    for a in ann_acc:
        a.set_text("")
    return line_p + line_acc + ann_p + ann_acc

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
            results = line.strip().split(',')
            rv = []
            rv.append(int(results[0]))
            for i in range(1,CHANNELS+1):
                rv.append(int(results[i]))
                rv.append(float(results[i+CHANNELS]))
            yield rv


def run(data):
    """
    Redraw the plot with the latest data.
    """
    epoch_buf.append(data[0])
    acc_buf = []
    p_buf = []
    for i in range(1,CHANNELS*2,2):
        acc_buf.append(data[i])
        p_buf.append(data[i+1])
    for i in range(CHANNELS):
        p_bufs[i].append(p_buf[i])
        acc_bufs[i].append(acc_buf[i])

    # Dynamically adjust axis limits if needed
    xmin, xmax = ax1.get_xlim()
    if data[0] >= xmax:
        ax1.set_xlim(xmin, 2 * xmax)
        ax2.set_xlim(xmin, 2 * xmax)
        ax1.figure.canvas.draw()
        ax2.figure.canvas.draw()
    ymin2, ymax2 = ax2.get_ylim()
    acc_sum = []
    for acc_buf in acc_bufs:
        acc_sum += acc_buf
    min_acc = min(acc_sum)
    max_acc = max(acc_sum)
    if min_acc <= ymin2 or max_acc >= ymax2:
        ax2.set_ylim(min_acc - 0.1, max_acc + 0.5 * max_acc)

    for i in range(0, CHANNELS, 2):
        # Update the data for each line
        line_p[i].set_data(epoch_buf, p_bufs[i])
        line_acc[i].set_data(epoch_buf, acc_bufs[i])
        # Update annotations with the latest y-values and position
        ann_p[i].set_position((epoch_buf[-1], p_bufs[i][-1]))
        ann_p[i].set_text(f'{p_bufs[i][-1]:.2f}')
        ann_acc[i].set_position((epoch_buf[-1], acc_bufs[i][-1]))
        ann_acc[i].set_text(f'{acc_bufs[i][-1]}')

    return line_p + line_acc + ann_p + ann_acc

if __name__ == '__main__':
    # Create the animation
    ani = animation.FuncAnimation(fig, run, read_data, init_func=init, interval=1, blit=True, repeat=False, cache_frame_data=False)
    plt.show()
