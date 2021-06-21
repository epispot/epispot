# Release Notes

Latest stable release: 2.1.1

Releases are listed from most recent to least recent. All `alpha` and in-development versions are released to the [epispot-nightly](https://pypi.org/project/epispot-nightly/) project while all other releases are shipped to the [main project](https://pypi.org/project/epispot/).

---

## 3.0.0-alpha-1 (massive-plots)

This is the first stage of the v3 release rollout. Following this, there will likely be many more `alpha-x` releases. The major changes in this release come from an epispot operation known as `massive-plots`.

Essentially, the main changes are that the `epi.plots` module is now completely updated to feature new, modern graphs using `plotly` for interactive, web-based graphics and `SciencePlots` to create native, scientific charts. Unfortunately, however, `epi.plots.plot_comp_nums` and `epi.plots.compare` are now deprecated. However, new, updated replacements for these can be found in the `epi.plots.native` module.

You can read the documentation for these replacements [here](https://epispot.github.io/epispot/en/v3.0.0-alpha-1/plots/native.html) and the documentation for the new `epi.plots` subpackage [here](https://epispot.github.io/epispot/en/v3.0.0-alpha-1/plots/index.html).
