"""
Docstrings provide additional documentation on a certain function.
They can be accessed via the built-in Python `help()` command.
These strings are formatted in Github-flavored markdown.
Additionally, all files will have a 'STRUCTURE' label.
"""

# imports
import warnings
import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

# local
from . import comps
from . import models
from . import pre
from . import plots
from . import fitters

# version info
__version__ = "v2.1.1.3"  # version (v#.#.#)
"""epispot's version info"""
__stable__ = False
"""stability of the build: True --> stable release (master), False --> unstable release (nightly)"""
__repo_data_url__ = 'https://www.github.com/epispot/epispot'  # source repo
"""URL to GitHub source"""
