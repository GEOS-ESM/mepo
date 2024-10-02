# mepo [![Actions Status](https://github.com/pchakraborty/mepo/workflows/Unit%20testing%20of%20mepo/badge.svg)](https://github.com/pchakraborty/mepo/actions) [![DOI](https://zenodo.org/badge/215067850.svg)](https://zenodo.org/badge/latestdoi/215067850) [![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye-up.com)

`mepo` is a tool, written in Python3, to manage (m)ultiple git r(epo)sitories, by attempting to create an illusion of a 'single repository' for multi-repository projects. Please see the [Wiki](../../wiki) for examples of `mepo` workflows.


## Installation

### Using pip

To install `mepo` using `pip`, run the following command:

```
pip install mepo
```

### Homebrew

Using Homebrew, you can install `mepo` by installing from the gmao-si-team tap:

```
brew install gmao-si-team/packages/mepo
```

This is equivalent to running:

```
brew tap gmao-si-team/packages
brew install mepo
```

### Spack

Mepo is also available via spack as a package. To install mepo using spack, run the following command:

```
spack install mepo
```

## Transitioning from `mepo` v1.x to v2.x

If you try to use mepo v2.x within a mepo v1.x repository, you will get an warning message:
```
Detected mepo1 style state
Run <mepo update-state> to permanently convert to mepo2 style
```

To update your repository to work with mepo v2.x, you can run the following command:
```
mepo update-state
```
and it will convert the repository from mepo v1 pickle-state to mepo v2 json-state.

## Commands

For more about the possible `mepo` commands, please see the [Mepo Commands](https://github.com/GEOS-ESM/mepo/wiki/Mepo-Commands) wiki page.

## Presentation

The SI Team has made a PowerPoint about `mepo` that can be found [here](https://github.com/GEOS-ESM/mepo/wiki/files/MEPO-2020Nov19.pptx).

## Contributing

Please check out our [contributing guidelines](CONTRIBUTING.md).

## License

All files are currently licensed under the Apache-2.0 license, see [`LICENSE`](LICENSE).

Previously, the code was licensed under the [NASA Open Source Agreement, Version 1.3](LICENSE-NOSA).
