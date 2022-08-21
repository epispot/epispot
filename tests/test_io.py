"""
Test epispot's ability to load and save models:
1. Creates a custom model and saves it to a file.
2. Loads the model from the file and checks that the model is correct.

STRUCTURE:
└ main
"""

from os import mkdir, path

import numpy as np

import epispot as epi


# TESTS
def test_main():
    """SIR Model"""

    # params
    n = 1e6
    r_0 = lambda t: 2.0 + 0.5 * np.sin(t)
    gamma = epi.params.Gamma(r_0=r_0, beta=3)

    # compile compartments
    susceptible = epi.comps.Susceptible(r_0, gamma, n)
    infected = epi.comps.Infected()
    removed = epi.comps.Removed()

    # compile parameters
    matrix = np.empty((3, 3), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    matrix[1][2] = (1.0, gamma)  # I => R

    # compile model
    sir_model = epi.models.Model(n)
    sir_model.add(susceptible, [1], matrix[0])
    sir_model.add(infected, [2], matrix[1])
    sir_model.add(removed, [], matrix[2])
    sir_model.compile()

    # get solutions
    solution = sir_model.integrate(np.linspace(0, 20, 100))
    predicted = solution[99]

    # save model
    if not path.exists('tests/artifacts'):
        mkdir('tests/artifacts')
    sir_model.save('tests/artifacts/SIR_Model.epi')

    # load model
    loaded = epi.models.Model.load('tests/artifacts/SIR_Model.epi')

    # check model
    re_solution = loaded.integrate(np.linspace(0, 20, 100))
    re_predicted = re_solution[99]
    assert np.allclose(predicted, re_predicted)
