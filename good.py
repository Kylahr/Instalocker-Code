import requests
import urllib3
import json
from base64 import b64encode
from time import sleep
import os
import sys
import psutil
import urllib.request
from colorama import Fore, Back, Style

champ_name = "Milio"
role = "BOOM"
# todo:
#   implement user input for gamedirs
#   click img for champion selection
#   5 buttons to select role
#   loading for images wait
#   check if u own champion selected

# Set to your game directory (where LeagueClient.exe is)
with open('path.txt', 'r') as file:
    # Read the entire contents of the file into a string
    gamedirs = [file.read()]
    print(gamedirs)

# Set to True to auto lock in the champion selection
championLock = False

# Set to True to stop script when match starts
stopWhenMatchStarts = True

#set to true to wait for 10 seconds to accept match.
#makes the chances to get the role you want higher since you join the lobby first
wait = False
#programm to load img if new version out
img_load = "champimg.py"


#get version
version_url = "http://ddragon.leagueoflegends.com/api/versions.json"
response = urllib.request.urlopen(version_url)
data = json.loads(response.read())
api_version = data[0]

champ_url = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/champion.json" % api_version

# Open the file in read mode ('r')
with open('version.txt', 'r') as file:
    # Read the entire contents of the file into a string
    version = file.read()
    print(version)
    
#Check if version changed and load new images if it did
if api_version != version:
    #os.system("python " + img_load)
    print("updating version and images.")
    #Upadate the version
    with open('version.txt', 'w') as file:
        file.writelines(api_version)
    sleep(10)    
    
###############################################################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Helper function
def request(method, path, query='', data=''):
    if not query:
        url = '%s://%s:%s%s' % (protocol, host, port, path)
    else:
        url = '%s://%s:%s%s?%s' % (protocol, host, port, path, query)

    print('%s %s %s' % (method.upper().ljust(7, ' '), url, data))
    # print(Back.BLACK + Fore.YELLOW + method.upper().ljust(7, ' ') + Style.RESET_ALL + ' ' + url + ' ' + data)

    fn = getattr(s, method)

    if not data:
        r = fn(url, verify=False, headers=headers)
    else:
        r = fn(url, verify=False, headers=headers, json=data)

    return r

###
# Read the lock file to retrieve LCU API credentials
#

lockfile = None
print('Waiting for League of Legends to start ...')

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

###
## Prepare Requests
#


# Prepare basic authorization header
userpass = b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')
headers = { 'Authorization': 'Basic %s' % userpass }
print(headers['Authorization'])
# Create Request session
s = requests.session()

###
## Wait for login
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

###
## Get available champions
#

championsOwned = []
while not championsOwned or len(championsOwned) < 1:
    r = request('get', '/lol-champions/v1/owned-champions-minimal')
    if r.status_code != 200:
        continue

    championsOwned = r.json()

      
owned = []
for champion in championsOwned:
    owned.append(champion["name"])
        
    if not champion['active']:
        continue

    if champion["name"] == champ_name:
        champId = champion['id']

      
while True:
    r = request('get', '/lol-gameflow/v1/gameflow-phase')

    if r.status_code != 200:
        print(Back.BLACK + Fore.RED + str(r.status_code) + Style.RESET_ALL, r.text)
        continue
    print(Back.BLACK + Fore.GREEN + str(r.status_code) + Style.RESET_ALL, r.text)

    phase = r.json()
    if wait:
        sleep(10)
    # Auto accept match
    if phase == 'ReadyCheck':
        r = request('post', '/lol-matchmaking/v1/ready-check/accept')  # '/lol-lobby-team-builder/v1/ready-check/accept')

    # Pick/lock champion
    elif phase == 'ChampSelect':
        r = request('get', '/lol-champ-select/v1/session')
        if r.status_code != 200:
            continue

        cs = r.json()
        actorCellId = -1
        chatid = cs["chatDetails"]["multiUserChatId"]
        for member in cs['myTeam']:
            if member['summonerId'] == summonerId:
                actorCellId = member['cellId']

        if actorCellId == -1:
            continue

        for action in cs['actions'][0]:
            if action['actorCellId'] != actorCellId:
                continue

            if action['championId'] == 0:

                url = '/lol-champ-select/v1/session/actions/%d' % action['id']
                data = {'championId': champId}
                print('Picking', champ_name, '(%d)' % champId, '..')

                # Pick champion
                r = request('patch', url, '', data)
                print(r.status_code, r.text)
                counter = 0
                #call role
                #sleep 10 then accept
                while counter <= 1:
                    r = request('post', '/lol-chat/v1/conversations/%s/messages' % chatid,'', {'body': role})
                    counter += 1


                # Lock champion
                if championLock and action['completed'] == False:
                    r = request('post', url+'/complete', '', data)
                    print(r.status_code, r.text)

    elif phase == 'InProgress':
        if not setPriority:
            for p in psutil.process_iter():
                name, exe, cmdline = '', '', []
                try:
                    name = p.name()
                    cmdline = p.cmdline()
                    exe = p.exe()
                    if p.name() == 'League of Legends.exe' or os.path.basename(p.exe()) == 'League of Legends.exe':
                        nice = p.nice(psutil.HIGH_PRIORITY_CLASS)
                        print('Set high process priority!', nice)
                        break
                except (psutil.AccessDenied, psutil.ZombieProcess):
                    pass
                except psutil.NoSuchProcess:
                    continue
            setPriority = True

        if stopWhenMatchStarts:
            break
        else:
            sleep(9)

    elif phase == 'Matchmaking' or phase == 'Lobby' or phase == 'None':
        setPriority = False

    sleep(1)



