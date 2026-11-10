#compdef mepo
#
# Zsh completion for mepo: commands, sub-commands (e.g. mepo branch create),
# options, option values, aliases from ~/.mepoconfig and component names,
# with descriptions.
#
# Usage: add to ~/.zshrc, after compinit has run
#     source /path/to/mepo/etc/mepo-completion.zsh
#
# Candidates come from `mepo __complete`, which reads mepo's own argument
# parser, so this script never needs updating when commands change.

_mepo() {
    local -a lines candidates
    local line name desc
    lines=("${(@f)$(command mepo __complete "${(@)words[2,CURRENT]}" 2>/dev/null)}")

    if [[ ${lines[1]} == ":files" ]]; then
        _files
        return
    fi

    for line in "${lines[@]}"; do
        [[ -z $line ]] && continue
        name=${line%%$'\t'*}
        desc=${line#*$'\t'}
        name=${name//:/\\:}  # ':' separates name and description for _describe
        if [[ -n $desc && $desc != $line ]]; then
            candidates+=("$name:$desc")
        else
            candidates+=("$name")
        fi
    done

    (( ${#candidates} )) && _describe -t mepo 'mepo' candidates
}

if [[ $zsh_eval_context[-1] == loadautofunc ]]; then
    # Autoloaded from $fpath (file installed as _mepo)
    _mepo "$@"
else
    # Sourced
    (( $+functions[compdef] )) || { autoload -Uz compinit && compinit }
    compdef _mepo mepo
fi
