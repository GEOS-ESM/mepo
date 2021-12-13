# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

### Added

### Changed

- When running `mepo compare` and `mepo status`, detatched branches will also display the commit id:
```
GEOSgcm_GridComp       | (b) feature/aogcm (DH, 0793f7b2)
```

### Removed

## [1.38.0] - 2021-09-10

### Added

- Added `CHANGELOG.md`
- Added changelog enforcer

### Changed

- Detach branches on clone

## [1.37.1] - 2021-09-02

### Fixed

- Fix for `mepo save`

## [1.37.0] - 2021-08-19

### Added

* Allows `mepo checkout -b <branch>` to run on all repos rather than requiring one to be specified

### Fixed

* Fixes a bug in handling paths with spaces in folder names

## [1.36.1] - 2021-08-19

### Changed

- Make the `mepo pull` and `mepo pull-all` commands verbose by default
  - The older, quieter behavior can be gotten by adding the new `--quiet` option to `pull` and `pull-all`

## [1.36.0] - 2021-06-23

### Fixed

- Fix bug in `mepo save`

### Added

- Allow use of `hash:` key in `components.yaml`

## [1.35.0] - 2021-06-10

### Changed

- Allow `checkout` on all repos

## [1.34.1] - 2021-06-10

### Fixed

- Fix bug in `tag` subcommand

## [1.34.0] - 2021-05-27

### Changed

- The `fetch-all` command is removed and "subsumed" into the `fetch` command.

- The `push-all` command was removed

### Added

