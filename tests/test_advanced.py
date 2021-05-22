"""
Test of advanced modeling techniques with epispot
(i.e. those *not* implemented in the `pre` module)
|- GLOBALS
   |- R_0
   |- N
   |- place
   |- gamma
   |- reinfection
   |- hospitalization
   |- cap
   |- critical
|- TESTS
   |- SIRS
   |- SIHCR
"""

import epispot as epi


# GLOBALS
ConstE = 2.718  # for Gaussian distributions as parameter values


def R_0(t):
    """R Naught--shifted Gaussian distribution"""
    return 5 * ConstE ** ((- 1 / 500) * (t - 30) ** 2)


def N(t):
    """Total population--1 million (constant)"""
    return 1e6


def place(t):
    """Placeholder for repetitive probability-rate definitions--returns 1"""
    return 1.0


def gamma(t):
    """Gamma--Gaussian distribution decay from 1/4 to 1/8"""
    return (1 / 8) + (1 / 8) * (ConstE ** ((-1 / 1000) * (t ** 2)))


def reinfection(t):
    """Reinfection rate from recovered--constant"""
    return 1 / 7


def hospitalization(t):
    """Probability of hospitalization--constant"""
    return 0.1


def cap(t):
    """Hospitalization limit--constant"""
    return 1e4


def critical(t):
    """Probability of entering the Critical compartment--constant"""
    return 0.5


# TESTS
def test_SIRS():
    """Recurrent SIRS Model Test (w/ starting state)"""

    # compile compartments
    Susceptible = epi.comps.Susceptible(0, R_0, gamma, N, p_resusceptibility=place, s_rate=reinfection)
    Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=place, recovery_rate=gamma)
    Removed = epi.comps.Recovered(2, p_from_inf=place, from_inf_rate=gamma, p_resusceptibility=place,
                                  s_rate=reinfection)

    # compile model
    SIRS_Model = epi.models.Model(N(0))
    SIRS_Model.add_layer(Susceptible, 'Susceptible', [Infected])
    SIRS_Model.add_layer(Infected, 'Infected', [Removed])
    SIRS_Model.add_layer(Removed, 'Removed', [Susceptible])

    # solve
    Solution = SIRS_Model.integrate(range(100), starting_state=[0.9 * N(0), 0.1 * N(0), 0])
    return Solution


def test_SIHCR():
    """
    Critical compartment test (w/ triage):
    Susceptible --> Infected -----------> Removed
                    |--> Hospitalized --/   /
                         |--> Critical ---/
    """

    # compile compartments
    Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
    Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=place, recovery_rate=gamma,
                                        hospital_rate=place, p_hospitalized=hospitalization)
    Hospitalized = epi.comps.Hospitalized(2, hos_rate=place, p_hos=hospitalization, cri_rate=place, p_cri=critical,
                                             recovery_rate=gamma, p_recovery=place, maxCap=cap,
                                             dump_to_layer=4)
    Critical = epi.comps.Critical(3, p_from_hos=critical, from_hos_rate=place, recovery_rate=gamma,
                                     p_recovery=place, maxCap=cap, dump_to_layer=4)
    Removed = epi.comps.Recovered(4, p_from_inf=place, from_inf_rate=gamma, p_from_hos=place,
                                     from_hos_rate=gamma, p_from_cri=place,
                                     from_cri_rate=gamma)

    # compile model
    SIHCR_Model = epi.models.Model(N(0))
    SIHCR_Model.add_layer(Susceptible, 'Susceptible', [Infected])
    SIHCR_Model.add_layer(Infected, 'Infected', [Removed, Hospitalized])
    SIHCR_Model.add_layer(Hospitalized, 'Hospitalized', [Removed, Critical])
    SIHCR_Model.add_layer(Critical, 'Critical', [Removed])
    SIHCR_Model.add_layer(Removed, 'Removed', [])

    # solve
    Solution = SIHCR_Model.integrate(range(100))
    return Solution
