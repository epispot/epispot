
![epispot](https://i.ibb.co/hXMjrCV/epi-spot.png)

---
    
# epispot v2

A Python package for the mathematical modeling of infectious diseases via 
compartmental models. Originally designed for epidemiologists, epispot can
be adapted for almost any type of modeling scenario.


## Features

The epispot package currently only supports compartmental models, though
we plan to expand the package to work for stochastic agent-based and spatial 
models as well. Currently, epispot offers the following:

- Quick compilation of compartmental models with the following compartments:
    - Susceptible
    - Infected
    - Recovered
    - Removed
    - Exposed
    - Dead
    - Critical
    - Hospitalized
- Custom-defined compartments for research
- Built-in graphing and visualization engine
  - Plots model predictions interactively
  - Creates comparisons between models

Due to its diverse range of features, epispot can be used for both research
and experimental modeling. If you would like to add more modeling support, please 
see the [contributing section](#contributing).
  
## Installation 

The epispot package can be installed from PyPI, Anaconda, or be built from the
source. Before reading this guide, it is important to note that there are actually 
*two* different versions of the epispot package. The first of which is the 
`master` package, which will always have a version tag like `v#.#.#`. 
This package is used to release stable versions of epispot. However, during 
important events, like the COVID-19 pandemic, the `nightly` package is used to
publish new features quickly. However, these versions may be unstable.

### PyPI
This is the easiest way to install epispot. Fire up a terminal and type:
```shell
pip install epispot
```
For the nightly version, use
```shell
pip install epispot-nightly
```
Pip will ask you to install `numpy` and `matplotlib` as dependencies if you 
haven't already. Additionally, it may require you to install `fire` for the CLI.
These can be installed beforehand with:
```shell
pip install numpy
pip install matplotlib
pip install fire
```

### Anaconda
Please note that the `nightly` version is **not** available on the `conda` 
package registry. However, it is still possible to install on `conda`-based
systems with
```shell
pip install epispot-nightly
```
which uses `pip` from Anaconda to install it.

The standard version of epispot is published to `conda` using the 
`conda-forge` channel. To install, please use:
```shell
conda config --add channels conda-forge
conda install -c conda-forge epispot
```

### Building from the source
This is the hardest way to install `epispot` and it is recommended that you
use either `PyPI` or `Anaconda` to install it instead. However, if you would like
to contribute to the repository, this will be particularly useful.

Clone the repository with:
```shell
git clone https://github.com/epispot/epispot  # clone epispot/epispot
cd epispot  # open project
pip install -r requirements.txt  # install package requirements
pip install -r bin/requirements.txt  # Install CLI requirements
```

Then, build the standard version with
```shell
python setup.py install
```
For the nightly version, use:
```shell
python setup-nightly.py install
```

## Quick Demo
Installing epispot from `pip` and then compiling a simple SIR model in less than 
40 seconds. 
[Link to source](https://github.com/epispot/epispot/tree/master/assets/demo.gif)

![](assets/demo.gif)

## Documentation

The documentation for the epispot package is generated automatically from 
the Python source code using Pdoc3. You can view the 
documentation for both the nightly and stable builds of epispot 
[here](https://epispot.github.io/epispot).

At first, the documentation may seem a bit hard to understand, especially
if you're new to epidemiology. That's why epispot has put together an entire
manual describing some basic concepts you'll need to know to master
epispot. You can view it [here](https://epispot.gitbook.io/manual/).
The GitHub source is available [here](https://github.com/epispot/manual).

  
## Usage/Examples

The GitHub repository has a vast array of samples using epispot. You can start 
by checking out the `explorables/` directory. In it, you'll find many programs 
designed for helping you get started with epispot and some hands-on examples.
  
## Badges

![latest-release](https://shields.mitmproxy.org/pypi/v/epispot.svg?color=success)
![conda](https://anaconda.org/conda-forge/epispot/badges/installer/conda.svg)
[![Downloads](https://pepy.tech/badge/epispot)](https://pepy.tech/project/epispot)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/quantum9Innovation/epispot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/quantum9Innovation/epispot/alerts/)
![open-issues](https://img.shields.io/github/issues-raw/epispot/epispot?color=orange)

### Statuses
| Pipeline | Status |
| --- | --- |
| Travis CI | [![Build Status](https://www.travis-ci.com/epispot/epispot.svg?branch=master)](https://www.travis-ci.com/epispot/epispot) |
| CodeCov | [![codecov](https://codecov.io/gh/epispot/epispot/branch/master/graph/badge.svg?token=WGIM127RFY)](https://codecov.io/gh/epispot/epispot) |
| PyPI main | ![latest-release](https://shields.mitmproxy.org/pypi/v/epispot.svg?color=success) |
| PyPI nightly | ![latest-release](https://shields.mitmproxy.org/pypi/v/epispot-nightly.svg?color=success) |
| Security | ![GitHub issue custom search in repo](https://img.shields.io/github/issues-search/epispot/epispot?color=success&label=known%20vulnerabilities&query=VULNERABILITY%20is:open%20is:issue) |

## Feedback

If you have any feedback, please

- Create a discussion on GitHub
- Create an issue if you've found a bug
- Submit a PR if you want to add a new feature
- Contact a [CODEOWNER](.github/CODEOWNERS)

  
## Contributing

Contributions are always welcome!
See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to get started,
including environment setup and instructions to build from the source.
Please note also that epispot has many guides dedicated to certain types of
contributions. Please see

- [DOCUMENTATION.md](DOCUMENTATION.md) for documentation additions
- [SECURITY.md](SECURITY.md) for epispot's security policy
  
## Citation

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-green.svg)](https://opensource.org/licenses/)

If you plan on using epispot in your project, please abide by the GPLv3 license.
This requires that any changes you make to epispot must be open-sourced under
the GPLv3 license as well and that you give credit to the author, which you can
do by citing the project in your research, linking back to the original repository,
or mentioning the author @quantum9innovation.

For research, you can also use epispot's DOI to reference the project:
> [![DOI](https://zenodo.org/badge/280527664.svg)](https://zenodo.org/badge/latestdoi/280527664)

The recommended citation for epispot is:
> quantum9innovation (2021, April 2). epispot/epispot: 
> (Version 2.1.0). Zenodo. http://doi.org/10.5281/zenodo.4624423

  
## Authors

Please see our [CODEOWNERS](.github/CODEOWNERS) file for authors. Because epispot
is an open-source project, different pieces of our code have different authors.
However, if citing epispot or using it in another project, you can put 
@quantum9innovation as the lead author.

  
## Acknowledgements

### Idea & Inspiration

The original idea for epispot came from a 
[3Blue1Brown video](https://www.youtube.com/watch?v=gxAaO2rsdIs) on basic 
infectious disease dynamics and an 
[interactive article](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/)
in the Washington Post. This in turn inspired the very basic infectious disease
dynamics simulated [here](https://quantum9innovation.github.io/disease/). However, 
what finally set the package into motion was a series of articles by Henry Froese,
available on Medium 
[here](https://towardsdatascience.com/infectious-disease-modelling-part-i-understanding-sir-28d60e29fdfc),
along with their corresponding interactive notebooks.

### Code Development & Maintenance

The epispot project is built on open source code and is itself open-source.
The initial core development was fueled by @quantum9innovation and much of the 
codebase was maintained by @Quantalabs. Additionally, thank you to all of 
epispot's open-source contributors!

![epispot's open-source contributors](https://contrib.rocks/image?repo=epispot/epispot)

### Dependencies

The epispot team also relies on the following open-source projects as dependencies:

- NumPy ([GitHub](https://github.com/numpy/numpy)), 
  the fundamental package for scientific computing with Python
- Matplotlib ([GitHub](https://github.com/matplotlib/matplotlib)), plotting with 
  Python
- Google Fire ([Github](https://github.com/google/python-fire)), a library for 
  automatically generating command line interfaces (CLIs) from absolutely any 
  Python object.

### External Code Management Tools

For code maintenance, epispot uses various tools including:

- Coverage.py ([PyPI](https://pypi.org/project/coverage/)) for code coverage 
  report generation
- Pdoc3 ([GitHub](https://github.com/pdoc3/pdoc)) for automatic documentation 
  generation
- GitBook ([Website](https://www.gitbook.com)) for documentation hosting
- CodeCov ([Website](https://about.codecov.io)) for code coverage report analysis
- LGTM ([Website](https://lgtm.com)) for CodeQL analysis
- DeepSource ([Website](https://deepsource.io)) for static code analysis
- GitLocalize ([Website](https://gitlocalize.com)) for localization of 
  documentation
- Zenodo ([Website](https://zenodo.org)) for automatic DOI & citations
