"""
The `epispot.models` classes store different types of epidemiological 
models in a compact form useful for integration. Models can be 
differentiated, integrated, and examined by calling class methods. 
Additionally, epispot models are portable—they can be used throughout 
the package to generate plots, run predictions, etc.
"""

from copy import deepcopy
from . import warnings
from . import np


class Model(object):
    """
    The base model class for 
    [compartmental models](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology). 
    Compartmental models are models composed of various sub-models, 
    known as "compartments." For example, the common SIR model is an 
    example of a compartmental model with the Susceptible, Infected, 
    and Removed compartments.

    .. versionadded:: v3.0.0-alpha-2

    """
    def __init__(self, initial_population, comps=None, comp_map=None, 
                 matrix=None):
        """
        Initialize the `Model` class; all optional parameters can be 
        added through the `epispot.models.Model.add` method.

        ## **Parameters**

        `initial_population`: Population at time zero

        `comps=None`: List of compartment classes to create the model

        `comp_map=None`: Map of how all the compartments connect.
                         The map should consist of a list of lists.
                         Each sublist represents the connections of the 
                         corresponding compartment in the `comps` list.
                         This sublist should contain the indices of each 
                         of the compartments in `comps` that it connects to.
                         If the compartment does not connect to any other 
                         compartments, leave the sublist blank.
        
        `matrix=None`: Rate and probability matrix describing the 
                       exchange rates between compartments. Like `map`,
                       this is a list of lists. Unlike `map`, however,
                       this matrix must not skip entries (i.e. no blank
                       sublists). Each sublist should contain rate and 
                       probability information in a tuple for every 
                       compartment. If the information is not 
                       necessary, use the tuple `(1, 1)` or `None` as a
                       placeholder.

        ## **Example**

        Let's say we have three compartments `A`, `B`, and `C`.
        These three compartments connect as shown below:

        ```text
        ┌───────────────────┐
        │                   ▼
        ┌───┐     ┌───┐     ┌───┐
        │ A │ ──▶ │ C │ ──▶ │ B │
        └───┘     └───┘     └───┘
        ```

        To create a compartmental model with these three classes, use:

        ```python
        comps = [A, B, C], 
        map = [
            [1, 2],     # A
            [],         # B
            [1]         # C
        ],
        matrix = [
            [None, (1/2, 1/3), (1/2, 1/3)],     # A[A, B, C] 
            [None, None, None],                 # B[A, B, C]
            [None, (1/2, 1/3), None]            # C[A, B, C]
        ]
        ```

        This creates a compartmental model where all the connections 
        have a probability of `1/2` and rate of `1/3`.
        
        ## **Additional Notes**

        This feature is currently only released to alpha versions of 
        epispot. This will likely be used (with minor changes) in the 
        full release of epispot v3. For more information about this 
        feature, or if you're interested in giving feedback, see the 
        discussion 
        [here on GitHub](https://github.com/epispot/epispot/issues/73).

        .. warning::
           As this is currently an alpha feature, the new compartmental 
           models in epispot are subject to change.

        """
        self.initial_population = initial_population
        self.compartments = comps
        if self.compartments:
            self.names = [comp.name for comp in self.compartments]
        self.map = comp_map
        self.matrix = matrix
        self.aggregated = None
        self.compiled = False

    def compile(self, custom=False):
        """
        Run a series of checks of the model and initialize some 
        class-wide variables.

        ## **Parameters**

        `custom=False`: Flag indicating if the model is using custom
                        compartments. If this is `False` (the default), 
                        all compartment compatibility checks will have 
                        to pass or an error will be raised. If this is 
                        `True`, those checks are bypassed since the 
                        model cannot check for custom compartments.

        ## **Additional Notes**

        Adding, removing, or modifying compartments after this step 
        will automatically de-compile the model, requiring it to be 
        compiled again after changes have been made.

        .. important:: 
           Only run after all the compartments have been
           added to the model.

        """
        if self.compiled:  # pragma: no cover
            warnings.warn("It looks like you're compiling a model more "
                          "than once. For clarity, it is recommended "
                          "that you only compile models once, and then "
                          "again if (and only if) changes have been "
                          "made.")

        # run model checks to ensure that the model is valid
        if not custom:
            for i, compartment in enumerate(self.compartments):
                compartment._check(self.map[i], self.compartments)
        
        # aggregate all compartments by type
        self.aggregated = {}
        for i, compartment in enumerate(self.compartments):
            if compartment.config['type'] not in self.aggregated:
                self.aggregated[compartment.config['type']] = []
            self.aggregated[compartment.config['type']].append(i)

        self.compiled = True

    def diff(self, time, system):
        """
        Differentiate `epispot.models.Model`. Used by 
        `epispot.models.Model.integrate` for evaluating model 
        predictions.

        ## **Parameters**

        `time`: Time to take the derivative at. This is important for 
                some time-dependent variables like compartment 
                parameters.

        `system`: System of state values (e.g `[973, 12, 15]`). This is 
                propagated to each of the individual compartments in 
                the model.

        ## **Return**

        List of corresponding compartment derivatives.
        
        """
        if not self.compiled:  # pragma: no cover
            warnings.warn('An epispot model has not been compiled yet. '
                          'Triggering integration will automatically '
                          'compile the model.')
            self.compile()

        derivative = np.zeros((len(self.compartments), ))
        for num, compartment in enumerate(self.compartments):
            if num in self.aggregated['Susceptible']:
                delta = compartment.diff(time, 
                                         system, 
                                         num,
                                         self.map[num], 
                                         self.matrix[num],
                                         infecteds=
                                         self.aggregated['Infected'])
            else:
                delta = compartment.diff(time, 
                                         system, 
                                         num,
                                         self.map[num], 
                                         self.matrix[num])
            derivative += delta
        
        return derivative

    def integrate(self, timesteps, starting_state=None):
        """
        Integrate the model using `epispot.models.Model.diff` to 
        arrive at future predictions using 
        [Euler's Method](https://en.wikipedia.org/wiki/Euler_method).
        By default, the step size (Δ) is set to exactly 1 day, as this 
        is usually the period for which epidemiological parameters are 
        estimated for. However, in future versions, we plan to update 
        this to add support for variable values of Δ.

        ## **Parameters**

        `timesteps`: range of evenly-spaced times starting at the 
                     epidemic start time and ending at the time of 
                     prediction.
        
        `starting_state=None`: List of initial values for each 
                               compartment. This is used as the initial 
                               vector for the integration process.
                               If no `starting_state` is provided, it 
                               will default to the having only 1 person
                               in the next non-Susceptible compartment.
        
        ## **Return**

        A list of lists. Each sublist is a vector representing the 
        value of each compartment at that specific time. The sublists
        range according to the `timesteps` parameter.

        ## **Example**

        For example, the following would be an expected return type for 
        an SIR model with a population of `100`.

        ```python
        [
            [99, 1, 0],  # S, I, R on day 1
            [98, 2, 0],  # S, I, R on day 2
            [95, 3, 2],  # S, I, R on day 3
            ...,
            [23, 24, 53]  # final prediction
        ]
        ```

        ## **Additional Notes**

        `delta` is expected to be added as an optional parameter in
        future releases of epispot v3. For now, however, it is set 
        to 1 day and cannot be changed.

        """
        # checks to make sure the model has been compiled
        if not self.compiled:  # pragma: no cover
            warnings.warn('An epispot model has not been compiled yet. '
                          'Triggering integration will automatically '
                          'compile the model.')
            self.compile()

        # initial parameter setup
        results = []
        delta = 1

        if starting_state is not None:
            system = starting_state
        else:
            system = np.zeros(len(self.compartments))
            system[0] = self.initial_population - 1
            system[1] = 1

        for timestep in timesteps:

            # calculate the derivative for each compartment at this 
            # timestep and update the system accordingly

            derivatives = self.diff(timestep, system)
            system += delta * derivatives
            results.append(deepcopy(system))

        return results

    def add(self, comp, comp_map, matrix):
        """
        Add a compartment to the model. This can also be done by 
        initializing the `epispot.models.Model` class beforehand.

        ## **Parameters**

        `comp`: Compartment class (e.g. `Susceptible()` or `Infected()`)

        `comp_map`: Slice of the larger `map` specified in 
                    `epispot.models.Model`. This should simply include the 
                    compartment connections for this specific compartment.

        `matrix`: Slice of the larger `matrix` specified in 
                  `epispot.models.Model`. As with `map`, this should 
                  only include the rates and probabilities for this
                  compartment's connections.

        ## **Error Handling**

        Initializing some parameters in `epispot.models.Model` without
        initializing all of them will raise a `ValueError`.

        ## **Additional Notes**

        See the documentation for `epispot.models.Model` for more help
        and examples.

        """
        if self.compiled:
            self.compiled = False

        if (self.compartments, self.map, self.matrix) == (None, None, None):
            self.compartments = [comp]
            self.names = [comp.name]
            self.map = [comp_map]
            self.matrix = [matrix]
        elif self.compartments is not None and self.map is not None and \
             self.matrix is not None:
            self.compartments.append(comp)
            self.names.append(comp.name)
            self.map.append(comp_map)
            self.matrix.append(matrix)
        else:  # pragma: no cover
            raise ValueError('Parameters for `epispot.models.Model` '
                             'have not been specified correctly.\n'
                             'If either `comps`, `map`, or `matrix` '
                             'have been initialized, then *all* '
                             'parameters must be initialized.')

    def rename(self, names):
        """
        Assign names to each compartment in the model.

        ## Parameters

        `names`: A list of names corresponding to `comps`

        """
        self.names = names
        for i, comp in enumerate(self.compartments):
            comp.name = names[i]
