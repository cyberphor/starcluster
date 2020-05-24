#!/usr/bin/env python3

# import built-in libraries
import glob
import string
import random

# import third-party libraries
import guerrillamail as gmail
import mechanicalsoup

# define global variables
browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')

# check for a valid Shodan API key in starcluster logs
def check_for_existing_key():
    key = 'Using Shodan API key'
    current_directory = glob.glob('./*.log')
    for log in current_directory:
        with open(log) as log_data:
            for log_entry in log_data:
                if key in log_entry:
                    shodan_api_key = log_entry.rstrip()[50:]
                    if len(shodan_api_key) == 32:
                        print(shodan_api_key)

def create_password():
    chars = string.ascii_letters + string.digits + '!@#$%^&*()?'
    password = ''.join(random.sample(chars,15))
    return password

def create_persona():
    try:
        inbox = gmail.GuerrillaMailSession()
        email = inbox.get_session_state()['email_address']
        username = email[:-23]
        return email, username, create_password()
    except gmail.GuerrillaMailException as error:
        print('[x] Guerrilla Mail failed: ')
        print(' ---> ' + error)
        exit()

def register_with_shodan():
    email, username, password = create_persona()
    shodan_home = 'https://www.shodan.io'
    shodan_login = 'https://account.shodan.io/login'
    shodan_register = 'https://account.shodan.io/register'

def main():
    check_for_existing_key()
    register_with_shodan()

if __name__ == '__main__':
    main()
