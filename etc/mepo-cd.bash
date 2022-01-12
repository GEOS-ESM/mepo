function usage_ () {
    echo "usage: "
    echo "       mepo-cd             : cd to root of mepo project"
    echo "       mepo-cd <component> : cd to directory of <component>"
    echo ""
    echo "mepo-cd accepts only 0 or 1 arguments"
}

function mepo-cd () {
    if [ "$#" -gt 1 ]; then
        usage_
        return 1
    fi
    if [ "$1" == "-h" ]; then
       usage_
       return 0
    fi
    if [ "$#" -eq 0 ]; then
       output=$(mepo whereis _root)
    else
       output=$(mepo whereis -i $1)
    fi
    if [ $? -eq 0 ]; then
        cd $output
    fi
}
