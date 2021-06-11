"""
Basic packaging checks
|- base
   |- sanity
   |- dependency
|- integrity
"""


def test_base():
    """Triggers automatic import checks from within epispot"""
    import epispot


def test_integrity():
    """Tests epispot's integrity (ensures no module is missing)"""
    from epispot import comps
    from epispot import fitters
    from epispot import models
    from epispot import pre
    from epispot.plots import web
