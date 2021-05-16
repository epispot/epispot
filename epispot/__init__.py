"""
.. include:: ../README.md
<!--- START: inline documentation

=======
epispot
=======

A tool for creating and testing compartmental epidemiological models faster than ever for the mathematical modeling of
infectious diseases. An idea from https://github.com/henrifroese/infectious_disease_modelling.

---

===============
DOI Information
===============

Recommended Citation for Research:
> q9i, & QLabs. (2021, April 2). epispot/epispot: (Version 2.1.0). Zenodo. http://doi.org/10.5281/zenodo.4624423

==========================
Checking your installation
==========================

When using epispot, epispot should automatically run a 'sanity check' to make sure everything was installed correctly.
To access some of epispot's metadata from the package itself and double-check your installation, run:

>>> import epispot as epi
>>> print(epispot.version)
>>> '2.x.x'  # should return something like this

>>> print(epispot.stable)
>>> True  # if this is False, you can always install a stable version from either Anaconda or the main package on PyPI

>>> help(epispot)
>>> 'Returns this docstring ...'

===============
Getting Started
===============

Start with the tutorials in `tests/tutorials`
(see https://www.github.com/epispot/epispot/tree/master/tests/tutorials). Next, check out the
documentation at https://epispot.github.io/epispot. You may also find
it helpful to see the examples in the `tests/examples` folder.

========
Features
========

- Compartmental models with the following compartments:
    - Susceptible (traditional SIR)
    - Infected (traditional SIR)
    - Recovered (traditional SIR)
    - Exposed (extended SIR)
    - Dead (extended SIR)
    - Critical (extended SIR)
    - Hospitalized (extended SIR)
- Custom-defined compartmental models (useful for research)
- Graphing and visualization engine
    - Plot model predictions interactively
    - Compare different model predictions

===================
Documentation Notes
===================

Docstrings provide additional documentation on a certain function.
They can be accessed via the built-in Python `help()` command.
These strings are formatted in GitHub-flavored markdown.
Additionally, all files will have a 'STRUCTURE' label. This README
is the only exception.

=======
Credits
=======

The epispot package is supported by the following contributors:
 - Head of Software & Development: @quantum9innovation - https://www.github.com/quantum9innovation
 - Head of Code Maintenance: @Quantalabs - https://www.github.com/quantalabs

Thank you also to all GitHub contributors!
See: https://www.github.com/epispot/epispot/insights/contributors

-->
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
