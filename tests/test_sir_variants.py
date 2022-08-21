"""
Test of all simple SIR-related models and variants.
Does not use any functions as parameters or otherwise special
parameters. This test is meant for *basic* code coverage. For advanced
coverage, use the test_advanced.py check.

STRUCTURE:
├ SIR
├ SEIR
└ SIRD
"""

import numpy as np

import epispot as epi


# TESTS
def test_sir():
    """SIR Pre-Compiled Model Test"""
    sir = epi.pre.sir(2.5, 1 / 2, 1e6)
    solution = sir.integrate(range(100))
    predicted = np.around(solution[99], -2)
    assert np.allclose(predicted, np.array([70900, 0, 929100]))

def test_seir():
    """SEIR Pre-Compiled Model Test"""
    seir = epi.pre.seir(2.5, 1 / 2, 1e6, 1 / 2)
    solution = seir.integrate(range(100))
    predicted = np.around(solution[99], -2)
    assert np.allclose(predicted, np.array([90300, 0, 0, 909700]))

def test_sird():
    """SIRD Pre-Compiled Model Test"""
    sird = epi.pre.sird(2.5, 1 / 2, 1e6, 1 / 3, rho=3 / 4)
    solution = sird.integrate(range(100))
    predicted = np.around(solution[99], -2)
    assert np.allclose(predicted, np.array([70900, 0, 464600, 464600]))
