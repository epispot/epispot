import epispot as epi


def R_0(t):
    return 2.0


def gamma(t):
    return 0.2


def N(t):
    return 1e+5


def p_recovery(t):
    return 1.0


def p_from_inf(t):
    return 1.0


Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_recovery, recovery_rate=gamma)
Recovered = epi.comps.Recovered(2, p_from_inf=p_from_inf, from_inf_rate=gamma)

Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Recovered], layer_names=['Susceptible', 'Infected',
                                                                                       'Recovered'],
                         layer_map=[[Infected],
                                    [Recovered], []])

epi.plots.plot_comp_nums(Model, range(0, 150, 1))
