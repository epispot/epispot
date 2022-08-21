"""
The `epispot.params` module stores various parameter distributions and estimations.
These parameter distributions are divided into two classes:
those useful for general epidemiological analysis and those useful for the analysis of a specific disease or variant of that disease.

Direct estimate from the literature are also available in the `epispot.estimates` sub-package,
but the underlying structure is similar to `epispot.params.Distribution`.

.. versionadded:: v3.0.0
.. important::
    Many features in this module are still in beta and are subject to changes.

"""

from . import np


class Distribution:
    """The base class for all parameter distributions."""

    def __init__(
        self,
        name=None,
        dist=lambda c: c,
        description=None,
    ):
        """
        Create a distribution to use in place of parameters:

        ## Function Parameters

        `z=0 (float)`: Amount of random noise to add to the distribution.
            *Magnitude of a uniform distribution (added to final result)*

        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        ## Parameters

        `name (str)`: Distribution name

        `dist=lambda c: c (func(t: float)->float)`: Function to generate the distribution

        `description (str)`: Description of the distribution

        `citation (str)`: Full citation of the distribution

        `in_text (str)`: In-text citation of the distribution

        ## Example

        ```python
        >>> from epispot.params import Distribution
        >>> dist = Distribution(
        ...     name='Logistic',
        ...     dist=lambda t: 1 / (1 + np.exp(-t)),
        ...     description='A logistic distribution',
        ... )
        >>> dist(0)
        0.5
        ```

        Create a logistic distribution and evaluate it at timestep zero.

        """
        self.name = name
        self.dist = dist
        self.description = description

    def __repr__(self):
        return f'<{self.name} distribution>'

    def __str__(self):
        return self.name

    def __about__(self):
        return self.description

    def __call__(self, t, z=0, **kwargs):
        return self.dist(t, **kwargs) + z * np.random.standard_normal()


class Gamma(Distribution):
    """Models γ in the SIR model."""

    def __init__(self, type='rel-beta', **kwargs):
        """
        Create a distribution for γ:

        ## Parameters

        `type='rel_beta'`: Type of distribution to use.

        **Options**:

        - `'rel-beta'`: Relative β distribution

        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        """
        if type == 'rel-beta':
            self.name = 'Relative-β Distribution'
            self.description = 'Distribution of γ relative to β'
            self.dist = lambda t: Gamma.rel_beta(t, **kwargs)

    @staticmethod
    def rel_beta(t, r_0, beta):
        """
        Distribution of γ relative to β.

        ## Function Parameters

        `r_0 (float|func(t: float)->float)`: Reproduction number

        `beta (float|func(t: float)->float)`: Transmission rate

        ## Example

        ```python
        >>> from epispot.params import Gamma
        >>> gamma = lambda t: Gamma.rel_beta(t, r_0=1, beta=0.5)
        >>> gamma(0)
        0.5
        ```

        Creates a gamma distribution for given R naught and beta values;
        epispot automatically calculates the value for gamma.

        """
        if callable(beta): beta = beta(t)
        if callable(r_0): r_0 = r_0(t)
        return beta / r_0


