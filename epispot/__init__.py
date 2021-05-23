"""
.. include:: ../README.md
<!-- Documentation available at: https://epispot.github.io/epispot -->
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
        import matplotlib  # lgtm [py/import-and-import-from]
    except ImportError:  # pragma: no cover
        raise ImportError('''Epispot requires matplotlib for creating interactive plots of models; install with either:
                                 >>> pip install matplotlib  # pip
                                 >>> conda install matplotlib  # anaconda''')


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
from . import plots
from . import fitters


def _sanity_check():
    """Pre-defined sanity check to check for installation errors"""

    if not version or not source:  # pragma: no cover
        message = \
        '''
        Version information and/or source for your epispot installation could not be found.
        This likely means
         (1) this version of epispot is deprecated or dated
         (2) your installation of epispot is unstable
        Try reinstalling epispot
         (1) From PyPI:
             $ pip install epispot
         (2) From Anaconda:
             $ conda config --add channels conda-forge
             $ conda install -c conda-forge epispot
         (3) From the GitHub Source:
             $ git clone https://github.com/epispot/epispot
             $ cd epispot
             $ python install setup-nightly.py
        If this fails or has failed before, then revert to epispot's last stable version.
        Again, you can do this via
         (1) PyPI:
             (a) Go to https://pypi.org/project/epispot
             (b) Scroll to the last MAJOR release in the form `a.0.0`
             (c) Install via `$ pip install epispot==a.0.0` -- replace `a` with version #
         (2) GitHub Source:
             (a) Go to https://github.com/epispot/epispot
             (b) Click the 'branches' tab
             (c) Select the last branch with name `vA.0.0` for some version number A
             (d) Install as `.zip`
             (e) Unzip
             (f) Run `$ python install setup.py`
        '''
        raise DeprecationWarning(message)


# version info
version = '2.1.1.10'
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
del _sanity_check
