![epispot](https://i.ibb.co/m9yS1yh/epispot-nightly.jpg)

---

# epispot nightly

A Python package for the mathematical modeling of infectious diseases via compartmental models. Originally designed for epidemiologists, epispot can be adapted for almost any type of modeling scenario.

> This is a nightly version of epispot and may contain possibly unstable code.  
> **Please see usage instructions prior to adding this project as a dependency**  
> If you prefer to use the stable version of epispot, please see
> the [project on PyPI](https://pypi.org/project/epispot)

## Installation

The epispot package can be installed from PyPI, Anaconda, or be built from the source. However, as epispot's nightly versions cannot be released per-commit to  the conda packaging registry, using Anaconda means that epispot will have to be installed via the built-in `pip` installer. Instructions for each platform are listed below.

### PyPI

This is the easiest way to install epispot nightly. Fire up a terminal and type:

```shell
pip install epispot-nightly
```

Pip will ask you to install `numpy` and `matplotlib` as dependencies if you haven't already. Additionally, it may require you to install `fire`, `plotly`, and `SciencePlots` for some `nightly` experiments.
These can be installed beforehand with:

```shell
pip install numpy
pip install matplotlib
pip install fire
pip install plotly
pip install SciencePlots
```

Update the package regularly with:

```shell
pip install epispot-nightly --upgrade
```

### Anaconda

Please note that the `nightly` version is **not** available on the `conda` package registry (although we may add it in the future). However, it is still possible to install on `conda`-based systems with

```shell
pip install epispot-nightly
```

which uses `pip` from Anaconda to install it. All dependencies are available on the conda package registry (except `SciencePlots`), but you may prefer to install them via `pip` to avoid cross-referencing packages installed on different registries.

`SciencePlots` can be installed using `pip` with:

```shell
pip install SciencePlots
```

Update the package regularly with:

```shell
pip install epispot-nightly --upgrade
```

If you installed the dependencies on conda instead of `pip` you may have to update them too after major releases. You can do that with:

```shell
conda update numpy
conda update matplotlib
conda update fire
conda update -c conda-forge plotly
```

### Building from the source

This is the hardest way to install `epispot-nightly` but it can be particularly useful if you plan on helping out with the development process. The main downside of this approach is that you will have to continuously run `git pull` and then rerun the steps listed below to get the latest version.

Clone the repository with:

```shell
git clone https://github.com/epispot/epispot
cd epispot/requirements
pip install -r pre-requirements.txt  # helps avoid version conflicts
pip install -r requirements-nightly.txt
```

If you're planning on helping out in the development process, it will be  helpful to install a few extra requirements with:

```shell
pip install -r requirements-dev.txt
```

Then, build the nightly version with:

```shell
python setup-nightly.py install
```

If you're working on a patch, you may find it helpful to use

```shell
python setup-nightly.py develop
```

instead because it will greatly simplify the constant reinstallation of the package.

## Usage

It is important to note that this package was designed specifically for getting releases out as soon as possible when modeling is important. During the COVID-19 pandemic, this strategy allowed epispot to  distribute versions quickly on PyPI; additionally, this package is used to ship `alpha` releases and other unstable code that is currently being developed in the epispot repository. `beta`-tagged releases and release candidates will be published on the [stable package](https://pypi.org/project/epispot/).

Please also note that security updates are not provided on previous nightly versions. To make sure that your version has no vulnerabilities, upgrade to the latest published version regularly. The latest version of the nightly package is the one that is maintained by our development team.

## Getting Started

Make sure you are already familiar with [epispot](https://www.pypi.org/project/epispot). If not, continue reading the auto-generated documentation published to this site. Additionally, we highly recommend reading the [epispot manual](https://epispot.gitbook.io) to get a better understanding of the documentation and how to use epispot.

## Current Statuses

Please note that these statuses reflect the most recent CI checks and are not related to this specific version. The following statuses show the progress of the current development.

| Pipeline | Status |
| --- | --- |
| Build (3.7-3.9) | [![Build](https://github.com/epispot/epispot/actions/workflows/build.yml/badge.svg)](https://github.com/epispot/epispot/actions/workflows/build.yml) |
| CodeCov | [![codecov](https://codecov.io/gh/epispot/epispot/branch/master/graph/badge.svg?token=WGIM127RFY)](https://codecov.io/gh/epispot/epispot) |
| PyPI main (latest) | ![latest-release](https://shields.mitmproxy.org/pypi/v/epispot.svg?color=success) |
| PyPI nightly (latest) | ![latest-release](https://shields.mitmproxy.org/pypi/v/epispot-nightly.svg?color=success) |

## Contributing

Contributions are always welcome!
See [CONTRIBUTING.md](https://github.com/epispot/epispot/tree/master/CONTRIBUTING.md) for instructions on how to get started, including environment setup and instructions to build from the source. Please note also that epispot has many guides dedicated to certain types of
contributions. Please see

- [DOCUMENTATION.md](https://github.com/epispot/epispot/tree/master/DOCUMENTATION.md) for documentation additions
- [SECURITY.md](https://github.com/epispot/epispot/tree/master/SECURITY.md) for epispot's security policy
  
### Thank you to all contributors!

---

![epispot's open-source contributors](https://contrib.rocks/image?repo=epispot/epispot)

Made with [contributors-img](https://contrib.rocks).
