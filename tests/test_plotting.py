"""
Test of the `plots` subpackage in `epispot`

STRUCTURE:
├ GLOBALS
    ├ N
    ├ start
        ├ 1
        └ 2
    └ Model
└ TESTS
    ├ web
        ├ plain
        └ full
    ├ stacked
        ├ plain
        └ full
    ├ native
        ├ plain
        └ full
    └ native-stack
        ├ plain
        └ full
"""

import numpy as np

import epispot as epi

# GLOBALS
N = 1e6
start_1 = np.array([N - 10, 10, 0, 0])
start_2 = np.array([N - 50, 25, 25, 0])
SEIR_Model = epi.pre.seir(2.5, 1 / 2, N, 1 / 2)


# TESTS
def test_plain_web():
    """In-browser plotting test (minimal parameters)"""
    figure = epi.plots.web.model(SEIR_Model, range(120))
    return figure

def test_full_web():
    """In-browser plotting test (all parameters)"""
    figure = epi.plots.web.model(SEIR_Model, range(120),
                                 title='SEIR Model Plot',
                                 starting_state=start_1,
                                 show_susceptible=True,
                                 log=True,
                                 colors=['red', 'green', 'blue', 'purple'])
    return figure


def test_plain_stacked():
    """In-browser plotting test for stacked area charts (minimal parameters)"""
    figure = epi.plots.web.stacked(SEIR_Model, range(120))
    return figure

def test_full_stacked():
    """In-browser plotting test for stacked area charts (all parameters)"""
    figure = epi.plots.web.stacked(SEIR_Model, range(120),
                                   title='SEIR Model Plot',
                                   starting_state=start_1,
                                   show_susceptible=True,
                                   log=True,
                                   colors=['red', 'green', 'blue', 'purple'])
    return figure


def test_plain_native():
    """Native plotting test (minimal parameters)"""
    figure = epi.plots.native.model(
        SEIR_Model,
        range(120),
        latex=False
    )  # `latex=False` flag speeds up testing
    return figure

def test_full_native():
    """Native plotting test (all parameters)"""
    # `latex=True` enabled by default
    figure = epi.plots.native.model(SEIR_Model, range(120),
                                    title='SEIR Model Plot',
                                    starting_state=start_2,
                                    show_susceptible=True,
                                    log=True)
    return figure


def test_plain_native_stack():
    """Native plotting test for stacked area charts (minimal parameters)"""
    figure = epi.plots.native.stacked(
        SEIR_Model,
        range(120),
        latex=False
    )  # `latex=False` flag speeds up testing
    return figure

def test_full_native_stack():
    """Native plotting test for stacked area charts (all parameters)"""
    # `latex=True` enabled by default
    figure = epi.plots.native.stacked(SEIR_Model, range(120),
                                      title='SEIR Model Plot',
                                      starting_state=start_2,
                                      compartments=[0, 3],
                                      show_susceptible=True,
                                      log=True)
    return figure
