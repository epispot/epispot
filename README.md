# ![epi-spot](https://i.ibb.co/m9yS1yh/epispot-nightly.jpg)
![build](https://img.shields.io/badge/build-nightly-black)
![latest-release](https://shields.mitmproxy.org/pypi/v/epispot-nightly.svg?color=success)
[![Downloads](https://pepy.tech/badge/epispot-nightly)](https://pepy.tech/project/epispot-nightly)
![build-status](https://github.com/epispot/epispot/workflows/build/badge.svg?branch=nightly)
![open-issues](https://img.shields.io/github/issues-search/epispot/epispot?color=red&label=Open%20Issues&query=is%3Aopen%20label%3Anightly)
[![codecov](https://codecov.io/gh/epispot/epispot/branch/nightly/graph/badge.svg?token=WGIM127RFY)](https://codecov.io/gh/epispot/epispot)

<br>

A tool for creating and testing epidemiological models faster than ever for the mathematical modeling of infectious 
diseases. An idea from https://github.com/henrifroese/infectious_disease_modelling.

> **This is a nightly build of epispot. Releases may contain unstable code and issues are to be expected.\
> Additionally, code within this branch may be deprecated at any time.\
> See the official stable build and all its features [here](https://pypi.org/project/epispot/)**

<br>

## Installation

Epispot nightly can _only_ be installed on pip at this time.
Install with:
```shell
pip install epispot-nightly
```
As a shorthand, use `import epispot as epi`.
Both nightly and stable packages cannot be used at the same time in the same file.
To ensure that you are using the latest version, run the following command regularly*:\
```shell
pip install epispot-nightly --upgrade
```

*updates are published after every commit (~1/day)\
See [CHANGELOG.md](https://www.github.com/epispot/epispot/tree/nightly/CHANGELOG.md)
for detailed update information

## Getting Started

Make sure you are already familiar with [epispot](https://www.pypi.org/project/epispot).
If not, checkout the [tests/ directory](https://www.github.com/epispot/epispot/tree/nightly/tests)
for hands-on examples.
You can view the new functions and changes by using the built-in Python `help()` command.
Epispot docs are located [here](https://epispot.github.io/epispot).

## Stay one step ahead
### And preview the latest features
Documentation can easily be accessed from function, class, and file docstrings.
Doc strings provide additional documentation on a certain function.
They can be accessed by the built-in Python `help()` command.
These strings are formatted in Github-flavored markdown.
Additionally, all files will have a 'STRUCTURE' label.

## Thanks to all contributers
<a href="https://github.com/epispot/epispot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=epispot/epispot" />
</a>

Made with [contributors-img](https://contrib.rocks).
