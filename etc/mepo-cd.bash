function usage_ () {
    echo "usage: mepo-cd <component>"
}

function mepo-cd () {
    if [ "$#" -ne 1 ]; then
        usage_
        return 1
    fi
    if mepo whereis $1; then
       cd $(mepo whereis $1)
    else
       return 1
    fi
}
