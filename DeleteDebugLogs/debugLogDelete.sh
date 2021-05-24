sfdx force:data:soql:query -q "SELECT Id from ApexLog" -r "csv" > delDebugLog.csv -u ShriDevOrg
sfdx force:data:bulk:delete -s ApexLog -f delDebugLog.csv -u ShriDevOrg