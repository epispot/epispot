"""
The `web` module contains various web-based plotting mechanisms.
These plotting mechanisms use `plotly` to generate in-browser plots of epispot models.
`plotly` is a required dependency for these modules. If you haven't already, install it with:
```shell
pip install plotly
```

## Structure:

- model()
- stacked()
"""

from . import px


def model(Model, time_frame, title='Compartment Populations over Time', 
          starting_state=None, show_susceptible=False, log=False, 
          colors=None):
    """
    Plots the results of one model using `plotly`.
    The results are displayed in-browser via a `localhost`.
    There are various ways to customize the generated plots by modifying
    the time frame or compartments displayed.

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
    - colors: (default:plotly default) A list of CSS-valid colors to cycle through in the plot
    - return: `plotly` figure (display in-browser with `.show()`)
    """

    DataFrame = {}
    System = Model.integrate(time_frame, starting_state=starting_state)
    
    # variable substitutions
    names = Model.names
    
    # setup
    for name in names:
        DataFrame[name] = []
    
    for day in System:
        for i, compartment in enumerate(day):
            DataFrame[names[i]].append(compartment)
    
    if not show_susceptible:
        del DataFrame[names[0]]

    if not colors:
        colors = px.colors.qualitative.Alphabet

    # plotting
    Figure = px.line(DataFrame, 
                    labels={
                        'index': 'Time (in days)',
                        'value': 'Compartment Population'
                    }, 
                    title=title,
                    color_discrete_sequence=colors, 
                    template='plotly_white',
                    log_y=log)
    
    Figure.update_layout(
        font = dict(
            family="Times New Roman, Serif",
            size=24,
            color="Black"
        ),
        margin=dict(
            l=250, 
            r=250, 
            t=150,
            b=150,
        ),
    )

    return Figure


def stacked(Model, time_frame, title='Compartment Populations over Time', 
            starting_state=None, show_susceptible=False, log=False, 
            colors=None):
    """
    Plots the results of one model using `plotly` as a stacked area chart.
    The results are displayed in-browser via a `localhost`.
    There are various ways to customize the generated plots by modifying
    the time frame or compartments displayed.

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
    - colors: (default:plotly default) A list of CSS-valid colors to cycle through in the plot
    - return: `plotly` figure (display in-browser with `.show()`)
    """

    DataFrame = {}
    System = Model.integrate(time_frame, starting_state=starting_state)

    # variable substitutions
    names = Model.names

    # setup
    for name in names:
        DataFrame[name] = []

    for day in System:
        for i, compartment in enumerate(day):
            DataFrame[names[i]].append(compartment)

    if not show_susceptible:
        del DataFrame[names[0]]

    if not colors:
        colors = px.colors.qualitative.Alphabet

    # plotting
    Figure = px.area(DataFrame,
                     labels={
                         'index': 'Time (in days)',
                         'value': 'Compartment Population'
                     },
                     title=title,
                     color_discrete_sequence=colors,
                     template='plotly_white',
                     log_y=log)

    Figure.update_layout(
        font=dict(
            family="Times New Roman, Serif",
            size=24,
            color="Black"
        ),
        margin=dict(
            l=250,
            r=250,
            t=150,
            b=150,
        ),
    )

    return Figure
