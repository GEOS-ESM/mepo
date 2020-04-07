#!/usr/bin/env bash

# complete -W "init clone status checkout branch diff where whereis history" mepo

_get_mepo_commands() {
    local mepo_cmd_list=""
    if [[ "$OSTYPE" == "darwin"* ]]
    then
       local mepodir=$(dirname $(readlink $(which mepo)))
    else
       local mepodir=$(dirname $(readlink -f $(which mepo)))
    fi
    for mydir in $(ls -d ${mepodir}/mepo.d/command/*/); do
        if [[ $mydir != *"__pycache__"* ]]; then
            mepo_cmd_list+=" $(basename $mydir)"
        fi
    done
    echo ${mepo_cmd_list}
}

_mepo_completions() {
    mepo_commands=$(_get_mepo_commands)
    COMPREPLY=($(compgen -W "${mepo_commands}" "${COMP_WORDS[1]}"))
}

complete -F _mepo_completions mepo
