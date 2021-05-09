"""
Test of all simple SIR-related models and variants
|- GLOBALS
   |- R_0
   |- N
   |- place
   |- gamma
   |- delta
   |- alpha
   |- p_inf_to_hos
   |- p_hos_to_rec
|- TESTS
   |- SIR
   |- SEIR
   |- SIRD
   |- SIHRD
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


def alpha(t):
    """Alpha--uphill spike"""
    if t < 30:
        return 0.05
    elif t < 60:
        return 0.1
    else:
        return 0.05


def p_inf_to_hos(t):
    """Infected --> Hospitalized probability--constant"""
    return 0.07


def p_hos_to_rec(t):
    """Hospitalized --> Recovered probability--opposite of alpha"""
    if t < 30:
        return 0.95
    elif t < 60:
        return 0.9
    else:
        return 0.95


# TESTS
def test_SIR():
    """SIR Pre-Compiled Model Test"""
    Model = epi.pre.SIR(R_0, N, place, gamma)
    Solution = Model.integrate(range(0, 100))
    return Solution


def test_SEIR():
    """SEIR Pre-Compiled Model Test"""
    Model = epi.pre.SEIR(R_0, N, place, gamma, delta)
    Solution = Model.integrate(range(0, 100))
    return Solution


def test_SIRD():
    """SIRD Pre-Compiled Model Test"""
    Model = epi.pre.SIRD(R_0, N, place, gamma, alpha, place)
    Solution = Model.integrate(range(0, 100))
    return Solution


def test_SIHRD():
    """SIHRD Pre-Compiled Model Test"""
    Model = epi.pre.SIHRD(R_0, N, place, gamma, alpha, place, p_inf_to_hos, place, p_hos_to_rec, place)
    Solution = Model.integrate(range(0, 100))
    return Solution
