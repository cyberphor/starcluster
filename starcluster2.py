#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    Automates searching Shodan for vulnerable systems within the same postal code. 
'''

# dunders
__author__ = 'Victor Fernandez III'
__version__ = '2.0.0'

# import built-in libraries
import datetime
import glob
import logging
import random
import re
import requests
import string
import sys
import time

# import third-party libraries
import guerrillamail
import shodan

# define global variables
product  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
platform = 'AppleWebKit/537.36 (KHTML, like Gecko) '
extensions = 'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
windows10 = product + platform + extensions
custom_headers = {'user-agent': windows10}
webpage = 'https://account.shodan.io/login'
pattern1 = '<input type="hidden" name="csrf_token" value='
pattern2 = '<li id="api-key-content" style="display:none">'
shodan_home = 'https://www.shodan.io'
shodan_login = 'https://account.shodan.io/login'
shodan_register = 'https://account.shodan.io/register'

# define logging
logging.basicConfig(
    filename = datetime.date.today().isoformat()+'_starcluster.log',
    level = logging.INFO,
    format = '%(asctime)s:%(message)s'
)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
log = logger.info

# check for a valid Shodan API key in starcluster logs
def api_key_check():
    key = 'Using Shodan API key'
    current_directory = glob.glob('./*.log')
    shodan_api_key = 'fails'
    for log in current_directory:
        with open(log) as log_data:
            for log_entry in log_data:
                if key in log_entry:
                    shodan_api_key = log_entry.rstrip()[50:]
    return shodan_api_key

def create_persona():
    try:
        inbox = guerrillamail.GuerrillaMailSession()
        email = inbox.get_session_state()['email_address']
        username = email[:-23]
        chars = string.ascii_letters + string.digits + '!@#$%^&*()?'
        password = ''.join(random.sample(chars,15))
        return inbox, email, username, password
    except:
        print('[x] Failed to contact Guerrilla Mail.')
        exit()

def register_with_shodan():
    inbox, email, username, password = create_persona()
    print('[*] Registering with Shodan...')
    with requests.session() as browser:
        response = browser.get(shodan_register, headers = custom_headers)
        searchme1 = response.text.split('\n')
        matches1 = []
        for line in searchme1:
            if re.findall(pattern1,line):
                matches1.append(line.split('value="')[1].split('" />')[0])
        cookie = matches1[0]
        creds = {
                'username': username, 
                'password': password, 
                'password_confirm': password, 
                'email': email,
                'csrf_token': cookie
        }
        register = browser.post(shodan_register, creds, headers = custom_headers)
    print(' ---> Waiting for confirmation email.')
    counter = 60
    while (len(inbox.get_email_list()) != 2):
        for i in range(10):
            sys.stdout.write(" ---> Giving up in %d/60 seconds." % counter)
            counter = counter - 1
            time.sleep(1)
            sys.stdout.flush()
            sys.stdout.write('\b' * 33)
        if (len(inbox.get_email_list()) == 2):
            sys.stdout.flush()
            sys.stdout.write('\b' * 33)
            print(' ---> You got mail.')
            break
        elif (counter == 0):
            sys.stdout.flush()
            sys.stdout.write('\b' * 33)
            print('[x] Max time exceeded. Exiting!')
            exit()
   
    msg = inbox.get_email(inbox.get_email_list()[0].guid).body
    return inbox, email, username, password, msg

def get_api_key():
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
        return matches2[0]

def find_neighborhood():
    postal_code = '79908'
    print('[*] Launching digital starcluster over: %s' % postal_code)
    return postal_code

def search_neighborhood():
    postal_code = find_neighborhood()
    neighbor_ip = '1.1.1.1'
    neighbor_port = '80'
    print(' ---> Neighbor - %s:%s' % (neighbor_ip, neighbor_port))
    print('[+] Done!')

def main():
    if api_key_check() == 'fails':
        print('[!] No API key found.')
        register_with_shodan()
    search_neighborhood()

if __name__ == '__main__':
    main()
