"""
This module (short for 'pre-compiled') contains models that have already been compiled and can be put to use immediately.
Each function returns an `epispot.models.Model` object and its corresponding methods.
Model parameters can still be changed even after compilation, but this will require recompilation which can be performed with:

```python
Model.compile(custom=False)
# if adding custom compartments:
Model.compile(custom=True)
```
"""

from . import comps, models, np


def sir(r_0, gamma, n):
    """
    The well-known
    [SIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model);
    a staple of epidemiology and the most basic tool for modeling
    infectious diseases.

    Susceptible → Infected → Removed

    ## Parameters

    `r_0 (float|func(t: float)->float)`: The
        [basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number),
        indicating how infectious a given disease is.
        A value of above 1 indicates a high probability of transmission and thus an increasing infected population.
        A value of 1 indicates a low probability of transmission and thus a constant infected population.
        A value below 1 indicates a low probability of transmission and also a decreasing infected population.

    `gamma (float|func(t: float)->float)`: The total recovery rate of patients.
        This is *not* a measure of how long it takes patients in any given compartment to recover but rather a measure of one divided by the average time of infectiousness.

    `n`: The initial population size; should be the same as that passed into the `epispot.models.Model` class.

    ## Returns

    A `epispot.models.Model` object

    """
    # compile compartments
    susceptible = comps.Susceptible(r_0, gamma, n)
    infected = comps.Infected()
    removed = comps.Removed()

    # compile parameters
    if callable(n):
        n = n(0)
    matrix = np.empty((3, 3), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    matrix[1][2] = (1.0, gamma)  # I => R

    # compile model
    sir_model = models.Model(n)
    sir_model.add(susceptible, [1], matrix[0])
    sir_model.add(infected, [2], matrix[1])
    sir_model.add(removed, [], matrix[2])
    sir_model.compile()

    return sir_model


def seir(r_0, gamma, n, delta):
    """
    An extension on the basic
    [SIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model)
    to include an 'exposed' compartment useful for modeling contact tracing.
    This is known as the
    [SEIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model)
    and is commonly used for diseases that have long incubation periods.

    Susceptible → Exposed → Infected → Removed

    ## Parameters

    `r_0 (float|func(t: float)->float)`: The
        [basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number),
        indicating how infectious a given disease is.
        A value of above 1 indicates a high probability of transmission and thus an increasing infected population.
        A value of 1 indicates a low probability of transmission and thus a constant infected population.
        A value below 1 indicates a low probability of transmission and also a decreasing infected population.

    `gamma (float|func(t: float)->float)`: The total recovery rate of patients.
        This is *not* a measure of how long it takes patients in any given compartment to recover but rather a measure of one divided by the average time of infectiousness.

    `n (float|func(t: float)->float)`: The initial population size;
        should be the same as that passed into the `epispot.models.Model` class.

    `delta (float|func(t: float)->float)`: The reciprocal of the incubation period for the disease.
        This is one divided by the time it takes an individual to transition from the `epispot.comps.Exposed` compartment to the `epispot.comps.Infected` compartment.

    ## Returns

    An `epispot.models.Model` object

    """
    # compile compartments
    susceptible = comps.Susceptible(r_0, gamma, n)
    exposed = comps.Exposed()
    infected = comps.Infected()
    removed = comps.Removed()

    # compile parameters
    if callable(n):
        n = n(0)
    matrix = np.empty((4, 4), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    matrix[1][2] = (1.0, delta)  # E => I
    matrix[2][3] = (1.0, gamma)  # I => R

    # compile model
    seir_model = models.Model(n)
    seir_model.add(susceptible, [1], matrix[0])
    seir_model.add(exposed, [2], matrix[1])
    seir_model.add(infected, [3], matrix[2])
    seir_model.add(removed, [], matrix[3])
    seir_model.compile()

    return seir_model


def sird(r_0, gamma, n, alpha, rho=1.0):
    """
    An addition to the
    [SIR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model),
    which separates the `epispot.comps.Removed` compartment into the `epispot.comps.Recovered` compartment and the `epispot.comps.Dead` compartment.

    Susceptible → Infected → Recovered, Dead

    ## Parameters

    `r_0 (float|func(t: float)->float)`: The
        [basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number),
        indicating how infectious a given disease is.
        A value of above 1 indicates a high probability of transmission and thus an increasing infected population.
        A value of 1 indicates a low probability of transmission and thus a constant infected population.
        A value below 1 indicates a low probability of transmission and also a decreasing infected population.

    `gamma (float|func(t: float)->float)`: The total recovery rate of patients.
        This is *not* a measure of how long it takes patients in any given compartment to recover but rather a measure of one divided by the average time of infectiousness.

    `n (float|func(t: float)->float)`: The initial population size;
        should be the same as that passed into the `epispot.models.Model` class.

    `alpha (float|func(t: float)->float)`: The probability of death
        (often referred to as—but not to be confused with—the 'death rate')
        for a certain disease.
        This is the percentage of individuals that are infected with the disease that will die.

    `rho=1.0 (float|func(t: float)->float)`: The reciprocal of the average time before death.
        This is the real 'death *rate*' of the disease, which represents the *time* of death rather than its probability.

    ## Returns

    A `epispot.models.Model` object

    """
    # compile compartments
    susceptible = comps.Susceptible(r_0, gamma, n)
    infected = comps.Infected()
    recovered = comps.Recovered()
    dead = comps.Dead()

    # compile parameters
    if callable(n):
        n = n(0)
    matrix = np.empty((4, 4), dtype=tuple)
    matrix.fill((1.0, 1.0))  # default probability and rate
    recovery_rate = (gamma - alpha * rho) / (1 - alpha)
    matrix[1][2] = (1.0 - alpha, recovery_rate)  # I => R
    matrix[1][3] = (alpha, rho)  # I => D

    # compile model
    sir_model = models.Model(n)
    sir_model.add(susceptible, [1], matrix[0])
    sir_model.add(infected, [2, 3], matrix[1])
    sir_model.add(recovered, [], matrix[2])
    sir_model.add(dead, [], matrix[3])
    sir_model.compile()

    return sir_model
