"""
.. include:: ../README.md
<!-- 
Documentation available at: 
https://epispot.github.io/epispot/en/v3.0.0-alpha-3 
-->
"""


def _dependency_check():
    """Checks dependencies"""
    try:
        import numpy
    except ImportError:  # pragma: no cover
        raise ImportError('In order to integrate `epispot` models, '
                          '`numpy` is a required dependency.\n'
                          'Install with either:\n'
                          ' $ pip install epispot\n'
                          ' $ conda install epispot')
    try:
        import matplotlib  # lgtm [py/import-and-import-from]
    except ImportError:  # pragma: no cover
        raise ImportError('In order to display plots, `matplotlib` is '
                          'a required dependency.\n'
                          'Install with either:\n'
                          ' $ pip install matplotlib\n'
                          ' $ conda install matplotlib')


# imports
import warnings
import random


# dependencies
_dependency_check()  # check for uninstalled dependencies
del _dependency_check
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


# local
from . import comps
from . import models
from . import pre
from . import fitters
from . import plots


# helper funcs
def _check_versions():
    """Checks for version conflicts"""
    pass

def _check_install():  # pragma: no cover
    """Checks for installation errors"""
    pass

def _check_updates():
    """Checks for updates"""
    pass

def sanity_check():
    """
    Sanity check to check for basic installation errors, 
    version conflicts, upgrades, etc.

    **Run this if you experience any problems with epispot and before 
    submitting any issues**
    
    """
    # check for installation errors
    if not source or not version:  # pragma: no cover
        _check_install()

    # check for version conflicts
    import sys
    if (sys.version_info[0] < 3) or \
           (sys.version_info[0] == 3 and sys.version_info[1] < 7):
        raise RuntimeError('Epispot requires Python 3.7 or later')  # pragma: no cover
    _check_versions()

    # check for updates
    _check_updates()


# version info
version = '3.0.0-alpha-3'
"""
Epispot's version info (updated every release)\n
Check version information with:

```
    >>> print(epispot.version)
```

Version information is also available through the `__version__` 
property, included for legacy support.
"""
__version__ = version  # alias for version

stable = False
"""
Build stability:

- True ⇒ main package (stable)
- False ⇒ nightly package (possibly unstable)
"""

# metadata
source = 'https://www.github.com/epispot/epispot'
"""URL to VCS source"""
raw = f'https://raw.githubusercontent.com/epispot/epispot/v{version}/'
"""URL to raw VCS source (must append file path)"""
docs = f'https://epispot.github.io/epispot/en/v{version}/'
"""Project documentation (version-specific)"""
issues = 'https://www.github.com/epispot/epispot/issues'
"""Bug tracker"""
