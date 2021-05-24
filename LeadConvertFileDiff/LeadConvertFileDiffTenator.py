from github import Github
from config import GIT_ACCESS_TOKEN, SALESFORCE_GIT_REPO, LEAD_CONVERT_FILE_PATH
import os
import urllib.parse as urlparse
from urllib.parse import parse_qs
import sys
import xmltodict
import pprint


class LEADCONVERT_FILE_NOT_FOUND(Exception):
    pass

def writeBinaryStringToFile(filename, binaryString):
    tempFile = open(filename, "wb")
    tempFile.write(binaryString)
    tempFile.close()

def retrievePRandFileContents(prToProcess):
    # Get the access token stored in config.py
    g = Github(GIT_ACCESS_TOKEN)
    # Get out the Salesforce Repo
    repo = g.get_repo(SALESFORCE_GIT_REPO)
    # Get the particular PR 
    # TODO: Add a validation to see if such a PR exists also, if OPEN | CLOSED | Passed CI Validation?
    pr = repo.get_pull(prToProcess)
    leadConvertFileObj=None
    for eachFile in pr.get_files():
        if eachFile.filename == LEAD_CONVERT_FILE_PATH:
            print("Found It!")
            leadConvertFileObj=eachFile
            break
    
    # If the PR does not have the LeadConvertFile raise an Exception
    if leadConvertFileObj is None:
        raise LEADCONVERT_FILE_NOT_FOUND
    
    # "ref" is the SHA of the new branch
    sourceBranchFileSHA=parse_qs(urlparse.urlparse(leadConvertFileObj.contents_url).query)['ref'][0]
    sourceBranchFileContents=repo.get_contents(path=LEAD_CONVERT_FILE_PATH, ref=sourceBranchFileSHA)

    # Retrieve the contents of our particular file, and copy into a temporary file for parsing
    # File IO can be avoided here by passing the BLOB for parsing
    writeBinaryStringToFile("tmpSourceBranchLCFile.xml", sourceBranchFileContents.decoded_content)

    # In the PR object returned by PyGithub, we get the base SHA to which the source branch is getting merged
    targetBranchFileContents=repo.get_contents(path=LEAD_CONVERT_FILE_PATH, ref=pr.base.sha)
    writeBinaryStringToFile("tmpTargetBranchLCFile.xml", targetBranchFileContents.decoded_content)

    return

def read_file_to_dict(filepath):
    with open(filepath) as fd:
        tempDict = xmltodict.parse(fd.read())
    
    return buildDictWithSourceObjKeys(tempDict)

def buildDictWithSourceObjKeys(dictToIterate):
    # We create our dictionary to make it easy to do set operations with dictionary keys.
    dictToReturn=dict()
    # Dictionary structure 
    # Input object is always LEAD.
    # {<Output_Object> : {<Input_Field> : <Output_Field> }}
    # e.g. {"Account" : {(Lead.)"XYZ__c" :  (Account.)"XYZ__c"}
    for eachObject in dictToIterate["LeadConvertSettings"]["objectMapping"]:
        lcTargetObj=eachObject['outputObject']

        if lcTargetObj not in dictToReturn:
            dictToReturn[lcTargetObj] = dict()
        
        innerFieldsDictToReturn = dictToReturn[lcTargetObj]

        for eachFieldDict in eachObject['mappingFields']:
            innerFieldsDictToReturn[eachFieldDict['inputField']] = eachFieldDict['outputField']
    
    return dictToReturn

def inverse_dictionary(incoming_dict):
    inverse_map_to_return = dict()
    for eachObjName in incoming_dict.keys():
        inverse_map_to_return[eachObjName] = {v: k for k, v in incoming_dict[eachObjName].items()}
    return inverse_map_to_return

def populate_arrays_with_field_differences(sourceLCDict, targetLCDict):
    fieldsDeleted = []
    fieldsAdded = []
    fieldMappingChanged = []
    inverseSourceFieldLCDict=inverse_dictionary(sourceLCDict)
    inverseTargetFieldLCDict=inverse_dictionary(targetLCDict)
    
    # we create inverse maps for our convenience 
    # TODO: Better logic to check if the field mapping has changed.
    for eachObjName in sourceLCDict.keys():
        # We do simple simple SET operations to verify 
        for eachDeletedField in list(sourceLCDict[eachObjName].keys()-targetLCDict[eachObjName].keys()):
            fieldsAdded.append(f"{eachObjName}.{eachDeletedField}")
        
        for eachAddedField in list(targetLCDict[eachObjName].keys()-sourceLCDict[eachObjName].keys()):
            fieldsDeleted.append(f"{eachObjName}.{eachAddedField}")

        for eachMappingChanged in list(inverseSourceFieldLCDict[eachObjName].keys()-inverseTargetFieldLCDict[eachObjName].keys()):
            actual_source_input_field=inverseSourceFieldLCDict[eachObjName][eachMappingChanged]
            actual_target_output_field=targetLCDict[actual_source_input_field] if (actual_source_input_field in targetLCDict) else None
            actual_target_input_field=actual_source_input_field if (actual_source_input_field in targetLCDict) else None
            if actual_target_output_field is not None:
                fieldMappingChanged.append(f"{eachObjName}[{actual_source_input_field}|{eachMappingChanged} --> {actual_target_input_field}|{actual_target_output_field}]")
    
    print('----------fieldsDeleted------')
    # Simple pretty print operation
    pprint.pprint(fieldsDeleted)
    print('----------fieldsAdded------')
    pprint.pprint(fieldsAdded)
    print('----------fieldMappingChanged------')
    pprint.pprint(fieldMappingChanged)
    return fieldsDeleted, fieldsAdded, fieldMappingChanged

if __name__ == "__main__":
    prToProcess = sys.argv[1]
    try:
        # Using PyGithub we get our necessary data from Github using a personal access token
        # the token has limited access to repo. (Can be controlled in GITHUB)
        retrievePRandFileContents(int(prToProcess))
    except LEADCONVERT_FILE_NOT_FOUND:
        print(f"The Lead Convert File was not changed in PR #{prToProcess}.")
        sys.exit()
    except:
        print("An error occurred during Github retrieval. Please verify if your GIT token is alive. If yes, please contact @Shridhar")
        sys.exit()

    # If both files retrieved and returned successfully, we can start parsing them
    try:
        # using xmltodict library, convert the XML to dict
        sourceLCDict = read_file_to_dict("tmpSourceBranchLCFile.xml")
        targetLCDict = read_file_to_dict("tmpTargetBranchLCFile.xml")
        fieldsDeleted, fieldsAdded, fieldMappingChanged= populate_arrays_with_field_differences(sourceLCDict, targetLCDict)
    except:
        print("An error occurred during XML parsing. Please verify if the Gearset CI job is successful for this PR. If yes, please contact @Shridhar")
        sys.exit()
