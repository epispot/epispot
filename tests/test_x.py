"""
Basic packaging checks
|- dependencies
|- sanity
|- integrity
"""

import epispot as epi


def test_dependencies():
    """Tests epispot's dependencies (triggers a check from within the package)"""
    epi._dependency_check()


def test_sanity():
    """Tests epispot's installation (triggers a check from within the package)"""
    epi._sanity_check()


def test_integrity():
    """Tests epispot's integrity (ensures no module is missing)"""
    from epispot import comps
    from epispot import fitters
    from epispot import models
    from epispot import plots
    from epispot import pre
