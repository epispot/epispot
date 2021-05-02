"""
Basic packaging checks:
|- dependencies
|- sanity check
|- package integrity
"""

import epispot


def test_dependencies():
    """Tests epispot's dependencies (triggers a check from within the package)"""
    epispot._dependency_check()


def test_sanity():
    """Tests epispot's installation (triggers a check from within the package)"""
    epispot._sanity_check()


def test_integrity():
    """Tests epispot's integrity (ensures no module is missing)"""
    from epispot import comps
    from epispot import fitters
    from epispot import models
    from epispot import plots
    from epispot import pre