class RNaught(Distribution):
    """Models R naught in the SIR model."""

    def __init__(self, type='rel-beta', **kwargs):
        """
        Create a distribution for R naught:

        ## Parameters

        `type='rel-beta' (|'logistic'|'bell')`: Type of distribution to use.

        **Options**:

        - `'rel-beta'`: Relative β distribution
        - `'logistic'`: Logistic distribution
        - `'bell'`: Bell curve distribution

        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        """
        if type == 'rel-beta':
            self.name = 'Relative-β Distribution'
            self.description = 'Distribution of γ relative to β'
            self.dist = lambda t: RNaught.rel_beta(t, **kwargs)
        elif type == 'logistic':
            self.name = 'Reverse Logistic Distribution'
            self.description = 'A reverse logistic distribution ' \
                               '(starts high and then drops)'
            self.dist = lambda t: RNaught.logistic(t, **kwargs)
        elif type == 'bell':
            self.name = 'Bell Curve'
            self.description = 'Follows the equation of a normal ' \
                               'distribution (peaks near the center)'
            self.dist = lambda t: RNaught.bell(t, **kwargs)

    @staticmethod
    def rel_beta(t, gamma, beta):
        """
        Distribution of R naught relative to β.

        ## Function Parameters

        `gamma (float)`: Total recovery rate

        `beta (float)`: Transmission rate

        ## Example

        ```python
        >>> from epispot.params import r_0
        >>> r_0 = lambda t: r_0.rel_beta(t, gamma=1, beta=0.5)
        >>> r_0(0)
        0.5
        ```

        Let epispot find the value of R naught given gamma and beta values.

        """
        if callable(beta): beta = beta(t)
        if callable(gamma): gamma = gamma(t)
        return beta / gamma

    @staticmethod
    def logistic(t, c=1, k=1, x_0=0, y_0=1):
        """
        Reverse logistic distribution of R naught:
        <!--- $$ \\frac{c}{1 + e^{k(x-x_0)}} + y_0 $$ -->

        ## Function Parameters

        `c=1 (float)`: Maximum variation

        ..note::

            With `y_0=0`, this gives the maximum *value* of
            the distribution.

        `k=1 (float)`: Rate of decline

        `x_0=0 (float)`: Center of the distribution

        `y_0=1 (float)`: Minimum value

        ## Example

        ```python
        >>> from epispot.params import r_0
        >>> r_0 = lambda t: r_0.logistic(t)
        >>> r_0(0)
        1.5
        ```

        Model R naught using a logistic curve.

        """
        return c / (1 + np.exp(k * (t - x_0))) + y_0

    @staticmethod
    def bell(t, k=1 / 10, x_0=10, y_0=1):
        """
        Bell curve distribution of R naught:
        <!--- $$ e^{-k(x-x_0)^2} $$ -->

        ## Function Parameters

        `k=1/10 (float)`: Variance (rate of decline)

        `x_0=0 (float)`: Center of the distribution

        `y_0=1 (float)`: Minimum value

        ## Example

        ```python
        >>> from epispot.params import r_0
        >>> r_0 = lambda t: r_0.bell(t)
        >>> r_0(0)
        1
        ```

        Create a bell curve-like distribution for R naught and let epispot calculate the defined values over different timesteps.

        """
        return np.exp(-k * (t - x_0)**2) + y_0


class N(Distribution):
    """Models N (population) in the SIR model."""

    def __init__(self, type='constant', **kwargs):
        """
        Create a distribution for N:

        ## Parameters

        `type='constant' (|'linear')`: Type of distribution to use.

        **Options**:

        - `'constant'`: Constant population
        - `'linear'`: Linear population increase/decline

        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        """
        if type == 'constant':
            self.name = 'Constant-valued Population'
            self.description = 'Constant population size, where ' \
                               'death and birth rates are identical'
            self.dist = lambda t: N.constant(t, **kwargs)
        elif type == 'linear':
            self.name = 'Linear Population Trend'
            self.description = 'Linear population trend, ' \
                               'accounting for birth and death ' \
                               'rates'
            self.dist = lambda t: N.linear(t, **kwargs)

    @staticmethod
    def constant(t, n_0):
        """
        Constant-valued population.

        ## Function Parameters

        `n_0 (int)`: Initial population size

        ## Example

        ```python
        >>> from epispot.params import N
        >>> population = lambda t: N.constant(t, N_0=10)
        >>> population(0)
        10
        ```

        Set a constant population of `10`.

        """
        return n_0

    @staticmethod
    def linear(t, n_0, birth=0, death=0):
        """
        Linear population trend.

        ## Function Parameters

        `n_0 (int)`: Initial population size

        `birth (float|func(t: float)->float)`: Birth rate

        `death (float|func(t: float)->float)`: Death rate

        ## Example

        ```python
        >>> from epispot.params import N
        >>> population = lambda t: N.linear(t, N_0=10, birth=0.2, death=0.1)
        >>> population(0)
        10
        ```

        Create a population structure with initial population of `10` and defined birth and death rates.

        ..note:: Callable arguments accepted for `birth` and `death`,
                 but they must give *cumulative* values for estimates to
                 be correct.

        """
        if callable(birth): birth = birth(t)
        if callable(death): death = death(t)
        return n_0 * (1 + birth * t - death * t)
