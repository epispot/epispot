"""
The `epispot.estimates.utils` module contains miscellaneous utilities for grouping and manipulating estimates stored in `epispot.estimates.data`.
It can also be used to import estimates that epispot does not already have.

"""

# imports
from . import np, storage


class Disease:
    """High-level grouping of estimates by disease."""

    def __init__(
        self,
        id,
        papers,
        name=None,
        description=None,
    ):
        """
        Group estimates by disease:

        ## Parameters

        `id (str)`: Unique scientific identifier for the disease
            (in the case of COVID-19, e.g. `'SARS-CoV-2'`)

        `papers (list[epispot.estimates.utils.Paper])`: List of `epispot.estimates.utils.Paper` objects for the disease

        `name=None (|str)`: Common (display) name for the disease

        `description=None (|str)`: Description of the disease

        ## Example

        ```python
        from epispot.estimates.utils import Disease
        covid = Disease(
            id='SARS-CoV-2',
            papers=[first_study, second_study, third_study],
            name='COVID-19',
            description='severe acute respiratory syndrome coronavirus 2',
        )
        ```

        Creates a `Disease` object for COVID-19, with relevant papers,
        name, and description.

        """
        self.id = id
        self.papers = papers
        self.name = name
        self.description = description

        storage.bulk.append(self)

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.name

    def __about__(self):
        return self.description


class Paper:
    """High-level grouping of parameter estimates by paper."""

    def __init__(
        self,
        id,
        params,
        metadata=None,
        in_text=None,
        full=None,
    ):
        """
        Group parameter estimates by paper:

        ## Parameters

        `id (tuple(str, str, int|str))`: Unique identifier tuple containing in-text citation info:
            e.g. `('Ganyani', 'et al.', 2020)`
            (replace `'et al.'` with a second author name if there are only two authors; omit if there is only one author)

        `params (list[epispot.estimates.utils.Estimate])`: List of `epispot.estimates.utils.Estimate` objects in the paper

        `metadata=None (|dict)`: Additional metadata about the paper as object with the following format:

        ```python
        {
            'title': 'Estimating the generation interval ...',
            'description': 'The 2019 coronavirus disease ...',
            'authors': ('Tapiwa Ganyani', 'Cécile Kremer', ...),
            'journal': 'Eurosurveillance',
            'date': datetime(2020, 3, 1),
            'url': 'https://www.eurosurveillance.org/...',
            'misc': {...}  # store other info here
        }
        ```

        `in_text=None (|str)`: More detailed in-text citation (as string) if necessary

        `full=None (|str)`: Full citation (as string) if necessary.
            Built-in estimates use APA style citations.

        ## Example

        ```python
        >>> from epispot.estimates.utils import Paper
        >>> ganyani = Paper(
        ...     id=('Ganyani', 'et al.', 2020),
        ...     params=[r_0, gamma, beta],
        ... )
        >>> ganyani.__cite__()
        'Ganyani et al. (2020)'
        ```

        Create a paper that references the study by Ganyani et al. (2020).

        """
        if not in_text:
            id_str = [str(i) for i in id]
            if len(id) == 2: in_text = ' '.join(id_str)
            else:
                if id[1] == 'et al.': in_text = ' '.join(id_str)
                else: in_text = id[0] + ', ' + ' '.join(id_str[1:])

        self.id = id
        self.params = params
        self.metadata = metadata
        self.in_text = in_text
        self.full = full

    def __repr__(self):
        return self.in_text

    def __str__(self):
        if self.metadata: return self.metadata['title']
        return self.in_text

    def __about__(self):
        if self.metadata: return self.metadata['description']
        if self.full: return self.full
        return self.in_text

    def __cite__(self):
        return self.in_text


class Estimate:
    """The base class for all estimates from the literature."""

    def __init__(
        self,
        id,
        dist,
        name=None,
        description=None,
    ):
        """
        Load an estimate or distribution from the literature:

        ## Function Parameters

        `z=0 (float)`: Amount of random noise to add to the distribution.
            *Magnitude of a uniform distribution (added to final result)*

        `**kwargs`: Additional keyword arguments to pass to the
                    distribution.

        ## Parameters

        `id (str)`: Identifier for the estimate (e.g. `'r_0'`)

        `dist (float | func(t: float)->float)`: Constant value or callable function for the estimate

        `name=None (|str)`: Name of the estimate

        `description=None (|str)`: Description for the estimate

        ## Example

        ```python
        >>> from epispot.estimates.utils import Estimate
        >>> dist = Estimate(
        ...     id='r_0',
        ...     dist=lambda t: 1 / (1 + np.exp(-t)),
        ...     name='Logistic R Naught Distribution',
        ...     description='A logistic distribution',
        ... )
        >>> dist(0)
        0.5
        ```

        Creates a logistic distribution for the value of R naught with respect to time.

        """
        self.id = id
        self.name = name
        self.dist = dist
        self.description = description

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.id

    def __about__(self):
        return self.name + ': ' + self.description

    def __call__(self, t, z=0, **kwargs):
        return self.dist(t, **kwargs) + z * np.random.standard_normal()
