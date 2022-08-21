"""
The `web` module contains various web-based plotting mechanisms.
These plotting mechanisms use `plotly` to generate in-browser plots of epispot models.
`plotly` is a required dependency for these modules.
If you haven't already, install it with:

```shell
pip install plotly
```

"""

from . import px


def model(model, time_frame, title='Compartment Populations over Time',
          show_susceptible=False, log=False, colors=None, **kwargs):
    """
    Plots the results of one model using `plotly`.
    The results are displayed in-browser via a `localhost`.
    There are various ways to customize the generated plots by modifying the time frame or compartments displayed.

    ## Parameters

    `model (epispot.models.Model)`: A `epispot.models.Model` object

    `time_frame (range)`: A `range()` describing the time period to plot;
        use `timesteps=` keyword argument to use `np.linspace` as the `time_frame` is simply for the x-axis

    `title='Compartment Populations over Time' (str)`: The title of the plot

    `show_susceptible=False (bool)`: Boolean value describing whether or not to plot the Susceptible compartment.

    ..important::
        This assumes that the Susceptible compartment is the first in `Model`

    ..note::
        This can potentially result in less visibility for other compartments
        since usually the Susceptible compartment comprises of many, many
        more individuals than the other compartments combined.

    `log=False (bool)`: Boolean value indicating whether or not to use a logarithmic scale when plotting `Model`

    `colors=None (list[str])`: A list of CSS-valid colors to cycle through in the plot;
        defaults to Plotly's theme colors.

    `**kwargs**`: Keyword arguments to pass into `epispot.models.Model.integrate()`

    ## Returns

    `plotly` figure (display in-browser with `.show()`) with the required data
    (`plotly.graph_objects.Figure`)

    """

    data_frame = {}
    system = model.integrate(time_frame, **kwargs)

    # variable substitutions
    names = model.names

    # setup
    for name in names:
        data_frame[name] = []

    for day in system:
        for i, compartment in enumerate(day):
            data_frame[names[i]].append(compartment)

    if not show_susceptible:
        del data_frame[names[0]]

    if not colors:
        colors = px.colors.qualitative.Alphabet

    # plotting
    figure = px.line(
        data_frame,
        labels={
            'index': 'Time (in days)',
            'value': 'Compartment Population'
        },
        title=title,
        color_discrete_sequence=colors,
        template='plotly_white',
        log_y=log
    )

    figure.update_layout(
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

    return figure


def stacked(model, time_frame, title='Compartment Populations over Time',
            show_susceptible=False, log=False, colors=None, **kwargs):
    """
    Plots the results of one model using `plotly` as a stacked area chart.
    The results are displayed in-browser via a `localhost`.
    There are various ways to customize the generated plots by modifying the time frame or compartments displayed.

    ## Parameters

    `model (epispot.models.Model)`: A `epispot.models.Model` object

    `time_frame (range)`: A `range()` describing the time period to plot;
        use `timesteps=` keyword argument to use `np.linspace` as the `time_frame` is simply for the x-axis

    `title='Compartment Populations over Time' (str)`: The title of the plot

    `show_susceptible=False (bool)`: Boolean value describing whether or not to plot the Susceptible compartment.

    ..important::
        This assumes that the Susceptible compartment is the first in `Model`

    ..note::
        This can potentially result in less visibility for other compartments
        since usually the Susceptible compartment comprises of many, many
        more individuals than the other compartments combined.

    `log=False (bool)`: Boolean value indicating whether or not to use a logarithmic scale when plotting `Model`

    `colors=None (list[str])`: A list of CSS-valid colors to cycle through in the plot;
        defaults to Plotly's theme colors.

    `**kwargs**`: Keyword arguments to pass into `epispot.models.Model.integrate()`

    ## Returns

    `plotly` figure (display in-browser with `.show()`) with the required data
    (`plotly.graph_objects.Figure`)

    """

    data_frame = {}
    system = model.integrate(time_frame, **kwargs)

    # variable substitutions
    names = model.names

    # setup
    for name in names:
        data_frame[name] = []

    for day in system:
        for i, compartment in enumerate(day):
            data_frame[names[i]].append(compartment)

    if not show_susceptible:
        del data_frame[names[0]]

    if not colors:
        colors = px.colors.qualitative.Alphabet

    # plotting
    figure = px.area(data_frame,
                     labels={
                         'index': 'Time (in days)',
                         'value': 'Compartment Population'
                     },
                     title=title,
                     color_discrete_sequence=colors,
                     template='plotly_white',
                     log_y=log)

    figure.update_layout(
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

    return figure
