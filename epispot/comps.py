"""
The `comps` module is a collection of compartments used to initialize
the `epispot.models.Model` object to create a compartmental model. Each
of these compartments are not very useful on their own, but when strung
together in a `epispot.models.Model` object, they can be quite powerful.
"""

from . import np

__pdoc__ = {}
__pdoc__['Compartment._base_check'] = True


class Compartment:
    """
    This class represents a compartment, used in compartmental models.
    The base compartmental model that all compartments can be used for is the `epispot.models.Model` class.
    Additionally, this class can be used with `super().__init__()` to create a custom compartment.
    """

    def __init__(self, name, config=None):
        """
        Initialize the compartment; invoke with:

        ```python
        class CustomCompartment(Compartment):
            def __init__():
                super().__init__(name='Custom Compartment', config={})
        ```

        ## Parameters

        `name (str)`: Name of the compartment (used in error messages)

        `config (dict{'type':'Susceptible'|'Infected'|None})`*: Configuration dictionary for the compartment.
            This allows epispot to identify special compartments.
            Currently, it should look like the dictionary shown in the example section.

        ## Example

        Example `config` dictionary:

        ```python
        valid_types = ['Susceptible', 'Infected', None]
        config = {
            'type': '',  # should be one of `valid_types`
        }
        ```

        ## Usage

        Here is an example of the simplest compartment that can be implemented as a subclass:

        ```python
        class Container(Compartment):
            def __init__(self):
                super().__init__('Container')
            def _check(self, minimap, compartments):
                self._base_check([], minimap, compartments)
        ```

        This creates a container compartment that can be used to hold portions of the population.
        Since it does not connect to any other compartments (indicated by the empty array `[]` passed into the `epispot.comps.Compartment._base_check()` function),
        it acts as a terminal state.

        ## Error Handling

        See the `epispot.comps.Compartment._base_check()` function for more information.

        ## Additional Notes

        *The `config` dictionary is likely to change in future releases.

        .. versionadded:: v3.0.0-alpha-2

        """
        if config is None:
            config = {}
        self.name = name
        self.config = config
        self._check_config()

    def __repr__(self):
        """A string representation of the compartment."""
        return f'<{self.name} Compartment @ epispot.comps.Compartment>'

    def _check_config(self):
        """Configuration dictionary checker"""
        if 'type' not in self.config.keys():
            self.config['type'] = None

    def _base_check(self, valid_compartments, minimap, compartments):
        """
        A helper function to check model integrity.
        Implement this in child classes through a `_check()` function.

        ## Parameters

        `valid_compartments (list[epispot.comps.Compartment])`: A list of valid compartments that the model can connect to.
            If any compartments not specified in this list are found, a `ValueError` will be raised
            (see "Error Handling").

        `minimap (list[int])`: A slice of the larger connections list given in the `map` parameter of `epispot.models.Model` specific to this compartment.

        `compartments (list[epispot.comps.Compartment])`: A copy of the `compartments` parameter in `epispot.models.Model`; used to check against `valid_compartments`.

        .. note::
            These last two parameters (`minimap` and `compartments`) should also be parameters in the `_check()` function.
            See the usage section of `epispot.comps.Compartment` for more information.

        ## Error Handling

        ### `ValueError`

        If any extraneous compartments are found in the `compartments` list,
        this method will automatically raise a `ValueError`.

        ## Returns

        `True` if no errors have been raised.

        """
        for compartment_no in minimap:

            compartment = compartments[compartment_no]
            valid = False

            for valid_compartment in valid_compartments:
                if isinstance(compartment, valid_compartment):
                    valid = True

            if not valid:  # pragma: no cover
                raise ValueError(f'Invalid compartment {compartment} '
                                 f'found connected to compartment '
                                 f'{self.name}.')

        return True

    @staticmethod
    def diff(time, system, pos, minimap, minimatrix):
        """
        Calculate the derivative of the compartment with respect to
        time.

        ## Parameters

        `time (float)`: Time to take the derivative at.
            Similar to `time` parameter in `epispot.models.Model.diff`.

        `system (list[float])`: A list containing the system of compartment values.
            Should be of the same shape as the `starting_state` parameter of `epispot.models.Model.integrate`.

        `pos (int)`: The index of the compartment in the `comps` parameter of `epispot.models.Model`.

        `minimap (list[int])`: This compartment's connections.
            Essentially, a slice of the larger `map` parameter of `epispot.models.Model`.

        `minimatrix (list[tuple(float|func(t: float)->float, float|func(t: float)->float)])`: A slice of the `matrix` parameter of `epispot.models.Model` specific to this compartment.

        ## Returns

        Derivative of the entire system calculated by the compartment (`list[float]`)

        """
        output = np.zeros(system.shape)
        for connection in minimap:

            # initialize parameters
            probability = minimatrix[connection][0]
            rate = minimatrix[connection][1]

            # initialize time-dependent parameters
            if callable(probability):
                probability = probability(time)
            if callable(rate):
                rate = rate(time)

            # evaluate compartment derivative
            deriv = probability * rate * system[pos]

            # ensure compartment populations are non-negative
            min_connection_deriv = -system[connection]
            max_pos_deriv = system[pos]
            deriv = max(deriv, min_connection_deriv)
            deriv = min(deriv, max_pos_deriv)

            output[connection] += deriv
            output[pos] -= deriv

        return output


