class StateDoesNotExistError(SystemExit):
    """Raised when the mepo state does not exist"""

    pass


class StateAlreadyInitializedError(SystemExit):
    """Raised when the mepo state has already been initialized"""

    pass


class RepoAlreadyClonedError(SystemExit):
    """Raised when the repository has already been cloned"""

    pass


class RegistryNotFoundError(FileNotFoundError):
    """Raised when the registry is not found"""

    pass


class SuffixNotRecognizedError(RuntimeError):
    """Raised when the registry suffix is not recognized"""

    pass


class NotInRootDirError(SystemExit):
    """Raised when a command is run not in the root directory"""

    pass
