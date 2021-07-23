"""
This module (short for 'pre-compiled') contains models that have 
already been compiled and can be put to use immediately. Each function 
returns an `epispot.models.Model` object and its corresponding methods. 
Model parameters can still be changed even after compilation, but this 
will require recompilation which can be performed with:

```python
Model.compile(custom=False)
# if adding custom compartments: 
Model.compile(custom=True)
```
"""

from . import comps
from . import models
from . import np


def SIR(R_0, gamma, N):
    """
    The well-known 
    [SIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model); 
    a staple of epidemiology and the most basic tool for modeling 
    infectious diseases.

    Susceptible → Infected → Removed

    ## **Parameters**

    `R_0`: The 
           [basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number), 
           indicating how infectious a given disease is. A value of 
           above 1 indicates a high probability of transmission and 
           thus an increasing infected population. A value of 1 
           indicates a low probability of transmission and thus a 
           constant infected population. A value below 1 indicates 
           a low probability of transmission and also a decreasing 
           infected population.

    `gamma`: The total recovery rate of patients. This is **not** a 
             measure of how long it takes patients in any given 
             compartment to recover but rather a measure of one 
             divided by the average time of infectiousness.

    `N`: The initial population size; should be the same as that 
         passed into the `epispot.models.Model` class.

    ## **Returns**

    An `epispot.models.Model` object

    """
    # compile compartments
    Susceptible = comps.Susceptible(R_0, gamma, N)
    Infected = comps.Infected()
    Removed = comps.Removed()

    # compile parameters
    if callable(N):
        N = N(0)
    matrix = np.empty((3, 3), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    matrix[1][2] = (1.0, gamma)  # I => R

    # compile model
    SIR_Model = models.Model(N)
    SIR_Model.add(Susceptible, [1], matrix[0])
    SIR_Model.add(Infected, [2], matrix[1])
    SIR_Model.add(Removed, [], matrix[2])
    SIR_Model.compile()

    return SIR_Model


def SEIR(R_0, gamma, N, delta):
    """
    An extension on the basic 
    [SIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model)
    to include an 'exposed' compartment useful for modeling contact 
    tracing. This is known as the 
    [SEIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model) 
    and is commonly used for diseases that have long incubation periods.

    Susceptible → Exposed → Infected → Removed

    ## **Parameters**

    `R_0`: The 
           [basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number), 
           indicating how infectious a given disease is. A value of 
           above 1 indicates a high probability of transmission and 
           thus an increasing infected population. A value of 1 
           indicates a low probability of transmission and thus a 
           constant infected population. A value below 1 indicates 
           a low probability of transmission and also a decreasing 
           infected population.

    `gamma`: The total recovery rate of patients. This is **not** a 
             measure of how long it takes patients in any given 
             compartment to recover but rather a measure of one 
             divided by the average time of infectiousness.

    `N`: The initial population size; should be the same as that 
         passed into the `epispot.models.Model` class.

    `delta`: The reciprocal of the incubation period for the disease. 
             This is one divided by the time it takes an individual to 
             transition from the `epispot.comps.Exposed` compartment to 
             the `epispot.comps.Infected` compartment.

    ## **Returns**

    An `epispot.models.Model` object

    """
    # compile compartments
    Susceptible = comps.Susceptible(R_0, gamma, N)
    Exposed = comps.Exposed()
    Infected = comps.Infected()
    Removed = comps.Removed()

    # compile parameters
    if callable(N):
        N = N(0)
    matrix = np.empty((4, 4), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    matrix[1][2] = (1.0, delta)  # E => I
    matrix[2][3] = (1.0, gamma)  # I => R

    # compile model
    SEIR_Model = models.Model(N)
    SEIR_Model.add(Susceptible, [1], matrix[0])
    SEIR_Model.add(Exposed, [2], matrix[1])
    SEIR_Model.add(Infected, [3], matrix[2])
    SEIR_Model.add(Removed, [], matrix[3])
    SEIR_Model.compile()

    return SEIR_Model


def SIRD(R_0, gamma, N, alpha, rho=1.0):
    """
    An addition to the 
    [SIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model); 
    which separates the `epispot.comps.Removed` compartment into the 
    `epispot.comps.Recovered` compartment and the `epispot.comps.Dead` 
    compartment.

    Susceptible → Infected → Recovered, Dead

    ## **Parameters**

    `R_0`: The 
           [basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number), 
           indicating how infectious a given disease is. A value of 
           above 1 indicates a high probability of transmission and 
           thus an increasing infected population. A value of 1 
           indicates a low probability of transmission and thus a 
           constant infected population. A value below 1 indicates 
           a low probability of transmission and also a decreasing 
           infected population.

    `gamma`: The total recovery rate of patients. This is **not** a 
             measure of how long it takes patients in any given 
             compartment to recover but rather a measure of one 
             divided by the average time of infectiousness.

    `N`: The initial population size; should be the same as that 
         passed into the `epispot.models.Model` class.

    `alpha`: The probability of death (often referred to as—but not to 
             be confused with—the 'death rate') for a certain disease.
             This is the percentage of individuals that are infected 
             with the disease that will die.

    `rho=1.0`: The reciprocal of the average time before death. This is 
               the real 'death *rate*' of the disease, which represents 
               the *time* of death rather than its probability.

    ## **Returns**

    An `epispot.models.Model` object

    """
    # compile compartments
    Susceptible = comps.Susceptible(R_0, gamma, N)
    Infected = comps.Infected()
    Recovered = comps.Recovered()
    Dead = comps.Dead()

    # compile parameters
    if callable(N):
        N = N(0)
    matrix = np.empty((4, 4), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    recovery_rate = (gamma - alpha * rho) / (1 - alpha) 
    matrix[1][2] = (1.0 - alpha, recovery_rate)  # I => R
    matrix[1][3] = (alpha, rho)  # I => D

    # compile model
    SIR_Model = models.Model(N)
    SIR_Model.add(Susceptible, [1], matrix[0])
    SIR_Model.add(Infected, [2, 3], matrix[1])
    SIR_Model.add(Recovered, [], matrix[2])
    SIR_Model.add(Dead, [], matrix[3])
    SIR_Model.compile()

    return SIR_Model
