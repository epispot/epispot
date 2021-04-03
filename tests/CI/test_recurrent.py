import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
repodir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, repodir)

import epispot as epi


def R_0(t):
    return 5 * 2.718 ** ((- 1 / 500) * (t - 30) ** 2)


def N(t):
    return 1e5


def p_rec(t):
    return 1.0


def rec_rate(t):
    return 1 / 7


def gamma(t):
    return p_rec(t) * rec_rate(t)


def reinfection(t):
    return 0.5


def reinfection_rate(t):
    return 1 / 7


# compile compartments
Susceptible = epi.comps.Susceptible(0, R_0, gamma, N, p_resusceptibility=reinfection, s_rate=reinfection_rate)
Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_rec, recovery_rate=rec_rate)
Removed = epi.comps.Recovered(2, p_from_inf=p_rec, from_inf_rate=rec_rate, p_resusceptibility=reinfection,
                              s_rate=reinfection_rate)

# compile model
SIR_Model = epi.models.Model(N(0))
SIR_Model.add_layer(Susceptible, 'Susceptible', [Infected])
SIR_Model.add_layer(Infected, 'Infected', [Removed])
SIR_Model.add_layer(Removed, 'Removed', [Susceptible])

epi.plots.plot_comp_nums(SIR_Model, range(0, 180))
print('Test complete: Build passing.')
