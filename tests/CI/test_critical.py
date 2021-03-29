import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
repodir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, repodir)

import epispot as epi


def R_0(t):
    return 10 * 2.718 ** ((- 1 / 500) * (t - 30) ** 2)


def N(t):
    return 1e5 + 10 * t


def p_rec(t):
    return 0.2


def rec_rate(t):
    return 1 / 7


def gamma(t):
    return p_rec(t) * rec_rate(t)


def hos_rate(t):
    return 1


def p_hos(t):
    return 0.5


def cri_rate(t):
    return 1


def p_cri(t):
    return 0.5


def rec_rate_from_hos(t):
    return 1 / 14


def p_rec_from_hos(t):
    return 0.5


def rec_rate_from_cri(t):
    return 1 / 21


def p_rec_from_cri(t):
    return 1.0


def cap(t):
    return 1e3


# compile compartments
Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_rec, recovery_rate=rec_rate)
Hospitalized = epi.comps.Hospitalized(2, hos_rate=hos_rate, p_hos=p_hos, cri_rate=cri_rate, p_cri=p_cri,
                                      recovery_rate=rec_rate_from_hos, p_recovery=p_rec_from_hos, maxCap=cap,
                                      dump_to_layer=4)
Critical = epi.comps.Critical(3, p_from_hos=p_cri, from_hos_rate=cri_rate, recovery_rate=rec_rate_from_cri,
                              p_recovery=p_rec_from_cri)
Removed = epi.comps.Recovered(4, p_from_inf=p_rec, from_inf_rate=rec_rate, p_from_hos=p_rec_from_hos,
                              from_hos_rate=rec_rate_from_hos, p_from_cri=p_rec_from_cri,
                              from_cri_rate=rec_rate_from_cri)

# compile model
Critical_Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Hospitalized, Critical, Removed],
                                  layer_names=['Susceptible', 'Infected', 'Hospitalized', 'Critical', 'Removed'],
                                  layer_map=[[Infected], [Hospitalized, Removed], [Critical, Removed], [Removed], []])

epi.plots.plot_comp_nums(Critical_Model, range(0, 120))
print('Test complete: Build passing.')
