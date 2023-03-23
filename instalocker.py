###############################################################################
# League of Legends (LCU API) script
#
# Auto accept matchmaking
# Automatic/instant pick champion
# Automatic/instant lock champion
# Set High process priority
#
# Usage:
# python lcu-mm-auto-accept-auto-lock-champion.py "Jax" "Xayah"
# 
# Edit the "championsPrio" list below to the champions you want.
# Champion names passed as arguments get highest priority.
#	
# Built on Python 3.x
# Dependencies: requests, colorama
# champion id on http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion.json change version for current.
import requests
import urllib3
import json
from base64 import b64encode
from time import sleep
import os
import sys
import psutil
from colorama import Fore, Back, Style

# Set to your game directory (where LeagueClient.exe is)
gamedirs = [r'C:\Riot Games\League of Legends']

# Set to True to auto lock in the champion selection
championLock = False

# List of the champion ID's you want to play as
#  order by preference; script tries to pick the first one first
#  If empty, does not pick champion, just accepts matchmaking
championsPrio = [
    902, # Poppy
    63, # Brand
    22, # Ashe
    92, # Riven
    122, # Darius
]

# Set to True to stop script when match starts
stopWhenMatchStarts = True

###############################################################################
champions = {"1":"Annie","2":"Olaf","3":"Galio","4":"Twisted Fate","5":"Xin Zhao","6":"Urgot","7":"LeBlanc","8":"Vladimir","9":"Fiddlesticks","10":"Kayle","11":"Master Yi","12":"Alistar","13":"Ryze","14":"Sion","15":"Sivir","16":"Soraka","17":"Teemo","18":"Tristana","19":"Warwick","20":"Nunu","21":"Miss Fortune","22":"Ashe","23":"Tryndamere","24":"Jax","25":"Morgana","26":"Zilean","27":"Singed","28":"Evelynn","29":"Twitch","30":"Karthus","31":"Cho\'Gath","32":"Amumu","33":"Rammus","34":"Anivia","35":"Shaco","36":"Dr. Mundo","37":"Sona","38":"Kassadin","39":"Irelia","40":"Janna","41":"Gangplank","42":"Corki","43":"Karma","44":"Taric","45":"Veigar","48":"Trundle","50":"Swain","51":"Caitlyn","53":"Blitzcrank","54":"Malphite","55":"Katarina","56":"Nocturne","57":"Maokai","58":"Renekton","59":"Jarvan IV","60":"Elise","61":"Orianna","62":"Wukong","63":"Brand","64":"Lee Sin","67":"Vayne","68":"Rumble","69":"Cassiopeia","72":"Skarner","74":"Heimerdinger","75":"Nasus","76":"Nidalee","77":"Udyr","78":"Poppy","79":"Gragas","80":"Pantheon","81":"Ezreal","82":"Mordekaiser","83":"Yorick","84":"Akali","85":"Kennen","86":"Garen","89":"Leona","90":"Malzahar","91":"Talon","92":"Riven","96":"Kog\'Maw","98":"Shen","99":"Lux","101":"Xerath","102":"Shyvana","103":"Ahri","104":"Graves","105":"Fizz","106":"Volibear","107":"Rengar","110":"Varus","111":"Nautilus","112":"Viktor","113":"Sejuani","114":"Fiora","115":"Ziggs","117":"Lulu","119":"Draven","120":"Hecarim","121":"Kha\'Zix","122":"Darius","126":"Jayce","127":"Lissandra","131":"Diana","133":"Quinn","134":"Syndra","136":"Aurelion Sol","141":"Kayn","142":"Zoe","143":"Zyra","145":"Kai\'Sa","150":"Gnar","154":"Zac","157":"Yasuo","161":"Vel\'Koz","163":"Taliyah","164":"Camille","201":"Braum","202":"Jhin","203":"Kindred","222":"Jinx","223":"Tahm Kench","236":"Lucian","238":"Zed","240":"Kled","245":"Ekko","254":"Vi","266":"Aatrox","267":"Nami","268":"Azir","412":"Thresh","420":"Illaoi","421":"Rek\'Sai","427":"Ivern","429":"Kalista","432":"Bard","497":"Rakan","498":"Xayah","516":"Ornn","555":"Pyke","902":"Milio"} # ,"-1":"None"}
championNames = {"Annie":"1","Olaf":"2","Galio":"3","Twisted Fate":"4","Xin Zhao":"5","Urgot":"6","LeBlanc":"7","Vladimir":"8","Fiddlesticks":"9","Kayle":"10","Master Yi":"11","Alistar":"12","Ryze":"13","Sion":"14","Sivir":"15","Soraka":"16","Teemo":"17","Tristana":"18","Warwick":"19","Nunu":"20","Miss Fortune":"21","Ashe":"22","Tryndamere":"23","Jax":"24","Morgana":"25","Zilean":"26","Singed":"27","Evelynn":"28","Twitch":"29","Karthus":"30","Cho\'Gath":"31","Amumu":"32","Rammus":"33","Anivia":"34","Shaco":"35","Dr. Mundo":"36","Sona":"37","Kassadin":"38","Irelia":"39","Janna":"40","Gangplank":"41","Corki":"42","Karma":"43","Taric":"44","Veigar":"45","Trundle":"48","Swain":"50","Caitlyn":"51","Blitzcrank":"53","Malphite":"54","Katarina":"55","Nocturne":"56","Maokai":"57","Renekton":"58","Jarvan IV":"59","Elise":"60","Orianna":"61","Wukong":"62","Brand":"63","Lee Sin":"64","Vayne":"67","Rumble":"68","Cassiopeia":"69","Skarner":"72","Heimerdinger":"74","Nasus":"75","Nidalee":"76","Udyr":"77","Poppy":"78","Gragas":"79","Pantheon":"80","Ezreal":"81","Mordekaiser":"82","Yorick":"83","Akali":"84","Kennen":"85","Garen":"86","Leona":"89","Malzahar":"90","Talon":"91","Riven":"92","Kog\'Maw":"96","Shen":"98","Lux":"99","Xerath":"101","Shyvana":"102","Ahri":"103","Graves":"104","Fizz":"105","Volibear":"106","Rengar":"107","Varus":"110","Nautilus":"111","Viktor":"112","Sejuani":"113","Fiora":"114","Ziggs":"115","Lulu":"117","Draven":"119","Hecarim":"120","Kha\'Zix":"121","Darius":"122","Jayce":"126","Lissandra":"127","Diana":"131","Quinn":"133","Syndra":"134","Aurelion Sol":"136","Kayn":"141","Zoe":"142","Zyra":"143","Kai\'Sa":"145","Gnar":"150","Zac":"154","Yasuo":"157","Vel\'Koz":"161","Taliyah":"163","Camille":"164","Braum":"201","Jhin":"202","Kindred":"203","Jinx":"222","Tahm Kench":"223","Lucian":"236","Zed":"238","Kled":"240","Ekko":"245","Vi":"254","Aatrox":"266","Nami":"267","Azir":"268","Thresh":"412","Illaoi":"420","Rek\'Sai":"421","Ivern":"427","Kalista":"429","Bard":"432","Rakan":"497","Xayah":"498","Ornn":"516","Pyke":"555", "Milio":"902"}
championIds = []

