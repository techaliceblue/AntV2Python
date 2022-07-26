import hashlib
import requests
import json


BASEURL = 'https://a3.aliceblueonline.com/rest/AliceBlueAPIService'

def get_session(client_key,api_key):
    url = BASEURL+"/api/customer/getAPIEncpkey"

    payload = json.dumps({
        "userId": client_key
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.json()
    if 'encKey' in data and data['encKey']:
        encKey=data['encKey']
        url = BASEURL+"/api/customer/getUserSID"
        key=client_key+api_key+encKey
        hash=hashlib.sha256(key.encode('utf-8')).hexdigest()
        payload = json.dumps({
            "userId": client_key,
            "userData": hash
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        return response.json()
    else:
        return response.json()

def invalid_sess(client_key,session_ID):
    url = BASEURL+'/api/ws/invalidateSocketSess'
    headers = {
        'Authorization': 'Bearer '+client_key+' '+session_ID,
        'Content-Type': 'application/json'
    }
    payload = {"loginType": "API"}
    datas = json.dumps(payload)
    response = requests.request("POST", url, headers=headers,data=datas)
    # print(response.text)
    return response.json()

def createSession(client_key,session_ID):
    url = BASEURL+'/api/ws/createSocketSess'

    headers = {
        'Authorization': 'Bearer '+client_key+' '+session_ID,
        'Content-Type': 'application/json'
    }
    payload = {"loginType": "API"}
    datas = json.dumps(payload)
    response = requests.request("POST", url, headers=headers,data=datas)

    # print(response.text)
    return response.json()

