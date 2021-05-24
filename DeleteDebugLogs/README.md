## Getting Started

Follow the below steps to delete all debug logs from desired environment.

### Prerequisites
These below commands and script is for the Mac OS only.

You should have the Salesforce CLI (SFDX) installed on your machine. [Link to installation](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_install_cli.htm#sfdx_setup_install_cli)


### Installing
Open command line and navigate to the relevant folder.

Authenticate the desired environment by SFDX with the following command:
```
sfdx force:auth:web:login -a <relevant_org_alias>
```

**Example** : `sfdx force:auth:web:login -a ShriDevOrg`

Verify the authentication by running the following command:
```
sfdx force:org:list
```

---

* Preferably create a folder to run the above script by running this command `mkdir deleteDebugLogs`
* Navigate inside the folder `cd deleteDebugLogs`
* Download the *debugLogDelete.sh* file into this folder.
* Open the file in any text editor and change *ShriDevOrg* to the alias name that you set in the installation step.
* Give the file executable access by this command: `chmod +x debugLogDelete.sh`
* Execute the script by this command: `./debugLogDelete`
* Batch job/s will be created in Salesforce which delete the debug logs.
* You can delete *delDebugLog.csv*.