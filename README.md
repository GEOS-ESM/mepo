# mepo [![Actions Status](https://github.com/pchakraborty/mepo/workflows/Unit%20testing%20of%20mepo/badge.svg)](https://github.com/pchakraborty/mepo/actions) [![DOI](https://zenodo.org/badge/215067850.svg)](https://zenodo.org/badge/latestdoi/215067850) [![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye-up.com) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/GEOS-ESM/mepo)

`mepo` is a tool, written in Python3, to manage (m)ultiple git r(epo)sitories, by attempting to create an illusion of a 'single repository' for multi-repository projects. Please see the [Wiki](../../wiki) for examples of `mepo` workflows.


## Installation

### Using pip

To install `mepo` using `pip`, run the following command:

```
pip install mepo
```

### Using uv

#### uv install

You can install `mepo` using the `uv` package manager. To do so, run the following command:

```
uv tool install mepo
```

#### uvx

If you'd like to run `mepo` without installing it, you can use `uvx` to run it directly:

```
uvx mepo
```

### Homebrew

`mepo` is available from the GMAO-SI-Team Homebrew tap:

```sh
brew install gmao-si-team/packages/mepo
```

This direct install form is recommended because it tells Homebrew exactly which formula from the tap you want to install.

#### Homebrew tap trust

Newer Homebrew versions warn about formulae from non-official taps. If you enable tap trust checks, or when Homebrew begins requiring them by default, you may need to explicitly trust this formula or tap.

To trust only the `mepo` formula:

```sh
brew trust --formula gmao-si-team/packages/mepo
```

If you prefer to tap the repository first and then install by short name:

```sh
brew tap gmao-si-team/packages
brew trust gmao-si-team/packages
brew install mepo
```

Only run `brew trust` for taps or formulae whose maintainers and source repository you trust. To remove the tap later:

```sh
brew untap gmao-si-team/packages
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
