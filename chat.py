import requests
import urllib3
import json
from base64 import b64encode
from time import sleep
import os
import sys
import psutil
from colorama import Fore, Back, Style



gamedirs = [r'C:\Riot Games\League of Legends']

championLock = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

role = input("Role call, input lane: ")

def request(method, path, query='', data=''):
    if not query:
        url = '%s://%s:%s%s' % (protocol, host, port, path)
    else:
        url = '%s://%s:%s%s?%s' % (protocol, host, port, path, query)

    print('%s %s %s' % (method.upper().ljust(7, ' '), url, data))

    fn = getattr(s, method)

    if not data:
        r = fn(url, verify=False, headers=headers)
    else:
        r = fn(url, verify=False, headers=headers, json=data)

    return r

lockfile = None
print('Waiting for League of Legends to start ..')

# Validate path / check that Launcher is started
while not lockfile:
    for gamedir in gamedirs:
        lockpath = r'%s\lockfile' % gamedir

        if not os.path.isfile(lockpath):
            continue

        print('Found running League of Legends, dir', gamedir)
        lockfile = open(r'%s\lockfile' % gamedir, 'r')

# Read the lock file data
lockdata = lockfile.read()
print(lockdata)
lockfile.close()

# Parse the lock data
lock = lockdata.split(':')
procname = lock[0]
pid = lock[1]

protocol = lock[4]
host = '127.0.0.1'
port = lock[2]

username = 'riot'
password = lock[3]

userpass = b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')
headers = { 'Authorization': 'Basic %s' % userpass }
print(headers['Authorization'])
# Create Request session
s = requests.session()

###
# Wait for login
#

# Check if logged in, if not then Wait for login
while True:
    sleep(1)
    r = request('get', '/lol-login/v1/session')

    if r.status_code != 200:
        print(r.status_code)
        continue

    # Login completed, now we can get data
    if r.json()['state'] == 'SUCCEEDED':
        break
    else:
        print(r.json()['state'])

summonerId = r.json()['summonerId']
print(summonerId)

counter = 0

while counter == 0:
    r = request('get', '/lol-gameflow/v1/gameflow-phase')
    phase = r.json()
    print(phase)

    # Pick/lock champion
    if phase == 'ChampSelect':
        r = request('get', '/lol-champ-select/v1/session')
        if r.status_code != 200:
            continue
        
        cs = r.json()
        chatid = cs["chatDetails"]["multiUserChatId"]
        
        #sleep 10 then accept
        while counter <= 2:
            r = request('post', '/lol-chat/v1/conversations/%s/messages' % chatid,'', {'body': role})
            counter += 1
            
    sleep(1)
