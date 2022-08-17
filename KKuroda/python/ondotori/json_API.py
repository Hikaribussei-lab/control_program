import requests
import json
import time
import sys
import traceback
import psutil

class API():
    def ondotori(self, dev):
        url = "https://api.webstorage.jp/v1/devices/current"
        api_key = "voeknmiivbe4ffk17d0gl2h3t06257su5ei8c0hauo1v5"
        login_id = "tbac1967"
        password = "hikaribussei"
        paylord = {'api-key': api_key, "login-id": login_id, 'login-pass': password}
        header = {'Host': 'api.webstrage.js:443', 'Content-Type': 'application/json', 'X-HTTP-Method-Override': 'GET'}
        try:
            ondotori_list = []
            response = requests.post(url, json.dumps(paylord).encode('utf-8'), headers=header).json()
            ondotori_list.append(response['devices'][dev]['name'])
            ondotori_list.append(response['devices'][dev]['battery'])
            ondotori_list.append(response['devices'][dev]['channel'][0]['value'])
            ondotori_list.append(response['devices'][dev]['channel'][1]['value'])
            return ondotori_list
        except Exception as e:
            print(traceback.print_exc())
