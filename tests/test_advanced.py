"""
Test of advanced modeling techniques with epispot
(i.e. those *not* implemented in the `pre` module)

STRUCTURE:
├ GLOBALS
    ├ E
    ├ r_0
    └ gamma
└ TESTS
    ├ SIRS
    └ SIHCR
"""

import numpy as np

import epispot as epi

# GLOBALS
r_0 = epi.params.RNaught(type='bell')
gamma = epi.params.Gamma(r_0=r_0, beta=2.5)


# TESTS
def test_sirs():
    """
    Recurrent SIR Model:
    Susceptible → Infected → Removed → Susceptible

    """
    # params
    n = 1e6

    # compile compartments
    susceptible = epi.comps.Susceptible(r_0, gamma, n)
    infected = epi.comps.Infected()
    removed = epi.comps.Removed()

    # compile parameters
    matrix = np.empty((3, 3), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    matrix[1][2] = (1.0, gamma)     # I => R
    matrix[2][0] = (0.5, 1.0)       # R => S

    # compile model
    sirs_model = epi.models.Model(n)
    sirs_model.add(susceptible, [1], matrix[0])
    sirs_model.add(infected, [2], matrix[1])
    sirs_model.add(removed, [0], matrix[2])
    sirs_model.compile()

    # get solutions
    solution = sirs_model.integrate(
        range(100), starting_state=np.array([n - 10, 10, 0])
    )
    predicted = np.around(solution[99], -2)
    assert np.allclose(predicted, np.array([400000, 200000, 400000]))

def test_sihcr():
    """
    Critical compartment test (without triage*):

    Susceptible → Infected → Removed
    Infected → Hospitalized → Removed
    Hospitalized → Critical → Removed

    *triage support is still in beta so tests are not fully complete

    """
    # params
    n = 1e6

    # compile compartments
    susceptible = epi.comps.Susceptible(r_0, gamma, n)
    infected = epi.comps.Infected()
    hospitalized = epi.comps.Hospitalized()
    critical = epi.comps.Critical()
    removed = epi.comps.Removed()

    # compile parameters
    matrix = np.empty((5, 5), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate

    matrix[1][4] = (0.5, gamma)                     # I => R
    matrix[1][2] = (0.5, lambda t: gamma(t) / 2)    # I => H
    matrix[2][4] = (0.5, gamma)                     # H => R
    matrix[2][3] = (0.5, lambda t: gamma(t) / 2)    # H => C
    matrix[3][4] = (1.0, gamma)                     # C => R

    # compile model
    sihcr_model = epi.models.Model(n)
    sihcr_model.add(susceptible, [1], matrix[0])
    sihcr_model.add(infected, [2, 4], matrix[1])
    sihcr_model.add(hospitalized, [3, 4], matrix[2])
    sihcr_model.add(critical, [4], matrix[3])
    sihcr_model.add(removed, [], matrix[4])
    sihcr_model.compile()

    # get solutions
    solution = sihcr_model.integrate(np.linspace(0, 20, 100))
    predicted = np.around(solution[99], -2)
    assert np.allclose(
        predicted,
        np.array([2.115e5, 1.000e2, 1.000e2, 5.000e2, 7.877e5])
    )
