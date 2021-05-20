"""
Test of all transforms performed with an epispot model,
including plotting and fitting modules
|- GLOBALS
   |- R_0
   |- N
   |- place
   |- gamma
|- MODELS
   |- SIR_Model
|- TESTS
   |- SIRS
   |- SIHCR
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
    """Gamma--Gaussian distribution decay from 1/4 to 1/8"""
    return (1 / 8) + (1 / 8) * (ConstE ** ((-1 / 1000) * (t ** 2)))


def delta(t):
    """Delta--constant"""
    return 1 / 1.5


# MODELS
PlotModel1 = epi.pre.SIR(R_0, N, place, gamma)
PlotModel2 = epi.pre.SEIR(R_0, N, place, gamma, delta)


# TESTS
def test_plots():
    """Base plotting test"""
    Base = epi.plots.plot_comp_nums(PlotModel1, range(100))
    Complex = epi.plots.plot_comp_nums(PlotModel2, range(100),
                                       starting_state=[0.8 * N(0), 0.15 * N(0), 0.05 * N(0), 0],
                                       seed=42)
    return Base, Complex


def test_fitters():
    """Base fitting test"""
    pass  # no fitters to test
