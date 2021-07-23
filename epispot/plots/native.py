"""
The `native` module contains various plotting mechanisms utilizing `matplotlib`.
Additionally, in order to display scientifically polished graphs, this module uses the
[Science-Plots](https://pypi.org/project/SciencePlots/1.0.8/) package.\
We strongly encourage you to cite the authors of this package as demonstrated below:

> John Garrett. (2021, June 2). SciencePlots (v1.0.8) (Version 1.0.8). Zenodo. http://doi.org/10.5281/zenodo.4893230

Unfortunately, the `SciencePlots` package is only available on `pip` at this time.
If you use an Anaconda system, you should still have no problem installing it since `pip` comes pre-installed with most versions.
Install with:
```shell
pip install SciencePlots
```

Additionally, all functions in this module have a `latex` flag which determines whether to use LaTeX or not.
In order to use LaTeX, please follow the installation instructions for your operating system listed on the
[`SciencePlots` project README](https://github.com/garrettj403/SciencePlots#faq).  <!-- spellcheck: disable -->

## Structure:

- model()
- stacked()
"""

from . import plt
plt.style.use(['science', 'no-latex'])  # default style


def model(Model, time_frame, title='Compartment Populations over Time', 
          starting_state=None, show_susceptible=False, log=False, 
          latex=True):
    """
    Plots the results of one model using `matplotlib`.
    The results are displayed natively via a `matplotlib` window.
    There are various ways to customize the generated plots by modifying
    the time frame or compartments displayed.
    Additionally, `matplotlib` allows editing plots even after
    they have been created to change things like colors, margins, etc.

    - Model: An `epispot.models.Model` object
    - time_frame: A `range()` describing the time period to plot
    - title: (`='Compartment Populations over Time`) The title of the plot
    - starting_state: (default:inherited) Initial model state (see `epispot.models.Model.integrate` parameter `starting_state`)
    - show_susceptible: (`=False`) Boolean value describing whether or not to plot the Susceptible compartment.\
                                   **This assumes that the Susceptible compartment is the first in `Model`**\
                                   Note:\
                                   > This can potentially result in less visibility for other compartments
                                   > since usually the Susceptible compartment comprises of many, many
                                   > more individuals than the other compartments combined.
    - log: (`=False`) Boolean value indicating whether or not to use a logarithmic scale when plotting `Model`
    - latex: (`=True`) Turn off if you do not have LaTeX installed or want quicker loading times
    - return: `pyplot` figure (display with `.show()`)
    """

    if latex:
        plt.style.use('science')

    DataFrame = {}
    System = Model.integrate(time_frame, starting_state=starting_state)

    # variable substitutions
    names = Model.names

    # setup
    for name in Model.names:
        DataFrame[name] = []

    for day in System:
        for i, compartment in enumerate(day):
            DataFrame[Model.names[i]].append(compartment)

    # plotting
    plt.figure(figsize=(9, 5))
    for compartment, _ in enumerate(Model.compartments):
        if (not show_susceptible and compartment != 0) or show_susceptible:
            plt.plot(time_frame, DataFrame[Model.names[compartment]], label=names[compartment])

    if log:
        plt.yscale('log')
    plt.title(title)
    plt.legend()

    return plt


def stacked(Model, time_frame, title='Compartment Populations over Time',
          starting_state=None, compartments=None, show_susceptible=False,
          log=False, latex=True):
    """
    Plots the results of one model using `matplotlib`.
    The results are displayed natively via a `matplotlib` window as a stacked area chart.
    There are various ways to customize the generated plots by modifying
    the time frame or compartments displayed.
    Additionally, `matplotlib` allows editing plots even after
    they have been created to change things like colors, margins, etc.

    - Model: An `epispot.models.Model` object
    - time_frame: A `range()` describing the time period to plot
    - title: (`='Compartment Populations over Time`) The title of the plot
    - starting_state: (default:inherited) Initial model state (see `epispot.models.Model.integrate` parameter `starting_state`)
    - compartments: (default:all) The indices of the compartments in the model to plot;
                    all other compartments will be hidden
    - show_susceptible: (`=False`) Boolean value describing whether or not to plot the Susceptible compartment.\
                                   **This assumes that the Susceptible compartment is the first in `Model`**\
                                   Note:\
                                   > This can potentially result in less visibility for other compartments
                                   > since usually the Susceptible compartment comprises of many, many
                                   > more individuals than the other compartments combined.
    - log: (`=False`) Boolean value indicating whether or not to use a logarithmic scale when plotting `Model`
    - latex: (`=True`) Turn off if you do not have LaTeX installed or want quicker loading times
    - return: `pyplot` figure (display with `.show()`)
    """

    if latex:
        plt.style.use('science')

    DataFrame = {}
    System = Model.integrate(time_frame, starting_state=starting_state)

    # variable substitutions
    if compartments is None:
        compartments = list(range(len(Model.compartments)))

    names = Model.names

    # setup
    for name in Model.names:
        DataFrame[name] = []

    for day in System:
        for i, compartment in enumerate(day):
            DataFrame[Model.names[i]].append(compartment)

    if not show_susceptible:
        for i, compartment in enumerate(compartments):
            if compartment == 0:
                del compartments[i]
                break

    # plotting
    plt.figure(figsize=(9, 5))
    plt.stackplot(time_frame, *[DataFrame[Model.names[compartment]] for compartment in compartments], 
                  labels=[names[compartment] for compartment in compartments])

    if log:
        plt.yscale('log')
    plt.title(title)
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.2), borderaxespad=0, ncol=2)  # spellcheck: disable
    plt.tight_layout()

    return plt
