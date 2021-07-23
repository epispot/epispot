"""
Test of advanced modeling techniques with epispot
(i.e. those *not* implemented in the `pre` module)

STRUCTURE:
├ GLOBALS
    ├ E
    ├ R_0
    └ gamma
└ TESTS
    ├ SIRS
    └ SIHCR
"""

import numpy as np
import epispot as epi


# GLOBALS
ConstE = 2.718  # for Gaussian distributions as parameter values

def R_0(t):
    """R Naught--shifted Gaussian distribution"""
    return 5 * ConstE ** ((- 1 / 500) * (t - 30) ** 2)

def gamma(t):
    """Gamma--Gaussian distribution decay from 1/4 to 1/8"""
    return (1 / 8) + (1 / 8) * (ConstE ** ((-1 / 1000) * (t ** 2)))


# TESTS
def test_SIRS():
    """
    Recurrent SIR Model:
    Susceptible → Infected → Removed → Susceptible
    
    """
    # params
    N = 1e6

    # compile compartments
    Susceptible = epi.comps.Susceptible(R_0, gamma, N)
    Infected = epi.comps.Infected()
    Removed = epi.comps.Removed()

    # compile parameters
    matrix = np.empty((3, 3), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    matrix[1][2] = (1.0, gamma)     # I => R
    matrix[2][0] = (0.5, 1.0)       # R => S

    # compile model
    SIRS_Model = epi.models.Model(N)
    SIRS_Model.add(Susceptible, [1], matrix[0])
    SIRS_Model.add(Infected, [2], matrix[1])
    SIRS_Model.add(Removed, [0], matrix[2])
    SIRS_Model.compile()

    # get solutions
    Solution = SIRS_Model.integrate(range(100), starting_state=
                                                np.array([N - 10, 10, 0]))
    return Solution

def test_SIHCR():
    """
    Critical compartment test (without triage*):
    
    Susceptible → Infected → Removed
    Infected → Hospitalized → Removed
    Hospitalized → Critical → Removed

    *triage support is still in beta so tests are not fully complete

    """
    # params
    N = 1e6

    # compile compartments
    Susceptible = epi.comps.Susceptible(R_0, gamma, N)
    Infected = epi.comps.Infected()
    Hospitalized = epi.comps.Hospitalized()
    Critical = epi.comps.Critical()
    Removed = epi.comps.Removed()

    # compile parameters
    matrix = np.empty((5, 5), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate

    matrix[1][4] = (0.5, gamma)                     # I => R
    matrix[1][2] = (0.5, lambda t: gamma(t) / 2)    # I => H
    matrix[2][4] = (0.5, gamma)                     # H => R
    matrix[2][3] = (0.5, lambda t: gamma(t) / 2)    # H => C
    matrix[3][4] = (1.0, gamma)                     # C => R

    # compile model
    SIHCR_Model = epi.models.Model(N)
    SIHCR_Model.add(Susceptible, [1], matrix[0])
    SIHCR_Model.add(Infected, [2, 4], matrix[1])
    SIHCR_Model.add(Hospitalized, [3, 4], matrix[2])
    SIHCR_Model.add(Critical, [4], matrix[3])
    SIHCR_Model.add(Removed, [], matrix[4])
    SIHCR_Model.compile()

    # get solutions
    Solution = SIHCR_Model.integrate(range(100), starting_state=
                                     np.array([N - 10, 10, 0, 0, 0]))
    return Solution
