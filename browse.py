#!/usr/bin/env python3

import requests
import re

product  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
platform = 'AppleWebKit/537.36 (KHTML, like Gecko) '
extensions = 'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
windows10 = product + platform + extensions
username = ''
password = ''
custom_headers = {'user-agent': windows10}
webpage = 'https://account.shodan.io/login'
pattern1 = '<input type="hidden" name="csrf_token" value='
pattern2 = '<li id="api-key-content" style="display:none">'

def get_shodan_api_key():
    with requests.session() as browser:
        response = browser.get(webpage, headers = custom_headers)
        searchme1 = response.text.split('\n')
        matches1 = []
        for line in searchme1:
            if re.findall(pattern1,line):
                matches1.append(line.split('value="')[1].split('" />')[0])
        cookie = matches1[0]
        creds = {'username': username, 'password': password, 'csrf_token': cookie}
        login = browser.post(webpage, creds, headers = custom_headers)
        searchme2 = login.text.split('\n')
        matches2 = []
        for line in searchme2:
            if re.findall(pattern2,line):
                matches2.append(line.split('API Key: ')[1].split('</li>')[0])
        print(matches2[0])

get_shodan_api_key()
