import epispot as epi  # load the epi-spot package


# variables (used when defining layers)


# basic reproductive number
def R_0(t):
    # we use a simple logistic function to model R_0 in this example
    return 2 - (2 / (1 + 2 ** (-t + 60)))  # these functions can be time-dependent


# all other variables are not time dependent (this is not required)


# recovery rate
def gamma(t):
    return 0.2


# total population
def N(t):
    return 1e+5


# probability of recovering
def p_recovery(t):
    return 1.0


# layers
Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)  # Susceptible layer
Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_recovery, recovery_rate=gamma)  # Infected layer
Recovered = epi.comps.Recovered(2, p_from_inf=p_recovery, from_inf_rate=gamma)  # Recovered layer

# the blank array in `layer_map` symbolizes that the Recovered layer has no further layers
Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Recovered], layer_names=['Susceptible', 'Infected',
                                                                                       'Recovered'],
                         layer_map=[[Infected],
                                    [Recovered], []])  # compile the model out of the layers defined above

# the `plot_comp_nums` method automatically integrates the model and plots the result
epi.plots.plot_comp_nums(Model, range(0, 150, 1), seed=12)
