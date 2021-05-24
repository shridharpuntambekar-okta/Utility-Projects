## Getting Started

This tool was designed to automate querying records from custom settings or (config) custom objects. Unlike custom metadata, custom settings or records of custom objects, are not versioned and hence not searchable. If such a need arises, to search through these records, we can enable the power of indexing done by any IDE to search through downloaded data.
e.g.: We need to update the API name of a particular field, and we need to do an impact analysis. If this field is part of a configuration which is stored as records in Salesforce, it is not directly searchable. In such a case, we can download the data from such config objects, on our local machines, and simple use any IDE to search for that field API name.

### Prerequisites
These below commands and script is for the Mac OS only.

You should have the Salesforce CLI (SFDX) installed on your machine. [Link to installation](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_install_cli.htm#sfdx_setup_install_cli)

You should have Python3 installed on your machine and set up in your environment variables. [Link to installation](https://www.python.org/downloads) | [Link to setup](https://docs.python-guide.org/starting/install3/osx/)


### Installing
* Execute command `brew install jq`

* Open command line and navigate to the relevant folder.
  Authenticate the desired environment by SFDX with the following command:
  ```
  sfdx force:auth:web:login -a <relevant_org_alias>
  ```

**Example** : `sfdx force:auth:web:login -a ShriDevOrg`

* Verify the authentication by running the following command:
  ```
  sfdx force:org:list
  ```

* Populate the authenticated org alias to the `sandboxAlias` variable on line 21 of `scriptToPullData.sh` 

* Populate the desired objects to query in the `objListToQuery.txt` file. Use API names of objects and one per line. Remove whitespaces and new lines.

---
### Execution

* To execute navigate to the base folder in terminal and enter following command:

`chmod +x scriptToPullData.sh`
`source scriptToPullData.sh`

---

* MAX_RECORD_COUNT_PERMISSIBLE parameter on line 23 of `scriptToPullData.sh` is number used to restrict this tool for custom settings and config object records. This is not a strict limit and can be increased. (Please note the limitation of the SFDX query command. It can timeout for too many records or too large a size of the file )
* The `createSOQL.py` uses a pre-defined list of System fields (viz. SystemModStamp) that are excluded from the query. You can update the variable set in the file, if you need these fields as well.



