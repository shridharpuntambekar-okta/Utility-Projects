import json
import requests
import random
import time
import datetime

def sf_api_call(action, parameters = {}, method = 'get', data = {}):
    instance_url = "<insert_org_domain_url>" #https://some--randomname.my.salesforce.com"
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'OAuth <copy_session_id_from_browser_cookie>'#copy the sid cookie. If more than one, then try each.
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters)
    else:
        # other methods not implemented in this example
        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))


if __name__ == '__main__':
	
	call = sf_api_call('/services/data/v47.0/query/?q=SELECT+Id,Name,FolderName,DeveloperName+FROM+Report')
	rows = call.get('records', [])
	next1 = call.get('nextRecordsUrl', None)

	while next1:
		call = sf_api_call(next1)
		rows.extend(call.get('records', []))
		next1 = call.get('nextRecordsUrl', None)

	reportFolderCall = sf_api_call('/services/data/v47.0/query/?q=SELECT+DeveloperName,Id,Name,Type+FROM+Folder+WHERE+Type=\'Report\'')
	
	folderNameToAPI = {}

	for eachFolder in reportFolderCall.get('records'):
		folderNameToAPI[eachFolder.get('Name')] = eachFolder.get('DeveloperName')
	
	#print('foldernames---->'+folderNameToAPI)
	xmlRows = []
	xmlRows.append(r'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
	xmlRows.append(r'<Package xmlns="http://soap.sforce.com/2006/04/metadata">')
	xmlRows.append(r'<types>')
	xmlRows.append(r'<name>Report</name>')
	
	for eachRow in rows:
		foldername = eachRow.get('FolderName')
		if foldername == 'Public Reports':
			foldername = 'unfiled$public'
		else:
			foldernameRet = folderNameToAPI.get(foldername)
			if foldernameRet is None:
				foldername = foldername.replace(' ','_')
			else:
				foldername = foldernameRet

		reportname = eachRow.get('DeveloperName')
		xmlString = f"<members>{foldername}/{reportname}</members>"
		xmlRows.append(xmlString)
	
	xmlRows.append(r'</types>')
	xmlRows.append(r'<version>48.0</version>')
	xmlRows.append(r'</Package>')

	with open('totalReportCount.txt', 'w') as p:
		p.write("%d" % len(xmlRows))

	with open('folderNames.xml', 'w') as f:
		for item in xmlRows:
			f.write("%s\n" % item)


	