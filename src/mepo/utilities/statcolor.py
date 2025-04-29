from . import colors


def red(string):
    return colors.RED + string + colors.RESET


def blue(string):
    return colors.BLUE + string + colors.RESET


def cyan(string):
    return colors.CYAN + string + colors.RESET


def green(string):
    return colors.GREEN + string + colors.RESET


def yellow(string):
    return colors.YELLOW + string + colors.RESET


def get_ordinary_change_status(short_status):
    unstaged_ = " with " + red("unstaged changes")
    deleted_unstaged_ = " but " + red("deleted, not staged")
    d = {
        # unstaged changes
        ".D": red("deleted, not staged"),
        ".M": red("modified, not staged"),
        ".A": red("added, not staged"),
        ".T": red("typechange, not staged"),
        # staged changes
        "D.": green("deleted, staged"),
        "M.": green("modified, staged"),
        "A.": green("added, staged"),
        "T.": green("typechange, staged"),
        # modified staged ...
        "MM": green("modified, staged") + unstaged_,
        "MD": green("modified, staged") + deleted_unstaged_,
        # added staged ...
        "AM": green("added, staged") + unstaged_,
        "AD": green("added, staged") + deleted_unstaged_,
        # typechange staged ...
        "TM": green("typechange, staged") + unstaged_,
        "TD": green("typechange, staged") + deleted_unstaged_,
    }
    return d[short_status]


def get_renamed_copied_status(short_status, new_file_name):
    new_file_name_ = " as " + yellow(new_file_name)
    unstaged_ = " with " + red("unstaged changes")
    deleted_unstaged_ = " but " + red("deleted, not staged")
    d = {
        # renamed
        "R.": green("renamed") + new_file_name_,
        "RM": green("renamed, staged") + new_file_name_ + unstaged_,
        "RD": green("renamed, staged") + new_file_name_ + deleted_unstaged_,
        # copied
        "C.": green("copied") + new_file_name_,
        "CM": green("copied, staged") + new_file_name_ + unstaged_,
        "CD": green("copied, staged") + new_file_name_ + deleted_unstaged_,
    }
    return d[short_status]
