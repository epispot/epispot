"""
Basic packaging checks

STRUCTURE: 
├ base
    ├ sanity
    └ dependency
└ integrity
"""


def test_base():
    """Triggers automatic import checks from within epispot"""
    import epispot
    epispot.sanity_check()


def test_integrity():
    """Tests epispot's integrity (ensures no module is missing)"""
    from epispot import comps
    from epispot import fitters
    from epispot import models
    from epispot import pre
    from epispot.plots import web
    from epispot.plots import native
