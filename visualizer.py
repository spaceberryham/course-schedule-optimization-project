import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from textwrap import fill

plt.rcParams.update({'font.size': 14})
day_index = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4}
day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

def wrap_text(text, width=10):
    return fill(text, width=width)

def time_to_float(t):
    dt = datetime.strptime(t, "%H:%M")
    return dt.hour + dt.minute / 60

# THIS IS THE METHOD USED BY run_all.py
# FOR EACH SCHEDULE, CREATE THE BLOCKS IN A PLOT
def vysualize(classes):

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))

    # Draw the class blocks
    for cls in classes:
        start = time_to_float(cls['begtime'])
        end = time_to_float(cls['endtime'])
        duration = end - start

        for d in cls['days']:
            x = day_index[d]
            y = start
            ax.text(x + 0.05, y + 0.15,
                    wrap_text(cls['name'], width=12),
                    va='top', ha='left',
                    fontsize=15, weight='bold',
                    fontname='Helvetica Neue')
            ax.broken_barh([(x, 0.95)], (y, duration), facecolors='skyblue')

    # Set labels and grid
    ax.set_xlim(0, 5)
    ax.set_ylim(7.0, 18.0)  # from 7:00 to 18:00
    ax.set_xticks(range(5))
    ax.set_xticklabels(day_labels)
    ax.set_yticks(range(7, 19))
    ax.set_yticklabels([f"{h}:00" for h in range(7, 19)])
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)

    ax.set_title("Weekly Class Schedule", fontsize=16)
    ax.invert_yaxis()  # Optional: makes earlier times appear at the top
    plt.tight_layout()
    plt.show()

    return fig

