"""
The `epispot.models` classes store different types of epidemiological
models in a compact form useful for integration. Models can be
differentiated, integrated, and examined by calling class methods.
Additionally, epispot models are portable—they can be used throughout
the package to generate plots, run predictions, etc.
"""

from copy import deepcopy

from . import dill, np, version, warnings


class Model:
    """
    The base model class for
    [compartmental models](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology).
    Compartmental models are models composed of various sub-models,
    known as "compartments."
    For example, the common SIR model is an example of a compartmental model with the Susceptible,
    Infected, and Removed compartments.

    .. versionadded:: v3.0.0-alpha-2
    """

    def __init__(self, initial_population, comps=None, comp_map=None,
                 matrix=None):
        """
        Initialize the `Model` class; all optional parameters can be added through the `epispot.models.Model.add` method.

        ## Parameters

        `initial_population (int)`: Population at time zero

        `comps=None (|list[epispot.comps.Compartment])`: List of compartment classes to create the model

        `comp_map=None (|list[list[int]])`: Map of how all the compartments connect.
            The map should consist of a list of lists.
            Each sublist represents the connections of the corresponding compartment in the `comps` list.
            This sublist should contain the indices of each of the compartments in `comps` that it connects to.
            If the compartment does not connect to any other compartments,
            leave the sublist blank.

        `matrix=None (|list[list[tuple(float|func(t: float)->float, float|func(t: float)->float)]])`:
            Rate and probability matrix describing the exchange rates between compartments.
            Like `map`, this is a list of lists.
            Unlike `map`, however, this matrix must not skip entries
            (i.e. no blank sublists).
            Each sublist should contain rate and probability information
            in a tuple for every compartment.
            If the information is not necessary, use the tuple `(1, 1)`
            as a placeholder.

        ## Example

        Let's say we have three compartments `A`, `B`, and `C`.
        These three compartments connect as shown below:

            ┌─────────────────────┐
            │                     ▼
            ┌───┐     ┌───┐     ┌───┐
            │ A │ ──> │ C │ ──> │ B │
            └───┘     └───┘     └───┘

        To create a compartmental model with these three classes, use:

        ```python
        comps = [A, B, C],
        map = [
            [1, 2],     # A
            [],         # B
            [1]         # C
        ],
        matrix = [
            [(1, 1), (1/2, 1/3), (1/2, 1/3)],     # A[A, B, C]
            [(1, 1), (1, 1), (1, 1)],                 # B[A, B, C]
            [(1, 1), (1/2, 1/3), (1, 1)]            # C[A, B, C]
        ]
        ```

        This creates a compartmental model where all the connections
        have a probability of `1/2` and rate of `1/3`.

        ## **Additional Notes**

        For more information about this
        feature, or if you're interested in giving feedback, see the
        discussion
        [here on GitHub](https://github.com/epispot/epispot/issues/73).

        ..versionadded:: v3.0.0-alpha-2

        """
        self.initial_population = initial_population
        self.compartments = comps
        if self.compartments:
            self.names = [comp.name for comp in self.compartments]
        self.map = comp_map
        self.matrix = matrix
        self.aggregated = None
        self.compiled = False
        self.version = version

    def compile(self, custom=False):
        """
        Run a series of checks of the model and initialize some class-wide variables.

        ## Parameters

        `custom=False (bool)`: Flag indicating if the model is using custom compartments.
            If this is `False` (the default), all compartment compatibility checks will have to pass or an error will be raised.
            If this is `True`, those checks are bypassed since the model cannot check for custom compartments.

        ## Additional Notes

        Adding, removing, or modifying compartments after this step will automatically de-compile the model,
        requiring it to be compiled again after changes have been made.

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
        Differentiate `epispot.models.Model`; used by `epispot.models.Model.integrate` for evaluating model predictions.

        ## Parameters

        `time (float)`: Time to take the derivative at.
            This is important for some time-dependent variables like compartment parameters.

        `system (list[float])`: System of state values (e.g `[973, 12, 15]`).
            This is propagated to each of the individual compartments in the model.

        ## Returns

        List of corresponding compartment derivatives (`list[float]`)

        """
        if not self.compiled:  # pragma: no cover
            warnings.warn('An epispot model has not been compiled yet. '
                          'Triggering integration will automatically '
                          'compile the model.')
            self.compile()

        derivative = np.zeros((len(self.compartments), ))
        for num, compartment in enumerate(self.compartments):
            if num in self.aggregated['Susceptible']:
                delta = compartment.diff(
                    time, system, num,
                    self.map[num], self.matrix[num],
                    infecteds=self.aggregated['Infected']
                )
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
        Integrate the model using `epispot.models.Model.diff` to arrive at future predictions using
        [Euler's Method](https://en.wikipedia.org/wiki/Euler_method).
        By default, the step size (Δ) is set to exactly 1 day, as this is usually the period for which epidemiological parameters are estimated for.
        However, this can be changed if necessary.

        ## Parameters

        `timesteps (range)`: range of evenly-spaced times starting at the epidemic start time and ending at the time of prediction.

        `starting_state=None (|list[int])`: List of initial values for each compartment.
            This is used as the initial vector for the integration process.
            If no `starting_state` is provided, it will default to the having only 1 person in the next non-Susceptible compartment.

        `delta=1 (|float)`: Δ, the step size for the integration process.
            Smaller values will result in more accurate predictions,
            but will be more costly.

        ## Returns

        A list of lists; each sublist is a vector representing the value of each compartment at that specific time.
        The sublists range according to the `timesteps` parameter.
        (`list[list[float]]`)

        ## Example

        For example, the following would be an expected return type for
        an SIR model with a population of `100`:

        ```python
        [
            [99, 1, 0],  # S, I, R on day 1
            [98, 2, 0],  # S, I, R on day 2
            [95, 3, 2],  # S, I, R on day 3
            ...,
            [23, 24, 53]  # final prediction
        ]
        ```

        """
        # checks to make sure the model has been compiled
        if not self.compiled:  # pragma: no cover
            warnings.warn('An epispot model has not been compiled yet. '
                          'Triggering integration will automatically '
                          'compile the model.')
            self.compile()

        # initial parameter setup
        results = []

        if starting_state is not None:
            system = starting_state
        else:
            system = np.zeros(len(self.compartments))
            system[0] = self.initial_population - 1
            system[1] = 1

        delta = timesteps[1] - timesteps[0]

        for timestep in timesteps:

            # calculate the derivative for each compartment at this
            # timestep and update the system accordingly

            derivatives = self.diff(timestep, system)
            system += delta * derivatives
            results.append(deepcopy(system))

        return results

    def add(self, comp, comp_map, matrix):
        """
        Add a compartment to the model.
        This can also be done by initializing the `epispot.models.Model` class beforehand.

        ## Parameters

        `comp (epispot.comps.Compartment)`: Compartment class (e.g. `epispot.comps.Susceptible` or `epispot.comps.Infected`)

        `comp_map (list[int])`: Slice of the larger `map` specified in `epispot.models.Model`.
            This should simply include the compartment connections for this specific compartment.

        `matrix (list[tuple(float|func(t: float)->float, float|func(t: float)->float)])`: Slice of the larger `matrix` specified in
                  `epispot.models.Model`. As with `map`, this should
                  only include the rates and probabilities for this
                  compartment's connections.

        ## Error Handling

        Initializing some parameters in `epispot.models.Model` without initializing all of them will raise a `ValueError`.

        ## Additional Notes

        See the documentation for `epispot.models.Model` for more help and examples.

        """
        if self.compiled:
            self.compiled = False

        if (self.compartments, self.map, self.matrix) == (None, None, None):
            self.compartments = [comp]
            self.names = [comp.name]
            self.map = [comp_map]
            self.matrix = [matrix]
        elif self.compartments is not None \
            and self.map is not None \
            and self.matrix is not None:
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

        `names (list[str])`: A list of names corresponding to `comps`

        """
        self.names = names
        for i, comp in enumerate(self.compartments):
            comp.name = names[i]

    def save(self, filename):
        """
        Save the model to a file.
        This can be used to load the model later.
        Standard file ending is `.epi`.

        ## Parameters

        `filename (str)`: Name of the file to save the model to

        ## Error Handling

        - If the file already exists, it will be overwritten.
        - If the model is not compiled, it will raise a `ValueError`.

        """
        if not self.compiled:  # pragma: no cover
            raise ValueError('Model has not been compiled yet. '
                             'Cannot save model.')

        with open(filename, 'wb') as f:
            dill.dump(self, f)

    @classmethod
    def load(cls, filename):
        """
        Load a model from a file.

        ## Parameters

        `filename (str)`: Name of the file to load the model from

        ## Security

        ..warning::
            Be careful when loading a model from a file. Untrusted sources
            could potentially embed malicious code into various parts of the
            model which can lead to arbitrary code execution.

        ## Error Handling

        - If the file does not exist, it will raise a
          `FileNotFoundError`.

        """
        with open(filename, 'rb') as f:
            loaded = dill.load(f)
            if not loaded.compiled:  # pragma: no cover
                loaded.compile()
            if loaded.version != version:  # pragma: no cover
                warnings.warn(
                    'This model has been imported from an '
                    f'older version of epispot v{loaded.version}. '
                    f'You have epispot v{version}.'
                )
            return loaded
