class StateDoesNotExistError(SystemExit):
    """Raised when the mepo state does not exist"""
    pass

class StateAlreadyInitializedError(SystemExit):
    """Raised when the mepo state has already been initialized"""
    pass

class RepoAlreadyClonedError(SystemExit):
    """Raised when the repository has already been cloned"""
    pass

class ConfigFileNotFoundError(FileNotFoundError):
    """Raised when the config file is not found"""
    pass

class SuffixNotRecognizedError(RuntimeError):
    """Raised when the config suffix is not recognized"""
    pass
