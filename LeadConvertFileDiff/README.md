## Getting Started

Many a times we use different CI tools to deploy the LeadConvertMapping file from one org to another.
If these CI tools, do not provide granular access to select which field mapping to deploy, we may end-up erroneously deploying mapping of fields that haven't been deployed or worse, mapping of some fields still in development. If the formatting of the file (`LeadConvertSettings.LeadConvertSetting-meta.xml`) in your CI tool and your Git is not the same, it can become tedious to understand which fields mappings have been deployed. 
Follow the below steps to run this script for your desired GIT repository.

### Prerequisites
These below commands and script is for the Mac OS only.

You should have Python3 installed on your machine and set up in your environment variables. [Link to installation](https://www.python.org/downloads) | [Link to setup](https://docs.python-guide.org/starting/install3/osx/)


### Installing
Remove .example extension from config.py

Run the command `pip install -r requirements.txt` to install all Python dependencies

Generate a Github Personal Access Token at https://github.com/settings/tokens.
Steps:
1) Give name = `LeadConvertFileDiffApp`
2) Scopes : all scopes under `repo` and `user` only.
3) Save
4) Copy the token in  `config.py`

In `config.py` generate the `SALESFORCE_GIT_REPO` parameter.

### Execution
In Terminal navigate to the LeadConvertFileDiff base folder and execute the following command
`python3 LeadConvertFileDiffTenator.py <PR_NUMBER>`

---
### Sample Execution
```
python3 LeadConvertFileDiffTenator.py 4327
Found It!
----------fieldsDeleted------
['Contact.Some_Field_On_Contact5__c']
----------fieldsAdded------
['Account.Some_Field_On_Account1__c',
 'Account.Some_Field_On_Account2__c',
 'Contact.Some_Field_On_Contact1__c',
 'Contact.Some_Field_On_Contact2__c',
 'Contact.Some_Field_On_Contact3__c',
 'Contact.Some_Field_On_Contact4__c',
]
----------fieldMappingChanged------
[]
```