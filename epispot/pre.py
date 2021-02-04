"""
The 'pre-compiled' module contains already compiled models which can be put to use immediately.
Each function returns an epispot Model object and its corresponding functions. Models parameters can still be changed
even after compilation.
STRUCTURE:
    - SIR()
"""

from . import comps
from . import models


def SIR(R_0, gamma, N, p_recovery, recovery_rate):
    """
    The well-known SIR Model; a staple of epidemiology and the most basic tool for modeling infectious diseases\
    Susceptible --> Infected --> Removed <br><br>

    R_0: the basic reproductive number--
         this is the average number of susceptibles infected by one infected\
         implemented as a function R_0(t):
            - t: time
            - return: R_0 value
    gamma: the infectious period--
           1 / average duration of infectious period\
           implemented as a function gamma(t):
            - t: time
            - return: infectious period
    N: the total population\
       implemented as a function N(t):
            - t: time
            - return: total population
    p_recovery: probability of recovery
                (only applicable if next layer is Recovered)\
                implemented as a function p_recovery(t):
                    - t: time
                    - return: probability of recovery
    recovery_rate: the recovery rate--different from the standard recovery rate `gamma`
                   measures only 1 / the time it takes to move to the Recovered layer
                   (only applicable if next layer is Recovered)\
                   implemented as a function recovery_rate(t):
                        - t: time
                        - return: recovery rate
    """

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
