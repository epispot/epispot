"""
Borrowed from epispot/covid-19 on GitHub
See: https://www.github.com/epispot/covid-19
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
repodir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, repodir)

import epispot as epi
import numpy as np
from copy import deepcopy


def build_model(params):

    """
    Builds a new epispot model and returns results.
    Used for parameter fitting.
    R_0 values: Divided into 10 periods (each 25.6 days long)
    """

    R_0_values = params[:10]
    initial_infecteds = params[10]
    initial_recovered = params[11]

    # Parameter Definitions

    def N(t):
        return 883305

    def R_0(t):
        return R_0_values[int(min(np.floor(t / 25.6), 9))]

    def gamma(t):
        return 1 / 8.89375

    def p_rec(t):
        return 0.6525

    def rec_rate(t):
        return 1 / 23

    def p_hos(t):
        return 0.3475

    def hos_rate(t):
        return 1 / 15

    def hos_stay(t):
        return 1 / 20

    def p_hos_to_rec(t):
        return 1.0

    # Model Build
    """
           ___________
          |           |
    S --> I --> H --> R
    """

    Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
    Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_rec, recovery_rate=rec_rate,
                                  p_hospitalized=p_hos, hospital_rate=hos_rate)
    Hospitalized = epi.comps.Hospitalized(2, hos_rate, p_hos, recovery_rate=hos_stay, p_recovery=p_hos_to_rec)
    Recovered = epi.comps.Recovered(3, p_from_inf=p_rec, from_inf_rate=rec_rate, p_from_hos=p_hos_to_rec,
                                    from_hos_rate=hos_stay)

    # Model Compiler
    Compiled_Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Hospitalized, Recovered],
                     layer_names=['Susceptible', 'Infected', 'Hospitalized', 'Recovered'],
                     layer_map=[[Infected], [Hospitalized, Recovered], [Recovered], []])

    # Model Output
    initial_vector = [883305 - 12 - initial_infecteds - initial_recovered, initial_infecteds, 12, initial_recovered]
    result = Compiled_Model.integrate(range(0, 256), starting_state=initial_vector)

    formatted = []
    for system in result:
        formatted.append([deepcopy(system)[2]])

    return formatted


def compile_model(params):

    """
    Builds a new epispot model and returns results.
    Used for parameter fitting.
    R_0 values: Divided into 10 periods (each 25.6 days long)
    """

    R_0_values = params[:10]
    initial_infecteds = params[10]
    initial_recovered = params[11]

    # Parameter Definitions

    def N(t):
        return 883305

    def R_0(t):
        return R_0_values[int(min(np.floor(t / 25.6), 9))]

    def gamma(t):
        return 1 / 8.89375

    def p_rec(t):
        return 0.6525

    def rec_rate(t):
        return 1 / 23

    def p_hos(t):
        return 0.3475

    def hos_rate(t):
        return 1 / 15

    def hos_stay(t):
        return 1 / 20

    def p_hos_to_rec(t):
        return 1.0

    # Model Build
    """
           ___________
          |           |
    S --> I --> H --> R
    """

    Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
    Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_rec, recovery_rate=rec_rate,
                                  p_hospitalized=p_hos, hospital_rate=hos_rate)
    Hospitalized = epi.comps.Hospitalized(2, hos_rate, p_hos, recovery_rate=hos_stay, p_recovery=p_hos_to_rec)
    Recovered = epi.comps.Recovered(3, p_from_inf=p_rec, from_inf_rate=rec_rate, p_from_hos=p_hos_to_rec,
                                    from_hos_rate=hos_stay)

    # Model Compiler
    Compiled_Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Hospitalized, Recovered],
                                      layer_names=['Susceptible', 'Infected', 'Hospitalized', 'Recovered'],
                                      layer_map=[[Infected], [Hospitalized, Recovered], [Recovered], []])

    return Compiled_Model


params_to_build = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 36.0, 4.0]
optimized_parameters = epi.fitters.grad_des(build_model, open('tests/CI/data/fit.csv'), params_to_build,
                                            1.0, 23, 883305, range(0, 255, 3))

print('\nOptimization complete. A verbose log of the optimized parameters is shown below.')
print(optimized_parameters)

San_Francisco_Model = compile_model(optimized_parameters)
print('\nModel compiled.')

"""
Important Dates
Model/Data Start Date: 3/23/20
Data End Date: 12/04/20
"""

R_0_values = optimized_parameters[:10]
initial_infecteds = optimized_parameters[10]
initial_recovered = optimized_parameters[11]

model_plot = San_Francisco_Model.integrate(range(0, 256),
starting_state=[883305 - 12 - initial_infecteds - initial_recovered, initial_infecteds, 12, initial_recovered])

cases = []  # from the model 'infected' category
pred_hos = []  # to test against actual hospitalized

for system in model_plot:

    cases.append(deepcopy(system)[1])
    pred_hos.append(deepcopy(system)[2])

actual_hos = []
hos_file = open('tests/CI/data/fit.csv', 'r').readlines()

for line in hos_file:
    actual_hos.append(float(line))

range_container = [[range(0, 257), actual_hos, 'Actual Hospitalizations'],
                   [range(0, 256), pred_hos, 'Predicted Hospitalizations'], [range(0, 256), cases, 'Predicted Cases']]
markup = [['line', [1897, 0, 146, 'Hospital Capacity']], ['highlighted-box', [122, 135, 0.5, 1]],
['point', [' Triage Required', 122, 1897]], ['arrow', [1, 10, 250, 100]]]
epi.plots.compare(range_container, 'San Francisco Predictions', 'From Hospitalization Data', markers=markup, seed=100)
print('Test complete: Build passing.')
