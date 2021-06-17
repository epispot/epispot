"""
This sub-package is responsible for plotting epispot models of the `epispot.models.Model` class.
This is done independently of any other modules and thus all functions within this subpackage
will require a reference to a `Model` class to plot.

## Structure

- web.py
"""


def _dependency_check():
    """Checks dependencies"""
    try:
        import plotly
    except ImportError:  # pragma: no cover
        raise ImportError('In order to create interactive web-based plots, it is highly recommended that you install `plotly` as an experimental dependency.\n'
                          'Install with either:\n'
                          ' $ pip install plotly\n'
                          ' $ conda install -c conda-forge plotly')
    try:
        from matplotlib import pyplot as plt
        plt.style.use('science')  # `SciencePlots` cannot be imported directly
    except ImportError:  # pragma: no cover
        raise ImportError('In order to create scientific plots with `matplotlib`, it is highly recommended that you install `SciencePlots` as an experimental' 
                          'dependency. Please note that `SciencePlots` is only available via `pip` at this time. If using Anaconda, '
                          'use the pre-existing `pip` installation to add `SciencePlots` to your environment.\n'
                          'Install with:\n'
                          ' $ pip install SciencePlots')


# imports
import warnings


# dependencies
_dependency_check()  # check for uninstalled dependencies
del _dependency_check
import plotly.express as px
from matplotlib import pyplot as plt
from matplotlib import colors


# local
from . import web
from . import native
