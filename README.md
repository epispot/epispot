# ![epi-spot](https://i.ibb.co/hXMjrCV/epi-spot.png)
![latest-release](https://shields.mitmproxy.org/pypi/v/epispot.svg?color=success)
[![Downloads](https://pepy.tech/badge/epispot)](https://pepy.tech/project/epispot)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/alerts/)
<br><br>

A tool for creating and testing epidemiological models faster than ever for the mathematical modelling of infectious 
diseases. An idea from https://github.com/henrifroese/infectious_disease_modelling.

<br>

![epi-spot social image](https://i.ibb.co/0KLfTm5/epi-spot-social.png)

## Installation

Install via `pip install epispot` <br>
As a shorthand, use as `import epispot as epi`

## Getting Started

Check the guides and tutorials found
in the `tests/tutorials` folder. All tutorials will have a `.md` file
followed by a corresponding code file. If you get stuck, don't understand 
something, or just need to reference the documentation, per-class 
documentation can be found in the `docs/epispot` folder. You may also find 
it helpful to see the examples in the `tests/examples` folder.

## Screenshots

![line-graph](tests/examples/line-graph.png)

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

## Compile your model at the speed of light
### and get insights that match
Documentation can easily be accessed from function, class, and file docstrings.
Doc strings provide additional documentation on a certain function.
They can be accessed by the built-in Python `help()` command.
These strings are formatted in Github-flavored markdown.
Additionally, all files will have a 'STRUCTURE' label.
