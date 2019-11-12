#!/usr/bin/env bash

# complete -W "init clone status checkout branch diff where whereis history" mepo

_get_mepo_commands() {
    local mepo_cmd_list=""
    local mepodir=$(dirname $(which mepo))
    for mydir in $(ls -d ${mepodir}/mepo.d/command/*/); do
        mepo_cmd_list+=" $(basename $mydir)"
    done
    echo ${mepo_cmd_list}
}

_mepo_completions() {
    mepo_commands=$(_get_mepo_commands)
    COMPREPLY=($(compgen -W "${mepo_commands}" "${COMP_WORDS[1]}"))
}

complete -F _mepo_completions mepo