class Susceptible(Compartment):
    """
    The Susceptible class is the 'S' of the 'SIR' Model.
    This is the portion of individuals who have not yet been exposed to the disease.
    This class can be used as an initial state.
    Because of this property, the Susceptible class is a special compartment and does not use the default parameter matrix.

    ## Structure

    `epispot.comps.Recovered` → `epispot.comps.Susceptible` → `epispot.comps.Exposed`, `epispot.comps.Infected`
    """

    def __init__(self, r_0, gamma, n):
        """
        Initialize the Susceptible class:

        ## Parameters

        `r_0 (float|func(t: float)->float)`: The
            [basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number),
            indicating how infectious a given disease is.
            A value of above 1 indicates a high probability of transmission and thus an increasing infected population.
            A value of 1 indicates a constant infected population.
            A value below 1 indicates a low probability of transmission and also a decreasing infected population.

        `gamma (float|func(t: float)->float)`: The total recovery rate of patients.
            This is **not** a measure of how long it takes patients in any given compartment to recover but rather the reciprocal of the average time (in days) of infectiousness.

        `N (float|func(t: float)->float)`: The initial population size; should be the same as that passed into the `epispot.models.Model` class.

        """
        config = {
            'type': 'Susceptible',
        }
        super().__init__('Susceptible', config=config)
        self.r_0 = r_0
        self.gamma = gamma
        self.n = n

    def _check(self, minimap, compartments):
        """Check wrapper for the Infected compartment"""
        self._base_check([Exposed, Infected], minimap, compartments)
        if len(minimap) != 1:  # pragma: no cover
            raise ValueError('The Susceptible compartment must have '
                             'exactly one connection to either the '
                             'Infected or Exposed compartment.')

    def diff(self, time, system, pos, minimap, minimatrix, infecteds=None):
        """
        Calculate the derivative of the compartment with respect to
        time.

        ## Parameters

        `time (float)`: Time to take the derivative at.
            Similar to `time` parameter in `epispot.models.Model.diff`.

        `system (list[float])`: A list containing the system of compartment values.
            Should be of the same shape as the `starting_state` parameter of `epispot.models.Model.integrate`.

        `pos (int)`: The index of the compartment in the `comps` parameter of `epispot.models.Model`.

        `minimap (list[int])`: This compartment's connections.
            Essentially, a slice of the larger `map` parameter of `epispot.models.Model`.

        `minimatrix (list[tuple(float|func(t: float)->float, float|func(t: float)->float)])`: A slice of the `matrix` parameter of `epispot.models.Model` specific to this compartment.

        `infecteds (list[int])`: A list of the indices of the Infected compartments
            (those with `'type'='Infected'`) in the `config` parameter of `epispot.comps.Compartment`).

        ## Returns

        Derivative of the entire system calculated by the compartment (`list[float]`)

        """
        if infecteds is None:
            infecteds = []
        output = np.zeros(system.shape)

        # initialize parameters
        r_0 = self.r_0
        gamma = self.gamma
        n = self.n

        # initialize time-dependent parameters
        if callable(r_0):
            r_0 = r_0(time)
        if callable(gamma):
            gamma = gamma(time)
        if callable(n):
            n = n(time)

        # get total number of infecteds
        total_infecteds = 0
        for i in infecteds:
            total_infecteds += system[i]

        for connection in minimap:

            # evaluate compartment derivative
            deriv = r_0 * gamma * system[pos] * total_infecteds / n
            deriv *= minimatrix[connection][0] * minimatrix[connection][1]

            # ensure compartment populations are non-negative
            min_connection_deriv = -system[connection]
            max_pos_deriv = system[pos]
            deriv = max(deriv, min_connection_deriv)
            deriv = min(deriv, max_pos_deriv)

            # apply derivative
            output[connection] += deriv
            output[pos] -= deriv

        return output


