"""
The `epispot.params` module stores various parameter distributions and 
estimations, many of which have been pulled from the literature. These 
parameter distributions are divided into two classes: those useful for 
general epidemiological analysis and those useful for the analysis of a 
specific disease or variant of that disease.

All estimates from literature can be accessed by their corresponding 
in-text citations. For full citations, use the `.__cite__()` method.

.. versionadded:: v3.0.0-beta

"""

from . import np


class Distribution:
    """The base class for all parameter distributions."""
    def __init__(
        self, 
        name=None, 
        dist=lambda c: c, 
        description=None, 
        citation=None, 
        in_text=None
    ):
        """
        Create a distribution to use in place of parameters.

        ## **Usage**

        `z=0`: Amount of random noise to add to the distribution.
               *Magnitude of a uniform distribution*
               *(added to final result)*

        `*args`: Additional arguments to pass to the distribution.
        `**kwargs`: Additional keyword arguments to pass to the 
                    distribution.

        ## **Parameters**

        `name`: Distribution name
        `dist`: Function to generate the distribution
        `description`: Description of the distribution
        `citation`: Full citation of the distribution
        `in_text`: In-text citation of the distribution

        ## **Example**

        <!--- spellcheck: stop -->
        ```python
        >>> from epispot.params import Distribution
        >>> dist = Distribution(
        ...     name='Logistic',
        ...     dist=lambda t: 1 / (1 + np.exp(-t)),
        ...     description='A logistic distribution',
        ...     citation='@book{garnier1838correspondance,\n'   \
                         'title={Correspondance math{\'e}matique et physique},\n'   \
                         'author={Garnier, J.G. and Quetelet, A.}\n'    \
                         'number={v. 10}\n' \
                         'lccn={03003361}\n'    \
                         'url={https://books.google.com/books?id=8GsEAAAAYAAJ}\n'   \
                         'year={1838}\n'    \
                         'publisher={Impr. d'H. Vandekerckhove}\n'  \
                         '}',
        ...     in_text='Verhulst 1838'
        ... )
        >>> dist(0)
        0.5
        ```
        <!--- spellcheck: start -->

        """
        self.name = name
        self.dist = dist
        self.description = description
        self.citation = citation
        self.in_text = in_text
    
    def __repr__(self):
        return self.dist
    def __str__(self):
        return self.name
    def __about__(self):
        return self.description
    def __call__(self, z=0, *args, **kwargs):
        return self.dist(*args, **kwargs) + z * np.random.random()
    def __cite__(self, type='full'):
        if type == 'full': return self.citation
        elif type == 'short': return self.in_text
        elif type == 'both': return f'{self.citation} ({self.in_text})'


class Gamma(Distribution):
    """Models γ in the SIR model."""
    def __init__(self, type='rel-beta', *args, **kwargs):
        """
        Create a distribution for γ.

        ## **Parameters**

        `type='rel_beta'`: Type of distribution to use.
                Options:
                    * `'rel-beta'`: Relative β distribution

        `*args`: Additional arguments to pass to the distribution.
        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        """
        if type == 'rel-beta':
                self.name = 'Relative-β Distribution'
                self.description = 'Distribution of γ relative to β'
                self.dist = lambda t: Gamma.rel_beta(t, *args, **kwargs)
    
    @staticmethod
    def rel_beta(t, R_0, beta):
        """
        Distribution of γ relative to β.

        ## **Usage**

        `R_0`: Reproduction number
        `beta`: Transmission rate

        ## **Example**

        ```python
        >>> from epispot.params import Gamma
        >>> gamma = lambda t: Gamma.rel_beta(t, R_0=1, beta=0.5)
        >>> gamma(0)
        0.5
        ```

        """
        if callable(beta): beta = beta(t)
        if callable(R_0): R_0 = R_0(t)
        return beta / R_0


