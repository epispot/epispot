"""
Doc strings provide additional documentation on a certain function.
They can be accessed by the built-in Python `help()` command.
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
__version__ = "v2.1.0"  # version (v#.#.#)
__stable__ = True  # True --> stable release, False --> unstable release
__repo_data_url__ = 'https://www.github.com/epispot/epispot'  # source repo
