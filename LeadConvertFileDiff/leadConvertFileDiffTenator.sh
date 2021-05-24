main(){
    function_instantiate_global_variables $1
    function_to_call_pythonscript_to_validate_pr
}

function_to_call_pythonscript_to_validate_pr(){
    python3 pyGithubTest.py $prToCheck
}

function_instantiate_global_variables(){
    echo "Entered f1"
    currentDirPath=`pwd`
    prToCheck=$1
}

main $1