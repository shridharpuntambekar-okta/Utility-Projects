pathToBaseSFDXFolder="<insert_complete_path_to_this_directory>"  #"/Users/shridharpuntambekar/.."

batchSize=7000

cd $pathToBaseSFDXFolder
if [ -d $pathToBaseSFDXFolder"/manifest" ] 
then
    echo "Directory $pathToBaseSFDXFolder/manifest exists." 
else
    echo "Directory $pathToBaseSFDXFolder/manifest does not exist."
    mkdir manifest
    touch manifest/package.xml
    echo "Directory created"
fi
pwd

cd RetrieveReportsMetadata/GetReportsXML
python3 genReportXML.py
totalReportCount=$(< "totalReportCount.txt")
echo totalReportCount $totalReportCount
echo batchSize $batchSize
totalIterations=$((($totalReportCount / $batchSize)+1))
echo totalIterations $totalIterations
cd ..

# Offset should be less than 10,000 items or 400MB as that is the limit specified by SFDX
# https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_force_mdapi.htm
# Keep offset ~6000
# Setting offset as 100 for demo purposes

echo "0,$batchSize" > offset.txt
for ((n=0;n<$totalIterations;n++))
do
    python3 $pathToBaseSFDXFolder"/RetrieveReportsMetadata/execCommand.py" $pathToBaseSFDXFolder
    sfdx force:source:retrieve -u ShriDevOrg -x $pathToBaseSFDXFolder"/manifest/package.xml"
done


for ((n=0;n<$totalIterations;n++))
do
    python3 $pathToBaseSFDXFolder"/RetrieveReportsMetadata/execCommand.py" $pathToBaseSFDXFolder
    # Pre-Requisite is to authenticate the org with SFDX with the below command
    # sfdx force:auth:web:login -r https://test.salesforce.com -a <alias_for_the_connection>
    # Supply the created alias to the command below "sfdx force:.. -u <alias_for_the_connection> .."
    sfdx force:source:retrieve -u ShriDevOrg -x $pathToBaseSFDXFolder"/manifest/package.xml"
done

