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
    return 0.5


def p_hospitalization(t):
    return 0.5


def delta(t):
    return 0.25


def alpha(t):
    return 0.5


# layers
Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)  # Susceptible layer
Exposed = epi.comps.Exposed(1, R_0, gamma, N, delta)
Infected = epi.comps.Infected(2, N, delta=delta, p_recovery=p_recovery, recovery_rate=gamma,
                              p_hospitalized=p_hospitalization,
                              hospital_rate=gamma)  # Infected layer
Hospitalized = epi.comps.Hospitalized(3, p_hos=p_hospitalization, hos_rate=gamma,
                                      p_recovery=p_recovery, recovery_rate=gamma, rho=gamma, alpha=alpha)
Recovered = epi.comps.Recovered(4, p_from_inf=p_recovery, from_inf_rate=gamma, p_from_hos=p_recovery,
                                from_hos_rate=gamma)  # Recovered layer
Dead = epi.comps.Dead(5, rho_hos=gamma, alpha_hos=alpha)  # Recovered layer

# the blank array in `layer_map` symbolizes that the Recovered layer has no further layers
Model = epi.models.Model(N(0), layers=[Susceptible, Exposed, Infected, Hospitalized, Recovered, Dead],
                         layer_names=['Susceptible', 'Exposed', 'Infected', 'Hospitalized', 'Recovered',
                                      'Dead'],
                         layer_map=[[Exposed], [Infected], [Recovered, Hospitalized], [Dead, Recovered], [],
                                    []])

# the `plot_comp_nums` method automatically integrates the model and plots the result
epi.plots.plot_comp_nums(Model, range(0, 100, 1), starting_state=[98000, 667, 1334, 0, 0, 0], seed=666)
print('stability: passing')
