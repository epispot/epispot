"""
The 'pre-compiled' module contains already compiled models which can be put to use immediately.
Each function returns an epispot Model object and its corresponding functions. Models parameters can still be changed
even after compilation.
STRUCTURE:
- SIR()
- SEIR()
- SIRD()
- SIHRD()
"""

from . import comps
from . import models


def SIR(R_0, N, p_recovery, recovery_rate):
    """
    The well-known SIR Model; a staple of epidemiology and the most basic tool for modeling infectious diseases\
    Susceptible --> Infected --> Removed <br><br>
    R_0: the basic reproductive number--
         this is the average number of susceptibles infected by one infected\
         implemented as a function R_0(t):
            - t: time
            - return: R_0 value
    N: the total population\
       implemented as a function N(t):
            - t: time
            - return: total population
    p_recovery: probability of recovery
                implemented as a function p_recovery(t):
                    - t: time
                    - return: probability of recovery
    recovery_rate: the recovery rate--different from the standard recovery rate `gamma`
                   measures only 1 / the time it takes to move to the Recovered layer\
                   implemented as a function recovery_rate(t):
                        - t: time
                        - return: recovery rate
    """

    def gamma(t):
        return p_recovery(t) * recovery_rate(t)

    # compile compartments
    Susceptible = comps.Susceptible(0, R_0, gamma, N)
    Infected = comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_recovery, recovery_rate=recovery_rate)
    Removed = comps.Recovered(2, p_from_inf=p_recovery, from_inf_rate=recovery_rate)

    # compile model
    SIR_Model = models.Model(N(0))
    SIR_Model.add_layer(Susceptible, 'Susceptible', [Infected])
    SIR_Model.add_layer(Infected, 'Infected', [Removed])
    SIR_Model.add_layer(Removed, 'Removed', [])

    return SIR_Model


def SEIR(R_0, N, p_recovery, recovery_rate, delta):
    """
    The SEIR Model; a variant of the SIR Model that investigates people who have been *exposed* to the virus
    so that they can be tracked down for contact tracing reasons\
    Susceptible --> Exposed --> Infected --> Removed <br><br>
    R_0: the basic reproductive number--
         this is the average number of susceptibles infected by one infected\
         implemented as a function R_0(t):
            - t: time
            - return: R_0 value
    N: the total population\
       implemented as a function N(t):
            - t: time
            - return: total population
    p_recovery: probability of recovery\
                implemented as a function p_recovery(t):
                    - t: time
                    - return: probability of recovery
    recovery_rate: the recovery rate--different from the standard recovery rate `gamma`
                   measures only 1 / the time it takes to move to the Recovered layer\
                   implemented as a function recovery_rate(t):
                        - t: time
                        - return: recovery rate
    delta: =None, the incubation period\
                  implemented as a function delta(t)--in most cases this should stay constant
                    - t: time
                    - return: incubation period
    """

    def gamma(t):
        return p_recovery(t) * recovery_rate(t)

    # compile compartments
    Susceptible = comps.Susceptible(0, R_0, gamma, N)
    Exposed = comps.Exposed(1, R_0, gamma, N, delta)
    Infected = comps.Infected(2, N, delta=delta, p_recovery=p_recovery, recovery_rate=recovery_rate)
    Removed = comps.Recovered(3, p_from_inf=p_recovery, from_inf_rate=recovery_rate)

    # compile model
    SEIR_Model = models.Model(N(0))
    SEIR_Model.add_layer(Susceptible, 'Susceptible', [Exposed])
    SEIR_Model.add_layer(Exposed, 'Exposed', [Infected])
    SEIR_Model.add_layer(Infected, 'Infected', [Removed])
    SEIR_Model.add_layer(Removed, 'Removed', [])

    return SEIR_Model


