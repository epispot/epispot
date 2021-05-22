"""
Basic packaging checks
|- base
   |- sanity
   |- dependency
|- integrity
"""

import os
import sys
import csv

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def test_base():
    """Triggers automatic import checks from within epispot"""
    import epispot


def test_integrity():
    """Tests epispot's integrity (ensures no module is missing)"""
    from epispot import comps
    from epispot import fitters
    from epispot import models
    from epispot import plots
    from epispot import pre
