"""
Basic packaging checks

STRUCTURE:
├ base
    ├ dependency (x2)
    └ sanity
└ integrity
"""


def test_base():
    """Triggers automatic import checks from within epispot"""
    import epispot
    epispot.dependency_check()
    epispot.plots.dependency_check()
    epispot.sanity_check()


def test_integrity():
    """Tests epispot's integrity (ensures no module is missing)"""
    from epispot import comps, models, params, pre
    from epispot.estimates import data, getters, storage, utils
    from epispot.plots import native, web
