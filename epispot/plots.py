"""
The 'plots' module contains all plotting functions for visualizing models.
These functions require the installation of matplotlib for graphics.
STRUCTURE:
- plot_comp_nums
- compare
"""

from . import plt
from . import random
from . import colors


def plot_comp_nums(Model, timesteps, starting_state=None, seed=100):
    """
    This is meant for plotting the number of people in each compartment over a period of time

    :param Model: an instance of the `Model` class
    :param timesteps: timesteps to plot as range(beg_time, end_time, day_length)
    :param starting_state: initial conditions vector: [comp_1_start, comp_2_start, ...]
    :param seed: =100, for generating new random colors
    :return: matplotlib plot
    """

    f, ax = plt.subplots(1, 1, figsize=(10, 4))
    integral = Model.integrate(timesteps, starting_state=starting_state)
    compartments = []

    for _ in integral[0]:
        compartments.append([])

    for timestep in integral:
        for compartment in range(len(timestep)):
            compartments[compartment].append(timestep[compartment])

    random.seed(a=seed)
    for layer in range(len(Model.layers)):
        color = (random.random(), random.random(), random.random())
        ax.plot(timesteps, compartments[layer], colors.to_hex(color), linewidth=2,
                label=Model.layer_names[layer])

    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)

    ax.set_xlabel('Time (days)')
    ax.set_ylabel('People')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)

    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)

    plt.show()


def compare(ranges, title="", subtitle="", markers=None, seed=200):
    """
    This function is used to compare multiple predictions which can range across time ranges.
    Often, this is used to compare real data with model predictions or to show the predictions after
    the real data in one window.

    :param ranges: A list of items to plot. Follow the idiom below:
                    [timesteps (use range(beg, end)), predictions (corresponding to each element in `timesteps`,
                    label (in str() format), ... ]
    :param title: ="", (str) the title of the plot
    :param subtitle: ="", (str) the subtitle of the plot
    :param markers: =[], a list of sequenced markers in the format:
                         ['marker name', [...marker parameters]]
                         'marker name' can be any of:
                            - line, param: [y, x1, x2, label]
                            - highlighted-box, param: [x1, x2, y1 (axis units), y2 (axis units)]
                            - point, param: [label, x, y]
                            - arrow, param: [x, y, dx, dy]
    :param seed: =200, for generating new random colors
    :return: matplotlib plot (log scale)
    """

    f, ax = plt.subplots(1, 1, figsize=(10, 4))
    plt.yscale('log')

    random.seed(a=seed)
    for r in ranges:
        color = (random.random(), random.random(), random.random())
        ax.plot(r[0], r[1], colors.to_hex(color), linewidth=2,
                label=r[2])

    if markers is not None:
        for marker in markers:

            if marker[0] == 'line':
                plt.hlines(marker[1][0], marker[1][1], marker[1][2], label=marker[1][3])

            if marker[0] == 'highlighted-box':
                plt.axvspan(marker[1][0], marker[1][1], ymin=marker[1][2], ymax=marker[1][3], facecolor='y', alpha=0.25)

            if marker[0] == 'point':
                plt.plot(marker[1][1], marker[1][2], 'ko')
                plt.annotate(marker[1][0], (marker[1][1] + 1, marker[1][2] + 1))

            if marker[0] == 'arrow':
                plt.arrow(marker[1][0], marker[1][1], marker[1][2], marker[1][3])

    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)

    ax.set_xlabel('Time (days)')
    ax.set_ylabel('People')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)

    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)

    plt.title(title+': '+subtitle)
    plt.show()
