# mepo [![Actions Status](https://github.com/{pchakraborty}/{mepo}/workflows/{Unit testing of mepo}/badge.svg)](https://github.com/{owner}/{repo}/actions)
`mepo` is a tool to manage (m)ultiple git r(epo)sitories, by attempting to create an illusion of a 'single repository' for multi-repository projects. A typical `mepo` workflow, using the fixture [GEOSgcm](https://github.com/GEOS-ESM/GEOSgcm) and its compoments, [fvdycore](https://github.com/GEOS-ESM/GFDL_atmos_cubed_sphere), [MAPL](https://github.com/GEOS-ESM/MAPL), can be

### Clone
#### Clone top level fixture
```shell
git clone -b v10.3.5 git@github.com:GEOS-ESM/GEOSgcm.git v10.3.5
```
#### Clone components
```shell
cd v10.3.5
mepo init # if repolist.yaml does not exist, run 'mepo init /path/to/repolist.yaml'
mepo clone # checkout components
```
TIP: run `mepo list` for a list of components

TIP: run `mepo whereis <component>` for the location of the component

### Create and checkout new feature branches
For example, create and checkout (from detached head) feature branch `feature/<username>/feature-dev` in components `MAPL`, and `fvdycore`
```shell
mepo checkout -b feature/<username>/feature-dev fvdycore MAPL
```
The above command is equivalent to running the following two commands
```shell
mepo branch create feature/<username>/feature-dev fvdycore MAPL
mepo checkout feature/<username>/feature-dev fvdycore MAPL
```
TIP: run `mepo compare` to compare the current state with the original/last saved state

### Develop and commit changes on feature branches
Edit files in each component. Then stage and commit *all* changes (across components)
```shell
mepo status # check status of every component
mepo stage fvdycore MAPL
mepo commit "commit message" fvdycore MAPL
```

### Merge
The first step in the merge process is to catch up with the latest changes in the `develop` branches of each component. This step still needs to be done manually, using `git` commands. For our example, `for component in ['fvdycore', 'MAPL']`, do
```shell
cd $(mepo whereis <component>)
git checkout <develop-branch>
git checkout feature/<username>/feature-dev
git merge <develop-branch>
```
Next, push the feature branches to remote
```shell
mepo push fvdycore MAPL
```
Finally, go to the GitHub location of each component and issue PRs. This step of issuing PRs can probably be handled by `mepo` at some point.

### Save state
`mepo` works by reading a list of components (default: repolist.yaml) and saving it as an internal state. All subsequent mepo commands work off that saved state. At any point during the development stage, the current state can be saved by running
```shell
mepo save
```
This updates the internal state as well as creates a new component list `repolist-new.yaml` that can be shared with others. A restriction for running the `save` command is that all local changes have been pushed to remote (i.e. (a) all local branches have a corresponding remote branch and (b) the latest commit ids of the local and remote branches must match).
