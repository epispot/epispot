"""
# epispot
A tool for creating and testing compartmental epidemiological models faster than ever for the mathematical modeling of
infectious diseases. An idea from https://github.com/henrifroese/infectious_disease_modelling.
---
## DOI Information
[![DOI](https://zenodo.org/badge/280527664.svg)](https://zenodo.org/badge/latestdoi/280527664)
### Citation:
> q9i, & QLabs. (2021, April 2). epispot/epispot: (Version 2.1.0). Zenodo. http://doi.org/10.5281/zenodo.4624423

## Checking your installation
When using epispot, epispot should automatically run a 'sanity check' to make sure everything was installed correctly.
To access some of epispot's metadata from the package itself and double-check your installation, run:
```python
>>> import epispot as epi
>>> print(epispot.version)
>>> '2.x.x'

>>> print(epispot.stable)
>>> True

>>> print(epispot.source)
>>> 'https://www.github.com/epispot/epispot'

>>> print(epispot.docs)
>>> 'https://epispot.github.io/epispot'

>>> print(epispot.issues)
>>> 'https://www.github.com/epispot/epispot/issues'

>>> help(epispot)
>>> 'Returns this docstring ...'

>>> help(epispot.some_module.some_function)
>>> 'Returns function docstring ...'
```

## Getting Started
Start with the tutorials in `tests/tutorials`
(see [GitHub repo](https://www.github.com/epispot/epispot/tree/master/tests/tutorials)). Next, check out the
documentation at https://epispot.github.io/epispot. You may also find
it helpful to see the examples in the `tests/examples` folder.

## Release Notes
See [GitHub repo](https://www.github.com/epispot/epispot/releases) for more info.

## Features
- Compartmental models with the following compartments:
    - Susceptible (traditional SIR)
    - Infected (traditional SIR)
    - Recovered (traditional SIR)
    - Exposed
    - Dead
    - Critical
    - Hospitalized
- Custom-defined compartmental models
- Graphing and visualization engine
    - Plot model predictions interactively
    - Compare different model predictions

## A Note on Documentation
Docstrings provide additional documentation on a certain function.
They can be accessed via the built-in Python `help()` command.
These strings are formatted in GitHub-flavored markdown.
Additionally, all files will have a 'STRUCTURE' label.

## Credits
The epispot package is supported by the following contributors:
 - Head of Software & Development: [@quantum9innovation](https://www.github.com/quantum9innovation)
 - Head of Code Maintenance: [@Quantalabs](https://www.github.com/quantalabs)

Thank you also to all [GitHub contributors](https://www.github.com/epispot/epispot/insights/contributors)
"""


def _dependency_check():
    """Checks dependencies"""
    try:
        import numpy
    except ImportError:  # pragma: no cover
        raise ImportError('''Epispot requires numpy for integrating models; install with either:
                                 >>> pip install numpy  # pip
                                 >>> conda install numpy  # anaconda''')
    try:
        import matplotlib
    except ImportError:  # pragma: no cover
        raise ImportError('''Epispot requires matplotlib for creating interactive plots of models; install with either:
                                 >>> pip install matplotlib  # pip
                                 >>> conda install matplotlib  # anaconda''')


# imports
import warnings
import random


# dependencies
_dependency_check()  # check for uninstalled dependencies
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


# local
from . import comps
from . import models
from . import pre
from . import plots
from . import fitters


def _sanity_check():
    """Pre-defined sanity check to check for installation errors"""

    if not version:
        warnings.warn('Version info could not be found; your version of epispot may be deprecated.', DeprecationWarning)
    if not source:
        warnings.warn('''No repository source indicated. Try installing directly from PyPI or Anaconda with:
                             >>> pip install epispot  # pip
                             >>> conda install epispot  # anaconda''', DeprecationWarning)
    if not docs:
        warnings.warn('Documentation source not found. Check the repository source for more information if it exists. '
                      'Otherwise, you can use the built-in Python `help` command to access documentation.',
                      DeprecationWarning)
    if not issues:
        warnings.warn('No issue tracker found for this version of epispot; your version of epispot may be deprecated',
                      DeprecationWarning)


# version info
version = '2.1.1.7'
"""
Epispot's version info (updated every nightly release)
Get with 
    >>> print(epispot.version)
"""

stable = False
"""
Build stability
- True --> main package (stable)
- False --> nightly package (possibly unstable)
"""

# metadata
source = 'https://www.github.com/epispot/epispot'
"""URL to GitHub source"""
docs = 'https://epispot.github.io/epispot'
"""Project documentation (not version-specific)"""
issues = 'https://www.github.com/epispot/epispot/issues'
"""Submit new issues or bugs here"""


_sanity_check()  # complete installation
