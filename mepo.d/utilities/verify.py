def valid_repos(specified_repos, allrepos):
    for reponame in specified_repos:
        if reponame not in allrepos:
            raise Exception('Unknown repo name [{}]'.format(reponame))
