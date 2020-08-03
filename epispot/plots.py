"""
The 'plots' module contains all plotting functions for visualizing models.
These functions require the installation of matplotlib for graphics.
"""

from . import plt


def plot_comp_nums(Model, timesteps, starting_state=None):
    """
    This is meant for plotting the number of people in each compartment over a period of time

    :param Model: an instance of the `Model` class
    :param timesteps: timesteps to plot as range(beg_time, end_time, day_length)
    :param starting_state: initial conditions vector: [comp_1_start, comp_2_start, ...]
    :return: matplotlib plot
    """

    f, ax = plt.subplots(1, 1, figsize=(10, 4))
    integral = Model.integrate(timesteps, starting_state=starting_state)
    compartments = []

    for compartment in integral[0]:
        compartments.append([])

    for timestep in integral:
        for compartment in range(len(timestep)):
            compartments[compartment].append(timestep[compartment])

    colors = ['#545454', '#5386e4', '#d138bf', '#f87666', '#f8f272', '#822e81',
              '#9fbbcc', '#ff784f', '#45cb85', '#a5cc6b']
    for layer in range(len(Model.layers)):
        ax.plot(timesteps, compartments[layer], colors[layer % 10], linewidth=2,
                label=Model.layer_names[layer])

    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)

    ax.set_xlabel('Time (days)')
    ax.set_ylabel('People')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    for spine in ('top', 'right', 'bottom', 'left'): ax.spines[spine].set_visible(False)
    plt.show()
