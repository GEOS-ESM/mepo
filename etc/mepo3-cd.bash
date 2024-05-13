function usage_ () {
    echo "usage: "
    echo "       mepo3-cd             : cd to root of mepo3 project"
    echo "       mepo3-cd <component> : cd to directory of <component>"
    echo ""
    echo "mepo3-cd accepts only 0 or 1 arguments"
}

function mepo3-cd () {
    if [ "$#" -gt 1 ]; then
        usage_
        return 1
    fi
    if [ "$1" == "-h" ]; then
       usage_
       return 0
    fi
    if [ "$#" -eq 0 ]; then
       output=$(python -m mepo3 whereis _root)
    else
       output=$(python -m mepo3 whereis -i $1)
    fi
    if [ $? -eq 0 ]; then
        cd $output
    fi
}