def SIRD(R_0, N, p_recovery, recovery_rate, alpha, rho):
    """
    The SIRD Model; a tweak on the SIR Model to separate Recovered & Dead compartments
    which allows for death predictions as well as herd immunity predictions\
    Susceptible --> Infected --> Recovered \
                    |----------> Dead <br><br>
    R_0: the basic reproductive number--
         this is the average number of susceptibles infected by one infected\
         implemented as a function R_0(t):
            - t: time
            - return: R_0 value
    N: the total population\
       implemented as a function N(t):
            - t: time
            - return: total population
    p_recovery: probability of recovery\
                implemented as a function p_recovery(t):
                    - t: time
                    - return: probability of recovery
    recovery_rate: the recovery rate--different from the standard recovery rate `gamma`
                   measures only 1 / the time it takes to move to the Recovered layer\
                   implemented as a function recovery_rate(t):
                        - t: time
                        - return: recovery rate
    rho: 1 / time until death\
         implemented as a function rho(t)--in most cases this should stay constant
            - t: time
            - return: death rate
    alpha: probability of death from Infected\
           implemented as a function alpha(t)
            - t: time
            - return: probability of death
    """

    def gamma(t):
        return p_recovery(t) * recovery_rate(t) + alpha(t) * rho(t)

    # compile compartments
    Susceptible = comps.Susceptible(0, R_0, gamma, N)
    Infected = comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_recovery, recovery_rate=recovery_rate,
                              death_rate=rho, p_death=alpha)
    Recovered = comps.Recovered(2, p_from_inf=p_recovery, from_inf_rate=recovery_rate)
    Dead = comps.Dead(3, rho_inf=rho, alpha_inf=alpha)

    # compile model
    SIRD_Model = models.Model(N(0))
    SIRD_Model.add_layer(Susceptible, 'Susceptible', [Infected])
    SIRD_Model.add_layer(Infected, 'Infected', [Recovered, Dead])
    SIRD_Model.add_layer(Recovered, 'Recovered', [])
    SIRD_Model.add_layer(Dead, 'Dead', [])

    return SIRD_Model


def SIHRD(R_0, N, p_recovery, recovery_rate, alpha, rho, p_hos, hos_rate, p_hos_to_rec, hos_to_rec_rate):
    """
    The SIHRD Model; Tracks patients from hospitalized to recovered to dead
    which allows for death, herd immunity, and triage predictions\
    Susceptible --> Infected --> Hospitalized --> Dead \
                    |            |--------------> Recovered \
                    |---------------------------/ <br><br>
    R_0: the basic reproductive number--
         this is the average number of susceptibles infected by one infected\
         implemented as a function R_0(t):
            - t: time
            - return: R_0 value
    N: the total population\
       implemented as a function N(t):
            - t: time
            - return: total population
    p_recovery: probability of recovery from Infected\
                implemented as a function p_recovery(t):
                    - t: time
                    - return: probability of recovery
    recovery_rate: the recovery rate from the Infected layer only
                   implemented as a function recovery_rate(t):
                        - t: time
                        - return: recovery rate
    rho: 1 / time until death\
         implemented as a function rho(t)--in most cases this should stay constant
            - t: time
            - return: death rate
    alpha: probability of death from Infected\
           implemented as a function alpha(t)
            - t: time
            - return: probability of death
    p_hos_to_rec: probability of recovery from Hospitalized\
                implemented as a function p_hos_to_rec(t):
                    - t: time
                    - return: probability of recovery
    hos_to_rec_rate: the recovery rate from the Hospitalized layer only
                   implemented as a function hos_to_rec_rate(t):
                        - t: time
                        - return: recovery rate
    """

    def gamma(t):
        return p_recovery(t) * recovery_rate(t) + p_hos(t) * hos_rate(t)

    # compile compartments
    Susceptible = comps.Susceptible(0, R_0, gamma, N)
    Infected = comps.Infected(1, N, R_0=R_0, gamma=gamma, hospital_rate=hos_rate, p_hospitalized=p_hos,
                              recovery_rate=recovery_rate, p_recovery=p_recovery)
    Hospitalized = comps.Hospitalized(2, hos_rate=hos_rate, p_hos=p_hos, p_recovery=p_hos_to_rec,
                                      recovery_rate=hos_to_rec_rate, rho=rho, alpha=alpha)
    Recovered = comps.Recovered(3, p_from_hos=p_hos_to_rec, from_hos_rate=hos_to_rec_rate,
                                p_from_inf=p_recovery, from_inf_rate=recovery_rate)
    Dead = comps.Dead(4, rho_hos=rho, alpha_hos=alpha)

    # compile model
    SIHRD_Model = models.Model(N(0))
    SIHRD_Model.add_layer(Susceptible, 'Susceptible', [Infected])
    SIHRD_Model.add_layer(Infected, 'Infected', [Hospitalized])
    SIHRD_Model.add_layer(Hospitalized, 'Hospitalized', [Recovered, Dead])
    SIHRD_Model.add_layer(Recovered, 'Recovered', [])
    SIHRD_Model.add_layer(Dead, 'Dead', [])

    return SIHRD_Model
