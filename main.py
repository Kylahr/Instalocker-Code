import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import Canvas
import customtkinter
from tkinter import filedialog

import requests
import urllib3
import json
from base64 import b64encode
from time import sleep

import os
import psutil
import urllib.request
from colorama import Fore, Back, Style

root = customtkinter.CTk()
root.title("Instalocker")
root.geometry("1080x720")
 
champ = "Annie" 
 
left_frame = Frame(root, width=300, bg="#1F2937")
left_frame.pack(side=LEFT, fill=Y)

right_frame = Frame(root)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
right_frame.configure(bg="#1F2937")
canvas = Canvas(right_frame, bg="#2a3f5b", highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True, padx= 30, pady = 20)

scrollbar = Scrollbar(right_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def on_mousewheel(event):
    canvas.yview_scroll(-1 * int(event.delta/120), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

def click(i):
    global champ
    champ = name[i]
    print(f"Clicked on image" , champ)
image_folder = "images"
images = []
name = []
for filename in os.listdir(image_folder):
    
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(image_folder, filename)
        image = Image.open(image_path).resize((64, 64))
        images.append(ImageTk.PhotoImage(image))
        name.append(filename[:-4])  
     
row = 0
col = 0

for i, image in enumerate(images):
    x = col*105
    y = row*105
    
    canvas.create_image(x, y, anchor=NW, image=image)
    canvas.create_text(x+32, y+78, text=name[i], anchor="center")
    canvas.create_rectangle(x, y, x + 64, y + 64, width=0, tags=f"image_{i}")
    canvas.tag_bind(f"image_{i}", "<Button-1>", lambda event, index = i: click(index))
 
    if (i+1) % 7 == 0:
        row += 1
        col = 0
    else:
        col += 1
        
def search_images(word):
    search_term = word
    
    if len(search_term.strip()) == 0:
        # display all images again
        canvas.delete("all")
        row = 0
        col = 0
        for i, image in enumerate(images):
            x = col*105
            y = row*105
            
            canvas.create_image(x, y, anchor=NW, image=image)
            canvas.create_text(x+32, y+78, text=name[i], anchor="center")
            canvas.create_rectangle(x, y, x + 64, y + 64, width=0, tags=f"image_{i}")
            canvas.tag_bind(f"image_{i}", "<Button-1>", lambda event, index = i: click(index))
            if (i+1) % 7 == 0:
                row += 1
                col = 0
            else:
                col += 1
    else:
        # display only the matching image
        for i, image_name in enumerate(name):
            if search_term.lower() == image_name.lower():
                canvas.delete("all")
                x = 0
                y = 0
                canvas.create_image(x, y, anchor=NW, image=images[i])
                canvas.create_text(x+32, y+78, text=image_name, anchor="center")
                canvas.create_rectangle(x, y, x + 64, y + 64, width=0, tags=f"image_{i}")
                canvas.tag_bind(f"image_{i}", "<Button-1>", lambda event, index = i: click(index))
                break


def getFolderPath():
    folder_selected = filedialog.askdirectory()
    with open('path.txt', 'w') as file:
        file.writelines(folder_selected)

def launch(champ, role):
    champ_name = champ
    role = role
    print(role)
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
    #if wait ==  "yes":
      #  wait = True
       # print("wait set true")
    #else: 
      #  wait = False
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
        os.system("python " + img_load)
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
                        print("chat")

                    # Lock champion
                    if championLock and action['completed'] == False:
                        r = request('post', url+'/complete', '', data)
                        sleep(0.2)
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

def start():
    # Get the value of the selected role from the OptionMenu
    role = selected.get()
    #wait = wait_for.get()
    # Call the launch function with the selected champion and role
    launch(champ, role)


selected = customtkinter.CTkOptionMenu(master=left_frame, width=200, values=["adc", "sup", "pre bot",
                                                "mid", "jgl", "top"],fg_color="#32926F", button_color="#32926F"
                                                ,button_hover_color="#267055", dropdown_fg_color="#32926F", corner_radius=10
)

selected.pack(pady=12, padx=0)
selected.place(relx=0.5, rely=0.35, anchor=CENTER)

wait_label = customtkinter.CTkLabel(master=left_frame, text="Does nothing", font=("Roboto", 24), text_color="#32926F")
wait_for = customtkinter.CTkOptionMenu(master=left_frame, width=200, values=["yes", "no"],fg_color="#32926F", button_color="#32926F"
                                                ,button_hover_color="#267055", dropdown_fg_color="#32926F", corner_radius=10
)
wait_label.place(relx=0.5, rely=0.4, anchor=CENTER)
wait_for.pack(pady=12, padx=0)
wait_for.place(relx=0.5, rely=0.44, anchor=CENTER)

search_box = Entry(left_frame, fg = "grey",   font=("helvetica", 14), bg="#2a3f5b")
search_box.pack(side=TOP, padx = 20, pady=20)
search_box.bind("<Return>", lambda event: search_images(search_box.get()))
path = customtkinter.CTkButton(master=left_frame, text="Path to lockfile", command= getFolderPath,  fg_color="#32926F", hover_color="#267055")
path.pack(pady=12, padx=10)
path.place(relx=0.5, rely=0.2, anchor=CENTER)

submit_button = customtkinter.CTkButton(master=left_frame, text="Start", command= start,  fg_color="#32926F", hover_color="#267055")
submit_button.pack(pady=12, padx=10)
submit_button.place(relx=0.5, rely=0.95, anchor=CENTER)
 
 
root.mainloop()
