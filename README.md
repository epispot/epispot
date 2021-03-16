# ![epi-spot](https://i.ibb.co/hXMjrCV/epi-spot.png)
![latest-release](https://shields.mitmproxy.org/pypi/v/epispot.svg?color=success)
![conda](https://anaconda.org/conda-forge/epispot/badges/installer/conda.svg)
[![Downloads](https://pepy.tech/badge/epispot)](https://pepy.tech/project/epispot)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/alerts/)
![lines of code](https://img.shields.io/tokei/lines/github/epispot/epispot?color=orange)
![open-issues](https://img.shields.io/github/issues-raw/epispot/epispot?color=orange)
![build-status](https://github.com/epispot/epispot/workflows/build/badge.svg?branch=master)
<br><br>

A tool for creating and testing epidemiological models faster than ever for the mathematical modeling of infectious 
diseases. An idea from https://github.com/henrifroese/infectious_disease_modelling.

**This is a nightly build of epispot. Releases may contain unstable code and issues are to be expected.\
Additionally, code within this branch may be deprecated at any time.\
See the official stable build and all its features [here](https://pypi.org/project/epispot/)**

To ensure that you are using the latest version, run the following command regularly*:\
`pip install epispot-nightly --upgrade` \
*updates are published after every commit (~1/day)

<br>

## Installation

Epispot nightly can _only_ be installed on pip at this time.
Install with:
```
pip install epispot-nightly
```
As a shorthand, use `import epispot as epi`.
Both nightly and stable packages cannot be used at the same time in the same file.

You can also install the `epispot-nightly` package from pip:
``` bash
pip install epispot-nightly
```
You can import it the same as `import epispot as epi`. Both packages cannot be used at the same time.

## Getting Started

Check the guides and tutorials found
in the `tests/tutorials` folder. All tutorials will have a `.md` file
followed by a corresponding code file. If you get stuck, don't understand 
something, or just need to reference the documentation, per-class 
documentation can be found at https://epispot.github.io/epispot. You may also find 
it helpful to see the examples in the `tests/examples` folder.

## Screenshots

![sf-case-study](https://github.com/epispot/epispot/blob/master/tests/assets/compare-function.png?raw=true)
![line-graph](https://github.com/epispot/epispot/blob/master/tests/assets/line-graph.png?raw=true)

## Features
- SIR-based models
  - Susceptible
  - Infected
  - Recovered
  - Exposed
  - Dead
  - Critical
  - Hospitalized
- Custom-defined compartmental models
  - Create custom models using the `Model` class
- Graphing Capabilities
  - Plot real data from a `.csv` file
  - Plot model predictions interactively
  - Compare different model predictions

## Stats
**GitHub Tests:** ![build-status](https://github.com/epispot/epispot/workflows/build/badge.svg?branch=master)
<br>**PyPi:** ![Downloads](https://pepy.tech/badge/epispot)
<br>**Anaconda:** ![Anaconda Donwloads](https://shields.io/conda/dn/conda-forge/epispot)

## Latest Release Notes (nightly build)

 - 3/13/21 2.0.1.23 Add documentation, triggering workflow. See commit description for deeper info.
 - 2/26/21 2.0.1.22 Automations
   - Automated code coverage reports
   - Working on automating release notes 
 - 2/12/21 2.0.1.17 Actions Test
 - 2/12/21 2.0.1.16: Stability Improvements
    - Allows for faster bug and issue tracking

**Stay one step ahead and preview the latest features with epispot-nightly.*
