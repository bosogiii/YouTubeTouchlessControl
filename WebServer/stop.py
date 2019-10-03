import requests
import json

if __name__=='__main__':
	url = "http://localhost:3000/gesture"
	data =  {'msg': 'stop'}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post(url, data=json.dumps(data), headers=headers)
