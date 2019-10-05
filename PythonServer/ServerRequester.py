import requests
import json

def requester(cmd):
    #print(cmd)

    try:
        if str(cmd) == 'play':
            print('send start')
            url = "http://localhost:3000/gesture"
            data =  {'msg': 'start'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
        elif str(cmd) == 'pause':
            print('send pause')
            url = "http://localhost:3000/gesture"
            data = {'msg': 'pause'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)

    except Exception as e:
        pass