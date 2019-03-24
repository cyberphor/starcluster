#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
    Automates searching Shodan for vulnerable systems within the same postal code. 
'''

# dunders
__author__ = 'Victor Fernandez III'
__version__ = '0.1.0'

# built-in libraries 
import argparse
import datetime
import glob
import itertools
import logging
import string
import sys
import time
import random

# third-party libraries
import guerrillamail
import mechanicalsoup
import shodan

def checkForExistingKey():
    # check local log for existing Shodan API key
    global shodanAPIkey
    key = 'Using Shodan API key'

    for file in glob.glob('./*.log'):
        with open(file) as logFile:
            for logEntry in logFile:
                if key in logEntry:
                    shodanAPIkey = logEntry.rstrip()[50:]
                    if len(shodanAPIkey) == 32:
                        return
                else:
                    shodanAPIkey = ''

def generateEmail():
    # generate email for Shodan account
    global gm
    global email
    global username
    
    try:
        gm = guerrillamail.GuerrillaMailSession()
        email = gm.get_session_state()['email_address']
        username = email[:-23]
    except guerrillamail.GuerrillaMailException:
        log('[!] The GuerrillaMail API might be down...')
        exit()

def generatePassword():
    # generate password for Shodan account
    global password
    characters = string.ascii_letters + string.digits + '!@#$%^&*()?'
    password =  ''.join(random.sample(characters,15))

def registerWithShodan():
    # register for a Shodan account
    generateEmail()
    generatePassword()

    log('[*] Registering with Shodan using the following credentials...')
    log(' +   Email address: '+email)
    log(' +   Username: '+username)
    log(' +   Password: '+password)
    browser.open(shodanRegistrationPage)
    browser.select_form()
    browser['username'] = username
    browser['password'] = password
    browser['password_confirm'] = password
    browser['email'] = email
    browser.submit_selected()

def activateShodanAccount():
    # activate Shodan account using emailed URL
    spinner = itertools.cycle(['|','/', '-', '\\','|'])
    log('[*] Waiting for confirmation email from Shodan. Standby...')
    maxWaitTime = 120
    startTime = time.time()
    while (len(gm.get_email_list()) != 2):
        for i in range(1,10):
            sys.stdout.write(' '+next(spinner)+' ')
            sys.stdout.flush()        
            sys.stdout.write('\b\b\b')
            time.sleep(.5)
        if (len(gm.get_email_list()) == 2):
            sys.stdout.flush()        
            log(' +   Email received.')
            break
        if time.time() > startTime + maxWaitTime:
            sys.stdout.flush()
            log('[!] Max wait time exceeded. Exiting...')
            exit()

    msg = gm.get_email((gm.get_email_list()[0].guid)).body
    soup = mechanicalsoup.form.BeautifulSoup
    activationURL = soup(msg, 'html.parser').find_all('a')[0].string
    browser.open(activationURL)

def getShodanAPIkey():
    # get API key from Shodan account if none found in local log
    global shodanAPIkey
    
    checkForExistingKey()

    if shodanAPIkey:
        log('[+] Using Shodan API key: '+shodanAPIkey)
    else:
        registerWithShodan()
        activateShodanAccount()

        browser.open(shodanLoginPage)
        browser.select_form("form[action='/login']")
        browser['username'] = username
        browser['password'] = password
        browser['continue'] = shodanHomePage
        browser.submit_selected()
        
        log('[*] Retrieving key...')
        shodanAPIkey = browser.get_current_page().find_all('li',{'id':'api-key-content'})[0].string[9:]
        log('[+] Using Shodan API key: '+shodanAPIkey)
    
def findNeighborhood():
    # find neighborhood using online service 
    global postalCode

    browser.open(keyCDN)
    postalCode = browser.get_current_page().find_all('td')[12].string    
    log('[*] Launching digital star-cluster over: '+postalCode)

def searchPostalCode():
    # use Shodan API to search for publicly-accessible devices
    try: 
        shodanAPI = shodan.Shodan(shodanAPIkey)
        neighborhood = shodanAPI.search(postalCode)
    except shodan.exception.APIError as error:
        log('[!] Shodan search failed: '+str(error))
        exit()

    for neighbor in neighborhood['matches']:
        neighborIP = str(neighbor['ip_str'])
        neighborPort = str(neighbor['port'])
        log(' +   Neighbor: '+neighborIP+':'+neighborPort)
    log('[!] Done.')

def main():
    # main script function
    
    # main variables
    global browser
    global keyCDN
    global log
    global postalCode
    global shodanAPIkey
    global shodanHomePage
    global shodanLoginPage
    global shodanRegistrationPage
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')
    keyCDN = 'https://tools.keycdn.com/geo'
    shodanHomePage = 'https://www.shodan.io'
    shodanLoginPage = 'https://account.shodan.io/login'
    shodanRegistrationPage = 'https://account.shodan.io/register'
    
    # script arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', help='Shodan API key')
    parser.add_argument('-p', help='postal code')
    args = parser.parse_args()
    shodanAPIkey = args.a
    postalCode = args.p

    # main logging parameters
    logging.basicConfig(
        filename=datetime.date.today().isoformat()+'_starcluster.log',
        level=logging.INFO,
        format='%(asctime)s:%(message)s'
        )
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    log = logger.info

    # main logic
    if shodanAPIkey and postalCode:
        log('[+] Using Shodan API key: '+str(shodanAPIkey))
        log('[*] Launching digital star-cluster over: '+str(postalCode))
        searchPostalCode()
    elif shodanAPIkey:
        log('[+] Using Shodan API key: '+str(shodanAPIkey))
        findNeighborhood()
        searchPostalCode()
    elif postalCode:
        log('[-] No key provided.')
        getShodanAPIkey()
        log('[*] Launching digital star-cluster over: '+str(postalCode))
        searchPostalCode()
    else:
        log('[-] No key provided.')
        getShodanAPIkey()
        findNeighborhood()
        searchPostalCode()

if __name__ == '__main__':
    main()
