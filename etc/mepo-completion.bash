#!/usr/bin/env bash
#
# Bash completion for mepo: commands, sub-commands (e.g. mepo branch create),
# options, option values, aliases from ~/.mepoconfig and component names.
#
# Usage: add to ~/.bashrc
#     source /path/to/mepo/etc/mepo-completion.bash
#
# Candidates come from `mepo __complete`, which reads mepo's own argument
# parser, so this script never needs updating when commands change.

_mepo_completions() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local IFS=$'\n'
    local -a lines
    lines=($(command mepo __complete "${COMP_WORDS[@]:1:COMP_CWORD}" 2>/dev/null))

    COMPREPLY=()
    if [[ ${lines[0]} == ":files" ]]; then
        compopt -o filenames 2>/dev/null
        COMPREPLY=($(compgen -f -- "$cur"))
        return 0
    fi

    local line name
    for line in "${lines[@]}"; do
        name=${line%%$'\t'*}
        [[ $name == "$cur"* ]] && COMPREPLY+=("$name")
    done
    return 0
}

complete -F _mepo_completions mepo