class Infected(Compartment):
    """
    The Infected class is the 'I' of the 'SIR' Model.
    This is the portion of individuals who are actively spreading the disease.
    Like the `epispot.comps.Susceptible` class, this is also a special compartment.

    ## Structure

    `epispot.comps.Susceptible`, `epispot.comps.Exposed` → `epispot.comps.Infected` → `epispot.comps.Recovered`, `epispot.comps.Hospitalized`, `epispot.comps.Critical`, `epispot.comps.Dead`, `epispot.comps.Removed`
    """

    def __init__(self):
        """Initialize the Infected class"""
        config = {
            'type': 'Infected',
        }
        super().__init__('Infected', config=config)

    def _check(self, minimap, compartments):
        """Check wrapper for the Infected compartment"""
        self._base_check([Recovered, Hospitalized, Critical, Dead, Removed],
                         minimap, compartments)


class Removed(Compartment):
    """
    The 'Removed' class is a special class that acts as the combination of both the `epispot.comps.Recovered` and `epispot.comps.Dead` compartments.
    This is a useful construct when the fatality and recovery rates are the same (or almost the same),
    or if you want to simplify your model by decreasing the number of compartments
    (like the 'R' in the classic SIR model).
    This compartment is a *terminal state*, meaning that it can (only) be used as the last compartment in a model.

    ##

    Any `epispot.comps.Compartment` → `epispot.comps.Removed` → `epispot.comps.Susceptible`
    """

    def __init__(self):
        """Initialize the Removed class"""
        super().__init__('Removed')

    def _check(self, minimap, compartments):
        """Check wrapper for the Removed compartment"""
        self._base_check([Susceptible], minimap, compartments)


class Recovered(Compartment):
    """
    The 'Recovered' class represents the portion of the population that has had the infection and subsequently recovered.
    In most epidemiological models and scenarios, the individuals in this class are assumed to have developed some immunity to the virus.
    However, this is not always the case.
    In rare occasions where resusceptibility *is* possible, connecting this class to the `epispot.comps.Susceptible` class is possible.
    This class can alternatively be used as a terminal state.

    ## Structure

    `epispot.comps.Infected`, `epispot.comps.Hospitalized`, `epispot.comps.Critical` → `epispot.comps.Recovered` → `epispot.comps.Susceptible`
    """

    def __init__(self):
        """Initialize the Recovered class"""
        super().__init__('Recovered')

    def _check(self, minimap, compartments):
        """Check wrapper for the Recovered compartment"""
        self._base_check([Susceptible], minimap, compartments)


class Exposed(Compartment):
    """
    The Exposed compartment is traditionally used as a way to simulate an incubation period for a disease.
    This compartment tracks people who have come into contact with an infected person and are bound to eventually become infectious themselves,
    but haven't yet developed symptoms or a way of spreading the disease to others.
    These are also usually the targets of most
    [contact tracing](https://en.wikipedia.org/wiki/Contact_tracing)
    efforts.

    `epispot.comps.Susceptible` → `epispot.comps.Exposed` → `epispot.comps.Infected`
    """

    def __init__(self):
        """Initialize the Exposed class"""
        super().__init__('Exposed')

    def _check(self, minimap, compartments):
        """Check wrapper for the Exposed compartment"""
        self._base_check([Infected], minimap, compartments)


class Dead(Compartment):
    """
    The Dead class is a fully terminal state in any compartmental model.
    It represents the portion of the population that have died because of *and only because of* the disease being analyzed.

    ## Structure

    `epispot.comps.Infected`, `epispot.comps.Critical`, `epispot.comps.Hospitalized`, `epispot.comps.Recovered` → `epispot.comps.Dead`

    .. note::
       As is convention with compartmental models, we assume that the dead compartment does not significantly alter the population structure that we're analyzing.
       In future versions of epispot, we do plan to add support for factoring in the deceased population into predictions,
       but at this time that is not a primary concern.
    """

    def __init__(self):
        """Initialize the Dead class"""
        super().__init__('Dead')

    def _check(self, minimap, compartments):
        """Check wrapper for the Dead compartment"""
        self._base_check([], minimap, compartments)


