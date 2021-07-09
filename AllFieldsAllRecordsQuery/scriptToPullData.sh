
main(){
    function_create_tmp_dir
    function_instantiate_global_variables $line
    function_to_get_all_fields_for_object $objectToQuery
    function_to_call_pythonscript_to_constuct_soqls $objectToQuery
    function_validate_record_count_and_query_records $objectToQuery
    function_destroy_tmp_dir
}

function_create_queried_recs_folder_if_not_exist(){
    mkdir -p queriedRecords
}

function_create_tmp_dir(){
    mkdir ".tmp"
}

function_destroy_tmp_dir(){
    rm -r ".tmp"
}

function_instantiate_global_variables(){
    objectToQuery=$line
    sandboxAlias='ShriDev'
    csFieldsTempFileName='.tmp/csFieldValues.txt'
    MAX_RECORD_COUNT_PERMISSIBLE=3000
}

function_to_get_all_fields_for_object(){
    #Command to pull schema and create a comma separated string with
    sfdx force:schema:sobject:describe -s $1 -u $sandboxAlias --json | jq '.result.fields[].name' | awk -v ORS=, '{ print $1 }' | sed 's/,$//' | sed 's/\"//g' | tr -d '\n' > $csFieldsTempFileName
}

function_to_call_pythonscript_to_constuct_soqls(){
    python3 createSOQL.py $csFieldsTempFileName $1
}

function_to_validate_record_count(){
    local countSOQL=$(< ".tmp/countSOQL.txt")

    echo $countSOQL

    local totalRecordsCount=`sfdx force:data:soql:query -u $sandboxAlias -q "$countSOQL" --json | jq '.result.records[0].expr0'`
    echo "TotalRecordCount=$totalRecordsCount"
    echo "Argumentpassed=$1"
    if ((($totalRecordsCount < $1) && ($totalRecordsCount != 0)))
    then
        return 0
    else
        return 1
    fi
}

function_read_actualSOQL_file_to_variable(){
    actualSOQL=$(< ".tmp/actualSOQL.txt")
    echo "Read actualSOQL to variable=$actualSOQL"
}

function_to_query_object_records(){
    echo "queryingActualdata for $1"
    function_read_actualSOQL_file_to_variable
    echo "actualSOQL = $actualSOQL"
    `sfdx force:data:soql:query -u $sandboxAlias -q "$actualSOQL" --json > "queriedRecords/${1}.json"`
}

function_validate_record_count_and_query_records(){
    if function_to_validate_record_count $MAX_RECORD_COUNT_PERMISSIBLE
    then 
        function_to_query_object_records $1
        echo "Completed retrieval for $1"
    else
        echo "No records, or more than $MAX_RECORD_COUNT_PERMISSIBLE records found for $1. Exiting"
    fi
}

# below line reads the object list and iterates through it one by one
cat objListToQuery.txt | while read line || [ -n "$line" ]; do main $line; done