for champion in champions:
    championIds.append(int(champion))

for argv in reversed(sys.argv[1:]):
    for champion in champions:
        if champions[champion] == argv:
            if argv in championNames:
                championsPrio.insert(0, int(champion))
            else:
                print(Back.RED + Fore.WHITE + 'Invalid champion', argv, Style.RESET_ALL)
                exit()
            break

priostr = []

for champion in championsPrio:
    if champion not in championIds:
        print(Back.RED + Fore.WHITE + 'Invalid champion ID', champion, Style.RESET_ALL)
        exit()

    priostr.append('%s (%d)' % (champions[str(champion)], champion))

print('Pick priority: %s ..' % (', '.join(priostr)))

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

###
# Prepare Requests
#

# Prepare basic authorization header
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

###
# Get available champions
#

championsOwned = []
championsOwnedIds = []
while not championsOwned or len(championsOwned) < 1:
    sleep(1)

    r = request('get', '/lol-champions/v1/owned-champions-minimal')

    if r.status_code != 200:
        continue

    championsOwned = r.json()

for champion in championsOwned:
    if not champion['active']:
        continue
    championsOwnedIds.append(champion['id'])

prios = []
for championId in championsPrio:
    if championId not in championsOwnedIds:
        pass
    else:
        prios.append(championId)
championsPrio = prios

picks = []
for championId in championsPrio:
    picks.append(champions[str(championId)])
pickstr = ' or '.join(picks)

if championLock:
    print('Will try to pick', pickstr, '..')
else:
    print('Will try to lock-in', pickstr, '..')

championIdx = 0

###
# Main worker loop
#

setPriority = False

while True:
    if championIdx >= len(championsPrio):
        championIdx = 0

    r = request('get', '/lol-gameflow/v1/gameflow-phase')

    if r.status_code != 200:
        print(Back.BLACK + Fore.RED + str(r.status_code) + Style.RESET_ALL, r.text)
        continue
    print(Back.BLACK + Fore.GREEN + str(r.status_code) + Style.RESET_ALL, r.text)

    phase = r.json()

    if championIdx != 0 and phase != 'ChampSelect':
        championIdx = 0

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

        for member in cs['myTeam']:
            if member['summonerId'] == summonerId:
                actorCellId = member['cellId']

        if actorCellId == -1:
            continue

        for action in cs['actions'][0]:
            if action['actorCellId'] != actorCellId:
                continue

            if action['championId'] == 0:
                championId = championsPrio[championIdx]
                championIdx = championIdx + 1

                url = '/lol-champ-select/v1/session/actions/%d' % action['id']
                data = {'championId': championId}

                championName = champions[str(championId)]
                print('Picking', championName, '(%d)' % championId, '..')

                # Pick champion
                r = request('patch', url, '', data)
                print(r.status_code, r.text)

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
