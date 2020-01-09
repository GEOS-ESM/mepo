function usage_ () {
    echo "usage: mepo-cd <component>"
}

function mepo-cd () {
    if [ "$#" -ne 1 ]; then
        usage_
        return 1
    fi
    output=$(mepo whereis $1)
    if [ $? -eq 0 ]; then
        cd $output
    fi
}
