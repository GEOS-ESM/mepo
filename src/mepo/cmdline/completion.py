"""Shell completion for mepo.

The shell scripts in etc/ (mepo-completion.bash, mepo-completion.zsh) call

    mepo __complete <word> ... <current-word>

with the words typed after `mepo`, the last one being the (possibly empty)
word under the cursor. Candidates are derived from the argparse parser itself,
so sub-commands, options and aliases from ~/.mepoconfig are always current.

Output protocol (one candidate per line):
    <candidate>\t<description>   description may be empty
    :files                        (single line) shell should complete file names
Filtering by the current word's prefix is left to the shell.
"""

import argparse
import json
import re
import warnings

FILES = ":files"

# Positional/option destinations whose values are file or directory names
_FILE_DESTS = {"registry", "directory"}
# Positional destinations whose values are mepo component names
_COMP_DESTS = {"comp_name"}


def _subparsers_action(parser):
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action
    return None


def _find_option(parser, option_string):
    return parser._option_string_actions.get(option_string)


def _short(text):
    """First sentence of text, on one line"""
    if not text or text == argparse.SUPPRESS:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0].rstrip(".")


def _option_help(action):
    try:
        params = dict(vars(action), prog="mepo")
        if params.get("choices") is not None:
            params["choices"] = ", ".join(str(c) for c in action.choices)
        return _short(action.help % params)
    except (TypeError, KeyError, ValueError):
        return _short(action.help)


def _component_names():
    """Component names from the mepo state, empty if not in a mepo clone"""
    from ..state import MepoState

    try:
        with open(MepoState.get_file(), "r") as fin:
            return [comp["name"] for comp in json.load(fin)]
    except (OSError, ValueError, KeyError, TypeError):
        return []


def _subcommands(subparsers):
    canonical = {}  # id(parser) -> name; add_parser registers the name before aliases
    for name, parser in subparsers.choices.items():
        canonical.setdefault(id(parser), name)
    out = []
    for name, parser in subparsers.choices.items():
        main_name = canonical[id(parser)]
        if name == main_name:
            out.append((name, _short(parser.description)))
        else:
            out.append((name, f"alias for {main_name}"))
    return out


def _options(parser, used):
    out = []
    for action in parser._actions:
        if not action.option_strings or action.help == argparse.SUPPRESS:
            continue
        if any(opt in used for opt in action.option_strings):
            continue
        desc = _option_help(action)
        for opt in action.option_strings:
            out.append((opt, desc))
    return out


def _positional_action(parser, index):
    """Positional action that the index-th positional word belongs to"""
    for action in parser._actions:
        if action.option_strings or isinstance(action, argparse._SubParsersAction):
            continue
        if action.nargs in ("*", "+", argparse.REMAINDER):
            return action
        count = action.nargs if isinstance(action.nargs, int) else 1
        if index < count:
            return action
        index -= count
    return None


def _values(action, already):
    if action is None:
        return []
    if action.choices:
        return [(str(c), "") for c in action.choices if c is not None]
    if action.dest in _FILE_DESTS:
        return FILES
    if action.dest in _COMP_DESTS:
        return [(name, "") for name in _component_names() if name not in already]
    return []


def candidates(words):
    """Return list of (candidate, description) tuples, or FILES"""
    from .parser import MepoArgParser

    if not words:
        words = [""]
    *previous, current = words

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        parser = MepoArgParser().build()

    positionals = []
    used_options = set()
    pending = None  # option waiting for its value
    for word in previous:
        if pending is not None:
            pending = None
            continue
        if word.startswith("-") and word != "-":
            option, has_value = word.split("=", 1)[0], "=" in word
            used_options.add(option)
            action = _find_option(parser, option)
            if action is not None and action.nargs != 0 and not has_value:
                pending = action
            continue
        subparsers = _subparsers_action(parser)
        if subparsers is not None and word in subparsers.choices:
            parser = subparsers.choices[word]
            positionals, used_options = [], set()
            continue
        positionals.append(word)

    if pending is not None:
        return _values(pending, positionals)
    if current.startswith("-"):
        return _options(parser, used_options)
    subparsers = _subparsers_action(parser)
    if subparsers is not None:
        return _subcommands(subparsers)
    return _values(_positional_action(parser, len(positionals)), positionals)


def main(words):
    try:
        result = candidates(words)
    except Exception:  # completion must never blow up in the user's shell
        return
    if result == FILES:
        print(FILES)
        return
    for name, desc in result:
        print(f"{name}\t{desc}")