- Add script that aids in making the [Mepo Commands](https://github.com/GEOS-ESM/mepo/wiki/Mepo-Commands) wiki page. For Markdown reasons, some of the Argparse parsers had to be changed to better work with Markdown syntax.

## [1.33.0] - 2021-05-26

### Fixed

- Obey config file for no style. Previously, if no style was passed into mepo, by default it chose prefix. This is fine for GEOSgcm, etc. but broke MAPL which uses naked.  For now, if no style is found passed in on the command line or in `.mepoconfig` assume what is in `components.yaml` is the correct sytle.

## [1.32.0] - 2021-05-25

### Changes

- Changes to tag subcommand
  - `mepo tag push` instead of `mepo push --tags`

## [1.31.0] - 2021-05-25

### Added

- Add mepo style support
- Add support for `.mepoconfig` file
- Created `mepo push-all`

### Changed

- Allow `mepo tag create` and `mepo tag delete` to work on all components

### Fixed

- Fixes to `mepo status`

## [1.30.1] - 2021-03-30

### Added

- Added `-q` flag for commands with `--quiet`

## [1.30.0] - 2021-03-30

### Changed

- Detect illegal `components.yaml`
- Added useful prints to `checkout` and `develop`

## [1.29.1] - 2021-03-19

### Changed

- Clean up for `mepo save`

## [1.29.0] - 2021-03-16

### Fixed

- Fix for `mepo clone`
- Fixes for `status` and `compare`

## [1.28.1] - 2021-01-05

### Fixed

- Fix bug in `mepo status`
- Clean up odd `save` issue

## [1.28.0] - 2020-11-20

### Added

- Add `mepo commit -a`

## [1.27.1] - 2020-11-20

### Fixed

- Fixed bug when doing `mepo clone URL` *without* `--config`.

## [1.27.0] - 2020-11-20

### Fixed

- Fix for using `config` with "all-in-one" clone

## [1.26.0] - 2020-11-17

### Added

- Added `--force` flag for `fetch` and `fetch-all`

## [1.25.0] - 2020-11-12

### Added

- Add `--staged` option to `mepo diff`

## [1.24.0] - 2020-11-09

### Fixed

- Fix for fixture initialization

## [1.23.1] - 2020-10-30

### Fixed

- Fixed bug for CI systems

## [1.23.0] - 2020-10-30

### Added

- Add ability to see fixture (see release notes for more)

## [1.22.0] - 2020-10-30

### Added

- Add `mepo-cd.csh`

## [1.21.1] - 2020-10-30

### Fixed

- Fixes for `whereis` and `diff`

## [1.21.0] - 2020-10-28

### Fixed

- Updates to allow mepo clones to be moved (#106)
- A bit of nicety on `mepo status` for detatched HEAD states
- Adds `mepo-cd.zsh` as I couldn't figure out how to get the bash script to work in zsh

## [1.20.1] - 2020-10-07

### Fixed

- Bug fixes for `mepo save`
  - The command would save the new yaml file in `pwd` rather than at the "root" directory where the original was. This was a bit confusing, so the command now saves at root level
  - `mepo save` did not handle hashes well. There is no reason it couldn't save to a hash, but it labeled it as a `branch` in the yaml file which, while not broken, was in consistent.

## [1.20.0] - 2020-09-01

### Added

- Add `dry-run` for `checkout-if-exists`

## [1.19.0] - 2020-08-26

### Added

- Add per-repo diff

## [1.18.0] - 2020-08-19

### Added

- Added `mepo tag` commands
- Added `.zenodo.json` file

### Changed

- Update `mepo branch list` to work on one or more repos

## [1.17.0] - 2020-08-18

### Added

- Add `restore-state` command
  - Note: at present this will restore *EVERYTHING* to the previous state. Not a repo here or there.

## [1.16.0] - 2020-07-17

### Added

- Add `pull`, `pull-all` and `fetch-all`

### Fixed

- Fix `.mepo` file on Darwin

## [1.15.0] - 2020-07-14

### Changed

- Updates to `clone` command

## [1.14.1] - 2020-07-08

### Fixed

- Fix for `mepo push`

## [1.14.0] - 2020-06-23

### Added

- Add `mepo stash`

## [1.13.0] - 2020-06-15

### Changed

- Updates for `clone` and `fetch` commands

### Fixes

- `mepo status` won't crash if a repo is not on a tag or branch

## [1.12.0] - 2020-06-01

### Changed

* Update the CI to use a matrix on Linux and macOS of python3.x and pypy3

### Fixed

* Fix the unit tests

## [1.11.0] - 2020-05-28

### Added

- Add license

## [1.10.1] - 2020-05-27

### Fixed

- Fix bad shebang

## [1.10.0] - 2020-05-27

### Changed

- Add to `mepo-cd` functionality

## [1.9.0] - 2020-04-07

### Added

- Add `mepo fetch` and `mepo fetch --all` ability.

## [1.8.0] - 2020-03-04

### Changed

- Add ability for single editor for multi-repo commit

## [1.7.0] - 2020-03-03

### Added

* Add `--name-only` to `mepo diff`
* Add colors to `mepo status` for non-original branches
* Make `checkout-if-exists` more verbose
* Make `mepo commit` act more like `git commit`

## [1.6.0] - 2020-02-19

### Added

- Add `checkout-if-exists` capability

## [1.5.0] - 2020-02-07

### Added

- Add ability to work with symlinks

## [1.4.0] - 2020-01-28

### Added

- Add the ability to have `recurse_submodules:` in the YAML file.

## [1.3.0] - 2020-01-16

### Added

- Add `mepo diff` command
- Add `CODEOWNERS`

## [1.2.0] - 2020-01-09

### Changed

- Updates to `status` and `compare`

### Added

- Add `mepo-cd` bash function

## [1.1.0] - 2019-12-19

### Added

- Add GitHub Action for unit tests
- Add README
- Add `develop` command

### Changed

- Lots of updates to internals

## [1.0.0] - 2019-12-08

### Changed

- Initial release of mepo

## [0.4] - 2019-11-12

### Added

- Add stage and unstage

## [0.3] - 2019-11-06

### Added

- Add init, clone, status, checkout, branch, diff, where, whereis, history, stage

## [0.2] - 2019-11-01

### Added

- Add init, clone, status, checkout, branch, diff, where

## [0.1] - 2019-10-28

### Added

- Add checkout and status