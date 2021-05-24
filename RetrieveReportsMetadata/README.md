## Getting Started

Follow the below steps to get all report metadata from any environment.

### Prerequisites
These below commands and script is for the Mac OS only.

You should have the Salesforce CLI (SFDX) installed on your machine. [Link to installation](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_install_cli.htm#sfdx_setup_install_cli)

You should have Python3 installed on your machine. Also update the Environment variables to access the Python binary with `python3` keyword.

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

* Copy over the `RetrieveReportsMetadata` folder as it is with it's contents.
* Navigate to `GetReportsXML/genReportXML.py`
* Update the `instance_url` variable to your desired org base URL.
* Log in to this desired instance in any browser. After successful login open the browser dev tools and navigate to session cookies.
* Replace `copy_session_id_from_browser_cookie` comment in `headers` JSON variable with the `sid` value from browser cookies.
* Open `retrieveMD.sh` and update line 35 and 45. References of `ShriDevOrg` should be updated be updated with the SFDX alias you want to query.
* Open `retrieveMD.sh` and update the `batchSize` variable. Keep it below < 6500
* Open `offset.txt` and set it as `0, <batch_size_you_entered_before>`

---

### Execution
* Navigate to `GetReportsXML` folder in terminal and enter following commands
`chmod +x retrieveMD.sh`
`source retrieveMD.sh`




