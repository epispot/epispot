"""
Test of the `plots` subpackage in `epispot`
|- GLOBALS
   |- R_0
   |- N
   |- place
   |- gamma
   |- delta
|- TESTS
   |- web
      |- plain
      |- full
   |- stacked
      |- plain
      |- full
   |- native
      |- plain
"""

import epispot as epi


# GLOBALS
ConstE = 2.718  # for Gaussian distributions as parameter values


def R_0(t):
    """R Naught--shifted Gaussian distribution"""
    return 5 * ConstE ** ((- 1 / 500) * (t - 30) ** 2)


def N(t):
    """Total population--1 million (constant)"""
    return 1e6


def place(t):
    """Placeholder for repetitive probability-rate definitions--returns 1"""
    return 1.0


def gamma(t):
    """Gamma--Gaussian distribution decay from 1/4 to 1/14"""
    return (1 / 14) + (5 / 28) * (ConstE ** ((-1 / 1000) * (t ** 2)))


def delta(t):
    """Delta--constant"""
    return 1 / 1.5


# TESTS
def test_plain_web():
    """In-browser plotting test (minimal parameters)"""
    Model = epi.pre.SEIR(R_0, N, place, gamma, delta)  # compile model
    Figure = epi.plots.web.model(Model, range(120))
    return Figure


def test_full_web():
    """In-browser plotting test (all parameters)"""
    Model = epi.pre.SEIR(R_0, N, place, gamma, delta)  # compile model
    Figure = epi.plots.web.model(Model, range(120), 
                                 title='SEIR Model Plot',
                                 starting_state=[N(0) - 10, 10, 0], 
                                 compartments=[0, 1, 2], 
                                 names=['Susceptible', 'Pre-infection', 'Infection'], 
                                 show_susceptible=True, 
                                 log=True, 
                                 colors=['red', 'green', 'blue']
                                 )
    return Figure


def test_plain_stacked():
    """In-browser plotting test for stacked area charts (minimal parameters)"""
    Model = epi.pre.SEIR(R_0, N, place, gamma, delta)  # compile model
    Figure = epi.plots.web.stacked(Model, range(120))
    return Figure


def test_full_stacked():
    """In-browser plotting test for stacked area charts (all parameters)"""
    Model = epi.pre.SEIR(R_0, N, place, gamma, delta)  # compile model
    Figure = epi.plots.web.stacked(Model, range(120),
                                 title='SEIR Model Plot',
                                 starting_state=[N(0) - 10, 10, 0],
                                 compartments=[0, 1, 2],
                                 names=['Susceptible',
                                        'Pre-infection', 'Infection'],
                                 show_susceptible=True,
                                 log=True,
                                 colors=['red', 'green', 'blue']
                                 )
    return Figure


def test_plain_native():
    Model = epi.pre.SEIR(R_0, N, place, gamma, delta)  # compile model
    Figure = epi.plots.native.model(Model, range(120), latex=False)  # `latex=False` flag speeds up testing
    return Figure
