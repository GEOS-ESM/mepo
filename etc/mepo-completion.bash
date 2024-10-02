#!/usr/bin/env bash

_get_mepo_commands() {
    local mepo_cmd_list=""
    local mepo_dir=$(python3 -c "import os, mepo; print(os.path.dirname(mepo.__file__))")
    for pyfile in $(ls ${mepo_dir}/command/*.py*); do
	command=${pyfile##*/} # remove path
	command=${command%.*} # remove extension
	command=$(echo $command | cut -d _ -f 1)
        mepo_cmd_list+=" $command"
    done
    echo ${mepo_cmd_list}
}

_mepo_completions() {
    mepo_commands=$(_get_mepo_commands)
    COMPREPLY=($(compgen -W "${mepo_commands}" "${COMP_WORDS[1]}"))
}

complete -F _mepo_completions mepo