class R_0(Distribution):
    """Models R_0 in the SIR model."""
    def __init__(self, type='rel-beta', *args, **kwargs):
        """
        Create a distribution for R_0.

        ## **Parameters**

        `type='rel-beta'`: Type of distribution to use.
                Options:
                    * `'rel-beta'`: Relative β distribution
                    * `'logistic'`: Logistic distribution
                    * `'bell'`: Bell curve distribution

        `*args`: Additional arguments to pass to the distribution.
        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        """
        if type == 'rel-beta':
                self.name = 'Relative-β Distribution'
                self.description = 'Distribution of γ relative to β'
                self.dist = lambda t: R_0.rel_beta(t, *args, **kwargs)
        elif type == 'logistic':
                self.name = 'Reverse Logistic Distribution'
                self.description = 'A reverse logistic distribution ' \
                                   '(starts high and then drops)'
                self.dist = lambda t: R_0.logistic(t, *args, **kwargs)
        elif type == 'bell':
                self.name = 'Bell Curve'
                self.description = 'Follows the equation of a normal ' \
                                   'distribution (peaks near the center)'
                self.dist = lambda t: R_0.bell(t, *args, **kwargs)
    
    @staticmethod
    def rel_beta(t, gamma, beta):
        """
        Distribution of R_0 relative to β.

        ## **Usage**

        `gamma`: Total recovery rate
        `beta`: Transmission rate

        ## **Example**

        ```python
        >>> from epispot.params import R_0
        >>> R_0 = lambda t: R_0.rel_beta(t, gamma=1, beta=0.5)
        >>> R_0(0)
        0.5
        ```

        """
        if callable(beta): beta = beta(t)
        if callable(gamma): gamma = gamma(t)
        return beta / gamma

    @staticmethod
    def logistic(t, c=1, k=1, x_0=0, y_0=1):
        """
        Reverse logistic distribution of R_0:
        ..math:: \frac{c}{1 + e^{k(x-x_0)}} + y_0

        ## **Usage**

        `c=1`: Maximum variation
               ..note:: With `y_0=0`, this gives the maximum *value* of 
                        the distribution.
        `k=1`: Rate of decline
        `x_0=0`: Center of the distribution
        `y_0=1`: Minimum value

        ## **Example**

        ```python
        >>> from epispot.params import R_0
        >>> R_0 = lambda t: R_0.logistic(t)
        >>> R_0(0)
        1.5
        ```

        """
        return c / (1 + np.exp(k * (t - x_0))) + y_0

    @staticmethod
    def bell(t, k=1/10, x_0=10, y_0=1):
        """
        Bell curve distribution of R_0:
        ..math:: e^{-k(x-x_0)^2}

        ## **Usage**

        `k=1/10`: Variance (rate of decline)
        `x_0=0`: Center of the distribution
        `y_0=1`: Minimum value

        ## **Example**

        ```python
        >>> from epispot.params import R_0
        >>> R_0 = lambda t: R_0.bell(t)
        >>> R_0(0)
        1
        ```

        """
        return np.exp(-k * (t - x_0)**2) + y_0


class N(Distribution):
    """Models N (population) in the SIR model."""
    def __init__(self, type='constant', *args, **kwargs):
        """
        Create a distribution for N.

        ## **Parameters**

        `type='constant'`: Type of distribution to use.
                Options:
                    * `'constant'`: Constant population
                    * `'linear'`: Linear population increase/decline

        `*args`: Additional arguments to pass to the distribution.
        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        """
        if type == 'constant':
                self.name = 'Constant-valued Population'
                self.description = 'Constant population size, where ' \
                                   'death and birth rates are identical'
                self.dist = lambda t: N.constant(t, *args, **kwargs)
        elif type == 'linear':
                self.name = 'Linear Population Trend'
                self.description = 'Linear population trend, ' \
                                   'accounting for birth and death ' \
                                   'rates'
                self.dist = lambda t: N.linear(t, *args, **kwargs)

    @staticmethod
    def constant(t, N_0):
        """
        Constant-valued population.

        ## **Usage**

        `N_0`: Initial population size

        ## **Example**

        ```python
        >>> from epispot.params import N
        >>> population = lambda t: N.constant(t, N_0=10)
        >>> population(0)
        10
        ```

        """
        return N_0

    @staticmethod
    def linear(t, N_0, birth=0, death=0):
        """
        Linear population trend.

        ## **Usage**

        `N_0`: Initial population size
        `birth`: Birth rate
        `death`: Death rate

        ## **Example**

        ```python
        >>> from epispot.params import N
        >>> population = lambda t: N.linear(t, N_0=10, birth=0.2, death=0.1)
        >>> population(0)
        10
        ```

        ..note:: Callable arguments accepted for `birth` and `death`, 
                 but they must give *cumulative* values for estimates to
                 be correct.

        """
        if callable(birth): birth = birth(t)
        if callable(death): death = death(t)
        return N_0 * (1 + birth * t - death * t)
                

class Estimate(Distribution):
    """
    TODO: Tracked in [#135](https://github.com/epispot/epispot/issues/135)
    """
    pass
 