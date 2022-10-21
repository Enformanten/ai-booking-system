from itertools import product

import matplotlib.pyplot as plt
import numpy as np

rooms = np.arange(12).reshape(3, -1)
template = np.zeros_like(rooms)

occupations = []
# 1st and last hour
occupation = np.zeros(12)
occupation[4] = 1
occupation = occupation.reshape(3, -1)

# 2nd hour
occupation2 = np.zeros(12)
occupation2[[3, 11]] = 1
occupation2 = occupation2.reshape(3, -1)

occupations = [occupation.copy(), occupation2, occupation.copy()]

fig, axes = plt.subplots(1, 3)


def plotter(ax, occupation):
    # Plot colormap showing occupation
    ax.imshow(occupation, zorder=0)

    # Write room number
    for i, j in product(*map(range, rooms.shape)):
        ax.text(j, i, str(rooms[i, j]), color="w")

    # Draw vertical lines
    y = np.linspace(*ax.get_ylim(), 100)
    x = np.ones_like(y)
    for i in range(rooms.shape[1] - 1):
        ax.plot((i + 0.5) * x, y, "w-", zorder=3)

    # Draw horizontal lines
    x = np.linspace(*ax.get_xlim(), 100)
    y = np.ones_like(x)
    for i in range(rooms.shape[0] - 1):
        ax.plot(x, (i + 0.5) * y, "w-")


for i, occupation in enumerate(occupations):
    plotter(axes[i], occupation)
    axes[i].set_title(f"hour {i}")
plt.savefig("sketch.pdf")
