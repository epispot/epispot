# ![epi-spot](https://i.ibb.co/hXMjrCV/epi-spot.png)
![latest-release](https://shields.mitmproxy.org/pypi/v/epispot.svg?color=success)
![conda](https://anaconda.org/conda-forge/epispot/badges/installer/conda.svg)
[![Downloads](https://pepy.tech/badge/epispot)](https://pepy.tech/project/epispot)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/alerts/)
![build-status](https://github.com/epispot/epispot/workflows/build/badge.svg?branch=master)
<br><br>

A tool for creating and testing epidemiological models faster than ever for the mathematical modeling of infectious 
diseases. An idea from https://github.com/henrifroese/infectious_disease_modelling.

<br>

![epi-spot social image](https://docs.google.com/drawings/d/e/2PACX-1vT6zazkjjnz8UMZz7mxPFXjnvC1Q1HgBLGcNwt0DEqla5N10kC_LPcdbuWae2VBWgCL7kynE8vCTzru/pub?w=1440&h=1080)

## Installation

Epispot can be installed via pip or via Anaconda.
If using pip, install with:
```
pip install epispot
```
For Anaconda, use:
```
conda config --add channels conda-forge
conda install -c conda-forge epispot
```

As a shorthand, use `import epispot as epi`.

## Getting Started

Check the guides and tutorials found
in the `tests/tutorials` folder. All tutorials will have a `.md` file
followed by a corresponding code file. If you get stuck, don't understand 
something, or just need to reference the documentation, per-class 
documentation can be found at https://epispot.github.io/epispot. You may also find 
it helpful to see the examples in the `tests/examples` folder.

## Screenshots

![sf-case-study](tests/assets/compare-function.png)
![line-graph](tests/assets/line-graph.png)

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

# Stats
**GitHub Tests:** ![build-status](https://github.com/epispot/epispot/workflows/build/badge.svg?branch=master)
<br>**PyPi:** ![Downloads](https://pepy.tech/badge/epispot)
<br>**Anaconda:** ![Anaconda Donwloads](https://shields.io/conda/dn/conda-forge/epispot)

## Compile your model at the speed of light
### and get insights that match
Documentation can easily be accessed from function, class, and file docstrings.
Doc strings provide additional documentation on a certain function.
They can be accessed by the built-in Python `help()` command.
These strings are formatted in Github-flavored markdown.
Additionally, all files will have a 'STRUCTURE' label.