class Hospitalized(Compartment):
    """
    The Hospitalized class represents the portion of individuals currently taking up space in the available hospitals.
    However, this is a distinct category from the `epispot.comps.Critical` portion of individuals,
    who require more resources (e.g. ICU beds, ventilators, etc.).
    This compartment also features
    [triage support](https://en.wikipedia.org/wiki/Triage).

    ## Structure

    `epispot.comps.Infected` → `epispot.comps.Hospitalized` → `epispot.comps.Critical`, `epispot.comps.Recovered`, `epispot.comps.Removed`, `epispot.comps.Dead`
    """

    def __init__(self, max_cap=None, index=None):
        """
        Initialize the Critical class:

        ## Parameters

        `max_cap=None (|int)`: The maximum number of individuals that available hospitals can hold.
            Specifying an amount will automatically trigger triage support,
            requiring a value for `index`.

        `index=None (|int)`: Index of the layer to use for triage.
            Only specify after giving a value for `max_cap`.

        ## Error Handling

        ### `ValueError`

        Failing to specify both a maximum capacity and an index when triage is enabled will raise a `ValueError`.

        """
        super().__init__('Hospitalized')
        self.maximum_capacity = max_cap
        self.triage_index = index

        if ((max_cap, index) != (None, None)) \
            and (max_cap is None or index is None):  # pragma: no cover
            raise ValueError('You must specify both a maximum '
                             'capacity and an index for triage '
                             'support.')

    def _check(self, minimap, compartments):
        """Check wrapper for the Hospitalized compartment"""
        self._base_check([Critical, Recovered, Removed, Dead], minimap,
                         compartments)

    def diff(self, time, system, pos, minimap, minimatrix):
        """
        Calculate the derivative of the compartment with respect to
        time.

        ## **Parameters**

        `time`: Time to take the derivative at. Similar to `time`
                parameter in `epispot.models.Model.diff`.

        `system`: A list containing the system of compartment values.
                  Should be of the same shape as the `starting_state`
                  parameter of `epispot.models.Model.integrate`.

        `pos`: The index of the compartment in the `comps` parameter of
               `epispot.models.Model`.

        `minimap`: This compartment's connections. Essentially, a slice
                   of the larger `map` parameter of
                   `epispot.models.Model`.

        `minimatrix`: A slice of the `matrix` parameter of
                      `epispot.models.Model` specific to this
                      compartment.

        ## **Returns**

        The compartment derivative

        """
        output = np.zeros(system.shape)
        for connection in minimap:

            # initialize parameters
            probability = minimatrix[connection][0]
            rate = minimatrix[connection][1]

            # initialize time-dependent parameters
            if callable(probability):
                probability = probability(time)
            if callable(rate):
                rate = rate(time)

            # evaluate compartment derivative
            deriv = probability * rate * system[pos]

            # ensure compartment populations are non-negative
            min_connection_deriv = -system[connection]
            max_pos_deriv = system[pos]
            deriv = max(deriv, min_connection_deriv)
            deriv = min(deriv, max_pos_deriv)

            output[connection] += deriv
            output[pos] -= deriv

        if (self.maximum_capacity is not None) and \
           (system[pos] > self.maximum_capacity):
            output[pos] = self.maximum_capacity - system[pos]
            output[self.triage_index] = -output[pos]

        return output


class Critical(Compartment):
    """
    The Critical class represents the portion of individuals currently taking up space in the available hospitals *and* using limited resources.
    Thus, this is a distinct category from the `epispot.comps.Hospitalized` portion of individuals, who don't require extra resources (ICU beds, ventilators, etc.).
    This compartment also features
    [triage support](https://en.wikipedia.org/wiki/Triage).

    ## Structure

    `epispot.comps.Hospitalized`, `epispot.comps.Infected` → `epispot.comps.Critical` → `epispot.comps.Recovered`, `epispot.comps.Removed`, `epispot.comps.Dead`
    """

    def __init__(self, max_cap=None, index=None):
        """
        Initialize the Critical class:

        ## Parameters

        `max_cap=None (|int)`: The maximum number of individuals that available hospitals can hold and have limited resources for.
            Specifying an amount will automatically trigger triage support,
            requiring a value for `index`.

        `index=None (|int)`: Index of the layer to use for triage.
            Only specify after giving a value for `max_cap`.

        ## Error Handling

        ### `ValueError`

        Failing to specify both a maximum capacity and an index when triage is enabled will raise a `ValueError`.

        """
        super().__init__('Critical')
        self.maximum_capacity = max_cap
        self.triage_index = index

        if ((max_cap, index) != (None, None)) and \
           (max_cap is None or index is None):  # pragma: no cover
            raise ValueError('You must specify both a maximum '
                             'capacity and an index for triage '
                             'support.')

    def _check(self, minimap, compartments):
        """Check wrapper for the Hospitalized compartment"""
        self._base_check([Recovered, Removed, Dead], minimap, compartments)

    def diff(self, time, system, pos, minimap, minimatrix):

        output = np.zeros(system.shape)
        for connection in minimap:

            # initialize parameters
            probability = minimatrix[connection][0]
            rate = minimatrix[connection][1]

            # initialize time-dependent parameters
            if callable(probability):
                probability = probability(time)
            if callable(rate):
                rate = rate(time)

            # evaluate compartment derivative
            deriv = probability * rate * system[pos]

            # ensure compartment populations are non-negative
            min_connection_deriv = -system[connection]
            max_pos_deriv = system[pos]
            deriv = max(deriv, min_connection_deriv)
            deriv = min(deriv, max_pos_deriv)

            output[connection] += deriv
            output[pos] -= deriv

        if (self.maximum_capacity is not None) and \
           (system[pos] > self.maximum_capacity):
            output[pos] = self.maximum_capacity - system[pos]
            output[self.triage_index] = -output[pos]

        return output
