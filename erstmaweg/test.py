import os
import time
import requests
import urllib.request
import json
version_url = "http://ddragon.leagueoflegends.com/api/versions.json"
response = urllib.request.urlopen(version_url)
data = json.loads(response.read())
current_version = data[0]
print(current_version)





import os
import time

# The path to the two Python files
file1_path = "path/to/file1.py"
file2_path = "path/to/file2.py"

# The URL of the game version file
version_url = "http://ddragon.leagueoflegends.com/api/versions.json"

# The time interval (in seconds) between version checks
check_interval = 60 * 60 # 1 hour

# The current and previous game versions
current_version = ""
previous_version = ""

# The main loop
while True:
    # Check the current game version
    response = urllib.request.urlopen(version_url)
    data = json.loads(response.read())
    current_version = data[0]

    # If the game version has changed, run the corresponding Python file
    if current_version != previous_version:
        if current_version == "13.7":
            os.system("python " + file2_path)
        else:
            os.system("python " + file1_path)

        # Update the previous game version
        previous_version = current_version

    # Wait for the next version check
    time.sleep(check_interval)
