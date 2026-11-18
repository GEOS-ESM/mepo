# mepo [![Actions Status](https://github.com/pchakraborty/mepo/workflows/Unit%20testing%20of%20mepo/badge.svg)](https://github.com/pchakraborty/mepo/actions) [![DOI](https://zenodo.org/badge/215067850.svg)](https://zenodo.org/badge/latestdoi/215067850) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/GEOS-ESM/mepo)

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

## Configuration

User settings live in `~/.mepoconfig`. See the [example configuration](etc/mepoconfig-example) for directory styles, command aliases, partial clones, and Git retry settings. You can edit the file directly or use `mepo config set section.option value`.

### Git transport retries

Mepo retries recognized transient network failures during clone, checkout, pull, and fetch, including those run by `mepo develop`. Read-only operations such as status and diff also retry when a partial clone needs to fetch missing objects. Missing branches/tags, authentication failures, merge conflicts, and other non-transport errors are not retried. Push, commit, and stash-changing operations are not automatically retried.

The defaults are:

```ini
[git]
attempts = 6
verbose = false
```

`attempts` counts the initial attempt, with a minimum of 1. Retries wait 5, 10, 15, ... seconds; the default allows five retries with 75 seconds of backoff in total, plus Git execution time. Set `attempts = 1` to disable retries. Retry detection currently recognizes English Git/SSH diagnostics only.

To configure retries and enable diagnostics for retried commands:

```sh
mepo config set git.attempts 6
mepo config set git.verbose true
```

Intermediate failures and retry notices are hidden by default. `mepo clone --verbose` (or `-v`) enables them for that clone invocation, including its post-clone checkout. Components that needed clone retries show `[N retries]` in the clone summary.

Retry-enabled commands use an SSH connection timeout of 20 seconds unless `GIT_SSH_COMMAND` is already set. This is a connection timeout, not a limit on the whole Git operation. Retry cleanup only removes a new clone's incomplete directory, never an existing repository or the repository during post-clone checkout retries.

**Upgrading from 2.5.0:** Move any `attempts` and `verbose` settings from `[clone]` to `[git]`; the old locations are no longer read. Partial-clone settings remain under `[clone]` as `partial`.

## Presentation

The SI Team has made a PowerPoint about `mepo` that can be found [here](https://github.com/GEOS-ESM/mepo/wiki/files/MEPO-2020Nov19.pptx).

## Contributing

Please check out our [contributing guidelines](CONTRIBUTING.md).

## License

All files are currently licensed under the Apache-2.0 license, see [`LICENSE`](LICENSE).

Previously, the code was licensed under the [NASA Open Source Agreement, Version 1.3](LICENSE-NOSA).
